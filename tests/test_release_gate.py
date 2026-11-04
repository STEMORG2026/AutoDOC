"""The release gate refuses a tag that disagrees with the package and the changelog."""
import importlib.util
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "autodoc_release_gate", ROOT / "scripts/doc-control/release_snapshot.py")
release = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(release)


def _tree(root, version, changelog_version=None):
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "demo"\nversion = "{version}"\n', encoding="utf-8")
    (root / "CHANGELOG.md").write_text(
        f"# Changelog\n\n## {changelog_version or version} — 2026-01-01\n", encoding="utf-8")


def test_a_matching_tag_version_and_changelog_are_accepted(tmp_path):
    _tree(tmp_path, "1.2.3")

    assert release.require_release_version("v1.2.3", tmp_path) == "1.2.3"


def test_a_tag_that_disagrees_with_pyproject_is_refused(tmp_path):
    _tree(tmp_path, "1.2.3")

    with pytest.raises(ValueError, match="does not match the declared project version 1.2.3"):
        release.require_release_version("v1.2.4", tmp_path)


def test_a_missing_changelog_section_is_refused(tmp_path):
    _tree(tmp_path, "1.2.3", changelog_version="1.2.2")

    with pytest.raises(ValueError, match='CHANGELOG.md has no "## 1.2.3" section'):
        release.require_release_version("v1.2.3", tmp_path)


def test_an_unreadable_project_version_is_a_release_error(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'demo'\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")

    with pytest.raises(ValueError, match="cannot read the declared project version"):
        release.require_release_version("v1.2.3", tmp_path)


def test_the_repository_tag_and_version_are_consistent():
    version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]

    assert release.require_release_version(f"v{version}") == version


def test_the_snapshot_runs_the_version_gate_before_creating_anything(tmp_path):
    output = tmp_path / "never"
    with pytest.raises(ValueError, match="does not match the declared project version"):
        release.snapshot("v9.9.9", output)
    assert not output.exists()
