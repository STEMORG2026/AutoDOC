# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-22T04:40Z · **Reconciled by:** 627F (session `20261022-0426-627F`,
PR #12 merged; C4R7 remains paused) · **Base tip:** `08229a0` on `master` (PR #12 merged); active continuation branch: `arena/627fcb46-autodoc`.

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `master` at `08229a0` (PR #12 merged); continuation branch `arena/627fcb46-autodoc` is active |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 192 contextual · 265 types (209 A + 56 B) · 16 detected facts · 3 declared traits — the prose numbers are checked against the indexes by `tests/test_catalog_counts.py` (D-001 fixed) |
| Build-ready | **15/15** · open core decisions **0** (owner decision 4 closed the last one, `DOC-A05-001` Data model, as not applicable) |
| Promotion cliff | Promoting to `beta` today would fail **2** core rows (License `DOC-A10-008`, Changelog `DOC-A15-003`); both gated on `is_public` |
| Stack | Python 3.11–3.15 declared, **zero runtime dependencies**; build/pytest/pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 70 controlled instances (28 generated targets, 42 human-owned, `make docs-health` 2026-10-21) · 384 Markdown files tracked |
| Tests | Local `make ci`: 267 passed + 190 subtests on Python 3.11; wheel/sdist smoke passed; PR #12 required check, impact and Python 3.11–3.15 matrix all green; evidence hashes verified (not signatures) |
| CI | 5 workflows; required check `AutoDOC guard / check` remains in GitHub ruleset `main` (P-007-A, strict); supplemental Python 3.11–3.15 matrix is non-blocking; nightly freshness warn-only; tag workflow builds snapshot + wheel/sdist artifacts, no PyPI publish |

## Active agents

`627F` — session `20261022-0426-627F` (**PAUSED (awaiting owner scope selection)**): reconciled
PR #12 after merge; confirmed that C4R7 remains paused and did not choose an optional roadmap item.
Local `make ci` passes on the merged base. The next step is an owner choice among non-gating P-006
follow-ups, or an explicit session-close instruction.

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

## Recently landed

| Date | Work | Commits |
| --- | --- | --- |
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

1. **Choose the next bounded task:** the installable CLI/package is already merged at `08229a0`.
   P-006 follow-ups are optional/non-gating; D-004 (`audience` consumer) is first if any P-006 item
   is selected. Other deferred work includes JS/TS + Rust toolchains, external dogfood, on-demand
   templates, and evidence signing. The user has not selected one yet.
2. **Session closure:** C4R7 remains paused awaiting the owner's explicit close; merging PR #12 did
   not close it. B71a also remains paused after PR #11 (`52d1b79`); do not close either by inference.
3. **Release boundary:** the package workflow builds artifacts only. PyPI/trusted publishing requires
   a separate owner decision. D-010 vulnerability scanning remains low/open; promotion to `beta`
   remains a deliberate event with cliff 2.

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
