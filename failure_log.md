## Failure Log

### Run 001 — 2026-04-26
**Change:** Add Group C features: rolling win % over last 4, 8, 16 games (home_win_pct_4/8/16, away_win_pct_4/8/16). Features computed in-memory via shift(1) rolling mean — no data leakage.
**Val log loss:** 0.619831
**Current best:** 0.623589
**Threshold required:** 0.611117 (current_best × 0.98)
**Improvement:** 0.60% — below the 1.5% minimum threshold.
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
**Improvement:** 1.09% — below the 1.5% minimum threshold.
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
**Improvement:** 0.60% — below the 1.5% minimum threshold.
**Decision:** Rejected. train.py reverted to baseline. best_meta.json restored to run_0 (0.623589).

---

### Run 005 — 2026-05-04
**Change:** Add elo_diff × home_win_pct_8 interaction term (13 features: baseline + rolling scoring avg + home win pct 4/8/16 + interaction).
**Val log loss:** 0.623928
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Result:** Regression — 0.623928 > 0.623589. Interaction term made performance slightly worse.
**Decision:** Rejected. train.py reverted to pre-Run-005 state. best_meta.json unchanged.

---

### Run 006 — 2026-05-04
**Change:** Add elo_diff² (elo_diff_sq = elo_diff ** 2) as a 13th feature. Model: logistic regression, 12 base features + squared ELO.
**Val log loss:** 0.622981
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Improvement:** 0.10% — below the 1.5% minimum threshold.
**Decision:** Rejected. train.py reverted to pre-Run-006 state. best_meta.json restored to run_0 (0.623589).

---

### Run 007 — 2026-05-04
**Change:** Add rest_diff × away_score_avg_8 interaction term (13 features: baseline + rolling scoring avg + home win pct 4/8/16 + interaction).
**Val log loss:** 0.624205
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Result:** Regression — 0.624205 > 0.623589. Interaction term made performance worse.
**Decision:** Rejected. train.py reverted to pre-Run-007 state. best_meta.json unchanged (save_best correctly skipped).

---

### Run 008 — 2026-05-04
**Change:** Bin elo_diff into 5 ordinal categories (quantile bins on train, fixed edges applied to val).
**Val log loss:** 0.625514
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Result:** Regression — 0.625514 > 0.623589. Discretizing ELO diff loses information; ordinal bin alongside raw elo_diff adds noise.
**Decision:** Rejected. train.py reverted to pre-Run-008 state. best_meta.json unchanged (save_best correctly skipped).

---

### Run 009 — 2026-05-04
**Change:** Add elo_diff² (elo_diff_sq = elo_diff ** 2) as a 4th feature on top of the true 3-feature baseline.
**Val log loss:** 0.622191
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Improvement:** 0.22% — below the 1.5% minimum threshold.
**Decision:** Rejected. train.py reverted to true 3-feature baseline. best_meta.json restored to run_0 (0.623589).

---

### Run 010 — 2026-05-04
**Change:** Drop rest_diff entirely — features reduced to elo_diff + home_game (2 features).
**Val log loss:** 0.622446
**Current best:** 0.623589
**Threshold required:** 0.614135 (current_best × 0.985)
**Improvement:** 0.18% — below the 1.5% minimum threshold.
**Decision:** Rejected. train.py reverted to 3-feature baseline. best_meta.json restored to run_0 (0.623589).

---

### Run 013 — 2026-05-11
**Change:** Set max_depth=4 in XGBoost model_config. 23-feature set unchanged.
**Val log loss:** 0.676621
**Current best (Week 5 block):** 0.647696 (Run 012)
**Threshold required:** 0.646077 (current_best × 0.9975)
**Result:** Regression — 0.676621 > 0.647696 (+4.47%). Deeper trees overfit more on the 23-feature set; CV std rises from 0.010 to 0.015.
**Decision:** Rejected. train.py reverted to Run 012 state (max_depth=2).

---

