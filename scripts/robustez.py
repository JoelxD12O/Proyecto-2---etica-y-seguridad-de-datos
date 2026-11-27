"""Robustez offline con semillas independientes, periodos y topes alternativos."""
import json, sys
from pathlib import Path
import numpy
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import backend.privacy as privacy  # noqa: E402
import backend.experiment as experiment  # noqa: E402

SEEDS = 30
def summary(x):
    x = numpy.asarray(x, float)
    m, sd = x.mean(), x.std(ddof=1)
    h = stats.t.ppf(0.975, len(x) - 1) * sd / numpy.sqrt(len(x))
    return {"mean": round(m, 3), "sd": round(sd, 3), "ci95": [round(m - h, 3), round(m + h, 3)],
            "min": round(x.min(), 3), "max": round(x.max(), 3)}


out = {"seeds": SEEDS, "fitbit": {}, "gym": {}}
csv = ROOT / "data/raw/dailyActivity_merged.csv"
for period, limit in [("2016-04", 120.0), ("2016-05", 120.0), ("2016-04", 90.0), ("2016-04", 150.0)]:
    privacy.LIMIT = limit
    experiment.LIMIT = limit
    mae = {e: [] for e in experiment.GRID}
    ret = {e: [] for e in experiment.GRID}
    for run in range(SEEDS):
        summ, util = experiment.analyze_fitbit(csv, period=period, trials=300, seed=20261126 + run)
        for u in util:
            mae[u["epsilon"]].append(u["mae_minutes"])
            ret[u["epsilon"]].append(u["returned_pct"])
    key = f"{period}_tope{int(limit)}"
    out["fitbit"][key] = {"reference": summ["reference"], "people": summ["people_in_period"],
                          "days": summ["observed_days_in_period"],
                          **{str(e): {"mae": summary(mae[e]), "returned_pct": summary(ret[e])} for e in experiment.GRID}}
    print(key, summ["reference"], {e: (out["fitbit"][key][str(e)]["mae"]["mean"], out["fitbit"][key][str(e)]["mae"]["sd"]) for e in experiment.GRID}, flush=True)
privacy.LIMIT = 120.0
experiment.LIMIT = 120.0

acc = {e: [] for e in experiment.GRID}
grp = {e: {"Female": [], "Male": []} for e in experiment.GRID}
for run in range(SEEDS):
    lab = experiment.model_lab(ROOT / "data/raw/gym_members_exercise_tracking.csv", repeats=30, seed=20261126 + run)
    for p in lab["validation_candidates"]:
        acc[p["epsilon"]].append(p["accuracy"])
    for e in experiment.GRID:
        for g in ("Female", "Male"):
            candidate = next(p for p in lab["validation_candidates"] if p["epsilon"] == e)
            grp[e][g].append(candidate["groups"][g]["accuracy"])
out["gym"] = {str(e): {"accuracy": summary(acc[e]), "Female": summary(grp[e]["Female"]),
                      "Male": summary(grp[e]["Male"])} for e in experiment.GRID}
out["gym_baseline"] = {"accuracy": lab["validation_reference"]["accuracy"], "scope": "validation"}
(ROOT / "evidence" / "robustez.json").write_text(json.dumps(out, indent=2), encoding="utf8")
print(json.dumps(out["gym"], indent=1))
