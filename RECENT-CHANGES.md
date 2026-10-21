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

- 52d1b79 2026-10-21 Merge pull request #11 from STEMORG2026/arena/48a62791-autodoc

## Changed paths at update time

- `.github/workflows/docs-guard.yml`
- `.github/workflows/release.yml`
- `.gitignore`
- `CHANGELOG.md`
- `CONTRIBUTING.md`
- `CONTROL/metadata/TRIGGERS.json`
- `Makefile`
- `QUICK-START.md`
- `README.md`
- `Taskfile.yaml`
- `docs/.doc-sync-map.yaml`
- `docs/00-governance/ADOPTION.md`
- `docs/00-governance/ENGINE-COVERAGE.md`
- `docs/05-architecture/AUTODOC-ARCHITECTURE.md`
- `docs/META/CODE-INVENTORY.md`
- `docs/META/DEPENDENCIES.md`
- `docs/META/OUTLINE.md`
- `docs/META/TEST-INVENTORY.md`
- `docs/generated/AUTOMATION-REFERENCE.md`
- `docs/generated/TRIGGER-REFERENCE.md`
- … and 11 more; use git diff --cached --name-only.
<!-- auto:end -->
