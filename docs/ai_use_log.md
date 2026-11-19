# AI use log

This is a factual summary of assistance in the DS-A5 repository. It does not reconstruct verbatim prompts or claim manual review of final assignment results.

| Work | AI assistance | Human review/status |
|---|---|---|
| Dataset feasibility | Codex inspected official NOAA/UCI sources, audited supplied local MetroPT-3 and UR3 data, and recorded access limitations and provenance. | User supplied local files and reviewed dataset-selection recommendations. NOAA ERDDAP access remained blocked. |
| Temporal protocol | Codex developed timestamp matching, gap, origin, availability, and leakage specifications and diagnostics. | ChatGPT independent analysis was reviewed by the user; the user explicitly approved freezing Evaluation Protocol v1.0 in the supplied request. |
| Code review and tests | Codex implemented non-modeling diagnostics and deterministic timestamp tests. | Tests and local integrity checks were executed and recorded; forecasting models were not trained. |
| Protocol freeze | Codex prepared the freeze manifest and repository commit. | User authorization was provided for protocol freezing and a local first commit. No GitHub push was performed. |

No final forecasting results exist in this phase. No claim is made that such results or a final notebook were manually reviewed.
