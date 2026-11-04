#!/usr/bin/env python3
"""Plan a phase-scaled adoption, and optionally record an adoption baseline.

The default run is read-only. It keeps the original bounded filename heuristic, then resolves the
catalog against the project's declared context (or a preview phase/profile supplied on the command
line) through the same `context` -> `recommend` -> `enforce` layers as `check`. That makes the plan
answer the questions an adopter actually has:

* which catalog types the declared phase and profile require, and which already exist under the
  default `docs/autodoc/` path but are not registered;
* which types are still undetermined because the owner has not declared an audience, kind or
  sensitive-data fact;
* how the required set grows from `idea` through `mature` (and shrinks to the sunset set);
* what event model the adopter's repository should wire, and what remains a human decision.

`--phase` and `--profile` preview values; they never edit `autodoc.toml`. `--write-baseline` is the
only write: it records the findings observed during adoption with `enforce.write_baseline`, so
enforcement can start from the current state and ratchet down. Configuration findings and
`secrets.inline` are never recorded.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTELLIGENCE = ROOT / 'scripts' / 'intelligence'
SCHEMA = 1
MAX_RENDERED = 20

# Adoption hints should be fast and should not crawl virtual environments, package caches or
# build outputs. These exclusions affect only this read-only heuristic scan.
SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', '.venv', 'venv', 'env', 'node_modules',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.tox', '.nox',
    '.next', '.nuxt', '.turbo', '.cache', 'build', 'dist', 'target',
})

RULES = [
    ('API contracts', ('openapi.yaml', 'routes.json', 'package.json'), 'A08-APIS'),
    ('Data', ('schema.sql', 'schema.prisma', 'models.py'), 'A05-DATA'),
    ('Build and supply chain', ('pyproject.toml', 'package-lock.json', 'Cargo.toml', 'go.mod'), 'A10-BUILD'),
    ('AI/ML', ('model.py', 'prompts', 'evals'), 'A21-AI-ML'),
    ('Deployment', ('Dockerfile', 'terraform', 'k8s'), 'A15-RELEASE'),
]

CI_PATTERNS = (
    '.github/workflows/*.yml', '.github/workflows/*.yaml', '.gitlab-ci.yml',
    '.circleci/config.yml', 'azure-pipelines.yml', 'Jenkinsfile',
)


def scan(project):
    # Search only within the selected directory; no writes, imports or code execution. Prune
    # common dependency/build caches before descent so an adoption hint stays bounded in practice.
    names = set()
    for directory, subdirectories, filenames in os.walk(project, followlinks=False):
        subdirectories[:] = [name for name in subdirectories if name not in SKIP_DIRS]
        names.update(subdirectories)
        names.update(filenames)
    return [(name, domain, [signal for signal in signals if signal in names])
            for name, signals, domain in RULES if any(signal in names for signal in signals)]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f'cannot load {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


context_module = _load('autodoc_adopt_context', INTELLIGENCE / 'context.py')
recommend = _load('autodoc_adopt_recommend', INTELLIGENCE / 'recommend.py')
enforce = _load('autodoc_adopt_enforce', INTELLIGENCE / 'enforce.py')
add_document = _load('autodoc_adopt_add_document', ROOT / 'scripts' / 'add-document.py')


def _resolve(project: Path, value: Path | None, default: Path) -> Path:
    """Resolve an option path against the project, so ``--config`` means the same as ``--repo``."""
    if value is None:
        return default
    value = value.expanduser()
    return (project / value if not value.is_absolute() else value).resolve()


def _target(document: dict) -> str:
    return (Path('docs') / 'autodoc' / add_document.library.destination(document)).as_posix()


def _status(project: Path, target: str) -> str:
    return 'unregistered' if (project / target).is_file() else 'missing'


def _requirement(project: Path, item: dict, documents: dict) -> dict:
    target = _target(documents[item['id']])
    return {
        'id': item['id'], 'name': item['name'], 'domain': item.get('domain'),
        'tier': item.get('effective_tier') or item.get('tier'),
        'phase_min': item.get('phase_min'),
        'severity': item.get('severity_effective'),
        'target': target, 'status': _status(project, target),
        'because': item.get('because'),
    }


def _undetermined(project: Path, item: dict, documents: dict) -> dict:
    target = _target(documents[item['id']])
    return {
        'id': item['id'], 'name': item['name'], 'domain': item.get('domain'),
        'target': target, 'status': _status(project, target),
        'unknown': sorted(token for token, state in item['tokens'].items() if state == 'unknown'),
    }


def _phase_ladder(documents, profile_document, context, placement, phases) -> list[dict]:
    """Count what each phase would require under the same declarations.

    The ladder is a preview, not a declaration: it uses the planned phase only as the starting
    point and changes one phase at a time, so an adopter can see where the next documents land.
    """
    ladder = []
    for phase in phases:
        trial = {**context, 'phase': phase}
        enforcement = context_module.enforcement(phase)
        groups = recommend.evaluate(documents, profile_document, trial, enforcement, placement)
        required = [item for item in groups['required']
                    if item['severity_effective'] != 'off']
        recommended = [item for item in groups['recommended']
                       if item['severity_effective'] != 'off']
        ladder.append({
            'phase': phase,
            'label': enforcement['label'],
            'open_required': len(required),
            'recommended': len(recommended),
            'undetermined': len(groups['undetermined']),
            'off': len(groups['off']),
            'required_ids': [item['id'] for item in required],
        })
    return ladder


def _unknown_count(groups, prefix: str) -> int:
    return sum(1 for item in groups['undetermined']
               if any(token.startswith(prefix) and state == 'unknown'
                      for token, state in item['tokens'].items()))


def _declaration_gaps(context: dict, groups: dict) -> list[dict]:
    """Name the declarations that would replace `undetermined` with a real answer."""
    gaps = []
    if not context.get('audience'):
        affected = _unknown_count(groups, recommend.AUDIENCE_PREFIX)
        if affected:
            gaps.append({
                'declaration': 'audience', 'declared': [],
                'affected': affected,
                'fix': 'declare audience = [...] in autodoc.toml; an empty audience leaves '
                       'reader-gated types undetermined',
            })
    if not context.get('kinds'):
        affected = _unknown_count(groups, 'kind:')
        if affected:
            gaps.append({
                'declaration': 'kinds', 'declared': [],
                'affected': affected,
                'fix': 'declare kinds = [...] in autodoc.toml; kinds are declared, never inferred',
            })
    facts: dict[str, set[str]] = {}
    for item in groups['undetermined']:
        for token, state in item['tokens'].items():
            if state != 'unknown' or token in recommend.SENTINELS:
                continue
            if token.startswith(recommend.PREFIXES + (recommend.AUDIENCE_PREFIX,
                                                       recommend.PHASE_PREFIX)):
                continue
            facts.setdefault(token, set()).add(item['id'])
    for token, ids in sorted(facts.items()):
        declared = context['facts'].get(token)
        gaps.append({
            'declaration': token, 'declared': declared, 'affected': len(ids),
            'fix': f'declare [facts] {token} with a value and a reason, or record a decision '
                   'for the affected documents',
        })
    return gaps


def _ci_files(project: Path) -> list[str]:
    found = set()
    for pattern in CI_PATTERNS:
        for path in project.glob(pattern):
            if path.is_file():
                found.add(path.relative_to(project).as_posix())
    return sorted(found)


def _trigger_model(project: Path) -> dict:
    """The event model to copy into the adopter's repository; AutoDOC does not install it."""
    return {
        'installed': False,
        'detected_files': _ci_files(project),
        'note': ('AutoDOC does not install CI, hooks or branch protection. This is the event model '
                 'from CONTROL/metadata/TRIGGERS.json: the pull request is the only gate, the '
                 'local hook is bypassable convenience, and network checks are scheduled triage.'),
        'events': [
            {
                'id': 'local', 'label': 'Before a push', 'posture': 'convenience',
                'blocking': False, 'network': False,
                'runs': ['autodoc check --repo .'], 'bypass': 'git push --no-verify',
            },
            {
                'id': 'pull_request', 'label': 'On every pull request', 'posture': 'gate',
                'blocking': True, 'network': False,
                'runs': ['autodoc check --repo .'], 'required_check': 'AutoDOC check',
            },
            {
                'id': 'schedule', 'label': 'Scheduled triage', 'posture': 'triage',
                'blocking': False, 'network': True,
                'runs': ['autodoc check --repo .', 'external link check (optional, warn-only)'],
                'note': 'External-link checks may use the network, are scheduled and warn-only, '
                        'and are never a required check.',
            },
        ],
    }


