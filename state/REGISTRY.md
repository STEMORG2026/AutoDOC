# REGISTRY — who is working here and what they own

**Last reconciled:** 2026-10-21T15:34Z (migration-prose check integrated; `make ci` green; B71a paused awaiting owner)

## Active — work in flight, or landed and awaiting the owner

One session holds a claim: `B71a` (migration prose validation), paused for owner review on `arena/48a62791-autodoc`.

| Agent ID | Model / type | Branch | Task (one line) | Started (UTC) | Claimed paths | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `B71a` | Arena.ai Agent Mode | `arena/48a62791-autodoc` | Integrate structural checks for four canonical migration titles into `stub_check`; findings route through existing `placeholders`/`stubs` families | 2026-10-21T14:59Z | `state/**`, `scripts/doc-control/stub_check.py`, `scripts/intelligence/enforce.py`, `CONTROL/metadata/CONTEXT-MODEL.json`, `autodoc.toml`, `tests/test_migration_prose.py`, `Makefile`, `NEXT-ACTION.md`, `CHANGELOG.md`, `CURRENT-STATE.md`, `CONTEXT-SNAPSHOT.md`, `RECENT-CHANGES.md`, `docs/00-governance/ENGINE-COVERAGE.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, `docs/META/**` | **PAUSED (awaiting owner)** |

## Closed by the owner

Only the owner's word moves a row here (MACP local rule 8, ADR-009). The nine prior rows were
closed by the owner's 2026-10-21 instruction; A90c was closed separately at 14:59Z by the owner's
“Close A90c, then proceed” instruction. Each session file carries its closing entry, and plans are
archived under `state/archive/plans/2026-10/` when one existed.

| Agent ID | Session | Branch | Task | Closed (UTC) | Plan |
| --- | --- | --- | --- | --- | --- |
| `A90c` | `sessions/20261021-1318-A90c-debt-d001.md` | `arena/44b2fb68-autodoc` | Debt D-001: repair catalog-count drift and add a derived-count guard | 2026-10-21T14:59Z | `agent-A90c-debt-d001.md` |
| `Abb7f` | `sessions/20261021-1257-Abb7f-session-close.md` | `arena/83bebb7f-autodoc` | Close the eight open sessions, archive plans, reconcile `state/` + `NEXT-ACTION.md` | 2026-10-21T13:05Z | `agent-Abb7f-session-close.md` |
| `A52ab` | `sessions/20261021-1138-A52ab-protection-review.md` | `arena/d2fb52ab-autodoc` | Branch-protection review: B-003, P-007 executed, PR #3 + PR #4 merged, post-merge test, B-003 struck | 2026-10-21T13:00Z | `agent-A52ab-protection-review.md` |
| `A476` | `sessions/20261001-1408-A476-post-merge-test.md` | `arena/01a0f476-autodoc` | Post-merge continuity test of PR #2 (`04f7386`); protection apply owner-run | 2026-10-21T13:00Z | `agent-A476-post-merge-test.md` |
| `A476` | `sessions/20261001-1242-A476-decision-round.md` | `arena/01a0f476-autodoc` | Owner decision round: six verdicts executed or recorded | 2026-10-21T13:00Z | `agent-A476-decision-round.md` |
| `A476` | `sessions/20261001-1228-A476-session-lifecycle.md` | `arena/01a0f476-autodoc` | Session-lifecycle correction (ADR-009, rules 8–10) | 2026-10-21T13:00Z | `agent-A476-session-lifecycle.md` |
| `A476` | `sessions/20261001-1219-A476-cold-clone-test.md` | `arena/01a0f476-autodoc` | Cold-clone continuity test + the P-001…P-006 dossier | 2026-10-21T13:00Z | `agent-A476-cold-clone-test.md` |
| `A476` | `sessions/20261001-1130-A476-decision-3.md` | `arena/01a0f476-autodoc` | Decision 3: 11 of 12 core decisions closed | 2026-10-21T13:00Z | `agent-A476-decision-3.md` |
| `A476` | `sessions/20261001-1120-A476-bootstrap-audit.md` | `arena/01a0f476-autodoc` | Full protocol transcription + Section 7 audit | 2026-10-21T13:00Z | never committed (recorded in `-1228`) |
| `A476` | `sessions/20261001-1110-A476-macp-adoption.md` | `arena/01a0f476-autodoc` | MACP adopted; `state/` bootstrapped | 2026-10-21T13:00Z | `agent-A476-macp-adoption.md` |

## Non-agent owner

| Who | Role | Scope |
| --- | --- | --- |
| `@Er-Sajan-PLG` | Repository owner and sole reviewer | Approves governed documents, records owner decisions, closes sessions, merges PRs, edits repository settings (branch protection / rulesets). No backup reviewer is configured. |

## Rules in force here

- **Sessions close only on the owner's word** (local rule 8): agents mark `PAUSED (awaiting owner)`;
  `COMPLETED`/`CLOSED` are the owner's labels, and a session's plan stays until then.
- **Persist before presenting** (local rule 9): decision rounds live in `DECISIONS.md` § Pending,
  never only in chat.
- **Handoff self-check** (local rule 10): before handing off, read the state as a stranger; if the
  next actions cannot be executed from state alone, fix state first.
- An **active** claim wins; shared files (`Makefile`, `pyproject.toml`, workflows,
  `CONTROL/metadata/**`) need a `[COORDINATION]` note in both sessions.
- A claim held by an agent `INACTIVE` for **>24h** may be taken over; record the takeover.
- Only the owner records owner decisions. Agents propose and implement; the owner decides, and
  takes decisions one at a time.
