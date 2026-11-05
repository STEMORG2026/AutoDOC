---
id: DOC-REF-005
title: "Migration guide"
type: SPEC
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-11-05
next_review: 2027-05-04
source_of_truth: human
supersedes: null
related: ["DOC-P3-GOV-010", "DOC-REF-001", "DOC-GOV-001", "DOC-TEST-002", "DOC-ARC-001"]
criticality: medium
review_days: 180
last_verified: 2026-11-05
last_reviewed: 2026-11-05
last_updated: 2026-11-05
auto_generated: false
---
# Migration guide

## Purpose and scope

This page says how to move to the current AutoDOC release from an older one. It answers the
catalog type `DOC-A23-003` (Migration guide), which is why `autodoc.toml` records that type as
satisfied by this page.

Two audiences:

- **Someone installing the tool.** Which package name to install, and what to do if you installed
  an older one under a different name.
- **Someone with an existing project.** What changed in the command line and in the generated
  output, and what did not change at all.

This is not a changelog. [CHANGELOG.md](../../CHANGELOG.md) records what each release contained;
this page records what a user has to *do* about it. It does not cover a service rollout, because
there is no service. It makes no promise about future compatibility: the project is pre-1.0, and
no support window is published yet.

## Details and decisions

### The version timeline

| Version | Distribution | On PyPI | Import package / CLI | What changed |
| --- | --- | --- | --- | --- |
| 0.3.0 | `autodoc` | **No** — never published | `autodoc` / `autodoc` | Installation was a locally built wheel |
| 0.3.1 | `autodoc-docs` | Yes, 2026-10-26 | `autodoc` / `autodoc` | The distribution was renamed; `autodoc adopt` became a read-only filename scan |
| 0.4.0 | `autodoc-docs` | Yes, 2026-11-04 | `autodoc` / `autodoc` | `autodoc adopt` became a phase-scaled adoption planner |

Both published releases are installable and neither is yanked (checked 2026-11-05).

### Migration 1 — the install name (0.3.0 → 0.3.1)

At 0.3.0 the distribution was named `autodoc`, and the documentation told you to install a wheel
you had built yourself:

```sh
python -m pip install /path/to/autodoc-0.3.0-py3-none-any.whl
```

That name is not available on PyPI: `autodoc` there is an unrelated project — "Autodoc Python
implementation", by Shinya Ohyanagi (`heavenshell/py-autodoc`). Installing it gives you a
different program. The distribution was renamed to `autodoc-docs` for that reason.

To move:

```sh
python -m pip uninstall autodoc        # if you installed the local 0.3.0 wheel
python -m pip install autodoc-docs==0.4.0
```

**Never `pip install autodoc`.** It installs someone else's package.

What did *not* change, so no code needs editing:

- The **import package** is still `autodoc`: `import autodoc` works exactly as before.
- The **CLI command** is still `autodoc`: `autodoc --version` still prints `autodoc <version>`.
- `autodoc/__init__.py` resolves the version from the `autodoc-docs` distribution first and
  falls back to `autodoc`, so a source checkout without installed metadata still reports a
  version.

Because `autodoc` 0.3.0 was never published, this migration affects only people who installed a
locally built wheel, or who tried `pip install autodoc` and got the other project.

### Migration 2 — `autodoc adopt` (0.3.1 → 0.4.0)

This is the only command whose behaviour changed between the two published releases.

**At 0.3.1**, `autodoc adopt` was a filename heuristic. It walked the project directory, looked
for names like `openapi.yaml`, `routes.json`, `schema.sql`, `pyproject.toml` or `Dockerfile`,
and printed the catalog domains those names suggest:

```
Suggested catalog domains (heuristics only; review applicability manually):
- A10-BUILD (Build and supply chain): pyproject.toml
Always consider A06-SECURITY, A07-PRIVACY and A11-TESTING; absence of a filename is not proof of non-applicability.
```

It read no configuration, resolved no requirements, and exited `0` — the only other outcome was
an argparse usage error, which exits `2`.

**At 0.4.0**, `autodoc adopt` resolves the declared context, the profile, the catalog and the
enforcement layer — the same layers `autodoc check` uses — and prints an adoption plan. The
heuristic domain list is still there, as one section of that plan; the plan adds the context in
use, the profile, the required set at each phase, the documents that exist but are not
registered, and the declarations that are still undetermined.

New options, all optional:

