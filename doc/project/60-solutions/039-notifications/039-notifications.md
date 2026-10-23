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

Responsibility maintenance operator alerts are a planned additional consumer,
not qualified delivery in the current lifecycle checkpoint. Its current tracing
diagnostic does not prove that an operator received an alert. The next slice must
reuse this queue with verified recipient binding, bounded durable domain outbox,
deduplication, privacy-minimal events and separate queued/delivered/opened/ack states.
Acknowledgment grants no repair or participant authority. See
`node:docs/development/RESPONSIBILITY-SAFE-MAINTENANCE-SHADOW-V3-PLAN-2026-10-19.md`.

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

### Planned Assessment Exposure Rendering

Status: `planned`, tracked once in
[P057-014](../../40-proposals/057-user-and-operator-notifications.md#assessment-exposure-at-rendering-boundaries),
using [P026's viewer-bound projection](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#viewer-bound-api-projection).
Render assessment notices from the current admitted recipient view, not a sender's
raw verdict, title or claimed urgency. Reuse registered renderers/actions, caller
binding and sealed storage; an unavailable view never falls back to peer content.
Recheck deferred delivery and reads, including previews and future OS delivery.

Hidden peer activity must not generate per-assessment queue rows, unread-count
changes, SSE pings or version churn visible to that recipient. Existing minimal
SSE payloads do not prove this stronger property. Preserve ordinary content
arrival and admitted urgent protection as separate lanes; a protective kind cannot
smuggle ratings or popularity aggregates. Retain refusal, restart, stale-queue and
two-viewer fixtures in the common exposure acceptance. No duplicate notification
transport or UI-only redaction is needed.

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

## Matrix recovery attention (P035-013, 2026-10-23)

The accepted additional consumer projects committed Agora recovery attention into
this queue through a host-owned, durable, idempotent source adapter. It preserves
recipient policy, metadata-only SSE, current authority and notification/task CAS.
Acknowledgment does not retry history. Only ordinary retry is batchable; explicit
gap acceptance and implausible-delay override remain single reasoned actions.
Focused qualification passed on 2026-10-23 at clean Node `885a78fd` / Orbidocs
`b16312f6`: 12 Synapse cases and five SQLite controls (four runtime, one separate
conformance), with actual queue/API/private UI, reply-loss/crash, restart and
carrier/S039 replay. The S039 guarded representation remains private; the new
redacted recovery control page separately supports no-JS preview/confirmation.
Actions preserve the originally inspected task CAS and notification version and
recheck current authority; they never replace stale revisions with fresh ones.
Identical source/legacy, extracted and fresh dual-store qualification is recorded
in `node:docs/evidence/matrix-opaque-envelope/2026-10-23-recovery-attention/README.md`.
This closes P035-013, not OS delivery, generic notification readiness or P035-014.

## Optional evidence-supervision consumer (P035-014)

The opt-in module requests notifications through the ordinary `notification.create`
and narrowly granted NotificationAllow policy. It owns a topology/freshness thread
and separate store/bundle integrity threads, stable incidents/generations and a
transactional outbox. Reading or handling an item never repairs or retires evidence.
S039 acceptance precedes outbox confirmation. Missing daemon/package availability
means no off-session alert; status/restart expose stale observations. This accepted
consumer is focused-runtime-qualified on 2026-10-23 through eleven real background/
S020/S039/UI cases, crash-after-acceptance idempotency and projection replay. See
`node:docs/evidence/matrix-opaque-envelope/2026-10-23-replica-supervision/README.md`. It
installs no permanent OS watchdog and does not change generic S039 readiness.


Independent signed instances need no legacy module HTTP credential to consume
`notification.create` through their authenticated channel. Before dispatch the
host rechecks the exact current admitted registration and delegates to the same
schema-gated notification owner. NotificationAllow remains mandatory; neither a
claimed sender nor an allow rule authenticates an unregistered module. No new
host capability, evidence-store knowledge or repair authority follows.
