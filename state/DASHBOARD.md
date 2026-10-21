# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-21T13:38Z · **Reconciled by:** A90c (session `20261021-1318-A90c`,
PAUSED awaiting owner close) · **Tip at reconciliation:** `5bbd7d8` on `master` (PR #8 merged;
PR #6 `f0aa0e3` and PR #7 `9e5155d` before it, every `master` run green)

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `master` at `5bbd7d8`; one session branch open (`arena/44b2fb68-autodoc`, PAUSED awaiting owner) |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 192 contextual · 265 types (209 A + 56 B) · 16 detected facts · 3 declared traits — the prose numbers are checked against the indexes by `tests/test_catalog_counts.py` (D-001 fixed) |
| Build-ready | **15/15** · open core decisions **0** (owner decision 4 closed the last one, `DOC-A05-001` Data model, as not applicable) |
| Promotion cliff | Promoting to `beta` today would fail **2** core rows (License `DOC-A10-008`, Changelog `DOC-A15-003`); both gated on `is_public` |
| Stack | Python 3.11, **zero runtime dependencies**; pytest + pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 70 controlled instances (28 generated targets, 42 human-owned, `make docs-health` 2026-10-21) · 384 Markdown files tracked |
| Tests | 247 passed + 182 subtests, ~26 s (2026-10-21); cold clone of `master` re-verified the same day |
| CI | 5 workflows; required check `AutoDOC guard / check` — **required in GitHub**: ruleset `main` (P-007-A, applied by the owner 2026-10-21, verified live: `deletion`, `non_fast_forward`, `required_status_checks` `AutoDOC guard / check` `strict: true`); nightly freshness warn-only; tag-gated release |

## Active agents

`A90c` — session `20261021-1318-A90c` (**PAUSED (awaiting owner close)**): debt **D-001** fixed —
eleven stale catalog-count claims corrected in eight human-owned documents (260 → 265; and
`CURRENT-STATE.md`'s third total, which summed to 263 instead of 265) — plus
`tests/test_catalog_counts.py`, which derives the counts from the indexes and the rules and fails
`make ci` when a document disagrees. Landed as **PR #8 → `5bbd7d8`**. **No other session is open**;
the eight closed on the owner's word stay closed. Register yourself in `REGISTRY.md` before work.

## Alerts

1. **D-001 fixed (2026-10-21).** The catalog counts are no longer remembered: eleven prose claims
   were corrected and `tests/test_catalog_counts.py` derives `265 / 209 / 56 / 24 / 49 / 192` from
   `CATALOG-*/INDEX.yaml` and `CATALOG-RULES.json`; a disagreement fails `make ci`. Its limits are in
   the test docstring (three-digit totals, the word "then" marks history, a bare "N core" is
   ambiguous between the default tier 24 and the `oss-library` profile's 26).

2. **Sessions closed (2026-10-21).** ADR-009's rule (only the owner's word closes a session) was
   honoured to the end: no agent ever wrote `COMPLETED`, and the close is recorded with the owner's
   instruction quoted in each of the nine session files. Nothing is open now — a new instruction
   starts a new session, not a resumption.

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

1. **Nothing is pending.** Protection is aligned and verified (ADR-011 recorded), PR #3/#4/#5/#6/#7/#8
   are merged, the post-merge tests passed, the eight sessions are closed on the owner's word, and
   D-001 is fixed. One session (`A90c`, D-001) is PAUSED awaiting the owner's close.
2. Optional follow-ups only, none gating: the P-006 deferrals in `state/DEBT.md` (`audience` consumer
   first if any is picked; JS/TS + Rust toolchains; external dogfood repository; template rendering
   on demand; evidence signing), the one other `open` item (D-010, vulnerability scanning — low,
   needs a network scanner), and promotion to `beta` remains a deliberate event with cliff 2.

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
