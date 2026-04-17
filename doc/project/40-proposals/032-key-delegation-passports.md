# Proposal 032: Key Delegation Passports

Based on:
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`
- `doc/project/40-proposals/030-identity-recovery-service.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`

## Status

Draft / Under Discussion.

## Date

2026-04-06

## Executive Summary

Capability passports are currently signed directly by a participant's private
key — the same high-value key that anchors the node's sovereign identity.
Every operational passport signing event therefore exposes that key to use,
increases its attack surface, and makes offline or locked-key operation
(Proposal 031) impractical for automated workflows.

This proposal introduces `key-delegation.v1` as a scoped delegation artifact:
a participant signs a delegation passport that authorises a separate
**proxy key** (`did:key`) to sign capability passports on the participant's
behalf, within explicit grant boundaries.  The proxy key can be node-resident,
frequently used, and rotated without touching the participant key.

The participant key is used once to issue (and, if needed, revoke) the
delegation.  All subsequent operational signing is performed by the proxy key.

## Problem

The current architecture couples three concerns in a single key:

1. **Identity anchor** — the participant key defines the participant's
   cryptographic identity and is embedded in `participant_id`.
2. **Operational signer** — the same key signs capability passports, revocations,
   and any future artifact that requires sovereign authority.
3. **Availability requirement** — because the key must be present for every
   operational signing event it cannot be kept cold or locked without breaking
   automated flows.

This coupling creates a security/availability trade-off with no good resolution:
locking the key (Proposal 031) breaks automation; keeping it hot reduces
key-at-rest security; rotating it changes the node's identity.

The delegation passport breaks the coupling by introducing a separate proxy key
whose scope is deliberately narrow and whose lifecycle is independent of the
participant key.

## Scope

This proposal covers:

- the `key-delegation.v1` artifact schema and its JSON Schema contract,
- `DelegationProof` — a compact inline bearer credential extracted from a full
  key-delegation passport and embedded next to proxy-key signatures,
- a **proxy key store** — generation, import, export, and local storage of
  non-participant, non-transport Ed25519 keys,
- extension of participant-signed artifacts (`capability-passport.v1`,
  issuer-signed `capability-passport-revocation.v1`, later participant
  ciphertexts) with optional `issuer_delegation` proof,
- a `/key` endpoint on the Seed Directory for registration and lookup of
  full delegation passports used for management, publication, audit, and
  revocation feeds,
- a `DelegationCache` on owning/managing nodes (analogous to `PassportCache`) for
  choosing a local proxy key; remote signature verification is self-contained,
- updated participant-artifact signing and verification algorithm that verifies
  the inline proof and then verifies the artifact with the proof's proxy key,
- daemon HTTP API for delegation lifecycle management.

Out of scope for this proposal:

- sub-delegation (proxy key delegating to a further proxy key) — the schema
  carries `max_chain_depth` to make this a future additive change,
- multi-signature (M-of-N) grants — noted in schema design but not implemented,
- `signing/org`, `signing/proxy`, or other non-capability grant types beyond
  `signing/capability`.

## Security Model

### What this improves

- **Participant key stays cold**: after issuing the delegation passport the
  participant key does not need to be available for routine operations.  It is
  only needed to issue, revoke, or re-issue delegations — infrequent, deliberate
  acts.
- **Blast radius of proxy key compromise**: a stolen proxy key grants signing
  authority only over the listed capabilities (or, if `*`, all capabilities),
  and only until the delegation expires or is revoked.  It does not grant
  identity authority, cannot change the participant's sovereign binding, and
  cannot create new delegations (at `max_chain_depth: 0`).
- **Forced expiry**: `expires_at` is mandatory.  There are no permanent
  delegations.  Short-lived proxy keys (30–90 days) limit the window of silent
  compromise.
- **Revocation path**: a delegation passport can be revoked at any time by the
  participant key.  Revocations propagate through the Seed Directory's existing
  revocation surface; consuming nodes must poll and respect them.

### What this does not protect against

- **Compromised participant key**: if the participant key is stolen the attacker
  can issue new delegations or revoke existing ones.  This proposal does not
  address the participant key's own security; that is Proposal 031's domain.
- **Delegation revocation lag**: nodes that cache delegation passports and do
  not poll the revocation surface promptly may continue to honour a revoked
  delegation for up to one cache TTL.  The TTL must be chosen to balance
  availability against revocation freshness.
- **Wildcard grant abuse**: a `["*"]` capability grant is operationally
  convenient but semantically equivalent to delegating full capability signing
  authority.  Operators should prefer explicit capability lists.

### Multisig note

The single-signature scheme of MVP does not prevent a future extension to M-of-N
signatures.  The `signature` object in `key-delegation.v1` is deliberately
structured to allow a future `co_signatures` array alongside the primary
`signature` field without breaking the schema.  This is noted as a Post-MVP
item.

## Design

### Proxy key store

A new category of keys managed by the daemon — distinct from the node transport
key and from participant keys — is called **proxy keys**.  Each proxy key is an
Ed25519 keypair identified by its public `did:key` representation.

#### Storage record

```
ProxyKeyRecord {
    key_id:     "key:did:key:z6Mk...",   // key: prefix + did:key
    did_key:    "did:key:z6Mk...",
    storage:    Plaintext { key_base64: "..." }
              | Encrypted { envelope: ParticipantKeyEnvelope },
    created_at: "<RFC3339>",
    label:      Option<String>,          // operator-supplied human label
}
```

The `Encrypted` variant reuses `participant-key-envelope.v1` from Proposal 031
verbatim (Argon2id KDF + AES-256-GCM AEAD).  Proxy key generation and import
therefore automatically benefit from the passphrase-lock subsystem without
duplication.

#### Generation

```
POST /v1/host/keys/generate
{ "label": "my-proxy-key", "passphrase": "<optional>" }