### Run 014 — 2026-05-11
**Change:** Set max_depth=6 in XGBoost model_config. 23-feature set unchanged.
**Val log loss:** 0.702775
**Current best (Week 5 block):** 0.647696 (Run 012)
**Threshold required:** 0.646077 (current_best × 0.9975)
**Result:** Identical to Run 011b (0.702775) — max_depth=6 is the XGBoost default, confirming 011b used depth 6. Regression vs Run 012 (+8.49%).
**Decision:** Rejected. train.py reverted to Run 012 state (max_depth=2).

---

### Run 015 — 2026-05-11
**Change:** Set n_estimators=100 explicitly. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.647696
**Current best (Week 5 block):** 0.647696 (Run 012)
**Threshold required:** 0.646077 (current_best × 0.9975)
**Result:** Identical to Run 012 — n_estimators=100 is the XGBoost default. No change in performance.
**Decision:** Rejected. train.py reverted to Run 012 state (max_depth=2, no explicit n_estimators).

---

### Run 016 — 2026-05-11
**Change:** Set n_estimators=300. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.663226
**Current best (Week 5 block):** 0.647696 (Run 012)
**Threshold required:** 0.646077 (current_best × 0.9975)
**Result:** Regression — 0.663226 > 0.647696 (+2.39%). More trees with depth=2 overfit further.
**Decision:** Rejected. train.py reverted to Run 012 state (max_depth=2).

---

### Run 017 — 2026-05-11
**Change:** Set n_estimators=500. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.687740
**Current best (Week 5 block):** 0.647696 (Run 012)
**Threshold required:** 0.646077 (current_best × 0.9975)
**Result:** Regression — 0.687740 > 0.647696 (+6.19%). n_estimators monotonically worsens: 100 (0.647696) < 300 (0.663226) < 500 (0.687740).
**Decision:** Rejected. train.py reverted to Run 012 state (max_depth=2).

---

### Run 020 — 2026-05-11
**Change:** Set learning_rate=0.3. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.647696
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** lr=0.3 is XGBoost default — identical result to Run 012 (0.647696). Regression vs Run 019 (+3.99%).
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, learning_rate=0.05).

---

### Run 021 — 2026-05-11
**Change:** Set subsample=0.6. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623504
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Marginal regression — 0.623504 > 0.622824 (+0.11%). Does not clear the 0.25% improvement bar.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 022 — 2026-05-11
**Change:** Set subsample=0.8. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623846
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.623846 > 0.622824 (+0.16%). subsample=0.8 worse than 0.6; both hurt performance vs Run 019.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 023 — 2026-05-11
**Change:** Set colsample_bytree=0.6. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.621875
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.15% (0.622824 → 0.621875) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 024 — 2026-05-11
**Change:** Set colsample_bytree=0.8. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.624324
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624324 > 0.622824 (+0.24%). colsample_bytree=0.8 is worse than 0.6; both hurt vs no column subsampling.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 025 — 2026-05-11
**Change:** Set min_child_weight=2. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.622572
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.04% (0.622824 → 0.622572) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 026 — 2026-05-11
**Change:** Set min_child_weight=5. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.622013
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.13% (0.622824 → 0.622013) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 027 — 2026-05-11
**Change:** Set reg_lambda=1. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.622824
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Identical to Run 019 — reg_lambda=1 is the XGBoost default. No improvement.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 028 — 2026-05-11
**Change:** Set reg_lambda=5. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.622305
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.08% (0.622824 → 0.622305) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 029 — 2026-05-11
**Change:** Set reg_alpha=0.1. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623085
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Marginal regression — 0.623085 > 0.622824 (+0.04%). L1 regularization at 0.1 slightly hurts performance.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 030 — 2026-05-11
**Change:** Set reg_alpha=1.0. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.624103
**Current best (Week 5 block):** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624103 > 0.622824 (+0.20%). Strong L1 penalty removes useful signal.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05). Week 5 block complete.

---

