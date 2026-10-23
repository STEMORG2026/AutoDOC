# Plan — production-readiness closeout (`PRD2`)

| Field | Value |
| --- | --- |
| Objective | Close the remaining release-readiness gaps on `master` after PR #19: the beta document delta, operator-run vulnerability auditing, two enforcement/readiness residuals, and the records that describe them. |
| Owner of the work | `PRD2` (session `20261022-1415-PRD2`) |
| Status | **ACTIVE — PR #21 open; checks pass; awaiting owner merge** |
| Opened (UTC) | 2026-10-22T14:15Z |

## Scope

**In:** record `LICENSE` and `CHANGELOG.md` as the homes for `DOC-A10-008` and `DOC-A15-003`;
verify the beta promotion preview is blocker-free; add an optional `audit` extra and `make audit`;
make the readiness score ignore acknowledged decisions whose declared paths are missing; default
`enforce.collect_findings()` to the tool checkout when no root is supplied; update user docs,
changelog, generated inventories/outline and coordination state; run `make ci`, the installed
wheel smoke and external dogfood.

**Out:** writing the `beta` declaration without the owner's explicit promotion, creating a tag,
publishing to PyPI, and closing PRD1/PRD2 or any other session. No runtime dependency is added.
No scanner is added to the required offline CI gate; the audit is operator-run and network-using.

## Approach

1. Add the two beta records to `[satisfied_by]` and prove the delta with `autodoc promote --to beta`
   (preview only).
2. Add the bounded `pip-audit` extra, a `make audit` target and honest documentation of its limits.
3. Normalize the enforcement root once, then reuse it; exclude unverifiable decisions from
   readiness and add focused regression tests.
4. Update the changelog, coverage/limitations and security docs; regenerate mapped output.
5. Run `make ci`, rebuild/install the wheel, rerun external dogfood, then reconcile state and open
   a PR. Leave beta promotion and release to the owner.

## Risks and mitigations

- **Risk:** a `[satisfied_by]` mapping hides a missing record. **Mitigation:** the checker verifies
  every local path; `promote` remains the second, independent check.
- **Risk:** adding an audit dependency changes the runtime posture. **Mitigation:** keep it in a
  separate optional extra, never import it from shipped code, and keep `dependencies = []`.
- **Risk:** readiness still overstates completion in another shape. **Mitigation:** test the
  invalid-path case directly and report the invalid count in the score data.
- **Risk:** “production ready” is read as release authorization. **Mitigation:** keep phase, tag,
  PyPI and session closure out of scope and state that boundary in the PR.

## Rollback strategy

Revert the closeout commit; the only configuration change is additive (`[satisfied_by]` entries and
an optional extra), and no phase or release state is written.

## Success criteria

- `autodoc promote --to beta` previews no requirement blockers while `phase` stays `build`.
- `make audit` succeeds with the audit extra installed and reports no known vulnerabilities.
- `make ci` passes with the new tests; installed-wheel smoke and external dogfood remain green.
- PR #21 is open with all checks passing and states that beta promotion, tag, PyPI publication
  and session closure are still owner decisions.
