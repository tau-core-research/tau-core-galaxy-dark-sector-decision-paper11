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


def audit_rows() -> list[dict[str, object]]:
    writer = read_csv(DERIVED / "frontier_authorized_evidence_writer_summary_v30.csv")[0]
    target_present = TARGET.exists()
    return [
        {
            "audit_id": "FPWEA31_POST_WRITER_EVIDENCE_ABSENCE",
            "writer_summary_source": "data/derived/frontier_authorized_evidence_writer_summary_v30.csv",
            "target_evidence_artifact": "data/input/source_import_provenance_evidence_v21.csv",
            "writer_status": writer["writer_status"],
            "writer_rows_written": writer["rows_written"],
            "writer_target_file_written": writer["target_file_written"],
            "target_evidence_input_present_after_audit": str(target_present).lower(),
            "absence_confirmed": str(not target_present).lower(),
            "evidence_gate_may_be_promoted": "false",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_absence_audit_only_no_evidence_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "FRONTIER_POST_WRITER_EVIDENCE_ABSENCE_AUDIT_V31",
            "absence_confirmed": row["absence_confirmed"],
            "target_evidence_input_present_after_audit": row["target_evidence_input_present_after_audit"],
            "evidence_gate_may_be_promoted": row["evidence_gate_may_be_promoted"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "FRONTIER_EVIDENCE_INPUT_ABSENCE_CONFIRMED"
            if row["absence_confirmed"] == "true"
            else "FRONTIER_EVIDENCE_INPUT_UNEXPECTEDLY_PRESENT",
            "claim_boundary": "post_writer_absence_audit_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = audit_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "frontier_post_writer_evidence_absence_audit_v31.csv",
        rows,
        [
            "audit_id",
            "writer_summary_source",
            "target_evidence_artifact",
            "writer_status",
            "writer_rows_written",
            "writer_target_file_written",
            "target_evidence_input_present_after_audit",
            "absence_confirmed",
            "evidence_gate_may_be_promoted",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "frontier_post_writer_evidence_absence_audit_summary_v31.csv",
        summary_rows,
        [
            "summary_id",
            "absence_confirmed",
            "target_evidence_input_present_after_audit",
            "evidence_gate_may_be_promoted",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_FRONTIER_POST_WRITER_EVIDENCE_ABSENCE_AUDIT_V31_BUILT")


if __name__ == "__main__":
    main()
