# Proposal 037: Generic Signing Service

Based on:
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`
- `doc/project/40-proposals/036-memarium.md`

## Status

Draft

## Date

2026-04-14

## Executive Summary

Orbiplex today signs multiple kinds of artifacts — capability passports, key
delegations, capability revocations, and (in proposal 035) Agora records — each
through an ad-hoc code path that independently reaches into key storage, applies
its own canonicalization, and calls `ed25519_dalek::SigningKey::sign()` directly.
As new signed artifact families appear (Memarium archival packages, node
advertisements beyond transport, future federated contracts), this pattern
duplicates key-access logic, bypasses shared policy, fragments audit, and
couples every artifact crate to the low-level signing primitive.

This proposal introduces a **generic signing service** as an explicit stratum
between key storage and artifact-specific logic. The service is defined by a
Rust trait (`HostSigner`) and exposed over local HTTP under the node
daemon's host-capability namespace (`/v1/host/capabilities/signer.*`).
Both surfaces delegate to a single `SignerEngine` which owns key access,
passphrase unlock (reusing proposal 031), proxy key selection (reusing
proposal 032), domain separation, policy, and audit.

The service **knows nothing about any specific artifact type**. Artifact-aware
crates (`agora-core`, `capability`, future `memarium-core`, …) own their own
canonicalization in thin adapter modules that call the signer. The same signing
path is used by in-process Rust callers (zero-copy, zero-HTTP) and by
out-of-process modules in any language (Python, shell, other runtimes) that
can make a local HTTP call.

Key decisions:

1. **Strict stratification**: `signer-core` (trait + types) ← `signer-service`
   (engine) ← `signer-http` (HTTP surface). None of these crates import or
   reference any artifact crate.
2. **Two-tier surface, optional high tier**: low-tier endpoint signs arbitrary
   bytes under a domain tag; high-tier endpoints are per-artifact convenience
   handlers that live in artifact crates (not in the signer), each a thin
   adapter over the low tier.
3. **Single engine, two callers**: in-process Rust callers use the trait;
   external modules use HTTP. Both share the same unlock cache, policy, and
   audit stream.
4. **Domain separation is mandatory**: every signature is produced over a
   domain-tagged payload, so a signature valid in one artifact family cannot
   accidentally be valid in another.
5. **Reuse, don't duplicate**: the envelope format, unlock cache, and proxy
   key store from proposals 031 and 032 are the substrate. The generic signer
   is the unifying interface over them.

## Context and Problem Statement

### Current state

- `capability/src/signing.rs` — `sign_as_participant()` signs capability passports
  by loading the participant signing key from storage and calling
  `SigningKey::sign()` directly.
- `agora-core/src/signature.rs` — `sign_record_with_signing_key()` accepts a
  `SigningKey` and signs an Agora record over canonical JSON with some fields
  excluded.
- Both paths independently implement key loading, canonical payload
  construction, and signature emission.
- Proposal 031 defines passphrase lock but its unlock/lock endpoints target
  `participant` specifically (`POST /v1/host/identity/participant/unlock`).
- Proposal 032 defines proxy keys but routing a signature to a proxy key rather
  than a participant key is buried inside the capability passport issuance
  flow; no generic "sign with this key_ref" surface exists.
- External modules in non-Rust languages have no way to sign as a participant
  at all — node-ui and every middleware module either skips signing or forwards
  pre-signed payloads supplied by the operator.

### Problems

1. **Key-access duplication**: every new signed artifact family adds another
   copy of "load key → maybe unlock → sign bytes". Changes to unlock, proxy
   routing, or audit must be replicated in each location.
2. **No domain separation**: the payload that goes into `SigningKey::sign()`
   differs by artifact type but is not explicitly tagged. A canonical payload
   constructed to match one family's shape could, in principle, be rehashed
   into another. This is a latent cross-protocol replay risk.
3. **No external access**: modules written in Python or other runtimes cannot
   sign as the participant. They must either ship key material into the module
   (unsafe) or accept pre-signed payloads (inflexible). The agora-verifier
   middleware already demonstrates the verify-side of this gap; the sign-side
   is entirely absent.
4. **Policy is per-flow**: "who can sign what in which domain" is implicit in
   each flow's code rather than declared. A future module with signing intent
   must either get a dedicated capability or rediscover the rules.
5. **Audit is fragmented**: each flow emits its own (or no) trace entry. There
   is no uniform record of "what was signed, by which key, for which caller,
   when".

### What is not the problem

- Key storage, envelope encryption, unlock cache, and proxy key schema are
  fully covered by proposals 031 and 032. This proposal does not redesign any
  of that.
- Artifact canonicalization is correctly domain-specific. Each artifact crate
  knows best what its canonical form is. The generic signer must not try to
  canonicalize anything.
- Signature verification is artifact-specific and already works. This proposal
  is about the signing side only.

## Scope

In scope:

- `signer-core` crate: `HostSigner` trait, request/response types, `KeyRef`,
  `DomainTag`, error taxonomy.
- `signer-service` crate: `SignerEngine` implementation that composes existing
  key storage (031), proxy key store (032), and unlock cache into the trait.
- `signer-http` crate: framework-neutral handlers for `signer.sign`,
  `signer.unlock`, `signer.lock`, and `signer.status`, mounted by the daemon
  under `/v1/host/capabilities/signer.*`.
- Domain-separated signing wrap: how the engine binds signatures to a domain
  tag that cannot collide with another family's canonical payload.
- Policy and authorization model for "which caller may sign in which domain".
- Uniform audit log of signing events.
- Migration guidance for existing direct-signing flows (passport, Agora record)
  to delegate through the engine without breaking wire format compatibility.

Out of scope:

- Canonical payload construction for any specific artifact (lives in that
  artifact's crate, as a separate thin adapter — called out but not specified
  here beyond illustrative examples).
- New artifact families. The Memarium archival package, advertisement
  extensions, and similar are covered by their own proposals; this one only
  shows how they would plug into the signer.
- Hardware-backed keys (HSM/TEE). The engine is designed so a future
  `KeyBackend` trait implementation can add that without API changes, but no
  hardware support is specified here.
- Verification. Entirely artifact-specific, covered by the relevant artifact's
  verifier.

## Architecture: stratified surfaces

```
┌────────────────────────────────────────────────────────────────┐
│ L0 — Key Storage (existing)                                    │
│   identity/participant key (plaintext or envelope, prop 031)   │
│   proxy keys (envelope, prop 032)                              │
│   node transport key (out of scope for this signer)            │
└────────────────────────────────────────────────────────────────┘
                              ↑  KeyBackend trait (in signer-service)
