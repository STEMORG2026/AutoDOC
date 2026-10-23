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
last_updated: 2026-10-23
auto_generated: false
---
# Recent changes

- Started the owner-requested safe autoevolution on `feat/autodoc-evolve` from `master` `249c2aa`:
  `autodoc evolve` plans from the same context/profile/catalog/enforcement layers, is read-only
  by default, refreshes generated drift with `--write`, and creates missing required documents
  only as unregistered `status: draft` instances with `--write --allow-add`. It reports
  undetermined facts, structural findings and existing-but-unregistered documents for a human,
  never overwrites an existing file, and never edits the phase/profile/decisions/catalog. Local
  pytest passes 315 tests + 188 subtests; PR #26 merged at `c0f90e0`, and PR #27 reconciled state
  at `4230703`. The owner closed EVOLVE's session on 2026-10-23 and its plan is archived; no
  release or tag was made.
- Promoted the declared phase from `build` to `beta` on 2026-10-23 after the owner authorized the
  write and `autodoc promote --to beta` previewed no catalog requirement changes. The declaration
  reports `beta-ready: 17/17`; `make ci` passes 307 tests + 188 subtests with package smoke and
  evidence hashes, and `make audit` reports no known vulnerabilities. Removed the `stubs` and
  `freshness.review` pins because beta already sets those severities; `tribal` and
  `freshness.critical` remain deliberately stricter. Updated README, ADOPTION, CORE-LIST-REVIEW,
  architecture, tests and state. PR #24 merged at `8f9c709`; post-merge `make ci` passes 307 tests + 188 subtests and
  `autodoc check` reports `beta-ready: 17/17`. No tag, PyPI publication, version change or
  session closure is included.
- Closed the remaining beta document delta on the PRD2 closeout branch: `LICENSE` and
  `CHANGELOG.md` are recorded as the homes for `DOC-A10-008` and `DOC-A15-003`, so `autodoc promote
  --to beta` previews with no requirement blockers while the declared phase stays `build`. Added
  the optional `audit` extra and operator-run `make audit` (pip-audit 2.10.1 found no known
  vulnerabilities in the installed development environment), stopped readiness from counting
  acknowledged decisions whose declared paths are missing, and defaulted
  `enforce.collect_findings()` to the tool checkout. `make ci` passes 307 tests + 190 subtests,
  wheel/sdist and clean-install smoke; PR #21 merged at `f8e2c76` and post-merge `make ci` passes.
  No phase write, release, PyPI publication or session closure is included.
- Dogfooded the installed `0.3.0` wheel against AutoDOC, `Universal_Software_Auditor`,
  `ai_infrastructure`, `requests`, Flask and Express. The packaged `check --repo` path bug was
  reproduced and fixed: `[instantiated]`/`[satisfied_by]` paths now resolve against the target
  project rather than the bundled tool root. The same branch rejects duplicate instance IDs in
  `add`, corrects the `promote` empty-delta wording, and adds regression tests. Local `make ci`
  passes (304 tests + 190 subtests, package smoke, unsigned evidence hashes verified); commit
  `deec574` merged in PR #19 at `06ccb0a`, and post-merge `make ci` passes. No release, PyPI
  publication, version decision or session closure is included.
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

- 4230703 2026-10-23 Merge pull request #27 from STEMORG2026/docs/post-pr26-reconciliation
- 824b3eb 2026-10-23 docs(state): reconcile PR 26 merge
- c0f90e0 2026-10-23 Merge pull request #26 from STEMORG2026/feat/autodoc-evolve
- e649ab1 2026-10-23 docs(state): record EVOLVE PR 26
- 32a9cdd 2026-10-23 feat: add safe autodoc evolve command
- 249c2aa 2026-10-23 Merge pull request #25 from STEMORG2026/docs/post-pr24-reconciliation
- 26e73ab 2026-10-23 docs(state): reconcile PR 24 merge
- 8f9c709 2026-10-23 Merge pull request #24 from STEMORG2026/chore/promote-beta
- ea31ace 2026-10-23 chore: promote declared phase to beta
- 3fda35b 2026-10-23 Merge pull request #23 from STEMORG2026/test/phase-agnostic-shipped-checks
- 9ae8131 2026-10-23 test: derive shipped-phase assertions from the declaration
- f040105 2026-10-23 Merge pull request #22 from STEMORG2026/docs/post-pr21-reconciliation
- a7a8e07 2026-10-23 docs(state): reconcile PR 21 merge
- f8e2c76 2026-10-23 Merge pull request #21 from STEMORG2026/feat/production-readiness-closeout
- 28188c3 2026-10-23 docs(state): record PR 21 open and checks passing
- a24c46a 2026-10-23 feat: close production-readiness gaps
- f2e8698 2026-10-22 Merge pull request #20 from STEMORG2026/docs/post-pr19-reconciliation
- a97b320 2026-10-22 docs(state): reconcile PR 19 merge
- 06ccb0a 2026-10-22 Merge pull request #19 from STEMORG2026/fix/dogfood-packaged-root
- a1ff829 2026-10-22 Merge branch 'master' into fix/dogfood-packaged-root

## Changed paths at update time

- `state/ARCHITECTURE.md`
- `state/BLOCKERS.md`
- `state/DASHBOARD.md`
- `state/DEBT.md`
- `state/DECISIONS.md`
- `state/INDEX.md`
- `state/REGISTRY.md`
- `state/archive/plans/2026-10/README.md`
- `state/archive/plans/2026-10/agent-EVOLVE-evolve-command.md`
- `state/sessions/20261023-0751-EVOLVE-evolve-command.md`
<!-- auto:end -->
