# Local Artifact Registry

Large source data and row-level prediction exports remain local and are excluded from Git. The compact metrics, manifests, execution logs, audit tables, reports, analysis tables, and figures are committed. This registry preserves local artifact provenance and reproduction instructions.

All file sizes are bytes. SHA-256 values were computed from the local files during the Phase 2B/3 documentation review.

## Original local source files excluded from Git

| Relative path | Size | SHA-256 | Source / retrieval |
|---|---:|---|---|
| `data/raw/metropt3/MetroPT3(AirCompressor).csv` | 218,300,507 | `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24` | UCI MetroPT-3 official archive listed in `docs/sources.md`; extract the CSV to this path |
| `data/raw/metropt3/Data Description_Metro.pdf` | 81,208 | `b00fac0e8899854078309bef4adaa480d82ecf14dc81c5097c3646973e824127` | PDF supplied in/extracted from the official UCI MetroPT-3 archive |
| `data/raw/ur3/dataset_02052023.xlsx` | 1,771,022 | `f0f10917de9056908a82cec1aa459ddf9da2d2db70d269b128f99241c8796091` | UCI UR3 CobotOps official archive listed in `docs/sources.md` |

Official retrieval URLs:

- MetroPT-3 page: https://archive.ics.uci.edu/dataset/791/metropt3%2Bdataset
- MetroPT-3 archive: https://archive.ics.uci.edu/static/public/791/metropt%2B3%2Bdataset.zip
- UR3 CobotOps page: https://archive.ics.uci.edu/dataset/963/ur3%2Bcobotops
- UR3 CobotOps archive: https://archive.ics.uci.edu/static/public/963/ur3%2Bcobotops.zip

For the MetroPT-3 source, download/extract the official archive and check the CSV hash with:

```sh
shasum -a 256 'data/raw/metropt3/MetroPT3(AirCompressor).csv'
```

The local UR3 XLSX is retained as source evidence but is not required to reproduce Phase 2B/3.

## Large row-level rolling prediction exports excluded from Git

| Relative path | Size | SHA-256 | Status / reproduction |
|---|---:|---|---|
| `results/rolling/development_predictions.csv` | 337,243,277 | `c53e94087feb4c2bd10cab0df0c3e08f4364f2eb97f10c22d9508575fe20d586` | Completed development output; regenerate using the development command below |
| `results/rolling/final_predictions.csv` | 120,884,905 | `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41` | Completed final output; regenerate using the final command below |
| `results/rolling/attempt_1/development_predictions.csv` | 266,588,905 | `497dadfbada32c4660832a17c71161b8b530d44a386797cae0fe4267b9300aa4` | Historical intermediate snapshot; its attempt manifest/log records the execution command. Preserve locally; current code regenerates the completed top-level output, not this intermediate snapshot |
| `results/rolling/attempt_1/final_predictions.csv` | 120,083,970 | `0919bf22d5dc36a1b05c6fb3d5e54091ec8a2407a8e65677d798db918bfb6d24` | Historical attempt snapshot; its attempt manifest/log records the execution command. Preserve locally |
| `results/rolling/attempt_2/development_predictions.csv` | 268,432,817 | `81d08f9f82c272cfe908fa6207ed182108654f0a6b0d29e0951d50f783251d5b` | Historical intermediate snapshot; its attempt manifest/log records the execution command. Preserve locally |
| `results/rolling/attempt_2/final_predictions.csv` | 120,884,905 | `e2cdf4de6f838f8f06d241149e514d09bc33e0192ac5073b7d1e02e83a12db41` | Historical attempt snapshot with the same hash as the completed final output |

The historical attempt directories, metrics, manifests, and runner logs remain preserved in Git. The prediction CSVs are omitted because they total over 1.2 GB and are exactly regenerable for the completed run from the frozen protocol, checked source data, and runner below; failed/intermediate attempts are retained by hash, metrics, manifest, and logs rather than uploading redundant hundreds-of-megabytes snapshots.

## Reproduction commands

Run in the `nussem1` Conda environment after verifying the MetroPT-3 source hash. The two evaluation commands execute the frozen rolling evaluation and create the large ignored row-level CSVs; they are listed for reproducibility and were not rerun to create the documentation commits.

```sh
conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase development
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase development
conda run -n nussem1 python scripts/run_rolling_evaluation.py --phase final
conda run -n nussem1 python scripts/verify_rolling_outputs.py --phase final
conda run -n nussem1 python scripts/audit_phase2b_outputs.py
conda run -n nussem1 python scripts/analyze_phase3.py
```

Phase 3 requires the local source CSV and the completed development/final prediction CSVs. Its inputs, outputs, hashes, metric definitions, and software versions are recorded in `results/analysis/analysis_manifest.json`.
