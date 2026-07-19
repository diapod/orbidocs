# Proposal 083: Sensorium Interactive Interfaces

Based on:

- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/045-sensorium-local-enaction-stratum.md`
- `doc/project/40-proposals/047-classification-label-propagation.md`
- `doc/project/40-proposals/048-sensorium-os-connector-action-classes.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/071-sensorium-workbench.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/40-proposals/082-sensorium-interfaces.md`
- `doc/project/60-solutions/030-sensorium/030-sensorium.md`
- `doc/project/60-solutions/036-room/036-room.md`
- `doc/project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md`
- `doc/project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md`

## Status

Accepted design / implementation complete and promoted to Solution 046.

This proposal is the completed hard-MVP release-blocking extension of the implemented
read-only Sensorium Interfaces V1 contract. P083-002 through P083-011 implement the shared
resource and schema layer, capability and Passport scope, pure coordinator, durable
host runtime, bounded LED adapter, host/direct-peer carrier boundary, and Workbench
terminal adapter, bounded operator/Room collaboration surface, full load/restart/
partial-failure/real-PTY conformance, and cross-document synchronization. P083-012
records the clean final authority and correctness review and promotes that actuation
boundary into Solution 046. Proposals 082 and 083 remain the observation and actuation
rationales; Solution 046 owns their combined implementation boundary.

## Date

2026-07-17

## Executive Summary

Sensorium Interfaces currently lets an authorized client observe an explicitly
published, bounded representation. Some enacted resources also have a meaningful
input surface: a client may set an LED, move an actuator, resize a terminal, or
send bytes to a Workbench-owned PTY. Treating every such input as a producer-
specific remote API would duplicate resource naming, grants, classification,
revocation, carrier binding, receipts, and lifecycle handling.

This proposal adds an actuation plane without weakening the observation/action
boundary:

```text
one enacted target
  -> one or more observation interfaces
  -> one or more actuation interfaces
```

Observation and actuation remain separate interface resources with separate
capabilities, grants, schemas, limits, and lifecycles. They may be grouped around
one host-private target, but an observation grant never implies actuation and an
actuation grant never implies observation.

An actuation interface selects one coordination mode at publication time:

- `shared`: multiple authorized callers may submit operations; the host accepts
  concurrent submissions but establishes one total accepted and effect order; or
- `exclusive-lease`: a grant makes a caller eligible to request control, while one
  short-lived control lease gives exactly one caller current write authority.

The exclusive lease is a host-owned, fenced baton. Every accepted exclusive
operation binds the exact interface, caller, source generation, lease id,
monotonically increasing lease epoch, sequence number, and current grant. Shared
operations bind the same resource, caller, generation, sequence, and grant without
lease fields. Expiry, handoff, preemption, revocation, source restart, or interface
withdrawal makes stale operations fail closed.

Workbench terminal observation remains a P082 read/subscription flow. Keyboard
input, resize, and signals use a separate P083 actuation interface backed by the
Workbench authority boundary. Terminal input defaults to `exclusive-lease`; Room
membership and the observation carrier never confer control.

## Context and Problem Statement

The implemented P082 contract deliberately excludes commands from its read and
subscription lanes. That separation is correct, but it does not imply that every
remote actuation surface should be designed independently.

Several resources need both directions under different authority:

- many clients may observe one Workbench terminal while only one client types;
- many clients may be allowed to request `led.set`, where serialized shared writes
  are sufficient;
- a robot or laboratory actuator may expose public telemetry but restrict control
  to one operator at a time;
- an authorized client may resize a terminal without receiving permission to send
  process signals;
- a Room may establish collaboration context while exact interface grants still
  determine who may observe, request control, or invoke a method.

Without a shared actuation contract, each provider must invent its own answers for:

- exact resource and method authority;
- concurrent submission and one total accepted order;
- exclusive ownership, renewal, handoff, expiry, and preemption;
- delayed or replayed packets after ownership changes;
- operation idempotency and uncertain outcomes;
- classification and retention of input payloads;
- carrier disconnects and source restarts;
- immutable causal receipts and bounded operator diagnostics.

The central distinction is between **eligibility** and **current authority**. A
grant says that a caller may invoke a shared interface or compete for an exclusive
lease. For an exclusive interface, only the current control lease authorizes an
effect. Conflating the two would either make grants too transient to administer or
make terminal control last for the full grant lifetime.

## Goals

- Add a transport-neutral actuation contract adjacent to P082 observation.
- Extend the existing P082 core, authority runtime, store, admission, receipt,
  classification, metrics, and conformance boundaries instead of duplicating them.
- Preserve separate least-authority grants for observation and actuation.
- Support shared submission and exclusive time-quantized control without provider-
  specific lock protocols.
- Reject delayed operations from a previous holder with a source-generation and
  lease-epoch fencing contract.
- Make claim queues, leases, payloads, outstanding work, deadlines, and receipts
  explicitly bounded.
- Reuse Capability Passports, P081 causal context and receipts, P047
  classification, Room collaboration context, and existing host policy.
- Let Workbench expose terminal control without presenting a Room, WSS session, or
  observation subscription as command authority.
- Keep concrete device and terminal effects inside their owning Sensorium or
  Workbench adapters.

## Non-Goals

- Merging observation and actuation into one ambient `read-write` grant.
- Direct remote access to connectors, device handles, PTYs, credentials, or private
  source bindings.
- Treating Room membership, carrier attachment, possession of an interface id, or
  an observation cursor as actuation authority.
- A distributed lock service for arbitrary application data.
- A parallel actuation publication, grant, revocation, fact, idempotency, or caller-
  admission service beside Solution 046.
- Concurrent execution of provider effects in the first implementation.
- Exactly-once effects across arbitrary provider crashes.
- Inferring whether an operation is safe from its JSON shape.
- Replacing P048 action classes, Workbench command profiles, or provider-local
  safety policy.
- Making a host-local shell safe without the process isolation required by P071.

## Terminology

- **enacted target**: a host-owned device, session, process, or logical resource
  that produces observations or accepts effects;
- **observation interface**: the implemented P082 read/subscription resource;
- **actuation interface**: an explicitly published P083 resource exposing a bounded,
  closed method catalog in which every method has one exact input schema;
- **actuation method**: a provider-domain effect such as `led.set` or
  `terminal.resize`, named by a descriptor method entry and independently scoped by
  an actuation grant;
- **control operation**: a coordination-plane transition such as `control.claim`,
  `control.cancel`, `control.renew`, `control.release`, or `control.handoff`; it is
  not an actuation method and never appears in the grant's method subset;
- **invoke operation**: one request to apply an exact actuation method with a
  schema-valid payload under current authority and fencing evidence;
- **actuation status**: a leak-minimal, grant-gated read of the current opaque source
  generation plus the caller's own claim/lease state and generic busy hints;
- **actuation grant**: durable, revocable eligibility to invoke an exact interface
  under exact method and limit bounds;
- **Room `actuate` grant**: collaboration-context permission to expose claim/invoke
  UI for a Room subject; it is never an actuation grant or current control authority;
- **control lease**: short-lived current authority for one caller to invoke an
  `exclusive-lease` interface;
- **lease epoch**: a monotonically increasing fencing number within one interface
  source generation;
- **source generation**: an opaque identity that changes whenever provider state is
  replaced or restarted such that prior control evidence is no longer valid;
- **shared mode**: multiple callers may submit operations, while the host still
  serializes acceptance and establishes one effect order;
- **exclusive mode**: exactly one current lease holder may submit effects;
- **operational impact**: a P082-owned ordered caution class attached to the exact
  enacted resource; it describes the consequences of interacting with the target,
  not caller authority or information sensitivity.

## Proposed Model / Decision

### 1. A Duplex Target Is Composed from Directional Resources

The system may present a terminal or device as logically read/write, but the wire
and authority model remains directional:

```text
terminal-session:01...
  observation: sensorium-interface:screen-01...
  observation: sensorium-interface:events-01...
  actuation:   sensorium-interface:input-01...
