#!/usr/bin/env python3
from __future__ import annotations

import csv
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data/derived"
INPUT = ROOT / "data/input"
PACKAGE_ROOT = ROOT / "review_packages/frontier_provenance_v46_review_package"
ZIP_PATH = ROOT / "review_packages/frontier_provenance_v46_review_package.zip"

PACKAGE_FILES = [
    {
        "source": DERIVED / "frontier_provenance_evidence_intake_contract_v44.csv",
        "target": "data/frontier_provenance_evidence_intake_contract_v44.csv",
        "role": "field-level review rules",
    },
    {
        "source": DERIVED / "frontier_provenance_evidence_intake_checklist_v44.csv",
        "target": "data/frontier_provenance_evidence_intake_checklist_v44.csv",
        "role": "row-level manual collection checklist",
    },
    {
        "source": DERIVED / "frontier_provenance_source_candidate_ledger_v45.csv",
        "target": "data/frontier_provenance_source_candidate_ledger_v45.csv",
        "role": "source candidate ledger",
    },
    {
        "source": DERIVED / "frontier_provenance_source_candidate_coverage_v45.csv",
        "target": "data/frontier_provenance_source_candidate_coverage_v45.csv",
        "role": "candidate galaxy-row coverage",
    },
    {
        "source": DERIVED / "frontier_provenance_evidence_payload_draft_v46.csv",
        "target": "data/frontier_provenance_evidence_payload_draft_v46.csv",
        "role": "review-required v21-shaped draft",
    },
    {
        "source": DERIVED / "frontier_provenance_evidence_payload_draft_review_v46.csv",
        "target": "data/frontier_provenance_evidence_payload_draft_review_v46.csv",
        "role": "per-row review action ledger",
    },
    {
        "source": DERIVED / "frontier_provenance_evidence_payload_draft_summary_v46.csv",
        "target": "data/frontier_provenance_evidence_payload_draft_summary_v46.csv",
        "role": "draft summary and claim boundary",
    },
    {
        "source": INPUT / "source_import_provenance_evidence_v21_TEMPLATE.csv",
        "target": "templates/source_import_provenance_evidence_v21_TEMPLATE.csv",
        "role": "fillable target input template",
    },
]


README = """# Frontier Provenance v46 Review Package

**Status:** review package only; not v21 evidence input; no source import; no endpoint scoring.

This package is for reviewing the proposed provenance evidence payload before
anything is copied to `data/input/source_import_provenance_evidence_v21.csv`.

## Reviewer Tasks

1. Verify each SPARC source route points to the intended pre-score source row.
2. Verify the source hash/accession matches the stated source file.
3. Verify the leakage-evidence id is a pre-score source-route review id, not a
   post-score/model-selection artifact.
4. Only after review may a later promotion step mark rows as
   `PROVENANCE_EVIDENCE_COMPLETE`.

## Hard Stops

- Do not treat this package as the v21 evidence input.
- Do not copy rows into `data/input/source_import_provenance_evidence_v21.csv`
  unless a separate review-promotion gate explicitly authorizes it.
- Do not use endpoint residuals, family winners, or scores to approve source
  routes.
"""

DO_NOT_COPY = """# Do Not Copy Without Review

The files in this package are review artifacts. They are not active source
inputs. The v46 payload draft intentionally keeps every row at
`REVIEW_REQUIRED_NOT_COMPLETE`.

Copying these rows into `data/input/source_import_provenance_evidence_v21.csv`
requires a later explicit review-promotion gate.
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_manifest(rows: list[dict[str, str]]) -> None:
    manifest_path = PACKAGE_ROOT / "REVIEW_MANIFEST.csv"
    with manifest_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["package_path", "source_path", "role", "claim_boundary"])
        writer.writeheader()
        writer.writerows(rows)


def build_package() -> None:
    if PACKAGE_ROOT.exists():
        shutil.rmtree(PACKAGE_ROOT)
    PACKAGE_ROOT.mkdir(parents=True, exist_ok=True)
    write_text(PACKAGE_ROOT / "README.md", README)
    write_text(PACKAGE_ROOT / "DO_NOT_COPY_WITHOUT_REVIEW.md", DO_NOT_COPY)

    manifest_rows: list[dict[str, str]] = [
        {
            "package_path": "README.md",
            "source_path": "generated_by_review_package_builder",
            "role": "review instructions",
            "claim_boundary": "review_package_only_no_evidence_no_scores",
        },
        {
            "package_path": "DO_NOT_COPY_WITHOUT_REVIEW.md",
            "source_path": "generated_by_review_package_builder",
            "role": "hard-stop notice",
            "claim_boundary": "review_package_only_no_evidence_no_scores",
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
                "claim_boundary": "review_package_only_no_evidence_no_scores",
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
    print(f"PAPER11_FRONTIER_PROVENANCE_REVIEW_PACKAGE_BUILT {ZIP_PATH}")


if __name__ == "__main__":
    main()
