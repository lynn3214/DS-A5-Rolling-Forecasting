# Source registry

UCI official dataset pages, inspected for Phase 1B/1C:

- MetroPT-3: https://archive.ics.uci.edu/dataset/791/metropt3%2Bdataset — DOI `10.24432/C5VW3R`, CC BY 4.0. Official listed archive URL: https://archive.ics.uci.edu/static/public/791/metropt%2B3%2Bdataset.zip
- UR3 CobotOps: https://archive.ics.uci.edu/dataset/963/ur3%2Bcobotops — DOI `10.24432/C5J891`, CC BY 4.0. Official listed archive URL: https://archive.ics.uci.edu/static/public/963/ur3%2Bcobotops.zip

Phase 3 failure-period provenance:

- MetroPT-3 UCI dataset record: https://archive.ics.uci.edu/dataset/791/metropt%2B3%2Bdataset. The official page provides company-reported air-leak windows and associated maintenance notes. Its first two failure rows both carry report number `#1`; the second row's `30Apr` maintenance note predates its stated May 29–30 event window. These source inconsistencies and unspecified timezone are retained as uncertainties in the Phase 3 analysis.

Phase 1C local files supplied under `data/raw/` and audited without modification:

- `data/raw/metropt3/MetroPT3(AirCompressor).csv`, SHA-256 `db30ccb4ea402e3c8bf2c99db06e288d4f2a772f6928f9dbe26a920d69793e24`, 218300507 bytes.
- `data/raw/ur3/dataset_02052023.xlsx`, SHA-256 `f0f10917de9056908a82cec1aa459ddf9da2d2db70d269b128f99241c8796091`, 1771022 bytes.

Earlier incomplete download attempts remain recorded in `results/audit/alternative_audit.json`; NOAA sources and HTTP 403 evidence remain in `data/manifest.json` and NOAA documents.
