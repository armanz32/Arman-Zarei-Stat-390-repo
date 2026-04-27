Evaluation Board

Summary

Val Log Loss (2024) 
Baseline (ELO diff, home, rest): 0.623589
Current best: 0.623589 |==
Best model type: Logistic Regression
Best features: ELO diff, home game, rest diff
2% improvement threshold: 0.611117
2025 test set: locked

Experiment Table

| Run | Model | Features | Val Loss | CV Mean ± Std | Δ vs Baseline | Accepted? |
|-----|-------|----------|----------|---------------|---------------|-----------|
| 000 | Logistic Regression | ELO diff, home, rest | 0.623589 | 0.648181 ± 0.005565 | — | Baseline |
| 001 | Logistic Regression | + rolling win% (4/8/16 home+away) | 0.619831 | 0.637591 ± 0.006189 | -0.60% | ❌ Rejected (<2%) |
| 002 | Logistic Regression | Groups A+B+C (15 features) | 0.616790 | 0.633451 ± 0.004513 | -1.09% | ❌ Rejected (<2%) |
| 003 | XGBoost | Groups A+B+C (15 features) | 0.628627 | 0.653370 ± 0.007373 | +0.81% | ❌ Rejected (regression) |
| 004 | XGBoost (d=3, n=100) | Groups A+B+C (15 features) | 0.619820 | 0.640998 ± 0.004798 | -0.60% | ❌ Rejected (<2%) |