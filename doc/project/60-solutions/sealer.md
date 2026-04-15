# Orbiplex Sealer

`Orbiplex Sealer` is the local authenticated-encryption organ of an Orbiplex
Node. Its constitutional role is symmetric to the Signer: where Signer is the
authoritative source of *authenticity* (who produced this artifact), Sealer is
the authoritative source of *confidentiality* (who may read this artifact).

Sealer is an in-process Rust component compiled with the daemon, exposed
through a thin trait so that other subsystems (Memarium, Agora, Catalog,
Backup, Identity) may protect bytes without duplicating AEAD code, nonce
policy, envelope format, or algorithm registry.

## Purpose

The component is responsible for the solution-level execution path of:

- authenticated-encryption of opaque caller-supplied plaintext bytes,
- opaque authenticated associated data (AAD) binding without interpreting it,
- self-describing envelope production consumable by future node versions,
- per-operation nonce generation under a consistent policy per suite,
- versioned ciphersuite selection with a strong default and explicit opt-in
  for alternatives,
- caller-scoped policy gating on `(caller, suite, key_ref)` consistent with
  the existing Signer policy model,
- audit trail for every seal and open decision,
- tombstone markers as a first-class sealed kind.

Sealer derives all symmetric key material through a `KeySource` trait; it
never manages key storage, key generation, key rotation, or passphrase
unlocking. Those responsibilities belong to Signer (or any other implementer
of `KeySource`).

## Scope

This document defines solution-level responsibilities of the Sealer component.

It does not define:

