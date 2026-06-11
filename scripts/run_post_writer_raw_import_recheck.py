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
    promotion_by_galaxy = {
        row["galaxy_id"]: row for row in read_csv(DERIVED / "post_writer_provenance_promotion_recheck_v33.csv")
    }
    audit_rows = read_csv(DERIVED / "source_import_provenance_audit_v20.csv")
    out: list[dict[str, object]] = []
    for index, row in enumerate(audit_rows, start=1):
        promotion = promotion_by_galaxy[row["galaxy_id"]]
        blockers = []
        if promotion["provenance_promotion_allowed_after_recheck"] == "false":
            blockers.append("post_writer_provenance_promotion_not_allowed")
        if promotion["provenance_rows_promoted_after_recheck"] == "0":
            blockers.append("zero_provenance_rows_promoted_after_recheck")
        if row["raw_import_decision"] == "DO_NOT_IMPORT_RAW":
            blockers.append("v20_raw_import_decision_not_import")
        out.append(
            {
                "recheck_id": f"PWRI34_{index:03d}",
                "source_audit_id": row["audit_id"],
                "galaxy_id": row["galaxy_id"],
                "promotion_recheck_source": "data/derived/post_writer_provenance_promotion_recheck_v33.csv",
                "v20_raw_import_decision": row["raw_import_decision"],
                "provenance_rows_promoted_after_recheck": promotion["provenance_rows_promoted_after_recheck"],
                "raw_import_recheck_blockers": ";".join(blockers),
                "raw_import_allowed_after_recheck": "false",
                "raw_rows_imported_after_recheck": 0,
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_raw_import_recheck_only_no_raw_import_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    allowed = sum(row["raw_import_allowed_after_recheck"] == "true" for row in rows)
    imported = sum(int(row["raw_rows_imported_after_recheck"]) for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_RAW_IMPORT_RECHECK_V34",
            "raw_import_recheck_rows": len(rows),
            "raw_import_allowed_rows_after_recheck": allowed,
            "raw_import_blocked_rows_after_recheck": len(rows) - allowed,
            "raw_rows_imported_after_recheck": imported,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_RAW_IMPORT_RECHECK_BLOCKED"
            if allowed == 0
            else "POST_WRITER_RAW_IMPORT_RECHECK_READY",
            "claim_boundary": "post_writer_raw_import_recheck_only_no_raw_import_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_raw_import_recheck_v34.csv",
        rows,
        [
            "recheck_id",
            "source_audit_id",
            "galaxy_id",
            "promotion_recheck_source",
            "v20_raw_import_decision",
            "provenance_rows_promoted_after_recheck",
            "raw_import_recheck_blockers",
            "raw_import_allowed_after_recheck",
            "raw_rows_imported_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_raw_import_recheck_summary_v34.csv",
        summary_rows,
        [
            "summary_id",
            "raw_import_recheck_rows",
            "raw_import_allowed_rows_after_recheck",
            "raw_import_blocked_rows_after_recheck",
            "raw_rows_imported_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_RAW_IMPORT_RECHECK_V34_BUILT")


if __name__ == "__main__":
    main()
