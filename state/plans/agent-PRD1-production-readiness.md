# Plan — production-readiness commands (`PRD1`)

## Objective

Close the remaining production-readiness gap in AutoDOC by implementing the context lifecycle and
single-document authoring paths that the shipped schema and documentation already advertise, then
verify with the repository gate and a clean-package smoke.

## Scope

In:

- `autodoc promote`: dry-run default, `--to`, `--date`, `--write`, `--force`, `--json`; validates the
  current context, computes enforcement deltas with the same catalog/context machinery as
  `recommend`, writes only top-level `phase`/`phase_declared` textually and atomically, and reports
  unsupported downgrades/backdating without `--force`.
- `autodoc add`: resolve one catalog document by ID, render a canonical/blank/example instance,
  preview by default, `--write` to the catalog-derived destination, refuse overwrite unless
  `--force`, create parents, and print the exact next step (metadata replacement, check).
- `autodoc init`: optional declaration flags for phase and optional profile so a new project can
  record owner-reviewed context at creation; keep interactive/zero-flag behavior compatible.
- CLI wiring, `runtime_root`/packaging, tests, docs, changelog, and coordination state.

Out:

- PyPI publication, tag creation, branch-protection changes, merging this session's PR without the
  owner's explicit authorization.
- Recording owner-reviewed declarations or inventing an owner decision about the release version or
  classifier. Version/classifier changes are proposed in the session/PR for owner decision.
- Rewriting generated docs or relaxing existing gates.

## Approach

1. Register session/plan and claim paths (done before code).
2. Add shared instance rendering/destination helpers to `scripts/doc-control/library.py` without
   changing the existing template-variant contract.
3. Implement `scripts/intelligence/promote.py` on top of `context_module` +
   `profiler.profile` + `recommend` and a minimal, comment-preserving TOML editor.
4. Implement `scripts/add-document.py` and expose both commands through `autodoc/cli.py`; add new
   scripts to `setup.py` runtime assets and installed-package smoke.
5. Extend `scripts/init-project.py` with declaration flags, then add focused tests for success,
   refusal, idempotence, malformed context, and no-write previews.
6. Update user-facing docs, changelog, version/classifier proposal, and state; run `make generate`
   if metadata/catalog/docs change, then `make ci` and a package smoke.

## Risks and mitigations

- TOML rewrite could damage comments or formatting: edit only the matched scalar lines with a
  newline-preserving replacement, validate by parsing the result, write via a temporary sibling and
  `os.replace`, preserve mode.
- Promotion could advertise impossible compliance: compute the delta with `recommend` before and
  after and refuse when newly required core documents are missing unless `--force`; print them.
- `add` could overwrite human work: preview by default and require `--force` for an existing file;
  validate IDs and destinations through the catalog loader.
- New runtime files could break the installed CLI: update `runtime_root` and package smoke in the
  same change.
- Scope creep into owner decisions: keep version/classifier as an explicit proposal and do not
  write `owner_reviewed` or close decisions.

## Rollback strategy

Revert the single production-readiness commit and restore `master` at `a28616b`; no data migration
or external state is touched. Promote writes are local, atomic and validated before replacement.

## Success criteria

- `autodoc promote` previews and writes a valid phase change with an accurate delta; invalid or
  downgrade/backdate requests fail with usage/findings codes as designed.
- `autodoc add` previews and writes one catalog-derived document safely.
- `autodoc init --phase/--profile` produces valid context without changing default behavior.
- New tests pass; `make ci` exits 0 and the isolated wheel/sdist smoke exercises the new commands.
- State and user docs describe the shipped behavior without claiming owner approval.

## Status — 2026-10-22T12:11Z

Implementation and local verification are complete: 301 tests + 190 subtests pass, package smoke
exercises all seven CLI commands, and `make ci` exits 0. The plan remains active only for the review
handoff (staged checks, commit/push, PR) and owner merge; the session is not closed. The `0.3.0` /
Beta version-classifier change is a proposal awaiting owner sign-off, not a recorded decision.
