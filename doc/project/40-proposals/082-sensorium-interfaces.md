# Proposal 082: Sensorium Interfaces

Based on:

- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/075-matrix-homeserver-runtime-profile.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/60-solutions/020-scheduler/020-scheduler.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/035-interaction-broker/035-interaction-broker.md`
- `doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`

## Status

Implemented / promoted to Solution 046

The frozen V1 contract is implemented in Node and promoted to
[Solution 046: Sensorium Interfaces](../60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).
This proposal remains the rationale, decision record, named-invariant catalog,
and implementation tracker. It is an explicit hard-MVP release blocker whose
implementation gate is satisfied.

## Date

2026-07-16

## Executive Summary

A Sensorium Interface is a host-owned, explicitly published projection of an
enacted representation. It allows an authorized consumer to obtain that
representation either:

- on demand, as one bounded read result; or
- over time, as a bounded cursor-based subscription.

The interface is not a connector, a capability, a store, a transport, or a new
organ. It is a resource governed by a small contract family. Capabilities authorize
operations on that resource; Sensorium, Workbench, and Artifact Delivery
providers produce or admit domain values; the Interaction Broker supplies bounded
probe/watch mechanics; and HTTP,
`channel_json`, authenticated peer sessions, Room live transport, and Artifact
Delivery remain interchangeable edge adapters with different delivery properties.

V1 has one canonical delivery contract: bounded cursor-based pull-batch. A live SSE,
WSS, or Room view is a thin carrier projection whose bounded adapter loop repeatedly
invokes read-next. It is not a second provider-push protocol.

This distinction is the central design rule:

```text
environment
  -> connector or Workbench provider
  -> domain admission and projection
  -> Sensorium Interface resource
  -> authorized read or subscription
  -> selected carrier adapter
  -> consumer
