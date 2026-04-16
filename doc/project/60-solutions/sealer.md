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
- caller-scoped policy gating on `(caller, suite, key_ref)` through the
  daemon capability/passport dispatch path,
- audit trail for every seal and open decision,
- tombstone markers as a first-class sealed kind.

Sealer derives all symmetric key material through a `KeySource` trait. The
Node reference implementation uses a dedicated envelope-encrypted sealer
master seed, not the Signer's Ed25519 seed. The `sealer-service` layer owns
the `KeySource` composition contract, unlock cache, and envelope-unsealing
trait; the daemon owns concrete file-backed envelope storage,
Argon2id/AES-256-GCM envelope decrypt, AAD validation, rate limiting, and
the local HTTP lifecycle for `sealer.master.init` and `sealer.unlock`.

## Scope

This document defines solution-level responsibilities of the Sealer component.

It does not define:

- every concrete module layout in an implementation repository,
- group/community key distribution above the local sealer master,
- master-key rotation/rekey beyond one configured active master version,
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
- accept `key_ref: KeyRef` as a logical reference — Sealer resolves it
  through the injected `KeySource`, never loads keys itself. The current Node
  implementation reuses `signer-core::KeyRef` as shared operator vocabulary;
  proposal 038 records the future split to a sealer-owned newtype,
- accept `suite: CiphersuiteId` selecting the AEAD family and version,
- return a self-describing envelope,
- on open, verify the tag before returning any plaintext; fail with a single
  opaque `OpenFailed` error for *cryptographic* verification failures
  (tag mismatch, AAD mismatch, wrong key) — these are indistinguishable at
  the public boundary by design,
- pre-crypto dispatch and credential failures (stale revocation view, missing
  passport, denied capability) are reported by the daemon/capability-binding
  layer before engine invocation; engine-local non-cryptographic failures use
  typed variants such as `NotAuthorized`, `UnknownSuite`, or `KeySource`.

Status:

- `done` in the Node reference implementation.

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

- `done` for the default suite and registry contract in the Node reference
  implementation; optional suites remain future/feature-gated.

### Key Source Boundary

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (sealer key-use taxonomy and derivation boundary)

Responsibilities:

- define a `KeySource` trait with a single method
  `derive_symmetric(caller, key_ref, suite, key_len, info) -> SymmetricKey`
  — KDF-proximity terminology uses `info`; wire/HTTP DTOs expose the same
  bytes as `derivation_info_b64u`; audit events record only
  `derivation_info_hash` (SHA-256 of the raw bytes), never the bytes
  themselves (see proposal 038 §`info` vs. `derivation_info`),
- require implementations to be pure functions of their inputs
  (identical inputs yield identical key bytes) so that `open` can recover
  the key without storing material in the envelope,
- require zeroization-on-drop of the returned `SymmetricKey`,
- compose `Sealer` over any `Arc<dyn KeySource>` without knowledge of whether
  the source is the daemon sealer master, a test stub, or a future HSM
  adapter.

The Node reference implementation uses `SealerMasterKeySource` in
`sealer-service`. It resolves the active master through a `SealerKeyBackend`,
requires the master to be initialized and unlocked, and derives AEAD keys with
HKDF-SHA256 domain `orbiplex-sealer-aead-key:v2`, binding the authorization
tag, suite id, active master version, requested key length, and caller-provided
`info`. Signer is not on the derivation path. A daemon regression test asserts
that repeated seal/open cycles do not call `HostSigner::sign`.

Status:

- `done` in the Node reference implementation.

### Caller-Scoped Policy and Audit

Based on:
- `doc/project/40-proposals/037-host-signer-surface.md` (domain policy + audit sink)

Responsibilities:

- gate every `seal`, `open`, and `derive_aead_key` on `(caller, suite,
  key_ref)` through the daemon dispatch capability gate; the engine still has
  an injected `SealerPolicy` for in-process invariants and testability,
- record every accepted, denied, and failed operation into an injected
  `SealerAuditSink`,
- record audit events without exposing plaintext, key material, or raw AAD
  (hash AAD before logging),
