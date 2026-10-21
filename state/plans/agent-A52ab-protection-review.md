# Plan — A52ab — branch-protection review and merge unblock

| Field | Value |
| --- | --- |
| Objective | Diagnose why PR #3 cannot merge under the owner's new branch protection, record the true state in `state/`, and present the alignment decision (P-007) for the owner's verdict |
| Owner of the work | `A52ab` (session `20261021-1138-A52ab`) |
| Status | **PAUSED (awaiting owner)** — the diagnosis and record are landed on the session branch; the unblock itself is owner-run (ruleset edit) and the verdict is pending (kept per MACP local rule 8) |
| Opened (UTC) | 2026-10-21T11:38Z |

## Scope

**In:** inspect the repository and the new protection (ruleset `main`, created 2026-10-21) with
read-only API calls; attempt the PR #3 merge once to capture the exact prohibition; reconcile
`state/` (this plan, the session file, `DECISIONS.md` § Pending P-007, `BLOCKERS.md` B-003,
`DASHBOARD.md`, `REGISTRY.md`, `INDEX.md`) and the now-stale `NEXT-ACTION.md` paragraph; align
stale session-status labels found along the way; `make ci` before every push.

**Out:** changing repository settings — this session's token has no Administration write
(verified 403 on the ruleset PUT, same limitation ADR-011 recorded), and the ruleset has no bypass
actor, so the edit is owner-run; merging PR #3 while the owner's own ruleset forbids it (the owner
decides how to unblock — a bypass would violate the protection they just configured); any
product/code change; inventing a verdict for P-007.

## Approach

1. Read the rules, the PR merge state and the check rollup; attempt the merge to capture the
   exact prohibition; confirm no other repository change exists behind "did some changes".
2. Present P-007 from `state/DECISIONS.md` § Pending — record what is fact, never a verdict
   (local rules 8–9).
3. Hand off under rule 10: the owner's next action must be executable from state alone (the
   exact ruleset edit is spelled out in P-007, B-003 and the dashboard).

## Progress

- 2026-10-21: diagnosis complete (ruleset `main` vs ADR-011's payload; unsigned PR commits; no
  CodeQL in the tree; merge attempt returns "the base branch policy prohibits the merge"); state
  reconciled and status labels aligned; `make ci` green (243 + 182 subtests); P-007 presented
  before the presentation in chat.
- 2026-10-21: owner verdict recorded — **P-007, option A**. Remaining: the owner-run ruleset
  edit (token 403 re-verified), then verify live rules, merge PR #3 + the protection-review PR,
  strike B-003, record the mechanism in ADR-011.
