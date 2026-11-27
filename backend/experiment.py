"""Trusted offline lab on the public archives. Never imported by the HTTP service."""

import csv, json
from collections import defaultdict
from pathlib import Path
from statistics import fmean
import numpy as np
from diffprivlib.mechanisms import Laplace
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from .privacy import private_mean, contributions, LIMIT
from .dataio import read_activity

GRID = (0.1, 0.5, 1.0, 2.0)


def analyze_fitbit(path, period="2016-04", trials=300, seed=3031):
    rows, duplicates = read_activity([path])
    records = [
        (u, d, m["minutes"]) for (u, d), m in rows.items() if d.startswith(period)
    ]
    values = contributions(records)
    if not values:
        raise ValueError("No hay datos de ese periodo.")
    grouped = defaultdict(list)
    for u, d, m in records:
        grouped[u].append(m)
    observed = [fmean(v) for v in grouped.values()]
    counts = [len(v) for v in grouped.values()]
    summary = {
        "processed_days": len(rows),
        "people_in_file": len(set(u for u, _ in rows)),
        "period": period,
        "people_in_period": len(values),
        "observed_days_in_period": len(records),
        "coverage_min_days": min(counts),
        "coverage_max_days": max(counts),
        "identical_duplicates": duplicates,
        "clipped_people": sum(x > LIMIT for x in observed),
        "unclipped_reference": round(fmean(observed), 3),
        "reference": round(fmean(values), 3),
        "row_weighted_reference": round(fmean(r[2] for r in records), 3),
    }
    result = []
    for eps in GRID:
        rng = np.random.RandomState(seed)
        samples = [private_mean(values, eps, rng=rng) for _ in range(trials)]
        errors = np.array([abs(x - fmean(values)) for x in samples if x is not None])
        result.append(
            {
                "epsilon": eps,
                "draws": trials,
                "returned_pct": round(100 * len(errors) / trials, 1),
                "mae_minutes": round(float(errors.mean()), 3) if len(errors) else None,
                "p90_abs_error": round(float(np.percentile(errors, 90)), 3)
                if len(errors)
                else None,
            }
        )
    return summary, result


def gym_records(path):
    # No ID linking Gym examples to Fitbit. The guarantee for this lab is row-level.
    result = []
    seen = set()
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            key = tuple(r.values())
            if key in seen:
                continue
            seen.add(key)
            exp = int(r["Experience_Level"])
            freq = int(r["Workout_Frequency (days/week)"])
            if exp not in range(1, 4) or freq not in range(1, 8):
                raise ValueError("Categoría de Gym fuera del dominio predefinido")
            duration = float(r["Session_Duration (hours)"])
            if not np.isfinite(duration) or not 0 <= duration <= 24:
                raise ValueError("Duración inválida")
            result.append(
                ((exp - 1) * 7 + freq - 1, int(duration >= 1.25), r["Gender"])
            )
    return result


