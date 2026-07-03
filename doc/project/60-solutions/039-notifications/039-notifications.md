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

## Status

Implemented MVP solution.

Operator notifications, durable queue, action execution, privacy-minimal SSE,
and user/pod-user recipient boundaries are implemented for the MVP slice.
Native desktop OS notification adapters and richer pod-user product UX remain
post-MVP presentation layers.

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

## Related Capability Data

- `039-notifications-caps.edn`
