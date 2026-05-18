# Temporal Storage Convention

The Temporal Storage Convention is a solution-level pattern for SQLite-backed
Node stores that need auditability, replay, non-blocking work, and current read
models without turning every component into a database framework.

Status: `accepted`

Date: `2026-05-18`

Based on: `doc/project/40-proposals/062-temporal-storage-convention.md`

## Executive Summary

Use temporal storage when a local store represents durable state transitions,
accepted facts, queue status, or privacy-sensitive workflows. The convention is
small:

```text
append transaction/event facts
  -> derive current projection rows
  -> serve API/UI from projection
  -> verify replay equivalence in tests
```

The event log is the recovery source of truth. The current table is a projection
for query speed and UI ergonomics. JSONL, when present, is a diagnostic/export
mirror unless a specific solution explicitly says otherwise.

This convention does not remove SQLite's single-writer property. It reduces the
amount of semantic work that must happen while code owns a write transaction:
network calls, middleware execution, signature verification, projection replay,
and operator UI transitions should not be hidden inside long critical sections.

## Context and Problem Statement

Several Node-local stores start as one mutable table that mixes three concerns:

1. durable fact recording;
2. current read-model state;
3. operational attempt/status tracking.

That works at small scale but creates ambiguous recovery rules. If a process
crashes between external work and a row update, it can be unclear whether the
operation was accepted, attempted, failed, or merely observed. Temporal storage
makes the state transition explicit before projecting it.

The pattern is especially useful for:

- notification queues;
- messaging outbox attempts;
- artifact delivery admissions and deliveries;
- Seed Directory accepted facts;
- Agora replay-fed projections;
- Whisper intake stages;
- local operator/audit workflows.

Do not apply it mechanically to short-lived caches, idempotency lookup tables,
opaque cursor tables, or stores that are already append-only unless there is a
concrete replay or audit need.

## Proposed Model / Decision

A temporal store has three conceptual parts.

### Transactions

A transaction row records local transaction time and shared metadata for one
atomic write:

```sql
CREATE TABLE domain_transactions (
  tx_id INTEGER PRIMARY KEY,
  tx_time TEXT NOT NULL,
  actor_kind TEXT NOT NULL,
  actor_id TEXT,
  causation_tx_id INTEGER REFERENCES domain_transactions(tx_id),
  correlation_id TEXT,
  signature_ref TEXT,
  comment TEXT
);
```

Use `tx_id` as the local, monotonic replay cursor. Use `tx_time` for human
inspection and coarse ordering, not as a replacement for the replay cursor.

`causation_tx_id` and `correlation_id` are different:

- `causation_tx_id` is the prior transaction that caused this one;
- `correlation_id` groups many transactions belonging to one saga/workflow.

Cross-store sagas are reconstructed by joining on `correlation_id`. There is no
global transaction registry in this convention.

### Events

An event row records an assertion, retraction, decision, attempt, or projection
fact for one subject:

```sql
CREATE TABLE domain_events (
  event_id TEXT PRIMARY KEY,
  tx_id INTEGER NOT NULL REFERENCES domain_transactions(tx_id),
  subject_id TEXT NOT NULL,
  event_kind TEXT NOT NULL,
  attribute TEXT NOT NULL,
  value_json TEXT NOT NULL,
  target_event_id TEXT REFERENCES domain_events(event_id),
  valid_from TEXT,
  valid_until TEXT,
  idempotency_key TEXT
);

CREATE UNIQUE INDEX domain_events_idempotency_idx
  ON domain_events(idempotency_key)
  WHERE idempotency_key IS NOT NULL;
```

Use `idempotency_key` as the default logical request deduplication mechanism.
Do not invent mandatory content digests unless the domain needs content-level
identity or abuse resistance.

Events may store either small typed deltas or redacted/sealed projection
snapshots. A snapshot is acceptable when it makes replay simpler and does not
expose plaintext that the projection is not allowed to expose.

For privacy-sensitive stores, the event log may carry sealed ciphertext if the
current projection carries the same sealed payload. The invariant is that event
rows must not leak plaintext beyond the store's declared local security boundary.

### Current Projection

A projection table is a read model derived from events:

```sql
CREATE TABLE domain_current (
  subject_id TEXT PRIMARY KEY,
  current_state TEXT NOT NULL,
  as_of_tx_id INTEGER NOT NULL REFERENCES domain_transactions(tx_id),
  version INTEGER NOT NULL
);
```

Projection rows carry `as_of_tx_id`, not `updated_at`. `updated_at` is too easy
to confuse with transaction time, valid time, observed time, or UI refresh time;
it also makes deterministic replay harder. If the domain needs those times, name
them explicitly as domain fields.

`version` remains useful as an optimistic-concurrency token for UI mutations,
but it is projection state derived from event application, not an independent
source of truth.