→ 201
{ "key_id": "key:did:key:z6Mk...", "did_key": "did:key:z6Mk...", "label": "my-proxy-key" }
```

The private key material never appears in the response.  The operator must call
the export endpoint explicitly to obtain it.

#### Import

```
POST /v1/host/keys/import
{
  "private_key_base64": "<raw 32-byte Ed25519 scalar, base64url>",
  "label": "imported",
  "passphrase": "<optional>"
}

→ 201
{ "key_id": "key:did:key:z...", "did_key": "did:key:z...", "label": "imported" }
```

#### Export (download)

```
GET /v1/host/keys/{key_id}/export?format=raw|envelope&passphrase=<optional>
```

- `format=raw` — returns the plaintext private key as base64url; only permitted
  if the key is currently unlocked (plaintext in memory or unlocked via
  passphrase).
- `format=envelope` — returns the `participant-key-envelope.v1` JSON blob
  exactly as stored on disk; can be imported to another node.

The export endpoint requires operator authentication (control token) and
produces an audit trace entry.

#### List and delete

```
GET    /v1/host/keys
DELETE /v1/host/keys/{key_id}
```

Deletion is refused if the key is currently referenced by a non-revoked,
non-expired delegation passport.

### `key-delegation.v1` schema

```json
{
  "schema":          "key-delegation.v1",
  "delegation_id":   "delegation:key:<timestamp>:<random>",
  "proxy_key":       "did:key:z6Mk...",
  "grants": {
    "signing/capability": ["network-ledger", "escrow"]
  },
  "max_chain_depth": 0,
  "issued_at":             "2026-04-06T12:00:00Z",
  "expires_at":            "2026-10-06T12:00:00Z",
  "issuer/participant_id": "participant:did:key:z...",
  "issuer/node_id":        "node:did:key:z...",
  "signature":             { "alg": "ed25519", "value": "<base64url>" }
}
```

**Field notes:**

- `delegation_id` — unique identifier, pattern `^delegation:key:.+$`.
- `proxy_key` — `did:key` representation of the delegated public key.
- `grants` — a map from grant type to list of target identifiers.
  - `signing/capability` — the proxy key may sign `capability-passport.v1`
    artifacts for the listed capability IDs.  The special value `"*"` grants
    all capability IDs.  The list must be non-empty.
  - Additional grant types (`signing/org`, `signing/proxy`) are reserved for
    future proposals and must be ignored by verifiers that do not recognise them
    (open-world extension semantics).
- `max_chain_depth` — `0` means the proxy key may not itself create delegation
  passports.  A value of `1` would allow one level of re-delegation.  MVP
  implementations must reject any delegation passport where `max_chain_depth > 0`
  until sub-delegation is formally specified.
- `expires_at` — **mandatory**.  Implementations must reject delegation passports
  lacking this field.  The recommended maximum TTL is 365 days; issuance UI
  should warn for values exceeding that.
- `issuer/node_id` — the node on which the delegation passport was created (and
  on which the signing participant key resided at time of issuance).
- `signature` — Ed25519 signature of the canonical JSON representation of the
  compact delegation contract (`delegation_id`, `proxy_key`, `principal_key`,
  `grants`, `expires_at`), signed by the private key of
  `issuer/participant_id`.

The full `key-delegation.v1` passport is a registration and management artifact.
Its metadata (`schema`, `issued_at`, `issuer/node_id`, `max_chain_depth`,
`parent_delegation_id`) travels through Seed Directory and operator surfaces, but
does not enter the MVP signature payload.  The signature covers the smaller
contract that can be embedded later as `DelegationProof`.

### `DelegationProof` inline bearer form

Every signature made with a proxy key carries a compact proof:

```json
{
  "delegation_id": "delegation:key:<timestamp>:<random>",
  "proxy_key": "did:key:z6Mk...",
  "principal_key": "did:key:z6MkPrincipal...",
  "grants": {
    "signing/capability": ["network-ledger", "escrow"]
  },
  "expires_at": "2026-10-06T12:00:00Z",
  "principal_signature": "<base64url>"
}
```

Verification is self-contained:

1. derive `participant:did:key:...` from `principal_key` and compare it to the
   expected participant id,
2. verify `principal_signature` over the canonical compact proof payload using
   `principal_key`,
3. verify the surrounding artifact signature using `proxy_key`,
4. check `expires_at > now`,
5. in domain policy, check `grants` for the required operation/target pair.

The verifier does not need to fetch `key-delegation.v1` from the Seed Directory.
If it also consumes revocation feeds it may reject an embedded
`delegation_id` that appears there, but that is a revocation policy layer, not a
dependency of signature verification.

### Extension to participant-signed artifacts

`capability-passport.v1` and issuer-signed
`capability-passport-revocation.v1` gain one optional field,
`issuer_delegation`, alongside existing `issuer/participant_id` and
`issuer/node_id`-style fields:

```json
"issuer/participant_id": "participant:did:key:z...",
"issuer/node_id":        "node:did:key:z...",
"issuer_delegation": {
  "delegation_id": "delegation:key:1775477969437951000:ab12",
  "proxy_key": "did:key:z6Mk...",
  "principal_key": "did:key:z6MkPrincipal...",
  "grants": { "signing/capability": ["network-ledger"] },
  "expires_at": "2026-10-06T12:00:00Z",
  "principal_signature": "<base64url>"
}
```

When both are absent the verifier uses the public key embedded in
`issuer/participant_id` (direct signing path — existing behaviour).  When
`issuer_delegation` is present, it gives the verifier the proxy key, original
participant key, grant set, expiry and principal signature inline.

The identifiers embedded in a proxy-signed capability passport form a complete
and unambiguous audit chain:

```
capability-passport
  issuer/participant_id   → sovereign identity that ultimately authorises the passport
  issuer/node_id          → node on which the passport was issued
  issuer_delegation.proxy_key          → proxy key did:key that produced the signature
  issuer_delegation.principal_key      → public key that derives to issuer/participant_id
  issuer_delegation.delegation_id      → management / revocation reference
  issuer_delegation.grants             → scope under which signing was authorised
  issuer_delegation.principal_signature→ issuer signature over the proof payload
