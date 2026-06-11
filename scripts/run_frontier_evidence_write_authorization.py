#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
TARGET = ROOT / "data/input/source_import_provenance_evidence_v21.csv"


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


def authorization_rows() -> list[dict[str, object]]:
    completion = read_csv(DERIVED / "frontier_work_order_completion_gate_summary_v28.csv")[0]
    all_closed = completion["work_orders_closed"] == completion["completion_gate_rows"]
    target_exists = TARGET.exists()
    blockers = []
    if not all_closed:
        blockers.append("frontier_work_orders_not_closed")
    if target_exists:
        blockers.append("target_evidence_input_already_present")
    return [
        {
            "authorization_id": "FEWA29_FRONTIER_EVIDENCE_WRITE",
            "completion_gate_source": "data/derived/frontier_work_order_completion_gate_summary_v28.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "completion_gate_status": completion["overall_status"],
            "completion_gate_rows": completion["completion_gate_rows"],
            "work_orders_closed": completion["work_orders_closed"],
            "target_evidence_input_present": str(target_exists).lower(),
            "write_blockers": ";".join(blockers) if blockers else "none",
            "write_authorized": "true" if not blockers else "false",
            "target_file_written": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "frontier_evidence_write_authorization_only_no_evidence_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "FRONTIER_EVIDENCE_WRITE_AUTHORIZATION_V29",
            "write_authorized": row["write_authorized"],
            "target_evidence_input_present": row["target_evidence_input_present"],
            "target_file_written": row["target_file_written"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_WRITE_BLOCKED"
            if row["write_authorized"] == "false"
            else "FRONTIER_EVIDENCE_WRITE_AUTHORIZED_NOT_WRITTEN",
            "claim_boundary": "frontier_evidence_write_authorization_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = authorization_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_evidence_write_authorization_v29.csv",
        rows,
        [
            "authorization_id",
            "completion_gate_source",
            "target_evidence_artifact",
            "completion_gate_status",
            "completion_gate_rows",
            "work_orders_closed",
            "target_evidence_input_present",
            "write_blockers",
            "write_authorized",
            "target_file_written",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_evidence_write_authorization_summary_v29.csv",
        summary_rows,
        [
            "summary_id",
            "write_authorized",
            "target_evidence_input_present",
            "target_file_written",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_EVIDENCE_WRITE_AUTHORIZATION_V29_BUILT")


if __name__ == "__main__":
    main()
