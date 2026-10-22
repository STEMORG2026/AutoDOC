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

- Dogfooded the installed `0.3.0` wheel against AutoDOC, `Universal_Software_Auditor`,
  `ai_infrastructure`, `requests`, Flask and Express. The packaged `check --repo` path bug was
  reproduced and fixed: `[instantiated]`/`[satisfied_by]` paths now resolve against the target
  project rather than the bundled tool root. The same branch rejects duplicate instance IDs in
  `add`, corrects the `promote` empty-delta wording, and adds regression tests. Local `make ci`
  passes (304 tests + 190 subtests, package smoke, unsigned evidence hashes verified); commit
  `deec574` is open as PR #19. No release, PyPI publication, version decision or session closure is
  included.
- Added the production-readiness commands after D-003 merged in PR #16 (`a28616b`): `autodoc add`
  previews or writes one catalog document with a project-qualified instance ID and current dates;
  `autodoc promote` previews the target phase's requirement/enforcement delta and writes only the
  top-level `phase`/`phase_declared`, blocking an unforced write while required documents remain
  unresolved; `autodoc init --phase/--profile` records an explicit initial declaration. Runtime
  packaging, installed-package smoke, usage/governance/architecture/exit-code docs, generated
  metadata and changelog are updated. Local `make ci` passed (301 tests + 190 subtests, package
  smoke, evidence hashes verified—not signatures); PR #18 merged at `1361ba2`. The `0.3.0`/Beta
  version proposal still needs owner sign-off.
- After PR #13 merged at `a704752`, implemented the owner-selected D-004 audience gate and D-002 JSDoc/TypeDoc/nightly Rustdoc JSON readers; PR #14 merged at `7a0fd47`. Post-merge local `make ci` passed (280 tests, 190 subtests). PR #15 state reconciliation merged at `990113b` after explicit owner authorization; its required guard/check and Python 3.11–3.15 matrix passed, with the impact step inside the guard job. The owner then selected D-003: the 265 catalog types now render canonical, blank and synthetic-example variants on demand into ignored `build/TEMPLATES` through Make and the installed CLI. All 795 old outputs matched byte-for-byte before removal; the two explanatory READMEs remain. Targeted tests passed (70 tests, 65 subtests); `make ci` passed (288 tests, 190 subtests, package smoke, evidence hashes verified—not signatures), and the Make rendering target produced all 265 blank variants in a temporary tree. `pre-commit run --all-files` and `make docs-staged-impact` passed; full `make ci` passed on the staged tree. Commit/push and the follow-up review PR remain. External tools are absent locally and covered with fake executables.
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

- deec574 2026-10-22 fix: resolve packaged check paths and dogfood guards
- adee921 2026-10-22 docs(state): record PR 18 checks passing
- 67180ea 2026-10-22 docs(state): record PR 18 review handoff
- 6a76106 2026-10-22 feat: add document instantiation and guarded phase promotion
- a28616b 2026-10-22 Merge pull request #16 from STEMORG2026/arena/912c4060-autodoc
- 7604cee 2026-10-22 feat: render catalog template variants on demand
- ffb10fc 2026-10-22 docs(state): record owner-selected D-003 scope
- 990113b 2026-10-22 Merge pull request #15 from STEMORG2026/arena/912c4060-autodoc
- a3bc86d 2026-10-22 docs(state): clarify PR15 impact check status
- ed0a4d3 2026-10-22 docs(state): record PR15 review handoff
- d9641d3 2026-10-22 chore(state): reconcile PR 14 merge
- 7a0fd47 2026-10-22 Merge pull request #14 from STEMORG2026/arena/894b93ee-autodoc
- bbda691 2026-10-22 docs(state): record D-004 and D-002 PR handoff
- ea03f0b 2026-10-22 feat: add audience gating and language references
- a704752 2026-10-22 Merge pull request #13 from STEMORG2026/arena/627fcb46-autodoc
- 83e3b21 2026-10-22 docs(state): record PR 13 handoff
- bd44be4 2026-10-22 docs(state): reconcile PR #12 merge
- 08229a0 2026-10-22 Merge pull request #12 from STEMORG2026/arena/072fcb8c-autodoc
- aa375ca 2026-10-22 docs(state): refresh package readiness status
- 3cc89b2 2026-10-22 docs(state): reconcile C4R7 package readiness

## Changed paths at update time

- `docs/05-architecture/AUTODOC-ARCHITECTURE.md`
- `docs/META/OUTLINE.md`
- `state/BLOCKERS.md`
- `state/DASHBOARD.md`
- `state/INDEX.md`
- `state/REGISTRY.md`
- `state/plans/agent-PRD1-production-readiness.md`
- `state/sessions/20261022-1145-PRD1-production-readiness.md`
<!-- auto:end -->
