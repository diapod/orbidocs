# Node Transport and Discovery MVP

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/30-stories/story-001-swarm-node-onboarding.md`
- `doc/project/60-solutions/000-node/000-node.md`

## Status

Accepted / hard-MVP implemented in the Node transport/discovery baseline.

The implemented cut includes stable node and participant identity, signed
endpoint advertisements, WSS/TLS carrier sessions, signed peer handshakes,
encrypted session frames, capability advertisement exchange, keepalive and
reconnect behavior, durable peer/advertisement state, network traces, and the
participant-scoped `signal-marker-envelope.v1` first application slice.

Post-MVP work remains for live node-id continuity/succession policy, richer
federation-wide peer-governor policy, richer hosted-user policy/read-models and
federated continuity above the minimal client-instance lifecycle, and broader
discovery-policy productization. Those layers extend the transport seed; they
are not blockers for the P014 hard-MVP baseline.

## Date

2026-03-23

## Executive Summary

This proposal defines the smallest practical networking seed on which the first
useful Orbiplex Node can be built.

The key decisions are:

1. MVP networking addresses **nodes**, not user nyms.
2. A Node needs a stable local **node identity** and a stable **participant role
   identity** before it can participate in the network without later role
   collapse.
3. Discovery should map **`node-id -> current signed endpoint advertisement`**, not
   `nym -> IP:port`.
4. The default transport should be **WSS over TCP 443**, with seed peers or a seed
   directory for bootstrap.
5. Direct TCP and UDP/NAT traversal are later optimizations, not day-one
   dependencies.
6. The first end-to-end protocol slice should be:
   - identity load/generation,
   - handshake,
   - capability advertisement,
   - keepalive,
   - and one simple signed application message.
7. The first useful signed application message should be **`signal-marker`**.
8. The first seed directory should support both advertisement fetch and
   advertisement publication.
9. MVP capability advertisement should expose only the **narrow core**, not
   attached roles or plugin-process surfaces as required semantics.
10. MVP capability IDs should be **schematic**, with at least one required core
    placeholder:
    - `core/messaging`
11. In the MVP baseline, one Node has one operator-participant by default:
    - `node-id` names the infrastructure role,
    - `participant-id` names the participation role,
    - both MAY share the same base `did:key`,
    - but the protocol must still treat them as distinct roles.

## Context and Problem Statement

Orbiplex already has richer protocol ideas:

- question envelopes,
- answer rooms,
- procurement,
- Whisper,
- archival handoff,
- and attached roles.

At proposal time, what was still missing for practical Node implementation was
a minimal networking baseline that says:

- how a node identifies itself,
- how another node finds it,
- how a session is established,
- what the first shared message shape looks like,
- and what can be postponed without blocking the first working Node.

Without that seed, Node implementation stays trapped in architecture talk.

## Goals

- Define the smallest credible Node networking baseline.
- Separate node identity from user or contextual nyms.
- Separate infrastructure role from participation role from day zero.
- Keep discovery simple enough for the first implementation.
- Make transport compatible with difficult real-world networks.
- Provide a practical implementation seed that can be mapped into the Node repo.

## Non-Goals

- This proposal does not define full multi-user `pod` tenancy, root identity, or PoP.
- This proposal does not define a global public nym registry.
- This proposal does not require DHT, libp2p, or generalized peer-to-peer routing.
- This proposal does not define final room semantics.
- This proposal does not define final federation governance or reputation policy.

## Decision

Orbiplex should adopt the following networking MVP baseline:

1. each Node has a locally generated long-lived keypair,
2. `node-id` is derived from the node public key as a strict `node:did:key` identifier,
3. `participant-id` is derived and persisted as a distinct role identifier even in
   the one-operator-per-node MVP,
4. transport baseline is `WSS/443`,
5. bootstrap uses:
   - statically configured seed peers as the mandatory first bootstrap layer,
   - with a minimal seed directory only as an optional extension after that,
6. discovery exchanges signed endpoint advertisements,
7. peers establish a signed handshake and exchange capability advertisements,
8. the first always-supported maintenance flow is `ping/pong` and reconnect.

This means that full nym systems, advanced relay graphs, and rich room protocols can
come later without blocking the first useful networked Node.

## Proposed Model

### 1. Minimal node identity

Each Node should have:

- a local long-lived keypair,
- a stable `node-id` derived from the public key,
- a stable `participant-id` role identifier,
- and a persisted local identity file.

For Ed25519 in v1, the canonical `node-id` format should be:

- `node:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`

The canonical `participant-id` format should be:

- `participant:did:key:z<base58btc(0xed01 || raw_ed25519_public_key)>`

This means:

- the underlying public-key fingerprint uses the `did:key` Ed25519 shape,
- `z...` is the base58btc multibase fingerprint,
- `node:` is the Orbiplex-specific technical identity prefix,
- parsers should be strict,
- and alternative textual forms should not be accepted in v1.

That persisted identity record should expose only public identity material plus
one local secret reference:

- `participant/id`
- `key/storage-ref`

For the MVP baseline, that reference should use:

- `local-file:identity/node-signing-key.v1.json`

This keeps the identity record separate from the secret backend from day one and
avoids a later migration away from inline private-key material.

This is enough for:

- peer addressing,
- role-aware participant attribution,
- signing handshake material,
- signing advertisements,
- and replay-resistant session establishment.

This MVP identity is **not** the same thing as:

- multi-user `pod-user` identity,
- root identity,
- anchor identity,
- `custodian_ref`,
- or a public contextual nym.

Those are higher-layer concerns.

For the MVP baseline, `node-id` and `participant-id` MAY share the same base
`did:key` fingerprint and therefore the same signing key material. The protocol
must nevertheless treat them as distinct role identifiers. Shared key material
is an operational simplification for the one-operator-per-node baseline, not a
protocol guarantee that later runtimes may rely on.

### 1.1. Role split in the MVP baseline

The first networking baseline should already distinguish:

- `node-id` for infrastructure-facing actions,
- `participant-id` for participation-facing actions.

In practice this means:

- endpoint advertisements, peer handshakes, keepalive, and other transport or
  discovery artifacts are `node-id`-scoped,
- first application-level messages such as `signal-marker` are
  `participant-id`-scoped,
- reputation and sanctions may later attach to different roles even when the
  same operator currently uses both.

This split is intentional. The handshake answers "do I trust this infrastructure
endpoint enough to establish a channel?", while application messages answer "do
I trust this participant acting over that channel?". Those are different
questions and should remain in different protocol layers.

This role split is normative even when both identifiers are backed by the same
keypair in MVP.

For boundary discipline, the networking MVP should know exactly two protocol-level
identity handles:

- `node-id` for infrastructure trust, addressing, advertisements, handshake, and
  keepalive,
- `participant-id` for participant-scoped message authorship and participation
  reputation carried over the established channel.

It should not depend on higher identity layers such as:

- `anchor-identity`,
- `pod-user-id`,
- public or contextual `nym`,
- or federation-local continuity bindings.

Those remain application-layer concerns. If a later networking implementation
starts importing those concepts as hard dependencies, the abstraction boundary is
leaking rather than improving.

The same is true for `nym` handling:

- networking MUST NOT require `nym` resolution,
- `nym` verification belongs to the application layer,
- transport sees only `node:did:key:...` and `participant:did:key:...`,
- and `nym` signatures are verified above the established encrypted session.

### 1.2. Thin clients in MVP

MVP does not require a multi-user `pod` model.

If a Node exposes a remote UI or thin-client surface in the MVP baseline, that
client should be treated as a delegated session or remote screen of the same
operator-participant, not as a separate hosted participant with its own
independent continuity layer.

### 1.3. Future participant bind over the established channel

Post-MVP multi-user or hosted-user participation should not widen
`peer-handshake.v1` into a transport-plus-participant artifact.

Instead, a later layer may introduce a participant-scoped session bind carried
over the already established encrypted `node↔node` channel. That later artifact
may be named something like:

- `participant-session.v1`, or
- `participant-bind.v1`

and should bind at least:

- `participant-id`,
- `via node-id`,
- a live session reference or channel context,
- and participant-side proof material.

This keeps transport authentication and participant authentication stratified:

- `peer-handshake.v1` answers whether the infrastructure endpoint is trusted,
- a later participant bind answers which participant is speaking through that
  endpoint.

In the MVP baseline this layer is implicit because `participant-id` and `node-id`
may share the same base `did:key`, and participant-scoped application messages can
therefore be verified directly without an extra bind artifact.

The first concrete schema seed for that later layer now lives in:

- `doc/schemas/participant-bind.v1.schema.json`

That schema is now an accepted, closed admission contract: unknown top-level
fields and unknown signature fields are rejected by schema validation before any
post-channel runtime may treat it as authority.
There is no lenient unknown-field compatibility mode for this freeze; producers
that need additional metadata must add an explicit schema field or a formal
extension point first.

The first concrete post-MVP consumer of that bind is expected to be the thin-client
or hosted-user attachment artifact:

- `doc/schemas/client-instance-attachment.v1.schema.json`

Its smallest lifecycle companion should be the matching detach artifact:

- `doc/schemas/client-instance-detachment.v1.schema.json`

The next post-MVP lifecycle companion may recover client access after loss or
migration through:

- `doc/schemas/client-instance-recovery.v1.schema.json`

The three `client-instance-*` schemas are also accepted, closed admission
contracts and are schema-gated as post-channel lifecycle artifacts. They remain
above the established session and embedded participant bind; they are not
handshake fields. As with `participant-bind.v1`, ad-hoc top-level metadata is
rejected rather than silently ignored.

Rotation is also deferred as a richer operational layer. In the hard-MVP
transport baseline:

- a new Ed25519 key means a new `node:did:key` and therefore a new `node-id`,
- overlap and succession proofs are an operational procedure rather than a live
  runtime feature,
- and persisted identities used by the MVP runtime should remain `active`.

The first post-MVP succession slice is now scoped as a local proof contract, not
as automatic continuity. It starts with local import/export, validation, pure
verification, and operator acceptance surfaces. The intended later direction is
Seed Directory publication and replay, but that is not part of the first NT-018
runtime slice.

### 2. Discovery baseline

The first discovery target should be:

- `node-id -> current endpoint advertisement`

not:

- `nym -> IP:port`

The healthier MVP is:

- the Node knows one or more seed peers,
- or the Node knows one minimal seed directory endpoint,
- peers publish to and fetch from signed endpoint advertisements,
- advertisements expire through TTL and must be refreshed.

The implementation baseline should therefore begin with a local static seed list,
not with a mandatory remote directory.

That seed list may carry, for local operator convenience:

- stable `node-id`,
- bootstrap address,
- and an optional human-friendly local label or self-chosen name.

Such labels are operational hints only. They are not part of `node-id`, are not
signed network identity, and may change without affecting protocol semantics.

For `node-advertisement.v1`, the signed surface should use a sign-then-attach
pattern:

- sign the whole semantic advertisement payload,
- exclude only the `signature` field itself,
- and exclude only transport-mutable per-hop metadata if a later wire wrapper
  carries such fields outside the semantic payload.

That payload should include at least:

- `advertisement/id`,
- `node/id`,
- `sequence/no`,
- `advertised-at`,
- `expires-at`,
- key material,
- endpoint set,
- and transport support claims.

The signing input for v1 should be:

- `node-advertisement.v1\x00 || deterministic_cbor(payload_without_signature)`

This gives domain separation, deterministic verification, and malleability
resistance. If a later wire framing carries raw advertisement bytes, receivers
should verify those exact bytes rather than re-canonicalizing them.

The first byte-exact advertisement conformance vector now lives in:

- `doc/project/20-memos/networking-signing-conformance-vectors.md`

For discovery state, v1 should treat advertisements as:

- one current active advertisement per `node-id`,
- with the highest seen `sequence/no` replacing older advertisements,
- and stale or equal sequence numbers rejected as non-current.

That current-advertisement view is not just an optimization. For the MVP done
state it should already exist as a local persistence cache:

- `WSS` client/server alone is not enough,
- the Node should durably remember the freshest known advertisement per
  `node-id`,
- and outbound dialing or reconnect should reuse that cache rather than depend
  on live rediscovery every time.

This keeps one coherent transport view per node identity and avoids conflicting
capability or endpoint state for the same `node-id`.

To prepare the later rotation layer without turning it into a live MVP feature,
node-id succession should be expressed as a separate proof artifact rather than
as an inline `node-advertisement.v1` field. Advertisements remain reachability
facts for their own `node-id`; a succession proof is a different fact that may
link `old-node-id -> new-node-id` under explicit local policy.

If a minimal seed directory is deployed, its first useful API should remain
narrow:

- `PUT /adv/{node-id}`:
  - publish or replace one signed advertisement if `sequence/no` is newer,
- `GET /adv/{node-id}`:
  - fetch the current signed advertisement for one node,
- `GET /adv?since={cursor}`:
  - fetch advertisements incrementally in small batches,
- no explicit delete endpoint:
  - expiry is TTL-driven.

This keeps the directory as a signed cache rather than a trust gate. Read access
should remain open, and write access should remain open to any correctly signed
publisher, but rate-limited and freshness-checked.

Proposal 025 and proposal 043 add a stricter operational profile for Seed
Directory deployments that issue `node-address-attestation.v1`: such a
deployment may actively probe the advertised WSS endpoint before accepting
`PUT /adv/{node-id}` and again before issuing `directory-confirmed` address
evidence. That probe is still address evidence, not capability authorization.

Explicit full-dump directory listing should be avoided in the first design,
because it turns the seed directory into a trivial topology-scraping endpoint.

Minimal request and response examples for that HTTP surface now live in:

- `doc/project/20-memos/seed-directory-http-examples.md`

### 3. Transport baseline

The default transport should be:

- `WSS` over TCP `443`

because it is:

- proxy-friendly,
- firewall-friendly,
- viable in mixed enterprise and consumer networks,
- already aligned with the broader communication proposal corpus.

Later transport layers may add:

- direct TCP,
- UDP hole punching,
- relay optimization,
- or more specialized transports.

But those should not block MVP.

For the MVP baseline, `WSS` should be treated as a carrier transport layer, not
as the primary identity protocol.

This means:

- TLS server authentication proves control of the advertised endpoint and gives
  baseline confidentiality and integrity for the carrier connection,
- Node-to-Node identity authentication still happens at the signed
  `peer-handshake.v1` layer,
- mutual TLS and client-certificate identity are not required for the MVP
  networking baseline,
- and reconnect should assume a fresh transport plus a fresh signed handshake,
  not protocol continuity derived from TLS session resumption.

For public `wss://` endpoints, the client should validate the presented server
certificate against the hostname carried in the advertised endpoint URL using
normal WebPKI rules.