| Option | Effect |
| --- | --- |
| `--phase` | Preview the plan at a phase without declaring it |
| `--profile` | Preview the plan at a profile without declaring it |
| `--config` | Use a context TOML other than `<project>/autodoc.toml` |
| `--baseline` | Use a baseline JSON other than `<project>/autodoc-baseline.json` |
| `--write-baseline` | Record the current findings as the adoption baseline, then exit |
| `--json` | Print the plan as JSON instead of text |

`--project-path` is unchanged: same default (the current directory), same meaning.

What this breaks:

- **A script that parsed the 0.3.1 output.** The text is still the first thing in the plan, but
  more follows it. If you parse adopt's output, move to `--json`, which did not exist at 0.3.1.
- **A script that assumed exit `0`.** At 0.4.0 the exit code is `2` when the declared context
  has a configuration error and `3` when AutoDOC itself fails. It is never `1`: the plan is a
  preview, so findings are reported and do not fail the command.

What this does *not* break:

- **`autodoc.toml` needs no edit.** `CONTROL/metadata/CONTEXT-SCHEMA.json` is byte-identical
  between the two tags — the same `urn:autodoc:context:1` schema, the same required keys, the
  same rules.
- **The check report is unchanged.** `scripts/intelligence/recommend.py`, `context.py`,
  `profile.py` and `enforce.py` are byte-identical between the two tags, so `autodoc check`
  produces the same findings, the same severities and the same exit codes (`0`, `1`, `2`, `3` —
  see [EXIT-CODES.md](EXIT-CODES.md)). Only `autodoc adopt` changed.

### Migration 3 — an adopted project (optional)

Nothing above is required for a project that already adopted AutoDOC. Two optional steps make
the adoption report quieter:

- **Record the documents that already exist.** A type that is answered by a file the repository
  owns can be registered in `[instantiated]` or `[satisfied_by]` in `autodoc.toml`, with a path
  the checker verifies. That moves the type out of the recommended list.
- **Record a baseline.** `autodoc check --write-baseline` records the findings observed during
  adoption, so a pre-existing problem is not a permanent failure. The baseline is a ratchet:
  fixing a finding makes its entry stale, and deleting the entry brings the finding back.

The catalog's own selection of which types this repository answers is in
[ADOPTION.md](../00-governance/ADOPTION.md), and the procedure for writing the decision is in
the [release runbook](../00-governance/RELEASE-RUNBOOK.md)'s sibling governance records.

### Upgrading

```sh
python -m pip install --upgrade autodoc-docs
autodoc --version
```

Pin the version in anything scripted. The project is pre-1.0 and publishes no support window;
the version rule the project follows is in the
[release runbook](../00-governance/RELEASE-RUNBOOK.md): a new user-visible capability moves the
minor version, a fix moves the patch version.

### Deprecation

Nothing has been deprecated and nothing has been removed. There is no published deprecation
policy yet — the catalog's deprecation-policy type is not required at this phase — so the only
honest statement is the observed one: across every published release, the import package, the
CLI command name, the `autodoc.toml` context schema and the `autodoc check` contract have been
stable. The distribution name changed once, before publication under the current name.

### Decisions

- **Rename the distribution, keep the import package.** `import autodoc` is what a user's code
  writes; `pip install autodoc-docs` is what an installer resolves. Only the second was
  unavailable.
- **Publish a migration guide beside the changelog.** A changelog answers "what changed"; a
  migration guide answers "what do I do". Registering the changelog against the migration type
  would have left the actual instructions unwritten.
- **Do not change the context schema for a new capability.** The adoption planner needed more
  output, not more configuration, so `autodoc.toml` stayed as it was and every existing project
  kept working unchanged.
- **Say what did not change.** A migration guide that lists only differences is read as a
  warning; stating which contracts are byte-identical between tags is what tells a reader
  whether they need to act.

## Verification and references

Check what you have installed:

```sh
autodoc --version                 # prints: autodoc <version>
python -m pip show autodoc-docs   # the distribution name to expect
python -c "import autodoc; print(autodoc.__version__)"
```

Compare a release against another:

```sh
git diff v0.3.1..v0.4.0 -- autodoc/ scripts/intelligence/
```

Related records:

- [CHANGELOG.md](../../CHANGELOG.md) — what each release contained.
- [RELEASE-RUNBOOK.md](../00-governance/RELEASE-RUNBOOK.md) — how a release is cut, verified and
  corrected.
- [EXIT-CODES.md](EXIT-CODES.md) — the `0`/`1`/`2`/`3` contract.
- [QUICK-START.md](../../QUICK-START.md) — the current install and first-run instructions.
- [ADOPTION.md](../00-governance/ADOPTION.md) — registering the types a project already answers.
- [LIMITATIONS.md](../00-governance/LIMITATIONS.md) — what a clean run does not prove.
