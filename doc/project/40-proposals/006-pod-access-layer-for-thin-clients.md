# Pod-Backed Access Layer for Thin Clients

Based on:
- `doc/project/20-memos/pod-backed-thin-clients.md`
- `doc/project/20-memos/client-simplicity.md`
- `doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`

## Status

Proposed (Draft)

## Date

2026-03-21

## Executive Summary

This proposal defines `pod` as a later node module that serves human users
through thin mobile or desktop clients which do not need to run a local language model
or a fully capable communication-participating node.

This is no longer treated as a prerequisite of the networking MVP. The baseline
defined by proposal `014` assumes one operator-participant per Node, while any
thin client in that MVP remains only a delegated session or remote screen of the
same operator. `pod` begins where Orbiplex wants to go beyond that one-user-per-node
baseline.

The key decision is simple:

1. a thin client is a legitimate participation mode, not a degraded exception,
2. model execution, routing, and most swarm-facing protocol duties may live on the
   serving node,
3. the client should retain only the responsibilities that must stay close to the
   user device: interaction, local secret storage, optional local cache, and explicit
   user controls,
4. a user must be able to later migrate from a `pod`-backed client to a fuller node
   profile without losing identity continuity, history portability, or the right to
   exit.

## Context and Problem Statement

Orbiplex wants real swarm participation to remain available to people who:

- use mobile devices,
- use locked-down work machines,
- have weak hardware,
- lack stable connectivity,
- cannot safely operate a publicly reachable node,
- do not want to administer a full runtime stack.

Without a formal access layer, the project risks collapsing into an implicit elite
model where only users with enough hardware, bandwidth, and operational skill can
participate with full communicative agency.

The opposite extreme is also undesirable: if clients become opaque SaaS front-ends to
strong nodes, users lose sovereignty, portability, and intelligibility of trust
boundaries.

The missing middle is a formal `pod` model:

- the serving node provides heavy capabilities,
- the client remains intentionally thin,
- the trust and export boundaries are explicit,
- the user can move along an access gradient over time.

## Goals

- Make mobile and desktop thin clients a first-class participation profile.
- Define `pod` as the node-side module that hosts those users.
- Preserve user sovereignty despite delegated execution.
- Keep migration to a fuller node profile possible.
- Define explicit trust boundaries between user, thin client, and serving node.
- Define the minimum identity layers required so hosted users are not confused with
  node operators or individual client devices.
- Support degraded and partial-offline operation where feasible.

## Non-Goals

- This proposal does not define a full billing or compensation model for hosted users.
- This proposal does not define exact cryptographic key-management UX.
- This proposal does not require every federation to allow anonymous or public `pod`
  hosting.
- This proposal does not yet define the complete wire schema for every `pod` event.

## Decision

Orbiplex should adopt a **pod-backed access layer** as a post-MVP participation
extension, not as the baseline required to ship the first useful networking Node.

The baseline model is:

1. A node MAY expose a `pod` module that hosts one or more human users.
2. A thin client MAY rely on such a `pod` module for model execution, routing,
   session continuity, and swarm-facing communication.
3. A thin client does NOT need to ship with a local language model or full
   communication stack to be considered a valid Orbiplex client.
4. The user-facing system MUST make clear which functions are local and which are
   delegated to the serving node.
5. The user MUST retain exportability, account portability, and a path to exit or
   migrate to another node or fuller node profile.

## Proposed Model

### 1. Participation profiles

Orbiplex should explicitly recognize at least three participation profiles:

- `full-node` - operator runs a communication-capable node with local execution,
- `pod-client` - user operates through a thin client backed by a serving node's `pod`
  module,
- `hybrid` - user keeps some local capabilities (keys, caches, selected tools, maybe
  some local models) while delegating the rest.

The same human may move between these profiles over time.

### 2. What the `pod` module does

The node-side `pod` module is responsible for:

- user tenancy,
- session continuity,
- policy enforcement,
- model invocation,
- memory-space access according to granted scope,
- swarm routing on the user's behalf,
- action trace production,
- export and migration support.

`pod` is therefore not only a transport gateway. It is a bounded hosting layer for
delegated participation.

### 3. What the thin client does

The thin client should focus on:

- user interaction,
- secure local storage for device-scoped secrets,
- explicit consent and policy controls,
- local notification and UX state,
- optional encrypted cache for recent conversations or working material,
- offline drafting where feasible.

The client should avoid silently becoming a second hidden runtime. If it grows major
execution responsibilities, that should be treated as movement toward `hybrid` or
`full-node`, not as accidental client bloat.

### 4. Identity and tenancy model

At minimum, a `pod`-hosted user needs:

- a stable user-scoped identifier inside the serving node,
- a portable identity bundle or migration token,
- clear linkage between device sessions and the hosted user identity,
- explicit policy on whether the serving node may correlate multiple devices.

The serving node may authenticate the user in different ways, but the architectural
rule is that tenancy must not collapse into opaque operator ownership. The user is not
"just another local account" with no export or continuity rights.

### 4.1. Identity layers

The `pod` model introduces a third participation identity beyond node identity and
operator identity. At minimum, the architecture should distinguish:

- `node-id` - the serving node as the operational host and accountable infrastructure
  actor,
- `pod-user-id` - the hosted user as a distinct participant whose continuity,
  exportability, and participation rights must not collapse into operator ownership,
- `client-instance-id` - a concrete device or install instance used by that hosted
  user,
- optional public `nym` or scoped pseudonym - the presentation layer visible to other
  participants where policy allows it.

