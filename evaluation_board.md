Evaluation Board

Summary

Val Log Loss (2024) 
Baseline (ELO diff, home, rest): 0.702775
Current best: 0.616811 (Run 077, pure LR on 15 features — Groups A+B+C) |== [Week 6 block in progress]
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
| 061 | XGBoost (max_depth=2, lr=0.05, n_estimators=500, early_stopping_rounds=10) | 23 features (Run 019 feature set) | 0.622517 | 0.635222 ± 0.007607 | -0.05% vs 019 | ❌ Rejected (<0.25% threshold) |
| 062 | XGBoost (max_depth=2, lr=0.03, n_estimators=500, early_stopping_rounds=10) | 23 features (Run 019 feature set) | 0.622536 | 0.635206 ± 0.007766 | -0.05% vs 019 | ❌ Rejected (<0.25% threshold) |
| 063 | XGBoost (max_depth=2, lr=0.05) | 25 features: Run 019 + home/away_win_pct_32 | 0.621702 | 0.635599 ± 0.007759 | -0.18% vs 019 | ❌ Rejected (<0.25% threshold) |
| 064 | XGBoost (max_depth=2, lr=0.05) | 27 features: Run 019 + home/away_pts_scored_32 + home/away_pts_allowed_32 | 0.625513 | 0.635555 ± 0.007883 | +0.43% vs 019 | ❌ Rejected (regression) |
| 065 | XGBoost (max_depth=2, lr=0.05) | 29 features: Run 019 + all 32-game rolling (win%, pts scored, pts allowed) | 0.625513 | 0.635648 ± 0.007995 | +0.43% vs 019 | ❌ Rejected (regression; identical to Run 064) |
| 066 | Ensemble XGBoost(019)+LR(002) w=0.5/0.5 | XGB: 23 features; LR: 15 features (Groups A+B+C) | 0.618727 | 0.633352 ± 0.008020 | -0.66% vs 019 | ✅ Accepted (new best: 0.618727) |
| 067 | Ensemble XGBoost(019)+LR(002) w=0.35/0.65 | XGB: 23 features; LR: 15 features (Groups A+B+C) | 0.617921 | 0.633362 ± 0.008195 | -0.13% vs 066 | ❌ Rejected (<0.25% threshold) |
| 068 | LightGBM (max_depth=2, lr=0.05, n_estimators=100) | 23 features (Run 019 feature set) | 0.622597 | 0.635452 ± 0.007721 | +0.62% vs 066 | ❌ Rejected (regression) |
| 069 | Random Forest (n_estimators=300, max_depth=6) | 23 features (Run 019 feature set) | 0.621606 | 0.633781 ± 0.007147 | +0.46% vs 066 | ❌ Rejected (regression) |
| 070 | Ensemble XGB(cbt=0.6)+LR w=0.5/0.5 | XGB: 23 features (cbt=0.6); LR: 15 features | 0.618306 | 0.633391 ± 0.008126 | -0.07% vs 066 | ❌ Rejected (<0.25% threshold) |
| 071 | XGBoost (max_depth=2, lr=0.05) | Top 10 features by feature_importances_ | 0.625539 | 0.637595 ± 0.009236 | +1.10% vs 066 | ❌ Rejected (regression) |
| 072 | XGBoost (max_depth=2, lr=0.05) | Top 15 features by feature_importances_ | 0.623045 | 0.634800 ± 0.007600 | +0.69% vs 066 | ❌ Rejected (regression) |
| 073 | Ensemble XGB+LR+RF w=0.33 each | XGB: 23 feat; LR: 15 feat; RF: 23 feat | 0.619347 | 0.633012 ± 0.007718 | +0.10% vs 066 | ❌ Rejected (regression) |
| 074 | Ensemble XGB+LR+LightGBM w=0.33 each | XGB: 23 feat; LR: 15 feat; LightGBM: 23 feat | 0.619805 | 0.633645 ± 0.007907 | +0.17% vs 066 | ❌ Rejected (regression) |
| 075 | Ensemble XGB+LR weight grid search (best: 0.3/0.7) | XGB: 23 feat; LR: 15 feat | 0.617695 | 0.633435 ± 0.008258 | -0.17% vs 066 | ❌ Rejected (<0.25% threshold; missed by 0.000515) |
| 076 | Ensemble XGB+LR w=0.2/0.8 | XGB: 23 feat; LR: 15 feat | 0.617311 | 0.633685 ± 0.008393 | -0.23% vs 066 | ❌ Rejected (<0.25% threshold; missed by 0.000131) |
| 077 | Ensemble XGB+LR w=0.0/1.0 (pure LR) | LR: 15 features (Groups A+B+C) | 0.616811 | 0.634619 ± 0.008704 | -0.31% vs 066 | ✅ Accepted (new best: 0.616811) |
| 078 | Logistic Regression C=0.1 | LR: 15 features (Groups A+B+C) | 0.616832 | 0.634450 ± 0.008692 | +0.003% vs 077 | ❌ Rejected (regression) |
| 079 | Logistic Regression C=0.5 | LR: 15 features (Groups A+B+C) | 0.616812 | 0.634598 ± 0.008704 | +0.000002% vs 077 | ❌ Rejected (regression; functionally identical) |
| 080 | Logistic Regression, no away rolling features | LR: 9 features (baseline + home_pts_scored_4/8/16 + home_win_pct_4/8/16) | 0.616564 | 0.643857 ± 0.009477 | -0.040% vs 077 | ❌ Rejected (<0.25% threshold) |
| 081 | Logistic Regression, differential features | LR: 9 features (baseline + win_pct_diff_4/8/16 + pts_scored_diff_4/8/16) | 0.618701 | 0.633577 ± 0.008656 | +0.28% vs 077 | ❌ Rejected (regression) |
| 082 | Logistic Regression + rest_days (17 features) | LR: 17 features (Groups A+B+C + home_rest_days + away_rest_days) | 0.616490 | 0.634783 ± 0.008574 | -0.052% vs 077 | ❌ Rejected (<0.25% threshold) |
| 083 | Logistic Regression C=2.0 | LR: 15 features (Groups A+B+C) | 0.616810 | 0.634630 ± 0.008704 | -0.0002% vs 077 | ❌ Rejected (<0.25% threshold; functionally identical) |
| 084 | Logistic Regression C=5.0 | LR: 15 features (Groups A+B+C) | 0.616810 | 0.634637 ± 0.008702 | -0.0002% vs 077 | ❌ Rejected (<0.25% threshold; identical to C=2.0) |
| 085 | Logistic Regression L1 penalty (liblinear) | LR: 15 features (Groups A+B+C) | 0.616755 | 0.634549 ± 0.008700 | -0.009% vs 077 | ❌ Rejected (<0.25% threshold) |
| 086 | Logistic Regression ElasticNet l1_ratio=0.5 (saga) | LR: 15 features (Groups A+B+C) | 0.616775 | 0.634583 ± 0.008703 | -0.006% vs 077 | ❌ Rejected (<0.25% threshold) |
| 087 | Logistic Regression penalty=None (no regularization) | LR: 15 features (Groups A+B+C) | 0.616810 | 0.634642 ± 0.008702 | -0.0002% vs 077 | ❌ Rejected (<0.25% threshold; identical to C≥2.0) |
| 088 | Logistic Regression + rolling point differential (margin_4/8/16) | LR: 21 features (Groups A+B+C + home/away_margin_4/8/16) | 0.625782 | 0.632255 ± 0.008843 | +1.45% vs 077 | ❌ Rejected (regression; margin collinear with pts_scored/allowed) |
| 089 | Logistic Regression, margin replaces pts_scored | LR: 15 features (baseline + home/away_margin_4/8/16 + home/away_win_pct_4/8/16) | 0.627550 | 0.633241 ± 0.008388 | +1.74% vs 077 | ❌ Rejected (regression; pts_scored + win_pct separately more informative than margin alone) |
| 090 | Logistic Regression + win streak features | LR: 17 features (Groups A+B+C + home_win_streak + away_win_streak) | 0.617948 | 0.634581 ± 0.008429 | +0.18% vs 077 | ❌ Rejected (regression; streak adds noise, not signal, on top of win% features) |