### Run 031 — 2026-05-11
**Change:** Set n_estimators=200. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623647
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.623647 > 0.622824 (+0.13%). More trees at lr=0.05 overfit; 200 trees worse than 100.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 032 — 2026-05-11
**Change:** Set n_estimators=150. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623662
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.623662 > 0.622824 (+0.13%). Nearly identical to Run 031; n_estimators >100 consistently hurts at lr=0.05.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 033 — 2026-05-11
**Change:** Set n_estimators=75 (second queue item labeled 032). max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.623293
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.623293 > 0.622824 (+0.08%). Fewer trees also hurt; 100 is optimal at lr=0.05.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 034 — 2026-05-11
**Change:** Set max_depth=3, lr=0.05 (lr already accepted; actual change is max_depth=2→3). 23-feature set unchanged.
**Val log loss:** 0.624253
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624253 > 0.622824 (+0.23%). max_depth=3 overfits on this feature set regardless of lr.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 035 — 2026-05-11
**Change:** Set learning_rate=0.03. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.624499
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624499 > 0.622824 (+0.27%). lr=0.03 is worse than lr=0.05; confirms 0.05 is optimal at 100 trees.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 036 — 2026-05-11
**Change:** Set learning_rate=0.07. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.624293
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624293 > 0.622824 (+0.24%). Both directions from 0.05 are worse; 0.05 is optimal at 100 trees.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 037 — 2026-05-11
**Change:** Set learning_rate=0.02. max_depth=2, 23-feature set unchanged.
**Val log loss:** 0.630057
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Significant regression — 0.630057 > 0.622824 (+1.17%). lr=0.02 underfits with 100 trees; model cannot converge.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05).

---

### Run 038 — 2026-05-11
**Change:** Set min_child_weight=3. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.622155
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.11% (0.622824 → 0.622155) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 039 — 2026-05-11
**Change:** Set min_child_weight=4. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.621710
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.18% (0.622824 → 0.621710) — below the 0.25% minimum threshold. Closest near-miss in the block.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 040 — 2026-05-11
**Change:** Set subsample=0.7. max_depth=2, lr=0.05, 23-feature set unchanged.
**Val log loss:** 0.625850
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.625850 > 0.622824 (+0.49%). subsample=0.7 worse than 0.6 and 0.8; all row subsampling hurts.
**Decision:** Rejected. train.py reverted to Run 019 state (max_depth=2, lr=0.05). Week 6 block complete.

---

### Run 041 — 2026-05-11
**Change:** Removed all window-16 rolling features (pts_scored_16, pts_allowed_16, win_pct_16 for home and away). 23 → 17 features.
**Val log loss:** 0.621545
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.205% (0.622824 → 0.621545) — below the 0.25% threshold by only 0.000277. Narrowest near-miss of all runs.
**Decision:** Rejected. train.py reverted to full 23-feature set. best_meta.json restored to run_24 (0.622824).

---

### Run 042 — 2026-05-11
**Change:** Removed all window-4 rolling features (pts_scored_4, pts_allowed_4, win_pct_4 for home and away). 23 → 17 features.
**Val log loss:** 0.626109
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.626109 > 0.622824 (+0.53%). Short-window features carry signal; removing them hurts.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 043 — 2026-05-11
**Change:** Removed all pts_allowed rolling features (home/away pts_allowed_4/8/16). 23 → 17 features.
**Val log loss:** 0.621625
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.192% (0.622824 → 0.621625) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to full 23-feature set. best_meta.json restored to run_24 (0.622824).

---

