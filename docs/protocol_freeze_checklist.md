# Protocol freeze checklist

- [x] Dataset/target/horizon and future-only target matching agree with executed development diagnostics.
- [x] Actual matched-label timestamp is used for origin availability in the diagnostic implementation.
- [x] Finite issue and target TP2 values are required; missing feature histories are defined as unavailable.
- [x] 60-second gap rule is explicit for issue-to-target and feature-history segments.
- [x] Persistence and deterministic seasonal-naive lookup rules are specified; no silent baseline substitution.
- [x] Ridge recipe, fixed feature order, window-local scaling, and no tuning are specified.
- [x] Development and candidate final interval boundaries and retraining rules are specified.
- [x] Method-specific coverage and common-timestamp metrics are prespecified.
- [x] Drift, critical-period, negative-result, and hypothetical fallback analyses are defined.
- [x] Seasonal/lag matcher, boundary, NaN, and gap tests executed successfully.
- [x] Independent user approval supplied after ChatGPT analysis; protocol freeze authorized.
- [x] Archive-availability assumption and unresolved timestamp timezone documented.
- [ ] Phase 2B execution captures runtime software/BLAS provenance and validates all asserted populations.

Status: FROZEN as Evaluation Protocol v1.0. Model implementation and final evaluation remain pending.