```

The common target binding is host-private. A remote descriptor or invitation may
disclose related interface ids only when the caller is independently authorized to
discover each resource. A related observation interface is therefore convenient
composition, not proof of actuation authority.

One interface keeps one primary meaning:

- an observation interface has one output schema and one delivery policy;
- an actuation interface has one receipt schema, one coordination mode, and a
  closed method catalog whose every entry binds one method name to one exact input
  schema.

This preserves P082's resource/capability split and avoids conditional grants whose
meaning changes with a request body.

The directional resources for one enacted target inherit the same host-validated
`sensorium-operational-context.v1` value and current `source/generation-ref` unless
local policy raises one direction. A read-only viewport over a production or
critical system remains production or critical: access mode does not make the
represented environment disposable. The actuation descriptor, status, invocation
admission, and receipt projection must therefore retain that context. Host policy
may use it to require stricter review, shorter leases, lower operation caps, or
explicit operator confirmation, but the class itself never grants or denies
authority without such an explicit policy.

When the source context or generation changes, every affected directional
publication is replaced and the old publication becomes stale under P082's
generation-or-supersession predicate. Neither the Room relay nor a direct-peer
carrier may keep an old direction live. A source-side downward correction is an
audited immutable replacement; consumer policy still may not lower the current
source declaration.

### 2. `sensorium.interface.invoke` Is a Separate Capability

The actuation operation class is:

- capability id: `sensorium.interface.invoke`;
- wire name: `sensorium/interface.invoke`;
- surfaces: `host-local`, `federated`;
- dispatchable: true;
- advertisable: true as generic protocol support only;
- Passport eligible: true through a dedicated
  `sensorium-interface-actuation@v1` grant profile;
- signing domain: false;
- host route: true;
- federated discovery: true without ambient descriptor disclosure.

`invoke` is preferred over `write` because input may be an ephemeral command rather
than a durable data write. Capability advertisement exposes no interface, target,
method, grant, lease, queue, or holder.

The same `invoke` authority gates actuation status for one exact granted interface.
Status returns the current opaque `source/generation-ref`, the caller's own claim or
lease state, and generic busy/queue hints; it never exposes another caller's identity
or becomes a searchable descriptor surface.

The existing source-local `sensorium.interface.manage` capability owns publication,
grant administration, withdrawal, operator inspection, and policy-driven
preemption actions for the first implementation. It remains non-delegable. The
authorization-policy entry must enumerate each allowed action explicitly before
`control.preempt` is enabled; possession of an undifferentiated manage grant is not
enough to acquire new preemption authority. Any future split of management authority
requires distinct-principal deployment evidence and an explicit contract revision.

### 3. Publication Freezes the Coordination and Input Contract

An actuation descriptor is explicit, local-only by default, and immutable except
through replacement by a new interface generation. Its public contract contains:

- `interface/id` and `interface/kind = actuation`;
- exact `receipt/schema-ref`;
- a closed non-empty `methods` list whose entries contain exact `method/name` and
  `input/schema-ref` values; each referenced schema is closed and defines one
  canonical payload for that method;
- `coordination/mode = shared | exclusive-lease`;
- payload, rate, per-caller outstanding-operation, per-interface
  outstanding-operation, deadline, and idempotency bounds;
- queue and lease bounds for `exclusive-lease`;
- classification ceiling and optional redaction profile for receipts;
- publication and expiry timestamps;
- safe display metadata that is not used for authorization.

The descriptor does not disclose the connector id, PTY handle, executable,
credential, private target binding, provider token, or source-generation value.
Those remain in a host-private binding validated by the owning adapter before every
effect. After grant admission, an authorized actuation-status response exposes only
a bounded opaque `source/generation-ref`; it carries no provider identity or private
binding and changes whenever stale operations must be fenced.

The caller cannot choose a less restrictive coordination mode in an invoke
request. A grant or current host policy may narrow methods and limits but may not
widen the descriptor.

### 4. A Grant Gives Eligibility, Not Exclusive Possession

An actuation grant binds:

- one canonical namespaced grantee ref;
- one exact actuation interface id;
- capability `sensorium.interface.invoke`;
- a non-empty exact method subset;
- caller and remote-node constraints where applicable;
- classification ceiling;
- maximum payload, rate, per-caller outstanding-operation, and deadline bounds;
- maximum claim wait, lease quantum, and cumulative hold bounds where applicable;
- issuance, expiry, revocation, and authority references.

Empty method or interface sets deny; they are never wildcards. The first grant
profile supports exact method names only. A Capability Passport proves delegated
eligibility, but the source host still admits it into current local authority and
checks current host policy and revocation before every claim and invoke.

One Passport may carry both `sensorium-interface@v1` observation scope and
`sensorium-interface-actuation@v1` actuation scope. Each requested operation must
match one complete profile on that profile's own terms. Interface ids, methods,
limits, node bindings, or classification bounds never combine across profiles.

For `shared`, a current grant plus the current authorized source-generation ref is
sufficient coordination authority. For `exclusive-lease`, a current grant permits
`claim`, queue cancellation, and acceptance of a handoff; an effect additionally
requires the current control lease.

Revoking a grant removes its queued claims, terminates its current control lease,
and refuses not-yet-applied operations. Previously applied effects cannot be
retracted and must not be described as revoked.

### 5. Shared Means Shared Admission, Not Unordered Effects

In `shared` mode, independent authorized callers may submit operations without
claiming control. The host-owned interface coordinator:

1. verifies the caller, exact grant, method, payload schema, classification,
   idempotency key, deadline, host policy, current source-generation ref, source
   readiness, and both outstanding-operation limits;
2. assigns a monotonically increasing accepted sequence within the current source
   generation;
3. records or projects an immutable accepted fact;
4. invokes the owning adapter in accepted order;
5. records a bounded terminal receipt.

The first implementation never executes effects concurrently for one interface.
One source generation therefore exposes a total order of unique accepted sequence
numbers, but concurrent arrivals are not promised the same relative order across
different executions. Provider declarations of method commutativity do not relax
this rule. Any later parallel profile must begin with structurally independent,
host-verifiable partition keys and a separate contract change.

The protocol hard-caps accepted-but-not-terminal operations at 64 per interface.
The effective interface cap is the narrowest of that hard cap, the descriptor, and
host policy. A separate per-caller cap is the narrowest of descriptor, grant, and
host policy. Saturation at either boundary is refused before assigning an accepted
sequence with `interface/rate-limited`; local diagnostics distinguish
`caller-outstanding` from `interface-outstanding` without disclosing other callers.

State-setting methods should be idempotent where the domain permits, for example
`led.set({"on": true})`. A method whose correctness depends on a prior value should
accept an explicit version precondition and refuse a mismatch. Silent last-writer-
wins behavior is not a generic Sensorium Interfaces guarantee.

### 6. Exclusive Control Is a Fenced, Time-Quantized Lease

An `exclusive-lease` interface has one logical coordinator and this state machine:

```text
free -> held -> free
  |       |
  |       +-> held by next epoch through release, handoff, expiry,
  |           revocation, preemption, or source-generation replacement
  +-> bounded FIFO claim queue
