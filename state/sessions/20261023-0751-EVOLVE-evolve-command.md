# Session 20261023-0751-EVOLVE — safe autoevolution command

## Owner request

After the owner asked AutoDOC to auto-evolve while documenting mature projects, the agent proposed
two bounded commands. The owner chose **both, as separate commands**, then authorized implementing
`autodoc evolve` first with “yes”.

This is a new bounded session. The corpus-side `evolve-catalog` command remains a separate,
unopened scope.

## Coordination and decisions

- Branch: `feat/autodoc-evolve`, starting at `master` `249c2aa` (PR #25 merged).
- Scope: implement `scripts/intelligence/evolve.py`, expose `autodoc evolve`, add runtime packaging,
  tests, usage/governance/architecture/exit-code documentation, generated output and state.
- Out of scope: `autodoc evolve-catalog`, phase/profile changes, approvals, catalog edits,
  release/tag/PyPI, version changes and session closure.
- Safety boundary: a plan is read-only by default. `--write` refreshes generated drift only.
  `--allow-add` is required to create missing required documents, and then only as `status: draft`.
  Drafts are never added to `[instantiated]`, approved, or counted as compliance.
- No existing document is overwritten, including an existing but unregistered target. Undetermined
  facts and structural findings are reported for a human decision.
- Maturity signals are advisory and never become a phase declaration.

## Claimed paths

- `scripts/intelligence/evolve.py`
- `autodoc/cli.py`, `setup.py`, `scripts/test_package.py`
- `tests/test_evolve.py`, `tests/test_cli.py`
- `README.md`, `QUICK-START.md`
- `docs/00-governance/{ADOPTION,ENGINE-COVERAGE}.md`
- `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, `docs/reference/EXIT-CODES.md`
- `docs/generated/AUTOMATION-REFERENCE.md`, `docs/META/{CODE-INVENTORY,TEST-INVENTORY,OUTLINE}.md`
- `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `state/**`

## Plan

Archived after closure: `state/archive/plans/2026-10/agent-EVOLVE-evolve-command.md`.

## Verification and evidence

- `pytest`: 315 tests + 188 subtests, including eight new `evolve`/CLI tests.
- `autodoc evolve --repo .`: 0 actions, 23 advisory recommended-document reports at beta; no
  phase/profile/decision/catalog change.
- Temporary beta project: preview found nine missing required documents; `--write` alone wrote
  nothing; `--write --allow-add` created nine draft instances and a second plan reported them as
  unregistered rather than satisfied.
- Generated drift fixture: planned, refreshed, verified, and absent from the following plan.
- Configuration-error fixture: exit 2, no writes.
- `make generate` and `make ci` pass (315 tests + 188 subtests, package-check included);
  `make audit` reports no known vulnerabilities. Post-merge `master` (`c0f90e0`) passes 315 tests
  + 188 subtests.

## Outcome

**COMPLETED — CLOSED by the owner on 2026-10-23** (owner instruction “close the session”; ADR-009 /
MACP local rule 8). The command merged in PR #26 at `c0f90e0`; PR #27 reconciled the state at
`4230703`. The plan was archived, not deleted.

### What was accomplished

- Added `scripts/intelligence/evolve.py` and the `autodoc evolve` CLI command without duplicating
  the context, profile, recommendation, enforcement, sync-engine or `add` policy.
- Read-only planning by default; `--write` refreshes only declared generated drift; `--write
  --allow-add` creates missing required documents only as unregistered `status: draft` instances.
- Added maturity signals, human and JSON reports, `--check` exit semantics, runtime packaging,
  command help, tests and package smoke coverage.
- Documented the safety boundary in usage, governance, architecture and exit-code references, and
  reconciled living state after the merge.

### What was not accomplished

- `autodoc evolve-catalog` was not started; it remains a separate, unopened scope.
- No release, tag, PyPI publication or version decision was included.
- No phase, profile, approval, decision or catalog change was made by `evolve`.
- No session closure occurred at merge time; the owner closed it separately on 2026-10-23.

### Files changed

| Path | Action | Summary |
| --- | --- | --- |
| `scripts/intelligence/evolve.py` | added | Planning, safe apply, maturity, reports and check mode |
| `autodoc/cli.py`, `setup.py`, `scripts/test_package.py` | modified | CLI wiring, runtime packaging and installed-command smoke coverage |
| `tests/test_evolve.py`, `tests/test_cli.py` | added / modified | Eight new evolve/CLI tests |
| `README.md`, `QUICK-START.md` | modified | User-facing command and safety boundary |
| `docs/00-governance/{ADOPTION,ENGINE-COVERAGE}.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, `docs/reference/EXIT-CODES.md` | modified | Governance, architecture and exit-code documentation |
| `docs/generated/AUTOMATION-REFERENCE.md`, `docs/META/{CODE-INVENTORY,TEST-INVENTORY,OUTLINE}.md` | modified | Regenerated metadata |
| `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `state/**` | modified | Living state, session record and archived plan |

### Decisions and rationale

- ADR-017 records the owner's choice of two separate commands and the safety boundary for
  `evolve`; `evolve-catalog` remains out of scope.
- Draft creation cannot satisfy a requirement: drafts stay out of `[instantiated]`, approvals and
  compliance counts.
- Existing documents are never overwritten; existing-but-unregistered targets are reports, not
  write targets.
- Maturity is advisory and cannot declare a phase.

### Technical debt, bugs and risks

- No new debt or known product bug was introduced. The editor's unresolved `pytest` import warning
  in `tests/test_promote.py` is environment-only; tests pass.
- Residual risk: `evolve-catalog` is unstarted; generated refreshes depend on the declared sync map;
  draft documents require human review and registration.

### Prioritized next steps

1. None for this session; it is closed.
2. If the owner opens the corpus scope, plan `autodoc evolve-catalog` as a separate session.
3. Release/tag/PyPI and the remaining paused sessions stay owner-only decisions.
