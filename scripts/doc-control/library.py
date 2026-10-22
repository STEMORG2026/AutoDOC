#!/usr/bin/env python3
"""Render catalog template variants on demand from the catalog's single source per type.

``CATALOG-A/B/INDEX.yaml`` define each document type. Canonical, blank and synthetic-example
Markdown files are derived output only and default to the ignored ``build/TEMPLATES/`` tree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path, PurePosixPath
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
VARIANTS = ("canonical", "blank", "example")
VARIANT_SUFFIX = {"canonical": "", "blank": ".blank", "example": ".example"}
TEMPLATE_DIR = PurePosixPath("TEMPLATES")


def render(
    doc: dict,
    variant: str,
    *,
    instance: str | None = None,
    today: date | None = None,
) -> str:
    """Render one deterministic Markdown variant from one catalog document record.

    ``instance`` and ``today`` let the authoring path produce a real declaration without changing
    the template previews: the defaults keep the original sample values, while ``add`` supplies a
    project-qualified id and the creation date.
    """
    if variant not in VARIANTS:
        raise ValueError(f"unknown template variant: {variant!r}")
    if not isinstance(doc, dict):
        raise ValueError("catalog template source must be a document record")
    name, id_, document_type = doc.get("name"), doc.get("id"), doc.get("type")
    if not isinstance(id_, str) or not re.fullmatch(r"(DOC|DEV)-[AB][0-9]{2}-[0-9]{3}", id_):
        raise ValueError(f"invalid catalog document id: {id_!r}")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"{id_}: catalog document name must be a non-empty string")
    if not isinstance(document_type, str) or not document_type.strip():
        raise ValueError(f"{id_}: catalog document type must be a non-empty string")
    instance = instance or (
        f"SAMPLE-{id_}" if variant == "example" else "REPLACE-WITH-UNIQUE-INSTANCE-ID")
    effective = today or date(2026, 9, 26)
    review = effective + timedelta(days=90)
    header = (
        f'---\nid: {instance}\ntitle: "{name}"\ntype: {doc["type"]}\n'
        'owner: "@assign-owner"\nreviewer: "@assign-reviewer"\nclassification: internal\n'
        f'status: draft\nversion: "0.1"\neffective_date: {effective.isoformat()}\n'
        f'next_review: {review.isoformat()}\nsource_of_truth: human\nsupersedes: null\n'
        'related: []\ncriticality: high\nreview_days: 90\nlast_verified: 1970-01-01\n'
        f'last_reviewed: 1970-01-01\nlast_updated: {effective.isoformat()}\nauto_generated: false\n---\n\n'
    )
    if variant == "example":
        body = (
            f'> Synthetic illustration of **{name}** (`{id_}`); not an approved project document '
            'or proof of any control. Dates above are sample values.\n\n'
            f'## Purpose and scope\n\nA sample team uses this {name.lower()} to define the boundary '
            'of a fictional service. Real scope, owner and audience must be confirmed.\n\n'
            '## Details and decisions\n\nThe sample team records assumptions, accountable decisions '
            'and alternatives here. It does not claim any service is deployed or audited.\n\n'
            '## Verification and references\n\nThe sample team would link its primary implementation '
            'or review record here and record the verification date. No evidence is supplied.\n'
        )
    elif variant == "blank":
        body = (
            f'> Blank instance for {name} (`{id_}`). Replace metadata including dates; '
            'the sample date is **not** verification.\n\n'
            '## Purpose and scope\n\n<!-- Fill in. -->\n\n## Details and decisions\n\n'
            '<!-- Fill in. -->\n\n## Verification and references\n\n<!-- Link evidence. -->\n'
        )
    else:
        body = (
            f'> Canonical structure for **{name}** (`{id_}`; {doc["type"]}). '
            'Choose an owner and unique instance ID before use.\n\n'
            f'## Purpose and scope\n\nState why {name.lower()} applies, who uses it and what is out of scope.\n\n'
            f'## Details and decisions\n\nDescribe the project-specific {name.lower()} facts, '
            'assumptions, alternatives, failure modes and responsible people.\n\n'
            '## Verification and references\n\nLink the authoritative code, policy, test or human '
            'approval; explain how to check the claims and when they must be reviewed.\n'
        )
    return header + f"# {name}\n\n" + body


def render_instance(
    doc: dict,
    variant: str = "canonical",
    *,
    instance_id: str | None = None,
    today: date | None = None,
) -> str:
    """Render a document intended for a project, using a real id and creation date."""
    if instance_id is not None:
        instance_id = instance_id.strip()
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", instance_id):
            raise ValueError(
                "instance id must start with a letter or digit and contain only "
                "letters, digits, dots, underscores or hyphens")
    return render(doc, variant, instance=instance_id, today=today or date.today())


def destination(doc: dict) -> Path:
    """The validated category-relative destination of one catalog document."""
    return _destination(doc)


def _destination(doc: dict) -> Path:
    """Return the category-relative build path after validating the catalog's logical target."""
    document_id = doc.get("id")
    raw = doc.get("template")
    if not isinstance(document_id, str) or not re.fullmatch(r"(DOC|DEV)-[AB][0-9]{2}-[0-9]{3}", document_id):
        raise ValueError(f"invalid catalog document id: {document_id!r}")
    if not isinstance(raw, str) or "\\" in raw:
        raise ValueError(f"{document_id}: template render destination must use a relative POSIX path")
    relative = PurePosixPath(raw)
    if (relative.is_absolute() or ".." in relative.parts or "." in relative.parts or
            raw != relative.as_posix() or len(relative.parts) != 3 or
            relative.parts[0] != TEMPLATE_DIR.as_posix() or
            not re.fullmatch(r"[A-Z-]+", relative.parts[1]) or
            relative.name != f"{document_id}.md"):
        raise ValueError(
            f"{document_id}: expected a logical destination TEMPLATES/<category>/{document_id}.md, "
            f"found {raw!r}"
        )
    return Path(*relative.parts[1:])