```

Under `sensorium.interface.invoke`, an eligible caller may use:

- `control.claim`: acquire immediately when free or enter a bounded FIFO queue;
- `control.cancel`: remove the caller's exact queued `claim/id` idempotently;
- `control.renew`: extend the current lease within descriptor, grant, and host-policy
  cumulative bounds;
- `control.release`: relinquish the lease idempotently;
- `control.handoff`: atomically release to a named queued eligible claimant;
- `invoke`: submit an effect under the current lease.

`control.preempt` is not in that caller operation family. It is a source-local,
non-delegable `sensorium.interface.manage` action available only to the operator or
an explicit emergency policy. It may end the current lease and establish a bounded
operator-held lease, but it does not grant remote invoke eligibility.

The protocol hard-caps the queue at 16 claims per interface; descriptor, grant, or
host policy may lower that bound. Every claim has its own id, deadline, caller
binding, and grant binding. Expired, revoked, or otherwise ineligible claims are
removed before selection. FIFO order applies among eligible ordinary claims;
operator preemption does not enter or reorder the queue.

At most one live queued claim may exist for `(interface/id, caller/ref)`. An exact
`control.claim` replay returns that claim; a different claim while it remains live
is refused with `interface/control-claim-exists`. `control.cancel` repeats the exact
`claim/id`, so cancellation remains unambiguous across retries and recovery.

A lease is not bound to a TCP, WSS, Room, or middleware connection. Carrier loss
therefore cannot silently transfer authority. The holder renews a short lease; loss
of renewal releases it after the bounded expiry. Host policy defines the quantum and
cumulative hold limit within descriptor and grant maxima.

Unsolicited or queue-bypassing handoff is forbidden in the first implementation.
The recipient first holds one live queued claim whose bounded request carries
`handoff/accept = true`. The holder then selects that exact `claim/id`, not an
unverified actor label. The coordinator rechecks recipient acceptance and its
current grant before atomically advancing the epoch.

### 7. Source Generation and Lease Epoch Fence Stale Effects

An authorized caller obtains the current opaque `source/generation-ref` through the
actuation-status surface after grant admission. Every shared and exclusive invoke
request repeats it. An exclusive control lease additionally contains:

- exact interface id and canonical holder ref;
- source generation, lease id, and positive monotonically increasing lease epoch;
- issued-at and expires-at timestamps;
- current grant id and authority refs;
- granted method and limit intersection.

Every exclusive `invoke` request also repeats the lease id, lease epoch,
caller-local sequence number, operation id, method, deadline, P081 causal context,
classification, and bounded payload. A shared request omits lease fields but never
omits the source-generation ref.

The coordinator rejects an operation when any binding is stale or mismatched. In
particular, packets buffered before a handoff cannot act after the epoch advances.
A source restart or replacement changes the source generation and invalidates every
lease, queued claim, and accepted-but-not-dispatched shared or exclusive operation
from the prior generation.

The coordinator rechecks the current grant, lease, epoch, expiry, policy, and source
generation immediately before handing an accepted effect to the adapter. Admission
at carrier attachment time is never sufficient.

Authority transitions and final adapter dispatch share one logical command order.
The first implementation admits only bounded synchronous adapter calls and does not
advance a handoff, release, expiry, revocation, or preemption transition past an
earlier operation already inside the provider effect boundary. Such a transition
completes after the bounded call returns or reaches a provider cancellation
boundary. Operations accepted but not yet dispatched are rechecked against the
current source generation and, for exclusive mode, the current epoch, then refused
when stale. This makes preemption latency honestly bounded by the current in-flight
operation deadline rather than pretending that a physical effect can be rolled
back.

### 8. Operations Produce Bounded Receipts

Every invoke operation has an idempotency key. In shared mode its scope is the
caller, interface, method, and source generation. In exclusive mode the scope also
contains the exact lease id and lease epoch. Repeating the same key with
semantically identical content inside that scope returns the same known receipt;
reuse with different content is refused.

`control.renew` extends expiry and cumulative hold inside the same lease id and
epoch, so legitimate invoke retries continue to deduplicate across renewal.
Handoff, release followed by reacquisition, preemption, expiry followed by
reacquisition, and source replacement establish a new idempotency scope. Invoke
admission checks source generation, lease, and epoch before idempotency replay, so
an old-epoch request cannot obtain a stale receipt instead of
`interface/control-stale`.

The final receipt outcomes are:

- `applied`: the provider confirms the effect;
- `refused`: no effect was admitted or handed to the provider;
- `failed`: the provider confirms that the admitted operation did not apply;
- `unknown`: the host cannot prove whether an effect occurred after a partial
  failure.

The generic contract does not claim exactly-once effects. Reconciliation defaults to
`none` and is an explicit per-method adapter opt-in. Supported mechanism classes are
state readback for convergent setters, exact operation-status lookup for providers
with a durable operation ledger, and native content-bound idempotent retry. These are
mechanisms under one adapter policy, not competing global modes. Generic runtime
never infers reconciliation from JSON shape or a provider assertion of
commutativity.

State readback can establish current target state but cannot prove whether one
irreversible stream element occurred. Raw PTY bytes, signals, and similar transient
effects therefore remain `unknown` after an uncertain outcome unless the provider
offers exact durable operation evidence; generic runtime never retries them
automatically.

Every final receipt carries a closed `evidence/class` independently of the adapter's
declared reconciliation mechanism:

- `host-admission`: the host proves that no provider dispatch occurred; valid for
  `refused`;
- `provider-ack`: the provider directly acknowledged the exact operation;
- `operation-status`: an exact durable provider operation record proves the outcome;
- `state-readback`: current target state was observed and the method contract
  explicitly declares target-state convergence sufficient; it never proves the
  occurrence of a transient stream element;
- `none`: no conclusive outcome evidence exists; required for `unknown`.

Native content-bound idempotent retry is a reconciliation mechanism, not an evidence
class; its resulting receipt still records the proof actually obtained. Outcome and
evidence class must be compatible: `failed` requires provider acknowledgement or an
exact operation-status record, while `applied` requires one of those classes or a
contractually sufficient state readback. A receipt also carries metadata, payload
digest, applied sequence or refusal reason, timestamps, classification, and P081
causality. An optional bounded `evidence/ref` or digest may identify classified
provider evidence, but durable generic audit facts do not retain raw input payloads
by default.

### 9. Carrier and Collaboration Context Never Become Authority

The first implemented remote carrier is authenticated direct-peer request/reply. It
carries claim, control, invoke, and receipt messages but owns no grant, queue, lease,
or source cursor. Local host capability and supervised `channel_json` adapters invoke
the same coordinator.

After P070 Phase 6A, the active relocatable Room relay becomes the default
firewall-proof remote carrier for collaborative status, claim, control, invoke, and
receipt traffic. The exact same fencing evidence travels in each request, so the relay
remains a pipe and cannot fabricate authority. Direct peer becomes an optional latency
upgrade for one controller-to-provider pair, particularly for terminal echo; failure
to establish it must fall back to the relay without changing holder, lease, or epoch.
Room does not depend on hole punching for correctness.

Room may provide audience, presence, observation, and handoff UI context. P083
reserves the explicit Room extension grant `actuate`; it is collaboration policy,
not an interface capability, actuation grant, or control lease. A Room member can
claim control or invoke through the collaboration surface only when all of these
remain true:

- current Room membership carries `actuate` and Room policy permits the action;
- the canonical Room subject matches the authenticated caller;
- the caller has an exact active actuation grant;
- the interface and method are within the session pre-authorization envelope;
- host policy admits the claim or invoke.

Ordinary Room live messages and the P082 observation pump remain presentation
surfaces. The implemented P083 relay wrapper is a distinct typed carrier envelope over the
same WSS connection; it does not reinterpret chat or projection frames as invoke
requests. Keyboard bytes are not published into the durable Room and are not accepted
merely because they arrived through an ordinary Room frame.

### 10. Classification, Disclosure, and Retention Apply to Input

Actuation payloads can be more sensitive than resulting observations. Terminal
input may contain passwords, tokens, personal text, or commands whose disclosure
would reveal host structure. Every invoke request therefore carries
`classification.v1` and remains subject to P047 no-broadening rules.

The generic durable record contains only bounded metadata:

- operation, interface, method, actor, grant, lease, and causal references;
- payload byte length and digest;
- accepted and terminal timestamps;
- outcome, refusal code, and source sequence;
- effective classification.

Raw payload retention is off by default. Provider-specific diagnostics may retain a
payload only under an explicit retention policy and classification-preserving
store. Shared observers receive resulting observations only through independently
authorized P082 interfaces.

The caller-declared payload classification is a lower bound, not a value that the
source may downgrade. Caller-side egress policy and source-side admission both run.
The source method may raise the effective tier or add bound subjects; descriptor and
grant ceilings then reject an effective tier they do not permit. A ceiling narrows
admissible input and receipt disclosure; it is not itself a minimum classification.

### 11. Workbench Terminal Control Uses Exclusive Leases

Workbench remains the owner of the PTY, terminal session, process lifetime,
resource caps, command profile, and environment backend. A shared terminal is
composed from:

- a P082 `workbench-terminal-screen` latest-state interface;
- optionally a P082 bounded terminal-event interface;
- a P083 Workbench terminal actuation interface.

The first terminal actuation method set is closed to:

- `terminal.input` with its exact bounded raw-PTY-byte schema;
- `terminal.resize` with its exact closed rows-and-columns schema;
- `terminal.signal` with its exact closed signal-name schema, only when separately
  allowed by Workbench policy.

The input and resize methods use `exclusive-lease`. A grant may omit `signal` while
permitting keyboard input. Terminal close, owner revocation, Workbench environment
teardown, source restart, or backend replacement terminates the lease, clears the
queue, and changes the source generation.

The operator must explicitly enable collaborative input for the exact Workbench
session, environment policy, and actuation method set before any remote invoke grant
can become effective. While that actuation interface is active, local operator
keystrokes use an operator-held control lease. If a remote caller currently holds
control, one manage-authorized preemption transition first advances the epoch and
establishes the operator lease; subsequent keystrokes use that lease until explicit
release or bounded expiry. The implementation MUST NOT preempt once per keystroke.
Neither path bypasses the coordinator, so local and remote input cannot interleave.
Outside collaborative publication, the existing local operator path remains
available under P071 policy.

The existing operator-only `sensorium-terminal-input.v1` contract cannot be reused
by pretending that a remote holder is the operator. The implementation must define
a successor Workbench input contract that preserves authenticated caller, exact
interface grant, control lease, source generation, epoch, sequence, and P081 causal
lineage through the final PTY write boundary. The local operator may continue to use
an operator path, but both paths converge on the same final Workbench safety and
session checks.

Process isolation remains a separate P071 concern. P083 provides no additional
filesystem, credential, or network containment for a host-local shell. The same
actuation contract may front a host-local, container, or microVM Workbench backend,
but the descriptor must not imply stronger isolation than the selected environment
actually enforces.

### 12. Sensorium Device Actuation Reuses Provider Policy

A Sensorium device adapter may publish a shared actuation interface such as:

```text
interface: sensorium-interface:led-01
mode: shared
method: led.set
input: {"on": true}
```

The coordinator establishes authority, ordering, classification, and receipts. The
Sensorium adapter still checks connector availability, source identity, local
allowlist, method schema, and device-specific safety immediately before the effect.
Where an operation maps to Sensorium OS, P048 remains the owner of action-class and
effect-envelope admission. P083 cannot broaden a denied or unavailable P048 action.

## P082 Reuse and Extension Boundary

P083 MUST be implemented as an in-place extension of the P082/Solution 046
component, not as a parallel interface service. New code should first extend or
extract a direction-neutral primitive from the existing implementation. A separate
actuation-specific primitive is justified only where observation and effect
semantics are materially different.

The target shape is:

```text
sensorium-interface-core
  common resource, lifecycle, authority, classification, causality, limits
  observation: read, subscription, cursor, frame and batch semantics
  actuation: invoke, coordination, fencing and receipt semantics

