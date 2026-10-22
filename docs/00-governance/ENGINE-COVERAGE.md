---
id: DOC-P2-001
title: "Engine coverage and honest limits"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.2"
effective_date: 2026-09-26
next_review: 2027-03-25
source_of_truth: human
supersedes: null
related: []
criticality: medium
review_days: 180
last_verified: 2026-09-26
last_reviewed: 2026-09-26
last_updated: 2026-10-22
auto_generated: false
---
# Engine coverage and honest limits

## How confidence is established

This is the project's test strategy in one place: what is verified, by what, and what is left
unverified. The catalog type `DEV-B07-001` Test strategy is satisfied by this document
(`[satisfied_by]` in `autodoc.toml`).

1. **Unit and integration tests decide behaviour.** The suite runs with `pytest` (no network, no
   fixtures beyond the repository itself) and covers accepted *and* rejected inputs: a parser that
   accepts a note is only trusted once a test shows it rejects the malformed variant. The current
   suite and its subtests are counted in the evidence pack, and the test inventory
   (`docs/META/TEST-INVENTORY.md`) is generated, not maintained by hand. `make ci` also builds a
   wheel and sdist, rebuilds a wheel from the sdist, and installs the wheel in a clean virtual
   environment outside the checkout to exercise the console CLI and target-root boundary.
2. **Golden fixtures decide enforcement semantics.** `tests/fixtures/` holds whole miniature
   repositories (library, service, typed-library) and a matrix of expected outcomes, so a change to
   phase, tier, profile or fact handling must either keep the matrix green or change it deliberately.
3. **Regeneration decides fact accuracy.** Generated documents are not reviewed for correctness —
   they are re-rendered in memory on every check (`make docs:drift`), and any difference between
   source and committed target fails. Review effort goes to human-owned judgement instead.
4. **The declared phase decides severity.** No check is "on" or "off" by accident: severity comes
   from `autodoc.toml` and `CONTROL/metadata/CONTEXT-MODEL.json`, the report names the families it
   did not run, and an undeclared phase reports instead of failing.
5. **CI decides what actually gates.** The named required check runs the same `make ci` locally
   and remotely on Python 3.11. A separate Python 3.11–3.15 compatibility matrix supplies
   additional non-blocking signals; only the configured named check is required by branch
   protection. The trigger model (`CONTROL/metadata/TRIGGERS.json`) is verified against the
   workflows, and scheduled network checks are warn-only by design.
6. **Evidence records that a run happened — it is unsigned** and proves nothing about who ran it or
   whether a reviewer agreed (`docs/00-governance/EVIDENCE-SIGNING.md`).

**What this strategy does not establish.** That prose is true, adequate or reviewed; that an
external system behaves as documented; that a dependency is vulnerability-free (no scanner is
installed); or that any project is compliant. The per-generator limits and the not-implemented list
below are part of the strategy, not footnotes to it.

## Implemented and tested
All outputs below have concrete sources in `docs/.doc-sync-map.yaml`; `make generate` writes,
`make docs:drift` checks without writing, and tests cover accepted and rejected inputs.

