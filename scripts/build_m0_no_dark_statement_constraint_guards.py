#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"
ARGUMENT_SIGNATURE_SUMMARY = DERIVED / "m0_no_dark_statement_argument_signature_summary_v13.csv"
STATEMENT_CONTRACT_SUMMARY = DERIVED / "m0_no_dark_frozen_expression_statement_summary_v12.csv"


FIELDNAMES = [
    "guard_id",
    "guard_class",
    "guard_role",
    "allowed_policy",
    "blocked_policy",
    "completion_status",
    "next_required_artifact",
    "forbidden_inputs",
    "guard_claim_allowed",
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


def argument_signature_ready() -> bool:
    if not ARGUMENT_SIGNATURE_SUMMARY.exists() or not STATEMENT_CONTRACT_SUMMARY.exists():
        return False
    signature = read_csv(ARGUMENT_SIGNATURE_SUMMARY)
    contract = read_csv(STATEMENT_CONTRACT_SUMMARY)
    return (
        len(signature) == 1
        and signature[0]["overall_status"] == "M0_NO_DARK_STATEMENT_ARGUMENT_SIGNATURE_READY_FOR_CONSTRAINT_GUARDS"
        and signature[0]["endpoint_scoring_allowed_anywhere"] == "false"
        and len(contract) == 1
        and contract[0]["overall_status"]
        in {
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_CONSTRAINT_GUARDS_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_PRE_DIMENSIONAL_PROOF_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FREEZE_PROVENANCE_BLOCKED",
            "M0_NO_DARK_FROZEN_EXPRESSION_STATEMENT_CONTRACT_READY_FOR_PAYLOAD",
        }
        and contract[0]["endpoint_scoring_allowed_anywhere"] == "false"
    )


def guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "M0NDSCG13_DOMAIN_GUARD",
            "guard_class": "domain_guard",
            "guard_role": "restrict the statement to declared source, baryonic, radial, and readout domains",
            "allowed_policy": "declared input domains only; missing or out-of-domain inputs block later formula use",
            "blocked_policy": "extend domain after endpoint residuals or fit failures",
        },
        {
            "guard_id": "M0NDSCG13_NULL_GUARD",
            "guard_class": "null_guard",
            "guard_role": "make null and absent-source states explicit",
            "allowed_policy": "explicit null-state route before formula construction",
            "blocked_policy": "silent default value inserted after scoring behavior is known",
        },
        {
            "guard_id": "M0NDSCG13_GAUGE_GUARD",
            "guard_class": "gauge_guard",
            "guard_role": "separate gauge/readout label freedom from physical prediction claims",
            "allowed_policy": "gauge/readout markers remain non-predictive until dimensional proof and formula body",
            "blocked_policy": "treat gauge label choice as empirical fit evidence",
        },
        {
            "guard_id": "M0NDSCG13_NO_DARK_GUARD",
            "guard_class": "no_dark_guard",
            "guard_role": "enforce M0 no-dark family exclusion of dark-sector compensation terms",
            "allowed_policy": "no hidden dark response, compensation, or fitted sector term in M0",
            "blocked_policy": "absorb residuals through an undeclared dark-sector proxy",
        },
        {
            "guard_id": "M0NDSCG13_FALLBACK_GUARD",
            "guard_class": "fallback_guard",
            "guard_role": "declare missing-input and failure behavior before formula body",
            "allowed_policy": "explicit block/fallback route with no prediction row produced",
            "blocked_policy": "posthoc exception chosen from best-fit curve quality",
        },
        {
            "guard_id": "M0NDSCG13_LEAKAGE_FREEZE_GUARD",
            "guard_class": "leakage_freeze_guard",
            "guard_role": "prevent endpoint-selected guard additions or reordering",
            "allowed_policy": "guards must be fixed before endpoint residuals, heldout scores, or family winners",
            "blocked_policy": "guard added, removed, or reordered after scoring information appears",
        },
    ]
    for row in rows:
        row["completion_status"] = "READY"
        row["next_required_artifact"] = "m0_no_dark_statement_pre_dimensional_proof_v13"
        row["forbidden_inputs"] = "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_exception"
        row["guard_claim_allowed"] = "false"
        row["formula_claim_allowed"] = "false"
        row["numeric_prediction_allowed"] = "false"
        row["endpoint_scoring_allowed"] = "false"
        row["claim_boundary"] = "m0_no_dark_statement_constraint_guards_only_no_formula_no_scores"
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    ready = sum(row["completion_status"] == "READY" for row in rows)
    blocked = len(rows) - ready
    upstream_ready = argument_signature_ready()
    return [
        {
            "summary_id": "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_V13",
            "constraint_guards_artifact": "m0_no_dark_statement_constraint_guards_v13",
            "argument_signature_status": "READY" if upstream_ready else "BLOCKED",
            "guard_rows": len(rows),
            "ready_guard_rows": ready,
            "blocked_guard_rows": blocked,
            "constraint_guards_written": "true" if upstream_ready and blocked == 0 else "false",
            "formula_body_written": "false",
            "formula_claim_allowed": "false",
            "numeric_predictions_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF"
            if upstream_ready and blocked == 0
            else "M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_BLOCKED",
            "next_required_artifact": "m0_no_dark_statement_pre_dimensional_proof_v13",
            "claim_boundary": "m0_no_dark_statement_constraint_guards_only_no_formula_no_scores_no_dark_sector_verdict",
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_no_dark_statement_constraint_guards_v13.md").write_text(
        """# M0 No-Dark Statement Constraint Guards v13

**Doc class:** no-dark M0 statement constraint-guard contract
**Status:** constraint guards ready; pre-dimensional proof blocked; no formula; no scoring

Script:

```text
scripts/build_m0_no_dark_statement_constraint_guards.py
```

Derived outputs:

```text
data/derived/m0_no_dark_statement_constraint_guards_v13.csv
data/derived/m0_no_dark_statement_constraint_guards_summary_v13.csv
```

This artifact records the domain, null, gauge/readout, no-dark, fallback, and
leakage/freeze guards required before any formula body can be considered.

## Current Result

The expected status is:

```text
M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_READY_FOR_PRE_DIMENSIONAL_PROOF
```

The next missing artifact is:

```text
m0_no_dark_statement_pre_dimensional_proof_v13
```

## Claim Boundary

This guard artifact does not define a velocity formula, does not assign
coefficients, does not compute predictions, does not score galaxies, and does
not decide the dark-sector question. It only freezes admissible guard policy
before dimensional proof and formula-body work.
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = guard_rows()
    write_csv(DERIVED / "m0_no_dark_statement_constraint_guards_v13.csv", rows, FIELDNAMES)
    write_csv(
        DERIVED / "m0_no_dark_statement_constraint_guards_summary_v13.csv",
        summary(rows),
        [
            "summary_id",
            "constraint_guards_artifact",
            "argument_signature_status",
            "guard_rows",
            "ready_guard_rows",
            "blocked_guard_rows",
            "constraint_guards_written",
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
    print("PAPER11_M0_NO_DARK_STATEMENT_CONSTRAINT_GUARDS_V13_BUILT")


if __name__ == "__main__":
    main()
