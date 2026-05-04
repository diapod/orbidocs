# Replay Scheduler

**Status:** Partially implemented (M1 crate + daemon host adapter)

**Based on:** `scheduler-impl.md`, `agora-m2-impl.md`, `agora-m2b-impl.md`, `agora-m2c-impl.md`, `dir-simplify.md`, `doc/project/60-solutions/008-agora/008-agora.md`, `doc/project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md`, `node/storage-projector`, `node/agora-projections`

**Date:** 2026-05-04

## Executive Summary

The Replay Scheduler is a shared host-owned runtime primitive for bounded periodic jobs.
Its first intended consumer is Agora projection replay: comments, resource opinions,
public gossip, Seed Directory projections, and offer publication projections can be
kept fresh from local relay stores without an external trigger.

The scheduler decides **when** a registered job may run. It does not decide whether a
component is allowed to perform a domain action, does not interpret Agora records, and
does not allow one middleware component to force work inside another component. Domain
authorization remains behind a host-owned authority gate, and each job stays owned by
an explicit component/runtime API.

The implementation should live as a reusable Node crate, tentatively
`node/replay-scheduler` / `orbiplex-node-replay-scheduler`, with the daemon/host
providing the standard runtime adapter.

As of 2026-05-04, Phase 1 exists in Node as `node/replay-scheduler`. It implements
the generic crate, durable SQLite launch ledger, bounded launch gates, jitter/backoff,
same-gate `run-once`, cooperative shutdown, job-source normalization helpers, and
contract tests. The daemon also has the first host adapter: it extracts jobs from
node config and effective signed middleware package fragments, registers
`agora.projection.replay` as the first production action, exposes host scheduler
status/control API, and renders `/admin/scheduler` with HTMX-refreshing job controls.

## Context and Problem Statement

Agora M2 moves several public and federated domains toward replay-fed projections.
Without a common scheduler, each component tends to grow its own periodic loop,
retry policy, shutdown behavior, status surface, and partial backoff logic. That
creates hidden coupling and makes it harder to reason about overload, missed launches,
and cross-component authority boundaries.

The scheduler is needed to provide one small, auditable primitive for:

- periodic projection replay per topic/domain,
- bounded concurrency and bounded retry,
- deterministic jitter to avoid synchronized launch spikes,
- durable launch state for restart safety,
- operator-visible status,
- one consistent authority gate for automatic and manual `run-once` launches.

This document is solution-level. It defines responsibilities and invariants. Concrete
module layout, exact Rust type names, and endpoint implementation details belong in
the Node implementation repository.

## Proposed Model / Decision

The core contract is deliberately small:

```text
Scheduler decides when a launch may be attempted.
Job decides what execution means.
Authority/policy gate decides whether the job may run now.
Projection/runtime decides how records are processed.
```

### Stratification

```text
replay-scheduler
  time source
  jitter/backoff policy
  launch ledger
  bounded worker pool
  ScheduledJob trait
  status snapshots

host/daemon adapter
  merges local job sources
  injects owner_component_id
  binds specs to runtime-owned APIs
  provides ScheduledJobAuthority

agora-service / other components
  own domain job specs
  own domain replay code
  expose domain-specific operator meaning

agora-projections / domain read models
  validate and apply records
  own cursors and projection semantics
```

The scheduler is generic. Agora is the first consumer, not the owner of the primitive.

### Responsibilities

The scheduler must implement:

- registration of already-normalized job specs,
- next-due calculation,
- stable per-job/per-window jitter,
- full jitter for transient retry where appropriate,
- capped backoff after failures,
- global and per-job concurrency limits,
- overlap policy,
- missed-launch policy,
- durable launch ledger,
- cooperative shutdown and bounded drain,
- in-memory status snapshots backed by durable launch history,
- operator-visible error classes.

The scheduler must not implement:

- Agora record validation,
- semantic interpretation of `record/kind` or `content/schema`,
- capability/passport/domain authorization,
- signing or delegated signing,
- direct cross-middleware calls without a host-owned capability boundary,
- component configuration merge,
- process restart or supervision,
- trust, moderation, reputation, or Seed Directory policy.

## Job Ownership and Authority Boundary

