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

### Classifying a Store: Cache vs. Fact Store With Eviction

Before deciding "this is a cache, skip the convention", apply the diagnostic
test. Misclassification goes both ways: temporalizing a real cache is
over-engineering, but treating a fact store as a cache hides provenance and
loses audit.

> If you might ever want to ask "what did this store contain at time T?"
> or "where did this value come from?" — it is not a cache. It is a
> temporal store with an eviction policy, and it falls under this
> convention.

True caches are memoizations of pure functions: input determines value, no
provenance to record, "what was it yesterday" is not a meaningful question.
They stay outside this convention.

| Shape | Treatment |
| --- | --- |
| Memoization of a pure function (compiled validator, parsed config, derived key) | True cache. No temporal axis. Outside this convention. |
| Idempotency lookup, pagination cursor, short-lived dedup index | True cache. TTL only, no history. Outside this convention. |
| Record of a remote claim or signed observation | Fact store. Inside this convention. |
| Cached passport / capability presentation with issuer, signature, validity | Fact store. Inside this convention. |
| Observed TLS fingerprint, route advertisement, peer evidence | Fact store. Inside this convention. |
| Resolver TTL state carrying remote claim payload | Hybrid. Split: store the fact under this convention; derive "should refetch?" as a query against `valid_until` or last observation. |

Two TTL meanings collide on the hybrid case and are the root of recurring
bugs. On a true cache, TTL means "how long the memoization remains
trustable". On a fact store, retention means "how long we keep history for
audit". They are different axes. A single column named `expires_at` that
sometimes means one and sometimes the other is the signal that the table
needs to be split.

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

### Per-Store Performance Profile

Each store declares a performance profile that controls retention,
compaction aggressiveness, power policy for background workers, and
projection-verify cadence. The architectural shape (events + projection
+ as-of) is profile-independent; operational cost is not.

Three named profiles:

| Dimension | `minimal` | `balanced` | `full-audit` |
| --- | --- | --- | --- |
| Retention horizon | 30 days | 180 days | 5 years / unlimited |
| Compaction trigger | age 30d **or** disk pressure ≥ 80% | age 180d **or** disk pressure ≥ 90% | age 5y, opt-in only |
| Compaction strategy | aggressive — drop subsumed | standard — subsumed → `compacted_snapshot` | minimal — retraction merge only |
| `tx_time` granularity beyond horizon | day-level | hour-level | full preserved |
| Workers on battery | skip non-critical | throttle 10× | normal |
| Projection checksum verify | lazy (on suspect) | periodic 1h | per-startup + 1h |
| As-of horizon | retention horizon | retention horizon | unlimited |
| SQLite `busy_timeout` | 200 ms | 1 s | 5 s |
| Default lease duration | 30 s | 60 s | 300 s |

Defaults follow a neutral `DeviceFootprint` axis owned by the temporal
convention:

```text
Ephemeral   → minimal       # laptops, dynamic IP, suspendy
Personal    → balanced      # home node, shared user resource
Hosted      → balanced      # VPS infrastructure
Critical    → full-audit    # seed-directory, bootstrap anchor
```

The daemon's `DaemonDiscoveryDeploymentClass` is mapped into
`DeviceFootprint` at config load (`LaptopDynamic → Ephemeral`,
`HomeNode → Personal`, `VpsStable → Hosted`, `SeedDirectory → Critical`,
`BootstrapAnchor → Critical`). Operators may set `device_footprint`
directly in the performance config when they want storage profile
decoupled from deployment-class defaults.

Per-store override in documentation may be shown as TOML notation, but
Orbiplex Node's real layered configuration is JSON. The canonical Node
shape is:

```json
{
  "performance": {
    "device_footprint": "personal",
    "default_profile": "minimal",
    "per_store": {
      "notifications": {
        "profile": "minimal"
      },
      "agora-relay": {
        "profile": "full-audit",
        "operator_acknowledged_disk_cost": true,
        "operator_acknowledged_disk_cost_at": "2026-05-18T12:00:00Z"
      }
    }
  }
}
```

