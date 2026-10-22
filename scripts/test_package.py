#!/usr/bin/env python3
"""Build and exercise AutoDOC's wheel/sdist in a clean venv outside the checkout."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import venv
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "pyproject.toml").open("rb") as project_file:
    PROJECT_VERSION = tomllib.load(project_file)["project"]["version"]


def run(command: list[str], *, cwd: Path, expected: int = 0, env: dict[str, str] | None = None):
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)
    if result.returncode != expected:
        print(f"Command returned {result.returncode}, expected {expected}: {' '.join(command)}", file=sys.stderr)
        if result.stdout:
            print("--- stdout ---\n" + result.stdout, file=sys.stderr)
        if result.stderr:
            print("--- stderr ---\n" + result.stderr, file=sys.stderr)
        raise RuntimeError("package verification command failed")
    return result


def extract_generated_sdist(archive_path: Path, destination: Path) -> Path:
    """Extract only ordinary files/directories from the just-built sdist, rejecting path escapes."""
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        tops = set()
        for member in members:
            path = PurePosixPath(member.name)
            if path.is_absolute() or ".." in path.parts or not path.parts:
                raise RuntimeError(f"unsafe path in generated sdist: {member.name!r}")
            if not (member.isdir() or member.isfile()):
                raise RuntimeError(f"unexpected special file in generated sdist: {member.name!r}")
            tops.add(path.parts[0])
        if len(tops) != 1:
            raise RuntimeError("sdist must contain exactly one top-level source directory")
        archive.extractall(destination, members=members)
    return destination / next(iter(tops))


def smoke_installed_cli(wheel: Path, work: Path) -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    environment.pop("PYTHONHOME", None)

    environment_dir = work / "venv"
    venv.EnvBuilder(with_pip=True).create(environment_dir)
    scripts_dir = environment_dir / ("Scripts" if os.name == "nt" else "bin")
    python_name = "python.exe" if os.name == "nt" else "python"
    cli_name = "autodoc.exe" if os.name == "nt" else "autodoc"
    venv_python = scripts_dir / python_name
    cli = scripts_dir / cli_name

    run([str(venv_python), "-m", "pip", "install", "--no-deps", str(wheel)], cwd=work, env=environment)
    version = run([str(cli), "--version"], cwd=work, env=environment)
    if version.stdout.strip() != f"autodoc {PROJECT_VERSION}":
        raise RuntimeError(f"unexpected installed version output: {version.stdout.strip()!r}")
    help_text = run([str(cli), "--help"], cwd=work, env=environment)
    if not all(command in help_text.stdout for command in ("check", "generate", "adopt", "init")):
        raise RuntimeError("installed CLI help omitted one or more supported commands")
    invalid = run([str(cli), "unsupported-command"], cwd=work, expected=2, env=environment)
    if "invalid choice" not in invalid.stderr:
        raise RuntimeError("installed CLI did not report invalid usage through argparse")

    project = work / "consumer-project"
    project.mkdir()
    (project / "pyproject.toml").write_text("[project]\nname = 'consumer-project'\n", encoding="utf-8")

    adopted = run([str(cli), "adopt", "--project-path", str(project)], cwd=work, env=environment)
    if "A10-BUILD" not in adopted.stdout:
        raise RuntimeError("installed adoption scan did not identify the project manifest")

    run([str(cli), "init", "--name", "Consumer Project", "--type", "cli", "--output", str(project)],
        cwd=work, env=environment)
    if not (project / "docs/autodoc/problem-statement.md").is_file():
        raise RuntimeError("installed init command did not scaffold the foundation documents")

    checked = run([str(cli), "check", "--repo", str(project), "--json"], cwd=work, env=environment)
    report = json.loads(checked.stdout)
    if not isinstance(report, dict):
        raise RuntimeError("installed check command did not produce a JSON report")

    (project / "config.schema.json").write_text(
        json.dumps({"properties": {"PORT": {
            "type": "integer", "default": 8080, "description": "HTTP listen port"
        }}}),
        encoding="utf-8",
    )
    (project / "docs/.doc-sync-map.yaml").write_text(
        json.dumps({"version": 1, "generated": [{
            "id": "config",
            "sources": ["config.schema.json"],
            "target": "docs/CONFIG-REFERENCE.md",
            "generator": "config",
        }]}),
        encoding="utf-8",
    )
    run([str(cli), "generate", "--root", str(project)], cwd=work, env=environment)
    generated = project / "docs/CONFIG-REFERENCE.md"
    if not generated.is_file() or "8080" not in generated.read_text(encoding="utf-8"):
        raise RuntimeError("installed generate command did not use the selected project root")
    run([str(cli), "generate", "--root", str(project), "--check"], cwd=work, env=environment)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="autodoc-package-") as temporary:
        work = Path(temporary)
        distributions = work / "dist"
        distributions.mkdir()
        run([sys.executable, "-m", "build", "--outdir", str(distributions)], cwd=ROOT)

        wheels = list(distributions.glob("autodoc-*.whl"))
        sdists = list(distributions.glob("autodoc-*.tar.gz"))
        if len(wheels) != 1 or len(sdists) != 1:
            raise RuntimeError("expected exactly one wheel and one source distribution")

        runtime_prefix = f"autodoc-{PROJECT_VERSION}.data/data/share/autodoc/"
        required_runtime = (
            "scripts/intelligence/enforce.py",
            "scripts/doc-sync/engine.py",
            "scripts/doc-control/check_catalog.py",
            "engine/extractors/facts.py",
            "CONTROL/metadata/CONTEXT-MODEL.json",
            "CATALOG-B/INDEX.yaml",
        )
        with ZipFile(wheels[0]) as archive:
            members = set(archive.namelist())
        missing = [relative for relative in required_runtime if runtime_prefix + relative not in members]
        if missing:
            raise RuntimeError("wheel is missing required runtime files: " + ", ".join(missing))
        if runtime_prefix + "scripts/test_package.py" in members:
            raise RuntimeError("wheel must not ship the development-only package test harness")
        if any(member == "engine/__init__.py" or member.startswith("engine/") for member in members):
            raise RuntimeError("wheel must not install AutoDOC's private engine as a generic top-level package")

        source = extract_generated_sdist(sdists[0], work / "sdist-source")
        rebuilt = work / "wheel-from-sdist"
        rebuilt.mkdir()
        run([sys.executable, "-m", "build", "--wheel", "--outdir", str(rebuilt), str(source)], cwd=work)
        if not list(rebuilt.glob("autodoc-*.whl")):
            raise RuntimeError("could not rebuild a wheel from the source distribution")

        smoke_installed_cli(wheels[0], work / "installed-smoke")

    print("Package check passed: wheel and sdist built; sdist rebuilt; clean wheel install exercised version/check/generate/adopt/init.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, subprocess.SubprocessError, tarfile.TarError, RuntimeError) as error:
        print(f"Package check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