```

No consumer reaches a connector directly. No carrier grants authority. No stream
creates a second source of truth.

This proposal owns publication, delegated read, subscription lifecycle, and
carrier-neutral flow control across Sensorium-backed views. Proposal 045 continues
to own local Sensorium admission and actuation. Proposal 071 and Room are first
consumers rather than alternate homes for the same semantics.

## Basis and Existing Substrate

This proposal refines and composes existing contracts rather than defining an
independent observation stack:

- [Proposal 045: Sensorium Local Enaction Stratum](045-sensorium-local-enaction-stratum.md)
  owns connector lanes, observation admission, local query/get, directives, and
  Sensorium policy;
- [Solution 030: Sensorium](../60-solutions/030-sensorium/030-sensorium.md)
  records local observation/query runtime as implemented, local Agora publication as
  partial, and cross-node read-through as deferred;
- [Proposal 071: Sensorium Workbench](071-sensorium-workbench.md)
  and [Solution 042: Sensorium Workbench](../60-solutions/042-sensorium-workbench/042-sensorium-workbench.md)
  already define bounded terminal events, screen snapshots, cursors, and
  Interaction Broker providers;
- [Proposal 070: Room Primitive](070-room-primitive.md) owns
  collaborative membership, grants, and best-effort live transport;
- [Proposal 024: Capability Passports](024-capability-passports-and-network-ledger-delegation.md)
  owns signed cross-node capability delegation;
- [Proposal 080: Multiplexed Middleware Channel](080-multiplexed-middleware-channel-executor.md)
  owns bounded host-to-middleware request/reply and observer transport;
- [Proposal 081: Horizontal Protocol Primitives](081-horizontal-protocol-primitives.md)
  owns canonical causal context and immutable execution receipts;
- [Proposal 047: Classification Label Propagation](047-classification-label-propagation.md)
  owns `classification.v1` propagation and no-broadening rules;
- [Solution 020: Replay Scheduler](../60-solutions/020-scheduler/020-scheduler.md),
  [Solution 029: Bounded Deferred Operations](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md),
  and [Solution 023: Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
  remain the host-owned primitives for polling, long-lived control operations, and
  large or store-and-forward artifacts.

The implementation should also follow `node/DEV-GUIDELINES.md`, especially its
rules for protocol/core/runtime stratification, schema-gating at boundaries, bounded
external work, explicit lifecycle state machines, and reuse of host-owned runtime
primitives.

## Context and Problem Statement

Sensorium can currently admit and query observations locally. Workbench can expose a
bounded terminal snapshot or event batch through the Interaction Broker. What is
missing is one shared contract for deliberately making such a view available to
another authorized local component or remote node.

Without that contract, each producer is likely to invent a different combination of:

- resource naming and discovery;
- read and stream APIs;
- grants and caller binding;
- cursors, replay, backpressure, and overflow;
- classification and redaction;
- revocation and stream closure;
- retention and capture;
- transport-specific envelopes.

The result would be three semantically different implementations for a terminal
view, a temperature sensor, and a camera, even though all three need the same
publication and subscription mechanics.

## Goals

- Define one host-owned resource representing an explicitly published view.
- Give on-demand reads and subscriptions the same payload and cursor semantics.
- Make the first implementation possible with existing Sensorium, Workbench,
  Interaction Broker, Replay Scheduler, `channel_json`, Room, and Artifact Delivery
  machinery.
- Keep authorization, classification, retention, and transport as separate strata.
- Support local components, direct authenticated peers, and collaborative Room use
  without making any one carrier canonical.
- Make queue, batch, byte, lease, deadline, replay, and retention bounds explicit.
- Preserve P081 causal context and receipt semantics across publication, read,
  subscription, revocation, and terminal outcomes.

## Non-Goals

- A general remote connector API.
- Direct consumer access to devices, terminals, or connector credentials.
- A lossless universal event bus.
- Global discovery of available sensors or interfaces.
- Automatic persistence of streams in Memarium.
- Moving Sensorium observations into Room, Matrix, or Agora as a new source of
  truth.
- Treating Room membership, Matrix membership, a transport session, or possession
  of an interface id as authorization.
- Adding actuation commands to the read/subscribe contract. Commands remain in
  separate Sensorium directive and Workbench tool-request lanes; their future
  interface-level authority and coordination contract is defined separately by
  [Proposal 083: Sensorium Interactive Interfaces](083-sensorium-interactive-interfaces.md).
- Promising erasure of information already received by an authorized consumer.

## Surveillance Is a Relationship, Not an API Shape

Surveillance is observation without adequate knowledge, consent, authority, or
scope. The same camera or terminal view can participate in care, collaboration,
operations, coercion, or surveillance. A schema cannot infer that relationship, but
the host can enforce structural preconditions:

- no interface becomes externally readable until an authorized source-side actor
  publishes it;
- interfaces are local-only and undiscoverable by default;
- the source operator can enumerate active interfaces, grants, subscriptions, and
  recent closures;
- grants bind a canonical namespaced authenticated subject ref, interface id,
  operations, classification ceiling, expiry, and rate/volume limits; bare ids
  are invalid because they cannot distinguish principal kinds;
- every emitted value passes source policy, redaction, and egress classification;
- revocation stops new reads and emissions within host-owned pull-loop and
  revocation-view freshness budgets; tests prove refusal before the next
  authorized emission without presenting durable-write latency as that bound;
- data already delivered is outside technical revocation and must not be described
  as retractable;
- representations involving third parties carry the appropriate
  `classification.v1.bound_subjects` projection and may require consent beyond the
  source operator.

The prohibited design is therefore an ambient, invisible, unbounded, or
unauthorized observation surface. The contract does not preclude a narrow interface
that affected parties knowingly and legitimately choose to share.

## Proposed Model

### 1. Interface Is a Resource; Capability Is an Operation Class

The phrase "interface = published capability" is rejected. It couples a resource
instance to an authorization vocabulary and would grow the capability registry for
every sensor, terminal session, or view.

Instead:

- `sensorium-interface:<id>` identifies one published view;
- `sensorium.interface.read` authorizes bounded on-demand reads;
- `sensorium.interface.subscribe` authorizes creation and use of a bounded
  subscription;
- `sensorium.interface.manage` authorizes publication, suspension, withdrawal, and
  grant administration on the source node.

The V1 registry posture is frozen with the operation classes:

| Capability id | `wire/name` | Surfaces | Dispatchable | Advertisable | Passport eligible | Signing domain | Host route | Federated discovery |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `sensorium.interface.read` | `sensorium/interface.read` | `host-local`, `federated` | true | true | true | false | true | true |
| `sensorium.interface.subscribe` | `sensorium/interface.subscribe` | `host-local`, `federated` | true | true | true | false | true | true |
| `sensorium.interface.manage` | `sensorium/interface.manage` | `host-local` | true | false | false | false | true | false |

Advertising `read` or `subscribe` declares protocol support only. It never advertises
an interface descriptor, source binding, grant, or active subscription. A grant or
Passport scope narrows a generic operation to one interface resource. Possession of
a valid Passport is evidence; the source node still performs local admission and
current restriction checks on every operation. The machine registry and its
authorization-policy sidecar MUST carry these flags explicitly; implementation
defaults may not infer them from the capability name.

`read` and `subscribe` remain separate because they grant different authority and
create different state. `read` authorizes one bounded stateless result. `subscribe`
authorizes creation, renewal, bounded consumption, and closure of one caller-bound
lease; it permits reads only through that lease and does not imply arbitrary
one-shot access. The initial `manage` capability is source-local and MUST NOT be
delegated through a cross-node Passport. Whether later local policy splits it into
publication and grant-administration capabilities is an explicit post-V1 policy
decision, not a wire concern hidden in the request body.

One interface has one projected meaning and one primary output schema. A terminal
screen and a terminal event feed should therefore be separate interface resources,
even if they share the same underlying Workbench session. This avoids conditionals
inside a supposedly stable interface and lets the more revealing event feed carry a
stricter policy.

### 2. Publication Is Explicit and Local by Default

Publishing creates a descriptor and a private source binding in host-owned storage.
The descriptor is safe to reveal only to an already authorized consumer; the source
binding remains local and may contain connector, terminal-session, topic, or provider
details that must not cross the boundary.

Conceptual descriptor:

```json
{
  "schema": "sensorium-interface-descriptor.v1",
  "schema/v": 1,
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "interface/name": "workbench-current-screen",
  "publisher/node-ref": "node:did:key:z6MkPublisherExample",
  "output/schema-ref": "urn:orbiplex:schema:sensorium-terminal-screen-snapshot:v1",
  "delivery/semantics": "latest-state",
  "access/modes": ["read", "subscribe"],
  "classification/max-tier": "Personal",
  "classification/topic-class": "sensorium-interface/workbench-visible-viewport",
  "redaction/profile-ref": "redaction:terminal-visible-viewport-v1",
  "limits": {
    "frame/max-bytes": 65536,
    "batch/max-frames": 32,
    "batch/max-bytes": 262144,
    "lease/max-seconds": 900
  },
  "overflow/policy": "coalesce-latest",
  "expires/at": "2026-07-13T13:00:00Z"
}
```

Lifecycle and health are a separate rebuildable projection:

```json
{
  "schema": "sensorium-interface-status.v1",
  "schema/v": 1,
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "lifecycle/status": "published",
  "health/status": "ready",
  "status/at": "2026-07-13T12:00:00Z"
}
```

The descriptor is an immutable publication contract. Limits remain nested because
they are security and delivery semantics that must be authorized together with the
output schema; they are not an independently swappable tuning profile. Lifecycle
and health are separated because they change over time. Changing the descriptor's
source projection, output schema, classification ceiling, or limits withdraws the
old interface and publishes a new `interface/id` rather than mutating its meaning in
place. A grant or current host policy may always narrow effective limits without
changing the descriptor; it cannot widen them.

P082-003 will materialize this descriptor as JSON Schema. The following semantic
invariants are frozen now:

- `delivery/semantics` is a closed enum: `latest-state` or `ordered-events` in v1;
- `latest-state` requires `overflow/policy = coalesce-latest`;
- `latest-state` forbids `replay/max-frames` and `replay/max-seconds`; it retains
  exactly one current complete snapshot per source generation, and its cursor is a
  change detector rather than a history promise;
- `ordered-events` permits `emit-gap` or `close-subscription`, never silent loss;
- `ordered-events` requires positive `replay/max-frames` and
  `replay/max-seconds`; effective replay retention is their intersection, so
  reaching either bound may evict the oldest event;
- all numeric bounds are positive and capped by host policy;
- `frame/max-bytes` caps each allocation and serialized frame, while
  `batch/max-bytes` independently caps their aggregate plus envelope overhead; a
  value above the frame cap becomes an Artifact Delivery reference, not an
  automatically fragmented frame;
- an expired, suspended, or withdrawn interface cannot admit new reads or
  subscriptions;
- the externally visible descriptor never contains connector credentials, local
  filesystem paths, middleware launch credentials, or the private source binding;
- interface publication does not create Seed Directory, Agora, or federation-root
  advertisement state.

### 3. Source Binding Is Polymorphic and Host-Private

The host binds an interface to a provider through data, then selects behavior through
a narrow provider trait. The interface runtime must not grow one transport or daemon
branch for every sensor type.

Conceptual local value:

```json
{
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "source/kind": "workbench-terminal-screen",
  "source/ref": "terminal-session:01JZEXAMPLE",
  "projection/profile-ref": "projection:terminal-visible-viewport-v1"
}
```

Illustrative core boundary:

```rust
pub trait SensoriumInterfaceSource: Send + Sync {
    fn source_kind(&self) -> &'static str;
    fn ready(&self) -> bool;
    fn validate_binding(
        &self,
        descriptor: &InterfaceDescriptor,
        binding: &InterfaceSourceBinding,
    ) -> Result<(), InterfaceSourceError>;
    fn next_batch(&self, context: InterfaceSourceWatchContext)
        -> Result<SourceBatch, InterfaceSourceError>;
}
```

The first runtime should adapt this boundary to the existing Interaction Broker
provider registry rather than implement another wait/watch engine. One
`ObservationSource::SensoriumInterface { interface_id }` variant can route all
interface watches to one registered domain provider; that provider then dispatches
by the private `source/kind`. This adds one broker integration point, not a new
source-specific `match` arm for every adapter.

Initial source adapters:

| Source kind | Existing producer | Initial projection |
|---|---|---|
| `sensorium-observation-query` | Sensorium Core `sensorium.observe.query` / `sensorium.observation.get` | admitted observation or bounded latest value |
| `workbench-terminal-screen` | Workbench terminal provider | `sensorium-terminal-screen-snapshot.v1` |
| `workbench-terminal-events` | Workbench terminal provider | bounded `sensorium-terminal-event.v1` batch |
| `artifact-snapshot` | Artifact Delivery object pointer | immutable by-reference payload |

The implemented daemon persists a generic, closed `source/binding` value with a
bounded private `source/config`, dispatches it through a registry of at most 64
adapters, and revalidates the adapter and binding on every read after restart.
Adding an adapter therefore extends the registry rather than a central source
`match`. The initial four adapters above are registered through that boundary.
Startup fails unless all four built-in adapters are registered. Unknown,
duplicate, unavailable, malformed, or excess adapters fail closed. Registry
`ready` state is a point-in-time operator signal; `next_batch` remains the
authoritative operation and may still fail closed when source readiness changes
after the snapshot. Registry snapshots clone adapter handles before invoking
`ready()`, so neither provider readiness nor source I/O runs under the registry
lock.

#### Source Policy and Interface Authority Compose

Sensorium Core currently emits `sensorium.read.local` as the default value in an
admitted observation's `admission.consumer_scopes`. It is a source-domain policy
scope, not a registered host-dispatch capability and not remote authority.

For `source/kind = sensorium-observation-query`, the two layers compose
conjunctively:

1. the host-local source adapter may query only observations whose Sensorium
   consumer-scope policy permits that local projection;
2. `sensorium.interface.read` or `sensorium.interface.subscribe` independently
   authorizes the bound caller to cross the published interface boundary;
3. the interface grant may narrow the source result but can never widen its
   consumer scopes, classification, redaction, retention, or query bounds.

A remote caller is never granted or asked to present `sensorium.read.local`. The
source node exercises that local scope internally, then performs interface admission
and egress checks. Neither layer replaces the other, and failure at either layer
fails the read closed.

### 4. Read and Subscribe Share One Batch Contract

An on-demand read returns one bounded result batch. A subscription returns a
sequence of the same result batches. The batch, not an individual frame, is the unit
of cursor progress, P081 causality, diagnostics, and carrier projection. Frames
remain small domain values inside that envelope.

Conceptual read request:

```json
{
  "schema": "sensorium-interface-read-request.v1",
  "schema/v": 1,
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "delivery/kind": "one-shot",
  "cursor/after": "opaque:provider-bound-cursor",
  "batch": {
    "frames/max": 16,
    "bytes/max": 131072,
    "wait/max-ms": 5000
  },
  "deadline/at": "2026-07-13T12:00:05Z",
  "causal/context": {
    "schema": "causal-context.v1",
    "schema/v": 1,
    "context/id": "causal-context:01K0EXAMPLE",
    "correlation/id": "corr:sensorium-read:01K0EXAMPLE",
    "operation/id": "operation:01K0EXAMPLE",
    "causation/refs": [],
    "origin/actor-ref": "component:arca",
    "created/at": "2026-07-13T12:00:00Z"
  }
}
```

For a one-shot read, `delivery/kind = one-shot` and `subscription/id` is absent. For
the next batch of an active subscription, the same request uses
`delivery/kind = subscription` and carries `subscription/id`. The schema makes this
a conditional invariant rather than using `null`. The host verifies that the
authenticated caller, interface id, cursor, and live lease all refer to the same
subscription. A cursor is never a subscription bearer token.

Conceptual subscription result:

```json
{
  "schema": "sensorium-interface-read-result.v1",
  "schema/v": 1,
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "delivery/kind": "subscription",
  "subscription/id": "sensorium-subscription:01K1EXAMPLE",
  "batch/outcome": "data",
  "cursor/next": "opaque:provider-bound-cursor-42",
  "frames": [
    {
      "schema": "sensorium-interface-frame.v1",
      "schema/v": 1,
      "frame/kind": "snapshot",
      "observed/at": "2026-07-13T12:00:01Z",
      "emitted/at": "2026-07-13T12:00:02Z",
      "payload/schema-ref": "urn:orbiplex:schema:sensorium-terminal-screen-snapshot:v1",
      "payload": {
        "schema": "sensorium-terminal-screen-snapshot.v1",
        "schema/v": 1,
        "terminal.session/ref": "terminal-session:01JZEXAMPLE",
        "from.seq/no": 40,
        "to.seq/no": 42,
        "viewport": {
          "rows": 24,
          "cols": 80,
          "cursor.row": 3,
          "cursor.col": 12,
          "text": "running tests..."
        },
        "classification": {
          "schema": "classification.v1",
          "source_tier": "Personal",
          "effective_tier": "Personal",
          "provenance": {
            "kind": "local-space",
            "space": "Personal"
          },
          "bound_subjects": {
            "personal_or_community": [
              {
                "kind": "nym",
                "id": "nym:did:key:z6MkWorkbenchOwner"
              }
            ]
          },
          "declassify_trail": []
        }
      },
      "classification": {
        "schema": "classification.v1",
        "source_tier": "Personal",
        "effective_tier": "Personal",
        "provenance": {
          "kind": "local-space",
          "space": "Personal"
        },
        "bound_subjects": {
          "personal_or_community": [
            {
              "kind": "nym",
              "id": "nym:did:key:z6MkWorkbenchOwner"
            }
          ]
        },
        "declassify_trail": []
      }
    }
  ],
  "delivery/diagnostics": {
    "coalesced/count": 0,
    "gap/count": 0
  },
  "causal/context": {
    "schema": "causal-context.v1",
    "schema/v": 1,
    "context/id": "causal-context:01K2EXAMPLE",
    "correlation/id": "corr:sensorium-subscription:01K1EXAMPLE",
    "operation/id": "operation:01K2EXAMPLE",
    "causation/refs": ["execution-receipt:01K1EXAMPLE"],
    "origin/actor-ref": "node:did:key:z6MkPublisherExample",
    "created/at": "2026-07-13T12:00:02Z"
  }
}
```

Batch and frame rules:

- `delivery/kind` is an explicit discriminator: `one-shot` forbids
  `subscription/id`, while `subscription` requires it;
- a subscription result requires `cursor/next`; a direct one-shot result may return
  it for later change detection, while a carrier projection that owns the source
  cursor locally may omit it;
- `cursor/after` and `cursor/next` are opaque, bounded, provider-defined progress
  tokens bound to the interface and source generation; frames carry no second
  cursor and no interface-local sequence number;
- for `latest-state`, a cursor lets long-poll express "wait until the projected
  state changes" instead of repeatedly returning the same snapshot;
- for `ordered-events`, array order defines order inside one batch and
  `cursor/next` advances past the complete batch; source payloads preserve stable
  domain ids or digests so replaying a partially consumed batch is idempotent;
- `frame/kind` is one of `snapshot`, `event`, `gap`, or `end`;
- `batch/outcome` is one of `data`, `no-change`, or `terminal`; failures use the
  typed error contract rather than a fourth pseudo-success outcome;
- a `snapshot` or `event` carries exactly one inline `payload` or one
  `artifact/ref`, never both;
- inline payloads pass the schema gate against the descriptor's
  `output/schema-ref` and byte cap before becoming typed values;
- large, binary, or durable values use an Artifact Delivery pointer rather than a
  larger frame;
- a `gap` identifies the lost or unavailable cursor interval and the recovery
  action; it cannot masquerade as an empty successful batch;
- a successful long-poll timeout is `batch/outcome = no-change` with an empty
  `frames[]`; it proves the request completed but is neither a heartbeat nor a gap;
- an `end` carries a typed terminal reason and no domain payload, closes the
  subscription, and MUST be the final frame in the final batch accepted for that
  `subscription/id`;
- `batch/outcome = terminal` is valid only for subscription delivery and requires
  exactly one final `end` frame;
- every value carries effective `classification.v1`; the consumer may narrow but
  never broaden it;
- when the domain payload already embeds `classification.v1`, its value must be
  structurally equal to the frame classification; a mismatch fails closed rather
  than asking the carrier to choose one;
- P081 context is batch metadata, never authorization. A receiving host derives a
  local context and preserves the accepted upstream context as evidence. Selective
  receipts describe read admission, delivered batches when they are external
  effects, and terminal transitions; the protocol does not emit a receipt or repeat
  full context for every frame. Adapter-owned read-next operations identify their
  actual carrier, such as SSE or Room projection, in correlation and operation ids.

The result contains a bounded `frames[]`, `cursor/next`, a typed batch outcome,
bounded delivery diagnostics, P081 context, and retry advice. A latest-state read
normally returns one snapshot. An ordered-events read may return several events up
to both requested and host caps. A consumer advances `cursor/after` only after it
has accepted the complete batch; otherwise the batch may be replayed.

### 5. Subscription Is a Lease, Not an Infinite Promise

Conceptual subscription request:

```json
{
  "schema": "sensorium-interface-subscribe-request.v1",
  "schema/v": 1,
  "interface/id": "sensorium-interface:01K0EXAMPLE",
  "cursor/after": "opaque:optional-resume-cursor",
  "lease/requested-seconds": 300,
  "batch": {
    "frames/max": 16,
    "bytes/max": 131072,
    "wait/max-ms": 5000
  },
  "deadline/at": "2026-07-13T12:00:05Z",
  "causal/context": {
    "schema": "causal-context.v1",
    "schema/v": 1,
    "context/id": "causal-context:01K1EXAMPLE",
    "correlation/id": "corr:sensorium-subscription:01K1EXAMPLE",
    "operation/id": "operation:01K1EXAMPLE",
    "causation/refs": [],
    "origin/actor-ref": "nym:did:key:z6MkSubscriberExample",
    "created/at": "2026-07-13T12:00:00Z"
  }
}
```

The host returns a subscription id, granted lease, effective caps, starting cursor,
and current state. Renewal is an explicit authorized operation. Expiry closes the
subscription even if the carrier remains connected.

`sensorium-interface-subscription-command.v1` carries the bound `subscription/id`,
an `action` closed to `renew` or `close`, deadline, and P081 causal context. `renew`
also carries `lease/requested-seconds`; it cannot extend beyond the descriptor,
grant, or host-policy expiry. `close` is idempotent. Neither operation accepts a
caller identity in its payload.

Publication state machine:

```text
published <-> suspended
published | suspended -> withdrawn
published | suspended -> expired
```

There is no protocol-visible `draft`. Publication atomically appends the immutable
descriptor and its initial `published` fact. `withdrawn` and `expired` are terminal;
resuming either requires a new interface id.

Subscription state machine:

```text
requested -> active -> closing -> closed
requested ---------------------> closed
active ------------------------> closed
```

The direct `requested -> closed` transition covers refusal. Expiry, revocation,
interface withdrawal, terminal source completion, or exhausted source failure may
close an active subscription directly. `degraded` is not a lifecycle state:
`sensorium-interface-subscription-status.v1` carries an orthogonal
`health/status = ready | degraded` plus a bounded typed reason while lifecycle state
remains `active`. A closed status carries exactly one terminal reason.

Every transition has an actor, timestamp, reason, causal context, and immutable
execution receipt where P081 requires one. Descriptor and lifecycle facts are
durable host-owned metadata. Live frames and cursors are ephemeral unless a source
contract explicitly gives them a bounded replay window. After an `end` frame, the
same subscription id returns the immutable closed status and cannot become active
again.

### 6. Pull-Batch Is the Mandatory V1 Flow-Control Profile

The semantic core defines exactly one v1 delivery profile: bounded cursor-based
pull or long-poll. It does not promise a permanently open lossless socket:

1. the consumer requests the next batch with frame, byte, and wait caps;
2. the provider returns immediately when data exists or waits only up to
   `wait/max-ms`;
3. the result offers `cursor/next` as the resume point after the complete batch;
4. after accepting the complete batch, the next request supplies the subscription
   id, that value as `cursor/after`, and fresh caps; this step acknowledges progress;
5. no request means no producer-side accumulation beyond the declared replay or
   latest-state buffer.

This is natural backpressure and maps directly to the existing Interaction Broker
watch contract. HTTP long-poll and authenticated peer calls expose it directly. An
SSE, WSS, or Room adapter may present results as a stream, but the adapter owns a
bounded loop that repeatedly calls the same read-next operation, retains the current
cursor, and stops with the lease. It does not introduce provider push, a second
subscription state machine, or a second recovery contract.

`channel_json` observer events remain source-side ingress hints from supervised
adapters to the host. They are not a Sensorium Interface egress profile. A future
acknowledged provider-to-consumer push protocol requires measured latency evidence
and a separate proposal.

The first Room projection is WSS-backed and restricted to `latest-state`. A shared
best-effort fan-out cannot maintain an independent ordered-event cursor for each
member. Ordered events therefore use direct pull-batch until a future carrier owns
per-consumer acknowledgement. A WSS Room pump may coalesce intermediate snapshots;
the next complete snapshot repairs presentation without pretending that a dropped
carrier event was delivered.

P070's future relocatable relay does not change that semantic boundary. Its
`(relay/epoch, relay/seq-no)` cursor belongs to the carrier and may replay a bounded
recent delivery or detect that the carrier window was lost. It is never the private
Sensorium source cursor. After relay failover or `cursor-expired`, the P082 adapter
opens or continues its host-owned source subscription and emits the current complete
latest-state snapshot; it does not claim ordered Sensorium replay.

No v1 carrier is lossless. If lossless retention is a domain requirement, the source
must create an explicit durable artifact or admitted fact under its own policy.

### 7. Cursor, Overflow, and Diagnostics

The opaque cursor is intentionally batch-level. It reuses Interaction Broker source
semantics and supports provider-side coalescing, downsampling, and source-generation
changes without exposing implementation offsets. It is useful for both delivery
semantics, but with different promises: `latest-state` uses it only for change
detection, while `ordered-events` uses it for bounded replay. `frame/seq` and
per-frame cursors would duplicate that contract and are therefore absent in v1.

`latest-state` and `ordered-events` have different correct behavior:

| Semantics | Buffer | On pressure | Resume |
|---|---|---|---|
| `latest-state` | exactly one current complete snapshot per source generation | replace the prior state and increment coalesce count | return the latest snapshot; no historical replay |
| `ordered-events` | bounded event window | emit a typed gap or close; never silently skip | replay from cursor if retained, otherwise report `cursor-expired` |

For `latest-state`, a cursor matching the current snapshot produces `no-change`
until the wait bound expires or the value changes. An older cursor from the same
source generation returns the current complete snapshot. A cursor from another
source generation returns `cursor-mismatch`; `cursor-expired` is reserved for an
`ordered-events` replay point that has left the retained window.

Examples:

- current temperature and current terminal screen are `latest-state`;
- terminal lifecycle events and threshold-crossing sensor events are
  `ordered-events`;
- a high-frequency raw sample stream should usually be aggregated in its adapter and
  exposed as latest state or bounded summaries, not pushed through Agora or Room as
  every raw sample.

Overflow policy remains explicit rather than using an ambiguous `gap-or-close`:
`coalesce-latest` is valid only for latest state; `emit-gap` and
`close-subscription` are valid only for ordered events. The descriptor fixes the
choice so two implementations cannot react differently to the same pressure.

Each read result carries bounded source diagnostics such as `coalesced/count` and
`gap/count`. Carrier adapters separately expose operator counters for queue depth,
`dropped/count`, and `last-drop/at`, because a drop after result creation is not a
source fact and must not be forged into the batch. Diagnostics contain counts,
timestamps, and typed reasons, never payload fragments or subject identities.

### 8. Authorization and Caller Binding Stay Above Transport

Authorization uses the authenticated caller established by the host, never an id
from the request body, URL, Matrix sender, or Room frame.

Local access:

- a supervised module receives a host-owned capability grant bound to its module
  identity;
- `channel_json` session attachment authenticates the module process but grants no
  Sensorium capability by itself;
- an operator control token authorizes only the operator surfaces defined by local
  policy, not arbitrary participant or remote-subject impersonation.

Cross-node access:

- a signed Capability Passport or equivalent source-authorized grant binds the
  remote subject, capability id, `interface/id`, operations, expiry,
  classification ceiling, and rate/volume caps;
- the source node verifies current issuer authority, signature, revocation,
  participant restrictions, and local egress policy at admission and re-checks
  revocation at every bounded batch;
- a Passport does not make the interface globally discoverable and does not bypass
  source-side policy.

Room access:

- current Room membership and the `observe` right are necessary but not sufficient;
- the caller must also hold an interface-scoped grant;
- `RoomLiveTransport::subscribe(room_id)` is a carrier call and must occur only after
  host authorization;
- member removal updates the pump's authorized recipient set before the next batch
  emission and prevents further projection to that subject; the pump's source lease
  remains host-owned until Room/session closure or the recipient set becomes empty;
- until Proposal 075 P075-011 provides Matrix-side kick/ban, Matrix-backed Room live
  transport must not carry private or high-sensitivity interfaces for which a stale
  Matrix member could continue receiving frames.

Session-delegated collaboration grants may be minted only inside a source-operator
pre-authorization envelope. Such a grant binds the interface, collaboration/session,
allowed member set or membership predicate, classification ceiling, limits, and
expiry. Room creation or Agent participation never self-authorizes an interface.

### 9. Classification and Redaction Apply Before Carrier Selection

An interface is an egress surface even when the carrier is local. The source
projection computes effective classification and redaction before any frame enters a
carrier queue.

Required rules:

- the descriptor defines a maximum classification ceiling and redaction profile;
- the descriptor carries a stable bounded `classification/topic-class` used to
  bind any interface-specific declassification authority;
- each frame carries the actual effective `classification.v1` value;
- the grant may narrow the ceiling but cannot widen the descriptor or source value;
- terminal sharing defaults to the bounded visible viewport snapshot; a full
  transcript requires the existing explicit classified capture path;
- invasive connectors retain their existing active-status, consent, and UI
  visibility preconditions;
- a carrier adapter never strips, rewrites, or infers classification;
- redaction or transformation evidence alone never lowers `effective_tier`;
- public projection must satisfy `bound_subjects` public-projection rules before
  serialization;
- wider-than-federation exposure follows the escalation discipline in
  [Swarm Communication Exposure Modes](../20-memos/swarm-communication-exposure-modes.md), not a
  transport shortcut.

#### Interface Is a P047 Declassification Surface

Before the P082 schemas are frozen, Proposal 047 and the shared classification core
MUST extend the closed `DeclassifyFact.surface` vocabulary with wire value
`interface` (`Surface::Interface` in the Rust projection). Reusing `bus`, `export`,
or the selected carrier surface would couple classification authority to transport
and would let an act intended for another boundary authorize an interface
accidentally.

An emitted frame may carry `effective_tier` lower than `source_tier` only when its
trail contains a currently valid `DeclassifyFact` whose:

- `surface` is `interface`;
- `topic_class` equals the immutable descriptor's
  `classification/topic-class`;
- subject, step, mode, expiry, revocation, and one-shot consumption satisfy P047;
- caller and capability evidence pass the existing `memarium.declassify` gate.

The interface guard re-evaluates that fact for every bounded batch before carrier
selection. A fact for Agora, Whisper, INAC, export, or bus does not match. Without a
matching interface fact, the frame keeps `effective_tier = source_tier`; a redaction
profile may still remove content, but it cannot silently declassify it.

### 10. Retention and Capture Are Separate Decisions

Watching a stream does not archive it. Interface runtime persists only:

- descriptor and private source binding;
- grants and revocations;
- subscription lifecycle facts;
- bounded counters and terminal diagnostics;
- P081 execution receipts and references to domain outcomes.

Payload frames remain ephemeral unless the source domain already retains them for a
declared replay window. Explicit capture follows an existing domain path:

- Workbench creates a classified capture artifact;
- Sensorium admits a selected observation or summary;
- Artifact Delivery moves a large immutable value by reference;
- Memarium admission is a separate, auditable policy decision.

The read-only interface cannot silently turn observation into durable capture.

## Carrier Adapters

The contract family is transport-neutral, but the first implementation is staged so
the adapter inventory does not become the acceptance scope accidentally.

| Surface | Role | V1 posture | Important boundary |
|---|---|---|---|
| host capability call | local read and pull-batch | core | authenticated module/actor binding comes from the host |
| authenticated peer session | direct node-to-node read and pull-batch | core remote | remote context and actor claims remain evidence until locally bound |
| HTTP long-poll or SSE | local UI projection | thin V1 adapter | adapter loops over read-next; SSE is not a second protocol |
| WSS-backed Room | collaborative latest-state fan-out | first live adapter; relocatable relay is post-MVP P070 work | membership plus interface grant; ordered events are refused; relay cursor never exposes source cursor |
| Matrix-backed Room | optional Room bridge | deferred for private/high-sensitivity data | requires P075-011 carrier-side eviction before sensitive use and imports no Matrix history/state semantics |
| `channel_json` RPC | supervised middleware caller | reuse when needed | invokes the same host capability dispatch; attachment grants no interface authority |
| `channel_json` event | source-side ingress hint | not an interface carrier | drop-and-count belongs to observation admission diagnostics |
| Artifact Delivery | large immutable payload indirection | reuse by reference | not a stream and not interface authority |

For WSS-backed Room, the payload is the canonical JSON serialization of one
`sensorium-interface-read-result.v1` under the registered content type
`application/vnd.orbiplex.sensorium-interface-read-result+json`. The pump projects
its internal subscription result as `delivery/kind = one-shot` and omits the source
`subscription/id` and cursor. Room sequence numbers remain carrier sequence. Room
consumers neither observe nor advance the host-owned source cursor.

The pump does not rewrite a source `batch/outcome = terminal` into a one-shot
terminal result, because that would violate the read-result discriminator. Instead,
it closes the dedicated interface-projection carrier session with the bounded typed
terminal reason from the source subscription. The durable Room remains open. A
`no-change` batch keeps the projection session open, so consumers distinguish
quiescence from termination by carrier-session closure. Reopening the view creates a
new source subscription. A Room carrier that cannot close only the projection
session MUST fail readiness rather than stop emitting silently or close an unrelated
Room.

### Vendor Media Type Registration

The repository already uses Orbiplex vendor media types for Inquirium transcript
facts and Sensorium virtual-environment exports, so this is not the first
`application/vnd.orbiplex.*` value. It is, however, the point at which their naming
must stop being ad hoc.

Before the first P082 carrier ships, Protocol ownership MUST provide one checked-in,
machine-validated vendor media-type inventory. Each entry binds a unique media type
to a schema ref, encoding, and owning proposal/component. The initial P082 entry is:

```text
application/vnd.orbiplex.sensorium-interface-read-result+json
  schema/ref: urn:orbiplex:schema:sensorium-interface-read-result:v1
  encoding: canonical-json
  owner/ref: P082
