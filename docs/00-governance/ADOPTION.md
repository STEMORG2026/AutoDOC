---
id: DOC-GOV-001
title: "AutoDOC self-adoption and applicability"
type: REC
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-09-26
next_review: 2027-03-25
source_of_truth: human
supersedes: null
related: ["DOC-ARC-001", "DOC-CAT-001"]
criticality: high
review_days: 180
last_verified: 2026-09-26
last_reviewed: 2026-09-26
last_updated: 2026-11-04
auto_generated: false
---
# AutoDOC self-adoption and applicability

## Purpose and scope
AutoDOC adopts its own governance for its actual code and bounded local demonstrations. This is a **draft selection**,
not a claim that every catalog type is instantiated or reviewed — the core list and the five
profiles themselves were owner-reviewed on 2026-10-01 (`owner_reviewed` in
`CONTROL/metadata/CATALOG-RULES.json` and `PROFILES.json`; review page
`docs/00-governance/CORE-LIST-REVIEW.md`). The repository owner
`@Er-Sajan-PLG` is the designated primary owner in `CONTROL/metadata/OWNERSHIP-MATRIX.yaml`;
no backup, security approver or external auditor has been assigned.

The installable Python distribution exposes this engine through `autodoc check`, `generate`,
`adopt`, `init`, `add`, `promote`, `evolve` and `templates`; it keeps bundled policy/catalog assets
separate from the project path being checked. `autodoc adopt` plans a phase-scaled adoption from
the declared context or a `--phase`/`--profile` preview, reports open required and
existing-but-unregistered documents, names undetermined declarations, shows the phase ladder, and
can write the adoption baseline with `--write-baseline`; the preview writes no declaration and the
baseline never records configuration errors or `secrets.inline`. `autodoc templates` renders
catalog variants on demand into the selected project's ignored `build/TEMPLATES/` tree; rendering
does not instantiate or adopt a document. `autodoc add` instantiates one type in the project, and
`autodoc promote` previews the enforcement delta before changing the declared phase; neither
records an owner decision on the owner's behalf. `autodoc evolve` plans safe updates and can create
missing required documents as drafts, but it never registers, approves or counts them as
compliant. It is a CLI, not a hosted service. The package is built and tested as wheel/sdist and is
published to PyPI from a tag through OIDC trusted publishing (`autodoc-docs` 0.4.0 is current);
adoption remains an explicit configuration and review process, not an automatic claim
that a project is governed.

## Selected document types

| Catalog type | Instance | Why applicable |
| --- | --- | --- |
| `DOC-A03-005` (ADR) | Not yet instantiated | Record material future architecture changes |
| `DOC-A09-005` (Contributing guide) | `CONTRIBUTING.md` | Repo contribution process |
| `DOC-A11-001` (Test strategy) | Not yet instantiated | Test scope and confidence need an owner review |
| `DEV-B04-001` (System overview) | `DOC-ARC-001` | The sync engine has trust and data-flow boundaries |
| `DEV-B11-003` (Freshness policy) | `CONTROL/policies/FRESHNESS-SLA-POLICY.md` | Calendar review rules |
| `DEV-B09-001` (Agent instructions) | `AGENTS.md` | Agent working context |
| `DEV-B09-010` (Agent memory) | `AGENT-MEMORY.md` | Existing session patterns and pitfalls |
| `DEV-B09-014` (Agent anti-patterns) | `ANTI-PATTERNS-FOR-AGENT.md` | Existing agent guardrails |
| `DEV-B11-002` (Ownership matrix) | `CONTROL/metadata/OWNERSHIP-MATRIX.yaml` | Existing owner and path matrix |
| `DOC-A15-004` (Release notes) | `CHANGELOG.md` | Existing release history |
| `DOC-A22-001` (User guide) | `QUICK-START.md` | Existing install and usage guide |
| `DEV-B03-003` (Risks and dependencies) | `SECURITY.md`, `CONTRIBUTING.md`, `docs/00-governance/LIMITATIONS.md`, `docs/adr/0001-zero-runtime-dependencies.md` | Existing security, dependency-policy, limitation and rationale records |
| `DEV-B05-003` (Error handling) | `docs/reference/EXIT-CODES.md` | Existing exit-code and tool-failure contract |
| `DOC-A22-005` (Troubleshooting guide) | `docs/reference/TROUBLESHOOTING.md` | New guide for CLI failures, exit codes and diagnosis |
| `DOC-A10-007` (Quality gates) | `docs/reference/QUALITY-GATES.md` | New record of blocking, advisory and release checks |
| `DOC-A11-002` (Test plan), `DOC-A11-003` (Unit test specification), `DOC-A11-004` (Integration test specification), `DEV-B07-002` (Acceptance criteria), `DEV-B07-003` (Test results) | `docs/00-governance/TEST-PLAN.md` | One plan covering layers, unit and integration specifications, acceptance criteria and result retention |
| `DOC-A10-002` (SBOM), `DOC-A10-003` (Build provenance), `DOC-A10-006` (License inventory) | `docs/00-governance/SUPPLY-CHAIN.md` | One record covering the CycloneDX SBOM, the unsigned source and release records, and the license inventory of declared dependencies |
| `DOC-A15-005` (Deployment runbook) | `docs/00-governance/RELEASE-RUNBOOK.md` | New procedure for the release path that exists: version and changelog preflight, the tag-triggered CI and trusted-publishing upload, post-publish verification, and the package-level correction path |

