#!/usr/bin/env python3
"""Add one catalog document to a project, previewing by default and never overwriting silently."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "scripts/doc-control/library.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


library = load_module("autodoc_library", LIBRARY)


def catalog(root: Path = ROOT) -> list[dict]:
    return [doc for doc, _ in library.catalog_sources(root)]


def find_document(document_id: str, root: Path = ROOT) -> dict:
    for doc in catalog(root):
        if doc["id"] == document_id:
            return doc
    raise ValueError(f"unknown catalog document id: {document_id!r}")


def project_instance_id(root: Path, doc: dict) -> str:
    slug = re.sub(r"[^A-Z0-9]+", "-", root.name.upper()).strip("-") or "PROJECT"
    return f"INST-{slug}-{doc['id']}"


FRONTMATTER_ID = re.compile(r'^id:\s*["\']?([^"\'\s]+)', re.MULTILINE)


def existing_instances(root: Path) -> dict[str, Path]:
    """Map instance IDs already declared under docs/ to their files."""
    found = {}
    docs = root / 'docs'
    if not docs.is_dir():
        return found
    for path in docs.rglob('*.md'):
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        if not text.startswith('---'):
            continue
        end = text.find('\n---', 3)
        if end == -1:
            continue
        match = FRONTMATTER_ID.search(text[:end])
        if match:
            found.setdefault(match.group(1), path)
    return found


def default_target(root: Path, doc: dict) -> Path:
    return root / "docs" / "autodoc" / library.destination(doc)


def resolve_target(root: Path, doc: dict, output: Path | None) -> Path:
    target = (root / output).resolve() if output and not output.is_absolute() else \
        (output.resolve() if output else default_target(root, doc).resolve())
    try:
        target.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"output must stay inside the project root: {target}") from error
    return target


def add(
    document_id: str,
    *,
    root: Path = ROOT,
    output: Path | None = None,
    variant: str = "canonical",
    instance_id: str | None = None,
    force: bool = False,
    write: bool = False,
    today: date | None = None,
) -> dict:
    root = root.expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"project root is not a directory: {root}")
    if variant not in library.VARIANTS:
        raise ValueError(f"variant must be one of {', '.join(library.VARIANTS)}")
    doc = find_document(document_id)
    target = resolve_target(root, doc, output)
    instance = instance_id or project_instance_id(root, doc)
    existing = existing_instances(root).get(instance)
    if existing and existing.resolve() != target:
        raise ValueError(
            f"instance id {instance} is already used by "
            f"{existing.relative_to(root).as_posix()}; choose --instance for a distinct id")
    exists = target.exists()
    if exists and not force:
        raise FileExistsError(f"refusing to overwrite existing document: {target}")
    content = library.render_instance(
        doc, variant, instance_id=instance, today=today)
    result = {
        "command": "add",
        "repo": str(root),
        "id": doc["id"],
        "name": doc["name"],
        "type": doc["type"],
        "variant": variant,
        "target": str(target),
        "relative_target": target.relative_to(root).as_posix(),
        "exists": exists,
        "overwritten": bool(exists and force),
        "written": False,
        "content": content,
    }
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        mode = "w" if force else "x"
        with target.open(mode, encoding="utf-8", newline="\n") as handle:
            handle.write(content)
        result["written"] = True
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", help="catalog type id, for example DOC-A03-001")
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="project receiving the document (default: current directory)")
    parser.add_argument("--output", type=Path,
                        help="exact destination file, relative to --root unless absolute")
    parser.add_argument("--variant", choices=library.VARIANTS, default="canonical",
                        help="template variant to instantiate (default: canonical)")
    parser.add_argument("--instance", dest="instance_id",
                        help="frontmatter instance id (default: INST-<PROJECT>-<CATALOG-ID>)")
    parser.add_argument("--write", action="store_true", help="write the file instead of previewing")
    parser.add_argument("--force", action="store_true", help="allow replacing an existing file")
    parser.add_argument("--json", action="store_true", help="print a machine-readable result")
    args = parser.parse_args(argv)
    try:
        result = add(args.document, root=args.root, output=args.output, variant=args.variant,
                     instance_id=args.instance_id, force=args.force, write=args.write)
    except FileExistsError as error:
        print(f"Add failed: {error}; pass --force to replace it", file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Add failed: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["written"]:
        print(f"Created {result['relative_target']}")
        print("Next: replace the placeholder owner, reviewer and sections; then add the catalog id "
              "to autodoc.toml [instantiated] if this is the project's controlling document.",
              file=sys.stderr)
    else:
        print(f"# Preview for {result['relative_target']}", file=sys.stderr)
        print("Preview only; pass --write to create the file.", file=sys.stderr)
        print(result["content"], end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
