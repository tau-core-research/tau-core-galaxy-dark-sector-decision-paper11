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


def template_rows() -> list[dict[str, object]]:
    scoring_rows = read_csv(DERIVED / "activated_scoring_rows_v08.csv")
    evidence_contract = read_csv(DERIVED / "leakage_evidence_contract_v10.csv")
    out: list[dict[str, object]] = []
    index = 1
    for scoring_row in scoring_rows:
        for evidence in evidence_contract:
            out.append(
                {
                    "leakage_evidence_row_id": f"LAET58_{index:03d}",
                    "galaxy_id": scoring_row["galaxy_id"],
                    "proposed_split": scoring_row["proposed_split"],
                    "evidence_id": evidence["evidence_id"],
                    "checked_object": evidence["checked_object"],
                    "required_evidence": evidence["required_evidence"],
                    "source_artifact": "FILL_REVIEWED_PRESCORE_SOURCE_OR_PROTOCOL_ARTIFACT",
                    "review_decision": "TEMPLATE_ROW_DO_NOT_IMPORT",
                    "review_note": "FILL_NO_ENDPOINT_RESIDUAL_OR_FAMILY_WINNER_USED",
                    "evidence_status": "TEMPLATE_ROW_DO_NOT_IMPORT",
                    "endpoint_scoring_allowed": "false",
                    "claim_boundary": "leakage_evidence_template_only_no_pass_no_scores",
                }
            )
            index += 1
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "summary_id": "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_V58",
            "template_file": "data/input/leakage_audit_evidence_v10_TEMPLATE.csv",
            "target_evidence_file": "data/input/leakage_audit_evidence_v10.csv",
            "template_rows": len(rows),
            "galaxies_covered": len({row["galaxy_id"] for row in rows}),
            "evidence_checks_per_galaxy": 4,
            "leakage_pass_rows_created": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_READY_NOT_EVIDENCE",
            "claim_boundary": "leakage_evidence_template_only_no_pass_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = template_rows()
    fieldnames = [
        "leakage_evidence_row_id",
        "galaxy_id",
        "proposed_split",
        "evidence_id",
        "checked_object",
        "required_evidence",
        "source_artifact",
        "review_decision",
        "review_note",
        "evidence_status",
        "endpoint_scoring_allowed",
        "claim_boundary",
    ]
    write_csv(INPUT / "leakage_audit_evidence_v10_TEMPLATE.csv", rows, fieldnames)
    write_csv(
        DERIVED / "leakage_audit_evidence_template_summary_v58.csv",
        summary(rows),
        [
            "summary_id",
            "template_file",
            "target_evidence_file",
            "template_rows",
            "galaxies_covered",
            "evidence_checks_per_galaxy",
            "leakage_pass_rows_created",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_LEAKAGE_AUDIT_EVIDENCE_TEMPLATE_V58_BUILT")


if __name__ == "__main__":
    main()
