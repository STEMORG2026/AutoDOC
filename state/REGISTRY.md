# REGISTRY — who is working here and what they own

**Last reconciled:** 2026-10-23T19:17Z (master `e556d54` after PR #28; this closing pass closed the eight remaining sessions and archived all plans. MACP local rule 11 now records the one-session/one-branch/owner-closes-all/passkey lifecycle; no session is open.)

## Active — work in flight, or landed and awaiting the owner

None. The owner closed all open sessions on 2026-10-23; the next unit of work starts a new session
on a new branch.

## Closed by the owner

Only the owner's word moves a row here (MACP local rule 8, ADR-009). The ten rows from 2026-10-21
were closed in the earlier owner round; A90c was closed separately on 2026-10-21; EVOLVE was closed
on 2026-10-23 by “close the session”; the eight rows below were closed on 2026-10-23 by the owner’s
“complete the works left to do in each session and close them” instruction. Plans are archived under
`state/archive/plans/2026-10/`.

| Agent ID | Session | Branch | Task | Closed (UTC) | Plan |
| --- | --- | --- | --- | --- | --- |
| `CLOSE` | `sessions/20261023-1218-CLOSE-close-all-open-sessions.md` | `docs/close-all-open-sessions` | Closing pass: audited and closed the eight remaining sessions, archived their plans, reconciled state, and added MACP rule 11 / ADR-018 | 2026-10-23T19:17Z | `agent-CLOSE-close-all-open-sessions.md` |
| `BETA` | `sessions/20261023-0612-BETA-beta-promotion.md` | `chore/promote-beta` (merged in PR #24) | Beta promotion merged at `8f9c709`: `phase = "beta"`, duplicate pins removed, phase-dependent docs/tests/state updated; no release/tag/PyPI | 2026-10-23T17:24Z | `agent-BETA-beta-promotion.md` |
| `PRD2` | `sessions/20261022-1415-PRD2-production-closeout.md` | `feat/production-readiness-closeout` (merged in PR #21) | Production-readiness closeout merged at `f8e2c76`: beta document homes, operator-run `make audit`, readiness fixes, docs/state; no phase write/release | 2026-10-23T17:24Z | `agent-PRD2-production-closeout.md` |
| `PRD1` | `sessions/20261022-1145-PRD1-production-readiness.md` | `arena/production-readiness-autodoc`; `fix/dogfood-packaged-root` (merged) | Production-readiness commands merged in PR #18 at `1361ba2`; installed-wheel dogfood fixes merged in PR #19 at `06ccb0a`; post-merge `make ci` passes 304 tests + 190 subtests | 2026-10-23T17:24Z | `agent-PRD1-production-readiness.md` |
| `912C` | `sessions/20261022-1011-912C-pr14-post-merge-reconciliation.md` | `arena/912c4060-autodoc` | D-003 on-demand catalog templates merged in PR #16 at `a28616b`; 795 prior variant outputs byte-matched and removed | 2026-10-23T17:24Z | `agent-912C-pr14-post-merge-reconciliation.md` |
| `894B` | `sessions/20261022-0445-894B-d004-language-readers.md` | `arena/894b93ee-autodoc` | D-004 audience applicability and D-002 JSDoc/TypeDoc/nightly Rustdoc JSON readers merged in PR #14 at `7a0fd47` | 2026-10-23T17:24Z | `agent-894B-d004-language-readers.md` |
| `627F` | `sessions/20261022-0426-627F-post-pr12-continuation.md` | `arena/627fcb46-autodoc` | PR #12 post-merge state reconciliation merged in PR #13 at `a704752`; owner then selected D-004/D-002, implemented separately by 894B | 2026-10-23T17:24Z | `agent-627F-post-pr12-continuation.md` |
| `C4R7` | `sessions/20261021-1820-C4R7-python-package-readiness.md` | `arena/072fcb8c-autodoc` | Installable zero-runtime-dependency Python CLI/package; wheel/sdist and release guidance; PR #12 merged at `08229a0`; no PyPI publish | 2026-10-23T17:24Z | `agent-C4R7-python-package-readiness.md` |
| `B71a` | `sessions/20261021-1459-B71a-migration-prose-validation.md` | `arena/48a62791-autodoc` | Migration-prose validation integrated into `stub_check.py`; canonical sections/prompts route through existing policy families; PR #11 merged at `52d1b79` | 2026-10-23T17:24Z | `agent-B71a-migration-prose-validation.md` |
| `EVOLVE` | `sessions/20261023-0751-EVOLVE-evolve-command.md` | `feat/autodoc-evolve` (merged in PR #26) | Owner-requested `autodoc evolve`: read-only plan, generated refresh, draft-only missing documents, maturity/JSON/check; merged at `c0f90e0` | 2026-10-23T10:26Z | `agent-EVOLVE-evolve-command.md` |
| `A90c` | `sessions/20261021-1318-A90c-debt-d001.md` | `arena/44b2fb68-autodoc` | Debt D-001: repair catalog-count drift and add a derived-count guard | 2026-10-21T14:59Z | `agent-A90c-debt-d001.md` |
| `Abb7f` | `sessions/20261021-1257-Abb7f-session-close.md` | `arena/83bebb7f-autodoc` | Close the eight open sessions, archive plans, reconcile `state/` + `NEXT-ACTION.md` | 2026-10-21T13:05Z | `agent-Abb7f-session-close.md` |
| `A52ab` | `sessions/20261021-1138-A52ab-protection-review.md` | `arena/d2fb52ab-autodoc` | Branch-protection review: B-003, P-007 executed, PR #3 + PR #4 merged, post-merge test, B-003 struck | 2026-10-21T13:00Z | `agent-A52ab-protection-review.md` |
| `A476` | `sessions/20261001-1408-A476-post-merge-test.md` | `arena/01a0f476-autodoc` | Post-merge continuity test of PR #2 (`04f7386`); protection apply owner-run | 2026-10-21T13:00Z | `agent-A476-post-merge-test.md` |
| `A476` | `sessions/20261001-1242-A476-decision-round.md` | `arena/01a0f476-autodoc` | Owner decision round: six verdicts executed or recorded | 2026-10-21T13:00Z | `agent-A476-decision-round.md` |
| `A476` | `sessions/20261001-1228-A476-session-lifecycle.md` | `arena/01a0f476-autodoc` | Session-lifecycle correction (ADR-009, rules 8–10) | 2026-10-21T13:00Z | `agent-A476-session-lifecycle.md` |
| `A476` | `sessions/20261001-1219-A476-cold-clone-test.md` | `arena/01a0f476-autodoc` | Cold-clone continuity test + the P-001…P-006 dossier | 2026-10-21T13:00Z | `agent-A476-cold-clone-test.md` |
| `A476` | `sessions/20261001-1130-A476-decision-3.md` | `arena/01a0f476-autodoc` | Decision 3: 11 of 12 core decisions closed | 2026-10-21T13:00Z | `agent-A476-decision-3.md` |
| `A476` | `sessions/20261001-1120-A476-bootstrap-audit.md` | `arena/01a0f476-autodoc` | Full MACP transcription + Section 7 audit | 2026-10-21T13:00Z | never committed (recorded in `-1228`) |
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
- **One session, one bounded work unit, one branch** (local rule 11): when the owner says “close the
  session”, every open session closes, its plan archives, and the next work starts a new session on
  a new branch. A closed session is immutable and reopens only with an explicit owner passkey.
- An **active** claim wins; shared files (`Makefile`, `pyproject.toml`, workflows,
  `CONTROL/metadata/**`) need a `[COORDINATION]` note in both sessions.
- A claim held by an agent `INACTIVE` for **>24h** may be taken over; record the takeover.
- Only the owner records owner decisions. Agents propose and implement; the owner decides, and
  takes decisions one at a time.
