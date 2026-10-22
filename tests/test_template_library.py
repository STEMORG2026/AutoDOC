"""On-demand rendering from catalog records, with no committed variant outputs."""

import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("template_library", ROOT / "scripts/doc-control/library.py")
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)


def test_every_catalog_type_renders_all_three_variants_from_one_entry():
    entries = library.catalog_sources(ROOT)

    assert len(entries) == 265
    assert len({doc["id"] for doc, _ in entries}) == len(entries)
    for doc, relative in entries:
        assert relative.parts[0] != "TEMPLATES"
        assert relative.name == f"{doc['id']}.md"
        assert all(library.render(doc, variant).startswith("---\n") for variant in library.VARIANTS)
    assert library.checked_in_outputs(ROOT) == []


def test_single_variant_writes_only_that_variant(tmp_path):
    assert library.run(variant="blank", output_dir=tmp_path, root=ROOT)

    outputs = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert len(outputs) == 265
    assert all(path.name.endswith(".md.blank") for path in outputs)
    example = tmp_path / "ARCHITECTURE/DOC-A03-001.md.blank"
    assert example.is_file()
    assert "<!-- Fill in. -->" in example.read_text(encoding="utf-8")
    assert not (tmp_path / "ARCHITECTURE/DOC-A03-001.md").exists()
    assert not (tmp_path / "ARCHITECTURE/DOC-A03-001.md.example").exists()


def test_all_variants_are_deterministic_and_use_catalog_relative_paths(tmp_path):
    assert library.run(output_dir=tmp_path, root=ROOT)

    outputs = [path for path in tmp_path.rglob("*") if path.is_file()]
    assert len(outputs) == 795
    for doc, relative in library.catalog_sources(ROOT):
        for variant, suffix in library.VARIANT_SUFFIX.items():
            target = tmp_path / Path(str(relative) + suffix)
            assert target.read_text(encoding="utf-8") == library.render(doc, variant)


def test_render_rejects_unsafe_destination_and_unknown_variant():
    with pytest.raises(ValueError, match="logical destination"):
        library._destination({"id": "DOC-A03-001", "template": "TEMPLATES/../escape.md"})
    with pytest.raises(ValueError, match="unknown template variant"):
        library.render({"id": "DOC-A03-001", "name": "C4 context", "type": "DES"}, "other")


def test_outputs_cannot_be_written_back_into_the_source_tree():
    with pytest.raises(ValueError, match="may not be written inside"):
        library.run(output_dir=ROOT / "TEMPLATES" / "generated", root=ROOT)


def test_source_check_rejects_committed_render_outputs():
    with patch.object(library, "checked_in_outputs", return_value=[ROOT / "TEMPLATES/example.md"]):
        assert not library.run(check=True, root=ROOT)


def test_source_check_passes_without_materializing_outputs():
    assert library.run(check=True, root=ROOT)
