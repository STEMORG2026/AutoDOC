---
id: DOC-P3-GOV-002
title: "Branch and tag protection (as configured)"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.2"
effective_date: 2026-09-26
next_review: 2027-05-04
source_of_truth: human
supersedes: null
related: ["DOC-P3-GOV-010", "DOC-REF-003", "DOC-P3-GOV-009", "DOC-GOV-001", "DOC-CI-001", "DOC-P3-GOV-001"]
criticality: high
review_days: 180
last_verified: 2026-11-05
last_reviewed: 2026-11-05
last_updated: 2026-11-05
auto_generated: false
---
# Branch and tag protection (as configured)

## Purpose and scope

This page records the protection that is **actually in force** on this repository, read back from
the GitHub API on 2026-11-05. It is a record of a configuration, not a wish list and not a
certificate.

It covers three settings that together decide what can reach the default branch, what can create
or move a release tag, and what has to happen before a package is uploaded:

- the **branch ruleset** that covers `master`;
- the **tag ruleset** that covers `v*.*.*` release tags;
- the **`pypi` deployment environment** that the publish job must pass.

Out of scope: what the required check verifies (that is the
[quality gates](../reference/QUALITY-GATES.md) record), and how a release is cut and corrected
(that is the [release runbook](RELEASE-RUNBOOK.md)).

Three things are deliberately **not** claimed here, because they are not configured:

- a pull request is **not** required — the branch ruleset has no "require a pull request" rule;
- code-owner approval is **not** required — `CODEOWNERS` exists but no rule enforces it;
- signed commits and linear history are **not** required.

## Details and decisions

### The repository these settings apply to

| Property | Value |
| --- | --- |
| Repository | `STEMORG2026/AutoDOC` (owner type: organization; public) |
| Default branch | `master` |
| Collaborators with write access | one — `Er-Sajan-PLG`, with admin |
| Protection mechanism | **rulesets**, not legacy branch protection |

The single-collaborator fact is the reason two common protections are absent, and it is stated
here so the absence reads as a decision rather than an oversight.

### The branch ruleset

| Field | Value |
| --- | --- |
| ID | `25542481` |
| Display name | `main` |
| Target | `branch` |
| Enforcement | `active` |
| Selector | `ref_name.include = ["~DEFAULT_BRANCH"]` |
| Bypass actors | none (`bypass_actors: []`, `current_user_can_bypass: never`) |
| Rules | `deletion`, `non_fast_forward`, `required_status_checks` |

The required check is `AutoDOC guard / check`, bound to the GitHub Actions app
(`integration_id: 15368`), with `strict_required_status_checks_policy: true` — a pull request must
be up to date with `master` before it can merge — and `do_not_enforce_on_create: false`.

**The display name is `main`; the default branch is `master`.** The name is a label. The
*selector* is `~DEFAULT_BRANCH`, a built-in reference that resolves to whatever the repository's
default branch is — here `master`. The ruleset therefore does cover `master`; the name is
historical and was not renamed when the default branch was.

**What it does not do.** There is no "require a pull request before merging" rule, so the ruleset
does not require a pull request. What it requires is that `AutoDOC guard / check` has passed on
the commit being pushed; how that commit arrives — a pull-request merge or a direct fast-forward —
is not constrained by any rule in this ruleset. Pull requests are this repository's normal path,
not a configuration-enforced one.

### The tag ruleset

| Field | Value |
| --- | --- |
| ID | `26592865` |
| Display name | `release-tags` |
| Target | `tag` |
| Enforcement | `active` |
| Selector | `ref_name.include = ["refs/tags/v*.*.*"]` |
| Bypass actors | none (`bypass_actors: []`, `current_user_can_bypass: never`) |
| Rules | `required_status_checks`, `deletion`, `update` |

The required check is the same one — `AutoDOC guard / check`, `integration_id: 15368` — with
`strict_required_status_checks_policy: false` and `do_not_enforce_on_create: false`.

