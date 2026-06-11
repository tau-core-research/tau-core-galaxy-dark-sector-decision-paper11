from __future__ import annotations

import csv
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_required_files_exist() -> None:
    required = [
        "README.md",
        "DATA_NOTICE.md",
        "CITATION.cff",
        "LICENSE",
        "paper11_submission_source/main.tex",
        "paper11_submission_source/refs.bib",
        "scripts/reproduce.py",
        "scripts/validate_protocol_manifests.py",
    ]
    for rel in required:
        assert (ROOT / rel).exists(), rel


def test_manuscript_scope_and_forbidden_overclaims() -> None:
    text = (ROOT / "paper11_submission_source/main.tex").read_text()
    assert "dark-sector necessity" in text.lower()
    assert "Response" in text
    forbidden = [
        "dark matter does not exist",
        "Tau Core replaces the standard dark sector",
        "lensing, CMB, BAO, growth, or cosmology are solved",
    ]
    for phrase in forbidden:
        assert phrase in text


def test_model_family_manifest_is_endpoint_disabled() -> None:
    path = ROOT / "data/source_manifest/model_family_decision_protocol.csv"
    rows = list(csv.DictReader(path.open()))
    assert {row["family_id"] for row in rows} == {"M0", "M1", "M2"}
    assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)


def test_arxiv_zip_is_source_only_if_present() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
