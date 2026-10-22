# Plans — active list

One file per active session, opened at MACP Step 9 and named `agent-<id>-<topic>.md`. A plan is
**moved, not deleted**, to `state/archive/plans/<YYYY-MM>/` when the owner closes its session
(rule 8 keeps it until that word; the archive keeps the record afterwards).

## Current plans

- `agent-912C-pr14-post-merge-reconciliation.md` — verify merged PR #14, reconcile post-merge state,
  and persist next-work options before owner selection; active on `arena/912c4060-autodoc`.
- `agent-894B-d004-language-readers.md` — D-004 audience applicability and D-002 language readers;
  PR #14 merged at `7a0fd47`; session paused until the owner explicitly closes it.
- `agent-627F-post-pr12-continuation.md` — PR #12 state reconciliation; PR #13 merged, owner chose
  the next scope, but the session remains paused until explicit owner closure.

An empty list here means no session is in flight. Reference plans as code spans, never as links —
their path changes when they are archived (local rule 4).
