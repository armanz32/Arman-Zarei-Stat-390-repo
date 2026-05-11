Evaluation Board

Summary

Val Log Loss (2024) 
Baseline (ELO diff, home, rest): 0.702775
Current best: 0.622824 (Run 019, XGBoost max_depth=2 lr=0.05) |== [Week 5 block complete]
Best model type: XGBoost
Best features: elo_diff, home_game, rest_diff + rolling pts scored/allowed 4/8/16 + rolling win% 4/8/16 + home_rest_days, away_rest_days (23 features)
Best config: max_depth=2, learning_rate=0.05, n_estimators=100 (all other params default)
2025 test set: locked

Experiment Table

| Run | Model | Features | Val Loss | CV Mean ± Std | Δ vs Baseline | Accepted? |
|-----|-------|----------|----------|---------------|---------------|-----------|
| 000 | Logistic Regression | ELO diff, home, rest | 0.623589 | 0.648181 ± 0.005565 | — | Baseline |
| 001 | Logistic Regression | + rolling win% (4/8/16 home+away) | 0.619831 | 0.637591 ± 0.006189 | -0.60% | ❌ Rejected (<1.5%) |
| 002 | Logistic Regression | Groups dA+B+C (15 features) | 0.616790 | 0.633451 ± 0.004513 | -1.09% | ❌ Rejected (<1.5%) |
| 003 | XGBoost | Groups A+B+C (15 features) | 0.628627 | 0.653370 ± 0.007373 | +0.81% | ❌ Rejected (regression) |
| 004 | XGBoost (d=3, n=100) | Groups A+B+C (15 features) | 0.619820 | 0.640998 ± 0.004798 | -0.60% | ❌ Rejected (<1.5%) |
| 005 | Logistic Regression | + elo_diff × home_win_pct_8 (13 features) | 0.623928 | 0.640814 ± 0.007667 | +0.05% | ❌ Rejected (regression) |
| 006 | Logistic Regression | + elo_diff² (13 features) | 0.622981 | 0.640554 ± 0.007697 | -0.10% | ❌ Rejected (<1.5%) |
| 007 | Logistic Regression | + rest_diff × away_score_avg_8 (13 features) | 0.624205 | 0.641083 ± 0.008146 | +0.10% | ❌ Rejected (regression) |
| 008 | Logistic Regression | + elo_diff_bin (5 quantile bins, 13 features) | 0.625514 | 0.640376 ± 0.007937 | +0.31% | ❌ Rejected (regression) |
| D01 | Logistic Regression | Diagnostic — baseline + rolling (12 features, no engineered) | 0.624245 | 0.640833 ± 0.007921 | +0.11% vs baseline | Diagnostic only |
| 009 | Logistic Regression | baseline + elo_diff² (4 features) | 0.622191 | 0.647926 ± 0.005452 | -0.22% | ❌ Rejected (<1.5%) |
| 010 | Logistic Regression | elo_diff + home_game only (2 features) | 0.622446 | 0.648547 ± 0.006189 | -0.18% | ❌ Rejected (<1.5%) |
| 011 | XGBoost (all defaults) | elo_diff, home_game, rest_diff (3 features) | 0.665846 | 0.697022 ± 0.009262 | +6.78% | ✅ Accepted (required Week 5 baseline) |
| 011b | XGBoost (all defaults) | baseline + rolling pts scored/allowed 4/8/16, rolling win% 4/8/16, rest days (23 features) | 0.702775 | 0.767613 ± 0.022218 | +12.70% | ✅ Accepted (required full-feature Week 5 baseline) |
| 012 | XGBoost (max_depth=2) | same 23 features | 0.647696 | 0.649534 ± 0.010045 | -7.84% vs 011b | ✅ Accepted |
| 013 | XGBoost (max_depth=4) | same 23 features | 0.676621 | 0.695058 ± 0.015476 | +4.47% vs 012 | ❌ Rejected (regression) |
| 014 | XGBoost (max_depth=6) | same 23 features | 0.702775 | 0.767613 ± 0.022218 | +8.49% vs 012 | ❌ Rejected (regression; max_depth=6 is XGBoost default) |
| 015 | XGBoost (max_depth=2, n_estimators=100) | same 23 features | 0.647696 | 0.649534 ± 0.010045 | 0.00% vs 012 | ❌ Rejected (n_estimators=100 is XGBoost default; identical result) |
| 016 | XGBoost (max_depth=2, n_estimators=300) | same 23 features | 0.663226 | 0.674836 ± 0.013239 | +2.39% vs 012 | ❌ Rejected (regression) |
| 017 | XGBoost (max_depth=2, n_estimators=500) | same 23 features | 0.687740 | 0.701497 ± 0.016145 | +6.19% vs 012 | ❌ Rejected (regression) |
| 018 | XGBoost (max_depth=2, lr=0.01) | same 23 features | 0.643467 | 0.653252 ± 0.004871 | -0.65% vs 012 | ✅ Accepted |
| 019 | XGBoost (max_depth=2, lr=0.05) | same 23 features | 0.622824 | 0.635533 ± 0.007571 | -3.19% vs 018 | ✅ Accepted (first to beat logistic regression baseline) |
| 020 | XGBoost (max_depth=2, lr=0.3) | same 23 features | 0.647696 | 0.649534 ± 0.010045 | +3.99% vs 019 | ❌ Rejected (lr=0.3 is XGBoost default; identical to Run 012) |
| 021 | XGBoost (max_depth=2, lr=0.05, subsample=0.6) | same 23 features | 0.623504 | 0.634973 ± 0.008547 | +0.11% vs 019 | ❌ Rejected (<0.25% threshold) |
| 022 | XGBoost (max_depth=2, lr=0.05, subsample=0.8) | same 23 features | 0.623846 | 0.634881 ± 0.008767 | +0.16% vs 019 | ❌ Rejected (<0.25% threshold) |
| 023 | XGBoost (max_depth=2, lr=0.05, colsample_bytree=0.6) | same 23 features | 0.621875 | 0.635448 ± 0.007824 | -0.15% vs 019 | ❌ Rejected (<0.25% threshold) |
| 024 | XGBoost (max_depth=2, lr=0.05, colsample_bytree=0.8) | same 23 features | 0.624324 | 0.635505 ± 0.007819 | +0.24% vs 019 | ❌ Rejected (regression) |
| 025 | XGBoost (max_depth=2, lr=0.05, min_child_weight=2) | same 23 features | 0.622572 | 0.635425 ± 0.007687 | -0.04% vs 019 | ❌ Rejected (<0.25% threshold) |
| 026 | XGBoost (max_depth=2, lr=0.05, min_child_weight=5) | same 23 features | 0.622013 | 0.635316 ± 0.007925 | -0.13% vs 019 | ❌ Rejected (<0.25% threshold) |
| 027 | XGBoost (max_depth=2, lr=0.05, reg_lambda=1) | same 23 features | 0.622824 | 0.635533 ± 0.007571 | 0.00% vs 019 | ❌ Rejected (reg_lambda=1 is XGBoost default; identical result) |
| 028 | XGBoost (max_depth=2, lr=0.05, reg_lambda=5) | same 23 features | 0.622305 | 0.635578 ± 0.007474 | -0.08% vs 019 | ❌ Rejected (<0.25% threshold) |
| 029 | XGBoost (max_depth=2, lr=0.05, reg_alpha=0.1) | same 23 features | 0.623085 | 0.635582 ± 0.007679 | +0.04% vs 019 | ❌ Rejected (regression) |
| 030 | XGBoost (max_depth=2, lr=0.05, reg_alpha=1.0) | same 23 features | 0.624103 | 0.635321 ± 0.007747 | +0.20% vs 019 | ❌ Rejected (regression) |
| 031 | XGBoost (max_depth=2, lr=0.05, n_estimators=200) | same 23 features | 0.623647 | 0.637780 ± 0.008369 | +0.13% vs 019 | ❌ Rejected (regression) |
| 032 | XGBoost (max_depth=2, lr=0.05, n_estimators=150) | same 23 features | 0.623662 | 0.636409 ± 0.007941 | +0.13% vs 019 | ❌ Rejected (regression) |
| 033 | XGBoost (max_depth=2, lr=0.05, n_estimators=75) | same 23 features | 0.623293 | 0.636497 ± 0.007465 | +0.08% vs 019 | ❌ Rejected (regression) |
| 034 | XGBoost (max_depth=3, lr=0.05) | same 23 features | 0.624253 | 0.636845 ± 0.006990 | +0.23% vs 019 | ❌ Rejected (regression) |
| 035 | XGBoost (max_depth=2, lr=0.03) | same 23 features | 0.624499 | 0.638115 ± 0.007225 | +0.27% vs 019 | ❌ Rejected (regression) |
| 036 | XGBoost (max_depth=2, lr=0.07) | same 23 features | 0.624293 | 0.636346 ± 0.008184 | +0.24% vs 019 | ❌ Rejected (regression) |
| 037 | XGBoost (max_depth=2, lr=0.02) | same 23 features | 0.630057 | 0.642843 ± 0.006562 | +1.17% vs 019 | ❌ Rejected (regression; underfitting at lr=0.02 with 100 trees) |
| 038 | XGBoost (max_depth=2, lr=0.05, min_child_weight=3) | same 23 features | 0.622155 | 0.635558 ± 0.007767 | -0.11% vs 019 | ❌ Rejected (<0.25% threshold) |
| 039 | XGBoost (max_depth=2, lr=0.05, min_child_weight=4) | same 23 features | 0.621710 | 0.635602 ± 0.007853 | -0.18% vs 019 | ❌ Rejected (<0.25% threshold) |
| 040 | XGBoost (max_depth=2, lr=0.05, subsample=0.7) | same 23 features | 0.625850 | 0.633866 ± 0.008131 | +0.49% vs 019 | ❌ Rejected (regression) |
| 041 | XGBoost (max_depth=2, lr=0.05) | 17 features: no window-16 | 0.621545 | 0.635023 ± 0.007600 | -0.21% vs 019 | ❌ Rejected (<0.25% threshold) |
| 042 | XGBoost (max_depth=2, lr=0.05) | 17 features: no window-4 | 0.626109 | 0.637144 ± 0.009038 | +0.53% vs 019 | ❌ Rejected (regression) |
| 043 | XGBoost (max_depth=2, lr=0.05) | 17 features: no pts_allowed | 0.621625 | 0.638089 ± 0.007925 | -0.19% vs 019 | ❌ Rejected (<0.25% threshold) |
| 044 | XGBoost (max_depth=2, lr=0.05) | 17 features: no pts_scored | 0.625224 | 0.642175 ± 0.007643 | +0.38% vs 019 | ❌ Rejected (regression) |
| 045 | XGBoost (max_depth=2, lr=0.05) | 11 features: baseline + win_pct + rest_days only | 0.622987 | 0.642895 ± 0.008895 | +0.03% vs 019 | ❌ Rejected (regression) |
| 046 | XGBoost (max_depth=2, lr=0.05) | 14 features: no away rolling | 0.622828 | 0.643120 ± 0.008790 | +0.0006% vs 019 | ❌ Rejected (regression; functionally identical) |
| 047 | XGBoost (max_depth=2, lr=0.05) | 14 features: no home rolling | 0.633376 | 0.647390 ± 0.007312 | +1.69% vs 019 | ❌ Rejected (regression; home features critical) |
| 048 | XGBoost (max_depth=2, lr=0.05) | 21 features: no rest_days | 0.621985 | 0.635718 ± 0.007622 | -0.14% vs 019 | ❌ Rejected (<0.25% threshold) |
| 049 | XGBoost (max_depth=2, lr=0.05) | 5 features: baseline + win_pct_8 only | 0.624457 | 0.641087 ± 0.010208 | +0.26% vs 019 | ❌ Rejected (regression) |
| 050 | XGBoost (max_depth=2, lr=0.05) | 7 features: baseline + pts_scored_8 + pts_allowed_8 | 0.624329 | 0.638002 ± 0.007817 | +0.24% vs 019 | ❌ Rejected (regression) |
| 051 | XGBoost (max_depth=2, lr=0.05, mcw=4) | 17 features: no window-16 | 0.621506 | 0.634945 ± 0.007781 | -0.21% vs 019 | ❌ Rejected (<0.25% threshold; missed by 0.000238) |
| 052 | XGBoost (max_depth=2, lr=0.05) | 13 features: no window-16, no pts_allowed | 0.621487 | 0.637270 ± 0.007484 | -0.21% vs 019 | ❌ Rejected (<0.25% threshold; missed by 0.000219) |
| 053 | XGBoost (max_depth=2, lr=0.05, mcw=4) | 17 features: no pts_allowed | 0.622266 | 0.638266 ± 0.007660 | -0.09% vs 019 | ❌ Rejected (<0.25% threshold) |
| 054 | XGBoost (max_depth=2, lr=0.05, mcw=4) | 13 features: no window-16, no pts_allowed | 0.622366 | 0.637357 ± 0.007501 | -0.07% vs 019 | ❌ Rejected (<0.25% threshold) |
| 055 | XGBoost (max_depth=2, lr=0.05, cbt=0.6) | 17 features: no window-16 | 0.622353 | 0.634931 ± 0.007963 | -0.08% vs 019 | ❌ Rejected (<0.25% threshold) |
| 056 | XGBoost (max_depth=2, lr=0.05) | 15 features: no window-16, no rest_days | 0.621538 | 0.634852 ± 0.007690 | -0.21% vs 019 | ❌ Rejected (<0.25% threshold; missed by 0.000270) |
| 057 | XGBoost (max_depth=2, lr=0.05) | 11 features: no window-16, no pts_allowed, no rest_days | 0.622442 | 0.637333 ± 0.007656 | -0.06% vs 019 | ❌ Rejected (<0.25% threshold) |
| 058 | XGBoost (max_depth=2, lr=0.05, cbt=0.6) | 17 features: no pts_allowed | 0.622866 | 0.637399 ± 0.008561 | +0.006% vs 019 | ❌ Rejected (regression) |
| 059 | XGBoost (max_depth=2, lr=0.05, mcw=4, cbt=0.6) | 13 features: no window-16, no pts_allowed | 0.621703 | 0.636615 ± 0.008007 | -0.18% vs 019 | ❌ Rejected (<0.25% threshold) |
| 060 | XGBoost (max_depth=2, lr=0.05, mcw=4) | 11 features: no window-16, no pts_allowed, no rest_days | 0.622918 | 0.637302 ± 0.007721 | +0.02% vs 019 | ❌ Rejected (regression) |
