import json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

seed = 42
np.random.seed(seed)

data_dir = Path("data/processed")

# Run 077 final model: pure LR on these 15 features
lr_features = [
    "elo_diff", "home_game", "rest_diff",
    "home_pts_scored_4", "home_pts_scored_8", "home_pts_scored_16",
    "away_pts_scored_4", "away_pts_scored_8", "away_pts_scored_16",
    "home_win_pct_4", "home_win_pct_8", "home_win_pct_16",
    "away_win_pct_4", "away_win_pct_8", "away_win_pct_16",
]


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


def load_all():
    train = pd.read_csv(data_dir / "train.csv")
    val   = pd.read_csv(data_dir / "val.csv")
    test  = pd.read_csv(data_dir / "test.csv")
    train["_split"] = "train"
    val["_split"]   = "val"
    test["_split"]  = "test"
    combined = pd.concat([train, val, test], ignore_index=True)
    combined["game_date"] = pd.to_datetime(combined["game_date"])
    combined = compute_rolling_features(combined)
    train = combined[combined["_split"] == "train"].copy()
    val   = combined[combined["_split"] == "val"].copy()
    test  = combined[combined["_split"] == "test"].copy()
    return train, val, test


def get_X_y(df, feats):
    df = df.dropna(subset=feats + ["home_win"])
    return df[feats].values, df["home_win"].values


if __name__ == "__main__":
    train, val, test = load_all()

    # Retrain on train + val combined (full labeled history before test)
    trainval = pd.concat([train, val], ignore_index=True)
    X_trainval, y_trainval = get_X_y(trainval, lr_features)
    X_test, y_test = get_X_y(test, lr_features)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(C=1.0, max_iter=1000, random_state=seed)),
    ])
    model.fit(X_trainval, y_trainval)

    test_preds = model.predict_proba(X_test)[:, 1]
    test_loss  = log_loss(y_test, test_preds)

    print(f"\n=== Run 077 — Final Test Evaluation ===")
    print(f"Model:        Pure Logistic Regression (C=1.0, L2)")
    print(f"Features:     {len(lr_features)} (lr_features_002)")
    print(f"Train+val:    {len(y_trainval)} games")
    print(f"Test games:   {len(y_test)}")
    print(f"Val log loss: 0.616811  (reported during development)")
    print(f"Test log loss: {test_loss:.6f}")
