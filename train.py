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

lr_features_002 = [
    "elo_diff", "home_game", "rest_diff",
    "home_pts_scored_4", "home_pts_scored_8", "home_pts_scored_16",
    "away_pts_scored_4", "away_pts_scored_8", "away_pts_scored_16",
    "home_win_pct_4", "home_win_pct_8", "home_win_pct_16",
    "away_win_pct_4", "away_win_pct_8", "away_win_pct_16",
]

model_config = {
    "type": "ensemble",
    "xgb_config": {"type": "xgboost", "max_depth": 2, "learning_rate": 0.05},
    "lr_config": {"type": "logistic_regression"},
    "xgb_weight": 0.0,
    "lr_weight": 1.0,
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
        exclude = {"type", "top_n_features"}
        params = {k: v for k, v in config.items() if k not in exclude}
        params.setdefault("random_state", seed)
        params.setdefault("eval_metric", "logloss")
        return XGBClassifier(**params)

    elif mtype == "lightgbm":
        from lightgbm import LGBMClassifier
        params = {k: v for k, v in config.items() if k != "type"}
        params.setdefault("random_state", seed)
        params.setdefault("verbose", -1)
        return LGBMClassifier(**params)

    elif mtype == "random_forest":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(
            n_estimators=config.get("n_estimators", 200),
            max_depth=config.get("max_depth", None),
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

    if model_config["type"] == "ensemble_weight_search":
        xgb_cfg = model_config["xgb_config"]
        lr_cfg = model_config["lr_config"]
        weight_grid = model_config["weight_grid"]

        X_train_xgb, y_train_xgb = get_X_y(train, features)
        X_val_xgb, _ = get_X_y(val, features)
        X_train_lr, y_train_lr = get_X_y(train, lr_features_002)
        X_val_lr, y_val = get_X_y(val, lr_features_002)

        xgb_model = build_model(xgb_cfg)
        xgb_model.fit(X_train_xgb, y_train_xgb)
        lr_model = build_model(lr_cfg)
        lr_model.fit(X_train_lr, y_train_lr)
        p_xgb_val = xgb_model.predict_proba(X_val_xgb)[:, 1]
        p_lr_val  = lr_model.predict_proba(X_val_lr)[:, 1]

        print("\nWeight grid search results:")
        best_loss, best_w_xgb, best_w_lr = float("inf"), None, None
        for w_xgb, w_lr in weight_grid:
            loss = log_loss(y_val, w_xgb * p_xgb_val + w_lr * p_lr_val)
            print(f"  XGB={w_xgb}, LR={w_lr} -> val_loss={loss:.6f}")
            if loss < best_loss:
                best_loss, best_w_xgb, best_w_lr = loss, w_xgb, w_lr
        print(f"\nBest weights: XGB={best_w_xgb}, LR={best_w_lr} -> val_loss={best_loss:.6f}")

        kf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
        cv_losses = []
        for ti, vi in kf.split(X_train_xgb, y_train_xgb):
            m_xgb = build_model(xgb_cfg)
            m_xgb.fit(X_train_xgb[ti], y_train_xgb[ti])
            m_lr = build_model(lr_cfg)
            m_lr.fit(X_train_lr[ti], y_train_lr[ti])
            p = best_w_xgb * m_xgb.predict_proba(X_train_xgb[vi])[:, 1] + best_w_lr * m_lr.predict_proba(X_train_lr[vi])[:, 1]
            cv_losses.append(log_loss(y_train_xgb[vi], p))
        cv_mean = np.mean(cv_losses)
        cv_std  = np.std(cv_losses)

        val_loss = best_loss
        model = (xgb_model, lr_model)
        model_config = dict(model_config, best_xgb_weight=best_w_xgb, best_lr_weight=best_w_lr)
        active_features = features

    elif model_config["type"] == "ensemble":
        xgb_cfg = model_config["xgb_config"]
        lr_cfg = model_config["lr_config"]
        rf_cfg = model_config.get("rf_config")
        lgbm_cfg = model_config.get("lgbm_config")
        w_xgb = model_config["xgb_weight"]
        w_lr = model_config["lr_weight"]
        w_rf = model_config.get("rf_weight", 0)
        w_lgbm = model_config.get("lgbm_weight", 0)

        X_train_xgb, y_train_xgb = get_X_y(train, features)
        X_val_xgb, _ = get_X_y(val, features)
        X_train_lr, y_train_lr = get_X_y(train, lr_features_002)
        X_val_lr, y_val = get_X_y(val, lr_features_002)

        kf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
        cv_losses = []
        for ti, vi in kf.split(X_train_xgb, y_train_xgb):
            m_xgb = build_model(xgb_cfg)
            m_xgb.fit(X_train_xgb[ti], y_train_xgb[ti])
            m_lr = build_model(lr_cfg)
            m_lr.fit(X_train_lr[ti], y_train_lr[ti])
            p = w_xgb * m_xgb.predict_proba(X_train_xgb[vi])[:, 1] + w_lr * m_lr.predict_proba(X_train_lr[vi])[:, 1]
            if rf_cfg:
                m_rf = build_model(rf_cfg)
                m_rf.fit(X_train_xgb[ti], y_train_xgb[ti])
                p += w_rf * m_rf.predict_proba(X_train_xgb[vi])[:, 1]
            if lgbm_cfg:
                m_lgbm = build_model(lgbm_cfg)
                m_lgbm.fit(X_train_xgb[ti], y_train_xgb[ti])
                p += w_lgbm * m_lgbm.predict_proba(X_train_xgb[vi])[:, 1]
            cv_losses.append(log_loss(y_train_xgb[vi], p))
        cv_mean = np.mean(cv_losses)
        cv_std = np.std(cv_losses)

        xgb_model = build_model(xgb_cfg)
        xgb_model.fit(X_train_xgb, y_train_xgb)
        lr_model = build_model(lr_cfg)
        lr_model.fit(X_train_lr, y_train_lr)
        val_preds = w_xgb * xgb_model.predict_proba(X_val_xgb)[:, 1] + w_lr * lr_model.predict_proba(X_val_lr)[:, 1]
        if rf_cfg:
            rf_model = build_model(rf_cfg)
            rf_model.fit(X_train_xgb, y_train_xgb)
            val_preds += w_rf * rf_model.predict_proba(X_val_xgb)[:, 1]
        if lgbm_cfg:
            lgbm_model = build_model(lgbm_cfg)
            lgbm_model.fit(X_train_xgb, y_train_xgb)
            val_preds += w_lgbm * lgbm_model.predict_proba(X_val_xgb)[:, 1]
        val_loss = log_loss(y_val, val_preds)
        model = (xgb_model, lr_model)
        active_features = features
    else:
        X_train, y_train = get_X_y(train, features)
        X_val, y_val = get_X_y(val, features)

        top_n = model_config.get("top_n_features")
        if top_n:
            probe_cfg = {k: v for k, v in model_config.items() if k != "top_n_features"}
            probe = build_model(probe_cfg)
            probe.fit(X_train, y_train)
            importance_pairs = sorted(zip(features, probe.feature_importances_), key=lambda x: x[1], reverse=True)
            print("\nFeature importances (descending):")
            for fname, fimp in importance_pairs:
                print(f"  {fname}: {fimp:.6f}")
            selected = [f for f, _ in importance_pairs[:top_n]]
            print(f"\nTop {top_n} selected: {selected}\n")
            X_train = X_train[:, [features.index(f) for f in selected]]
            X_val   = X_val[:,   [features.index(f) for f in selected]]
            active_features = selected
        else:
            active_features = features

        model, cv_mean, cv_std = train_model(X_train, y_train, model_config)
        val_loss = log_loss(y_val, model.predict_proba(X_val)[:, 1])

    runtime = time.time() - t0

    log_features = active_features if model_config["type"] != "ensemble" else features
    log_result(run_id, val_loss, cv_mean, cv_std, log_features, model_config, runtime)
    save_best(model, val_loss, run_id)
    print(f"\nVal log loss: {val_loss:.6f} | CV: {cv_mean:.6f} ± {cv_std:.6f} | Time: {runtime:.1f}s")