For controlled or private deployments, additional local trust roots may be
configured out of band by the operator, but this trust configuration should stay
deployment-local:

- it should not become protocol semantics,
- and `node-advertisement.v1` should not carry TLS certificate blobs, pinsets,
  or custom trust material in the MVP baseline.

When multiple endpoints are present in one advertisement, the receiver should:

1. filter out unsupported transports,
2. prefer the sender-advertised endpoint priority among compatible endpoints,
3. still allow local runtime constraints to override that hint.

In v1 this mostly reduces to ordered preference among `wss` endpoints. Wider
transport ranking can be added later when more than one transport family is
actually standardized.

### 4. Session baseline

The first session lifecycle should be:

1. connect to seed or known peer over WSS,
2. send signed `peer-handshake`,
3. receive signed `peer-handshake-ack`,
4. exchange `capability-advertisement`,
5. maintain liveness with `ping/pong`,
6. reconnect and refresh advertisement when needed.

For the MVP baseline, this should not mean maintaining a full mesh of permanent
connections to all known peers. A healthier default is:

- keep a small active working set of long-lived sessions,
- target `2` active `hot` peer sessions as the normal default,
- allow temporary probes or overlap up to `4` live sessions,
- keep other known peers in discovery state (`cold` or `warm`) until they are
  actually needed.

