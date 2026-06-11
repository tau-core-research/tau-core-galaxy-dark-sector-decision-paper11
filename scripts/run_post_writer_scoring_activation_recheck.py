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
    leakage_by_galaxy = {
        row["galaxy_id"]: row for row in read_csv(DERIVED / "post_writer_leakage_audit_recheck_v37.csv")
    }
    activation_rows = read_csv(DERIVED / "scoring_activation_gate_v13.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(activation_rows, start=1):
        leakage_row = leakage_by_galaxy[row["galaxy_id"]]
        blockers = []
        if leakage_row["leakage_pass_after_recheck"] != "true":
            blockers.append("post_writer_leakage_audit_not_passed")
        if leakage_row["activation_allowed_after_recheck"] != "true":
            blockers.append("post_writer_leakage_recheck_disallows_activation")
        if row["activation_decision"] != "ACTIVATE_FOR_SCORING":
            blockers.append("v13_activation_gate_not_passed")
        out.append(
            {
                "recheck_id": f"PWSAR38_{index:03d}",
                "activation_gate_id": row["activation_gate_id"],
                "galaxy_id": row["galaxy_id"],
                "leakage_recheck_source": "data/derived/post_writer_leakage_audit_recheck_v37.csv",
                "v37_leakage_pass_after_recheck": leakage_row["leakage_pass_after_recheck"],
                "v37_activation_allowed_after_recheck": leakage_row["activation_allowed_after_recheck"],
                "v13_activation_decision": row["activation_decision"],
                "v13_blocking_requirements": row["blocking_requirements"],
                "activation_recheck_blockers": ";".join(blockers),
                "activation_decision_after_recheck": "DO_NOT_ACTIVATE" if blockers else "ACTIVATE_FOR_SCORING",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_scoring_activation_recheck_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    activated = sum(row["activation_decision_after_recheck"] == "ACTIVATE_FOR_SCORING" for row in rows)
    global_blockers = sum(
        row["current_status"] == "BLOCKED" for row in read_csv(DERIVED / "scoring_activation_global_blockers_v13.csv")
    )
    return [
        {
            "summary_id": "POST_WRITER_SCORING_ACTIVATION_RECHECK_V38",
            "activation_recheck_rows": len(rows),
            "rows_activated_after_recheck": activated,
            "row_level_blocked_rows_after_recheck": len(rows) - activated,
            "global_blockers_after_recheck": global_blockers,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_SCORING_ACTIVATION_RECHECK_BLOCKED"
            if activated == 0 or global_blockers
            else "POST_WRITER_SCORING_ACTIVATION_RECHECK_READY",
            "claim_boundary": "post_writer_scoring_activation_recheck_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    write_csv(
        DERIVED / "post_writer_scoring_activation_recheck_v38.csv",
        rows,
        [
            "recheck_id",
            "activation_gate_id",
            "galaxy_id",
            "leakage_recheck_source",
            "v37_leakage_pass_after_recheck",
            "v37_activation_allowed_after_recheck",
            "v13_activation_decision",
            "v13_blocking_requirements",
            "activation_recheck_blockers",
            "activation_decision_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_scoring_activation_recheck_summary_v38.csv",
        summary(rows),
        [
            "summary_id",
            "activation_recheck_rows",
            "rows_activated_after_recheck",
            "row_level_blocked_rows_after_recheck",
            "global_blockers_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_SCORING_ACTIVATION_RECHECK_V38_BUILT")


if __name__ == "__main__":
    main()
