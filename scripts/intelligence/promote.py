#!/usr/bin/env python3
"""Preview or apply a declared phase promotion, with the enforcement delta it causes.

A promotion is an explicit owner event, never an inference. The command validates the current
context, evaluates the same catalog under the current and target phases, and writes only the
top-level `phase` and `phase_declared` values, preserving the rest of the file byte-for-byte.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
import tomllib
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECOMMEND = ROOT / "scripts/intelligence/recommend.py"
ALLOWED_KEYS = {"phase", "phase_declared"}
SCALAR_LINE = re.compile(
    r'^(?P<prefix>[ \t]*(?P<key>[A-Za-z0-9_-]+)[ \t]*=[ \t]*)'
    r'(?P<value>"(?:[^"\\]|\\.)*"|\'[^\']*\')(?P<suffix>[ \t]*(?:#.*)?)(?P<newline>\r?\n)?$'
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


recommend = load_module("autodoc_recommend_for_promote", RECOMMEND)
context_module = recommend.context_module


def phase_order() -> tuple[str, ...]:
    return tuple(phase["id"] for phase in recommend.MODEL["phases"])


def _top_level(lines: list[str]) -> list[bool]:
    result: list[bool] = []
    in_table = False
    for line in lines:
        if line.lstrip().startswith("["):
            in_table = True
        result.append(not in_table)
    return result


def _find_scalar(lines: list[str], key: str) -> tuple[int, re.Match[str]] | None:
    matches = []
    top_level = _top_level(lines)
    for index, line in enumerate(lines):
        if not top_level[index]:
            continue
        match = SCALAR_LINE.match(line)
        if match and match.group("key") == key:
            matches.append((index, match))
    if len(matches) > 1:
        raise ValueError(f"autodoc.toml defines {key} more than once at top level")
    return matches[0] if matches else None


def _newline_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def _set_scalar(text: str, key: str, value: str) -> str:
    lines = text.splitlines(keepends=True)
    found = _find_scalar(lines, key)
    newline = _newline_for(text)
    if found:
        index, match = found
        lines[index] = (match.group("prefix") + f'"{value}"' + match.group("suffix")
                        + (match.group("newline") or newline))
        return "".join(lines)

    insertion = f'{key} = "{value}"{newline}'
    anchor = 0
    if key == "phase_declared":
        phase = _find_scalar(lines, "phase")
        if phase:
            anchor = phase[0] + 1
    if anchor == 0:
        top_level = _top_level(lines)
        for index, line in enumerate(lines):
            if top_level[index] and re.match(r"^[ \t]*schema[ \t]*=", line):
                anchor = index + 1
                break
    lines.insert(anchor, insertion)
    return "".join(lines)


def _validate_text(text: str, context_module) -> dict:
    raw = tomllib.loads(text)
    context = context_module.normalise(raw)
    problems = context_module.validate(context)
    if problems:
        raise ValueError("; ".join(problems))
    return context


def _unchanged_outside_allowed(before: dict, after: dict) -> None:
    def rest(document: dict) -> dict:
        return {key: value for key, value in document.items() if key not in ALLOWED_KEYS}

    if rest(before) != rest(after):
        raise ValueError("the promotion edit would change more than phase and phase_declared")


def rewrite_context(text: str, phase: str, declared: str) -> str:
    updated = _set_scalar(text, "phase", phase)
    updated = _set_scalar(updated, "phase_declared", declared)
    _unchanged_outside_allowed(tomllib.loads(text), tomllib.loads(updated))
    _validate_text(updated, context_module)
    return updated


def write_atomic(path: Path, text: str) -> None:
    mode = path.stat().st_mode
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def _snapshot(documents: list[dict], profile_document: dict, context: dict, phase: str) -> dict:
    candidate = {**context, "phase": phase}
    enforcement = context_module.enforcement(phase)
    placement = recommend.profile_placement(documents, candidate)
    groups = recommend.evaluate(documents, profile_document, candidate, enforcement, placement)
    required = [item for item in groups["required"] if item["severity_effective"] != "off"]
    failing = [item for item in required if item["severity_effective"] == "error"]
    return {"enforcement": enforcement, "groups": groups, "required": required, "failing": failing}


def _items(items: list[dict]) -> list[dict]:
    return [{"id": item["id"], "name": item["name"], "severity": item["severity_effective"]}
            for item in sorted(items, key=lambda item: item["id"])]


def _difference(after: list[dict], before: list[dict]) -> list[dict]:
    previous = {item["id"] for item in before}
    return _items([item for item in after if item["id"] not in previous])


def build_delta(before: dict, after: dict) -> dict:
    newly_required = _difference(after["required"], before["required"])
    no_longer_required = _difference(before["required"], after["required"])
    newly_failing = _difference(after["failing"], before["failing"])
    no_longer_failing = _difference(before["failing"], after["failing"])
    return {
        "newly_required": newly_required,
        "no_longer_required": no_longer_required,
        "newly_failing": newly_failing,
        "no_longer_failing": no_longer_failing,
        "required_missing": _items(after["required"]),
        "blocked": bool(after["enforcement"]["fail"] and after["required"]),
    }


def promote(
    *,
    repo: Path,
    config: Path,
    target: str,
    declared: str,
    write: bool = False,
    force: bool = False,
) -> tuple[int, dict]:
    repo = repo.expanduser().resolve()
    config = config.expanduser().resolve()
    if not repo.is_dir():
        raise ValueError(f"repository is not a directory: {repo}")
    if not config.is_file():
        raise ValueError(f"context file does not exist: {config}")
    phases = phase_order()
    if target not in phases:
        raise ValueError(f"unknown phase {target!r}; choose one of {', '.join(phases)}")
    try:
        declared_date = date.fromisoformat(declared)
    except ValueError as error:
        raise ValueError(f"declared date must be YYYY-MM-DD: {declared!r}") from error
    if declared_date > date.today():
        raise ValueError(f"declared date is in the future: {declared}")

    text = config.read_text(encoding="utf-8")
    context = _validate_text(text, context_module)
    current = context["phase"]
    current_label = context_module.enforcement(current)["label"]
    target_label = context_module.enforcement(target)["label"]
    same = current == target
    if current in phases and not same and phases.index(target) < phases.index(current) and not force:
        raise ValueError(
            f"refusing to demote {current} -> {target} without --force; promotion moves forward only")
    previous_date = context.get("phase_declared")
    if previous_date and not same and declared < previous_date and not force:
        raise ValueError(
            f"refusing to backdate the declaration from {previous_date} to {declared} without --force")

    documents = recommend.catalog()
    profile_document = recommend.profiler.profile(repo, context["facts"])
    before = _snapshot(documents, profile_document, context, current) if current in phases else None
    after = _snapshot(documents, profile_document, context, target)
    if before is None:
        delta = {
            "newly_required": _items(after["required"]),
            "no_longer_required": [],
            "newly_failing": _items(after["failing"]),
            "no_longer_failing": [],
            "required_missing": _items(after["required"]),
            "blocked": bool(after["enforcement"]["fail"] and after["required"]),
        }
    else:
        delta = build_delta(before, after)

    result = {
        "command": "promote",
        "repo": str(repo),
        "config": str(config),
        "from": {"phase": current, "enforcement": current_label,
                 "declared": context.get("phase_declared")},
        "to": {"phase": target, "enforcement": target_label, "declared": declared},
        "changed": not same,
        "write": bool(write),
        "force": bool(force),
        "written": False,
        "delta": delta,
    }
    if same:
        result["written"] = False
        return 0, result
    if delta["blocked"] and not force:
        return 1, result

    if write:
        updated = rewrite_context(text, target, declared)
        write_atomic(config, updated)
        check = _validate_text(config.read_text(encoding="utf-8"), context_module)
        if check["phase"] != target or check["phase_declared"] != declared:
            raise ValueError("the written context did not read back with the promoted values")
        result["written"] = True
    return (1 if delta["blocked"] else 0), result


def render(result: dict) -> str:
    source = result["from"]["enforcement"]
    target = result["to"]
    lines = [f"Promotion: {source} -> {target['enforcement']}, declared {target['declared']}"]
    if not result["changed"]:
        lines.append("No change: the project already declares this phase.")
        return "\n".join(lines) + "\n"
    delta = result["delta"]
    for key, label in (("newly_required", "Newly required"),
                       ("newly_failing", "Newly failing"),
                       ("no_longer_required", "No longer required"),
                       ("no_longer_failing", "No longer failing")):
        items = delta[key]
        if items:
            lines.append(f"{label}:")
            lines.extend(f"  + {item['id']} {item['name']} ({item['severity']})"
                         if key.startswith("newly") else
                         f"  - {item['id']} {item['name']} ({item['severity']})"
                         for item in items)
    if not any(delta[key] for key in ("newly_required", "newly_failing",
                                      "no_longer_required", "no_longer_failing")):
        lines.append("Delta: no catalog requirement changes.")
    if delta["blocked"]:
        lines.append(f"Blocked: {len(delta['required_missing'])} required document(s) have no "
                     "document and no recorded decision at the target phase.")
        lines.extend(f"  ! {item['id']} {item['name']}" for item in delta["required_missing"])
        if not result["force"]:
            lines.append("Nothing was written. Add the documents or record decisions, or pass "
                         "--force to write the declaration anyway.")
        elif not result["written"]:
            lines.append("Preview only. --force permits the write; add --write to apply it.")
    if result["written"]:
        lines.append(f"Updated {result['config']}.")
        lines.append("Next: run the repository gate and commit autodoc.toml with the documents "
                     "that justify the promotion.")
    elif not (delta["blocked"] and not result["force"]):
        lines.append("Preview only. Pass --write to update autodoc.toml.")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(),
                        help="repository whose facts are evaluated (default: current directory)")
    parser.add_argument("--config", type=Path,
                        help="context TOML (default: <repo>/autodoc.toml)")
    parser.add_argument("--to", required=True, help="target phase id")
    parser.add_argument("--date", default=date.today().isoformat(),
                        help="declaration date in YYYY-MM-DD (default: today)")
    parser.add_argument("--write", action="store_true", help="apply the promotion instead of previewing")
    parser.add_argument("--force", action="store_true",
                        help="allow a demotion, backdate or write while required documents are missing")
    parser.add_argument("--json", action="store_true", help="print a machine-readable result")
    args = parser.parse_args(argv)
    config = args.config or (args.repo / "autodoc.toml")
    try:
        code, result = promote(repo=args.repo, config=config, target=args.to,
                               declared=args.date, write=args.write, force=args.force)
    except (OSError, ValueError, KeyError, TypeError, tomllib.TOMLDecodeError) as error:
        print(f"Promotion failed: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(render(result), end="")
    if result["delta"]["blocked"] and not result["written"]:
        print("Promotion blocked before writing.", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