def model_lab(path, repeats=30, seed=3031):
    """Select epsilon on validation only; the historically inspected test is descriptive."""
    data = gym_records(path)
    X = np.array([r[0] for r in data])
    y = np.array([r[1] for r in data])
    group = np.array([r[2] for r in data])
    idx = np.arange(len(data))
    development, test = train_test_split(
        idx, test_size=0.3, random_state=3031, stratify=y
    )
    train, validation = train_test_split(
        development, test_size=0.25, random_state=3032, stratify=y[development]
    )

    def histogram(indices):
        counts = np.zeros((21, 2))
        np.add.at(counts, (X[indices], y[indices]), 1)
        return counts

    def privatize(counts, epsilon, stage, run):
        sequence = np.random.SeedSequence([seed, stage, GRID.index(epsilon), run])
        rng = np.random.RandomState(sequence.generate_state(1)[0])
        mechanism = Laplace(epsilon=epsilon, sensitivity=1, random_state=rng)
        return np.array(
            [max(0.0, mechanism.randomise(c)) for c in counts.flat]
        ).reshape(counts.shape)

    def score(counts, fitted, evaluated):
        probabilities = (counts[:, 1] + 1) / (counts.sum(axis=1) + 2)
        predicted = (probabilities[X[evaluated]] >= 0.5).astype(int)
        actual = y[evaluated]
        matrix = confusion_matrix(actual, predicted, labels=[0, 1])
        groups = {}
        for name in sorted(set(group[evaluated])):
            mask = group[evaluated] == name
            cm = confusion_matrix(actual[mask], predicted[mask], labels=[0, 1])
            tn, fp, fn, tp = cm.ravel()
            groups[str(name)] = {
                "n": int(mask.sum()),
                "accuracy": float(accuracy_score(actual[mask], predicted[mask])),
                "tpr": float(tp / (tp + fn)) if tp + fn else None,
                "fpr": float(fp / (fp + tn)) if fp + tn else None,
                "confusion_matrix": cm.tolist(),
            }
        confidence = np.where(y == 1, probabilities[X], 1 - probabilities[X])
        membership_values = np.r_[confidence[fitted], confidence[evaluated]]
        labels = np.r_[np.ones(len(fitted)), np.zeros(len(evaluated))]
        attack_fpr, attack_tpr, _ = roc_curve(labels, membership_values)
        return {
            "accuracy": float(accuracy_score(actual, predicted)),
            "balanced_accuracy": float(balanced_accuracy_score(actual, predicted)),
            "precision": float(precision_score(actual, predicted, zero_division=0)),
            "recall": float(recall_score(actual, predicted, zero_division=0)),
            "f1": float(f1_score(actual, predicted, zero_division=0)),
            "confusion_matrix": matrix.tolist(),
            "attack_auc": float(roc_auc_score(labels, membership_values)),
            "attack_advantage": float(max(attack_tpr - attack_fpr)),
        }, groups

    def aggregate(samples):
        metrics = [item[0] for item in samples]
        names = [key for key in metrics[0] if key != "confusion_matrix"]
        result = {key: round(fmean(item[key] for item in metrics), 4) for key in names}
        result["accuracy_sd"] = round(float(np.std([m["accuracy"] for m in metrics], ddof=1)), 4)
        result["confusion_matrix"] = np.rint(
            np.mean([m["confusion_matrix"] for m in metrics], axis=0)
        ).astype(int).tolist()
        result["groups"] = {}
        for name in samples[0][1]:
            rows = [item[1][name] for item in samples]
            result["groups"][name] = {
                "n": rows[0]["n"],
                **{
                    key: round(fmean(row[key] for row in rows), 4)
                    if all(row[key] is not None for row in rows) else None
                    for key in ("accuracy", "tpr", "fpr")
                },
            }
        return result

    validation_counts = histogram(train)
    validation_reference, _ = score(validation_counts, train, validation)
    candidates = []
    for epsilon in GRID:
        samples = [
            score(privatize(validation_counts, epsilon, 0, run), train, validation)
            for run in range(repeats)
        ]
        result = aggregate(samples)
        result["epsilon"] = epsilon
        groups = list(result["groups"].values())
        tpr = [g["tpr"] for g in groups if g["tpr"] is not None]
        result["tpr_gap"] = round(max(tpr) - min(tpr), 4) if len(tpr) == 2 else None
        result["eligible"] = (
            result["accuracy"] >= validation_reference["accuracy"] - 0.05
            and result["balanced_accuracy"] >= validation_reference["balanced_accuracy"] - 0.05
            and result["tpr_gap"] is not None
            and result["tpr_gap"] <= 0.15
        )
        candidates.append(result)
    selected = next((item["epsilon"] for item in candidates if item["eligible"]), None)
    final_counts = histogram(development)
    baseline, baseline_groups = score(final_counts, development, test)
    final = (
        aggregate([
            score(privatize(final_counts, selected, 1, run), development, test)
            for run in range(repeats)
        ])
        if selected is not None else None
    )
    return {
        "task": "Sesión de al menos 75 minutos; unidad protegida: fila de entrenamiento",
        "split": {"train": len(train), "validation": len(validation), "test": len(test)},
        "selection_rule": "Menor epsilon con pérdida media de accuracy y balanced accuracy <= 0.05 y brecha TPR <= 0.15 en validación",
        "validation_reference": validation_reference,
        "validation_candidates": candidates,
        "selected_epsilon": selected,
        "test_baseline": baseline,
        "test_baseline_groups": baseline_groups,
        "test_trivial_accuracy": float(accuracy_score(y[test], np.full(len(test), int(np.mean(y[development]) >= 0.5)))),
        "test_class_counts": np.bincount(y[test], minlength=2).tolist(),
        "test_selected": final,
        "repetitions": repeats,
        "test_history": "El mismo dataset y resultados de prueba de una versión anterior ya fueron observados; evaluación descriptiva, no confirmación independiente.",
    }


def run(root):
    resultdir = root / "evidence"
    resultdir.mkdir(exist_ok=True)
    summary, utility = analyze_fitbit(root / "data/raw/dailyActivity_merged.csv")
    model = model_lab(root / "data/raw/gym_members_exercise_tracking.csv")
    evidence = {
        "scope": "Laboratorio offline con archivos públicos. Referencias exactas y semillas experimentales; no es una publicación DP.",
        "fitbit": summary,
        "utility": utility,
        "gym": model,
    }
    (resultdir / "experimentos.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf8"
    )
    return evidence


if __name__ == "__main__":
    from .config import ROOT

    result = run(ROOT)
    print(
        json.dumps(
            {
                "fitbit": result["fitbit"],
                "utility": result["utility"],
                "model": result["gym"]["test_selected"],
            },
            indent=2,
        )
    )