Every runtime job must carry explicit ownership data:

- `job_id`,
- `owner_component_id`,
- `owner_runtime_api`,
- `domain`,
- optional `topic_key`,
- `action`.

These fields are not UI metadata. They are the inputs to the host-owned
`ScheduledJobAuthority`. The same authority path must be used for periodic launches
and operator-triggered `run-once` launches.

Example normalized Agora replay job:

```json
{
  "job_id": "agora.comments.replay.default",
  "owner_component_id": "agora-service",
  "owner_runtime_api": "component-local",
  "action": "agora.projection.replay",
  "domain": "comments",
  "topic_key": "ai.orbiplex.comments/example",
  "interval_ms": 15000,
  "enabled": true
}
```

A component may register or configure jobs for its own runtime API. A component must
not register a job that invokes another component's private action unless the host
exposes an explicit delegated capability contract for that action.

## Local Job Sources and Merge Rules

Job sources are local and host-owned. Valid sources include:

- global host configuration,
- component configuration,
- built-in or external middleware package factory configuration that has become
  effective after Local Readiness Gate acceptance,
- runtime-owned registration API for the calling component's own jobs,
- explicit operator action such as enabling replay for a topic.

Invalid sources include:

- an Agora record that directly creates a local job,
- a remote peer that forces a local resynchronization,
- middleware A registering a job to execute middleware B without a host policy gate.

The host/daemon adapter, not the scheduler crate, normalizes job sources into final
`ScheduledJobSpec` values. Merge rules:

1. Global host jobs receive an explicit host-owned `owner_component_id`, such as
   `daemon`.
2. Component config jobs receive the owner id of that component.
3. Middleware package factory jobs receive the owner id of the package/component that
   contributes the job.
4. Runtime registration may only register the caller's own `owner_component_id`,
   unless an explicit delegated capability contract exists.
5. `job_id` conflicts are configuration errors unless an explicit override mechanism
   is used under the same owner. The accepted override shape is: same
   `owner_component_id`, same `job_id`, and explicit `override_existing: true`.
   The daemon parser also accepts `override: true` as a compatibility alias.

`owner_runtime_api` is a string at the configuration/wire boundary. The host adapter
normalizes known values and rejects unknown values before the scheduler sees the job.

Middleware package job specs are read only from effective package configuration. In
other words, package artifact signing and operator acceptance are handled before job
extraction:

```text
middleware package artifact signed/accepted
  -> package config becomes effective
  -> host adapter extracts package-owned job specs
  -> scheduler receives normalized jobs
```

The scheduler does not validate package signatures.

The first implemented package fragment kind is:

```json
{
  "kind": "daemon.scheduler_jobs",
  "path": "config/scheduler-jobs.json"
}
```

The fragment body is a map keyed by `job_id`. Each value is a daemon scheduler job
config. Daemon-facing job ids are also used in host HTTP paths, so they must be a
single path segment using only ASCII letters, digits, `.`, `_`, `-`, and `~`.
For Agora replay jobs, `action` is `agora.projection.replay` and the action-specific
payload is carried under `agora_projection_replay`. The host adapter normalizes
that shape into a `ScheduledJobSpec`; the generic scheduler never reads package
manifests or Agora semantics directly.

Example:

```json
{
  "agora.comments.example": {
    "owner_component_id": "agora-service",
    "owner_runtime_api": "component-local",
    "action": "agora.projection.replay",
    "domain": "agora.comments",
    "topic_key": "ai.orbiplex.comments/example",
    "interval_ms": 15000,
    "agora_projection_replay": {
      "executor_id": "agora-service",
      "record_kind": "comment",
      "content_schema": "plain-comment.v1",
      "limit": 100
    }
  }
}
```

## Launch Ledger

The runtime scheduler requires a durable launch ledger from the first implementation.
An in-memory ledger is acceptable only as a test fixture. If the durable ledger cannot
be opened, runtime startup must fail closed or the scheduler must be disabled with a
clear operator-visible error. Silent fallback to volatile runtime state is not allowed.

The launch ledger is separate from domain cursors. It records scheduler decisions,
not domain projection state.

Minimum logical tables:

