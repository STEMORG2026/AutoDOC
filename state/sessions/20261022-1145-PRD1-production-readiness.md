# Session 20261022-1145-PRD1 — production-readiness commands

## Owner request

“What did we do so far?” followed by “Continue if you have next steps…” after the owner had asked to
finish the remaining AutoDOC work and make it production level, pulling first. The pull, D-003 merge
and duplicate-PR cleanup were completed before this session file was opened; this session covers the
remaining production-readiness implementation on `arena/production-readiness-autodoc`.

## Coordination and decisions

- Active branch: `arena/production-readiness-autodoc`, created from `master` at the D-003 merge
  commit `a28616b`.
- D-003 is merged (PR #16, merge commit `a28616b`); duplicate PR #17 is closed as superseded.
- The unpulled remote had a large update; `git pull --rebase` was run before the work below.
- The 912C, 894B, 627F, C4R7 and B71a sessions remain paused/in progress as recorded. This session
  does not close or overwrite them.
- Scope proposed here is implementation, tests, documentation and state: `autodoc promote`,
  `autodoc add`, and declaration flags on `autodoc init`. PyPI publication, merges without owner
  authorization, and owner-only decisions (version/classifier policy, owner-reviewed declarations)
  remain out of scope.
- The release-version and classifier choice are owner decisions. This session may propose them but
  must not record them as approved.

## Claimed paths

- `autodoc/cli.py`, `scripts/intelligence/promote.py`, `scripts/add-document.py`
- `scripts/doc-control/library.py`, `scripts/init-project.py`, `scripts/adopt.py`
- `setup.py`, `scripts/test_package.py`, `Makefile`, `autodoc.toml`
- `tests/test_promote.py`, `tests/test_add_document.py`, `tests/test_cli.py`,
  `tests/test_template_library.py`
- `CHANGELOG.md`, `QUICK-START.md`, `IMPLEMENTATION-GUIDE.md`, `README.md`, `CURRENT-STATE.md`,
  `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `pyproject.toml`
- `state/**` for this session's own coordination records

## Plan

See `state/plans/agent-PRD1-production-readiness.md`.

## Progress log

- `2026-10-22T11:45Z` [START] Registered before code changes. Confirmed the branch created from
  `a28616b`, reviewed `autodoc/cli.py`, `scripts/intelligence/{context,profile,recommend}.py`,
  `scripts/init-project.py`, `scripts/add-document.py` (absent), `setup.py`, `Makefile` and the
  existing tests. Planning `promote`/`add`/`init` declarations and their verification.
- `2026-10-22T12:11Z` [PROGRESS] Implemented `autodoc add`, `autodoc promote` and `init --phase/
  --profile`; added shared instance rendering/destination helpers; wired runtime packaging and
  installed-package smoke coverage. Added focused tests: targeted suite 25 passed, full suite 301
  passed with 190 subtests. Recreated the missing `.venv` and reinstalled the editable package so
  the `--version` check reads project metadata.
- `2026-10-22T12:11Z` [PROGRESS] `make generate` refreshed the generated references after the
  version bump; `make ci` then passed end to end: 301 tests + 190 subtests, package smoke exercised
  version/check/generate/adopt/init/add/promote/templates, and stored evidence hashes verified
  (hashes, not signatures).
- `2026-10-22T12:11Z` [DISCOVERY] D-003 is merged on `master` through PR #16 at `a28616b`; the
  branch base, local `master` and `origin/master` agree after `git fetch`, so no rebase is needed.
  The registry/dashboard still described D-003 as in progress; this handoff reconciles that.
- `2026-10-22T12:11Z` [DECISION] Version/classifier are proposed as `0.3.0` / Beta in this change
  but remain owner decisions; no owner approval is recorded. The command behaviour and tests are
  independent of that proposal.

## Outcome

**PARTIAL — implementation and verification complete; review PR and owner merge pending.** The
session is not closed: local rule 8 reserves `COMPLETED`/`CLOSED` for the owner's word.

### Accomplished

- `autodoc promote --to <phase>` previews catalog/enforcement deltas, refuses a normal write while
  target-phase required documents lack a document/decision, supports explicit demotion/backdate/
  incomplete writes only with `--force`, preserves the rest of `autodoc.toml`, and writes only the
  top-level `phase` and `phase_declared` values atomically.
- `autodoc add <catalog-id>` previews or writes one catalog-derived document with a
  project-qualified instance ID and current creation dates; paths are root-bounded and existing
  files require `--force`.
- `autodoc init` accepts optional `--phase` and `--profile`, validates both against the shipped
  model/profiles, and never overwrites an existing `autodoc.toml`.
- Runtime packaging, CLI help, installed-package smoke, user/adoption/architecture/exit-code docs,
  changelog and generated metadata are updated. `make ci` is green on the worktree.
- Full suite: 301 passed, 190 subtests passed. Package smoke: wheel/sdist build, sdist rebuild and
  clean-wheel exercise of all seven commands passed.

### Not accomplished

- No commit, push or PR yet at the time this log was written; the next step is the review handoff.
- PyPI publication, merging without owner authorization, session closure and an owner verdict on
  the version/classifier proposal remain out of scope.
- No new ADR: the commands implement already-declared behaviour (phase change is an explicit event;
  context is declared), so no design decision was made on the owner's behalf.

### Files changed

| Path | Action | Summary |
| --- | --- | --- |
| `scripts/intelligence/promote.py` | added | Preview/apply promotion, delta, guarded atomic TOML edit |
| `scripts/add-document.py` | added | Single catalog-document preview/write |
| `scripts/doc-control/library.py` | modified | Instance/date rendering and public destination helper |
| `scripts/init-project.py` | modified | `--phase`/`--profile` declaration writer |
| `autodoc/cli.py` | modified | `add`/`promote`, init flags, runtime requirements |
| `setup.py`, `scripts/test_package.py` | modified | Ship and smoke-test the new runtime scripts |
| `tests/test_promote.py`, `tests/test_add_document.py`, `tests/test_cli.py` | added/modified | Focused behaviour and installed-CLI integration coverage |
| `README.md`, `QUICK-START.md`, `IMPLEMENTATION-GUIDE.md`, `CHANGELOG.md` | modified | User-facing command/version documentation |
| `docs/00-governance/{ADOPTION,ENGINE-COVERAGE}.md`, `docs/05-architecture/AUTODOC-ARCHITECTURE.md`, `docs/reference/EXIT-CODES.md` | modified | Adoption, coverage, boundary and exit-code docs |
| `pyproject.toml` | modified | Version `0.3.0`; Beta classifier proposal |
| `docs/META/*`, `docs/generated/AUTOMATION-REFERENCE.md` | regenerated | Generated inventories/references refreshed |
| `state/**`, living-state files | modified | Handoff reconciliation and session registration |

### Key decisions and rationale

- A promotion that reaches a failing phase is blocked at exit `1` when required documents remain
  unresolved; `--force` applies the declaration anyway but leaves the findings and exit `1`.
  Demotion/backdating are usage errors (`2`) unless forced. Same phase is a no-op (`0`).
- `add` defaults to `docs/autodoc/<category>/<ID>.md`, validates the catalog record's destination,
  and never records `[instantiated]`; acknowledgment remains a human decision.
- Version `0.3.0` and Beta are proposed for owner sign-off, not recorded as approved.

### Debt, bugs and risks

- No new technical debt or unrelated bugs found.
- `promote` evaluates the target phase against the current repository's detected facts; fields that
  change outside `autodoc.toml` can change the delta. This is intentional and is shown before a
  write.
- The installed package's version is read from package metadata; an editable install must be
  refreshed after a version bump (done in this session).
- External language tools remain absent locally; package/CLI tests use the existing fake-tool
  coverage and do not claim those tools ran.

### Next steps

1. Stage, run pre-commit and `make docs-staged-impact`, then commit and push this branch.
2. Open a review PR; keep it open for owner review and do not merge without explicit authorization.
3. Owner decides whether to keep `0.3.0` / Beta and whether to merge.
4. If the owner requests follow-up changes, keep this session paused rather than opening a new one.
