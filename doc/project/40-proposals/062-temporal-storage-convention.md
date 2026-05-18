# Proposal 062: Temporal Storage Convention

Status: Accepted

Date: 2026-05-18

Based on: implementation schema review across Node SQLite stores.

Promoted to: `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`

This proposal records the rationale and decision history. The canonical
implementation guidance now lives in the promoted solution document.

## Executive Summary

Orbiplex should adopt a small temporal storage convention for database-backed
Node components that currently mutate operational or domain state in place.
The convention is not a new database framework. It is a repeatable pattern:
append durable facts or events, then maintain rebuildable current projections
for fast reads.

This helps avoid long critical sections and semantic blocking. A writer can
persist a small intent, attempt, decision, or accepted fact quickly; background
workers and projectors can process the heavier work later. SQLite still has one
writer, so this proposal does not remove physical write serialization. It
reduces the need to hold locks while network calls, middleware execution,
signature verification, replay, or UI state transitions are in progress.

The recommended rule is selective adoption:

- use temporal event/history tables for queues, status machines, accepted
  public/federated facts, and privacy-sensitive workflows;
- keep current projection tables for query surfaces and UI;
- do not temporalize short-lived caches, idempotency lookups, cursors, or stores
  that are already append-only unless there is a concrete audit or replay need.

## Context and Problem Statement

Several Node SQLite stores combine three responsibilities in one mutable table:

1. durable fact recording,
2. current read-model state,
3. operational status tracking.

That shape is simple at first, but it can force code into long or fragile
critical sections:

```text
lock / transaction
  -> read current row
  -> decide next step
  -> perform external work or expensive validation
  -> update row
```

In a distributed node, the external work may include HTTP/WSS/Matrix transport,
capability verification, replay, middleware calls, sealing, Memarium writes, or
operator-facing transitions. Holding semantic ownership of a row across that
work creates retry races, recovery ambiguity, and weak audit trails.

A temporal storage convention separates the write path from the read path:

```text
short transaction: append intent / accepted fact / attempt
work outside the database lock
short transaction: append result / decision
project current state from events
```

The current projection must be derived from the event log, not co-authored
with it. "Derived" means: every value in the projection is computable from
the events alone, and projection rebuild from the event log is a tested
property of the component. This is the load-bearing decision of this
proposal — it converts the projection from a second source of truth into a
performance cache.

The model has two complementary readings:

- **Information model** (what is true): the event log is the database.
  A value at time T is the set of all (assert) events with `tx_time <= T`
  minus all subsequent (retract) events referring to them, filtered by
  `valid_from <= T < valid_until` where validity matters.
- **Operational model** (how to query fast): the current projection is the
  precomputed view of "now". UI and APIs read from the projection.
  Historical and what-if queries replay events on demand.

This split is what makes the rest of the proposal coherent.

## Proposed Model / Decision

Adopt a project-wide convention for SQLite-backed state that distinguishes two
semantic time axes plus ordinary operational timestamps.

### Time Axes

Two axes carry semantic weight; everything else is a domain attribute that
happens to be timestamped.

1. **Transaction time** — represented by monotonic local `tx_id` plus
   human-readable `tx_time`. `tx_id` is the local replay/as-of cursor owned
   by the store. `tx_time` records when *this* node recorded the fact and is
   for audit and inspection, not for deterministic replay ordering.
2. **Valid time** — `valid_from` and `valid_until`. The interval during which
   the world claims this fact holds. Independent of when the node learned of
   it. Required only for domains where a fact's truth has a start and end
   (credentials, bindings, scoped trust, route advertisements).

Everything else is a domain attribute. Treat `recorded_at`, `observed_at`,
`accepted_at`, `occurred_at`, `authored_at`, `published_at`, `revoked_at`,
`signed_at`, `expires_at`, `started_at`, `finished_at`, `retry_after`, and
`lease_until` as *fields on facts of a specific kind*, not as a generic time
axis vocabulary. They are real and useful — but they are protocol or
operational metadata, not bitemporal primitives.

This matters because confusing axes is the most expensive mistake in temporal
systems. If `observed_at` is sometimes "when local node observed remote
fact" and sometimes "domain time", queries that look the same return
different answers depending on which producer wrote the row. Pinning the
two-axis bitemporal model up front prevents that drift.

