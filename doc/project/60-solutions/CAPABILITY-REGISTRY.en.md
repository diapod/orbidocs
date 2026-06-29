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
and this document is its human-facing, CI-validated projection.

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
| `sensorium.workbench.terminal` | `sensorium/workbench.terminal` | local actuation | bounded PTY/session capability for Sensorium Workbench | Sensorium Workbench connector | partial | High-risk effect surface; the current connector keeps terminal disabled by factory config, then allows bounded PTY sessions and structured argv commands only after explicit grants and configured command profiles. Raw input, resize, and signal are operator-confirmed paths. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `sensorium.workbench.file` | `sensorium/workbench.file` | local actuation | bounded file snapshot/read surface under leased workspace roots | Sensorium Workbench connector | partial | First opt-in connector slice implements allowlisted workspace snapshot/read with capped request/read bytes plus traversal, root-self, symlink-traversal, oversized-file, and invalid-root-config refusal; it is not ambient filesystem authority. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `sensorium.workbench.patch` | `sensorium/workbench.patch` | local actuation | bounded patch application surface under leased workspace roots | Sensorium Workbench connector | planned | Current connector exposes a fail-closed patch gate; execution still requires artifact-ref input, provenance, digest checks, policy gates, and operator approval unless an explicit lease permits it. This registry entry is visible and passport-eligible, but not dispatchable until a supervised patch handler is admitted. |
| `sensorium.workbench.env` | `sensorium/workbench.env` | local actuation | bounded environment/sandbox lifecycle surface for Workbench sessions | Sensorium Workbench connector | partial | First opt-in connector slice reports allowlisted host-local workspace environments; lifecycle create/close and cleanup/recovery are still future. Registry flags allow both host-route visibility and supervised middleware dispatch for this handler. |
| `interaction-broker.wait` | `host/interaction-broker.wait` | host coordination | host-owned bounded wait over registered observation sources | daemon interaction broker | planned | Waits are control-plane coordination with deadlines and idempotency; they do not authorize termination or domain effects. |
| `interaction-broker.watch` | `host/interaction-broker.watch` | host coordination | host-owned bounded watch/replay cursor over registered observation sources | daemon interaction broker | planned | Watch replay windows are bounded by count/time and carry metadata-safe events only. |
| `interaction-broker.probe` | `host/interaction-broker.probe` | host coordination | host-owned active probe for progress, liveness, file state, or artifact presence | daemon interaction broker | planned | Probes produce diagnostics or outcomes; effectful remediation remains with the owning connector/operator path. |
| `escrow` | `role/escrow` | attached supervisory role | supervisor of hold, release, refund, freeze, and dispute paths for settlement contracts | escrow supervisor node or attached service | yes | This capability governs the lifecycle of reserved funds for a contract, not full ledger authority. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification, or adjudication surface | future oracle service | planned | Machine status: `reserved`. At this stage it is a namespace reservation and extension direction rather than an admissible runtime capability or full hard-MVP runtime slice. |

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
