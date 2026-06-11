#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def recheck_rows() -> list[dict[str, object]]:
    requirements = read_csv(DERIVED / "scoring_input_requirements_v07.csv")
    activation_summary = read_csv(DERIVED / "post_writer_scoring_activation_recheck_summary_v38.csv")[0]
    out: list[dict[str, object]] = []
    for index, row in enumerate(requirements, start=1):
        blockers = []
        if row["current_status"].startswith("BLOCKED"):
            blockers.append("v07_requirement_blocked")
        if activation_summary["rows_activated_after_recheck"] == "0":
            blockers.append("post_writer_activation_recheck_zero_rows")
        if activation_summary["endpoint_scoring_allowed_anywhere"] != "true":
            blockers.append("post_writer_activation_recheck_scoring_not_allowed")
        out.append(
            {
                "recheck_id": f"PWSPR39_{index:03d}",
                "requirement_id": row["requirement_id"],
                "required_artifact": row["required_artifact"],
                "v07_current_status": row["current_status"],
                "v38_rows_activated_after_recheck": activation_summary["rows_activated_after_recheck"],
                "preflight_recheck_blockers": ";".join(blockers),
                "preflight_requirement_status_after_recheck": "BLOCKED" if blockers else "READY",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_scoring_preflight_recheck_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    blocked = sum(row["preflight_requirement_status_after_recheck"] == "BLOCKED" for row in rows)
    formula_components = read_csv(DERIVED / "scoring_formula_components_v07.csv")
    return [
        {
            "summary_id": "POST_WRITER_SCORING_PREFLIGHT_RECHECK_V39",
            "preflight_requirement_rows": len(rows),
            "blocked_requirements_after_recheck": blocked,
            "ready_requirements_after_recheck": len(rows) - blocked,
            "formula_policy_components_ready_not_run": len(formula_components),
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_PREFLIGHT_RECHECK_BLOCKED"
            if blocked
            else "POST_WRITER_SCORING_PREFLIGHT_RECHECK_READY",
            "claim_boundary": "post_writer_scoring_preflight_recheck_only_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_scoring_preflight_recheck_v39.csv",
        rows,
        [
            "recheck_id",
            "requirement_id",
            "required_artifact",
            "v07_current_status",
            "v38_rows_activated_after_recheck",
            "preflight_recheck_blockers",
            "preflight_requirement_status_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_scoring_preflight_recheck_summary_v39.csv",
        summary(rows),
        [
            "summary_id",
            "preflight_requirement_rows",
            "blocked_requirements_after_recheck",
            "ready_requirements_after_recheck",
            "formula_policy_components_ready_not_run",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_SCORING_PREFLIGHT_RECHECK_V39_BUILT")


if __name__ == "__main__":
    main()
