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
Acceptance threshold: A change is accepted only if: new_val_log_loss < current_best_val_log_loss * 0.98
This means a minimum 2% improvement is required. Improvements smaller than 2% are discarded even if positive.
Current best val log loss: [UPDATE THIS AFTER EACH ACCEPTED RUN]

The Loop (execute exactly in this order)
Step 1 — Read the queue: Read the next unchecked item in the Experiment Queue below. Do not skip items or reorder them.

Step 2 — Make exactly one change: Edit train.py to implement that item and nothing else. Do not bundle multiple queue items into one run.
Step 3 — Run the experiment; python train.py
Record the val log loss and CV mean ± std printed to stdout.

Step 4 — Evaluate: Compare new_val_log_loss against current_best_val_log_loss * 0.98.
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

Iteration Log
Append one entry per run. Do not edit previous entries.

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
Notes: Improvement of ~0.60% (0.623589 → 0.619831) falls below the 2% required threshold (0.611117). train.py reverted to baseline.

Run 002 — Groups A + B + C (baseline + rolling scoring avg + rolling win %)
Date: [4/26/2026]
Change: Added Group B (home/away_score_avg_4/8/16) and Group C (home/away_win_pct_4/8/16) on top of baseline. 15 features total. Groups A+B+C definition clarified by human operator before run.
Val log loss: [0.616790]
CV mean ± std: [0.633451] ± [0.004513]
Accepted: No
Notes: Improvement of ~1.09% (0.623589 → 0.616790) falls below the 2% required threshold (0.611117). train.py reverted to baseline.

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
Notes: Best XGBoost config (depth=3, trees=100) achieves 0.60% improvement over baseline — identical to logistic regression with rolling features (Run 001: 0.619831). Below the 2% threshold. Shallower/fewer trees consistently outperform deeper/more trees. train.py reverted to baseline.

