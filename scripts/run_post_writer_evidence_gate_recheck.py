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
    absence = read_csv(DERIVED / "frontier_post_writer_evidence_absence_audit_summary_v31.csv")[0]
    evidence_gate = read_csv(DERIVED / "source_import_provenance_evidence_gate_summary_v22.csv")[0]
    blockers = []
    if absence["absence_confirmed"] == "true":
        blockers.append("post_writer_evidence_absence_confirmed")
    if evidence_gate["provenance_promotion_allowed"] == "false":
        blockers.append("v22_provenance_promotion_not_allowed")
    return [
        {
            "recheck_id": "PWEGR32_POST_WRITER_EVIDENCE_GATE_RECHECK",
            "absence_audit_source": "data/derived/frontier_post_writer_evidence_absence_audit_summary_v31.csv",
            "evidence_gate_source": "data/derived/source_import_provenance_evidence_gate_summary_v22.csv",
            "absence_confirmed": absence["absence_confirmed"],
            "evidence_input_status": evidence_gate["evidence_input_status"],
            "valid_evidence_rows": evidence_gate["valid_evidence_rows"],
            "provenance_promotion_allowed_before_recheck": evidence_gate["provenance_promotion_allowed"],
            "recheck_blockers": ";".join(blockers) if blockers else "none",
            "provenance_promotion_allowed_after_recheck": "false" if blockers else "true",
            "endpoint_scoring_allowed": "false",
            "claim_boundary": "post_writer_evidence_gate_recheck_only_no_promotion_no_scores",
        }
    ]


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    row = rows[0]
    return [
        {
            "summary_id": "POST_WRITER_EVIDENCE_GATE_RECHECK_V32",
            "absence_confirmed": row["absence_confirmed"],
            "valid_evidence_rows": row["valid_evidence_rows"],
            "provenance_promotion_allowed_after_recheck": row["provenance_promotion_allowed_after_recheck"],
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_EVIDENCE_GATE_RECHECK_BLOCKED"
            if row["provenance_promotion_allowed_after_recheck"] == "false"
            else "POST_WRITER_EVIDENCE_GATE_RECHECK_READY",
            "claim_boundary": "post_writer_evidence_gate_recheck_only_no_promotion_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_evidence_gate_recheck_v32.csv",
        rows,
        [
            "recheck_id",
            "absence_audit_source",
            "evidence_gate_source",
            "absence_confirmed",
            "evidence_input_status",
            "valid_evidence_rows",
            "provenance_promotion_allowed_before_recheck",
            "recheck_blockers",
            "provenance_promotion_allowed_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_evidence_gate_recheck_summary_v32.csv",
        summary_rows,
        [
            "summary_id",
            "absence_confirmed",
            "valid_evidence_rows",
            "provenance_promotion_allowed_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_EVIDENCE_GATE_RECHECK_V32_BUILT")


if __name__ == "__main__":
    main()