| Source format | Generator/output | Supported scope | Tests |
| --- | --- | --- | --- |
| Demo `routes.json` | Task API reference | Exactly three implemented routes | `test_phase2.py`, `test_example.py` |
| Demo config JSON | Config reference + described `.env.example` | `integer`/`string` defaults | `test_phase2.py` |
| Described `.env.example` | `docs/reference/ENVIRONMENT.md` | `KEY=value`, preceding comment | `test_phase3.py` |
| Demo SQLite DDL | Data dictionary | Simple CREATE TABLE columns only | `test_phase2.py` |
| Example alert JSON-compatible YAML | Alert catalog | Condition, severity, existing runbook required | `test_phase3.py` |
| PEP 621 manifests | Declared dependency references | Direct declarations, no resolution | `test_phase2.py` |
| Python AST and ATX Markdown | Per-language code inventory and outline | Parsed declarations/headings, not behavior | `test_phase2.py`, `test_languages.py` |
| Declared toolchain (`go doc -all .`) | On-demand language reference (`make docs-languages SHOW=go`) | Runs the language's own tool inside the repository, offline and with a timeout; an absent tool is reported, never replaced | `test_languages.py` |
| `CONTROL/metadata/TRIGGERS.json` + workflows | Trigger reference (`docs/generated/TRIGGER-REFERENCE.md`), `make docs-triggers` | Workflow names, trigger keys, filters and job names only; a job produced by a reusable workflow is unverified | `test_triggers.py` |
| Controlled Markdown | Scheduled external link triage, `make docs-links-external` | Line-based extraction; fenced code skipped, local and example hosts skipped as documented-not-deployed, one request per host per second, capped, warn-only | `test_external_links.py` |
| Controlled migration docs | Structural prose check via `stub_check.py` and `make docs-stubs` | Four canonical migration titles; required headings and retained prompts only. The direct check warns on drafts/fails approved docs; CI applies existing phase and pin severity to `placeholders`/`stubs` | `test_migration_prose.py` |
| Catalog rules file | `CATALOG-A/B/INDEX.yaml` | Seeds names; derives type, tier, `phase_min`, `applies_when`, maturity | `test_catalog.py` |
| Repository files | `profile.json` three-valued facts | File presence only; `unknown` when nothing could be read | `test_profile.py` |
| `autodoc.toml` `[facts]` traits | declared personal-data / payments / safety values | Declaration only; no detector exists, and unanswered is `unknown`, never false | `test_profile.py`, `test_resolver.py` |
| `autodoc.toml` + context model | Validated declared context | Declarations only; never inferred | `test_context.py` |
| Profile + catalog + context | Obligations with severity and `--check` | Phase-scaled; advisory without a declared phase | `test_resolver.py` |
| Fixture repositories | kind x phase x ecosystem matrix | Awkward cases: no manifest, unread ecosystem, docs-only | `test_profile.py` |
| Enforcement policy | severity per check family per phase | One precedence: override, phase default, report | `test_enforce.py` |
| Adoption baseline | suppressed findings and stale entries | Keyed by rule and location; never suppresses a new finding | `test_enforce.py` |
| Installable CLI | `autodoc check/generate/adopt/init` | Bundled tool root is separate from the selected project root; zero runtime dependencies | `test_cli.py`, `scripts/test_package.py` |
| Wheel + source distribution | `make package` / `make package-check` | Build both formats, rebuild from sdist, install wheel in a clean venv outside the checkout | `scripts/test_package.py` |
| Python compatibility | Python 3.11–3.15 | Supplemental matrix; non-blocking. The named required gate runs full `make ci` on Python 3.11 | `.github/workflows/docs-guard.yml` |
| Exit codes | `0`, `1`, `2` | Documented in `docs/reference/EXIT-CODES.md` | `test_enforce.py` |
| Catalogs/workflow files | Three views, CI inventory, completeness | Stable IDs and file hashes | `test_engine.py`, `test_phase3.py` |
| Frontmatter + sync map | Master/human inventories; JSON + Mermaid graph | References and actual mapped paths | `test_engine.py`, `test_phase3.py` |
| Local tool matrix/prompt files | Allowlist, prompt and model inventories | No LLM, shell or network tool execution | `test_local_tools.py`, `test_agent_example.py` |

## The generation contract
Every generator declares its exactness and its limits in one table in `scripts/doc-sync/engine.py`:
`exact` is the authoritative record of what it reads, `heuristic` is a bounded extraction that can
miss something of the kind it reports. The label and its limits are written into every generated
Markdown file, so a reader can judge the output without reading the generator; a heuristic
generator emits an advisory `generator.heuristic` finding by default, which the phase severity or
a `[severity]` pin can turn down but never turns into silent trust. No mapping may name a
generator without a label, and the label table is asserted to match the generator registry.

Per-language references follow the same rule and one more: a language gets a generator only where
its **own tool** can be integrated — AutoDOC never hand-rolls a parser for a language whose
toolchain exists — and a language with no generator is reported as **L0** (file and manifest facts
only) rather than guessed at. The runner uses a scrubbed environment, offline flags where supported,
no shell and a timeout; Rust runs from a temporary copy to keep normal Cargo outputs and lockfiles
out of the inspected checkout. This is environment isolation, not an OS security sandbox; JSDoc/
TypeDoc config or plugins and Rust build scripts/procedural macros may execute. Python is extracted in-process with the interpreter's
own parser; Go integrates `go doc -all .`; JavaScript uses JSDoc `-X`; TypeScript uses TypeDoc
`--json`; and Rust uses nightly rustdoc JSON through `cargo rustdoc`. Missing tools are reported
with their reason. A reference produced by an external toolchain is printed on demand and never
committed to a drift-checked target, because the same repository on two machines would disagree.

## The event contract
`CONTROL/metadata/TRIGGERS.json` is the one place that says when AutoDOC runs: the local hook
(convenience, bypassable), the pull request (the only gate, and never needing the network), the
default branch (a generated-diff artifact, never a bot commit), the schedule (triage only) and a
release tag (a snapshot). `triggers.py --check` holds the declaration to the repository — every
workflow file must be claimed, every declared command must resolve, exactly one event may block,
and a required check may not be filtered — and the rendered form is a mapped generated document,
so editing a workflow without updating the model fails the build rather than silently changing
when checks run. The scheduled workflow is built to match: each check reports even when an earlier
one fails, and a single closing step makes the run red for triage. The external link check is the
only thing that opens a network connection, it is scheduled, rate-limited and warn-only, and it is
deliberately absent from `make ci`.

