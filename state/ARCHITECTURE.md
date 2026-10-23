# ARCHITECTURE — coordination-layer view

**Last reconciled:** 2026-10-23 (PR #24 merged the beta promotion at `8f9c709`. BETA/PRD1/PRD2/912C await explicit owner closure; 894B/C4R7/B71a/627F remain paused)

This file is the agent's orientation map, not the authoritative design. When they disagree, the
authoritative documents win: `docs/05-architecture/AUTODOC-ARCHITECTURE.md` (system),
`docs/00-governance/ENGINE-COVERAGE.md` (what is verified, and its limits),
`CONTROL/metadata/CONTEXT-MODEL.json` (phases, enforcement, facts).

## Components

| Piece | Where | Role |
| --- | --- | --- |
| CLI + distribution | `autodoc/`, `setup.py`, `MANIFEST.in` | `autodoc` console command over existing scripts; wheel data under `share/autodoc`; project roots are explicit and separate from bundled tool assets |
| Sync engine | `scripts/doc-sync/*` | Sources → deterministic generators → mapped targets; drift, impact, freshness checks |
| Intelligence | `scripts/intelligence/*` | `profile` (facts) → `context` (declarations) → `recommend` (applicability) → `enforce` (severity at the declared phase) → `triggers` (when CI runs what) |
| Doc control | `scripts/doc-control/*` | Catalog build/check, guards, health, evidence packing, release snapshot, link checks, hooks |
| Machine policy | `CONTROL/metadata/*` | Rules, profiles under review, context model, triggers, schemas — machine-written JSON |
| Catalog + templates | `CATALOG-A/B/C`, catalog renderer, ignored `build/TEMPLATES/` | 265 document types, 24 core, 49 extended; all three variants render on demand from each catalog record |
| Governed docs | `docs/**` + named root files | Human-owned controlled Markdown with frontmatter, review dates, ownership |
| Coordination | `state/**` | This protocol's workspace. **Not** part of the product architecture and excluded from `engine.controlled()` |

## Flows

- **Documentation:** mapped source → generator (labeled `exact` or `heuristic`) → target; `docs-drift` fails the build when a target is stale. The installed `autodoc` CLI resolves its bundled tool root separately from `check --repo` and `generate --root` project paths.
- **Applicability:** three-valued facts → profile → `recommend`; a catalog `reader` adds the implicit AND token `audience:<reader>` (match=true, non-match in a non-empty audience=false/not-applicable, empty=unknown, `assess` exempt) → decision states (`[instantiated]`, `[satisfied_by]`, `[not_applicable]`, open, off, undetermined) at the declared phase's severity.
- **Gating:** `CONTROL/metadata/TRIGGERS.json` declares which events run what; one blocking event, one required status check (`AutoDOC guard / check`), network checks scheduled and warn-only.

## Invariants worth knowing before touching anything

1. Facts are capability-named (`has_cli`), three-valued (true / false / **unknown** — never silently false), and either detector-backed (with stated limits and fixtures) or declaration-only with a reason.
2. Phase, kinds, audiences, obligations and personal-data/payment/safety traits are **declared, never inferred**; evidence is only a hint. Catalog `reader` metadata consumes the declared audience as an implicit AND predicate under ADR-014. Undeclared phase → advisory only.
3. Human edits TOML; machines write JSON; never round-trip TOML. Use `json_style.dumps()` for machine JSON.
4. Exit-code contract: 2 config/usage, 3 internal failure, 1 findings; a crash never exits 1.
5. Docs co-change with behavior; `make generate` first, then tests and `make ci`.

## Audit facts (Section 7 Step 1, 2026-10-01)

- **Runtime:** Python 3.11–3.15 declared (`>=3.11,<3.16`), **zero runtime dependencies** (stdlib only); dev extras `build>=1,<2`, `pytest>=8,<10`, and `pre-commit>=3,<5`; optional `audit = ["pip-audit>=2.10,<3"]` is operator-run and never imported by shipped code; build backend `setuptools>=77`. The installed CLI ships a wheel/sdist with only its runtime scripts and policy/catalog data.
- **Scale:** The pre-migration snapshot on 2026-10-21 had 1039 tracked files (65 `.py`, 384 `.md`) including the 795 template variants. After the D-003 working-tree migration on 2026-10-22, the source tree contains 271 files (73 `.py`, 129 `.md`); 70 controlled Markdown documents (24 generated, 46 human-owned; 28 mapped generated targets in total, four non-Markdown); and 265 catalog types with 795 renderable outputs, none checked in. Counts exclude ignored `build/` outputs.
- **Demo surface:** SQLite (`EXAMPLE-PROJECT/db/schema.sql`, single `tasks` table, no migrations) and a stdlib threaded HTTP server with three routes (`GET/POST /tasks`, `GET /health`), **no auth**, 1–4096-byte body cap, JSON 400/404 errors.
- **Readers:** Python declarations via AST (exact, in-process) and Go references via `go doc -all .`; `master` now includes JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON via `cargo rustdoc`. These external references run on demand, validate tool output, and report missing tools as L0 in that run. Node v22.22.3 is present locally; JSDoc, TypeDoc, Cargo, rustc and rustdoc are absent, so the integrations are validated with fake-tool tests here.
- **Gates:** post-merge `master` at `06ccb0a` passes local `make ci` with 304 tests + 190 subtests, including catalog checks, guards, drift, staged-impact check, wheel/sdist package smoke and evidence hashing; hashes are not signatures. PR #18 merged at `1361ba2` and PR #19 at `06ccb0a` after their required checks and declared Python 3.11–3.15 matrices passed; master guard and generation-preview runs are green. The supplemental matrix remains non-blocking. Nightly freshness is warn-only.
- **Known-issue markers:** none inline (0 TODO/FIXME/XXX/HACK); the known surface is `LIMITATIONS.md` and `ENGINE-COVERAGE.md`.

## Change log

| Date | Change |
| --- | --- |
| 2026-10-23 | BETA's owner-authorized `beta` declaration (2026-10-23) merged in PR #24 at `8f9c709`; duplicate severity pins were removed and phase-dependent docs/tests/state updated. Post-merge `make ci` passes with beta-ready 17/17; no release or closure. |
| 2026-10-23 | PR #23 made the shipped-phase tests derive from `autodoc.toml`, so a promotion no longer fails CI on hard-coded `build` assertions. |
| 2026-10-23 | PRD2's closeout merged in PR #21 at `f8e2c76`: `LICENSE`/`CHANGELOG.md` are beta document homes, the optional `audit` extra plus `make audit` are documented, and readiness treats unverifiable declared paths as open; beta promotion previews clean but no phase write, release or closure is included. |
| 2026-10-22 | PR #18 merged `autodoc add`, guarded `autodoc promote` and `init --phase/--profile` at `1361ba2`. Installed-wheel dogfood then found target-root path resolution, duplicate instance-ID and promote-wording defects; PR #19 merged the fixes at `06ccb0a`, and post-merge `make ci` plus master CI passed. No release or session closure was authorized. |
| 2026-10-22 | Owner selected D-004 followed by D-002 after PR #13 merged at `a704752`; the audience rule and JSDoc/TypeDoc/nightly Rustdoc JSON readers merged to `master` in PR #14 at `7a0fd47`; post-merge local CI passed. No PyPI publication or session closure was authorized. |
| 2026-10-22 | C4R7 added the installable `autodoc` CLI, isolated wheel/sdist packaging and smoke tests, separate tool/project roots, version metadata and temporary tag-run distribution artifacts; PR #12 merged at `08229a0`. PyPI publishing remains unauthorized/unconfigured; C4R7 and B71a remain paused until explicit owner closure. |
| 2026-10-01 | Decision 3 closed the open core decisions: new `docs/00-governance/PROJECT-CHARTER.md`, `docs/adr/` (first ADR), `SECURITY.md`, `CODE_OF_CONDUCT.md`; module contracts, test strategy, dependency setup and dependency policy now have named homes (`autodoc.toml` declarations); readiness 15/16 at commit `1a65f5d`. |
| 2026-10-01 | Full MACP transcription landed (Sections 2–7 + REMEMBER verbatim) and the Section 7 Step 1 audit completed; `state/` files reconciled at `d26d798`. |
| 2026-10-01 | `state/` added as the MACP coordination layer (`docs/00-governance/MACP.md`). It is deliberately outside the controlled-document set; `guards.py` still scans its Markdown for links, tribal phrases and key markers. |
