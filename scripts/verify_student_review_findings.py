#!/usr/bin/env python
"""Student-requested post-hoc descriptive diagnostics; never fits a model."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.temporal import SPEC, FEATURES, GAP_NS, TOL_NS, construct_features, target_eligibility

RAW = ROOT / "data/raw/metropt3/MetroPT3(AirCompressor).csv"
OUT = ROOT / "results/student_review_diagnostics"
DEV = [(f"D{i+1}", f"2020-{i+3:02d}-01", f"2020-{i+3:02d}-15") for i in range(5)]
FINAL = [("F1", "2020-08-01", "2020-08-06"), ("F2", "2020-08-07", "2020-08-12"),
         ("F3", "2020-08-13", "2020-08-18"), ("F4", "2020-08-19", "2020-08-24"),
         ("F5", "2020-08-25", "2020-08-30")]
HISTORICAL = ["data/raw/metropt3/MetroPT3(AirCompressor).csv",
              "results/rolling/development_predictions.csv", "results/rolling/development_metrics.json",
              "results/rolling/final_predictions.csv", "results/rolling/final_metrics.json",
              "results/analysis/paired_baseline_pairs.csv"]
FROZEN = ["docs/evaluation_protocol_v1.md", "docs/evaluation_protocol_freeze_manifest.json",
          "docs/feature_availability.md", "src/temporal.py", "src/rolling_evaluation.py"]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def quantiles(values):
    a = np.asarray(values, dtype=float)
    a = a[np.isfinite(a)]
    if not len(a):
        return {f"q{q:02d}": None for q in (5, 25, 50, 75, 95)}
    return {f"q{q:02d}": float(np.quantile(a, q / 100)) for q in (5, 25, 50, 75, 95)}


def tail_components(differences, fraction):
    """Largest absolute differences, stable tie-break by original row order."""
    d = np.asarray(differences, dtype=float)
    if not len(d):
        return {"selected_count": 0, "signed_sum": 0.0, "absolute_sum": 0.0,
                "signed_share_of_net": None, "absolute_share_of_absolute_total": None}
    k = max(1, int(np.ceil(len(d) * fraction)))
    order = np.argsort(-np.abs(d), kind="stable")[:k]
    net = float(d.sum())
    abs_total = float(np.abs(d).sum())
    signed = float(d[order].sum())
    absolute = float(np.abs(d[order]).sum())
    return {"selected_count": k, "signed_sum": signed, "absolute_sum": absolute,
            "signed_share_of_net": signed / net if abs(net) > 1e-15 else None,
            "absolute_share_of_absolute_total": absolute / abs_total if abs_total else None}


def scalar_lookup(ts, values, issue_idx, lag_s):
    """Small independent scalar implementation of frozen past-only lookup."""
    requested = int(ts[issue_idx]) - int(lag_s * 1e9)
    j = int(np.searchsorted(ts, requested, side="right") - 1)
    if j < 0:
        return j, None, "no_past_observation", False
    age = (requested - int(ts[j])) / 1e9
    if age < 0:
        raise AssertionError("future observation selected")
    if age > TOL_NS / 1e9:
        return j, age, "stale_over_5s", False
    if not np.isfinite(values[j]):
        return j, age, "nonfinite_feature", False
    if np.any(np.diff(ts[j:issue_idx + 1]) > GAP_NS):
        return j, age, "history_gap_over_60s", False
    return j, age, "eligible", True


def period_rows(ts, start, end):
    a = np.datetime64(start, "ns").astype("int64")
    b = np.datetime64(end, "ns").astype("int64")
    return np.flatnonzero((ts >= a) & (ts < b))


def lag_record(period_type, period_id, issue, ts, col, lag_s, values, prefix):
    req = ts[issue] - np.int64(lag_s * 1e9)
    ix = np.searchsorted(ts, req, side="right") - 1
    has = ix >= 0
    safe = np.maximum(ix, 0)
    age = (req - ts[safe]).astype(float) / 1e9
    age[~has] = np.nan
    within = has & (age >= 0) & (age <= TOL_NS / 1e9)
    finite = np.zeros(len(issue), dtype=bool)
    finite[within] = np.isfinite(values[ix[within]])
    gaps = np.zeros(len(issue), dtype=bool)
    gaps[within] = (prefix[issue[within]] - prefix[ix[within]]) > 0
    eligible = within & finite & ~gaps
    stale = has & (age > TOL_NS / 1e9)
    rec = {"period_type": period_type, "period_id": period_id, "lag_seconds": lag_s,
           "feature": col, "candidate_issue_count": len(issue),
           "exact_match_count": int((has & (age == 0)).sum()),
           "age_0_exclusive_5_inclusive_match_count": int((has & (age > 0) & (age <= TOL_NS / 1e9)).sum()),
           "acceptable_age_0_to_5_match_count": int(within.sum()), "stale_over_5s_count": int(stale.sum()),
           "no_past_observation_count": int((~has).sum()),
           "nonfinite_value_rejection_count": int((within & ~finite).sum()),
           "history_gap_rejection_count": int((within & finite & gaps).sum()),
           "final_lag_eligibility_count": int(eligible.sum()),
           "successful_lookup_age_seconds": quantiles(age[eligible]),
           "unsuccessful_lookup_age_seconds": quantiles(age[has & ~eligible]),
           "observed_past_match_age_seconds": quantiles(age[has]),
           "failure_categories_are_exclusive_by_precedence": "no-past; stale; nonfinite; gap; eligible; exact and positive-age accepted counts overlap only within acceptable matches"}
    return rec, eligible, {"ix": ix, "age": age, "within": within, "finite": finite, "gaps": gaps}


def summarize_period(period_type, period_id, issue, ts, matrix, lag_details):
    n = len(issue)
    candidates = np.ones(n, bool)
    feature_ok = np.column_stack(matrix)
    any_gap = np.column_stack([lag_details[j]["gaps"] for j in range(7)]).any(axis=1)
    intervals = np.diff(ts)
    interval_sec = intervals[np.maximum(issue - 1, 0)] / 1e9 if n else np.array([])
    interval_ns = intervals[np.maximum(issue - 1, 0)] if n else np.array([], dtype=np.int64)
    return {"period_type": period_type, "period_id": period_id, "candidate_issue_count": int(candidates.sum()),
            "joint_seven_feature_eligible_count": int(feature_ok.all(axis=1).sum()),
            "joint_seven_feature_eligibility_rate": float(feature_ok.all(axis=1).mean()) if n else None,
            "joint_history_gap_exclusion_count_among_candidates": int(any_gap.sum()),
            "sampling_interval_seconds": {"q05": quantiles(interval_sec)["q05"],
                "median": quantiles(interval_sec)["q50"], "q95": quantiles(interval_sec)["q95"],
                "count_exactly_9s": int((interval_ns == 9_000_000_000).sum()),
                "count_exactly_10s": int((interval_ns == 10_000_000_000).sum()),
                "count_11_to_60s": int(((interval_ns > 10_000_000_000) & (interval_ns <= 60_000_000_000)).sum()),
                "count_other_1_to_8s": int(((interval_ns > 0) & (interval_ns < 9_000_000_000)).sum()),
                "gt_60s_count": int((interval_sec > 60).sum())},
            **{FEATURES[j]: int(feature_ok[:, j].sum()) for j in range(7)}}


def metric(y, pred):
    e = np.asarray(pred, float) - np.asarray(y, float)
    return {"count": int(len(e)), "mae": float(np.mean(np.abs(e))) if len(e) else None,
            "rmse": float(np.sqrt(np.mean(e * e))) if len(e) else None}


def build_tail_rows(df):
    rows = []
    for name, g in list(df.groupby("origin_id", sort=True)) + [("POOLED", df)]:
        d = g.seasonal_minus_persistence_abs_error.to_numpy(float)
        rec = {"origin_id": name, "paired_count": len(d), "mean_difference_bar": float(d.mean()),
               "median_difference_bar": float(np.median(d)), "minimum_bar": float(d.min()), "maximum_bar": float(d.max()),
               "win_tie_loss": {"seasonal_win": int((d < -1e-12).sum()), "tie": int((np.abs(d) <= 1e-12).sum()),
                                "seasonal_loss": int((d > 1e-12).sum())},
               "difference_quantiles_bar": quantiles(d),
               "tail_definition": "top ceil(fraction*n) rows ranked by absolute paired error difference; stable original-row tie order"}
        for pct in (1, 5):
            rec[f"largest_{pct}pct_absolute_difference_tail"] = tail_components(d, pct / 100)
        rows.append(rec)
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    protected_paths = set(HISTORICAL + FROZEN)
    for base in (ROOT / "results/rolling", ROOT / "results/analysis", ROOT / "notebooks", ROOT / "submission"):
        if base.exists():
            protected_paths.update(str(p.relative_to(ROOT)) for p in base.rglob("*") if p.is_file())
    protected_paths = sorted(protected_paths)
    before = {p: sha256(ROOT / p) for p in protected_paths}
    git_status_before = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
    git_log = subprocess.check_output(["git", "log", "-5", "--oneline"], cwd=ROOT, text=True)
    df = pd.read_csv(RAW, parse_dates=["timestamp"])
    ts = df.timestamp.to_numpy(dtype="datetime64[ns]").astype("int64")
    if not np.all(np.diff(ts) > 0):
        raise RuntimeError("Source timestamps are not strictly increasing; stop for investigation")
    arrays = {name: df[name].to_numpy(float) for name in sorted({c for c, _ in SPEC})}
    X, provenance, feature_ok = construct_features(ts, arrays)
    feature_matrix_ok = np.isfinite(X)
    if len(X) != len(df):
        raise AssertionError("Feature reconstruction length mismatch")
    bad_gap = (np.diff(ts) > GAP_NS).astype(np.int64)
    prefix = np.r_[0, np.cumsum(bad_gap)]

    # Reusable production feature result plus independent scalar parity checks.
    checks = []
    sample = np.unique(np.r_[np.arange(min(40, len(ts))), np.linspace(0, len(ts)-1, 100, dtype=int),
                             np.arange(max(0, len(ts)-40), len(ts))])
    scalar_checks = 0
    for i in sample:
        for j, (col, lag_s) in enumerate(SPEC):
            ix, _, reason, eligible = scalar_lookup(ts, arrays[col], int(i), lag_s)
            expected_ix = int(provenance[i, j])
            if eligible != (expected_ix >= 0) or (eligible and ix != expected_ix):
                raise AssertionError(f"Scalar/production mismatch at row={i}, feature={FEATURES[j]}")
            scalar_checks += 1
    checks.append(f"scalar past-only lookup parity: {scalar_checks} deterministic cases")

    periods = [("month", f"2020-{m:02d}", f"2020-{m:02d}-01", f"2020-{m+1:02d}-01" if m < 8 else "2020-09-01") for m in range(2, 9)]
    periods += [("frozen_window", oid, start, end) for oid, start, end in FINAL]
    lag_rows, joint_rows = [], []
    period_joint = {}
    lag_eligible_global = []
    feature_specs = list(SPEC)
    for typ, pid, start, end in periods:
        issue = period_rows(ts, start, end)
        per_lag_ok, details = [], []
        for j, (col, lag_s) in enumerate(feature_specs):
            rec, elig, det = lag_record(typ, pid, issue, ts, col, lag_s, arrays[col], prefix)
            if not np.array_equal(elig, feature_matrix_ok[issue, j]):
                raise RuntimeError(f"STOP: period lag diagnostic diverges from frozen production feature eligibility: {pid}/{FEATURES[j]}")
            if rec["exact_match_count"] + rec["age_0_exclusive_5_inclusive_match_count"] + rec["stale_over_5s_count"] + rec["no_past_observation_count"] != len(issue):
                raise AssertionError(f"Lookup age categories do not partition candidate issues: {pid}/{FEATURES[j]}")
            lag_rows.append(rec)
            per_lag_ok.append(elig)
            details.append(det)
        joint = np.column_stack(per_lag_ok).all(axis=1)
        joint_rows.append(summarize_period(typ, pid, issue, ts, per_lag_ok, details))
        period_joint[(typ, pid)] = {"candidate": int(len(issue)), "joint": int(joint.sum()),
                                     "joint_rate": float(joint.mean()) if len(issue) else None,
                                     "gap_rows": int(np.column_stack([d["gaps"] for d in details]).any(axis=1).sum())}
    checks.append(f"monthly/frozen-period lookup tables: {len(lag_rows)} feature-period rows")

    # Monthly sampling descriptors and label-valid expanding training reconciliation.
    target_idx, target_ok = target_eligibility(ts, df.TP2.to_numpy(float), np.arange(len(ts)))
    training_rows = []
    saved = {"development": json.loads((ROOT / "results/rolling/development_metrics.json").read_text()),
             "final": json.loads((ROOT / "results/rolling/final_metrics.json").read_text())}
    for phase, windows in (("development", DEV), ("final", FINAL)):
        for oid, start, end in windows:
            origin = np.datetime64(start, "ns").astype("int64")
            eligible = (ts < origin) & target_ok & (ts[np.maximum(target_idx, 0)] <= origin) & feature_ok
            actual = int(eligible.sum())
            fold = next(x for x in saved[phase]["origins"] if x["origin_id"] == oid)
            expected = int(fold["training_sample_count"])
            if actual != expected:
                raise RuntimeError(f"STOP: {oid} training reconstruction {actual} != saved Phase 2B {expected}")
            training_rows.append({"phase": phase, "origin_id": oid, "origin": start,
                "training_issue_lt_origin": True, "actual_label_le_origin": True,
                "target_and_gap_eligible_count": int(((ts < origin) & target_ok & (ts[np.maximum(target_idx, 0)] <= origin)).sum()),
                "feature_eligible_training_count_reconstructed": actual,
                "saved_phase2b_training_sample_count": expected, "count_match": True})
    checks.append("D1-D5 and F1-F5 expanding training counts exactly match saved Phase 2B metrics")

    # Paired baseline error tails recomputed from saved final predictions, then exact identity checks.
    pred = pd.read_csv(ROOT / "results/rolling/final_predictions.csv")
    valid = pred[pred.target_pair_eligible & pred.prediction_available].copy()
    piv = valid.pivot(index=["origin_id", "issue_row", "target_row"], columns="method", values="prediction")
    both = piv.dropna(subset=["persistence", "seasonal_naive"]).reset_index()
    matched_target, matched_ok = target_eligibility(ts, df.TP2.to_numpy(float), both.issue_row.to_numpy(dtype=int))
    if not np.all(matched_ok) or not np.array_equal(matched_target, both.target_row.to_numpy(dtype=int)):
        raise RuntimeError("STOP: paired predictions do not resolve to the frozen original target matcher")
    label = valid[valid.method == "persistence"].drop_duplicates(["origin_id", "issue_row", "target_row"])
    label_map = label.set_index(["origin_id", "issue_row", "target_row"]).observed_tp2
    both["label"] = [label_map.loc[(r.origin_id, r.issue_row, r.target_row)] for r in both.itertuples()]
    both["persistence_abs_error"] = np.abs(both.persistence - both.label)
    both["seasonal_abs_error"] = np.abs(both.seasonal_naive - both.label)
    both["seasonal_minus_persistence_abs_error"] = both.seasonal_abs_error - both.persistence_abs_error
    saved_pairs = pd.read_csv(ROOT / "results/analysis/paired_baseline_pairs.csv")
    calc_ids = set(map(tuple, both[["origin_id", "issue_row", "target_row"]].itertuples(index=False, name=None)))
    saved_f2 = saved_pairs[saved_pairs.origin_id == "F2"]
    calc_f2 = both[both.origin_id == "F2"]
    saved_f2_ids = set(map(tuple, saved_f2[["origin_id", "issue_row", "target_row"]].itertuples(index=False, name=None)))
    calc_f2_ids = set(map(tuple, calc_f2[["origin_id", "issue_row", "target_row"]].itertuples(index=False, name=None)))
    if calc_ids != set(map(tuple, saved_pairs[["origin_id", "issue_row", "target_row"]].itertuples(index=False, name=None))):
        raise RuntimeError("STOP: saved Phase 3 paired baseline identities differ from final predictions")
    if calc_f2_ids != saved_f2_ids or len(calc_f2) != 22979:
        raise RuntimeError(f"STOP: F2 paired population discrepancy: {len(calc_f2)} rows")
    tails = build_tail_rows(both)
    checks.append("paired persistence/seasonal identities exactly match saved Phase 3 artifact; F2 n=22,979")

    # F2 all-three population; identity is exact origin + original issue row + matched target row.
    f2_all3 = valid[(valid.origin_id == "F2") & valid.common_target]
    f2_sets = {m: set(map(tuple, f2_all3[f2_all3.method == m][["origin_id", "issue_row", "target_row"]].itertuples(index=False, name=None)))
               for m in ("persistence", "seasonal_naive", "ridge")}
    if not (f2_sets["persistence"] == f2_sets["seasonal_naive"] == f2_sets["ridge"]) or len(f2_sets["ridge"]) != 18:
        raise RuntimeError("STOP: F2 all-three common identity/count discrepancy")
    sensitivity_rows = []
    for pop, ids in (("persistence_seasonal_pairs", calc_f2_ids), ("all_three_common", f2_sets["ridge"])):
        subset = valid[(valid.origin_id == "F2") & valid.apply(lambda r: (r.origin_id, r.issue_row, r.target_row) in ids, axis=1)]
        by_method = {}
        methods = ("persistence", "seasonal_naive") if pop == "persistence_seasonal_pairs" else ("persistence", "seasonal_naive", "ridge")
        for method in methods:
            g = subset[subset.method == method]
            if len(g):
                by_method[method] = metric(g.observed_tp2.to_numpy(), g.prediction.to_numpy())
        sensitivity_rows.append({"population": pop, "identity_key": "origin_id + issue_row + actual target_row",
                                 "identity_count": len(ids), "method_metrics": by_method})
    f2_issue_rows = np.array(sorted({int(k[1]) for k in f2_sets["ridge"]}), dtype=int)
    f2_target_rows = np.array(sorted({int(k[2]) for k in f2_sets["ridge"]}), dtype=int)
    delta = df.TP2.to_numpy(float)[f2_target_rows] - df.TP2.to_numpy(float)[f2_issue_rows]
    sensitivity_rows.append({"population": "all_three_common_descriptive_target_change",
        "identity_key": "18 all-three common issue/target pairs", "identity_count": len(delta),
        "issue_to_target_tp2_change_bar": {"median": float(np.median(delta)), "min": float(delta.min()), "max": float(delta.max()),
                                            "abs_median": float(np.median(np.abs(delta)))}})
    checks.append("F2 all-three common population has 18 identical issue/target identities")

    # Save compact CSV/JSON artifacts with stable schemas.
    lag_df = pd.DataFrame(lag_rows)
    for c in ("successful_lookup_age_seconds", "unsuccessful_lookup_age_seconds", "observed_past_match_age_seconds"):
        q = pd.json_normalize(lag_df[c]).add_prefix(c + "_")
        lag_df = pd.concat([lag_df.drop(columns=[c]), q], axis=1)
    lag_df.to_csv(OUT / "monthly_lag_alignment.csv", index=False)
    pd.DataFrame(joint_rows).to_csv(OUT / "monthly_joint_feature_eligibility.csv", index=False)
    pd.DataFrame(training_rows).to_csv(OUT / "expanding_training_reconciliation.csv", index=False)
    pd.DataFrame(tails).to_json(OUT / "paired_error_tail_summary.json", orient="records", indent=2)
    pd.DataFrame(sensitivity_rows).to_json(OUT / "f2_population_sensitivity.json", orient="records", indent=2)

    # Figure: means and medians with paired-n labels, plus tail share of total |difference|.
    origin_rows = [r for r in tails if r["origin_id"] != "POOLED"]
    x = np.arange(len(origin_rows))
    means = [r["mean_difference_bar"] for r in origin_rows]
    medians = [r["median_difference_bar"] for r in origin_rows]
    tail5 = [100*r["largest_5pct_absolute_difference_tail"]["absolute_share_of_absolute_total"] for r in origin_rows]
    ns = [r["paired_count"] for r in origin_rows]
    fig, (ax, bx) = plt.subplots(2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    ax.bar(x, means, .52, label="Mean signed difference")
    ax.scatter(x, medians, color="#e87517", marker="D", s=38, zorder=3, label="Median signed difference")
    ax.axhline(0, color="black", lw=.8)
    ax.set_ylabel("Seasonal − persistence absolute error (bar)")
    ax.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    ax.set_title("Paired error difference: mean, median, and tail concentration", fontsize=12)
    for xi, n in zip(x, ns):
        ax.text(xi, ax.get_ylim()[0], f"n={n:,}", ha="center", va="bottom", fontsize=8)
    bx.bar(x, tail5, color="#9b6bb5")
    bx.set_ylabel("Top 5% share of Σ|difference| (%)")
    bx.set_xticks(x, [r["origin_id"] for r in origin_rows])
    bx.set_xlabel("Frozen final origin")
    bx.grid(axis="y", alpha=.25)
    fig.tight_layout(rect=[0, 0, .82, 1])
    fig.savefig(OUT / "paired_error_tails.png", dpi=160)
    plt.close(fig)

    after = {p: sha256(ROOT / p) for p in protected_paths}
    if before != after:
        raise RuntimeError("Protected historical/frozen source hash changed during diagnostics")
    outputs = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != "diagnostic_manifest.json")
    import numpy, matplotlib as mpl
    manifest = {"title": "Student-requested post-hoc descriptive diagnostics",
        "status": "PASS", "command": "conda run -n nussem1 python scripts/verify_student_review_findings.py",
        "python": platform.python_version(), "numpy": numpy.__version__, "pandas": pd.__version__,
        "matplotlib": mpl.__version__, "randomness": "No random sampling used; scalar parity checks use deterministic rows spread across the archive.",
        "source_hashes_before": before, "protected_hashes_after": after,
        "git_status_before_final_run": git_status_before,
        "recent_commits_at_audit_start": git_log,
        "diagnostic_code_sha256": {"scripts/verify_student_review_findings.py": sha256(ROOT / "scripts/verify_student_review_findings.py"),
                                   "tests/test_student_review_diagnostics.py": sha256(ROOT / "tests/test_student_review_diagnostics.py")},
        "checks": checks, "frozen_config_unchanged": True,
        "monthly_periods": [x[1] for x in periods if x[0] == "month"],
        "feature_order": list(FEATURES), "horizon_seconds": 600, "lookup_tolerance_seconds": 5,
        "gap_threshold_seconds": 60,
        "interpretation_limits": ["Naive timestamps have no verified timezone or release-time history.",
          "Observed lookup failures do not establish physical clock drift.",
          "Post-hoc diagnostics are descriptive and are not model selection or protocol revision."],
        "output_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in outputs}}
    (OUT / "diagnostic_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps({"status": "PASS", "checks": checks, "outputs": manifest["output_hashes"]}, indent=2))


if __name__ == "__main__":
    main()
