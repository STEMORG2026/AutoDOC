---
id: DOC-P3-GOV-010
title: "Release and deployment runbook"
type: PROC
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-11-05
next_review: 2027-05-04
source_of_truth: human
supersedes: null
related: ["DOC-P3-GOV-009", "DOC-P3-GOV-003", "DOC-P3-GOV-005", "DOC-P3-GOV-001", "DOC-REF-003", "DOC-REF-002", "DOC-TEST-002", "DOC-GOV-001", "DOC-P2-003", "DOC-CI-001", "DEV-AGENT-001"]
criticality: high
review_days: 180
last_verified: 2026-11-05
last_reviewed: 2026-11-05
last_updated: 2026-11-05
auto_generated: false
---
# Release and deployment runbook

## Purpose and scope

This page is the procedure for releasing AutoDOC: from the decision to cut a version, through the
tag that triggers CI, to the published `autodoc-docs` distribution on PyPI, the verification that
follows, and the correction path if the published release is wrong. It answers the catalog type
`DOC-A15-005` (Deployment runbook), which is why `autodoc.toml` records that type as satisfied
by this page.

"Deployment" here means **package publication**, not a service rollout. AutoDOC ships a Python
library and a CLI. It has no server, no container, no infrastructure-as-code and no deploy
workflow, so the `has_deploy` fact is false and there is no environment to roll back. The
catalog's separate rollback type (`DOC-A15-006`) is gated on `has_deploy` and therefore does not
apply. What follows is the release path that exists, plus the package-level correction path that
is its honest equivalent of a rollback.

In scope: the version decision, the preflight gate, creating and pushing the tag, what CI does
with it, what PyPI does with it, how the result is verified, and what to do when it is wrong.

Not in scope: what the distribution contains (the
[supply chain record](SUPPLY-CHAIN.md)), which checks block a merge
([quality gates](../reference/QUALITY-GATES.md)), and how the suite is run
([test plan](TEST-PLAN.md)).

This is a procedure, not a certificate. It does not prove that a published release is correct,
secure or compliant, and it makes no claim about service operations, on-call duty or incident
response, because this project has none.

## Details and decisions

### Authority and roles

- The repository owner (`@Er-Sajan-PLG`, per `CONTROL/metadata/OWNERSHIP-MATRIX.yaml`) decides
  the version number, approves the tag and the publication, and performs any PyPI correction.
  Creating a tag, publishing a release and yanking a release are owner decisions.
- [AGENTS.md](../../AGENTS.md) lists tagging, publishing and outward-facing actions as forbidden
  without the owner's explicit approval for that specific action. An agent may prepare the
  change, run the checks and report the result; it may not tag or publish.
- CI is the executor, not the decision-maker. It verifies; it does not choose a version.

### Step 1 — Decide the version

The version in `pyproject.toml` is the single source of truth, and the release gate compares it
against the tag. Observed practice: a new user-visible CLI capability moves the minor version
(`autodoc adopt` → 0.4.0); a fix moves the patch version. The version bump is committed and
merged **before** the tag, because the gate refuses a tag that disagrees with the declared
version.

### Step 2 — Preflight

Everything below is checked locally before the tag exists:

```sh
make generate      # rebuild generated documents from their sources
make docs-drift    # must print IN SYNC
make ci            # the blocking gate: docs, enforcement, impact, tests, package, evidence
make secret-scan   # advisory; needs gitleaks on PATH
```

And by eye:

- `pyproject.toml` `project.version` is the intended `X.Y.Z`.
- `CHANGELOG.md` has a `## X.Y.Z` section. The gate matches the heading `^## X.Y.Z` followed by
  whitespace or end of line, so `## 0.4.0 — 2026-11-04` passes and `## Unreleased` does not.
- `LICENSE` is present. The gate fails closed without it.
- The release commit is merged into `master`, and `master` equals `origin/master`.
- The tag will point at that exact commit.

### Step 3 — Tag

```sh
git tag vX.Y.Z <commit-sha>
git push origin vX.Y.Z
```

The tag is the release trigger. `v0.4.0` is a lightweight tag pointing directly at commit
`56e24af` — the GitHub API reports that ref's object type as `commit`, not `tag`.

There is **no tag ruleset and no tag protection rule** on this repository (checked 2026-11-04);
the only ruleset covers the `main` branch. Pushing a `v*.*.*` tag is therefore enough to start a
publication. Adding tag protection is an owner decision, listed below as an open gap.

