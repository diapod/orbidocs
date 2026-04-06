# Solution 032: Key Delegation Passports — Implementation Guidelines

Proposal: `doc/project/40-proposals/032-key-delegation-passports.md`

## Layered Implementation Order

Apply the change set from the bottom up:

1. contracts and schemas,
2. capability types and verification helpers,
3. daemon-side storage and runtime state,
4. Seed Directory persistence and query surfaces,
5. HTTP/API surfaces and operator flows.

Each layer should compile and make sense on its own before the next one starts
depending on it.

## Layer 0 — JSON Schemas

### `key-delegation.v1`

Add a new schema for the delegation artifact. The contract should carry:

- `schema = "key-delegation.v1"`,
- `delegation_id`,
- `proxy_key`,
- `grants`,
- `max_chain_depth`,
- `issued_at`,
- `expires_at`,
- optional `parent_delegation_id`,
- `issuer/participant_id`,
- `issuer/node_id`,
- `signature`.

Practical constraints:

- `delegation_id` should use the `delegation:key:` prefix,
- `proxy_key` must be `did:key:...`,
- `expires_at` is mandatory,
- `max_chain_depth > 0` stays schema-valid but runtime-rejected in MVP,
- `grants["signing/capability"]` must be a non-empty array when present.

### `capability-passport.v1`

The current passport contract already uses flat slash-style issuer fields such
as `issuer/participant_id` and `issuer/node_id`. Extend that same top-level
shape with:

```json
"issuer/signing_key":   { "type": "string", "pattern": "^did:key:z" },
"issuer/delegation_id": { "type": "string", "pattern": "^delegation:key:.+" }
```

Require pairing semantics:

```json
"allOf": [
  {
    "if": { "required": ["issuer/signing_key"] },
    "then": { "required": ["issuer/delegation_id"] }
  },
  {
    "if": { "required": ["issuer/delegation_id"] },
    "then": { "required": ["issuer/signing_key"] }
  }
]
```

### Schema publication

Expose the new delegation schema from the daemon alongside the existing schema
surfaces:

```rust
"/v1/schemas/key-delegation" => key_delegation_schema_response(),
```

## Layer 1 — `capability` crate

### New module: `delegation.rs`

This module should define the delegation artifact and its validation rules.

Suggested public surface:

```rust
pub const KEY_DELEGATION_SCHEMA_V1: &str = "key-delegation.v1";
pub const KEY_DELEGATION_ID_PREFIX: &str = "delegation:key:";
pub const GRANT_SIGNING_CAPABILITY: &str = "signing/capability";
pub const GRANT_WILDCARD: &str = "*";

pub type KeyDelegationGrants = BTreeMap<String, Vec<String>>;

pub struct KeyDelegationPassport { ... }
pub struct KeyDelegationSignature { ... }
```

Minimal required behavior:

- structural `validate()`,
- `canonical_payload_json()` without `signature`,
- `sign_with_issuer_private_key_base64url()`,
- `verify_signature()`,
- `verify(now_rfc3339)`,
- `grants_allow_capability(...)`.

### `CapabilityPassport`

Extend `CapabilityPassport` with:

```rust
#[serde(rename = "issuer/signing_key", skip_serializing_if = "Option::is_none", default)]
pub issuer_signing_key: Option<String>,

#[serde(rename = "issuer/delegation_id", skip_serializing_if = "Option::is_none", default)]
pub issuer_delegation_id: Option<String>,
```

Validation rules:

- both fields must be present together or absent together,
- `issuer/signing_key` must start with `did:key:`,
- `issuer/delegation_id` must start with `delegation:key:`.

Verification rules:

- when `issuer/signing_key` is absent, preserve the existing direct participant
  signing path,
- when present, verify the passport signature against the proxy `did:key`
  instead of the participant key.

Suggested signing helper:

```rust
pub fn sign_with_proxy_key_base64url(
    &mut self,
    proxy_private_key_base64: &str,
) -> Result<(), CapabilityPassportError>
```

### `CapabilityPassportRevocation`

Revocations now need to target both capability passports and key delegations.
Change the struct from a single mandatory `passport_id` to a paired model:

```rust
pub passport_id: Option<String>,
pub target_id: Option<String>,
```

Rules:

- exactly one of `passport_id` or `target_id` must be present,
- `passport_id` still means capability-passport revocation,
- `target_id` means delegation revocation and must validate against
  `delegation:key:`.

Helpful methods:

```rust
pub fn effective_target_id(&self) -> Option<&str>;
pub fn is_delegation_revocation(&self) -> bool;
```

### `delegation_cache.rs`

Add a dedicated cache for delegation passports. MVP can stay simple:

- primary index: `delegation_id -> passport`,
- secondary index: `proxy_key -> delegation_id` or `proxy_key -> Vec<delegation_id>`.

Important note:

