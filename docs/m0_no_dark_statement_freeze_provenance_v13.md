# M0 No-Dark Statement Freeze Provenance v13

**Doc class:** no-dark M0 statement freeze-provenance contract
**Status:** statement freeze provenance ready; payload blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_freeze_provenance.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_freeze_provenance_v13.csv
data/derived/m0_no_dark_statement_freeze_provenance_summary_v13.csv
```

This artifact records that the M0 no-dark statement-side route is fixed before
payload construction and before endpoint scoring. It freezes route identity and
timing only; it does not freeze a formula body.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_FREEZE_PROVENANCE_READY_FOR_PAYLOAD
```

The next missing artifact is:

```text
m0_no_dark_frozen_expression_payload_v11
```

## Claim Boundary

This freeze-provenance artifact does not define a velocity formula, does not
assign coefficients, does not compute predictions, does not score galaxies, and
does not decide the dark-sector question. It only records that the statement
route was fixed before payload and scoring work.
