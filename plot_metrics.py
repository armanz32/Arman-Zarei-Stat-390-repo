import json
import matplotlib.pyplot as plt
from pathlib import Path

END_RUN = 63

runs = sorted(Path("results/runs").glob("run_*.json"))
ids, losses = [], []

for r in runs:
    d = json.load(open(r))
    run_id = d["run_id"]
    
    if 16 <= int(str(run_id)) <= END_RUN:
        ids.append(str(run_id))
        losses.append(d["val_loss"])

plt.figure(figsize=(14, 5))
plt.plot(ids, losses, marker="o")
plt.xticks(rotation=45, ha="right")
plt.xlabel("Run")
plt.ylabel("Val Log Loss")
plt.title("Week 5 Experiment Block — Val Log Loss (Runs 016–063)")
plt.legend()
plt.tight_layout()
plt.savefig("metric_over_time.png")