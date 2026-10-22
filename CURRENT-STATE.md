---
id: CURRENT-STATE-MD
title: "Current state"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "1.0"
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
# Current state

AutoDOC has a working sync map, standard-library runtime, three authoritative catalog indices,
265 catalog types, a task API demo and two local tool-policy demonstrations without an LLM or web calls.
The owner-selected D-003 migration is implemented on `arena/d5317c9e-autodoc` after PR #15 merged:
each catalog record remains the single source per type, and canonical, blank and synthetic-example
variants render on demand into ignored `build/TEMPLATES/` through Make and the installed CLI. Before
removal, all 795 generated outputs were compared byte-for-byte with the prior files; all matched.
The tracked variants are now removed, with two explanatory READMEs retained under `TEMPLATES/`.
The D-003 worktree passes `make ci` on Python 3.11 (288 tests, 190 subtests, package smoke and
unsigned evidence-hash verification); staged `make docs-staged-impact` and `pre-commit run --all-files`
also pass. Commit/push and the follow-up review PR remain. It also has an installable `autodoc` CLI with zero runtime dependencies, wheel/sdist builds,
and clean-environment install smoke coverage. Its checks validate controlled-document metadata,
generated drift, age, source-to-human-review impact, and the structure of instantiated migration
documents (required sections and unfilled template prompts, not semantic correctness). A catalog
entry represents a possible document, not a completed compliance obligation.

The demo includes structured agent context and CI can retain actual test-run evidence as an artifact.

When AutoDOC runs is declared, not implied: one event model (`CONTROL/metadata/TRIGGERS.json`,
rendered into `docs/generated/TRIGGER-REFERENCE.md`) names the local hook, the pull request, the
default branch, the schedule and a release tag, and `triggers.py --check` holds it to the workflows
in `make ci`. The pull request is the only blocking event; the one check that opens the network is
scheduled, rate-limited and warn-only.

A health command measures canonical/blank/example renderability from catalog records, instantiated docs,
deadlines and drift; it does not write template outputs.
The human inventory, relationship graph, catalog views and code/test/dependency outlines are generated.
CI packages actual test-run evidence without claiming a signed build or license approval.
The release-tag workflow fails closed if `LICENSE` is missing; the owner selected Apache-2.0 on
2026-10-01 (`LICENSE`, `pyproject.toml`, `docs/00-governance/LICENSE-DECISION.md`).

The user-selected production target — an installable Python CLI/package, not a hosted service — is
implemented on C4R7: `autodoc check/generate/adopt/init`, separate bundled tool and target-project
roots, wheel/sdist build and clean-venv smoke coverage. Python 3.11–3.15 are declared; the
supplemental CI matrix is non-blocking, while the required `AutoDOC guard / check` runs `make ci`
on Python 3.11. Tagged workflows build temporary GitHub Actions artifacts only; the package is
not published to PyPI and no publication was authorized. The local full check passed (267 tests,
190 subtests, plus wheel/sdist install smoke). PR #12 merged into `master` at `08229a0` on
2026-10-22; its required check, impact job and supplemental Python 3.11–3.15 matrix all passed on
GitHub. C4R7 remains paused because merging is not an explicit session-close instruction. B71a
also remains paused after PR #11 merged.

PR #13's post-merge reconciliation is merged at `a704752`. The owner then selected D-004 followed
by D-002 and confirmed the audience rule recorded in ADR-014. Both implementations are now on
`master` through PR #14, merged at `7a0fd47224751be04dfdc6275d2381028a6064fd` on 2026-10-22.
Required, impact and Python 3.11–3.15 GitHub checks passed. A post-merge local `make ci` also passed
on Python 3.11 (280 tests and 190 subtests); evidence hashes verify, not signatures. The 894B session
remains paused; merging did not close it. PR #15's post-merge state reconciliation merged at
`990113b` after the owner explicitly authorized it; its required guard and Python 3.11–3.15 matrix
passed (the PR impact step ran within the guard check; no separate impact status was listed). The owner
then selected D-003; implementation is complete on the assigned branch `arena/d5317c9e-autodoc`, pending push and review-PR handoff.

