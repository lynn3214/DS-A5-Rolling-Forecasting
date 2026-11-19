#!/usr/bin/env python
"""Reproduce descriptive Phase 3 drift, coverage, and failure analyses."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "ds_a5_mplconfig"))
os.environ.setdefault("XDG_CACHE_HOME", str(Path(tempfile.gettempdir()) / "ds_a5_cache"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/raw/metropt3/MetroPT3(AirCompressor).csv"
ROLL = ROOT / "results/rolling"
OUT = ROOT / "results/analysis"
FIG = OUT / "figures"
EXPECTED = {
    "data/raw/metropt3/MetroPT3(AirCompressor).csv": "db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24",
    "results/rolling/development_predictions.csv": "c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586",
    "results/rolling/development_metrics.json": "1c97599d08311a2cadca555313ee1ab87d7c3648539e34f73235c316dafde641",
    "results/rolling/final_predictions.csv": "e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41",
    "results/rolling/final_metrics.json": "6af02ab6d02e491b622f66d3b0b45b62a871a6c264f917c92d519ced2f9f4d11",
}
PRED_COLS = [
    "origin_id", "issue_row", "issue_timestamp", "nominal_target_timestamp",
    "target_row", "actual_target_timestamp", "observed_tp2", "method",
    "prediction", "prediction_available", "missing_reason", "target_pair_eligible",
    "target_pair_reason", "feature_eligible", "absolute_error", "squared_error",
    "common_target",
]
METHODS = ["persistence", "seasonal_naive", "ridge"]
FEATURE_SIGNALS = ["TP2", "TP3", "Motor_current", "Oil_temperature"]
STATE_SIGNALS = ["COMP", "DV_eletric", "Towers", "MPG", "LPS", "Pressure_switch", "Oil_level"]
OTHER_SIGNALS = ["H1", "DV_pressure", "Reservoirs"]
ALL_COLS = ["timestamp", *FEATURE_SIGNALS, *OTHER_SIGNALS, *STATE_SIGNALS, "Caudal_impulses"]

DEV = [("D1", "2020-03-01", "2020-03-15"), ("D2", "2020-04-01", "2020-04-15"),
       ("D3", "2020-05-01", "2020-05-15"), ("D4", "2020-06-01", "2020-06-15"),
       ("D5", "2020-07-01", "2020-07-15")]
FINAL = [("F1", "2020-08-01", "2020-08-06"), ("F2", "2020-08-07", "2020-08-12"),
         ("F3", "2020-08-13", "2020-08-18"), ("F4", "2020-08-19", "2020-08-24"),
         ("F5", "2020-08-25", "2020-08-30")]
EVENTS = [
    {"event_id": "UCI_failure_1a", "report_number": "1 (first row)", "start": "2020-04-18 00:00:00", "end": "2020-04-18 23:59:00", "event": "Air leak; high stress", "source_note": "The UCI table labels this row Report #1."},
    {"event_id": "UCI_failure_1b", "report_number": "1 (second row)", "start": "2020-05-29 23:30:00", "end": "2020-05-30 06:00:00", "event": "Air leak; high stress", "source_note": "The UCI table also labels this row Report #1 and appends 'Maintenance on 30Apr at 12:00', which predates the reported failure window; unresolved."},
    {"event_id": "UCI_failure_3", "report_number": "3", "start": "2020-06-05 10:00:00", "end": "2020-06-07 14:30:00", "event": "Air leak; high stress", "source_note": "The UCI table reports maintenance on 8Jun at 16:00."},
    {"event_id": "UCI_failure_4", "report_number": "4", "start": "2020-07-15 14:30:00", "end": "2020-07-15 19:00:00", "event": "Air leak; high stress", "source_note": "The UCI table reports maintenance on 16Jul at 00:00."},
]
UCI_URL = "https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def metrics(errors: np.ndarray) -> tuple[int, float | None, float | None]:
    if not len(errors):
        return 0, None, None
    return int(len(errors)), float(np.mean(np.abs(errors))), float(np.sqrt(np.mean(errors ** 2)))


def read_predictions(phase: str) -> pd.DataFrame:
    path = ROLL / f"{phase}_predictions.csv"
    d = pd.read_csv(path, usecols=PRED_COLS, parse_dates=["issue_timestamp", "nominal_target_timestamp", "actual_target_timestamp"])
    d["phase"] = phase
    d["issue_day"] = d.issue_timestamp.dt.floor("D")
    d["issue_row"] = d.issue_row.astype("int64")
    d["target_pair_eligible"] = d.target_pair_eligible.astype(bool)
    d["prediction_available"] = d.prediction_available.astype(bool)
    d["feature_eligible"] = d.feature_eligible.astype(bool)
    return d


def verify_inputs() -> dict[str, str]:
    got = {rel: sha256(ROOT / rel) for rel in EXPECTED}
    for rel, expected in EXPECTED.items():
        if got[rel] != expected:
            raise AssertionError(f"Input hash mismatch for {rel}: {got[rel]} != {expected}")
    return got


def verify_predictions(dev: pd.DataFrame, final: pd.DataFrame) -> dict[str, int]:
    d = pd.concat([dev, final], ignore_index=True)
    if d.duplicated(["phase", "origin_id", "issue_row", "method"]).any():
        raise AssertionError("Duplicate phase-origin-issue-method rows")
    method_counts = d.groupby(["phase", "origin_id", "issue_row"]).method.nunique()
    if not method_counts.eq(3).all():
        raise AssertionError("Every saved issue must have three method records")
    issue_flags = d.groupby(["phase", "origin_id", "issue_row"]).target_pair_eligible.nunique()
    if not issue_flags.eq(1).all():
        raise AssertionError("Target eligibility differs among methods for the same issue")
    scored = d.target_pair_eligible & d.prediction_available
    if d.loc[scored, "prediction"].isna().any() or d.loc[scored, "observed_tp2"].isna().any():
        raise AssertionError("A scored row has a missing prediction or label")
    if d.loc[~d.prediction_available, "prediction"].notna().any():
        raise AssertionError("Unavailable predictions must remain missing")
    if ((d.method == "ridge") & d.prediction_available & ~d.feature_eligible).any():
        raise AssertionError("Ridge prediction exists without frozen feature eligibility")
    for phase, g in d[d.method == "ridge"].groupby("phase"):
        model_available = np.array([origin != "D1" for origin in g.origin_id], dtype=bool)
        # D1 has no fitted estimator; all other recorded origins executed a fit.
        expected = g.feature_eligible.to_numpy(bool) & model_available
        if not np.array_equal(g.prediction_available.to_numpy(bool), expected):
            raise AssertionError(f"Ridge prediction/feature availability mismatch in {phase}")
    return {"prediction_rows": int(len(d)), "issue_rows": int(method_counts.size), "scored_rows": int(scored.sum())}


def verify_saved_metrics(allpred: pd.DataFrame) -> dict[str, int]:
    """Recompute per-origin and pooled metrics against the archived summaries."""
    checks = 0
    for phase in ["development", "final"]:
        ref = json.loads((ROLL / f"{phase}_metrics.json").read_text())
        d = allpred[allpred.phase == phase]
        for fold in ref["origins"]:
            oid = fold["origin_id"]
            g = d[d.origin_id == oid]
            for method in METHODS:
                m = g[(g.method == method) & g.target_pair_eligible & g.prediction_available]
                e = m.prediction.to_numpy(float) - m.observed_tp2.to_numpy(float)
                n, mae, rmse = metrics(e)
                expected = fold["method_metrics"][method]
                if n != expected["count"] or (mae is not None and not np.isclose(mae, expected["mae"])) or (rmse is not None and not np.isclose(rmse, expected["rmse"])):
                    raise AssertionError(f"Per-origin saved metric mismatch: {phase} {oid} {method}")
                checks += 1
            scored = g[g.target_pair_eligible & g.prediction_available]
            pivot = scored.pivot_table(index=["issue_row", "target_row"], columns="method", values="prediction", aggfunc="first").reindex(columns=METHODS).dropna()
            if len(pivot) != fold["common_target_count"]:
                raise AssertionError(f"Per-origin common count mismatch: {phase} {oid}")
            labels = scored[scored.method == "persistence"].set_index(["issue_row", "target_row"]).observed_tp2
            for method in METHODS:
                e = pivot[method].to_numpy(float) - labels.reindex(pivot.index).to_numpy(float)
                n, mae, rmse = metrics(e)
                expected = fold["common_target_metrics"][method]
                if n != expected["count"] or (mae is not None and not np.isclose(mae, expected["mae"])) or (rmse is not None and not np.isclose(rmse, expected["rmse"])):
                    raise AssertionError(f"Per-origin common metric mismatch: {phase} {oid} {method}")
                checks += 1
        valid = d[d.target_pair_eligible & d.prediction_available]
        for method, g in valid.groupby("method"):
            e = g.prediction.to_numpy(float) - g.observed_tp2.to_numpy(float)
            n, mae, rmse = metrics(e)
            expected = ref["pooled_method_specific"][method]
            if n != expected["count"] or not np.isclose(mae, expected["mae"]) or not np.isclose(rmse, expected["rmse"]):
                raise AssertionError(f"Pooled method metric mismatch: {phase} {method}")
            checks += 1
        pivot = valid.pivot_table(index=["origin_id", "issue_row", "target_row"], columns="method", values="prediction", aggfunc="first").reindex(columns=METHODS).dropna()
        labels = valid[valid.method == "persistence"].set_index(["origin_id", "issue_row", "target_row"]).observed_tp2
        if len(pivot) != ref["pooled_common_targets"]["persistence"]["count"]:
            raise AssertionError(f"Pooled common count mismatch: {phase}")
        for method in METHODS:
            e = pivot[method].to_numpy(float) - labels.reindex(pivot.index).to_numpy(float)
            n, mae, rmse = metrics(e)
            expected = ref["pooled_common_targets"][method]
            if n != expected["count"] or not np.isclose(mae, expected["mae"]) or not np.isclose(rmse, expected["rmse"]):
                raise AssertionError(f"Pooled common metric mismatch: {phase} {method}")
            checks += 1
    return {"saved_metric_recalculations_passed": checks}


def paired_baseline_outputs(final: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    pair_rows: list[dict] = []
    origin_rows: list[dict] = []
    for origin, g in final.groupby("origin_id", sort=False):
        issue = g[g.method == "persistence"]
        candidate_n = int(issue.issue_row.nunique())
        valid_n = int(issue.target_pair_eligible.sum())
        method_stats = {}
        for method in ["persistence", "seasonal_naive"]:
            m = g[(g.method == method) & g.target_pair_eligible & g.prediction_available].copy()
            e = m.prediction.to_numpy(float) - m.observed_tp2.to_numpy(float)
            n, mae, rmse = metrics(e)
            method_stats[method] = {"n": n, "mae": mae, "rmse": rmse,
                                    "available": int(g[(g.method == method) & g.prediction_available].shape[0]),
                                    "candidate_coverage": float(g[(g.method == method) & g.prediction_available].issue_row.nunique() / candidate_n),
                                    "valid_target_coverage": float(n / valid_n) if valid_n else np.nan}
        a = g[(g.method == "persistence") & g.target_pair_eligible & g.prediction_available]
        b = g[(g.method == "seasonal_naive") & g.target_pair_eligible & g.prediction_available]
        key = ["origin_id", "issue_row", "target_row"]
        a = a[key + ["issue_timestamp", "actual_target_timestamp", "prediction", "observed_tp2"]].rename(columns={"prediction": "persistence_prediction", "observed_tp2": "persistence_label"})
        b = b[key + ["prediction", "observed_tp2"]].rename(columns={"prediction": "seasonal_naive_prediction", "observed_tp2": "seasonal_naive_label"})
        p = a.merge(b, on=key, how="inner", validate="one_to_one")
        if not np.allclose(p.persistence_label, p.seasonal_naive_label, rtol=0, atol=0):
            raise AssertionError(f"Paired target labels differ for {origin}")
        p["persistence_abs_error"] = (p.persistence_prediction - p.persistence_label).abs()
        p["seasonal_naive_abs_error"] = (p.seasonal_naive_prediction - p.seasonal_naive_label).abs()
        p["seasonal_minus_persistence_abs_error"] = p.seasonal_naive_abs_error - p.persistence_abs_error
        tol = 1e-12
        p["pair_result_for_seasonal"] = np.select(
            [p.seasonal_minus_persistence_abs_error < -tol, p.seasonal_minus_persistence_abs_error > tol],
            ["win", "loss"], default="tie")
        p["origin_id"] = origin
        pair_rows.extend(p.to_dict("records"))
        common_n = len(p)
        p_err = p.persistence_prediction.to_numpy(float) - p.persistence_label.to_numpy(float)
        s_err = p.seasonal_naive_prediction.to_numpy(float) - p.seasonal_naive_label.to_numpy(float)
        _, p_mae, p_rmse = metrics(p_err)
        _, s_mae, s_rmse = metrics(s_err)
        diffs = p.seasonal_minus_persistence_abs_error.to_numpy(float)
        origin_rows.append({
            "origin_id": origin, "candidate_issue_count": candidate_n, "valid_target_pair_count": valid_n,
            "persistence_scored_count": method_stats["persistence"]["n"],
            "persistence_candidate_coverage": method_stats["persistence"]["candidate_coverage"],
            "persistence_valid_target_coverage": method_stats["persistence"]["valid_target_coverage"],
            "persistence_separate_mae": method_stats["persistence"]["mae"], "persistence_separate_rmse": method_stats["persistence"]["rmse"],
            "seasonal_scored_count": method_stats["seasonal_naive"]["n"],
            "seasonal_candidate_coverage": method_stats["seasonal_naive"]["candidate_coverage"],
            "seasonal_valid_target_coverage": method_stats["seasonal_naive"]["valid_target_coverage"],
            "seasonal_separate_mae": method_stats["seasonal_naive"]["mae"], "seasonal_separate_rmse": method_stats["seasonal_naive"]["rmse"],
            "candidate_coverage_difference_seasonal_minus_persistence": method_stats["seasonal_naive"]["candidate_coverage"] - method_stats["persistence"]["candidate_coverage"],
            "valid_target_coverage_difference_seasonal_minus_persistence": method_stats["seasonal_naive"]["valid_target_coverage"] - method_stats["persistence"]["valid_target_coverage"],
            "paired_count": common_n, "paired_persistence_mae": p_mae, "paired_persistence_rmse": p_rmse,
            "paired_seasonal_mae": s_mae, "paired_seasonal_rmse": s_rmse,
            "paired_mae_difference_seasonal_minus_persistence": (s_mae - p_mae) if common_n else np.nan,
            "paired_mean_abs_error_difference_seasonal_minus_persistence": float(np.mean(diffs)) if common_n else np.nan,
            "paired_median_abs_error_difference_seasonal_minus_persistence": float(np.median(diffs)) if common_n else np.nan,
            "seasonal_win_count": int((p.pair_result_for_seasonal == "win").sum()),
            "tie_count": int((p.pair_result_for_seasonal == "tie").sum()),
            "seasonal_loss_count": int((p.pair_result_for_seasonal == "loss").sum()),
            "population_sensitivity_note": "Separate-population MAE is descriptive only; paired common-population results are the fair within-origin comparison.",
        })
    return pd.DataFrame(origin_rows), pd.DataFrame(pair_rows)


def prediction_summaries(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    day_rows, origin_rows = [], []
    for keys, g in d.groupby(["phase", "origin_id", "issue_day", "method"], sort=True):
        phase, origin, day, method = keys
        candidates = int(g.issue_row.nunique())
        valid = int(g.target_pair_eligible.sum())
        avail = int(g.prediction_available.sum())
        scored = g[g.target_pair_eligible & g.prediction_available]
        err = scored.prediction.to_numpy(float) - scored.observed_tp2.to_numpy(float)
        n, mae, rmse = metrics(err)
        day_rows.append({"phase": phase, "origin_id": origin, "issue_day": day.strftime("%Y-%m-%d"), "method": method,
                         "candidate_issue_count": candidates, "valid_target_pair_count": valid,
                         "available_prediction_count": avail, "scored_count": n,
                         "missing_or_invalid_target_count": candidates-valid,
                         "unavailable_prediction_count": candidates-avail,
                         "unavailable_prediction_rate": (candidates-avail)/candidates if candidates else np.nan,
                         "label_invalid_rate": (candidates-valid)/candidates if candidates else np.nan,
                         "prediction_coverage": avail/candidates if candidates else np.nan,
                         "scored_coverage_of_candidates": n/candidates if candidates else np.nan,
                         "mae": mae, "rmse": rmse, "evaluation_status": "HAS_CANDIDATE_ISSUES"})
    for (phase, origin, method), g in d.groupby(["phase", "origin_id", "method"], sort=True):
        candidates = int(g.issue_row.nunique()); valid = int(g.target_pair_eligible.sum()); avail = int(g.prediction_available.sum())
        scored = g[g.target_pair_eligible & g.prediction_available]
        err = scored.prediction.to_numpy(float)-scored.observed_tp2.to_numpy(float)
        n, mae, rmse = metrics(err)
        origin_rows.append({"phase": phase, "origin_id": origin, "method": method,
                            "candidate_issue_count": candidates, "valid_target_pair_count": valid,
                            "available_prediction_count": avail, "scored_count": n,
                            "candidate_coverage": avail/candidates if candidates else np.nan,
                            "valid_target_coverage": n/valid if valid else np.nan, "mae": mae, "rmse": rmse})
    daily = pd.DataFrame(day_rows)
    # Explicitly represent calendar days without frozen evaluation issues so plots
    # break across unevaluated gaps instead of connecting adjacent windows.
    for phase, windows in [("development", DEV), ("final", FINAL)]:
        start = pd.Timestamp(windows[0][1])
        end = pd.Timestamp(windows[-1][2]) - pd.Timedelta(days=1)
        observed = set(zip(daily.loc[daily.phase == phase, "issue_day"], daily.loc[daily.phase == phase, "method"]))
        for day in pd.date_range(start, end, freq="D"):
            day_s = day.strftime("%Y-%m-%d")
            for method in METHODS:
                if (day_s, method) not in observed:
                    day_rows.append({"phase": phase, "origin_id": None, "issue_day": day_s, "method": method,
                                     "candidate_issue_count": 0, "valid_target_pair_count": 0,
                                     "available_prediction_count": 0, "scored_count": 0,
                                     "missing_or_invalid_target_count": 0, "unavailable_prediction_count": 0,
                                     "unavailable_prediction_rate": np.nan, "label_invalid_rate": np.nan,
                                     "prediction_coverage": np.nan, "scored_coverage_of_candidates": np.nan,
                                     "mae": np.nan, "rmse": np.nan, "evaluation_status": "NO_SAVED_EVALUATION_ISSUES"})
                    observed.add((day_s, method))
    daily = pd.DataFrame(day_rows)
    return daily, pd.DataFrame(origin_rows)


def summarize_drift(sensor: pd.DataFrame) -> pd.DataFrame:
    sensor = sensor.copy()
    sensor["month"] = sensor.timestamp.dt.to_period("M").astype(str)
    ts_ns = sensor.timestamp.astype("int64").to_numpy()
    dt = np.diff(ts_ns) / 1e9
    gap_over_60 = np.r_[False, dt > 60]
    dup = np.r_[False, dt == 0]
    sensor["gap_over_60_before_row"] = gap_over_60
    sensor["duplicate_timestamp_after_previous"] = dup
    rows = []
    for month, g in sensor.groupby("month", sort=True):
        obs_ts = g.timestamp.astype("int64").to_numpy()
        diffs = np.diff(obs_ts)/1e9
        record = {"period_type": "calendar_month", "period_id": month, "row_count": int(len(g)),
                  "first_timestamp": g.timestamp.min().isoformat(sep=" "), "last_timestamp": g.timestamp.max().isoformat(sep=" "),
                  "timestamp_duplicate_count": int(np.sum(diffs == 0)),
                  "gap_over_60s_count": int(np.sum(diffs > 60)),
                  "gap_over_60s_rate_per_interval": float(np.mean(diffs > 60)) if len(diffs) else np.nan,
                  "sampling_interval_median_s": float(np.median(diffs)) if len(diffs) else np.nan,
                  "sampling_interval_p05_s": float(np.quantile(diffs, .05)) if len(diffs) else np.nan,
                  "sampling_interval_p95_s": float(np.quantile(diffs, .95)) if len(diffs) else np.nan}
        for col in ALL_COLS[1:]:
            if col in FEATURE_SIGNALS or col == "Caudal_impulses":
                vals = g[col].dropna().to_numpy(float)
                record[f"{col}_missing_rate"] = float(g[col].isna().mean())
                for q, val in zip([5,25,50,75,95], np.quantile(vals, [.05,.25,.5,.75,.95]) if len(vals) else [np.nan]*5):
                    record[f"{col}_p{q}"] = float(val)
        for col in STATE_SIGNALS:
            x = g[col].to_numpy(float)
            finite = np.isfinite(x)
            record[f"{col}_missing_rate"] = float(1-finite.mean())
            if finite.any():
                record[f"{col}_value_0_rate"] = float(np.mean(x[finite] == 0))
                record[f"{col}_value_1_rate"] = float(np.mean(x[finite] == 1))
                record[f"{col}_other_value_rate"] = float(np.mean(~np.isin(x[finite], [0,1])))
            else:
                record[f"{col}_value_0_rate"] = record[f"{col}_value_1_rate"] = record[f"{col}_other_value_rate"] = np.nan
            transitions = int(np.sum(np.isfinite(x[1:]) & np.isfinite(x[:-1]) & (x[1:] != x[:-1])))
            elapsed_hours = (g.timestamp.max()-g.timestamp.min()).total_seconds()/3600
            record[f"{col}_transitions"] = transitions
            record[f"{col}_transitions_per_hour"] = transitions/elapsed_hours if elapsed_hours else np.nan
        # Keep row position, not label index, as stable within-month order.
        rows.append(record)
    # Summaries for the exact frozen development/final evaluation periods.
    for phase, windows in [("development", DEV), ("final", FINAL)]:
        for oid, start, end in windows:
            a, b = pd.Timestamp(start), pd.Timestamp(end)
            g = sensor[(sensor.timestamp >= a) & (sensor.timestamp < b)]
            if not len(g):
                continue
            obs_ts = g.timestamp.astype("int64").to_numpy(); diffs=np.diff(obs_ts)/1e9
            record = {"period_type": "frozen_evaluation_window", "period_id": f"{phase}_{oid}", "row_count": int(len(g)),
                      "first_timestamp": g.timestamp.min().isoformat(sep=" "), "last_timestamp": g.timestamp.max().isoformat(sep=" "),
                      "timestamp_duplicate_count": int(np.sum(diffs == 0)), "gap_over_60s_count": int(np.sum(diffs > 60)),
                      "gap_over_60s_rate_per_interval": float(np.mean(diffs > 60)) if len(diffs) else np.nan,
                      "sampling_interval_median_s": float(np.median(diffs)) if len(diffs) else np.nan,
                      "sampling_interval_p05_s": float(np.quantile(diffs,.05)) if len(diffs) else np.nan,
                      "sampling_interval_p95_s": float(np.quantile(diffs,.95)) if len(diffs) else np.nan}
            for col in FEATURE_SIGNALS + STATE_SIGNALS + ["Caudal_impulses"]:
                x = g[col].to_numpy(float); record[f"{col}_missing_rate"] = float(np.mean(~np.isfinite(x)))
                vals=x[np.isfinite(x)]
                if col in FEATURE_SIGNALS or col == "Caudal_impulses":
                    for q,val in zip([5,25,50,75,95], np.quantile(vals,[.05,.25,.5,.75,.95]) if len(vals) else [np.nan]*5): record[f"{col}_p{q}"]=float(val)
                if col in STATE_SIGNALS:
                    record[f"{col}_value_0_rate"]=float(np.mean(vals==0)) if len(vals) else np.nan
                    record[f"{col}_value_1_rate"]=float(np.mean(vals==1)) if len(vals) else np.nan
                    record[f"{col}_other_value_rate"]=float(np.mean(~np.isin(vals,[0,1]))) if len(vals) else np.nan
                    record[f"{col}_transitions"]=int(np.sum(np.isfinite(x[1:])&np.isfinite(x[:-1])&(x[1:]!=x[:-1])))
                    hours=(g.timestamp.max()-g.timestamp.min()).total_seconds()/3600
                    record[f"{col}_transitions_per_hour"]=record[f"{col}_transitions"]/hours if hours else np.nan
            rows.append(record)
    return pd.DataFrame(rows)


def ridge_regime_summary(final: pd.DataFrame, sensor: pd.DataFrame) -> pd.DataFrame:
    # Feature eligibility and COMP are descriptive issue-time diagnostics only;
    # COMP is not introduced into the frozen model.
    comp = sensor.COMP.to_numpy(float)
    motor = sensor.Motor_current.to_numpy(float)
    ts = sensor.timestamp.astype("int64").to_numpy()
    issue_idx = final.issue_row.to_numpy(int)
    gap_rows = np.flatnonzero(np.diff(ts) > 60_000_000_000)
    start_time = ts[issue_idx] - 300_000_000_000
    start_row = np.searchsorted(ts, start_time, side="left")
    left = np.searchsorted(gap_rows, start_row, side="left")
    right = np.searchsorted(gap_rows, issue_idx, side="left")
    final = final.copy()
    final["issue_COMP"] = comp[issue_idx]
    final["issue_Motor_current"] = motor[issue_idx]
    final["gap_in_lookback_300s"] = right > left
    rows = []
    # one record per origin/regime/state with common denominators visible
    for group_col in ["issue_COMP", "gap_in_lookback_300s"]:
        for (origin, value), g in final.groupby(["origin_id", group_col], dropna=False, sort=True):
            issues = g[g.method == "persistence"]
            ridge = g[g.method == "ridge"]
            candidate = int(issues.issue_row.nunique())
            feature_rows = ridge[ridge.feature_eligible]
            rows.append({"origin_id": origin, "stratifier": group_col, "stratum": str(value),
                         "candidate_issue_count": candidate,
                         "feature_eligible_issue_count": int(feature_rows.issue_row.nunique()),
                         "feature_eligibility_rate": int(feature_rows.issue_row.nunique())/candidate if candidate else np.nan,
                         "ridge_available_count": int(ridge.prediction_available.sum()),
                         "ridge_scored_count": int((ridge.prediction_available & ridge.target_pair_eligible).sum()),
                         "motor_current_median_A": float(np.nanmedian(issues.issue_Motor_current)) if issues.issue_Motor_current.notna().any() else np.nan,
                         "regime_interpretation": "Descriptive association only; COMP and continuity are not causal explanations."})
    return pd.DataFrame(rows)


def critical_period_analysis(allpred: pd.DataFrame, sensor: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    source_ts=sensor.timestamp
    for ev in EVENTS:
        start,end=pd.Timestamp(ev["start"]),pd.Timestamp(ev["end"])
        source_n=int(((source_ts>=start)&(source_ts<=end)).sum())
        overlap=[]
        for phase, windows in [("development",DEV),("final",FINAL)]:
            for oid, ws, we in windows:
                if start < pd.Timestamp(we) and end >= pd.Timestamp(ws): overlap.append((phase,oid))
        for phase,oid in overlap:
            origin_all=allpred[(allpred.phase==phase)&(allpred.origin_id==oid)]
            event_issue=set(origin_all[(origin_all.method=="persistence")&(origin_all.issue_timestamp>=start)&(origin_all.issue_timestamp<=end)].issue_row.astype(int))
            for label, rows_g in [("reported_event_issue_times",origin_all[origin_all.issue_row.isin(event_issue)]),
                                  ("other_eligible_issue_times_same_origin",origin_all[~origin_all.issue_row.isin(event_issue)])]:
                for method in METHODS:
                    m=rows_g[rows_g.method==method]
                    scored=m[m.target_pair_eligible&m.prediction_available]
                    err=scored.prediction.to_numpy(float)-scored.observed_tp2.to_numpy(float)
                    n,mae,rmse=metrics(err)
                    rows.append({"event_id":ev["event_id"],"official_report_number":ev["report_number"],"event_description":ev["event"],
                                 "official_start_inclusive_naive_time":ev["start"],"official_end_inclusive_naive_time":ev["end"],
                                 "phase":phase,"origin_id":oid,"comparison_group":label,"method":method,
                                 "source_observation_count_in_reported_period":source_n,"candidate_issue_count":int(m.issue_row.nunique()),
                                 "valid_target_pair_count":int(m.target_pair_eligible.sum()),"available_prediction_count":int(m.prediction_available.sum()),
                                 "scored_count":n,"mae":mae,"rmse":rmse,
                                 "source_note":ev["source_note"],"timestamp_alignment_note":"Issue timestamps and report timestamps are naive; timezone/alignment is unverified.",
                                 "labeling_note":"Event membership is assigned by forecast issue timestamp; this is retrospective subgrouping, not a causal/event-truth label."})
                # Paired baseline row for exact issue/target identity, separate from method-specific rows.
                p=rows_g[(rows_g.method=="persistence")&rows_g.target_pair_eligible&rows_g.prediction_available]
                s=rows_g[(rows_g.method=="seasonal_naive")&rows_g.target_pair_eligible&rows_g.prediction_available]
                pair=p[["origin_id","issue_row","target_row","prediction","observed_tp2"]].merge(
                    s[["origin_id","issue_row","target_row","prediction"]],on=["origin_id","issue_row","target_row"],suffixes=("_persistence","_seasonal"),validate="one_to_one")
                pe=pair.prediction_persistence.to_numpy(float)-pair.observed_tp2.to_numpy(float)
                se=pair.prediction_seasonal.to_numpy(float)-pair.observed_tp2.to_numpy(float)
                n,pmae,prmse=metrics(pe); _,smae,srmse=metrics(se)
                rows.append({"event_id":ev["event_id"],"official_report_number":ev["report_number"],"event_description":ev["event"],
                             "official_start_inclusive_naive_time":ev["start"],"official_end_inclusive_naive_time":ev["end"],
                             "phase":phase,"origin_id":oid,"comparison_group":label,"method":"paired_baselines",
                             "source_observation_count_in_reported_period":source_n,"candidate_issue_count":int(pair.issue_row.nunique()),
                             "valid_target_pair_count":n,"available_prediction_count":n,"scored_count":n,
                             "mae":pmae,"rmse":prmse,"paired_persistence_mae":pmae,"paired_persistence_rmse":prmse,
                             "paired_seasonal_mae":smae,"paired_seasonal_rmse":srmse,"paired_count":n,
                             "source_note":ev["source_note"],"timestamp_alignment_note":"Issue timestamps and report timestamps are naive; timezone/alignment is unverified.",
                             "labeling_note":"Event membership is assigned by forecast issue timestamp; this is retrospective subgrouping, not a causal/event-truth label."})
        if not overlap:
            rows.append({"event_id":ev["event_id"],"official_report_number":ev["report_number"],"event_description":ev["event"],
                         "official_start_inclusive_naive_time":ev["start"],"official_end_inclusive_naive_time":ev["end"],
                         "phase":None,"origin_id":None,"comparison_group":"no_saved_evaluation_window_overlap","method":"all",
                         "source_observation_count_in_reported_period":source_n,"candidate_issue_count":0,"valid_target_pair_count":0,
                         "available_prediction_count":0,"scored_count":0,"mae":np.nan,"rmse":np.nan,
                         "source_note":ev["source_note"],"timestamp_alignment_note":"Issue timestamps and report timestamps are naive; timezone/alignment is unverified.",
                         "labeling_note":"Raw sensor observations exist, but the frozen protocol saved no evaluation predictions for this period."})
    return pd.DataFrame(rows)


def make_figures(daily: pd.DataFrame, origin: pd.DataFrame, final: pd.DataFrame, drift: pd.DataFrame,
                 paired: pd.DataFrame) -> list[Path]:
    FIG.mkdir(parents=True, exist_ok=True)
    outs=[]
    colors={"persistence":"#1f77b4","seasonal_naive":"#ff7f0e","ridge":"#2ca02c"}
    # Daily MAE in three method panels. Counts label each statistic; null days are not drawn as zero.
    fig,axes=plt.subplots(3,1,figsize=(14,12),sharex=True)
    fd=daily[daily.phase=="final"]
    for ax,method in zip(axes,METHODS):
        g=fd[fd.method==method].sort_values("issue_day")
        x=pd.to_datetime(g.issue_day); y=g.mae.to_numpy(float); n=g.scored_count.to_numpy(int)
        ax.plot(x,y,marker="o",lw=1.3,color=colors[method]); ax.set_title(f"{method}: daily MAE (n = scored forecasts at each point)")
        ax.set_ylabel("MAE (bar)"); ax.grid(alpha=.25)
        for xx,yy,nn,candidates in zip(x,y,n,g.candidate_issue_count.to_numpy(int)):
            if np.isfinite(yy): ax.annotate(f"n={nn}",(xx,yy),xytext=(0,5),textcoords="offset points",ha="center",fontsize=6)
            elif nn == 0:
                ax.annotate("no eval" if candidates == 0 else "n=0",(xx,ax.get_ylim()[0]),xytext=(0,3),textcoords="offset points",ha="center",fontsize=5,rotation=90)
    axes[-1].set_xlabel("Forecast issue day (gaps are days with no saved evaluation window)")
    fig.suptitle("Final evaluation: daily error by method; unavailable predictions are not zero errors")
    fig.tight_layout(); p=FIG/"phase3_daily_mae_final.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    # Coverage rates with numerator/denominator shown for every daily estimate.
    fig,axes=plt.subplots(3,1,figsize=(14,12),sharex=True)
    for ax,method in zip(axes,METHODS):
        g=fd[fd.method==method].sort_values("issue_day"); x=pd.to_datetime(g.issue_day)
        ax.plot(x,g.prediction_coverage,marker="o",color=colors[method],label="Prediction availability / candidates")
        ax.plot(x,g.scored_coverage_of_candidates,marker="x",ls="--",color="#555555",label="Scored / candidates")
        ax.set_ylim(-.03,1.05); ax.set_ylabel("Fraction"); ax.set_title(f"{method}: daily coverage (labels show available/candidate; scored/candidate in table)"); ax.grid(alpha=.25)
        for xx,yy,a,c in zip(x,g.prediction_coverage,g.available_prediction_count,g.candidate_issue_count):
            if c:
                ax.annotate(f"{a}/{c}",(xx,yy),xytext=(0,5),textcoords="offset points",ha="center",fontsize=5)
            else:
                ax.annotate("no eval",(xx,.02),xytext=(0,2),textcoords="offset points",ha="center",fontsize=5,rotation=90)
        ax.legend(loc="lower left",fontsize=7)
    axes[-1].set_xlabel("Forecast issue day")
    fig.suptitle("Final evaluation: daily prediction availability and scored coverage")
    fig.tight_layout(); p=FIG/"phase3_daily_coverage_final.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    # Final per-origin MAE/RMSE with exact scored n labels.
    fo=origin[(origin.phase=="final")].copy(); order=[x[0] for x in FINAL]
    fig,axes=plt.subplots(1,2,figsize=(14,6))
    width=.24; xpos=np.arange(len(order))
    for k,method in enumerate(METHODS):
        g=fo[fo.method==method].set_index("origin_id").reindex(order); x=xpos+(k-1)*width
        for ax,col,title in [(axes[0],"mae","MAE by origin"),(axes[1],"rmse","RMSE by origin")]:
            vals=g[col].to_numpy(float); bars=ax.bar(x,vals,width,label=method,color=colors[method])
            for xx,v,n in zip(x,vals,g.scored_count.to_numpy(int)):
                if np.isfinite(v): ax.annotate(f"n={n}",(xx,v),xytext=(0,3),textcoords="offset points",ha="center",fontsize=6,rotation=90)
            ax.set_title(title); ax.set_ylabel("Error (bar)"); ax.grid(axis="y",alpha=.25)
    for ax in axes: ax.set_xticks(xpos,order); ax.legend(fontsize=8)
    fig.suptitle("Final per-origin errors; each method's metric uses its own eligible scored population")
    fig.tight_layout(); p=FIG/"phase3_final_origin_metrics.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    # Method-specific final error distributions; counts are explicit and populations differ.
    fig,ax=plt.subplots(figsize=(9,6)); arrays=[]; labels=[]
    for method in METHODS:
        g=final[(final.method==method)&final.target_pair_eligible&final.prediction_available]
        arrays.append((g.prediction-g.observed_tp2).abs().to_numpy(float)); labels.append(f"{method}\nn={len(g):,}")
    ax.boxplot(arrays,tick_labels=labels,showfliers=False); ax.set_ylabel("Absolute error (bar)"); ax.grid(axis="y",alpha=.25)
    ax.set_title("Final absolute-error distributions (method-specific populations; not paired comparisons)")
    fig.tight_layout(); p=FIG/"phase3_final_error_distributions.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    # Observed monthly sensor distributions and continuity summaries.
    mon=drift[drift.period_type=="calendar_month"].sort_values("period_id"); fig,axes=plt.subplots(5,1,figsize=(13,16),sharex=True)
    dates=pd.to_datetime(mon.period_id+"-15")
    for ax,col,label in zip(axes[:4],FEATURE_SIGNALS,["TP2 (bar)","TP3 (bar)","Motor current (A)","Oil temperature (C)"]):
        med=mon[f"{col}_p50"].to_numpy(float); lo=mon[f"{col}_p25"].to_numpy(float); hi=mon[f"{col}_p75"].to_numpy(float)
        ax.plot(dates,med,marker="o"); ax.fill_between(dates,lo,hi,alpha=.2); ax.set_ylabel(label); ax.grid(alpha=.25)
    axes[4].plot(dates,mon.gap_over_60s_count,marker="o",color="#d62728",label="Intervals >60s (count)")
    axes[4].set_ylabel("Gap count"); axes[4].grid(alpha=.25)
    right=axr=axes[4].twinx(); right.plot(dates,mon.COMP_value_1_rate,marker="s",color="#9467bd",label="COMP=1 share")
    right.set_ylabel("COMP=1 share")
    left_handles,left_labels=axes[4].get_legend_handles_labels(); right_handles,right_labels=right.get_legend_handles_labels()
    axes[4].legend(left_handles+right_handles,left_labels+right_labels,loc="best")
    axes[4].set_xticks(dates,[f"{m}\nn={n:,}" for m,n in zip(mon.period_id,mon.row_count)],fontsize=7)
    axes[4].set_xlabel("Calendar month and source-observation count (upper panels show median and IQR)")
    fig.suptitle("Observed sensor and continuity distributions by calendar month")
    fig.tight_layout(); p=FIG/"phase3_monthly_drift_overview.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    # Paired seasonal-vs-persistence per-pair absolute error differences.
    fig,ax=plt.subplots(figsize=(10,6)); labels=[]; vals=[]
    for oid,g in paired.groupby("origin_id",sort=False):
        labels.append(f"{oid}\nn={len(g)}"); vals.append(g.seasonal_minus_persistence_abs_error.to_numpy(float))
    if vals:
        ax.boxplot(vals,tick_labels=labels,showfliers=False); ax.axhline(0,color="black",lw=1,ls="--")
    ax.set_ylabel("Seasonal-naive − Persistence absolute error (bar)"); ax.set_title("Exact paired final baseline errors; negative favors seasonal-naive per pair")
    ax.grid(axis="y",alpha=.25); fig.tight_layout(); p=FIG/"phase3_paired_baseline_error_difference.png"; fig.savefig(p,dpi=160); plt.close(fig); outs.append(p)
    return outs


def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True)
    hashes=verify_inputs()
    sensor=pd.read_csv(DATA,usecols=ALL_COLS,parse_dates=["timestamp"])
    if not sensor.timestamp.is_monotonic_increasing:
        raise AssertionError("Original observation timestamps are not sorted")
    dev,final=read_predictions("development"),read_predictions("final")
    counts=verify_predictions(dev,final)
    allpred=pd.concat([dev,final],ignore_index=True)
    metric_checks=verify_saved_metrics(allpred)
    paired_summary,paired_pairs=paired_baseline_outputs(final)
    daily,origin=prediction_summaries(allpred)
    for r in origin.itertuples(index=False):
        dg=daily[(daily.phase==r.phase)&(daily.origin_id==r.origin_id)&(daily.method==r.method)]
        if (int(dg.candidate_issue_count.sum()) != r.candidate_issue_count or
            int(dg.valid_target_pair_count.sum()) != r.valid_target_pair_count or
            int(dg.available_prediction_count.sum()) != r.available_prediction_count or
            int(dg.scored_count.sum()) != r.scored_count):
            raise AssertionError(f"Daily-to-origin count reconciliation failed: {r.phase} {r.origin_id} {r.method}")
    drift=summarize_drift(sensor)
    regime=ridge_regime_summary(final,sensor)
    critical=critical_period_analysis(allpred,sensor)
    outputs=[]
    products=[(paired_summary,"paired_baseline_comparison.csv"),(paired_pairs,"paired_baseline_pairs.csv"),
              (daily,"error_coverage_by_day.csv"),(origin,"origin_metric_coverage_summary.csv"),
              (drift,"drift_summary.csv"),(regime,"ridge_availability_by_regime.csv"),
              (critical,"critical_period_summary.csv")]
    for frame,name in products:
        path=OUT/name; frame.to_csv(path,index=False); outputs.append(path)
    outputs.extend(make_figures(daily,origin,final,drift,paired_pairs))
    # A descriptive persistence fallback replay is explicitly not a deployed or validated policy.
    hy=final[final.target_pair_eligible].pivot_table(index=["origin_id","issue_row","target_row"],columns="method",values="prediction",aggfunc="first").reindex(columns=METHODS)
    avail=final[final.method=="ridge"].set_index(["origin_id","issue_row","target_row"]).prediction_available.reindex(hy.index).fillna(False).astype(bool)
    hybrid=hy.ridge.where(avail,hy.persistence)
    labels=final[(final.method=="persistence")&final.target_pair_eligible].set_index(["origin_id","issue_row","target_row"]).observed_tp2.reindex(hy.index)
    he=hybrid.to_numpy(float)-labels.to_numpy(float); hn,hmae,hrmse=metrics(he)
    valid_ridge=final[(final.method=="ridge")&final.target_pair_eligible]
    fallback_n=int((~valid_ridge.prediction_available).sum()); valid_n=int(len(valid_ridge))
    fallback_record={"status":"DESCRIPTIVE_OFFLINE_REPLAY_ONLY","rule":"Use saved Ridge prediction when available; otherwise use saved persistence prediction.",
                     "eligible_target_count":valid_n,"fallback_trigger_count":fallback_n,
                     "fallback_trigger_fraction_of_valid_targets":fallback_n/valid_n if valid_n else None,
                     "prediction_coverage_after_replay":hn/valid_n if valid_n else None,
                     "scored_count":hn,"mae":hmae,"rmse":hrmse,
                     "caveats":["This policy was not implemented or live-tested.","This is an explicitly permitted retrospective availability replay, not a new confirmatory model comparison.","Persistence and labels rely on the frozen zero-additional-latency retrospective assumption."]}
    fb=OUT/"fallback_replay_summary.json"; fb.write_text(json.dumps(fallback_record,indent=2)); outputs.append(fb)
    output_hashes={str(p.relative_to(ROOT)):sha256(p) for p in outputs}
    source_ts=sensor.timestamp
    source_dt=source_ts.diff().dt.total_seconds().dropna()
    sensor_cols=[c for c in ALL_COLS if c!="timestamp"]
    dataset_overview={"row_count":int(len(sensor)),"timestamp_min_naive":source_ts.min().isoformat(sep=" "),
                      "timestamp_max_naive":source_ts.max().isoformat(sep=" "),"timestamp_order_monotonic":bool(source_ts.is_monotonic_increasing),
                      "duplicate_timestamp_extra_rows":int(source_ts.duplicated().sum()),
                      "sensor_missing_value_total":int(sensor[sensor_cols].isna().sum().sum()),
                      "sensor_missing_counts":{c:int(sensor[c].isna().sum()) for c in sensor_cols},
                      "sampling_interval_seconds":{"median":float(source_dt.median()),"p05":float(source_dt.quantile(.05)),"p95":float(source_dt.quantile(.95))},
                      "intervals_over_60_seconds":int((source_dt>60).sum()),
                      "intervals_over_60_seconds_rate":float((source_dt>60).mean()),
                      "timestamp_semantics":"Naive event-time values; source file index is not used as elapsed time."}
    manifest={"phase":"3","status":"PASS_WITH_LIMITATIONS","dataset":"MetroPT-3","dataset_sha256":hashes[str(DATA.relative_to(ROOT))],
              "source_hashes":hashes,"prediction_rows":counts,"protocol_commit":"ca83f0a295a68337aebc070cfd481645418cda13",
              "analysis_script_sha256":sha256(Path(__file__).resolve()),
              "dataset_overview":dataset_overview,
              "critical_period_source_url":UCI_URL,
              "critical_period_timestamp_basis":"UCI company-report windows are interpreted as naive timestamps and assigned by forecast issue time; timezone alignment is unverified.",
              "metric_definitions":{"MAE":"mean absolute (prediction - observed TP2) among available predictions with valid target pairs","RMSE":"square root of mean squared (prediction - observed TP2) on the same scored rows","paired_error_difference":"seasonal-naive absolute error minus persistence absolute error, paired on origin_id + issue_row + actual target_row"},
              "pairing_identity":"origin_id + issue_row + actual target_row",
              "execution_command":"conda run -n nussem1 python scripts/analyze_phase3.py",
              "verification":{"input_hashes_match_phase2b_audit":True,"paired_rows_use_exact_identity":True,"invalid_targets_excluded":True,"unavailable_predictions_not_zero_errors":True,"all_methods_per_issue":True,"metrics_recomputed_from_saved_predictions":True,**metric_checks},
              "versions":{"python":platform.python_version(),"numpy":np.__version__,"pandas":pd.__version__,"matplotlib":matplotlib.__version__},
              "critical_period_events":EVENTS,
              "assumptions_and_limits":["Source and UCI event timestamps are naive; timezone/alignment cannot be established.","Rows are strongly serially dependent and forecast horizons overlap; forecast rows are not independent replicates.","Failure windows are retrospective labels, not verified event truth at the sensor clock.","Rolling origin metrics are descriptive; no causal drift attribution or deployment threshold validation is performed.","Daily Ridge metrics are shown only with explicit scored sample counts; zero-coverage days remain missing metrics."],
              "outputs":output_hashes}
    manifest_path=OUT/"analysis_manifest.json"; manifest_path.write_text(json.dumps(manifest,indent=2,default=str))
    print(json.dumps({"status":manifest["status"],"input_hashes_verified":len(hashes),"prediction_rows":counts,"metric_checks":metric_checks,
                      "paired_counts":paired_summary[["origin_id","paired_count"]].to_dict("records"),
                      "output_files":len(outputs),"manifest":str(manifest_path.relative_to(ROOT))},indent=2))


if __name__ == "__main__":
    main()
