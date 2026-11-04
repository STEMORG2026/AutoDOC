---
id: DOC-REF-002
title: "Troubleshooting guide"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-11-04
next_review: 2027-05-03
source_of_truth: human
supersedes: null
related: ["DOC-REF-001", "DOC-REF-003", "DOC-P3-GOV-001", "DOC-ARC-001", "DOC-P2-001"]
criticality: medium
review_days: 180
last_verified: 2026-11-04
last_reviewed: 2026-11-04
last_updated: 2026-11-04
auto_generated: false
---
# Troubleshooting guide

## Purpose and scope

This guide is for anyone running `autodoc` or this repository's `make` targets and getting a
result they did not expect. It explains how to read the exit code, find the check that produced
a finding, and fix the input rather than the symptom. It does not replace the command help
(`autodoc <command> --help`), the catalog explanation of one type
(`make docs-explain DOC=<ID>`), or the reference pages linked below.

It is not a bug tracker and it does not certify a repository. AutoDOC checks that documents
exist and are structurally sound and extracts bounded facts; it cannot prove prose true or a
project compliant. [LIMITATIONS.md](../00-governance/LIMITATIONS.md) states what the checks
cannot see, and [ENGINE-COVERAGE.md](../00-governance/ENGINE-COVERAGE.md) states how confidence
is established.

## Start with the exit code

Every command shares one contract, documented in full in [EXIT-CODES.md](EXIT-CODES.md):

| Code | Meaning | First move |
| --- | --- | --- |
| `0` | Nothing at failing severity. An advisory run, a clean run, or a run whose findings are all baseline-suppressed. | Read the report and decide what to write next. |
| `1` | Findings at `error` severity, or a mapped check (drift, freshness, stubs, links) failed. | Fix the finding, record a decision, or baseline it during adoption. |
| `2` | The declaration or invocation is invalid: unknown phase, profile, catalog id, rule or fact; missing mapped path; malformed baseline; unreadable TOML. | Fix the input. The repository was not judged. |
| `3` | AutoDOC itself failed. The message says so explicitly. | Report a bug with the details below. |

Two distinctions explain most confusion:

- **`2` is not `3`.** A rejected declaration is your input; a crash is the tool. Neither says
  anything about documentation quality.
- **`0` can mean "nothing new".** A baseline suppresses recorded findings, and an undeclared
  phase makes every finding advisory. A missing `autodoc.toml` is **not** a configuration
  error: `autodoc check` reports `phase: undeclared (advisory)` and exits `0`. Enforcement
  starts when a phase is declared.

## Diagnose before changing anything

```sh
autodoc check --repo . --json --output /tmp/autodoc-report.json
autodoc check --repo . --config path/to/autodoc.toml
make docs-recommend                  # applicable types and recorded decisions
make docs-explain DOC=DEV-B07-003    # what one type asks for and why it applies
make docs-triggers                   # which event runs what, and what blocks a merge
make docs-health                     # measured counts, not correctness
```

`--json` is the machine-readable form; `--output` keeps it out of the terminal. `--repo`
selects the project root and `--config` selects a different context file, so a wrong root is
easy to spot before editing declarations.

Read the finding's rule family before acting:

| Family | What it means | Usual fix |
| --- | --- | --- |
| `recommend.core` | A required type has no document or recorded decision; or a skip is contradicted by a now-true predicate. | Write or register the document, or record a decision. |
| `recommend.extended` | A recommended type has no document. | Write or register it, or decide it does not apply. |
| `recommend.decision` | A recorded decision is being displayed for review. | Read it; no action unless it no longer holds. |
| `drift` | A generated target differs from its sources. | Regenerate and commit both. |
| `freshness.review`, `freshness.critical` | A human document is past `next_review` or `last_verified + review_days`. | Obtain a real review. |
| `stubs`, `placeholders` | An approved document is title-only, or a template prompt is unfilled. | Write it or remove it. |
| `links.local` | A relative Markdown link does not resolve. | Fix the path or the target. |
| `tribal` | An instruction depends on private knowledge. | Replace it with a documented owner or process. |
| `secrets.inline` | A private-key marker is committed into tracked text. | Remove it from history and rotate the key. |
| `generator.heuristic` | A generator names a limit a human should review. | Review the output; it is a hint, not proof. |