SensoriumInterfaceRuntime + SensoriumInterfaceStore
  common publication, grants, revocation, facts, idempotency, restart and metrics
  observation projections and Interaction Broker source adapters
  actuation coordinators and effect adapters

shared host and peer admission
  one authenticated caller and Passport boundary
  operation-specific read/subscribe or invoke/control dispatch
```

### Reuse Matrix

| P082 implementation asset | P083 reuse posture |
|---|---|
| `node:sensorium-interface-core` crate boundary | Extend this crate with direction-neutral resource/authority values and an `actuation` module; do not create a competing top-level interactive-interface core. |
| `INTERFACE_ID_PREFIX`, `InterfaceLifecycle`, `InterfaceStatus`, expiry and health validation | Reuse one interface id namespace and lifecycle. Direction does not create a second publication state machine. |
| `SensoriumInterfaceDescriptor` validation | Extract a common resource envelope for id, publisher, lifecycle, classification, expiry and safe metadata; keep closed observation and actuation wire descriptors around that shared core. The actuation variant binds one exact input schema per method rather than copying P082's single output-schema shape. |
| `SensoriumInterfaceRuntime` and `SensoriumInterfaceStore` | Extend the existing runtime and SQLite store through forward migrations. Do not open a second database or rebuild publication and grant projections elsewhere. |
| `sensorium_interface_publications` | Store both directional descriptor kinds under the same interface-id uniqueness and lifecycle rules, with an explicit indexed direction/kind discriminator. |
| `sensorium_interface_grants`, canonical namespaced grantee refs and `active_grant` admission | Reuse the grant table and current-status lookup; add a typed bounded `scope_json` projection for exact actuation methods and limits rather than creating another grant authority. Canonical scope or its digest becomes part of grant idempotency and Passport replay equality. |
| `sensorium_interface_facts`, `sensorium_interface_idempotency`, `execution_fact`, and P081 receipts | Reuse the same immutable fact, idempotency and causal-receipt spine with new actuation fact kinds and honest terminal outcomes. Raw input remains outside generic fact payloads. |
| `InterfaceAdmissionContext`, authenticated actor binding, leak-minimal lookup and action-specific `manage` policy | Reuse before every publication, grant, control and invoke action. P083 adds operation-specific checks but no second caller model. |
| `InterfaceRevocationGuard`, Passport trust-anchor verification, allowed-caller checks, target/issuer binding and atomic Passport admission | Reuse the verification and transaction mechanics; extend profile dispatch with the separate `sensorium-interface-actuation@v1` scope evaluator required by method, payload and control-lease bounds. `admit_verified_passport` must compare canonical actuation scope on replay; the current explicit `{interface, grantee, capability, expiry}` comparison is insufficient after `scope_json` exists. |
| P047 `Surface::Interface`, classification lattice and no-broadening helpers | Reuse the same classification vocabulary and validation. Add input admission and receipt disclosure checks without introducing an actuation-specific tier order. |
| `SensoriumInterfaceSourceRegistry` capacity, canonical source-kind validation, readiness snapshots and lock-release-before-I/O discipline | Extract or reuse the bounded registry mechanics for an actuation-adapter registry, while keeping read-source and effect-adapter traits separate. |
| Host-capability and authenticated direct-peer admission | Extend the current dispatch and peer message-chain boundary with control/invoke variants; reuse caller, node, Passport, deadline, revocation and error-redaction checks. |
| Room canonical subject keys and current Room-plus-interface authority intersection | Reuse subject normalization and dual-authority checks for collaborative claim/invoke. P082 `observe` remains read-only; P083 adds the explicit Room extension grant `actuate`, which still does not replace an interface grant or lease. |
| Bounded metrics and `node:tools/conformance/sensorium_interfaces_conformance.py` harness | Extend the existing manage snapshot and conformance runner with closed actuation dimensions and tests; do not create an identifier-bearing telemetry path or unrelated runner. |

### Shared Runtime and Storage Evolution

The existing publication record should evolve into a closed directional enum, for
example `InterfaceDescriptor::Observation | Actuation`, whose variants share one
validated resource envelope. The private binding follows the same pattern. The read
variant continues to select a `SensoriumInterfaceSourceAdapter`; the actuation
variant selects a separate `SensoriumInterfaceActuationAdapter`.

The current grants table already owns exact interface, grantee, capability, status,
expiry, and revocation. P083 should migrate that table with a bounded typed scope
projection rather than store method authority in a new table. Canonical scope or a
domain-separated digest of it must participate in grant replay comparison, including
the atomic `admit_verified_passport` path; the same Passport id with a different
method or limit scope is a conflict, never an idempotent replay. Control claims,
leases, and accepted operations are genuinely new state machines and receive
dedicated tables keyed back to the existing publication and grant rows. Their final
receipts remain on the operation projection and append to the existing fact and
idempotency spine rather than creating a second receipt store.

The existing idempotency table must also migrate from a caller-supplied key alone to
a domain-separated effective key. Shared invoke keys include source generation;
exclusive invoke keys additionally include lease id and epoch. The stored canonical
request digest still detects conflicting content inside that effective scope.

The actuation coordinator belongs inside the existing `SensoriumInterfaceRuntime`.
It may live in a separate Rust module and own its own bounded in-memory coordinator
map, but publication, grant, revocation, restart reconciliation, operator
inspection, and metrics remain one runtime responsibility. Restart first rebuilds
the common resource and authority projections, then invalidates old actuation source
generations before admitting new control work.

### Deliberate Non-Reuse

Reuse stops where the semantic contract changes:

- a P082 subscription lease authorizes bounded observation over time; a P083
  control lease authorizes current exclusive effects. They MUST remain different
  types, tables, ids, and transitions, with distinguishable typed variants inside
  the shared interface error vocabulary;
- P082 cursors, frames, batches, replay and overflow policy have no meaning on the
  invoke path and MUST NOT be added to actuation requests;
- Interaction Broker probe/watch remains a read-side source engine. Effects MUST
  NOT be smuggled through watch requests, source cursors, or source-provider output;
- `SensoriumInterfaceSourceAdapter` remains read-only. The implementation MUST use
  a separate, small effect-adapter trait rather than add optional mutating methods
  that every observation provider must refuse;
- SSE and the WSS Room projection remain outbound observation carriers. A future
  bidirectional carrier invokes the same actuation coordinator through a separate
  authenticated message family;
- P082 read metrics and actuation metrics may share one bounded snapshot, but their
  operation semantics and latency measures remain separately named.

This boundary maximizes code and storage reuse while preserving the decisive
architectural separation: common authority is shared; observation flow control and
effect coordination are not conflated.

## End-to-End Examples

### Shared LED

```text
1. The source operator publishes a shared `led.set` actuation interface.
2. Two clients receive exact, expiring invoke grants.
3. Each reads actuation status and receives the same current opaque generation ref.
4. Both submit idempotent state-setting operations concurrently under that ref.
5. The coordinator validates both and assigns unique accepted sequences 41 and 42.
6. The adapter applies them in that total order and returns two classified receipts.
7. Observers learn the resulting LED state only through a separate observation
   interface.
