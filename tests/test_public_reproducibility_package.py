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
        "docs/frozen_policy_bundle_instance_v01.md",
        "docs/galaxy_decision_endpoint_manifest_v01.md",
        "docs/galaxy_sample_freeze_v01.md",
        "docs/scoring_rule_freeze_v01.md",
        "docs/control_manifest_v01.md",
        "docs/decision_threshold_v01.md",
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


def test_policy_bundle_and_endpoint_manifest_are_not_results() -> None:
    bundle = list(csv.DictReader((ROOT / "data/source_manifest/frozen_policy_bundle_instance_v01.csv").open()))
    endpoint = list(csv.DictReader((ROOT / "data/source_manifest/galaxy_decision_endpoint_manifest_v01.csv").open()))
    assert len(bundle) == 9
    assert len(endpoint) == 8
    assert all(row["endpoint_scoring_allowed"] == "false" for row in bundle)
    assert all(row["endpoint_scoring_allowed"] == "false" for row in endpoint)
    statuses = " ".join(row["current_status"] for row in endpoint)
    assert "M0_wins" not in statuses
    assert "M1_wins" not in statuses
    assert "M2_wins" not in statuses


def test_pre_registration_manifests_are_not_endpoint_results() -> None:
    files = [
        "galaxy_sample_freeze_v01.csv",
        "scoring_rule_freeze_v01.csv",
        "control_manifest_v01.csv",
    ]
    for name in files:
        rows = list(csv.DictReader((ROOT / "data/source_manifest" / name).open()))
        assert rows
        assert all(row["endpoint_scoring_allowed"] == "false" for row in rows)

    thresholds = list(csv.DictReader((ROOT / "data/source_manifest/decision_threshold_v01.csv").open()))
    assert {row["verdict_label"] for row in thresholds} == {
        "M0_SUFFICIENT",
        "M1_FAVORED",
        "M2_BENCHMARK_STRONGER",
        "UNRESOLVED",
    }
    assert all("PENDING" in row["current_status"] for row in thresholds)


def test_arxiv_zip_is_source_only_if_present() -> None:
    zip_path = ROOT / "arxiv_submission_source.zip"
    if not zip_path.exists():
        return
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "main.tex" in names
    assert "refs.bib" in names
    assert "main.pdf" not in names
