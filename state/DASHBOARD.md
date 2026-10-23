# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-23T04:40Z · **Reconciled by:** PRD2 (session `20261022-1415-PRD2`,
post-merge reconciliation) · **Base tip:** `f8e2c76` on `master` (PR #21 merged the
production-readiness closeout); post-merge `make ci` passes 307 tests + 190 subtests. PRD2 is
**PAUSED — merged; awaiting explicit owner closure**, as are PRD1 and 912C; release and beta
promotion decisions remain owner-only.

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `master` at `f8e2c76` (PR #21 merged the closeout; local `master` synced). No implementation branch is active; this state-only reconciliation branch is awaiting review |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 192 contextual · 265 types (209 A + 56 B) · 16 detected facts · 3 declared traits — the prose numbers are checked against the indexes by `tests/test_catalog_counts.py` (D-001 fixed) |
| Build-ready | **17/17** applicable core types under the `oss-library` profile · open core decisions **0** · invalid decisions **0** |
| Promotion cliff | **None on the preview:** `autodoc promote --to beta` exits 0 with `Delta: no catalog requirement changes` after `LICENSE` and `CHANGELOG.md` were recorded as the homes for `DOC-A10-008` and `DOC-A15-003`. The phase remains `build`; writing the promotion is an owner decision |
| Stack | Python 3.11–3.15 declared, **zero runtime dependencies**; build/pytest/pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 70 controlled Markdown documents (24 generated, 46 human-owned); 28 mapped generated targets in total (four non-Markdown); 265 catalog types can render all 795 variants on demand, none checked in. PRD1 adds single-document instantiation and guarded phase promotion. |
| Tests | Post-merge `master` `make ci` passes on Python 3.14.8: 307 tests + 190 subtests, wheel/sdist build + clean-install smoke (`check/generate/adopt/init/add/promote/templates`), and unsigned evidence hashes verified (not signatures). `make audit` (pip-audit 2.10.1) reports `No known vulnerabilities found` in the installed development environment. |
| CI | 5 workflows; required check `AutoDOC guard / check` remains in GitHub ruleset `main` (P-007-A, strict); supplemental Python 3.11–3.15 matrix is non-blocking; nightly freshness warn-only; tag workflow builds snapshot + wheel/sdist artifacts, no PyPI publish |

## Active agents

`PRD2` — session `20261022-1415-PRD2` (**PAUSED — merged; awaiting explicit owner closure**):
recorded `LICENSE` and `CHANGELOG.md` as the homes for the two beta-gated core rows, added the
optional `audit` extra and `make audit`, stopped readiness from counting declared paths that do not
exist, and defaulted the enforcement root to the tool checkout. Previewed beta promotion is now
blocker-free, but the phase stays `build`; writing the promotion, tagging, PyPI publication and
session closure remain owner decisions. PR #21 merged at `f8e2c76`; merging did not close the
session.

`PRD1` — session `20261022-1145-PRD1` (**PAUSED — merged; awaiting explicit owner closure**):
implemented `autodoc promote` (preview/apply phase deltas, guarded write, force-only
demotion/backdate), `autodoc add` (one catalog document, root-bounded, preview by default) and
`init --phase/--profile`. PR #18 merged by the owner at `1361ba2`. Installed-wheel dogfood then
found that packaged `check` resolved `[instantiated]`/`[satisfied_by]` paths against the bundled
tool root instead of `--repo`; the follow-up also rejects duplicate instance IDs and corrects the
`promote` empty-delta wording. PR #19 merged at `06ccb0a`; PR #20 then merged the post-PR19 state reconciliation at `f2e8698`.
The `0.3.0` / Beta proposal and release decision remain owner-only. Merging did not close the
session.

`912C` — session `20261022-1011-912C` (**PAUSED — merged; awaiting explicit owner closure**):
D-003's on-demand catalog-template rendering merged in PR #16 at `a28616b`. The implementation kept
one catalog record per type, byte-matched and removed the 795 tracked variants, and exposes Make and
installed-CLI rendering into ignored `build/TEMPLATES/`. PR #15's reconciliation remains at
`990113b`; merging did not close the session.

`894B` — session `20261022-0445-894B` (**PAUSED (awaiting explicit owner closure)**): implemented
D-004 audience applicability and D-002 JSDoc/TypeDoc/nightly Rustdoc JSON readers; PR #14 merged at
`7a0fd47`. The session remains paused because the owner asked to merge, not to close it.

`627F` — session `20261022-0426-627F` (**PAUSED (awaiting explicit owner closure)**): reconciled
PR #12 after merge; PR #13's state update merged at `a704752`. The owner selected D-004 then D-002;
this is now handled by 894B. The prior merge did not explicitly close this session.

`C4R7` — session `20261021-1820-C4R7` (**PAUSED (awaiting explicit owner closure)**): added the
installable zero-runtime-dependency CLI/package, distinct tool/project roots, wheel/sdist build and
isolated installation smoke tests. PR #12 merged into `master` at `08229a0`; local `make ci` passed
(267 tests, 190 subtests), package smoke and artifact builds passed, and the required check, impact
job and Python 3.11–3.15 matrix passed on GitHub. No PyPI publication was authorized; merging did
not close the session.

`B71a` — session `20261021-1459-B71a` (**PAUSED (awaiting owner)**): migration-prose validation is
merged in PR #11 at `52d1b79`; the implementation is structural only. The session remains paused;
merging did not constitute the owner's explicit close. A90c's D-001 session was closed by the owner
at 14:59Z; its plan is archived. The nine earlier sessions remain closed.

## Alerts

**Current follow-up (2026-10-23).** PR #19 merged the installed-wheel dogfood fixes at `06ccb0a`;
PR #20 reconciled the post-merge state at `f2e8698`; PR #21 merged the production-readiness
closeout at `f8e2c76`, and post-merge `make ci` passes 307 tests + 190 subtests. The closeout
records a blocker-free beta preview, adds the operator-run audit, and fixes the invalid-decision
readiness count. The owner still needs to decide whether to write the `beta` promotion, keep
`0.3.0` / Beta, and release. 894B/627F/C4R7/B71a remain paused; 912C, PRD1 and PRD2 are merged but
not explicitly closed. D-007 and PyPI publishing remain unauthorized; D-009's external dogfood was
executed but its formal acceptance/record remains open. D-010's operator-run scanner now exists;
its formal close still needs the owner or a recorded verification.

1. **D-001 fixed (2026-10-21).** The catalog counts are no longer remembered: eleven prose claims
   were corrected and `tests/test_catalog_counts.py` derives `265 / 209 / 56 / 24 / 49 / 192` from
   `CATALOG-*/INDEX.yaml` and `CATALOG-RULES.json`; a disagreement fails `make ci`. Its limits are in
   the test docstring (three-digit totals, the word "then" marks history, a bare "N core" is
   ambiguous between the default tier 24 and the `oss-library` profile's 26).

2. **Prior sessions closed (2026-10-21).** The nine sessions closed in the earlier owner round
   remain closed. A90c was closed by the owner's explicit instruction “Close A90c, then proceed”
   at 14:59Z; its plan is archived. B71a is a new session, not a resumption, and is paused awaiting
   owner review.

3. **B-003 cleared (2026-10-21).** The owner applied P-007-A: ruleset `main` (id `25542481`) carries
   exactly `deletion`, `non_fast_forward` and `required_status_checks` → `AutoDOC guard / check`
   (`strict: true`) — ADR-011's payload as a ruleset. The `required_signatures` and CodeQL rules
   that blocked every merge are gone; PR #3, #4 and #5 merged with merge commits and their `master`
   runs are green.

4. **Post-merge continuity test passed (2026-10-21)** on a cold clone of `master` at `87be33b`:
   state-only read correct (15/15, 0 open, cliff 2, P-007 decided and executed, B-003 struck);
   cold numbers verify with system `python3` and no install (`recommend.py` 15/15;
   `check_catalog.py` valid); `make ci` exit 0 on the clone. Details in session
   `20261021-1138-A52ab`.

5. **B-001 cleared (2026-10-01)** — the owner confirmed the v1.3 page ("proceed with recomendation")
   and the recording landed: `owner_reviewed` in both machine files, page → `approved`, caveat off
   `NEXT-ACTION.md` + `ADOPTION.md`, D-011 fixed (commit `039e508`).

6. **B-002 cleared (2026-10-01)** — the owner acknowledged the decision-3 deviation and kept the
   real ADR; ADR-008 records it (commit `3ad5a57`).
7. Environment resets recur (ten recoveries on 2026-10-01, #11–#20; #21 on 2026-10-21 took the venv only)
   and one sandbox quirk: a depth-1 clone made the `doc-state-sync` hook regenerate
   `RECENT-CHANGES.md` from a one-commit history — unshallow first. Never force-push.

## Recently merged

| Date | Work | Commits |
| --- | --- | --- |
| 2026-10-23 | **Production-readiness closeout merged:** beta document homes, operator-run `make audit`, invalid-decision readiness fix and default enforcement root; post-merge `make ci` passes 307 tests + 190 subtests; no phase write, release or closure | PR #21 → `f8e2c76` |
| 2026-10-22 | **Post-PR19 state reconciliation merged:** PR #20 records PR #19, dogfood, and paused-session status; no release or closure | PR #20 → `f2e8698` |
| 2026-10-22 | **PRD1 production-readiness commands merged:** `autodoc add`, guarded `autodoc promote`, `init --phase/--profile` | PR #18 → `1361ba2` |
| 2026-10-22 | **Installed-wheel dogfood fixes merged:** target-root path resolution for `[instantiated]`/`[satisfied_by]`, duplicate instance-ID refusal and corrected promote wording; 304 tests + 190 subtests; release still owner-gated | PR #19 → `06ccb0a` |
| 2026-10-22 | **D-003 on-demand catalog templates merged:** 265 types render canonical/blank/example variants into ignored `build/TEMPLATES`; 795 tracked variants removed after byte-match; no session closure or PyPI publication | PR #16 → `a28616b` |
| 2026-10-22 | **D-004 audience applicability and D-002 language readers merged:** owner-confirmed `reader` semantics; JSDoc, TypeDoc and nightly Rustdoc readers; no session closure or PyPI publication | PR #14 → `7a0fd47` |
| 2026-10-22 | **Post-merge state reconciliation merged:** package readiness reflected after PR #12; C4R7/B71a preserved as paused; no PyPI publication | PR #13 → `a704752` |
| 2026-10-22 | **Installable CLI/package merged:** zero-runtime-dependency `autodoc` CLI, wheel/sdist packaging, isolated install smoke, Python 3.11–3.15 matrix; no PyPI publish | PR #12 → `08229a0` |
| 2026-10-21 | **Migration-prose structure checks merged:** canonical sections/prompts routed through existing enforcement families; B71a remains paused pending explicit owner closure | PR #11 → `52d1b79` |
| 2026-10-21 | **D-001 session closed by owner** (“Close A90c, then proceed”); its plan was archived; PR #10 is the current master tip; new session B71a registered for the named migration-prose validation follow-up | PR #10 → `c4a9d43` |
| 2026-10-21 | **Debt D-001 closed** (owner instruction: "continue"): eleven stale catalog-count claims corrected across eight documents (260 → 265, and one total that summed to 263), a derived-count guard added (`tests/test_catalog_counts.py`, 4 tests), D-001 → fixed, dashboard/architecture/NEXT-ACTION reconciled | `d3ebf4a` — PR #8 merged at `5bbd7d8` |
| 2026-10-21 | **Closing pass** (owner instruction: "continue from this here and also close the session"): the eight open sessions closed on the owner's word, their plans archived (not deleted), `REGISTRY`/`INDEX`/`DASHBOARD`/`NEXT-ACTION.md` reconciled, rule-10 self-check run on a cold clone | this branch's closing commit + PR |
| 2026-10-21 | Branch-protection review → fix → test (owner instructions: "Cannot merge the commit…" then "done, test it"): ruleset `main` diagnosed vs ADR-011; **B-003** raised; **P-007** decided (option A) and the owner's edit verified live; PR #3 merged (`04f7386`); PR #4 merged (`87be33b`); post-merge continuity test passed on a cold clone of `master`; **B-003 struck**; closing record in PR #5 (`cffa527`) | `77ca6c6`, `6da01b2`, `a642a31`, `eab749b`, `2976760` |
| 2026-10-01 | Post-merge continuity test of PR #2 on a cold clone of `master`; session `20261001-1408-A476` + plan; dashboard/registry/index/blockers reconciled | `eec4050`, `41dead9` — PR #3 merged at `04f7386` |
| 2026-10-01 | Owner round executed: decision 4 landed; the review recorded (**B-001 cleared**); the ADR deviation acknowledged (**B-002 cleared**); shutdown reconcile + rule-10 self-check | `c7980f9`, `039e508`, `3ad5a57`, `5dd9112`, `e14135e`, `ce4feba` |
| 2026-10-01 | Owner decision 4 executed: demo-only facts declared false; detector self-match fixed; **15/15, 0 open**; beta cliff 4 → 2 | `c7980f9` |
| 2026-10-01 | Session-lifecycle correction (ADR-009 + MACP local rules 8–10) | `c57b149`, `14310ea` |
| 2026-10-01 | Cold-clone continuity test + the P-001…P-006 dossier | `b3a4490` + reconcile |
| 2026-10-01 | Owner decision 3 executed: 11 of 12 core decisions closed | `1a65f5d` + reconcile |
| 2026-10-01 | Full MACP transcription + Section 7 bootstrap audit | `d26d798` + reconcile |
| 2026-10-01 | MACP adopted: protocol in governance, `state/` bootstrapped | `868588e`, `f417a8f` |
| 2026-10-01 | Owner flags A/B/C applied; `CORE-LIST-REVIEW.md` v1.3 | `f37d98a`, `c02d733` |
| 2026-10-01 | Core-list review; license; enforcement layer; §3–§7 lanes | `5164b06`…`2454ea1`, `90478d4` |
| Earlier | Catalog, profiles, facts, triggers, evidence and language work | see `RECENT-CHANGES.md` |

## Next actions (source of truth: `NEXT-ACTION.md`)

1. **Owner release decision:** decide whether to keep the proposed `0.3.0` / Beta
   version-classifier change, whether to write the `beta` phase promotion, and whether to release.
   No release or PyPI publication is proposed by this branch.
2. **Deferred scope:** D-007 remains unselected; D-009's external dogfood was executed but its
   formal acceptance/record remains open. D-010's `make audit` mechanism is implemented; record its
   first accepted run if the owner wants the debt formally closed. No implementation work is
   pending for the closeout scope.
3. **Session closure and release boundaries:** PRD2, PRD1 and 912C are merged but not closed; 894B,
   627F, C4R7 and B71a remain paused/awaiting explicit owner closure. Only the owner closes
   sessions. Package workflows build artifacts only; PyPI/trusted publishing needs a separate owner
   decision; promotion to `beta` remains a deliberate owner write, though its preview now shows no
   blockers. PR #21 merged at `f8e2c76`; merging did not close PRD2.

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
