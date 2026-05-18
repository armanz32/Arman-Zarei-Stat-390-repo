You are an AutoResearch agent. Your job is to iteratively improve an NFL game prediction model by making one controlled change per run, evaluating it, and deciding whether to keep it. You are NOT a general assistant. You do not answer questions. You do not explain things. You execute the loop below and nothing else.

What You Are Allowed To Do:

Read any file in this repo
Edit train.py
Append rows to evaluation_board.md
Append entries to failure_log.md
Append entries to the Iteration Log at the bottom of this file

What You Are Never Allowed To Do

Modify prepare.py
Change the train/val/test split logic
Touch any file in data/processed/ directly
Load or evaluate on the 2025 test set
Change the acceptance threshold defined below
Change the metric being optimized
Edit previous rows in evaluation_board.md or the Iteration Log

If you are unsure whether an action is allowed, do not take it. Log the ambiguity in failure_log.md and stop.

Metric & Acceptance Rule
Metric: Log loss on the 2024 validation season (produced by train.py)
Acceptance threshold: A change is accepted only if: new_val_log_loss < current_best_val_log_loss * 0.9975
This means a minimum 0.25% improvement is required. Improvements smaller than 0.25% are discarded even if positive.

The Loop (execute exactly in this order)
Step 1 — Read the queue: Read the next unchecked item in the Experiment Queue below. Do not skip items or reorder them.

Step 2 — Make exactly one change: Edit train.py to implement that item and nothing else. Do not bundle multiple queue items into one run.
Step 3 — Run the experiment; python train.py
Record the val log loss and CV mean ± std printed to stdout.

Step 4 — Evaluate: Compare new_val_log_loss against current_best_val_log_loss * 0.9975.
If accepted: Update "Current best val log loss" above. Save the model checkpoint to results/best_model/. Mark the queue item ✅.
If rejected: Revert train.py to its previous state (the accepted version). Mark the queue item ❌. Log the failure in failure_log.md.

Step 5 — Log the result
Append one row to evaluation_board.md and one entry to the Iteration Log at the bottom of this file.

Step 6 — Stop
Do not proceed to the next queue item automatically. Wait for the human operator to confirm before beginning the next run.

Reproducibility Rules:
train.py must set random_state=42  on every stochastic component.
Every run must produce the same val log loss if re-run with no code changes.
If a run is not reproducible, reject it and log the reason.

Experiemnt Queue
❌ 001: Add Group C features: rolling win % over last 4, 8, 16 games
❌ 002: Add Groups A + B + C together 
❌ 003: Switch model to XGBoost, keep Groups A + B + C
❌ 004: Tune XGBoost: grid search over max_depth ∈ {3,5,7}, n_estimators ∈ {100,300}
❌ 005: Add elo_diff × home_win_pct_8 interaction term
❌ 006: Add elo_diff² (squared ELO diff)
❌ 007: rest_diff × away_score_avg_8 interaction
❌ 008: Bin elo_diff into 5 ordinal categories
❌ 009: Add elo_diff² (squared ELO diff)
❌ 010: Drop rest_diff entirely

Week 5 Experiment Block:
Goal: Explore XGBoost as a replacement model and tune hyperparameters
Threshold: 0.25% better than the baseline
011: Swap model to XGBoost, all default params, keep current feature set
011b: Add rolling scoring: home/away_pts_scored/allowed_4/8/16, rolling win%: home/away_win_pct_4/8/16, and rest detail: home_rest_days, away_rest_days features
012: Set max_depth = 2
013: Set max_depth = 4
014: Set max_depth = 6
015: Set n_estimators = 100
016: Set n_estimators = 300
017: Set n_estimators = 500
018: Set learning_rate = 0.01
019: Set learning_rate = 0.05
020: Set learning_rate = 0.3
021: Set subsample = 0.6
022: Set subsample = 0.8
023: Set colsample_bytree = 0.6
024: Set colsample_bytree = 0.8
025: Set min_child_weight = 2
026: Set min_child_weight = 5
027: Set reg_lambda = 1
028: Set reg_lambda = 5
029: Set reg_alpha = 0.1
030: Set reg_alpha = 1.0
031: Set n_estimators=200
032: Set n_estimators=150
032: Set n_estimators=75
034: Set max_depth=3, lr=0.05
035: Set lr=0.03
036: Set lr=0.07
037: Set lr=0.02
038: Set min_child_weight=3
039: Set min_child_weight=4
040: Set subsample=0.7
041: Remove all window-16 features (keep only 4 and 8 game windows)
042: Remove all window-4 features (keep only 8 and 16 game windows)
043: Remove pts_allowed features (keep only pts_scored and win_pct)
044: Remove pts_scored features (keep only pts_allowed and win_pct)
045: Remove all scoring features, keep only win_pct + baseline
046: Remove away rolling features entirely
047: Remove home rolling features entirely
048: Remove rest_days features
049: Keep only baseline + win_pct_8
050: Keep only baseline + pts_scored_8 + pts_allowed_8
051: Remove window-16 features + set min_child_weight=4
052: Remove window-16 features + remove pts_allowed features
053: Remove pts_allowed features + set min_child_weight=4
054: Remove window-16 features + remove pts_allowed features + set min_child_weight=4
055: Remove window-16 features + set colsample_bytree=0.6
056: Remove window-16 features + remove rest_days features
057: Remove window-16 features + remove pts_allowed features + remove rest_days features
058: Remove pts_allowed features + set colsample_bytree=0.6
059: Remove window-16 features + remove pts_allowed features + set min_child_weight=4 + set colsample_bytree=0.6
060: Remove window-16 features + remove pts_allowed features + set min_child_weight=4 + remove rest_days features

Week 6 Experiment Block:
❌ 061: Add early_stopping_rounds=10, n_estimators=500, eval_set=[(X_val, y_val)] to Run 019 config (max_depth=2, lr=0.05)
❌ 062: Same as 061 but set learning_rate=0.03
❌ 063: Add 32-game rolling win% (home + away) to Run 019 config (23+2 features)
❌ 064: Add 32-game rolling pts scored/allowed (home + away) to Run 019 config (23+4 features)
❌ 065: Add all 32-game rolling features (win%, pts scored, pts allowed — home + away) to Run 019 config (27 features)
✅ 066: Ensemble — average predictions of Run 019 (XGBoost) and Run 002 (Logistic Regression) with equal weights (0.5/0.5)
❌ 067: Ensemble — average predictions of Run 019 (XGBoost) and Run 002 (Logistic Regression) with weights (0.35 XGB / 0.65 LR)
❌ 068: Swap model to LightGBM, same 23 features, equivalent config (max_depth=2, learning_rate=0.05, n_estimators=100)
❌ 069: Swap model to Random Forest, same 23 features (n_estimators=300, max_depth=6)
❌ 070: Take best result from runs 061-069 and add colsample_bytree=0.6 on top of it
❌ 071: Use XGBoost Run 019 config, keep only top 10 features by feature_importances_ (log importances first, then retrain)
❌ 072: Use XGBoost Run 019 config, keep only top 15 features by feature_importances_
❌ 073: Ensemble Run 019 (XGBoost) + Run 002 (LR) + Run 069 (Random Forest), equal weights (0.33 each)
❌ 074: Ensemble Run 019 (XGBoost) + Run 002 (LR) + LightGBM (Run 068 result), equal weights
❌ 075: Grid search ensemble weights for run 066 (try 0.4/0.6, 0.3/0.7, 0.6/0.4) and take best
❌ 076: Ensemble Run 019 (XGBoost) + Run 002 (LR) with weights 0.2 XGB / 0.8 LR
✅ 077: Ensemble Run 019 (XGBoost) + Run 002 (LR) with weights 0.0 XGB / 1.0 LR (pure LR)

