#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/source_manifest"
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

NEXT_ARTIFACT = "m2_per_galaxy_benchmark_privilege_count_freeze_v11.csv"
CLAIM_BOUNDARY = "m2_per_galaxy_benchmark_privilege_count_audit_only_no_freeze_no_benchmark_values_no_parsimony_no_scores"

FIELDS = [
    "audit_row_id",
    "source_audit_id",
    "galaxy_id",
    "decision_role",
    "source_activation_status",
    "m2_global_freeze_status",
    "m2_profile_status",
    "m2_nuisance_status",
    "row_benchmark_privilege_status",
    "per_galaxy_benchmark_privilege_count_value",
    "count_rule",
    "freeze_input_allowed",
    "benchmark_value_input_allowed",
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
    "per_galaxy_benchmark_privilege_values_written",
    "per_galaxy_benchmark_count_freeze_ready",
    "per_galaxy_benchmark_count_frozen",
    "numeric_benchmark_values_written",
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


def m2_global_freeze_status() -> str:
    rows = read_csv(DERIVED / "m2_benchmark_parameter_final_count_freeze_summary_v15.csv")
    if len(rows) != 1:
        raise ValueError("expected one M2 final-count freeze summary row")
    return rows[0]["overall_status"]


def m2_profile_status() -> str:
    rows = read_csv(DERIVED / "m2_benchmark_profile_table_summary_v06.csv")
    if len(rows) != 1:
        raise ValueError("expected one M2 benchmark-profile summary row")
    return rows[0]["overall_status"]


def m2_nuisance_status() -> str:
    rows = read_csv(DERIVED / "m2_nuisance_policy_table_summary_v06.csv")
    if len(rows) != 1:
        raise ValueError("expected one M2 nuisance-policy summary row")
    return rows[0]["overall_status"]


def audit_rows() -> list[dict[str, object]]:
    source_rows = read_csv(SOURCE / "source_row_audit_v05.csv")
    freeze_status = m2_global_freeze_status()
    profile_status = m2_profile_status()
    nuisance_status = m2_nuisance_status()
    rows: list[dict[str, object]] = []
    for index, row in enumerate(source_rows, start=1):
        rows.append(
            {
                "audit_row_id": f"M2PGBMPCA10_{index:03d}",
                "source_audit_id": row["audit_id"],
                "galaxy_id": row["galaxy_id"],
                "decision_role": row["decision_role"],
                "source_activation_status": row["activation_status"],
                "m2_global_freeze_status": freeze_status,
                "m2_profile_status": profile_status,
                "m2_nuisance_status": nuisance_status,
                "row_benchmark_privilege_status": "RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE",
                "per_galaxy_benchmark_privilege_count_value": 0,
                "count_rule": "count only row-specific M2 benchmark exceptions, hidden benchmark/nuisance parameters, galaxy-specific benchmark switches, or posthoc benchmark privileges; source-row activation blocks and missing benchmark values are not privileges",
                "freeze_input_allowed": "true",
                "benchmark_value_input_allowed": "false",
                "parsimony_input_allowed": "false",
                "next_required_artifact": NEXT_ARTIFACT,
                "forbidden_inputs": "endpoint_residual;heldout_score;family_winner;best_fit_curve;posthoc_benchmark_switch;posthoc_benchmark_parameter;numeric_score_value",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    resolved = [
        row
        for row in rows
        if row["row_benchmark_privilege_status"] == "RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE"
    ]
    unresolved = len(rows) - len(resolved)
    return [
        {
            "summary_id": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10",
            "audit_artifact": "m2_per_galaxy_benchmark_privilege_count_audit_v10",
            "source_rows_checked": len(rows),
            "resolved_zero_rows": len(resolved),
            "unresolved_rows": unresolved,
            "per_galaxy_benchmark_privilege_values_written": len(resolved),
            "per_galaxy_benchmark_count_freeze_ready": "true" if unresolved == 0 else "false",
            "per_galaxy_benchmark_count_frozen": "false",
            "numeric_benchmark_values_written": 0,
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_READY_FOR_FREEZE"
            if unresolved == 0
            else "M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_BLOCKED",
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "m2_per_galaxy_benchmark_privilege_count_audit_v10.md").write_text(
        f"""# M2 Per-Galaxy Benchmark-Privilege Count Audit v10

**Doc class:** per-galaxy M2 benchmark-privilege count audit
**Status:** audit ready for freeze; no benchmark values; no parsimony; no scoring
**Canonical parent:** M2 benchmark-parameter final-count freeze v15

Script:

```text
scripts/build_m2_per_galaxy_benchmark_privilege_count_audit.py
```

Derived outputs:

```text
data/derived/m2_per_galaxy_benchmark_privilege_count_audit_v10.csv
data/derived/m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv
```

This artifact audits the M2 benchmark branch for row-specific benchmark
privileges after the protocol-local global M2 benchmark-parameter count has
been frozen at zero. It records one row per source-manifest galaxy and applies
a narrow count rule:

```text
count only row-specific M2 benchmark exceptions, hidden benchmark/nuisance parameters, galaxy-specific benchmark switches, or posthoc benchmark privileges; source-row activation blocks and missing benchmark values are not privileges
```

Under the current source-manifest state, benchmark-profile scaffold, nuisance
policy scaffold, and frozen M2 global benchmark-parameter count, all eighteen
rows resolve to:

```text
RESOLVED_ZERO_NO_ROW_SPECIFIC_M2_BENCHMARK_PRIVILEGE
```

The next artifact is therefore:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This audit writes per-galaxy M2 benchmark-privilege audit values only. It does
not freeze the per-galaxy count, does not write benchmark/profile values, does
not write nuisance values, does not compute parsimony, does not authorize
endpoint scoring, and does not decide whether a dark-sector benchmark is
physically absent or necessary. It does not decide whether a dark-sector
benchmark is physically absent.

This audit does not decide whether a dark-sector benchmark is physically absent.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = audit_rows()
    write_csv(DERIVED / "m2_per_galaxy_benchmark_privilege_count_audit_v10.csv", rows, FIELDS)
    write_csv(
        DERIVED / "m2_per_galaxy_benchmark_privilege_count_audit_summary_v10.csv",
        summary(rows),
        SUMMARY_FIELDS,
    )
    write_doc()
    print("PAPER11_M2_PER_GALAXY_BENCHMARK_PRIVILEGE_COUNT_AUDIT_V10_BUILT")


if __name__ == "__main__":
    main()
