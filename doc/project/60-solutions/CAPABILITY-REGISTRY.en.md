# Capability ID Registry

This document is the human-facing registry of capability IDs used across the
Node <-> Node and Node <-> Seed Directory trust and discovery surfaces.

It is not the full solution capability matrix. It is a narrower artifact that:

- maps each `capability_id` to its semantic meaning,
- shows the corresponding role or runtime class,
- records the wire-visible name,
- helps keep `orbidocs`, `node`, and passport contracts in sync.

## Scope

This registry covers capability IDs used as:

- identifiers in `capability-passport.v1`,
- identifiers in `capability-advertisement.v1`,
- routing or discovery predicates in the Node runtime.

Historically it excluded host-local capabilities such as `recovery.sign` or
`catalog.local.query`. That boundary is now superseded: `node/capability/capability-registry.v1.json`
is the enforced machine source of truth for both federated and host-local capabilities,
and this document is its mechanically checked human-facing projection. The curated
semantic table covers entries selected by `docs.human-registry`; the generated
[complete host-local catalogue](#host-local-capabilities) covers all host capabilities.

## Assertion Layers

Capability advertising and capability passports are related, but not
interchangeable.

Use the following layers:

| Layer | Artifact | Meaning | Trust basis | Examples |
|---|---|---|---|---|
| Protocol-native capability | `capability-advertisement.v1` with a self-issued passport-form assertion | "this peer currently speaks this baseline protocol surface" | node signature, self-issued capability passport, and successful peer session | `core/messaging`, `core/keepalive` |
| Passport-backed capability | `capability-passport.v1` carried in advertisement or indexed by Seed Directory | "this node is authorized or accepted for this capability profile" | profile-specific passport policy, issuer signature, revocation checks | `network-ledger`, `seed-directory`, `escrow` |
| Federation-recommended service | passport-backed capability plus federation policy | "this passport-backed capability is recommended or safe under this federation's policy" | high-assurance issuer, federation allowlist, local policy | approved ledger, trusted seed directory, certified offer catalog |
| Sovereign/private capability | sovereign capability id, optionally passport-backed | "this node offers an identity-anchored capability outside the global bare-name namespace" | anchor identity plus optional passport and local policy | `audio-transcription@participant:did:key:...`, `~audio-transcription@participant:did:key:...` |
| Self-announced custom capability | `capability-advertisement.v1` with a self-issued passport-form assertion | "this node says it can do this; verify by protocol use or local policy" | node signature plus self-issued passport; no federation endorsement unless separately attached | experimental plugin, non-critical discovery hint |

Therefore:

- `capability-advertisement.v1` is the live discovery and routing view and may
  be exchanged directly without Seed Directory,
- `capability-passport.v1` is the durable authority, consent, or endorsement
  proof for capability profiles that require one,
- `capability-schema.v1` is the optional machine-readable contract for a
  capability profile and is referenced by content-addressed `schema/ref`,
- the Seed Directory indexes passport-backed capabilities for network discovery,
- and consumers must apply local policy before treating any advertised
  capability as trusted.

## Public Passport Classes

The registry distinguishes public network publication from closed deployment
catalogs.

For publicly broadcast capability passports:

| Class | Passport `capability_id` | Wire/query projection | Issuer expectation |
|---|---|---|---|
| Official / community-recognized | registered formal bare id, e.g. `network-ledger`, `seed-directory`, `offer-catalog` | stable mapped name such as `core/network-ledger`, `role/seed-directory`, `role/offer-catalog` | participant, organization, council, or federation key at the highest assurance required by the community policy |
| Compatible sovereign implementation | sovereign id without `~`, e.g. `offer-catalog@participant:did:key:...`, plus `capability_profile.compatible_with` | `sovereign/...` plus anchor-aware filtering | the anchoring identity or delegated signer; consumers verify the compatibility claim against schema/profile evidence and local policy |
| Custom / operator-authored | sovereign id with `~`, e.g. `~article-review@participant:did:key:...` or `~article-review@org:did:key:...` | `sovereign/...` plus anchor-aware filtering | the anchoring identity or delegated signer; consumers apply local endorsement and reputation policy; `schema/ref` describes the custom protocol |

A public custom service MUST NOT mint a new unanchored bare formal
`capability_id` and publish it as if it were a community-recognized capability.
It should either use an existing registered formal id or use a sovereign
identity-anchored id.

Closed operator-owned deployments are different. They may use a local Seed
Directory as a deployment catalog for a known set of formal capabilities, with
trust coming from explicit configuration, allowlisted node ids, and established
peer sessions rather than public federation endorsement. Story-009 uses this
closed-deployment rule for the `offer-catalog` passports on node B/C.

## Sources of Truth

The source of truth is:

- `node:capability/capability-registry.v1.json`

This document, the legacy Rust projection in `node:capability/src/lib.rs`, and the
passport/advertisement fixtures are checked against that source by
`orbidocs:scripts/check-capability-registry.py`.

If any of the following changes:

- `capability_id`,
- wire name,
- capability semantics,
- eligibility flags,
- or the primary runtime owner,

then update the machine registry first and let the human projection follow it.

## Capability Registry

The `Passport in MVP` column is an implementation/readiness note, not the
machine registry status. Canonical machine status is `active`, `deprecated`, or
`reserved` in `node:capability/capability-registry.v1.json`; `reserved` entries
are visible here only to prevent namespace squatting and remain denied at
admission.

| capability_id | Wire name | Class | Semantic role | Typical runtime owner | Passport in MVP | Notes |
|---|---|---|---|---|---|---|
| `core/messaging` | `core/messaging` | protocol-native infrastructure | baseline encrypted peer messaging/session capability required for peer sessions | Node protocol / peer supervisor | self-issued advertisement/passport-form assertion | Mandatory baseline capability; peers lacking it are rejected by handshake/session validation. |
| `core/discovery` | `core/discovery` | protocol-native infrastructure | baseline peer discovery and advertisement exchange surface | Node protocol / discovery runtime | self-issued advertisement/passport-form assertion | Used for discovery and advertisement semantics; formal registry row keeps code constants and docs aligned. |
| `core/keepalive` | `core/keepalive` | protocol-native infrastructure | baseline keepalive/reconnect liveness surface | Node protocol / peer supervisor | self-issued advertisement/passport-form assertion | Protocol-native capability; not an attached service role. |
| `network-ledger` | `core/network-ledger` | infrastructure | remote settlement-ledger authority for other nodes | settlement-capable Node | yes | This capability means ledger authority, not merely one hold or one policy. |
| `seed-directory` | `role/seed-directory` | infrastructure | catalog of capability passports, revocations, and advertisements used for bootstrap and discovery | Seed Directory service or embedded Node service | yes | This capability covers trusted catalog publication and lookup semantics. |
| `node-primary-operator` | `role/node-primary-operator` | binding / governance | participant-issued authority binding naming the primary operator of a node | capability / Seed Directory / daemon acceptance path | yes | Binding-only capability; consumers must verify the node-operator binding artifact, not treat it as a generic service. |
| `offer-catalog` | `role/offer-catalog` | domain role | federated offer surface used for responder-side fetch and discovery | Dator on the supply side, Arca on the demand/discovery side | yes, when delegated by passport | The capability is domain-level; implementations may split supply and observed/discovery concerns across modules. |
| `corpus.provider` | `app/corpus-provider` | application reasoning role | topic-scoped Corpus reasoning provider eligible to receive `corpus-reasoning-query.v1` and return `corpus-reasoning-bid.v1` | Corpus provider AD acceptor / Corpus-capable service offer | hard-MVP done | The capability authorizes the operational provider role; topic expertise remains in `service-offer.v1` Corpus extension fields, never in the capability id. |
| `contact-catalog` | `role/contact-catalog` | domain role | opt-in contact discovery surface returning route candidates or invitation-required results for external contact handles | Contact Catalog middleware | yes | Seed Directory may advertise Contact Catalog providers, but it must not store raw people-directory mappings. MVP lookup is invitation-only with authenticated callers. |
| `email-attestation` | `role/email-attestation` | contact-control service role | service that challenges an email channel and orchestrates issuance of `email-control@v1` passports | attestation service discovered through Seed Directory | yes | This capability authorizes an attestation provider role, not control of a specific email address. |
| `phone-attestation` | `role/phone-attestation` | contact-control service role | service that challenges a phone channel and orchestrates issuance of `phone-control@v1` passports | attestation service discovered through Seed Directory | yes | This capability authorizes an attestation provider role, not control of a specific phone number. |
| `email-control` | `proof/email-control` | contact-control proof | proof that a subject currently controls one email address for selected purposes | attestation service discovered through Seed Directory | yes | This is contact-control evidence, not legal identity assurance. Contact Catalog admission treats it as freshness-bound input evidence. |
| `phone-control` | `proof/phone-control` | contact-control proof | proof that a subject currently controls one phone number for selected purposes | attestation service discovered through Seed Directory | yes | This is contact-control evidence, not legal identity assurance. Short TTLs and reassignment-aware policy are expected. |
| `agora-vault` | `app/agora-vault` | encrypted artifact storage | scoped authority to put, list, get, or delete opaque encrypted artifacts under an Agora Vault subject | Agora service / daemon host capability bridge | yes | Uses the `agora-vault@v1` profile. Public lookup is by opaque `artifact/id` only; vault subjects, participants, nyms, topics, and plaintext metadata stay outside the public entry. |
| `messaging.accept` | `app/messaging.accept` | application advertisement | node advertisement that this node currently accepts messaging delivery using the canonical `messaging-receive@v1` receive-consent profile | messaging middleware / Node capability advertisement | self-issued advertisement plus receive-profile evidence | Published only when the messaging service and inbound acceptor are ready. Route policy defaults to `privacy = private-direct` and lookup consumers may filter for this capability before sending contact requests. |
| `messaging-receive` | `app/messaging-receive` | application consent | narrow recipient-issued authority allowing one sender subject to deliver messages to one accepted route | messaging middleware / Contact Catalog contact-request acceptor | yes | Used by Story 010 as the concrete passport minted after accepting a contact request. It does not grant friend-class capabilities. |
| `messaging-send` | `app/messaging-send` | application authorship | participant-side authority to sign and enqueue outbound messaging envelopes for a local messaging client | messaging middleware / Node signing host | yes | Signing delegation uses `signing/messaging-send`; receive consent remains a separate `messaging-receive` passport. |
| `room.open` | `app/room.open` | application coordination | authority to open a durable Room skeleton and initial room policy projection | Room primitive / daemon room host | planned | This is a room-domain capability, not a transport adapter grant. WSS and Matrix live-plane adapters consume the resulting room projection. |
| `room.join` | `app/room.join` | application coordination | authority to request or accept membership in an existing Room under its policy | Room primitive / daemon room host | planned | Join authority is evaluated against room policy, grants, expiry, and attested membership; it does not imply live-message send authority by itself. |
| `room.membership-query` | `app/room.membership-query` | application query | authority to request signer-backed Room membership or grant attestations | Room primitive / daemon room host | yes | Implemented as authenticated `agora-service` projection queries backed by the local host signer; middleware does not mint attestations directly. |
| `sensorium.workbench.terminal` | `sensorium/workbench.terminal` | local actuation | bounded PTY/session capability for Sensorium Workbench | Sensorium Workbench connector | partial | Solution owner: Solution 042 Sensorium Workbench. High-risk effect surface; terminal remains disabled by factory config, then allows bounded PTY sessions and structured argv only after explicit grants and exact or bounded-prefix command profiles validated through the Rust actuation bridge. Raw input, resize, signal, and cancel are operator-confirmed paths. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `sensorium.workbench.file` | `sensorium/workbench.file` | local actuation | bounded file snapshot/read surface under leased workspace roots | Sensorium Workbench connector | partial | Solution owner: Solution 042 Sensorium Workbench. The connector implements allowlisted host-local and managed-copy snapshot/read with capped request/read bytes, Rust path admission, and traversal, root-self, symlink, oversized-file, and invalid-root refusal; it is not ambient filesystem authority. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `sensorium.workbench.patch` | `sensorium/workbench.patch` | local actuation | bounded patch application surface under leased workspace roots | Sensorium Workbench connector | partial | Solution owner: Solution 042 Sensorium Workbench. The connector implements artifact-backed patch apply behind digest/size checks, workspace containment, explicit grants, and operator confirmation for host-local or managed-copy roots; verified artifacts can be handed off explicitly to Artifact Delivery and/or metadata-only Memarium provenance. The formal registry dispatch gate remains closed. |
| `sensorium.workbench.env` | `sensorium/workbench.env` | local actuation | bounded environment/sandbox lifecycle surface for Workbench sessions | Sensorium Workbench connector | partial | Solution owner: Solution 042 Sensorium Workbench. The connector reports host-local environments and implements bounded `fixture-copy.v1` allocation, artifact export, persisted lifecycle, and operator-confirmed teardown while refusing PTY without process isolation. Container and microVM backends remain future. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `sensorium.interface.read` | `sensorium/interface.read` | observation | bounded one-shot read of one explicitly granted Sensorium Interface | Sensorium Interfaces runtime | yes, `sensorium-interface@v1` | Solution 046 owns the implemented operation; every invocation remains scoped to an exact interface resource, remote node where applicable, classification ceiling, batch caps, current host policy, and revocation evidence. Generic support advertisement exposes no descriptor or grant. |
| `sensorium.interface.subscribe` | `sensorium/interface.subscribe` | observation | create, renew, consume, and close one bounded caller-bound interface lease | Sensorium Interfaces runtime | yes, `sensorium-interface@v1` | Subscription authority is separate from one-shot read authority and is implemented with exact interface, caller, lease, cursor, classification, batch, and current revocation constraints. |
| `sensorium.interface.remote-feed` | `sensorium/interface.remote-feed` | host coordination | initiate one bounded authenticated peer egress feed on behalf of a local caller | Sensorium Interfaces runtime | no; host-local only | This grant permits recipient-side peer egress but carries no source authority. Every remote operation still requires a separate current `sensorium.interface.subscribe` Passport scoped to the exact remote node and interface. |
| `sensorium.interface.invoke` | `sensorium/interface.invoke` | actuation | invoke an exact method on one explicitly granted actuation interface and coordinate its bounded shared or exclusive control | Sensorium Interfaces runtime | yes, `sensorium-interface-actuation@v1` | The implemented P083 foundation binds every effect to the authenticated caller, exact interface, method, classification, opaque source generation, grant and limits; exclusive effects additionally require the current lease, epoch, and caller sequence. Observation, Room membership, and carrier attachment confer no invoke authority. |
| `sensorium.interface.manage` | `sensorium/interface.manage` | host control | source-local observation and actuation publication, lifecycle, grant, revocation, inspection, metrics, and policy-driven preemption | Sensorium Interfaces runtime | no; host-local only | The implemented capability is non-advertisable and Passport-ineligible. Its authorization policy enumerates a closed action set, including `control.preempt`; authenticated caller binding, an active exact invoke grant for an operator lease, immutable management facts, and restart reconstruction remain mandatory. |
| `http.fetch.bounded` | `host/http.fetch.bounded` | host network effect | one bounded HTTP(S) fetch admitted for an exact middleware consumer, action, origin policy, and destination class | daemon bounded HTTP fetch host | no; host-local only | Implemented as a reusable daemon-owned primitive with P084 as its first consumer. It resolves and classifies every address, pins the selected connection, revalidates same-origin redirects, enforces intersected byte/time/concurrency limits, and returns only bounded bytes or an Artifact Delivery pointer. It is not a public proxy and grants no Sensorium observation or publication authority. |
| `inference.policy.evaluate` | `host/inference.policy.evaluate` | data-only assessment | bounded evaluation of explicit receiving policy against declared or realized evidence | inference provenance core through daemon | no; host-local only | Returns admit, warn or deny for exact subjects. Does not authenticate source assertions, install policy, dispatch inference or authorize effects. |
| `service.order.result.prepare` | `host/service.order.result.prepare` | data-only derivation | content-bound procurement result preparation from the unchanged source product | procurement core through daemon | no; host-local only | Preserves source boundary and time. Does not observe execution, authenticate source, persist a commit, deliver artifacts or settle payment. |
| `artifact.delivery.retain` | `host/artifact.delivery.retain` | host storage effect | retain one authenticated caller-owned, content-bound object in Artifact Delivery | daemon Artifact Delivery object store | no; host-local only | Implemented for P084 representation retention. The host verifies exact caller/owner, digest, size, classification, causal context, and digest-bound idempotency before storage, then returns an immutable ref and P081 receipt. It grants no read, delivery, publication, or recipient authority. |
| `interaction-broker.wait` | `host/interaction-broker.wait` | host coordination | host-owned bounded wait over registered observation sources | daemon interaction broker | no; host-local only | Implemented control-plane coordination with deadlines, idempotency, daemon-issued grant context, durable recovery/retention, and live built-in plus dynamic source providers. |
| `interaction-broker.watch` | `host/interaction-broker.watch` | host coordination | host-owned bounded watch/replay cursor over registered observation sources | daemon interaction broker | no; host-local only | Implemented bounded watch resources, stable provider cursors, grant-context admission, retention-backed replay, and live Workbench, Room, Artifact Delivery, approval, Memarium-query, and Sensorium Interface providers. |
| `interaction-broker.probe` | `host/interaction-broker.probe` | host coordination | host-owned active probe for progress, liveness, file state, or artifact presence | daemon interaction broker | no; host-local only | Implemented bounded probes and diagnostics across registered providers; effectful remediation remains with the owning connector or operator path. |
| `whisper.trace.publish` | `host/whisper.trace.publish` | local authoring | validates and publishes one bounded `whisper-trace.v1` assertion through the existing Agora or AD/INAC carrier | Whisper Intake trace authoring provider | yes | Host-local and non-passportable. Inline disclosure requires exact sender-host operator consent; the resulting signed `agora-record.v1` remains subject to disclosure, signing, and carrier admission policy. |
| `escrow` | `role/escrow` | attached supervisory role | supervisor of hold, release, refund, freeze, and dispute paths for settlement contracts | escrow supervisor node or attached service | yes | This capability governs the lifecycle of reserved funds for a contract, not full ledger authority. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification, or adjudication surface | future oracle service | planned | Machine status: `reserved`. At this stage it is a namespace reservation and extension direction rather than an admissible runtime capability or full hard-MVP runtime slice. |

<!-- BEGIN GENERATED HOST CAPABILITIES -->

<a id="host-local-capabilities"></a>

## Complete Host-local Catalogue

Generated from `node:capability/capability-registry.v1.json`; do not edit this block.
Regenerate both languages with `make capability-registry-docs`.
Includes every entry with the `host-local` surface, regardless of lifecycle status
or `docs.human-registry` (which selects only the curated table above).

Entries: **186** host-local / **218** total; **25** owner groups.

Grouped by the exact registry `owner`, then sorted by `capability/id`.
`dispatchable` and `host-route` are independent eligibility flags; the last column
lists the other flags set to `true` (omitted flags are `false`). Entries may also
have the `federated` surface, shown explicitly below.

Neither an entry nor `active` status guarantees an installed handler, a running
endpoint, or caller authorization. Runtime availability, grants, approvals and
domain policy remain separate checks. Wire names are not endpoint URLs.

### <code>Sensorium Interfaces runtime</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>sensorium.interface.invoke</code> | <code>sensorium/interface.invoke</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.interface.manage</code> | <code>sensorium/interface.manage</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.interface.read</code> | <code>sensorium/interface.read</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.interface.remote-feed</code> | <code>sensorium/interface.remote-feed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.interface.subscribe</code> | <code>sensorium/interface.subscribe</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>Sensorium Workbench connector</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>sensorium.workbench.env</code> | <code>sensorium/workbench.env</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.file</code> | <code>sensorium/workbench.file</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.patch</code> | <code>sensorium/workbench.patch</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | false | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>sensorium.workbench.terminal</code> | <code>sensorium/workbench.terminal</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>Whisper Intake trace authoring provider</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>whisper.trace.publish</code> | <code>host/whisper.trace.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>capability/passport domain</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>memarium.read</code> | <code>app/memarium.read</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |

### <code>daemon Agent host runtime</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>agent.assistant.draft.accept</code> | <code>host/agent.assistant.draft.accept</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.assistant.escalate</code> | <code>host/agent.assistant.escalate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.binding.create</code> | <code>host/agent.binding.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.controller.run</code> | <code>host/agent.controller.run</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.effect.dispatch</code> | <code>host/agent.effect.dispatch</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.effect.propose</code> | <code>host/agent.effect.propose</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.fork</code> | <code>host/agent.fork</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-flow.bind</code> | <code>host/agent.inference-flow.bind</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.admit</code> | <code>host/agent.inference-passage.admit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.commit</code> | <code>host/agent.inference-passage.commit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-passage.invoke</code> | <code>host/agent.inference-passage.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.inference-terminal.select</code> | <code>host/agent.inference-terminal.select</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.product.read</code> | <code>host/agent.product.read</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.resume</code> | <code>host/agent.resume</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.spawn</code> | <code>host/agent.spawn</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.status</code> | <code>host/agent.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.stop</code> | <code>host/agent.stop</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.suspend</code> | <code>host/agent.suspend</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agent.turn-order.resolve</code> | <code>host/agent.turn-order.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Artifact Delivery host capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>artifact.delivery.retain</code> | <code>host/artifact.delivery.retain</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Corpus Agent effect bridge</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>corpus.room.turn</code> | <code>host/corpus.room.turn</code> | <code>active</code> | <code>host-local</code> | true | false | — |

### <code>daemon Corpus Agent moderation effect bridge</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>corpus.room.moderate</code> | <code>host/corpus.room.moderate</code> | <code>active</code> | <code>host-local</code> | true | false | — |

### <code>daemon Inquirium host runtime</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>inquirium.assistant.feedback.append</code> | <code>host/inquirium.assistant.feedback.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.export</code> | <code>host/inquirium.assistant.transcript.export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.import</code> | <code>host/inquirium.assistant.transcript.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.rebuild</code> | <code>host/inquirium.assistant.transcript.rebuild</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.search</code> | <code>host/inquirium.assistant.transcript.search</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.context-grant.issue</code> | <code>host/inquirium.context-grant.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.context-grant.revoke</code> | <code>host/inquirium.context-grant.revoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.operator-question.transition</code> | <code>host/inquirium.operator-question.transition</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.training-grant.issue</code> | <code>host/inquirium.training-grant.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.training-grant.revoke</code> | <code>host/inquirium.training-grant.revoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon Sensorium Virt host broker</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>sensorium.virt.host</code> | <code>host/sensorium.virt.host</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon bounded HTTP fetch host</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>http.fetch.bounded</code> | <code>host/http.fetch.bounded</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon capability host capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>capability.passport.publish</code> | <code>host/capability.passport.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.revocation.sign</code> | <code>host/capability.passport.revocation.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.revocation.verify</code> | <code>host/capability.passport.revocation.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.verify</code> | <code>host/capability.passport.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon capability passport publication reconciler</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>capability.passport.reconcile</code> | <code>host/capability.passport.reconcile</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon gateway control</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>gateway.sovereign-manual-receipt</code> | <code>host/gateway.sovereign-manual-receipt</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon host capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>memarium.promote</code> | <code>host/memarium.promote</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon identity host capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>identity.nym.create</code> | <code>host/identity.nym.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.org.create</code> | <code>host/identity.org.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.create</code> | <code>host/identity.participant.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.import</code> | <code>host/identity.participant.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-bundle-export</code> | <code>host/identity.participant.recovery-bundle-export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-bundle-import</code> | <code>host/identity.participant.recovery-bundle-import</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.participant.recovery-export</code> | <code>host/identity.participant.recovery-export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.pseudonym-vault.export</code> | <code>host/identity.pseudonym-vault.export</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.pseudonym-vault.import</code> | <code>host/identity.pseudonym-vault.import</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon interaction broker</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>interaction-broker.probe</code> | <code>host/interaction-broker.probe</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>interaction-broker.wait</code> | <code>host/interaction-broker.wait</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>interaction-broker.watch</code> | <code>host/interaction-broker.watch</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon operator settlement control</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>ledger.operator-credit</code> | <code>host/ledger.operator-credit</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>daemon operator-extension lifecycle host</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>operator.extension.inspect</code> | <code>host/operator.extension.inspect</code> | <code>active</code> | <code>host-local</code> | false | true | — |
| <code>operator.extension.lifecycle</code> | <code>host/operator.extension.lifecycle</code> | <code>active</code> | <code>host-local</code> | false | true | — |
| <code>operator.extension.safe-mode</code> | <code>host/operator.extension.safe-mode</code> | <code>active</code> | <code>host-local</code> | false | true | — |

### <code>daemon or supervised middleware host capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>agora.publish.authorize</code> | <code>host/agora.publish.authorize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.admit</code> | <code>host/agora.record.admit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.sign</code> | <code>host/agora.record.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.record.verify</code> | <code>host/agora.record.verify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.relay</code> | <code>host/agora.relay</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>advertisable</code>, <code>passport/eligible</code>, <code>federated-discovery</code> |
| <code>agora.subscribe.authorize</code> | <code>host/agora.subscribe.authorize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.trace.append</code> | <code>host/agora.trace.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>agora.vault.delete</code> | <code>host/agora.vault.delete</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.get</code> | <code>host/agora.vault.get</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.list</code> | <code>host/agora.vault.list</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>agora.vault.put</code> | <code>host/agora.vault.put</code> | <code>active</code> | <code>federated</code>, <code>host-local</code> | true | true | <code>passport/eligible</code> |
| <code>artifact.delivery.send</code> | <code>host/artifact.delivery.send</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>artifact.delivery.status</code> | <code>host/artifact.delivery.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>artifact.delivery.submit</code> | <code>host/artifact.delivery.submit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.issue</code> | <code>host/capability.passport.issue</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.lookup</code> | <code>host/capability.passport.lookup</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.passport.sign</code> | <code>host/capability.passport.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>capability.revocation.snapshot</code> | <code>host/capability.revocation.snapshot</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>contact.lookup</code> | <code>host/contact.lookup</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.messaging-recovery.mirror</code> | <code>host/identity.messaging-recovery.mirror</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.recovery</code> | <code>host/identity.recovery</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>identity.routing-subject.create</code> | <code>host/identity.routing-subject.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.offer</code> | <code>host/inac.offer</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.push</code> | <code>host/inac.push</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inac.request</code> | <code>host/inac.request</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.activity.feed</code> | <code>host/inquirium.assistant.activity.feed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.transcript.excise</code> | <code>host/inquirium.assistant.transcript.excise</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.assistant.turn</code> | <code>host/inquirium.assistant.turn</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.classify</code> | <code>host/inquirium.classify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.embed</code> | <code>host/inquirium.embed</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.generate</code> | <code>host/inquirium.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.image.edit</code> | <code>host/inquirium.image.edit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.image.generate</code> | <code>host/inquirium.image.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.rerank</code> | <code>host/inquirium.rerank</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.summarize</code> | <code>host/inquirium.summarize</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.transform</code> | <code>host/inquirium.transform</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-recipient-mailbox.resolve</code> | <code>host/local-recipient-mailbox.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.group.resolve</code> | <code>host/local-relationship.group.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.membership.append</code> | <code>host/local-relationship.membership.append</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.membership.latest</code> | <code>host/local-relationship.membership.latest</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>local-relationship.predicate.evaluate</code> | <code>host/local-relationship.predicate.evaluate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.cache</code> | <code>host/memarium.cache</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.crisis.resolve</code> | <code>host/memarium.crisis.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.crisis.status</code> | <code>host/memarium.crisis.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.declassify</code> | <code>host/memarium.declassify</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.forget</code> | <code>host/memarium.forget</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.index</code> | <code>host/memarium.index</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>memarium.write</code> | <code>host/memarium.write</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.rewrite.broadcast</code> | <code>host/middleware.rewrite.broadcast</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.rewrite.peer-message</code> | <code>host/middleware.rewrite.peer-message</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.snooper.observe</code> | <code>host/middleware.snooper.observe</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>middleware.snooper.test</code> | <code>host/middleware.snooper.test</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>notification.create</code> | <code>host/notification.create</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>offer-catalog.query</code> | <code>host/offer-catalog.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>offers.local.query</code> | <code>host/offers.local.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>peer.message.dispatch</code> | <code>host/peer.message.dispatch</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>peer.session.establish</code> | <code>host/peer.session.establish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.hsm.store</code> | <code>host/recovery.hsm.store</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.hsm.unseal</code> | <code>host/recovery.hsm.unseal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>recovery.sign</code> | <code>host/recovery.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.derive-aead-key</code> | <code>host/sealer.derive-aead-key</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.master.init</code> | <code>host/sealer.master.init</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.open</code> | <code>host/sealer.open</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.seal</code> | <code>host/sealer.seal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sealer.unlock</code> | <code>host/sealer.unlock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>seed.directory.query</code> | <code>host/seed.directory.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.audit.read</code> | <code>host/sensorium.audit.read</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.invoke</code> | <code>host/sensorium.connector.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.operation.cancel</code> | <code>host/sensorium.connector.operation.cancel</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.operation.status</code> | <code>host/sensorium.connector.operation.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.connector.os.action</code> | <code>host/sensorium.connector.os.action</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.directive.invoke</code> | <code>host/sensorium.directive.invoke</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.directive.list</code> | <code>host/sensorium.directive.list</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.health</code> | <code>host/sensorium.health</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observation.get</code> | <code>host/sensorium.observation.get</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observe.query</code> | <code>host/sensorium.observe.query</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.observe.submit</code> | <code>host/sensorium.observe.submit</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.operation.cancel</code> | <code>host/sensorium.operation.cancel</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.operation.status</code> | <code>host/sensorium.operation.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.os.catalog.reload</code> | <code>host/sensorium.os.catalog.reload</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.os.catalog.status</code> | <code>host/sensorium.os.catalog.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>sensorium.topic.summary</code> | <code>host/sensorium.topic.summary</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.derive-shared-secret</code> | <code>host/signer.derive-shared-secret</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.lock</code> | <code>host/signer.lock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.sign</code> | <code>host/signer.sign</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.status</code> | <code>host/signer.status</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>signer.unlock</code> | <code>host/signer.unlock</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>whisper.intake</code> | <code>host/whisper.intake</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>whisper.redaction.prepare</code> | <code>host/whisper.redaction.prepare</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.orchestrate</code> | <code>host/workflow.orchestrate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.step.completed.publish</code> | <code>host/workflow.step.completed.publish</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>workflow.test.trigger</code> | <code>host/workflow.test.trigger</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>inference-provenance-core through daemon host boundary</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>inference.policy.evaluate</code> | <code>host/inference.policy.evaluate</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>procurement core through daemon host boundary</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>service.order.result.prepare</code> | <code>host/service.order.result.prepare</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised JSON-e Flow acceptance capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>role.agent.inference-passage.acceptance</code> | <code>host/role.agent.inference-passage.acceptance</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised middleware Corpus turn-order flow</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>role.corpus.turn-order.resolve</code> | <code>host/role.corpus.turn-order.resolve</code> | <code>active</code> | <code>host-local</code> | true | true | — |

### <code>supervised middleware or test fixture capability</code>

| capability_id | Wire name | Status | Surfaces | `dispatchable` | `host-route` | Other enabled flags |
|---|---|---|---|---|---|---|
| <code>base.rumor-rewrite</code> | <code>host/base.rumor-rewrite</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>base.whisper-redaction</code> | <code>host/base.whisper-redaction</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.anthropic</code> | <code>host/inquirium.adapter.anthropic</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.openai</code> | <code>host/inquirium.adapter.openai</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>inquirium.adapter.simulator</code> | <code>host/inquirium.adapter.simulator</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.minimal</code> | <code>host/other.minimal</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.operator-hinting</code> | <code>host/other.operator-hinting</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>other.test</code> | <code>host/other.test</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-editor-in-chief.execute</code> | <code>host/role.bielik-editor-in-chief.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-git-publisher.execute</code> | <code>host/role.bielik-git-publisher.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-illustrator.execute</code> | <code>host/role.bielik-illustrator.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-publication-verifier.execute</code> | <code>host/role.bielik-publication-verifier.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.bielik-researcher.execute</code> | <code>host/role.bielik-researcher.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.example-summarizer.execute</code> | <code>host/role.example-summarizer.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.example.execute</code> | <code>host/role.example.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.inquirium.generate</code> | <code>host/role.inquirium.generate</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw-signal.execute</code> | <code>host/role.raw-signal.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component2</code> | <code>host/role.raw.component2</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component3</code> | <code>host/role.raw.component3</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.raw.component4</code> | <code>host/role.raw.component4</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.test.execute</code> | <code>host/role.test.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |
| <code>role.test.success.execute</code> | <code>host/role.test.success.execute</code> | <code>active</code> | <code>host-local</code> | true | true | — |

<!-- END GENERATED HOST CAPABILITIES -->

## Semantic Distinctions

### `network-ledger` vs `escrow`

- `network-ledger` answers: "who is the ledger authority?"
- `escrow` answers: "who supervises the conditional release of funds for this contract?"

These roles may be co-located, but they are not semantically identical.

### `offer-catalog`

`offer-catalog` is a domain capability, not the name of one concrete process.
In the current MVP:

- Dator owns the supply side and responder-side fetch,
- Arca owns the demand side, observed catalog, and discovery.

The capability remains singular even if the runtime realizes it through more than
one module.

### `contact-catalog`

`contact-catalog` discovers opt-in contact routes, not people. A provider may
be discovered through Seed Directory, but the catalog's domain policy owns:

- admitted contact-control evidence,
- lookup indexes,
- route candidate disclosure,
- rate limits,
- no-match audit behavior,
- and revocation or expiry of contact claims.

The MVP profile is invitation-only. Consumers should expect
`contact-lookup-result.v1` to name a `routing-subject`, `contact_nym`, or
invitation path, never a raw root participant by default.

## Next Actions

- Extend this registry when new stable inter-node capability IDs appear.
- Add a more precise `issuer -> consumer -> scope` table once attached-role
  passports start carrying richer `scope` semantics than the current MVP.
