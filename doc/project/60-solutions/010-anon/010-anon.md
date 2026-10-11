# Orbiplex Anon

`Orbiplex Anon` is a Node-attached outbound privacy component that can realize stronger sender obscurity, relay indirection, and onion-like forwarding for protocol artifacts that request such treatment.

It is not specific to `Whisper`. `Whisper` is only one plausible consumer of this capability.

## Purpose

The component is responsible for the solution-level execution path of:
- outbound privacy posture realization,
- relay-capability discovery,
- derived forwarding nym handling,
- bounded hop-policy enforcement,
- and transport-level downgrade or hard-fail decisions under Node policy.

## Scope

This document defines solution-level responsibilities of the Anon component.

It does not define:
- the semantics of rumors, evidence, or association bootstrap,
- a requirement that every Node deployment ship with anonymous relay,
- application-level disclosure policy,
- or concrete cryptographic implementation details.

## Must Implement

### Outbound Privacy Profile Realization

Based on:
- `doc/project/20-memos/orbiplex-anon.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-signal.v1`

Responsibilities:
- inspect outbound routing/privacy intent on protocol artifacts,
- realize allowed profiles such as `relayed` and `onion-relayed`,
- refuse silent downgrade when the caller marked privacy posture as `hard-fail`,
- expose a clear success, degrade, or reject result back to Node egress.

Status:
- `todo`

### Derived Nym and Hop Policy Enforcement

Based on:
- `doc/project/20-memos/orbiplex-anon.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-signal.v1`

Responsibilities:
- derive forwarding nyms without exposing stable origin identity,
- enforce maximum hop count and forwarding limits,
- preserve bounded auditability of routing policy without exposing the full route.

Status:
- `todo`

## May Implement

### General Protected Egress

Based on:
- `doc/project/20-memos/orbiplex-anon.md`

Related schemas:

Responsibilities:
- provide the same outbound privacy surface to non-Whisper artifacts,
- remain reusable by future sensitive relay paths such as witness requests or protected archival handoff.

Status:
- `optional`

## AD Privacy Integration: Planned Direction

Planned 2026-10-11; the `todo` runtime status above is unchanged. Realize outbound
privacy intent through the host's
[S023 Artifact Delivery](../023-artifact-delivery/023-artifact-delivery.md)
transport-selection boundary. Consumers such as
[P013 Whisper](../../40-proposals/013-whisper-social-signal-exchange.md#transport-boundary-with-outbound-privacy-capabilities)
declare requirements; they do not construct relay chains or depend on the Anon
module name. Anon provides a narrowly admitted privacy realization behind that
boundary, not a second component-facing delivery API or admission registry.

### Implementation Recommendations

Keep privacy requirements as data: required/preferred profile, allowed relay
classes, hop/byte/time budgets, linkability scope and explicit downgrade permission.
First map those requirements onto existing routing contracts; freeze missing
schema extensions before exposing an adapter. A selected route must satisfy the
required profile before enqueue/send; re-evaluate after route changes and on retry.
If no compatible adapter exists, `hard-fail` means refusal without transmission.
An allowed downgrade is an explicit decision visible to the authorized caller,
not a successful anonymity claim.

Use existing host sealing/key-custody and AD lifecycle primitives, but do not claim
that `inac-direct` provides anonymous or onion routing. INAC may carry a protected
hop only after the profile proves that its session identity, envelope and receipt
metadata expose no more than the declared threat model permits. Each relay
authenticates and authorizes its own hop; no hop receives ambient onward authority.
The final domain acceptor remains the sole owner of end-artifact admission.

The profile must specify what the origin, each relay, destination and operator can
observe. Protect source/destination correlations, stable ids, timing and return
paths across AD recipient expansion, delivery ids, ledgers, logs and retries.
Minimize retention and bound loop/replay handling. If the existing AD metadata
model cannot meet the requested profile, report it as unsupported and close that
gap before claiming anonymity; do not weaken the claim or invent new cryptography.
The first slice may prove refusal and explicit downgrade without implementing
onion routing. Reference `node:DEV-GUIDELINES.md` for authorization-before-effects,
bounded lifecycle and honest recovery semantics.

### Privacy Integration Tracker

This is the single-source tracker for the S010/P013 AD integration, not a claim
that anonymity is implemented. All entries are `todo`.

| ID | Task | Status | Depends on | Completion gate |
|---|---|---|---|---|
| S010-001 | Freeze privacy profile and metadata threat model | todo | S023 routing/admission contract | Record observable data per actor, request/result shapes, hop authority, budgets, downgrade/refusal rules and metadata-retention limits; evaluate AD ledger/recipient expansion and whether INAC is suitable per hop. Unsupported guarantees remain explicit. |
| S010-002 | Compose privacy provider with AD route selection | todo | S010-001 | Reuse declared middleware/host adapter contracts, sealer and AD lifecycle; unavailable required privacy refuses before enqueue/transmission, allowed downgrade is visible, and retry/fallback cannot weaken a hard requirement. No consumer-owned relay topology or private delivery queue. |
| S010-003 | Retain privacy and failure-boundary acceptance | todo | S010-002 | Prove missing-provider refusal, policy changes during retry, relay failure, bounded loops, duplicate/replay handling, return-path scope and diagnostic redaction. Any implemented multi-hop profile has retained per-actor metadata evidence against S010-001; direct TLS/INAC success is not anonymity evidence. Reconcile Node ledger with only the proven profile. |

## Out of Scope

- rumor semantics and threshold policy
- final disclosure decisions
- application-level room bootstrap policy
- mandatory deployment in every Node

## Consumes

- artifacts carrying outbound routing/privacy intent, including `whisper-signal.v1`

## Produces

- delivery outcomes for Node egress under direct, relayed, or onion-relayed posture

## Related Capability Data

- `anon-caps.edn`

## Notes

Anon may be attached as a separate process or service. Callers should depend on the declared outbound privacy capability, not on the module name itself.