### Step 4 — What the tag triggers

Pushing the tag starts two workflows (observed for `v0.4.0`):

| Workflow | File | Result on the tag |
| --- | --- | --- |
| AutoDOC release snapshot | `.github/workflows/release.yml` | Builds the snapshot and the distribution; publishes on a tag |
| AutoDOC guard | `.github/workflows/docs-guard.yml` | Runs the documentation check against the tagged tree |

**Snapshot job.** It checks out the tagged tree at full depth, installs Python 3.11, and runs

```sh
python scripts/doc-control/release_snapshot.py --tag "$TAG" --output "$RUNNER_TEMP/autodoc-release"
```

That script is the release gate. It refuses the release unless all of the following hold:

1. The tag matches `v<major>.<minor>.<patch>`.
2. The tag's version equals `project.version` in `pyproject.toml`.
3. `CHANGELOG.md` contains a `## <version>` section.
4. `LICENSE` exists.
5. The checkout's `HEAD` is the tagged commit.
6. Generated documentation is in sync with its sources (`engine.generate(check=True)`).
7. No controlled document whose `criticality` is `critical` is overdue for review. This
   repository has no `critical` document today, so in practice the drift check is the part of
   this condition that can block; an overdue review at `high` or below prints a warning and
   does not stop the release.
8. The snapshot output directory does not already exist — an existing snapshot is never mutated.

It then writes every controlled document plus `RELEASE-MANIFEST.json`, which records the tag,
the commit and the SHA-256 of each file. The job installs `build>=1,<2`, runs `make package`, and
uploads two artifacts: `autodoc-release-snapshot` (the document snapshot) and
`autodoc-python-distribution` (the wheel and sdist from `dist/`).

**Publish job.** It runs only when `github.ref` starts with `refs/tags/v`, needs the snapshot job,
and uses `environment: pypi` with `permissions: {contents: read, id-token: write}`. It downloads
`autodoc-python-distribution` **from the same run**, re-verifies those exact files, and only
then uploads:

```sh
python scripts/test_package.py --dist-dir dist
# then: pypa/gh-action-pypi-publish@7245906fb61fa33a13554f9d5fb856fe61758086
```

Because the job downloads rather than rebuilds, what is verified is what is uploaded.

### Step 5 — What the artifact verification proves

`scripts/test_package.py --dist-dir dist` checks, against the downloaded files:

- Exactly one wheel and one sdist, named `autodoc_docs-<version>-py3-none-any.whl` and
  `autodoc_docs-<version>.tar.gz`. The name stem is derived from `pyproject.toml`, so a rename
  cannot desynchronise the guard from the build.
- The wheel carries the required runtime files under its `.data/share/autodoc/` prefix, and does
  **not** ship the development-only `scripts/test_package.py` harness or the private `engine`
  package as a top-level install.
- The sdist contains one top-level source directory, no absolute paths, no `..` escapes and no
  special files, and rebuilds into a wheel.
- The wheel installs into a clean virtual environment outside the checkout, and the installed CLI
  reports the declared version, lists all nine supported commands in `--help`, exits `2` on an
  invalid command, and exercises `templates`, `adopt`, `init`, `add`, `promote`, `check --json`
  and `evolve --json` against a throwaway project.

It does not prove the code is correct, safe or useful.

### Step 6 — Publish to PyPI

The upload uses **OIDC trusted publishing**. No API token is stored in this repository; the
publish job exchanges its OIDC token for a PyPI upload token through the trusted publisher
registered for this repository and workflow file. The publisher recorded in the 0.4.0 attestation
is `GitHub/STEMORG2026/AutoDOC/release.yml`, environment `pypi`.

The `pypi` GitHub environment exists with **no protection rules and no deployment branch policy**
(checked 2026-11-04). There is therefore no manual approval step between the tag and the upload:
pushing a `v*.*.*` tag publishes. The safeguards that do exist are the owner's tag discipline
and the gate in step 4, not a second approval.

**Manual dispatch.** `workflow_dispatch` takes a required `tag` input, described upstream as an
"Existing version tag checked out at the same commit". The snapshot job runs and uploads its
artifacts, but the publish job is skipped, because `github.ref` is a branch ref rather than a
tag. Use it to re-run the gate and rebuild the artifacts for an existing tag without
publishing. No dispatch run has been made on this repository (checked 2026-11-04).