Iteration Log
Append one entry per run. Do not edit previous entries.

Prepend entries to failure_log.md — new entries must always be appended to the BOTTOM of the file

Run 000 — Baseline
Date: [4/19/2026]
Change: Baseline — logistic regression, features: ELO diff, home indicator, rest diff
Val log loss: [0.623589]
CV mean ± std: [0.648181] ± [0.005565]
Accepted: Yes (baseline)
Notes: Starting point. All future runs are measured against this.

Run 001 — Group C: rolling win % (last 4, 8, 16 games)
Date: [4/26/2026]
Change: Added home_win_pct_4/8/16 and away_win_pct_4/8/16 computed in-memory from game history (no data leakage via shift(1)).
Val log loss: [0.619831]
CV mean ± std: [0.637591] ± [0.006189]
Accepted: No
Notes: Improvement of ~0.60% (0.623589 → 0.619831) falls below the 1.5% required threshold (0.614135). train.py reverted to baseline.

Run 002 — Groups A + B + C (baseline + rolling scoring avg + rolling win %)
Date: [4/26/2026]
Change: Added Group B (home/away_score_avg_4/8/16) and Group C (home/away_win_pct_4/8/16) on top of baseline. 15 features total. Groups A+B+C definition clarified by human operator before run.
Val log loss: [0.616790]
CV mean ± std: [0.633451] ± [0.004513]
Accepted: No
Notes: Improvement of ~1.09% (0.623589 → 0.616790) falls below the 1.5% required threshold (0.614135). train.py reverted to baseline.

Run 003 — XGBoost, Groups A + B + C
Date: [4/26/2026]
Change: Switched model from logistic regression to XGBoost (n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42). Same 15 features as Run 002.
Val log loss: [0.628627]
CV mean ± std: [0.653370] ± [0.007373]
Accepted: No
Notes: Regression — XGBoost (0.628627) is worse than the baseline (0.623589). train.py reverted to baseline.

Run 004 — XGBoost grid search (max_depth ∈ {3,5,7}, n_estimators ∈ {100,300}), Groups A+B+C
Date: [4/26/2026]
Change: Grid search over 6 XGBoost hyperparameter combos selected by CV. Best: max_depth=3, n_estimators=100 (CV=0.640998). Same 15 features as Run 002/003.
Val log loss: [0.619820]
CV mean ± std: [0.640998] ± [0.004798]
Accepted: No
Notes: Best XGBoost config (depth=3, trees=100) achieves 0.60% improvement over baseline — identical to logistic regression with rolling features (Run 001: 0.619831). Below the 1.5% threshold. Shallower/fewer trees consistently outperform deeper/more trees. train.py reverted to baseline.

Run 005 — elo_diff × home_win_pct_8 interaction term
Date: [5/4/2026]
Change: Added elo_diff_x_home_win_pct_8 = elo_diff * home_win_pct_8 as a 13th feature. Model: logistic regression. Base feature set: Groups A+B (baseline + rolling scoring avg + home win pct 4/8/16).
Val log loss: [0.623928]
CV mean ± std: [0.640814] ± [0.007667]
Accepted: No
Notes: Regression — interaction term made performance worse (0.623928 > 0.623589 baseline). elo_diff × home_win_pct_8 provides no additive signal over the existing individual features; may introduce collinearity. train.py reverted to pre-Run-005 state.

Run 006 — elo_diff² (squared ELO diff)
Date: [5/4/2026]
Change: Added elo_diff_sq = elo_diff ** 2 as a 13th feature. Model: logistic regression. Base feature set: baseline + rolling scoring avg + home win pct 4/8/16.
Val log loss: [0.622981]
CV mean ± std: [0.640554] ± [0.007697]
Accepted: No
Notes: Tiny improvement of ~0.10% (0.623589 → 0.622981) — below the 1.5% threshold (0.614135). The quadratic ELO term adds marginal signal but not enough to cross the bar. train.py reverted. best_meta.json restored to run_0 (0.623589).

Run 007 — rest_diff × away_score_avg_8 interaction
Date: [5/4/2026]
Change: Added rest_diff_x_away_score_avg_8 = rest_diff * away_score_avg_8 as a 13th feature. Model: logistic regression. Base feature set: baseline + rolling scoring avg + home win pct 4/8/16.
Val log loss: [0.624205]
CV mean ± std: [0.641083] ± [0.008146]
Accepted: No
Notes: Regression — 0.624205 > 0.623589 (baseline). The rest/scoring interaction hurts performance. train.py reverted to pre-Run-007 state. best_meta.json unchanged (save_best correctly skipped).

Run 008 — Bin elo_diff into 5 ordinal categories
Date: [5/4/2026]
Change: Added elo_diff_bin as a 13th feature — 5 quantile bins computed on training data, applied to val with fixed edges (-inf/+inf clipped). Model: logistic regression. Base feature set: baseline + rolling scoring avg + home win pct 4/8/16.
Val log loss: [0.625514]
CV mean ± std: [0.640376] ± [0.007937]
Accepted: No
Notes: Regression — 0.625514 > 0.623589 (baseline). Discretizing ELO diff loses continuous signal; the ordinal bin alongside the raw elo_diff feature introduces redundancy that hurts more than it helps. train.py reverted to pre-Run-008 state. best_meta.json unchanged (save_best correctly skipped).

Run 009 — elo_diff² (squared ELO diff), true baseline
Date: [5/4/2026]
Change: Added elo_diff_sq = elo_diff ** 2 as a 4th feature on top of the true 3-feature baseline (elo_diff, home_game, rest_diff).
Val log loss: [0.622191]
CV mean ± std: [0.647926] ± [0.005452]
Accepted: No
Notes: Improvement of ~0.22% (0.623589 → 0.622191) — below the 1.5% threshold (0.614135). Better than Run 006 (0.622981), which tested the same feature on top of 12 features. Squared ELO adds marginal signal but not enough to clear the bar. train.py reverted to true baseline. best_meta.json restored to run_0 (0.623589).

