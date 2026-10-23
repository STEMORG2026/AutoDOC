"""Source-checkout smoke tests for the installable CLI and project-root boundary."""

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT_VERSION = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]


def run_cli(*arguments, cwd):
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        filter(None, (str(ROOT), environment.get("PYTHONPATH")))
    )
    return subprocess.run(
        [sys.executable, "-m", "autodoc", *map(str, arguments)],
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_version_and_help_are_available_without_a_checkout_cwd(tmp_path):
    version = run_cli("--version", cwd=tmp_path)
    help_result = run_cli("--help", cwd=tmp_path)

    assert version.returncode == 0
    assert version.stdout.strip() == f"autodoc {PROJECT_VERSION}"
    assert help_result.returncode == 0
    assert all(command in help_result.stdout for command in (
        "check", "generate", "adopt", "init", "add", "promote", "evolve", "templates"))


def test_generate_uses_explicit_project_root(tmp_path):
    project = tmp_path / "consumer"
    (project / "docs").mkdir(parents=True)
    (project / "config.schema.json").write_text(
        json.dumps({
            "properties": {
                "PORT": {
                    "type": "integer",
                    "default": 8080,
                    "description": "HTTP listen port",
                }
            }
        }),
        encoding="utf-8",
    )
    (project / "docs/.doc-sync-map.yaml").write_text(
        json.dumps({
            "version": 1,
            "generated": [{
                "id": "config",
                "sources": ["config.schema.json"],
                "target": "docs/CONFIG-REFERENCE.md",
                "generator": "config",
            }],
        }),
        encoding="utf-8",
    )

    generated = run_cli("generate", "--root", project, cwd=tmp_path)
    checked = run_cli("generate", "--root", project, "--check", cwd=tmp_path)

    target = project / "docs/CONFIG-REFERENCE.md"
    assert generated.returncode == 0, generated.stderr
    assert target.is_file()
    assert "8080" in target.read_text(encoding="utf-8")
    assert checked.returncode == 0, checked.stderr


def test_templates_render_from_bundled_catalog_into_selected_project_build(tmp_path):
    project = tmp_path / "consumer"
    project.mkdir()

    rendered = run_cli("templates", "--root", project, "--variant", "blank", cwd=tmp_path)

    target = project / "build/TEMPLATES/ARCHITECTURE/DOC-A03-001.md.blank"
    assert rendered.returncode == 0, rendered.stderr
    assert target.is_file()
    text = target.read_text(encoding="utf-8")
    assert "id: REPLACE-WITH-UNIQUE-INSTANCE-ID" in text
    assert "<!-- Fill in. -->" in text
    assert not (project / "TEMPLATES").exists()


def test_check_adopt_and_init_operate_on_selected_project(tmp_path):
    project = tmp_path / "consumer"
    project.mkdir()
    (project / "pyproject.toml").write_text("[project]\nname = 'consumer'\n", encoding="utf-8")

    adopted = run_cli("adopt", "--project-path", project, cwd=tmp_path)
    checked = run_cli("check", "--repo", project, "--json", cwd=tmp_path)
    initialized = run_cli("init", "--name", "Consumer", "--type", "cli", "--output", project, cwd=tmp_path)

    assert adopted.returncode == 0, adopted.stderr
    assert "A10-BUILD" in adopted.stdout
    assert checked.returncode == 0, checked.stderr
    report = json.loads(checked.stdout)
    assert isinstance(report, dict)
    assert initialized.returncode == 0, initialized.stderr
    assert (project / "docs/autodoc/problem-statement.md").is_file()


def test_adoption_scan_skips_dependency_and_build_trees(tmp_path):
    from scripts.adopt import scan

    project = tmp_path / "consumer"
    hidden = project / ".venv/lib/site-packages"
    hidden.mkdir(parents=True)
    (hidden / "pyproject.toml").write_text("[project]\n", encoding="utf-8")

    assert scan(project) == []


def test_add_and_promote_operate_on_selected_project(tmp_path):
    project = tmp_path / "consumer"
    project.mkdir()

    initialized = run_cli(
        "init", "--name", "Consumer", "--type", "cli", "--output", project,
        "--phase", "prototype", cwd=tmp_path)
    assert initialized.returncode == 0, initialized.stderr
    assert (project / "autodoc.toml").is_file()

    added = run_cli("add", "DOC-A03-001", "--root", project, "--write", cwd=tmp_path)
    assert added.returncode == 0, added.stderr
    document = project / "docs/autodoc/ARCHITECTURE/DOC-A03-001.md"
    assert document.is_file()

    preview = run_cli("promote", "--repo", project, "--to", "build", "--json", cwd=tmp_path)
    assert preview.returncode == 0, preview.stderr
    result = json.loads(preview.stdout)
    assert result["changed"] is True
    assert result["written"] is False

    written = run_cli("promote", "--repo", project, "--to", "build", "--write", cwd=tmp_path)
    assert written.returncode == 0, written.stderr
    assert tomllib.loads((project / "autodoc.toml").read_text(encoding="utf-8"))["phase"] == "build"


def test_evolve_plans_safe_actions_and_checks_pending_work(tmp_path):
    project = tmp_path / "consumer"
    project.mkdir()
    (project / "README.md").write_text("# Consumer\n", encoding="utf-8")
    (project / "autodoc.toml").write_text(
        'schema = 1\nphase = "beta"\nphase_declared = "2026-10-23"\n'
        'audience = ["contributors", "external-users"]\n',
        encoding="utf-8",
    )

    preview = run_cli("evolve", "--repo", project, "--json", cwd=tmp_path)
    assert preview.returncode == 0, preview.stderr
    plan = json.loads(preview.stdout)
    assert plan["summary"]["actions"] >= 1
    assert plan["summary"]["written"] == 0
    assert not (project / "docs").exists()

    checked = run_cli("evolve", "--repo", project, "--check", cwd=tmp_path)
    assert checked.returncode == 1
    assert "create" in checked.stdout
    assert not (project / "docs").exists()

    conflict = run_cli("evolve", "--repo", project, "--check", "--write", cwd=tmp_path)
    assert conflict.returncode == 2