```sql
CREATE TABLE IF NOT EXISTS scheduled_jobs (
    job_id TEXT PRIMARY KEY,
    owner_component_id TEXT NOT NULL,
    owner_runtime_api TEXT NOT NULL,
    domain TEXT NOT NULL,
    topic_key TEXT,
    action TEXT NOT NULL,
    enabled INTEGER NOT NULL,
    interval_ms INTEGER NOT NULL,
    next_due_at TEXT,
    last_started_at TEXT,
    last_finished_at TEXT,
    last_status TEXT,
    consecutive_failures INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scheduled_launches (
    launch_id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL,
    scheduled_for TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,
    attempt INTEGER NOT NULL DEFAULT 1,
    error_class TEXT,
    error_message TEXT,
    outcome_json TEXT,
    UNIQUE(job_id, scheduled_for)
);
```

`launch_id` should be deterministic, for example from canonical JSON over
`job_id`, `scheduled_for`, and `attempt`. This makes restart recovery and duplicate
launch detection auditable.

## Scheduling Semantics

Default policies:

```text
overlap = SkipIfRunning
catch_up = RunOnceIfMissed
```

Rationale: replay/projection jobs should be idempotent, but the dependencies they
exercise are not necessarily cheap. After downtime, the system should catch up with
one bounded run rather than creating a replay storm.

A run should be short and bounded. For Agora projection replay:

```text
one run = one bounded replay page or one bounded replay loop with a deadline
```

The first daemon adapter uses the page form: `agora.projection.replay` requires a
positive `agora_projection_replay.limit`, and the Agora projection store advances
its own durable cursor after each page. The scheduler job does not loop over all
remaining pages in one launch; the next scheduler tick advances the next bounded
page.

Not:

```text
one run = replay everything without limit
```

Stable jitter should be deterministic per `job_id` and scheduled window so restarts
remain diagnosable while avoiding synchronized launches. Transient retry can use full
jitter with capped backoff.

## Failure Modes and Mitigations

| Failure class | Meaning | Mitigation |
| --- | --- | --- |
| `transient` | temporary transport/store failure | capped backoff + jitter |
| `overloaded` | dependency rejects or signals overload | longer cooldown; no tight loop |
| `authorization-denied` | authority/capability gate denied launch | disable or slow retry; operator-visible |
| `invalid-config` | local job spec/config is invalid | fail closed or disable job; operator-visible |
| `non-retryable` | domain error where retry is not useful | mark failed; operator-visible |
| `deadline-exceeded` | job exceeded execution budget | backoff; domain may reduce page size |
| ambiguous started launch | restart found `started` without `finished_at` | fail closed for that launch window; avoid double launch |

The scheduler must never busy-spin on repeated failure.

## Shutdown Contract

The scheduler must support:

- a stop token visible to running jobs,
- no new launches after stop begins,
- graceful drain up to `shutdown_grace`,
- final status persistence for interrupted jobs,
- cooperative cancellation between replay pages or other bounded work units.

The scheduler does not preemptively kill a job. Jobs must observe the stop token at
safe boundaries.

## Agora Projection Replay as First Consumer

Agora service should register projection replay jobs for public/federated read models,
for example:

- comments,
- resource opinions,
- public gossip,
- Seed Directory accepted-record projections,
- offer publication snapshot projections.

Each Agora-owned job invokes the Agora projection layer, such as
`ProjectionStore::replay_topic_from_relay(...)`, and returns a generic job outcome:

```json
{
  "schema": "scheduled-job-outcome.v1",
  "records_seen": 100,
  "records_applied": 97,
  "records_skipped": 2,
  "records_rejected": 1,
  "cursor": "1234",
  "lag_hint": {
    "topic_key": "ai.orbiplex.comments/example",
    "last_sequence": 1234
  }
}
```

The scheduler sees this as data. Agora remains responsible for explaining what the
numbers mean for a topic, schema, cursor, or read model.

## Operator Visibility

The scheduler crate should expose pure data snapshots. If HTTP is exposed, it belongs
to the host component or component-specific UI surface, not to the generic crate.

A host may expose:

