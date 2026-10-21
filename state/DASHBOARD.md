# DASHBOARD — AutoDOC

**Last reconciled:** 2026-10-21T11:57Z · **Reconciled by:** A52ab (protection-review session `20261021-1138-A52ab`, PAUSED awaiting owner) · **Tip at reconciliation:** `4d0c50f` (the PR #2 merge; this reconcile follows on `arena/d2fb52ab-autodoc`)

## Project

| Field | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` — a self-updating documentation engine, not a compliance certificate |
| Branch | `arena/d2fb52ab-autodoc` (session branch; **PR #3** from `arena/01a0f476-autodoc` is open — approved and green but **blocked** by ruleset `main` — and this branch carries the protection review) |
| Declared phase | `build` (warn) — declared 2026-09-30, never inferred |
| Kinds / profile | `library` / `oss-library` (26 core types) |
| Catalog | 24 core · 49 extended · 265 types (prose still says 260 — D-001) · 16 detected facts · 3 declared traits |
| Build-ready | **15/15** · open core decisions **0** (owner decision 4 closed the last one, `DOC-A05-001` Data model, as not applicable) |
| Promotion cliff | Promoting to `beta` today would fail **2** core rows (License `DOC-A10-008`, Changelog `DOC-A15-003`); both gated on `is_public` |
| Stack | Python 3.11, **zero runtime dependencies**; pytest + pre-commit for dev; SQLite and a 3-route HTTP server only in the synthetic demo |
| Docs | 68 controlled (24 generated, 44 human-owned); 361 Markdown files tracked |
| Tests | 243 passed + 182 subtests, ~23 s (protection-review run, 2026-10-21) |
| CI | 5 workflows; required check `AutoDOC guard / check` (green on PR #3) — **not required in GitHub yet**: ruleset `main` omits it (P-007); nightly freshness warn-only; tag-gated release |

## Active agents

`A52ab` — session `20261021-1138-A52ab` (**PAUSED (awaiting owner)**): branch-protection review —
why PR #3 cannot merge under ruleset `main`, state reconciled, **P-007** presented; awaiting the
owner's verdict and the ruleset edit. Of the `A476` sessions, four are
**landed — awaiting owner close** (`20261001-1110`, `-1120`, `-1130`, `-1219` cold-clone) and two
are **PAUSED (awaiting owner)** (`-1228` lifecycle, `-1242` decision round).
**No session is complete** — only the owner closes one (ADR-009). Register yourself in
`REGISTRY.md` before starting work.

## Alerts

1. **Everything is blocked at GitHub — ruleset `main` (B-003).** The owner protected `master`
   2026-10-21 (11:27Z) with ruleset `main` (id `25542481`): `deletion`, `non_fast_forward`,
   `code_quality`, `required_signatures`, `code_scanning` — and **no** required status check.
   PR #3 is approved and green and still cannot merge ("the base branch policy prohibits the
   merge"): its commits are unsigned and the tree has no CodeQL workflow the two CodeQL rules
   could read. ADR-011's `AutoDOC guard / check` requirement is absent from the ruleset. The
   alignment decision is **P-007** (`state/DECISIONS.md` § Pending); the edit is owner-run
   (agent token: settings write 403; no bypass actor on the ruleset).
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
   force-push.
6. **Continuity verified:** a cold clone of the session branch, read by a stranger, can state the
   position, the gates and the whole pending decision round, and can verify the numbers with system
   `python3` and no install (`state/sessions/20261001-1219-A476-cold-clone-test.md`).
7. **Sessions await the owner's close** (ADR-009, MACP local rule 8): no session is complete.
   Two are `PAUSED (awaiting owner)` (`-1228` lifecycle, `-1242` decision round) plus this
   protection review; four are `landed — awaiting owner close` (`-1110`, `-1120`, `-1130`,
   `-1219`); their plans are kept. Only the owner's word moves a session to CLOSED. Companion
   rules: **persist before presenting** (decision rounds live in `DECISIONS.md` § Pending, never
   only in chat) and the **handoff self-check** (local rule 10).

## Recently landed (sessions await the owner's close)

| Date | Work | Commits |
| --- | --- | --- |
| 2026-10-21 | Branch-protection review (owner instruction): ruleset `main` read live and compared to ADR-011; PR #3's merge block diagnosed (unsigned commits + CodeQL rules with no CodeQL); B-003 raised; **P-007** alignment round written; stale session-status labels aligned; `NEXT-ACTION.md`'s "apply the required check" paragraph corrected — **on `arena/d2fb52ab-autodoc`, PR open and itself blocked by B-003** | the protection-review commit(s) on `arena/d2fb52ab-autodoc` |
| 2026-10-01 | Post-merge continuity test of PR #2 on a cold clone of `master`; new session + plan; dashboard/registry/index/blockers reconciled; ADR-011 status updated (PR #3, awaiting merge) | `eec4050`, `41dead9` (branch `arena/01a0f476-autodoc`) |
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

1. **Owner: decide P-007 and align ruleset `main`** (GitHub → Settings → Rules → Rulesets →
   `main`). Recommended (option A): keep *Block deletions* and *Block force pushes*; **remove**
   *Require signed commits*, *Require code quality* and *Require code scanning*; **add**
   *Require status checks to pass* → `AutoDOC guard / check`, with *Require branches to be up to
   date before merging*. Until this lands, **no** PR can merge — PR #3 is the proof. Alternatives
   B (keep signed commits, squash-only merges) and C (keep the CodeQL rules, land CodeQL first)
   are dossiers in `state/DECISIONS.md` P-007.
2. **Owner: merge PR #3** once unblocked — merge commit matches the history — or instruct the
   agent to merge; then the protection-review PR from `arena/d2fb52ab-autodoc` the same way.
3. **Owner: close the sessions you consider done** (ADR-009, rule 8) — seven await close across
   the two session branches.
4. After the ruleset carries the required check, record the applied mechanism in ADR-011
   (ruleset `main`, not the classic payload from `APPLY=1 make docs-require-check` — that PUT
   becomes redundant). Not claimed complete until then.

This dashboard summarizes; it never overrides `NEXT-ACTION.md` or an owner instruction. Sessions
are closed only by the owner.
