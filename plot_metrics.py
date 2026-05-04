import json
import matplotlib.pyplot as plt
from pathlib import Path

runs = sorted(Path("results/runs").glob("run_*.json"))
ids, losses = [], []
for r in runs:
    d = json.load(open(r))
    ids.append(d["run_id"])
    losses.append(d["val_loss"])

plt.plot(ids, losses, marker="o")
plt.axhline(0.623589, linestyle="--", color="red", label="Baseline")
plt.xlabel("Run")
plt.ylabel("Val Log Loss")
plt.title("Val Log Loss Across Runs")
plt.legend()
plt.savefig("metric_over_time.png")