This gives redundancy without turning discovery into an always-connected flood
of idle TCP/WSS sessions.

The MVP leaves room for a federation-wide peer-health or peer-governor policy.
The current local runtime already exposes `peer-status.v1` as an
operator-facing read model and classifies peers as `cold`, `warm`, `hot`, or
`blocked` from observed session quality, repeated failures, explicit local
policy, and operator decisions. Cross-directory or reputation-weighted peer
governance remains a later policy layer rather than a transport-handshake
concern.

For abuse control at this layer, rate limiting and backpressure should remain
per-node rather than per-participant or per-nym. If one node emits too much
traffic through many participant-scoped or nym-scoped application artifacts,
peers should degrade the node-level relationship instead of forcing nym
resolution into the transport boundary.

This baseline should use a two-message handshake:

- `hello -> ack`

not:

- `hello -> challenge -> ack`

The `ack` is sufficient as the response-binding step in v1, provided that it
cryptographically binds to the original initiation attempt.

For `peer-handshake.v1`, the signed surface should also use sign-then-attach:

- sign the semantic handshake payload,
- exclude only the `signature` field itself,
- and keep framing-only transport metadata outside the signed payload.

The signed payload should bind at least:

- `handshake/id`,
- `handshake/mode`,
- `sender/node-id`,
- optional `recipient/node-id` when directed,
- `ts`,
- `nonce`,
- `ack/of-handshake-id` when present,
- any offered capability claims,
- and any negotiated terms.

