# Feature and label availability map

| Field | Exact timestamp rule | Eligibility | Availability evidence |
|---|---|---|---|
| TP2 lags 10/60/300s; TP3 and Motor_current lags 60/300s | Requested time = issue time minus lag | Latest row at or before requested time; age 0–5s; finite; no >60s adjacent timestamp gap from selected row through latest row at/before issue | No historical release log. Zero-additional-latency is a retrospective assumption only |
| Persistence TP2 | Historical row at/before issue | Latest finite value, age <=5s; no >60s gap from that row through issue | Same unverified assumption |
| Seasonal-naive TP2 | `reference=issue+600s-24h` | Latest finite observation at/before reference, reference minus observation 0–5s, and observation <= issue. No 24h-wide continuity requirement | Same unverified assumption |
| Label TP2 | Earliest row in `[issue+600s, issue+605s]` | Issue and target values finite; no >60s gap between issue and target. Training label actual timestamp <= origin; evaluation target < interval end | Archive has no publication timestamps |

All source timestamps are naive. Event time does not establish release time. No interpolation or future-looking feature lookup is allowed. Missing features make Ridge prediction unavailable; seasonal-naive unavailability is recorded, never replaced with persistence.
