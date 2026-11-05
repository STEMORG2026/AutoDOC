---
id: DOC-REF-004
title: "Type definitions"
type: SPEC
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-11-05
next_review: 2027-05-04
source_of_truth: human
supersedes: null
related: ["DOC-ARC-001", "DOC-P2-001", "DOC-REF-001", "DOC-P3-GOV-001", "DOC-CI-001"]
criticality: medium
review_days: 180
last_verified: 2026-11-05
last_reviewed: 2026-11-05
last_updated: 2026-11-05
auto_generated: false
---
# Type definitions

## Purpose and scope

This page records the shapes of the data that crosses AutoDOC's own module boundaries: what a
fact record contains, what a finding record contains, which of those shapes are checked by a
machine and which are a convention. It answers the catalog type `DEV-B05-002` (Type definitions),
which is why `autodoc.toml` records that type as satisfied by this page.

AutoDOC is plain Python on the standard library. It has **no static type checker**: `mypy` and
`pyright` are not in the development dependencies, there is no configuration file for either, and
no CI job runs one. The function signatures are annotated, and those annotations are read by
humans — they are not verified. What *is* verified is listed below.

Three kinds of definition exist here, and the difference matters:

| Kind | Where | Verified by |
| --- | --- | --- |
| Machine contract | JSON Schema files under `CONTROL/metadata/` | A validator that runs in `make ci` |
| In-code record shape | Dict literals built in the modules | Tests that pin the fields |
| Type annotation | Function signatures | Nothing — no checker runs |

The page covers the first two. It does not restate the module boundaries
([AUTODOC-ARCHITECTURE.md](../05-architecture/AUTODOC-ARCHITECTURE.md)), the error contract
([EXIT-CODES.md](EXIT-CODES.md)), or what the checks mean
([QUALITY-GATES.md](QUALITY-GATES.md)). It does not certify that the shapes are correct, and it
does not claim that a record conforming to this page is meaningful.

## Details and decisions

### The machine contracts

| Contract | Defined in | Validated by | Runs in |
| --- | --- | --- | --- |
| Catalog index | `CONTROL/metadata/CATALOG-SCHEMA.json` | `scripts/doc-control/check_catalog.py` | `make docs-catalog`, `make generate` |
| Declared context | `CONTROL/metadata/CONTEXT-SCHEMA.json` | `scripts/intelligence/context.py`, reusing the catalog validator | `make docs-catalog`, every `autodoc check` and `autodoc adopt` |
| Controlled-document metadata | `CONTROL/metadata/FRONT-MATTER-SCHEMA.json` | `scripts/validate/frontmatter_validator.py` and `engine.validate()` | `make docs-metadata`, `make docs-freshness`, the release gate |
| Adoption baseline | `CONTROL/metadata/BASELINE-SCHEMA.json` | **No code loads it.** `enforce.load_baseline()` checks `schema == 1` and that every entry is an object with a string `key`. | `make ci` (through `enforce.py`) |
| Trigger model | `CONTROL/metadata/TRIGGERS.json` | `scripts/intelligence/triggers.py --check` | `make ci` |
| Ownership matrix | `CONTROL/metadata/OWNERSHIP-MATRIX.yaml` | `scripts/doc-control/check_ownership.py` | `make docs-ownership` |

The catalog, context and profile model are generated from
`CONTROL/metadata/CATALOG-RULES.json`, `CONTEXT-MODEL.json` and `PROFILES.json`; `check_catalog.py`
validates those against their own rules rather than against a JSON Schema.

Two of those files are worth a note:

- **The validator implements a keyword subset, not JSON Schema.** `check_catalog.py` supports
  `$schema`, `$id`, `title`, `description`, `type`, `required`, `properties`,
  `additionalProperties`, `items`, `enum`, `pattern`, `minItems`, `uniqueItems`, `minimum`,
  `minLength`, `const` and `oneOf`. A schema that uses any other keyword **fails the check**
  rather than being silently ignored, so a schema can never be weakened by adding vocabulary the
  validator does not understand.
- **The baseline schema is prose.** `BASELINE-SCHEMA.json` is referenced only from
  [AUTODOC-ARCHITECTURE.md](../05-architecture/AUTODOC-ARCHITECTURE.md); no module reads it. The
  shape it describes is the shape `enforce.write_baseline()` writes, and the runtime check is
  `enforce.load_baseline()`, which verifies the schema number and the entry keys and then trusts
  the rest of a file the tool wrote itself. A hand-edited entry with a plausible `key` is
  therefore accepted; that is why the baseline is a ratchet, not a security control, and why
  `secrets.inline` findings are never baselined.

### The canonical finding record

Every check AutoDOC runs ends up as one record. The canonical shape is:

```
{kind, rule, severity, location, detail, message, fix, because}
```

| Field | Meaning |
| --- | --- |
| `kind` | `config`, `requirement`, `decision` or `check` — where the finding came from |
| `rule` | The check family, e.g. `recommend.core`, `drift`, `stubs`, `links.local`, `secrets.inline`, `tribal`, `placeholders`, `generator.heuristic`, `freshness.critical`, `freshness.review`, `context.config` |
| `severity` | `error`, `warn`, `report` or `off` after the declared phase is applied |
| `location` | The file, path or catalog id the finding is about |
| `detail` | One sentence saying what is wrong |
| `message` | The sentence as shown to a reader |
| `fix` | What to do about it |
| `because` | Which phase and policy produced this severity |