```

For future sub-delegated chains (`max_chain_depth > 0`), each `key-delegation.v1`
record gains an optional `parent_delegation_id` field that points to the
delegation from which it was derived.  The root of the chain is always a
delegation whose issuer is a direct participant key (no `parent_delegation_id`).
This keeps chain traversal a simple ID-linked walk with a bounded depth, and
every step is independently verifiable.

`issuer_delegation` is excluded from the surrounding artifact's canonical
payload.  It has its own principal signature and can be copied unchanged beside
multiple proxy-key signatures until it expires.

### Capability passport issuance with proxy key

When the daemon issues or signs a passport:

1. The daemon resolves the proxy key from the proxy key store.
2. It tries to find a non-expired, non-revoked local delegation passport for
   this proxy key granting `signing/capability` over the requested
   `capability_id` (or `*`).
3. If found and the proxy private key is unlocked, it signs the capability
   passport with the proxy private key and embeds `delegation_passport.to_proof()`
   as `issuer_delegation`.
4. Otherwise it falls back to direct participant-key signing and leaves
   `issuer_delegation` absent.
5. `issuer/participant_id` is set to the issuing participant (the same
   participant who issued the delegation passport).

The signed capability passport is otherwise identical to a directly signed one
and follows the same storage and publication flow.

### Seed Directory `/key` endpoint

A new endpoint is added to the Seed Directory alongside `/cap` and `/revocations`:

#### Register delegation

```
POST /key
Content-Type: application/json

