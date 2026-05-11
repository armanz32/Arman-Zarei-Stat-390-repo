import json
import os
import time
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

seed = 42
np.random.seed(seed)

data_dir = Path("data/processed")
results_dir = Path("results/runs")
best_dir = Path("results/best_model")
results_dir.mkdir(parents=True, exist_ok=True)
best_dir.mkdir(parents=True, exist_ok=True)

baseline_features = ["elo_diff", "home_game", "rest_diff"]
rolling_features_011b = [
    "home_pts_scored_4", "home_pts_scored_8", "home_pts_scored_16",
    "home_pts_allowed_4", "home_pts_allowed_8", "home_pts_allowed_16",
    "away_pts_scored_4", "away_pts_scored_8", "away_pts_scored_16",
    "away_pts_allowed_4", "away_pts_allowed_8", "away_pts_allowed_16",
    "home_win_pct_4", "home_win_pct_8", "home_win_pct_16",
    "away_win_pct_4", "away_win_pct_8", "away_win_pct_16",
    "home_rest_days", "away_rest_days",
]
features = baseline_features + rolling_features_011b

model_config = {
    "type": "xgboost",
    "max_depth": 2,
    "learning_rate": 0.05,
}
cv = 5

def compute_rolling_features(df):
    df = df.sort_values("game_date").reset_index(drop=True)
    windows = [4, 8, 16]
    team_history = {}
    records = []
    for _, row in df.iterrows():
        home, away = row["home_team"], row["away_team"]
        rec = {}
        for w in windows:
            for team, prefix in [(home, "home"), (away, "away")]:
                hist = team_history.get(team, {"scored": [], "allowed": [], "wins": []})
                sc = hist["scored"][-w:]
                al = hist["allowed"][-w:]
                wi = hist["wins"][-w:]
                rec[f"{prefix}_pts_scored_{w}"] = sum(sc) / len(sc) if sc else None
                rec[f"{prefix}_pts_allowed_{w}"] = sum(al) / len(al) if al else None
                rec[f"{prefix}_win_pct_{w}"] = sum(wi) / len(wi) if wi else None
        records.append(rec)
        h_won = int(row["home_score"] > row["away_score"])
        for team, scored, allowed, won in [
            (home, row["home_score"], row["away_score"], h_won),
            (away, row["away_score"], row["home_score"], 1 - h_won),
        ]:
            if team not in team_history:
                team_history[team] = {"scored": [], "allowed": [], "wins": []}
            team_history[team]["scored"].append(scored)
            team_history[team]["allowed"].append(allowed)
            team_history[team]["wins"].append(won)
    rolling_df = pd.DataFrame(records, index=df.index)
    df = pd.concat([df, rolling_df], axis=1)
    df = df.fillna(df.median(numeric_only=True))
    return df

#load data
def load_data():
    train = pd.read_csv(data_dir / "train.csv")
    val = pd.read_csv(data_dir / "val.csv")
    train["_split"] = "train"
    val["_split"] = "val"
    combined = pd.concat([train, val], ignore_index=True)
    combined["game_date"] = pd.to_datetime(combined["game_date"])
    combined = compute_rolling_features(combined)
    train = combined[combined["_split"] == "train"].copy()
    val = combined[combined["_split"] == "val"].copy()
    return train, val

def get_X_y(df, feats):
    df = df.dropna(subset=feats + ["home_win"])
    X = df[feats].values
    y = df["home_win"].values
    return X, y

#build model
def build_model(config):
    mtype = config.get("type", "logistic_regression")

    if mtype == "logistic_regression":
        clf = LogisticRegression(
            C=config.get("C", 1.0),
            max_iter=config.get("max_iter", 1000),
            random_state=seed,
        )
        return Pipeline([("scaler", StandardScaler()), ("clf", clf)])

    elif mtype == "xgboost":
        from xgboost import XGBClassifier
        params = {k: v for k, v in config.items() if k != "type"}
        params.setdefault("random_state", seed)
        params.setdefault("eval_metric", "logloss")
        return XGBClassifier(**params)

    elif mtype == "random_forest":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(
            n_estimators=config.get("n_estimators", 200),
            random_state=seed,
        )
    #safety
    else:
        raise ValueError(f"Unknown model type: {mtype}")
    
def train_model(X_train, y_train, config):
    model = build_model(config)

    kf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
    cv_losses = []
    for ti, vi in kf.split(X_train, y_train):
        m = build_model(config)
        m.fit(X_train[ti], y_train[ti])
        preds = m.predict_proba(X_train[vi])[:, 1]
        cv_losses.append(log_loss(y_train[vi], preds))

    cv_mean = np.mean(cv_losses)
    cv_std = np.std(cv_losses)

    model.fit(X_train, y_train)
    return model, cv_mean, cv_std

#log
def get_next_run_id():
    existing = list(results_dir.glob("run_*.json"))
    if not existing:
        return 0
    ids = [int(p.stem.split("_")[1]) for p in existing]
    return max(ids) + 1

def log_result(run_id, val_loss, cv_mean, cv_std, feats, config, runtime):
    record = {
        "run_id": run_id,
        "val_loss": round(val_loss, 6),
        "cv_mean": round(cv_mean, 6),
        "cv_std": round(cv_std, 6),
        "features": feats,
        "config": config,
        "runtime_s": round(runtime, 2),
    }
    path = results_dir / f"run_{run_id:03d}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    print(json.dumps(record, indent=2))

def save_best(model, val_loss, run_id):
    import pickle
    meta_path = best_dir / "best_meta.json"

    if meta_path.exists():
        with open(meta_path) as f:
            best_meta = json.load(f)
        if val_loss >= best_meta["val_loss"]:
            return

    with open(best_dir / "best_model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(meta_path, "w") as f:
        json.dump({"run_id": run_id, "val_loss": round(val_loss, 6)}, f, indent=2)
    print(f"New best model saved (run {run_id}, val_loss={val_loss:.6f})")

#main
if __name__ == "__main__":
    run_id = get_next_run_id()
    print(f"\n=== Run {run_id:03d} | Model: {model_config['type']} | Features: {len(features)} ===\n")

    t0 = time.time()
    train, val = load_data()
    X_train, y_train = get_X_y(train, features)
    X_val, y_val = get_X_y(val, features)

    model, cv_mean, cv_std = train_model(X_train, y_train, model_config)
    val_loss = log_loss(y_val, model.predict_proba(X_val)[:, 1])
    runtime = time.time() - t0

    log_result(run_id, val_loss, cv_mean, cv_std, features, model_config, runtime)
    save_best(model, val_loss, run_id)
    print(f"\nVal log loss: {val_loss:.6f} | CV: {cv_mean:.6f} ± {cv_std:.6f} | Time: {runtime:.1f}s")