Run 010 — Drop rest_diff entirely
Date: [5/4/2026]
Change: Removed rest_diff from features, leaving only elo_diff and home_game (2 features).
Val log loss: [0.622446]
CV mean ± std: [0.648547] ± [0.006189]
Accepted: No
Notes: Improvement of ~0.18% (0.623589 → 0.622446) — below the 1.5% threshold (0.614135). Dropping rest_diff marginally helps, suggesting it adds slight noise, but the gain is well below the bar. train.py reverted to 3-feature baseline. best_meta.json restored to run_0 (0.623589).

Run 011 — XGBoost, all default parameters, 3-feature baseline
Date: [5/11/2026]
Change: Swapped model from logistic regression to XGBoost with all default parameters (random_state=42, eval_metric=logloss). Features unchanged: elo_diff, home_game, rest_diff.
Val log loss: [0.665846]
CV mean ± std: [0.697022] ± [0.009262]
Accepted: Yes (required Week 5 XGBoost baseline — accepted regardless of threshold)
Notes: Regression — XGBoost defaults (0.665846) are substantially worse than baseline logistic regression (0.623589), +6.78%. Default XGBoost (n_estimators=100, max_depth=6, learning_rate=0.3) overfits on only 3 features. Change retained as mandated Week 5 baseline; subsequent runs will tune hyperparameters.

Run 011b — XGBoost, all default parameters, full 23-feature set
Date: [5/11/2026]
Change: Kept XGBoost with all default parameters. Expanded features from 3 to 23: added rolling pts scored/allowed (home/away, windows 4/8/16), rolling win% (home/away, windows 4/8/16), and home_rest_days/away_rest_days. Rolling features computed in-memory on combined train+val sorted by game_date to avoid leakage at season boundary.
Val log loss: [0.702775]
CV mean ± std: [0.767613] ± [0.022218]
Accepted: Yes (required full-feature Week 5 baseline — accepted regardless of threshold)
Notes: Further regression — XGBoost defaults with 23 features (0.702775) are worse than Run 011 (0.665846, +5.56%) and substantially worse than baseline logistic regression (0.623589, +12.70%). High CV std (0.022) indicates instability. Default XGBoost severely overfits on the expanded feature set. Retained as mandated full-feature Week 5 baseline; hyperparameter tuning runs (012–030) will attempt to recover.

Run 012 — XGBoost max_depth=2, 23-feature set
Date: [5/11/2026]
Change: Set max_depth=2 in XGBoost model_config. All other settings unchanged (23 features, all other params default).
Val log loss: [0.647696]
CV mean ± std: [0.649534] ± [0.010045]
Accepted: Yes (7.84% improvement vs Week 5 block baseline 011b: 0.702775 → 0.647696; threshold 0.701019)
Notes: Shallower trees dramatically reduce overfitting — CV std drops from 0.022 to 0.010 and val loss improves by 7.84% vs 011b. Still above the overall logistic regression best (0.623589) but accepted per Week 5 block decision rule. New block best: 0.647696.

Run 013 — XGBoost max_depth=4, 23-feature set
Date: [5/11/2026]
Change: Set max_depth=4 in XGBoost model_config. All other settings unchanged (23 features, all other params default).
Val log loss: [0.676621]
CV mean ± std: [0.695058] ± [0.015476]
Accepted: No
Notes: Regression vs Run 012 (0.647696 → 0.676621, +4.47%). Deeper trees re-introduce overfitting — CV std rises from 0.010 to 0.015. max_depth=4 is worse than max_depth=2 on this feature set. train.py reverted to Run 012 state (max_depth=2).

Run 014 — XGBoost max_depth=6, 23-feature set
Date: [5/11/2026]
Change: Set max_depth=6 in XGBoost model_config. All other settings unchanged (23 features, all other params default).
Val log loss: [0.702775]
CV mean ± std: [0.767613] ± [0.022218]
Accepted: No
Notes: Identical result to Run 011b (0.702775) — XGBoost's default max_depth is 6, so this is the same configuration. Confirmed that max_depth=6 is the worst setting tested; max_depth=2 (Run 012) is the current block best. train.py reverted to Run 012 state (max_depth=2).

Run 015 — XGBoost max_depth=2, n_estimators=100
Date: [5/11/2026]
Change: Set n_estimators=100 explicitly. All other settings: max_depth=2, 23 features, other params default.
Val log loss: [0.647696]
CV mean ± std: [0.649534] ± [0.010045]
Accepted: No
Notes: Identical result to Run 012 — n_estimators=100 is the XGBoost default, so no change was actually made. train.py reverted to Run 012 state (max_depth=2, no explicit n_estimators).

Run 016 — XGBoost max_depth=2, n_estimators=300
Date: [5/11/2026]
Change: Set n_estimators=300. All other settings: max_depth=2, 23 features, other params default.
Val log loss: [0.663226]
CV mean ± std: [0.674836] ± [0.013239]
Accepted: No
Notes: Regression vs Run 012 (+2.39%). More trees with depth=2 overfit — CV std rises from 0.010 to 0.013. train.py reverted to Run 012 state (max_depth=2).

Run 017 — XGBoost max_depth=2, n_estimators=500
Date: [5/11/2026]
Change: Set n_estimators=500. All other settings: max_depth=2, 23 features, other params default.
Val log loss: [0.687740]
CV mean ± std: [0.701497] ± [0.016145]
Accepted: No
Notes: Regression vs Run 012 (+6.19%). n_estimators monotonically worsens performance — 100 < 300 < 500 trees all degrade. Overfitting increases with each additional tree at depth=2. train.py reverted to Run 012 state.

Run 018 — XGBoost max_depth=2, learning_rate=0.01
Date: [5/11/2026]
Change: Set learning_rate=0.01. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.643467]
CV mean ± std: [0.653252] ± [0.004871]
Accepted: Yes (-0.65% vs Run 012 block best: 0.647696 → 0.643467; threshold 0.646077)
Notes: Slow learning rate dramatically reduces variance — CV std drops to 0.005 (lowest yet). Lower lr forces conservative updates, better generalization. New block best: 0.643467.

Run 019 — XGBoost max_depth=2, learning_rate=0.05
Date: [5/11/2026]
Change: Set learning_rate=0.05. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.622824]
CV mean ± std: [0.635533] ± [0.007571]
Accepted: Yes (-3.19% vs Run 018: 0.643467 → 0.622824; threshold 0.641857)
Notes: First run to beat the original logistic regression baseline (0.623589 → 0.622824). lr=0.05 better balances bias-variance than lr=0.01 with 100 trees. New best: 0.622824.

