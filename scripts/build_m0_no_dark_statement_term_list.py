#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
STATEMENT_SUMMARY = DERIVED / "m0_no_dark_source_side_expression_statement_summary_v13.csv"
STATEMENT_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"


FIELDNAMES = [
    "term_entry_id",
    "term_class",
    "allowed_role",
    "allowed_content",
    "blocked_content",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "term_claim_allowed",
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


def source_side_statement_ready() -> bool:
    if not STATEMENT_SUMMARY.exists() or not STATEMENT_CONTRACT_SUMMARY.exists():
        return False
    statement = read_csv(STATEMENT_SUMMARY)
    contract = read_csv(STATEMENT_CONTRACT_SUMMARY)
    return (
        len(statement) == 1
        and statement[0]["overall_status"] == "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST"
        and statement[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(contract) == 1
        and contract[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_TERM_LIST_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_ARGUMENT_SIGNATURE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_CONSTRAINT_GUARDS_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FREEZE_PROVENANCE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        }
        and contract[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def term_rows() -> list[dict[str, object]]:
    rows = [
        {
            "term_entry_id": "M0NDSTL13_SOURCE_STATE_TERM",
            "term_class": "source_state_term",
            "allowed_role": "source-side morphology/readout state placeholder",
            "allowed_content": "typed source-state term class inherited from approved source-basis records",
            "blocked_content": "term fitted from endpoint residuals",
        },
        {
            "term_entry_id": "M0NDSTL13_BARYONIC_INPUT_TERM",
            "term_class": "baryonic_input_term",
            "allowed_role": "baryonic/source input carrier",
            "allowed_content": "typed baryonic input term class with later argument binding required",
            "blocked_content": "posthoc normalization inferred from best-fit curves",
        },
        {
            "term_entry_id": "M0NDSTL13_READOUT_OPERATOR_TERM",
            "term_class": "readout_operator_term",
            "allowed_role": "source-to-observable readout operation shell",
            "allowed_content": "operator term class selected by pre-score admissibility only",
            "blocked_content": "operator selected by heldout score or family winner",
        },
        {
            "term_entry_id": "M0NDSTL13_NO_DARK_CONSTRAINT_TERM",
            "term_class": "no_dark_constraint_term",
            "allowed_role": "M0 no-dark eligibility and exclusion guard",
            "allowed_content": "constraint marker preventing dark-sector compensation terms in M0",
            "blocked_content": "hidden fitted dark-response or compensation term",
        },
        {
            "term_entry_id": "M0NDSTL13_NULL_FALLBACK_TERM",
            "term_class": "null_fallback_term",
            "allowed_role": "null, gauge, missing-input, and failure-route guard",
            "allowed_content": "explicit fallback/null route term class with no silent exception",
            "blocked_content": "posthoc exception added after poor endpoint residuals",
        },
        {
            "term_entry_id": "M0NDSTL13_ASSEMBLY_OPERATOR_TERM",
            "term_class": "assembly_operator_term",
            "allowed_role": "non-numeric composition shell for later formula body construction",
            "allowed_content": "composition/operator class only; no algebraic expression or coefficients",
            "blocked_content": "complete velocity formula, coefficient value, or executable scoring callable",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_statement_argument_signature_v13"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_term_addition"
        row["term_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_statement_term_list_only_term_classes_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = source_side_statement_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_TERM_LIST_V13",
            "term_list_artifact": "m0_no_dark_statement_term_list_v13",
            "source_side_statement_status": "READY" if upstream_ready else "BLOCKED",
            "term_entries": len(rows),
            "ready_term_entries": ready,
            "blocked_term_entries": blocked,
            "term_list_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_STATEMENT_TERM_LIST_BLOCKED",
            "next_required_artifact": "m0_no_dark_statement_argument_signature_v13",
            "claim_boundary": "m0_no_dark_statement_term_list_only_term_classes_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_statement_term_list_v13.md").write_text(
        """# M0 No-Dark Statement Term List v13

**Doc class:** no-dark M0 statement term-list contract
**Status:** term classes ready; argument signature blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_term_list.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_term_list_v13.csv
data/derived/m0_no_dark_statement_term_list_summary_v13.csv
```

This artifact records the allowed term classes for the M0 no-dark source-side
statement path. It does not assemble these terms into a mathematical
expression. It does not bind concrete arguments, choose coefficients, compute
predictions, or score endpoint residuals.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_TERM_LIST_READY_FOR_ARGUMENT_SIGNATURE
```

The next missing artifact is:

```text
m0_no_dark_statement_argument_signature_v13
```

## Claim Boundary

This term-list artifact allows only term classes: source-state, baryonic input,
readout-operator, no-dark constraint, null/fallback, and assembly-operator
slots. It does not define a velocity formula and does not decide the
dark-sector question.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = term_rows()
    write_csv(DERIVED / "m0_no_dark_statement_term_list_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_statement_term_list_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "term_list_artifact",
            "source_side_statement_status",
            "term_entries",
            "ready_term_entries",
            "blocked_term_entries",
            "term_list_written",
            "formula_body_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_STATEMENT_TERM_LIST_V13_BUILT")


if __name__ == "__main__":
    main()
