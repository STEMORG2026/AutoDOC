# BLOCKERS — active blockers and dependencies

**Last reconciled:** 2026-10-21T11:57Z (B-003 raised — merges blocked at GitHub; P-007 is the clearing decision)

| ID | Blocker | Blocks | Owner who can clear it | Raised |
| --- | --- | --- | --- | --- |
| **B-003** | **Branch ruleset `main` (id `25542481`, active since 2026-10-21 11:27Z) blocks every merge to `master`.** Its `required_signatures` rule rejects PR #3's unsigned commits (`eec4050`, `41dead9`), its two CodeQL rules (`code_quality`, `code_scanning`) wait for a CodeQL workflow this tree does not have, and ADR-011's required check `AutoDOC guard / check` is not in the ruleset. PR #3 is approved and green and still gets "the base branch policy prohibits the merge". Clearing action: the owner edits the ruleset per **P-007** (`state/DECISIONS.md`) — GitHub → Settings → Rules → Rulesets → `main`; this session's token writes no repository settings (403) and the ruleset has no bypass actor | PR #3, the protection-review PR from `arena/d2fb52ab-autodoc`, and every future merge to `master` | `@Er-Sajan-PLG` | 2026-10-21 |
| ~~B-001~~ | **CLEARED 2026-10-01** — the owner confirmed v1.3 ("proceed with recomendation") and the recording landed: `owner_reviewed` notes in `CONTROL/metadata/CATALOG-RULES.json` + `PROFILES.json`, page → `approved`, caveat off `NEXT-ACTION.md` + `ADOPTION.md`, D-011 refreshed | Nothing — done | `@Er-Sajan-PLG` | 2026-10-01 |
| ~~B-002~~ | **CLEARED 2026-10-01** — the owner acknowledged the decision-3 ADR deviation and kept the real ADR (P-002, "proceed with recomendation"); ADR-008 now records it | Nothing — done | `@Er-Sajan-PLG` | 2026-10-01 |

Decision 3 was started under the owner's "continue work" instruction and is now **complete**
(11 of 12 closed; `DOC-A05-001` reserved for decision 4). No upstream dependency blocks decision 4.

When a blocker clears: strike it here, record the clearing date in the session that saw it, and
reconcile `DASHBOARD.md`.
