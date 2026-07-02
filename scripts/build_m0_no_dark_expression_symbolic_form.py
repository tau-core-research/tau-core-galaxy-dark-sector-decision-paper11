#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
SOURCE_RULE_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_expression_source_rule_contract_summary_v12.csv"


FIELDNAMES = [
    "symbolic_component_id",
    "source_rule_slot_id",
    "component_class",
    "allowed_symbolic_role",
    "allowed_form",
    "blocked_form",
    "allowed_handoff",
    "forbidden_inputs",
    "symbolic_component_status",
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


def source_rule_contract_ready() -> bool:
    if not SOURCE_RULE_CONTRACT_SUMMARY.exists():
        return False
    rows = read_csv(SOURCE_RULE_CONTRACT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_EXPRESSION_SOURCE_RULE_READY_FOR_SYMBOLIC_FORM"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def symbolic_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_formula_switch"
    rows = [
        {
            "symbolic_component_id": "M0NDSF12_SOURCE_STATE_PLACEHOLDER",
            "source_rule_slot_id": "M0NDESR12_RULE_DERIVATION",
            "component_class": "source_state_placeholder",
            "allowed_symbolic_role": "placeholder for source-side morphology/readout state",
            "allowed_form": "typed source-state symbol only",
            "blocked_form": "numeric source term fitted from endpoint residuals",
            "allowed_handoff": "input_domain_source_state_binding",
        },
        {
            "symbolic_component_id": "M0NDSF12_NO_DARK_CONSTRAINT_PLACEHOLDER",
            "source_rule_slot_id": "M0NDESR12_OUTPUT_CLASS",
            "component_class": "no_dark_constraint_placeholder",
            "allowed_symbolic_role": "placeholder enforcing M0 no-dark family eligibility",
            "allowed_form": "dimensionless eligibility marker",
            "blocked_form": "dark-response compensation or hidden fitted sector term",
            "allowed_handoff": "input_domain_family_constraint_binding",
        },
        {
            "symbolic_component_id": "M0NDSF12_BARYONIC_INPUT_PLACEHOLDER",
            "source_rule_slot_id": "M0NDESR12_NULL_AND_FALLBACK",
            "component_class": "baryonic_input_placeholder",
            "allowed_symbolic_role": "placeholder for baryonic/source input binding",
            "allowed_form": "typed baryonic input symbol with unresolved state allowed",
            "blocked_form": "post-hoc normalization inferred from best-fit curves",
            "allowed_handoff": "input_domain_baryonic_binding",
        },
        {
            "symbolic_component_id": "M0NDSF12_READOUT_OPERATOR_PLACEHOLDER",
            "source_rule_slot_id": "M0NDESR12_ADMISSIBILITY",
            "component_class": "readout_operator_placeholder",
            "allowed_symbolic_role": "placeholder for admissible readout operation from source state to observable family",
            "allowed_form": "typed readout operator shell without coefficient values",
            "blocked_form": "operator chosen by heldout score or family winner",
            "allowed_handoff": "input_domain_readout_signature",
        },
        {
            "symbolic_component_id": "M0NDSF12_FAILURE_ROUTE_PLACEHOLDER",
            "source_rule_slot_id": "M0NDESR12_LEAKAGE_AUDIT",
            "component_class": "failure_route_placeholder",
            "allowed_symbolic_role": "placeholder for blocked, null, gauge, or unresolved routes",
            "allowed_form": "explicit blocked-route symbol",
            "blocked_form": "silent exception that bypasses missing symbolic requirements",
            "allowed_handoff": "input_domain_failure_policy",
        },
        {
            "symbolic_component_id": "M0NDSF12_FORM_ASSEMBLY_SHELL",
            "source_rule_slot_id": "M0NDESR12_SOURCE_BASIS",
            "component_class": "form_assembly_shell",
            "allowed_symbolic_role": "non-numeric assembly shell for later input-domain and dimensional audits",
            "allowed_form": "abstract composition shell with no coefficient values and no velocity output",
            "blocked_form": "complete velocity formula or endpoint-scored callable",
            "allowed_handoff": "input_domain_contract",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["symbolic_component_status"] = "READY"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_expression_symbolic_form_only_shell_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["symbolic_component_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_V12",
            "symbolic_form_artifact": "m0_no_dark_expression_symbolic_form_v12",
            "source_rule_contract_status": "READY" if source_rule_contract_ready() else "BLOCKED",
            "symbolic_components": len(rows),
            "ready_symbolic_components": ready,
            "blocked_symbolic_components": blocked,
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_READY"
            if blocked == 0 and source_rule_contract_ready()
            else "M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_input_domain_v12",
            "claim_boundary": "m0_no_dark_expression_symbolic_form_only_shell_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_expression_symbolic_form_v12.md").write_text(
        """# M0 No-Dark Expression Symbolic Form v12

**Doc class:** no-dark M0 expression symbolic-form shell
**Status:** symbolic form shell ready; input-domain binding still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_expression_symbolic_form.py
```

Derived outputs:

```text
data/derived/m0_no_dark_expression_symbolic_form_v12.csv
data/derived/m0_no_dark_expression_symbolic_form_summary_v12.csv
```

This artifact declares the allowed symbolic/algorithmic shell for the M0
no-dark expression path. It is intentionally not a velocity formula. It names
the source-state placeholder, no-dark constraint placeholder, baryonic input
placeholder, readout operator placeholder, failure-route placeholder, and
non-numeric assembly shell that later artifacts must bind, audit, and freeze.

## Current Result

The expected status is:

```text
M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_READY
```

Six symbolic shell components are ready:

- source-state placeholder;
- no-dark constraint placeholder;
- baryonic/source input placeholder;
- readout operator placeholder;
- failure-route placeholder;
- form-assembly shell.

The next missing artifact is:

```text
m0_no_dark_expression_input_domain_v12
```

## Claim Boundary

This symbolic-form shell does not define a complete expression, does not write
a formula, does not assign coefficients, does not compute predicted velocities,
does not score galaxies, and does not decide the dark-sector question. It only
authorizes the next construction artifact: input-domain binding.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = symbolic_rows()
    write_csv(DERIVED / "m0_no_dark_expression_symbolic_form_v12.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_expression_symbolic_form_summary_v12.csv",
        summary(rows),
        [
            "summary_id",
            "symbolic_form_artifact",
            "source_rule_contract_status",
            "symbolic_components",
            "ready_symbolic_components",
            "blocked_symbolic_components",
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
    print("PAPER11_M0_NO_DARK_EXPRESSION_SYMBOLIC_FORM_V12_BUILT")


if __name__ == "__main__":
    main()
