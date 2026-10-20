# Licensing Baseline for Orbiplex Swarm Components

Based on: `doc/project/10-challenges/001-licensing.md`

## Status

Proposed

The artifact split below is the revised design direction. This document is not
a license grant, contributor-rights clearance, or authorization to change source
licenses. The 2026-10-20 revision changes documentation only.

## Date

2026-02-22

Revised: 2026-10-20

## Executive Summary

Protect the shared Node implementation with `AGPL-3.0-only`, while making an
explicitly bounded integration surface available under `Apache-2.0`. Keep prose
under `CC-BY-4.0` and preserve the licenses of third-party artifacts.

The distinction is between improving the reference implementation and building
independent software that interoperates with it. It is not a distinction between
commercial and noncommercial users, nor between large and small crates.

No package becomes Apache-licensed merely by appearing in the candidate list.
Every extraction needs a closed dependency and bundled-asset inventory, rights
review, explicit approval, and a separately reviewed licensing change.

## Context and Problem Statement

Orbiplex Swarm includes multiple artifact classes with different legal and ecosystem requirements:

- runtime software (`swarm-node`, `orchestrator`, GUI assistant),
- machine-readable protocol artifacts (schemas, test vectors, reference implementations),
- documentation artifacts (protocol prose, manuals, runbooks),
- UI font assets.

The upstream concerns are reciprocity, human agency, open interfaces and the
ability to exit or fork; see
[Core Values](../../normative/30-core-values/en/CORE-VALUES.en.md) and
[Vision](../../normative/20-vision/en/VISION.en.md). This proposal turns those
concerns into artifact boundaries and release checks. The values do not uniquely
determine a license, and licensing does not replace constitutional authority,
participant consent, or host authorization.

Input analysis is documented in:

- `doc/project/10-challenges/001-licensing.md`
- `doc/project/30-stories/story-001-swarm-node-onboarding.md`
- `doc/project/50-requirements/requirements-001-node-onboarding.md`

### Current implementation versus the earlier proposal

`Fact, inspected 2026-10-20`: `node:Cargo.toml` declares `AGPL-3.0-only`;
all 161 packages returned by the inspected workspace metadata report that
license. This includes integration-facing Rust libraries. The earlier P001
proposal instead recommended Apache for the runtime. Its `Proposed` status did
not override the licenses on the code.

The dated dependency investigation belongs in Node:
`node:docs/audits/INTEGRATION-LICENSING-2026-10-20.md`. It records inspected
revisions, candidate closures, packaging dependencies and evidence limits, not
a legal opinion or a new implementation-completion claim.

## Proposed Model / Decision

### Options considered

1. **Strong copyleft everywhere.** Protects reciprocal software development but
   unnecessarily couples independent integrators to implementation licensing;
   it also fails to distinguish software from prose, data and third-party assets.
2. **Permissive everywhere.** Lowers integration friction but does not require
   source availability for proprietary improvements to the reference service.
3. **Layered hybrid.** Protects the reference implementation while deliberately
   permitting broad reuse of the interface and client-side building blocks.
   Selected, with the revised boundary below.

### Artifact baseline

These are defaults for project-owned material that the project has authority
to license, not permission to replace third-party notices.

| Artifact | Target license | Boundary |
|---|---|---|
| Reference Node daemon, host services, organ implementations, orchestrator, UI and project-owned product middleware | `AGPL-3.0-only` | Running a product component out of process does not by itself change its project licensing default. |
| Internal implementation libraries, including domain `*-core` crates | `AGPL-3.0-only` | Purity, small size or a `core` suffix is not a reason to relicense a library. |
| Explicitly selected SDKs, protocol clients and helpers for independent middleware | `Apache-2.0` | Only after their production/build dependency closure and bundled assets are cleared. |
| Machine-readable protocol schemas, public registry vocabulary, reference vectors and executable integration examples intended for copying | `Apache-2.0` | Select public contract material; this does not make every runtime fixture, configuration, registry policy or generated artifact permissive. |
| Manuals, architecture documents and protocol prose | `CC-BY-4.0` | Mark copyable code separately under a software license. |
| Project-owned font software | `OFL-1.1` where appropriate | Third-party fonts retain their original terms. |
| Third-party code, artwork, models, weights and datasets | Their applicable licenses | Keep provenance and notices; inclusion in an AGPL repository is not relicensing authority. |