## Implemented validators
Metadata (required fields, enums, unique IDs), relationship IDs and supersedes cycles,
ownership path authority, critical-date freshness, source/target mapping integrity, generator
byte drift, path-based human review impact, offline local links, key markers and tribal phrases.
`stub_check.py` also fails **approved** human documents with no section and no content beyond
their title, so a placeholder index cannot inflate the inventory or the health counts; drafts
warn instead. For the four canonical migration-document titles it also checks for the template's
three required sections and unchanged prompt sentences, routing drafts to `placeholders` and
approved documents to `stubs`. The direct checker warns on drafts and fails approved documents;
`make ci` applies the existing phase and pin severity to those families. This is structural only:
no truth, adequacy, completeness or reversibility is inferred. Generated targets are excluded because byte drift validates them, not
prose volume. The catalog index is validated against `CATALOG-SCHEMA.json` plus rule cross-checks (unknown
flags, mixed sentinels, core types without a reason or with an undetectable predicate, duplicate
ids, missing templates, and a vocabulary that no profiler detector backs). Predicate tokens are checked against their
own vocabularies too: `kind:<id>` must be a declared kind, `phase>=<id>` a declared phase, and an
`obligation:<id>` a declared obligation. The resolver derives `audience:<reader>` from the catalog's
validated `reader`: a matching declared audience is true, a mismatch in a non-empty declared set
is false/not-applicable, an empty set is unknown, and assess-only entries are exempt. A kind is
either detected from files by a detector that states its limits or explicitly declaration-only
with a reason no file can tell.
CI artifacts contain actual test output; `make evidence` packages a scoped **unsigned** hash-
verifiable record. `make ci` also checks staged impact locally, or compares HEAD with `BASE`
when there is no staged change (CI supplies the PR base SHA). It uses pytest; no
line-coverage plugin/percentage is configured.

## Mapped but template-only
The 265 types have canonical/blank/synthetic-example templates, but a type is **not** an
instantiated document. A human-authored instance is checked for ownership/freshness only once
created under a controlled path; source-change review requires an explicit map rule. There is
no deterministic extractor for ADR rationale, risk acceptance, user guides, incident analysis,
security policies or other judgment-heavy catalog entries. Do not treat template completeness
as production documentation coverage.

## Partially supported
The task API source is a JSON registry, **not** OpenAPI. SQL is a deliberately narrow SQLite
subset; unsupported DDL fails. The alert file is not connected to production monitoring.
Dependencies are declared requirements, not installed packages, licenses or transitive SBOM.
External links are not checked offline. Local agent demos have no LLM or network provider.
Git-derived living-state blocks cannot infer a human next action. Code inventory cannot
establish runtime semantics or guarantee every dynamic symbol is represented.

## Explicitly not implemented

| Input | Status and reason |
| --- | --- |
| OpenAPI / AsyncAPI | `NOT_IMPLEMENTED`: no checked-in contract or parser mapping. |
| General YAML alerts or tool policies | `NOT_IMPLEMENTED`: examples accept only the JSON-compatible YAML subset; YAML syntax without a bounded parser fails. |
| Arbitrary SQL dialects and DDL | `NOT_IMPLEMENTED`: the SQLite demo parser only handles its declared CREATE TABLE subset; it refuses partial dictionaries. |
| Docker, Kubernetes and vendor APIs | `NOT_IMPLEMENTED`: no tested extractor or authoritative input/credential integration is configured. |
| External link reachability, live monitoring, signed evidence | `NOT_IMPLEMENTED`: offline guard only checks local links; there are no monitors, signing keys or approval policy. |

## Not supported / integration needed
OpenAPI/AsyncAPI and CLI parsing need real contracts plus tests. Docker/Kubernetes extractors
need project-specific parsers. Cloud cost, deployed services and vendor APIs need
scoped credentials and owners. Signed provenance requires key management and a verification
policy; GitHub issue creation and CODEOWNERS branch protection need owner approval. No
semantic prose correctness, line coverage or audit certification is claimed. Scope and effort
are project-dependent; do not quote estimates as measured facts.

## Known environment constraints
The go-task binary is not installed in this sandbox. The Taskfile delegates to Make but
`task ci` was not executable here; `make ci` is the canonical local verification path. Node
v22.22.3 is present, but `jsdoc`, `typedoc`, `cargo`, `rustc` and `rustdoc` are not installed here;
the integrations are tested with fake executables and no toolchain is installed for this change.
Python 3.11–3.15 are tested in the workflow matrix and `pyproject.toml` declares `>=3.11,<3.16`; runtime extraction uses the standard library. The owner selected Apache-2.0 on 2026-10-01 (`LICENSE`), so release snapshots are gated by the tag and a clean tree. Tagged release runs build wheel/sdist artifacts without publishing them to PyPI.
