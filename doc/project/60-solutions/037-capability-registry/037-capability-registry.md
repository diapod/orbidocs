# Capability Registry

Based on:

- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/007-capability-advertisement/007-capability-advertisement.md`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md`

Related schemas:

- `capability-registry.v1`
- `capability-authorization-policy.v1`
- `capability-advertisement.v1`
- `capability-passport-present.v1`
- `seed-capability-registration.v1`

## Status

Implemented solution.

## Date

2026-06-25

## Executive Summary

Capability Registry is the canonical machine-readable source of known Orbiplex
capability identifiers. It defines which capability ids exist, how they may be
used, where they may appear, and which runtime gates must refuse them when they
are unregistered or ineligible.

The registry is not a complete authorization engine. It answers the naming and
eligibility question first: "is this capability id known, active, and eligible
for this surface?" Capability passports, host grants, operator approvals, and
domain-specific policy still decide whether a caller may use the capability in a
particular situation.

The authorization-policy sidecar adds checked policy metadata for capability
families that need it early, such as Sensorium Workbench and Interaction Broker,
without turning the registry into a workflow or governance engine.

## Context and Problem Statement

Before the registry, capabilities could enter the system through several
surfaces: advertisements, passports, host routes, middleware reports, Seed
Directory records, or literal daemon route declarations. If those surfaces each
kept their own allow-set, drift would be easy and dangerous.

The registry gives the node one checked data source for capability id grammar,
wire names, lifecycle status, and surface eligibility. New unregistered
capability ids fail closed until the registry and its projections are updated.

## Proposed Model / Decision

The checked-in registry is a data contract.

Each `capability-registry.v1` entry carries:

- `capability/id`;
- owner/component metadata;
- one or more closed registry surfaces: `federated` and/or `host-local`;
- canonical `wire/name`;
- lifecycle `status`;
- the fixed use-specific eligibility flags: `dispatchable`, `advertisable`,
  `passport/eligible`, `signing-domain`, `host-route`, and
  `federated-discovery`.

Runtime gates derive admission from the registry:

- capability advertisement signing and verification;
- capability passport validation;
- daemon host-capability dispatch and literal host routes;
- supervised middleware module-report admission;
- CI drift checks over docs, fixtures, and runtime projections.

`capability-authorization-policy.v1` is a sidecar. It carries required grants,
caller posture, approval mode, autonomy floor, and COI policy for selected
capability families. It is validated against registered capability refs, but its
runtime enforcement belongs to host-policy consumers.

## Must Implement

### Machine Capability Registry

Based on:

- `doc/project/40-proposals/072-capability-registry.md`

Related schemas:

- `capability-registry.v1`

Responsibilities:

- keep the checked-in registry as the canonical machine source of capability
  ids;
- validate capability id grammar, unique wire names, lifecycle status, and
  surface eligibility flags;
- reject malformed static registry material before runtime surfaces treat it as
  an allow-set;
- preserve legacy runtime projections only as checked projections, not as
  second authorities.

Status:

- `done`

### Runtime Admission Gates

Based on:

- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/007-capability-advertisement/007-capability-advertisement.md`

Related schemas:

- `capability-advertisement.v1`
- `capability-passport-present.v1`
- `seed-capability-registration.v1`

Responsibilities:

- deny unregistered or ineligible capability ids at advertisement, passport,
  host dispatch, host-route, and middleware report gates;
- derive dispatchable and host-route admission from registry flags;
- require dynamic middleware reports to claim only registered and eligible host
  capability handlers;
- keep authorization separate from registry existence.

Status:

- `done`

### Drift and Documentation Checks

Based on:

- `doc/project/40-proposals/072-capability-registry.md`

Related schemas:

- `capability-registry.v1`
- `capability-authorization-policy.v1`

Responsibilities:

- validate human EN/PL registry projections against the machine registry;
- validate passport, advertisement, Seed Directory, and authorization-policy
  fixtures against registered capability refs;
- validate literal daemon host-capability POST routes against the registry;
- fail CI or local checks on code/docs/fixture drift.

Status:

- `done`

### Capability Authorization Policy Sidecar

Based on:

- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/071-sensorium-workbench.md`

Related schemas:

- `capability-authorization-policy.v1`

Responsibilities:

- express required grants, caller posture, approval mode, autonomy floor, and
  COI policy as checked data;
- validate policy entries against registered capability ids;
- seed policy coverage for Sensorium Workbench and Interaction Broker
  capabilities;
- leave runtime grant issuance and enforcement to host-policy consumers.

Status:

- `done`

## May Implement

### Federation Namespace Governance

Based on:

- `doc/project/40-proposals/072-capability-registry.md`

Related schemas:

- `capability-registry.v1`

Responsibilities:

- define public namespace allocation and registration authority;
- define federation-extension revocation and supersession policy;
- keep governance outside the node-local registry enforcement slice until a
  separate proposal accepts it.

Status:

- `deferred`

## Out of Scope

- deciding whether a caller has a concrete grant for one operation;
- replacing capability passports or operator approvals;
- owning federation namespace governance in this solution slice;
- treating the legacy Rust projection as a second source of truth;
- embedding workflow policy in the registry.

## Consumes

- checked-in registry data;
- human capability registry tables;
- capability advertisement/passport/Seed Directory fixtures;
- daemon host-route declarations;
- middleware module reports.

## Produces

- fail-closed registry admission decisions;
- checked capability registry projections;
- authorization policy sidecar validation;
- drift-check diagnostics.

## Related Capability Data

- `037-capability-registry-caps.edn`