```

This inventory is build-time protocol data, not network authority and not a ninth
Sensorium envelope. Duplicate names or one name bound to multiple schemas fail
validation. Existing Orbiplex vendor media types should be backfilled into the same
inventory rather than preserved as parallel conventions.

## Host-Owned Runtime Reuse

### Interaction Broker

Use Interaction Broker probe/watch as the first read and subscription engine. It
already owns source-bound opaque cursors, event and byte caps, deadlines, wait/watch
lifecycle, replay bounds, and source-provider dispatch. Sensorium Interfaces should
add a source provider and projection policy, not another watch registry. The broker
owns bounded source reads; the interface runtime owns publication and subscription
authority. Their states are composed rather than copied.

### Replay Scheduler

Use Replay Scheduler only when the underlying adapter is pull-only and the host must
periodically enact a new observation. The scheduled job invokes a bounded adapter
operation and submits the result through Sensorium admission. It does not own
subscriptions and does not write interface frames directly.

### Bounded Deferred Operations

Use Bounded Deferred Operations for publication, remote subscription setup, capture,
or cleanup that may legitimately outlive one request. Do not create one deferred
operation per frame. A subscription is its own leased state machine, while a
deferred operation may own a bounded transition that creates or closes it.

### `channel_json`

Use `channel_json` for supervised adapter-to-host observation events and
host-to-module bounded calls. Its outer frame is executor transport, not the
Sensorium Interface domain envelope. Embedded payloads remain schema-gated. Observer
queue loss must surface as source-ingress diagnostics and must not be mistaken for
an ordered interface stream or repaired by inventing an interface cursor.

### Artifact Delivery

Use Artifact Delivery for values that exceed inline caps, require asynchronous
delivery, or must be immutable and independently admitted. The interface frame
carries an artifact ref and classification, while Artifact Delivery retains route,
transport, and recipient admission semantics.

The implemented `artifact-snapshot` adapter accepts only a read-only
`latest-state` interface bound to an admitted `artifact-object-pointer.v1`. Each
read pins the requested admission id to the returned accepted admission record,
requires its artifact ref, and includes the admission schema, digest, receipt time,
and source generation in cursor change detection. The interface publisher supplies
the explicit frame classification, which is still checked against descriptor and
current declassification constraints; the interface frame does not grant Artifact
Delivery fetch authority. The private admission id is selected by the local
`sensorium.interface.manage` publisher, not supplied by a reader. Publication is
therefore an explicit local reprojection of an accepted pointer; Artifact Delivery
does not need a second admission-to-interface binding, while consumers still need
the exact interface grant and separate Artifact Delivery fetch authority where
dereferencing is allowed.

### Temporal Storage and P081

Append publication, grant, subscription, revocation, and terminal facts through the
Temporal Storage Convention. Use canonical P081 contexts and selective receipts at
authority boundaries, delivered result batches when they are external effects,
retries/cancellations, and terminal states. Do not create a global interface event
log, per-frame receipt stream, or duplicate source-domain facts.

## End-to-End Examples

### Temperature Sensor: On Demand

```text
1. A supervised adapter reads the physical sensor through its connector.
2. The adapter submits a bounded sensorium-observation.v1 through channel_json.
3. Sensorium Core validates, classifies, and admits the observation.
4. The source operator publishes a latest-state interface bound to that query.
5. An authenticated consumer calls sensorium.interface.read with interface id,
   deadline, and caps.
