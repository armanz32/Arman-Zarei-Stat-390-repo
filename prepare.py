import nfl_data_py as nfl
import pandas as pd
import numpy as np
import os

# constants
first_season = 2004
val_season = 2024
test_season = 2025
windows = [4, 8, 16]
elo_k = 20
elo_init = 1500
seed = 42
out_dir = "data/processed"

#load data
def load_schedules():
    seasons = list(range(first_season, test_season + 1))
    df = nfl.import_schedules(seasons)
    df = df[df["game_type"] == "REG"].copy()
    df = df.dropna(subset=["home_score", "away_score"])
    df["game_date"] = pd.to_datetime(df["gameday"])
    df = df.sort_values("game_date").reset_index(drop=True)
    df["home_win"] = (df["home_score"] > df["away_score"]).astype(int)
    return df

#elo computation
def compute_elo(df):
    elo = {}
    home_elo, away_elo = [], []

    for _, row in df.iterrows():
        h, a = row["home_team"], row["away_team"]
        he = elo.get(h, elo_init)
        ae = elo.get(a, elo_init)
        home_elo.append(he)
        away_elo.append(ae)
        exp_h = 1 / (1 + 10 ** ((ae - he) / 400))
        actual_h = row["home_win"]
        elo[h] = he + elo_k * (actual_h - exp_h)
        elo[a] = ae + elo_k * ((1 - actual_h) - (1 - exp_h))

    df = df.copy()
    df["home_elo"] = home_elo
    df["away_elo"] = away_elo
    df["elo_diff"] = df["home_elo"] - df["away_elo"]
    return df

#misc features
def add_misc_features(df):
    df = df.copy()
    df["home_game"] = 1
    last_game = {}
    home_rest, away_rest = [], []

    for _, row in df.iterrows():
        h, a = row["home_team"], row["away_team"]
        gd = row["game_date"]
        home_rest.append(min((gd - last_game[h]).days, 14) if h in last_game else 7)
        away_rest.append(min((gd - last_game[a]).days, 14) if a in last_game else 7)
        last_game[h] = gd
        last_game[a] = gd

    df["home_rest_days"] = home_rest
    df["away_rest_days"] = away_rest
    df["rest_diff"] = df["home_rest_days"] - df["away_rest_days"]
    return df

#split/save data
def split_and_save(df):
    os.makedirs(out_dir, exist_ok=True)
    train = df[df["season"] < val_season]
    val = df[df["season"] == val_season]
    test = df[df["season"] == test_season]
    train.to_csv(f"{out_dir}/train.csv", index=False)
    val.to_csv(f"{out_dir}/val.csv", index=False)
    test.to_csv(f"{out_dir}/test.csv", index=False)
    print(f"Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")

#main
if __name__ == "__main__":
    print("Loading schedules...")
    df = load_schedules()
    print("Computing ELO...")
    df = compute_elo(df)
    print("Adding features...")
    df = add_misc_features(df)
    print("Saving splits...")
    split_and_save(df)
    print("Done.")