- concrete module layout in an implementation repository,
- concrete key backend, key storage, or unlock policy (Signer's concern),
- key agreement protocols for group-wide key distribution (future work;
  a separate solution will document the group key agreement layer),
- envelope format variants beyond the canonical JSON v1 described below
  (a CBOR wire variant may be added later as an additional envelope schema
  or encoding, not as an AEAD ciphersuite),
- responsibilities owned by other components (Memarium decides what is a
  Crisis-space AAD; Sealer only binds it).

## Must Implement

### Opaque AEAD Over Byte Buffers

Based on:
- `doc/normative/40-constitution/en/CONSTITUTION.en.md` (Art. V.7 confidentiality of Crisis material)
- `doc/project/40-proposals/036-memarium.md` (space encryption requirement)

Responsibilities:

- accept `plaintext: bytes` and `aad: bytes` without interpreting either
  (caller owns canonicalization of AAD),
- accept `key_ref: SealerKeyRef` as a logical reference — Sealer resolves it
  through the injected `KeySource`, never loads keys itself
  (opaque `String` newtype owned by `sealer-core`, not re-exported from
  `signer-core`; see proposal 038 §Sealer KeyRef Type),
- accept `suite: CiphersuiteId` selecting the AEAD family and version,
- return a self-describing envelope,
- on open, verify the tag before returning any plaintext; fail with a single
  opaque `OpenFailed` error for *cryptographic* verification failures
  (tag mismatch, AAD mismatch, wrong key) — these are indistinguishable at
  the public boundary by design,
- pre-crypto policy and credential failures (stale revocation view, missing
  passport, denied by policy) produce distinct first-class error variants
  (`SealerError::RevocationStale`, `SealerError::Denied`, etc.) so that
  operators can diagnose them without weakening the confidentiality
  boundary.

Status:

- `todo`

### Ciphersuite Registry (Versioned, Configurable Default)

Based on:
- `doc/project/40-proposals/036-memarium.md` (space-specific encryption policy)

Responsibilities:

- define a registry of supported ciphersuites keyed by stable `CiphersuiteId`
  strings of the form `"<family>@v<n>"`,
- ship with a mandatory default suite `xchacha20-poly1305@v1`
  (256-bit key, 192-bit random nonce, Poly1305 tag appended to ciphertext),
- ship with an optional suite `aes-256-gcm-siv@v1` for environments preferring
  misuse-resistant AES (available behind a feature flag),
- make the default suite configurable at engine construction through
  `SealerEngineConfig::default_suite`,
- reject unknown suite ids with a typed error; never silently fall back,
- never ship deprecated suites — introducing `@v2` requires an explicit
  decision recorded in the implementation ledger.

Status:

- `todo`

### Key Source Boundary

Based on:
- `doc/project/40-proposals/037-host-signer-surface.md` (signer as authoritative key provider)

Responsibilities:

- define a `KeySource` trait with a single method
  `derive_symmetric(caller, key_ref, suite, info) -> SymmetricKey`
  — KDF-proximity terminology uses `info`; wire/HTTP DTOs expose the same
  bytes as `derivation_info_b64u`; audit events record only
  `derivation_info_hash` (SHA-256 of the raw bytes), never the bytes
  themselves (see proposal 038 §`info` vs. `derivation_info`),
- require implementations to be pure functions of their inputs
  (identical inputs yield identical key bytes) so that `open` can recover
  the key without storing material in the envelope,
- require zeroization-on-drop of the returned `SymmetricKey`,
- compose `Sealer` over any `Arc<dyn KeySource>` without knowledge of whether
  the source is a Signer, a test stub, or a future HSM adapter.

The Signer engine implements `KeySource` through a new `derive_aead_key` path
(`HKDF-SHA256(master, salt = key_ref_bytes, info = suite_id ∥ caller_hash ∥ info)`).
That adapter is defined in the Signer crate family, not here.

Status:

- `todo`

### Caller-Scoped Policy and Audit

Based on:
- `doc/project/40-proposals/037-host-signer-surface.md` (domain policy + audit sink)

Responsibilities:

- gate every `seal` and `open` on `(caller, suite, key_ref)` through an
  injected `SealerPolicy` trait,
- record every accepted, denied, and failed operation into an injected
  `SealerAuditSink`,
- record audit events without exposing plaintext, key material, or raw AAD
  (hash AAD before logging),
- deny-by-default: missing policy entries produce `Denied`, not `Allowed`.

Status:

- `todo`

### Passport-Aware Policy (Key-Use Authorization)

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (§CallerBinding Ownership, §scope.allowed_callers and Passport Version,
  §Revocation Freshness)

The default `SealerPolicy` MAY be composed with a passport-aware verifier
that authorizes `(caller, suite, key_ref)` through:

- a `CallerBinding` resolver (crate: `caller-binding`) that maps the
  incoming `CallerIdentity` to a subject key or module subject,
- a `capability-passport.v1` carrying one or more typed key-use profiles
  in `scope.profiles[]` (e.g. `sealer-access@v1`,
  `memarium-space-access@v1`, `community-key-access@v1`),
- a `RevocationView` with a configured maximum staleness `T_max`.

Verifier decision rule:

1. Resolve `CallerBinding` from `CallerIdentity`.
2. Verify passport signature, expiry, and issuer constraints.
3. OR over `scope.profiles[]`: at least one recognized profile must
   authorize the requested `(grant_type, target)`.
4. `scope.allowed_callers` (top-level scope) must contain the
   `CallerBinding` subject.
5. Effective `T_max = min(profile.max_revocation_staleness_seconds,
   local verifier T_max)`. If `now - RevocationView.checked_at > T_max`,
   fail closed with `SealerError::RevocationStale`.
6. Emit audit: `caller_label`, `caller_source_digest` (authtok digest for
   HTTP callers), `passport_id`, `passport_digest`, `grant_type`, `target`,
   `key_ref`,
   `derivation_info_hash`, `revocation_freshness`, `decision`.

Sealer itself does not parse passports. The passport-aware verifier
lives in a separate adapter documented in `capability-binding.md` and feeds
`SealerPolicy.authorize_*` with an
already-decided outcome. Sealer stays on bytes; passport semantics stay
in the adapter.

Status:

- `todo`

### Canonical JSON Envelope v1

Based on:
- operator-facing at-rest storage parity with `ParticipantKeyEnvelope` in the
  daemon (same family of concerns: readable, diff-friendly, debug-grep-able)

Responsibilities:

- serialize envelopes as canonical JSON objects with fixed key ordering and
  base64url encoding (no padding) for all binary fields,
- include at minimum: `schema`, `suite`, `key_ref`, `kind`, `nonce`,
  `ciphertext`,
- use `schema = "orbiplex.sealer.envelope.v1"` as the stable marker,
- accept only envelopes declaring this schema value; reject foreign
  `schema` values with a typed error.

Envelope shape:

```json
{
  "schema": "orbiplex.sealer.envelope.v1",
  "suite": "xchacha20-poly1305@v1",
  "key_ref": "key:community:wroclaw-mutual-aid:space:community:epoch:7:aead",
  "kind": "payload",
  "nonce": "<base64url-no-pad>",
  "ciphertext": "<base64url-no-pad>"
}
```

The AAD is **not** embedded in the envelope. Callers transport the AAD through
their own schema and pass the identical bytes to `open`. This preserves the
opaque-bytes contract and avoids coupling envelope layout to caller semantics.

Notes:

- A CBOR-serialized wire variant (`orbiplex.sealer.envelope.cbor.v1`) may be
  added later as an additional schema if on-wire size or a deterministic
  signing image become binding. It is out of scope for v1.
- Canonicality applies to envelope metadata only. `nonce` and `ciphertext`
  are inherently non-deterministic.

Status:

- `todo`

### Tombstone Sealing

Based on:
- `doc/project/40-proposals/036-memarium.md` (`ForgetPolicy::Tombstone`,
  `ForgetPolicy::Restricted`)

Responsibilities:

- support `SealKind::Tombstone` as a request variant,
- produce an envelope with `kind = "tombstone"` whose ciphertext is a sealed
  empty plaintext bound to the caller-supplied AAD,
- on `open`, return `OpenedPayload::Tombstoned` rather than zero-length
  plaintext bytes, so callers cannot confuse a tombstoned entry with a
  legitimately empty one,
- continue to require AAD match and tag verification for tombstones;
  tombstones are as tamper-evident as regular sealed payloads.

Status:

- `todo`

### Nonce Policy

Based on:
- Memarium requirement (append-only, potentially billions of entries per key)

Responsibilities:

- generate nonces with OS-provided CSPRNG through `getrandom`,
- size nonces per suite (192-bit for XChaCha20-Poly1305, 96-bit for GCM-SIV),
- never expose deterministic nonces in production; a deterministic nonce
  source is available **only** through a cfg-gated test constructor,
- never accept a caller-supplied nonce on the `seal` path.

Status:

- `todo`

### Dual Access Surface (In-Process Trait + HTTP via Daemon)

Based on:
- existing Signer pattern (`signer-core` trait + `signer-http` framework-agnostic
  handlers + daemon dispatch),
- the operational reality that some modules are compiled into the daemon
  (Rust crates, in-process agents) while others are supervised children
  written in other languages (Python, TypeScript) that reach the host
  through HTTP.

Responsibilities:

- expose the `Sealer` trait as the canonical in-process surface; in-process
  callers receive an `Arc<dyn Sealer>` from the daemon and call methods
  directly (no serialization, no network),
- expose a framework-agnostic HTTP shim that takes
  `(Arc<dyn Sealer>, CallerIdentity, request_body_bytes)` and returns
  `(status_code: u16, body_json: String)`, to be mounted by the daemon on
  its existing manual dispatch — no separate process, no new listener,
- route HTTP calls through the daemon's existing host-capability authtok
  resolution so that a supervised module's `CallerIdentity` is derived the
  same way as any other host capability caller,
- share the wire contract with the in-process trait: HTTP request bodies
  deserialize into the same semantic shape as `SealRequest`/`OpenRequest`,
  with bytes encoded as base64url-without-padding,
- map `SealerError` to stable HTTP status codes and a uniform error
  envelope `{ "status": "<code>", "reason": "<message>" }`,
- keep the HTTP shim free of HTTP-framework dependencies (no `axum`, no
  `hyper`) — the daemon adapts the `(u16, String)` outcome to its own
  dispatch format.

Rationale: this mirrors the existing Signer split so that a module written
in Python can call the Signer and the Sealer through the same local HTTP
surface with the same authtok, and an in-process Rust consumer pays zero
serialization overhead for either.

Status:

- `todo`

## May Implement

### CBOR Wire Envelope

Based on:
- future protocol-native artifacts that benefit from compactness and a
  single canonical byte image for signing or hashing

Responsibilities:

- define `orbiplex.sealer.envelope.cbor.v1` as a parallel schema with the
  same semantics as the JSON envelope,
- reuse `ciborium = "0.2"` already present in the workspace (`protocol`
  crate),
- make JSON vs. CBOR selection a caller concern at seal time through a
  separate envelope encoding selector, not through `CiphersuiteId`.

Status:

- `optional`

### Streaming Seal

Based on:
- potential use of Sealer for large archival payloads

Responsibilities:

- expose a streaming seal/open interface over a `Read`/`Write` adapter for
  payloads that do not fit comfortably in memory,
- preserve the same AAD binding and envelope-outside-of-ciphertext layout.

Status:

- `future`

## Out of Scope

- key generation, rotation, revocation, storage, or escrow
  (Signer / key backend concern),
- passphrase unlocking or unlock caching
  (Signer concern),
- key agreement for groups (Community space key distribution)
  (separate future solution),
- canonicalization of caller payloads or AAD
  (caller concern — Sealer treats both as opaque bytes),
- interpretation of `key_ref` namespacing rules
  (caller / KeySource concern),
- digital signatures
  (Signer concern; Sealer does not overlap this surface).

## Consumes

- `plaintext: bytes`
- `aad: bytes`
- `key_ref: SealerKeyRef` (opaque `String` newtype, owned by `sealer-core`)
- `suite: CiphersuiteId`
- `derivation_info: bytes` (wire/HTTP DTO field name; `info` at KDF call site)
- `CallerIdentity` (reused from `signer-core`)
- `SymmetricKey` from an injected `KeySource`

## Produces

- `SealEnvelope` (canonical JSON v1 document)
- `OpenedPayload::{Payload(bytes), Tombstoned}`
- Audit events through the injected `SealerAuditSink`, including
  `derivation_info_hash` (never the raw bytes)
- Typed error values (`SealerError`):
  - opaque `OpenFailed` for cryptographic verification failures,
  - first-class `RevocationStale`, `Denied`, `UnknownSuite`, and related
    non-opaque variants for pre-crypto policy and credential failures.

## Host Capability Surface

Sealer exposes a local host-capability surface (`sealer.seal`,
`sealer.open`) through the in-process `Sealer` trait and the
daemon-mounted HTTP shim. This surface is intended for local modules
supervised by the same daemon — in-process Rust consumers receive an
`Arc<dyn Sealer>`, and supervised children written in other languages
reach it through the daemon's existing authtok-resolved HTTP dispatch.

Sealer is NOT itself a network-advertised or federated capability. It
does not appear in `CapabilityProfile` advertisements, it does not
participate in Seed Directory capability discovery, and it does not
cross the node boundary directly.

Network-facing capabilities that rely on Sealer (e.g. `memarium.write`
with space-encryption enforcement, `memarium.read` with transparent
decryption, `agora.submit` with end-to-end encrypted payloads) are
owned by their respective host components and consume Sealer as a
lower layer.

The rationale for keeping Sealer (and its passport-aware verifier) off
the wire while passport artifacts themselves federate across nodes is
captured in `doc/project/20-memos/authorization-locality.md`.

## Crate Boundary

### `sealer-core` crate

Defines the trait boundary and domain types:

- `Sealer` trait (`seal`, `open`),
- `KeySource` trait (`derive_symmetric`),
- `SealerPolicy` trait (`authorize_seal`, `authorize_open`),
- `SealerAuditSink` trait (`record`),
- `SealRequest`, `SealResponse`, `OpenRequest`, `OpenResponse`,
- `CiphersuiteId`, `SealerKeyRef` (opaque `String` newtype owned by
  `sealer-core`, not re-exported from `signer-core`),
  `SymmetricKey` (zeroize-on-drop),
- `SealEnvelope` (parse + serialize canonical JSON v1),
- `SealKind::{Payload, Tombstone}`,
- `OpenedPayload::{Payload(bytes), Tombstoned}`,
- `SealerError` with `OpenFailed` as the single opaque variant for
  cryptographic verification failures, plus first-class `RevocationStale`,
  `Denied`, `UnknownSuite`, and related non-opaque variants for
  pre-crypto policy and credential failures.

Does not depend on any specific AEAD crate or key source.

### `sealer-service` crate

Implements:

- `SealerEngine` — concrete `Sealer` composing
  (`Arc<dyn KeySource>`, `SealerPolicy`, `SealerAuditSink`, `SealerEngineConfig`),
- `xchacha20-poly1305@v1` suite (default, always available),
- `aes-256-gcm-siv@v1` suite (optional, feature `aes-gcm-siv`),
- OS-CSPRNG nonce generator,
- deterministic nonce generator available only under `cfg(any(test, feature = "test-determinism"))`.

Depends on: `sealer-core`, `orbiplex-node-crypto` (for re-used primitives),
`chacha20poly1305`, `getrandom`, `base64`, `serde_json`, `zeroize`.

### `sealer-http` crate

Framework-agnostic HTTP handlers mounted into the daemon's manual dispatch.
Each handler takes `Arc<dyn Sealer>`, a resolved `CallerIdentity`, and raw
request bytes, and returns `(status_code: u16, body_json: String)`. Follows
the same pattern as `signer-http`.

Depends on: `sealer-core`, `serde_json`, `base64`.

### `sealer-signer-bridge` crate (future, may live in `signer-service`)

Provides `impl KeySource for SignerEngine` over the Signer's new
`derive_aead_key` surface. Kept out of `sealer-service` so that a test
deployment of Sealer does not pull in the Signer engine.

## Notes

Sealer is stratified below all modules that need confidentiality and above
the byte-level AEAD primitives in `orbiplex-node-crypto`. Its interface is
byte-oriented by design: callers own the semantics of what they seal, what
they bind into AAD, and how they version their own payload schemas. Sealer
owns the mechanics of AEAD, nonce, envelope, and policy gating.

The core operational invariant is that `open(seal(plaintext, aad, key_ref))`
recovers `plaintext` if and only if the caller presents the identical `aad`
bytes and the `KeySource` returns the identical `SymmetricKey` for the same
`(key_ref, suite, info)` triple. Any *cryptographic* divergence produces
the same opaque `OpenFailed` error; diagnostic detail lives in the audit
sink, never in the error value. Pre-crypto policy and credential failures
(stale revocation view, missing passport, denied by policy) use their own
non-opaque error variants by design — they do not reveal
confidentiality-relevant information, and hiding them behind `OpenFailed`
would only make operator diagnosis harder.

The envelope is at-rest operator-facing first (canonical JSON, base64url
binaries) for parity with the existing `ParticipantKeyEnvelope` shape. The
CBOR wire variant is explicitly deferred to a future revision; callers
encoding payloads over the protocol remain free to wrap the JSON envelope
in their own canonical payload for signing, exactly as they do today with
the existing JSON-based artifacts.

Implementation-specific decomposition, file ownership, and delivery status
belong in the concrete Node repository's implementation ledger.
