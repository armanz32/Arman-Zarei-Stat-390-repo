Arman Zarei — Stat 390 NFL Game Prediction

Can an AI agent autonomously improve an NFL game prediction model overnight, and do those improvements generalize?

Data: nfl-data-py, seasons 2004–2025, regular season games only
Metric: Log loss on 2024 validation season
Baseline: Logistic regression on ELO differential, home indicator, rest day difference
Baseline Val Loss: 0.623589
Agent: Edits train.py each iteration, accepts only ≥2% improvements
Test Set: 2025 season — locked until final evaluation

How to Run

1. Install dependencies
pip install nfl-data-py scikit-learn xgboost numpy --no-deps

2. Prepare the data (run once)
python prepare.py

*This downloads NFL schedule data, computes ELO ratings, engineers features, and saves train/val/test CSVs to data/processed/.

3. Run the model
python train.py

*This trains the baseline logistic regression on 2004–2023, evaluates on 2024, and saves the result to results/runs/.

Repository Structure:
Arman-Zarei-Stat-390-repo/
├─ prepare.py FROZEN - data pipeline
├─ train.py EDITABLE - model and training loop
├─ program.md EDITABLE - agent instructions and iteration log
├─ README.md
├─ research_log.md
├─ evaluation_board.md
├─ failure_log.md
├─ final_report_skeleton.md
├─ data/
│  ├─ raw/
│  └─ processed/ train.csv, val.csv, test.csv
└─ results/
├─ runs/ per-run JSON logs
└─ best_model/ best saved model