{
  "delegation": { /* key-delegation.v1 object */ },
  "node_id":    "node:did:key:z..."
}
```

The Seed Directory verifies:
- The `key-delegation.v1` signature is valid (using the public key embedded in
  `issuer/participant_id`).
- `expires_at` is present and in the future.
- `max_chain_depth` is `0` (MVP restriction; relaxed when sub-delegation is
  specified).

On success the delegation is stored and indexed by both `proxy_key` and
`issuer/participant_id`.

#### Query by delegation ID (primary lookup)

```
GET /key?delegation_id=delegation:key:1775477969437951000:ab12

→ 200
{
  "delegation":    { /* key-delegation.v1 */ },
  "registered_at": "...",
  "node_id":       "node:did:key:z..."
}
```

Returns exactly one entry or `404`. This lookup is for operator inspection,
publication state, revocation/audit, and local prewarming. It is no longer
required by remote passport verification.

#### Query by proxy key (secondary lookup)

```
GET /key?proxy_key=did:key:z6Mk...
```

Returns all active (non-expired, non-revoked) delegations where `proxy_key`
matches the given `did:key`.  Multiple concurrent delegations for the same proxy
key from different participants are possible but unusual; the response is a list.
Used primarily by the background sync task for proactive cache pre-warming.

#### Query by participant (discovery and auditing)

```
GET /key?participant_id=participant:did:key:z...&capability=network-ledger
```

Returns all active delegations issued by that participant for the given
capability.  Useful for monitoring, auditing, and key rotation workflows.

#### Revocation

Delegation passports are revoked through the existing `/revocations` surface,
using the same `capability-passport-revocation.v1` schema with `revocation_id`
referencing the `delegation_id` field:

```json
{
  "schema":         "capability-passport-revocation.v1",
  "revocation_id":  "revocation:delegation:key:...",
  "target_id":      "delegation:key:<timestamp>:<random>",
  "signed_by":      "issuer",
  "reason":                "key_rotation",
  "revoked_at":            "...",
  "issuer/participant_id": "participant:did:key:z...",
  "issuer/node_id":        "node:did:key:z...",
  "signature":             { "alg": "ed25519", "value": "..." }
}
```

Seed Directory consumers poll `/revocations` with the existing cursor mechanism.
The daemon's background sync (`sync_seed_directories_once`) invalidates affected
delegation cache entries on receiving a matching revocation.

### `DelegationCache`

A new in-memory cache on every consuming node, structurally analogous to
`PassportCache`:

```rust
struct CachedDelegation {
    delegation:  KeyDelegationPassport,
    cached_at:   Instant,
    valid_until: Option<Instant>,  // None = use delegation.expires_at
}

// primary index: keyed by delegation_id (exact, deterministic lookup)
// secondary index: keyed by proxy_key did:key (for proactive pre-warming by capability)
type DelegationCache = HashMap<String, CachedDelegation>;
```

Two management lookup paths are supported:

- **By `delegation_id`** (primary for management/revocation): exact match from
  the `issuer_delegation.delegation_id` field embedded in the capability
  passport, or from an issued-delegation record.
- **By `proxy_key`** (secondary, used for proactive pre-warming): the background
  sync task fetches all active delegations for `PASSPORT_SYNC_CAPABILITY_IDS`
  and indexes them by both `delegation_id` and `proxy_key`.

The cache is populated:
- proactively by the background seed-sync task (adds `signing/capability`
  delegations for `PASSPORT_SYNC_CAPABILITY_IDS`, analogous to how capability
  passports are pre-fetched),
- on-demand when a verifier encounters a `delegation_id` not present in the
  cache (fires an async Seed Directory fetch via `/key?delegation_id=...`).

TTL default: 10 minutes.  Revocation events (received via `/revocations` poll)
immediately invalidate matching entries regardless of TTL.

### Verification algorithm

The updated capability passport verification procedure:

```
verify_capability_passport(passport, sovereign_participant_ids, now, required_grant):

  participant_id = passport["issuer/participant_id"]
  unless participant_id ∈ sovereign_participant_ids:
    reject("issuer is not a sovereign participant")

  proof = passport["issuer_delegation"]
  if proof is absent:
    // direct signing path — existing behaviour
    verify_signature(passport, public_key_from_did_key(participant_id)) or reject
    return OK

  // proxy signing path
  if participant_id_from_did_key(proof.principal_key) != participant_id:
    reject("delegation issuer mismatch")

  verify_signature(proof.canonical_payload, proof.principal_key, proof.principal_signature)
    or reject("delegation proof signature invalid")

  if proof.expires_at <= now:
    reject("delegation proof expired")

  verify_signature(passport, proof.proxy_key) or reject("proxy signature invalid")

  grants = proof.grants[required_grant.type] ?? []
  unless required_grant.target ∈ grants or "*" ∈ grants:
    reject("capability not covered by delegation grant")

  return OK