`operator_acknowledged_disk_cost = true` is **required** when a store
runs `full-audit` on a host whose `DeviceFootprint` default would otherwise
be `minimal` or `balanced` (i.e. `Ephemeral`, `Personal`, or `Hosted`).
Readiness gate refuses to bring the store up otherwise. The flag is recorded with its acknowledgement timestamp and
shown in operator UI; this is how a public service hosted on a personal
device avoids becoming an invisible disk eater.

`Critical` footprints do not require this acknowledgement because
`full-audit` is their expected default. They are still operator-visible:
Node emits a startup warning for any store whose resolved SQLite pragmas use
`synchronous = "FULL"`, because that setting improves durability but can make
writes fsync-bound even on critical infrastructure.

The acknowledgement covers **retention, not availability**. A `full-audit`
store on a personal device preserves history when the process runs; it
does not become reachable when the laptop is asleep, offline, or
suspended. Operators hosting a public service from a personal device must
understand this asymmetry before setting the flag — convention provides
an audit story, not an HA story. Intermittent reachability is the expected
operating mode of personal-device-hosted public services and is reported
in operator UI as informational, not as a fault.

Background workers read their store's profile and adapt power policy
accordingly. There is no separate "power policy" axis.

Compaction runs under two triggers, both required for every profile:
**planned** (age-based, on a background worker that respects the profile's
power policy — throttled or skipped on battery for low-profile stores)
and **emergency** (disk-pressure-based, runs synchronously when free
space drops below the profile's threshold, bypassing power policy because
the alternative is a failed write). The emergency trigger always emits an
operator notification so disk pressure is visible.

Profile change is **immediate by default**: when the profile changes,
the new retention horizon and compaction strategy apply to existing
history at the next compaction pass. This is a destructive operation
that requires `operator_acknowledged_compaction_on_change = true`
alongside the profile change; the config validator refuses to apply the
change otherwise. Convention chooses sharp cut over gradual transition
so that a store's stated profile is also its actual profile across the
whole history. Gradual transition remains available as an opt-in
(`profile_change_mode = "gradual"`) for rare cases where phased rollout
is wanted.

### Storage Layout Manifest

Each store writes a manifest at
`<data-dir>/storage/<store>/manifest.json`:

```json
{
  "store/id": "notifications",
  "schema/user-version": 4,
  "profile": "minimal",
  "operator-acknowledgements": { "disk-cost": null },
  "files": [
    "events.sqlite",
    "events.sqlite-wal",
    "events.sqlite-shm",
    "audit/"
  ],
  "size/bytes": 12345678,
  "as-of-tx-id": 42891
}
```

Operator UI reads manifests to render disk usage, profile, and backup
scope per store. A user wanting to back up their notifications copies
exactly the files listed in the manifest; restore is a directory-paste.
This makes "what is this file?" answerable without grep against source
code.

### Adopting the Profile Layer in a Node Store

A new Node store should adopt the operational profile layer in this order:

1. Choose one stable `StoreId` from the reserved vocabulary or add a new
   documented id. Current reserved ids are `notifications`,
   `artifact-delivery`, `inac`, `agora-relay`, `agora-projections`, and
   `messaging`.
2. Accept a `StoreProfileHandle` in the store configuration. Stores must not
   read daemon config or deployment-class values directly.
3. Apply `handle.sqlite_pragmas()` immediately after SQLite connect, before
   migrations or write-path work.
4. Use `should_compact(handle.resolved(), stats)` as the shared decision
   boundary, then run only domain-specific compaction that preserves replay
   invariants.
5. Write `<data-dir>/storage/<store>/manifest.json` after boot and after
   commits that materially change file layout, schema version, projection
   cursor, or storage size.
6. Let daemon/operator endpoints expose profile and manifest snapshots. The
   manifest remains a derived operator view, never recovery authority.

### Component Contract: One Schema, Profile-Aware Indices and Queries

A store using this convention declares its relationship in two layers,
not one. The component need not know about every dimension of the
profile — only what is described below.

**Layer 1 — store-level binary decision: temporal or not.**

A component states once, in its manifest:

```json
{ "store/id": "notifications", "temporal": true, "profile": "minimal", ... }
```