def _build_errors(problems: list[str], project: Path, heuristics, config_path: Path) -> dict:
    return {
        'command': 'adopt', 'schema': SCHEMA, 'project': str(project),
        'config': str(config_path) if config_path.is_file() else None,
        'heuristics': [{'name': name, 'domain': domain, 'matches': matches}
                       for name, domain, matches in heuristics],
        'errors': problems, 'exit_code': 2,
    }


def build_plan(project: Path, config: Path | None = None, phase: str | None = None,
               profile: str | None = None, baseline: Path | None = None,
               write_baseline: bool = False) -> dict:
    """Build the read-only plan, writing only the optional baseline."""
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f'project root is not a directory: {project}')
    heuristics = scan(project)
    config_path = _resolve(project, config, project / 'autodoc.toml')
    context = context_module.normalise(context_module.load(config_path))
    declared_phase, declared_profile = context['phase'], context['profile']

    model = context_module.load_model()
    phases = [entry['id'] for entry in model['phases']]
    if phase is not None and phase not in phases:
        raise ValueError(f'unknown phase {phase!r}; choose one of {", ".join(phases)}')
    profile_ids = context_module.profile_ids()
    if profile is not None and profile not in profile_ids:
        raise ValueError(f'unknown profile {profile!r}; choose one of {", ".join(profile_ids)}')

    planned_phase = phase if phase is not None else declared_phase
    planned_profile = profile if profile is not None else declared_profile
    planned_context = {**context, 'phase': planned_phase, 'profile': planned_profile}
    problems = context_module.validate_model() + context_module.validate(planned_context)
    if problems:
        return _build_errors(problems, project, heuristics, config_path)

    profile_document = recommend.profiler.profile(project, planned_context['facts'])
    documents = recommend.catalog()
    by_id = {document['id']: document for document in documents}
    enforcement = context_module.enforcement(planned_phase)
    placement = recommend.profile_placement(documents, planned_context)
    groups = recommend.evaluate(documents, profile_document, planned_context, enforcement, placement)

    required = [_requirement(project, item, by_id) for item in groups['required']
                if item['severity_effective'] != 'off']
    recommended = [_requirement(project, item, by_id) for item in groups['recommended']
                   if item['severity_effective'] != 'off']
    advisory = [_requirement(project, item, by_id) for item in groups['reported']]
    undetermined = [_undetermined(project, item, by_id) for item in groups['undetermined']]

    findings = recommend.findings(documents, planned_context, groups, enforcement, root=project)
    config_errors = [
        {'location': item.get('location'), 'detail': item.get('detail'),
         'fix': item.get('fix', '')}
        for item in findings if item.get('kind') == 'config'
    ]

    baseline_path = _resolve(project, baseline, project / 'autodoc-baseline.json')
    baseline_result = {
        'path': str(baseline_path), 'written': False, 'entries': 0,
        'exempt': [], 'phase': planned_phase, 'off_checks': [],
    }
    if write_baseline and not config_errors:
        collected, off = enforce.collect_findings(
            profile_document, planned_context, documents, groups, enforcement, root=project)
        baseline_result['off_checks'] = off
        collected_config = [item for item in collected if item.get('kind') == 'config']
        if collected_config:
            config_errors = [
                {'location': item.get('location'), 'detail': item.get('detail'),
                 'fix': item.get('fix', '')}
                for item in collected_config
            ]
            baseline_result['refused'] = True
        else:
            data = enforce.write_baseline(baseline_path, collected, planned_phase)
            baseline_result.update({
                'written': True,
                'entries': len(data['entries']),
                'exempt': data.get('exempt', []),
                'findings_seen': len(collected),
                'secret_findings': sum(1 for item in collected
                                       if item.get('rule') in enforce.BASELINE_EXEMPT),
            })
    elif write_baseline:
        baseline_result['refused'] = True

    ladder = _phase_ladder(documents, profile_document, planned_context, placement, phases)
    gaps = _declaration_gaps(planned_context, groups)
    triggers = _trigger_model(project)
    summary = {
        'open_required': len(required),
        'required_missing': sum(1 for item in required if item['status'] == 'missing'),
        'required_unregistered': sum(1 for item in required if item['status'] == 'unregistered'),
        'recommended': len(recommended),
        'advisory': len(advisory),
        'undetermined': len(undetermined),
        'declaration_gaps': len(gaps),
        'baseline_entries': baseline_result['entries'],
    }
    exit_code = 2 if config_errors else 0
    result = {
        'command': 'adopt', 'schema': SCHEMA, 'project': str(project),
        'config': str(config_path) if config_path.is_file() else None,
        'heuristics': [{'name': name, 'domain': domain, 'matches': matches}
                       for name, domain, matches in heuristics],
        'phase': {
            'declared': declared_phase,
            'planned': planned_phase,
            'preview': phase is not None and phase != declared_phase,
            'enforcement': {
                'label': enforcement['label'], 'declared': enforcement['declared'],
                'fail': enforcement['fail'], 'core': enforcement['core'],
                'extended': enforcement['extended'],
            },
        },
        'profile': {
            'declared': declared_profile,
            'planned': planned_profile,
            'preview': profile is not None and profile != declared_profile,
            'name': placement['name'], 'why': placement['why'],
            'core_types': len(placement['core']),
            'added': placement['added'], 'removed': placement['removed'],
        },
        'kinds': recommend.kind_summary(profile_document, planned_context),
        'requirements': {
            'open_required': required, 'recommended': recommended,
            'advisory': advisory, 'undetermined': undetermined,
        },
        'declaration_gaps': gaps,
        'phase_ladder': ladder,
        'triggers': triggers,
        'baseline': baseline_result,
        'config_errors': config_errors,
        'summary': summary,
        'exit_code': exit_code,
    }
    result['next_steps'] = _next_steps(result)
    return result


