# Notifications

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`
- `doc/project/40-proposals/009-communication-exposure-modes.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/052-tauri-hosted-node-ui.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `notification.v1`
- `notification-create.v1`
- `notification-action.v1`
- `notification-action-result.v1`
- `notification-state-changed.v1`
- `notification-allow.v1`
- `notification-delivery-policy.v1`

## Responsibility maintenance M0 (2026-10-20)

The [S040 contract](../040-capability-limited-restrictions/040-safe-maintenance-contracts.md)
freezes separate future maintenance grants and recipient-bound alert references.
No live registry/policy entry or notification action/delivery is added at M0.
The host operator owner must admit current grants and resolve the actual S039
recipient; absent recipient stays pending. Acknowledgment supplies no authority.
M4/M5/Q qualification and full P051-010 alignment remain open.

## Status

Implemented MVP solution.

Operator notifications, durable queue, action execution, privacy-minimal SSE,
and user/pod-user recipient boundaries are implemented for the MVP slice.
Native desktop OS notification adapters and richer pod-user product UX remain
post-MVP presentation layers.

Responsibility maintenance is an implemented additional consumer at the
2026-10-23 M5 owner checkpoint. Its bounded domain intents and independent control
reserve feed this queue through S020. `operator:default` is the shared mailbox;
access and delivery additionally require the actual current signed operator
binding. Only the canonical operator inbox exposes these notices; general/admin
aliases, counts and SSE do not disclose them. Separate queued, delivered, opened
and acknowledged states remain distinct. Verified archive-backed retrieval permits
closed resident-metadata recovery without waiting for acknowledgment.

This is owner/routing conformance; final Q must still qualify the actual API/UI
and retention paths on its clean candidate. Earlier tracing alone proves no
operator delivery. Acknowledgment grants no maintenance, repair or participant
authority. v1 remains authoritative, all D7 components remain false and maintenance
is disabled by default. See
`node:docs/development/RESPONSIBILITY-MAINTENANCE-ALERTS-CONTRACT.md` and
`node:docs/audits/RESPONSIBILITY-MAINTENANCE-Q-REVIEW-2026-10-23.md`.

## Date

2026-07-03

## Executive Summary

Notifications are the local attention-management layer for users and operators.
They turn node facts, middleware requests, policy decisions, and long-running
work results into durable, recipient-scoped attention items.

A notification is not an event stream, an inbox protocol, or an OS popup. Those
are delivery and presentation surfaces. The notification solution owns the
semantic queue, idempotency, recipient isolation, local policy evaluation,
schema-defined actions, and privacy-minimal state-change pings.

## Context and Problem Statement

Many Orbiplex components need to ask a human to notice something: readiness
blockers, trust remediation, failed deliveries, relevant whispers, contact
requests, and operator questions. If every component emits its own UI fragment
or event stream, attention policy becomes duplicated and unsafe.

The solution creates one local contract:

```text
domain fact / middleware request
  -> notification.create
  -> policy evaluation
  -> durable recipient queue
  -> UI/API projection
  -> optional schema-defined action
```

## Proposed Model / Decision

The daemon hosts the store and host capability, while the semantics belong to
the human-facing UI stratum. Components may request local attention, but they do
not own the UI and cannot inject arbitrary HTML.

The durable store separates mutable queue projection from append-only audit and
transaction facts. `body/input` is accepted only as transient request material;
durable rows keep title, body text, body ref, digest/redacted summary, actions,
and source references.

SSE carries only `notification-state-changed.v1` snapshots: recipient id,
optional notification id, unread count, maximum unread priority, and last
changed timestamp. It never carries title, body, kind, subject, action payload,
or raw input.

## Must Implement

### Notification Contracts and Policy

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`

Related schemas:

- `notification.v1`
- `notification-create.v1`
- `notification-allow.v1`
- `notification-delivery-policy.v1`

Responsibilities:

- define typed notification queue records and create requests;
- scope idempotency by `(sender/id, idempotency/key)`;
- enforce `NotificationAllow` for external middleware;
- evaluate local delivery policy before interrupting or pinging recipients;
- keep structured `body/input` transient and out of durable storage.

Status:

- `done`

### Durable Queue and Audit

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`

Related schemas:

- `notification.v1`

Responsibilities:

- persist notifications across daemon and UI restarts;
- keep a temporal event log as the recovery source of truth;
- maintain a current queue projection for low-latency reads;
- keep JSONL audit as a redacted diagnostic/export mirror;
- support opened, handled, snoozed, delete, collapse, supersede, and
  idempotency conflict paths.

Status:

- `done`

### Host Capability and Legacy Bridge

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`

Related schemas:

- `notification-create.v1`

Responsibilities:

- expose `notification.create` as the canonical middleware entry point;
- bind sender identity to authenticated component identity;
- adapt legacy `notify_emit` into the same queue and policy path;
- deny unknown or unauthorized sender/kind/recipient combinations fail-closed.

Status:

- `done`

### Operator and User Presentation Surfaces

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`

Related schemas:

- `notification.v1`
- `notification-state-changed.v1`

Responsibilities:

- expose list/detail/opened/handled/snooze/delete routes;
- render operator and admin inboxes;
- expose user and pod-user scoped read/action routes with caller-binding
  isolation;
- publish privacy-minimal SSE pings and refresh read models after reconnect.

Status:

- `done` for the MVP surfaces; first-class pod-user session UX remains product
  hardening.

### Schema-Defined Actions

Based on:

- `doc/project/40-proposals/057-user-and-operator-notifications.md`

Related schemas:

- `notification-action.v1`
- `notification-action-result.v1`

Responsibilities:

- render only schema-defined action widgets;
- dispatch registered action refs through daemon-owned handlers;
- reject expired, replayed, stale-version, unauthorized, or unwired actions;
- record action-submitted audit facts with bound actor identity.

Status:

- `done`

## May Implement

### Native OS Notifications

Based on:

- `doc/project/40-proposals/052-tauri-hosted-node-ui.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`

Related schemas:

- `notification-state-changed.v1`

Responsibilities:

- project local notification state into native desktop notification APIs;
- preserve redaction and quiet-hours policy;
- never make OS delivery the source of notification authority.

Status:

- `deferred`

## Out of Scope

- arbitrary HTML/HTMX fragments supplied by middleware;
- cross-node notification aggregation;
- using notification action buttons as direct domain authority;
- persisting raw `body/input`;
- treating SSE as a full event replay log in MVP.

## Consumes

- node facts and diagnostic refs;
- middleware `notification.create` requests;
- local attention and authorization policy;
- recipient/caller binding state.

## Produces

- durable notification queue projections;
- notification audit facts;
- `notification-state-changed.v1` SSE payloads;
- action result records.

## Planned Matrix recovery source (P035-013)

Durable account-history `blocked` and `awaiting-operator-retry` facts are a planned
host-owned notification source. Emit idempotent lifecycle updates after the recovery
transaction commits; do not expose pagination tokens or treat notification delivery
as recovery success. A button resolves current local operator authority and a fresh
inspected task revision. Credible Retry-After keeps its not-before; the implausible
escape remains a separate action requiring a reason. A bounded bulk operation uses
a CAS and result per task, including partial failures, and cannot clear other limits.

P035-013 owns implementation and runtime evidence. This planned adapter does not
claim active alerts, batch retry or authority granted by a notification.

## Related Capability Data

- `039-notifications-caps.edn`