Run 020 — XGBoost max_depth=2, learning_rate=0.3
Date: [5/11/2026]
Change: Set learning_rate=0.3. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.647696]
CV mean ± std: [0.649534] ± [0.010045]
Accepted: No
Notes: lr=0.3 is the XGBoost default — identical result to Run 012 (0.647696). Confirms default learning rate is too aggressive for this feature set. train.py reverted to Run 019 state (lr=0.05).

Run 021 — XGBoost max_depth=2, lr=0.05, subsample=0.6
Date: [5/11/2026]
Change: Set subsample=0.6. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.623504]
CV mean ± std: [0.634973] ± [0.008547]
Accepted: No
Notes: Marginal regression vs Run 019 (+0.11%: 0.622824 → 0.623504). Subsampling 60% of rows does not help — insufficient data variation benefit at this tree count. train.py reverted to Run 019 state.

Run 022 — XGBoost max_depth=2, lr=0.05, subsample=0.8
Date: [5/11/2026]
Change: Set subsample=0.8. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.623846]
CV mean ± std: [0.634881] ± [0.008767]
Accepted: No
Notes: Regression vs Run 019 (+0.16%: 0.622824 → 0.623846). subsample=0.8 slightly worse than subsample=0.6; both fail to improve on Run 019. Subsampling hurts at this n_estimators. train.py reverted to Run 019 state.

Run 023 — XGBoost max_depth=2, lr=0.05, colsample_bytree=0.6
Date: [5/11/2026]
Change: Set colsample_bytree=0.6. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.621875]
CV mean ± std: [0.635448] ± [0.007824]
Accepted: No
Notes: Improvement of 0.15% (0.622824 → 0.621875) — below the 0.25% threshold (0.621268). Column subsampling at 60% is close but misses the bar. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

Run 024 — XGBoost max_depth=2, lr=0.05, colsample_bytree=0.8
Date: [5/11/2026]
Change: Set colsample_bytree=0.8. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.624324]
CV mean ± std: [0.635505] ± [0.007819]
Accepted: No
Notes: Regression vs Run 019 (+0.24%: 0.622824 → 0.624324). colsample_bytree=0.8 worse than 0.6 and both fail vs no subsampling. train.py reverted to Run 019 state.

Run 025 — XGBoost max_depth=2, lr=0.05, min_child_weight=2
Date: [5/11/2026]
Change: Set min_child_weight=2. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.622572]
CV mean ± std: [0.635425] ± [0.007687]
Accepted: No
Notes: Improvement of 0.04% (0.622824 → 0.622572) — below the 0.25% threshold (0.621268). Raising minimum leaf weight slightly helps but not enough. train.py reverted to Run 019 state. best_meta.json restored.

Run 026 — XGBoost max_depth=2, lr=0.05, min_child_weight=5
Date: [5/11/2026]
Change: Set min_child_weight=5. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.622013]
CV mean ± std: [0.635316] ± [0.007925]
Accepted: No
Notes: Improvement of 0.13% (0.622824 → 0.622013) — below the 0.25% threshold (0.621268). min_child_weight=5 slightly better than =2 (0.622572) but both miss the bar. train.py reverted to Run 019 state. best_meta.json restored.

Run 027 — XGBoost max_depth=2, lr=0.05, reg_lambda=1
Date: [5/11/2026]
Change: Set reg_lambda=1. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.622824]
CV mean ± std: [0.635533] ± [0.007571]
Accepted: No
Notes: Identical to Run 019 — reg_lambda=1 is the XGBoost default. No change in performance. train.py reverted to Run 019 state.

Run 028 — XGBoost max_depth=2, lr=0.05, reg_lambda=5
Date: [5/11/2026]
Change: Set reg_lambda=5. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.622305]
CV mean ± std: [0.635578] ± [0.007474]
Accepted: No
Notes: Improvement of 0.08% (0.622824 → 0.622305) — below the 0.25% threshold (0.621268). Heavier L2 penalty marginally helps but not enough. train.py reverted to Run 019 state. best_meta.json restored.

Run 029 — XGBoost max_depth=2, lr=0.05, reg_alpha=0.1
Date: [5/11/2026]
Change: Set reg_alpha=0.1. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.623085]
CV mean ± std: [0.635582] ± [0.007679]
Accepted: No
Notes: Marginal regression vs Run 019 (+0.04%: 0.622824 → 0.623085). L1 regularization at 0.1 slightly hurts. train.py reverted to Run 019 state.

Run 030 — XGBoost max_depth=2, lr=0.05, reg_alpha=1.0
Date: [5/11/2026]
Change: Set reg_alpha=1.0. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.624103]
CV mean ± std: [0.635321] ± [0.007747]
Accepted: No
Notes: Regression vs Run 019 (+0.20%: 0.622824 → 0.624103). Strong L1 penalty hurts — sparsity regularization removes useful signal. Week 5 hyperparameter block complete. train.py reverted to Run 019 state (final accepted: max_depth=2, lr=0.05).

Run 031 — XGBoost max_depth=2, lr=0.05, n_estimators=200
Date: [5/11/2026]
Change: Set n_estimators=200. All other settings: max_depth=2, lr=0.05, 23 features.
Val log loss: [0.623647]
CV mean ± std: [0.637780] ± [0.008369]
Accepted: No
Notes: Regression vs Run 019 (+0.13%: 0.622824 → 0.623647). More trees at lr=0.05 begin to overfit — CV std rises from 0.008 to 0.008. 200 trees is worse than 100 with this lr. train.py reverted to Run 019 state.

Run 032 — XGBoost max_depth=2, lr=0.05, n_estimators=150
Date: [5/11/2026]
Change: Set n_estimators=150. All other settings: max_depth=2, lr=0.05, 23 features.
Val log loss: [0.623662]
CV mean ± std: [0.636409] ± [0.007941]
Accepted: No
Notes: Regression vs Run 019 (+0.13%: 0.622824 → 0.623662). Nearly identical to Run 031 (200 trees). n_estimators between 100 and 200 consistently hurt at lr=0.05. train.py reverted to Run 019 state.

Run 033 — XGBoost max_depth=2, lr=0.05, n_estimators=75
Date: [5/11/2026]
Change: Set n_estimators=75 (second queue item labeled 032). All other settings: max_depth=2, lr=0.05, 23 features.
Val log loss: [0.623293]
CV mean ± std: [0.636497] ± [0.007465]
Accepted: No
Notes: Regression vs Run 019 (+0.08%: 0.622824 → 0.623293). Fewer trees also hurts — 100 is optimal at lr=0.05; both directions (75 and 150+) are worse. train.py reverted to Run 019 state.

