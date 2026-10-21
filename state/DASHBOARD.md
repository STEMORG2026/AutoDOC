# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-21T12:25Z · **Reconciled by:** A52ab (protection-review session `20261021-1138-A52ab`, PAUSED awaiting owner) · **Tip at reconciliation:** `04f7386` on `master` (**PR #3 merged**); this branch carries the merge-resolve and the P-007-A record

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `arena/d2fb52ab-autodoc` (session branch; **PR #4** open — protection review + P-007 record; **PR #3 merged** to `master` at `04f7386`) |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 265 types (prose still says 260 — D-001) · 16 detected facts · 3 declared traits |
| Build-ready | **15/15** · open core decisions **0** (owner decision 4 closed the last one, `DOC-A05-001` Data model, as not applicable) |
| Promotion cliff | Promoting to `beta` today would fail **2** core rows (License `DOC-A10-008`, Changelog `DOC-A15-003`); both gated on `is_public` |
| Stack | Python 3.11, **zero runtime dependencies**; pytest + pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 68 controlled (24 generated, 44 human-owned); 361 Markdown files tracked |
| Tests | 243 passed + 182 subtests, ~23 s (protection-review run, 2026-10-21) |
| CI | 5 workflows; required check `AutoDOC guard / check` — **required in GitHub since 2026-10-21** via ruleset `main` (P-007-A applied by the owner and verified live: `deletion`, `non_fast_forward`, `required_status_checks` `AutoDOC guard / check` `strict: true`); nightly freshness warn-only; tag-gated release |

## Active agents

`A52ab` — session `20261021-1138-A52ab` (**PAUSED (awaiting owner)**): branch-protection review —
ruleset `main` diagnosed, **P-007** decided (option A) and applied by the owner (rules verified
live); PR #3 merged at `04f7386`; the post-merge continuity test and the B-003 strike follow on
this branch. `A476` sessions: three **PAUSED (awaiting owner)** (`20261001-1228` lifecycle,
`-1242` decision round, `-1408` post-merge test of PR #2) and four **landed — awaiting owner
close** (`-1110`, `-1120`, `-1130`, `-1219` cold-clone). **No session is complete** — only the
owner closes one (ADR-009). Register yourself in `REGISTRY.md` before starting work.

## Alerts

1. **P-007-A is applied and verified (2026-10-21).** The owner edited ruleset `main` (id
   `25542481`); the live branch rules now read `deletion`, `non_fast_forward` and
   `required_status_checks` → `AutoDOC guard / check` (`strict: true`) — exactly the ADR-011
   payload as a ruleset. The `required_signatures` and CodeQL rules that blocked every merge are
   gone; PR #3 and PR #4 flipped `BLOCKED` → `CLEAN`. **B-003 stays open** until PR #4 lands and
   the post-merge test passes; then it is struck.
2. **B-001 cleared (2026-10-01)** — the owner confirmed the v1.3 page ("proceed with recomendation")
   and the recording landed: `owner_reviewed` in both machine files, page → `approved`, caveat off
   `NEXT-ACTION.md` + `ADOPTION.md`, D-011 fixed (commit `039e508`).
3. Nothing is failing in the tree: the gate is green (`make ci` exit 0, re-run 2026-10-21:
   243/243 + 182 subtests), catalog valid, resolver at **15/15 with zero open decisions**.
4. **B-002 cleared (2026-10-01)** — the owner acknowledged the decision-3 deviation and kept the
   real ADR; ADR-008 records it (commit `3ad5a57`). The ADR row was closed with a real ADR
   (`docs/adr/0001-zero-runtime-dependencies.md`) instead of the queued `[not_applicable]`, because
   the resolver reports every skip on an `always` row as a permanent stale-decision warning.
   Reversible; see the decision-3 session summary.
5. Environment resets recur (ten recoveries on 2026-10-01, #11–#20: HEAD back to `19ca0d4`, wedged
   index, dirty-tree variant, venv deleted). #17 is logged in the lifecycle session; #18, #19 and
   #20 in the decision-round session. Recovery recipe is in the audit session's summary; never
   force-push. The protection-review session adds one sandbox quirk: a depth-1 clone made the
   `doc-state-sync` hook regenerate `RECENT-CHANGES.md` from a one-commit history — unshallow
   first (session `20261021-1138-A52ab`).
6. **Continuity verified:** a cold clone of the session branch, read by a stranger, can state the
   position, the gates and the whole pending decision round, and can verify the numbers with system
   `python3` and no install (`state/sessions/20261001-1219-A476-cold-clone-test.md`).
7. **Sessions await the owner's close** (ADR-009, MACP local rule 8): eight sessions are open —
   three `PAUSED (awaiting owner)` plus this review, four `landed — awaiting owner close`; their
   plans are kept. Only the owner's word moves a session to CLOSED. Companion rules:
   **persist before presenting** (decision rounds live in `DECISIONS.md` § Pending, never only in
   chat) and the **handoff self-check** (local rule 10).

## Recently landed (sessions await the owner's close)

| Date | Work | Commits |
| --- | --- | --- |
| 2026-10-21 | Branch-protection review (owner instruction): ruleset `main` read live and compared to ADR-011; PR #3's merge block diagnosed (unsigned commits + CodeQL rules with no CodeQL); B-003 raised; **P-007** decided (option A) and the owner's edit verified live; PR #3 merged at `04f7386`; state reconciled across both session branches — **on `arena/d2fb52ab-autodoc`, PR #4** | `77ca6c6`, `6da01b2`, `a642a31`, + the merge-resolve |
| 2026-10-01 | Post-merge continuity test of PR #2 on a cold clone of `master`; new session + plan; dashboard/registry/index/blockers reconciled; ADR-011 status updated | `eec4050`, `41dead9` — **PR #3 merged** at `04f7386` |
| 2026-10-01 | Owner round executed: decision 4 landed; the review recorded (`owner_reviewed`, page → `approved`, caveat off, D-011 — **B-001 cleared**); the ADR deviation acknowledged (**B-002 cleared**); the branch-protection payload printed (owner-run application); shutdown reconcile + rule-10 self-check + session log ordered | `c7980f9`, `039e508`, `3ad5a57`, `5dd9112`, `e14135e`, `ce4feba` |
| 2026-10-01 | Owner decision 4 executed: the demo-only facts are declared false with reasons; the detector's self-match is fixed at its source (no override, regression-tested); the last open core decision closes — **15/15, 0 open**; beta cliff 4 → 2 | `c7980f9` |
| 2026-10-01 | Session-lifecycle correction (owner instruction): MACP local rules 8–10 + ADR-009 — sessions close only on the owner's word; persist-before-present; handoff self-check; all sessions/plans relabelled; deleted plans restored where possible | `c57b149` + handoff-log `14310ea` |
| 2026-10-01 | Cold-clone continuity test: verdict (a new agent can continue from `state/` alone), five gap fixes, and the pending-decision dossier P-001…P-006 in `DECISIONS.md` | `b3a4490` + reconcile commit |
| 2026-10-01 | Owner decision 3 executed: 11 of 12 open core decisions closed (charter, README, ADR, module contract, test strategy, dependency setup/policy, SECURITY.md, CODE_OF_CONDUCT.md); readiness 4/16 → **15/16** | `1a65f5d` + reconcile commit |
| 2026-10-01 | Full MACP transcription (Sections 2–7 + REMEMBER) and the Section 7 bootstrap audit | `d26d798` + the reconcile commit |
| 2026-10-01 | MACP adopted: protocol in governance, `state/` bootstrapped, agent pointers | `868588e`, `f417a8f` |
| 2026-10-01 | Owner flags A/B/C applied and re-validated; `CORE-LIST-REVIEW.md` v1.3 (24 core / 49 extended; build-ready 4/16; beta cliff 12 of 24) | `f37d98a`, `c02d733` |
| 2026-10-01 | Core-list review delivered; license decided (Apache-2.0); enforcement layer; §3–§7 lanes | `5164b06`…`2454ea1`, `90478d4` |
| Earlier | Catalog, profiles, facts, triggers, evidence and language work | see `RECENT-CHANGES.md` |

## Next actions (source of truth: `NEXT-ACTION.md`)

1. **Agent (this session): land PR #4 and finish the test** — guard green → merge (merge commit),
   then the post-merge continuity test on a cold clone of `master` (state read, cold numbers with
   system `python3`, `make ci`, guard runs on `master`), recorded in the same session; strike
   B-003 and close out P-007 in `DECISIONS.md` in that record. Nothing on GitHub settings is
   pending: P-007-A is applied and verified.
2. **Owner: close the sessions you consider done** (ADR-009, rule 8) — eight await close across
   the two session branches.
3. The ADR-011 mechanism is recorded: ruleset `main` carries the required check
   (`AutoDOC guard / check`, `strict: true`); the classic payload from
   `APPLY=1 make docs-require-check` is superseded and stays as a dry-run reference.

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
