# Plan — 912C — owner-selected D-003 on-demand templates

| Field | Value |
| --- | --- |
| Objective | After reconciling PR #14/#15, implement the owner's D-003 selection: keep one catalog source record per type and render canonical, blank and synthetic-example variants on demand into ignored `build/TEMPLATES/`. |
| Owner of the work | `912C` (session `20261022-1011-912C`) |
| Branch | `arena/d5317c9e-autodoc`, based at PR #15 merge `990113b5c496b833af9e855cb6e3870d816c1cb4` |
| Status | **IN PROGRESS — implementation, `make ci`, pre-commit and staged impact passed; PR #17 is open/mergeable and all checks passed on `af1e68c` (a state-only update triggers a fresh run); PR #16 remains open/mergeable on the earlier branch per the no-close instruction, with all checks passed; do not merge or close either PR without owner authorization** |
| Opened (UTC) | 2026-10-22T10:39Z |

## Predecessor work

- PR #14 merged at `7a0fd47`; D-004/D-002 remain implemented on `master`.
- PR #15 was explicitly authorized, merged at `990113b`, and its state/check-status reconciliation is on `master`.
- The owner selected D-003 after PR #15 settled. Selection was recorded in `state/DECISIONS.md` before any D-003 code changes.
- Measured pre-migration tree: 265 catalog types, 265 canonical + 265 blank + 265 example outputs (795 generated variant files), and two explanatory README files under `TEMPLATES/`.

## Scope

**In:**
- Keep `CATALOG-A/B/INDEX.yaml` as the single per-type source; the current `library.py` already deterministically derives all three variants from each catalog entry.
- Make template rendering explicit/on-demand, with the default destination `build/TEMPLATES/` (ignored by Git); support an individual variant or all variants.
- Expose the same renderer through a Make target and the installed `autodoc templates` CLI, bundling only the renderer and catalog data required by the package.
- Update validation, completeness/health/relationship reports, package smoke tests, usage documentation, and migration safeguards to describe renderable outputs rather than committed files.
- Remove the 795 generated variants from `TEMPLATES/`, retaining its two explanatory README files.

**Out:** D-007 evidence signing, D-009 external dogfood, further adoption/promotion scope, hosted service, PyPI publication, closing any paused session, or merging the D-003 review PR without explicit owner authorization.

## Approach

1. Keep all work on the assigned branch `arena/d5317c9e-autodoc`; selection is recorded before implementation.
2. Extend `scripts/doc-control/library.py` to validate catalog source records and render selected variants beneath an output root; default to `build/TEMPLATES/` and fail closed on invalid/colliding destinations.
3. Add `make docs-templates` and `autodoc templates`; keep ordinary `make generate` and CI from materializing ignored output as a side effect.
4. Reconcile catalog validation, completeness/health, relationship links, generated outlines, package runtime data, and documentation with logical output paths and on-demand rendering.
5. Add tests for output paths, all variants, isolation from the consumer project, source-tree cleanliness, and a clean installed wheel/sdist CLI. Verify deterministic generation against the existing renderer before removing its committed outputs.
6. Run generation, documentation checks, `make ci`, package smoke, pre-commit and staged impact; commit and push only this branch; open a review PR and wait.

## Risks and mitigations

- **Risk:** treating `doc['template']` as a checked-in file after removing it. **Mitigation:** retain its catalog-defined relative render destination, validate its shape, and make every consumer render or display `build/<path>` deliberately.
- **Risk:** quietly changing sample output during migration. **Mitigation:** compare all 795 pre-migration outputs byte-for-byte against the existing deterministic renderer before deleting them; test every supported variant.
- **Risk:** installed `autodoc templates` cannot find catalog sources. **Mitigation:** include the renderer and catalog indexes in wheel/sdist runtime data; exercise the command from a clean installed environment outside the checkout.
- **Risk:** generated files pollute Git. **Mitigation:** default to the existing ignored `build/` tree and add a guard that rejects committed variant outputs.

## Rollback strategy

Revert only D-003 changes on this branch; leave PR #14/#15 merge commits on `master` untouched. The renderer remains usable against the catalog source if generated files are deleted.

## Success criteria

- The catalog remains the one source per type; no canonical/blank/example variant output is tracked (the two explanatory README files may remain).
- Rendering all 265 types produces 795 deterministic files beneath `build/TEMPLATES/`; selecting one variant writes only that variant.
- `make docs-templates` and installed `autodoc templates` render into the requested project/build directory without consulting the consumer's catalog or files.
- Validators and reports distinguish renderability from materialized output; normal `make generate`/`make ci` do not write template outputs.
- `make ci`, the clean package install smoke, pre-commit and staged impact pass; follow-up PR remains open for owner review.

## Execution record — 2026-10-22

- Compared all 795 generated canonical/blank/example files with the tracked pre-migration variants: **795/795 byte-for-byte identical**. Removed the 795 tracked variants only after this comparison; retained the two README files.
- The targeted D-003 suite passed (70 tests, 65 subtests); the Make target rendered 265 blank variants to a temporary output tree.
- `make ci` passed on Python 3.11: 288 tests, 190 subtests, package smoke and evidence hash verification (not signatures). Staging, `pre-commit run --all-files` and `make docs-staged-impact` passed; commits `71ba468`, `156ba8e`, `7fa962b` and `af1e68c` are pushed on the assigned branch. PR #17 is open/mergeable and all checks passed on `af1e68c` (a state-only update triggers a fresh run); PR #16 remains open/mergeable on the earlier branch per the no-close instruction, with all checks passed after reopening. Do not merge or close either PR without owner authorization.
