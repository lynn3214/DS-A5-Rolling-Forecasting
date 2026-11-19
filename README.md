# DS-A5 Rolling Forecasting

This repository records the DS-A5 dataset feasibility audit and the frozen Evaluation Protocol v1.0. It does **not** contain Phase 2B model implementation, trained models, final evaluation results, or the final assignment notebook.

## Frozen protocol

The independently approved protocol uses MetroPT-3, predicts TP2 pressure (bar) 600 elapsed seconds ahead, and evaluates an expanding rolling-origin design. Full details and exact rules are in [`docs/evaluation_protocol_v1.md`](docs/evaluation_protocol_v1.md); the freeze record is [`docs/evaluation_protocol_freeze_manifest.json`](docs/evaluation_protocol_freeze_manifest.json).

## Data acquisition and integrity

The original MetroPT-3 CSV is excluded from Git. Obtain it from the official UCI page:

- Dataset page: https://archive.ics.uci.edu/dataset/791/metropt3%2Bdataset
- Official archive: https://archive.ics.uci.edu/static/public/791/metropt%2B3%2Bdataset.zip

Extract `MetroPT3(AirCompressor).csv` to `data/raw/metropt3/`, then verify the expected SHA-256:

```sh
shasum -a 256 'data/raw/metropt3/MetroPT3(AirCompressor).csv'
```

Expected SHA-256: `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`.

## Environment and audit reproduction

Use the `nussem1` conda environment. Dependencies used by the audit are listed in `requirements.txt`.

```sh
conda activate nussem1
python scripts/audit_alternatives.py
python scripts/diagnose_forecast_task.py
python -m pytest -q tests
```

These commands reproduce the data audit and non-modeling diagnostics; they do not train forecasting models. See `docs/sources.md` for provenance and the preserved NOAA/UR3 feasibility investigations.

## AI-use disclosure

See [`docs/ai_use_log.md`](docs/ai_use_log.md). The log distinguishes Codex implementation, ChatGPT independent analysis, and user review. No claim is made that final assignment results have been manually reviewed.