When `temporal: false`, the convention does not apply to the store at
all (pure cache, memoization, idempotency-only lookup). When
`temporal: true`, the store inherits `domain_transactions`,
`domain_events`, the projection table, replay tests, manifest, and the
profile resolver. There is no per-table opt-in inside one store — the
decision is binary at the store level.

**Layer 2 — within a temporal store, schema is one, indices and queries
are profile-aware.**

| Aspect | Strategy |
| --- | --- |
| Table schema (DDL, columns, constraints) | One schema per store-kind. Identical across profiles. |
| Indices | Profile-aware. Declared as data with `min_profile`. |
| Queries | Profile-aware. Three named SQL strings + match dispatcher. |
| Retention, compaction, power policy | Profile-driven (already in this convention). |
| Snapshot vs delta in events | Profile-aware. `minimal` may prefer snapshots; `full-audit` deltas. |

Rationale: schema is the domain contract — what this store *means*.
Profile is the operational dialect — how intensively we use it. Mixing
them produces two stores pretending to be one, makes profile change a
schema migration (blocking adoption), and turns replay-equivalence tests
into N × N combinations.

**Indices as data:**

```rust
pub struct IndexSpec {
    pub name: &'static str,
    pub columns: &'static [&'static str],
    pub min_profile: PerformanceProfile,
}

pub const NOTIFICATION_INDICES: &[IndexSpec] = &[
    IndexSpec { name: "events_subject_tx_idx",  columns: &["subject_id", "tx_id"], min_profile: Minimal },
    IndexSpec { name: "events_correlation_idx", columns: &["correlation_id"],      min_profile: Balanced },
    IndexSpec { name: "events_actor_idx",       columns: &["actor_id"],            min_profile: FullAudit },
];
```

Migration code filters by `min_profile <= current_profile` and runs
`CREATE INDEX IF NOT EXISTS`. Profile upgrade adds indices safely;
profile downgrade leaves them in place (drop is opt-in to avoid
surprising the next upgrade).

**Queries as data, dispatcher as code:**

```rust
mod notification_queries {
    pub const LIST_MINIMAL: &str = "SELECT ... FROM notification_current ORDER BY tx_id DESC LIMIT 50";
    pub const LIST_BALANCED: &str = LIST_MINIMAL;  // explicit equality, not duplication
    pub const LIST_FULL_AUDIT: &str = "
        SELECT c.*, COUNT(e.event_id) AS event_count
        FROM notification_current c
        LEFT JOIN notification_events e ON e.subject_id = c.subject_id
        GROUP BY c.subject_id ORDER BY c.tx_id DESC LIMIT 50";
}

fn list_notifications(profile: PerformanceProfile, ...) -> Result<...> {
    let sql = match profile {
        PerformanceProfile::Minimal   => notification_queries::LIST_MINIMAL,
        PerformanceProfile::Balanced  => notification_queries::LIST_BALANCED,
        PerformanceProfile::FullAudit => notification_queries::LIST_FULL_AUDIT,
    };
    // execute(sql, ...)
}
```

Three strings, one match. No trait machinery, no codegen. Most queries
in a typical store have a single variant — only the ones whose cost
truly differs across profiles (joins against events, aggregations over
`correlation_id`, audit views) carry three.

**Three pitfalls to avoid:**

1. **"Column only for full-audit"** — the column exists in the schema
   regardless of profile; under `minimal` it is simply `NULL`. Schema
   constant, contract clear, no profile-conditional DDL.
2. **Query result differs across profiles** — a query like
   `SELECT FROM events WHERE tx_time > NOW() - 1 year` returns empty under
   `minimal` (30-day retention) and full history under `full-audit`. This
   is correct behavior, not a bug. Operator UI must label such views as
   "history limited by retention profile".
3. **As-of query past compaction horizon** — as-of `T` reconstructs from
   event log. Beyond the compaction horizon, only snapshots remain. The
   API returns `Result<View, AsOfBeyondRetention>` — a typed error, not a
   silent partial result.

## Time Axes

The convention recognizes two semantic time axes:

1. **Transaction time**: when this local store recorded the fact. This is owned
   by the local store and is the default replay/as-of axis.
