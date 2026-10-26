# Changelog

## 0.3.1 — 2026-10-26

Released `autodoc-docs` 0.3.1 to PyPI via OIDC trusted publishing. The distribution was renamed
from `autodoc` to `autodoc-docs` (the `autodoc` name is taken on PyPI by an unrelated project).
The import package and CLI stay `autodoc`; only the distribution name changes. Tag `v0.3.1`
at commit `f978bc8`.

- Distribution rename guard in `scripts/test_package.py` now derives the PEP 427 filename stem
  from `pyproject.toml` instead of hardcoding, so a rename cannot desynchronise the check from
  the build. Wheel builds as `autodoc_docs-0.3.1-py3-none-any.whl`.
- Fixed `autodoc/__init__.py` version resolution to try `autodoc-docs` first, then fall back to
  `autodoc` for source checkouts.
- `scripts/test_package.py --dist-dir` mode resolves wheel path absolutely so verification works
  in GitHub Actions where the working directory shifts.
- Living state files (CURRENT-STATE.md, NEXT-ACTION.md, RECENT-CHANGES.md) updated to record
  the PyPI publication.

## 0.3.0 — 2026-10-25

First tagged release (Beta). Tag `v0.3.0` points at commit `3748d0f`; the release snapshot and the
wheel/sdist were built from that commit and verified (70-file manifest hashes checked, wheel
installed into a clean venv and run against AutoDOC itself). The debt backlog was closed the same
day: D-009 accepted, D-010 accepted with a clean scan, D-007 explicitly deferred while the phase is
`beta`. PyPI publication was deliberately not performed; the tag remains the release of record.

- Added a tag-triggered `publish` job to the release workflow. It downloads the wheel and sdist the
  snapshot job built in the same run, verifies those exact files with
  `scripts/test_package.py --dist-dir`, and only then uploads them to PyPI through OIDC trusted
  publishing under a `pypi` environment. A manual dispatch still builds and snapshots but never
  publishes, and the job needs `id-token: write`.
- Extended `scripts/test_package.py` with `--dist-dir`: it verifies an existing wheel and sdist
  instead of rebuilding, and refuses filenames that do not match the declared project version. The
  artifact that would be published is therefore the one that was exercised, not a rebuild.
- Publishing stays switched off until the owner registers the PyPI project, its trusted publisher
  (this repository and the `release.yml` workflow) and the `pypi` environment; no PyPI release
  exists yet.
