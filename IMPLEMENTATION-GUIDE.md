# Implementation guide

## Select, instantiate, connect

1. Filter the catalogs by project phase and risk; record exclusions rather than materializing every starter.
   Declare an initial phase/profile with `autodoc init --phase build --profile oss-library` (or add
   the values to `autodoc.toml`). Later changes are explicit events: `autodoc promote --to beta`
   previews the newly required and newly failing types, and `--write` applies the declaration only
   when target-phase required documents exist or a decision is recorded. Use `--force` only for a
   deliberate demotion, backdate, or known-incomplete promotion; the preview and write share the
   same delta.
2. Instantiate one type with `autodoc add DOC-A03-001 --root /existing/project` (add `--write` to
   create `docs/autodoc/<category>/<ID>.md` with a project-qualified instance ID and current
   creation dates), or render a blank or canonical variant on demand with
   `autodoc templates --root /existing/project --variant blank` (or
   `make docs-templates TEMPLATE_VARIANT=blank` in this checkout) and copy the matching file from
   `build/TEMPLATES/`. Replace the placeholder owner/reviewer and content, then add full metadata per
   `CONTROL/metadata/FRONT-MATTER-SCHEMA.json`; keep the **new instance ID**, not the catalog ID.
   `add` never records the document as satisfying the catalog type — confirm the content first, then
   add it to `[instantiated]`.
   The built-in dependency-free parser accepts one scalar per line and JSON-compatible inline
   arrays for `related`; nested YAML and multiline scalar values need a custom parser.
3. Declare the authoritative source, generator and committed target in `docs/.doc-sync-map.yaml`.
   This file uses JSON syntax, which is valid YAML, so Python's standard library can parse it.
   Glob patterns are rooted in this repository. Source globs must match or generation fails.
4. For human-owned docs, add `review` mappings. A block-level rule fails PRs when mapped
   source paths change without a target change. A warn-level rule only logs a reminder.
5. Add project-specific generators to `GENERATORS` in `scripts/doc-sync/engine.py`, test both
   success and failure paths, and regenerate. Unsupported schemas must fail rather than emit
   apparently correct but incomplete documents.
6. On PRs, run generation in check mode and impact against the base SHA. Protected branch
   settings and real CODEOWNERS are required to actually prevent merging without approval.

## Example map rule

```json
{"id": "config", "sources": ["EXAMPLE-PROJECT/config.schema.json"],
 "target": "EXAMPLE-PROJECT/docs/CONFIG-REFERENCE.md", "generator": "config"}
```

Changing `config.schema.json` changes both the server default and the generated reference.
A generated target is committed in the same PR. `CURRENT-STATE.md`, `NEXT-ACTION.md`, and
`RECENT-CHANGES.md` require human review for mapped code changes; the state helper updates
only the observable file list, never invents priorities. Read the
[policy](CONTROL/policies/DOCUMENTATION-POLICY.md) for limitations.

## Self-adoption example

AutoDOC itself maps all three catalog indices and GitHub workflow files into generated
references in `docs/generated/`. Its source-to-human mappings require architecture and
adoption records to co-change with relevant implementation or catalog edits. The
`CONTROL/metadata/OWNERSHIP-MATRIX.yaml` file lists the actual primary document owner;
`check_ownership.py` checks path authority without pretending to supply an approver.
