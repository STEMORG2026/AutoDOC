# Plan — C4R7 — installable AutoDOC Python CLI/package

| Field | Value |
| --- | --- |
| Objective | Turn AutoDOC's current repository-only scripts into an installable, dependency-free Python CLI with a buildable wheel/sdist and isolated-install smoke coverage. |
| Owner of the work | `C4R7` (session `20261021-1820-C4R7`) |
| Status | **CLOSED (owner's word, 2026-10-23) — PR #12 merged at `08229a0`** |
| Opened (UTC) | 2026-10-21T18:20Z |

## Scope

**In:** a small `autodoc` console entry point for version/check/generate/adopt/init; wheel and sdist packaging that includes the runtime scripts and their catalog/policy assets; project-root handling that works from an installed wheel; isolated installation and CLI smoke tests; build artifacts in CI release workflow; supported Python-version declaration and concise usage/limitations documentation.

**Out:** publishing to PyPI or configuring trusted publishing (requires owner account/project settings); deploying a hosted service; adding runtime dependencies; changing enforcement semantics or claiming semantic/compliance validation; closing the paused B71a session without the owner's explicit close.

## Approach

1. Treat AutoDOC as the repo-based documentation tool described in README; preserve zero runtime dependencies and expose its existing operations rather than redesigning the engine.
2. Add a console script that dispatches to the existing scripts from a packaged runtime-data root; accept an explicit project root for checks and generation.
3. Package the runtime Python files plus the machine-readable catalog/context data required by the CLI; keep development docs/state/tests out of the installed runtime.
4. Add build metadata and a build/install smoke test that builds an sdist/wheel, installs the wheel into a clean venv, exercises CLI commands against a temporary project, and verifies version/help/errors.
5. Integrate package verification into CI/release artifacts, document supported Python versions and install/use limits, then run `make generate`, `make check`, `make ci`, and staged-impact checks.

## Risks and mitigations

- **Risk:** scripts currently conflate installed tool resources and the project being checked. **Mitigation:** keep the package runtime root separate from explicit `--repo`/`--root` project paths; test from a clean venv outside the source checkout.
- **Risk:** package-data rules silently omit a required schema/catalog/script. **Mitigation:** assert required runtime files at CLI startup and exercise `check`, `generate`, `init`, and `adopt` from an installed wheel.
- **Risk:** a wheel may be installable but not publishable/released. **Mitigation:** build and attach artifacts only; do not claim PyPI publication or use credentials.
- **Risk:** broad “production ready” language could overstate the result. **Mitigation:** scope the deliverable to an installable CLI/package and keep the existing structural-only limits explicit.

## Rollback strategy

Remove the `autodoc` entry point and package-data build support, restore the prior `pyproject.toml` and release workflow, and run `make generate` plus `make ci`. Existing repository scripts remain the source-compatible interface.

## Success criteria

- `pip install <wheel>` in a clean environment provides `autodoc --version`, `check`, `generate`, `adopt`, and `init` without runtime dependencies.
- The installed CLI operates on an explicit temporary project root without relying on the source checkout.
- Both wheel and sdist build successfully; CI retains required gate naming and verifies distribution artifacts.
- Documentation states what is supported and does not call AutoDOC a hosted service or compliance certificate.

## Outcome recorded

- `make ci`: **267 tests + 190 subtests passed** on local Python 3.11; evidence hashes verified.
- `make package-check`: wheel/sdist build, sdist-to-wheel rebuild, and clean installed-wheel smoke (version/help/invalid usage plus check/generate/adopt/init) passed.
- `make package`: produced the 0.2.0 wheel and sdist. No runtime dependencies were added.
- Commits `6af0c03` and `b8ba4c2` are on `arena/072fcb8c-autodoc`; PR #12 merged into `master` at `08229a0`.
- GitHub's required `AutoDOC guard / check`, impact job and supplemental Python 3.11–3.15 matrix all passed. Local Python 3.11 `make ci` also passed.
- No PyPI publishing or trusted-publishing setup was authorized. C4R7 remains paused awaiting explicit owner closure; do not close B71a.