┌────────────────────────────────────────────────────────────────┐
│ L1 — SignerEngine (new, in signer-service)                     │
│   • resolves KeyRef → backing key                              │
│   • applies domain separation wrap                             │
│   • enforces caller/domain policy                              │
│   • manages unlock cache (delegates to 031's envelope format)  │
│   • emits uniform audit events                                 │
└────────────────────────────────────────────────────────────────┘
          ↑                                                  ↑
          │ trait HostSigner                                 │ HTTP
          │ (in signer-core)                                 │ (in signer-http)
          │                                                  │
┌─────────┴─────────────────────┐              ┌────────────┴──────────────────┐
│ L2 — In-process artifact      │              │ L2 — External module callers  │
│ adapters (each in its own     │              │ (any language, over local     │
│ artifact crate; zero coupling │              │ HTTP; thin client library     │
│ to signer internals):         │              │ per runtime)                  │
│                               │              │                               │
│ agora-core/sign_adapter.rs    │              │ middleware-modules/lib/       │
│ capability/sign_adapter.rs    │              │   host_signer.py              │
│ memarium-core/sign_adapter.rs │              │ shell: `orbiplex sign …`      │
│   (future)                    │              │                               │
└───────────────────────────────┘              └───────────────────────────────┘
          ↑                                                  ↑
          │                                                  │
┌─────────┴─────────────────────┐              ┌────────────┴──────────────────┐
│ L3 — In-process callers       │              │ L3 — External callers         │
│   • daemon passport issuance  │              │   • agora-verifier module     │
│   • node-ui compose flow      │              │   • future Memarium module    │
│   • node internal advertisers │              │   • operator scripts          │
└───────────────────────────────┘              └───────────────────────────────┘

Artifact-specific HTTP endpoints (optional, per artifact crate):
   agora-http exposes /v1/host/agora.record.sign       (thin; wraps agora-core adapter)
   capability-http exposes /v1/host/passport.sign      (thin; wraps capability adapter)
   memarium-http exposes /v1/host/memarium.record.sign (future; thin; wraps memarium adapter)

The signer itself exposes only (daemon mounts these under its
host-capability namespace; `signer-http` is framework-neutral handlers):
   /v1/host/capabilities/signer.sign    (arbitrary bytes, domain-tagged)
   /v1/host/capabilities/signer.unlock
   /v1/host/capabilities/signer.lock
   /v1/host/capabilities/signer.status
```

**The non-negotiable invariant**: `signer-core`, `signer-service`, and
`signer-http` depend on no artifact crate. An artifact crate never needs to be
rebuilt when the signer changes, and the signer never needs to be rebuilt when
an artifact is added or changed.

## Design

### `signer-core` crate

Contains only request/response types, error taxonomy, key/domain vocabulary,
and the synchronous trait. Zero I/O and no async runtime dependency. Signing
and storage mechanics live in `signer-service`; HTTP marshalling lives in
`signer-http`.

```rust
// signer-core/src/lib.rs

/// Reference to a key managed by the host.
///
/// Opaque string form: transports across process boundaries identically to its
/// in-process form.
#[derive(Clone, Debug, Eq, PartialEq, Hash, serde::Serialize, serde::Deserialize)]
#[serde(tag = "kind", rename_all = "kebab-case")]
pub enum KeyRef {
    /// The primary participant signing key (the identity anchor).
    PrimaryParticipant,
    /// A proxy key identified by its `key:did:key:...` id (see proposal 032).
    Proxy { key_id: String },
    /// A reserved form for future derived-key schemes.
    Derived { purpose: String, index: u32 },
}

/// Domain separator for the signed payload.
///
/// Semantics: the engine binds the signature to this tag so that two payloads
/// that happen to share canonical bytes in different artifact families cannot
/// produce interchangeable signatures.
///
/// Format: `"{family}.{artifact}.v{version}"`, e.g. `"agora.record.v1"`,
/// `"passport.v1"`, `"memarium.archival-package.v1"`.
///
/// A domain tag is a stable part of the signed payload; changing it invalidates
/// every pre-existing signature for that family. Bump the version component
/// rather than renaming an existing tag.
#[derive(Clone, Debug, Eq, PartialEq, Hash, serde::Serialize, serde::Deserialize)]
pub struct DomainTag(pub String);

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct SignRequest {
    pub key_ref: KeyRef,
    pub domain: DomainTag,
    /// Canonical payload bytes, as produced by the caller.
    #[serde(with = "base64url_no_pad")]
    pub payload: Vec<u8>,
    /// Optional token returned by `unlock`. `None` means "use the default
    /// session token, if any; otherwise fail with KeyLocked".
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub unlock_token: Option<UnlockToken>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct SignResponse {
    pub alg: String,                  // "ed25519" for MVP
    #[serde(with = "base64url_no_pad")]
    pub signature: Vec<u8>,
    pub key_public: String,           // multibase-encoded public key
    pub key_ref: KeyRef,              // echoed for caller convenience
    pub domain: DomainTag,            // echoed
    #[serde(with = "time::serde::rfc3339")]
    pub signed_at: time::OffsetDateTime,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct UnlockRequest {
    pub key_ref: KeyRef,
    pub passphrase: String,           // may be empty (reuse proposal 031 semantics)
    /// Optional caller-specified TTL. Engine may clamp to configured maximum.
    pub ttl_seconds: Option<u64>,
    /// Whether the resulting token should be shared across callers or scoped
    /// to this caller only. See "Unlock scoping" below.
    pub scope: UnlockScope,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum UnlockScope {
    Session,          // default; valid for any authorized caller during TTL
    PerCaller,        // valid only for the caller that issued the unlock
    SingleUse,        // valid for exactly one sign, then evicted
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct UnlockResponse {
    pub unlock_token: UnlockToken,
    #[serde(with = "time::serde::rfc3339")]
    pub expires_at: time::OffsetDateTime,
    pub ttl_seconds: u64,
    pub key_ref: KeyRef,
}

#[derive(Clone, Debug, Eq, PartialEq, Hash, serde::Serialize, serde::Deserialize)]
pub struct UnlockToken(pub String);  // opaque; random 32+ bytes, base64url

#[derive(Clone, Debug, thiserror::Error)]
pub enum SignerError {
    #[error("key not found: {0:?}")]
    KeyNotFound(KeyRef),

    #[error("key locked: {0:?}")]
    KeyLocked(KeyRef),

    #[error("key revoked: {0:?}")]
    KeyRevoked(KeyRef),

    #[error("unlock failed (wrong passphrase or corrupt envelope)")]
    UnlockFailed,

    #[error("unlock rate limited: retry after {retry_after_seconds}s")]
    UnlockRateLimited { retry_after_seconds: u64 },

    #[error("domain {domain:?} not authorized for caller {caller:?}")]
    DomainNotAuthorized { domain: DomainTag, caller: String },

    #[error("invalid key_ref: {0}")]
    InvalidKeyRef(String),

    #[error("unlock token invalid or expired")]
    InvalidUnlockToken,

    #[error("engine internal error: {0}")]
    Internal(String),
}

pub trait HostSigner: Send + Sync {
    fn sign(&self, caller: &CallerIdentity, req: SignRequest)
        -> Result<SignResponse, SignerError>;

    fn unlock(&self, caller: &CallerIdentity, req: UnlockRequest)
        -> Result<UnlockResponse, SignerError>;

    fn lock(&self, caller: &CallerIdentity, key_ref: &KeyRef)
        -> Result<(), SignerError>;

    fn status(&self, caller: &CallerIdentity, key_ref: &KeyRef)
        -> Result<KeyStatus, SignerError>;

    fn derive_shared_secret(
        &self,
        caller: &CallerIdentity,
        req: DeriveSharedSecretRequest,
    ) -> Result<DeriveSharedSecretResponse, SignerError>;
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct KeyStatus {
    pub key_ref: KeyRef,
    pub known: bool,
    pub locked: bool,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    #[serde(with = "time::serde::rfc3339::option")]
    pub expires_at: Option<time::OffsetDateTime>,
    pub key_public: Option<String>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct DeriveSharedSecretRequest {
    pub key_ref: KeyRef,
    pub domain: DomainTag,
    #[serde(with = "base64url_no_pad_array")]
    pub peer_public: [u8; 32],
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub unlock_token: Option<UnlockToken>,
}

#[derive(Clone, Debug, serde::Serialize, serde::Deserialize)]
pub struct DeriveSharedSecretResponse {
    pub alg: String, // "x25519"
    #[serde(with = "base64url_no_pad_array")]
    pub shared_secret: [u8; 32],
    pub key_public: String,
    pub key_ref: KeyRef,
    pub domain: DomainTag,
    #[serde(with = "time::serde::rfc3339")]
    pub derived_at: time::OffsetDateTime,
}

/// Identifies who is asking the engine to sign.
/// Populated from host-capability authtok on HTTP, or from in-process
/// construction context for internal callers.
#[derive(Clone, Debug)]
pub struct CallerIdentity {
    pub source: CallerSource,
    pub label: String,        // "daemon-internal", "agora-verifier", "node-ui", …
}

#[derive(Clone, Debug)]
pub enum CallerSource {
    Internal,                 // in-process Rust caller
    HttpModule { authtok_id: String },
}
```

### `signer-service` crate

Contains the engine. This is where policy, audit, and unlock cache live. The
crate itself stays artifact-agnostic: it depends on `signer-core` and
`crypto`, and receives a `KeyBackend` supplied by the daemon. The daemon-side
backend is the layer that bridges to identity storage, proposal 031 envelopes,
and proposal 032 proxy keys.

```rust
pub struct SignerEngine {
    key_backend: Arc<dyn KeyBackend>,   // abstraction over 031/032 storage
    unlock_cache: UnlockCache,          // in-memory, zeroize-on-drop
    policy: Arc<DomainPolicy>,
    audit: Arc<dyn AuditSink>,
}

impl HostSigner for SignerEngine {
    fn sign(&self, caller: &CallerIdentity, req: SignRequest)
        -> Result<SignResponse, SignerError>
    {
        self.policy.authorize(caller, &req.domain)?;              // policy gate
        let unlocked = self.unlock_cache.resolve(&req.key_ref, &req.unlock_token, caller)?;
        let bytes_to_sign = if self.config.wrap_with_domain {
            apply_domain_wrap(&req.domain, &req.payload).to_vec()
        } else {
            req.payload.clone()
        };
        let signature = unlocked.sign(&bytes_to_sign);            // ed25519
        let resp = SignResponse { /* … */ };
        self.audit.record_sign(caller, &req, &resp);
        Ok(resp)
    }
    // unlock, lock, status — similar structure
}

pub trait KeyBackend: Send + Sync {
    fn load(&self, key_ref: &KeyRef) -> Result<KeyRecord, SignerError>;
    fn public_key(&self, key_ref: &KeyRef) -> Result<String, SignerError>;
    fn is_revoked(&self, key_ref: &KeyRef) -> Result<bool, SignerError>;
}

/// Returned by KeyBackend::load.
/// Either a ready-to-use key (plaintext, not recommended outside dev),
/// or an envelope that must be unlocked via passphrase (proposal 031 format).
pub enum KeyMaterial {
    Plaintext(SigningKey),
    Envelope(Vec<u8>),
}
```

### Domain separation wrap

```
fn apply_domain_wrap(domain: &DomainTag, payload: &[u8]) -> [u8; 32] {
    // SHA-256 domain binding; result is what actually goes into Ed25519.
    // Length prefixes prevent ambiguity between domain and payload bytes.
    let mut h = Sha256::new();
    h.update(b"orbiplex-sig-v1\0");                     // scheme tag
    h.update(&(domain.0.len() as u32).to_be_bytes());
    h.update(domain.0.as_bytes());
    h.update(&(payload.len() as u64).to_be_bytes());
    h.update(payload);
    h.finalize().into()
}
```

For signatures produced with `wrap_with_domain = true`, the verifier for that
artifact family must apply the identical wrap before Ed25519 verification.
Verifiers for artifact families that predate this proposal (capability
passport direct signing, Agora record pre-037) continue to work because the
MVP engine keeps `wrap_with_domain = false` for wire compatibility. See
"Migration" below.

### Policy

Declared in daemon configuration; the engine's `DomainPolicy::authorize` is the
one and only check:

```toml
[signer.domain_policy]
# Who may sign in which domain. Keys are caller labels; values are domain globs.
# This example mirrors the daemon's MVP `default_policy()` (see
# `daemon/src/signer_integration.rs`). Configuration-driven overrides are a
# Phase 2 follow-up.

"daemon-internal"   = ["*"]                               # daemon built-in code

# The operator (control plane / node-ui) can sign anything the daemon itself
# can sign. The full list reflects every artifact family currently migrated
# onto the SignerEngine.
"operator"          = ["passport.v1",
                       "agora.record.v1",
                       "capability.revocation.v1",
                       "node.peer-handshake.v1",
                       "node.advertisement.v1",
                       "node.capability-advertisement.v1",
                       "node.peer-message.v1",
                       "node.signal-marker.v1",
                       "node.operator-acceptance.v1",
                       "recovery.envelope.v1",
                       "key-delegation.v1"]

"agora-verifier"    = []                                  # verify-only, no signing
"memarium-service"  = ["memarium.*"]                      # glob: any memarium.* domain
# Missing entries default to the deny-all policy.
```

Policy is authoritative; the signer never consults artifact crates to decide
what is allowed.

### Unlock cache (reuses proposal 031)

The envelope format, KDF parameters, AEAD, eviction semantics, and HTTP 423
contract are taken verbatim from proposal 031. This proposal adds only:

- **Generic key_ref addressing**: 031's unlock endpoint takes `participant_id`;
  the new endpoint takes `KeyRef`, which can resolve to primary participant,
  proxy, or derived. Internally `KeyRef::PrimaryParticipant` maps to the same
  physical key 031 locks.
- **Unlock scoping** (`Session` | `PerCaller` | `SingleUse`): 031 implicitly
  uses session scope. Per-caller and single-use are new options, opt-in per
  call.
- **Shared cache for in-process and HTTP callers**: one `UnlockCache` instance;
  both trait calls and HTTP calls see the same unlocked keys. An unlock done
  via `/v1/host/identity/participant/unlock` (031) remains valid for a
  subsequent `signer.sign` call for the same key.

### Audit

Every `sign`, `unlock`, `lock`, and policy rejection is recorded:

```json
{
  "event": "signer.sign",
  "ts": "2026-04-14T12:34:56.789Z",
  "caller": { "source": "http-module", "label": "agora-verifier",
              "authtok_id": "authtok-abc" },
  "key_ref": { "kind": "primary-participant" },
  "domain": "agora.record.v1",
  "payload_hash": "sha256:…",
  "result": "ok",
  "error_code": null
}
```

`payload_hash` rather than payload: the audit must not leak signed content.
The stream joins the existing `trace/*` commit-log facts, is restart-safe, and
is exportable via existing `/v1/trace/*` surfaces.

### HTTP surface (`signer-http` + daemon mount)

`signer-http` is intentionally framework-neutral: it exposes four pure
handler functions (`handle_sign`, `handle_unlock`, `handle_lock`,
`handle_status`) that take `(&dyn HostSigner, &CallerIdentity, &[u8] body)`
and return `(u16 status, String body_json)`. It does not ship a router.
The Orbiplex Node daemon mounts these handlers under its
`/v1/host/capabilities/*` host-capability surface — the same surface that
houses `capability.passport.*`, `node-operator-bindings/*`, and the other
host capabilities — rather than on a separate `/v1/host/signer.*`
namespace. All four endpoints are POST with a JSON body so the status
query can carry a typed `KeyRef` instead of trying to URL-encode the
tagged enum.

Endpoints (all host-capability authenticated by the existing
`ORBIPLEX_HOST_CAPABILITY_AUTH_HEADER` token scheme; middleware modules
present `X-Orbiplex-Module-Authtok` and the daemon resolves caller
identity to `http_module(<module_id>)`):

```
POST /v1/host/capabilities/signer.sign
  Request:  SignRequest (JSON)
  Response: 200 SignResponse | 401 invalid_unlock_token | 403 domain_not_authorized
            | 404 key_not_found | 410 key_revoked | 423 key_locked

POST /v1/host/capabilities/signer.unlock
  Request:  UnlockRequest
  Response: 200 UnlockResponse | 401 unlock_failed | 404 key_not_found
            | 429 unlock_rate_limited

POST /v1/host/capabilities/signer.lock
  Request:  { "key_ref": KeyRef }
  Response: 200

POST /v1/host/capabilities/signer.status
  Request:  { "key_ref": KeyRef }
  Response: 200 KeyStatus | 404 key_not_found
```

The 423 response body matches proposal 031's shape:

```json
{
  "status": "key_locked",
  "key_ref": { "kind": "primary-participant" },
  "hint": "POST /v1/host/capabilities/signer.unlock"
}
```

### Per-artifact convenience endpoints (not part of signer-http)

Each artifact crate that wants HTTP access for external modules exposes its own
thin handler, in its own crate, under its own route namespace:

```
agora-http:
  POST /v1/host/agora.record.sign
    Request:  AgoraRecord with record/id and record/signature absent or null
    Handler:
      1. Fill record/ts = now() and record/id = sha256(canonical).
      2. payload = agora_core::canonical_sign_payload(&record)
      3. sig = host_signer.sign(caller, SignRequest {
             key_ref: KeyRef::PrimaryParticipant,
             domain: DomainTag("agora.record.v1".into()),
             payload,
             unlock_token: req.unlock_token,
         })?
      4. record.signature = AgoraSignature { alg: sig.alg, value: sig.signature }
      5. Respond { "record": record }

capability-http:
  POST /v1/host/passport.sign           (analogous, domain: passport.v1)

memarium-http (future):
  POST /v1/host/memarium.record.sign    (analogous, domain: memarium.*.v1)
```

These are **optional**. A runtime that prefers to compute its own canonical
payload (because it wants absolute control over bytes) can always call
`/v1/host/capabilities/signer.sign` directly.

## In-process callers

Built-in daemon code uses the trait directly:

```rust
// daemon/src/lib.rs (passport issuance, excerpt)
let signer: Arc<dyn HostSigner> = host_context.signer.clone();
let caller = CallerIdentity::internal("daemon-internal");

let payload = canonicalize_passport(&unsigned)?;
let resp = signer.sign(&caller, SignRequest {
    key_ref: KeyRef::PrimaryParticipant,
    domain: DomainTag("passport.v1".into()),
    payload,
    unlock_token: None,   // use session unlock if any; 423 otherwise
})?;
let signed = attach_signature(unsigned, resp.signature);
```

No HTTP roundtrip. No JSON (de)serialization. The engine is the same
`SignerEngine` instance as the HTTP surface; policy, unlock cache, and audit
are shared.

node-ui lives in the daemon process, so its compose flow uses the trait too.
The browser → node-ui traffic still goes over HTTP (browser → node-ui), but
node-ui → signer is in-process.

## Out-of-process callers

A Python middleware module uses the existing host-capability auth scheme with
a new client library:

```python
# middleware-modules/lib/host_signer.py
class HostSigner:
    @classmethod
    def from_env(cls) -> "HostSigner":
        # Reads ORBIPLEX_HOST_CAPABILITY_BASE_URL,
        #        ORBIPLEX_HOST_CAPABILITY_AUTH_HEADER,
        #        ORBIPLEX_HOST_CAPABILITY_AUTHTOK_FILE
        ...

    def sign(self, key_ref: dict, domain: str, payload: bytes,
             unlock_token: str | None = None) -> dict:
        req = {
            "key_ref": key_ref,
            "domain": domain,
            "payload": base64url_no_pad(payload),
            "unlock_token": unlock_token,
        }
        return self._post("/v1/host/capabilities/signer.sign", req)

    def unlock(self, key_ref: dict, passphrase: str,
               ttl_seconds: int | None = None,
               scope: str = "session") -> dict:
        ...

    def lock(self, key_ref: dict) -> None:
        ...

    def status(self, key_ref: dict) -> dict:
        ...
```

For convenience, artifact-specific helpers live next to the artifact's existing
client libraries, not in `host_signer.py`:

```python
# middleware-modules/lib/agora_record_signer.py
def sign_agora_record(unsigned: dict,
                      signer: HostSigner | None = None) -> dict:
    """Submit unsigned Agora record; daemon canonicalizes + signs + returns it."""
    signer = signer or HostSigner.from_env()
    # Use the artifact-specific endpoint if available; fall back to raw.
    return signer._post("/v1/host/agora.record.sign", unsigned)["record"]
```

This keeps the `HostSigner` class free of any Agora knowledge, consistent with
the stratification invariant.

## Components and Roles

### `signer-core` crate

- Types: `KeyRef`, `DomainTag`, `SignRequest`, `SignResponse`, `UnlockRequest`,
  `UnlockResponse`, `UnlockToken`, `UnlockScope`, `KeyStatus`, `SignerError`,
  `CallerIdentity`, `CallerSource`.
- Trait: `HostSigner`.
- Constants: `SIGNATURE_SCHEME_TAG = "orbiplex-sig-v1\0"`.
- Pure helpers: `apply_domain_wrap()`.

### `signer-service` crate

- `SignerEngine` implementing `HostSigner`.
- `KeyBackend` trait; default implementation composed from existing identity
  and proxy-key storage.
- `UnlockCache` wrapping the 031 envelope format and TTL semantics.
- `DomainPolicy` loading configuration and answering authorize queries.
- `AuditSink` trait; default implementation writes to the commit log.

### `signer-http` crate

- Framework-neutral handler functions (`handle_sign`, `handle_unlock`,
  `handle_lock`, `handle_status`) that take `(&dyn HostSigner,
  &CallerIdentity, &[u8] body)` and return `(u16, String)` so any HTTP
  server can mount them. No router, no middleware — the daemon mounts the
  handlers under `/v1/host/capabilities/signer.*` and supplies the
  `CallerIdentity` from its existing authtok paths (control token →
  `operator`; `X-Orbiplex-Module-Authtok` → `http_module(<module_id>)`).
- JSON ↔ request/response type marshalling only; all real work is the trait.

### Artifact crates (no new crate per artifact; extension to existing)

- `agora-core`: new module `sign_adapter.rs` with
  `sign_agora_record_via_host(record, &dyn HostSigner)`.
- `capability`: refactor of `sign_as_participant()` to go through a
  `sign_passport_via_host(scope, &dyn HostSigner)` helper. The existing
  function remains as a shim that builds a `SignerEngine` locally during its
  call, for backward compatibility in offline tooling.
- `agora-http`, `capability-http` (or their equivalents): thin HTTP handlers
  for convenience endpoints.
- Future `memarium-core`: same pattern when the time comes.

### daemon

- Constructs one `SignerEngine` at startup, wiring the key backend, policy
  configuration, unlock cache, and audit sink.
- Passes an `Arc<dyn HostSigner>` to every internal subsystem that needs to
  sign (passport issuer, Agora service for in-process sign paths, any future
  middleware host that needs signing on behalf of a participant).
- Mounts `signer-http` routes alongside existing host-capability routes.

## Workflows

### In-process capability passport issuance (migration of existing flow)

1. Operator triggers `POST /v1/host/capabilities/capability.passport.issue`.
2. Daemon builds the unsigned passport object.
3. `capability/sign_adapter::sign_passport_via_host(unsigned, &*host_signer)`:
   - canonicalize,
   - call `host_signer.sign(internal_caller, { key_ref: primary-participant,
     domain: passport.v1, payload, unlock_token: None })`,
   - attach signature.
4. If the key is locked, signer returns `KeyLocked`; the handler returns
   HTTP 423 per proposal 031 semantics, node-ui prompts for passphrase, calls
   `signer.unlock`, retries.
5. Signed passport is stored and optionally published per proposal 025.

Wire format of the passport is unchanged.

### Out-of-process Agora record signing (new capability)

1. Middleware module (Python) constructs an unsigned Agora record (no
   `record/id`, no `record/signature`).
2. Calls `signer.sign_agora_record(unsigned_dict)` which POSTs to
   `/v1/host/agora.record.sign`.
3. `agora-http` handler canonicalizes, calls in-process `HostSigner::sign` with
   `domain = "agora.record.v1"`, attaches signature, returns full record.
4. Module POSTs the signed record to Agora HTTP API
   `/v1/agora/topics/{topic}/records`.

### Raw signing for an artifact with no convenience endpoint yet

1. Module constructs canonical payload itself (per the artifact's specification).
2. Calls `signer.sign(key_ref, domain, payload_bytes)` directly.
3. Module assembles the artifact with the returned signature.

This path is the escape hatch for new artifact families, research prototypes,
and cross-language bit-exact experimentation.

### Unlock shared across in-process and external callers

1. Operator unlocks via node-ui passphrase modal → node-ui calls
   `HostSigner::unlock` in-process.
2. Background Memarium preservation module (external, Python) wakes and wants
   to sign an archival package.
3. Its `signer.sign(...)` call succeeds without 423: the in-process unlock
   populated the shared cache with `UnlockScope::Session`, valid for any
   authorized caller during TTL.

Per-caller or single-use scope is available when the operator wants to avoid
ambient unlock across unrelated modules.

### Emergency lock

1. Operator clicks "Lock now" in node-ui.
2. node-ui calls `HostSigner::lock(PrimaryParticipant)`.
3. Engine evicts the cache entry, zeroizes memory.
4. All subsequent sign calls — in-process and HTTP — return 423 until next
   unlock.

## Migration Strategy

The goal is to migrate existing direct-signing flows without changing any wire
format, so that already-published artifacts remain valid and consuming nodes
require no upgrade.

Phase 1 — introduce the signer:

1. Land `signer-core`, `signer-service`, `signer-http` crates.
2. Wire `SignerEngine` in daemon startup.
3. Register `/v1/host/capabilities/signer.*` routes in the daemon.
4. Add `unlock_token` acceptance to existing `/v1/host/identity/participant/unlock`
   (alias pointing at the same engine) so proposal 031 clients keep working.

Phase 2 — migrate passport signing:

1. Add `capability/sign_adapter.rs`.
2. Refactor `daemon` passport issuance to call the adapter instead of
   `sign_as_participant()`.
3. Keep `sign_as_participant()` as a shim for offline tooling and tests.
4. Verify passport wire format unchanged via cross-version fixtures.

Phase 3 — introduce Agora signing:

1. Add `agora-core/sign_adapter.rs`.
2. Add `agora-http` endpoint `agora.record.sign`.
3. Wire node-ui compose flow through the adapter (P8 in Agora TODO).
4. Add `host_signer.py` and `agora_record_signer.py` for external modules.

Phase 4 — domain separation cutover (post-MVP consideration):

The domain-wrap scheme adds a versioned prefix to the signed bytes. Applying it
to passport or Agora signing **would change the wire format** (verifiers would
need to apply the same wrap). Two strategies:

- **Strategy A — parallel domain tag alongside legacy verification**: artifacts
  produced after cutover carry `"alg": "ed25519+domain-v1"`; verifiers accept
  both `ed25519` (legacy, no wrap) and `ed25519+domain-v1` (with wrap) during
  a transition window. Oldest artifact crates migrate when their verifier
  catches up.
- **Strategy B — keep legacy on legacy**: MVP domain-wrap applies only to new
  families (Memarium, future). Passport and Agora keep their existing canonical
  scheme; domain separation for them relies on the implicit separation already
  present in their respective canonical payload shapes. This preserves zero
  churn but sacrifices the cross-family separation property for those two
  families.

Recommendation: Strategy B for MVP (zero regression for existing Orbiplex
nodes), Strategy A scheduled as a follow-up hardening.

## Relationship to Prior Proposals

### Proposal 024 (Capability Passports)

Proposal 024 defines the passport artifact and its direct-signing scheme. This
proposal adds a thin adapter so that passport signing flows through the
generic engine, without changing the artifact schema or wire format.

### Proposal 031 (Participant Key Passphrase Lock)

Complementary. Proposal 031 defines the envelope, KDF, unlock cache, TTL, and
HTTP 423 contract. This proposal reuses all of that; its only addition on the
lock/unlock surface is generic `KeyRef` addressing (so the same unlock cache
serves primary participant and proxy keys) and optional unlock scoping.

The existing endpoint `POST /v1/host/identity/participant/unlock` remains
supported as an alias for `signer.unlock` with `key_ref =
PrimaryParticipant`.

### Proposal 032 (Key Delegation Passports)

Complementary. Proposal 032 defines proxy keys and delegation passports. This
proposal adds a signing surface that can address proxy keys uniformly with
participant keys via `KeyRef::Proxy { key_id }`. The choice of which key a
particular artifact's adapter uses (primary vs proxy with a matching
delegation) remains the adapter's responsibility — the engine only signs
what it is told to sign.

### Proposal 035 (Agora Topic-Addressed Record Relay)

Consumer. Agora's UI compose flow (P8 in Agora TODO) and external module
signing capability are the first external-facing use cases for the generic
signer. No Agora schema change.

### Proposal 036 (Memarium)

Consumer. Memarium's archival package, cross-space links, and crisis-cache
records will all sign through the generic signer with their own domain tags
and canonicalization adapters. This gives Memarium signing without adding
any signing code to the Memarium crate beyond a thin adapter.

## Known Limitations (MVP)

- **Software keys only**: no HSM/TEE integration. The `KeyBackend` trait
  leaves room for it.
- **Single-host policy**: `DomainPolicy` is loaded from daemon configuration at
  startup. Hot reload is not supported in MVP.
- **No signature batch endpoint**: each sign is one HTTP call. High-volume
  batch scenarios would benefit from a batch endpoint; deferred until there is
  a real batch caller.
- **Legacy wire format preserved for passport and Agora**: per migration
  Strategy B, existing families do not get the domain wrap. New families must
  opt in explicitly.
- **Audit stream shares commit log**: operationally simple but means audit
  volume contributes to commit log size. High-frequency signing workloads may
  motivate a dedicated audit store later.

## Post-MVP

- **HSM / TEE backend**: implement `KeyBackend` over a PKCS#11 or platform
  TEE API.
- **Domain-wrap cutover (Strategy A)**: migrate passport and Agora to
  domain-tagged signatures over a transition window with dual-acceptance
  verifiers.
- **Batch sign endpoint**: `POST /v1/host/capabilities/signer.sign.batch` for workloads
  that need many signatures per unlock gesture.
- **Policy hot reload**: watch the configuration file and apply changes
  without restart.
- **Sub-delegation-aware sign**: once proposal 032 post-MVP enables
  `max_chain_depth > 0`, the engine transparently attaches chained
  `DelegationProof` arrays when signing with a sub-delegated proxy key.
- **Pluggable canonicalizers**: a registration point in `signer-http` that
  lets artifact crates register convenience endpoints without each needing
  its own HTTP crate. Optional; only pursued if the per-artifact HTTP crate
  approach proves clunky.
