#!/usr/bin/env python3
"""Plan safe documentation evolution for a project, and apply only the safe parts.

`evolve` is the project-side half of AutoDOC's autoevolution. It answers one question without
changing anything: what would improve this project's documentation now, and which of those changes
are safe for a tool to perform unattended?

The plan is derived from the same context, profile, catalog, and enforcement layers as `check`, so
it cannot disagree with the gate. The apply step is deliberately narrower than the gate:

* generated artifacts may be refreshed from their declared sources;
* missing required documents may be created as `draft` instances with `--allow-add`, but they are
  never registered, approved, satisfied, or counted as compliant;
* undetermined facts, structural findings, and existing-but-unregistered documents are reported,
  never guessed at or overwritten.

An agent never decides the project's phase, profile, applicability, or approvals. Those stay with
the owner, and this command never writes `autodoc.toml`, the catalog, or a decision record.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTELLIGENCE = Path(__file__).resolve().parent
CONTROL = ROOT / 'scripts' / 'doc-control'
SCHEMA = 1
MAX_RENDERED_REPORTS = 20
ACTION_REFRESH = 'refresh_generated'
ACTION_CREATE = 'create_document'


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f'cannot load {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


context_module = _load('autodoc_evolve_context', INTELLIGENCE / 'context.py')
recommend = _load('autodoc_evolve_recommend', INTELLIGENCE / 'recommend.py')
enforce = _load('autodoc_evolve_enforce', INTELLIGENCE / 'enforce.py')
add_document = _load('autodoc_evolve_add_document', ROOT / 'scripts' / 'add-document.py')


def _git(repo: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ['git', '-C', str(repo), *args],
            capture_output=True, text=True, check=False)
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _matches(repo: Path, patterns: tuple[str, ...]) -> bool:
    return any(path.exists() for pattern in patterns for path in repo.glob(pattern))


def maturity(repo: Path) -> dict:
    """Report observable maturity signals. The level is advisory, never a phase declaration."""
    signals: dict[str, bool | int] = {
        'license': _matches(repo, ('LICENSE', 'LICENSE.*', 'COPYING', 'COPYING.*')),
        'changelog': _matches(repo, ('CHANGELOG', 'CHANGELOG.*', 'CHANGES', 'CHANGES.*')),
        'ci': _matches(repo, ('.github/workflows/*.yml', '.github/workflows/*.yaml',
                              '.gitlab-ci.yml', '.circleci/config.yml', 'azure-pipelines.yml',
                              'Jenkinsfile')),
        'tests': _matches(repo, ('tests', 'test', 'spec', 'pytest.ini', 'tox.ini')),
        'package': _matches(repo, ('pyproject.toml', 'package.json', 'Cargo.toml', 'go.mod',
                                   'pom.xml', 'build.gradle', 'build.gradle.kts')),
    }
    toplevel = _git(repo, 'rev-parse', '--show-toplevel')
    in_repository_root = bool(toplevel) and Path(toplevel).resolve() == repo
    tag_text = (_git(repo, 'tag', '--list', 'v*') or '') if in_repository_root else ''
    signals['tags'] = len([line for line in tag_text.splitlines() if line.strip()])
    count_text = _git(repo, 'rev-list', '--count', 'HEAD') if in_repository_root else None
    try:
        signals['commits'] = int(count_text or 0)
    except ValueError:
        signals['commits'] = 0
    if (signals['license'] and signals['changelog'] and (signals['ci'] or signals['tests'])
            and (signals['tags'] or signals['commits'] >= 50)):
        level = 'mature'
    elif ((signals['license'] or signals['changelog'] or signals['package'])
          and (signals['ci'] or signals['tests'] or signals['package'])):
        level = 'growing'
    else:
        level = 'early'
    return {'level': level, 'signals': signals}


def _context(repo: Path, config: Path | None) -> tuple[Path, dict]:
    config = (config or repo / 'autodoc.toml').expanduser().resolve()
    if not config.is_file():
        raise ValueError(f'context file does not exist: {config}')
    context = context_module.normalise(context_module.load(config))
    problems = context_module.validate(context)
    if problems:
        raise ValueError('; '.join(problems))
    return config, context


def _target(document: dict) -> str:
    return (Path('docs') / 'autodoc' / add_document.library.destination(document)).as_posix()


def _finding(item: dict) -> dict:
    return {'kind': 'finding', 'rule': item.get('rule'), 'severity': item.get('severity'),
            'location': item.get('location'), 'detail': item.get('detail'),
            'fix': item.get('fix', '')}


def build_plan(repo: Path, config: Path | None = None, baseline: Path | None = None) -> dict:
    """Build a read-only plan. This function never writes to the project."""
    repo = repo.expanduser().resolve()
    if not repo.is_dir():
        raise ValueError(f'project root is not a directory: {repo}')
    config, context = _context(repo, config)
    documents = recommend.catalog()
    profile_document = recommend.profiler.profile(repo, context['facts'])
    enforcement = context_module.enforcement(context['phase'])
    placement = recommend.profile_placement(documents, context)
    groups = recommend.evaluate(documents, profile_document, context, enforcement, placement)
    findings, off = enforce.collect_findings(
        profile_document, context, documents, groups, enforcement, root=repo)
    baseline_path = ((repo / 'autodoc-baseline.json') if baseline is None
                     else baseline.expanduser().resolve())
    baseline_data = enforce.load_baseline(baseline_path)
    kept, suppressed, stale = enforce.apply_baseline(findings, baseline_data)

    documents_by_id = {document['id']: document for document in documents}
    required_by_id = {item['id']: item for item in groups['required']
                      if item.get('decision') is None}
    actions: list[dict] = []
    reports: list[dict] = []
    config_errors: list[dict] = []
    seen_generated: set[str] = set()

    for item in kept:
        if item.get('kind') == 'config':
            config_errors.append({'kind': 'config', 'rule': item.get('rule'),
                                  'severity': item.get('severity'),
                                  'location': item.get('location'),
                                  'detail': item.get('detail'), 'fix': item.get('fix', '')})
            continue
        if item.get('rule') == 'drift':
            target = item.get('location')
            if target in seen_generated:
                continue
            seen_generated.add(target)
            if item.get('severity') in ('warn', 'error'):
                actions.append({
                    'kind': ACTION_REFRESH, 'target': target,
                    'reason': item.get('detail', ''), 'safe': True, 'written': False,
                })
            else:
                reports.append(_finding(item))
            continue
        if item.get('rule') == 'recommend.core' and item.get('location') in required_by_id:
            continue
        reports.append(_finding(item))

    for doc_id, item in required_by_id.items():
        finding = next((entry for entry in kept
                        if entry.get('rule') == 'recommend.core'
                        and entry.get('location') == doc_id), None)
        if finding is None:
            continue
        document = documents_by_id[doc_id]
        target = _target(document)
        if (repo / target).exists():
            reports.append({
                'kind': 'unregistered', 'id': doc_id, 'name': item['name'],
                'target': target,
                'fix': 'review it, then declare it in [instantiated] with the path',
            })
            continue
        if item['severity_effective'] not in ('warn', 'error'):
            reports.append({'kind': 'missing_advisory', 'id': doc_id, 'name': item['name'],
                            'target': target, 'severity': item['severity_effective']})
            continue
        actions.append({
            'kind': ACTION_CREATE, 'id': doc_id, 'name': item['name'], 'target': target,
            'variant': 'canonical', 'requires_allow_add': True, 'safe': True, 'written': False,
            'reason': finding.get('detail', ''),
        })

    for item in groups['undetermined']:
        unknown = sorted(token for token, state in item['tokens'].items() if state == 'unknown')
        reports.append({'kind': 'undetermined', 'id': item['id'], 'name': item['name'],
                        'unknown': unknown,
                        'fix': 'declare the fact in autodoc.toml, or record a decision'})

    for entry in stale:
        reports.append({'kind': 'baseline_stale', 'key': entry.get('key'),
                        'rule': entry.get('rule'), 'location': entry.get('location'),
                        'fix': 'remove the stale entry or record the finding again'})

    summary = {
        'actions': len(actions),
        'generated': sum(1 for action in actions if action['kind'] == ACTION_REFRESH),
        'documents': sum(1 for action in actions if action['kind'] == ACTION_CREATE),
        'reports': len(reports),
        'undetermined': sum(1 for report in reports if report['kind'] == 'undetermined'),
        'findings': sum(1 for report in reports if report['kind'] == 'finding'),
        'baseline_suppressed': len(suppressed),
        'baseline_stale': len(stale),
        'written': 0,
        'errors': 0,
    }
    return {
        'command': 'evolve', 'schema': SCHEMA, 'repo': str(repo), 'config': str(config),
        'phase': context['phase'], 'phase_declared': context['phase_declared'],
        'enforcement': {'phase': enforcement['phase'], 'label': enforcement['label'],
                        'fail': enforcement['fail'], 'declared': enforcement['declared']},
        'maturity': maturity(repo),
        'actions': actions, 'reports': reports, 'config_errors': config_errors,
        'off': off,
        'baseline': {'path': str(baseline_path), 'suppressed': len(suppressed),
                     'stale': len(stale)},
        'summary': summary,
    }


def apply_plan(result: dict, repo: Path, allow_add: bool = False) -> tuple[int, dict]:
    """Apply the safe parts of a plan. Returns (exit code, result)."""
    repo = repo.expanduser().resolve()
    errors: list[str] = []
    refreshed = False
    for action in result['actions']:
        if action['kind'] == ACTION_REFRESH:
            try:
                with contextlib.redirect_stdout(io.StringIO()), \
                        contextlib.redirect_stderr(io.StringIO()), enforce.repo_scope(repo):
                    action['written'] = bool(enforce.engine.generate(check=False))
                refreshed = refreshed or action['written']
            except (OSError, ValueError) as error:
                action['error'] = str(error)
                errors.append(f"{action['target']}: {error}")
        elif action['kind'] == ACTION_CREATE and allow_add:
            try:
                added = add_document.add(action['id'], root=repo, write=True)
                action['written'] = True
                action['target'] = added['relative_target']
            except (OSError, ValueError, FileExistsError) as error:
                action['error'] = str(error)
                errors.append(f"{action['id']}: {error}")
    if refreshed:
        remaining: list[dict] = []
        try:
            with contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()), enforce.repo_scope(repo):
                enforce.engine.generate(check=True, findings=remaining)
        except (OSError, ValueError) as error:
            errors.append(f'verification failed: {error}')
        for item in remaining:
            if item.get('rule') == 'drift':
                errors.append(f"still stale after refresh: {item.get('location')}")
    result['summary']['written'] = sum(1 for action in result['actions']
                                       if action.get('written'))
    result['summary']['pending'] = sum(1 for action in result['actions']
                                       if not action.get('written'))
    result['summary']['errors'] = len(errors)
    result['errors'] = errors
    return (1 if errors else 0), result


def evolve(*, repo: Path, config: Path | None = None, baseline: Path | None = None,
           write: bool = False, allow_add: bool = False) -> tuple[int, dict]:
    result = build_plan(repo, config=config, baseline=baseline)
    if result['config_errors']:
        return 2, result
    if write:
        return apply_plan(result, repo, allow_add=allow_add)
    return 0, result


def _maturity_line(document: dict) -> str:
    signals = document['signals']
    positive = [name for name, value in signals.items()
                if name not in ('tags', 'commits') and value]
    if signals['tags']:
        positive.append(f"{signals['tags']} tag(s)")
    if signals['commits']:
        positive.append(f"{signals['commits']} commit(s)")
    detail = ', '.join(positive) if positive else 'no maturity signals'
    return f"Maturity: {document['level']} ({detail})"


def render(result: dict) -> str:
    lines = [f"AutoDOC evolve — {result['repo']}",
             f"Phase: {result['enforcement']['label']}",
             _maturity_line(result['maturity'])]
    if result['off']:
        lines.append(f"Off at this phase: {', '.join(result['off'])}")
    if result['config_errors']:
        lines.append('')
        lines.append('Blocked by configuration errors:')
        for item in result['config_errors']:
            lines.append(f"  ! {item['location']}: {item['detail']}")
            if item.get('fix'):
                lines.append(f"    fix: {item['fix']}")
    if result['actions']:
        lines.append('')
        lines.append(f"Actions ({len(result['actions'])}):")
        for action in result['actions']:
            if action['kind'] == ACTION_REFRESH:
                line = f"  refresh  {action['target']}"
            else:
                suffix = ' (draft)' if action.get('written') else ' (draft; requires --allow-add)'
                line = (f"  create   {action['id']} {action['name']} -> {action['target']}"
                        f"{suffix}")
            if action.get('written'):
                line += ' [written]'
            elif action.get('error'):
                line += f" [failed: {action['error']}]"
            lines.append(line)
    if result['reports']:
        lines.append('')
        lines.append(f"Reports ({len(result['reports'])}):")
        for report in result['reports'][:MAX_RENDERED_REPORTS]:
            if report['kind'] == 'undetermined':
                tokens = ', '.join(report['unknown']) or 'facts'
                lines.append(f"  undetermined  {report['id']} {report['name']}: {tokens}")
            elif report['kind'] == 'unregistered':
                lines.append(f"  unregistered  {report['id']} {report['name']}: "
                             f"{report['target']} exists but is not declared")
                lines.append(f"                fix: {report['fix']}")
            elif report['kind'] == 'baseline_stale':
                lines.append(f"  stale baseline  {report['key']} "
                             f"({report['rule']} {report['location']})")
            elif report['kind'] == 'missing_advisory':
                lines.append(f"  advisory      {report['id']} {report['name']}: "
                             f"missing (severity {report['severity']})")
            else:
                lines.append(f"  {report['severity']}  {report['rule']} "
                             f"{report['location']}: {report['detail']}")
        if len(result['reports']) > MAX_RENDERED_REPORTS:
            lines.append(f"  ... {len(result['reports']) - MAX_RENDERED_REPORTS} more report(s)")
    lines.append('')
    summary = result['summary']
    lines.append(f"{summary['actions']} action(s), {summary['reports']} report(s), "
                 f"{summary['baseline_suppressed']} baseline-suppressed.")
    if result['config_errors']:
        lines.append('Nothing was written. Fix the configuration errors first.')
    elif summary['written']:
        lines.append(f"Wrote {summary['written']} action(s). Run 'autodoc check' to verify.")
        if summary.get('pending'):
            lines.append(f"{summary['pending']} action(s) were not applied "
                         f"(document creation needs --allow-add).")
    elif not result['actions']:
        lines.append('No safe actions pending.')
    else:
        lines.append('Preview only. --write refreshes generated docs; '
                     '--write --allow-add creates draft documents.')
    lines.append('No phase, profile, decision, approval or catalog change is made.')
    return '\n'.join(lines) + '\n'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path.cwd(),
                        help='project to evolve (default: current directory)')
    parser.add_argument('--config', type=Path,
                        help='context file (default: <repo>/autodoc.toml)')
    parser.add_argument('--baseline', type=Path,
                        help='baseline file (default: <repo>/autodoc-baseline.json)')
    parser.add_argument('--write', action='store_true',
                        help='apply safe actions (generated refresh, and drafts with --allow-add)')
    parser.add_argument('--allow-add', action='store_true',
                        help='with --write, create missing required documents as drafts')
    parser.add_argument('--check', action='store_true',
                        help='exit 1 when an action is pending, without writing')
    parser.add_argument('--json', action='store_true', help='print a machine-readable plan')
    args = parser.parse_args(argv)
    if args.check and args.write:
        parser.error('--check cannot be combined with --write')
    try:
        code, result = evolve(repo=args.repo, config=args.config, baseline=args.baseline,
                              write=args.write, allow_add=args.allow_add)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f'Evolve failed: {error}', file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render(result), end='')
    if args.check and code == 0 and result['actions']:
        return 1
    return code


if __name__ == '__main__':
    raise SystemExit(main())
