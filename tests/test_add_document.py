"""Single-document authoring: preview first, write safely, never overwrite silently."""

import importlib.util
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("autodoc_add", ROOT / "scripts/add-document.py")
assert spec is not None and spec.loader is not None
add_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_module)


def test_preview_uses_project_instance_and_todays_date_without_writing(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()

    result = add_module.add("DOC-A03-001", root=project)

    target = project / "docs/autodoc/ARCHITECTURE/DOC-A03-001.md"
    assert result["written"] is False
    assert not target.exists()
    assert result["relative_target"] == "docs/autodoc/ARCHITECTURE/DOC-A03-001.md"
    assert f"id: INST-DEMO-DOC-A03-001" in result["content"]
    assert f"effective_date: {date.today().isoformat()}" in result["content"]
    assert "# C4 context" in result["content"]


def test_write_creates_the_file_and_refuses_silent_overwrite(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()

    first = add_module.add("DOC-A03-001", root=project, write=True)
    target = project / first["relative_target"]
    assert first["written"] is True
    assert target.is_file()

    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        add_module.add("DOC-A03-001", root=project, write=True)

    replacement = add_module.add(
        "DOC-A03-001", root=project, variant="blank", force=True, write=True)
    assert replacement["overwritten"] is True
    assert "<!-- Fill in. -->" in target.read_text(encoding="utf-8")


def test_an_existing_instance_id_is_not_reused_for_a_second_file(tmp_path):
    project = tmp_path / "demo"
    existing = project / "docs/autodoc/foundation.md"
    existing.parent.mkdir(parents=True)
    existing.write_text("---\nid: INST-DEMO-DOC-A03-001\n---\n# Existing\n", encoding="utf-8")

    with pytest.raises(ValueError, match="already used"):
        add_module.add("DOC-A03-001", root=project, write=True)

    result = add_module.add(
        "DOC-A03-001", root=project, instance_id="INST-DEMO-DOC-A03-001-alt", write=True)
    assert result["written"] is True
    assert "id: INST-DEMO-DOC-A03-001-alt" in result["content"]


def test_output_can_name_an_exact_file_inside_the_project(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()

    result = add_module.add(
        "DOC-A03-001", root=project, output=Path("docs/c4-context.md"), write=True)

    assert result["relative_target"] == "docs/c4-context.md"
    assert (project / "docs/c4-context.md").is_file()


def test_unknown_ids_and_paths_outside_the_project_are_rejected(tmp_path):
    project = tmp_path / "demo"
    project.mkdir()

    with pytest.raises(ValueError, match="unknown catalog document id"):
        add_module.add("DOC-Z99-999", root=project)
    with pytest.raises(ValueError, match="must stay inside"):
        add_module.add("DOC-A03-001", root=project, output=Path("../outside.md"), write=True)