The signing input for v1 should be:

- `peer-handshake.v1\x00 || deterministic_cbor(payload_without_signature)`

`peer-handshake.v1` remains node-scoped in v1. It should authenticate the
serving infrastructure endpoint, not the later participant role speaking over
that encrypted channel.

For v1 session establishment, the long-lived Node identity remains the
`node:did:key:...` Ed25519 signing identity. The corresponding static X25519
key-agreement public key may be deterministically derived from that identity key
for the DH terms that bind long-lived identity to the session attempt.

This means MVP does not need any additional static X25519 field in
`node-identity.v1` or `node-advertisement.v1`.

It also means `peer-handshake.v1` does not need to carry `participant-id`.
Participant authentication belongs at the application-message layer over the
already established node-to-node session, not inside the transport-session
handshake itself.

The same boundary applies to higher identity layers:

- `peer-handshake.v1` should not depend on `anchor-identity`,
- it should not depend on `pod-user-id`,
- and it should not route or negotiate on `nym`.

Those concepts may later appear in application payloads or participant-bound
artifacts, but they are outside the MVP transport-session contract.

`peer-handshake.v1` SHOULD instead carry:

- a fresh per-handshake ephemeral X25519 public key in `session/pub`,
- encoded as raw unpadded base64url for the 32-byte X25519 public key,
- without `did:key`, multicodec prefixes, or identity wrappers.

