# M0 No-Dark Payload Leakage Certificate v12

**Doc class:** no-dark M0 payload leakage certificate
**Status:** payload leakage certificate ready; formula tables still blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_leakage_certificate.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_leakage_certificate_v12.csv
data/derived/m0_no_dark_payload_leakage_certificate_summary_v12.csv
```

This artifact certifies that the machine-readable M0 no-dark payload remains
pre-endpoint. It records forbidden input manifests, freeze ordering,
serialization/hash policy, source-provenance guards, null/fallback stop
behavior, and the handoff to later formula-table contracts.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_LEAKAGE_CERTIFICATE_READY_FOR_FORMULA_TABLES
```

The next required artifact is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This leakage certificate does not assign numerical values, does not define a
velocity formula, does not expose a prediction callable, does not compute
predictions, does not score galaxies, and does not decide the dark-sector
question. It only certifies that the serialized payload boundary excludes
endpoint-derived information before later formula-table work.
