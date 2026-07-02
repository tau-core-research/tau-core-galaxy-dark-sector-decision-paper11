#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"


FIELDNAMES = [
    "fallback_policy_id",
    "policy_class",
    "fallback_scope",
    "allowed_policy",
    "blocked_policy",
    "shape_readout_guard",
    "counting_rule",
    "forbidden_inputs",
    "policy_status",
    "fallback_prediction_rows_written",
    "numeric_predictions_written",
    "endpoint_scoring_allowed",
    "claim_boundary",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def scale_policy_ready() -> bool:
    path = DERIVED / "m0_no_dark_scale_policy_summary_v07.csv"
    if not path.exists():
        return False
    rows = read_csv(path)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_SCALE_POLICY_READY"
        and rows[0]["numeric_scale_values_written"] == "0"
        and rows[0]["prediction_rows_written"] == "0"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def policy_rows() -> list[dict[str, object]]:
    common_forbidden = (
        "endpoint_residual;heldout_score;family_winner;best_fit_curve;"
        "posthoc_exception;posthoc_label_switch;posthoc_null_rescue"
    )
    rows = [
        {
            "fallback_policy_id": "M0NDFP07_ZERO_RESPONSE_ROUTE",
            "policy_class": "zero_response_policy",
            "fallback_scope": "inactive_or_zero_source_readout",
            "allowed_policy": "inactive source/readout routes may hand forward as declared zero-response states before scoring",
            "blocked_policy": "turning a zero-response route into a hidden fitted correction after seeing residuals",
            "shape_readout_guard": "zero-response must remain distinguishable from a successful shape/readout prediction",
            "counting_rule": "zero-response fallback writes no numeric prediction in this policy artifact",
        },
        {
            "fallback_policy_id": "M0NDFP07_MISSING_LABEL_ROUTE",
            "policy_class": "missing_label_policy",
            "fallback_scope": "missing_or_unpromoted_source_labels",
            "allowed_policy": "missing or unpromoted labels route to blocked or null states until independently promoted",
            "blocked_policy": "selecting a substitute morphology/readout label from endpoint residual shape",
            "shape_readout_guard": "missing-label fallback cannot be used as a post-hoc label switch",
            "counting_rule": "any later substitute label must pass the source-side promotion and counting path",
        },
        {
            "fallback_policy_id": "M0NDFP07_INADMISSIBLE_INPUT_ROUTE",
            "policy_class": "inadmissible_input_policy",
            "fallback_scope": "invalid_units_out_of_domain_or_unbound_symbols",
            "allowed_policy": "inadmissible inputs route to declared blocked states and do not emit prediction rows",
            "blocked_policy": "repairing invalid inputs with endpoint-specific unit, scale, or coefficient exceptions",
            "shape_readout_guard": "input inadmissibility remains a gate failure, not a weak prediction",
            "counting_rule": "repair privileges must be declared as new counted policy rows before scoring",
        },
        {
            "fallback_policy_id": "M0NDFP07_NULL_GAUGE_ROUTE",
            "policy_class": "null_gauge_policy",
            "fallback_scope": "null_gauge_or_readout_degenerate_cases",
            "allowed_policy": "null/gauge-degenerate cases may be marked non-identifiable before prediction rows",
            "blocked_policy": "choosing among degenerate readouts by held-out score or family winner",
            "shape_readout_guard": "degeneracy must be reported as non-identifiability, not hidden as a fitted success",
            "counting_rule": "degeneracy-breaking choices count as explicit model privileges",
        },
        {
            "fallback_policy_id": "M0NDFP07_FAILURE_REPORTING_ROUTE",
            "policy_class": "failure_reporting_policy",
            "fallback_scope": "formula_body_scale_or_source_rule_failure",
            "allowed_policy": "failure modes must be reported in machine-readable status columns before scoring",
            "blocked_policy": "silently dropping hard rows, hard radii, or failed galaxies from family comparison",
            "shape_readout_guard": "row sensitivity remains auditable and cannot be erased by exception handling",
            "counting_rule": "dropped or exception-handled rows require explicit exclusion accounting",
        },
        {
            "fallback_policy_id": "M0NDFP07_PREDICTION_TABLE_HANDOFF",
            "policy_class": "prediction_table_handoff_policy",
            "fallback_scope": "handoff_to_family_prediction_table_contract",
            "allowed_policy": "fallback semantics may hand off to the prediction-table contract as readiness metadata only",
            "blocked_policy": "writing fallback velocity predictions or endpoint scores from this policy artifact",
            "shape_readout_guard": "fallback handoff does not convert policy readiness into empirical support",
            "counting_rule": "numeric fallback predictions require a later executable formula/prediction artifact",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["policy_status"] = "READY" if scale_policy_ready() else "BLOCKED_UPSTREAM_SCALE_POLICY"
        row["fallback_prediction_rows_written"] = 0
        row["numeric_predictions_written"] = 0
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_fallback_policy_only_no_predictions_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["policy_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_FALLBACK_POLICY_V07",
            "source_artifact": "m0_no_dark_scale_policy_v07",
            "policy_rows": len(rows),
            "ready_policy_rows": ready,
            "blocked_policy_rows": blocked,
            "fallback_prediction_rows_written": 0,
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_FALLBACK_POLICY_READY"
            if blocked == 0
            else "M0_NO_DARK_FALLBACK_POLICY_BLOCKED",
            "next_required_artifact": "family_prediction_tables_v08.csv"
            if blocked == 0
            else "m0_no_dark_scale_policy_v07",
            "claim_boundary": "m0_no_dark_fallback_policy_only_no_predictions_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_fallback_policy_v07.md").write_text(
        """# M0 No-Dark Fallback Policy v07

**Doc class:** no-dark M0 formula-table fallback policy
**Status:** fallback policy ready; no fallback prediction rows; no numeric predictions; no scoring

Script:

```text
scripts/build_m0_no_dark_fallback_policy.py
```

Derived outputs:

```text
data/derived/m0_no_dark_fallback_policy_v07.csv
data/derived/m0_no_dark_fallback_policy_summary_v07.csv
```

This artifact fills the fallback-policy slot of the M0 no-dark formula table.
It imports the fixed-scale discipline from `m0_no_dark_scale_policy_v07` and
projects it to zero-response, missing-label, inadmissible-input, null/gauge,
failure-reporting, and prediction-table handoff routes.

## Current Result

The expected status is:

```text
M0_NO_DARK_FALLBACK_POLICY_READY
```

The policy is scoring-safe:

```text
fallback route != fitted rescue
failure state != dropped hard row
null/gauge route != empirical success
```

It forbids hidden exception terms, post-hoc label switches, residual-specific
null rescues, and silent row/radius drops. Fallback states may only be carried
forward as explicit readiness metadata until a later executable prediction
artifact authorizes numeric prediction rows.

The next formula-table handoff is:

```text
family_prediction_tables_v08.csv
```

## Claim Boundary

This policy does not write fallback velocity predictions, compute velocities,
compare M0/M1/M2, activate endpoint scoring, or decide the dark-sector
question. It only closes the fallback-policy slot of the M0 no-dark formula
table.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = policy_rows()
    write_csv(DERIVED / "m0_no_dark_fallback_policy_v07.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_fallback_policy_summary_v07.csv",
        summary(rows),
        [
            "summary_id",
            "source_artifact",
            "policy_rows",
            "ready_policy_rows",
            "blocked_policy_rows",
            "fallback_prediction_rows_written",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_FALLBACK_POLICY_V07_BUILT")


if __name__ == "__main__":
    main()
