---
id: DEV-AGENT-001
title: "AutoDOC agent instructions"
type: REF
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-09-26
next_review: 2027-03-25
source_of_truth: human
supersedes: null
related: []
criticality: medium
review_days: 180
last_verified: 2026-09-26
last_reviewed: 2026-09-26
last_updated: 2026-11-04
auto_generated: false
---
# AutoDOC agent instructions

## Project overview
AutoDOC is a self-updating, self-documenting documentation engine, not a compliance certificate.

## Working sequence
0. Read [`docs/00-governance/MACP.md`](docs/00-governance/MACP.md) and follow it: it is the
   agent workflow, and it points at [`state/DASHBOARD.md`](state/DASHBOARD.md) first. Register a
   session under `state/sessions/` before starting work, and log as you go.
   **MACP is currently SUSPENDED (owner decision, 2026-10-25)** — the notice at the top of
   `docs/00-governance/MACP.md` governs. While suspended: do not run the startup/shutdown
   sequences, do not register a session, and do not write to `state/`. Skip to step 1 and work
   directly.
1. Read `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, and `CONTEXT-SNAPSHOT.md`.
2. Consult `docs/.doc-sync-map.yaml` for the source-to-target contract; inspect source and tests.
3. Make the smallest source change, add tests, regenerate, and review human-owned impact.
4. Run `make check` and `make test`; report remaining unverified behavior.

## Hard constraints
Never rename AutoDOC, edit generated docs by hand, fabricate evidence, or overwrite human
priorities. Controlled files need metadata and ownership. See `ANTI-PATTERNS-FOR-AGENT.md`.
`state/**` is coordination data, not a controlled document set: no generator may write there, and
no agent may record an owner decision there or in the machine files on the owner's behalf.

## Forbidden actions
Do not take these actions unless the owner approved that specific action in the current
conversation. Approval covers one named action, not a session or a category.

- Creating or pushing tags, publishing packages or releases, or bumping a version for publication.
- Rewriting, force-pushing or deleting branches, tags, or history (`git push --force`,
  `git tag -d`, rebasing shared commits).
- Deleting files or state, or running `git clean -fdx`, outside a scratch directory you created.
- Changing branch protection, rulesets, repository settings, or the required check.
- Reading, printing, committing, or transmitting secrets, credentials, tokens, or `.env` files.
- Sending outbound messages, or opening, approving or merging a pull request on the owner's behalf.
- Adding a runtime dependency; that needs an owner decision and an ADR (see `CONTRIBUTING.md`).

## Human confirmation
Ask before any action that is irreversible or leaves this machine: publishing, tagging, deleting
history, changing protection, or sending anything outward. State what will change, where, and
whether an undo exists. If the owner has not answered, stop. A recorded owner decision in the
repository is evidence; an inference from silence is not.