### Step 7 — Verify the published release

```sh
gh run list --workflow=release.yml --limit 5
gh run view <run-id>
curl -s https://pypi.org/pypi/autodoc-docs/json | python -m json.tool | head -40
curl -s https://pypi.org/integrity/autodoc-docs/<version>/<wheel-filename>/provenance
```

Check all four:

1. The workflow run concluded `success`.
2. PyPI lists the wheel and the sdist for the new version, and neither file is yanked.
3. The integrity endpoint returns PEP 740 provenance for both files.
4. A clean environment can install the exact version and `autodoc --version` reports it.

Observed for 0.4.0 on 2026-11-04:

- Tag `v0.4.0` → commit `56e24af`.
- Run `41789431156`, success, created 2026-11-04T07:01:50Z, updated 07:02:35Z; the release was
  published at 07:02:30Z.
- PyPI project `autodoc-docs` (owner `Er.Sajan-PLG`).
- Wheel SHA-256 `9f002267044f6a18e6b2a0bbc603722c3c0f4e530d3639db4f8bd5519c1746f3`.
- PEP 740 provenance present for the wheel and for the sdist, publisher
  `GitHub/STEMORG2026/AutoDOC/release.yml`, environment `pypi`.
- No GitHub Release object exists for any tag. The tag, the `CHANGELOG.md` section and the PyPI
  release are the release record.
- Both workflow artifacts — `autodoc-release-snapshot` and `autodoc-python-distribution` — expire
  on 2027-02-02, the repository's default 90-day retention. Download and store the snapshot
  outside the repository if it must be kept; the manifest's own scope says "unsigned local
  documentation snapshot; store externally for retention".

### Step 8 — Correct a wrong release

PyPI's rules bound what can be done, and they are not negotiable:

- A release can be **yanked**, but deletion is permanent and irreversible: a deleted project,
  release or file cannot be restored, and a deleted file cannot be re-uploaded.
- Yanking applies to the **whole release**, not to individual files.
- A yanked release is ignored by installers, unless it is the only release matching an `==` or
  `===` specifier (PEP 592).
- A filename can never be reused, even after a project is deleted and recreated. A published
  version therefore cannot be replaced in place; the correction is a new version.

Procedure, all of it an owner action:

1. Decide the release is broken — it does not install, it violates its own compatibility
   guarantee, or it contains a security issue.
2. Yank it: `https://pypi.org/manage/project/autodoc-docs/releases/` → **Options** → **Yank** →
   confirm, and give a reason. PyPI strongly encourages a reason; it is shown on the release page
   and in the index APIs.
3. Verify the yank: `GET /simple/autodoc-docs/` (JSON) reports `"yanked": true` for that
   version's files.
4. Fix the cause on `master` and cut a **new version** (`X.Y.Z+1`) through steps 1–7. The broken
   version's filenames are not reusable, so a re-upload under the same version is not an option.
5. Record what happened in `CHANGELOG.md` and in the failure log below.

What yanking does **not** do: it does not remove the files from PyPI, it does not uninstall the
package from anyone who already installed it, and it does not stop
`pip install autodoc-docs==X.Y.Z` — an installer still accepts a yanked release when it is the
only match for an exact specifier. A yank can be undone by un-yanking the release, which is why
it is preferred to deletion.

### Observed failures

These are real runs, not hypotheticals.

1. **Runs `40272129345` and `40272550733` (2026-10-26, tag `v0.3.1`) — the snapshot job refused
   the release.** Message: `Release blocked: Doc drift or critical freshness failure; release
   aborted`. The tagged commit's generated documentation did not match its sources. Fix: run
   `make generate`, commit the regenerated documents, and tag the corrected commit.
2. **Runs `40271932742` and `40272322153` (2026-10-26, tag `v0.3.1`) — the publish job refused
   the artifact.** Message: `Package check failed: package verification command failed`,
   preceded by `Could not install packages due to an OSError: [Errno 2] No such file or
   directory: '.../installed-smoke/dist/autodoc_docs-0.3.0-py3-none-any.whl'` and the same for
   `0.3.1`. The check looked for the wheel under the smoke-test working directory's `dist/`
   subdirectory, where the wheel was not. The fix — resolving the wheel path absolutely in
   `--dist-dir` mode — merged in PR #33 (`80fbd3e`); the current script resolves it with
   `wheel.resolve()`. Run `40272720960` for the same tag then succeeded.
