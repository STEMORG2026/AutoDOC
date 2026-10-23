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

See `state/plans/agent-EVOLVE-evolve-command.md`.

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
  `make audit` reports no known vulnerabilities. The PR is the remaining gate.

## Outcome

**ACTIVE — PR #26 open on `feat/autodoc-evolve`; awaiting owner review/merge.** No release,
tag, PyPI publication, phase change or session closure is included.