Where stronger identity continuity exists, `pod-user-id` may also point toward a
portable `anchor-identity` or another stable identity root. Where it does not, it
must still remain distinct from both `node-id` and `client-instance-id`.

This mirrors the existing `station-id` pattern in the root/nym model: many devices may
exist under one higher-order participant without automatically creating many
independent voices or reputations.

### 4.2. Separation of responsibility

These layers must not be collapsed because they answer different questions:

- `node-id` answers who hosted, routed, retained, and enforced policy,
- `pod-user-id` answers who participated, accumulated user-level history, and carries
  user-scoped rights or sanctions,
- `client-instance-id` answers which device/session was used and which concrete
  endpoint may have been compromised.

Compromise of one client instance should normally first affect that client instance or
session, not automatically the whole hosted user identity, and not automatically the
entire serving node.

### 5. Trust boundaries

The trust model should distinguish at least:

- what the device can protect locally,
- what the serving node can observe,
- what the federation can observe,
- what other swarm participants can infer.

At baseline:

- the serving node can usually observe plaintext prompts and outputs unless stronger
  end-to-end mechanisms are used,
- the device should protect its own local secrets and local unlock path,
- the system should make delegated trust visible rather than pretending the user is
  self-hosted.

This keeps sovereignty honest: a `pod-client` user may participate meaningfully, but
must know where trust has been delegated.

### 6. Session and continuity model

`pod` should preserve continuity across:

- reconnects,
- device changes,
- intermittent connectivity,
- temporary use of shared or weak devices.

This implies server-side session state with bounded retention and explicit export. A
lost phone should not imply loss of the user's entire participation history, but a
serving node should also not keep indefinite undeclared memory by default.

### 7. Degraded and offline behavior

A thin client cannot match the resilience of a full node, but it should still degrade
gracefully.

Recommended baseline:

- read-only access to cached recent state when offline,
- ability to draft messages or notes locally for later sync,
- explicit UI when an action requires a live serving node,
- optional fallback to another trusted `pod` host after migration or recovery.

The key rule is clarity: offline inability should be explicit, not masqueraded as
local execution.

### 8. Migration and right to exit

Migration is a constitutional requirement for this model, not a nice-to-have.

A `pod`-hosted user should be able to:

- export their data and conversation history,
- export or transfer portable identity material according to federation policy,
- move to another `pod` host,
- upgrade into a `hybrid` or `full-node` profile,
- leave without protocol-level lock-in.

The access layer fails its purpose if convenience for hosted users turns into hidden
capture.

### 9. Minimal contract sketch

The full schema can come later, but `pod`-backed participation should expose at least
semantics equivalent to:

```json
{
  "profile/type": "pod-client",
  "pod/id": "pod:pl-wro-node-7f3c:user-42",
  "serving-node/id": "node:pl-wro-7f3c",
  "pod-user/id": "pod-user:did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
  "client-instance/id": "client:ios-a13-82d1",
  "models/local?": false,
  "session/state": "attached",
  "export/capable?": true,
  "migration/allowed?": true
}
```

These fields may be implemented directly or deterministically derived from richer
state, but their semantics must exist.

## Trade-offs

1. Accessibility vs sovereignty purity:
   - Benefit: far more people can participate.
   - Cost: some trust moves from local machine to serving node.
2. Simplicity vs hosting complexity:
   - Benefit: very lightweight client UX.
   - Cost: `pod` host must take on tenancy, security, and policy burden.
3. Fast onboarding vs stronger local guarantees:
   - Benefit: lower friction for mobile and weak devices.
   - Cost: weaker local autonomy unless hybrid/full-node migration remains real.

## Failure Modes and Mitigations

### 1. Hidden lock-in

Failure:
- the user becomes dependent on one `pod` host with poor export or migration support.

Mitigation:
- require explicit export semantics,
- require migration path as part of baseline contract,
- expose hosted profile clearly in UX and policy.

### 2. Opaque trust delegation

Failure:
- user believes they are operating locally while the serving node sees everything.

Mitigation:
- explicit trust-boundary disclosure,
- device UI that labels delegated execution,
- policy metadata on what the serving node may observe or retain.

### 3. Client bloat

Failure:
- the "thin" client silently accumulates hidden runtime complexity.

Mitigation:
- preserve profile taxonomy,
- treat major local execution additions as `hybrid` profile evolution,
- keep the baseline client contract intentionally narrow.

### 4. Hosting abuse

Failure:
- a `pod` operator overreaches, surveils users, or distorts participation.

Mitigation:
- auditable hosting policy,
- export and migration rights,
- reputation and governance constraints on serving nodes,
- possibility of federation-specific trust thresholds for `pod` hosts.

## Open Questions

1. What minimum local secret material must stay on-device for a `pod-client` user?
2. Should a single `pod` host be allowed to serve pseudonymous multi-user communities,
   or should some federations require stronger user attestation?
3. Which actions must be impossible without explicit live confirmation from the user
   device?
4. How much user history should a `pod` host retain by default?
5. Should `pod` hosting reputation be separate from general node reputation?
6. Should `pod-user-id` be a strictly host-local identity, or should federations allow
   portable cross-host continuity by default?

## Next Actions

1. Define `pod` module requirements: tenancy, export, migration, retention, and trace
   semantics.
2. Define thin-client requirements for mobile and desktop profiles.
3. Define trust-boundary UX requirements so delegated execution is always explicit.
4. Define migration stories: `pod-client -> another pod`, `pod-client -> hybrid`,
   `pod-client -> full-node`.
5. Define a dedicated identity and responsibility model for `pod-user-id` and
   `client-instance-id`.