## Time Axes

The convention recognizes two semantic time axes:

1. **Transaction time**: when this local store recorded the fact. This is owned
   by the local store and is the default replay/as-of axis.
2. **Valid time**: the interval during which the fact claims to hold in the
   domain. Use `valid_from` and `valid_until` only when the domain needs them.

Other timestamps such as `observed_at`, `accepted_at`, `signed_at`,
`expires_at`, `started_at`, `finished_at`, and `retry_after` are domain or
operational fields. They are useful, but they are not generic temporal axes.

## Write Path Contract

Write paths should be short and explicit:

```text
begin transaction
  -> insert domain_transactions row
  -> insert one or more domain_events rows
  -> update current projection rows as a pure consequence
commit
append optional JSONL/export mirror after commit
emit optional SSE/UI ping after commit
```

Network calls, Matrix/WSS sends, Memarium writes, model calls, middleware calls,
and expensive verification should not happen while holding the SQLite write
transaction. If such work is needed, append an intent/attempt event first, do the
work outside the transaction, then append a result/decision event.

## Replay and Test Contract

A store using this convention is not done until it has replay tests:

- fresh schema creates transactions, events, and projection tables;
- migration bootstraps existing current rows into replayable events;
- replay from events equals the live projection row-by-row for representative
  state transitions;
- `as_of` replay before and after a transition returns the expected state;
- delete/retraction removes the subject from the current projection while
  preserving event history;
- future `user_version` fails closed;
- privacy tests prove event rows do not contain forbidden plaintext.

A test-only helper such as `projection_snapshot_from_events()` is enough for the
first pilot. Do not expose new daemon APIs just to prove replay unless an
operator-facing historical query is already part of the product contract.

## Migration Pattern

For an existing mutable table:

1. Add transaction and event tables.
2. Add nullable `as_of_tx_id` to the current projection table.
3. Create synthetic bootstrap transaction/events for existing rows.
4. Set `as_of_tx_id` for every current row.
5. From this point forward, every mutation appends events and updates projection
   in the same SQLite transaction.
6. Keep old JSONL audit as a mirror until at least one more store validates the
   pattern.

Batch bootstrap work in bounded transactions. A batch size around 100 rows is a
reasonable default for local SQLite profiles: it avoids one commit per row while
keeping migration locks and rollback scope small.

## Current Adoption

The first implemented pilot is Node's notification store:

```text
notification_transactions
notification_events
notification_queue.as_of_tx_id
```

`notification_events` is now the recovery source for notification state, while
`notification_queue` remains the current API/UI projection. For User/PodUser
notifications, event snapshots may include sealed nonce/ciphertext so replay can
rebuild the projection; plaintext title/body/actions and transient `body/input`
must not be present in event rows.

The next recommended pilot is the Messaging outbox status/attempt store. Extract
a shared helper crate only after at least two stores converge on the same shape.

## Trade-offs

Benefits:

- deterministic replay;
- clearer crash recovery;
- auditability without relying on mutable current rows;
- shorter semantic critical sections;
- simpler `as_of` tests and historical debugging;
- a common storage vocabulary across Node components.

Costs:

- more tables and migrations;
- projection code must be tested, not assumed;
- event payload privacy must be reviewed explicitly;
- poorly designed events can become opaque snapshots with weak domain meaning;
- SQLite still serializes writers, so this is not a physical concurrency cure.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| --- | --- |
| Projection drifts from events | Replay-equivalence tests and `as_of_tx_id` on projection rows. |
| Event log leaks private payloads | Store redacted/sealed snapshots only; add string-search privacy tests for forbidden plaintext. |
| Long migration locks local profile | Batch bootstrap rows in bounded transactions. |
| `updated_at` becomes a hidden temporal axis | Do not use `updated_at` on projections; use `as_of_tx_id` and explicit domain timestamps. |
| JSONL and SQLite disagree | Treat SQLite event log as source of truth; JSONL is a post-commit mirror. |
| Cross-store saga is expected to be atomic | Use `correlation_id` for reconstruction; this convention does not provide distributed transactions. |
| Duplicate logical requests create duplicate events | Use `idempotency_key` uniqueness at the event boundary. |

## Open Questions

1. Which second store should be migrated first: Messaging outbox attempts or
   Artifact Delivery delivery/admission events?
2. After two pilots, is a small shared helper crate justified, or are local
   store-specific helpers still clearer?
3. Which operator-facing historical queries should become real APIs rather than
   test-only replay helpers?

## Next Actions

1. Use this solution as the default checklist when designing new SQLite-backed
   operational stores.
2. Complete the second pilot in Messaging outbox status and attempts.
3. Add replay-equivalence tests for that second pilot.
4. Reassess a shared temporal helper crate after the second pilot, not before.