- deny-by-default: missing policy entries produce a typed not-authorized
  decision, not `Allowed`.

Status:

- `partial`: engine-local policy/audit exists, and the deployed daemon
  authorizes HTTP calls through capability binding before engine invocation.

### Passport-Aware Policy (Key-Use Authorization)

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (§CallerBinding Ownership, §scope.allowed_callers and Passport Version,
  §Revocation Freshness)

In the Node daemon, Sealer HTTP calls are authorized before engine invocation
by the shared passport-aware capability verifier. It authorizes `(caller,
grant_type, key_ref)` through:

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
   fail closed before engine invocation with a revocation-stale dispatch
   denial.
6. Emit audit: `caller_label`, `caller_source_digest` (authtok digest for
   HTTP callers), `passport_id`, `passport_digest`, `grant_type`, `target`,
   `key_ref`,
   `derivation_info_hash`, `revocation_freshness`, `decision`.

Sealer itself does not parse passports. The passport-aware verifier lives in
a separate adapter documented in `capability-binding.md`; the daemon calls the
engine only after the verifier authorizes the request. Sealer stays on bytes;
passport semantics stay in the adapter.

Status:

- `done` in the Node daemon through capability-binding and real
  `RevocationViewSource` snapshots.

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

- `done` in the Node reference implementation.

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

- `done` in the Node reference implementation.

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

- `done` in the Node reference implementation.

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

Current daemon-mounted routes:

- `sealer.master.init` initializes a local envelope-encrypted sealer master
  version and is operator-only,
- `sealer.unlock` unlocks a configured local master version into the
  daemon-local cache and is operator-only,
- `sealer.seal`, `sealer.open`, and `sealer.derive-aead-key` are available to
  authorized local modules through the existing module authtok/passport path.

Missing masters fail as unavailable, locked masters fail as locked, and bad
passphrases/rate limits remain distinct lifecycle errors. These errors are
operational state, not AEAD tag detail.

Rationale: this mirrors the existing Signer split so that a module written
in Python can call the Signer and the Sealer through the same local HTTP
surface with the same authtok, and an in-process Rust consumer pays zero
serialization overhead for either.

Status:

- `done` for the listed Node daemon routes.

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

- arbitrary key generation, rotation, revocation, storage, or escrow beyond
  the local envelope-encrypted sealer master,
- group/community key distribution and rekey governance,
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
- `key_ref: KeyRef` (currently shared operator vocabulary from `signer-core`;
  proposal 038 records the future split to a sealer-owned newtype)
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
  - first-class `NotAuthorized`, `UnknownSuite`, `KeySource`, and related
    non-opaque variants for engine-local operational failures.
  - daemon/capability-binding may return dispatch denials such as
    revocation-stale before the engine is invoked.

## Host Capability Surface

Sealer exposes a local host-capability surface (`sealer.master.init`,
`sealer.unlock`, `sealer.seal`, `sealer.open`, `sealer.derive-aead-key`)
through the in-process `Sealer` trait and the daemon-mounted HTTP shim.
`sealer.master.init` and `sealer.unlock` are local operator lifecycle
operations; module callers use the seal/open/derive operations through their
own passports. This surface is intended for local modules
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

- `Sealer` trait (`seal`, `open`, `derive_aead_key`),
- `KeySource` trait (`derive_symmetric` with explicit `key_len`),
- `SealerPolicy` trait (`authorize_seal`, `authorize_open`,
  `authorize_derive_aead_key`),
- `SealerAuditSink` trait (`record`),
- `SealRequest`, `SealResponse`, `OpenRequest`, `OpenResponse`,
  `DeriveAeadKeyRequest`, `DeriveAeadKeyResponse`,
- `CiphersuiteId`, `KeyRef` (currently reused from `signer-core` in the Node
  implementation),
  `SymmetricKey` (zeroize-on-drop),
