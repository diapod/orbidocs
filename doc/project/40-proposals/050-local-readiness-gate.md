# Proposal 050: Local Readiness Gate

Based on:

- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/034-node-operator-binding-and-derived-node-assurance.md`
- `doc/project/40-proposals/044-host-owned-generic-module-store.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`

## Status

Draft

## Date

2026-04-22

## Executive Summary

The Node needs a local startup posture for cases where the control plane can
safely run, but the full runtime must not start yet. The original implementation
called the first instance of this posture **Config Approval Mode**, because the
only blocking condition was a stale or denied signed middleware configuration
artifact.

This proposal generalizes that posture into **Local Readiness Gate**.

A Local Readiness Gate is a daemon phase in which a minimal local control plane
is available, Node UI can show actionable blockers, and runtime components that
depend on unresolved local artifacts, keys, passports, or signatures remain
stopped. Config approval becomes one gate item type, not the name of the mode.

The purpose is to keep startup semantics honest:

- missing or stale local authority material is not silently ignored,
- dependent runtime components do not start in a partially configured state,
- the operator gets a small local surface to complete or reject the required
  actions,
- once all blockers are resolved, the daemon can exit for supervisor restart or
  restart itself through an explicit local control operation.

## Problem

A node is a composition of local components. If one component requires an
operator-signed action catalog, a local participant key, a capability passport,
or another host-owned artifact before it can safely run, the node is not fully
ready. Treating that condition as a normal degraded runtime is misleading: other
components may start, observe incomplete state, and create confusing secondary
failures.

The narrower Config Approval Mode solved one case: stale signed configuration
artifacts. It did not name the broader invariant: **local runtime should start
only after local readiness prerequisites have been satisfied or explicitly
rejected by the operator.**

## Decision

Orbiplex Node SHOULD expose a daemon phase named:

```text
local_readiness_gate
```

This phase replaces the previous `config_approval` phase name. Consumers MAY
continue to tolerate `config_approval` as a legacy label while nodes migrate.

In `local_readiness_gate`:

- daemon control endpoints are available,
- Node UI is available,
- local identity and operator signing surfaces needed to resolve blockers are
  available,
- runtime middleware, peer sessions, and story workflows that depend on the
  blocked material are not started,
- each blocker is represented as explicit data with a kind, subject, reason,
  and an operator action path where possible.

Signed middleware configuration approval is represented as:

```json
{
  "kind": "signed-middleware-config-artifact",
  "module_id": "sensorium-os",
  "artifact_id": "action-catalog",
  "reason": "signature-stale"
}
```

The existing middleware-config-artifact signing endpoints remain the concrete
operator action surface for that blocker kind.

## Minimal Components

The gate may run only components that do not depend on unresolved gated
artifacts. The minimal local set is:

| Component | Role | Dependency rule |
| --- | --- | --- |
| daemon control plane | exposes local status and operator endpoints | must not require gated middleware artifacts |
| health/control endpoint | serves local JSON status and operator APIs | must not depend on gated middleware runtime |
| Node UI | operator-facing view and approval actions | may depend only on daemon control APIs |
| node identity read surface | shows node identity and local participant state | may read host-owned identity material |
| operator signing surface | signs or denies gate actions | must be explicit and audit-producing |
| host-owned config artifact store | stores signed sidecars and decisions | must be local and append/audit friendly |

Seed Directory or other local read-only services MAY run in this phase only if
they do not require unresolved gate artifacts. They MUST NOT be used to imply
that the full node runtime is ready.

Middleware runtime, peer session orchestration, workflow execution, and
capability advertisement redistribution SHOULD wait until the gate is clear.

## Gate Item Classes

The initial gate item classes are:

| Kind | Meaning | First concrete use |
| --- | --- | --- |
| `signed-middleware-config-artifact` | a declared middleware config fragment needs a valid grant or deny sidecar | Sensorium OS action catalog |
| `missing-local-participant-key` | a local service needs a participant key before host-issued passports can be produced | Dator offer-catalog passport issuance |
| `missing-local-capability-passport` | a configured local service needs a host-issued or operator-provided passport before runtime | story/service offer publication |
| `stale-local-capability-passport` | a required passport is expired or revoked according to local policy | production service startup |

The initial implementation supports the first three classes. Passport staleness
is represented as `missing-local-capability-passport` with
`reason: "passport-stale-or-revoked"` until revocation-specific operator flows
become richer.

## Configuration Shape

Nodes declare local readiness prerequisites as data:

```json
{
  "local_readiness": {
    "require_operator_participant_key": true,
    "required_capability_passports": [
      {
        "id": "story009-json-e-flow.memarium-space-access",
        "label": "Story-009 JSON-e role provider Memarium passport",
        "capability_id": "memarium-space-access",
        "module_id": "story009.json-e-flow.roles"
      }
    ]
  }
}
```

`node_id` may be supplied per required passport. If omitted, the local node id is
used. This keeps the gate generic: Story-009 is one profile, not hard-coded
daemon behavior.

## Operator Flow

1. The daemon starts the minimal control plane.
2. The daemon computes local readiness blockers.
3. If no blockers exist, normal runtime starts.
4. If blockers exist, the daemon enters `local_readiness_gate` and exposes the
   blocker list.
5. Node UI shows each blocker with the safest available action: sign, deny,
   create/import key, issue/import passport, or inspect.
6. The operator completes or rejects the blockers.
7. When the blocker list is empty, the node either:
   - exits with a restart-required status for the supervisor, or
   - performs an explicit daemon restart/reload operation.

The first implementation may require manual daemon restart after signing. A
later implementation may auto-restart after the final blocker is resolved, but
that transition MUST be visible in the audit trail.

## API Shape

The daemon SHOULD expose a local operator endpoint:

```text
GET /v1/operator/local-readiness-gate/pending
```

Minimal response:

```json
{
  "schema": "orbiplex.local-readiness-gate.v1",
  "status": "blocked",
  "phase": "local_readiness_gate",
  "restart_required": false,
  "next_action": "resolve-pending-readiness-actions",
  "minimal_components": [
    "daemon-control-plane",
    "health-control-endpoint",
    "node-ui",
    "node-identity",
    "operator-signing-surface",
    "host-owned-config-artifact-store"
  ],
  "pending": [
    {
      "kind": "signed-middleware-config-artifact",
      "module_id": "sensorium-os",
      "artifact_id": "action-catalog",
      "reason": "signature-stale"
    }
  ]
}
```

When the blocker list becomes empty while the daemon is still in
`local_readiness_gate`, the endpoint MUST NOT report ordinary `ready`. The
runtime was intentionally not started in that process. The response SHOULD use:

```json
{
  "schema": "orbiplex.local-readiness-gate.v1",
  "status": "restart_required",
  "phase": "local_readiness_gate",
  "restart_required": true,
  "next_action": "restart-daemon",
  "pending": []
}
```

This keeps the lifecycle boundary explicit: resolving readiness blockers does
not silently start dependent middleware in a partially initialized daemon.

Specialized endpoints such as
`/v1/operator/middleware-config-artifacts/pending` MAY remain available for
specific UI panels and tooling, but they are subordinate to the Local Readiness
Gate contract.

The daemon MAY also expose:

```text
POST /v1/daemon/restart
```

Node UI MAY surface this as the Local Readiness Gate continuation action when
`status` is `restart_required`.

## Compatibility

`Config Approval Mode` is deprecated terminology. Documentation that still
mentions it SHOULD describe it as the former name for the signed-configuration
case of Local Readiness Gate and link to this proposal.

Implementations SHOULD tolerate the old daemon phase label `config_approval`
while migrating UIs and scripts, but new status snapshots SHOULD use
`local_readiness_gate`.

## Non-Goals

- This proposal does not define federation readiness.
- This proposal does not let middleware bypass operator approval by starting in
  a partial mode.
- This proposal does not define the full UI for participant-key creation or
  passport issuance.
- This proposal does not replace the signed middleware configuration artifact
  sidecar mechanism; it places it under a wider readiness gate.
