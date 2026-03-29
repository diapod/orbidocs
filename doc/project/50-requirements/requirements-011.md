# Requirements 011: Reference Contracts for Bundled `Dator` and `Arca`

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/020-bundled-python-middleware-modules.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/30-stories/story-006.md`
- `doc/project/60-solutions/node.md`

Date: `2026-03-30`
Status: Draft (hard MVP slice)

## Executive Summary

This document freezes the minimum reference contract for the two bundled hard-MVP
middleware modules:

- `Orbiplex Dator`
- `Orbiplex Arca`

It does not create a second middleware protocol. Both modules still consume the
host `WorkflowEnvelope` and emit `MiddlewareDecision` through the supervised
`http_local_json` runtime. What this document adds is the minimum semantic scope of
each module so implementation can proceed without ambiguity.

## Module Roles

### `Orbiplex Dator`

`Dator` is the exchange-facing middleware module for priced service work.

Its hard-MVP role is to help the host with:

- service publication and service metadata shaping,
- procurement-facing execution shaping for offered services,
- model-backed preprocessing or drafting requests routed through the host,
- response shaping for exchange-visible outputs,
- queue posture and bounded acceptance posture for service work.

`Dator` is not the authority for:

- transport identity,
- protocol signing,
- settlement,
- reputation,
- participant restrictions.

Those remain host responsibilities.

### `Orbiplex Arca`

`Arca` is the workflow orchestration middleware module.

Its hard-MVP role is to help the host with:

- multi-step local and remote workflow orchestration,
- bounded retries and phase sequencing,
- host-mediated file or publication preparation,
- coordination of repeated or scheduled content workflows,
- preserving workflow-local causality in a way the host can trace.

`Arca` is not the authority for:

- signing external contracts,
- substituting operators silently,
- bypassing procurement or settlement rules,
- independently changing provider identity or payment semantics.

## Shared Transport and Envelope Contract

Both bundled modules MUST:

- be launched as supervised Python services through `http_local_json`,
- expose loopback HTTP readiness and invocation endpoints,
- accept host-generated `WorkflowEnvelope` input,
- return host-validated `MiddlewareDecision` output,
- support host-owned `middleware-init` and module reporting.

Neither module may require:

- direct access to host secret material,
- direct control of network peer sessions,
- direct invocation of settlement rails,
- direct bypass of host field-registry or policy checks.

## Hard-MVP `Dator` Contract

At minimum, `Dator` MUST be able to:

- shape service-offer publication metadata for exchange-facing work,
- translate a selected service execution path into host-usable procurement and
  response workflow intent,
- request model-backed work through the host rather than vendor APIs directly,
- surface bounded queue pressure or temporary unavailability as host-visible
  middleware outcomes,
- shape final response payloads without becoming the settlement authority.

For hard MVP, `Dator` SHOULD treat the current executable substrate as canonical:

- `procurement-contract.v1`
- `response-envelope.v1`
- `procurement-receipt.v1`
- `ledger-hold.v1`
- `ledger-transfer.v1`
- `gateway-receipt.v1`

That means `Dator` MAY present richer exchange semantics, but MUST project them
back into the current host procurement and settlement artifacts.

## Hard-MVP `Arca` Contract

At minimum, `Arca` MUST be able to:

- orchestrate multi-phase content workflows spanning local and remote execution,
- preserve explicit phase boundaries and retry posture,
- request remote paid work through host procurement rather than side channels,
- stage local output preparation through host-approved mutations,
- stop and surface failure when a downstream phase cannot proceed under policy.

`Arca` MUST NOT silently replace one provider with another or alter the economic
meaning of a workflow step without an explicit host-approved transition.

## Module Report Expectations

Both bundled modules MUST report at least:

- module name,
- short description,
- module version,
- capability ids,
- middleware contract version,
- host API version expectation.

Recommended capability ids:

- `dator/exchange-service-publication`
- `dator/service-execution-shaping`
- `arca/workflow-orchestration`
- `arca/phase-retry-and-publication-shaping`

These ids remain descriptive in MVP; they are not yet independent protocol
authorities.

## Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| FR-001 | The hard MVP MUST bundle two reference middleware modules: `Orbiplex Dator` and `Orbiplex Arca`. | Fact | Proposal 020 |
| FR-002 | Both bundled modules MUST be implemented in Python and launched through the supervised `http_local_json` executor. | Fact | Proposal 020 + Requirements 010 |
| FR-003 | `Dator` MUST consume `WorkflowEnvelope` and emit `MiddlewareDecision` without introducing a second invocation protocol. | Fact | Requirements 010 |
| FR-004 | `Arca` MUST consume `WorkflowEnvelope` and emit `MiddlewareDecision` without introducing a second invocation protocol. | Fact | Requirements 010 |
| FR-005 | `Dator` MUST shape exchange-facing service work while delegating model invocation, settlement, signing, and restriction enforcement to the host. | Fact | Story 006 + project values |
| FR-006 | `Arca` MUST shape workflow orchestration while delegating signing, settlement, and policy authority to the host. | Fact | Story 006 + project values |
| FR-007 | `Dator` MUST project its richer service semantics back into the currently executable host substrate based on procurement, response, and settlement artifacts. | Fact | Story 006 |
| FR-008 | `Arca` MUST route remote paid steps through host procurement rather than side-channel execution. | Fact | Story 006 |
| FR-009 | Both bundled modules MUST support `middleware-init` and return module reports with stable version and capability metadata. | Fact | Requirements 010 |
| FR-010 | The host MUST remain free to reject or clip module-proposed mutations through field-registry and policy validation. | Fact | Story 006 + project values |

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|---|---|---|---|
| NFR-001 | Bundled reference modules SHOULD accelerate hard-MVP delivery without becoming privileged special cases outside the generic middleware host contract. | Fact | Proposal 020 |
| NFR-002 | The semantic difference between `Dator` and `Arca` MUST stay visible in module reports and operator surfaces. | Inference | Operability |
| NFR-003 | The modules SHOULD remain replaceable by other implementations as long as the host-facing middleware contract is preserved. | Fact | Proposal 020 |

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| `Dator` starts calling model vendors directly | Hidden credentials and trace collapse | Keep model access host-mediated only. |
| `Arca` treats workflow intent as authority to bypass procurement | Hidden economic side channels | Require remote paid work to project into host procurement artifacts. |
| Bundled modules become effectively privileged because they ship with Node | Architecture drifts into opaque monolith | Preserve the same `WorkflowEnvelope` / `MiddlewareDecision` and supervision boundary as for any external module. |
| Module metadata is too weak to diagnose runtime drift | Operators cannot tell which module build is running | Require versioned module reports on `middleware-init`. |

## Next Actions

1. Add hard-MVP component configs for bundled `Dator` and `Arca`.
2. Define their first capability ids and version strings.
3. Add integration scenarios covering:
   - `Dator` publication and service execution shaping,
   - `Arca` multi-phase workflow orchestration,
   - host rejection of invalid module decisions,
   - startup and lifecycle supervision for both modules.
