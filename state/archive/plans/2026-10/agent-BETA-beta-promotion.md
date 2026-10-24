# Plan — beta phase promotion (`BETA`)

| Field | Value |
| --- | --- |
| Objective | Write the owner-authorized `beta` phase declaration on `master`, keep the enforcement pins honest, update phase-dependent documentation and state, and prove the gate stays green. |
| Owner of the work | `BETA` (session `20261023-0612-BETA`) |
| Status | **CLOSED (owner's word, 2026-10-23) — PR #24 merged at `8f9c709`** |
| Opened (UTC) | 2026-10-23T06:12Z |

## Scope

**In:** change `phase` to `beta` and `phase_declared` to 2026-10-23; remove severity pins that
merely duplicate beta defaults (`stubs`, `freshness.review`); update README, ADOPTION,
CORE-LIST-REVIEW, architecture, tests and state; regenerate `TRIGGER-REFERENCE`; run `make ci` and
`make audit`; open the promotion PR.

**Out:** release tag, PyPI publication, version/classifier changes, and session closure. No
runtime dependency is added.

## Approach

1. Use `autodoc promote --to beta --write` and keep the explanatory comment truthful.
2. Remove duplicate pins and update the pin-policy test to compare against the declared phase.
3. Update the phase-dependent docs and regenerate mapped output.
4. Run the full gate and audit; open the owner-gated PR; reconcile state.

## Risks and mitigations

- **Risk:** beta strictness surfaces new failures. **Mitigation:** run `autodoc check` and
  `make ci` at beta; only warnings remain.
- **Risk:** stale phase prose. **Mitigation:** update README, ADOPTION, CORE-LIST-REVIEW,
  architecture and the generated trigger reference in the same change.
- **Risk:** the promotion is read as release authorization. **Mitigation:** keep tag, PyPI,
  version and session closure out of scope and state that boundary in the PR.

## Rollback strategy

Revert the promotion commit; the phase declaration returns to `build` and no release artifact or
external publication exists.

## Success criteria

- `autodoc check` reports `beta-ready: 17/17` with no failing findings.
- `make ci` passes 307 tests + 188 subtests, package smoke and evidence verification.
- `make audit` reports no known vulnerabilities.
- PR #24 merged at `8f9c709` with all checks passing; post-merge `make ci` passes 307 tests +
  188 subtests. No tag, PyPI publication or session closure.