def _next_steps(result: dict) -> list[str]:
    if result.get('config_errors'):
        return ['Fix the configuration errors above; no plan is reliable until the context is valid.']
    required = result['requirements']['open_required']
    missing = [item for item in required if item['status'] == 'missing']
    unregistered = [item for item in required if item['status'] == 'unregistered']
    steps = []
    if not result['phase']['declared'] and not result['phase']['preview']:
        steps.append('Declare a phase in autodoc.toml, or preview one with --phase <id>.')
    if unregistered:
        steps.append(f'Register {len(unregistered)} existing required document(s) in '
                     '[instantiated] with their paths; they exist but are not acknowledged.')
    if missing:
        steps.append(f'Create {len(missing)} missing required document(s) with '
                     '`autodoc evolve --repo . --write --allow-add`, or one at a time with '
                     '`autodoc add <ID> --root . --write`. Drafts are not compliance.')
    if result['requirements']['undetermined']:
        steps.append('Declare the missing audience, kinds or facts listed above; undetermined '
                     'types are reported, never failed.')
    if not result['baseline']['written']:
        steps.append('Record existing findings with `autodoc adopt --project-path . '
                     '--write-baseline` before treating the gate as a ratchet.')
    else:
        steps.append('Run `autodoc check --repo .`; the baseline suppresses what existed, so only '
                     'new findings fail.')
    steps.append('Configure a required pull-request check that runs `autodoc check --repo .`; '
                 'AutoDOC does not install CI, hooks or branch protection.')
    return steps