Three properties of this ruleset are worth stating separately, because each removes a different
accident:

- **There is no `creation` rule.** A `creation` rule would stop the tag being created at all.
  There is none, so a release tag can still be created — but only on a commit whose
  `AutoDOC guard / check` has already succeeded. The check is recorded on the *commit*, and the
  guard workflow runs on every push, so a commit that has been merged into `master` acquires the
  check when that workflow finishes. Tagging before the run completes is rejected; tag after it.
- **The `deletion` rule** stops a release tag being deleted.
- **The `update` rule** stops a release tag being moved to a different commit.

Because there are no bypass actors, those two rules bind the owner too: the only way to delete or
move a release tag is to change or delete the ruleset first. That is deliberate — a published
release's tag is part of the release record — and it is also why correcting a wrong tag is
recorded as an owner action with admin rights, not a routine operation.

### The `pypi` deployment environment

| Field | Value |
| --- | --- |
| Name | `pypi` |
| Protection rules | `required_reviewers` — reviewer `Er-Sajan-PLG` |
| `prevent_self_review` | `false` |
| `can_admins_bypass` | `false` |
| `deployment_branch_policy` | `null` (any ref may deploy) |

The publish job in `.github/workflows/release.yml` declares `environment: pypi`, so a tag push now
produces a deployment that **waits for a reviewer** instead of uploading immediately. Only one of
the required reviewers has to approve, and that reviewer is the repository owner.

`prevent_self_review` is `false` because the owner is the only collaborator and the owner is also
the person who creates the tag and pushes it. With self-review prevention on, the one person
able to approve would be the one person forbidden from approving, and no release could ever be
published. The protection that survives is a real one: the upload waits for a deliberate approval
click rather than following the push automatically.

`deployment_branch_policy` is `null` because the tag ruleset, not the environment, is what
constrains the ref: the publish job's own `if: startsWith(github.ref, 'refs/tags/v')` guard means
it only ever runs for a tag, and the tag ruleset only permits a tag on a commit whose check has
passed.

### Reading the configuration back

```sh
# Both rulesets, in full.
gh api repos/STEMORG2026/AutoDOC/rulesets --jq '.[] | {id, name, target, enforcement}'
gh api repos/STEMORG2026/AutoDOC/rulesets/25542481
gh api repos/STEMORG2026/AutoDOC/rulesets/26592865

# Which rules actually apply to the default branch.
gh api repos/STEMORG2026/AutoDOC/rules/branches/master --jq '.[] | {type, ruleset_id}'

# The environment the publish job must pass.
gh api repos/STEMORG2026/AutoDOC/environments/pypi
```

**The legacy endpoint is not evidence.** `GET /repos/STEMORG2026/AutoDOC/branches/master/protection`
returns `404 {"message": "Branch not protected"}`. That says only that this repository does not
use *legacy branch protection*; the legacy API knows nothing about rulesets. The ruleset-based
read above is the correct one, and it returns three rules for `master`. Reading the 404 as
"unprotected" would be wrong.

### CODEOWNERS is declared but not enforced

`.github/CODEOWNERS` lists `@Er-Sajan-PLG` for `*`, `/docs/`, `/CONTROL/`, `/TEMPLATES/` and
`/EXAMPLE-PROJECT/docs/`. No ruleset rule requires a code-owner approval, so those entries carry
no enforcement today: they are a routing map, not a gate.

Requiring it was not configured because GitHub does not count a pull request author's own approval
("Pull request authors cannot approve their own pull requests" — GitHub's *Approving a pull
request with required reviews*). With exactly one collaborator, every pull request would be its
own author's, so a code-owner requirement would block every pull request permanently.

### `make docs-require-check` is superseded

