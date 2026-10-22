# Generated document shells

Do not hand-edit generated facts. Set an authoritative source and generator in
`docs/.doc-sync-map.yaml`, add a regression test, then run `generate-all.py`.
The example's API, configuration, environment and SQLite schema outputs demonstrate this pattern.
Catalog entries declare logical destinations for human-owned templates; render canonical, blank
or synthetic-example variants only when needed with `make docs-templates` or `autodoc templates`.
Rendered files go under ignored `build/TEMPLATES/`; generated targets have their own frontmatter.
