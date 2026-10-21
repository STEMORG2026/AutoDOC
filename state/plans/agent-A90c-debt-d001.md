# Plan — A90c — debt D-001: make the catalog counts checkable

| Field | Value |
| --- | --- |
| Objective | Close D-001 by repairing the drifted catalog numbers in the prose **and** adding a check that fails when a human-owned document restates a catalog count that disagrees with the indexes |
| Owner of the work | `A90c` (session `20261021-1318-A90c`) |
| Status | **PAUSED (awaiting owner)** — work landed; a session closes only on the owner's word (ADR-009) |
| Opened (UTC) | 2026-10-21T13:18Z |

## Scope

**In:** the human-owned documents that restate catalog counts (`README.md`, `CURRENT-STATE.md`,
`CONTEXT-SNAPSHOT.md`, `QUICK-START.md`, `IMPLEMENTATION-GUIDE.md`, `RECENT-CHANGES.md`,
`docs/00-governance/ADOPTION.md`, `docs/00-governance/ENGINE-COVERAGE.md`,
`docs/00-governance/LIMITATIONS.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`); one regression
test deriving the counts from `CATALOG-A/INDEX.yaml`, `CATALOG-B/INDEX.yaml` and
`CONTROL/metadata/CATALOG-RULES.json`; `state/DEBT.md` (D-001 → fixed), the dashboard's catalog row
and the session/plan/index/registry bookkeeping.

**Out:** changing the catalogs, the rules file, the rule tiers, or any count that is *not* drifted
(a correct number is not churn); generated documents (they are regenerated, never hand-edited — the
one stale figure inside a generated file, `docs/META/CODE-INVENTORY.md`, is a **line number**, not
a count); session logs (append-only — their historical "260" stays).

## Approach

1. Derive the truth from the sources: `265` types (`209` A + `56` B), `24` core, `49` extended,
   `192` contextual. Note that `CURRENT-STATE.md` is wrong twice: it says `260` and also
   `45 extended and 194 contextual`.
2. Fix each drifted sentence in place, and mark genuinely historical statements with the word
   **then** (the check's escape hatch) instead of deleting the history.
3. Add `tests/test_catalog_counts.py`: it derives the counts, then scans the human-owned controlled
   documents plus `state/DASHBOARD.md` and `state/ARCHITECTURE.md` for count claims and fails on a
   mismatch. The test states its own limit: it reads *numbers next to the words that give them
   meaning*, not semantics.
4. `make generate` (no state file feeds a target), `make ci`, then reconcile and hand off.

## Done when

`make ci` is green with a deliberately-drifting count failing the new test, no human-owned document
says `260 types`, `45 extended` or `194 contextual`, and D-001 is `fixed (<commit>)` in `state/DEBT.md`.
