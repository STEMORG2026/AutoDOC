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
last_updated: 2026-10-23
auto_generated: false
---
# Next action

## Immediate focus
PR #18 merged PRD1's production-readiness commands at `1361ba2`; PR #19 merged the installed-wheel
dogfood fixes at `06ccb0a`; PR #20 merged the post-PR19 state reconciliation at `f2e8698`; PR #21
merged PRD2's closeout at `f8e2c76`, and post-merge `make ci` passes. The closeout records the
existing `LICENSE` and `CHANGELOG.md` as the homes for the two
beta-gated core rows (`DOC-A10-008`, `DOC-A15-003`), so the installed `autodoc promote --to beta`
preview exits 0 with `Delta: no catalog requirement changes`. The owner then authorized the
promotion: PR #24 wrote `phase = "beta"` and merged at `8f9c709`, and the repository reports
`beta-ready: 17/17`. The closeout
also adds the optional `audit` extra and
operator-run `make audit`, fixes readiness so a missing declared path is counted as open rather
than acknowledged, and defaults `enforce.collect_findings()` to the tool checkout. `make ci` passes
(307 tests + 190 subtests, wheel/sdist and clean-install smoke for all seven commands, unsigned
evidence hashes verified); `make audit` with pip-audit 2.10.1 reports no known vulnerabilities.

The proposed `0.3.0` and Beta classifier record no owner approval. D-007 remains unselected;
D-009's external dogfood was executed but its formal acceptance/record remains open. D-010's
mechanism is implemented and its first run is recorded in `state/DEBT.md`; formal closure remains
owner-optional. Do not publish to PyPI or close any paused session by inference; the beta
promotion is merged, and release/tag decisions remain owner-only.

D-007 (evidence signing) remains deferred and non-gating. D-009 (external dogfood) was executed
against the installed wheel and five additional repositories; its formal owner acceptance/record
remains open. D-010's operator-run scanner now exists (`make audit`); its first run found no known
vulnerabilities, and formal closure remains owner-optional. PRD1, PRD2, 912C, BETA and EVOLVE
are merged but not closed; C4R7 remains paused after PR #12; B71a remains paused after PR #11;
627F remains paused after PR #13; 894B remains paused after PR #14. Merging did not explicitly
close those sessions.
The release workflow builds temporary GitHub Actions artifacts only; PyPI publishing remains
unauthorized.

PR #11 merged at `52d1b79` on 2026-10-21; this did **not** close B71a, which remains paused awaiting
the owner's explicit close. The migration-prose checks remain structural only, not semantic or
reversibility claims. A real OpenAPI contract remains deferred until the demo source implements
one. Existing env/alert references are example-only; do not claim deployed monitoring. The catalog
applicability review is done — recorded 2026-10-01 (see Owner decisions below).

## Landed — `autodoc evolve`
EVOLVE's owner-requested safe autoevolution command merged in PR #26 at `c0f90e0` on
`feat/autodoc-evolve` from `master` `249c2aa`. The command is read-only by default; `--write`
refreshes generated drift; `--write --allow-add` creates missing required documents as
unregistered drafts. It never registers/approves a draft, overwrites an existing document, or
edits the phase/profile/decisions/catalog. Post-merge `make ci` passes 315 tests + 188 subtests.
EVOLVE is paused awaiting the owner's explicit closure; no release or session closure is included.
`autodoc evolve-catalog` remains a separate unopened scope.

## Owner decisions
Done: the license is Apache-2.0 (owner decision, 2026-10-01): canonical text in `LICENSE`, SPDX
expression in `pyproject.toml`, decision record in `docs/00-governance/LICENSE-DECISION.md`.
Release snapshots are no longer gated on the licence; they still require a `vX.Y.Z` tag checked
out at the same commit. Done: the core list and the five profiles are owner-reviewed
(2026-10-01) — `owner_reviewed` is recorded in `CONTROL/metadata/CATALOG-RULES.json` and
`PROFILES.json`, `docs/00-governance/CORE-LIST-REVIEW.md` is `approved`, and every applicable
core decision is closed (the resolver reports 17/17 beta-ready with 0 open and 0 invalid under
the `oss-library` profile). Remaining
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
thread**; D-003 merged through PR #16 and its production-readiness follow-up through PR #18,
while D-007 remains unselected and D-009's dogfood execution awaits formal acceptance. Promotion to
`beta` is written and merged in PR #24 at `8f9c709` (the preview showed no requirement blockers);
release/tag/PyPI remain separate owner decisions. D-004 and D-002 were the earlier
owner-selected follow-up and are now merged by PR #14. One debt item closed on
2026-10-21 without a decision: **D-001** (catalog count drift) — the prose numbers were corrected
and `tests/test_catalog_counts.py` now derives them from the indexes, so a stale count fails `make
ci`; D-010's operator-run scanner is now available as `make audit` and its first run found no known
vulnerabilities.

