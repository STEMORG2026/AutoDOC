# ARCHITECTURE — coordination-layer view

**Last reconciled:** 2026-10-22 (PR #13 merged at `a704752`; PR #14 open with D-004 and D-002 implemented and all checks passing; C4R7, B71a and 627F remain paused)

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
| Catalog + templates | `CATALOG-A/B/C`, `TEMPLATES/**` | 265 document types, 24 core, 49 extended; templates per type |
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

- **Runtime:** Python 3.11–3.15 declared (`>=3.11,<3.16`), **zero runtime dependencies** (stdlib only); dev extras `build>=1,<2`, `pytest>=8,<10`, and `pre-commit>=3,<5`; build backend `setuptools>=77`. The installed CLI ships a wheel/sdist with only its runtime scripts and policy/catalog data.
- **Scale:** 1015 tracked files = 64 `.py`, 361 `.md`, and 265 catalog types × 3 template variants; 68 controlled docs (24 generated, 44 human-owned). **Refreshed 2026-10-21:** 1039 tracked files = 65 `.py`, 384 `.md`; 70 controlled instances (28 generated targets, 42 human-owned) — the counts a reader should cite today.
- **Demo surface:** SQLite (`EXAMPLE-PROJECT/db/schema.sql`, single `tasks` table, no migrations) and a stdlib threaded HTTP server with three routes (`GET/POST /tasks`, `GET /health`), **no auth**, 1–4096-byte body cap, JSON 400/404 errors.
- **Readers:** Python declarations via AST (exact, in-process) and Go references via `go doc -all .`; the active follow-up branch adds JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON via `cargo rustdoc`. These external references run on demand, validate tool output, and report missing tools as L0 in that run. Node v22.22.3 is present locally; JSDoc, TypeDoc, Cargo, rustc and rustdoc are absent, so the new integrations use fake-tool tests here.
- **Gates:** the current follow-up branch passes local `make ci` on Python 3.11 (280 tests + 190 subtests), including catalog checks, guards, drift, impact, package smoke and evidence hashing. PR #13 merged at `a704752`; PR #14's required `AutoDOC guard / check`, impact job and supplemental Python 3.11–3.15 matrix all pass. PR #14 awaits owner review; the supplemental matrix remains non-blocking. Nightly freshness is warn-only.
- **Known-issue markers:** none inline (0 TODO/FIXME/XXX/HACK); the known surface is `LIMITATIONS.md` and `ENGINE-COVERAGE.md`.

## Change log

| Date | Change |
| --- | --- |
| 2026-10-22 | Owner selected D-004 followed by D-002 after PR #13 merged at `a704752`; D-004's closed-audience semantics and JSDoc/TypeDoc/nightly Rustdoc JSON readers are implemented on `arena/894b93ee-autodoc` in PR #14; all checks pass, awaiting owner review. No PyPI publication or session closure was authorized. |
| 2026-10-22 | C4R7 added the installable `autodoc` CLI, isolated wheel/sdist packaging and smoke tests, separate tool/project roots, version metadata and temporary tag-run distribution artifacts; PR #12 merged at `08229a0`. PyPI publishing remains unauthorized/unconfigured; C4R7 and B71a remain paused until explicit owner closure. |
| 2026-10-01 | Decision 3 closed the open core decisions: new `docs/00-governance/PROJECT-CHARTER.md`, `docs/adr/` (first ADR), `SECURITY.md`, `CODE_OF_CONDUCT.md`; module contracts, test strategy, dependency setup and dependency policy now have named homes (`autodoc.toml` declarations); readiness 15/16 at commit `1a65f5d`. |
| 2026-10-01 | Full MACP transcription landed (Sections 2–7 + REMEMBER verbatim) and the Section 7 Step 1 audit completed; `state/` files reconciled at `d26d798`. |
| 2026-10-01 | `state/` added as the MACP coordination layer (`docs/00-governance/MACP.md`). It is deliberately outside the controlled-document set; `guards.py` still scans its Markdown for links, tribal phrases and key markers. |