6. The host verifies the resource-scoped grant and egress policy.
7. The interface provider queries Sensorium Core and returns one classified result
   batch.
8. The host appends the selective P081 receipt and returns the result.
```

No remote party calls the sensor connector. If the sample is stale, the response
contains freshness and a typed stale/source-unavailable outcome according to source
policy; it does not silently perform unbounded external work.

### Temperature Sensor: Continuous Updates

```text
1. A push-capable adapter emits observation candidates as values change and
   Sensorium admits them; or a Replay Scheduler job polls a pull-only sensor at a
   bounded interval and submits each candidate through the same admission path.
2. The interface projection coalesces observations into latest state.
3. The consumer creates a five-minute pull-batch subscription.
4. Repeated bounded long-polls return only new snapshots and batch cursor progress.
5. A local SSE adapter owns that read-next loop and projects each result batch as an
   SSE event; a peer session can expose the pull contract directly.
6. Missing demand causes no unbounded queue; the provider retains only latest state.
7. Expiry or revocation closes the subscription and emits a terminal receipt.
```

### Workbench Terminal: Collaborative Live View

```text
1. Workbench owns the PTY and produces bounded screen snapshots.
2. The operator publishes a latest-state interface for the visible viewport only.
3. A collaboration session instantiates temporary interface grants for authorized
   Room members inside the operator's pre-authorized envelope.
