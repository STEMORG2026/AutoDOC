"""Regression tests for catalog count claims in human-owned documents.

D-001 recorded that the prose said "260 catalog types" long after the indexes held 265, and one
sentence carried a third, inconsistent total (24 core + 45 extended + 194 contextual = 263).
A remembered number is the defect; these tests derive the counts from the sources and then read
every claim a reader can see:

* the indexes (`CATALOG-A/INDEX.yaml`, `CATALOG-B/INDEX.yaml`) hold the types;
* `CONTROL/metadata/CATALOG-RULES.json` holds the core and extended tiers;
* the human-owned controlled documents, plus `state/DASHBOARD.md` and `state/ARCHITECTURE.md`
  (the two coordination documents that quote numbers), must agree with them.

What counts as a claim, and what deliberately does not:

* a **three-digit** number next to "type(s)", "template triples" or one of the phrasings the drift
  actually used ("copying 265 empty documents", "265 *possible* document types", "not 265
  instantiated governed documents") is a catalog total. Three digits is the shape of a catalog
  total, and it is what keeps narrower counts such as "72 types with no detectable predicate" out
  of this check. A general "any number before the word documents" rule was tried and rejected: it
  matched dates (`2026-10-01 … docs/…`) and ids (`DEV-B07-001`), which is how a check teaches
  people to ignore it;
* a paired "<N> core … <M> extended" is the tier split, checked against the rules;
* "<N> extended" and "<N> contextual" are checked individually;
* a bare "<N> core" is **not** checked: it is ambiguous between the default core tier (24) and a
  profile's core set (the `oss-library` profile has 26: 24 default + 3 added − 1 removed). Naming
  that ambiguity here is cheaper than a false failure that teaches a reader to ignore the test.

A sentence that deliberately describes an earlier catalog is exempt only when the word **then**
appears on the same line — so a stale number can be either corrected or marked as history, never
left ambiguous. The limit is stated rather than hidden: this reads numbers next to the words that
give them meaning, not the intent of the sentence.
"""

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/doc-sync'))
import engine  # noqa: E402

# Coordination documents that quote numbers and are not session logs (logs are append-only).
EXTRA_DOCUMENTS = [ROOT / 'state/DASHBOARD.md', ROOT / 'state/ARCHITECTURE.md']

# A number is a claim when the words next to it say what it counts.
TOTAL_CLAIMS = (
    re.compile(r'(?<![\w.])(\d{3})[- ]\s*(?:catalog\s+)?types?\b(?!\s+core)'),
    re.compile(r'(?<![\w.])(\d{3})\s+template\s+triples?\b'),
    # Three further shapes the drift actually appeared in. They are spelled out rather than
    # generalised to "any number before the word documents", which matched dates and ids.
    re.compile(r'(?<![\w.])(\d{3})\s+empty\s+(?:docs?|documents?)\b'),
    re.compile(r'(?<![\w.])(\d{3})\s+\*?possible\*?\s+document\s+types?\b'),
    re.compile(r'(?<![\w.])(\d{3})\s+instantiated\b'),
)
TIER_PAIR = re.compile(r'(?<![\w.])(\d{1,3})\s+core\b[^\n]{0,8}?(\d{1,3})\s+extended\b')
TIER_SINGLE = re.compile(r'(?<![\w.])(\d{1,3})\s+(extended|contextual)\b')


def counts():
    """Derive the catalog counts from the indexes and the rules, never from prose."""
    per_catalog = {}
    total = 0
    for name in ('CATALOG-A', 'CATALOG-B'):
        index = json.loads((ROOT / name / 'INDEX.yaml').read_text())
        ids = [doc['id'] for domain in index['domains'] for doc in domain['documents']]
        per_catalog[name] = len(ids)
        total += len(ids)
    rules = json.loads((ROOT / 'CONTROL/metadata/CATALOG-RULES.json').read_text())
    core = len(rules['tier']['core'])
    extended = len(rules['tier']['extended'])
    return {'types': total, 'CATALOG-A': per_catalog['CATALOG-A'],
            'CATALOG-B': per_catalog['CATALOG-B'], 'core': core, 'extended': extended,
            'contextual': total - core - extended}


def documents():
    """Human-owned controlled documents (generated ones are checked by drift, not by prose)."""
    found = [path for path in engine.controlled()
             if engine.parse_frontmatter(path)['auto_generated'] == 'false']
    found.extend(path for path in EXTRA_DOCUMENTS if path.is_file())
    return found


def claims_in(text):
    """Yield (number, kind) for each count claim; a line marked "then" is explicit history."""
    for line in text.splitlines():
        if 'then' in line.lower():
            continue
        for pattern in TOTAL_CLAIMS:
            for match in pattern.finditer(line):
                yield int(match.group(1)), 'types'
        pair = TIER_PAIR.search(line)
        if pair:
            yield int(pair.group(1)), 'core'
            yield int(pair.group(2)), 'extended'
            continue  # the pair already counted that "extended"; don't read it twice
        for match in TIER_SINGLE.finditer(line):
            yield int(match.group(1)), match.group(2)


class CatalogCountTests(unittest.TestCase):
    def test_derived_counts_are_internally_consistent(self):
        data = counts()
        self.assertEqual(data['types'], data['CATALOG-A'] + data['CATALOG-B'])
        self.assertEqual(data['types'], data['core'] + data['extended'] + data['contextual'])
        self.assertEqual(data['core'], 24)
        self.assertEqual(data['extended'], 49)

    def test_every_documented_count_matches_the_indexes(self):
        data = counts()
        allowed = {'types': {data['types'], data['CATALOG-A'], data['CATALOG-B']},
                   'core': {data['core']},
                   'extended': {data['extended']},
                   'contextual': {data['contextual']}}
        problems = []
        for path in documents():
            for value, kind in claims_in(path.read_text()):
                if value not in allowed[kind]:
                    problems.append(f'{path.relative_to(ROOT)}: "{value} {kind}" is not one of '
                                    f'{sorted(allowed[kind])}')
        self.assertEqual(problems, [], 'catalog count claims disagree with the indexes:\n' +
                         '\n'.join(problems))

    def test_a_stale_number_is_caught_and_history_is_escapable(self):
        data = counts()
        stale = f'| catalog | {data["types"] - 5} catalog types |\n'
        current = f'| catalog | {data["types"]} catalog types |\n'
        marked = f'| catalog | {data["types"] - 5} catalog types then |\n'
        self.assertEqual(list(claims_in(current)), [(data['types'], 'types')])
        self.assertEqual(list(claims_in(stale)), [(data['types'] - 5, 'types')],
                         'a stale claim must be seen, not skipped')
        self.assertEqual(list(claims_in(marked)), [],
                         'a line marked "then" is history the reader chose to keep, so it is skipped')

    def test_the_ambiguous_bare_core_count_is_not_read(self):
        self.assertEqual(list(claims_in('| profile | `oss-library` (26 core types) |\n')), [])
        self.assertEqual(list(claims_in('| catalog | 24 core · 49 extended · 265 types |\n')),
                         [(265, 'types'), (24, 'core'), (49, 'extended')])


if __name__ == '__main__':
    unittest.main()
