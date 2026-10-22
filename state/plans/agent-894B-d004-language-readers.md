# Plan — 894B — D-004 audience applicability + D-002 language readers

| Field | Value |
| --- | --- |
| Objective | Implement the owner-selected D-004 reader-derived audience gate, then D-002 JavaScript/TypeScript and Rust toolchain readers, with tests and truthful limits. |
| Owner of the work | `894B` (session `20261022-0445-894B`) |
| Branch | `arena/894b93ee-autodoc`, based at PR #13 merge `a704752` |
| Status | **IN PROGRESS — CI, staged-impact and pre-commit checks passed; commit/push/PR handoff pending** |
| Opened (UTC) | 2026-10-22T04:45Z |

## Owner decision and semantics

After PR #13 merged, the owner selected D-004 followed by D-002. The owner confirmed the proposed
D-004 rule: catalog `reader` is an implicit AND applicability token; a matching declared audience
is true; a mismatch in a non-empty declared audience set is false/not applicable; an empty audience
is unknown; and `assess` remains exempt. Record this as ADR-014. D-002 integrates JSDoc `-X`,
TypeDoc `--json`, and nightly Rustdoc JSON through `cargo rustdoc`.

## Scope

**In:** wire the reader token through three-valued applicability and reports; update the context and
catalog descriptions; add the JSDoc, TypeDoc and nightly Rustdoc JSON integrations behind explicit
tool probes; keep language references on-demand; protect the inspected checkout from Cargo output
by running Rustdoc from a temporary project copy; add fake-tool tests; update documentation, generated
inventories and living state; validate the existing beta-phase tests with explicitly declared
audiences under the confirmed closed-audience semantics.

**Out:** any other deferred P-006 item; publishing to PyPI; closing C4R7, B71a or 627F without the
owner's explicit word; changing D-004 semantics; installing local generators/toolchains; merging the
follow-up PR without owner authorization.

## Approach

1. Keep all work on `arena/894b93ee-autodoc`; confirm PR #13 remains the merged base and do not
   re-merge it.
2. Implement D-004 from catalog `reader` metadata, preserving three-valued applicability and the
   `assess` exemption; surface audiences and derivation in reports and explanations.
3. Add D-002's canonical tools with probes, output validation, offline/timeout handling and fake
   executables. Rust generation uses a temporary copy and is environment-isolated, not an OS sandbox.
4. Update policy/schema and coverage/limitations/architecture docs; refresh generated references.
5. Run focused tests, `make ci`, package checks as covered by CI, `git diff --check`, and staged
   impact/ownership checks. Reconcile `state/` and the owner decision.
6. Commit and push only this branch, open a follow-up PR, record its checks, and pause for owner
   review. Do not merge it without explicit authorization.

## Risks and mitigations

- **Risk:** guessing what an empty or mismatched audience means. **Mitigation:** implement only the
  owner's confirmed semantics and test match, mismatch, empty, and `assess` cases.
- **Risk:** presenting unavailable tools as integrated output. **Mitigation:** report missing tools
  as L0 for that run, validate JSON artifacts, and test commands with fake executables; do not
  install toolchains in this environment.
- **Risk:** Cargo writes into the inspected repository or appears sandboxed. **Mitigation:** copy the
  Rust project to a temporary directory, redirect build output, use offline mode, and state clearly
  that this is environment isolation rather than an OS security sandbox.
- **Risk:** treating PR #13 merge or this implementation as permission to close other sessions,
  publish or merge. **Mitigation:** preserve those boundaries and wait for explicit owner direction.

## Rollback strategy

Revert only the D-004/D-002 follow-up commits on `arena/894b93ee-autodoc`; PR #13 and its merged
base at `a704752` remain untouched.

## Success criteria

- Reader match is true, a declared non-match is not applicable, empty audience is undetermined, and
  `assess` is exempt; all are visible in reports/explanations and regression-tested.
- JSDoc `-X`, TypeDoc `--json`, and nightly Rustdoc JSON are exercised with fake tools; missing tools
  are reported honestly; no generated external-tool reference is committed.
- Repository docs and generated inventories agree with the implementations and limitations.
- `make ci`, `git diff --check` and staged review checks pass; PR is open for review, not merged.
- No PyPI publish or session closure occurs by inference.
