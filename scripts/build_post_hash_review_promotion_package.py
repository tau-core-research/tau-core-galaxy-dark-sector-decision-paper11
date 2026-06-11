#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
PACKAGE_ROOT = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_review_package"
ZIP_PATH = ROOT / "review_packages/frontier_post_hash_review_promotion_v51_review_package.zip"

PACKAGE_FILES = [
    {
        "source": DERIVED / "frontier_provenance_evidence_payload_draft_v46.csv",
        "target": "data/frontier_provenance_evidence_payload_draft_v46.csv",
        "role": "review-required v21-shaped draft",
    },
    {
        "source": DERIVED / "frontier_provenance_evidence_payload_draft_review_v46.csv",
        "target": "data/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "role": "original per-row review action ledger",
    },
    {
        "source": DERIVED / "frontier_provenance_review_response_intake_v48.csv",
        "target": "data/frontier_provenance_review_response_intake_v48.csv",
        "role": "completed review response intake",
    },
    {
        "source": DERIVED / "frontier_provenance_review_response_intake_summary_v48.csv",
        "target": "data/frontier_provenance_review_response_intake_summary_v48.csv",
        "role": "completed review response summary",
    },
    {
        "source": DERIVED / "frontier_review_promotion_gate_v49.csv",
        "target": "data/frontier_review_promotion_gate_v49.csv",
        "role": "pre-hash promotion gate",
    },
    {
        "source": DERIVED / "frontier_review_promotion_gate_summary_v49.csv",
        "target": "data/frontier_review_promotion_gate_summary_v49.csv",
        "role": "pre-hash promotion gate summary",
    },
    {
        "source": DERIVED / "frontier_external_hash_recompute_audit_v50.csv",
        "target": "data/frontier_external_hash_recompute_audit_v50.csv",
        "role": "external source hash recomputation audit",
    },
    {
        "source": DERIVED / "frontier_external_hash_recompute_audit_summary_v50.csv",
        "target": "data/frontier_external_hash_recompute_audit_summary_v50.csv",
        "role": "external source hash recomputation summary",
    },
    {
        "source": DERIVED / "post_hash_frontier_review_promotion_recheck_v51.csv",
        "target": "data/post_hash_frontier_review_promotion_recheck_v51.csv",
        "role": "post-hash promotion recheck",
    },
    {
        "source": DERIVED / "post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        "target": "data/post_hash_frontier_review_promotion_recheck_summary_v51.csv",
        "role": "post-hash promotion recheck summary",
    },
]

README = """# Frontier Post-Hash Review Promotion Package

**Status:** review package only; not v21 evidence input; no source import; no endpoint scoring.

This package is for a human review-promotion decision after the v50 external
SPARC hash recomputation audit closed the hash caveat.

## What Is Already Closed

- The v46 draft has the v21 column shape but remains review-required.
- The v48 response passed route/prescore checks but did not authorize v21 copy.
- The v50 hash audit recomputed and matched the SPARC Table1 hash.
- The v51 recheck confirms hash support for all eighteen review rows.

## What Is Still Needed

The reviewer must explicitly decide whether the eighteen rows may be promoted
to active v21 provenance evidence.

Use:

```text
templates/frontier_review_promotion_authorization_TEMPLATE.csv
```

Only a later ingestion gate may consume a completed authorization response. This
package itself must not be copied into:

```text
data/input/source_import_provenance_evidence_v21.csv
```

## Hard Stops

- Do not treat this package as active v21 evidence.
- Do not mark `PROVENANCE_EVIDENCE_COMPLETE` from this package alone.
- Do not import observed values or run endpoint scoring from this package.
- Do not use endpoint residuals, family winners, or score outcomes to authorize
  provenance rows.
"""

DO_NOT_COPY = """# Do Not Copy Without Explicit Promotion Authorization

This package documents that the external SPARC hash caveat is closed, but it is
not itself a promotion decision.

Rows may be copied into `data/input/source_import_provenance_evidence_v21.csv`
only after a completed authorization response explicitly marks the relevant
rows as `PROMOTE_TO_COMPLETE_V21_EVIDENCE` and a later ingestion gate accepts
that response.
"""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def authorization_template_rows() -> list[dict[str, object]]:
    rows = read_csv(DERIVED / "post_hash_frontier_review_promotion_recheck_v51.csv")
    out: list[dict[str, object]] = []
    for row in rows:
        out.append(
            {
                "review_id": row["review_id"],
                "galaxy_id": row["galaxy_id"],
                "primary_table1_hash_recomputed_matched": row["primary_table1_hash_recomputed_matched"],
                "current_recheck_decision": row["promotion_recheck_decision"],
                "reviewer_promotion_decision": "KEEP_REVIEW_REQUIRED_NOT_COMPLETE_NO_V21_WRITE",
                "may_copy_to_v21_after_authorization": "false",
                "may_mark_provenance_complete_after_authorization": "false",
                "endpoint_scoring_allowed": "false",
                "reviewer_notes": "",
            }
        )
    return out


def write_manifest(rows: list[dict[str, str]]) -> None:
    write_csv(
        PACKAGE_ROOT / "REVIEW_MANIFEST.csv",
        rows,
        ["package_path", "source_path", "role", "claim_boundary"],
    )


def build_package() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_EXPLICIT_PROMOTION.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_post_hash_review_promotion_package_builder",
            "role": "review instructions",
            "claim_boundary": "post_hash_review_promotion_package_only_no_evidence_no_scores",
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_EXPLICIT_PROMOTION.md",
            "source_path": "generated_by_post_hash_review_promotion_package_builder",
            "role": "hard-stop notice",
            "claim_boundary": "post_hash_review_promotion_package_only_no_evidence_no_scores",
        },
    ]

    for item in PACKAGE_FILES:
        target = PACKAGE_ROOT / item["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item["source"], target)
        manifest_rows.append(
            {
                "package_path": item["target"],
                "source_path": str(item["source"].relative_to(ROOT)),
                "role": item["role"],
                "claim_boundary": "post_hash_review_promotion_package_only_no_evidence_no_scores",
            }
        )

    template_target = PACKAGE_ROOT / "templates/frontier_review_promotion_authorization_TEMPLATE.csv"
    write_csv(
        template_target,
        authorization_template_rows(),
        [
            "review_id",
            "galaxy_id",
            "primary_table1_hash_recomputed_matched",
            "current_recheck_decision",
            "reviewer_promotion_decision",
            "may_copy_to_v21_after_authorization",
            "may_mark_provenance_complete_after_authorization",
            "endpoint_scoring_allowed",
            "reviewer_notes",
        ],
    )
    manifest_rows.append(
        {
            "package_path": "templates/frontier_review_promotion_authorization_TEMPLATE.csv",
            "source_path": "generated_from_post_hash_frontier_review_promotion_recheck_v51",
            "role": "fillable promotion authorization response template",
            "claim_boundary": "post_hash_review_promotion_package_only_no_evidence_no_scores",
        }
    )

    write_manifest(manifest_rows)

    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PACKAGE_ROOT.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(PACKAGE_ROOT.parent))


def main() -> None:
    build_package()
    print(f"PAPER11_POST_HASH_REVIEW_PROMOTION_PACKAGE_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
