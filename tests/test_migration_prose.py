"""Regression tests for migration prose checks integrated with the stub policy."""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'stub_check_migration', ROOT / 'scripts/doc-control/stub_check.py')
stub_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stub_check)
library_spec = importlib.util.spec_from_file_location(
    'template_library_migration', ROOT / 'scripts/doc-control/library.py')
template_library = importlib.util.module_from_spec(library_spec)
library_spec.loader.exec_module(template_library)


def document(title, status='approved', sections=None):
    if sections is None:
        sections = {
            'Purpose and scope': 'This migration is for the task store and defines its scope.',
            'Details and decisions': 'The change preserves the existing identifier and records the owner.',
            'Verification and references': 'Run the migration tests and review the release checklist.',
        }
    body = [f'# {title}', '']
    for heading in stub_check.MIGRATION_SECTIONS:
        if heading in sections:
            body.extend([f'## {heading}', '', sections[heading], ''])
    return ('---\nid: TEST-MIGRATION-001\n'
            f'title: {title}\n'
            f'status: {status}\n'
            'auto_generated: false\n---\n' + '\n'.join(body))


def template_prompts(title):
    return {
        section: stub_check.MIGRATION_PROMPTS[section].format(title=title.casefold())
        for section in stub_check.MIGRATION_SECTIONS
    }