Do not change `AGPL-3.0-only` to `AGPL-3.0-or-later` implicitly. New project
modules must not introduce `GPL-2.0-only`; third-party compatibility is reviewed
per combination. MPL, LGPL, custom linking exceptions and dual licensing are not
additional defaults: any such exception requires a separate compatibility and
rights decision.

### What reciprocity does and does not mean

AGPLv3 section 13 requires a modified network-interactive version to offer its
Corresponding Source to remote users. Distribution has separate source
obligations. This supports user freedom; it does not require an upstream pull
request or prohibit commercial hosting. Mere network interaction is not
conveying a copy, and independent works in an aggregate do not automatically
inherit AGPL. [AGPLv3](https://spdx.org/licenses/AGPL-3.0-only.html)

An Apache SDK is not a blanket permission to combine arbitrary proprietary code
with the AGPL implementation. Conversely, using an independent client must not
be described as automatically relicensing that client. Review the actual work,
including copied implementation and dependencies; process separation and JSON
alone are not a legal safe harbor.

Apache provides broad reuse and an explicit contributor patent grant, with
notice requirements; it does not require publication of modifications.
Permitting closed independent integrations is an intentional trade-off.
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)

Software licensing does not grant access to private data, host capabilities,
models or the network. It does not make Creator Credits, donations or community
membership conditions of exercising the software license.

### Integration-surface selection

Prefer reusing existing contracts and client implementations over introducing a
parallel SDK. Select by external responsibility, not directory name:

| Candidate | Proposed treatment |
|---|---|
| `protocol` with `canonical-json` and `capability-id` | First Rust contract slice; audit included contract registries and vectors as well as Cargo dependencies. |
| Python channel, UI, host-client and configuration-snapshot helpers | First client slice; package an explicit file set, not the whole middleware support directory. |
| `middleware-channel-core` and `middleware-channel-client` | High-value Rust SDK, blocked by their current dependency on the full Schema Gate. Extract shared channel validation before considering a license change. |
| `http-runtime` and `communication-trace-core` | Supporting candidates for that SDK; retain bounded runtime and tracing contracts without pulling in the host recorder or supervisor. |
| `middleware` contract crate, `signer-core`, Sensorium provider contracts, INAC and Artifact Delivery contracts | Follow-on candidates with named external consumers and separately closed dependency/asset sets. Not all are needed by the first SDK. |

Keep the current full `schema-gate`, runtime/supervision, storage, authorization
owners and organ implementations outside this first surface. Do not relicense
Agent, Corpus or Inquirium just because an SDK currently reaches them
transitively. The Node audit owns exact edges, exclusions and candidate priority.

### Concrete integration scenario

An independently authored sensor connector uses the selected Apache channel
client and public schemas. Node still performs package admission, capability
checks and data classification. The client license confers no execution
authority. Changes to Node's host enforcement remain changes to the AGPL
implementation; publishing a client SDK does not weaken those controls.

### Decision history

The 2026-02-22 version selected a hybrid with Apache for runtime and integration
code, CC BY for prose and OFL for fonts. The 2026-10-20 revision replaces the
runtime and internal-library recommendation with AGPL, retains the permissive
integration goal, and makes extraction conditional on evidence and authorization.
The older challenge remains historical option analysis, not a competing baseline.

## Trade-offs

- **Reciprocity versus adoption:** protect shared runtime improvements while
  accepting that permissive client code may be used in closed integrations.
- **Simple labels versus accurate boundaries:** multiple licenses need an
  explicit file/package map, but one repository-wide label hides real differences.
- **Reuse versus extraction cost:** a common validator avoids divergent SDK and
  host semantics; extracting it costs work and must preserve refusal behavior.
- **Short-term versus long-term:** document and audit now; change licenses only
  in an authorized, reviewable follow-up. No new runtime readiness is claimed.

## Failure Modes and Mitigations

