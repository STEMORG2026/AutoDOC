---
id: DEV-AGENT-005
title: "AutoDOC context snapshot"
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
# AutoDOC context snapshot

## What works
AutoDOC's versioned map generates references for the example API/config/schema, its own
catalogs/workflows, a Python AST symbol/test inventory, Markdown outline, declared dependencies,
filtered 265-type catalog views, two local tool-authorization examples, a described environment,
checked alert catalog, unsigned test-evidence pack and template completeness report. Generation is
deterministic. CI checks drift, metadata, ownership, freshness, templates, human review impact,
actual test results, and required sections/template prompts of instantiated migration documents.
That prose check is structural only; it cannot judge correctness.

## Boundaries
`EXAMPLE-PROJECT` is not a production service. The task API's route registry is not OpenAPI.
No migration documents are instantiated here; the prose check runs only when one of the recognized
migration documents exists. TypeScript, arbitrary SQL, signed build provenance, external compliance
and LLM execution are not implemented. Root `NEXT-ACTION.md` is human-owned; a Git-derived state
block cannot invent the next human priority. Branch protection still needs a repository-admin
decision; the license is Apache-2.0 (`LICENSE`), so release snapshots require only a `vX.Y.Z` tag
at the same commit.

## Commands
`make generate`, `make check`, `make test`; see `docs/.doc-sync-map.yaml` and `README.md`. The
installed CLI exposes `check`, `generate`, `adopt`, `init` (optionally with `--phase`/`--profile`),
`add` (one catalog document), `promote` (explicit phase change with its delta), and `templates`
(on-demand catalog variants).
