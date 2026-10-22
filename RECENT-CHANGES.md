---
id: RECENT-CHANGES-MD
title: "Recent changes"
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
# Recent changes

- After PR #13 merged at `a704752`, implemented the owner-selected D-004 audience gate and D-002 JSDoc/TypeDoc/nightly Rustdoc JSON readers on `arena/894b93ee-autodoc`; local `make ci` passed (280 tests, 190 subtests). PR #14 is open and all required GitHub checks pass; it awaits owner review. External tools are absent locally and covered with fake executables.
- Merged PR #12 (`08229a0`): installable zero-runtime-dependency CLI, wheel/sdist assets, isolated project-root commands, package smoke tests, and passing Python 3.11–3.15 CI; tagged runs build temporary artifacts without PyPI publication.
- Added structural validation for canonical migration-document sections and prompts; findings route
  through the existing `placeholders`/`stubs` policy families, so CI retains phase/pin severity.
- Replaced print-only scripts with deterministic generators, drift and impact checks.
- Added example API, configuration and SQLite schema with generated references.
- Added catalogs, template variants, metadata policy and tests.
- Integrated agent context in the demo and a scoped CI test evidence artifact.
- Made example SQL schema idempotent and added measured health reporting.
- Self-adopted catalogs and CI workflows, added architecture/adoption reviews and ownership checks.
- Added AST/Markdown/manifest inventories, 260-type catalog views (the catalog held 260 then), agent tool example and scoped evidence packaging.
- Tightened demo API, config and SQL extraction to fail on unsupported contracts.
- Added described environment/alert references, Mermaid graph, local tool policy demo and JUnit-derived unsigned evidence.

<!-- auto:start -->
## Last 20 Git commits

- ea03f0b 2026-10-22 feat: add audience gating and language references
- a704752 2026-10-22 Merge pull request #13 from STEMORG2026/arena/627fcb46-autodoc
- 83e3b21 2026-10-22 docs(state): record PR 13 handoff
- bd44be4 2026-10-22 docs(state): reconcile PR #12 merge
- 08229a0 2026-10-22 Merge pull request #12 from STEMORG2026/arena/072fcb8c-autodoc
- aa375ca 2026-10-22 docs(state): refresh package readiness status
- 3cc89b2 2026-10-22 docs(state): reconcile C4R7 package readiness
- b8ba4c2 2026-10-21 test: verify installed CLI help and usage errors
- 6af0c03 2026-10-21 feat: ship AutoDOC as an installable CLI
- 52d1b79 2026-10-21 Merge pull request #11 from STEMORG2026/arena/48a62791-autodoc
- 37c698a 2026-10-21 chore(state): reconcile migration validation PR
- 0d51069 2026-10-21 feat: validate migration document prose structure
- c4a9d43 2026-10-21 Merge pull request #10 from STEMORG2026/arena/44b2fb68-autodoc
- 58641ce 2026-10-21 Close the record: PR #8 and PR #9 merged, cold-clone check, and why the merge chain stops
- 0febe31 2026-10-21 Merge pull request #9 from STEMORG2026/arena/44b2fb68-autodoc
- a30fc5f 2026-10-21 Reconcile state for D-001: registry, index, dashboard, session handoff
- 55f70ce 2026-10-21 Record D-001's merge (PR #8, 5bbd7d8) and the post-merge cold-clone check
- 5bbd7d8 2026-10-21 Merge pull request #8 from STEMORG2026/arena/44b2fb68-autodoc
- d3ebf4a 2026-10-21 Fix D-001: correct the catalog counts and make them checkable
- 9e5155d 2026-10-21 Merge pull request #7 from STEMORG2026/arena/83bebb7f-autodoc

## Changed paths at update time

- `state/ARCHITECTURE.md`
- `state/DASHBOARD.md`
- `state/DEBT.md`
- `state/DECISIONS.md`
- `state/INDEX.md`
- `state/REGISTRY.md`
- `state/plans/README.md`
- `state/plans/agent-894B-d004-language-readers.md`
- `state/sessions/20261022-0445-894B-d004-language-readers.md`
<!-- auto:end -->