### Run 044 — 2026-05-11
**Change:** Removed all pts_scored rolling features (home/away pts_scored_4/8/16). 23 → 17 features.
**Val log loss:** 0.625224
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.625224 > 0.622824 (+0.38%). pts_scored carries more signal than pts_allowed.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 045 — 2026-05-11
**Change:** Removed all pts_scored and pts_allowed features; kept baseline + win_pct_4/8/16 + rest_days. 23 → 11 features.
**Val log loss:** 0.622987
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Marginal regression — 0.622987 > 0.622824 (+0.03%). Remarkable: 11 features nearly match 23; scoring adds almost no signal.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 046 — 2026-05-11
**Change:** Removed all away rolling features (away_pts_scored/allowed_4/8/16, away_win_pct_4/8/16). 23 → 14 features.
**Val log loss:** 0.622828
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression of 0.000004 — functionally identical. Away rolling features add near-zero signal.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 047 — 2026-05-11
**Change:** Removed all home rolling features (home_pts_scored/allowed_4/8/16, home_win_pct_4/8/16). 23 → 14 features.
**Val log loss:** 0.633376
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Significant regression — 0.633376 > 0.622824 (+1.69%). Home rolling features are far more informative than away features.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 048 — 2026-05-11
**Change:** Removed home_rest_days and away_rest_days. 23 → 21 features. rest_diff baseline retained.
**Val log loss:** 0.621985
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.135% (0.622824 → 0.621985) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to full 23-feature set. best_meta.json restored to run_24 (0.622824).

---

### Run 049 — 2026-05-11
**Change:** Features reduced to baseline + home_win_pct_8 + away_win_pct_8 only. 23 → 5 features.
**Val log loss:** 0.624457
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624457 > 0.622824 (+0.26%). Too sparse; loses more signal than the 11-feature set (Run 045).
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 050 — 2026-05-11
**Change:** Features reduced to baseline + home/away_pts_scored_8 + home/away_pts_allowed_8. 23 → 7 features.
**Val log loss:** 0.624329
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.624329 > 0.622824 (+0.24%). 8-game scoring window alone insufficient; better than 5-feature set but still regresses.
**Decision:** Rejected. train.py reverted to full 23-feature set.

---

### Run 051 — 2026-05-11
**Change:** Removed all _16 rolling features + set min_child_weight=4. 23 → 17 features.
**Val log loss:** 0.621506
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.212% (0.622824 → 0.621506) — missed threshold by 0.000238. Less than additive combination.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 052 — 2026-05-11
**Change:** Removed all _16 rolling features AND all pts_allowed features. 23 → 13 features.
**Val log loss:** 0.621487
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.215% (0.622824 → 0.621487) — missed threshold by 0.000219. Best result so far but still below.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 053 — 2026-05-11
**Change:** Removed all pts_allowed features + set min_child_weight=4. 23 → 17 features.
**Val log loss:** 0.622266
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.09% only. Worse than either change alone — negative interaction.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 054 — 2026-05-11
**Change:** Removed all _16 rolling features + all pts_allowed features + set min_child_weight=4. 23 → 13 features.
**Val log loss:** 0.622366
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Only 0.07% improvement — worse than any two-way combo. Diminishing returns with combinations.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 055 — 2026-05-11
**Change:** Removed all _16 rolling features + set colsample_bytree=0.6. 23 → 17 features.
**Val log loss:** 0.622353
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Only 0.076% improvement — far less than additive. Column subsampling negates feature pruning benefit.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 056 — 2026-05-11
**Change:** Removed all _16 rolling features AND home/away_rest_days. 23 → 15 features.
**Val log loss:** 0.621538
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.206% (0.622824 → 0.621538) — missed threshold by 0.000270.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 057 — 2026-05-11
**Change:** Removed all _16 rolling features + all pts_allowed features + home/away_rest_days. 23 → 11 features.
**Val log loss:** 0.622442
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Only 0.061% improvement. Three-way feature removals show strongly diminishing returns.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 058 — 2026-05-11
**Change:** Removed all pts_allowed features + set colsample_bytree=0.6. 23 → 17 features.
**Val log loss:** 0.622866
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Marginal regression (+0.006%). colsample_bytree cancels the pts_allowed removal benefit entirely.
**Decision:** Rejected. train.py reverted to Run 019 state.

---

### Run 059 — 2026-05-11
**Change:** Removed all _16 rolling features + all pts_allowed features + set min_child_weight=4 + colsample_bytree=0.6. 23 → 13 features.
**Val log loss:** 0.621703
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Improvement of 0.180% — worse than Run 052 (two-way combo). Adding more changes actively hurts.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 060 — 2026-05-11
**Change:** Removed all _16 rolling features + all pts_allowed features + home/away_rest_days + set min_child_weight=4. 23 → 11 features.
**Val log loss:** 0.622918
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression (+0.015%). Most aggressive combination is worst result — four-way changes degrade the model. Best combination remains Run 052 (two-way: no window-16 + no pts_allowed).
**Decision:** Rejected. train.py reverted to Run 019 state.

