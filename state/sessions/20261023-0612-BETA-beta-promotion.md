# Session 20261023-0612-BETA — beta phase promotion

## Owner request

“merged, proceed.” This followed PR #23 (phase-agnostic shipped checks) merging at `3fda35b`,
and the owner's earlier “merged, proceed” after the post-PR21 reconciliation. The owner authorized
opening the beta promotion PR; the merge is the phase-write event.

## Coordination and decisions

- Branch: `chore/promote-beta`, starting at `3fda35b`.
- Scope: write the `beta` declaration and declaration date, remove severity pins that duplicate
  the beta defaults, update phase-dependent docs/tests, regenerate mapped output, verify, and
  reconcile state.
- Out of scope: creating a tag, publishing to PyPI, changing the `0.3.0`/Beta version metadata,
  and closing any session. Those remain separate owner decisions.
- This is a new bounded session, not a reopening of PRD2.

## Claimed paths

- `autodoc.toml`, `README.md`, `tests/test_enforce.py`
- `docs/00-governance/{ADOPTION,CORE-LIST-REVIEW}.md`
- `docs/05-architecture/AUTODOC-ARCHITECTURE.md`
- `docs/generated/TRIGGER-REFERENCE.md`
- `CURRENT-STATE.md`, `NEXT-ACTION.md`, `RECENT-CHANGES.md`, `state/**`

## Plan

See `state/plans/agent-BETA-beta-promotion.md`.

## Verification and evidence

- Pre-promotion preview: `autodoc promote --to beta` exited 0 with
  `Delta: no catalog requirement changes`.
- Beta declaration: `autodoc check` reports `beta-ready: 17/17`, phase `beta (strict)`.
- `make ci` on the promotion branch: 307 tests + 188 subtests, wheel/sdist and clean-install
  smoke, evidence hashes verified.
- `make audit` (pip-audit 2.10.1): `No known vulnerabilities found`.
- PR #23 made the shipped-phase tests derive from the declaration; this session also updates the
  pin policy test so it compares pins with the declared phase, not `build`.

## Outcome

**PAUSED — PR open; awaiting owner merge and explicit session closure.** The beta promotion is
owner-gated: merging the PR records the phase write. No tag, PyPI publication or session closure
is included.
