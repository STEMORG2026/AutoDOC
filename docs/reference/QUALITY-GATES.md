---
id: DOC-REF-003
title: "Quality gates"
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
related: ["DOC-ARC-001", "DOC-REF-001", "DOC-REF-002", "DOC-CI-001", "DOC-P2-001", "DOC-P3-GOV-003"]
criticality: medium
review_days: 180
last_verified: 2026-11-04
last_reviewed: 2026-11-04
last_updated: 2026-11-04
auto_generated: false
---
# Quality gates

## Purpose and scope

This page says which automated checks can stop a change, which only report, and what each one
actually proves. It is written for contributors deciding what to run before opening a pull
request, and for reviewers deciding whether a red job is a blocker.

The authoritative wiring is `CONTROL/metadata/TRIGGERS.json`, rendered by
`make docs-triggers` and verified against the workflow files by
`python scripts/intelligence/triggers.py --check` (part of `make ci`). This page explains that
model; it does not replace it. When the two disagree, the trigger model and the workflow files
win, and this page is wrong.

A gate proves structure and bounded facts. It does not prove that prose is true, that an
architecture is sound, or that a project is compliant. [LIMITATIONS.md](../00-governance/LIMITATIONS.md)
lists the blind spots, and [ENGINE-COVERAGE.md](../00-governance/ENGINE-COVERAGE.md) describes
how confidence is established.

## The one blocking gate

The protected default branch requires exactly one status check:

| Property | Value |
| --- | --- |
| Required check | `AutoDOC guard / check` |
| Workflow and job | `.github/workflows/docs-guard.yml`, job `check` |
| Trigger | `pull_request`, `push`, `workflow_dispatch` |
| Path or tag filter | none — the check reports on every pull request |
| Strict mode | required: the branch must be up to date before merging |
| Also enforced by the ruleset | deletion and non-fast-forward protection on the default branch |

GitHub matches a required status check by the **job name**, not by the `workflow / job` string
shown in the UI, so the job is deliberately named `AutoDOC guard / check`. Renaming it without
updating the ruleset silently disables the gate. The live ruleset `main` was verified against the
repository on 2026-11-04 with:

```sh
gh api repos/STEMORG2026/AutoDOC/rulesets
gh api repos/STEMORG2026/AutoDOC/rulesets/<id>
```

The dry-run payload that `make docs-require-check` prints states the same requirement;
`APPLY=1` changes repository settings and is an owner action, not a contributor step.

The `check` job runs `make ci` on Python 3.11 and then, on pull requests, compares the branch
with its base commit:

```sh
make ci
python scripts/intelligence/change_analyzer.py --base "$BASE"
```

It checks out with full history (`fetch-depth: 0`) because the impact analysis needs the base
commit, and it uploads the actual test-run JSON and the evidence pack even when the job fails.

## What `make ci` runs

`make ci` is the canonical local equivalent of the blocking job. Its stages are ordered so a
cheap structural failure is reported before an expensive build:

| Stage | Command | What it establishes | What it does not establish |
| --- | --- | --- | --- |
| `check` | `make docs-verify` | Frontmatter, inventory, ownership coverage, review dates, sync map, generated drift, stubs, catalog schema, template library, completeness, local links, key markers | That the content is correct or complete |
| `docs-enforce` | `scripts/intelligence/enforce.py` | Findings at the declared phase's severity, with the documented exit code | That the declared phase is the right phase |
| `self-doc` | sync map, trigger model, ownership, catalog drift, change analyzer | That source changes have their mapped review paths, and that the event model matches the workflows | That a human actually reviewed the mapped document |
| `test` | `pytest` | The behaviour the suite covers, including accepted and rejected inputs | Behaviour no test exercises |
| `package-check` | `scripts/test_package.py` | Wheel and sdist build; sdist rebuilds a wheel; the wheel installs in a clean venv outside the checkout and the CLI runs | That the package works on an unsupported interpreter |
| `evidence` | test evidence, evidence pack, hash verification | An unsigned record of the run, its scope and its artifact hashes | Identity, approval, or signed provenance |

`make check` is the fast PR-equivalent subset; `make test` is pytest alone; `make lint` adds the
frontmatter validator to the guard pass. Use the smaller targets while diagnosing, but do not
treat a green subset as a green gate.

The evidence pack is deliberately unsigned. SHA-256 verifies that stored artifacts did not
change, not who produced them or whether anyone approved them. There is no signing key or trust
policy in this repository; see [EVIDENCE-SIGNING.md](../00-governance/EVIDENCE-SIGNING.md).

## Advisory jobs and events

These run on pull requests or on a schedule but do not block a merge. A red result is triage for
a human, not a merge veto.