4. Interaction Broker watches the Workbench terminal provider with bounded caps.
5. One bounded WSS Room pump repeatedly pulls the latest-state interface and
   projects each batch as a cursor-free one-shot result in room-live-message.v1.
6. Slow consumers receive coalesced current screen state, not an unbounded backlog.
7. Reconnect receives the next complete snapshot emitted by the pump; Room members
   do not own the pump's source cursor.
8. Member removal revokes that member's projected access. The host-owned pump closes
   when its source subscription terminates, the Room/session ends, or no authorized
   recipients remain. Source termination closes the dedicated projection carrier
   session without closing the durable Room; carrier eviction follows independently.
```

Keyboard input is not sent through this observation stream. It remains a separately
authorized `sensorium-workbench-tool-request.v1` directive in the implemented V1
path. [Proposal 083](083-sensorium-interactive-interfaces.md) preserves that
observation/action boundary while defining a future, separately granted and fenced
actuation interface for collaborative terminal control.

## Error Contract

This proposal freezes a small transport-neutral error vocabulary:

| Code | Meaning | Retry posture |
|---|---|---|
| `interface/not-found` | resource absent or leak-minimal unauthorized lookup | no, unless descriptor may appear later |
| `interface/not-published` | suspended, withdrawn, or expired | no until state changes |
| `interface/unauthorized` | bound caller lacks current scoped authority | no without new authority |
| `interface/classification-denied` | egress or grant ceiling refuses the value | no without narrower projection/policy change |
| `interface/source-unavailable` | provider is unavailable or not ready | bounded retry with backoff |
| `interface/deadline-exceeded` | read/watch exceeded caller or host deadline | retryable when policy allows |
| `interface/cursor-expired` | requested replay point is outside retention | request a fresh snapshot or close |
| `interface/cursor-mismatch` | cursor belongs to another interface/source epoch | no; caller must discard cursor |
| `interface/overloaded` | bounded admission or worker capacity is full | retry after supplied delay |
| `interface/schema-mismatch` | provider output violates declared schema | no automatic retry; operator fault |
| `interface/revoked` | grant or collaboration authority was withdrawn | no without new grant |
| `interface/subscription-closed` | the lease is terminal and its immutable status is available | no; create a new subscription when authorized |

These detailed reasons are internal machine and audit vocabulary. A remote boundary
may project `not-published` to `not-found`, and `classification-denied` or `revoked`
to `unauthorized`, when disclosure would reveal protected state. The trace retains
the detailed local reason. Carrier failures are normalized separately and never
replace domain errors.

## Trade-offs

- Pull-batch is less visually immediate than a raw firehose, but it provides natural
  backpressure, cursor recovery, and transport portability. SSE or WSS Room can
  restore low-latency presentation through an adapter-owned pull loop without
  changing the core contract.
- A provider-defined opaque cursor is less transparent than a numeric sequence, but
  it directly reuses Interaction Broker, supports aggregation and source epochs, and
  eliminates per-frame delivery counters.
- One interface per projected meaning creates more descriptors, but avoids optional
  mode matrices and permits precise grants and classification. UI may group related
  interfaces without turning that grouping into authority or a multi-output wire
  contract.
- Explicit publication and grants add operator work, but make observation visible,
  revocable, auditable, and explainable.
- Descriptor immutability includes `expires/at`. Extending an interface therefore
  publishes a new `interface/id`, invalidates the old subscriptions, and requires
  fresh grants. This creates deliberate identity churn and operator work, but
  prevents routine renewal from becoming an invisible path to indefinite
  observation. A future stable-id renewal profile would require a separate bounded
  lease contract and must not be smuggled in as descriptor mutation.
- Best-effort live carriers cannot promise lossless delivery. The alternative would
  be a durable event platform whose retention and authority semantics are far larger
  than this feature.
- Reusing Interaction Broker may require one new source variant and provider adapter,
  but avoids a second cursor, watch, and timeout subsystem.

## Failure Modes and Mitigations

| Failure mode | Consequence | Mitigation |
|---|---|---|
| Interface id treated as a secret bearer token | unauthorized observation | authenticated caller binding plus resource-scoped authorization |
| Connector exposed directly | policy and classification bypass | host-private source binding and provider-only access |
| Capability id minted per sensor | registry explosion and coupled policy | generic operation capabilities scoped to interface resources |
| Room or Matrix membership treated as authority | carrier controls access | host checks current Room and interface grants before subscription |
| Slow consumer creates unbounded backlog | memory exhaustion and stale view | pull-batch default, explicit caps, coalesce/gap/close policy |
| Carrier projection treated as a second stream protocol | divergent lifecycle and recovery | adapter owns one bounded loop over canonical read-next |
| P047 declassification for another surface reused by an interface | unintended disclosure | require `surface = interface` and exact descriptor topic-class binding per batch |
| `sensorium.read.local` treated as caller authority | source-policy bypass or duplicate grants | keep it inside the Sensorium source adapter and compose it with interface authorization |
| Room pump stops without a terminal signal | consumers confuse termination with quiescence | close only the dedicated projection carrier session with a typed reason |
| Vendor media type coined ad hoc | incompatible carrier dispatch | validate one checked-in unique media-type inventory |
| Source observation event dropped in `channel_json` | stale admitted source view | source-ingress drop counter and freshness diagnostics; no forged delivery gap |
| Cursor reused after source restart | wrong replay or reordered data | bind opaque cursor to interface and source generation |
| Revocation described as retracting old data | false safety guarantee | stop only future emissions; document delivered-data boundary |
| Stream silently becomes durable | privacy and retention drift | explicit capture/admission operation only |
| Large frame blocks shared transport | head-of-line pressure | strict inline cap and Artifact Delivery ref |
| Interface runtime duplicates domain store | divergent facts | retain only descriptor/lifecycle metadata; source domain owns values |
| Adapter-specific code accumulates in daemon | closed and fragile architecture | one interface provider registry and source-specific adapters |

## Implementation Strata

```text
protocol contracts
  immutable descriptor, interface/subscription status, read result batches,
  subscribe/command requests, frames, typed errors

