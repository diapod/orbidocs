# Coding Guide 032 — Key Delegation Passports

This guide is the implementation-oriented companion to Proposal 032.

The rule of thumb is simple:

- one coherent step per file or subsystem,
- keep the tree compiling after each step,
- prefer explicit contracts over broad rewrites.

## Step 1 — extend the `capability` crate

### 1a. Add delegation-specific modules

Create:

- `capability/src/delegation.rs`
- `capability/src/delegation_cache.rs`
- `capability/src/signing.rs`

Export the public types from `capability/src/lib.rs`.

### 1b. Extend `CapabilityPassport`

Add:

```rust
#[serde(skip_serializing_if = "Option::is_none", default)]
pub issuer_delegation: Option<DelegationProof>,
```

Validation requirements:

- if present, `issuer_delegation.principal_key` derives to
  `issuer/participant_id`,
- `issuer_delegation.proxy_key` and `principal_key` start with `did:key:`,
- `issuer_delegation.delegation_id` starts with `delegation:key:`,
- canonical passport payload explicitly removes both `signature` and
  `issuer_delegation`.

### 1c. Add participant signing context

Add the one participant-level primitive:

```rust
pub enum ParticipantSigningContext {
    Direct { private_key_base64: String, participant_id: String },
    Delegated { proxy_private_key_base64: String, proof: DelegationProof },
}
```

Then make capability passports and issuer-signed revocations use:

```rust
sign_as_participant(payload, &ctx)
verify_participant_signature(payload, &sig, expected_participant_id, now)
```

### 1d. Add delegated verification behavior

Update `verify_signature(now)` so that:

- direct passports verify against `issuer/participant_id`,
- proxy-signed passports first verify inline `DelegationProof`, then verify the
  artifact with `proof.proxy_key`,
- `verify_with_policy` / `verify_with_anchor_policy` receive
  `required_grant: Option<(&str, &str)>` and check it when a proof is present.

### 1e. Generalize revocation targeting

Replace the old single-target revocation shape with:

```rust
pub passport_id: Option<String>,
pub target_id: Option<String>,
```

and add:

```rust
pub fn effective_target_id(&self) -> Option<&str>;
pub fn is_delegation_revocation(&self) -> bool;
```

Then run:

```sh
cargo check -p orbiplex-node-capability
```

## Step 2 — add delegation artifact support

In `capability/src/delegation.rs`, implement:

- `KEY_DELEGATION_SCHEMA_V1`,
- `KEY_DELEGATION_ID_PREFIX = "delegation:key:"`,
- `GRANT_SIGNING_CAPABILITY`,
- `GRANT_WILDCARD`,
- `KeyDelegationPassport`,
- `KeyDelegationSignature`,
- `DelegationProof`,
- structural `validate()`,
- canonical payload builder,
- issuer signing,
- signature verification,
- grant matching.

Keep the full-passport MVP guard explicit on registration/management surfaces:

```rust
if passport.max_chain_depth > 0 {
    return Err(...);
}
```

## Step 3 — add daemon-side proxy key storage

Introduce daemon records such as:

```rust
struct ProxyKeyRecord { ... }
struct IssuedKeyDelegationRecord { ... }
```

Persist them with the same engineering style used elsewhere in daemon state:

- append-only facts or records,
- startup replay,
- checkpoint capture,
- in-memory maps rebuilt from persisted state.

Suggested runtime additions:

- `proxy_key_records`,
- `proxy_key_cache`,
- `issued_delegations`,
- `delegation_cache`.

Then run:

```sh
cargo check -p orbiplex-node-daemon
```

## Step 4 — add daemon-side issuance and verification logic

### 4a. Proxy key generation/import

Generate a new Ed25519 keypair, derive:

```text
did:key:<multibase>
key:did:key:<multibase>
```

and store the private key as:

- plaintext, or
- `ParticipantKeyEnvelope` when passphrase-protected.

### 4b. Delegation issuance

Build a `KeyDelegationPassport` from:

- operator participant identity,
- local node identity,
- proxy key did:key,
- grant list,
- expiry time.

Then sign it with the participant key.

Important: generated delegation ids should use the same prefix as the schema and
docs:

```rust
generate_trace_id(KEY_DELEGATION_ID_PREFIX.trim_end_matches(':'))
```

### 4c. Delegation-aware passport issuance

When issuing/signing a capability passport:

1. resolve the proxy key,
2. resolve a live delegation,
3. verify grant coverage for the requested capability,
4. build `DelegationProof` with `key_delegation_passport.to_proof()`,
5. sign with `ParticipantSigningContext::Delegated`,
6. embed returned `issuer_delegation`.

If there is no matching active delegation or no unlocked proxy key, fall back to
`ParticipantSigningContext::Direct` and do not set `issuer_delegation`.

### 4d. Verification

Do not make runtime verification fetch the full delegation passport. Add an
inline verifier branch that:

- verifies the proof's principal signature with `proof.principal_key`,
- checks `proof.principal_key` derives to the expected participant id,
- checks proof expiry,
- verifies the capability passport or issuer revocation with `proof.proxy_key`,
- checks the required grant at the domain-policy boundary.

## Step 5 — add Seed Directory `/key`

### 5a. Storage

Create `key_delegations` persistence keyed by `delegation_id`.

### 5b. Handlers

Add:

- `PUT /key/{delegation_id}`
- `GET /key/{delegation_id}`
- `GET /key?proxy_key=...`
- `GET /key?participant_id=...&capability=...`

### 5c. Revocation feed

Ensure revocation serialization can carry `target_id` cleanly so delegation
revocations flow through the same feed as passport revocations.

Then run:

```sh
cargo check -p orbiplex-node-seed-directory
```

## Step 6 — wire the caches and sync loop

Background sync should:

- prefetch capability passports,
- prefetch key delegations for local management/signing and operator views,
- invalidate passport cache entries on passport revocations,
- invalidate delegation cache entries on delegation revocations.

Do not couple the two caches into one structure. Their semantics are related,
but not identical.

Do not pass `DelegationCache` into remote capability passport signature
verification. A proxy-signed artifact is verified from its embedded proof.

## Step 7 — expose operator surfaces

Add daemon HTTP surfaces for:

- proxy key lifecycle,
- delegation issue/publish/revoke,
- optional schema exposure for `key-delegation.v1`.

Node UI can follow later, but the daemon contract should be stable first.

## Step 8 — final consistency sweep

Before calling the slice done, check these explicitly:

- all delegation ids use `delegation:key:...`,
- no code path still assumes `revocation.passport_id` is mandatory,
- proxy signatures embed `issuer_delegation`, and direct signatures clear it,
- canonical payload builders remove `issuer_delegation` before signing,
- required grants are checked for delegated capability passports at the same
  policy boundary that checks sovereignty/anchor,
- Seed Directory and daemon agree on `/key` payload shape,
- verification rejects `max_chain_depth > 0`,
- the docs and the code use the same field names.

## Recommended verification commands

```sh
cargo check -p orbiplex-node-capability
cargo check -p orbiplex-node-daemon
cargo check -p orbiplex-node-seed-directory
```

If the tree is not compiling after one step, stop and fix that layer before
moving upward. The delegation slice touches trust, signing, revocation, and
discovery at the same time; blurred layering here will hurt later.
