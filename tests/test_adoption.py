"""Scaffolding is opt-in, creates unique instance IDs and never overwrites edits."""
import importlib.util
import json
from unittest.mock import patch
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _adopt(project, *arguments):
    return subprocess.run(
        [sys.executable, str(ROOT / 'scripts/adopt.py'), '--project-path', str(project),
         *arguments],
        capture_output=True, text=True, check=False)


def _context(project, extra=''):
    (project / 'pyproject.toml').write_text(
        '[project]\nname = "consumer"\nversion = "0.1.0"\n', encoding='utf-8')
    (project / 'autodoc.toml').write_text(
        'schema = 1\nphase = "build"\nprofile = "oss-library"\n'
        'audience = ["contributors", "external-users"]\nkinds = ["library"]\n' + extra,
        encoding='utf-8')


def _document(project, relative):
    path = project / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '---\nid: INST-CONSUMER-TEST\ntitle: "Test document"\ntype: SPEC\n'
        'owner: "@owner"\nreviewer: "@reviewer"\nclassification: internal\n'
        'status: draft\nversion: "0.1"\neffective_date: 2026-01-01\n'
        'next_review: 2099-01-01\nsource_of_truth: human\nsupersedes: null\n'
        'related: []\ncriticality: high\nreview_days: 90\nlast_verified: 1970-01-01\n'
        'last_reviewed: 1970-01-01\nlast_updated: 2026-01-01\nauto_generated: false\n---\n\n'
        '# Test document\n\n<!-- Add content. -->\n',
        encoding='utf-8')
    return path


class AdoptionTests(unittest.TestCase):
    def test_new_project_scaffold_is_safe_to_rerun(self):
        with tempfile.TemporaryDirectory() as folder:
            command = [sys.executable, str(ROOT / 'scripts/init-project.py'), '--name', 'Sample App',
                       '--type', 'web-api', '--output', folder]
            subprocess.run(command, check=True, capture_output=True)
            docs = sorted((Path(folder) / 'docs/autodoc').glob('*.md'))
            self.assertEqual(len(docs), 10)
            self.assertIn('id: INST-SAMPLE-APP-DEV-', docs[0].read_text())
            docs[0].write_text('intentionally edited')
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(docs[0].read_text(), 'intentionally edited')


    def test_owned_documents_are_within_declared_scope(self):
        spec = importlib.util.spec_from_file_location('ownership', ROOT / 'scripts/doc-control/check_ownership.py')
        ownership = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ownership)
        self.assertTrue(ownership.check())
        doc = ROOT / 'CURRENT-STATE.md'
        with patch.object(ownership, 'controlled', return_value=[doc]):
            with patch.object(ownership, 'parse_frontmatter', return_value={'owner': '@unknown'}):
                self.assertFalse(ownership.check())

    def test_adoption_is_read_only(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'go.mod'
            path.write_text('module example')
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/adopt.py'),
                                     '--project-path', folder], capture_output=True, text=True, check=True)
            self.assertIn('A10-BUILD', result.stdout)
            self.assertEqual([p.name for p in Path(folder).iterdir()], ['go.mod'])


class AdoptionPlanTests(unittest.TestCase):
    def test_phase_and_profile_preview_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            _context(project)
            before = (project / 'autodoc.toml').read_text(encoding='utf-8')

            result = _adopt(project, '--phase', 'beta', '--profile', 'regulated', '--json')

            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual(plan['phase']['declared'], 'build')
            self.assertEqual(plan['phase']['planned'], 'beta')
            self.assertTrue(plan['phase']['preview'])
            self.assertEqual(plan['profile']['declared'], 'oss-library')
            self.assertEqual(plan['profile']['planned'], 'regulated')
            self.assertTrue(plan['profile']['preview'])
            self.assertGreater(plan['summary']['open_required'], 0)
            self.assertEqual((project / 'autodoc.toml').read_text(encoding='utf-8'), before)
            self.assertFalse((project / 'autodoc-baseline.json').exists())
            self.assertEqual(
                [step['phase'] for step in plan['phase_ladder']],
                ['idea', 'prototype', 'build', 'beta', 'live', 'mature', 'sunset'])
            self.assertIn('open_required', plan['phase_ladder'][0])

    def test_unknown_phase_and_profile_are_usage_errors(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            _context(project)

            phase = _adopt(project, '--phase', 'no-such-phase')
            profile = _adopt(project, '--profile', 'no-such-profile')

            self.assertEqual(phase.returncode, 2)
            self.assertIn('unknown phase', phase.stderr)
            self.assertEqual(profile.returncode, 2)
            self.assertIn('unknown profile', profile.stderr)

    def test_existing_required_document_is_reported_unregistered(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            _context(project)
            _document(project, 'docs/autodoc/SPECIFICATIONS/DEV-B01-001.md')

            result = _adopt(project, '--json')

            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            item = next(item for item in plan['requirements']['open_required']
                        if item['id'] == 'DEV-B01-001')
            self.assertEqual(item['status'], 'unregistered')
            self.assertGreaterEqual(plan['summary']['required_unregistered'], 1)

    def test_write_baseline_records_findings_and_excludes_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            _context(project)
            _document(project, 'docs/autodoc/SPECIFICATIONS/DEV-B01-001.md')
            marker = '-----BEGIN ' + 'RSA PRIVATE KEY-----'
            (project / 'docs/keys.md').write_text(f'# Key\n\n{marker}\n', encoding='utf-8')

            result = _adopt(project, '--write-baseline', '--json')

            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertTrue(plan['baseline']['written'])
            baseline = json.loads(
                (project / 'autodoc-baseline.json').read_text(encoding='utf-8'))
            self.assertEqual(baseline['schema'], 1)
            self.assertEqual(baseline['phase'], 'build')
            self.assertTrue(baseline['entries'])
            self.assertNotIn('secrets.inline', {entry['rule'] for entry in baseline['entries']})
            self.assertIn('secrets.inline', baseline['exempt'])
            self.assertEqual(plan['baseline']['entries'], len(baseline['entries']))

    def test_configuration_error_refuses_baseline(self):
        with tempfile.TemporaryDirectory() as folder:
            project = Path(folder)
            _context(project, '\n[instantiated]\nDOC-Z99-999 = "docs/nope.md"\n')

            result = _adopt(project, '--write-baseline', '--json')

            self.assertEqual(result.returncode, 2, result.stderr)
            plan = json.loads(result.stdout)
            self.assertTrue(plan['config_errors'])
            self.assertFalse(plan['baseline']['written'])
            self.assertFalse((project / 'autodoc-baseline.json').exists())


if __name__ == '__main__':
    unittest.main()
