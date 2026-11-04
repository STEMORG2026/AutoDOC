---
id: DOC-P3-GOV-009
title: "Supply chain record"
type: SPEC
owner: "@Er-Sajan-PLG"
reviewer: "@Er-Sajan-PLG"
classification: public
status: draft
version: "0.1"
effective_date: 2026-11-04
next_review: 2027-05-03
source_of_truth: human
supersedes: null
related: ["DOC-P3-GOV-003", "DOC-P3-GOV-004", "DOC-P3-GOV-005", "DOC-P3-GOV-001", "DOC-REF-003", "DOC-P2-001", "DOC-GOV-001"]
criticality: medium
review_days: 180
last_verified: 2026-11-04
last_reviewed: 2026-11-04
last_updated: 2026-11-04
auto_generated: false
---
# Supply chain record

## Purpose and scope

This page records what AutoDOC produces and claims about its software supply chain: a CycloneDX
SBOM, an unsigned source record, a license inventory of declared dependencies, and the
vulnerability-handling path. It answers the catalog types `DOC-A10-002` (SBOM), `DOC-A10-003`
(build provenance) and `DOC-A10-006` (license inventory), which is why `autodoc.toml` records
them as satisfied by this page.

The subject is the `autodoc-docs` distribution and the repository that builds it. It does not
cover the synthetic dependencies of `EXAMPLE-PROJECT`
([EXAMPLE-DEPENDENCIES.md](../reference/EXAMPLE-DEPENDENCIES.md)), an adopter's own supply
chain, or the security of third-party tools themselves.

It is a record, not a certificate. No SLSA level, signed provenance, reproducible-build claim,
or compliance attestation is made. [EVIDENCE-SIGNING.md](EVIDENCE-SIGNING.md) records why the
evidence is unsigned, and [LIMITATIONS.md](LIMITATIONS.md) lists the blind spots.

## Details and decisions

### SBOM

`make evidence` writes `evidence/out/sbom.json`. An observed run (2026-11-04):

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.5",
  "version": 1,
  "metadata": {
    "timestamp": "2026-11-04T09:07:09.842408+00:00",
    "component": {"type": "application", "name": "autodoc-docs", "version": "0.4.0"}
  },
  "components": [],
  "properties": [
    {"name": "autodoc:scope",
     "value": "Declared project only; no installed or optional dependency resolution"}
  ]
}
```

The empty `components` list is a claim about the shipped package, not an oversight:
`pyproject.toml` declares `dependencies = []`, and the packer fails closed. If any runtime
dependency appears, `scripts/doc-control/evidence_pack.py` raises `Runtime dependencies exist;
install/resolution-based SBOM integration required` and refuses to produce a pack. A new runtime
dependency therefore cannot silently ship with an empty SBOM.

Scope and limits, stated rather than implied:

- **Declared project only.** There is no installed-environment resolution, so transitive and
  vendored packages are not components.
- **Extras are declared but not shipped.** `build`, `pytest`, `pre-commit`, `coverage` and
  `pip-audit` are declared in `pyproject.toml` and are not components, because the wheel does
  not contain them.
- **No purl, CPE, VEX or dependency graph,** and the timestamp is when the pack was written,
  not when anything was built.
- **Per run, never committed.** The file lives in ignored `evidence/out/`, is uploaded as the
  `autodoc-evidence-pack` CI artifact with `if: always()`, and its SHA-256 is recorded in
  `evidence-pack.json`. `make check-evidence` re-verifies that hash. The pack is unsigned.

Reproduce:

```sh
make evidence
cat evidence/out/sbom.json
make check-evidence
```

### Build provenance

Two records exist, and neither is an attestation:

| Record | Produced by | Contains | Does not contain |
| --- | --- | --- | --- |
| `evidence/out/source-record.json` | `make evidence` | Commit SHA, branch, dirty flag, builder (`GITHUB_RUN_ID` or `local`), SHA-256 of named sources | A build, a builder identity, or a signature |
| `RELEASE-MANIFEST.json` | `scripts/doc-control/release_snapshot.py` | Tag, commit, scope, SHA-256 of every controlled document | Artifact hashes, a signature, or a statement about the wheel |

The source record says so itself: `"signed": false` and `"warning": "No build was attested or
signed; this is not SLSA provenance."` The release snapshot's recorded scope is `unsigned local
documentation snapshot; store externally for retention`.

What the release workflow actually guarantees:

- The snapshot job runs only for a `v*.*.*` tag and refuses a tag that is not `vX.Y.Z`, that
  disagrees with `project.version`, that has no matching `## <version>` section in
  [CHANGELOG.md](../../CHANGELOG.md), or whose checkout is not the tagged commit. It also
  requires `LICENSE`, drift-free generated documentation, and no overdue critical review.
- It builds the wheel and source distribution once and uploads them as a run artifact.
- The publish job runs only for tag refs, downloads the artifact from that same run, re-runs
  `scripts/test_package.py --dist-dir` against those exact files, and only then publishes
  through OIDC trusted publishing.
