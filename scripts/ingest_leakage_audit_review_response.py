#!/usr/bin/env python3
from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
RESPONSE_DIR = ROOT / "review_packages/leakage_audit_v58_completed_review_response"
RESPONSE_ZIP = ROOT / "review_packages/leakage_audit_v58_completed_review_response.zip"

REQUIRED_RESPONSE_FILES = {
    "leakage_audit_v58_review_response.csv",
    "leakage_audit_v58_review_completed_summary.csv",
    "leakage_audit_v58_review_notes.md",
    "leakage_audit_v58_review_validation_log.txt",
}


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


def zip_file_count() -> int:
    with zipfile.ZipFile(RESPONSE_ZIP) as archive:
        names = {Path(name).name for name in archive.namelist() if not name.endswith("/")}
    return len(names & REQUIRED_RESPONSE_FILES)


def response_rows() -> list[dict[str, object]]:
    rows = read_csv(RESPONSE_DIR / "leakage_audit_v58_review_response.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        pass_authorized = row["reviewer_leakage_pass_authorized"] == "true"
        activation_authorized = row["may_activate_row_after_ingestion"] == "true"
        scoring_allowed = row["endpoint_scoring_allowed"] == "true"
        out.append(
            {
                "leakage_evidence_row_id": row["leakage_evidence_row_id"],
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "evidence_id": row["evidence_id"],
                "checked_object": row["checked_object"],
                "source_artifact": row["source_artifact"],
                "review_decision": row["review_decision"],
                "reviewer_leakage_pass_authorized": row["reviewer_leakage_pass_authorized"],
                "may_activate_row_after_ingestion": row["may_activate_row_after_ingestion"],
                "endpoint_scoring_allowed": row["endpoint_scoring_allowed"],
                "intake_decision": "ACCEPT_AS_REVIEWED_NO_GO_NOT_EVIDENCE"
                if not pass_authorized and not activation_authorized and not scoring_allowed
                else "BLOCKED_UNSAFE_LEAKAGE_REVIEW_RESPONSE",
                "claim_boundary": "leakage_review_response_intake_only_no_evidence_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    source_summary = read_csv(RESPONSE_DIR / "leakage_audit_v58_review_completed_summary.csv")[0]
    pass_authorized = sum(row["reviewer_leakage_pass_authorized"] == "true" for row in rows)
    activation_authorized = sum(row["may_activate_row_after_ingestion"] == "true" for row in rows)
    scoring_allowed = sum(row["endpoint_scoring_allowed"] == "true" for row in rows)
    no_go_rows = sum(row["review_decision"] == "NO_GO_EVIDENCE_REQUIRED_NOT_FILLED" for row in rows)
    safe_no_go = (
        len(rows) == 72
        and no_go_rows == len(rows)
        and pass_authorized == 0
        and activation_authorized == 0
        and scoring_allowed == 0
        and source_summary["target_evidence_rows_created_by_this_package"] == "0"
    )
    return [
        {
            "summary_id": "LEAKAGE_AUDIT_REVIEW_RESPONSE_INTAKE_V60",
            "response_zip": "review_packages/leakage_audit_v58_completed_review_response.zip",
            "response_files_present": zip_file_count(),
            "review_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "review_decision": source_summary["decision"],
            "no_go_rows": no_go_rows,
            "leakage_pass_rows_authorized": pass_authorized,
            "activation_rows_authorized": activation_authorized,
            "target_evidence_rows_created_by_response": source_summary["target_evidence_rows_created_by_this_package"],
            "endpoint_scoring_allowed_anywhere": str(scoring_allowed > 0).lower(),
            "overall_status": "LEAKAGE_REVIEW_RESPONSE_ACCEPTED_AS_NO_GO_NOT_EVIDENCE"
            if safe_no_go
            else "LEAKAGE_REVIEW_RESPONSE_BLOCKED_OR_UNSAFE",
            "next_required_action": source_summary["next_required_action"],
            "claim_boundary": "leakage_review_response_intake_only_no_evidence_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = response_rows()
    write_csv(
        DERIVED / "leakage_audit_review_response_intake_v60.csv",
        rows,
        [
            "leakage_evidence_row_id",
            "galaxy_id",
            "proposed_split",
            "evidence_id",
            "checked_object",
            "source_artifact",
            "review_decision",
            "reviewer_leakage_pass_authorized",
            "may_activate_row_after_ingestion",
            "endpoint_scoring_allowed",
            "intake_decision",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "leakage_audit_review_response_intake_summary_v60.csv",
        summary(rows),
        [
            "summary_id",
            "response_zip",
            "response_files_present",
            "review_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "review_decision",
            "no_go_rows",
            "leakage_pass_rows_authorized",
            "activation_rows_authorized",
            "target_evidence_rows_created_by_response",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_action",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_AUDIT_REVIEW_RESPONSE_INTAKE_V60_BUILT")


if __name__ == "__main__":
    main()
