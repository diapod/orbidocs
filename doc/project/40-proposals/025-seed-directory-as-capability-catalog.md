# Proposal 025: Seed Directory as Capability Catalog

Based on:
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/20-memos/seed-directory-http-examples.md`
- `doc/schemas/capability-advertisement.v1.schema.json`
- `doc/schemas/node-advertisement.v1.schema.json`

## Status

Draft

## Date

2026-04-01

## Executive Summary

The Seed Directory defined in Proposal 014 is a signed cache for
`node-advertisement.v1` artifacts. It answers the question: given a
`node:did:key:...`, what are its current endpoints?

This proposal extends the Seed Directory to also answer: which Nodes currently
hold a given infrastructure capability, verified by a sovereign-signed passport?

The extension adds two complementary surfaces to the Seed Directory:

1. a **capability registration surface** — Nodes with sovereign-issued passports
   register per-capability, and the directory verifies each passport before
   storing it,
2. a **federated revocation surface** — sovereign operators publish revocations
   for artifacts whose validity may be relied on by other Nodes; consumers poll
   for them.

This revocation surface is not the universal home for every revocation in a
Node. Revocations that affect only local dispatch, local modules, local
operator UI, or local host capabilities remain node-local policy projections.
They may be represented by the same signed revocation artifact shape, but they
do not need Seed Directory publication unless another Node is expected to rely
on the artifact being revoked.

The Seed Directory itself is modeled as a capability (`seed-directory`), with
its own passports shipped in the software distribution. This closes the
bootstrap chain: to find Nodes with any capability, you first find the Seed
Directory via passports pinned in your local distribution.

## Context and Problem Statement

Proposal 024 introduced `capability-passport.v1` as the signed delegation
artifact for infrastructure capabilities and defined static-config discovery
for hard-MVP. Static config is sufficient for a single closed deployment, but
it scales poorly:

- each operator must manually maintain config for every capability node,
- there is no network-level query surface for "who currently runs capability X",
- revocation has no propagation channel.

The Seed Directory already solves the analogous problem for Node endpoints: it
is a shared, signed cache rather than a per-operator config problem. Extending
it to capabilities applies the same solution to the capability discovery problem.

A self-referential element is necessary for bootstrap: the Seed Directory itself
must be discoverable without prior knowledge of any running node. Modeling
`seed-directory` as a capability and shipping its passports with the distribution
solves this without introducing a separate hard-coded lookup mechanism.

## Goals

- Extend the Seed Directory with capability registration and query surfaces.
- Require a valid capability passport for every capability registration.
- Define the consumer verification flow: independent passport check, local cache,
  revocation polling.
- Define `seed-directory` as the self-referential capability whose passports are
  shipped in the software distribution.
- Establish the naming convention between `CapabilityAdvertisementV1` capability
  strings and capability passport `capability_id` values.
- Support multiple capabilities per Node, each with its own passport.
- Support sovereign capability ids plus sovereign-aware lookup filters without
  collapsing them into the global bare-name namespace.

## Non-Goals

- This proposal does not define gossip-based capability propagation.
- This proposal does not define capability marketplace or auction mechanisms.
- This proposal does not define per-capability wire protocols. Those are defined
  per capability (e.g. `network-ledger` wire protocol is out of scope here).
- This proposal does not define OpenAPI, ETag headers, or rate-limiting headers
  for the extended Seed Directory. Those may be added without a new proposal.
- This proposal does not define multi-federation capability directories.

## Decision

### 1. One Registration Per (Node, Capability) Pair

A Node with multiple capabilities registers each separately. One call to
`PUT /cap/{node-id}/{capability-id}` registers one capability entry backed by
one passport.

A Node with three capabilities makes three separate PUT requests. The Seed
Directory stores, verifies, and serves each entry independently. Per-entry
independence allows:

- different expiry per capability,
- independent revocation per capability,
- partial updates without re-registering all capabilities.

### 2. Registration Requires a Valid Passport

The `PUT /cap/{node-id}/{capability-id}` request body MUST carry:

- a signed `capability-advertisement.v1` artifact for the Node,
- a `capability-passport.v1` artifact for the specific `capability_id`.

The Seed Directory MUST verify before storing:

1. the passport `signature` — direct passports verify against the issuer
   participant public key recovered from `issuer/participant_id`; passports
   with `issuer_delegation` first verify that inline proof against the issuer
   participant, then verify the passport with `issuer_delegation.proxy_key`,
2. `issuer/participant_id` is recognized as a sovereign operator under the
   directory's own local sovereign key set,
3. `passport.node_id == {node-id}` in the URL path,
4. `passport.capability_id == {capability-id}` in the URL path,
5. `passport.expires_at` is either absent or in the future,
6. `passport_id` is not present in the directory's revocation log.

If any check fails, the directory MUST return `403 Forbidden` with a
machine-readable reason string. Self-reported capability advertisements without
a passport are accepted only for non-critical capabilities (see Section 7).

The directory stores the passport alongside the capability entry so that
consumers can retrieve it directly.

### 3. Extended HTTP Surface

The existing `/adv` surface is unchanged. The new capability surfaces are:

The Seed Directory does not rely on bearer-token authentication for capability
catalog operations. Discovery reads are open, and write authorization is derived
solely from signed artifacts:

- `PUT /cap` is accepted only when the embedded `capability-passport.v1`
  verifies and its sovereign issuer policy passes.
- `POST /revoke` is accepted only when the
  `capability-passport-revocation.v1` verifies under either the `issuer` or
  `subject` authority path.
- `GET /cap*` and `GET /revocations` are intentionally public discovery
  surfaces so Nodes can bootstrap without pre-shared HTTP credentials.

```
# Capability registration (one per node+capability pair)
PUT  /cap/{node-id}/{capability-id}
     Body: { "advertisement": capability-advertisement.v1,
             "passport":      capability-passport.v1 }
     → 201 Created | 200 OK (replace) | 403 Forbidden | 409 Conflict (stale)