- PyPI records PEP 740 attestations for a trusted-publishing upload. They describe the upload;
  they are not SLSA provenance and not signed documentation evidence.

Not claimed: a SLSA level, hermetic or reproducible builds, hash-pinned build dependencies, or
signatures. The build backend is `setuptools>=77`, installed in PEP 517 isolation from PyPI at
build time, so the build environment is not pinned by hash and the build is not hermetic. A
local `make package` is an ordinary unattested build.

### License inventory

The project is Apache-2.0: `LICENSE` holds the text, `pyproject.toml` declares
`license = "Apache-2.0"` and `license-files = ["LICENSE"]`, and `tests/test_agent_example.py`
pins both declarations plus the license text. The release snapshot's `require_license` refuses a
checkout without `LICENSE`, and `tests/test_agent_example.py` pins that refusal too.

Inspecting a wheel built with `make package` on 2026-11-04 showed only the `autodoc` package
(plus data and `.dist-info`), `License-Expression: Apache-2.0`, `dist-info/licenses/LICENSE`, and
no unconditional `Requires-Dist`. Nothing that requires attribution is shipped.

Declared dependencies and their licenses, observed on 2026-11-04:

| Dependency | Group | Declared range | License | Observed version |
| --- | --- | --- | --- | --- |
| `build` | dev | `>=1,<2` | MIT | 1.6.1 |
| `pytest` | dev | `>=8,<10` | MIT | 9.1.1 |
| `pre-commit` | dev | `>=3,<5` | MIT | 4.7.0 |
| `coverage` | dev | `>=7,<8` | Apache-2.0 | 7.17.0 |
| `pip-audit` | audit | `>=2.10,<3` | Apache-2.0 | 2.10.1 |
| `setuptools` | build backend | `>=77` | MIT | 84.2.1 |

The declared ranges in `pyproject.toml` are the source of truth; the versions are the
environment this table was verified in, not pins. Licenses were read from each installed
distribution's metadata and license file, including the license file for `pip-audit`, whose
package metadata carries no license expression.

Limits:

- Transitive dependencies of those tools are not inventoried. There is no automated license
  gate.
- A new dependency's license is checked in review against
  [CONTRIBUTING.md](../../CONTRIBUTING.md), which requires compatibility with Apache-2.0 and a
  visible notice when attribution is required.
- `pip-audit` answers vulnerability questions, not license questions.

### Vulnerability handling

[SECURITY.md](../../SECURITY.md) is authoritative for reporting and response. The relevant
supply-chain facts:

- The required offline gate (`make ci`) never queries an advisory service.
- `make audit` runs `pip-audit` against the installed development environment after installing
  the optional `audit` extra. It opens the network and its result is a point-in-time record.
- The `Dependency audit` CI job runs the same scan on pull requests and pushes. It is advisory,
  not the required check: a live advisory or a service outage must not block an unrelated
  change.
- `make secret-scan` runs gitleaks over full history; CI pins and checksum-verifies the scanner.
- There is no automated dependency updater and no bot pull request. A range is bumped manually,
  `make ci` is run, and the reason goes in the commit message.

### Decisions

- **Keep the SBOM declared-only until a runtime dependency exists.** The fail-closed guard is
  the integrity mechanism; adding resolution now would claim more than the package ships.
- **Do not claim a SLSA level or sign the records.** Signing needs key custody, rotation and a
  revocation procedure that do not exist; [EVIDENCE-SIGNING.md](EVIDENCE-SIGNING.md) holds that
  decision.
- **Inventory declared dependencies, not the resolved environment.** A resolved list would be a
  snapshot of one machine and would drift without a code change.

## Verification and references

```sh
make evidence                                    # sbom.json, source-record.json, the pack
make check-evidence                              # re-verifies the recorded SHA-256 values
make package                                     # builds wheel and sdist into dist/
make audit                                       # pip-audit; audit extra and network
make secret-scan                                 # gitleaks; needs the binary on PATH
python scripts/test_package.py --dist-dir dist   # artifact naming and clean install
```

- [SECURITY.md](../../SECURITY.md) — reporting, response and vulnerability scope.
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — dependency policy and license compatibility.
- [EVIDENCE-SIGNING.md](EVIDENCE-SIGNING.md) — why nothing is signed.
- [LICENSE-DECISION.md](LICENSE-DECISION.md) — the Apache-2.0 decision record.
- [QUALITY-GATES.md](../reference/QUALITY-GATES.md) — which checks block, which advise.
- [LIMITATIONS.md](LIMITATIONS.md) — what a clean record does not prove.
- [EXAMPLE-DEPENDENCIES.md](../reference/EXAMPLE-DEPENDENCIES.md) — the synthetic example's
  dependencies, which are not part of this package.
- `scripts/doc-control/evidence_pack.py`, `scripts/doc-control/release_snapshot.py` and
  `.github/workflows/release.yml` — the implementations this page describes.