AutoDOC now self-hosts its catalog and workflow inventories. Catalog and control-code changes
are mapped to human adoption or architecture review; declared ownership is checked in CI.

The catalog is generated from `CONTROL/metadata/CATALOG-RULES.json` and validated against
`CATALOG-SCHEMA.json`, so document type, tier, phase, maturity and applicability are data a
reviewer can diff. `priority` is gone: it came from three domain prefixes and classified UAT as
core for every project. It is replaced by 24 hand-picked core types (three of them gated by
declared traits) — including `README`, which
was missing from all 260 types that existed then — each with a recorded reason, a detectable `applies_when` predicate
and an authored `severity_by_phase` (the phases it is off in; `phase_min` is derived, never a
second source), over 49 extended and 192 contextual types.

Which of those types count as core is now a profile, not a constant: `CONTROL/metadata/PROFILES.json`
holds `default`, `startup`, `oss-library`, `internal-service` and `regulated` as small deltas of
the default set, each addition carrying a reason and its own phases. This repository declares
`profile = "oss-library"`, which adds the code of conduct, the vulnerability-disclosure route and
the dependency policy, and drops the runbook; the addition of `License` (DOC-A10-008) states the
redistribution terms the repository now answers with Apache-2.0. Every type any profile can list passes the
admission rule — a reader question, a detectable predicate, its phases, and named checks or an
explicit template-only/human label — and `check_catalog.py` fails when one does not.

Kinds follow the same rule as phases: `profile.py` detects evidence per kind with stated limits
(and says `declaration-only` where no file can honestly tell), `make docs-hint` shows it, and the
declaration in `autodoc.toml` is what gates documents. This repository declares `kinds = ["library"]`
— the hint also offered `application`, from an example inside the repository rather than a program
it ships — which turned three undetermined kind-gated documents into two not-applicable and one
applicable. Requirements resolve as Catalog x Context: a declared context in `autodoc.toml` (phase, audience,
kinds, declared duties) against fifteen file-detected facts and three declared traits, so a
fact that cannot be read makes a type **undetermined** rather than silently satisfied. Since PR #14 merged, a catalog `reader` adds an implicit AND token `audience:<reader>`: a declared
match is true, a non-match within a non-empty audience set is false/not applicable, an empty audience
is unknown, and `assess`-only entries are exempt. Severity scales with phase, per column: `build`
warns about required docs and fails structural breakage with drift and freshness off; `beta` adds
drift and freshness as warnings; `live` and `mature` fail all four; `sunset` shrinks to the sunset
profile. This repository declares `build` (2026-09-30) and is currently build-ready **15/15**, with 0 open
core decisions; missing required documents warn rather than fail at this phase. Generated references are labeled too: each generator declares `exact` or
`heuristic` and what it cannot see, the label travels with the file, and a heuristic generator
warns by default. Per-language references integrate the language's own tool: Python uses `ast`, Go uses `go doc`,
and the merged D-002 implementation adds JavaScript JSDoc `-X`, TypeScript TypeDoc `--json`, and
nightly Rustdoc JSON through `cargo rustdoc`. The external tools run on demand with a scrubbed environment,
timeout, output validation and offline settings where supported; Rust runs from a temporary project
copy, but this is not an OS security sandbox. Missing tools are reported as L0 in that run. Here
Node v22.22.3 is present, but JSDoc, TypeDoc, Cargo, rustc and rustdoc are absent; fake executables
exercise the new integrations. `make docs-languages` reports availability and limits for the
languages this repository actually contains. Traits follow the same rule: `handles_personal_data`, `handles_payments`
and `safety_critical` are declared in `[facts]`, never inferred — no detector exists for a fact
about the world — and an unanswered trait leaves the documents that depend on it undetermined.
This repository answers all three `false` with a reason, so the PII inventory, cardholder data
flow, hazard analysis and the deeper privacy set are not applicable here.

<!-- auto:start -->
- Catalog types: 265 (not necessarily instantiated).
- Controlled docs: 70 (24 generated, 46 human-owned).
- Overdue human-owned docs: 0.
- Open gaps: see `docs/00-governance/ENGINE-COVERAGE.md`; this block does not infer intent.
<!-- auto:end -->
