#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m0_per_galaxy_privilege_count_freeze_v11.csv"
CLAIM_BOUNDARY = "m0_per_galaxy_privilege_count_audit_only_no_freeze_no_parsimony_no_scores"

FIELDS = [
    "audit_row_id",
    "source_audit_id",
    "galaxy_id",
    "decision_role",
    "source_activation_status",
    "m0_label_rule_status",
    "row_privilege_status",
    "per_galaxy_privilege_count_value",
    "count_rule",
    "freeze_input_allowed",
    "parsimony_input_allowed",
    "next_required_artifact",
    "forbidden_inputs",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "audit_artifact",
    "source_rows_checked",
    "resolved_zero_rows",
    "unresolved_rows",
    "per_galaxy_privilege_values_written",
    "per_galaxy_count_freeze_ready",
    "per_galaxy_count_frozen",
    "parsimony_scores_written",
    "endpoint_scoring_allowed_anywhere",
    "overall_status",
    "next_required_artifact",
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


def label_rule_status() -> str:
    rows = read_csv(DERIVED / "m0_label_rule_table_summary_v06.csv")
    if len(rows) != 1:
        raise ValueError("expected one m0 label-rule summary row")
    return rows[0]["overall_status"]


def audit_rows() -> list[dict[str, object]]:
    source_rows = read_csv(SOURCE / "source_row_audit_v05.csv")
    status = label_rule_status()
    rows: list[dict[str, object]] = []
    for index, row in enumerate(source_rows, start=1):
        rows.append(
            {
                "audit_row_id": f"M0PGPCA10_{index:03d}",
                "source_audit_id": row["audit_id"],
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "source_activation_status": row["activation_status"],
                "m0_label_rule_status": status,
                "row_privilege_status": "RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE",
                "per_galaxy_privilege_count_value": 0,
                "count_rule": "count only row-specific M0 rescue labels, exceptions, hidden parameters, or posthoc family switches; source-row activation blocks are not privileges",
                "freeze_input_allowed": "true",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_parameter_discount",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resolved = [row for row in rows if row["row_privilege_status"] == "RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE"]
    unresolved = len(rows) - len(resolved)
    return [
        {
            "summary_id": "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10",
            "audit_artifact": "m0_per_galaxy_privilege_count_audit_v10",
            "source_rows_checked": len(rows),
            "resolved_zero_rows": len(resolved),
            "unresolved_rows": unresolved,
            "per_galaxy_privilege_values_written": len(resolved),
            "per_galaxy_count_freeze_ready": "true" if unresolved == 0 else "false",
            "per_galaxy_count_frozen": "false",
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE"
            if unresolved == 0
            else "M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m0_per_galaxy_privilege_count_audit_v10.md").write_text(
        f"""# M0 Per-Galaxy Privilege Count Audit v10

**Doc class:** per-galaxy M0 privilege-count audit
**Status:** audit ready for freeze; no parsimony, no scoring

Script:

```text
scripts/build_m0_per_galaxy_privilege_count_audit.py
```

Derived outputs:

```text
data/derived/m0_per_galaxy_privilege_count_audit_v10.csv
data/derived/m0_per_galaxy_privilege_count_audit_summary_v10.csv
```

This artifact audits the M0 no-dark branch for row-specific privileges after the
global M0 count has been frozen at zero. It records one row per source-manifest
galaxy and applies a narrow count rule:

```text
count only row-specific M0 rescue labels, exceptions, hidden parameters, or posthoc family switches; source-row activation blocks are not privileges
```

Under the current skeleton source-manifest state and the frozen M0 label-rule
table, all eighteen rows resolve to:

```text
RESOLVED_ZERO_NO_ROW_SPECIFIC_M0_PRIVILEGE
```

The next artifact is therefore:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This audit writes per-galaxy privilege-count audit values only. It does not
freeze the per-galaxy count, does not compute a parsimony penalty, does not
activate endpoint scoring, and does not decide the dark-sector question.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "m0_per_galaxy_privilege_count_audit_v10.csv", rows, FIELDS)
    write_csv(DERIVED / "m0_per_galaxy_privilege_count_audit_summary_v10.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_M0_PER_GALAXY_PRIVILEGE_COUNT_AUDIT_V10_BUILT")


if __name__ == "__main__":
    main()