def catalog_sources(root: Path = ROOT) -> list[tuple[dict, Path]]:
    """Load unique catalog entries and their validated category-relative destinations."""
    entries: list[tuple[dict, Path]] = []
    seen_ids: set[str] = set()
    seen_paths: set[Path] = set()
    for catalog in ("CATALOG-A", "CATALOG-B"):
        index_path = root / catalog / "INDEX.yaml"
        data = json.loads(index_path.read_text(encoding="utf-8"))
        if data.get("version") != 1:
            raise ValueError(f"unsupported catalog version in {index_path.relative_to(root)}")
        for domain in data.get("domains", []):
            for doc in domain.get("documents", []):
                document_id = doc.get("id")
                if document_id in seen_ids:
                    raise ValueError(f"duplicate catalog ID: {document_id}")
                seen_ids.add(document_id)
                destination = _destination(doc)
                if destination in seen_paths:
                    raise ValueError(f"duplicate template render destination: {destination}")
                seen_paths.add(destination)
                # Exercise every renderer while the input record is still in hand; a broken
                # catalog entry fails before any output is written.
                for variant in VARIANTS:
                    if not render(doc, variant):
                        raise ValueError(f"{document_id}: {variant} renderer returned empty output")
                entries.append((doc, destination))
    if not entries:
        raise ValueError("catalogs contain no template sources")
    return entries


def _inside(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def checked_in_outputs(root: Path = ROOT) -> list[Path]:
    """Return rendered variants found under the source tree; explanatory README files are allowed."""
    template_root = root / "TEMPLATES"
    if not template_root.is_dir():
        return []
    return sorted(
        path for path in template_root.rglob("*")
        if path.is_file() and path.name != "README.md" and
        path.name.endswith((".md", ".md.blank", ".md.example"))
    )


def run(
    check: bool = False,
    variant: str = "all",
    output_dir: Path | None = None,
    *,
    root: Path = ROOT,
) -> bool:
    """Validate catalog sources or render selected variants into an output tree."""
    if variant not in (*VARIANTS, "all"):
        raise ValueError(f"variant must be one of {', '.join((*VARIANTS, 'all'))}")
    entries = catalog_sources(root)
    if check:
        committed = checked_in_outputs(root)
        if committed:
            print("Generated template variants must not be committed; found:", file=sys.stderr)
            for path in committed[:20]:
                print(" ", path.relative_to(root), file=sys.stderr)
            if len(committed) > 20:
                print(f"  ... and {len(committed) - 20} more", file=sys.stderr)
            return False
        print(
            f"Catalog template sources valid: {len(entries)} types; canonical, blank and example "
            "variants render on demand."
        )
        return True

    selected = VARIANTS if variant == "all" else (variant,)
    destination_root = (output_dir or root / "build" / "TEMPLATES").expanduser().resolve()
    source_root = (root / "TEMPLATES").resolve()
    if _inside(destination_root, source_root):
        raise ValueError("template outputs may not be written inside the TEMPLATES source directory")

    prepared: list[tuple[Path, str]] = []
    seen_targets: set[Path] = set()
    for doc, relative in entries:
        for selected_variant in selected:
            suffix = VARIANT_SUFFIX[selected_variant]
            target = (destination_root / Path(str(relative) + suffix)).resolve()
            if not _inside(target, destination_root):
                raise ValueError(f"template output escapes its output directory: {target}")
            if target in seen_targets:
                raise ValueError(f"duplicate template output path: {target}")
            seen_targets.add(target)
            prepared.append((target, render(doc, selected_variant)))

    for target, content in prepared:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    rendered = ", ".join(selected)
    print(f"Rendered {len(prepared)} {rendered} template file(s) for {len(entries)} catalog types to {destination_root}")
    return True


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="validate catalog render sources and reject committed generated variants; do not write files",
    )
    parser.add_argument(
        "--variant", choices=(*VARIANTS, "all"), default="all",
        help="variant to render (default: all three)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / "build" / "TEMPLATES",
        help="output tree root (default: <tool-root>/build/TEMPLATES)",
    )
    args = parser.parse_args(argv)
    try:
        return 0 if run(args.check, args.variant, args.output_dir) else 1
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Template rendering failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
