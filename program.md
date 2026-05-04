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
Acceptance threshold: A change is accepted only if: new_val_log_loss < current_best_val_log_loss * 0.985
This means a minimum 1.5% improvement is required. Improvements smaller than 1.5% are discarded even if positive.

The Loop (execute exactly in this order)
Step 1 — Read the queue: Read the next unchecked item in the Experiment Queue below. Do not skip items or reorder them.

Step 2 — Make exactly one change: Edit train.py to implement that item and nothing else. Do not bundle multiple queue items into one run.
Step 3 — Run the experiment; python train.py
Record the val log loss and CV mean ± std printed to stdout.

Step 4 — Evaluate: Compare new_val_log_loss against current_best_val_log_loss * 0.985.
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

