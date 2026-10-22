"""Add only the runtime scripts and reference data to wheel installs."""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath
from typing import Any, cast

from setuptools import setup

ROOT = Path(__file__).resolve().parent
DATA_PREFIX = PurePosixPath("share/autodoc")
RUNTIME_FILES = (
    "scripts/adopt.py",
    "scripts/add-document.py",
    "scripts/init-project.py",
    "scripts/doc-control/check_catalog.py",
    "scripts/doc-control/library.py",
    "scripts/doc-control/guards.py",
    "scripts/doc-control/stub_check.py",
    "scripts/doc-sync/engine.py",
    "scripts/doc-sync/languages.py",
    "scripts/intelligence/context.py",
    "scripts/intelligence/enforce.py",
    "scripts/intelligence/profile.py",
    "scripts/intelligence/promote.py",
    "scripts/intelligence/recommend.py",
)


def runtime_data_files() -> list[tuple[str, tuple[str, ...]]]:
    """Return the executable runtime files plus the catalog/context inputs they need.

    Development scripts, the full documentation tree, examples, tests, Git state, and working
    state are not copied into the wheel. ``MANIFEST.in`` separately includes build inputs in the
    source distribution.
    """
    sources = [ROOT / relative for relative in RUNTIME_FILES]
    for directory, suffixes in (
        ("engine", {".py"}),
        ("CONTROL/metadata", {".json", ".yaml"}),
        ("CATALOG-A", {".yaml"}),
        ("CATALOG-B", {".yaml"}),
        ("CATALOG-C", {".yaml"}),
    ):
        sources.extend(
            path for path in sorted((ROOT / directory).rglob("*"))
            if path.is_file() and path.suffix in suffixes
        )

    destinations: dict[str, list[str]] = {}
    for source in sources:
        if not source.is_file():
            raise RuntimeError(f"missing required AutoDOC runtime input: {source.relative_to(ROOT)}")
        relative = source.relative_to(ROOT)
        destination = (DATA_PREFIX / PurePosixPath(relative.parent.as_posix())).as_posix()
        destinations.setdefault(destination, []).append(relative.as_posix())
    return sorted((destination, tuple(sorted(files)))
                  for destination, files in destinations.items())


# setuptools invokes setup.py from the source root in normal builds; make direct invocations
# deterministic too, so every file named in data_files remains relative to the distribution.
os.chdir(ROOT)
setup(data_files=cast(Any, runtime_data_files()))