Run 034 — XGBoost max_depth=3, lr=0.05
Date: [5/11/2026]
Change: Set max_depth=3 (lr=0.05 unchanged from accepted state). 23 features unchanged.
Val log loss: [0.624253]
CV mean ± std: [0.636845] ± [0.006990]
Accepted: No
Notes: Regression vs Run 019 (+0.23%: 0.622824 → 0.624253). max_depth=3 consistently overfits on this 23-feature set regardless of lr. max_depth=2 remains optimal. train.py reverted to Run 019 state.

Run 035 — XGBoost max_depth=2, lr=0.03
Date: [5/11/2026]
Change: Set learning_rate=0.03. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.624499]
CV mean ± std: [0.638115] ± [0.007225]
Accepted: No
Notes: Regression vs Run 019 (+0.27%: 0.622824 → 0.624499). lr=0.03 is between 0.01 and 0.05; both of those were tested and 0.05 was better. Confirms lr=0.05 is the optimal learning rate at 100 trees. train.py reverted to Run 019 state.

Run 036 — XGBoost max_depth=2, lr=0.07
Date: [5/11/2026]
Change: Set learning_rate=0.07. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.624293]
CV mean ± std: [0.636346] ± [0.008184]
Accepted: No
Notes: Regression vs Run 019 (+0.24%: 0.622824 → 0.624293). lr=0.07 is slightly faster than 0.05 and worse. Both directions (0.03 and 0.07) from 0.05 are worse, confirming 0.05 is optimal at 100 trees. train.py reverted to Run 019 state.

Run 037 — XGBoost max_depth=2, lr=0.02
Date: [5/11/2026]
Change: Set learning_rate=0.02. All other settings: max_depth=2, 23 features, n_estimators default (100).
Val log loss: [0.630057]
CV mean ± std: [0.642843] ± [0.006562]
Accepted: No
Notes: Significant regression vs Run 019 (+1.17%: 0.622824 → 0.630057). lr=0.02 underfits with only 100 trees — the model cannot converge in time. Would require many more trees to compensate. train.py reverted to Run 019 state.

Run 038 — XGBoost max_depth=2, lr=0.05, min_child_weight=3
Date: [5/11/2026]
Change: Set min_child_weight=3. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.622155]
CV mean ± std: [0.635558] ± [0.007767]
Accepted: No
Notes: Improvement of 0.11% (0.622824 → 0.622155) — below the 0.25% threshold (0.621268). Sits between min_child_weight=2 (0.04% improvement) and =5 (0.13% improvement); =5 remains the closest near-miss. train.py reverted to Run 019 state. best_meta.json restored.

Run 039 — XGBoost max_depth=2, lr=0.05, min_child_weight=4
Date: [5/11/2026]
Change: Set min_child_weight=4. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.621710]
CV mean ± std: [0.635602] ± [0.007853]
Accepted: No
Notes: Improvement of 0.18% (0.622824 → 0.621710) — below the 0.25% threshold (0.621268). Closest near-miss in this block. min_child_weight trend: 2→0.04%, 3→0.11%, 4→0.18%, 5→0.13%; peak signal appears around 4. train.py reverted to Run 019 state. best_meta.json restored.

Run 040 — XGBoost max_depth=2, lr=0.05, subsample=0.7
Date: [5/11/2026]
Change: Set subsample=0.7. All other settings: max_depth=2, lr=0.05, 23 features, n_estimators default (100).
Val log loss: [0.625850]
CV mean ± std: [0.633866] ± [0.008131]
Accepted: No
Notes: Regression vs Run 019 (+0.49%: 0.622824 → 0.625850). subsample=0.7 worse than both 0.6 (Run 021) and 0.8 (Run 022). All subsample values tested (0.6, 0.7, 0.8) hurt performance. Week 6 block complete. train.py reverted to Run 019 state.