- `SealEnvelope` (parse + serialize canonical JSON v1),
- `SealKind::{Payload, Tombstone}`,
- `OpenedPayload::{Payload(bytes), Tombstoned}`,
- `SealerError` with `OpenFailed` as the single opaque variant for
  cryptographic verification failures, plus first-class `NotAuthorized`,
  `UnknownSuite`, `KeySource`, and related non-opaque variants for
  engine-local operational failures.

Does not depend on any specific AEAD crate or key source.

### `sealer-service` crate

Implements:

- `SealerEngine` — concrete `Sealer` composing
  (`Arc<dyn KeySource>`, `SealerPolicy`, `SealerAuditSink`, `SealerEngineConfig`),
- `SealerMasterKeySource` — concrete `KeySource` over a daemon-provided
  sealer master backend and unlock cache,
- `SealerKeyBackend`, `SealerEnvelopeUnsealer`, and `SealerUnlockCache` as
  sealer-owned traits/runtime helpers with the same method shape as the
  signer-side envelope pattern, but without a `sealer-service` to
  `signer-service` dependency,
- `xchacha20-poly1305@v1` suite (default, always available),
- `aes-256-gcm-siv@v1` suite (optional, feature `aes-gcm-siv`),
- OS-CSPRNG nonce generator,
- deterministic nonce generator available only under `cfg(any(test, feature = "test-determinism"))`.

Depends on: `sealer-core`, `signer-core` for shared caller/key-ref/unlock
vocabulary, `chacha20poly1305`, `hkdf`, `sha2`, `getrandom`, `base64`,
`serde_json`, `time`, `zeroize`.

### `sealer-http` crate

Framework-agnostic HTTP handlers mounted into the daemon's manual dispatch.
Each handler takes `Arc<dyn Sealer>`, a resolved `CallerIdentity`, and raw
request bytes, and returns `(status_code: u16, body_json: String)`. Follows
the same pattern as `signer-http`.

Depends on: `sealer-core`, `serde_json`, `base64`.

### Daemon-side sealer integration

The daemon owns the concrete operational backend:

- `DaemonFileBackedSealerKeyBackend` for reading and writing local master
  envelope files,
- sealer master envelope JSON shape,
- Argon2id/AES-256-GCM envelope decrypt with sealer-specific AAD
  `sealer-master:<version>`,
- unlock rate limiting and lifecycle routing,
- operator-only `sealer.master.init` / `sealer.unlock`,
- module passport authorization for `sealer.seal`, `sealer.open`, and
  `sealer.derive-aead-key`.

Layering rule: `sealer-service` owns traits and runtime composition; the daemon
owns files, paths, config, concrete envelope JSON, and daemon-private crypto
helpers. A future shared `envelope-keystore` crate should be extracted only
when a third consumer makes the duplication mechanically removable.

## Notes

Sealer is stratified below all modules that need confidentiality and above
the byte-level AEAD primitive crates. Its interface is
byte-oriented by design: callers own the semantics of what they seal, what
they bind into AAD, and how they version their own payload schemas. Sealer
owns the mechanics of AEAD, nonce, envelope, and policy gating.

The core operational invariant is that `open(seal(plaintext, aad, key_ref))`
recovers `plaintext` if and only if the caller presents the identical `aad`
bytes and the `KeySource` returns the identical `SymmetricKey` for the same
`(key_ref, suite, key_len, active_master_version, info)` inputs. Any
*cryptographic* divergence produces the same opaque `OpenFailed` error;
diagnostic detail lives in the audit sink, never in the error value. Pre-crypto
dispatch and credential failures (stale revocation view, missing passport,
denied capability) remain non-opaque operational denials by design — they do
not reveal AEAD verification detail, and hiding them behind `OpenFailed` would
only make operator diagnosis harder.

The envelope is at-rest operator-facing first (canonical JSON, base64url
binaries) for parity with the existing `ParticipantKeyEnvelope` shape. The
CBOR wire variant is explicitly deferred to a future revision; callers
encoding payloads over the protocol remain free to wrap the JSON envelope
in their own canonical payload for signing, exactly as they do today with
the existing JSON-based artifacts.

Implementation-specific decomposition, file ownership, and delivery status
belong in the concrete Node repository's implementation ledger.
