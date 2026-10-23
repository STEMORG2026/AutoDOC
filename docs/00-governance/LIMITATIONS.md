---
id: DOC-P3-GOV-001
title: "AutoDOC limitations"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
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
# AutoDOC limitations

AutoDOC has 265 *possible* document types, but only configured, tested extractors generate
facts. All other types are templates and human-owned instances subject to metadata, ownership,
review-path and freshness checks **when instantiated and mapped**; templates alone are not
inventoried human documents. There is no semantic proof of prose accuracy or architecture
rationale, diagram rendering, external link availability, approval or compliance.

The demo API uses a three-route JSON registry, **not** OpenAPI. SQL accepts only the documented
SQLite CREATE TABLE subset; unknown statements fail. Dependencies are declared PEP 621
requirements, not installed/transitive packages or known license information; `make audit` is an
operator-run network check with the optional `audit` extra, not part of the offline gate. Alerts are
versioned example declarations, not live monitoring. The agent examples have no LLM or network.
Cloud costs, Kubernetes state, SaaS/vendor APIs, real model behavior and signed attestations
require independent project-owned integrations and credentials. GitHub branch protection is
not configured by a checked-in file; the license is Apache-2.0 (2026-10-01), and release-tag snapshots additionally require a `vX.Y.Z` tag checked out at the same commit.
Generated graph edges are factual references, not proof of architecture semantics.

Enforcement is only as strong as the declared phase. While no phase is declared every finding
is advisory and the exit code is `0`; a baseline suppresses findings recorded during adoption, so
`0` can mean "nothing new" rather than "nothing wrong". The report separates new findings,
baseline-suppressed findings and stale baseline entries so those two states are never conflated.
This repository pins its pre-existing structural checks (`drift`, `stubs`, `placeholders`,
`links.local`, `secrets.inline`, `tribal`, freshness) to `error` so that the policy layer did not
lower them; that choice lives in `autodoc.toml` and can be deleted to let the phase decide. The
reference integrity and manifest-aware checks (L1) cover two ecosystems only, and no L2
code-aware check exists yet, so a clean run does not mean the reference documentation is correct.

Applicability predicates come from `scripts/intelligence/profile.py`, which records **file
presence only**: a `has_public_api_surface` fact means a contract file exists, not that an
interface works, and a `false` fact means "no evidence found" rather than proof of absence.
Facts are three-valued: `unknown` is returned when no configured source could be evaluated —
an ecosystem with no reader, or no manifest at all — and a predicate over an unknown fact makes
a type **undetermined**, which is reported separately and never silently satisfied. Generated,
vendored and test-input directories (`fixtures/`, `testdata/`, `node_modules/`, virtualenvs) are
skipped and the profile lists what it skipped; a project whose shipped corpus *is* its product
would need those paths declared instead. Example and demo directories are **not** skipped, so
this repository still reports `has_public_api_surface` from `EXAMPLE-PROJECT/routes.json`. Only Python
and JavaScript have manifest readers today, so dependency questions in other ecosystems are
`unknown` rather than false. The four heuristic content scans are bounded and name their limits;
the credential scan records file paths and never values. Phase is a declaration: an undeclared
phase means advisory-only output, and the phase hint never sets enforcement. Kinds and audiences
are validated and displayed. Kind predicates are three-valued, so an undeclared kind leaves its
documents **undetermined** until the owner answers. A catalog `reader` adds an implicit
`audience:<reader>` AND predicate: a declared match is true, a non-match in a non-empty audience
is not-applicable, an empty audience is unknown, and assess-only entries are exempt. Three facts are
**declaration-only** (`handles_personal_data`, `handles_payments`, `safety_critical`): they are
facts about the world, so they carry a stated reason instead of a detector, are answered in
`[facts]`, and their documents are undetermined until they are. A trait is never read from
evidence, and an unanswered trait is never read as `false`. Profiling this repository reports `has_public_api_surface`,
`has_persistent_state`, `has_env` and `has_ai` because the synthetic examples contain those
files, which is exactly why the report demands a recorded decision instead of assuming the
project owns an API or a database. Generated references are labeled, not trusted: every generator states whether it is `exact` or
`heuristic` and what it cannot see, and a heuristic generator warns by default. Per-language
coverage is honest about its reach: Python is extracted in-process with the interpreter's parser;
Go integrates `go doc -all .`; JavaScript integrates JSDoc `-X`; TypeScript integrates TypeDoc
`--json`; and Rust uses nightly rustdoc JSON through `cargo rustdoc`. These are tool-output
references, not AutoDOC parsers: local JSDoc/TypeDoc configuration and plugins can affect output
and may execute code; Rust requires a root Cargo library manifest and offline-resolvable dependencies,
and build scripts
or procedural macros may execute in a temporary project copy. The runner scrubs environment
variables, uses a timeout and does not install tools or packages, but is not an OS security sandbox.
Missing toolchains leave that language at L0 in that run. `make docs-languages` prints availability
and limits. External-tool references are printed on demand and never committed: the same repository
on two machines could disagree, and an environment-dependent generated target cannot be drift-checked. What runs when is declared, not inferred: `CONTROL/metadata/TRIGGERS.json` names each event,
its commands, what may block and what may only warn, and `triggers.py --check` verifies the
workflows, the hook and the Makefile against it. The workflow reader is line-based and reads names,
trigger keys, filters and job names; a job produced by a reusable workflow, or a workflow the
reader cannot parse, is reported as unverified rather than passed. The scheduled run is triage: it
surfaces overdue review, drift and link rot for a human, and it is not a merge gate. The external
link check is honest about its reach — it is line-based (fenced code is skipped, indented code and
HTML bodies are read as prose), it opens one connection at a time with a per-host delay and a cap,
treats 401/403/405/429 as reachable, skips local and reserved example hosts as documented rather
than deployed, and never fails a build unless an owner asks for `--strict`. The catalog tiers are a reviewable proposal, not a
measurement of any project's obligations, and a member of a tier is a *possible* document.
