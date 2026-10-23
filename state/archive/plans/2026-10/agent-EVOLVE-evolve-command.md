# Plan — safe autoevolution (`EVOLVE`)

| Field | Value |
| --- | --- |
| Objective | Add a bounded `autodoc evolve` command that plans safe documentation updates for a project, refreshes generated drift, and creates missing required documents only as unregistered drafts. |
| Owner of the work | `EVOLVE` (session `20261023-0751-EVOLVE`) |
| Status | **CLOSED (owner's word, 2026-10-23)** — merged in PR #26 at `c0f90e0`; plan archived at the owner's close |
| Opened (UTC) | 2026-10-23T07:51Z |

## Scope

**In:** a read-only plan by default; `--write` for generated drift; `--allow-add` for draft-only
creation; `--check` for CI; JSON output; maturity signals; CLI and wheel packaging; tests and docs.
The plan reuses the existing context, profile, recommendation, enforcement, sync-engine, library and
`add` modules rather than creating a second policy.

**Out:** `evolve-catalog`; registering or approving drafts; editing `autodoc.toml`, the catalog,
decision records or approvals; overwriting existing files; release/tag/PyPI/version changes; session
closure.

## Approach

1. Build the plan from `context.normalise/validate`, `profile.profile`,
   `recommend.catalog/evaluate/profile_placement`, `enforce.collect_findings` and the baseline.
2. Turn only drift findings into refresh actions. Turn only missing required documents that are not
   baselined into create actions; if the default target already exists, report it as unregistered
   instead of overwriting it.
3. Report undetermined facts, recommended-document gaps, structural findings and stale baseline
   entries without acting on them.
4. Apply refresh actions through `enforce.repo_scope` and `engine.generate`; apply create actions
   through `add_document.add`, never writing the context file.
5. Verify refreshed drift, then expose the command through the installed CLI and wheel.
6. Test read-only planning, write boundaries, draft non-registration, no-overwrite, drift,
   configuration blocking, maturity and CLI exit codes.

## Risks and mitigations

- **Risk:** an agent-created draft is mistaken for compliance. **Mitigation:** drafts stay out of
  `[instantiated]`; the second plan reports them as unregistered, and docs state the boundary.
- **Risk:** a heuristic writes a wrong generated artifact. **Mitigation:** only targets declared in
  `docs/.doc-sync-map.yaml` are refreshed, using the existing labeled generators; a post-write drift
  check fails on remaining drift.
- **Risk:** an existing human document is overwritten. **Mitigation:** create actions are derived
  only for absent targets; `add` also refuses existing files without `--force`, which `evolve`
  never passes.
- **Risk:** unknown facts are guessed. **Mitigation:** undetermined facts are reports only, with the
  tokens a human must declare.
- **Risk:** maturity is read as a phase. **Mitigation:** it is advisory output; no phase write path
  exists in the command.

## Rollback strategy

Remove the `evolve` script, CLI subcommand and runtime entry; revert the tests/docs/state commit.
Generated refreshes are ordinary generator output and can be regenerated; draft files created with
`--allow-add` are unregistered and can be deleted by the owner.

## Success criteria

- `autodoc evolve --repo <project>` is read-only and exits 0 unless `--check` finds pending actions.
- `--write` refreshes generated targets and verifies no drift remains.
- `--write --allow-add` creates missing required docs as drafts; a second plan reports them as
  unregistered and creates nothing.
- Configuration errors exit 2 and write nothing.
- `pytest`, `make ci`, `make audit` and `make package-check` pass; the installed CLI exposes
  `evolve`; no release, tag, PyPI publication, phase change or session closure is included.
