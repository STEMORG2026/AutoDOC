"""Small dependency-free CLI over AutoDOC's existing repository scripts.

The installed Python package is kept separate from the user project. The policy/data scripts live
under the distribution's ``share/autodoc`` data directory; ``--repo`` and ``--root`` always name
the project being inspected or generated.
"""

from __future__ import annotations

import argparse
import site
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import Sequence

from . import __version__


def runtime_root() -> Path:
    """Locate the bundled AutoDOC scripts and policy data, never the target project.

    An editable/source checkout is useful for development. Normal installs place data files under
    ``sysconfig.get_path('data')/share/autodoc``; ``site.USER_BASE`` covers ``pip install --user``.
    """
    candidates: list[Path] = [Path(__file__).resolve().parents[1]]
    data_directory = sysconfig.get_path("data")
    if data_directory:
        candidates.append(Path(data_directory) / "share" / "autodoc")
    if site.USER_BASE:
        candidates.append(Path(site.USER_BASE) / "share" / "autodoc")

    required = (
        "scripts/intelligence/enforce.py",
        "scripts/intelligence/evolve.py",
        "scripts/intelligence/promote.py",
        "scripts/doc-sync/engine.py",
        "scripts/doc-control/library.py",
        "scripts/add-document.py",
        "scripts/init-project.py",
        "scripts/adopt.py",
        "engine/extractors/facts.py",
        "CONTROL/metadata/CONTEXT-MODEL.json",
        "CATALOG-A/INDEX.yaml",
        "CATALOG-B/INDEX.yaml",
    )
    checked: set[Path] = set()
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate in checked:
            continue
        checked.add(candidate)
        if all((candidate / relative).is_file() for relative in required):
            return candidate

    raise RuntimeError(
        "AutoDOC runtime files are missing. Reinstall the complete AutoDOC distribution; "
        "the target project is not a substitute for the installed tool assets."
    )


def _add_check_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--repo", type=Path, default=Path.cwd(),
        help="project to inspect (default: current directory)",
    )
    parser.add_argument("--config", type=Path, help="context TOML (default: <repo>/autodoc.toml)")
    parser.add_argument("--baseline", type=Path, help="baseline JSON (default: <repo>/autodoc-baseline.json)")
    parser.add_argument("--write-baseline", action="store_true", help="record current findings as a baseline")
    parser.add_argument("--fail-on-stale", action="store_true", help="fail when old baseline entries no longer match")
    parser.add_argument("--json", action="store_true", help="print a machine-readable JSON report")
    parser.add_argument("--output", type=Path, help="write the report to this file instead of stdout")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="autodoc",
        description="Installable CLI for AutoDOC's bounded documentation checks and generators.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="check a project using its declared context and baseline")
    _add_check_arguments(check)

    generate = commands.add_parser("generate", help="generate mapped factual documents for a project")
    generate.add_argument(
        "--root", type=Path, default=Path.cwd(),
        help="project containing docs/.doc-sync-map.yaml (default: current directory)",
    )
    generate.add_argument("--check", action="store_true", help="check for drift without writing files")
    generate.add_argument("--only", help="run one generator ID from the project's sync map")

    adopt = commands.add_parser("adopt", help="read-only heuristic scan for potentially relevant catalog domains")
    adopt.add_argument("--project-path", type=Path, default=Path.cwd(), help="project to scan (default: current directory)")

    init = commands.add_parser("init", help="scaffold starter documents in an existing project")
    init.add_argument("--name", required=True, help="project name")
    init.add_argument(
        "--type", default="generic", choices=["generic", "web-api", "cli", "library", "ai-agent"],
        help="project type recorded in scaffold prompts (default: generic)",
    )
    init.add_argument("--output", type=Path, default=Path.cwd(), help="existing project directory (default: current directory)")
    init.add_argument("--phase", help="declare the initial phase in autodoc.toml")
    init.add_argument("--profile", help="declare the catalog profile in autodoc.toml")

    add = commands.add_parser("add", help="instantiate one catalog document in a project")
    add.add_argument("document", help="catalog type id, for example DOC-A03-001")
    add.add_argument(
        "--root", type=Path, default=Path.cwd(),
        help="project receiving the document (default: current directory)",
    )
    add.add_argument("--output", type=Path, help="exact file, relative to --root unless absolute")
    add.add_argument(
        "--variant", choices=["canonical", "blank", "example"], default="canonical",
        help="template variant to instantiate (default: canonical)",
    )
    add.add_argument("--instance", dest="instance_id", help="frontmatter instance id")
    add.add_argument("--write", action="store_true", help="write the file instead of previewing")
    add.add_argument("--force", action="store_true", help="allow replacing an existing file")
    add.add_argument("--json", action="store_true", help="print a machine-readable result")

    promote = commands.add_parser("promote", help="preview or apply a declared phase promotion")
    promote.add_argument("--repo", type=Path, default=Path.cwd(),
                         help="repository whose facts are evaluated (default: current directory)")
    promote.add_argument("--config", type=Path, help="context TOML (default: <repo>/autodoc.toml)")
    promote.add_argument("--to", required=True, help="target phase id")
    promote.add_argument("--date", help="declaration date in YYYY-MM-DD (default: today)")
    promote.add_argument("--write", action="store_true", help="apply the promotion instead of previewing")
    promote.add_argument("--force", action="store_true",
                         help="allow a demotion, backdate or write with missing required documents")
    promote.add_argument("--json", action="store_true", help="print a machine-readable result")

    evolve = commands.add_parser("evolve", help="plan safe documentation updates for a project")
    evolve.add_argument("--repo", type=Path, default=Path.cwd(),
                        help="project to evolve (default: current directory)")
    evolve.add_argument("--config", type=Path, help="context TOML (default: <repo>/autodoc.toml)")
    evolve.add_argument("--baseline", type=Path,
                        help="baseline JSON (default: <repo>/autodoc-baseline.json)")
    evolve.add_argument("--write", action="store_true",
                        help="apply safe actions (generated refresh, and drafts with --allow-add)")
    evolve.add_argument("--allow-add", action="store_true",
                        help="with --write, create missing required documents as drafts")
    evolve.add_argument("--check", action="store_true",
                        help="exit 1 when an action is pending, without writing")
    evolve.add_argument("--json", action="store_true", help="print a machine-readable plan")

    templates = commands.add_parser("templates", help="render catalog templates on demand into a project build directory")
    templates.add_argument(
        "--root", type=Path, default=Path.cwd(),
        help="project receiving rendered files (default: current directory)",
    )
    templates.add_argument(
        "--output", type=Path,
        help="output tree root (default: <root>/build/TEMPLATES)",
    )
    templates.add_argument(
        "--variant", choices=["all", "canonical", "blank", "example"], default="all",
        help="variant to render (default: all three)",
    )
    return parser