2. **Valid time**: the interval during which the fact claims to hold in the
   domain. Use `valid_from` and `valid_until` only when the domain needs them.

Other timestamps such as `observed_at`, `accepted_at`, `signed_at`,
`expires_at`, `started_at`, `finished_at`, and `retry_after` are domain or
operational fields. They are useful, but they are not generic temporal axes.

Wall-clock and monotonic clock have separate roles:

- **Wall-clock** (RFC3339 / `SystemTime`) stamps `tx_time` once at commit.
  Audit-shaped, human-readable, may drift on NTP correction. Acceptable
  for a stamp written once.
- **Monotonic clock** (`Instant`, or a runtime clock abstraction with
  equivalent semantics) drives operational time: lease deadlines, retry
  schedules, snooze "is it time yet?" checks, rate-limit windows. It is
  immune to NTP and timezone shifts; suspend/resume behavior is
  platform-dependent, so strict lease systems should detect resume by comparing
  wall-clock and monotonic deltas.

End-user devices suspend; a laptop closed for hours wakes with wall-clock
jumped. Lease and retry timers must not depend on wall-clock alone, or they can
mass-expire on resume.

Exception: comparing `valid_until` (a wall-clock value from a protocol
message) against current time uses wall-clock — the operand itself is
wall-clock-anchored.

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

The first implemented core pilot is Node's notification store:

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

The notification pilot now also adopts the first performance-profile layer:
Node resolves a daemon-owned `performance` config at boot, maps
`DaemonDiscoveryDeploymentClass` to the neutral `DeviceFootprint` axis unless
overridden, injects a read-only `StoreProfileHandle` into notification-store,
applies profile-derived SQLite pragmas, writes
`storage/notifications/manifest.json`, exposes
`GET /v1/operator/storage/profiles`, and accepts explicit per-store profile
changes through `POST /v1/operator/storage/profile-change/{store_id}` by
writing a restart-required operator config fragment.

The adopted slice intentionally stops at the safe shared boundary:
`temporal-profile` owns dimensions, validation, power policy, and compaction
decision calculation; `bounded-work-runtime` can run profiled passes with a
`DevicePowerSource`; `device-power` currently provides the portable
`AlwaysAC` fallback; and `storage-manifest` owns atomic manifest writes.
Destructive notification event compaction, emergency disk-pressure compaction
that emits operator notifications, and additional real device-power detectors
remain future store-specific/runtime layers. Until those are implemented,
notification-store should be described as "temporal event-log/projection plus
performance-profile wiring done", not as "all compaction policy fully
operational".

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
| Fact store mislabelled as cache (no audit, no provenance) | Apply the cache-vs-fact-store diagnostic at design time; if "what did this contain at time T?" is ever a useful question, the table is in scope of this convention. |
| Public service on personal device runs disk to zero | `full-audit` profile on a host whose `DeviceFootprint` would default to `minimal`/`balanced` requires explicit `operator_acknowledged_disk_cost = true`; readiness gate refuses startup otherwise; operator UI reports disk usage per `full-audit` store. |
| Wall-clock skew after suspend mass-expires leases and retries | Use monotonic clock for all operational timers; on resume past a threshold (~5 minutes), run projection checksum verify and lease audit before resuming normal work. |
| Profile change silently destroys history | Profile change is immediate by default; config validator refuses the change unless `operator_acknowledged_compaction_on_change = true` accompanies it. Gradual transition available as explicit opt-in. |
| Cross-store saga fragments after retention expiry | Accepted as expected outcome. Cross-store `correlation_id` queries return partial sagas with explicit gaps; UI labels them "partial — retention expired in: <store list>". No global minimum retention across joined stores. |
| Schema diverges per profile, making migration hard | One schema per store-kind, identical across profiles. Profile drives indices and queries only. Profile upgrade adds indices via `CREATE INDEX IF NOT EXISTS`; profile change is never a schema migration. |
| As-of query past compaction horizon returns silent partial result | As-of queries return `Result<View, AsOfBeyondRetention>`. Beyond the horizon, only snapshots remain; the API surfaces a typed error rather than fabricating a partial view. |

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