This keeps the layers distinct:

- identity layer:
  - `node:did:key:...` -> Ed25519 signing identity, with static X25519 derivable for DH,
- session layer:
  - `session/pub` -> fresh ephemeral X25519 public key for the current handshake.

For the Noise-IK-like v1 baseline, the intended session derivation uses:

- `DH1 = X25519(EK_initiator, IK_responder_derived_x25519)`
- `DH2 = X25519(IK_initiator_derived_x25519, EK_responder)`
- `DH3 = X25519(EK_initiator, EK_responder)`

Forward secrecy in v1 relies primarily on fresh ephemeral keys and the `DH3`
term, not on the long-lived identity-derived DH terms alone.

This is accepted as a pragmatic MVP compromise. It does not provide ideal key
separation between signing and key agreement, and may later evolve into a richer
continuity or rotation model.

`ack/of-handshake-id` must be signed, because it cryptographically binds the
response to one concrete initiation attempt. Protocol version belongs in the
interpretation context and domain separator, not in the core semantic payload.
Per-hop transport profile should remain framing metadata unless it is being
asserted as a capability claim.

For reachability probes, `peer-handshake.v1` may also carry
`probe/challenge` and `probe/purpose`. These fields are not transport
framing metadata: when present, they are part of the signed semantic payload.
Seed Directory uses this to produce `directory-confirmed`
`node-address-attestation.v1` evidence: the directory sends a fresh challenge,
the target node answers with a signed `ack`, and the resulting transcript hash
can be attached to address evidence without exposing plaintext transcript
material.

In v1 the handshake family should stay symmetric at schema level:

- the same `peer-handshake.v1` family covers both `hello` and `ack`,
- `ack/of-handshake-id` is the binding field that turns the second message into
  the acknowledgment of the first,
- and the existing `handshake/mode` field may remain as an explicit discriminator
  for clarity and easier interoperability, even though the semantic asymmetry is
  already visible through `ack/of-handshake-id`.

The first positive `ack` fixture and byte-exact handshake signing vector now live
close to the schema layer:

- `doc/schemas/examples/bootstrap.ack.peer-handshake.json`
- `doc/project/20-memos/networking-signing-conformance-vectors.md`

Replay resistance for the baseline handshake should be defined by:

- a clock-skew window of `+-30s`,
- a per-peer nonce cache with retention of roughly `120s`,
- and a local pending-handshake timeout of `30s` for outstanding `hello`
  attempts.

This baseline is aligned with a Noise-IK-style two-message authenticated
exchange, but the current MVP still treats transport framing and later session
crypto details as separable from the semantic handshake contract.

Within that boundary, `ping/pong` is more than a transport convenience. In the
MVP it remains only a liveness primitive, but it is already the seed of a later
peer governor: the same signals can later feed health tracking, degradation,
promotion, reconnect policy, and eventual `cold/warm/hot/blocked` transitions.

Even though full peer-governor semantics remain deferred, the MVP should
already expose the smallest peer-state transition traces:

- `peer/discovered`
- `peer/connected`
- `peer/disconnected`

Without those, an operator cannot tell whether the node is isolated, flapping,
or gradually building a live peer set.

The capability advertisement should not try to describe the whole implementation.
It should publish passport-form capability assertions plus one small
wire-visible projection for fast matching.

The projection remains a small set of schematic core capability identifiers,
such as:

- required minimum:
  - `core/messaging`
- optional additions:
  - `core/discovery`
  - `core/relay`
  - `core/keepalive`

Capabilities that are already implicit in the successful execution of the
handshake, such as "can sign the handshake" or "is a protocol participant",
should not be modeled as mandatory advertised core capabilities in v1.

