---
id: NEXT-ACTION-MD
title: "Next action"
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
# Next action

## Immediate focus
Post-merge state reconciliation is proposed in PR #13 from `arena/627fcb46-autodoc`; its required
gate and Python 3.11–3.15 jobs pass, and owner review is pending. The user-selected installable
Python CLI/package is implemented and merged by PR #12 at `08229a0` (2026-10-22): wheel/sdist
builds, `autodoc check/generate/adopt/init`, distinct tool and target-project roots, and clean-venv
smoke tests. Local `make ci` passed (267 tests, 190 subtests);
the required `AutoDOC guard / check`, impact job and supplemental Python 3.11–3.15 matrix all
passed on GitHub. C4R7 remains paused; merging did not explicitly close the session. The release
workflow builds temporary GitHub Actions artifacts only; PyPI publishing was not authorized.

No follow-up from the five non-gating P-006 deferrals has been selected. D-004 (`audience` consumer)
is first if any P-006 item is chosen; other listed work includes JS/TS + Rust toolchains, external
repository dogfood, on-demand template rendering and evidence signing. Ask the owner to choose the
next bounded item; do not implement one or publish to PyPI by inference.

PR #11 merged at `52d1b79` on 2026-10-21; this did **not** close B71a, which remains paused awaiting
the owner's explicit close. The migration-prose checks remain structural only, not semantic or
reversibility claims. A real OpenAPI contract remains deferred until the demo source implements
one. Existing env/alert references are example-only; do not claim deployed monitoring. The catalog
applicability review is done — recorded 2026-10-01 (see Owner decisions below).

## Owner decisions
Done: the license is Apache-2.0 (owner decision, 2026-10-01): canonical text in `LICENSE`, SPDX
expression in `pyproject.toml`, decision record in `docs/00-governance/LICENSE-DECISION.md`.
Release snapshots are no longer gated on the licence; they still require a `vX.Y.Z` tag checked
out at the same commit. Done: the core list and the five profiles are owner-reviewed
(2026-10-01) — `owner_reviewed` is recorded in `CONTROL/metadata/CATALOG-RULES.json` and
`PROFILES.json`, `docs/00-governance/CORE-LIST-REVIEW.md` is `approved`, and every applicable
core decision is closed (the resolver reports 15/15 build-ready with 0 open). Remaining
(updated 2026-10-21, after the fix): **nothing on protection** — the owner applied P-007-A
(ruleset `main` carries `deletion`, `non_fast_forward` and required check `AutoDOC guard /
check` `strict: true`; the signed-commits and CodeQL rules are removed), the live rules were
verified, PR #3 (`04f7386`) and PR #4 (`87be33b`) merged, and the post-merge continuity test
passed on a cold clone of `master` (B-003 cleared). ADR-011 records the mechanism (ruleset
`main`; `APPLY=1 make docs-require-check` is superseded and stays a dry-run reference). The
housekeeping that remained — closing the sessions (ADR-009) — is done: the owner closed all eight
on 2026-10-21 ("continue from this here and also close the session"), their plans are archived
under `state/archive/plans/2026-10/`, and their closing entries quote the instruction. A90c's
D-001 session was subsequently closed on 2026-10-21 by the owner's explicit instruction
"Close A90c, then proceed"; its plan is archived too. **Nothing is pending on the protection/D-001
thread**; the optional P-006 follow-ups listed in `state/DEBT.md` are the only deferred ideas, and
promotion to `beta` stays a deliberate event (cliff 2). One debt item closed on
2026-10-21 without a decision: **D-001** (catalog count drift) — the prose numbers were corrected
and `tests/test_catalog_counts.py` now derives them from the indexes, so a stale count fails `make
ci`; the only `open` debt left is D-010 (vulnerability scanning, low, needs a network scanner).

## Shrink before detection (owner decision, 2026-10-01)
1. Done. The approved-stub check failed on 28 title-only placeholders and they were retired;
   controlled documents went from 92 to 64 without losing any content.
2. Done. Classification rules moved into `CATALOG-RULES.json`, a catalog schema plus validator
   were added, `priority` was replaced by a hand-picked core tier with detectable `applies_when`
   predicates, and `profile.py` + `recommend.py` evaluate them against recorded decisions.
3. Done. Context schema, phase ladder and three-valued facts: undeclared phase is advisory, so
   **nothing fails here yet by design**, and `save`/`promote`-style phase changes are a later step.
4. **Owner decisions pending, in order:**
   - Done: the phase is declared (`build`, 2026-09-30) and kinds too (`library`); the evidence
     for both comes from `make docs-hint` and the declaration is what counts.
   - Done (2026-10-01): the 24-type core list and the phasing in `CATALOG-RULES.json` are
     owner-reviewed, and all 12 applicable core decisions are recorded (`[instantiated]`,
     `[satisfied_by]`; the last one closed by declaring `has_persistent_state` false with a
     reason) — the resolver reports 15/15 build-ready with 0 open. Three core types
     (`PII inventory`, `Cardholder data flow`, `Hazard analysis`) remain gated by declared
     traits and apply only once the owner answers. The demo-only facts
     (`has_public_api_surface`, `has_http_api`, `has_persistent_state`, `has_env`, `has_ai`)
     are declared false with reasons in `autodoc.toml`, and the detector no longer matches
     its own source.
   - Kinds and traits are implemented: `kind:` and `phase>=` are three-valued and now consumed,
     and `handles_personal_data`, `handles_payments`, `safety_critical` are declaration-only
     facts whose documents stay undetermined until answered. `audience` is validated and
     displayed but no predicate consumes it yet. Do not describe it as working.
5. Done. Enforcement is one policy: `scripts/intelligence/enforce.py` runs obligations and the
   structural families at the severity the declared phase sets, with a baseline for adoption,
   documented exit codes, a pre-push hook and a dry-run branch-protection helper. `make ci` runs it.
6. Partly done. Per-language references: Python is extracted in-process (exact) and Go's
   toolchain is integrated behind a probe; every other language is reported as L0 with the reason.
   The installed `autodoc init` creates ten draft foundations and `autodoc adopt` is a read-only
   filename heuristic; neither performs a full phase-scaled adoption or baseline write. Next in
   this step: add tested JavaScript/TypeScript and Rust tool integrations where justified; extend
   adoption/scaffolding with owner-reviewed phase/profile decisions; implement `promote` and `add`;
   render templates on demand instead of committing 780 variants; and dogfood on a repository
   that is not this one.
7. Done. Event triggers are declared in `CONTROL/metadata/TRIGGERS.json` and verified by
   `triggers.py --check` (in `make ci`): one blocking event, one required check, no undeclared
   workflow, no filtered required check, and no network from a gate. The scheduled workflow reports
   every check and summarises once; the external link check is scheduled, rate-limited and
   warn-only. Next in this direction: adopters' repositories need their own trigger model, which is
   part of `adopt` in step 6.

A heuristic generator may warn by default only if its output names what it cannot see.
