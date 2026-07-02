#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SYMBOLIC_FORM_SUMMARY = DERIVED / "m0_no_dark_expression_symbolic_form_summary_v12.csv"


FIELDNAMES = [
    "input_domain_id",
    "symbolic_component_id",
    "domain_class",
    "allowed_domain",
    "required_binding",
    "blocked_domain",
    "allowed_handoff",
    "forbidden_inputs",
    "input_domain_status",
    "expression_claim_allowed",
    "formula_claim_allowed",
    "numeric_prediction_allowed",
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


def symbolic_form_ready() -> bool:
    if not SYMBOLIC_FORM_SUMMARY.exists():
        return False
    rows = read_csv(SYMBOLIC_FORM_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def input_domain_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_label_switch"
    rows = [
        {
            "input_domain_id": "M0NDID12_SOURCE_STATE_DOMAIN",
            "symbolic_component_id": "M0NDSF12_SOURCE_STATE_PLACEHOLDER",
            "domain_class": "source_state_domain",
            "allowed_domain": "typed morphology/readout source-state records with unresolved state allowed",
            "required_binding": "bind to source-side morphology/readout provenance before coefficient or formula work",
            "blocked_domain": "source-state value filled from endpoint residuals",
            "allowed_handoff": "coefficient_freeze_source_state_scope",
        },
        {
            "input_domain_id": "M0NDID12_NO_DARK_CONSTRAINT_DOMAIN",
            "symbolic_component_id": "M0NDSF12_NO_DARK_CONSTRAINT_PLACEHOLDER",
            "domain_class": "no_dark_constraint_domain",
            "allowed_domain": "dimensionless M0 no-dark eligibility marker",
            "required_binding": "preserve no-dark family constraint without adding fitted dark-response terms",
            "blocked_domain": "hidden dark-sector compensator or endpoint-tuned absence constraint",
            "allowed_handoff": "coefficient_freeze_family_constraint_scope",
        },
        {
            "input_domain_id": "M0NDID12_BARYONIC_INPUT_DOMAIN",
            "symbolic_component_id": "M0NDSF12_BARYONIC_INPUT_PLACEHOLDER",
            "domain_class": "baryonic_input_domain",
            "allowed_domain": "typed baryonic/source input records with units unresolved only as explicit null state",
            "required_binding": "bind baryonic/source provenance and unit path before dimensional audit",
            "blocked_domain": "normalization or missing unit repaired from best-fit curves",
            "allowed_handoff": "coefficient_freeze_baryonic_input_scope",
        },
        {
            "input_domain_id": "M0NDID12_READOUT_OPERATOR_DOMAIN",
            "symbolic_component_id": "M0NDSF12_READOUT_OPERATOR_PLACEHOLDER",
            "domain_class": "readout_operator_domain",
            "allowed_domain": "typed readout operator signature without numeric coefficients",
            "required_binding": "bind readout signature before kernel or equation construction",
            "blocked_domain": "operator selected by heldout score or family winner",
            "allowed_handoff": "coefficient_freeze_readout_operator_scope",
        },
        {
            "input_domain_id": "M0NDID12_FAILURE_ROUTE_DOMAIN",
            "symbolic_component_id": "M0NDSF12_FAILURE_ROUTE_PLACEHOLDER",
            "domain_class": "failure_route_domain",
            "allowed_domain": "explicit blocked, null, gauge, missing-input, or unresolved route markers",
            "required_binding": "failure markers must dominate post-hoc exception creation",
            "blocked_domain": "silent exception path or endpoint-selected bypass",
            "allowed_handoff": "coefficient_freeze_failure_policy_scope",
        },
        {
            "input_domain_id": "M0NDID12_FORM_ASSEMBLY_DOMAIN",
            "symbolic_component_id": "M0NDSF12_FORM_ASSEMBLY_SHELL",
            "domain_class": "form_assembly_domain",
            "allowed_domain": "abstract composition-domain shell with no velocity output and no coefficient values",
            "required_binding": "expose all required domains before coefficient-count or machine-form work",
            "blocked_domain": "complete formula, callable prediction function, or endpoint-scored expression",
            "allowed_handoff": "coefficient_freeze_assembly_scope",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["input_domain_status"] = "READY"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_input_domain_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["input_domain_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_V12",
            "input_domain_artifact": "m0_no_dark_expression_input_domain_v12",
            "symbolic_form_status": "READY" if symbolic_form_ready() else "BLOCKED",
            "input_domain_rows": len(rows),
            "ready_input_domain_rows": ready,
            "blocked_input_domain_rows": blocked,
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY"
            if blocked == 0 and symbolic_form_ready()
            else "M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_coefficient_freeze_v12",
            "claim_boundary": "m0_no_dark_expression_input_domain_only_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_input_domain_v12.md").write_text(
        """# M0 No-Dark Expression Input Domain v12

**Doc class:** no-dark M0 expression input-domain binding record
**Status:** input-domain binding ready; coefficient freeze still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_input_domain.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_input_domain_v12.csv
data/derived/m0_no_dark_expression_input_domain_summary_v12.csv
```

This artifact binds the symbolic-form shell to allowed input domains. It records
the source-state, no-dark constraint, baryonic/source input, readout-operator,
failure-route, and form-assembly domains that later coefficient and dimensional
artifacts must respect.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_READY
```

Six input-domain rows are ready:

- source-state domain;
- no-dark constraint domain;
- baryonic/source input domain;
- readout-operator domain;
- failure-route domain;
- form-assembly domain.

The next missing artifact is:

```text
m0_no_dark_expression_coefficient_freeze_v12
```

## Claim Boundary

This input-domain binding does not define a complete expression, does not write
a formula, does not assign coefficients, does not compute predicted velocities,
does not score galaxies, and does not decide the dark-sector question. It only
authorizes the next construction artifact: coefficient-freeze policy.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = input_domain_rows()
    write_csv(DERIVED / "m0_no_dark_expression_input_domain_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_input_domain_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "input_domain_artifact",
            "symbolic_form_status",
            "input_domain_rows",
            "ready_input_domain_rows",
            "blocked_input_domain_rows",
            "expression_claim_allowed",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_EXPRESSION_INPUT_DOMAIN_V12_BUILT")


if __name__ == "__main__":
    main()