---

### Run 061 — 2026-05-18
**Change:** Added early_stopping_rounds=10, n_estimators=500 to Run 019 config (max_depth=2, lr=0.05). eval_set=[(X_val, y_val)] passed at fit time; CV folds use val fold as eval_set. 23 features unchanged.
**Val log loss:** 0.622517
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Improvement:** 0.049% (0.622824 → 0.622517) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 062 — 2026-05-18
**Change:** Same as 061 but learning_rate=0.03 (early_stopping_rounds=10, n_estimators=500, max_depth=2). eval_set=[(X_val, y_val)] at fit; CV folds use val fold as eval_set. 23 features unchanged.
**Val log loss:** 0.622536
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Improvement:** 0.046% (0.622824 → 0.622536) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state. best_meta.json restored to run_24 (0.622824).

---

### Run 063 — 2026-05-18
**Change:** Added home_win_pct_32 and away_win_pct_32 (32-game rolling win%) to Run 019 config. 23 → 25 features. window=32 added to compute_rolling_features.
**Val log loss:** 0.621702
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Improvement:** 0.180% (0.622824 → 0.621702) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 019 state (windows=[4,8,16], 23 features). best_meta.json restored to run_24 (0.622824).

---

### Run 064 — 2026-05-18
**Change:** Added home/away_pts_scored_32 and home/away_pts_allowed_32 (32-game rolling pts scored/allowed) to Run 019 config. 23 → 27 features. window=32 added to compute_rolling_features.
**Val log loss:** 0.625513
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.625513 > 0.622824 (+0.43%). 32-game scoring features add noise rather than signal; contrast with Run 063 (32-game win% was a near-miss improvement).
**Decision:** Rejected. train.py reverted to Run 019 state (windows=[4,8,16], 23 features).

---

### Run 065 — 2026-05-18
**Change:** Added all 32-game rolling features (home/away win_pct_32, pts_scored_32, pts_allowed_32) to Run 019 config. 23 → 29 features (spec noted 27, actual count is 29). windows expanded to [4,8,16,32].
**Val log loss:** 0.625513
**Current best:** 0.622824 (Run 019)
**Threshold required:** 0.621268 (current_best × 0.9975)
**Result:** Regression — 0.625513 > 0.622824 (+0.43%). Identical to Run 064; adding win_pct_32 on top of the scoring_32 features provides no additional benefit. 32-game scoring features dominate and hurt regardless of whether win% is included.
**Decision:** Rejected. train.py reverted to Run 019 state (windows=[4,8,16], 23 features).

---

### Run 067 — 2026-05-18
**Change:** Ensemble of Run 019 XGBoost and Run 002 LR with weights 0.35 XGB / 0.65 LR (vs 0.5/0.5 in Run 066).
**Val log loss:** 0.617921
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Improvement:** 0.130% (0.618727 → 0.617921) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 066 state (weights 0.5/0.5). best_meta.json restored to run_71 (0.618727).

---

### Run 068 — 2026-05-18
**Change:** Swapped model to LightGBM (max_depth=2, learning_rate=0.05, n_estimators=100). Same 23 features as Run 019. (lightgbm installed via pip before run.)
**Val log loss:** 0.622597
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.622597 > 0.618727 (+0.62%). LightGBM with equivalent config performs worse than the XGBoost+LR ensemble and slightly worse than XGBoost alone (Run 019: 0.622824 comparison inconclusive — new best is ensemble).
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 069 — 2026-05-18
**Change:** Swapped model to Random Forest (n_estimators=300, max_depth=6). Same 23 features as Run 019.
**Val log loss:** 0.621606
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.621606 > 0.618727 (+0.46%). Random Forest with these parameters does not match the XGBoost+LR ensemble.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 070 — 2026-05-18
**Change:** Added colsample_bytree=0.6 to the XGBoost component of Run 066 ensemble (XGB max_depth=2, lr=0.05, cbt=0.6 + LR, weights 0.5/0.5).
**Val log loss:** 0.618306
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Improvement:** 0.068% (0.618727 → 0.618306) — below the 0.25% minimum threshold.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state (no colsample_bytree). best_meta.json restored to run_71 (0.618727).

