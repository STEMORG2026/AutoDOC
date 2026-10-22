# Quick start

AutoDOC is a self-updating, self-documenting documentation engine with **truthful, verifiable
automation and explicit limits**. The installable CLI supports Python 3.11–3.15 and has no runtime
dependencies. Install Python 3.11+, make, and optionally go-task for source development.

```sh
make setup          # isolated development/build/test dependencies and pre-commit hooks
make ci             # canonical docs, tests, package install smoke and evidence checks
make package        # build wheel + sdist into dist/
make package-check  # build, rebuild from sdist, install in a clean venv, exercise CLI
make docs:drift     # read-only generator check (IN SYNC on success)
make evidence       # actual tests + unsigned run evidence
```

`Taskfile.yaml` is available for [go-task](https://taskfile.dev/) users. The go-task binary is not
installed in this environment; use the same `make` targets instead of treating task absence as a
documentation-engine failure.

## Install the CLI

Download the wheel from the `autodoc-python-distribution` artifact of a tagged GitHub Actions
release run, create an environment, and install the wheel by path:

```sh
python -m venv .venv
. .venv/bin/activate                 # Windows: .venv\\Scripts\\activate
python -m pip install /path/to/autodoc-0.2.0-py3-none-any.whl
autodoc --version
autodoc check --repo /path/to/project
autodoc generate --root /path/to/project --check
```

Available commands are `check`, `generate`, `adopt` (read-only heuristic scan), and `init` (draft
scaffold in an existing directory). The 3.11–3.15 CI compatibility matrix is supplemental and
non-blocking; the configured required gate runs full `make ci` on Python 3.11. The installed tool
assets are separate from the selected project root. `check` honors that project's `autodoc.toml` and baseline; an undeclared phase is
advisory unless severity is pinned. `generate` needs the target project's
`docs/.doc-sync-map.yaml`. The release workflow creates temporary workflow artifacts only: AutoDOC
is not published to PyPI and does not create a GitHub Release. These checks establish structural
facts and bounded extracted facts, not semantic correctness or regulatory compliance.

## Dependencies and versions

The engine itself needs **no third-party runtime packages** — `pyproject.toml` declares
`dependencies = []` and the code imports only the standard library
([why](docs/adr/0001-zero-runtime-dependencies.md)). The development tools, declared as bounded
ranges in `[project.optional-dependencies].dev`, are `build>=1,<2`, `pytest>=8,<10`, and
`pre-commit>=3,<5`. `make setup` resolves them into `.venv/`; `make ci` verifies both source tests
and an installed wheel. There is no lockfile and no automated updater; version changes are made in
the manifest and verified by a full `make ci` run. The policy for choosing, updating and removing
dependencies — including vulnerability and licence handling — is in
[CONTRIBUTING.md](CONTRIBUTING.md#dependencies).

## Adopt an existing project

1. Run `autodoc adopt --project-path /path/to/project` (or `python scripts/adopt.py --project-path ...` in a source checkout) for **heuristic suggestions**; it does not modify the project or establish regulatory applicability. Common dependency and build caches are pruned from the scan.
2. Browse [the 265-type catalog](docs/01-catalogs/CATALOG-INDEX.md), select relevant types,
   assign real owners and record non-applicability. Do not copy 265 empty documents.
3. Configure the target project, choose an explicit phase/profile, and adapt a sync map to its actual sources. Generate only factual references with supported extractors, and create human-owned records for design decisions.
4. In a source checkout, run `make docs:verify`, `make test`, and `make package-check`; enable required checks/CODEOWNERS approval manually in repository settings. For an installed tool, use `autodoc check --repo /path/to/project`. AutoDOC cannot observe an unrelated project until configured there.

## New project and new documents

`autodoc init --name "My App" --type web-api --output /existing/project` creates ten **draft** foundations without overwrites. The source-checkout equivalent is `python scripts/init-project.py --name "My App" --type web-api --output /existing/project`. The type is recorded in scaffold prompts; the same ten foundation types are created for every type. `1970-01-01` means unverified.
For a single type, render its blank variant into the target project's ignored build tree with
`autodoc templates --root /existing/project --variant blank` or, in a source checkout,
`make docs-templates TEMPLATE_VARIANT=blank`. Copy the matching `build/TEMPLATES/<category>/<ID>.md.blank`,
assign a new *instance* ID, real owner/reviewer, actual review dates and project-specific facts;
then add a source/review mapping. Catalog IDs name *types*, not deployed artifacts. To add a type,
update `CONTROL/metadata/CATALOG-RULES.json` and run `make generate` to rebuild the catalog indexes;
variants render separately on demand.

## Add a deterministic extractor

Implement a scoped parser in `engine/extractors/`, render facts in `scripts/doc-sync/engine.py`,
add a mapped source/target in `docs/.doc-sync-map.yaml`, and test accepted and rejected inputs.
Run `make generate && make ci`; update [engine coverage](docs/00-governance/ENGINE-COVERAGE.md).
Unsupported formats must fail or be documented as not implemented, never silently pass.

## Interpret a failure

- `Generated documentation drift: path`: inspect its map sources, run `make generate` and
  commit source with target. Do **not** hand-edit an AUTO-GENERATED file.
- `review <target>` or `Living state not updated`: have a human review the listed document,
  update it and stage it. Co-change does not certify accuracy.
- `overdue review (critical)`: obtain a real review; do not simply reset a date.
- `Missing source` or `Unsupported SQL`: fix the map/source or add a tested extractor.
- `Release blocked`: read `docs/00-governance/LICENSE-DECISION.md`; the gate fails when
  `LICENSE` is missing, the tag is not `vX.Y.Z`, or the checked-out commit is not the tagged one.

Run `make help` for all aliases. Use `make docs:staged` for staged changes; `make docs:impact`
compares committed HEAD to `BASE=origin/master` and does **not** include uncommitted edits.