The baseline layer adds three optional fields to the same record: `baseline` (the matching
baseline entry), `baseline_age_days`, and `baseline_exempt` (set on a security finding that the
baseline was not allowed to suppress).

**Two shapes enter the enforcement layer, and one leaves it.** The delegated checkers —
`guards.py`, `stub_check.py`, and the sync engine's drift and freshness checks — emit the narrow
shape `{rule, location, detail}`, optionally with `fix`. `recommend.py` emits the full shape
directly. `enforce.py` widens the narrow shape: it supplies `kind: "check"`, the resolved
`severity`, a composed `message`, a `fix` (from `guards.FIXES` when the checker did not give
one) and a `because`. That widening is the only place the two shapes meet, so it is the only
place a change to either shape can break the other.

A consequence worth stating: because the narrow shape has no `severity`, severity is **always**
resolved by `enforce.py` from the declared phase and the `[severity]` pins. A checker cannot
choose its own severity.

### The fact record

`profile.py` produces one record per fact. The shape is:

```
{value, detection, exactness, evidence, limits}
```

- `value` is three-valued: `"true"`, `"false"` or `"unknown"`. `unknown` means no configured
  source could be evaluated; it never means false.
- `detection` is `"files"` for a detected fact and `"declaration-only"` for a declared trait.
- `exactness` is `"exact"`, `"heuristic"`, or `null` for a declaration-only fact.
- `evidence` lists the paths or manifest entries that matched, at most five.
- `limits` states what the detector cannot see.

A declaration-only fact additionally carries `label`. A fact overridden in `autodoc.toml` keeps
the detected `exactness` and `limits`, has its `value` replaced by the declared one, its
`evidence` replaced by `["declared"]`, and gains `declared_reason`.

The profile document itself is `{version, repo, file_count, languages, ecosystems, facts, kinds,
excluded, note}`, with `version` currently `2`.

### The context record

The normalised declared context is:

```
{version, phase, phase_declared, profile, audience, kinds, obligations, facts,
 not_applicable, satisfied_by, instantiated, severity, resolved_aliases, alias_problems}
```

This is the shape `CONTEXT-SCHEMA.json` validates, and it is what `context.normalise()` produces
from `autodoc.toml` before validation. The three decision tables (`not_applicable`,
`satisfied_by`, `instantiated`) map a catalog id — or an unambiguous name slug — to a decision;
a slug is substituted for the id and the substitution is recorded in `resolved_aliases`, with any
ambiguity in `alias_problems`. The documented spelling of the schema number is `schema = 1`;
`version` is an accepted alias that must agree with it.

### The baseline entry

```
{key, rule, location, recorded_at, detail?}
```

`key` is `rule|location|fingerprint(detail)`. The file around it is
`{schema, recorded_at, phase, note?, entries[]}`. `schema` must be `1`.

### Decisions

- **Keep the machine contracts in JSON Schema, not in annotations.** A schema is data, so it can
  be validated, diffed and read without running the code. An annotation is checked by nothing.
- **Do not add a type checker.** It would be a development dependency, and the runtime set is
  deliberately empty ([ADR-0001](../adr/0001-zero-runtime-dependencies.md)). The schemas plus the
  tests give the same protection for the shapes that actually cross a boundary.
- **Normalise findings in one place.** Two producer shapes are widened into one canonical record
  by `enforce.py`, rather than each checker inventing its own severity and fix text.
- **Leave the baseline schema unloaded until something loads it.** It documents the shape; the
  runtime validation is deliberately narrow, and the baseline never suppresses a security
  finding.

## Verification and references

```sh
make docs-catalog      # catalog schema, rules, index and the declared context
make docs-metadata     # controlled-document frontmatter against its schema
make docs-ownership    # the ownership matrix
make docs-verify       # all of the above, plus drift, stubs and the sync map
python scripts/intelligence/triggers.py --check   # the trigger model against the workflows
```

Related records:

- [AUTODOC-ARCHITECTURE.md](../05-architecture/AUTODOC-ARCHITECTURE.md) — the module boundaries
  these records cross.
- [ENGINE-COVERAGE.md](../00-governance/ENGINE-COVERAGE.md) — what each check family is trusted
  to decide.
- [EXIT-CODES.md](EXIT-CODES.md) — the exit codes the severity maps to.
- [QUALITY-GATES.md](QUALITY-GATES.md) — which checks block and which advise.
- [LIMITATIONS.md](../00-governance/LIMITATIONS.md) — the blind spots a clean run does not cover.
- `CONTROL/metadata/CATALOG-SCHEMA.json`, `CONTEXT-SCHEMA.json`, `FRONT-MATTER-SCHEMA.json`,
  `BASELINE-SCHEMA.json`, `TRIGGERS.json`, `OWNERSHIP-MATRIX.yaml` — the contracts themselves.
- `scripts/doc-control/check_catalog.py`, `scripts/intelligence/context.py`,
  `scripts/intelligence/profile.py`, `scripts/intelligence/recommend.py`,
  `scripts/intelligence/enforce.py`, `scripts/doc-control/guards.py` — the producers and
  validators this page describes.
