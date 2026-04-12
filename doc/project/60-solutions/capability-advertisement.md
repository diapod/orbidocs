# Capability Advertisement

`Capability Advertisement` is the Node-facing solution contract for communicating
what a peer can do right now, together with the passport-form evidence needed to
evaluate those claims without a Seed Directory lookup.

It is not a component. It is a protocol artifact and read-side presentation
boundary used by Nodes, Seed Directories, and future discovery or routing
surfaces.

## Purpose

The artifact answers:

> What capabilities does this Node present now, under which capability ids,
> wire-visible names, assertion kinds, and credentials?

It deliberately separates two layers:

- `capabilities/presented` — the passport-form assertions and credentials,
- `capabilities/core` — the compatibility and routing projection derived from
  presented capabilities.

The projection is useful for fast matching. The presented passport assertions
are the verification input.

## Scope

This solution document covers:

- direct Node-to-Node capability exchange after handshake,
- datagram-style or broadcast capability publication where a transport permits it,
- responses to explicit capability queries,
- Seed Directory registration payloads that include the Node's capability
  advertisement,
- and custom or sovereign capabilities using the passport capability-id
  namespace.

It does not define:

- capability-specific wire protocols,
- federation recommendation policy,
- revocation transport beyond using passport and revocation artifacts,
- implementation-local host capabilities such as `recovery.sign` or
  `catalog.local.query`.

## Contract

Based on:

- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/50-requirements/requirements-006.md`
- `doc/project/60-solutions/CAPABILITY-REGISTRY.en.md`

Related schemas:

- `capability-advertisement.v1`
- `capability-schema.v1`
- `capability-schema-present.v1`
- `capability-passport.v1`
- `capability-passport-revocation.v1`
- `node-advertisement.v1`
- `peer-handshake.v1`

## Required Semantics

### Passport-Form Presentation

Every capability advertisement must carry `capabilities/presented`.

Each presented capability carries at least:

- `capability/id`
- `wire/name`
- `assertion/kind`
- `passport`

The `passport` field is the credential to verify. It may be a full
`capability-passport.v1` or a profile-compatible passport assertion accepted by
the relevant capability profile.

Receivers must verify the presented credential under:

- the capability profile,
- issuer or self-issued assertion rules,
- revocation state,
- and local policy.

### Routing Projection

`capabilities/core` is retained as a projection for compatibility and routing.

It should be derivable from:

- `capabilities/presented[*].wire/name`

It must not be treated as the authoritative trust proof.

### Assertion Kinds

The first assertion kinds are:

- `self-issued-passport`
- `issuer-passport`
- `federation-endorsed-passport`

`self-issued-passport` is sufficient for baseline protocol capabilities such as
`core/messaging` when local policy accepts self-issued claims.

`issuer-passport` is used when a capability profile requires another signer,
for example a sovereign operator or other accepted authority.

`federation-endorsed-passport` is used when the presented passport also carries
or references federation policy or endorsement material. The endorsement is a
policy input, not a replacement for the passport signature.

### Custom Capabilities

Custom capabilities should not invent unscoped global names.

They should use the same namespace as `capability-passport.v1`, including
identity-anchored forms such as:

- `audio-transcription@participant:did:key:z...`
- `~audio-transcription@participant:did:key:z...`

Their wire-visible projection uses:

- `sovereign/...`
- or `sovereign-informal/...`

with anchor reconstruction rules defined by the capability registry and Seed
Directory proposal.

### UI Presentation

Human-facing UI should display a capability by a short readable name, not by the
full `capability/id` string.

For identity-anchored custom capabilities, the UI should visibly mark that the
shown name is scoped or sovereign and make the full identifier available through
a link, copy action, pop-up hint, or detail drawer. The long identifier remains
the protocol identity of the capability; the short name is only the display
label.

### Capability Profile Metadata

A presented capability may include profile metadata for human display and
machine negotiation:

```json
{
  "capability/profile": {
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

`capability/profile` is metadata. It helps UI, negotiation, validation, and
operator inspection, but it does not replace `capability/id`, passport
verification, revocation checks, or local policy.

The same metadata may also appear inside `capability-passport.v1` as
`capability_profile`. When present in the passport, it is part of the signed
passport payload. When copied into `capability-advertisement.v1`, it is a
presentation summary.

`doc/url` is only a convenience mirror for humans. It must not be required for
protocol operation.

### Capability Schema Artifacts

Machine-readable capability schemas are represented as `capability-schema.v1`
artifacts.

The stable identity of the contract is:

- `schema/id`

The fetchable content-addressed reference is:

- `schema/ref`

The `schema/ref` should use an Orbiplex content address such as:

```text
orbiplex:blob:sha256:...
```

Receivers must treat `schema/ref` as the integrity anchor. A schema payload
fetched from any peer, cache, Seed Directory, or archivist surface is usable only
after its canonical content hashes to the advertised reference.

The first shape is:

```json
{
  "schema": "capability-schema.v1",
  "schema/id": "urn:orbiplex:capability-profile:audio-transcription:v1",
  "schema/ref": "orbiplex:blob:sha256:...",
  "schema/media-type": "application/schema+json",
  "capability/id": "audio-transcription@participant:did:key:z...",
  "wire/name": "sovereign/audio-transcription",
  "display/name": "Audio transcription",
  "description": "Transcribes audio input into timestamped text segments.",
  "lang": "en",
  "doc/ref": "orbiplex:blob:sha256:...",
  "content": {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "urn:orbiplex:capability-profile:audio-transcription:v1"
  },
  "published-at": "2026-04-12T10:00:00Z",
  "author/node-id": "node:did:key:z...",
  "author/participant-id": "participant:did:key:z...",
  "signature": {
    "alg": "ed25519",
    "value": "..."
  }
}
```

The schema artifact may describe:

- `scope` shape,
- request input shape,
- response output shape,
- expected error classes,
- retry and idempotency semantics,
- resource or artifact references used by the capability.

### Peer Message Kinds

Capability schema retrieval uses the existing authenticated Node-to-Node peer
message envelope. It does not require an HTTP URL.

Well-known message kinds:

| Message kind | Direction | Payload |
|---|---|---|
| `capability.schema.present.request` | requester -> provider | asks for one capability schema by `schema/ref` and optionally `schema/id` |
| `capability.schema.present.response` | provider -> requester | returns one `capability-schema-present.v1` payload containing a `capability-schema.v1` artifact or an error object |

Request payload:

```json
{
  "schema/ref": "orbiplex:blob:sha256:...",
  "schema/id": "urn:orbiplex:capability-profile:audio-transcription:v1",
  "accepted/media-types": [
    "application/schema+json"
  ]
}
```

Response payload:

```json
{
  "schema": "capability-schema-present.v1",
  "status": "ok",
  "artifact": {
    "schema": "capability-schema.v1"
  }
}
```

Error payload:

```json
{
  "schema": "capability-schema-present.v1",
  "status": "error",
  "error": {
    "kind": "schema-unavailable",
    "detail": "local node cannot present requested capability schema"
  }
}
```

Receivers should verify:

1. the peer session identity,
2. the response correlation id at the peer-message envelope layer,
3. the `capability-schema.v1` signature when present,
4. the content hash implied by `schema/ref`,
5. and local policy for the capability profile.

## Node Responsibilities

A Node that emits `capability-advertisement.v1` should:

- sign the advertisement with its Node identity,
- include a current `published-at`,
- include transport profiles currently exposed,
- include `core/messaging` as the minimal baseline wire projection,
- include a matching `capabilities/presented` entry for `core/messaging`,
- avoid advertising capabilities not currently routable or usable,
- keep `capabilities/core` synchronized with `capabilities/presented`,
- include enough passport material for the receiver to evaluate the claim
  without a Seed Directory lookup,
- serve any advertised `schema/ref` it can resolve through
  `capability.schema.present.request`, unless local policy intentionally
  withholds that schema.

## Receiver Responsibilities

A receiver should:

- validate the advertisement signature and freshness,
- treat `capabilities/core` as routing projection only,
- verify each relevant presented passport assertion before trusting it,
- apply local policy to decide whether self-issued, issuer-issued, or
  federation-endorsed assertions are acceptable,
- check revocation state for passport-backed capabilities when the profile
  requires revocation awareness,
- and tolerate unknown capability ids by ignoring or quarantining them rather
  than failing the entire peer relationship.

## Seed Directory Relationship

Seed Directory publication is optional for communicating capabilities.

The same capability advertisement may be:

- exchanged directly after handshake,
- returned in response to a peer capability query,
- broadcast where the transport profile permits it,
- or embedded in `PUT /cap` registration payloads.

The Seed Directory indexes capabilities it accepts under its own policy. It is a
discovery and caching surface, not the only authority that makes a capability
claim visible.

## Consumes

- `capability-passport.v1`
- `capability-schema.v1`
- `capability-schema-present.v1`
- `capability-passport-revocation.v1`
- `peer-handshake.v1`
- `node-advertisement.v1`

## Produces

- `capability-advertisement.v1`
- `capability-schema.v1`
- `capability-schema-present.v1`

## Notes

This solution keeps the core small:

- capability identifiers live in the passport namespace,
- advertisements provide the live presentation,
- Seed Directory provides optional indexing,
- and consumers retain local policy authority over trust.