- Renamed the distribution from `autodoc` to **`autodoc-docs`**. `autodoc` on PyPI is already
  taken by an unrelated project, so publishing under it was impossible (and `pip install autodoc`
  would install someone else's package). The import package stays `autodoc` and the CLI stays
  `autodoc`, so `import autodoc` and `autodoc --version` are unchanged; only the distribution name
  and therefore `pip install` change. The guard in `scripts/test_package.py` now derives the
  PEP 427 filename stem from `pyproject.toml` instead of hardcoding it, so a rename cannot
  desynchronise the check from the build.

- Added `autodoc evolve`: a read-only-by-default plan for safe documentation updates on an
  existing project, with `--write` for generated drift, `--write --allow-add` for missing required
  documents as unregistered drafts, and `--check`/`--json` modes. It reuses the existing context,
  profile, catalog and enforcement layers; it never registers or approves a draft, overwrites an
  existing document, edits `autodoc.toml`, or changes the phase/profile/decisions/catalog.
- Recorded the existing `LICENSE` and `CHANGELOG.md` as the homes for the two beta-gated core
  records (`DOC-A10-008`, `DOC-A15-003`); `autodoc promote --to beta` now previews with no
  requirement blockers.
- Added the optional `audit` extra and `make audit`, an operator-run `pip-audit` check for known
  vulnerabilities in the installed environment. It opens the network and stays out of the offline
  `make ci` gate; the runtime dependency set remains empty.
- Stopped the readiness score from counting an `[instantiated]`/`[satisfied_by]` decision whose
  declared path is missing, and made `enforce.collect_findings()` default its root to the tool
  checkout instead of dereferencing `None`.
- Fixed the installed-wheel `autodoc check` path boundary: `[instantiated]` and
  `[satisfied_by]` locations now resolve against the selected `--repo`, not the bundled tool
  root, and the check still reports genuinely missing destinations.
- Made `autodoc add` reject an instance ID already declared by another document and point at
  `--instance` for a distinct ID.
- Corrected the `autodoc promote` preview so it no longer says there are no enforcement changes
  when the phase changes the enforcement mode without adding a requirement.
- Dogfooded the installed wheel against AutoDOC, `Universal_Software_Auditor`,
  `ai_infrastructure`, `requests`, Flask and Express; the packaged-root defect was found by that
  run.
- Added `autodoc add <catalog-id>`: previews or writes one catalog-derived document with a
  project-qualified instance ID and creation date, refuses silent overwrites, and keeps the
  destination inside the selected project.
- Added `autodoc promote --to <phase>`: previews the catalog's newly required and newly failing
  types, refuses a write while a target-phase required document lacks a document or decision,
  preserves the rest of `autodoc.toml`, and writes only the top-level `phase` and
  `phase_declared` values. Demotions, backdates and forced incomplete promotions require
  `--force`, and the remaining findings stay visible.
- Extended `autodoc init` with `--phase` and `--profile` declarations while preserving existing
  files, and shipped the new runtime scripts through the wheel/sdist smoke test.
- Implemented owner-selected D-003: catalog records render canonical, blank or synthetic-example
  variants on demand into ignored `build/TEMPLATES/` through Make and the installed `autodoc templates`
  command. Removed the 795 tracked variants after a byte-for-byte comparison confirmed all generated
  outputs match the prior files; added renderer, CLI and package coverage.
- Added reader-derived audience applicability: catalog `reader` is an implicit AND token (match=true,
  non-match in a non-empty declared set=false/not applicable, empty=unknown, `assess` exempt). Added
  on-demand JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON through `cargo rustdoc`; missing
  tools are reported as L0 for that run, and fake-tool tests cover the integrations.
- Added an installable, zero-runtime-dependency `autodoc` CLI (`check`, `generate`, `adopt`,
  `init`) with separate tool/project roots, wheel/sdist builds, clean-venv smoke coverage and
  Python 3.11–3.15 CI. Tagged runs build temporary GitHub Actions artifacts; PyPI publishing is
  not configured or authorized.
- Extended the structural document check to validate required sections and unchanged prompts for
  the four canonical migration document titles. Draft findings use the existing `placeholders`
  family, approved findings use `stubs`; the check makes no semantic or reversibility claim.
- Selected **Apache-2.0** as the license (owner decision, 2026-10-01): added the canonical
  `LICENSE` text, declared `license = "Apache-2.0"` with `license-files = ["LICENSE"]` in
  `pyproject.toml` (built with setuptools ≥ 77 so the metadata carries
  `License-Expression: Apache-2.0`), and recorded the decision and its consequences in
  `docs/00-governance/LICENSE-DECISION.md` while keeping the comparison of alternatives.
  The release gate no longer blocks on a missing license: it fails closed only if `LICENSE`
  is ever removed, and still requires a `vX.Y.Z` tag checked out at the same commit.
  Licenses are still never inferred from file contents.
- Implemented AutoDOC's deterministic sync, drift, human-review impact and freshness checks.
- Added three catalogs, generated template variants, governed metadata, CI and a task API example.
- Made task API SQLite setup idempotent; added scoped test evidence and health reporting.
- Added self-documenting catalog and CI workflow references plus human architecture/adoption records.
- Added declared owner-scope validation to local and CI checks.
- Added deterministic Python/Markdown/dependency inventories and three catalog navigation views.
- Added checked agent context and a local tool-dispatch example with explicit unsupported web search.
- Added derived human inventory/relationship graph, offline guards and an unsigned run-evidence pack.
- Added a fail-closed release snapshot workflow pending an owner-selected license.
- Reject unsupported demo route, config and SQL changes instead of generating partial references.
- Added described environment and alert extraction with runbook validation.
- Added the local-only allowlisted tool-policy demo, relationship visualization and measured JUnit evidence.
- Hardened ownership/supersedes checks and made Makefile the canonical harness.
- Added an approved-stub check; it failed on 28 title-only `docs/*/_index.md` placeholders, which
  were then retired from the controlled inventory. Health now reports substantive versus stub docs.
- Moved every catalog classification rule out of Python into `CATALOG-RULES.json` (a
  behavior-preserving refactor: 260 ids, names, types and template paths unchanged), added
  `CATALOG-SCHEMA.json` and a validator with an explicit keyword subset, and replaced the
  domain-prefix `priority` with a hand-picked core tier plus detectable `applies_when`
  predicates. Added a file-presence profiler and an applicability report that joins the profile
  with the decisions recorded in `autodoc.toml`.
- Aligned enforcement with the refined phase table: five blocks (advisory, build, beta,
  live+mature, sunset), drift and freshness off until beta, warning at beta, failing from live,
  and sunset reduced to its profile with every other family off. Report-level findings are now
  emitted as informational instead of being dropped, `off` families are named in the report so a
  skipped check is never mistaken for a clean one, the report carries a maturity score relative
  to the declared phase, and the declared context accepts `schema = 1` and `phase_declared`, with
  name-slug keys resolved to catalog ids (ambiguity is an error, and every substitution is
  recorded).
- Added the enforcement layer: `scripts/intelligence/enforce.py` resolves one severity per check
  family (obligations, drift, stubs, placeholders, local links, committed key markers, tribal
  instructions, freshness) from `[severity]`, then the declared phase, then `report`, and reports
  each finding with rule id, severity, location, reason, fix hint and the context that caused it.
  Added the adoption baseline (`autodoc-baseline.json`, schema-checked, keyed by rule and
  location, with stale-entry reporting so it can ratchet down), documented exit codes
  (`0`/`1`/`2`, `docs/reference/EXIT-CODES.md`), a pre-push hook, a dry-run-by-default
  branch-protection helper, and the capability level in every report. The checker functions the
  enforcement layer calls now return structured findings, so severity, baseline and exit codes
  come from one place rather than from printed strings.
- Made project kinds a declaration with evidence behind it (§3): `profile.py` gained a detector
  per detectable kind with stated exactness and limits (packaging shape, entry points, web/data/AI
  dependencies, UI dependencies, deployment and infrastructure files, workspace markers), and the
  kinds no file can honestly separate — `plugin`, `embedded`, `research`, `content`, `template` —
  are marked `declaration-only` with a reason instead of a guess. `make docs-hint` prints the
  evidence for phases and kinds; the declaration in `autodoc.toml` is what counts. Two predicate
  tokens became three-valued: `kind:<id>` is undetermined until kinds are declared, `phase>=<id>`
  until a phase is; both are now consumed by catalog entries (SDK guide, model registry, ETL
  specification, observability strategy, postmortem) so the forms are exercised rather than merely
  allowed. Kind-gated documents and kinds with no supporting evidence are reported, and a
  repository with no evidence at all gets the generic baseline — reported as such, never guessed.
  This repository declares `kinds = ["library"]`; `docs-hint` also suggested `application`, which
  came from an example inside the repository, and that difference is exactly why kinds are asked
  for rather than inferred.
- Moved the core-set decision into data: `CONTROL/metadata/PROFILES.json` holds `default`,
  `startup`, `oss-library`, `internal-service` and `regulated` as deltas of the hand-picked core
  list, each addition carrying a reason and the phases it is off in; `profile` in `autodoc.toml`
  selects one and the report states the resulting set with its additions and removals. Catalog
  entries gained the §5.1 fields — `question` (the reader question), `reader`, `support`
  (`checked` / `template-only` / `human`), `checks`, `events`, and `severity_by_phase`, which
  subsumes the authored `phase_min` (now derived by the generator, so the two cannot disagree).
  An admission rule in `check_catalog.py` requires every type any profile can list to state the
  reader question it answers, a detectable predicate, its phases and named checks or an explicit
  label; a type nothing can detect cannot be required. Two types were reconciled for the
  profiles: `License` (DOC-A10-008) is added as the project's redistribution terms, while the
  old `License inventory` becomes extended (dependency licensing belongs with the SBOM), and
  `Code of conduct` (DOC-A09-009) joins the oss-library profile. A type that is off at the
  current phase is now listed with its reason and the phase it lands at, in both text and JSON.
- Added a declared context: phases with phase-scaled enforcement (undeclared is advisory and
  nothing fails), declared kinds, audiences and obligations, and a validated `autodoc.toml` with
  `[facts]`, `[satisfied_by]`, `[not_applicable]` and `[severity]`. Facts became three-valued
  (`true` / `false` / `unknown`) with stated exactness and limits, and an unknown fact now makes
  an obligation **undetermined** instead of silently satisfied. Predicates gained `kind:<id>`,
  `obligation:<id>` and `{all, any}` forms. Added `README` as the 261st catalog type — the
  every-phase document that was missing — plus a fixture matrix of awkward repositories,
  `make docs-hint`, and `make docs-explain`.
- Made personal data, payments and safety declared traits (§4): `handles_personal_data`,
  `handles_payments` and `safety_critical` are facts about the world, so the vocabulary now names
  its two routes — fifteen facts read from files with stated limits, and three that are
  declaration-only with a stated reason why no detector can exist. `check_catalog.py` follows the
  same honesty rule it applies to kinds: a fact that claims both routes, claims neither, or has no
  consumer is refused. The catalog consumes the traits — the PII inventory plus the new
  `Cardholder data flow` and `Hazard analysis` are core types required only once their trait is
  true, and the deeper privacy set moves to the personal-data trait — so an unanswered trait
  leaves exactly those documents **undetermined**, reported and never read as `false`. Both
  reports state each trait's answer, `--hint` prints the open questions, and this repository
  answers all three `false` with reasons.
- Made generation honest per language and per generator (§6): every generator now declares its
  exactness (`exact` or `heuristic`) and its limits in one table, the label travels in the marker
  of every generated Markdown file, `header()` requires it so a new generator cannot ship
  unlabeled, and a heuristic generator warns by default as `generator.heuristic` — advisory at
  build, pin-able, never silently trusted. Per-language references integrate the language's own
  tool instead of reimplementing it: Python is extracted in-process with the interpreter's parser
  (exact, with docstring summaries), and Go integrates `go doc -all .` behind a probe. The runner
  executes the tool inside the repository with a scrubbed environment (the caller's variables are
  never inherited), the toolchain's offline flags, no shell and a timeout, and a missing, failing
  or hanging tool is reported with its reason rather than replaced or faked. A language with no
  generator is L0 — file and manifest facts only — and both reports say so; `make docs-languages`
  prints the per-language situation, and a reference from an external toolchain is on demand
  (`SHOW=<language>`) and never committed, because a drift-checked target that depends on the
  machine cannot be reproducible. `docs/META/CODE-INVENTORY.md` became the per-language inventory,
  and the automation reference now carries each mapping's exactness and limits.
- Declared the event model instead of implying it (§7): `CONTROL/metadata/TRIGGERS.json` names each
  event, what it runs, what may stop a merge, what is only triage, and what never happens (no
  network from a gate, no bot commit, no scheduled required check). `scripts/intelligence/triggers.py
  --check` verifies the declaration against the repository and runs in `make ci`: every workflow
  must be claimed by a declared job, every declared job exists with the declared trigger events and
  filters, every declared command resolves to a file or Make target, exactly one event blocks and
  one check is required, and a required check may not be path-, tag- or branch-filtered — the
  pending-forever trap. The rendered plan is a mapped generated document
  (`docs/generated/TRIGGER-REFERENCE.md`), so editing a workflow without updating the model fails
  the build; `make docs-triggers` prints the same view with the declared phase's severities.
  The scheduled workflow now matches its posture: every check reports even when an earlier one
  fails and one closing summary makes the run red for triage. External link checking arrived as
  the one network-touching check (`make docs-links-external`), deliberately absent from `make ci`:
  scheduled, one connection at a time, at least a second between requests to the same host, capped
  per run, treating auth and rate-limit answers as reachable, skipping local and reserved example
  hosts as documented-not-deployed, and warn-only unless an owner asks for `--strict`.
