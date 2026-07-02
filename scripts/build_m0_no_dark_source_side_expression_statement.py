#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
STATEMENT_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"


FIELDNAMES = [
    "statement_component_id",
    "statement_component_class",
    "statement_role",
    "allowed_content",
    "blocked_content",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "statement_claim_allowed",
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


def statement_contract_ready() -> bool:
    if not STATEMENT_CONTRACT_SUMMARY.exists():
        return False
    rows = read_csv(STATEMENT_CONTRACT_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_STATEMENT_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_SOURCE_SIDE_EXPRESSION_STATEMENT_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_TERM_LIST_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_ARGUMENT_SIGNATURE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_CONSTRAINT_GUARDS_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FREEZE_PROVENANCE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        }
        and rows[0]["next_required_artifact"]
        in {
            "m0_no_dark_source_side_expression_statement_v13",
            "m0_no_dark_statement_term_list_v13",
            "m0_no_dark_statement_argument_signature_v13",
            "m0_no_dark_statement_constraint_guards_v13",
            "m0_no_dark_statement_pre_dimensional_proof_v13",
            "m0_no_dark_statement_freeze_provenance_v13",
            "m0_no_dark_frozen_expression_payload_v11",
        }
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def statement_rows() -> list[dict[str, object]]:
    rows = [
        {
            "statement_component_id": "M0NDSS13_STATEMENT_ENVELOPE",
            "statement_component_class": "statement_envelope",
            "statement_role": "pre-score source-side expression statement container",
            "allowed_content": "non-numeric statement envelope with no velocity formula body",
            "blocked_content": "complete fitted velocity expression",
        },
        {
            "statement_component_id": "M0NDSS13_SOURCE_SIDE_SCOPE",
            "statement_component_class": "source_side_scope",
            "statement_role": "restrict statement inputs to approved source-side records",
            "allowed_content": "references to upstream source-basis, admissibility, null/fallback, output-class, and leakage-audit records",
            "blocked_content": "endpoint residuals, heldout scores, family winners, or best-fit curves",
        },
        {
            "statement_component_id": "M0NDSS13_NO_DARK_FAMILY_BINDING",
            "statement_component_class": "no_dark_family_binding",
            "statement_role": "bind the statement to the M0 no-dark family only",
            "allowed_content": "M0 no-dark family identity and no-dark constraint flag",
            "blocked_content": "dark-sector compensation term or hidden fitted sector response",
        },
        {
            "statement_component_id": "M0NDSS13_OUTPUT_INTENT",
            "statement_component_class": "output_intent",
            "statement_role": "declare later handoff toward a velocity-readout output class",
            "allowed_content": "output intent only; no numeric velocity rows",
            "blocked_content": "v_pred_km_s values or endpoint-scored callable",
        },
        {
            "statement_component_id": "M0NDSS13_FREEZE_GUARD",
            "statement_component_class": "freeze_guard",
            "statement_role": "guard that term lists and argument signatures must be frozen before scoring",
            "allowed_content": "freeze-precondition record",
            "blocked_content": "posthoc term additions or coefficient changes after scoring",
        },
        {
            "statement_component_id": "M0NDSS13_NEXT_SLOT_HANDOFF",
            "statement_component_class": "next_slot_handoff",
            "statement_role": "handoff to the concrete term-list artifact",
            "allowed_content": "explicit next-required artifact pointer",
            "blocked_content": "direct jump to predictions, scoring, or dark-sector verdict",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_statement_term_list_v13"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_expression_switch"
        row["statement_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_source_side_expression_statement_envelope_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = statement_contract_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_V13",
            "statement_artifact": "m0_no_dark_source_side_expression_statement_v13",
            "frozen_expression_statement_contract_status": "READY" if upstream_ready else "BLOCKED",
            "statement_components": len(rows),
            "ready_statement_components": ready,
            "blocked_statement_components": blocked,
            "source_side_statement_record_written": "true" if upstream_ready and blocked == 0 else "false",
            "statement_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_BLOCKED",
            "next_required_artifact": "m0_no_dark_statement_term_list_v13",
            "claim_boundary": "m0_no_dark_source_side_expression_statement_envelope_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_source_side_expression_statement_v13.md").write_text(
        """# M0 No-Dark Source-Side Expression Statement v13

**Doc class:** no-dark M0 source-side expression statement envelope
**Status:** statement envelope ready; term list blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_source_side_expression_statement.py
```

Derived outputs:

```text
data/derived/m0_no_dark_source_side_expression_statement_v13.csv
data/derived/m0_no_dark_source_side_expression_statement_summary_v13.csv
```

This artifact writes the source-side statement envelope required by the v12
frozen-expression statement contract. It does not write the mathematical
expression body. It fixes the allowed pre-score role of the statement, its
source-side scope, M0 no-dark family binding, output intent, freeze guard, and
handoff to the concrete term-list artifact.

## Current Result

The expected status is:

```text
M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_READY_FOR_TERM_LIST
```

The next missing artifact is:

```text
m0_no_dark_statement_term_list_v13
```

## Claim Boundary

This source-side statement envelope does not define a velocity formula, does
not list admissible terms, does not bind arguments, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only authorizes the next formula-side
construction artifact: the frozen term list.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = statement_rows()
    write_csv(DERIVED / "m0_no_dark_source_side_expression_statement_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_source_side_expression_statement_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "statement_artifact",
            "frozen_expression_statement_contract_status",
            "statement_components",
            "ready_statement_components",
            "blocked_statement_components",
            "source_side_statement_record_written",
            "statement_body_written",
            "formula_claim_allowed",
            "numeric_predictions_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    write_doc()
    print("PAPER11_M0_NO_DARK_SOURCE_SIDE_EXPRESSION_STATEMENT_V13_BUILT")


if __name__ == "__main__":
    main()
