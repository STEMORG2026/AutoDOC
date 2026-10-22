# BLOCKERS — active blockers and dependencies

**Last reconciled:** 2026-10-22T13:20Z (no active blockers. B-003 remains cleared; PR #16 merged D-003 at `a28616b`; PR #18 merged PRD1's production-readiness commands at `1361ba2`; the installed-wheel dogfood fix is open as PR #19, awaiting owner review. The first PR #19 guard/impact failure was the expected living-state co-change gate, not a code defect.)

| ID | Blocker | Blocks | Owner who can clear it | Raised |
| --- | --- | --- | --- | --- |
| ~~B-003~~ | **CLEARED 2026-10-21** — the owner applied P-007-A: ruleset `main` now carries exactly `deletion`, `non_fast_forward` and `required_status_checks` → `AutoDOC guard / check` (`strict: true`); the `required_signatures` and CodeQL rules are gone. PR #3 (`04f7386`) and PR #4 (`87be33b`) merged with merge commits and the post-merge continuity test passed on a cold clone of `master` (state read, cold numbers, `make ci` exit 0, guard green on both merges) | Nothing — done | `@Er-Sajan-PLG` | 2026-10-21 |
| ~~B-001~~ | **CLEARED 2026-10-01** — the owner confirmed v1.3 ("proceed with recomendation") and the recording landed: `owner_reviewed` notes in `CONTROL/metadata/CATALOG-RULES.json` + `PROFILES.json`, page → `approved`, caveat off `NEXT-ACTION.md` + `ADOPTION.md`, D-011 refreshed | Nothing — done | `@Er-Sajan-PLG` | 2026-10-01 |
| ~~B-002~~ | **CLEARED 2026-10-01** — the owner acknowledged the decision-3 ADR deviation and kept the real ADR (P-002, "proceed with recomendation"); ADR-008 now records it | Nothing — done | `@Er-Sajan-PLG` | 2026-10-01 |

Decision 3 was started under the owner's "continue work" instruction and is now **complete**
(11 of 12 closed; `DOC-A05-001` reserved for decision 4). No upstream dependency blocks decision 4.

When a blocker clears: strike it here, record the clearing date in the session that saw it, and
reconcile `DASHBOARD.md`.
