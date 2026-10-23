"""Phase promotion previews the enforcement delta and edits only the declaration values."""

import importlib.util
import tomllib
from datetime import date, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "autodoc_promote", ROOT / "scripts/intelligence/promote.py")
assert spec is not None and spec.loader is not None
promote_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promote_module)

CONFIG = """# owner comment
schema = 1

phase = "build"
phase_declared = "2026-01-01"
audience = ["contributors", "external-users"]

[facts]
"""


def write_config(tmp_path: Path, text: str = CONFIG) -> Path:
    (tmp_path / "LICENSE").write_text("test license\n", encoding="utf-8")
    path = tmp_path / "autodoc.toml"
    path.write_text(text, encoding="utf-8")
    return path


def run(tmp_path: Path, *, target: str, write: bool = False, force: bool = False,
        declared: str = "2026-10-22", text: str = CONFIG):
    path = write_config(tmp_path, text)
    code, result = promote_module.promote(
        repo=tmp_path, config=path, target=target, declared=declared, write=write, force=force)
    return code, result, path


def test_preview_reports_the_beta_cliff_without_writing(tmp_path):
    code, result, path = run(tmp_path, target="beta")

    assert code == 1
    assert result["changed"] is True
    assert result["written"] is False
    assert [item["id"] for item in result["delta"]["newly_required"]] == [
        "DOC-A10-008", "DOC-A15-003"]
    assert result["delta"]["blocked"] is True
    assert path.read_text(encoding="utf-8") == CONFIG


def test_write_refuses_missing_required_documents_without_force(tmp_path):
    code, result, path = run(tmp_path, target="beta", write=True)

    assert code == 1
    assert result["written"] is False
    assert tomllib.loads(path.read_text(encoding="utf-8"))["phase"] == "build"


def test_forced_write_changes_only_the_two_declarations(tmp_path):
    before = tomllib.loads(CONFIG)
    code, result, path = run(tmp_path, target="beta", write=True, force=True)

    assert code == 1
    assert result["written"] is True
    text = path.read_text(encoding="utf-8")
    after = tomllib.loads(text)
    assert after["phase"] == "beta"
    assert after["phase_declared"] == "2026-10-22"
    assert "# owner comment" in text
    before.pop("phase")
    before.pop("phase_declared")
    after.pop("phase")
    after.pop("phase_declared")
    assert before == after


def test_forward_promotion_to_a_warn_phase_writes_cleanly(tmp_path):
    text = CONFIG.replace('"build"', '"prototype"')
    code, result, path = run(tmp_path, target="build", write=True, text=text)

    assert code == 0
    assert result["written"] is True
    assert tomllib.loads(path.read_text(encoding="utf-8"))["phase"] == "build"


def test_preview_does_not_claim_no_enforcement_change_when_the_mode_changes(tmp_path):
    text = 'schema = 1\nphase = "build"\nphase_declared = "2026-01-01"\n'
    code, result, path = run(tmp_path, target="beta", text=text)

    assert code == 0
    assert "no catalog requirement or enforcement changes" not in promote_module.render(result)
    assert "Delta: no catalog requirement changes." in promote_module.render(result)


def test_same_phase_is_a_noop(tmp_path):
    code, result, path = run(tmp_path, target="build")

    assert code == 0
    assert result["changed"] is False
    assert result["written"] is False
    assert path.read_text(encoding="utf-8") == CONFIG


def test_demotion_and_backdating_need_force(tmp_path):
    with pytest.raises(ValueError, match="refusing to demote"):
        run(tmp_path, target="prototype")
    with pytest.raises(ValueError, match="refusing to backdate"):
        run(tmp_path, target="beta", declared="2025-12-31")


def test_missing_declarations_are_inserted_after_schema(tmp_path):
    text = "# generated\nschema = 1\n"
    today = date.today().isoformat()
    code, result, path = run(tmp_path, target="build", write=True, declared=today, text=text)

    assert code == 0
    assert result["written"] is True
    written = path.read_text(encoding="utf-8")
    assert written.index("schema = 1") < written.index('phase = "build"')
    assert written.index('phase = "build"') < written.index("phase_declared")
    assert tomllib.loads(written)["phase_declared"] == today


def test_unknown_phase_and_future_date_are_usage_errors(tmp_path):
    with pytest.raises(ValueError, match="unknown phase"):
        run(tmp_path, target="shipping")
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="future"):
        run(tmp_path, target="beta", declared=tomorrow)
