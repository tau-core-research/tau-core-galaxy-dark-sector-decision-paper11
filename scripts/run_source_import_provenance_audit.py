#!/usr/bin/env python3
from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"

COMPLETE = "PROVENANCE_COMPLETE"


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
    rows = read_csv(DERIVED / "source_import_provenance_manifest_v19.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        statuses = [
            row["catalog_status"],
            row["file_or_table_status"],
            row["row_identity_status"],
            row["hash_or_accession_status"],
            row["leakage_evidence_status"],
        ]
        complete = all(status == COMPLETE for status in statuses)
        blockers = []
        if row["catalog_status"] != COMPLETE:
            blockers.append("catalog_provenance_missing")
        if row["file_or_table_status"] != COMPLETE:
            blockers.append("file_or_table_provenance_missing")
        if row["row_identity_status"] != COMPLETE:
            blockers.append("row_identity_missing")
        if row["hash_or_accession_status"] != COMPLETE:
            blockers.append("hash_or_accession_missing")
        if row["leakage_evidence_status"] != COMPLETE:
            blockers.append("leakage_evidence_missing")
        out.append(
            {
                "audit_id": row["provenance_id"].replace("SIP19", "SIPA20"),
                "galaxy_id": row["galaxy_id"],
                "proposed_split": row["proposed_split"],
                "provenance_complete": str(complete).lower(),
                "raw_import_decision": "ALLOW_RAW_IMPORT" if complete else "DO_NOT_IMPORT_RAW",
                "blocking_requirements": ";".join(blockers) if blockers else "none",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "provenance_audit_only_no_source_import_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    complete_rows = sum(1 for row in rows if row["provenance_complete"] == "true")
    allowed_rows = sum(1 for row in rows if row["raw_import_decision"] == "ALLOW_RAW_IMPORT")
    return [
        {
            "summary_id": "SOURCE_IMPORT_PROVENANCE_AUDIT_V20",
            "audited_rows": len(rows),
            "provenance_complete_rows": complete_rows,
            "raw_import_allowed_rows": allowed_rows,
            "raw_import_blocked_rows": len(rows) - allowed_rows,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "RAW_IMPORT_BLOCKED_BY_PROVENANCE",
            "next_required_artifact": "data/input/source_import_raw_sparc_like_v15.csv",
            "claim_boundary": "provenance_audit_only_no_source_import_no_scores",
        }
    ]


def main() -> None:
    rows = audit_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "source_import_provenance_audit_v20.csv",
        rows,
        [
            "audit_id",
            "galaxy_id",
            "proposed_split",
            "provenance_complete",
            "raw_import_decision",
            "blocking_requirements",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "source_import_provenance_audit_summary_v20.csv",
        summary_rows,
        [
            "summary_id",
            "audited_rows",
            "provenance_complete_rows",
            "raw_import_allowed_rows",
            "raw_import_blocked_rows",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "next_required_artifact",
            "claim_boundary",
        ],
    )
    print("PAPER11_SOURCE_IMPORT_PROVENANCE_AUDIT_V20_BUILT")


if __name__ == "__main__":
    main()
