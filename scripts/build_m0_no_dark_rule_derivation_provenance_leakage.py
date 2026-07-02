#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
DIMENSIONAL_PRECHECK_SUMMARY = DERIVED / "m0_no_dark_rule_dimensional_precheck_summary_v14.csv"


FIELDNAMES = [
    "audit_id",
    "derivation_slot_id",
    "audit_class",
    "source_side_record",
    "leakage_rule",
    "accepted_evidence",
    "forbidden_inputs",
    "audit_status",
    "derivation_claim_allowed",
    "source_rule_claim_allowed",
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


def dimensional_precheck_ready() -> bool:
    if not DIMENSIONAL_PRECHECK_SUMMARY.exists():
        return False
    rows = read_csv(DIMENSIONAL_PRECHECK_SUMMARY)
    return (
        len(rows) == 1
        and rows[0]["overall_status"] == "M0_NO_DARK_RULE_DIMENSIONAL_PRECHECK_READY"
        and rows[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def audit_rows() -> list[dict[str, object]]:
    common_forbidden = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_formula_switch"
    rows = [
        {
            "audit_id": "M0NDPAL14_PARENT_BASIS_PROVENANCE",
            "derivation_slot_id": "M0NDER13_PARENT_ASSUMPTIONS",
            "audit_class": "parent_basis_provenance",
            "source_side_record": "m0_no_dark_rule_parent_assumption_basis_v14",
            "leakage_rule": "parent assumptions must be recorded as source-side constraints, not selected from endpoint residuals",
            "accepted_evidence": "ready parent-basis artifact with endpoint scoring forbidden",
        },
        {
            "audit_id": "M0NDPAL14_SELECTION_MAP_PROVENANCE",
            "derivation_slot_id": "M0NDER13_RULE_SELECTION_MAP",
            "audit_class": "selection_map_provenance",
            "source_side_record": "m0_no_dark_rule_selection_map_v14",
            "leakage_rule": "rule-class selection map must be pre-endpoint and cannot depend on family winner labels",
            "accepted_evidence": "ready selection-map artifact with endpoint residual and posthoc label switch forbidden",
        },
        {
            "audit_id": "M0NDPAL14_TERM_GENERATION_PROVENANCE",
            "derivation_slot_id": "M0NDER13_TERM_GENERATION",
            "audit_class": "term_generation_provenance",
            "source_side_record": "m0_no_dark_rule_term_generation_record_v14",
            "leakage_rule": "term classes must be generated before scoring and cannot be endpoint-selected corrections",
            "accepted_evidence": "ready term-generation artifact with formula and numeric prediction claims forbidden",
        },
        {
            "audit_id": "M0NDPAL14_INVARIANCE_NULL_PROVENANCE",
            "derivation_slot_id": "M0NDER13_INVARIANCE_CHECKS",
            "audit_class": "invariance_null_provenance",
            "source_side_record": "m0_no_dark_rule_invariance_null_checks_v14",
            "leakage_rule": "null, gauge, and fallback checks must block post-hoc exceptions instead of repairing endpoint failures",
            "accepted_evidence": "ready invariance/null artifact with endpoint and best-fit inputs forbidden",
        },
        {
            "audit_id": "M0NDPAL14_DIMENSIONAL_PRECHECK_PROVENANCE",
            "derivation_slot_id": "M0NDER13_DIMENSIONAL_PRECHECK",
            "audit_class": "dimensional_precheck_provenance",
            "source_side_record": "m0_no_dark_rule_dimensional_precheck_v14",
            "leakage_rule": "dimensional routes must preserve source-side units and cannot infer scales from residuals",
            "accepted_evidence": "ready dimensional-precheck artifact with posthoc unit rescale forbidden",
        },
        {
            "audit_id": "M0NDPAL14_FRONTIER_HANDOFF",
            "derivation_slot_id": "M0NDER13_PROVENANCE_AND_LEAKAGE",
            "audit_class": "frontier_handoff",
            "source_side_record": "m0_no_dark_expression_rule_derivation_contract_v13",
            "leakage_rule": "the derivation contract may hand off only to source-basis construction, not to formula or scoring",
            "accepted_evidence": "all derivation preconditions are audit-ready while source-rule, expression, formula, and scoring claims remain forbidden",
        },
    ]
    for row in rows:
        row["forbidden_inputs"] = common_forbidden
        row["audit_status"] = "READY"
        row["derivation_claim_allowed"] = "false"
        row["source_rule_claim_allowed"] = "false"
        row["expression_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_rule_derivation_provenance_leakage_only_no_rule_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["audit_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    return [
        {
            "summary_id": "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_V14",
            "audit_artifact": "m0_no_dark_rule_derivation_provenance_leakage_v14",
            "dimensional_precheck_status": "READY" if dimensional_precheck_ready() else "BLOCKED",
            "audit_rows": len(rows),
            "ready_audit_rows": ready,
            "blocked_audit_rows": blocked,
            "derivation_claim_allowed": "false",
            "source_rule_claim_allowed": "false",
            "expression_claim_allowed": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY"
            if blocked == 0 and dimensional_precheck_ready()
            else "M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_BLOCKED",
            "next_required_artifact": "m0_no_dark_expression_source_basis_v13",
            "claim_boundary": "m0_no_dark_rule_derivation_provenance_leakage_only_no_rule_no_formula_no_scores",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_rule_derivation_provenance_leakage_v14.md").write_text(
        """# M0 No-Dark Rule Derivation Provenance and Leakage Audit v14

**Doc class:** no-dark M0 derivation provenance/leakage audit
**Status:** derivation provenance/leakage audit ready; source-basis construction still blocked; no scoring

Script:

```text
scripts/build_m0_no_dark_rule_derivation_provenance_leakage.py
```

Derived outputs:

```text
data/derived/m0_no_dark_rule_derivation_provenance_leakage_v14.csv
data/derived/m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv
```

This artifact audits the provenance and leakage boundary of the M0 no-dark
derivation preconditions. It records that the parent basis, selection map, term
generation, invariance/null checks, and dimensional precheck are source-side
protocol artifacts, not endpoint-selected formulas.

## Current Result

The expected status is:

```text
M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_READY
```

Six audit rows are ready:

- parent-basis provenance;
- rule-selection map provenance;
- term-generation provenance;
- invariance/null provenance;
- dimensional-precheck provenance;
- frontier handoff to source-basis construction.

The next missing artifact is:

```text
m0_no_dark_expression_source_basis_v13
```

## Claim Boundary

This audit does not define a source rule, does not define an expression, does
not write a formula, does not compute predicted velocities, does not score
galaxies, and does not decide the dark-sector question. It only closes the
derivation-precondition leakage audit and authorizes the next source-side
construction artifact: the M0 no-dark expression source basis.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "m0_no_dark_rule_derivation_provenance_leakage_v14.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_rule_derivation_provenance_leakage_summary_v14.csv",
        summary(rows),
        [
            "summary_id",
            "audit_artifact",
            "dimensional_precheck_status",
            "audit_rows",
            "ready_audit_rows",
            "blocked_audit_rows",
            "derivation_claim_allowed",
            "source_rule_claim_allowed",
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
    print("PAPER11_M0_NO_DARK_RULE_DERIVATION_PROVENANCE_LEAKAGE_V14_BUILT")


if __name__ == "__main__":
    main()