def _absolute_directory(parser: argparse.ArgumentParser, value: Path, option: str) -> Path:
    directory = value.expanduser().resolve()
    if not directory.is_dir():
        parser.error(f"{option} must be an existing directory: {directory}")
    return directory


def _absolute_file(value: Path) -> Path:
    return value.expanduser().resolve()


def _run_script(script: Path, arguments: Sequence[str]) -> int:
    """Execute an existing script with the same interpreter and preserve its exit code."""
    try:
        return subprocess.run(
            [sys.executable, str(script), *arguments],
            check=False,
        ).returncode
    except OSError as error:
        print(f"AutoDOC could not start {script.name}: {error}", file=sys.stderr)
        return 2


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        tool_root = runtime_root()
    except RuntimeError as error:
        print(f"AutoDOC error: {error}", file=sys.stderr)
        return 2

    if args.command == "check":
        project = _absolute_directory(parser, args.repo, "--repo")
        command = ["--repo", str(project)]
        for option in ("config", "baseline", "output"):
            value = getattr(args, option)
            if value is not None:
                command.extend(("--" + option, str(_absolute_file(value))))
        for option in ("write_baseline", "fail_on_stale", "json"):
            if getattr(args, option):
                command.append("--" + option.replace("_", "-"))
        return _run_script(tool_root / "scripts/intelligence/enforce.py", command)

    if args.command == "generate":
        project = _absolute_directory(parser, args.root, "--root")
        command = ["generate", "--root", str(project)]
        if args.check:
            command.append("--check")
        if args.only:
            command.extend(("--only", args.only))
        return _run_script(tool_root / "scripts/doc-sync/engine.py", command)

    if args.command == "adopt":
        project = _absolute_directory(parser, args.project_path, "--project-path")
        return _run_script(tool_root / "scripts/adopt.py", ["--project-path", str(project)])

    if args.command == "init":
        project = _absolute_directory(parser, args.output, "--output")
        command = ["--name", args.name, "--type", args.type, "--output", str(project)]
        if args.phase:
            command.extend(("--phase", args.phase))
        if args.profile:
            command.extend(("--profile", args.profile))
        return _run_script(tool_root / "scripts/init-project.py", command)

    if args.command == "add":
        project = _absolute_directory(parser, args.root, "--root")
        command = [args.document, "--root", str(project), "--variant", args.variant]
        if args.output is not None:
            command.extend(("--output", str(args.output)))
        if args.instance_id:
            command.extend(("--instance", args.instance_id))
        for option in ("write", "force", "json"):
            if getattr(args, option):
                command.append("--" + option)
        return _run_script(tool_root / "scripts/add-document.py", command)

    if args.command == "promote":
        project = _absolute_directory(parser, args.repo, "--repo")
        command = ["--repo", str(project), "--to", args.to]
        if args.config is not None:
            command.extend(("--config", str(_absolute_file(args.config))))
        if args.date:
            command.extend(("--date", args.date))
        for option in ("write", "force", "json"):
            if getattr(args, option):
                command.append("--" + option)
        return _run_script(tool_root / "scripts/intelligence/promote.py", command)

    if args.command == "evolve":
        project = _absolute_directory(parser, args.repo, "--repo")
        command = ["--repo", str(project)]
        for option in ("config", "baseline"):
            value = getattr(args, option)
            if value is not None:
                command.extend(("--" + option, str(_absolute_file(value))))
        for option in ("write", "allow_add", "check", "json"):
            if getattr(args, option):
                command.append("--" + option.replace("_", "-"))
        return _run_script(tool_root / "scripts/intelligence/evolve.py", command)

    if args.command == "templates":
        project = _absolute_directory(parser, args.root, "--root")
        if args.output is None:
            destination = project / "build" / "TEMPLATES"
        else:
            destination = args.output.expanduser()
            if not destination.is_absolute():
                destination = project / destination
        destination = destination.resolve()
        return _run_script(
            tool_root / "scripts/doc-control/library.py",
            ["--variant", args.variant, "--output-dir", str(destination)],
        )

    parser.error(f"unknown command: {args.command}")
    return 2