| Failure | Required mitigation |
|---|---|
| Apache label on an SDK that still depends on uncleared AGPL implementation | Check normal/build, optional-feature and target-specific closures; separate host-only test harnesses and review shipped test assets. |
| Removing validation to make the dependency graph smaller | Share the existing family validator and all relevant semantic checks; retain negative and cross-language fixtures. |
| Cargo graph is clean but `include_str!`, generated code, schemas or copied helpers import uncleared material | Inventory compile-time files, recursive schema references, templates and distribution contents. |
| Root license or a copyright header overwrites third-party provenance | File-level exceptions, original notices and dependency-license review. |
| A new foundation is assumed to own every contribution | Review actual rights and contributor terms before any alternate grant. |
| SDK license is mistaken for host authorization or a general exception to AGPL | Document independent-client scope and keep admission at existing owners. |

## Open Questions

1. Which exact files have sufficient provenance and rights for an alternate
   Apache grant? The dependency audit does not answer this legal question.
2. Which contributor terms should govern future changes across AGPL and Apache
   surfaces? Do not assume a DCO transfers copyright or grants arbitrary relicensing.
3. Which target/feature/package matrix will be supported for the first standalone
   Rust and Python SDK releases?

## Next Actions

1. Review the Node audit and select the small contract/Python slice first.
2. Clear rights and packaging inputs before authorizing any license edits.
3. Prepare the shared channel-validation extraction and standalone consumer
   tests; do not broaden the permissive set to hide existing coupling.
4. Apply approved licensing changes separately, then publish the file-level map
   and contributor/release guidance.

### Implementation tracker

Statuses: `todo`, `partial`, `done`. Audit completion is not licensing completion.

| ID | Status | Task | Dependencies | Completion gate |
|---|---|---|---|---|
| P001-001 | done | Record the scoped integration dependency audit | None | Dated Node audit pins source revisions, normal/build versus dev edges, non-Cargo assets and incomplete platform/legal coverage. |
| P001-002 | todo | Clear the selected artifact and contribution inventory | P001-001 | Exact files/packages, generated and copied inputs, external dependency terms and notices, rights holders and explicit authorization are recorded. |
| P001-003 | todo | Prepare an independently consumable SDK boundary | P001-001 | Shared channel validation is reused by host and client; standalone consumers need no unrelated host/domain crates or sibling checkout; refusal and wire semantics remain unchanged. This task alone grants no license. |
| P001-004 | todo | Apply the approved license map | P001-002; P001-003 for the Rust channel SDK | Separate authorized change updates package/file metadata, license texts and notices; unselected implementation remains AGPL and third-party notices survive. |
| P001-005 | todo | Gate package and dependency drift | P001-002, P001-003 | Supported target/features and normal/build closures are checked; distribution assets and dev harnesses are classified; an accidental AGPL dependency in the selected Apache surface fails. |
| P001-006 | todo | Publish integration and release licensing guidance | P001-004, P001-005 | Examples, contributor terms, source-offer/release procedures and a machine-readable third-party inventory match actual packages, not just this proposal. |

### Implementation recommendations

1. Follow `node:DEV-GUIDELINES.md`: keep one owner of each validation contract.
   Reuse the current Schema Gate family machinery behind a dependency-light
   boundary consumed by both the SDK and the full host gate. Preserve closed
   schema resolution, boundary directions, limits and semantic checks.
2. Keep the Node workspace default AGPL. Give approved exceptions explicit
   package/file metadata; do not flip the workspace default to simplify SDK work.
3. Use manifest metadata for discovery, then inspect generated/embedded inputs
   and package contents. A dependency's advertised license is evidence, not
   proof of all bundled-file terms.
4. Keep normal/build closure checks separate from integration-test harnesses.
   An AGPL host may exercise the SDK without making the host part of the SDK;
   do not ship host test code as permissive examples without clearance.
5. Prefer standalone-consumer fixtures using existing golden vectors and
   canonical schemas. Do not invent a second JSON validator, transport protocol,
   authorization model or Python configuration resolver.
6. Prose and copyable software examples need distinct, discoverable licensing.
   CC recommends software-specific licenses for software, while allowing CC
   for documentation. [Creative Commons FAQ](https://creativecommons.org/faq/)
7. Reconcile implementation ledgers only when ownership or implementation
   evidence actually changes. This documentation revision changes neither
   runtime behavior nor capability completion.
