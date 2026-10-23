# REGISTRY — who is working here and what they own

**Last reconciled:** 2026-10-23T07:10Z (PR #24 merged the beta promotion at `8f9c709`; post-merge `make ci` passes. BETA, PRD2, PRD1 and 912C are merged but await explicit owner closure; 894B/627F/C4R7/B71a remain paused)

## Active — work in flight, or landed and awaiting the owner

C4R7's package-readiness work is merged (PR #12, `08229a0`) and its session remains **PAUSED awaiting explicit owner closure**; merging did not close it. PR #13's state reconciliation is merged at `a704752`; session 627F remains paused. D-004 and D-002 were merged in PR #14 at `7a0fd47`; session 894B remains paused because merging did not close it. B71a (migration prose validation) remains paused on `arena/48a62791-autodoc`; PR #11 merging did not close it. PR #15's state reconciliation merged at `990113b` after explicit owner authorization, and 912C's D-003 implementation merged in PR #16 at `a28616b`; 912C remains paused pending explicit owner closure. PRD1's production-readiness commands merged in PR #18 at `1361ba2`; post-merge installed-wheel dogfood found the packaged-root path defect, fixed and merged in PR #19 at `06ccb0a`; PR #20 reconciled the state at `f2e8698`. PRD1's session remains paused pending explicit owner closure; merging did not close it. PRD2's closeout merged in PR #21 at `f8e2c76`; its session is paused pending explicit owner closure. It is a separate bounded session, not a reopening of PRD1. BETA's phase promotion merged in PR #24 at `8f9c709`; its session is paused pending explicit owner closure.

| Agent ID | Model / type | Branch | Task (one line) | Started (UTC) | Claimed paths | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `BETA` | opencode agent | `chore/promote-beta` (merged in PR #24) | Beta promotion merged at `8f9c709`: `phase = "beta"`, declaration date 2026-10-23, duplicate pins removed, phase-dependent docs/tests/state updated; post-merge `make ci` passes 307 tests + 188 subtests; no release/tag/PyPI/closure | 2026-10-23T06:12Z | `autodoc.toml`, `README.md`, `tests/test_enforce.py`, `docs/00-governance/{ADOPTION,CORE-LIST-REVIEW}.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, `docs/generated/TRIGGER-REFERENCE.md`, `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `state/**` | **PAUSED (merged; awaiting explicit owner closure)** |
| `PRD2` | opencode agent | `feat/production-readiness-closeout` (merged in PR #21) | Production-readiness closeout merged at `f8e2c76`: beta document homes, operator-run audit, readiness fixes, docs/state; post-merge `make ci` passes 307 tests + 190 subtests; no phase write/release/closure | 2026-10-22T14:15Z | `autodoc.toml`, `pyproject.toml`, `Makefile`, `scripts/intelligence/{enforce,recommend}.py`, `tests/{test_enforce,test_promote}.py`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`, `docs/00-governance/{ENGINE-COVERAGE,LIMITATIONS}.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, generated metadata, `state/**` | **PAUSED (merged; awaiting explicit owner closure)** |
| `PRD1` | opencode agent | `arena/production-readiness-autodoc`; `fix/dogfood-packaged-root` (merged) | Production-readiness commands merged in PR #18 at `1361ba2`; installed-wheel dogfood fixes merged in PR #19 at `06ccb0a`; post-merge `make ci` passes 304 tests + 190 subtests | 2026-10-22T11:45Z | `autodoc/cli.py`, `scripts/intelligence/{promote,recommend,enforce}.py`, `scripts/add-document.py`, `scripts/doc-control/library.py`, `scripts/init-project.py`, `setup.py`, `Makefile`, tests, usage/release docs, `state/**` | **PAUSED (merged; awaiting explicit owner closure)** |
| `912C` | Arena.ai Agent Mode | `arena/912c4060-autodoc` | Owner-selected D-003: catalog template variants render on demand into ignored `build/TEMPLATES`; merged in PR #16 at `a28616b` | 2026-10-22T10:11Z | `scripts/doc-control/library.py`, `autodoc/cli.py`, `setup.py`, `Makefile`, catalog validators, tests, template docs, `state/**` | **PAUSED (merged; awaiting explicit owner closure)** |
| `894B` | Arena.ai Agent Mode | `arena/894b93ee-autodoc` | Owner-selected D-004 audience applicability followed by D-002 JSDoc, TypeDoc and nightly Rustdoc JSON readers; PR #14 merged at `7a0fd47` | 2026-10-22T04:45Z | `scripts/intelligence/recommend.py`, `scripts/doc-sync/{languages,engine}.py`, tests, toolchain fixtures, `CONTROL/metadata/**`, `autodoc.toml`, coverage/architecture docs, `docs/META/**`, living-state files, `state/**` | **PAUSED (awaiting explicit owner closure)** |
| `627F` | Arena.ai Agent Mode | `arena/627fcb46-autodoc` | PR #13 post-merge state reconciliation; merged at `a704752`; owner selected D-004 then D-002 | 2026-10-22T04:26Z | `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `state/**` | **PAUSED (awaiting explicit owner closure)** |
| `C4R7` | Arena.ai Agent Mode | `arena/072fcb8c-autodoc` | Installable zero-runtime-dependency Python CLI/package; wheel/sdist and release guidance; PR #12 merged at `08229a0`; no PyPI publish | 2026-10-21T18:20Z | `pyproject.toml`, `setup.py`, `MANIFEST.in`, `autodoc/`, `scripts/doc-sync/engine.py`, CLI scripts, `Makefile`, `Taskfile.yaml`, package tests, workflows, usage/architecture docs, `state/**`, living-state files | **PAUSED (awaiting explicit owner closure)** |
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
