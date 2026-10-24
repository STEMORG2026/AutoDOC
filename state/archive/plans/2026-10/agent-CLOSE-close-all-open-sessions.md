# Plan — CLOSE — close every remaining open session

| Field | Value |
| --- | --- |
| Objective | Audit and close the eight remaining open sessions, archive their plans, reconcile the state, and add the missing session-lifecycle/passkey convention to MACP. |
| Owner of the work | `CLOSE` (session `20261023-1218-CLOSE`) |
| Branch | `docs/close-all-open-sessions` |
| Status | **CLOSED (owner's word, 2026-10-23)** — all eight remaining sessions closed; plans archived; MACP rule 11 added |
| Opened (UTC) | 2026-10-23T12:18Z |

## Scope

**In:** the eight paused sessions (BETA, PRD2, PRD1, 912C, 894B, 627F, C4R7, B71a), their session
files and plans; `REGISTRY`, `INDEX`, `DASHBOARD`, `CURRENT-STATE`, `NEXT-ACTION`,
`RECENT-CHANGES`, `ARCHITECTURE`, `DEBT`, `BLOCKERS`; the missing MACP session-lifecycle rule.

**Out:** new product features, release/tagging, PyPI publication, or reopening a closed session
without an explicit owner passkey.

## Approach

1. Audit each paused session and plan; distinguish finished work that only needs closure from work
   that still has a concrete implementation gap.
2. Add the missing session lifecycle rule to MACP: one session maps to one bounded unit of work
   and one branch; when the owner says “close the session”, all open sessions close; the next unit
   of work starts a new session and branch; a closed session can only be reopened with an explicit
   owner passkey.
3. Move every complete session’s plan to `state/archive/plans/2026-10/`, mark the session
   `CLOSED`, and reconcile `REGISTRY`/`INDEX`/`DASHBOARD`/living state.
4. Run `make generate`, `pre-commit`, and `make ci`; commit, push, open the PR, watch checks, and
   merge after they pass.
5. Confirm from `master` that no session remains open.

## Risks and mitigations

- **Risk:** closing a session whose work is incomplete. **Mitigation:** audit each plan first and
  leave genuinely unfinished work open only long enough to finish it in this pass.
- **Risk:** conflating session closure with product release. **Mitigation:** closure is state
  bookkeeping only; release/tagging/PyPI remain owner-only and untouched.
- **Risk:** reopening a closed session accidentally. **Mitigation:** archive the plan and record
  the passkey rule; a closed session is immutable without an explicit owner passkey.

## Success criteria

- No open session remains after this pass.
- Every closed session has a `CLOSED` status, an archived plan and an INDEX/REGISTRY row that agree.
- MACP records the one-session/one-branch/owner-closes-all/passkey lifecycle.
- `make generate`, `pre-commit` and `make ci` pass; the closing PR is merged and verified on `master`.

## Outcome

- Audited the eight remaining sessions; all implementation, tests and PRs are merged and no concrete
  implementation gap remained.
- Closed BETA, PRD2, PRD1, 912C, 894B, 627F, C4R7 and B71a on the owner’s instruction; archived
  their plans; reconciled REGISTRY, INDEX, DASHBOARD and living state.
- Added MACP local rule 11 and ADR-018: one session, one bounded work unit, one branch;
  “close the session” closes all open sessions; the next work starts a new session on a new branch;
  a closed session reopens only with an explicit owner passkey.
- No release, tag or PyPI publication was made.