The effective severity of each family depends on the declared phase and on pins in
`autodoc.toml`; the header of `autodoc check` prints the pins in force. `off` means the check
does not run, `report` prints without failing, `warn` never fails the gate, and `error` does.

## Installation and environment

- **Python 3.11–3.15.** The package declares `requires-python = ">=3.11,<3.16"` and has no
  runtime dependencies. A different interpreter is unsupported, not silently tolerated.
- **Two install modes.** Install the release with `python -m pip install autodoc-docs==0.4.0`,
  or work from a source checkout with `make setup`, which creates `.venv/` and installs the
  development extras. Mixing a global `autodoc` with a checkout is the usual source of
  "the command does not see my change".
- **Stale editable metadata.** If `autodoc --version` disagrees with `pyproject.toml` after a
  version change, the environment still has the old distribution metadata. Reinstall with
  `.venv/bin/python -m pip install -e . --no-deps` (or rerun `make setup`).
- **`make secret-scan` exits `2` when `gitleaks` is not on `PATH`.** Install it from its signed
  release page or run the scan in CI; the target never downloads a scanner.
- **`make audit` needs the optional `audit` extra and opens the network.** It is intentionally
  not part of the offline `make ci` gate.
- **go-task is optional.** The `Taskfile.yaml` targets delegate to `make`; a missing `task`
  binary is not an AutoDOC failure.
- **Missing language tools are not failures.** `make docs-languages SHOW=javascript` reports
  whether a generator's external tool is available. Without it, that language stays at L0
  (file and manifest facts only) for that run.

## Configuration errors (exit 2)

Typical messages:

```text
Enforcement error: context.phase: 'nonsense' is not a declared phase
[error] context.config autodoc.toml [instantiated]: DOC-A22-005 points at a missing path docs/nope.md
```

The frequent causes:

- **Unknown phase or profile.** Phases are `idea`, `prototype`, `build`, `beta`, `live`,
  `mature`, `sunset`; profiles are `default`, `startup`, `oss-library`, `internal-service`,
  `regulated`. A phase is a declaration, never an automatic transition.
- **A mapped path that does not exist.** `[instantiated]` and `[satisfied_by]` paths resolve
  against the project root (`--repo`), not against the directory containing the config file.
  URLs in `[satisfied_by]` are recorded and existence-checked only by a human; local paths are
  checked on every run.
- **An unknown catalog id.** Use an id from `CATALOG-A` or `CATALOG-B`; ids are stable and are
  never renumbered for a new entry.
- **A `[not_applicable]` entry without a reason.** The reason is mandatory and is displayed.
- **An unknown rule in `[severity]`.** A severity for a rule nothing honours is rejected as
  inert data.
- **An unknown fact, or a `[facts]` override with no reason.** Every override must say why the
  detector is wrong for this repository.
- **A malformed or missing baseline.** Run without `--baseline`, or regenerate it with
  `--write-baseline` after fixing the configuration.

`make docs-catalog` validates the catalog and declared context; `make docs-metadata` validates
controlled Markdown frontmatter. Both are independent of the findings report.

## Findings (exit 1)

- **Required, recommended, undetermined.** A required type with no document and no decision is
  a finding that can fail the gate; a recommended one warns at `beta`. Undetermined means a
  predicate could not be evaluated (usually a fact is `unknown`), and it is reported separately
  rather than quietly treated as "not applicable". Answer the declaration instead of guessing.
- **Baselines ratchet.** `--write-baseline` records current findings during adoption and
  excludes configuration errors and `secrets.inline`. A matching entry is suppressed; an entry
  whose finding was fixed becomes stale and warns; deleting an entry by hand brings the finding
  back. `--fail-on-stale` turns stale entries into a failure. A baseline is not a blanket and
  should not be used to hide a problem you can fix.
