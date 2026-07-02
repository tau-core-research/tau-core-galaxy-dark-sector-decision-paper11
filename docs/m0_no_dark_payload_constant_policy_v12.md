# M0 No-Dark Payload Constant Policy v12

**Doc class:** no-dark M0 payload constant-policy contract
**Status:** constant policy ready; dimensional trace blocked; no values; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_payload_constant_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_payload_constant_policy_v12.csv
data/derived/m0_no_dark_payload_constant_policy_summary_v12.csv
```

This artifact declares the allowed constant, scale, branch, switch, and free
parameter policy classes before any formula body is written.

## Current Result

The expected status is:

```text
M0_NO_DARK_PAYLOAD_CONSTANT_POLICY_READY_FOR_DIMENSIONAL_TRACE
```

The next missing artifact is:

```text
m0_no_dark_payload_dimensional_trace_v12
```

## Claim Boundary

This constant-policy artifact does not assign numerical values, does not define
a velocity formula, does not compute predictions, does not score galaxies, and
does not decide the dark-sector question. It only fixes which constant and
switch policy classes are admissible before dimensional tracing.