Capability advertisement is the Node-to-Node and datagram-friendly way to
communicate capabilities without requiring a Seed Directory lookup. Each
presented capability should carry a passport or passport-compatible assertion:

- `capability/id` — canonical capability id,
- `wire/name` — routing projection such as `core/messaging`,
  `role/seed-directory`, or `sovereign/audio-transcription`,
- `assertion/kind` — `self-issued-passport`, `issuer-passport`, or
  `federation-endorsed-passport`,
- `passport` — the credential the receiver verifies under the capability
  profile and local policy,
- optional `capability/profile` — short display metadata plus `schema/id`,
  `schema/ref`, and `schema/media-type` for machine negotiation.

This keeps custom capabilities out of a chaotic global taxonomy. A custom
capability can live in the same passport namespace as other capabilities, for
example:

- `audio-transcription@participant:did:key:z...`
- `~audio-transcription@participant:did:key:z...`

`capabilities/core` remains a compatibility and routing projection. It should
be derivable from `capabilities/presented[*].wire/name`; it is not the
authoritative proof.

The advertisement answers "what capabilities does this peer present right now,
with what credentials?". The passport answers "under which issuer, scope, and
policy may this node be accepted for this capability profile?".

If a presented capability includes `schema/ref`, the referenced
`capability-schema.v1` artifact should be fetchable over the authenticated peer
message channel with:

- `capability.schema.present.request`
- `capability.schema.present.response`

The `schema/ref` is content-addressed. Receivers must verify fetched schema
content against that reference before using it for scope, input, output, error,
or retry validation. A `doc/url` may exist as a human mirror, but it is not a
runtime dependency.

### 5. First useful message slice

After handshake and capability exchange, the first application-level slice should be
very small.

The first useful signed message should be:

- one simple signed `signal-marker` message scoped to `participant-id`.

The point is that Node can:

- sign it,
- validate it,
- send it,
- receive it,
- and trace it end to end.

Higher-layer publication such as reduced `question-envelope` may follow later, once
the seed transport and session slice is already proven end to end.

At this stage the proposal freezes the **semantic** `signal-marker` decision, not
and now also freezes the canonical participant-scoped publication envelope for
that marker. `signal-marker-envelope.v1` is the minimal signed wire artifact,
while the separately visible `signal-marker.v1` marker remains the semantic or
UI-facing artifact it may reference.

## Operational and Implementation Boundaries

### Required done state

For the networking MVP, required done state is broader than "a WSS client and
server can talk".

It already includes:

- persisted local identity with import/export validation,
- advertisement persistence cache with monotonic replacement,
- signed advertisement publish/fetch,
- signed handshake plus encrypted session establishment,
- capability exchange,
- keepalive and reconnect,
- and the first participant-scoped `signal-marker` send/receive slice.

### Minimal trace surface

The MVP should freeze one small but explicit network trace vocabulary.

Required event families:

- `identity/loaded`
- `identity/generated`
- `advertisement/published`
- `advertisement/fetched`
- `advertisement/rejected`
- `peer/discovered`
- `peer/connected`
- `peer/disconnected`
- `handshake/started`
- `handshake/accepted`
- `handshake/rejected`
- `session/established`
- `capability/exchanged`
- `keepalive/lost`
- `keepalive/restored`
- `signal-marker/sent`
- `signal-marker/received`
- `error/occurred`

Each event should share at least one bounded skeleton:

```json
{
  "trace/id": "tr:01JV...",
  "event/type": "handshake/rejected",
  "ts": "2026-03-28T14:12:00Z",
  "node/self": "node:did:key:z6MkA...",
  "peer": "node:did:key:z6MkB...",
  "detail": {
    "code": "E_HS_REPLAY"
  }
}
```

`node/self` is part of the contract because operators may aggregate traces from
many nodes.

### Frozen MVP boundary error classes

The networking MVP should freeze eleven stable machine-readable boundary codes:

- `E_TRANSPORT_UNAVAILABLE`
- `E_TRANSPORT_REJECTED`
- `E_ADV_EXPIRED`
- `E_ADV_STALE_SEQ`
- `E_SIG_INVALID`
- `E_SIG_UNKNOWN_SIGNER`
- `E_HS_REPLAY`
- `E_HS_UNKNOWN_REF`
- `E_PROTO_VERSION`
- `E_PROTO_INVALID`
- `E_PROTO_CAP_MISSING`

Those codes group into the following classes:

- `transport/unavailable`
- `transport/rejected`
- `advertisement/expired`
- `advertisement/stale-sequence`
- `signature/invalid`
- `signature/unknown-signer`
- `handshake/replay-suspected`
- `handshake/unknown-ref`
- `protocol/version-mismatch`
- `protocol/invalid-contract`
- `protocol/capability-missing`

