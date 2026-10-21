# Plan — B71a — migration prose validation

| Field | Value |
| --- | --- |
| Objective | Extend the existing structural-document check so instantiated migration design/plan/test-plan/guide docs must replace their canonical prompts with authored section content, without claiming semantic review. |
| Owner of the work | `B71a` (session `20261021-1459-B71a`) |
| Status | **PAUSED (awaiting owner)** |
| Opened (UTC) | 2026-10-21T14:59Z |

## Scope

**In:** controlled human-owned Markdown with one of the four migration titles represented in catalog templates (`Migration design`, `Migration plan`, `Migration test plan`, `Migration guide`); required sections and prompt detection based on those templates; draft findings routed to the existing `placeholders` family and approved findings to `stubs`; integration with `stub_check.collect()` and its direct check; regression tests; generated references and concise documentation of limits.

**Out:** a new enforcement family or independent gate; parsing or validating SQL/database migration code; checking that migrations are reversible; inventing an OpenAPI contract; judging truth/adequacy of prose; changing catalog applicability; or creating migration documents for the demo (it has no migrations and its persistent-state fact is declared false).

## Approach

1. Reuse the existing controlled-document/frontmatter discovery and define a small, explicit contract for the four migration titles using their canonical section names and prompt sentences.
2. Parse Markdown headings and prose without counting frontmatter, code fences, comments or quoted template boilerplate. Report missing sections, empty sections, or retained canonical prompts; skip generated docs and unrelated titles.
3. Return findings through the existing structural policy: drafts use `placeholders`, approved docs use `stubs`, preserving phase severity, pins and baseline handling. Integrate with `stub_check.collect()` and `make docs-stubs`; do not add a parallel gate.
4. Add tests for valid prose, all prompt variants, missing sections, draft-vs-approved family assignment, generated/unrelated docs, and the repository's current no-migration state.
5. Update the architecture/coverage and living/changelog docs, regenerate mapped targets, then run focused tests, `make check`, and `make test`/`make ci` as the environment permits.

## Risks and mitigations

- **Risk:** a structural check may be misread as proof the migration plan is safe. **Mitigation:** name the check as structural, document that it cannot establish truth, completeness or reversibility, and keep semantic approval human-owned.
- **Risk:** the repository has no migration instance, so an untested scanner could appear green vacuously. **Mitigation:** test the validator with temporary controlled fixtures for each title and explicit negative cases.
- **Risk:** a future template wording change could desynchronize the prompt detector. **Mitigation:** test the canonical templates and keep accepted titles/headings/prompts in one small module with clear tests.

## Rollback strategy

Remove the migration-specific rules and tests from `stub_check.py`, restore the documentation, then run `make generate` and the verification suite. No application data or migration files are modified.

## Success criteria

- The check ignores unrelated/generated docs and reports only the four defined migration titles.
- Missing/empty required prose and unchanged template prompts route to existing `placeholders` (draft) / `stubs` (approved); the direct checker warns on drafts and fails approved docs, while CI retains phase/pin severity.
- Tests prove the behavior using fixtures even though AutoDOC itself has no migration instance.
- Mapped outputs are regenerated and `make check` plus the full test suite pass.