- **A skip contradicted by a true predicate.** `recorded not_applicable, but its predicate is
  true now (has_tests); re-check` means the fact behind the skip became true. Confirm the
  reason still holds, or remove the skip and write the document. The checker re-surfaces the
  contradiction by design; there is no permanent silence for it.
- **Overdue review.** The due date is the earlier of `next_review` and
  `last_verified + review_days`. Obtain a real review and update the record; resetting a date
  without reading the document defeats the check. Overdue critical documents fail; other
  overdue documents warn unless pinned.

## Generated-document drift

A target that starts with `<!-- AUTO-GENERATED BY AUTODOC ENGINE. ... -->` is written from the
sources named in `docs/.doc-sync-map.yaml`. Do not edit it by hand: the next generation run
will overwrite the edit, and CI reports drift.

```sh
make generate              # rewrite targets from sources
make docs-drift            # read-only check; prints IN SYNC on success
autodoc generate --root /path/to/project --check
```

`autodoc generate` needs the target project's `docs/.doc-sync-map.yaml`. When the message is
`Missing source`, `Unsupported SQL` or an unsupported language, fix the map or the source, or
add a tested extractor; unsupported formats must fail or be documented as not implemented,
never silently pass. References produced by external toolchains are printed on demand and never
committed, because the same repository on two machines could disagree.

## Review and living-state checks

- `review <target>` or `Living state not updated` means a mapped human document or a
  living-state file needs a real update in the same change. Co-change is a prompt, not a
  certification of accuracy.
- `change_analyzer.py --base <ref>` compares commits, so uncommitted edits are invisible to it.
  Use `make docs-staged-impact` for the index, and the pull request's base SHA in CI.
- `BASE=origin/master make self-doc` compares committed `HEAD` with `origin/master`; fetch
  first, or the comparison uses a stale remote ref.

## Release and packaging

- `Release blocked` or `Tag ... does not match` comes from the release gate. The tag must be
  `vX.Y.Z`, equal `project.version`, and have a matching `## <version>` section in
  [CHANGELOG.md](../../CHANGELOG.md); `LICENSE` must exist; the checkout must be at the tag
  commit; generated documentation must be in sync and no critical review may be overdue.
- `make package` builds the wheel and source distribution into `dist/`. `make package-check`
  additionally rebuilds from the sdist and exercises the installed CLI in a clean virtual
  environment outside the checkout.
- **Publishing is tag-only.** A manual dispatch of the release workflow builds and snapshots but
  never uploads. The publish job verifies the exact artifact built in the same run before
  trusted publishing. See [QUALITY-GATES.md](QUALITY-GATES.md) for the full sequence.

## When it is a tool bug (exit 3)

Exit `3` means AutoDOC failed, not the repository. Report it with:

- `autodoc --version` and `python --version`;
- the exact command and the smallest project or configuration that reproduces it;
- the message and, when available, the `--json` report;
- whether the failure is reproducible without network access.

Do not report a security vulnerability in a public issue; follow [SECURITY.md](../../SECURITY.md).
Usage questions belong in the issue tracker with the same details, because "the command
returned 2" and "the command crashed" have different owners.

## Verification and references

This guide is kept true by the same commands it describes:

- `autodoc check --repo .` — the report header, rule families and exit code in practice.
- `make docs-catalog`, `make docs-metadata`, `make docs-drift` — the checks named above.
- `make docs-triggers` — the event model rendered from `CONTROL/metadata/TRIGGERS.json`.
- [EXIT-CODES.md](EXIT-CODES.md) — the authoritative code contract per command.
- [QUALITY-GATES.md](QUALITY-GATES.md) — what blocks a merge or a release, and what reports.
- [QUICK-START.md](../../QUICK-START.md) — install, adopt, promote and evolve workflows.
- [LIMITATIONS.md](../00-governance/LIMITATIONS.md) — what a clean run does not prove.