sensorium-interface core
  pure validation, lifecycle transitions, batch cursor/source binding,
  delivery-policy decisions, classification no-broadening checks

domain source adapters
  Sensorium observation query, Workbench terminal screen/events,
  Artifact snapshot; no transport knowledge

host runtime
  authenticated caller binding, grant verification, provider registry,
  Interaction Broker composition, lease state, temporal facts, receipts

carrier adapters
  host capability and peer pull-batch; HTTP/SSE and WSS Room projections;
  channel_json source ingress and AD payload indirection; no domain authority

UI and operator surfaces
  publish/suspend/withdraw, grant/revoke, list active subscriptions,
  inspect bounds, gaps, drops, and terminal reasons
```

The schema gate validates ingress and egress contracts. The pure core must not depend
on daemon, HTTP, WebSocket, Matrix, SQLite, async runtime, or a concrete Sensorium
provider. Runtime stores may use SQLite/Temporal Storage, but the protocol does not
encode that choice.

## Named Acceptance Invariants

- `inv-sif-single-delivery-contract`: providers expose only bounded read-next;
  SSE, WSS, and Room presentation is implemented by adapter-owned pull loops, not a
  second push protocol.
- `inv-sif-batch-cursor-only`: only requests and result batches carry interface
  cursors; frames carry neither a cursor nor an interface-local sequence number.
- `inv-sif-cursor-not-authority`: cursor possession without an authenticated caller,
  matching interface, live lease where required, and current grant is refused.
- `inv-sif-end-is-terminal`: `end` is the final frame of the final batch; the
  subscription remains closed and returns its immutable terminal status afterward.
- `inv-sif-latest-state-has-no-replay`: a `latest-state` descriptor rejects replay
  bounds, retains one current complete snapshot, and uses its cursor only for change
  detection.
- `inv-sif-classification-match`: every emitted frame carries `classification.v1`;
  when its payload also embeds the label, the two values are structurally equal.
- `inv-sif-interface-declassification-only`: a frame whose effective tier is lower
  than its source tier has a currently valid P047 fact bound to `surface = interface`
  and the descriptor's exact classification topic class.
- `inv-sif-source-policy-composes`: `sensorium.read.local` source admission and
  interface caller authorization are both required for an observation-query source;
  neither grant satisfies the other.
- `inv-sif-independent-byte-caps`: every frame satisfies `frame/max-bytes` and every
  complete result satisfies `batch/max-bytes`; neither cap is inferred from the
  other.
- `inv-sif-carrier-not-authority`: transport attachment, Room membership, Matrix
  identity, and interface id possession never replace resource-scoped admission.
- `inv-sif-room-v1-latest-state-only`: the first WSS Room adapter refuses
  `ordered-events` interfaces and never exposes a per-member source cursor.
- `inv-sif-room-terminal-visible`: source subscription termination closes the
  dedicated Room projection carrier session with a typed reason; `no-change` does
  not close it, and the durable Room is not closed as a side effect.
- `inv-sif-revocation-lag-bounded`: revocation prevents new source reads and carrier
  emission within configured local pull-loop and peer revocation-freshness budgets,
  without claiming that revoke transaction duration measures that lag or that
  previously delivered data can be erased.
- `inv-sif-registered-media-type`: every Orbiplex vendor media type used by a P082
  carrier has one unique checked-in binding to its schema and encoding.
- `inv-sif-source-adapter-open`: source-specific validation and batch production
  live behind the bounded adapter registry; persisted bindings are revalidated on
  every read, and an unknown or unavailable adapter cannot be bypassed after restart.
- `inv-sif-operator-evidence-bounded`: read metrics use only bounded source-kind,
  carrier, and delivery-kind dimensions; flat revoke-commit and resource-count
  metrics never carry caller, grant, subscription, or interface ids.

## Frozen Initial Decisions

The design questions are resolved as of 2026-07-17. Decisions 1-6 freeze the V1
baseline; decisions 7-9 close the evidence-gated follow-up review:

1. P082 is the dedicated home for Sensorium Interface semantics; P045 retains local
   Sensorium admission and actuation.
2. Implementation order is authenticated direct pull-batch, then local SSE and
   WSS-backed Room latest-state projection. Provider push is not a V1 protocol.
3. Cross-node authority reuses Capability Passport with interface-specific scope;
   for direct pull, `node_id` names the authenticated remote consumer and
   `issuer/node_id` names the local source node. Local grants remain host-owned
   runtime facts.
4. Remote descriptors are disclosed only through a direct grant/invitation or an
   authorized collaboration context. There is no federation-wide catalog in V1.
5. Every frame carries `classification.v1`; a payload copy, when present, is
   structurally equal. Generic carriers do not learn schema-specific JSON pointers.
6. V1 has one source-local `sensorium.interface.manage` capability with
   action-specific policy and distinct publish/grant/revoke/withdraw facts. It is
   never remotely delegated.
7. Bounded pull-batch remains the only data-delivery protocol. No separately
   acknowledged provider-push or push-hint profile is added. If operational evidence
   later justifies readiness hints, P082 data readiness and P083 claim readiness must
   reuse one authority-neutral, disclosure-bounded notification substrate rather than
   define two push mechanisms. Each hint audience must pass the same current grant
   and applicable collaboration-policy checks as the corresponding read or claim; a
   hint neither confers authority nor reveals resource activity to an unauthorized
   recipient.
8. There is no searchable descriptor catalog. Listing resources already disclosed by
   the caller's own current grants, invitations, or collaboration context is
   authority inspection, not existence discovery, and must preserve leak-minimal
   `not-found` behavior. A searchable inventory that reveals otherwise undisclosed
   resources is a separate disclosure oracle and requires a new decision.
9. `sensorium.interface.manage` remains one source-local, non-delegable capability.
   Current runtime dispatch and capability-authorization policy enumerate the closed
   observation and P083 actuation action vocabulary, including `control.preempt`;
   wildcard or capability-only admission cannot acquire preemption authority.

## Implementation Tracker

| Id | Work item | Status | Acceptance boundary |
|---|---|---|---|
| P082-001 | Freeze the proposal architecture, V1 decisions, bounds, named invariants, and implementation order | done | This document records the frozen resource/capability split, one pull-batch contract, direct-only descriptor disclosure, Passport reuse, classification placement, and local management posture. |
| P082-002 | Extend P047 and the shared classification core with `Surface::Interface` plus exact descriptor topic-class matching | done | `orbiplex-node-classification` implements `Surface::Interface`; tests reject other surfaces, topic mismatch, expiry, revocation, and consumed one-shot facts. |
| P082-003 | Freeze descriptor/interface-status, read request/result, subscribe request/status/command, frame schemas, and typed errors | done | Eight closed schemas plus core semantic validation cover terminal, latest-state no-replay, ordered replay bounds, byte caps, classification equality, conflicting frame payload sources, and unknown-field refusal. |
| P082-004 | Register `read`, `subscribe`, and local `manage` with the exact flags and authorization-policy posture frozen above | done | Machine registry, Rust constants, policy sidecar, and human registry agree; only read/subscribe are Passport-eligible and generic advertisement exposes no descriptor. |
| P082-005 | Seed a shared checked-in Orbiplex vendor media-type inventory and register the P082 read-result type | done | `vendor-media-types.v1` binds the P082 read-result media type uniquely and is validated by protocol/schema-gate tests. |
| P082-006 | Implement the pure lifecycle, batch-cursor binding, delivery-policy, classification, and limit core | done | `sensorium-interface-core` has no daemon, transport, SQLite, async-runtime, or concrete provider dependency and proves the named semantic invariants. |
| P082-007 | Add schema-gate families and positive/negative fixtures | done | Schema-gate embeds all eight schemas and validates positive, cross-field-negative, and unsupported-boundary fixtures. |
| P082-008 | Add one Sensorium Interface source to Interaction Broker and its provider registry | done | The daemon registers the `sensorium-interface` source kind and reuses broker watch cursors, deadlines, and caps. |
| P082-009 | Adapt admitted Sensorium observations with conjunctive `sensorium.read.local` and interface authority checks | done | Sensorium observation binding preserves source admission and independently checks interface authority; temperature one-shot and subscription tests pass. |
| P082-010 | Adapt Workbench terminal screen snapshots and ordered event batches | done | Workbench screen latest-state and terminal ordered-events are separate source bindings with separate descriptor semantics. |
| P082-011 | Add host publication, grant, subscription, revocation, and inspection surfaces | done | The daemon runtime persists immutable management facts, idempotency, grants, subscriptions, terminal states, and restart-rebuildable projections. Grants require canonical namespaced grantee refs; cursor advancement is serialized per subscription, while independent subscriptions may read concurrently; verified Passport admission is one immediate atomic transaction with explicit revoked-replay diagnostics. |
| P082-012 | Add local host-capability and authenticated direct-peer pull-batch surfaces | done | Host dispatch and peer message-chain tests verify caller binding, signed `sensorium-interface@v1` Passport scope, exact remote target and local source issuer, resource limits, and current revocation. |
| P082-013 | Add local SSE and WSS-backed Room latest-state adapters | done | Loopback module-authenticated SSE and WSS Room projection use adapter-owned read-next loops with carrier-specific causal ids, current grant checks, typed close, ordered-event refusal, and no durable Room close. Room recipients match canonical stable subject keys only; the adapter caps active pumps at 64 and reaps terminal pump and carrier state together. |
| P082-014 | Add named-invariant tests plus temperature and Workbench end-to-end acceptance flows | done | Focused core/runtime tests cover temperature one-shot and continuous flows, restart, revocation, concurrent and revoked Passport replay, canonical grantee refs, tier-vocabulary alignment, frame schema negatives, carrier-specific traces, and subscription lock isolation; peer, SSE, and real WSS tests cover signed remote target binding and collaborative terminal view. |
| P082-015 | Synchronize P024, P042, P045, P047, P066, P070, P071, P072, P075, P080, P081, Solutions 030/035/042, Node ledgers, and applicable readiness tracking | done | Solution 046 owns the implemented boundary. P024/P045/P047/P069/P070/P071/P072/P081 and Solutions 030/035/036/042 carry the applicable explicit cross-links; P042/P066/P075/P080 were reviewed and retain non-competing owner semantics. Node MVP/implementation ledgers, capability registries, generated solution/schema views, and the readiness snapshot are synchronized. |
| P082-016 | Replace the closed source-binding enum with an open, bounded source-adapter registry and migrate the Sensorium and Workbench adapters | done | Generic host-private bindings are shape-bounded and revalidated after restart; duplicate, unknown, unready, and excess adapters fail closed, daemon startup requires all four built-ins, and point-in-time readiness never replaces authoritative `next_batch` refusal. |
| P082-017 | Add the Artifact Delivery-backed immutable snapshot adapter | done | `artifact-snapshot` emits only an accepted `artifact-object-pointer.v1` ref through a read-only latest-state interface, pins admission identity, redacts AD-host failures, preserves classification checks, and uses stable digest-bound cursor change detection; local manage authority deliberately selects the private admission binding. |
| P082-018 | Expose bounded operator evidence for source readiness, carrier reads, occupancy, no-change, errors, active leases, Room pumps, and local revoke commit duration | done | The host-local manage `metrics` action reports no actor, interface, grant, or subscription identifiers; read dimensions are capped by 64 registered source kinds, four carrier classes, and two delivery kinds, while `revoke-commit-us` remains flat. Source-registry, active-subscription, metric-accumulator, and Room failures degrade independently; counters are process-local and reset on restart. |
| P082-019 | Add and run the host/direct-peer/SSE/Room conformance and load harness, then synchronize solution and readiness artifacts | done | `node:tools/conformance/sensorium_interfaces_conformance.py` prebuilds daemon/core plus the required Workbench contract bridge with a separate build timeout, uses exact full Rust test names with one test thread, fails fast by default, distinguishes build/test timeouts and unrecognized libtest output, emits only output digests on failure, and now extends the original bounded host, signed peer, SSE, and Room observation checks with the P083 load, restart, partial-failure, Room baton, and real Workbench PTY matrix. |
| P082-020 | Make the Room latest-state adapter relay-epoch-aware after P070 Phase 6A | deferred post-MVP | Reconnect uses only `(relay/epoch, relay/seq-no)` carrier state, never a source cursor; epoch change or expired carrier replay refreshes one current complete snapshot after rechecking Room membership and interface grant. This item does not reopen or block the completed P082 hard-MVP contract. |

## Open Questions

No unresolved design questions remain. The former provider-push, descriptor-catalog,
and management-capability questions are resolved by decisions 7-9. Any later change
requires operational evidence and an explicit contract revision.

## Next Actions

1. Collect representative local and federated snapshots from the implemented
   `metrics` action and compare read-next latency, occupancy, and no-change rate by
   carrier, delivery kind, and source kind. Inspect the flat `revoke-commit-us`
   cost separately; measure end-to-end enforcement at carrier and peer authority
   boundaries rather than inferring it from durable-write latency.
2. Add another producer adapter only through the implemented source-provider and
   classification contracts.
3. Keep pull-batch, direct disclosure, and one source-local manage capability as the
   baseline. Treat any future push, existence-discovery, or authority-split proposal
   as an explicit contract revision with operational evidence.
4. Implement P082-020 only through P070 Phase 6A; do not add an Interface-specific
   relay, membership service, or failover protocol.