## Shrink before detection (owner decision, 2026-10-01)
1. Done. The approved-stub check failed on 28 title-only placeholders and they were retired;
   controlled documents went from 92 to 64 without losing any content.
2. Done. Classification rules moved into `CATALOG-RULES.json`, a catalog schema plus validator
   were added, `priority` was replaced by a hand-picked core tier with detectable `applies_when`
   predicates, and `profile.py` + `recommend.py` evaluate them against recorded decisions.
3. Done. Context schema, phase ladder and three-valued facts: undeclared phase is advisory, so
   **nothing fails here yet by design**. `autodoc promote` now performs an explicit phase change
   with the target delta shown before writing; it does not infer a phase from history.
4. **Owner decisions pending, in order:**
   - Done: the phase is declared (`build`, 2026-09-30) and kinds too (`library`); the evidence
     for both comes from `make docs-hint` and the declaration is what counts.
   - Done (2026-10-01): the 24-type core list and the phasing in `CATALOG-RULES.json` are
     owner-reviewed, and all 12 applicable core decisions are recorded (`[instantiated]`,
     `[satisfied_by]`; the last one closed by declaring `has_persistent_state` false with a
     reason) — the resolver reports 17/17 beta-ready with 0 open and 0 invalid. Three core types
     (`PII inventory`, `Cardholder data flow`, `Hazard analysis`) remain gated by declared
     traits and apply only once the owner answers. The demo-only facts
     (`has_public_api_surface`, `has_http_api`, `has_persistent_state`, `has_env`, `has_ai`)
     are declared false with reasons in `autodoc.toml`, and the detector no longer matches
     its own source.
   - Kinds, traits and the selected D-004 reader gate are implemented on `master` after PR #14:
     `kind:` and `phase>=` are three-valued; `handles_personal_data`, `handles_payments`,
     `safety_critical` remain declaration-only. A catalog `reader` is an implicit AND audience
     token (match=true, non-match in a non-empty declaration=false/not applicable, empty=unknown;
     `assess` exempt), confirmed by the owner and recorded in ADR-014.
5. Done. Enforcement is one policy: `scripts/intelligence/enforce.py` runs obligations and the
   structural families at the severity the declared phase sets, with a baseline for adoption,
   documented exit codes, a pre-push hook and a dry-run branch-protection helper. `make ci` runs it.
6. Partly done. Per-language references: Python is extracted in-process (exact), Go uses `go doc`,
   and the merged D-002 implementation adds JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON
   through `cargo rustdoc`; these external references are on-demand and report missing tools as L0
   for that run. Local JSDoc, TypeDoc and Rust toolchains are absent; fake executables cover the integrations.
   The installed `autodoc init` creates ten draft foundations and can record an initial
   phase/profile declaration; `autodoc adopt` is a read-only filename heuristic; `autodoc add`
   instantiates one catalog type; and `autodoc promote` applies an explicit declared-phase change
   after showing its delta. D-003 template rendering merged in PR #16. Installed-wheel dogfood was
   executed against `Universal_Software_Auditor`, `ai_infrastructure`, `requests`, Flask and
   Express; it found the packaged-root path defect now fixed in PR #19. Remaining work in this
   step: a full phase-scaled adoption/baseline workflow and formal acceptance of the D-009
   evidence.
7. Done. Event triggers are declared in `CONTROL/metadata/TRIGGERS.json` and verified by
   `triggers.py --check` (in `make ci`): one blocking event, one required check, no undeclared
   workflow, no filtered required check, and no network from a gate. The scheduled workflow reports
   every check and summarises once; the external link check is scheduled, rate-limited and
   warn-only. Next in this direction: adopters' repositories need their own trigger model, which is
   part of `adopt` in step 6.

A heuristic generator may warn by default only if its output names what it cannot see.
