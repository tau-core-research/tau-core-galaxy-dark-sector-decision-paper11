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


def pass_rows() -> list[dict[str, object]]:
    rows = read_csv(INPUT / "leakage_audit_evidence_v10.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        review_ready = (
            row["review_decision"] == "READY_FOR_LEAKAGE_REVIEW_NOT_PASS"
            and row["evidence_status"] == "TARGET_EVIDENCE_ROW_WRITTEN_REVIEW_PENDING"
            and row["reviewer_leakage_pass_authorized"] == "false"
            and row["may_activate_row_after_ingestion"] == "false"
            and row["endpoint_scoring_allowed"] == "false"
        )
        out.append(
            {
                "pass_review_id": row["leakage_evidence_row_id"].replace("LAET58", "LAPRG78"),
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "source_artifact": row["source_artifact"],
                "source_artifact_hash_or_accession": row["source_artifact_hash_or_accession"],
                "source_row_selector": row["source_row_selector"],
                "pass_review_decision": "LEAKAGE_COMPONENT_PASS_REVIEWED_NO_ACTIVATION"
                if review_ready
                else "LEAKAGE_COMPONENT_PASS_BLOCKED",
                "leakage_component_pass_authorized": "true" if review_ready else "false",
                "activation_rows_authorized": "0",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_audit_pass_review_gate_only_no_activation_no_scores",
            }
        )
    return out


def coverage_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for galaxy_id in sorted({str(row["galaxy_id"]) for row in rows}):
        subset = [row for row in rows if row["galaxy_id"] == galaxy_id]
        passed = [row for row in subset if row["leakage_component_pass_authorized"] == "true"]
        out.append(
            {
                "galaxy_id": galaxy_id,
                "passed_leakage_components": len(passed),
                "required_leakage_components": 4,
                "galaxy_leakage_pass_authorized": "true" if len(passed) == 4 else "false",
                "activation_rows_authorized": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "leakage_audit_pass_review_gate_coverage_only_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]], coverage: list[dict[str, object]]) -> list[dict[str, object]]:
    component_passes = sum(row["leakage_component_pass_authorized"] == "true" for row in rows)
    galaxy_passes = sum(row["galaxy_leakage_pass_authorized"] == "true" for row in coverage)
    return [
        {
            "summary_id": "LEAKAGE_AUDIT_PASS_REVIEW_GATE_V78",
            "input_artifact": "data/input/leakage_audit_evidence_v10.csv",
            "component_rows_reviewed": len(rows),
            "component_pass_rows_authorized": component_passes,
            "galaxies_covered": len(coverage),
            "galaxy_leakage_pass_rows_authorized": galaxy_passes,
            "activation_rows_authorized": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_PASS_REVIEWED_ACTIVATION_PENDING"
            if galaxy_passes == len(coverage)
            else "LEAKAGE_AUDIT_PASS_REVIEW_BLOCKED",
            "next_required_artifact": "scoring_activation_gate_recheck_after_leakage_pass",
            "claim_boundary": "leakage_audit_pass_review_gate_only_no_activation_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = pass_rows()
    coverage = coverage_rows(rows)
    summary_rows = summary(rows, coverage)
    write_csv(
        DERIVED / "leakage_audit_pass_review_gate_v78.csv",
        rows,
        [
            "pass_review_id",
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "source_artifact",
            "source_artifact_hash_or_accession",
            "source_row_selector",
            "pass_review_decision",
            "leakage_component_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_audit_pass_review_coverage_v78.csv",
        coverage,
        [
            "galaxy_id",
            "passed_leakage_components",
            "required_leakage_components",
            "galaxy_leakage_pass_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_audit_pass_review_summary_v78.csv",
        summary_rows,
        [
            "summary_id",
            "input_artifact",
            "component_rows_reviewed",
            "component_pass_rows_authorized",
            "galaxies_covered",
            "galaxy_leakage_pass_rows_authorized",
            "activation_rows_authorized",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_AUDIT_PASS_REVIEW_GATE_V78_BUILT")


if __name__ == "__main__":
    main()
