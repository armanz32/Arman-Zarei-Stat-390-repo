Week 2:

Goal: Establish a reproducible baseline model before the agent begins updating

What I Tried:
- Created and ran prepare.py to download data, define metrics and create splits
- Created and ran train.py to make a logistic regression on ELO differential, home game and rest days

Results: 
- Val log loss: 0.623589, CV mean ± std: 0.648181 ± 0.005565, Runtime per iteration: 0.11 seconds
- Reproducibility: ran train.py twice and got same values for both

Observations:
- The baseline model got a val log loss of 0.6235 which is stronger than what I expected to be close to 0.64 considering there are only 3 features
- The CV Mean of 0.648 is higher than the Val log loss meaning 2024 is more predictable than the average season

Goal for next week: Establish an auto research agent loop