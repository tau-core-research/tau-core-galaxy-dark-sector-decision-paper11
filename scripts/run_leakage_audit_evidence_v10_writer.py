#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"


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


def evidence_rows() -> list[dict[str, object]]:
    template = {
        row["leakage_evidence_row_id"]: row
        for row in read_csv(INPUT / "leakage_audit_evidence_v10_TEMPLATE.csv")
    }
    v76_rows = read_csv(DERIVED / "full_leakage_evidence_ingestion_gate_v76.csv")
    out: list[dict[str, object]] = []
    for row in sorted(v76_rows, key=lambda item: item["leakage_evidence_row_id"]):
        source = template[row["leakage_evidence_row_id"]]
        out.append(
            {
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": source["checked_object"],
                "required_evidence": source["required_evidence"],
                "source_artifact": row["candidate_artifact_uri_or_id"],
                "source_artifact_hash_or_accession": row["candidate_artifact_hash_or_accession"],
                "source_row_selector": row["candidate_row_selector"],
                "source_gate": row["source_gate"],
                "review_decision": "READY_FOR_LEAKAGE_REVIEW_NOT_PASS",
                "review_note": "written from v76 full ingestion gate; no endpoint residual, family winner, or score used by this writer",
                "evidence_status": "TARGET_EVIDENCE_ROW_WRITTEN_REVIEW_PENDING",
                "reviewer_leakage_pass_authorized": "false",
                "may_activate_row_after_ingestion": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_audit_evidence_v10_writer_only_review_pending_no_pass_no_scores",
            }
        )
    return out


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for galaxy_id in sorted({str(row["galaxy_id"]) for row in rows}):
        subset = [row for row in rows if row["galaxy_id"] == galaxy_id]
        out.append(
            {
                "galaxy_id": galaxy_id,
                "target_evidence_rows_written": len(subset),
                "required_evidence_rows": 4,
                "leakage_review_ready": "true" if len(subset) == 4 else "false",
                "leakage_pass_authorized": "false",
                "activation_rows_authorized": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_audit_evidence_v10_writer_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]], coverage: list[dict[str, object]]) -> list[dict[str, object]]:
    review_ready = sum(row["leakage_review_ready"] == "true" for row in coverage)
    return [
        {
            "summary_id": "LEAKAGE_AUDIT_EVIDENCE_V10_WRITER_V77",
            "target_evidence_file": "data/input/leakage_audit_evidence_v10.csv",
            "input_artifact": "data/derived/full_leakage_evidence_ingestion_gate_v76.csv",
            "target_evidence_rows_written": len(rows),
            "galaxies_covered": len(coverage),
            "galaxies_ready_for_leakage_review": review_ready,
            "leakage_pass_rows_authorized": 0,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_EVIDENCE_WRITTEN_REVIEW_PENDING"
            if review_ready == len(coverage)
            else "LEAKAGE_AUDIT_EVIDENCE_WRITE_INCOMPLETE",
            "next_required_artifact": "leakage_audit_pass_review_gate_after_v10_evidence",
            "claim_boundary": "leakage_audit_evidence_v10_writer_only_review_pending_no_pass_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = evidence_rows()
    coverage = coverage_rows(rows)
    summary_rows = summary(rows, coverage)
    write_csv(
        INPUT / "leakage_audit_evidence_v10.csv",
        rows,
        [
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "required_evidence",
            "source_artifact",
            "source_artifact_hash_or_accession",
            "source_row_selector",
            "source_gate",
            "review_decision",
            "review_note",
            "evidence_status",
            "reviewer_leakage_pass_authorized",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_audit_evidence_v10_writer_coverage_v77.csv",
        coverage,
        [
            "galaxy_id",
            "target_evidence_rows_written",
            "required_evidence_rows",
            "leakage_review_ready",
            "leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_audit_evidence_v10_writer_summary_v77.csv",
        summary_rows,
        [
            "summary_id",
            "target_evidence_file",
            "input_artifact",
            "target_evidence_rows_written",
            "galaxies_covered",
            "galaxies_ready_for_leakage_review",
            "leakage_pass_rows_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_AUDIT_EVIDENCE_V10_WRITER_V77_BUILT")


if __name__ == "__main__":
    main()