# Query: all capabilities of one node
GET  /cap/{node-id}
     → { node_id, endpoints[], capabilities: [ { capability_id, passport,
                                                  published_at, expires_at } ] }
     → 404 if node not found

# Query: all nodes with a given capability
GET  /cap?capability={capability-id-or-wire-name}
        [&anchor={anchor-id}]
        [&include_formal=true|false]
        [&include_sovereign_formal=true|false]
        [&include_sovereign_informal=true|false]
        [&include_sovereign=true|false]
     → { items: [ { node_id, endpoints[], capability_id, passport,
                    published_at, expires_at, anchor_identity, informal } ],
          next, max-items }

# Revocation log
POST /revoke
     Body: capability-passport-revocation.v1
     → 200 OK | 403 Forbidden (bad revocation signature)

GET  /revocations?since={cursor}
     → { items: [ { passport_id, node_id, capability_id, revoked_at } ],
         next, max-items }

# Node address attestation
GET  /attest/node-address/{node-id}
     → node-address-attestation.v1
     → 503 if directory signing is missing, or if a configured active probe fails
```

`GET /cap?capability` joins capability entries with the `/adv` table to return
current endpoints alongside each passport. A Node missing a current advertisement
is returned without endpoints (`endpoints: []`) rather than being omitted; the
consumer may still use the passport for out-of-band contact.

Flag defaults:

- `include_formal = true`
- `include_sovereign_formal = true`
- `include_sovereign_informal = false`
- `include_sovereign` is a shortcut for both sovereign flags

This keeps old `GET /cap?capability=...` callers backward-compatible while
still suppressing informal sovereign capabilities unless the consumer asks for
them explicitly.

### 3a. Capability Query Predicate/Filter

Capability discovery consumers may need to ask for "Nodes with capability X
that also satisfy local trust policy Y" without first downloading an arbitrary
page of unrelated entries and filtering it locally.  The Seed Directory query
surface therefore accepts an optional predicate/filter object for capability
discovery. Callers should still keep local post-filtering as a compatibility and
defense-in-depth layer because older Seed Directory endpoints may ignore unknown
query parameters.

The first predicate set stays deliberately small and index-friendly:

- `node_id` / `node_ids` — restrict results to one or more known Nodes,
- `issuer` / `issuers` — restrict results to passports issued by
  a known participant or sovereign operator,
- `capability_id` — keep the primary capability selector explicit inside the
  predicate form when clients use a structured query body,
- `endorsement` — restrict results to entries carrying a recognized federation
  or policy endorsement,
- `passport_profile` — filter by projected passport profile markers. This starts
  as a shallow marker match and can become index-backed when profile projection
  stabilizes.

The predicate is a discovery optimization and policy expression, not an
authorization decision.  Consumers MUST still verify the served Node's passport
after connecting, and local policy MAY reject a result even if the Seed
Directory predicate matched it.

Until this contract is implemented, clients that apply local trust filters
SHOULD avoid passing a page-size `limit` to the Seed Directory before applying
their own filter.  They should filter the returned entries locally and then
apply their acceptance limit.  This prevents untrusted first-page entries from
starving trusted peers.

### 4. Consumer Verification Flow

A Node consuming a passport-backed service MUST:

1. Query the Seed Directory: `GET /cap?capability={capability-id}`.
2. Select a candidate Node from the response.
3. Connect to the candidate Node via the standard inter-node transport.
4. Request the capability passport directly from the serving Node via a
   post-handshake artifact exchange (`capability-passport-present.v1`).
5. Verify the passport independently:
   - valid Ed25519 signature; for delegated passports, first verify inline
     `issuer_delegation`, then verify the passport with the proof's `proxy_key`;
     for direct passports, verify with the issuer participant key,
   - `passport.node_id` matches the `node:did:key:...` of the peer session,
   - `passport.capability_id` matches the capability being consumed,
   - `expires_at` is absent or in the future.
6. Cache the passport locally with TTL equal to `expires_at` (or a configured
   maximum if `expires_at` is absent).
7. Reject the connection if any verification step fails.

Step 5 is the critical independence guarantee: the consumer does not trust the
Seed Directory's copy of the passport. It trusts only what the serving Node
presents and what the locally-pinned sovereign key can verify.

### 5. Revocation Artifact and Polling

Revocation is expressed as a `capability-passport-revocation.v1` artifact.
Two signing authorities are recognised, discriminated by the `signed_by` field:

**`signed_by: "issuer"`** — sovereign operator revocation. The same participant
who issued the original passport declares it void. Semantics: *"I withdraw the
delegation I granted."* The `issuer/participant_id` field is required and MUST
match the issuer of the original passport.

```json
{
  "schema":        "capability-passport-revocation.v1",
  "revocation_id": "passport-revocation:...",
  "passport_id":   "passport:capability:...",
  "node_id":       "node:did:key:...",
  "capability_id": "network-ledger",
  "revoked_at":    "2026-04-01T12:00:00Z",
  "signed_by":     "issuer",
  "reason":        "operator key rotation",
  "issuer/participant_id": "participant:did:key:...",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

**`signed_by: "subject"`** — self-revocation by the node. The node whose
capability is being revoked signs the revocation using its own node key (the
private key corresponding to `node_id`). Semantics: *"I no longer offer this
capability."* The `issuer/participant_id` field MUST NOT be present; the Seed
Directory recovers the signer public key from `node_id` directly.

```json
{
  "schema":        "capability-passport-revocation.v1",
  "revocation_id": "passport-revocation:...",
  "passport_id":   "passport:capability:...",
  "node_id":       "node:did:key:...",
  "capability_id": "network-ledger",
  "revoked_at":    "2026-04-01T12:00:00Z",
  "signed_by":     "subject",
  "reason":        "node decommissioned",
  "signature": { "alg": "ed25519", "value": "..." }
}
```

Self-revocation covers the common operational case where a node is being
decommissioned while the sovereign operator is offline. It is not a security
escalation: a node can only withdraw its own passport, never grant capabilities.
The worst-case effect of a compromised node key performing self-revocation is
availability loss, not privilege escalation.

The Seed Directory verifies the revocation signature before storing:

- `signed_by == "issuer"`: verify Ed25519 against `issuer/participant_id` public
  key, check that issuer is sovereign under the directory's policy, check that
  `issuer/participant_id` matches the original passport's issuer.
- `signed_by == "subject"`: verify Ed25519 against the public key derived from
  `node_id`, check that `node_id` matches the original passport's `node_id`. No
  sovereignty check required.

The revocation log is append-only. Both `signed_by` values and the signer
reference are stored for audit.

Consumers MUST poll `GET /revocations?since={cursor}` at an interval no greater
than half the minimum expected passport TTL for capabilities they are actively
consuming. On finding a revocation entry for a cached passport, the consumer
MUST immediately invalidate its local cache and re-verify before continuing
operations.

This polling requirement applies to consumers of Seed Directory-published,
federated capability or delegation artifacts. A Node may also maintain a
separate local `RevocationView` for node-local dispatch decisions; that local
view may include revocations that were never published to the Seed Directory.

Nodes SHOULD also proactively re-verify passports for long-running sessions when
they detect that a cached passport is approaching expiry.

### 6. `seed-directory` as a Self-Referential Capability

The Seed Directory is itself modeled as a capability to unify the bootstrap
chain. A Node acting as a Seed Directory holds a `capability-passport.v1` with
`capability_id = "seed-directory"`.

These passports are shipped with the software distribution, equivalent to TLS
root trust anchors:

```toml
# Shipped in the default node configuration

[[network.seed_directory]]
node_id  = "node:did:key:z6Mk..."
endpoint = "https://seed-01.orbiplex.example"
passport = """{ ... capability-passport.v1 for seed-directory ... }"""

[[network.seed_directory]]
node_id  = "node:did:key:z6Mk..."
endpoint = "https://seed-02.orbiplex.example"
passport = """{ ... }"""
```

At daemon startup, each seed directory passport MUST be verified:

1. signature valid,
2. issuer sovereign under local policy,
3. `capability_id == "seed-directory"`,
4. `node_id` matches the configured endpoint's Node.

A seed directory entry whose passport fails verification MUST be skipped with
a logged warning. If no valid seed directory entry remains, the Node starts in
isolated mode and logs a startup warning.

The Seed Directory does not register itself in its own catalog. Its endpoints
are known from the shipped passports only.

### 7. Capability Naming Convention

Capability naming now has three related layers:

| Context | Pattern | Example |
| :--- | :--- | :--- |
| Formal wire capability name | `core/...`, `role/...`, `plugin/...`, or bare formal name | `role/seed-directory` |
| Sovereign wire capability name | `sovereign/...` or `sovereign-informal/...` | `sovereign/audio-transcription` |
| Capability passport `capability_id` | formal bare id or sovereign id with anchor | `seed-directory`, `audio-transcription@participant:did:key:z...` |

Formal mappings stay stable:

```
role/seed-directory   →  seed-directory
core/network-ledger   →  network-ledger
role/escrow           →  escrow
plugin/oracle-basic   →  oracle-basic
```

Unknown formal capabilities may also appear as bare formal wire names and map
to themselves.

Sovereign capabilities intentionally do not have a pure-name reverse mapping.
Instead:

```
sovereign/audio-transcription + anchor_identities["audio-transcription"]
  → audio-transcription@participant:did:key:z...
```

Informal sovereign capabilities use the same anchor rule but carry the
`sovereign-informal/` wire prefix and the leading `~` in the reconstructed
passport capability id.

### 8. Directory-Indexed vs. Node-Presented Capabilities

Capability advertisements are no longer raw self-reported strings. They are
Node-signed presentations of passport-form capability assertions.

The Seed Directory still distinguishes two discovery paths:

| Path | Seed Directory publication | Examples |
| :--- | :--- | :--- |
| Directory-indexed (`PUT /cap`) | Yes, accepted only after directory policy verifies the passport | `seed-directory`, `network-ledger`, `escrow`, `oracle` |
| Node-presented (`capability-advertisement.v1`) | No directory required; the peer evaluates the presented passport under local policy | `core/messaging`, `core/discovery`, custom sovereign capability |

`capability-advertisement.v1` may be sent directly after handshake, returned in
response to a capability query, or broadcast where the transport profile admits
datagram-style publication. It carries the presented capability assertions and
the credentials needed for local verification.

`GET /cap?capability=` remains the passport-backed directory lookup surface. It
returns capabilities that the Seed Directory has accepted for indexing. A peer
MAY still accept a directly presented capability that is absent from the Seed
Directory if local policy allows that assertion kind and passport profile.

This separation prevents conflation of directory availability with capability
truth. The directory helps peers find and cache capabilities; it is not the only
way a Node may communicate a signed capability assertion.

Operator-binding availability uses the same passport-backed availability pattern
but adds one extra rule. A `node-primary-operator` passport is only the
participant-side consent half of a `node-operator-binding.v1` bundle. A Seed
Directory MUST NOT accept or serve it as an operator binding unless the payload
also carries the Node's signed acceptance, or an equivalent
`node-operator-binding.v1` bundle, proving that the target Node accepted that
participant as its primary operator. Publishing such a bundle is an explicit
privacy/disclosure decision by the Node, not a default capability-gossip step.

## Artifact Shapes

### `capability-passport.v1` (normative reference to Proposal 024)

Full field list in `doc/schemas/capability-passport.v1.schema.json`.

Capability passports may carry optional `capability_profile` metadata:

```json
{
  "capability_profile": {
    "display/name": "Audio transcription",
    "description": "Transcribes audio input into timestamped text segments.",
    "lang": "en",
    "doc/ref": "orbiplex:blob:sha256:...",
    "doc/url": "https://example.org/capabilities/audio-transcription",
    "schema/id": "urn:orbiplex:capability-profile:audio-transcription:v1",
    "schema/ref": "orbiplex:blob:sha256:...",
    "schema/media-type": "application/schema+json"
  }
}
```

These fields help humans and programs understand the capability profile, but do
not create trust by themselves. The passport signature, issuer policy,
revocation state, and receiver-local policy remain authoritative.

`doc/url` is only a convenience mirror. Runtime behavior MUST NOT depend on
dereferencing it.

### `capability-schema.v1`

Full field list in `doc/schemas/capability-schema.v1.schema.json`.

`capability-schema.v1` is the portable machine-readable description of a
capability profile. It may describe:

- accepted `scope` fields,
- request input shape,
- response output shape,
- error classes,
- retry and idempotency semantics,
- artifact or resource references used by that capability.

The artifact uses:

- `schema/id` as the stable logical contract name,
- `schema/ref` as the content-addressed Orbiplex reference,
- `schema/media-type` to identify the schema language,
- `content` for the actual machine-readable schema,
- a signature for portable provenance when the artifact is cached or relayed.

Nodes may expose schema artifacts through the peer-message kind
`capability.schema.present.request` / `capability.schema.present.response`.
Seed Directory may index or cache them later, but it is not the mandatory
runtime transport for schema retrieval.

The response payload for that peer-message exchange is
`capability-schema-present.v1`, a thin wrapper carrying either:

- `status = "ok"` plus `artifact = { ... capability-schema.v1 ... }`,
- or `status = "error"` plus an error object.

### `capability-passport-revocation.v1`

Full field list in `doc/schemas/capability-passport-revocation.v1.schema.json`.

Fields always required:

- `schema` = `"capability-passport-revocation.v1"`
- `revocation_id` with prefix `"passport-revocation:"`
- `passport_id` — the passport being revoked
- `node_id` — the Node whose capability is revoked
- `capability_id` — the capability being revoked
- `revoked_at` — RFC 3339
- `signed_by` — `"issuer"` or `"subject"` (see Section 5)
- `signature` — Ed25519 over canonical JSON without `signature` field

Conditional fields:

- `issuer/participant_id` — required when `signed_by == "issuer"`, MUST match
  the issuer of the original passport; MUST NOT be present when
  `signed_by == "subject"`
- `reason` — optional human-readable note (both paths)

### Seed Directory Registration Request

```json
{
  "advertisement": { /* capability-advertisement.v1 */ },
  "passport":      { /* capability-passport.v1 */ }
}
```

### `GET /cap?capability=network-ledger` Response

```json
{
  "items": [
    {
      "node_id": "node:did:key:z6MkLedger",
      "endpoints": [
        { "endpoint/url": "wss://ledger.example/peer",
          "endpoint/transport": "wss",
          "endpoint/role": "listener",
          "endpoint/priority": 0 }
      ],
      "capability_id": "network-ledger",
      "passport": { /* capability-passport.v1 */ },
      "published_at": "2026-04-01T10:00:00Z",
      "expires_at":   "2027-04-01T10:00:00Z",
      "anchor_identity": null,
      "informal": false
    }
  ],
  "next": "cur:01JQCAPCUR002",
  "max-items": 100
}
```

### `GET /cap?capability=audio-transcription&include_sovereign=true` Response

```json
{
  "items": [
    {
      "node_id": "node:did:key:z6MkAudio",
      "endpoints": [
        { "endpoint/url": "wss://audio.example/peer",
          "endpoint/transport": "wss",
          "endpoint/role": "listener",
          "endpoint/priority": 0 }
      ],
      "capability_id": "audio-transcription@participant:did:key:z6MkAnchor",
      "passport": { /* capability-passport.v1 */ },
      "published_at": "2026-04-01T10:00:00Z",
      "expires_at":   "2027-04-01T10:00:00Z",
      "anchor_identity": "participant:did:key:z6MkAnchor",
      "informal": false
    }
  ],
  "next": "cur:01JQCAPCUR002",
  "max-items": 100
}
```

### `GET /revocations?since=cur:...` Response

```json
{
  "items": [
    {
      "revocation_id": "passport-revocation:01JQREV001",
      "passport_id":   "passport:capability:network-ledger:01hznx",
      "node_id":       "node:did:key:z6MkOldLedger",
      "capability_id": "network-ledger",
      "revoked_at":    "2026-04-01T12:00:00Z",
      "signed_by":     "issuer"
    },
    {
      "revocation_id": "passport-revocation:01JQREV002",
      "passport_id":   "passport:capability:seed-directory:02abcd",
      "node_id":       "node:did:key:z6MkDecommissioned",
      "capability_id": "seed-directory",
      "revoked_at":    "2026-04-01T14:30:00Z",
      "signed_by":     "subject"
    }
  ],
  "next": "cur:01JQREVCUR003",
  "max-items": 100
}
```

## Implementation Notes

- The reference Node runtime now ships an embedded Seed Directory service
  inside the daemon process. It keeps the same HTTP surface and SQLite schema as
  the earlier sidecar design so deployments can still treat it as the same
  logical service.
- The Seed Directory persistence layer gains three capability-specific tables:
  `capability_registrations`, `capability_passports`, `revocations`.
- `capability_registrations` indexes `(node_id, capability_id)` as primary key
  with `published_at`, `expires_at`, and a foreign key to the passport record.
- `revocations` stores `revocation_id`, `passport_id`, `node_id`,
  `capability_id`, `revoked_at`, and `signed_by`. The signer identity
  (`issuer/participant_id` or `node_id`) is recoverable from the stored
  `passport_id` and `signed_by` columns; it need not be duplicated.
- The `revocations` table is the Seed Directory's federated publication log. It
  is not a required storage backend for node-local revocations whose effect is
  limited to one Node's dispatch gate.
- `GET /cap?capability` joins `capability_registrations` with
  `node_advertisements` to return current endpoints.
- `GET /attest/node-address/{node-id}` assembles
  `node-address-attestation.v1` from the current signed advertisement. In the
  embedded daemon implementation both `PUT /adv/{node-id}` and
  `GET /attest/node-address/{node-id}` use an active WSS
  `peer-handshake.v1` probe when a probe is configured. `GET /attest` issues
  `directory-confirmed` evidence only after a fresh successful probe; if a
  deployment has no probe configured, the same surface can still emit
  `directory-accepted` evidence.
- The two probes have different purposes: the PUT-time probe protects the
  directory write gate, while the attestation-time probe produces fresh
  third-party evidence. A PUT followed immediately by GET may therefore dial
  twice in the MVP. Add a short TTL cache for `ReachabilityProof` keyed by
  `(node_id, endpoint_url)` once traces show this is noisy.
- Active probes are synchronous in the embedded MVP server. Before operating at
  larger registration volume, bound probe concurrency with a semaphore or move
  probing into a small async worker pool with limited fan-out.
- capability registration rows should also project `anchor_identity` and
  `informal` as derived columns from the stored passport capability id so query
  filtering does not need to re-parse every passport blob on the hot path.
- `POST /revoke` branches on `signed_by`:
  - `"issuer"`: verify Ed25519 against `issuer/participant_id`; check issuer is
    sovereign; check issuer matches original passport's `issuer/participant_id`.
  - `"subject"`: verify Ed25519 against the public key decoded from `node_id`;
    check `node_id` matches original passport's `node_id`. No sovereignty check.
  Both paths: reject if `passport_id` is already in the revocation log (idempotent
  reject, not an error) or if the referenced passport is unknown.
- HTTP bearer tokens are deliberately out of scope for this surface. Operators
  may still place the service behind generic rate limiting or network policy,
  but such controls are operational hardening, not part of the capability trust
  model.
- The sovereign key set used by the Seed Directory for passport verification is
  loaded at startup from configuration, following the same pattern as the Node
  daemon's sovereign operator list.
- The `capability-passport-present.v1` post-handshake artifact (for direct
  Node-to-Node passport exchange, step 4 of the consumer flow) is a thin
  wrapper: `{ "schema": "capability-passport-present.v1", "passport": { ... } }`.
  Its full schema may be defined without a new proposal.
- The `capability-schema.v1` artifact is fetched over the existing peer-message
  channel with `capability.schema.present.request` and
  `capability.schema.present.response`. A URL may be carried as a documentation
  hint, but the protocol dependency is the content-addressed `schema/ref`, not
  the URL.
- Revocation cursor format follows the same opaque string pattern as `/adv?since`.

## Consequences

### Positive

- Single service answers both endpoint and capability queries.
- Passport verification at registration prevents unsigned capability claims.
- Consumer-side independent verification prevents directory-compromise attacks.
- `seed-directory` as a capability unifies the bootstrap mechanism.
- Multiple capabilities per Node are first-class, not an afterthought.
- Self-revocation (`signed_by: "subject"`) allows clean node decommissioning
  without requiring the sovereign operator to be online.

### Negative

- The embedded Seed Directory service grows in scope and maintenance surface.
- Consumers must implement revocation polling, adding operational complexity.
- Self-referential bootstrap (directory passports in distribution) requires
  governance discipline for key rotation.

## Alternatives Considered

### Accept raw self-reported capabilities without passport-form assertions

Rejected. Raw capability strings create taxonomy drift and cannot be audited as
governance or operator decisions. A Node may self-issue and directly present a
passport-form assertion, but receivers still evaluate that assertion under local
policy. Critical capabilities such as `network-ledger` require a suitable issuer
or federation policy before they are trusted.

### Separate capability directory service

Rejected. A second service multiplies bootstrap complexity. The existing Seed
Directory already has the persistence layer, inter-node trust model, and
deployment footprint needed.

### Gossip-based capability propagation

Deferred. Gossip is appropriate for eventual consistency at scale; for hard-MVP
with a small known set of infrastructure nodes, a single trusted directory with
polling is simpler and easier to audit.

## Open Questions

- Should `PUT /cap/{node-id}/{capability-id}` use `sequence/no` for ordering
  (like `/adv`) or rely on `expires_at` for replacement semantics?
- Should `GET /cap/{node-id}` return expired entries with a flag, or omit them?
- Should the Seed Directory enforce a maximum registration count per Node?
- Should `capability-passport-present.v1` be defined in this proposal or in a
  separate transport memo?
