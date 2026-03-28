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
- `doc/project/30-stories/story-005.md`
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
- `doc/project/30-stories/story-005.md`
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