`scripts/doc-control/require-docs-check.py` prints the classic
`required_status_checks` payload and, with `APPLY=1`, PUTs it to
`.../branches/<branch>/protection/required_status_checks`. That is the **legacy** endpoint, which
this repository does not use. The script stays a dry-run reference: it changes nothing without
`APPLY=1`, and with `APPLY=1` it would write to an endpoint this repository does not read. The
live configuration is the ruleset, and it is changed through the rulesets API.

### Undo paths

Each of these is an owner action with admin rights. None of them rewrites history.

| To undo | Command |
| --- | --- |
| The tag ruleset | `gh api -X DELETE repos/STEMORG2026/AutoDOC/rulesets/26592865` |
| The branch ruleset | `gh api -X DELETE repos/STEMORG2026/AutoDOC/rulesets/25542481` |
| The environment's reviewer | `gh api -X PUT repos/STEMORG2026/AutoDOC/environments/pypi --input -` with `{"reviewers": [], "wait_timer": 0, "prevent_self_review": false, "can_admins_bypass": true, "deployment_branch_policy": null}` |

Deleting a ruleset takes effect on the next push; it does not alter any commit, and it does not
undo a release that was already published. A published release is corrected the way PyPI allows —
by yanking and cutting a new version — as described in the [release runbook](RELEASE-RUNBOOK.md).

### Decisions

- **Rulesets, not legacy branch protection.** One mechanism covers branches and tags, and the
  ruleset API is what the repository's own tooling can read back.
- **The required check stays the single gate.** `AutoDOC guard / check` is required on `master`
  and on release tags; nothing else is required. `Python compatibility`, `Secret scan`,
  `Dependency audit` and `impact` stay advisory, so a flaky advisory job cannot block a merge.
- **A release tag is immutable without an owner action.** `deletion` and `update` with no bypass
  actors mean a tag cannot quietly be rewritten.
- **A tag needs the check to have passed, but a `creation` rule is not used.** Blocking tag
  creation outright would break the release path; requiring the check keeps the tag honest.
- **One approval for publication, with self-review allowed.** The environment's required reviewer
  turns "push a tag and it publishes" into "push a tag and approve the deployment", which is a
  real step in a single-collaborator repository. Blocking self-review would make it impossible.
- **A pull request is not required.** The check is the gate; the pull request is the habit.

## Verification and references

```sh
gh api repos/STEMORG2026/AutoDOC/rulesets --jq '.[] | {id, name, target, enforcement}'
gh api repos/STEMORG2026/AutoDOC/rules/branches/master --jq '.[].ruleset_id'
gh api repos/STEMORG2026/AutoDOC/environments/pypi --jq '{protection_rules, can_admins_bypass}'
gh api repos/STEMORG2026/AutoDOC/collaborators --jq '.[].login'
```

Related records:

- [RELEASE-RUNBOOK.md](RELEASE-RUNBOOK.md) — what a tag triggers, and how a published release is
  corrected.
- [QUALITY-GATES.md](../reference/QUALITY-GATES.md) — what the required check actually verifies,
  and which jobs are advisory.
- [SUPPLY-CHAIN.md](SUPPLY-CHAIN.md) — what is published, and under which provenance.
- [TRIGGER-REFERENCE.md](../generated/TRIGGER-REFERENCE.md) — the declared event model, including
  the release and dependency-audit events.
- `CONTROL/metadata/TRIGGERS.json` — the trigger model that names the required check.
- `.github/workflows/release.yml` — the `publish` job and its `environment: pypi`.
- `.github/CODEOWNERS` — the declared owners, not an enforced gate.
- [AGENTS.md](../../AGENTS.md) — why changing these settings is an owner decision.

External references consulted for this page (2026-11-05):

- GitHub — available rules for rulesets: <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>
- GitHub — approving a pull request with required reviews: <https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/approving-a-pull-request-with-required-reviews>
- GitHub — create or update an environment: <https://docs.github.com/en/rest/deployments/environments#create-or-update-an-environment>