These catalog IDs designate **types**; instance IDs identify the actual controlled files.
Files outside the controlled Markdown paths can be useful documentation without being counted
as governed instances in `MASTER-INDEX.json`. Keep the selection table current as scope changes.

## Rollout and success criteria

Start with local generation and PR checks, then attach real project sources, assign owners,
review policies and enable protected-branch checks. Success means generated bytes match
sources, human-owned mapped records receive real review, and test evidence names its actual
commit and command. `make ci` passing alone does not grant regulatory or production status.

## Non-applicability and gaps
Enterprise privacy records, DR evidence, penetration-test reports, signed provenance,
model evaluations and vendor records cannot be inferred from local examples.
No production service or audit cycle exists here. Deployment here is a package publication rather
than a service rollout, so the deployment-runbook type is answered by the release runbook
(`docs/00-governance/RELEASE-RUNBOOK.md`), which records the tag → CI → trusted-publishing →
PyPI procedure and the package-level correction path. The catalog's separate rollback type stays
not applicable, because `has_deploy` is false: there is no environment to roll back. Test results
are answered by the test plan
(`docs/00-governance/TEST-PLAN.md`), which records where per-run results live instead of
committing a stale snapshot. API/config/schema references, agent
allowlist inventories and a scoped unsigned test-run pack demonstrate the mechanism, not
certification. Release snapshots run under the owner-selected Apache-2.0 license
(`LICENSE`, 2026-10-01). A backup reviewer and project-specific extractors remain open; the
required branch-protection check is owner-run (`make docs-require-check` prints the payload,
`APPLY=1` applies it).

## Verification and references
Check `docs/generated/CATALOG-REFERENCE.md` for the catalog inventory, and
`CONTROL/metadata/MASTER-INDEX.json` for instantiated controlled documents.
Run `python scripts/doc-control/check_ownership.py` after any ownership change.
Owner review must be recorded before changing this file from draft to approved.

## Enforcement decisions (step 6, 2026-10-01)
Enforcement is now one policy applied once: `scripts/intelligence/enforce.py` resolves each check
family's severity from `[severity]` in `autodoc.toml`, then the declared phase's block, then
`report`. Adoption gets a baseline (`autodoc-baseline.json`, written by `autodoc check
--write-baseline`, `autodoc adopt --write-baseline`, or `make docs-baseline`) so an inherited
repository can enforce only what is new and ratchet down as entries go stale. Exit codes are
documented in `docs/reference/EXIT-CODES.md`: `0` success, `1` findings, `2` usage or configuration
error. `make ci` now runs `docs-enforce`. This repository keeps its structural
gates at `error` through explicit `[severity]` pins on top of the declared `build` block;
`recommend.*` is deliberately **not** pinned — every core decision is recorded (2026-10-01), so
the phase default applies and a pin would only duplicate it.

The phase-scaled adoption plan added on 2026-11-04 is a preview of that same policy, not a second
resolver. `autodoc adopt` reports the open required set, documents that already exist at their
default path but are not registered, declarations that still leave types undetermined, and the
required set at every phase. `--phase`/`--profile` change only the plan; they never write
`autodoc.toml`. `--write-baseline` writes the same schema-1 baseline as `check --write-baseline`,
so the two entry points cannot drift, and configuration findings (exit `2`) block a write. The
adoption plan never installs CI: it prints the same one-gate event model the repository uses
(pull request blocking, local hook bypassable, scheduled network checks warn-only) for the adopter
to wire in their own repository.

## Applicability decisions (step 3, 2026-10-01)
The catalog now separates tiers: **24 hand-picked core** types (each with a recorded reason and
the phase at which it becomes required, in `CONTROL/metadata/CATALOG-RULES.json`), 49
**extended**, and 192 **contextual**. `README` was added as a type: the spec's only
every-phase document was missing from all 260 types that existed then. `priority` is gone (it was a byproduct of three
domain prefixes). A type's `applies_when` is a predicate over **three-valued facts** detected by
`make docs-profile`, never a project-type label; the 72 types with no detectable predicate are
marked `assess` and are never auto-recommended. `make docs-recommend` joins the profile with
`autodoc.toml`, and severity scales with the declared phase — undeclared is advisory; this
repository declares `beta`. `recommend.py --check` fails only what the declared phase requires.
**The core list and the phase ladder were owner-reviewed on 2026-10-01** (see the
`owner_reviewed` note in the machine files). Every applicable core type is recorded: the resolver
reports 17/17 beta-ready with 0 open decisions. The demo-only facts
(`has_public_api_surface`, `has_http_api`, `has_persistent_state`, `has_env`, `has_ai`) are
declared false with reasons in `autodoc.toml`, because the only evidence for them was the
synthetic `EXAMPLE-PROJECT` and example projects — and the listener detector no longer matches
its own source (which is why `has_network_listener` needed no override).

Since PR #14 merged, D-004 consumes catalog `reader` metadata as an implicit AND token: a matching
declared audience is true; a mismatch within a non-empty audience set is not applicable; an empty
audience is unknown; and `assess` remains exempt. ADR-014 records the owner-confirmed rule. The
merged implementation adds on-demand JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON via
`cargo rustdoc`; these are tool outputs, not custom parsers, and missing toolchains remain L0 in that
run.

## Phase 3 applicability
Environment and alert references are exercised only by the task demo. The local tool-policy
example is not an adopted service and creates no new production on-call obligations. Its
versioned matrix documents a strictly denied network/shell boundary. Catalog entries remain
possible types, not 265 instantiated governed documents.