def _render_items(items, label, formatter) -> list[str]:
    lines = [f'{label} ({len(items)}):']
    for item in items[:MAX_RENDERED]:
        lines.append('  ' + formatter(item))
    if len(items) > MAX_RENDERED:
        lines.append(f'  ... {len(items) - MAX_RENDERED} more')
    return lines


def render(result: dict) -> str:
    lines = [f"AutoDOC adopt — {result['project']}"]
    config = result.get('config')
    lines.append(f"Context: {config or 'none (undeclared; use --phase/--profile to preview)'}")
    lines.append('')
    lines.append('Suggested catalog domains (heuristics only; review applicability manually):')
    for item in result['heuristics']:
        lines.append(f"- {item['domain']} ({item['name']}): {', '.join(item['matches'])}")
    lines.append('Always consider A06-SECURITY, A07-PRIVACY and A11-TESTING; absence of a '
                 'filename is not proof of non-applicability.')

    if result.get('errors'):
        lines.append('')
        lines.append('Blocked by configuration errors:')
        for problem in result['errors']:
            lines.append(f'  ! {problem}')
        lines.append('Nothing was written. Fix the context first.')
        return '\n'.join(lines) + '\n'
    if result.get('config_errors'):
        lines.append('')
        lines.append('Blocked by configuration errors:')
        for item in result['config_errors']:
            lines.append(f"  ! {item['location']}: {item['detail']}")
            if item.get('fix'):
                lines.append(f"    fix: {item['fix']}")
        lines.append('Nothing was written. Fix the context first.')

    phase = result['phase']
    suffix = ''
    if phase['preview']:
        suffix = f" [preview; declared {phase['declared'] or 'none'}]"
    elif phase['declared']:
        suffix = ' [declared]'
    lines.append('')
    lines.append(f"Adoption plan (preview; declarations are not written): "
                 f"phase {phase['enforcement']['label']}{suffix}")
    profile = result['profile']
    profile_suffix = ''
    if profile['preview']:
        profile_suffix = f" [preview; declared {profile['declared'] or 'none'}]"
    lines.append(f"Profile: {profile['name']} ({profile['core_types']} core types){profile_suffix}")
    lines.append(recommend.kind_line(result['kinds'], result['requirements']))
    lines.append(f"Missing required severity: {phase['enforcement']['core']}; "
                 f"missing recommended severity: {phase['enforcement']['extended']}.")
    if not phase['declared']:
        lines.append('Phase undeclared: findings are advisory and nothing fails. '
                     '--phase previews a phase without declaring it.')

    lines.append('')
    lines.append('Phase ladder (open required / recommended / undetermined):')
    for step in result['phase_ladder']:
        marker = ' <- planned' if step['phase'] == phase['planned'] else ''
        lines.append(f"  {step['phase']:<10} {step['open_required']:>3} / "
                     f"{step['recommended']:>3} / {step['undetermined']:>3}{marker}")

    requirements = result['requirements']
    if requirements['open_required']:
        lines.append('')
        lines.extend(_render_items(
            requirements['open_required'], 'Open required at the planned phase',
            lambda item: (f"{item['status']:<12} {item['id']} {item['name']} -> "
                          f"{item['target']}")))
    if requirements['advisory']:
        lines.append('')
        lines.extend(_render_items(
            requirements['advisory'], 'Advisory core types',
            lambda item: (f"{item['status']:<12} {item['id']} {item['name']} -> "
                          f"{item['target']}")))
    if requirements['recommended']:
        lines.append('')
        lines.extend(_render_items(
            requirements['recommended'], 'Recommended',
            lambda item: (f"{item['status']:<12} {item['id']} {item['name']} -> "
                          f"{item['target']}")))
    if requirements['undetermined']:
        lines.append('')
        lines.extend(_render_items(
            requirements['undetermined'], 'Undetermined',
            lambda item: (f"{item['status']:<12} {item['id']} {item['name']}: "
                          f"{', '.join(item['unknown'])}")))
    if result['declaration_gaps']:
        lines.append('')
        lines.append(f"Declaration gaps ({len(result['declaration_gaps'])}):")
        for gap in result['declaration_gaps'][:MAX_RENDERED]:
            lines.append(f"  {gap['declaration']}: {gap['affected']} type(s) — {gap['fix']}")

    baseline = result['baseline']
    lines.append('')
    if baseline['written']:
        lines.append(f"Baseline written: {baseline['path']} "
                     f"({baseline['entries']} entry/entries, phase {baseline['phase'] or 'none'}).")
        if baseline.get('secret_findings'):
            lines.append(f"{baseline['secret_findings']} secrets.inline finding(s) were not recorded; "
                         'they always fail.')
    elif baseline.get('refused'):
        lines.append('Baseline not written because configuration errors must be fixed first.')
    else:
        lines.append(f"Baseline: not written (default: {baseline['path']}). "
                     '--write-baseline records current findings before enforcement starts.')

    lines.append('')
    lines.append('Trigger model (recommended; AutoDOC does not install it):')
    for event in result['triggers']['events']:
        posture = 'blocking' if event['blocking'] else event['posture']
        lines.append(f"  {posture:<10} {event['label']}: {', '.join(event['runs'])}")
    if result['triggers']['detected_files']:
        lines.append(f"  Detected CI files: {', '.join(result['triggers']['detected_files'])}")
    lines.append(f"  {result['triggers']['note']}")

    lines.append('')
    lines.append('Next steps:')
    for number, step in enumerate(result['next_steps'], 1):
        lines.append(f'  {number}. {step}')
    lines.append('No phase, profile, document, approval or catalog change was made'
                 + (' by this run.' if not baseline['written'] else
                    '; only the baseline was written.'))
    return '\n'.join(lines) + '\n'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-path', type=Path, default=Path.cwd(),
                        help='project to adopt (default: current directory)')
    parser.add_argument('--config', type=Path,
                        help='context TOML (default: <project>/autodoc.toml; relative to the project)')
    parser.add_argument('--phase', help='preview a phase without declaring it')
    parser.add_argument('--profile', help='preview a profile without declaring it')
    parser.add_argument('--baseline', type=Path,
                        help='baseline JSON (default: <project>/autodoc-baseline.json; '
                             'relative to the project)')
    parser.add_argument('--write-baseline', action='store_true',
                        help='record current findings as the adoption baseline and exit')
    parser.add_argument('--json', action='store_true', help='print a machine-readable plan')
    args = parser.parse_args(argv)
    try:
        result = build_plan(args.project_path, config=args.config, phase=args.phase,
                            profile=args.profile, baseline=args.baseline,
                            write_baseline=args.write_baseline)
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print(f'Adopt failed: {error}', file=sys.stderr)
        return 2
    except Exception as error:  # noqa: BLE001 - a crash must not impersonate findings
        print(f'Internal error: {type(error).__name__}: {error}', file=sys.stderr)
        print('This is a tool failure, not a finding about this repository.', file=sys.stderr)
        return 3
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render(result), end='')
    return result.get('exit_code', 0)


if __name__ == '__main__':
    raise SystemExit(main())