Operational rule: every event row carries `tx_time`. Validity-bearing facts
additionally carry `valid_from` / `valid_until`. Other timestamps are
schema-level attributes inside the payload or hoisted as typed columns when
queryable.

`updated_at` is **not** a permitted column on current projections. It carries
no information that `as_of_tx` does not carry better; it invites use as a
substitute for one of the real axes; and it makes projection rebuild
non-deterministic (replay must reproduce wall-clock). Projections carry
`as_of_tx_id` instead — the transaction identifier whose application
produced this projection row. Two replays of the same event log produce
identical `as_of_tx_id` values.

#### Wall-Clock vs. Monotonic Clock

Two different clock sources, two different uses, do not conflate:

- **Wall-clock** (`std::time::SystemTime` / RFC3339) — used for `tx_time`
  only. Stamped once at commit. Auditable, human-inspectable, survives
  process restart. Subject to NTP adjustment and timezone changes; that is
  acceptable for an audit field stamped once.
- **Monotonic** (`std::time::Instant`, or a runtime clock abstraction with
  equivalent semantics) — used for *all operational time*: lease deadlines,
  retry schedules, rate-limit windows, snooze expiry comparisons against
  "is it time yet?", scheduler tick. It does not jump on NTP correction or
  timezone change. Suspend/resume behavior is platform-dependent, so runtimes
  that need strict lease semantics should detect resume by comparing wall-clock
  and monotonic deltas.

End-user devices suspend. A laptop closed for 8 hours wakes with wall-clock
shifted. Lease-timing or retry-timing based purely on wall-clock may
mass-expire on resume. Convention enforces the clock split rather than leaving
each store to rediscover the bug.

Single explicit exception: comparing `valid_until` (wall-clock fact from a
protocol message) against current time uses wall-clock — because the value
itself is wall-clock-anchored. A monotonic comparison would be type-wrong.

### Storage Shape

The shape has three tables, not two. Hoist the transaction into a first-class
entity so causality, signatures, operator identity, and replay determinism
all hang off one place.

```sql
CREATE TABLE domain_transactions (
  tx_id INTEGER PRIMARY KEY,                  -- monotonic per store
  tx_time TEXT NOT NULL,                      -- RFC3339; assigned at commit
  actor_kind TEXT NOT NULL,                   -- 'operator' | 'component' | 'daemon' | 'remote'
  actor_id TEXT,                              -- binding id, component id, peer node id
  causation_tx_id INTEGER REFERENCES domain_transactions(tx_id),
                                                -- prior tx that caused this one
  correlation_id TEXT,                        -- saga / workflow id, cross-cutting
  signature_ref TEXT,                         -- reference to signed envelope, when applicable
  comment TEXT                                -- operator-visible "why"
);

CREATE TABLE domain_events (
  event_id TEXT PRIMARY KEY,
  tx_id INTEGER NOT NULL REFERENCES domain_transactions(tx_id),
  subject_id TEXT NOT NULL,
  event_kind TEXT NOT NULL,                   -- 'assert' | 'retract' | domain-specific
  attribute TEXT NOT NULL,                    -- which fact about the subject changes
  value_json TEXT NOT NULL,                   -- the asserted/retracted value
  target_event_id TEXT REFERENCES domain_events(event_id),
                                                -- required for retractions/excisions
  valid_from TEXT,                            -- when validity-bearing
  valid_until TEXT,
  idempotency_key TEXT
);

CREATE UNIQUE INDEX domain_events_idempotency_idx
  ON domain_events(idempotency_key)
  WHERE idempotency_key IS NOT NULL;

CREATE INDEX domain_events_subject_tx_idx
  ON domain_events(subject_id, tx_id DESC);

CREATE INDEX domain_events_subject_validity_idx
  ON domain_events(subject_id, valid_from DESC, valid_until);

CREATE TABLE domain_current (
  subject_id TEXT PRIMARY KEY,
  current_state TEXT NOT NULL,
  as_of_tx_id INTEGER NOT NULL REFERENCES domain_transactions(tx_id),
  version INTEGER NOT NULL                    -- optimistic-concurrency cursor for UI mutations
);
```

