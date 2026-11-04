---
id: DOC-TEST-002
title: "Test plan"
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
related: ["DOC-P2-001", "DOC-TEST-001", "DOC-REF-003", "DOC-ARC-001", "DOC-REF-001", "DOC-P3-GOV-003"]
criticality: medium
review_days: 180
last_verified: 2026-11-04
last_reviewed: 2026-11-04
last_updated: 2026-11-04
auto_generated: false
---
# Test plan

## Purpose and scope

This plan records how AutoDOC is tested, what each layer is allowed to claim, and what "done"
means for a change. It covers the test plan, the unit and integration specifications, the
acceptance criteria and the place where per-run results live, which is why the catalog types
`DOC-A11-002`, `DOC-A11-003`, `DOC-A11-004`, `DEV-B07-002` and `DEV-B07-003` are satisfied by
this page (`[satisfied_by]` in `autodoc.toml`).

It does not restate the test strategy, which lives in
[ENGINE-COVERAGE.md](ENGINE-COVERAGE.md), or the test inventory, which is generated from the
suite in [TEST-INVENTORY.md](../META/TEST-INVENTORY.md). It does not certify that the tests are
sufficient, that prose is true, or that a passing run is compliance evidence. Those limits are
stated in [LIMITATIONS.md](LIMITATIONS.md).

## Test layers

| Layer | Where | What it decides | Runs in the blocking gate |
| --- | --- | --- | --- |
| Unit | `tests/test_*.py`, in-process | Pure functions, parsers, resolvers, generators and guards, including rejected inputs | Yes |
| Golden policy matrix | `tests/fixtures/enforcement/cases.json` and `tests/test_enforcement_contract.py` | Severity resolution, baseline handling, exit codes and report wording across phases and decisions | Yes |
| Integration | `tests/test_phase2.py`, `tests/test_phase3.py`, fixture repositories under `tests/fixtures/repos/` | The whole context → profile → resolver → enforcement path on miniature projects | Yes |
| Process contract | subprocess tests in `tests/test_enforcement_contract.py`, `tests/test_cli.py` | `0`/`1`/`2`/`3` exit codes, agreement between entry points, project-root boundary, dry-run defaults | Yes |
| Generator and release contracts | `tests/test_engine.py`, `tests/test_release_gate.py`, `tests/test_package_dist.py` | Deterministic docs, tag/version/changelog checks, artifact naming | Yes |
| Language and link adapters | `tests/test_languages.py`, `tests/test_external_links.py`, fake toolchains | Missing tools become L0; the network probe is rate-limited, mocked and warn-only | Yes, with the network mocked |
| Package installation | `make package-check` | Wheel and sdist build, sdist rebuild, clean-venv install, CLI smoke | Yes |
| Evidence | `make evidence` | A passing, same-commit, hash-verified unsigned run record | Yes |

The blocking gate is `make ci` on Python 3.11. The compatibility matrix on Python 3.11–3.15
runs `make test` only and is supplemental; it catches interpreter-specific breakage without
multiplying the blocking path.

## Unit test specification

Unit tests cover the smallest unit that owns a decision, not every function for its own sake:

- **Parsers and extractors.** Python AST declarations and tests, Markdown headings, declared
  dependencies, environment and alert extraction, and local tool policy. A parser is trusted
  only once a test shows it rejects the malformed variant as well as accepting the valid one.
- **Context and catalog.** Phase and profile declarations, fact overrides with reasons,
  audience and kind tokens, decision tables, stable catalog ids and counts derived from the
  indexes (`tests/test_catalog_counts.py` keeps prose counts honest).
- **Resolution and severity.** Required versus recommended, applicability predicates,
  three-valued facts, `undetermined` versus `not applicable`, severity pins and baseline
  suppression.
- **Markdown and metadata guards.** Local links, private-key markers, tribal phrases, frontmatter
  and migration prompts.
- **Triggers and release.** Event-model parsing, required-check naming, unfiltered required
  jobs, tag/version/changelog agreement and artifact naming.

Tests are `tests/test_<area>.py`; classes group a behaviour and test names state the rule, not
the implementation. They run offline and isolate writes in temporary directories; read-only tests
may inspect the worktree. The policy layer mocks its collectors instead of depending on their
side effects.
`tests/fixtures/enforcement/cases.json` is the golden matrix: changing a phase, tier or fact
rule must keep the matrix green or change it deliberately. `tests/fixtures/repos/` supplies
docs-only, Python, Node, TypeScript and Go project shapes; `tests/fixtures/toolchains/` supplies
good, failing, slow and stable fake toolchains.

A skipped or expected-failure test is not evidence. It must name the reason and the owner, and
it must not be used to make a red suite look green.

## Integration test specification

- **Golden repositories.** Each fixture is a whole miniature project, so the integration tests
  exercise context loading, fact detection, profile membership, open and recorded decisions,
  phase-scaled severity and the exit code together.
- **Process boundary.** `tests/test_enforcement_contract.py` runs the real entry points in a
  subprocess: a usage or configuration error exits `2`; an internal crash exits `3` and never
  `1`; both entry points agree; `--fail-on-stale` is opt-in; the branch-protection helper is a
  dry run by default and cannot mutate anything when `gh` is broken.
- **Project-root boundary.** `tests/test_cli.py` runs the CLI against temporary project roots
  and asserts that the installed tool's assets and the selected project's `autodoc.toml` do not
  leak into each other.
- **Packaging.** `scripts/test_package.py` builds the wheel and sdist, rebuilds a wheel from the
  sdist, installs it in a clean virtual environment outside the checkout, and exercises
  `version`, `check`, `generate`, `adopt`, `init`, `add`, `promote`, `evolve` and `templates`.
  `tests/test_package_dist.py` refuses an artifact set whose names or version do not match the
  declared project.
