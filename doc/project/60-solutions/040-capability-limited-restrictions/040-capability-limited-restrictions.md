# Capability-Limited Restrictions

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`
- `doc/project/50-requirements/requirements-015-newcomer-surface-limits.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`

Related schemas:

- `participant-capability-limits.v1`
- `participant-effective-limits.v1`
- `surface-access-policy.v1`

## Status

Implemented solution.

This solution captures the implemented `participant-capability-limits.v1`
runtime slice. Newcomer and membership/sponsorship policies may project into
the same effective-limits vocabulary, but their social-policy source artifacts
remain outside this solution.

## Date

2026-07-03

## Executive Summary

Capability-Limited Restrictions are the host-owned enforcement layer for
temporarily reducing a participant's operational influence on specific
surfaces. The model is layered: protected floors remain available, hard blocks
deny selected privileged operations, and soft factors alter ranking or cooldown
without silently becoming bans.

The solution is intentionally auditable rather than folkloric. Imports are
schema-gated, stale or already-dead records are rejected, clear operations can
carry `reason/ref`, and replay reconstructs the current participant restriction
state from durable facts.

## Context and Problem Statement

Orbiplex needs practical ways to reduce harm without turning every incident into
a global identity ban. Newcomer limits, probation, sponsor liability, fraud
holds, and operator sanctions all need a common lower layer that can say:

```text
participant X may not use operation Y until time T
participant X is ranked lower for operation family Z
participant X has slower cooldown for operation family W
```

Before this solution, such restrictions risked becoming scattered across
procurement, messaging, governance, and UI-specific checks.

## Proposed Model / Decision

The participant capability-limits layer is a local host enforcement read model.
It consumes signed or operator-imported restriction records and clear
tombstones, then exposes deterministic decisions to operation gates.

Rules:

- protected floor operations cannot be hard-blocked by this layer;
- hard blocks fail closed for configured privileged operation families;
- soft priority factors affect ranking/scoring;
- soft rate-limit factors affect cooldown;
- stale imports do not overwrite newer facts or clear tombstones;
- already-expired hard blocks are rejected before mutating state;
- operator-visible refresh events are metadata-only.

## Must Implement

### Capability Limits Contract

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- define the canonical restriction artifact;
- reject unsafe or unknown hard-block targets;
- keep protected floor operations unblocked;
- validate participant ids, reason refs, expiry windows, and soft factors.

Status:

- `done`

### Schema-Gated Import and Clear

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- reject invalid, oversized, stale, already-dead, or already-expired imports;
- preserve monotonic `recorded-at` and `last_cleared_at` semantics;
- accept optional bounded `reason/ref` when clearing restrictions;
- emit clear tombstones instead of deleting history.

Status:

- `done`

### Operation Enforcement Hooks

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- enforce hard blocks on the first privileged operation set;
- apply priority-factor penalties in procurement ranking;
- apply rate-limit-factor cooldowns at admitted operation gates;
- keep participant-side accept/dispute/reject controls separate from operator
  execution controls.

Status:

- `done`

### Durable Replay and Operator Visibility

Based on:

- `doc/project/40-proposals/018-layered-capability-limited-participant-restrictions.md`

Related schemas:

- `participant-capability-limits.v1`

Responsibilities:

- append imports and clear tombstones to the daemon commit log;
- replay the current read model deterministically;
- expose import, list, detail/export, and clear routes;
- emit metadata-only refresh events for operator surfaces.

Status:

- `done`

## May Implement

### Newcomer Effective-Limits Projection

Based on:

- `doc/project/50-requirements/requirements-015-newcomer-surface-limits.md`
- `doc/project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md`

Related schemas:

- `participant-effective-limits.v1`
- `surface-access-policy.v1`

Responsibilities:

- project entry profile, surface access policy, sanctions, and appeals into one
  effective-limits read model;
- keep social membership policy outside the enforcement primitive;
- allow newcomer defaults and sanctions to share operation vocabulary without
  sharing authority.

Status:

- `post-MVP`

## Out of Scope

- moral classification of participants;
- global federation ban semantics;
- deciding membership or sponsorship status;
- replacing capability passports or operation-specific authorization;
- blocking protected floor operations.

## Consumes

- participant capability-limits records;
- clear tombstones;
- operation admission context;
- procurement ranking inputs.

## Produces

- hard-block decisions;
- soft ranking/cooldown modifiers;
- durable replay state;
- metadata-only operator refresh events.

## Related Capability Data

- `040-capability-limited-restrictions-caps.edn`
