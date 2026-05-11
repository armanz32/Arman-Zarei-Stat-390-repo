Evaluation Board

Summary

Val Log Loss (2024) 
Baseline (ELO diff, home, rest): 0.623589
Current best: 0.623589 |==
Best model type: Logistic Regression
Best features: ELO diff, home game, rest diff
1.5% improvement threshold: 0.614135
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