| Job or event | Where | Posture | Why it is not required |
| --- | --- | --- | --- |
| `Python compatibility` (3.11–3.15) | `docs-guard.yml` | supplemental | The required gate already runs the full suite on 3.11; the matrix catches version-specific breakage without multiplying the blocking path. |
| `Dependency audit` (`pip-audit`) | `docs-guard.yml` | advisory, network | It queries a live advisory service. A transient outage or a new advisory must not block an unrelated documentation change. |
| `Secret scan` (`gitleaks`) | `docs-guard.yml` | report | The scanner is pinned and checksum-verified, and the scan is local, but the job is not in the ruleset. A finding is a red job for triage, not a merge veto. |
| `impact` | `self-doc-check.yml` | advisory, path-filtered | It runs only when implementation, catalog or workflow paths change. A path-filtered job may not report at all, so it cannot be the sole required check. |
| Generation preview | `docs-generation-preview.yml` | report after merge | It publishes a diff artifact for review; no bot commit is pushed and no pull request is affected. |
| Nightly and Monday freshness | `docs-staleness.yml` | triage | It surfaces drift, overdue review and external link rot on a schedule. The external link check opens the network and is rate-limited and warn-only; it never blocks. |

At the time of writing (2026-11-04), `Dependency audit` runs in `docs-guard.yml` but is not
listed in `CONTROL/metadata/TRIGGERS.json`. The trigger check verifies every declared job and
every workflow file, not every job inside an already-declared workflow, so the audit job is not
yet visible in `make docs-triggers`. Treat it as advisory until the model lists it.

## Reproducing a gate locally

```sh
make setup                 # .venv, development extras, pre-commit hooks, generated docs
make ci                    # the full blocking job
make lint                  # guards plus frontmatter validation
make docs-staged-impact    # change analyzer over the index
BASE=<sha> make self-doc   # change analyzer over committed HEAD
make audit                 # optional: pip-audit, opens the network
make secret-scan           # optional: gitleaks over the full history
```

The pre-push hook (`make hooks-install`) runs `make docs-enforce` only. It is a convenience that
`git push --no-verify` bypasses; the required check remains the real gate. The hook does not run
the test suite or the package check.

## The release gate

Publishing is a separate, tag-triggered sequence in `.github/workflows/release.yml`. A manual
dispatch builds and snapshots but **never** publishes.

1. **Snapshot job.** For a `vX.Y.Z` tag it requires: a semantic-version tag; a tag that equals
   `project.version` in `pyproject.toml`; a matching `## <version>` section in
   [CHANGELOG.md](../../CHANGELOG.md); a present `LICENSE`; a checkout at the tagged commit;
   generated documentation in sync; and no critical review overdue. It then builds the wheel and
   sdist and uploads both the snapshot and the distributions as temporary artifacts.
2. **Publish job.** It runs only for tag refs, downloads the distribution artifact from the same
   run, re-runs `scripts/test_package.py --dist-dir` against those exact files, and only then
   uploads them to PyPI through OIDC trusted publishing under the owner-registered `pypi`
   environment. A manual dispatch cannot reach this job.

PyPI records attestations for trusted-publishing uploads. Those are provenance records for the
upload, not SLSA attestations and not signed documentation evidence; this repository makes no
stronger claim.

## Changing a gate

- **Workflow changes must be declared.** A new workflow file must be claimed by a declared job,
  and every declared command must resolve, or `triggers.py --check` fails as part of `make ci`.
  A job added inside an already-declared workflow is not currently detected — update the model
  anyway so `make docs-triggers` stays accurate.
- **Keep the required check unfiltered and uniquely named.** A path or tag filter can prevent the
  required check from reporting, which blocks every pull request that skips it.
- **Ruleset changes are owner actions.** Do not change branch protection, required checks or
  bypass actors from a pull request. `make docs-require-check` prints the payload and changes
  nothing without `APPLY=1`.
- **Do not weaken a check to make a change pass.** Fix the input, or record a reasoned decision
  in `autodoc.toml`; a pinned severity or a baseline is visible in the report and in review.
- **Update this page and the trigger model together**, so the explanation and the wiring cannot
  drift apart.

## Verification and references

- `make docs-triggers` — the event model, required check and declared job wiring.
- `python scripts/intelligence/triggers.py --check` — verifies the model against the workflows.
- `make ci` — the blocking job's exact stages.
- `.github/workflows/docs-guard.yml`, `release.yml`, `self-doc-check.yml`,
  `docs-generation-preview.yml`, `docs-staleness.yml` — the workflows themselves.
- [TRIGGER-REFERENCE.md](../generated/TRIGGER-REFERENCE.md) — the generated reference.
- [TEST-INVENTORY.md](../META/TEST-INVENTORY.md) — what the suite contains.
- [EXIT-CODES.md](EXIT-CODES.md) — how a failing run distinguishes findings from tool failure.
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — what to do when a gate fails.
