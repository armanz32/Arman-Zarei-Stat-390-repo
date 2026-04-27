## Failure Log

### Run 001 — 2026-04-26
**Change:** Add Group C features: rolling win % over last 4, 8, 16 games (home_win_pct_4/8/16, away_win_pct_4/8/16). Features computed in-memory via shift(1) rolling mean — no data leakage.
**Val log loss:** 0.619831
**Current best:** 0.623589
**Threshold required:** 0.611117 (current_best × 0.98)
**Improvement:** 0.60% — below the 2% minimum threshold.
**Decision:** Rejected. train.py reverted to baseline. best_meta.json restored to run_0 (0.623589).

---

### Run 002 — 2026-04-26 — BLOCKED: Ambiguity
**Change requested:** Add Groups A + B + C together.
**Ambiguity:** "Group A" and "Group B" are referenced in the Experiment Queue but are never defined anywhere in the repository (not in program.md, research_log.md, README.md, prepare.py, or any other file). Group C is defined (rolling win % over last 4, 8, 16 games). Groups A and B have no definition.
**Action taken:** No changes made to train.py. Logging ambiguity per protocol and stopping.
**Resolution needed:** Human operator must define what features constitute Group A and Group B before Run 002 can proceed.
**Resolved:** Group A = baseline (elo_diff, home_game, rest_diff); Group B = rolling scoring avg (home/away_score_avg_4/8/16). Run 002 proceeded after clarification.

---

### Run 002 — 2026-04-26
**Change:** Add Groups A + B + C: baseline + home/away_score_avg_4/8/16 + home/away_win_pct_4/8/16 (15 features total).
**Val log loss:** 0.616790
**Current best:** 0.623589
**Threshold required:** 0.611117 (current_best × 0.98)
**Improvement:** 1.09% — below the 2% minimum threshold.
**Decision:** Rejected. train.py reverted to baseline. best_meta.json restored to run_0 (0.623589).

---

### Run 003 — 2026-04-26
**Change:** Switch to XGBoost (n_estimators=200, max_depth=4, learning_rate=0.05), Groups A+B+C (15 features).
**Val log loss:** 0.628627
**Current best:** 0.623589
**Threshold required:** 0.611117 (current_best × 0.98)
**Result:** Regression — 0.628627 > 0.623589 (baseline). XGBoost performed worse than logistic regression with default hyperparameters on this dataset.
**Decision:** Rejected. train.py reverted to baseline. best_meta.json unchanged (save_best correctly skipped).

---

### Run 004 — 2026-04-26
**Change:** XGBoost grid search over max_depth ∈ {3,5,7} × n_estimators ∈ {100,300}. Groups A+B+C (15 features).
**Grid results:** d=3/n=100: 0.640998 ✓ | d=3/n=300: 0.651590 | d=5/n=100: 0.650658 | d=5/n=300: 0.673162 | d=7/n=100: 0.663970 | d=7/n=300: 0.699592
**Best config:** max_depth=3, n_estimators=100
**Val log loss:** 0.619820
**Current best:** 0.623589
**Threshold required:** 0.611117 (current_best × 0.98)
**Improvement:** 0.60% — below the 2% minimum threshold.
**Decision:** Rejected. train.py reverted to baseline. best_meta.json restored to run_0 (0.623589).