- **Adapters.** Language generators are exercised through fake toolchains, including missing,
  failing and slow tools; the external-link checker is exercised with mocked transports and
  asserts the rate limit and warn-only posture. No blocking test opens the network.
- **Evidence.** `make evidence` runs the real suite, then refuses to package a run that failed,
  came from another commit, has mismatched output hashes, or follows a documentation-drift or
  critical-freshness failure. A passing pack is a same-commit record, not an approval.

## Acceptance criteria

A change is acceptable when all of the following hold. A green gate alone is not acceptance;
it is the minimum.

1. **Behaviour is tested.** New or changed behaviour has a test that failed before the change and
   passes after it. Parsers and validators also have a rejected-input test.
2. **The blocking gate passes.** `make ci` passes locally and the required
   `AutoDOC guard / check` check passes on the pull request.
3. **Documentation is regenerated, not hand-edited.** Mapped targets are rebuilt, committed with
   their sources, and `make docs-drift` reports `IN SYNC`.
4. **Human-owned impact is reviewed.** Affected living-state files and mapped human documents are
   updated in the same change, and the change analyzer clears against the pull request base.
5. **No unapproved dependency or platform change.** The runtime dependency list stays empty; a
   dependency change has an owner decision and an ADR, and a licence compatible with Apache-2.0.
6. **Claims match artifacts.** Evidence attached to a change is an actual run, from the same
   commit, with its scope named. No audit, test or backup is claimed without its artifact.
7. **Release changes pass the release gate.** The tag is `vX.Y.Z`, equals `project.version`, has
   a `## <version>` section in [CHANGELOG.md](../../CHANGELOG.md), and `LICENSE` is present.
8. **Owner-only actions are approved.** Tagging, publishing, ruleset changes and history
   rewrites are not implied by a green pull request.

## Where results live

Test results are per-run records, not a committed snapshot. Committing them would make the next
commit stale by definition, so the repository keeps the mechanism and the audit trail, not a
copy of every run.

| Artifact | Produced by | Contains | Retention |
| --- | --- | --- | --- |
| `evidence/out/test-evidence.json` | `make evidence` or the CI check job | Commit, command, exit code, JUnit counts, Python and pytest versions, stdout/stderr hashes, full output | Local; replaced on the next run |
| `evidence/out/` evidence pack | `make evidence` | The test record plus check results, a documentation record, an unsigned source record, an SBOM with no components (runtime dependencies are empty) and a manifest of artifact hashes | Local; replaced on the next run |
| `autodoc-test-evidence` CI artifact | `docs-guard.yml`, `if: always()` | The same test-evidence JSON from the actual run | GitHub Actions retention; not committed |
| `autodoc-evidence-pack` CI artifact | `docs-guard.yml`, `if: always()` | The full pack from the actual run | GitHub Actions retention; not committed |

`make evidence` refuses a test record that failed, that belongs to another commit, or whose
output hashes do not match, and it refuses to package after documentation drift or a critical
freshness failure. The pack is explicitly `unsigned: true`: SHA-256 proves the stored bytes did
not change, not who produced them or whether anyone approved them. There is no signing key or
trust policy here; see [EVIDENCE-SIGNING.md](EVIDENCE-SIGNING.md).

A recorded run, kept as a dated snapshot rather than a live status:

| Date | Commit | Command | Result |
| --- | --- | --- | --- |
| 2026-11-04 | `6c84a53` | `make ci` | 331 tests and 188 subtests passed (519 JUnit cases), package check passed, evidence hashes verified |

The authoritative current result is the latest CI artifact for the commit under review, not this
table. The table records that a full run was actually verified when this page was written.

## Coverage, flakiness and scope limits

- **Coverage is a floor, not a proof.** `pyproject.toml` declares branch coverage with
  `fail_under = 70`; it was measured at 74% lines+branches on 2026-10-26. The threshold is
  enforced by the local ci-fabric stage in `ci.toml`, not by the offline `make ci` gate. A
  passing threshold says which lines ran, not whether the assertions are meaningful.
- **No flaky retries.** A test that fails intermittently is a defect. Retrying until green hides
  the defect and is not an acceptance path.
- **The suite is offline.** Blocking tests do not resolve DNS or open sockets. The external-link
  check is scheduled, rate-limited and warn-only; `make audit` is an operator-run network check.
- **Unsupported inputs must be honest.** An ecosystem without a reader, a toolchain that is not
  installed, or a format with no extractor is reported as L0 or as an error, never silently
  treated as passing. The suite pins that behaviour for the supported languages.
- **The suite cannot judge prose.** It proves structure, bounded extraction, exit codes and
  packaging. Semantic correctness, architecture quality and regulatory compliance remain human
  judgements.

## Verification and references

- `make test` — the full pytest suite.
- `make ci` — the blocking gate, including package installation and evidence verification.
- `make package-check` — the clean-venv install and CLI smoke described above.
- `make evidence` and `make check-evidence` — produce and hash-verify a local unsigned pack.
- `python scripts/intelligence/triggers.py --check` — confirms the CI wiring this plan assumes.
- [ENGINE-COVERAGE.md](ENGINE-COVERAGE.md) — the strategy and its honest limits.
- [TEST-INVENTORY.md](../META/TEST-INVENTORY.md) — generated per-file test discovery.
- [QUALITY-GATES.md](../reference/QUALITY-GATES.md) — what blocks a merge or release.
- [EXIT-CODES.md](../reference/EXIT-CODES.md) — the process contract the tests enforce.