```

### Workbench Terminal Baton

```text
1. Workbench creates a terminal session and owns its PTY.
2. The operator publishes screen observation and terminal actuation interfaces.
3. Authorized Room participants receive Room `observe` / `actuate` grants plus
   separate exact observation and invoke grants.
4. Client A claims control and receives source generation G, lease L, epoch 7.
5. Client B enters the bounded claim queue with `handoff/accept = true` while A
   types.
6. Every A input batch carries G/L/7 and a strictly increasing holder sequence.
7. A hands off to B; the coordinator rechecks B and advances the lease epoch to 8.
8. A delayed G/L/7 packet is refused before the Workbench adapter sees it.
9. B types under G/L2/8; all observers continue receiving independent screen
   snapshots.
10. Terminal close invalidates the lease, queue, actuation source generation, and
    observation source lifecycle without closing the durable Room.
```

## Error Contract

| Code | Meaning | Retry posture |
|---|---|---|
| `interface/actuation-not-found` | resource absent or leak-minimal unauthorized lookup | no unless separately invited |
| `interface/invoke-forbidden` | current grant, method, classification, or host policy denies invocation | no without new authority or narrower input |
| `interface/control-required` | exclusive interface invocation has no control lease | claim first |
| `interface/control-busy` | lease is held and the claim queue is unavailable or full | bounded retry after status hint |
| `interface/control-queued` | claim is accepted but not current authority | await bounded claim status |
| `interface/control-claim-exists` | caller already has a different live queued claim for this interface | cancel or await the existing claim |
| `interface/control-stale` | source generation, lease id, epoch, holder, or sequence is stale | no; claim current control |
| `interface/control-expired` | claim or lease deadline passed | create a new claim |
| `interface/control-preempted` | operator or explicit policy ended the lease | no without a new claim |
| `interface/method-denied` | actuation method is absent from descriptor, grant, lease where applicable, or current policy intersection | no |
| `interface/input-invalid` | input fails closed-schema or semantic validation | no without correction |
| `interface/input-too-large` | payload exceeds effective byte cap | no without a smaller operation |
| `interface/rate-limited` | effective rate, per-caller outstanding, or per-interface outstanding cap is exhausted | bounded retry; local diagnostics identify the saturated scope |
| `interface/idempotency-conflict` | operation id is reused with different semantics | no; use a new id |
| `interface/source-replaced` | source generation changed before effect | refresh admitted actuation status and reclaim control where required; obtain new authority only if current grant/policy no longer admits the interface |
| `interface/effect-unknown` | partial failure prevents proof of application | provider-specific reconciliation |

Unauthorized resource lookup remains leak-minimal. Operator inspection may expose a
more precise local diagnostic than a remote caller receives.

## Alternatives Considered

### Keep All Actuation Outside Sensorium Interfaces

This preserves the P082 boundary but forces every provider to reinvent remote
grants, fencing, receipts, and carrier semantics. It also makes terminal control and
simple device control structurally unrelated despite sharing the same authority
problem. Rejected.

### Add a Single Read/Write Flag and Grant to P082

This is superficially small but couples observation to effects, makes least-
authority grants difficult, and encourages carriers or subscriptions to become
implicit control sessions. Rejected.

### Reuse the Actuation Grant as the Exclusive Baton

Short grants would create unnecessary delegation churn; long grants would give one
holder control for too long. Revocation and handoff would also become grant-
administration operations rather than fast coordination. Rejected.

### Use Connection Ownership as Exclusive Control

Socket ownership cannot survive reconnect safely, encourages transport-specific
semantics, and cannot fence delayed packets after handoff. Rejected.

### Directional Resources with a Host-Owned Coordinator

This keeps authority explicit, gives shared devices and exclusive terminals one
small coordination core, preserves provider ownership, and makes stale control
evidence testable. Accepted.

## Trade-offs

- Separate observation and actuation resources add publication and grant work, but
  prevent ambient write authority and allow independent revocation.
- Fenced leases add identifiers and lifecycle state, but make delayed input after
  handoff structurally rejectable.
- Serializing effects limits throughput, but gives the first implementation one
  total and auditable order. Concurrent arrival does not imply a reproducible order
  across executions, and parallel provider execution is outside the initial
  contract.
- A bounded FIFO queue improves collaboration ergonomics, but introduces cleanup,
  fairness, expiry, and privacy obligations.
- Short leases limit abandoned control, but require renewal traffic and careful
  behavior under network partitions.
- Metadata-only durable receipts reduce secret retention, but can leave provider-
  specific investigation dependent on separately authorized diagnostics.
- `unknown` outcomes are less convenient than claiming exactly once, but accurately
  represent partial failures across non-transactional physical effects.

## Failure Modes and Mitigations

| Failure mode | Risk | Mitigation |
|---|---|---|
| Observation grant is accepted as control | unauthorized effects | separate capability, resource, grant profile, and dispatch path |
| Room or WSS session is treated as authority | collaboration membership becomes ambient write access | intersect current Room policy with exact interface grant and current lease before every effect |
| Relay failover or direct-peer upgrade changes control ownership | carrier state becomes an implicit lease transition | reconnect through the same coordinator, recheck grant/generation/lease/epoch, and change only the carrier binding |
| Old holder packet arrives after handoff | keystrokes or device commands execute under stale authority | bind source generation and monotonically increasing lease epoch; recheck at final adapter boundary |
| Caller holds a grant but no baton | concurrent terminal corruption | exclusive invocation requires both current grant and current control lease |
| Shared callers race in provider I/O | effects have no common total order | one logical coordinator assigns unique accepted sequences and serializes first-implementation effects |
| Many shared grantees fill per-caller allowances | aggregate pending work grows without bound | enforce a hard 64-operation per-interface cap independently of narrower per-caller caps |
| Claim queue grows or retains dead authority | resource exhaustion or unfair control | cap at 16, expire claims, remove revoked entries, expose bounded diagnostics |
| One caller submits many live claims | queue monopoly and ambiguous cancellation | allow one live queued claim per caller/interface and require exact `claim/id` cancellation |
| Carrier disconnect releases control immediately | transient network loss transfers authority unexpectedly | lease is host-owned and expires by time, not socket lifecycle |
| Carrier reconnect preserves stale control | replay after ownership change | require current source generation, epoch, holder, and sequence on every invoke |
| Process crashes after physical effect | duplicate retry or false failure | content-bound idempotency plus honest `unknown` outcome; provider reconciliation where available |
| Old operation id is reused under a later lease tenure | stale receipt replaces a new stream effect | include lease id and epoch in exclusive idempotency scope; renewal keeps the same epoch |
| Runtime guesses reconciliation for transient input | raw PTY bytes or signals are duplicated | adapter reconciliation is explicit opt-in; irreversible streams require exact durable operation evidence and are never generically retried |
| Terminal input is stored in generic audit | passwords or private commands leak | store digest and metadata only by default; payload retention requires explicit classified policy |
| Operator preemption races with invoke | effect occurs after withdrawal | serialize preemption and invocation in one coordinator and recheck immediately before adapter dispatch |
| Handoff or preemption overtakes in-flight provider I/O | an old-holder effect completes under the new epoch | use bounded synchronous adapter calls and one authority/dispatch order; complete the transition only after return or a provider cancellation boundary |
| Source restarts with persisted leases | stale baton controls replacement resource | change source generation and invalidate leases and claims during restart reconciliation |
| Provider method widens P048 or Workbench policy | interface bypasses local safety | provider-local policy always narrows; unavailable or denied underlying action fails closed |
| A read-only projection or permissive adapter publishes a lower operational-impact class than its environment | deliberators understate the consequences of observations or later control | inherit the exact environment/resource context for every derived interface; local policy may only raise it |
| An old directional publication survives a source-context replacement | observations or effects proceed under obsolete assumptions | inherit the current source generation, withdraw every affected old direction as superseded, and reject it through P082 before read or invoke admission |
| Operational-impact context is interpreted as actuation authority | a caution label becomes an implicit permission | continue to require the exact capability, grant, method, generation, lease, and epoch; context changes reasoning posture only |
| Passport replay changes only method or limit scope | broader authority aliases an earlier grant id | include canonical `scope_json` or its digest in atomic Passport replay equality |
| Room collaboration uses an unnamed action grant | implementations choose incompatible or ambient authority | reserve the explicit `actuate` extension grant and still intersect exact interface authority |
| Room session bearer reaches a shared projection | another member can impersonate the session subject | mint 256 random bits at join and keep the ref only in the joining client's admission envelopes |
| Withdrawn or closed-Room groups retain active capacity | the bounded registry saturates with no usable groups | remove explicit withdrawals immediately and reap closed or terminal Rooms at every group management/access boundary |
| One carrier disconnect deletes a Room-scoped group | transient member loss removes collaboration for everyone | keep group lifetime tied to Room lifecycle and explicit manage withdrawal, not to one session |
| Holder identity is disclosed to all claimants | collaboration metadata leak | remote status exposes own claim and generic busy/queue position only; operator gets full inspection |
| P083 creates a second publication or grant store | lifecycle and revocation diverge by direction | migrate `SensoriumInterfaceStore` and reuse one publication, grant, fact, idempotency, and revocation authority |
| Read adapters gain optional mutating methods | observation providers accidentally expose effects or implement inconsistent refusal | keep separate read-source and actuation-adapter traits over shared bounded registry mechanics |

## Implementation Guidance

The implementation should extend the existing P082 component one stratum at a
time. Protocol and pure-core contracts come first, host authority and persistence
second, provider and carrier adapters third, and operator/collaboration surfaces
last. Each stratum must preserve the named invariants and may depend only on lower
strata; carrier convenience must never become an authority shortcut.

The guidance below defines ownership and dependency direction. Concrete closure is
tracked separately in the ordered `P083-*` work items under
[Implementation Tracker](#implementation-tracker).

### Protocol and Pure Core

- extend `sensorium-interface-core` with a shared resource/authority layer and a
  separate actuation module; do not create a parallel core crate;
- define the per-method-schema actuation descriptor, grant scope, actuation status,
  control request/status/lease, invoke request, and receipt schemas around the
  shared resource envelope;
- add pure validation for coordination modes, exact method scopes, both outstanding
  limits, one-live-claim uniqueness, total sequence order, source generation, lease
  epochs, fenced idempotency, and receipt transitions;
- carry on every final receipt the closed Section 8 evidence class that established
  its outcome: host admission, provider acknowledgement, durable operation status,
  contractually sufficient state readback, or `none`. Readback proves that the
  requested state holds, not that this operation executed; without the evidence
  class a shared-mode `applied` silently conflates the two whenever a concurrent
  caller requested the same state;
- keep the core free of daemon, SQLite, async runtime, provider, and carrier
  dependencies.

### Capability and Policy

- register `sensorium.interface.invoke` with the frozen posture;
- define `sensorium-interface-actuation@v1` Passport scope and evaluator;
- add source-local manage actions for publication, grant, preemption, queue and lease
  inspection;
- require exact method scopes and current host-policy admission;
- treat an empty `remote/node-ids` grant scope as exact host-local authority only;
  federated Passport profiles require the authenticated remote node explicitly;
- keep caller control operations under `invoke`, but enumerate `control.preempt`
  only in the closed source-local `manage` action policy.

### Host Runtime

- extend `SensoriumInterfaceRuntime` and `SensoriumInterfaceStore` through forward
  migrations; reuse publication, grant, fact, idempotency, revocation, receipt,
  restart, inspection, and metric ownership;
- persist the genuinely new claim, control-lease, operation, preemption, and
  terminal-receipt state under that existing runtime;
- migrate grant/Passport replay equality to include canonical actuation scope and
  migrate idempotency keys to include source generation plus lease id/epoch where
  applicable;
- rebuild the common resource and authority projections first, then invalidate prior
  actuation source generations, and only then admit new control work; restart order
  is itself a fencing contract, not an implementation detail;
- run one bounded logical coordinator per active actuation interface without holding
  registry or database locks across provider I/O;
- enforce the accepted operation deadline as a hard adapter-call bound with an
  explicit terminal/retryable classification. `inv-sii-preemption-linearized` holds
  only while an in-flight effect cannot outlive that bound, so an adapter able to
  block without one silently converts bounded preemption latency into an unbounded
  wait; a timed-out call yields `unknown`, never an assumed outcome;
- enforce the independent per-caller, 64-operation per-interface, 16-claim queue,
  and one-live-claim-per-caller bounds before accepting work;
- cap each serialized durable actuation-coordinator projection at 16 MiB on both
  read and write; crossing the cap fails before provider dispatch rather than
  creating an oversized SQLite authority record;
- expose bounded status and aggregate metrics without unbounded actor or interface
  dimensions, and name each actuation latency for the boundary it actually measures;
  preemption and effect latency are elapsed-time measures at the enforcement
  boundary and must not reuse a write-commit timing shape.

### Provider Adapters

- reuse the P082 bounded registry mechanics but define a separate small actuation
  adapter trait for readiness, input validation, final policy checks, effect
  application, and optional reconciliation;
- treat adapter `ready` as a bounded health/admission hint rather than an atomic
  effect guarantee; `apply` performs the authoritative provider-state check at the
  effect boundary and reports source termination or an honest uncertain outcome;
- make the reconciliation mechanism an explicit per-method adapter declaration with
  `none` as the default and no generic retry of irreversible streams;
- emit the actual closed receipt evidence class separately from the declared
  reconciliation mechanism, and reject outcome/evidence combinations that do not
  satisfy the Section 8 contract;
- implement a bounded fixture LED adapter for shared-mode conformance;
- implement Workbench terminal input, resize, and optional signal methods behind
  the Workbench authority boundary;
- preserve Sensorium OS action-class enforcement where an adapter invokes P048.

### Carrier Adapters

- extend the P082 host-local and authenticated direct-peer admission boundaries with
  claim/control/invoke surfaces first;
- reuse `channel_json` only as a bounded caller transport, never as authority;
- use bounded polling and Room presence hints for claim readiness; do not add a
  separate federated push protocol;
- treat the P070 `session/ref` as a 256-bit private bearer used only at the caller's
  admission boundary; never copy it into actuation status, Room messages, fan-out
  acknowledgements, shared observations, or collaboration-group state;
- materialize exactly one complete matching `sensorium-interface-actuation@v1`
  profile for an interface and authenticated peer in the first direct-peer runtime;
  reject zero or multiple matches until a canonical, limit-preserving profile
  intersection is specified;
- add collaborative Room UI or a bidirectional live carrier only after the direct
  contract and fencing tests pass, and require the explicit Room extension grant
  `actuate` in addition to interface authority;
- implement the P070 relocatable relay wrapper as the default firewall-proof remote
  collaboration carrier after P070 Phase 6A; keep direct peer as an optional latency
  upgrade and reuse the exact same coordinator request/receipt schemas and fencing.

### Operator Surface

- extend the existing `sensorium.interface.manage` surface to publish or withdraw an
  actuation interface;
- grant or revoke exact methods;
- inspect current holder, remaining quantum, bounded queue, recent metadata-only
  receipts, and source generation;
- preempt control once with a recorded reason, establish a bounded operator lease,
  and route subsequent operator input through that lease until release or expiry;
- group observation and actuation interfaces for one target without combining their
  grants. A group is Room-scoped rather than session-owned: explicit withdrawal
  releases its active slot immediately, Room close/terminal state reaps it before
  access or inspection, daemon stop clears it, and one member-session disconnect does
  not withdraw it for other current members.

## Named Acceptance Invariants

- `inv-sii-observation-never-implies-actuation`: no read, subscribe, cursor,
  observation grant, Room membership, or carrier attachment satisfies invoke
  authority.
- `inv-sii-room-session-bearer-private`: a Room session ref never appears in a live
  payload, collaboration status, fan-out response, durable fact, or shared
  observation; the carrier binds the authenticated session outside those values.
- `inv-sii-room-group-room-scoped`: withdrawal and Room termination release group
  capacity, while one member-session disconnect cannot remove a group still usable by
  other currently admitted members.
- `inv-sii-single-authority-runtime`: observation and actuation reuse one
  publication, grant, revocation, fact, idempotency, caller-admission, and operator-
  inspection runtime; no directional side store may independently authorize an
  interface.
- `inv-sii-directional-state-distinct`: observation subscriptions and actuation
  control leases remain distinct types and state machines even though they share
  resource and authority primitives.
- `inv-sii-exact-resource-and-method`: every control request binds one exact
  interface and grant; every invoke additionally binds one actuation method inside
  descriptor, grant, lease where applicable, and policy intersection.
- `inv-sii-provider-policy-only-narrows`: the interface coordinator cannot widen a
  Workbench, Sensorium, Sensorium OS, device, emergency, or host-policy decision.
- `inv-sii-shared-order-total`: one source generation exposes unique, monotonically
  increasing accepted sequence numbers and one total effect order even when callers
  submit concurrently; relative arrival order is not promised across executions.
- `inv-sii-exclusive-single-holder`: at most one unexpired lease holder exists for
  an exclusive interface generation.
- `inv-sii-stale-epoch-refused`: a prior source generation, lease id, epoch, holder,
  or sequence cannot reach the provider effect boundary.
- `inv-sii-grant-is-not-baton`: an invoke grant alone never authorizes an exclusive
  effect.
- `inv-sii-lease-is-not-transport`: carrier attachment, reconnect, or disconnect
  cannot create or transfer a control lease.
- `inv-sii-queue-bounded-and-live`: the claim queue is capped, expiring, revocation-
  aware, and cannot retain ineligible authority.
- `inv-sii-one-live-claim-per-caller`: one caller has at most one queued claim for an
  interface, and cancellation binds its exact claim id.
- `inv-sii-operation-backlog-bounded`: accepted-but-not-terminal work is bounded
  independently per caller and per interface before sequence assignment.
- `inv-sii-preemption-linearized`: operator preemption advances authority before a
  later effect can be dispatched and reports bounded delay behind an already
  in-flight effect.
- `inv-sii-source-replacement-fences-all`: replacement changes source generation and
  invalidates every prior claim, lease, and accepted-but-not-applied operation.
- `inv-sii-idempotency-content-bound`: an operation id replays only semantically
  identical content and never aliases another caller, method, interface, or source
  generation.
- `inv-sii-idempotency-fenced`: exclusive invoke replay additionally binds lease id
  and epoch; renewal preserves the epoch, while later authority tenure cannot replay
  an earlier receipt.
- `inv-sii-effect-outcome-honest`: partial failure becomes `unknown` rather than a
  fabricated success or failure.
- `inv-sii-receipt-evidence-explicit`: every final receipt carries a closed evidence
  class compatible with its outcome; `unknown` uses `none`, and state readback never
  proves occurrence of a transient stream element.
- `inv-sii-irreversible-unknown-not-retried`: an uncertain irreversible stream
  effect is never generically retried or inferred from state readback without exact
  durable provider evidence.
- `inv-sii-passport-scope-replay-exact`: atomic Passport replay compares canonical
  method and limit scope in addition to interface, grantee, capability, and expiry.
- `inv-sii-payload-retention-explicit`: generic durable facts contain no raw
  actuation payload unless an explicit classified retention policy permits it.
- `inv-sii-terminal-exclusive-default`: Workbench terminal input and resize require
  an exclusive control lease in the initial profile.
- `inv-sii-room-authority-intersection`: collaborative invocation requires current
  Room `actuate` policy, exact subject binding, exact interface grant, current lease
  where required, and current host policy.

## Frozen Initial Decisions

The design decisions are accepted as of 2026-07-17. Decisions 1-15 originated in
the 2026-07-16 baseline; decisions 16-28 close the pre-P083-002 review, decision 29
records the implemented direct-peer scope materialization boundary, decision 30
adopts P070's relocatable relay without changing P083 authority, and decision 31
records the post-MVP operational-context extension:

1. Sensorium Interfaces may expose actuation, but observation and actuation remain
   separate directional resources and authority planes.
2. The actuation capability is `sensorium.interface.invoke`; it never follows from
   `read` or `subscribe`.
3. Actuation publication freezes either `shared` or `exclusive-lease`; callers
   cannot select or widen the mode per request.
4. Shared mode permits concurrent submission but the first implementation
   establishes one total serialized effect order.
5. An actuation grant gives eligibility. Exclusive current authority is a separate
   short-lived control lease.
6. Exclusive leases are fenced by exact caller, source generation, lease id,
   monotonically increasing epoch, expiry, and holder-local sequence.
7. Exclusive control uses a bounded FIFO queue, explicit renewal/release, accepted
   handoff, and source-local operator preemption.
8. Room, carriers, observation subscriptions, and connection ownership never confer
   actuation authority.
9. Workbench terminal input and resize use `exclusive-lease`; terminal signals are
   a separately grantable method.
10. Generic durable operation evidence stores payload metadata and digest, not raw
    input, by default.
11. The first implemented remote carrier is authenticated direct-peer request/reply;
    revised by Decision 30, richer live interaction remains an adapter over the same
    coordinator.
12. P083 does not weaken P048 action classes, Workbench profiles, environment
    isolation, source policy, or emergency policy.
13. Once implemented, P083 extends the existing Solution 046 component rather than
    creating a second component that competes for Sensorium Interface authority.
14. Implementation reuses the existing P082 core crate, runtime, store, publication,
    grant, revocation, fact, idempotency, classification, receipt, host/peer
    admission, Room-subject, metrics, and conformance machinery. Read subscriptions
    and actuation control leases remain deliberately separate state machines.
15. P082 and P083 are explicit hard-MVP release blockers. Their implementation and
    promotion gates are satisfied through P083-013; the post-MVP relay carrier does
    not reopen the completed hard-MVP boundary.
16. Each actuation method has its own exact closed input schema. The descriptor uses
    a method catalog, not one polymorphic interface-wide input schema.
17. Outstanding work is bounded independently per caller and per interface. The
    protocol hard-caps accepted-but-not-terminal work at 64 operations per interface,
    and saturation is refused before sequence assignment.
18. One caller may have at most one live queued claim per interface. Claim
    cancellation binds the exact `claim/id`.
19. Every shared and exclusive invoke binds an authorized opaque
    `source/generation-ref`; it is obtained from actuation status rather than the
    public descriptor.
20. Exclusive idempotency scope includes lease id and epoch. `control.renew` does not
    advance either value; a new authority tenure cannot replay a prior tenure's
    receipt.
21. Actuation methods are distinct from control operations. Caller claim/renew/
    release/handoff uses `sensorium.interface.invoke`, while `control.preempt` is an
    explicitly enumerated source-local `sensorium.interface.manage` action. One
    preemption establishes an operator lease; it is not repeated per keystroke.
22. Shared effects remain serialized. Method-level commutativity assertions are not
    accepted as proof for parallel execution; only a future structurally keyed,
    host-verifiable partition contract may reopen this decision.
23. Direct handoff to a caller outside the claim queue is refused. The recipient
    first holds one eligible queued claim and explicitly accepts the handoff.
24. Claim readiness uses bounded polling and collaboration-presence hints. P083 does
    not define a federated push profile; any future hint mechanism must be shared with
    P082 data-readiness notification rather than duplicated. The substrate must be
    authority-neutral and disclosure-bounded: every hint audience passes the same
    current grant and applicable collaboration-policy checks as the corresponding
    claim or read.
25. The coordination vocabulary remains exactly `shared | exclusive-lease`. A
    fixed-size permit set or keyed lease mode requires a separate contract change.
26. Reconciliation is per-method adapter opt-in with `none` as the default. State
    readback, durable operation-status lookup, and native idempotent retry are
    mechanism classes under that policy; uncertain irreversible streams remain
    `unknown` without exact durable operation evidence. Receipts separately record
    the actual closed evidence class; native retry is a mechanism, not proof.
27. Collaborative actuation uses the explicit Room extension grant `actuate`, which
    is necessary but never sufficient without exact interface authority and a lease
    where required.
28. Migrating grants with actuation `scope_json` also extends grant idempotency and
    atomic Passport replay equality. A repeated Passport id with different method or
    limit scope is a conflict.
29. The first direct-peer runtime admits exactly one complete matching
    `sensorium-interface-actuation@v1` profile for the interface and authenticated
    peer. Zero or multiple matching profiles fail closed rather than silently
    unioning methods or widening independently bounded limits. Empty
    `remote/node-ids` is reserved for exact host-local grant admission and is never
    a federated wildcard.
30. After P070 Phase 6A, the relocatable Room relay is the default firewall-proof
    collaborative carrier and direct peer is an optional latency upgrade. Carrier
    selection never changes grants, source generation, lease, lease epoch,
    idempotency scope, or operation order, and Room remains independent of hole
    punching.
31. Observation and actuation interfaces over one enacted target reuse P082's
    `sensorium-operational-context.v1`. Access mode cannot lower the target class;
    host policy may use a higher class to narrow autonomy and limits, but the class
    is never grant, lease, membership, or effect authority. Currentness is the P082
    source-generation plus effective-publication predicate, not a carrier or
    wall-clock TTL; correction uses audited immutable replacement.

## Implementation Tracker

The tracker is the authoritative implementation checklist for this proposal. Work
items are ordered by dependency, although independent tests and documentation may
advance in parallel. An item becomes `done` only when its acceptance boundary is
implemented, refusal-tested where applicable, and synchronized with the affected
code and documentation. P083-002 through P083-011 had to be `done` before promotion;
P083-012 records the completed promotion and final hard-MVP closure.

| Id | Work item | Status | Acceptance boundary |
|---|---|---|---|
| P083-001 | Freeze directional resources, invoke capability posture, shared/exclusive coordination, fencing, receipts, and implementation order | done | This document records the accepted contract, review-closure decisions, alternatives, named invariants, failure model, and first implementation sequence. |
| P083-002 | Freeze the shared resource envelope plus per-method actuation descriptor, actuation status, control request/status/lease, invoke request/receipt, grant-scope, and Workbench input successor schemas | done | Observation and actuation wire contracts reuse one resource envelope while remaining closed directional schemas; each method binds one canonical payload schema; the receipt has a closed evidence-class enum; semantic checks reject unknown fields, empty scopes, missing generation refs, stale fencing evidence, invalid transitions, incompatible outcome/evidence pairs, unbounded payloads, and classification mismatch. |
| P083-003 | Register `sensorium.interface.invoke` and the exact `sensorium-interface-actuation@v1` Passport profile | done | Machine registry, Rust constants, closed manage-action policy, human registries, and the existing Passport parsing/trust/caller/revocation machinery agree; the actuation scope evaluator is new, and canonical method/limit scope participates in atomic Passport replay equality. |
| P083-004 | Extend `sensorium-interface-core` with pure shared-resource plus actuation coordination, grant-intersection, fencing, idempotency, and receipt logic | done | The existing core crate gains direction-neutral resource primitives and a separate actuation module; it retains no daemon, SQLite, provider, carrier, or async-runtime dependency and proves per-method schemas, total shared order, both outstanding limits, one-live-claim uniqueness, generation fencing, epoch-scoped idempotency, receipt-evidence compatibility, and the other named invariants. |
| P083-005 | Extend the existing store/runtime with durable claim queue, control lease, preemption, operation, receipt, restart, inspection, and bounded metrics state | done | `SensoriumInterfaceRuntime` and `SensoriumInterfaceStore` remain the owners; publication/grant/fact/idempotency/revocation machinery is migrated with scoped replay equality and fenced effective idempotency keys; one coordinator enforces the 64-operation interface cap, 16-claim cap, one live claim per caller, and serialized authority/effects. |
| P083-006 | Reuse the bounded registry mechanics for a separate actuation-adapter trait and bounded shared LED fixture | done | Read-source and effect-adapter traits remain distinct; unknown, duplicate, unavailable, stale-generation, and over-cap adapters fail closed; concurrent LED tests prove sequence uniqueness, total order, observer agreement, content-bound idempotency, explicit reconciliation mechanisms, and the actual evidence class on each receipt without claiming reproducible arrival order. |
| P083-007 | Extend existing host-local and authenticated direct-peer admission with claim/control/invoke surfaces | done | Existing caller, node, Passport, deadline, revocation and error-redaction checks are reused; carrier attachment grants no authority; every shared/exclusive invoke checks exact method, classification, source-generation ref, and, where applicable, lease and epoch. |
| P083-008 | Integrate Workbench terminal input/resize/signal through the actuation adapter | done | A remote caller is never represented as the operator; each method has an exact schema and lineage reaches the PTY boundary; one preemption establishes the operator lease; stale-holder bytes, close, revoke, restart, handoff, and uncertain irreversible-stream retry are refusal-tested. |
| P083-009 | Extend operator and Room collaboration surfaces for grant, queue, holder, handoff, preemption, and grouped observation/control | done | The manage policy owns strict publish/withdraw/inspect actions over a process-local 64-group registry; inspection reuses exact interface grant/preemption state. Room adds the closed `actuate` grant, derives the canonical session subject and current membership atomically from one live-transport snapshot, and then delegates status/control/invoke to the existing exact grant, method, generation, lease, epoch, sequence, and host-policy runtime. The 256-bit session bearer stays outside frames and shared projections. Explicit withdrawal releases capacity immediately; closed/terminal Rooms are reaped at group boundaries, while one session disconnect leaves the Room-scoped group available to other current members. Observe remains separate, readiness is bounded polling, restart loses grouping fail-closed, and raw terminal input is neither sent nor persisted as Room content. |
| P083-010 | Extend the P082 conformance harness with load, restart, partial-failure, and end-to-end terminal baton tests | done | The runner prebuilds daemon/core plus the required Rust Workbench contract bridge, executes 19 exact Rust checks and two external tests, and covers caller/interface backlog and claim-queue saturation, duplicate claims, expiry/renewal, handoff/stale epoch, cross-tenure idempotency, source replacement, restart, honest partial failure, observer-only denial, Room dual authority, and two Sensorium controllers writing through a real Workbench shell PTY. |
| P083-011 | Synchronize P045/P047/P048/P070/P071/P072/P081/P082, Solutions 030/036/042/046, Node ledgers, capability registries, trackers, and readiness snapshot | done | The cross-document audit found no competing semantics in P045/P047/P048/P072/P081 or Solutions 030/036/042; P070, P071, P082, P083, Solutions 036/042/046, Room schemas, manage policy fixtures, Node ledgers/MVP checklist, generated views, and the readiness snapshot now describe the same P083-011 boundary. |
| P083-012 | Promote the implemented contract into Solution 046's actuation boundary | done | P083-002 through P083-011 are complete; the final review found no unresolved correctness or authority blocker, and Solution 046 now owns the promoted actuation boundary without introducing a competing interface-authority component. |
| P083-013 | Add the P070 Phase 6A relay carrier and optional direct-peer upgrade/fallback | done | The closed relay delivery envelope carries status, claim, control, invoke, and receipt schemas over the active epoch and filters observation versus actuation visibility from current Room grants. Relay selection and failover never alter exact interface grants, generation, lease, epoch, operation sequence, idempotency, or host policy. The three-node acceptance profile covers old-epoch refusal, endpoint failover, egress/evidence denial, membership revocation, P082 latest-state, and P083 fenced invoke carriage; direct peer remains an optional latency path. This post-MVP item does not reopen the completed P083-012 hard-MVP boundary. |
| P083-014 | Apply P082 operational context to interactive resources and actuation policy | todo | Reuse `sensorium-operational-context.v1` plus `source/generation-ref` in the common resource envelope; require them for collaborative or remote actuation; preserve them through status and receipts; enforce the inherited 512-byte summary cap; reject descriptor/source drift, old generations, and superseded directional publications; and replace all affected directions when source context changes. Policy tests prove that higher-impact targets can only narrow autonomy, lease, operation, and review posture, while a reasoned source-side correction remains possible through immutable replacement. Room and direct-peer carriers remain opaque and cannot lower the class, decide freshness, or create authority. |

Runtime implementation evidence promoted by P083-012 is owned by
`node:sensorium-interface-core/src/actuation.rs`,
`node:daemon/src/sensorium_interface_runtime/actuation_runtime.rs`,
`node:daemon/src/sensorium_interface_room_projection.rs`,
`node:daemon/src/host_capabilities_host.rs`,
`node:daemon/src/peer_runtime_host.rs`,
`node:daemon/src/interaction_broker_file_tree_provider.rs`, and the Workbench
service boundary. The focused and conformance tests cover schema families, Passport
scope, shared total order, saturation, registry refusal, lease/handoff/preemption
fencing, restart, honest partial failure, direct-peer LED invocation, Room dual
authority, observer continuity, remote identity at the PTY boundary, two-controller
real PTY input, provider-confirmed terminal close, and opaque evidence refs.

## Open Questions

No unresolved design questions remain for the initial hard-MVP implementation. The
former serialization, handoff, claim-notification, coordination-mode, and
reconciliation questions are resolved by decisions 22-26, and direct-peer profile
materialization is closed by decision 29. Any later relaxation requires operational
evidence and an explicit contract change; it is not an implementation-local
optimization.

## Next Actions

1. Collect operational evidence before reopening provider push, descriptor
   discovery, shared parallelism, or split management authority.
2. Measure relay and optional direct-peer latency against the same fenced requests;
   do not add P083-specific NAT traversal or carrier authority.