The proposal allows multiple active delegations for the same `proxy_key` from
different issuers. If the secondary index assumes only one delegation per proxy
key, document that as an MVP simplification or store a vector immediately.

## Layer 2 — daemon-side storage and runtime

### Proxy key store

Add a new local key category for proxy keys. These are not:

- participant identity keys,
- node transport keys.

They are operational signing keys used only under the scope of a delegation
passport.

Suggested stored record:

```rust
struct ProxyKeyRecord {
    key_id: String,
    proxy_key_did: String,
    storage: ProxyKeyStorage,
    created_at: String,
    deleted: bool,
}
```

Suggested storage enum:

```rust
enum ProxyKeyStorage {
    Plaintext { private_key_base64url: String },
    Encrypted(ParticipantKeyEnvelope),
}
```

This reuse of `ParticipantKeyEnvelope` keeps the storage story simple and
aligned with Proposal 031.

### Issued delegation records

Persist issued delegations separately from proxy keys:

```rust
struct IssuedKeyDelegationRecord {
    delegation_id: String,
    key_id: String,
    capability_ids: Vec<String>,
    issued_at: String,
    expires_at: String,
    deleted: bool,
}
```

The commit-log integration should cover:

- replay,
- checkpoint capture,
- rebuild of in-memory maps on startup.

### Runtime fields

Daemon state should gain at least:

- `proxy_key_records`,
- `proxy_key_cache` or an equivalent unlock/cache mechanism,
- `issued_delegations`,
- `delegation_cache`.

### Delegation ID generation

Keep generated IDs aligned with the contract prefix:

```rust
generate_trace_id(KEY_DELEGATION_ID_PREFIX.trim_end_matches(':'))
```

Do not generate `delegation:...` if the rest of the slice validates and
documents `delegation:key:...`.

## Layer 3 — Seed Directory

### Persistence

Add a `key_delegations` table with at least:

- `delegation_id`,
- `proxy_key`,
- `participant_id`,
- `node_id`,
- `expires_at`,
- `published_at`,
- `delegation_json`.

### HTTP surface

Add:

- `PUT /key/{delegation_id}` for explicit id-bound registration,
- `GET /key/{delegation_id}` for exact lookup,
- `GET /key?proxy_key=...`,
- `GET /key?participant_id=...&capability=...`.

Verification on write should enforce:

- valid delegation signature,
- sovereign issuer,
- `max_chain_depth == 0` in MVP,
- body `delegation_id` matching the URL id where applicable.

### Revocation feed

The existing revocation feed should carry delegation revocations cleanly by
including `target_id` in the serialized entry shape. Consumers then use
`effective_target_id()` instead of hard-wiring `passport_id`.

## Layer 4 — verification and sync

### Capability passport verification

The delegated verification branch should:

1. validate direct participant sovereignty,
2. verify the capability passport signature with the proxy key,
3. resolve `issuer/delegation_id`,
4. load the delegation from cache or Seed Directory,
5. verify the delegation signature with the participant key,
6. verify issuer match, expiry, revocation, and grant coverage,
7. reject `max_chain_depth > 0` in MVP.

This keeps the trust chain explicit:

```text
participant key
  -> signs key-delegation.v1
       -> authorizes proxy did:key
            -> signs capability-passport.v1
```

### Background sync

`sync_seed_directories_once` should:

- prefetch delegation records relevant to passport verification,
- invalidate delegation cache entries on delegation revocations,
- keep passport cache and delegation cache separate but parallel in behavior.

## Layer 5 — daemon HTTP/API surface

### Proxy keys

Suggested endpoints:

- `POST /v1/host/keys/generate`
- `POST /v1/host/keys/import`
- `GET /v1/host/keys`
- `POST /v1/host/keys/{key_id}/unlock`
- `DELETE /v1/host/keys/{key_id}`

### Delegations

Suggested endpoints:

- `POST /v1/host/capabilities/capability.key-delegation.issue`
- `POST /v1/host/capabilities/capability.key-delegation.publish`
- `POST /v1/host/capabilities/capability.key-delegation.revoke`

Capability passport issuance should also accept an optional `proxy_key_id`
parameter, selecting the delegated signing path instead of direct participant
signing.

## Practical sequencing

Recommended commit order:

1. schemas + `capability` types,
2. revocation target generalization,
3. delegation cache,
4. proxy key store in daemon,
5. issued delegation records and runtime rebuild,
6. Seed Directory `/key` persistence and handlers,
7. daemon verification chain,
8. HTTP/operator surfaces.

Each step should leave the tree in a compiling state.

## MVP boundaries

Keep these restrictions explicit in both code and docs:

- no sub-delegation,
- no multisig,
- no wildcard revocation by issuer,
- no attempt to collapse participant keys and proxy keys into one abstraction,
- no hidden transport-level meaning for proxy keys.

The feature is application-layer delegation, not a new identity anchor.