---

### Run 071 — 2026-05-18
**Change:** XGBoost Run 019 config (max_depth=2, lr=0.05); train probe on all 23 features, select top 10 by feature_importances_, retrain on those 10.
**Top 10 selected:** elo_diff, home_win_pct_8, home_win_pct_4, home_win_pct_16, away_pts_scored_16, away_pts_scored_8, home_pts_scored_8, away_win_pct_8, away_pts_scored_4, home_pts_scored_16
**Val log loss:** 0.625539
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.625539 > 0.618727 (+1.10%). Aggressive feature pruning to top 10 removes too much signal; notably home_game and home_rest_days had zero importance in the probe model.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 072 — 2026-05-18
**Change:** XGBoost Run 019 config (max_depth=2, lr=0.05); train probe on all 23 features, select top 15 by feature_importances_, retrain on those 15.
**Top 15 selected:** elo_diff, home_win_pct_8/4/16, away_pts_scored_16/8/4, home_pts_scored_8/16, away_win_pct_8, home_pts_allowed_16/4, home_pts_scored_4, away_pts_allowed_4, away_win_pct_16
**Val log loss:** 0.623045
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.623045 > 0.618727 (+0.69%). Top 15 is better than top 10 (0.625539) but still below both the current best (0.618727) and the old Run 019 baseline (0.622824). Feature importance-based pruning consistently hurts on this dataset.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 073 — 2026-05-18
**Change:** 3-model ensemble: XGBoost (Run 019, 23 features) + LR (Run 002, 15 features) + Random Forest (n_estimators=300, max_depth=6, 23 features). Equal weights (1/3 each).
**Val log loss:** 0.619347
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.619347 > 0.618727 (+0.10%). Adding Random Forest dilutes the stronger XGB+LR signal. RF alone (Run 069: 0.621606) drags down the ensemble.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 074 — 2026-05-18
**Change:** 3-model ensemble: XGBoost (Run 019, 23 features) + LR (Run 002, 15 features) + LightGBM (max_depth=2, lr=0.05, n_estimators=100, 23 features). Equal weights (1/3 each).
**Val log loss:** 0.619805
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Result:** Regression — 0.619805 > 0.618727 (+0.17%). Adding LightGBM also dilutes — LightGBM alone (Run 068: 0.622597) is weaker and brings the ensemble down vs the 2-model XGB+LR.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state.

---

### Run 075 — 2026-05-18
**Change:** Grid search weights for Run 066 ensemble (XGB+LR). Tested: (0.4/0.6)=0.618168, (0.3/0.7)=0.617695, (0.6/0.4)=0.619373. Best: XGB=0.3, LR=0.7.
**Val log loss:** 0.617695 (best from grid)
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Improvement:** 0.167% (0.618727 → 0.617695) — below the 0.25% minimum threshold. Missed by 0.000515.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state. best_meta.json restored to run_71 (0.618727).

---

### Run 076 — 2026-05-18
**Change:** Ensemble Run 019 (XGBoost) + Run 002 (LR) with weights 0.2 XGB / 0.8 LR.
**Val log loss:** 0.617311
**Current best:** 0.618727 (Run 066)
**Threshold required:** 0.617180 (current_best × 0.9975)
**Improvement:** 0.229% (0.618727 → 0.617311) — below the 0.25% minimum threshold. Missed by 0.000131. Narrowest near-miss of all runs.
**Decision:** Rejected. train.py reverted to Run 066 ensemble state. best_meta.json restored to run_71 (0.618727).
