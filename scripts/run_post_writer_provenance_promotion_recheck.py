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
    evidence_recheck = read_csv(DERIVED / "post_writer_evidence_gate_recheck_summary_v32.csv")[0]
    promotion_rows = read_csv(DERIVED / "source_import_provenance_promotion_gate_v23.csv")
    blockers = []
    if evidence_recheck["provenance_promotion_allowed_after_recheck"] == "false":
        blockers.append("post_writer_evidence_gate_recheck_not_allowed")
    if evidence_recheck["valid_evidence_rows"] == "0":
        blockers.append("zero_valid_evidence_rows_after_writer")
    out: list[dict[str, object]] = []
    for index, row in enumerate(promotion_rows, start=1):
        row_blockers = blockers + ["v23_promotion_decision_not_promote"]
        out.append(
            {
                "recheck_id": f"PWPPR33_{index:03d}",
                "source_promotion_gate_id": row["promotion_gate_id"],
                "galaxy_id": row["galaxy_id"],
                "evidence_recheck_source": "data/derived/post_writer_evidence_gate_recheck_summary_v32.csv",
                "v23_promotion_decision": row["promotion_decision"],
                "valid_evidence_rows_after_writer": evidence_recheck["valid_evidence_rows"],
                "promotion_recheck_blockers": ";".join(row_blockers),
                "provenance_promotion_allowed_after_recheck": "false",
                "provenance_rows_promoted_after_recheck": 0,
                "raw_import_allowed_after_recheck": "false",
                "endpoint_scoring_allowed": "false",
                "claim_boundary": "post_writer_provenance_promotion_recheck_only_no_promotion_no_scores",
            }
        )
    return out


def summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    promoted = sum(int(row["provenance_rows_promoted_after_recheck"]) for row in rows)
    allowed = sum(row["provenance_promotion_allowed_after_recheck"] == "true" for row in rows)
    return [
        {
            "summary_id": "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_V33",
            "promotion_recheck_rows": len(rows),
            "promotion_allowed_rows_after_recheck": allowed,
            "promotion_blocked_rows_after_recheck": len(rows) - allowed,
            "provenance_rows_promoted_after_recheck": promoted,
            "raw_import_allowed_rows_after_recheck": 0,
            "endpoint_scoring_allowed_anywhere": "false",
            "overall_status": "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_BLOCKED"
            if allowed == 0
            else "POST_WRITER_PROVENANCE_PROMOTION_RECHECK_READY",
            "claim_boundary": "post_writer_provenance_promotion_recheck_only_no_promotion_no_scores_no_dark_sector_verdict",
        }
    ]


def main() -> None:
    rows = recheck_rows()
    summary_rows = summary(rows)
    write_csv(
        DERIVED / "post_writer_provenance_promotion_recheck_v33.csv",
        rows,
        [
            "recheck_id",
            "source_promotion_gate_id",
            "galaxy_id",
            "evidence_recheck_source",
            "v23_promotion_decision",
            "valid_evidence_rows_after_writer",
            "promotion_recheck_blockers",
            "provenance_promotion_allowed_after_recheck",
            "provenance_rows_promoted_after_recheck",
            "raw_import_allowed_after_recheck",
            "endpoint_scoring_allowed",
            "claim_boundary",
        ],
    )
    write_csv(
        DERIVED / "post_writer_provenance_promotion_recheck_summary_v33.csv",
        summary_rows,
        [
            "summary_id",
            "promotion_recheck_rows",
            "promotion_allowed_rows_after_recheck",
            "promotion_blocked_rows_after_recheck",
            "provenance_rows_promoted_after_recheck",
            "raw_import_allowed_rows_after_recheck",
            "endpoint_scoring_allowed_anywhere",
            "overall_status",
            "claim_boundary",
        ],
    )
    print("PAPER11_POST_WRITER_PROVENANCE_PROMOTION_RECHECK_V33_BUILT")


if __name__ == "__main__":
    main()
