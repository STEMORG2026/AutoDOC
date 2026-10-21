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

- Added an installable zero-runtime-dependency CLI with bundled wheel/sdist assets, isolated project-root commands, package smoke checks and Python 3.11–3.15 CI; tagged runs build temporary artifacts without PyPI publication.
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

- 6af0c03 2026-10-21 feat: ship AutoDOC as an installable CLI
- 52d1b79 2026-10-21 Merge pull request #11 from STEMORG2026/arena/48a62791-autodoc

## Changed paths at update time

- `docs/META/CODE-INVENTORY.md`
- `scripts/test_package.py`
- `state/DASHBOARD.md`
- `state/INDEX.md`
- `state/REGISTRY.md`
- `state/plans/agent-C4R7-python-package-readiness.md`
- `state/sessions/20261021-1820-C4R7-python-package-readiness.md`
<!-- auto:end -->
