#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
DOCS = ROOT / "docs"

STATUS = "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10_READY_FOR_GLOBAL_SCORING_PREREQUISITES"
NEXT_ARTIFACT = "control_runner_outputs_v08.csv"
CLAIM_BOUNDARY = "numeric_parameter_count_table_final_values_only_no_parsimony_no_scores_no_verdict"

FIELDS = [
    "final_count_row_id",
    "source_count_value_row_id",
    "readiness_id",
    "family_id",
    "count_domain",
    "source_final_numeric_count_status",
    "closure_decision",
    "final_numeric_count_status",
    "numeric_parameter_count_value",
    "per_galaxy_privilege_count_value",
    "shared_discount_count_value",
    "final_parsimony_count_value",
    "count_value_source",
    "parsimony_input_allowed",
    "next_required_artifact",
    "endpoint_scoring_allowed",
    "claim_boundary",
]

SUMMARY_FIELDS = [
    "summary_id",
    "final_values_artifact",
    "v08_status",
    "closure_status",
    "shared_discount_status",
    "final_count_rows",
    "final_numeric_count_values_written",
    "per_galaxy_privilege_values_written",
    "shared_discount_count_total",
    "final_parsimony_count_total",
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


def summary_row(filename: str) -> dict[str, str]:
    rows = read_csv(DERIVED / filename)
    if len(rows) != 1:
        raise ValueError(f"expected one summary row in {filename}")
    return rows[0]


def closure_rows_by_readiness() -> dict[str, dict[str, str]]:
    return {row["readiness_id"]: row for row in read_csv(DERIVED / "numeric_count_readiness_closure_v09.csv")}


def final_value_for(row: dict[str, str]) -> tuple[int, int, str]:
    family = row["family_id"]
    domain = row["count_domain"]
    if domain == "global_formula_parameters" and family == "M0":
        return int(summary_row("m0_global_final_count_freeze_summary_v15.csv")["frozen_k_m0_global"]), 0, "m0_global_final_count_freeze_v15"
    if domain == "per_galaxy_privileges" and family == "M0":
        return 0, int(summary_row("m0_per_galaxy_privilege_count_freeze_summary_v11.csv")["frozen_per_galaxy_privilege_count_total"]), "m0_per_galaxy_privilege_count_freeze_v11"
    if domain == "global_response_parameters" and family == "M1":
        return int(summary_row("m1_response_parameter_final_count_freeze_summary_v15.csv")["frozen_k_m1_global"]), 0, "m1_response_parameter_final_count_freeze_v15"
    if domain == "per_galaxy_response_privileges" and family == "M1":
        return 0, int(summary_row("m1_per_galaxy_response_privilege_count_freeze_summary_v11.csv")["frozen_per_galaxy_response_privilege_count_total"]), "m1_per_galaxy_response_privilege_count_freeze_v11"
    if domain == "benchmark_profile_parameters" and family == "M2":
        return int(summary_row("m2_benchmark_parameter_final_count_freeze_summary_v15.csv")["frozen_k_m2_global"]), 0, "m2_benchmark_parameter_final_count_freeze_v15"
    if domain == "per_galaxy_benchmark_privileges" and family == "M2":
        return 0, int(summary_row("m2_per_galaxy_benchmark_privilege_count_freeze_summary_v11.csv")["frozen_per_galaxy_benchmark_privilege_count_total"]), "m2_per_galaxy_benchmark_privilege_count_freeze_v11"
    if domain == "shared_inputs_and_masks" and family == "ALL":
        return 0, 0, "shared_input_count_discount_policy_v10"
    raise ValueError(f"unmapped final count row: {family} {domain}")


def final_rows() -> list[dict[str, object]]:
    v08_summary = summary_row("numeric_parameter_count_table_summary_v08.csv")
    closure_summary = summary_row("numeric_count_readiness_closure_summary_v09.csv")
    shared_summary = summary_row("shared_input_count_discount_policy_summary_v10.csv")
    if v08_summary["overall_status"] != "NUMERIC_PARAMETER_COUNT_TABLE_V08_BLOCKED_ON_FINAL_NUMERIC_COUNT_VALUES":
        raise ValueError("v08 count table is not at the final-values blocker")
    if closure_summary["overall_status"] != "NUMERIC_COUNT_READINESS_CLOSURE_READY_FOR_FINAL_COUNTS":
        raise ValueError("numeric count readiness closure is not ready for final counts")
    if shared_summary["overall_status"] != "SHARED_INPUT_COUNT_DISCOUNT_POLICY_V10_READY_FINAL_NUMERIC_COUNTS_PENDING":
        raise ValueError("shared input count-discount policy is not ready")

    closures = closure_rows_by_readiness()
    shared_discount = int(shared_summary["shared_discount_count_total"])
    rows: list[dict[str, object]] = []
    for index, source in enumerate(read_csv(DERIVED / "numeric_parameter_count_table_v08.csv"), start=1):
        closure = closures[source["readiness_id"]]
        numeric_count, privilege_count, count_source = final_value_for(source)
        final_parsimony_count = numeric_count + privilege_count - shared_discount
        rows.append(
            {
                "final_count_row_id": f"NPCFV10_{index:03d}",
                "source_count_value_row_id": source["count_value_row_id"],
                "readiness_id": source["readiness_id"],
                "family_id": source["family_id"],
                "count_domain": source["count_domain"],
                "source_final_numeric_count_status": source["final_numeric_count_status"],
                "closure_decision": closure["closure_decision"],
                "final_numeric_count_status": "FINAL_NUMERIC_COUNT_VALUE_FROZEN",
                "numeric_parameter_count_value": numeric_count,
                "per_galaxy_privilege_count_value": privilege_count,
                "shared_discount_count_value": shared_discount if source["family_id"] == "ALL" else 0,
                "final_parsimony_count_value": final_parsimony_count,
                "count_value_source": count_source,
                "parsimony_input_allowed": "true",
                "next_required_artifact": NEXT_ARTIFACT,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10",
            "final_values_artifact": "numeric_parameter_count_table_final_values_v10",
            "v08_status": summary_row("numeric_parameter_count_table_summary_v08.csv")["overall_status"],
            "closure_status": summary_row("numeric_count_readiness_closure_summary_v09.csv")["overall_status"],
            "shared_discount_status": summary_row("shared_input_count_discount_policy_summary_v10.csv")["overall_status"],
            "final_count_rows": len(rows),
            "final_numeric_count_values_written": sum(row["final_numeric_count_status"] == "FINAL_NUMERIC_COUNT_VALUE_FROZEN" for row in rows),
            "per_galaxy_privilege_values_written": sum(row["count_domain"].startswith("per_galaxy") for row in rows),
            "shared_discount_count_total": sum(int(row["shared_discount_count_value"]) for row in rows),
            "final_parsimony_count_total": sum(int(row["final_parsimony_count_value"]) for row in rows),
            "parsimony_scores_written": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": STATUS,
            "next_required_artifact": NEXT_ARTIFACT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_doc() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "numeric_parameter_count_table_final_values_v10.md").write_text(
        f"""# Numeric Parameter Count Table Final Values v10

**Doc class:** final numeric parameter-count value freeze
**Status:** final count values frozen; global scoring prerequisites still blocked
**Canonical parent:** Numeric parameter count table v08

Script:

```text
scripts/build_numeric_parameter_count_table_final_values.py
```

Derived outputs:

```text
data/derived/numeric_parameter_count_table_final_values_v10.csv
data/derived/numeric_parameter_count_table_final_values_summary_v10.csv
```

This artifact closes the explicit final-count-value blocker opened by
`numeric_parameter_count_table_v08.csv`. It reads the family-specific final
count freezes, the per-galaxy privilege freezes, and the shared-input discount
policy, then freezes seven final count rows.

The frozen count values are all zero in this protocol state:

```text
M0 global = 0
M0 per-galaxy privilege total = 0
M1 global = 0
M1 per-galaxy response privilege total = 0
M2 global = 0
M2 per-galaxy benchmark privilege total = 0
shared input discount total = 0
```

The next required artifact is:

```text
{NEXT_ARTIFACT}
```

## Claim Boundary

This artifact freezes numeric count values only. It does not compute endpoint residuals,
does not run controls, does not compute parsimony scores, compares no families,
and makes no dark-sector verdict.

Claim boundary:

```text
{CLAIM_BOUNDARY}
```
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = final_rows()
    write_csv(DERIVED / "numeric_parameter_count_table_final_values_v10.csv", rows, FIELDS)
    write_csv(DERIVED / "numeric_parameter_count_table_final_values_summary_v10.csv", summary(rows), SUMMARY_FIELDS)
    write_doc()
    print("PAPER11_NUMERIC_PARAMETER_COUNT_TABLE_FINAL_VALUES_V10_BUILT")


if __name__ == "__main__":
    main()