class MigrationProseTests(unittest.TestCase):
    def fields(self, title, status='approved', generated='false'):
        return {'title': title, 'status': status, 'auto_generated': generated}

    def test_authored_sections_pass_for_each_migration_title(self):
        for title in stub_check.MIGRATION_TEMPLATES:
            with self.subTest(title=title):
                self.assertEqual([], stub_check.migration_findings_for(
                    'migration.md', self.fields(title), document(title)))

    def test_canonical_renders_define_the_detected_prompts(self):
        sources = {
            doc['template']: doc for doc, _ in template_library.catalog_sources(ROOT)
        }
        for title, template in stub_check.MIGRATION_TEMPLATES.items():
            with self.subTest(title=title):
                text = template_library.render(sources[template], 'canonical')
                findings = stub_check.migration_findings_for(
                    template, self.fields(title), text)
                self.assertEqual(3, len(findings))
                self.assertTrue(all('canonical template prompt' in item['detail']
                                    for item in findings))
                self.assertTrue(all(item['rule'] == 'stubs' for item in findings))

    def test_markdown_emphasis_does_not_hide_headings_or_template_prompts(self):
        title = 'Migration plan'
        sections = template_prompts(title)
        text = document(title, sections={
            section: f'**{prompt}**' for section, prompt in sections.items()
        })
        for section in stub_check.MIGRATION_SECTIONS:
            text = text.replace(f'## {section}', f'## **{section}**')
        findings = stub_check.migration_findings_for(
            'migration-plan.md', self.fields(title), text)
        self.assertEqual(3, len(findings))
        self.assertTrue(all('canonical template prompt' in item['detail']
                            for item in findings))

    def test_draft_findings_use_placeholders_family(self):
        title = 'Migration plan'
        findings = stub_check.migration_findings_for(
            'migration-plan.md', self.fields(title, status='draft'),
            document(title, status='draft', sections=template_prompts(title)))
        self.assertEqual(3, len(findings))
        self.assertTrue(all(item['rule'] == 'placeholders' for item in findings))

    def test_approved_findings_use_stubs_family(self):
        title = 'Migration guide'
        findings = stub_check.migration_findings_for(
            'migration-guide.md', self.fields(title),
            document(title, sections=template_prompts(title)))
        self.assertEqual(3, len(findings))
        self.assertTrue(all(item['rule'] == 'stubs' for item in findings))

    def test_missing_section_is_reported(self):
        title = 'Migration design'
        sections = {
            'Purpose and scope': 'It explains why the change is needed and who uses it.',
            'Verification and references': 'Run the migration test suite and inspect the result.',
        }
        findings = stub_check.migration_findings_for(
            'migration-design.md', self.fields(title), document(title, sections=sections))
        self.assertEqual(["missing required section 'Details and decisions'"],
                         [item['detail'] for item in findings])

    def test_empty_section_is_reported(self):
        title = 'Migration plan'
        sections = document(title).replace(
            '## Details and decisions\n\nThe change preserves the existing identifier and records the owner.',
            '## Details and decisions\n\n')
        findings = stub_check.migration_findings_for(
            'migration-plan.md', self.fields(title), sections)
        self.assertEqual(["section 'Details and decisions' has no authored prose"],
                         [item['detail'] for item in findings])

    def test_h1_is_not_accepted_as_a_required_section(self):
        title = 'Migration plan'
        text = document(title).replace('## Details and decisions', '# Details and decisions')
        findings = stub_check.migration_findings_for(
            'migration-plan.md', self.fields(title), text)
        self.assertIn("missing required section 'Details and decisions'",
                      [item['detail'] for item in findings])

    def test_fenced_code_and_blockquotes_do_not_count_as_authored_prose(self):
        title = 'Migration test plan'
        sections = {
            heading: '> quoted guidance only\n\n```text\nexample placeholder\n```'
            for heading in stub_check.MIGRATION_SECTIONS
        }
        findings = stub_check.migration_findings_for(
            'migration-test-plan.md', self.fields(title), document(title, sections=sections))
        self.assertEqual(3, len(findings))
        self.assertTrue(all('no authored prose' in item['detail'] for item in findings))

    def test_horizontal_rules_do_not_count_as_authored_prose(self):
        title = 'Migration plan'
        sections = {
            heading: '---\n\n***\n\n_ _ _\n\n- - -'
            for heading in stub_check.MIGRATION_SECTIONS
        }
        findings = stub_check.migration_findings_for(
            'migration-plan.md', self.fields(title), document(title, sections=sections))
        self.assertEqual(3, len(findings))
        self.assertTrue(all('no authored prose' in item['detail'] for item in findings))

    def test_html_comments_do_not_count_as_authored_prose(self):
        title = 'Migration guide'
        sections = {
            heading: '<!-- Add project-specific information here. -->'
            for heading in stub_check.MIGRATION_SECTIONS
        }
        findings = stub_check.migration_findings_for(
            'migration-guide.md', self.fields(title), document(title, sections=sections))
        self.assertEqual(3, len(findings))
        self.assertTrue(all('no authored prose' in item['detail'] for item in findings))

    def test_generated_and_unrelated_documents_are_ignored(self):
        text = document('Migration plan')
        self.assertEqual([], stub_check.migration_findings_for(
            'generated.md', self.fields('Migration plan', generated='true'), text))
        marked = '<!-- AUTO-GENERATED BY AUTODOC ENGINE. test -->\n' + text
        self.assertEqual([], stub_check.migration_findings_for(
            'marked-generated.md', self.fields('Migration plan'), marked))
        self.assertEqual([], stub_check.migration_findings_for(
            'readme.md', self.fields('README'), text))

    def test_findings_join_existing_collect_results(self):
        finding = {'rule': 'stubs', 'location': 'docs/migration.md',
                   'detail': 'missing required section', 'fix': 'write the section'}
        with patch.object(stub_check, 'scan', return_value=([], [])), \
                patch.object(stub_check, 'migration_findings', return_value=[finding]):
            self.assertEqual([finding], stub_check.collect())

    def test_check_warns_for_draft_and_fails_approved_migration_findings(self):
        approved = {'rule': 'stubs', 'location': 'docs/migration.md',
                    'detail': 'missing required section', 'fix': 'write the section'}
        draft = dict(approved, rule='placeholders')
        with patch.object(stub_check, 'scan', return_value=([], [])), \
                patch.object(stub_check, 'migration_findings', return_value=[draft]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertTrue(stub_check.check())
        with patch.object(stub_check, 'scan', return_value=([], [])), \
                patch.object(stub_check, 'migration_findings', return_value=[approved]):
            output = io.StringIO()
            with contextlib.redirect_stderr(output):
                self.assertFalse(stub_check.check())
        self.assertIn('approved migration document', output.getvalue())

    def test_no_candidate_migration_documents_is_a_clean_noop(self):
        with patch.object(stub_check, 'controlled', return_value=[]):
            self.assertEqual([], stub_check.migration_findings())

    def test_scan_reads_controlled_frontmatter_and_routes_draft_findings(self):
        title = 'Migration plan'
        text = document(title, status='draft', sections=template_prompts(title))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'migration-plan.md'
            path.write_text(text, encoding='utf-8')
            with patch.object(stub_check, 'controlled', return_value=[path]):
                findings = stub_check.migration_findings()
        self.assertEqual(3, len(findings))
        self.assertTrue(all(item['rule'] == 'placeholders' for item in findings))


if __name__ == '__main__':
    unittest.main()