The class and code are for machines; context and peer details are for
operators. Those concerns should stay separate.

### Schema-gate boundary

`schema-gate` should validate not only JSON ingress/egress received from the
network, but also identity-file import/export as a required runtime boundary.

That means:

- `node-identity.v1` import and export already belong in the required MVP gate,
- network ingress/egress still covers `node-advertisement.v1`,
  `peer-handshake.v1`, and `capability-advertisement.v1`,
- and post-networking participant binding may widen that gate later without
  collapsing transport and application layers.

## MVP Seed Checklist

1. Define local Node identity file format. **Done.**
2. Freeze `node-id` derivation rule as strict `node:did:key`. **Done.**
3. Define signed endpoint advertisement shape. **Done.**
4. Define peer handshake shape. **Done.**
5. Define capability advertisement shape. **Done.**
6. Define keepalive and reconnect behavior. **Done.**
7. Define seed peer / seed directory configuration. **Done.**
8. Implement load-or-generate local identity. **Done.**
9. Implement WSS bootstrap connection to a seed peer. **Done.**
10. Implement signed handshake and handshake acknowledgment. **Done.**
11. Implement capability advertisement exchange. **Done.**
12. Implement `ping/pong` / equivalent keepalive. **Done.**
13. Implement `signal-marker` end to end as the first signed application message. **Done.**
14. Add required network traces and diagnostics for:
    - identity load/generation,
    - advertisement publish/fetch/reject,
    - peer discovered/connect/disconnect,
    - handshake start/accept/reject,
    - session established,
    - capability exchange,
    - keepalive lost/restored,
    - signal-marker send/receive,
    - and `error/occurred`.
    **Done.**
15. Freeze the eleven MVP boundary error classes and their stable wire-visible codes. **Done.**
16. Treat advertisement persistence cache and identity import/export schema validation as part of required done state, not later polish. **Done.**

## Implementation Reconciliation

Reconciled on 2026-06-29 against:

- `node:docs/MVP.md`
- `node:docs/implementation-ledger.toml`
- `node:protocol`
- `node:network`
- `node:peer-runtime`
- `node:daemon`
- `node:tools/acceptance/story-000-operator`

The hard-MVP interpretation is that P014 closes the minimal transport seed, not
the entire future networking program. In that interpretation:

- identity import/export, strict role ids, `local-file:` key storage, and active
  identity checks are present;
- signed `node-advertisement.v1` publication, replacement, expiry, and durable
  cache behavior are present;
- WSS/TLS carrier handling, signed `peer-handshake.v1`, 3DH-derived encrypted
  frames, replay protection, keepalive, reconnect, peer supervisor lifecycle,
  peer quality scorecards, and manual block/unblock are present;
- `capability-advertisement.v1` exchange is present and tied into the checked
  capability registry / authorization policy path;
- `signal-marker-envelope.v1` is implemented as the first participant-scoped
  signed message above the encrypted session;
- Story 000 provides the operator-facing two-node smoke path for the baseline.

The open work is now post-MVP expansion:

- live succession/continuity semantics for changing `node-id`;
- richer federation-level peer-governor policy and cross-directory discovery
  reconciliation;
- richer hosted-user policy, UI/read-models, and federated continuity above the
  minimal post-channel participant-bind/client-instance lifecycle;
- additional transports or NAT traversal beyond the WSS seed.

## Document Seed Needed Next

The next minimal schema set should likely be:

1. `node-identity.v1`
2. `node-advertisement.v1`
3. `peer-handshake.v1`
4. `capability-advertisement.v1`
5. `participant-bind.v1`
6. `client-instance-{attachment,detachment,recovery}.v1`

Operator-local read models:

5. `peer-status.v1`

This read model formalizes local peer-health tracking and governor-oriented
transitions such as `cold -> warm -> hot -> blocked`. It is not a handshake
field and does not make federation-wide trust decisions.

## Trade-offs

1. WSS/443 vs custom raw transport:
   - Benefit: works sooner in real networks.
   - Cost: less transport purity and some framing overhead.
2. Seed peers/directory vs global decentralized discovery:
   - Benefit: much lower bootstrap cost.
   - Cost: less ideological purity in the first version.
3. Node identity first vs full nym model first:
   - Benefit: practical implementability.
   - Cost: higher-layer identity remains deferred.
4. Minimal handshake first vs complete protocol family first:
   - Benefit: one working slice sooner.
   - Cost: more protocol surface still pending.

