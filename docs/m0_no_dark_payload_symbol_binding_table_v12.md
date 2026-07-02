# M0 No-Dark Payload Symbol Binding Table v12

**Doc class:** no-dark M0 payload symbol-binding contract
**Status:** symbol bindings ready; constant policy blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_symbol_binding_table.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_symbol_binding_table_v12.csv
data/derived/m0_no_dark_payload_symbol_binding_table_summary_v12.csv
```

This artifact binds payload symbol classes to approved source-side inputs,
operator metadata, guards, and assembly metadata before any formula body is
written.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_SYMBOL_BINDING_TABLE_READY_FOR_CONSTANT_POLICY
```

The next missing artifact is:

```text
m0_no_dark_payload_constant_policy_v12
```

## Claim Boundary

This symbol-binding table does not define a velocity formula, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only fixes which approved source-side
objects later payload symbols may refer to.