```text
GET /v1/scheduler
GET /v1/scheduler/jobs/{job-id}
POST /v1/scheduler/jobs/{job-id}/run-once
POST /v1/scheduler/jobs/{job-id}/pause
POST /v1/scheduler/jobs/{job-id}/resume
```

Component UIs should add domain meaning. For example, Agora UI should show topic,
record kind, content schema, cursor, lag, applied/skipped/rejected counts, and the
last domain error for Agora-owned replay jobs.

## Implementation Phases

### Phase 1 — Scheduler crate and clean runtime

- Add `node/replay-scheduler`.
- Define scheduler config, job spec, job trait, authority trait, outcomes, and error
  classes.
- Implement durable SQLite launch ledger from the start.
- Implement stable jitter, full jitter, capped backoff, bounded worker pool, and
  cooperative shutdown.
- Add restart/double-launch tests.

Status: done for the generic crate. The implementation enforces bounded concurrent
launches by global and per-job gates; it does not yet expose a daemon-owned HTTP/API
surface.

### Phase 2 — Host adapter and job-source merge

- Normalize global host jobs, component jobs, and middleware-package factory jobs
  from effective package configuration after Local Readiness Gate acceptance.
- Inject `owner_component_id`, `owner_runtime_api`, and `action`.
- Normalize `owner_runtime_api` as a string and reject unknown values.
- Reject conflicting `job_id` values unless the override has the same
  `owner_component_id`, the same `job_id`, and explicit `override_existing: true`.
- Block runtime registration for another component's owner id unless a delegated
  capability contract allows it.

### Phase 3 — Agora adapter

- Register Agora M2 projection jobs from Agora-owned configuration.
- Route jobs to `ProjectionStore::replay_topic_from_relay(...)`.
- Add status to host scheduler status and/or Agora status surface.
- Cover in-memory and SQLite relay/store paths in tests.

### Phase 4 — Operator UI

- Host UI shows generic scheduler mechanics.
- Agora UI surfaces Agora-owned jobs with domain-specific meaning.
- `run-once`, pause, and resume remain gated by the same authority path as periodic
  launches.

## Trade-offs

Benefits:

- one scheduler primitive instead of ad-hoc loops,
- consistent overload/backoff/shutdown semantics,
- restart-safe launch accounting,
- clear authority boundary between timing and domain permission,
- reusable primitive for non-Agora maintenance jobs.

Costs and constraints:

- durable ledger adds implementation cost early,
- host adapter must normalize job sources carefully,
- strict ownership prevents some convenient shortcuts,
- distributed leadership is explicitly deferred.

Deferred intentionally:

- distributed scheduler leadership,
- declarative DAG/dependency scheduling,
- remote peers creating local jobs,
- public protocol semantics for scheduler state.

## Invariants

- Scheduler does not run work without an explicit registered owner.
- Scheduler does not accept runtime job specs missing owner/action fields.
- Scheduler never lets one middleware force another middleware's private action
  without host-owned capability/policy approval.
- Host adapter owns job-source merge and owner injection.
- Every launch has a deterministic `launch_id`.
- Runtime uses a durable launch ledger.
- Default policy prevents overlap.
- Default missed-launch policy runs at most one catch-up launch.
- Retry has backoff, jitter, cap, and visible error class.
- Shutdown is cooperative and bounded.
- Replay jobs are idempotent and paged or deadline-bounded.
- Operator can inspect due/running/failed/paused state and the reason for failure.

## Open Questions

No protocol-level open questions remain for the M1 scheduler contract.

Implementation details still need normal code review when the crate lands:

1. The exact list of initially known `owner_runtime_api` string values.
2. The exact audit payload for accepted same-owner overrides.
3. The concrete host configuration path for global scheduler settings.

## Next Actions

1. Wire the host/daemon adapter that owns global, component, and middleware-package
   job-source extraction after Local Readiness Gate acceptance.
2. Wire Agora projection replay jobs as the first real consumer.
3. Add host scheduler status/run-once/pause/resume routes and keep component-specific
   rendering inside the owning UI, starting with Agora.
4. Keep scheduler documentation synchronized with the Rust data shapes as host
   integration lands.

## Related Capability Data

- `020-scheduler-caps.edn`