3. **Run `41789431156` (2026-11-04, tag `v0.4.0`) succeeded**, so the same path works end to end
   today.

A tag that points at the wrong commit cannot be corrected silently: deleting or moving a tag is
an owner decision under [AGENTS.md](../../AGENTS.md), and rewriting history is forbidden. The
recovery is a new version, or an owner-approved tag move.

### Decisions

- **The tag is the only publish trigger.** The publish job is guarded by
  `startsWith(github.ref, 'refs/tags/v')`, so a manual dispatch can rebuild and snapshot but can
  never upload. There is no path that publishes without a `v*.*.*` tag.
- **Verify the exact artifact before upload.** The publish job re-runs the package check against
  the downloaded `dist/` files rather than rebuilding, so the thing checked is the thing
  published.
- **No GitHub Release object.** The workflow creates none and none exists. The tag, the
  `CHANGELOG.md` section and the PyPI release are the release record; adding GitHub Releases
  would add a fourth artifact to keep in step.
- **Yank, never delete.** Deletion is irreversible and frees no filename; yanking is the
  documented non-destructive alternative and can be undone.
- **A broken release is corrected by a new version**, because PyPI forbids reusing a filename.
- **Two gaps are left open for the owner, deliberately.** The `pypi` environment has no required
  reviewers, so a tag push publishes without a second approval; and there is no tag ruleset, so
  a tag can point at any commit. Both are repository settings rather than code, and both are
  owner decisions under [AGENTS.md](../../AGENTS.md).

## Verification and references

Run locally:

```sh
make generate
make docs-drift
make ci
make secret-scan
python scripts/doc-control/release_snapshot.py --tag vX.Y.Z --output /tmp/autodoc-release
python scripts/test_package.py --dist-dir dist
gh run view <run-id> --log-failed
```

The local snapshot command only succeeds on a checkout of the tagged commit — the same condition
the CI job enforces.

Related records:

- `.github/workflows/release.yml` — the pipeline this page describes.
- `scripts/doc-control/release_snapshot.py` — the release gate.
- `scripts/test_package.py` — the artifact verification.
- [CHANGELOG.md](../../CHANGELOG.md) — the release history; the gate requires a `## <version>`
  section in it.
- [SUPPLY-CHAIN.md](SUPPLY-CHAIN.md) — SBOM, provenance and licenses of what is published.
- [QUALITY-GATES.md](../reference/QUALITY-GATES.md) — which checks block and which advise.
- [TEST-PLAN.md](TEST-PLAN.md) — how the suite is run and where results live.
- [TROUBLESHOOTING.md](../reference/TROUBLESHOOTING.md) — diagnosing local failures.
- [EVIDENCE-SIGNING.md](EVIDENCE-SIGNING.md) — why no release record here is signed.
- [LICENSE-DECISION.md](LICENSE-DECISION.md) — the Apache-2.0 decision the gate depends on.
- [LIMITATIONS.md](LIMITATIONS.md) — what a clean release does not prove.
- [ADOPTION.md](ADOPTION.md) — the catalog selection, including this type.
- [AGENTS.md](../../AGENTS.md) — the forbidden-action list that keeps tagging, publishing and
  yanking owner decisions.
- [SECURITY.md](../../SECURITY.md) — vulnerability reporting; a security issue in a published
  release follows that path.
- `CONTROL/metadata/TRIGGERS.json` — the trigger model. It describes the release workflow's
  snapshot job; it does not yet describe the publish job.

External references consulted for this page (2026-11-05):

- PyPI — yanking: <https://docs.pypi.org/project-management/yanking/>
- PyPI — publishing troubleshooting (filename reuse): <https://docs.pypi.org/publishing/troubleshooting/>
- PyPI — project management troubleshooting (deletion is permanent): <https://docs.pypi.org/project-management/troubleshooting/>
- PyPI — publishing with trusted publishing: <https://docs.pypi.org/publishing/publishing-to-pypi/>
- PyPI — the index API (`yanked` per file): <https://docs.pypi.org/api/index-api/>
- PEP 592 — yanked releases: <https://peps.python.org/pep-0592/>