## Remaining Open Questions

None for the hard-MVP transport seed. Static seed peers are sufficient for the
baseline, and the implemented Seed Directory path is an optional discovery
extension above that seed.

NT-018 node-id succession decisions are frozen for the first implementation
slice:

1. The first proof lifecycle is local import/export plus schema-gate validation.
   Future Seed Directory publication is the desired direction, but not required
   for the first slice.
2. Both the old `node-id` key and the new `node-id` key sign the same canonical
   payload.
3. `expires-at` is required.
4. `revocation/ref` is optional in v1.
5. Only one active successor is accepted per old `node-id` by default.
6. Discovery and peer stores may mark a successor candidate, but routing may use
   it only under an explicit `accept-node-succession` policy grant.
7. The signed surface is canonical JSON without signature fields, with domain
   separation.
8. The proof contains `succession/mode` and optional `reason/ref`.
9. The first implementation includes operator API import, list, accept, and
   reject surfaces. A richer UI surface remains optional.
10. Endpoint evidence and TLS pins do not transfer automatically; the successor
    node must have its own endpoint evidence.

The local NT-018 slice is implemented in Node as of 2026-06-29:
`node-succession.v1` is schema-gated, generated by
`/v1/identity/rotation/prepare`, imported and accepted through
`/v1/operator/node-succession/*`, persisted as a local operator decision, and
covered by Story 000 `rotation-smoke`. Seed Directory publication/replay of
succession proofs and automatic endpoint-evidence migration are deliberately
not part of this slice.

Decisions after the local NT-018 slice:

1. `/v1/operator/node-succession/{succession_id}/accept` derives
   `accepted_by`, `accepted_at`, and `policy_ref` from the host. The request body
   may carry only optional operator rationale. Even in the local single-operator
   slice, the acceptance fact is consumed by later routing policy, so host-attested
   provenance is required and caller-supplied provenance is rejected.
2. `/v1/operator/node-succession/{succession_id}/reject` follows the same
   provenance rule: `rejected_by` and `rejected_at` are host-derived, and the
   request body may carry only the rejection reason. Reject facts are audit
   facts, not caller-authored claims.
3. `accept-node-succession:*` must resolve through the local policy registry
   before the peer governor or discovery resolver may use a successor candidate
   for routing. The succession fact remains immutable history; routing eligibility
   is a live, revocable policy resolution. Reuse the existing Capability Registry /
   `capability-authorization-policy.v1` sidecar path rather than introducing a
   succession-specific allow-set.

Post-MVP hosted-client lifecycle decision:

1. `client-instance-recovery.v1` admission requires a local detachment read-model
   proof that `recovery/from-detachment-id` is known to the serving node, belongs
   to the same `client-instance/id`, and was authorized by the same participant
   that is attempting recovery. Without that local lifecycle read model, recovery
   must fail closed rather than treating the bare detachment reference as
   authority.
2. The local lifecycle read model is a bounded cache of admitted detachment facts,
   not a new source of authority. Replayed detachments are idempotent and do not
   overwrite the first admitted record for a `detachment/id`; evicted detachments
   become unknown, so dependent recovery fails closed.

Test hardening backlog:

1. Add a daemon-level WSS/local-control acceptance test for
   `client-instance-detachment.v1` followed by `client-instance-recovery.v1`
   once the test harness has a stable way to bind participant lifecycle payloads
   to the live peer-session id. The hard admission rule is currently covered in
   `peer-runtime`; the remaining gap is end-to-end daemon wiring coverage.

Runtime gate tracker:

1. Before node succession affects peer-governor, discovery, dialer, or routing
   selection, implement the live gate:
   `accept-node-succession:*` resolves through Capability Registry plus the
   local `capability-authorization-policy.v1` sidecar. Until that gate exists,
   accepted succession facts may remain audit and operator state, but MUST NOT
   change routing eligibility.

## Next Actions

1. Keep `NodeIdentity`, `NodeAdvertisement`, `PeerHandshake`, and
   `CapabilityAdvertisement` aligned as one versioned networking family.
2. Keep Solution 000, Requirements 006, `node/docs/MVP.md`, and the Node
   implementation ledger synchronized when transport ownership or scope changes.
3. Track federated succession publication/replay, richer peer-governor policy,
   richer hosted-user policy/read-models, and additional transports as post-MVP
   extensions rather than as blockers for P014.
4. Keep the `accept-node-succession:*` Capability Registry gate ahead of any
   future successor-routing consumer; missing policy resolution must fail closed
   rather than honoring an accepted succession fact directly.
