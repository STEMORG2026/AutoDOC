# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-21T12:35Z · **Reconciled by:** A52ab (protection-review session `20261021-1138-A52ab`, PAUSED awaiting owner close) · **Tip at reconciliation:** `87be33b` on `master` (**PR #3 and PR #4 merged**; this branch carries the post-merge test record)

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `arena/d2fb52ab-autodoc` (session branch; **PR #3** merged at `04f7386`, **PR #4** merged at `87be33b`; the post-merge test record rides the next PR from this branch) |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 265 types (prose still says 260 — D-001) · 16 detected facts · 3 declared traits |
| Build-ready | **15/15** · open core decisions **0** (owner decision 4 closed the last one, `DOC-A05-001` Data model, as not applicable) |
| Promotion cliff | Promoting to `beta` today would fail **2** core rows (License `DOC-A10-008`, Changelog `DOC-A15-003`); both gated on `is_public` |
| Stack | Python 3.11, **zero runtime dependencies**; pytest + pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 68 controlled (24 generated, 44 human-owned); 361 Markdown files tracked |
| Tests | 243 passed + 182 subtests, ~23 s (2026-10-21); cold clone of `master` re-verified the same day |
| CI | 5 workflows; required check `AutoDOC guard / check` — **required in GitHub**: ruleset `main` (P-007-A, applied by the owner 2026-10-21, verified live: `deletion`, `non_fast_forward`, `required_status_checks` `AutoDOC guard / check` `strict: true`); nightly freshness warn-only; tag-gated release |

## Active agents

`A52ab` — session `20261021-1138-A52ab` (**PAUSED (awaiting owner close)**): the whole loop is
done — ruleset `main` diagnosed (B-003), P-007 decided (option A) and applied by the owner,
rules verified live, PR #3 + PR #4 merged (`04f7386`, `87be33b`), post-merge continuity test
passed on a cold clone of `master`, B-003 struck. `A476` sessions: three **PAUSED (awaiting
owner)** (`20261001-1228` lifecycle, `-1242` decision round, `-1408` post-merge test of PR #2)
and four **landed — awaiting owner close** (`-1110`, `-1120`, `-1130`, `-1219` cold-clone).
**No session is complete** — only the owner closes one (ADR-009). Register yourself in
`REGISTRY.md` before starting work.

## Alerts

1. **B-003 cleared (2026-10-21).** The owner applied P-007-A: ruleset `main` (id `25542481`) now
   carries exactly `deletion`, `non_fast_forward` and `required_status_checks` → `AutoDOC guard /
   check` (`strict: true`) — ADR-011's payload as a ruleset. The `required_signatures` and CodeQL
   rules that blocked every merge are gone; PR #3 and PR #4 merged with merge commits and their
   `master` runs are green (guard 1m27s / 1m16s; preview 10s / 9s).
2. **Post-merge continuity test passed (2026-10-21)** on a cold clone of `master` at `87be33b`:
   state-only read correct (15/15, 0 open, cliff 2, P-007 decided and executed, B-003 struck);
   cold numbers verify with system `python3` and no install (`recommend.py` 15/15;
   `check_catalog.py` valid); `make ci` exit 0 on the clone. Details in session
   `20261021-1138-A52ab`.
3. **B-001 cleared (2026-10-01)** — the owner confirmed the v1.3 page ("proceed with recomendation")
   and the recording landed: `owner_reviewed` in both machine files, page → `approved`, caveat off
   `NEXT-ACTION.md` + `ADOPTION.md`, D-011 fixed (commit `039e508`).
4. **B-002 cleared (2026-10-01)** — the owner acknowledged the decision-3 deviation and kept the
   real ADR; ADR-008 records it (commit `3ad5a57`).
5. Environment resets recur (ten recoveries on 2026-10-01, #11–#20) and one sandbox quirk on
   2026-10-21: a depth-1 clone made the `doc-state-sync` hook regenerate `RECENT-CHANGES.md` from
   a one-commit history — unshallow first (session `20261021-1138-A52ab`). Never force-push.
6. **Sessions await the owner's close** (ADR-009, MACP local rule 8): eight sessions are open —
   four `PAUSED (awaiting owner)` (incl. this review) and four `landed — awaiting owner close`;
   their plans are kept. Only the owner's word moves a session to CLOSED.

## Recently landed (sessions await the owner's close)

| Date | Work | Commits |
| --- | --- | --- |
| 2026-10-21 | Branch-protection review → fix → test (owner instructions: "Cannot merge the commit…" then "done, test it"): ruleset `main` diagnosed vs ADR-011; **B-003** raised; **P-007** decided (option A) and the owner's edit verified live; PR #3 merged (`04f7386`); PR #4 merged (`87be33b`); post-merge continuity test passed on a cold clone of `master`; **B-003 struck** | `77ca6c6`, `6da01b2`, `a642a31`, `eab749b`, `2976760`, + the closing record |
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

1. **Owner: close the sessions you consider done** (ADR-009, rule 8) — eight await close across
   the two session branches. Nothing else is pending from this thread: the protection is aligned
   and verified (ADR-011 recorded), PR #3 and PR #4 are merged, and the post-merge test passed.
2. Optional follow-ups are unchanged (P-006 deferrals in `state/DEBT.md`; promotion to `beta`
   remains a deliberate event with cliff 2).

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
