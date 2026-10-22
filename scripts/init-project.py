#!/usr/bin/env python3
"""Scaffold a small, explicit starter set of controlled docs in an existing project directory."""
import argparse
import importlib.util
import json
import re
import tomllib
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOUNDATION = ['Problem statement', 'Goals and non goals', 'Scope', 'Success metrics',
              'System overview', 'ADR', 'Test strategy', 'Local setup', 'Current state', 'Next action']


def load_module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'cannot load module from {relative}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def declaration_values(phase, profile):
    model = json.loads((ROOT / 'CONTROL/metadata/CONTEXT-MODEL.json').read_text())
    profiles = json.loads((ROOT / 'CONTROL/metadata/PROFILES.json').read_text())
    phases = [entry['id'] for entry in model['phases']]
    profile_ids = [entry['id'] for entry in profiles['profiles']]
    if phase and phase not in phases:
        raise ValueError(f'unknown phase {phase!r}; choose one of {", ".join(phases)}')
    if profile and profile not in profile_ids:
        raise ValueError(f'unknown profile {profile!r}; choose one of {", ".join(profile_ids)}')
    return phases, profile_ids


def write_context(target, phase, profile):
    if not phase and not profile:
        return None
    path = target / 'autodoc.toml'
    if path.exists():
        print('Skipped existing', path)
        return path
    lines = ['# AutoDOC declared context. Phase and profile are declarations, never inferences.',
             'schema = 1', '']
    if phase:
        lines += [f'phase = "{phase}"',
                  f'phase_declared = "{date.today().isoformat()}"',
                  '# Change the declaration deliberately with `autodoc promote`.']
    if profile:
        lines.append(f'profile = "{profile}"')
    content = '\n'.join(lines) + '\n'
    context = load_module('autodoc_context', 'scripts/intelligence/context.py')
    problems = context.validate(context.normalise(tomllib.loads(content)))
    if problems:
        raise ValueError('; '.join(problems))
    path.write_text(content, encoding='utf-8')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--name', required=True, help='Project name (not the AutoDOC repository name)')
    parser.add_argument('--type', default='generic', choices=['generic', 'web-api', 'cli', 'library', 'ai-agent'])
    parser.add_argument('--output', required=True, type=Path, help='Existing project directory')
    parser.add_argument('--phase', help='Declare the initial phase in autodoc.toml')
    parser.add_argument('--profile', help='Declare the catalog profile in autodoc.toml')
    args = parser.parse_args()
    if not args.output.is_dir():
        parser.error('--output must be an existing directory (never scaffolds over a missing path)')
    try:
        declaration_values(args.phase, args.profile)
    except ValueError as error:
        parser.error(str(error))
    context_path = write_context(args.output, args.phase, args.profile)
    if context_path:
        print('Created', context_path)
    catalog = json.loads((ROOT / 'CATALOG-B/INDEX.yaml').read_text())
    docs = [d for domain in catalog['domains'] for d in domain['documents']]
    chosen = [next(d for d in docs if d['name'] == name) for name in FOUNDATION]
    target = args.output / 'docs' / 'autodoc'
    slug = re.sub(r'[^A-Z0-9]+', '-', args.name.upper()).strip('-') or 'PROJECT'
    today = date.today()
    for doc in chosen:
        name = doc['name'].lower().replace(' ', '-')
        path = target / (name + '.md')
        if path.exists():
            print('Skipped existing', path)
            continue
        content = (f'---\nid: INST-{slug}-{doc["id"]}\ntitle: "{args.name}: {doc["name"]}"\n'
                   f'type: {doc["type"]}\nowner: "@assign-owner"\nreviewer: "@assign-reviewer"\n'
                   f'classification: internal\nstatus: draft\nversion: "0.1"\n'
                   f'effective_date: {today}\nnext_review: {today + timedelta(days=90)}\n'
                   f'source_of_truth: human\nsupersedes: null\nrelated: []\ncriticality: high\n'
                   f'review_days: 90\nlast_verified: 1970-01-01\nlast_reviewed: 1970-01-01\nlast_updated: {today}\n'
                   f'auto_generated: false\n---\n\n'
                   f'# {doc["name"]}\n\n> Draft scaffold for {args.name} ({args.type}). '
                   'Replace owner, reviewer and content; dates are creation dates, not proof of verification.\n\n'
                   '## Purpose and scope\n\n<!-- Describe applicability. -->\n\n'
                   '## Details and decisions\n\n<!-- Add project facts and reasoning. -->\n\n'
                   '## Verification and references\n\n<!-- Link primary sources. -->\n')
        target.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print('Created', path)
    print('Next: assign owners, replace placeholders, select other applicable catalog entries and configure a sync map.')


if __name__ == '__main__':
    main()