Run 041 — Remove window-16 features (17 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features (home/away pts_scored_16, pts_allowed_16, win_pct_16). Features: 23 → 17.
Val log loss: [0.621545]
CV mean ± std: [0.635023] ± [0.007600]
Accepted: No
Notes: Improvement of 0.205% (0.622824 → 0.621545) — below the 0.25% threshold (0.621268) by only 0.000277. Window-16 features add noise rather than signal. Narrowest near-miss of all runs. train.py reverted to full 23-feature set. best_meta.json restored.

Run 042 — Remove window-4 features (17 features)
Date: [5/11/2026]
Change: Removed all _4 rolling features (home/away pts_scored_4, pts_allowed_4, win_pct_4). Features: 23 → 17.
Val log loss: [0.626109]
CV mean ± std: [0.637144] ± [0.009038]
Accepted: No
Notes: Regression vs Run 019 (+0.53%: 0.622824 → 0.626109). Short-window (4-game) features carry useful signal — removing them hurts. Contrast with Run 041 (removing window-16 helped). train.py reverted to full 23-feature set.

Run 043 — Remove pts_allowed features (17 features)
Date: [5/11/2026]
Change: Removed all pts_allowed rolling features (home/away pts_allowed_4/8/16). Features: 23 → 17.
Val log loss: [0.621625]
CV mean ± std: [0.638089] ± [0.007925]
Accepted: No
Notes: Improvement of 0.192% (0.622824 → 0.621625) — below the 0.25% threshold (0.621268). pts_allowed features add marginal noise; pts_scored and win_pct carry most of the signal. Second-closest near-miss alongside Run 041. train.py reverted to full 23-feature set. best_meta.json restored.

Run 044 — Remove pts_scored features (17 features)
Date: [5/11/2026]
Change: Removed all pts_scored rolling features (home/away pts_scored_4/8/16). Features: 23 → 17.
Val log loss: [0.625224]
CV mean ± std: [0.642175] ± [0.007643]
Accepted: No
Notes: Regression vs Run 019 (+0.38%: 0.622824 → 0.625224). pts_scored is more informative than pts_allowed — removing it hurts more (Run 043 removing pts_allowed: +0.19% improvement; this run removing pts_scored: -0.38% regression). train.py reverted to full 23-feature set.

Run 045 — Baseline + win_pct + rest_days only (11 features)
Date: [5/11/2026]
Change: Removed all pts_scored and pts_allowed features. Features: 23 → 11 (baseline + win_pct_4/8/16 home+away + rest_days).
Val log loss: [0.622987]
CV mean ± std: [0.642895] ± [0.008895]
Accepted: No
Notes: Marginal regression (+0.03%: 0.622824 → 0.622987). Remarkable — 11 features nearly match 23. Scoring features add very little. win_pct + baseline captures almost all predictive signal. train.py reverted to full 23-feature set.

Run 046 — Remove away rolling features (14 features)
Date: [5/11/2026]
Change: Removed all away rolling features (away_pts_scored/allowed_4/8/16, away_win_pct_4/8/16). Features: 23 → 14.
Val log loss: [0.622828]
CV mean ± std: [0.643120] ± [0.008790]
Accepted: No
Notes: Regression of 0.0006% (0.622824 → 0.622828). Functionally identical to current best — away rolling features contribute essentially zero net signal. train.py reverted to full 23-feature set.

Run 047 — Remove home rolling features (14 features)
Date: [5/11/2026]
Change: Removed all home rolling features (home_pts_scored/allowed_4/8/16, home_win_pct_4/8/16). Features: 23 → 14.
Val log loss: [0.633376]
CV mean ± std: [0.647390] ± [0.007312]
Accepted: No
Notes: Significant regression (+1.69%: 0.622824 → 0.633376). Sharp asymmetry: home features are far more predictive than away features (Run 046 removing away features: +0.0006%; this run removing home features: +1.69%). train.py reverted to full 23-feature set.

Run 048 — Remove rest_days features (21 features)
Date: [5/11/2026]
Change: Removed home_rest_days and away_rest_days. Features: 23 → 21 (rest_diff baseline feature retained).
Val log loss: [0.621985]
CV mean ± std: [0.635718] ± [0.007622]
Accepted: No
Notes: Improvement of 0.135% (0.622824 → 0.621985) — below the 0.25% threshold (0.621268). home/away_rest_days add marginal noise on top of rest_diff. train.py reverted to full 23-feature set. best_meta.json restored.

Run 049 — Baseline + win_pct_8 only (5 features)
Date: [5/11/2026]
Change: Features reduced to baseline + home_win_pct_8 + away_win_pct_8 only.
Val log loss: [0.624457]
CV mean ± std: [0.641087] ± [0.010208]
Accepted: No
Notes: Regression vs Run 019 (+0.26%: 0.622824 → 0.624457). Too sparse — loses more signal than Run 045 (11 features at 0.622987). Single window win% at 8 games is insufficient. train.py reverted to full 23-feature set.

Run 050 — Baseline + pts_scored_8 + pts_allowed_8 (7 features)
Date: [5/11/2026]
Change: Features reduced to baseline + home/away_pts_scored_8 + home/away_pts_allowed_8 only.
Val log loss: [0.624329]
CV mean ± std: [0.638002] ± [0.007817]
Accepted: No
Notes: Regression vs Run 019 (+0.24%: 0.622824 → 0.624329). 8-game scoring window alone is insufficient. Slightly better than Run 049 (5 features) — scoring at 8 games has more signal than win_pct_8 alone, but still not competitive with the full set. train.py reverted to full 23-feature set.

Run 051 — No window-16 + min_child_weight=4 (17 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features AND set min_child_weight=4.
Val log loss: [0.621506]
CV mean ± std: [0.634945] ± [0.007781]
Accepted: No
Notes: Improvement of 0.212% (0.622824 → 0.621506) — missed threshold by 0.000238. Combining the two best individual near-misses (Run 041: -0.205%, Run 039: -0.179%) yields less than additive improvement. train.py reverted to Run 019 state. best_meta.json restored.

Run 052 — No window-16 + no pts_allowed (13 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features AND all pts_allowed features. Features: 23 → 13.
Val log loss: [0.621487]
CV mean ± std: [0.637270] ± [0.007484]
Accepted: No
Notes: Improvement of 0.215% (0.622824 → 0.621487) — missed threshold by 0.000219. Best result yet but still below the bar. Slightly better than Run 051. train.py reverted to Run 019 state. best_meta.json restored.

Run 053 — No pts_allowed + min_child_weight=4 (17 features)
Date: [5/11/2026]
Change: Removed all pts_allowed features AND set min_child_weight=4.
Val log loss: [0.622266]
CV mean ± std: [0.638266] ± [0.007660]
Accepted: No
Notes: Improvement of only 0.09% (0.622824 → 0.622266) — worse than either change alone (Run 043: -0.192%, Run 039: -0.179%). Negative interaction between removing pts_allowed and raising min_child_weight. train.py reverted to Run 019 state. best_meta.json restored.

Run 054 — No window-16 + no pts_allowed + min_child_weight=4 (13 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features, all pts_allowed features, AND set min_child_weight=4.
Val log loss: [0.622366]
CV mean ± std: [0.637357] ± [0.007501]
Accepted: No
Notes: Improvement of only 0.07% (0.622824 → 0.622366) — worse than any two-way combination. Adding min_child_weight=4 on top of the 052 feature set hurts. The improvements are not additive; diminishing returns with each combination. train.py reverted to Run 019 state. best_meta.json restored.

Run 055 — No window-16 + colsample_bytree=0.6 (17 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features AND set colsample_bytree=0.6.
Val log loss: [0.622353]
CV mean ± std: [0.634931] ± [0.007963]
Accepted: No
Notes: Improvement of only 0.076% (0.622824 → 0.622353) — far less than additive. colsample_bytree negates the feature pruning benefit. Feature set and column subsampling interact negatively. train.py reverted to Run 019 state. best_meta.json restored.

Run 056 — No window-16 + no rest_days (15 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features AND home/away_rest_days. Features: 23 → 15.
Val log loss: [0.621538]
CV mean ± std: [0.634852] ± [0.007690]
Accepted: No
Notes: Improvement of 0.206% (0.622824 → 0.621538) — missed threshold by 0.000270. Consistent with the window-16 removal dominating the improvement; adding rest_days removal provides minimal additional gain. train.py reverted to Run 019 state. best_meta.json restored.

Run 057 — No window-16 + no pts_allowed + no rest_days (11 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features, all pts_allowed features, AND home/away_rest_days. Features: 23 → 11.
Val log loss: [0.622442]
CV mean ± std: [0.637333] ± [0.007656]
Accepted: No
Notes: Only 0.061% improvement (0.622824 → 0.622442). Three-way feature removal continues the pattern of strongly diminishing returns — each additional removal reduces the net benefit. The 052 two-way combo remains the best combination found. train.py reverted to Run 019 state. best_meta.json restored.

Run 058 — No pts_allowed + colsample_bytree=0.6 (17 features)
Date: [5/11/2026]
Change: Removed all pts_allowed features AND set colsample_bytree=0.6.
Val log loss: [0.622866]
CV mean ± std: [0.637399] ± [0.008561]
Accepted: No
Notes: Marginal regression (+0.006%: 0.622824 → 0.622866). colsample_bytree completely cancels out the pts_allowed removal benefit. Column subsampling combined with any feature pruning consistently shows negative interaction. train.py reverted to Run 019 state.

Run 059 — No window-16 + no pts_allowed + min_child_weight=4 + colsample_bytree=0.6 (13 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features and all pts_allowed features; set min_child_weight=4 and colsample_bytree=0.6.
Val log loss: [0.621703]
CV mean ± std: [0.636615] ± [0.008007]
Accepted: No
Notes: Improvement of 0.180% (0.622824 → 0.621703) — worse than Run 052 (0.621487, two-way combo). Four-way combinations are worse than two-way. Adding mcw=4 and cbt=0.6 on top of the 052 feature set actively hurts. train.py reverted to Run 019 state. best_meta.json restored.

Run 060 — No window-16 + no pts_allowed + min_child_weight=4 + no rest_days (11 features)
Date: [5/11/2026]
Change: Removed all _16 rolling features, all pts_allowed features, and home/away_rest_days; set min_child_weight=4.
Val log loss: [0.622918]
CV mean ± std: [0.637302] ± [0.007721]
Accepted: No
Notes: Regression vs Run 019 (+0.015%: 0.622824 → 0.622918). The most aggressive combination is the worst — adding more changes beyond the optimal two-way set (Run 052) consistently degrades. Week 7 combination block complete; best result: Run 052 (0.621487, -0.215%). train.py reverted to Run 019 state.

Run 061 — XGBoost early stopping (n_estimators=500, early_stopping_rounds=10)
Date: [5/18/2026]
Change: Added n_estimators=500 and early_stopping_rounds=10 to Run 019 config (max_depth=2, lr=0.05). eval_set=[(X_val, y_val)] used for final fit; CV folds use val fold as eval_set. 23 features unchanged.
Val log loss: [0.622517]
CV mean ± std: [0.635222] ± [0.007607]
Accepted: No
Notes: Improvement of 0.049% (0.622824 → 0.622517) — below the 0.25% threshold (0.621268). Early stopping with n_estimators=500 provides marginal benefit; the model likely stops well before 500 trees but the optimal tree count at lr=0.05 is already close to the default 100. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

Run 062 — XGBoost early stopping lr=0.03 (n_estimators=500, early_stopping_rounds=10)
Date: [5/18/2026]
Change: Same as 061 but learning_rate=0.03. n_estimators=500, early_stopping_rounds=10, max_depth=2. eval_set=[(X_val, y_val)] for final fit. 23 features unchanged.
Val log loss: [0.622536]
CV mean ± std: [0.635206] ± [0.007766]
Accepted: No
Notes: Improvement of 0.046% (0.622824 → 0.622536) — below the 0.25% threshold (0.621268). Nearly identical to Run 061 (lr=0.05 with early stopping). Early stopping does not meaningfully help at either lr=0.05 or lr=0.03 with 500 trees. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

Run 063 — Add 32-game rolling win% (25 features)
Date: [5/18/2026]
Change: Added home_win_pct_32 and away_win_pct_32 to Run 019 config. windows expanded to [4,8,16,32] in compute_rolling_features. 23 → 25 features.
Val log loss: [0.621702]
CV mean ± std: [0.635599] ± [0.007759]
Accepted: No
Notes: Improvement of 0.180% (0.622824 → 0.621702) — below the 0.25% threshold (0.621268). Adding 32-game win% is a near-miss; longer-window signal helps slightly but not enough to clear the bar. train.py reverted to Run 019 state (windows=[4,8,16], 23 features). best_meta.json restored to run_24 (0.622824).

Run 064 — Add 32-game rolling pts scored/allowed (27 features)
Date: [5/18/2026]
Change: Added home/away_pts_scored_32 and home/away_pts_allowed_32 to Run 019 config. windows expanded to [4,8,16,32]. 23 → 27 features.
Val log loss: [0.625513]
CV mean ± std: [0.635555] ± [0.007883]
Accepted: No
Notes: Regression — 0.625513 > 0.622824 (+0.43%). 32-game scoring features add noise; contrast with Run 063 (32-game win% slightly helped). Long-window scoring is less informative than long-window win%. train.py reverted to Run 019 state (windows=[4,8,16], 23 features).

Run 065 — Add all 32-game rolling features (29 features)
Date: [5/18/2026]
Change: Added home/away_win_pct_32, pts_scored_32, pts_allowed_32 to Run 019 config. windows=[4,8,16,32]. 23 → 29 features (spec listed 27; actual count is 29 — 6 new features).
Val log loss: [0.625513]
CV mean ± std: [0.635648] ± [0.007995]
Accepted: No
Notes: Regression — identical to Run 064 (0.625513). Adding 32-game win% on top of 32-game scoring features has zero marginal effect. 32-game scoring features dominate negatively regardless of win% inclusion. train.py reverted to Run 019 state (windows=[4,8,16], 23 features).

Run 066 — Ensemble XGBoost (Run 019) + LR (Run 002), weights 0.5/0.5
Date: [5/18/2026]
Change: Ensemble of Run 019 XGBoost (max_depth=2, lr=0.05, 23 features) and Run 002 LR (Groups A+B+C, 15 features) with equal weights. Predictions averaged: 0.5 × XGB + 0.5 × LR. CV computed on ensemble predictions per fold.
Val log loss: [0.618727]
CV mean ± std: [0.633352] ± [0.008020]
Accepted: Yes
Notes: First acceptance in Week 6 block. Improvement of 0.658% (0.622824 → 0.618727) — exceeds 0.25% threshold (0.621268). Ensemble diversity between XGB and LR provides genuine complementary signal. New best: 0.618727. Model checkpoint saved (run_71).

Run 067 — Ensemble XGBoost (Run 019) + LR (Run 002), weights 0.35/0.65
Date: [5/18/2026]
Change: Same ensemble as Run 066 but shifted weight toward LR: 0.35 × XGB + 0.65 × LR.
Val log loss: [0.617921]
CV mean ± std: [0.633362] ± [0.008195]
Accepted: No
Notes: Improvement of 0.130% (0.618727 → 0.617921) — below the 0.25% threshold (0.617180). LR-heavy weighting is marginally better than equal weights but not enough to clear the bar. train.py reverted to Run 066 state (weights 0.5/0.5). best_meta.json restored to run_71 (0.618727).

Run 068 — LightGBM (max_depth=2, lr=0.05, n_estimators=100)
Date: [5/18/2026]
Change: Swapped model to LightGBM with equivalent config to Run 019 (max_depth=2, learning_rate=0.05, n_estimators=100). Same 23 features.
Val log loss: [0.622597]
CV mean ± std: [0.635452] ± [0.007721]
Accepted: No
Notes: Regression vs current best Run 066 (+0.62%: 0.618727 → 0.622597). LightGBM with equivalent config does not match the XGBoost+LR ensemble. Notably, LightGBM is slightly better than XGBoost alone (Run 019: 0.622824) but far below the ensemble. train.py reverted to Run 066 ensemble state.

Run 069 — Random Forest (n_estimators=300, max_depth=6)
Date: [5/18/2026]
Change: Swapped model to Random Forest (n_estimators=300, max_depth=6). Same 23 features as Run 019.
Val log loss: [0.621606]
CV mean ± std: [0.633781] ± [0.007147]
Accepted: No
Notes: Regression vs current best Run 066 (+0.46%: 0.618727 → 0.621606). Random Forest does not match the XGBoost+LR ensemble. CV std (0.007) is the lowest in the block, indicating stability, but absolute performance falls short. train.py reverted to Run 066 ensemble state.

Run 070 — Ensemble XGB (cbt=0.6) + LR, weights 0.5/0.5 (on top of Run 066)
Date: [5/18/2026]
Change: Added colsample_bytree=0.6 to the XGBoost component of the accepted Run 066 ensemble. Best run from 061-069 was Run 066 (0.618727); this adds cbt=0.6 on top.
Val log loss: [0.618306]
CV mean ± std: [0.633391] ± [0.008126]
Accepted: No
Notes: Improvement of 0.068% (0.618727 → 0.618306) — below the 0.25% threshold (0.617180). colsample_bytree=0.6 in the ensemble context provides marginal benefit, consistent with its pattern in solo XGBoost runs (Run 023: -0.15%). Week 6 block complete. Final accepted state: Run 066 ensemble (XGB + LR, 0.5/0.5, val_loss=0.618727). train.py reverted to Run 066 ensemble state. best_meta.json restored to run_71 (0.618727).

Run 071 — XGBoost Run 019 config, top 10 features by feature_importances_
Date: [5/18/2026]
Change: Train probe XGBoost (max_depth=2, lr=0.05) on all 23 features, log importances, select top 10, retrain on those 10. Top 10: elo_diff, home_win_pct_8/4/16, away_pts_scored_16/8/4, home_pts_scored_8/16, away_win_pct_8. Note: home_game and home_rest_days had zero importance.
Val log loss: [0.625539]
CV mean ± std: [0.637595] ± [0.009236]
Accepted: No
Notes: Regression vs current best (+1.10%: 0.618727 → 0.625539). Pruning to top 10 features drops too much signal — notably home_game (zero importance probe artifact) is important for calibration. train.py reverted to Run 066 ensemble state.

Run 072 — XGBoost Run 019 config, top 15 features by feature_importances_
Date: [5/18/2026]
Change: Train probe XGBoost (max_depth=2, lr=0.05) on all 23 features, select top 15 by importances, retrain on those 15. Top 15 adds: home_pts_allowed_16/4, home_pts_scored_4, away_pts_allowed_4, away_win_pct_16 beyond the top 10.
Val log loss: [0.623045]
CV mean ± std: [0.634800] ± [0.007600]
Accepted: No
Notes: Regression vs current best (+0.69%: 0.618727 → 0.623045). Better than top 10 (0.625539) but still regresses vs both Run 066 (0.618727) and Run 019 (0.622824). Importance-based pruning consistently hurts — the 8 pruned features contribute net positive signal even at low importances. train.py reverted to Run 066 ensemble state.

Run 073 — 3-model Ensemble XGBoost + LR + Random Forest, equal weights
Date: [5/18/2026]
Change: 3-model ensemble: XGBoost (Run 019, max_depth=2, lr=0.05, 23 features) + LR (Run 002, 15 features) + Random Forest (n_estimators=300, max_depth=6, 23 features). Weights: 1/3 each.
Val log loss: [0.619347]
CV mean ± std: [0.633012] ± [0.007718]
Accepted: No
Notes: Regression vs current best (+0.10%: 0.618727 → 0.619347). Adding RF to the XGB+LR ensemble slightly hurts — RF alone (Run 069: 0.621606) is weaker than XGB alone and dilutes the superior XGB+LR signal. train.py reverted to Run 066 ensemble state.

Run 074 — 3-model Ensemble XGBoost + LR + LightGBM, equal weights
Date: [5/18/2026]
Change: 3-model ensemble: XGBoost (Run 019, max_depth=2, lr=0.05, 23 features) + LR (Run 002, 15 features) + LightGBM (max_depth=2, lr=0.05, n_estimators=100, 23 features). Weights: 1/3 each.
Val log loss: [0.619805]
CV mean ± std: [0.633645] ± [0.007907]
Accepted: No
Notes: Regression vs current best (+0.17%: 0.618727 → 0.619805). Adding LightGBM also hurts — LightGBM alone (Run 068: 0.622597) is weaker than XGB, diluting the XGB+LR ensemble more than RF did. 2-model XGB+LR (Run 066) remains the optimal combination. train.py reverted to Run 066 ensemble state.

Run 075 — Weight grid search on Run 066 ensemble (XGB=0.3, LR=0.7 is best)
Date: [5/18/2026]
Change: Grid search over 3 weight combos for XGB+LR ensemble. Results: (0.4/0.6)=0.618168, (0.3/0.7)=0.617695, (0.6/0.4)=0.619373. Best: XGB=0.3, LR=0.7. CV computed with best weights.
Val log loss: [0.617695]
CV mean ± std: [0.633435] ± [0.008258]
Accepted: No
Notes: Improvement of 0.167% (0.618727 → 0.617695) — below the 0.25% threshold (0.617180). Missed by 0.000515. LR-heavy weighting consistently helps (Run 067: 0.35/0.65 was also better than equal weights) but none of the tested combos clear the bar. train.py reverted to Run 066 ensemble state. best_meta.json restored to run_71 (0.618727).

Run 076 — Ensemble XGB + LR, weights 0.2/0.8
Date: [5/18/2026]
Change: Ensemble Run 019 (XGBoost, max_depth=2, lr=0.05, 23 features) + Run 002 (LR, 15 features) with weights 0.2 XGB / 0.8 LR.
Val log loss: [0.617311]
CV mean ± std: [0.633685] ± [0.008393]
Accepted: No
Notes: Improvement of 0.229% (0.618727 → 0.617311) — below the 0.25% threshold (0.617180). Missed by 0.000131. Narrowest near-miss of all 76 runs. LR-heavy trend continues: 0.5/0.5=0.618727, 0.35/0.65=0.617921, 0.3/0.7=0.617695, 0.2/0.8=0.617311 — still improving but not crossing the bar. train.py reverted to Run 066 ensemble state. best_meta.json restored to run_71 (0.618727).

Run 077 — Pure LR (XGB weight=0.0, LR weight=1.0)
Date: [5/18/2026]
Change: Ensemble weights set to 0.0 XGB / 1.0 LR — effectively pure Logistic Regression on lr_features_002 (15 features: baseline + rolling pts scored 4/8/16 + rolling win pct 4/8/16).
Val log loss: [0.616811]
CV mean ± std: [0.634619] ± [0.008704]
Accepted: Yes
Notes: Improvement of 0.310% (0.618727 → 0.616811) — exceeds 0.25% threshold (0.617180). LR-heavy weight trend finally clears the bar at 0/1. Reveals that the LR on 15 features consistently outperforms any XGB contribution in this ensemble; pure LR beats all mixed weights. New best: 0.616811. Model checkpoint saved (run_82).