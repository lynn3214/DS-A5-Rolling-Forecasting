# NOAA SanctSound Dataset Feasibility Audit

## Executive verdict: PARTIAL

**PARTIAL** — official NOAA catalog metadata supports the existence and broad coverage of three processed `TOL_1h` candidate products, but direct data retrieval was blocked by DNS resolution failure. Therefore timestamp semantics, actual fields/units in retrieved arrays, gaps, valid stretches, monthly coverage, and five rolling origins cannot be empirically confirmed. No station/band is selected. Recommendation: do not begin Phase 2 using SanctSound until bounded ERDDAP retrieval and the quality audit succeed.

## Evidence and status

- **VERIFIED (metadata-level):** three station records and stated coverage spans listed in `candidate_comparison.md`.
- **VERIFIED (metadata-level):** TOLs represent one-third-octave bands; NOAA descriptions define hourly values as medians of qualifying one-second values, converted to dB re 1 µPa. Minimum counts differ by record (SB02_07: 1,800; PM02_01: 1,782); verify exact FK03_04 product detail before use.
- **BLOCKED:** direct NOAA passive-acoustic landing page and ERDDAP endpoints could not resolve from this runtime. Exact errors are in `sources.md` and `data/manifest.json`.
- **UNKNOWN:** array schema, units/attributes, frequency coordinate, fill values, quality flags, timestamp timezone and interval convention, duplicate/out-of-order records, missing hours, file sizes/checksums, license terms, actual publication latency.
- **ASSUMED only:** hypothetical retrospective low-latency forecasting where only completed past intervals are admissible. Historical real-time availability is not established.

## Candidate/task feasibility

The metadata spans vary considerably. SB02_07 and FK03_04 may be short for a robust five-origin study; PM02_01 has the longest stated span. This is an inference from catalog coverage, not proof of continuity. A candidate task could forecast one documented band for the next completed hourly interval from prior completed band observations and deterministic calendar features. The target must be aligned to the interval end only after inspecting coordinate attributes. Persistence is conceptually possible; a 24-hour seasonal naive baseline requires verified daily continuity and is currently unconfirmed.

## Rolling origins and critical periods

No rolling origins are proposed as verified time points because no observed timestamps or gaps were retrieved. At least five chronological origins, usable training counts, and evaluation coverage must be generated from the actual timestamp index after retrieval. Expanding/sliding feasibility is UNKNOWN. High-noise periods defined from held-out targets would be post-hoc descriptive subgrouping, not a prospective trigger. Exploratory nonstationarity and statistically established drift cannot be assessed without observations.

## Leakage risks to control in a later phase

Fit normalization and preprocessing inside each training window; use only completed observations at issue time; prohibit future-aware temporal joins, interpolation, global imputation, target-derived filtering, lookahead rolling statistics, QC based on future values, and station/band selection based on held-out errors. Keep outages explicit.

## Workload, limits, and recommendation

The audit script is standard-library-only and lightweight. It currently probes dataset metadata endpoints and records failures; it does not yet retrieve tabular observations or calculate quality metrics. This is an explicit limitation, not an empirical pass. If NOAA access remains unavailable, investigate UR3 CobotOps or a conventional hourly series as alternatives, but do not silently substitute them in this audit.

**Go/no-go:** no-go for Phase 2 pending empirical access verification. **Single next action:** rerun `conda activate nussem1 && python scripts/audit_noaa.py` in an environment with NOAA DNS/network access, then extend the same audit to a fixed bounded hourly subset before selecting a station.

## Execution/verification log

- Python: 3.10.18, conda environment `nussem1`.
- `conda run -n nussem1 python scripts/audit_noaa.py`: process returned exit 2 (all three candidates BLOCKED); manifest written.
- Direct NOAA curl probe: failed, `curl: (6) Could not resolve host: www.ncei.noaa.gov`.
- No forecasting models or final assignment artifacts were created. No empirical observation statistics or figures are claimed.