Why the attribute-shaped `(attribute, value_json)` instead of only opaque
`payload_json`: many projections can dispatch per attribute without parsing
every payload schema. A `revoke` event can set `attribute = 'revoked'`,
`value_json = { "by": "...", "reason": "..." }`. A `rename` can set
`attribute = 'name'`. The projection layer becomes a fold-over-attributes,
which is shorter, easier to test, and common across domains.

This is a convention, not a ban on typed domain payloads. If a domain event is
an invariant-bearing composite that must be accepted or rejected as one unit,
the event may store a typed payload envelope in `value_json` and use an
attribute such as `attribute = 'domain-event'` or a domain-specific attribute
name. Domain event kinds with multiple independent attribute changes can be
modelled as multiple rows in one transaction (`tx_id` joins them). Domain event
kinds with one composite invariant should remain one row.

The contract is the separation, not the column names. What is non-negotiable:

- transactions are entities; events reference transactions; events do not
  carry actor/causation metadata directly (de-duplicates the columns and
  prevents inconsistent metadata across events of one tx);
- the projection carries `as_of_tx_id`, not `updated_at`;
- assertion and retraction are different `event_kind` values, not column
  flips on a current row;
- `idempotency_key` enforces de-dup of the same logical request at the event
  boundary; content-level de-duplication is a separate domain decision and
  should use explicit digests or uniqueness constraints when needed.

#### causation_id vs correlation_id

These are different relations and easy to confuse:

- `causation_tx_id` is a **DAG edge** — "the prior transaction that caused
  this one". Used to walk causal history. Single parent, on the transaction.
- `correlation_id` is a **process tag** — "all transactions belonging to
  this saga/workflow". Used to find all activity tied to one user intent,
  one delivery, one onboarding. Many transactions share it; non-causal.

Conflating them produces queries that are correct in the happy path and
wrong under retry/replay.

#### Assertions, Retractions, and Revocations

Domain mutations are expressed as new events, never as updates to existing
rows. Three patterns cover almost every case:

- **Assert** a new fact: append an event with `event_kind = 'assert'`.
- **Retract** an earlier assertion (it never should have happened — bug,
  corruption, parser drift): append `event_kind = 'retract'` with
  `target_event_id` referencing the original. The projection ignores
  retracted facts; the original event row remains for audit.
- **Revoke** at a domain level (the fact was legitimately true but is no
  longer): append a domain event like `event_kind = 'revoked'` with its own
  `valid_from`. The projection treats the original fact as bounded by the
  revocation time. Audit shows both facts.