```

The remote verification path has no Seed Directory fetch and no
`DelegationCache` dependency.  Seed Directory and the local cache remain useful
for discovering, publishing, listing, revoking, and choosing local delegation
records before signing.

## Components and Roles

### Daemon — proxy key store

- Stores `ProxyKeyRecord` on disk under `data_dir/proxy-keys/`.
- Shares the `ParticipantKeyEnvelope` format (and unlock/lock mechanism from
  Proposal 031) for encrypted storage.
- Exposes CRUD HTTP surface for generation, import, export, and deletion.

### Daemon — delegation passport lifecycle

- Issues `key-delegation.v1` passports on operator request: resolves proxy key,
  builds and signs the artifact, stores as `IssuedKeyDelegationRecord` on disk.
- Revokes via the existing revocation path; stores revocation record.
- Refreshes `local_delegation_passports` (in-memory map analogous to
  `LocalCapabilityPassports`) after each issue, revoke, or delete.

### Daemon — verification layer

- Extends participant signing with `ParticipantSigningContext`:
  `Direct { participant_id, private_key }` or
  `Delegated { proxy_private_key, proof }`.
- Extends capability-passport and issuer-revocation verification to accept
  inline `issuer_delegation` and to check the required grant at the policy
  boundary.
- Keeps `DelegationCache` on the management/signing side; remote verification is
  self-contained.

### Daemon — background sync

- `sync_seed_directories_once` fetches `/key` entries for all
  `PASSPORT_SYNC_CAPABILITY_IDS` alongside the existing `/cap` fetch.
- Populates `DelegationCache` and invalidates entries matching revocations from
  `/revocations`.

### Seed Directory — `/key` surface

- Accepts `POST /key` registrations; verifies delegation signature and policy
  constraints before storing.
- Answers `GET /key?proxy_key=...` and `GET /key?participant_id=...&capability=...`
  queries.
- Participates in the existing `/revocations` cursor feed for delegation
  revocation events.

### Node UI — delegation management

- Lists active proxy keys and their associated delegations.
- Guides operator through: generate/import proxy key → issue delegation → publish
  to Seed Directory.
- Shows delegation expiry prominently; warns when `expires_at` is within 14 days.
- Shows revocation action on each live delegation.
- Handles `signing_key` display in capability passport detail view.

## Workflows

### Issue a delegation passport

1. Operator generates or imports a proxy key via
   `POST /v1/host/keys/generate` or `POST /v1/host/keys/import`.
2. Operator opens "Delegation" panel; selects the proxy key and the capability
   IDs to grant (e.g. `network-ledger`); sets `expires_at`.
3. UI calls `POST /v1/host/capabilities/capability.key-delegation.issue`.
4. Daemon verifies the participant key is available (unlocked per Proposal 031
   if passphrase-locked), builds and signs the `key-delegation.v1` artifact,
   and stores it on disk.
5. Operator publishes: `POST /v1/host/capabilities/capability.key-delegation.publish`.
6. Daemon pushes the delegation to Seed Directory `/key`; logs the registered
   entry with `last_published_at`.

### Sign a capability passport using the proxy key

1. Operator (or automated flow) calls
   `POST /v1/host/capabilities/capability.passport.issue`
  for a capability covered by an active local delegation.
2. Daemon chooses a participant signing context. If a matching delegation and
   unlocked proxy key are available it chooses `Delegated`; otherwise it chooses
   `Direct` and requires the participant key.
3. In delegated mode the daemon signs the capability passport with the proxy key
   and embeds `issuer_delegation`. The participant key is not required.
4. Capability passport is stored and may be published to Seed Directory `/cap`
   as usual.

### Rotate proxy key

1. Operator generates a new proxy key.
2. Operator issues a new delegation passport for the new key.
3. Operator revokes the old delegation: the local daemon stops choosing it for
   future signatures. Already issued capability passports remain valid until
   their own `expires_at` and the embedded proof's `expires_at` unless the
   passport itself is revoked or a consuming policy additionally rejects
   revoked proof `delegation_id`s.
4. Operator deletes the old proxy key from the store (refused if it is the
   `signing_key` of any non-expired capability passport that hasn't been
   superseded — UI should warn).

### Emergency revocation

1. Participant key is unlocked.
2. Operator calls `POST /v1/host/capabilities/capability.key-delegation.revoke`
   with `delegation_id`.
3. Daemon signs a revocation artifact and publishes to Seed Directory
   `/revocations`.
4. Other nodes pick up the revocation on their next `/revocations` poll; their
   `DelegationCache` entries are invalidated.
5. Future local issuance does not use the revoked delegation. Already-issued
   proxy-signed artifacts still carry enough proof to verify until proof expiry;
   revoke the capability passport too if the intended effect is immediate
   withdrawal of that passport.

## Relationship to Prior Proposals

### Proposal 024 (Capability Passports)

This proposal extends Proposal 024's signing model. The
`capability-passport.v1` schema gains optional `issuer_delegation` carrying a
compact inline proof. Verification logic gains the proof → proxy-key branch.
All existing direct-signed passports continue to work without modification.

### Proposal 025 (Seed Directory as Capability Catalog)

The Seed Directory gains a new `/key` endpoint alongside `/cap` and
`/revocations`.  The operational model (node pushes, directory verifies and
stores, consumers poll) is identical.  Delegation revocations flow through the
existing `/revocations` cursor.

### Proposal 030 (Identity Recovery Service)

Orthogonal.  Proposal 030 addresses recovery after loss of the participant key;
this proposal reduces how often the participant key must be used.  Together they
form a coherent key hygiene strategy: the participant key is cold (030 ensures
it can be recovered if lost; 032 ensures it rarely needs to be live).

### Proposal 031 (Participant Key Passphrase Lock)

Directly complementary.  Proposal 031 makes the participant key require explicit
human unlock; this proposal reduces the operations that require the participant
key to fire, making the locked-by-default posture practical for production nodes.

The proxy key store shares the `ParticipantKeyEnvelope` storage format with
Proposal 031's key encryption layer, avoiding parallel implementations.

## Known Limitations (MVP)

- **`max_chain_depth: 0` only**: sub-delegation is not implemented.  The field
  exists in the schema but verifiers reject any delegation with a non-zero value.
- **Single signature**: M-of-N multisig is not implemented.  The schema is
  designed to accommodate a future `co_signatures` extension field without
  breaking existing delegations.
- **`signing/capability` grant type only**: other grant types (`signing/org` etc.)
  are reserved namespace entries.  Verifiers ignore unknown grant types; issuance
  UI must not allow them until a covering proposal is accepted.
- **Revocation lag**: consuming nodes that do not run the seed-sync background
  task (or run it infrequently) may honour a revoked delegation for up to one
  cache TTL.  This is a deployment concern, not a protocol flaw, but it means
  revocation is eventually consistent, not immediate.
- **No wildcard revocation**: revoking all delegations for a participant (e.g.
  after participant key compromise) requires enumerating and revoking each
  delegation individually.  A "revoke all by issuer" shortcut is a Post-MVP
  item.
- **Proxy key tied to a single node**: the proxy key store is local.  A proxy
  key generated on one node cannot be automatically shared with sibling nodes in
  a multi-node deployment.  Operators must import/export manually.

## Post-MVP

- **Sub-delegation** (`max_chain_depth: 1`): a proxy key may issue a further
  delegation, allowing tiered key hierarchies for large operator teams.
- **M-of-N multisig**: `co_signatures` array in `key-delegation.v1`; verifier
  requires ≥ M valid signatures over the same canonical payload.
- **Additional grant types**: `signing/org` (sign org identity artifacts),
  `signing/proxy` (explicit permission to create sub-delegations),
  `signing/revocation` (proxy key may sign revocations on behalf of participant).
- **Wildcard revocation**: `POST /key/revoke-all?issuer=participant:did:key:z...`
  for emergency key compromise scenarios.
- **Delegation health monitor**: daemon background task that warns when
  active delegations are within N days of `expires_at`; surfaces in UI and
  optionally triggers an SSE event.
- **Cross-node proxy key sync**: a signed export bundle that can be imported on
  a sibling node, with the provenance of the original node recorded.