Retraction and revocation are distinct: retraction is an epistemic
correction ("we were wrong"), revocation is a temporal change ("it was
true, now it isn't"). Operator UIs should expose both as separate verbs.

### Operational Status Shape

For queues, delivery attempts, deferred work, and transport retries, prefer an
attempt/event table over repeated in-place mutation:

```sql
CREATE TABLE operation_attempts (
  attempt_id TEXT PRIMARY KEY,
  operation_id TEXT NOT NULL,
  attempt_no INTEGER NOT NULL,
  started_at TEXT NOT NULL,
  finished_at TEXT,
  status TEXT NOT NULL,
  retry_after TEXT,
  failure_class TEXT,
  diagnostic_json TEXT,
  UNIQUE(operation_id, attempt_no)
);
```

The current operation row may still keep `status`, `next_due_at`, or
`last_error` as a projection. The attempts are the durable explanation.

### Leases Instead of Long Locks

Background workers should not hold database locks while doing external work. If
exclusive processing is needed, use a short lease:

```text
lease_owner
lease_until
attempt_no
```

The worker claims work in one transaction, performs the external work outside the
transaction, and appends the result in another transaction. Expired leases are
recoverable by another worker.

### As-Of Queries as a First-Class Primitive

Once events reference transactions, "what did this store believe at time T?"
is just a query against `domain_events` filtered by `tx_id <=
tx_of(T)` and projected. This should be exposed as a runtime primitive in
each component's store API, not as an ad-hoc replay procedure for tests
only. Concrete uses:

- **operator forensics**: "show me the Contact Catalog as it was when the
  delivery decision was made";
- **debugging**: "show me Seed Directory's view of node-X advertisements at
  the moment we dialed";
- **undo UX**: preview "as the relevant subject/correlation looked five
  minutes ago" and then append explicit compensating or retracting events for
  that bounded scope; never silently roll back unrelated transactions that
  happened after the same wall-clock time;
- **proof of decision**: "this delivery was sent under this trust state",
  reconstructible offline from event log + transaction signatures.

The replay equivalence tests proposed for Seed Directory are a special case
of this primitive. Component authors should derive both from the same
underlying store API, not write two replay codepaths.

### Speculation Without Persistence

A useful sibling to as-of queries: apply a candidate transaction *without
committing*, then query the resulting projection. Use cases include "what
would this policy change do to currently-active routes?" and "what would
revoking this capability passport invalidate?". This is `Datomic.with`-style
speculation, implemented locally as: load current state into an in-memory
overlay, apply the candidate event(s), project, return — the persisted store
is untouched. Useful for operator preview/confirm flows on destructive
operations.

### Performance Profiles

Orbiplex Node runs on a spectrum of hardware: end-user laptops on battery,
home servers, VPSes, dedicated seed-directory boxes. The temporal
architecture is the same everywhere; *how much history we keep, how
aggressively we compact, how background work respects power* differs per
store. This is captured as a **per-store performance profile**, not as a
node-wide setting — because a user may run a public service (e.g., a
shared Agora relay) on the same laptop that hosts their private
notifications, and the two stores have legitimately different policies.

Three named profiles cover the practical range:

| Dimension | `minimal` | `balanced` | `full-audit` |
| --- | --- | --- | --- |
| Retention horizon (events) | 30 days | 180 days | 5 years / unlimited |
| Compaction trigger | age 30d **or** disk pressure ≥ 80% | age 180d **or** disk pressure ≥ 90% | age 5y, opt-in only |
| Compaction strategy | aggressive — subsumed events drop | standard — subsumed → `compacted_snapshot` | minimal — retraction merge only |
| `tx_time` granularity beyond horizon | day-level | hour-level | full preserved |
| Background workers on battery | skip non-critical | throttle 10× | normal |
| Projection checksum verify | lazy (on suspect) | periodic 1h | per-startup + 1h |
| As-of query horizon | retention horizon | retention horizon | unlimited replay |
| JSONL audit mirror | optional | yes | yes + replication hook |
| SQLite `busy_timeout` | 200 ms | 1 s | 5 s |
| Default lease duration | 30 s | 60 s | 300 s |

Default profile follows from a neutral `DeviceFootprint` axis owned by the
temporal convention itself:

```text
Ephemeral   → default_profile = "minimal"      # laptops, dynamic IP, suspendy
Personal    → default_profile = "balanced"     # home node, shared user resource
Hosted      → default_profile = "balanced"     # VPS infrastructure, no suspend
Critical    → default_profile = "full-audit"   # seed-directory, bootstrap anchor
```

`DeviceFootprint` is a pure semantic axis — "what shape of host is this
store running on?" — with no knowledge of dialer policy, discovery, or
network role. Daemon converts its own `DaemonDiscoveryDeploymentClass`
into a `DeviceFootprint` at config load (`LaptopDynamic → Ephemeral`,
`HomeNode → Personal`, `VpsStable → Hosted`, `SeedDirectory → Critical`,
`BootstrapAnchor → Critical`); operators may also override
`device_footprint` directly in the performance config when they want to
decouple storage profile from deployment-class defaults. This keeps the
temporal convention zero-dependency on daemon-level concepts.

Per-store override is always available:

```toml
[performance]
default_profile = "minimal"

[stores.notifications]
profile = "minimal"

[stores.agora_relay]
profile = "full-audit"
operator_acknowledged_disk_cost = true
```

The `operator_acknowledged_disk_cost = true` flag is **required** when a
store runs `full-audit` on a host whose `DeviceFootprint` default would
otherwise be `minimal` or `balanced` (i.e. `Ephemeral`, `Personal`, or
`Hosted`). This is not bureaucracy. It is the only way to keep "hidden
disk eater" failures from happening: the operator explicitly accepts that
this one store will grow without the device-class ceiling, and the
readiness gate refuses to bring the store up if the flag is absent on a
footprint mismatch. Operator UI lists all `full-audit` stores and the
date of acknowledgement.

The acknowledgement covers retention, not availability. Hosting a public
service from a `full-audit` store on a personal device guarantees that
*when the process runs*, history is preserved according to the profile.
It does not guarantee that the service is reachable when the laptop is
asleep, offline, mid-suspend, or has no network. This asymmetry must be
understood before setting the flag — public-service availability on
personal devices is best-effort and conditional on the host being awake
and connected. Convention does not provide an HA story; it provides an
audit story. Operator UI surfaces "this `full-audit` store has been
unreachable for X hours" as informational, not as a fault, because for a
personal device intermittent reachability is the expected operating mode.

Power-state awareness derives from the profile rather than being a separate
declaration. Each background worker reads its store's profile and adapts:
`minimal` → skip non-critical on battery, `balanced` → throttle 10×,
`full-audit` → normal. There is no separate "power policy" axis to
maintain.

#### Cross-Store Correlation Across Profiles

**Decision: accept partial sagas. No cross-store retention coordination.**

A saga spanning stores with different retention windows
(`notifications: minimal` ↔ `outbox: balanced`) will leave fragments
behind as the shorter-retention store compacts. Cross-store
`correlation_id` queries return *partial sagas* with explicit gaps. This
is the expected outcome of per-store policy, not a bug to fix. Operator UI
labels such results as "partial — retention expired in: <store list>".
The store that still has data is authoritative for its part; the missing
part is missing, not reconstructed.

Trying to enforce a global minimum retention across joined stores would
collapse the per-store flexibility that motivated the profile model and
re-introduce hidden disk costs through the back door (the shortest-lived
store would be forced to keep history just because some other store
referenced its `correlation_id`). Convention pays the cost on the saga
side, not the storage side.

#### Profile Change Mid-Life

Changing a store's profile (e.g., `balanced` → `minimal`) is a configuration
change with immediate consequences for existing history. The default is the
sharp cut:

- **Immediate** (default): on profile change, the new retention horizon and
  compaction policy apply to existing history at the next compaction pass.
  Events beyond the new horizon are compacted or dropped according to the
  new profile's strategy. This is a *destructive operation on history*
  and requires explicit operator acknowledgement at config-change time —
  the operator UI / config validator refuses to apply the change until
  `operator_acknowledged_compaction_on_change = true` accompanies it,
  framed as "I accept that history beyond the new horizon will be
  compacted irreversibly".

Two reasons immediate is the default rather than gradual: profile changes
are rare and intentional (not background tuning), and a "gradual" model
leaves the store in a hybrid state where audit semantics differ across
time ranges — confusing for forensics. A sharp cut keeps the meaning of
"this store's profile is X" stable: as soon as it says X, everything in
the store conforms to X.

Gradual transition remains available as an explicit opt-in
(`profile_change_mode = "gradual"` alongside the profile change) for the
rare case where operators want to phase a change without touching old
history.

### Compaction as MVP

The original draft listed compaction as a future concern. On end-user
devices it is not — event logs that grow forever fill user disks
invisibly. Compaction must be available from the first migration of any
store under this convention.

Two trigger types, both required:

- **Planned**: age-based, runs on a background worker, respects the
  profile's power policy (skip/throttle on battery for low-profile stores).
  This is the normal path; users never see it.
- **Emergency**: disk-pressure-based, runs synchronously when free space
  drops below the threshold defined by the profile. Bypasses power policy
  because the alternative is a failed write. Always emits an operator
  notification so the user sees that the device is under disk pressure.

The compaction algorithm itself is unchanged: events fully subsumed by a
later assertion on the same `(subject_id, attribute)` pair, beyond the
profile's retention horizon, are replaced by a `compacted_snapshot` event
(`balanced`/`full-audit`) or removed (`minimal`). Excision remains a
separate, separately-authorized mechanism; compaction and excision never
run together.

## Recommended Adoption Targets

### Seed Directory

Seed Directory is a strong candidate because it is both a policy surface and a
federated discovery projection.

Recommended direction:

- append accepted facts for node advertisements, capability registrations,
  node-operator bindings, routing-subject bindings, and revocations;
- maintain current projection tables for the stable Seed Directory HTTP API;
- make replay equivalence testable:

```text
SeedDirectoryHTTP(ProjectionFromSqliteCurrent)
==
SeedDirectoryHTTP(ProjectionFromAcceptedFactsReplay)
```

The current tables can remain query-optimized. The accepted facts become the
local source of replay and audit.

### Messaging Outbox

The outbox currently has mutable state such as delivery state, attempt count,
last error, and next attempt time. This should become:

- `outbox_events` for submitted, routed, attempted, deferred, failed, and sent;
- `outbox_attempts` for transport attempts;
- existing outbox row as current projection.

This allows transport work to happen outside the database lock and makes
recovery deterministic.

### Notification Store

Notification state transitions such as opened, snoozed, handled, and action
invoked should be evented:

- `notification_events` records user/operator-visible transitions;
- current queue rows stay optimized for UI listing;
- optimistic version checks may remain for UI updates, but durable explanation
  lives in events.

### Whisper Intake

Whisper intake has privacy-sensitive stages: raw private material, redaction
draft, quarantine, candidate-ready, and Memarium sync. Temporal tracking is useful,
but raw private material must not be copied repeatedly.

Recommended direction:

- append stage events containing sealed references, digests, and metadata;
- keep raw/private payloads in sealed private storage;
- keep current intake item as the operator-facing projection.

### Artifact Delivery

Artifact Delivery has delivery runs, inbound admissions, retries, stream state,
and recovery. Add delivery/admission event or attempt tables for:

- submitted;
- target started;
- deferred;
- retry scheduled;
- transport failed;
- admission accepted/refused;
- recovery claimed/interrupted.

The existing current run/admission tables remain useful for status APIs.

### Contact Catalog

Contact Catalog already has a healthy mix of projections, audit rows, remote
claim caches, tombstones, and projection runs. The main work is to formalize the
pattern and ensure current rows are rebuildable from authoritative facts or
remote claim history where required.

## Stores That Should Not Be Changed Blindly

### Append-only Record Stores

The Node SQLite record store already has a temporal append-only model with
recorded and occurred times. Do not add another temporal layer unless a concrete
query or audit requirement appears.

### Agora Relay Store

Agora relay records are already append-only per topic. The mutable topic head is
an operational sequence allocator. Temporal storage does not remove the need for
a short transaction when assigning a local sequence.

### Scheduler

The replay scheduler already follows the recommended split: current job rows plus
launch history rows. It should be treated as a reference pattern.

### Caches, Cursors, and Idempotency Tables

Short-lived cache tables, idempotency lookup tables, and projection cursors should
not become fully temporal by default. They need TTLs, observed/updated times, and
diagnostics. Full history is justified only when replay, audit, or operator
forensics require it.

#### Cache vs. Fact Store With Eviction

Many tables called "cache" in existing code are not caches; they are fact
stores with provenance, mislabelled because the access pattern is lookup.
The diagnostic test:

> If you might ever want to ask "what did this cache contain at time T?"
> or "where did this value come from?" — it is not a cache. It is a
> temporal store with an eviction policy. Migrate it to the event-log
> model.

True caches are memoizations of pure functions: input determines value,
no provenance to record, "what was it yesterday" is not a meaningful
question. They stay temporal-free.

| Shape | Treatment |
|---|---|
| Memoization of a pure function (compiled validator, parsed config, derived key) | True cache. Hash key + value. No temporal axis. |
| Idempotency lookup, pagination cursor, short-lived dedup index | True cache. TTL only. No history. |
| Record of a remote claim or signed observation ("Seed Directory at T said X about node Y") | Fact store. Event-log model with retention, not eviction-only. |
| Cached passport / capability presentation with issuer, signature, validity | Fact store. Event-log model. |
| Observed TLS fingerprint, route advertisement, peer evidence | Fact store. Event-log model. |
| Resolver TTL state (cache-shaped) carrying remote claim payload (fact-shaped) | Hybrid — split. Store the fact; derive "should refetch?" as a query against `valid_until` or last `observed_at`. |

Two TTL meanings collide on these tables and are the root of recurring
bugs. On a true cache, TTL means "how long the memoization remains
trustable". On a fact store, retention means "how long we keep history
for audit". They are different axes. A single column called `expires_at`
that sometimes means one and sometimes the other is the sign of a table
that needs to be split.

## Trade-offs

### Benefits

- shorter critical sections;
- clearer recovery after crashes or interrupted operations;
- stronger auditability;
- replayable projections;
- easier equivalence tests between legacy/current stores and replay-fed views;
- fewer hidden status overwrites in queues and transport code.

### Costs

- more tables and indexes;
- projection maintenance code;
- more explicit retention policy;
- higher write volume;
- possible confusion if time axes are not named consistently.

### Constraints

- SQLite still serializes writes. This proposal reduces semantic blocking, not
  physical writer serialization.
- Current projections remain necessary for low-latency UI and query APIs.
- Retention must be explicit, especially for privacy-sensitive domains.

## Failure Modes and Mitigations

### Event Log Grows Without Bound

Mitigation: define per-domain retention and compaction. For append-only protocol
facts, retention can be long. For operational attempts, retention can be bounded
by age and count.

### Projection Drift

Mitigation: add rebuild tests and periodic projection checksums for important
stores. For Seed Directory and Artifact Delivery, use replay equivalence tests.

### Time Axis Confusion

Mitigation: use the naming contract above. Do not use `updated_at` as a
substitute for validity, observation, signature, or acceptance time.

### Duplicate Events From Retry

Mitigation: use `idempotency_key`, content digest, or protocol record id as a
unique key. Event append should be idempotent where retry is expected.

### Privacy Leakage Through History

Mitigation: event tables for private workflows must store sealed references,
digests, or metadata, not repeated plaintext payloads.

The deeper tension — "facts are forever" vs. "private data must be
deletable" — is real and must be addressed explicitly, not avoided.
Decision rule:

- **Default**: events store sealed references, digests, and metadata. The
  plaintext lives behind a sealed reference owned by the domain. Deleting
  the plaintext at the source naturally renders the event row uninformative
  without altering the event log itself. This is the preferred path.
- **Excision** (hard removal of an event row): permitted only when the
  domain explicitly requires it (legal request, operator action), recorded
  as its own `event_kind = 'excised'` transaction that names the removed
  `event_id` and reason but not the removed value. The original row is
  physically deleted; the excision fact stays. Projection rebuild treats
  an excised event as if it never asserted, but the excision tx remains
  visible to audit.
- **Never**: silent overwrite or in-place mutation of a prior event for
  privacy reasons. That breaks the audit guarantee for everything else.

This mirrors the excision pattern used by immutable database systems such as
Datomic: facts are immutable by default; hard removal is a separately
authorized, separately audited operation.

### Over-engineering Caches

Mitigation: require a concrete replay, audit, or operator-forensics need before
adding history to cache-like stores.

### Wall-Clock Skew After Suspend

Mitigation: separate monotonic from wall-clock as in the Time Axes section.
On resume from a suspend longer than a threshold (suggested 5 minutes),
run a projection-checksum verify against last-known-good and a lease
audit (any lease whose monotonic deadline has passed becomes recoverable
by another worker, regardless of wall-clock).

### Public Service On Personal Device Fills Disk

Mitigation: the `full-audit` profile combined with `Ephemeral` or
`Personal` device footprints requires explicit
`operator_acknowledged_disk_cost = true`. Readiness gate refuses to
bring such a store up otherwise. Periodic disk-usage report to operator
UI lists every `full-audit` store with its current size and trend, so
growth is never invisible.

## Example Flow

Delivery status without a long lock:

```text
1. Insert delivery event: submitted.
2. Project current row: pending.
3. Worker claims delivery with lease_owner + lease_until.
4. Worker sends through transport outside the DB transaction.
5. Insert attempt event: completed or failed.
6. Project current row: accepted, deferred, failed-retryable, or failed-terminal.
```

The durable explanation is the event/attempt sequence. The current row is a
read-optimized view.

## Implementation Guidance

Adopt this incrementally. The migration order is deliberate: dual-write is
the most dangerous step and must not be the steady state.

1. Document the convention in the relevant solution pages when a component is
   migrated.
2. Add event/attempt and transaction tables alongside existing current
   tables. Begin writing them, but treat them as the source of truth from
   day one.
3. **Derive** the current projection from the events at the point of write,
   in the same transaction. This is not dual-write — it is single-write
   into events, with a synchronous projection update as a step of the same
   commit. The legacy mutable table is removed in this step or replaced
   by the projection.
4. Add replay/projection rebuild tests. Replay the event log into a fresh
   projection table and compare row-by-row with the live projection. CI
   gate on equality.
5. Expose as-of queries on the component's store API.
6. Only then consider whether the legacy current row was carrying any
   information the events did not, and remove the residue.

The "dual-write current rows and events for one migration step" pattern
should be avoided as a target state. Dual-write is where divergence bugs
live: any path that writes one and not the other corrupts the read model.
Either the projection is derived (single source), or it is a separate
authority (don't temporalize).

Recommended first pilots:

1. Notification state transitions. The domain is small, internal, and
   already separates audit from projection in proposal 057 — making the
   projection derived rather than dual-written is the cheapest first
   migration.
2. Messaging outbox status and attempts.
3. Seed Directory accepted facts.
4. Artifact Delivery delivery/admission events.
5. Whisper intake stage events with sealed references.

Notification store moved to the top because it already had the right
architectural shape: a local queue projection and a separate audit trail. The
implemented pilot makes the SQLite temporal event log the recovery source of
truth, keeps `notification_queue` as the derived current projection, and keeps
JSONL as a diagnostic/export mirror rather than the only rebuild source.

## Decisions

The following were Open Questions in the draft. After the bitemporal model
above, they have clearer defaults.

1. **Shared helper crate**: yes, after the first two migrations converge.
   Likely surface: typed `TxId`, `EventId`, an `EventLog` trait, a
   `Projection` trait with replay-equivalence harness, and an `AsOf`
   primitive. Do not pre-build it — extract from working code in
   notification-store and outbox-store.
2. **Time format**: RFC3339 for `tx_time`; integer counters for operational
   durations and hot-path scheduling fields. Persisted ledger timestamps that
   already use integer Unix nanoseconds may keep that representation, but the
   bitemporal convention should not mix timestamp formats inside one store.
   The rule is one audited transaction-time representation per store, plus
   integer durations/counters where humans do not read the value directly.
3. **`tx_id` representation**: monotonic integer per store, allocated at
   commit. Not ULID, not UUID. The integer makes "events since tx N" a
   trivial range scan; per-store monotonicity is sufficient because event
   logs do not federate across stores.
4. **Compaction**: define per-domain, but specify the algorithm centrally.
   Compaction removes only events whose effect is wholly subsumed by a
   later event on the same `(subject_id, attribute)`, and only beyond a
   per-domain retention horizon. Excision is a separate mechanism with
   stronger audit. The two never run together.
5. **Projection rebuild as startup diagnostic**: yes, but lazy and bounded.
   On boot, compute a checksum of the projection and compare against a
   stored "last-known-good" checksum from a prior shutdown. Mismatch
   triggers a background full replay with operator notification, not a
   blocking rebuild.
6. **Cross-store sagas**: do not introduce a shared `correlation_id`
   registry. Each component owns its event log. Cross-store sagas are
   reconstructed by joining `correlation_id` columns at query time. A registry
   would pull the design toward a distributed transaction manager, which is
   explicitly out of scope.
7. **Large-value equality**: rely on `idempotency_key` as the generic
   de-duplication mechanism. Do not add a mandatory content digest column to
   the base event shape. Stores that need indexed content equality may add a
   domain-specific digest column, but that is an optimization, not part of the
   temporal contract.

## Remaining Open Questions

None for the draft convention. Future implementation work may still raise
store-specific retention, compaction, and migration questions.

## Next Actions

1. Complete the second pilot in Messaging outbox status and attempts.
2. Implement outbox event/attempt tables without changing public behavior.
3. Add replay equivalence tests for the outbox pilot.
4. Reassess whether a small shared temporal helper crate is justified after two
   migrations.
