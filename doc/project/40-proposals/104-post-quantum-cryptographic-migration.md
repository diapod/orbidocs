# Proposal 104: Post-Quantum Cryptographic Migration and Algorithm Agility

Status: **Proposed (Draft)**. Date: **2026-11-28**.

Based on:

- [P014: Node Transport](014-node-transport-and-discovery-mvp.md),
  [P035: Agora Relay](035-agora-topic-addressed-record-relay.md) and
  [P037: Signing Service](037-generic-signing-service.md)
- [P038: Key Roles](038-key-roles-and-key-use-taxonomy.md) and
  [P059: Key Role Derivation](059-participant-and-nym-key-role-derivation.md)
- [S005: Sealer](../60-solutions/005-sealer/005-sealer.md),
  [S008: Agora](../60-solutions/008-agora/008-agora.md),
  [S023: Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md)
  and [S025: Contact Catalog](../60-solutions/025-contact-catalog/025-contact-catalog.md)
- External: [RFC 10024](https://www.rfc-editor.org/rfc/rfc10024) (hybrid key
  agreement for TLS 1.3), [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final)
  (ML-KEM), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) (ML-DSA),
  [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final) (SLH-DSA) and
  [NIST IR 8547](https://csrc.nist.gov/pubs/ir/8547/final)

## Executive Summary

Every public-key operation in Orbiplex uses Curve25519: X25519 for key
agreement, Ed25519 for signatures and Ristretto255 for contact PSI. The
symmetric layer uses 256-bit keys and needs no migration. A recorded ciphertext
protected by X25519 alone can be decrypted once a cryptographically relevant
quantum computer exists ("harvest now, decrypt later"). Signatures can only be
forged after such a machine exists, but long-lived identity anchors need years of
lead time.

Decision: adopt PQ/T hybrids, not pure post-quantum algorithms. Use
X25519MLKEM768 from RFC 10024 for TLS and one Orbiplex hybrid KEM,
`x25519-mlkem768@v1`, with the same component order for Orbiplex-native key
agreement. Migrate confidentiality first: TLS, then the stored formats that
third parties keep (the AD Matrix mailbox and Agora vault key wraps). Prepare
signatures, but migrate them only after composite ML-DSA profiles are
published. `node-id` and participant identifiers stay Ed25519 `did:key`; PQ
keys are bound to them by signed records.

`aws-lc-rs`, already in the Node lock file, covers TLS and ML-DSA, including
seed-based ML-DSA keys. It offers no safe seed-based ML-KEM key generation, so
RustCrypto `ml-kem` is the single ML-KEM backend (section 3). This proposal
changes no schema, capability or runtime by itself.

## Context and Problem Statement

Checked on `2026-11-28` against Node `e68457064`.

- **Fact.** TLS uses `rustls` 0.23.46. The `aws-lc-rs` provider's default
  groups contain X25519MLKEM768, placed first when the `prefer-post-quantum`
  feature is enabled, which the current workspace feature graph does. The
  `ring` provider offers no ML-KEM group.
- **Fact.** `network` installs `aws-lc-rs` as the process-default provider
  lazily, on the first peer TLS stream. `reqwest` 0.12 with `rustls-tls` uses
  the process default when one is installed and otherwise `ring`. An HTTPS
  client built before the first peer stream therefore negotiates classical
  X25519 only. No component requires a hybrid group or records the negotiated
  one.
- **Fact.** The peer session layer runs a 3DH X25519 schedule (static ×
  ephemeral in both directions plus ephemeral × ephemeral), HKDF-SHA256 with
  info `session-v1`, and ChaCha20-Poly1305. It is forward secret but classical.
- **Fact.** The AD Matrix mailbox suite `node-static-x25519+a256gcm` derives
  its AES-256-GCM key from static-static X25519 between the two node identity
  keys, with a fixed HKDF salt and info. Each node pair has one long-lived key,
  without forward secrecy. Ciphertexts persist on Matrix homeservers.
- **Fact.** Agora vault entries wrap content keys per recipient with
  `x25519-hkdf-sha256+xchacha20-poly1305` and an ephemeral sender key. Entries
  are replicated across relays.
- **Fact.** Contact PSI blinds candidate elements as Ristretto255 points.
- **Fact.** Signatures are Ed25519 with domain separation
  (`ed25519+domain-v1`). Schemas contain 240 `alg` fields; 94 schemas pin the
  value to `"const": "ed25519"`.
- **Fact.** Symmetric primitives: XChaCha20-Poly1305, ChaCha20-Poly1305 and
  AES-256-GCM with 256-bit keys; HKDF-SHA256, HMAC-SHA256 and SHA-256 digests;
  Argon2id; PBKDF2-SHA512 inside BIP39.
- **Fact.** `aws-lc-rs` 1.18.1 (in the lock file) exposes ML-KEM-768 in `kem`
  and ML-DSA-44/65/87 in `signature`, outside its `unstable` module.
- **Fact.** In that version `PqdsaKeyPair::from_seed` builds an ML-DSA key from
  a 32-byte seed. `kem::DecapsulationKey` offers only random `generate` and
  `new` over the 2,400-byte expanded key, from which it cannot return the
  encapsulation key. AWS-LC's seed-based ML-KEM generation
  (`EVP_PKEY_keygen_deterministic`, 64-byte seed, declared in an experimental
  header) is reachable only through unsafe FFI, which the workspace forbids
  (`unsafe_code = "forbid"`).
- **Fact.** RustCrypto `ml-kem` 0.3.0 provides `DecapsulationKey::from_seed`
  over the 64-byte `d || z` seed of FIPS 203 and deprecates the expanded key
  encoding. It is not in the Node lock file.

External state:

- **Fact.** FIPS 203, 204 and 205 standardize ML-KEM, ML-DSA and SLH-DSA
  (August 2024).
- **Fact.** RFC 10024 (Proposed Standard, August 2026) defines
  X25519MLKEM768, SecP256r1MLKEM768 and SecP384r1MLKEM1024 for TLS 1.3. In
  X25519MLKEM768 the ML-KEM shared secret precedes the X25519 one.
- **Fact.** NIST published the final IR 8547 on 2026-10-27. NIST's
  announcement ties it to federal deadlines of 2030 for key establishment and
  2031 for signatures on high-value systems, and to 2035 for completing the
  migration. Secondary reports state that quantum-vulnerable public-key
  algorithms are deprecated after 2030 and disallowed after 2035. P104-001
  verifies these dates against the report before any profile cites them.
- **Fact.** X-Wing (`draft-connolly-cfrg-xwing-kem`) and HPKE with ML-KEM
  (`draft-ietf-hpke-pq`) are still Internet-Drafts. Composite ML-DSA
  (`draft-ietf-lamps-pq-composite-sigs`) was in the RFC Editor queue in July
  2026.

- **Inference.** Exposure grows with how long recorded ciphertext stays
  valuable and with who can record it. Stored formats held by third parties
  come first, then live transport. Authentication can wait, but every
  signature format must already be able to name another algorithm.

## Proposed Model / Decision

### 1. Priority rules

1. **Confidentiality first.** Public-key key agreement whose output protects
   data a third party can record moves to a PQ/T hybrid now.
2. **Hybrid only in the first waves.** The classical component guards against
   young PQ implementations and cryptanalysis; the ML-KEM component guards
   against harvest-now-decrypt-later. Pure ML-KEM is a later profile.
3. **Signatures prepare, then migrate.** Formats gain algorithm agility now.
   Long-lived trust anchors move to composite signatures once the composite
   profile is published; short-lived signatures follow.
4. **Symmetric layer unchanged.** Invariant: symmetric keys are at least
   256 bits; no 128-bit key is introduced.
5. **Identity continuity.** PQ adoption never changes `node-id` or a
   participant identifier.

### 2. Migration table

Waves: `now` starts with the first slice; `next` follows once the hybrid KEM
and key bindings exist; `later` waits for the named external standard; `keep`
needs no change.

| Area / owner | Current | Exposure | Wave | Target algorithm or suite |
| --- | --- | --- | --- | --- |
| TLS carriers: peer WSS, seed directory, HTTP fetch, Room WSS / `network` | `aws-lc-rs` offers X25519MLKEM768 first; `reqwest` may fall back to `ring` (X25519 only); nothing enforced or recorded | Recordable traffic | `now` | X25519MLKEM768 (RFC 10024), required between Orbiplex nodes and offered first to external servers with an X25519 fallback; SecP256r1MLKEM768 only for a FIPS-oriented profile |
| AD Matrix mailbox / S023 | `node-static-x25519+a256gcm`: one static key per node pair, no forward secrecy | Highest: stored on homeservers | `now` | `x25519-mlkem768+a256gcm@v1`: per-message ephemeral X25519 plus ML-KEM-768 encapsulation to the recipient's bound key; forward secret |
| Agora vault key wrap / S008, P035 | `x25519-hkdf-sha256+xchacha20-poly1305`, ephemeral sender key | High: replicated across relays | `now` | `x25519-mlkem768-hkdf-sha256+xchacha20-poly1305@v1`; adds 1,088 bytes of ML-KEM ciphertext per recipient |
| Peer session layer / P014, `network` | 3DH X25519, `session-v1`, ChaCha20-Poly1305 | Medium while TLS is hybrid; end-to-end across relays | `next` | `session-v2`: the same 3DH plus one ML-KEM-768 encapsulation, both secrets and the transcript bound into HKDF-SHA256 |
| Participant, nym and routing DH roles / P059 | X25519 keys derived by HKDF purpose from the root | Depends on consumer | `next` | Additional ML-KEM-768 role keys derived from the same root under new purposes; v1 purposes remain |
| PQ key binding / P037, P014 | — | — | `now` (contract) | `pq-key-binding.v1`: the Ed25519 identity signs its ML-KEM (later ML-DSA) public keys; `node-id` unchanged |
| Long-lived signatures: identity artifacts, succession, federation root, recovery | Ed25519 | Forgery after a quantum computer; long verification lifetime | `later` | Composite ML-DSA-65 + Ed25519 (`ed25519+mldsa65@v1`) once the LAMPS composite draft is published; SLH-DSA-SHA2-128s co-signature for rare root ceremonies |
| Short-lived signatures: handshakes, receipts, admissions | Ed25519 | Low | `later` | Follow the long-lived profile; Ed25519 until then |
| TLS listener certificates | ECDSA P-256, self-signed (`rcgen` default) | Low: endpoint authentication only (P014) | `later` | ML-DSA certificates when `rustls`/`webpki` and peers support them |
| Contact PSI / S025 | Ristretto255 blinding | Medium: low-entropy inputs testable from recorded transcripts | `later` | No standardized PQ PSI or OPRF to adopt; bound transcript retention now and revisit |
| Symmetric AEAD at rest and in transit | XChaCha20-Poly1305, ChaCha20-Poly1305, AES-256-GCM, 256-bit keys | Grover leaves about 128-bit strength | `keep` | Unchanged; `aes-256-gcm-siv@v1` stays a reserved optional suite (S005) |
| KDF, MAC and hash | HKDF-SHA256, HMAC-SHA256, SHA-256, Argon2id, PBKDF2-SHA512 | Adequate | `keep` | Unchanged; SHA-384/512 only if a regulatory profile requires it |
| Mnemonic and root derivation / P059 | BIP39 → PBKDF2-SHA512 → SLIP-0010 | Symmetric seed | `keep` | Same root; PQ keys derive from it, so no new mnemonic is needed |

### 3. Hybrid KEM `x25519-mlkem768@v1`

One L0 primitive in `node:crypto`, reused by the mailbox, vault wraps and
session v2:

- Encapsulation to a recipient's X25519 public key and ML-KEM-768
  encapsulation key yields `ct = mlkem_ct || x25519_ephemeral_pub` and a 32-byte
  shared secret.
- `ss = HKDF-SHA256(salt = suite id, ikm = ss_mlkem || ss_x25519,
  info = context || ct || recipient key refs)`. The ML-KEM secret comes first,
  as in X25519MLKEM768. **Inference.** Binding `ct` and the recipient keys
  into `info` prevents recombining components across encapsulations.
- An all-zero X25519 output, a malformed ciphertext or a wrong-length key is a
  typed refusal.
- When X-Wing or HPKE with ML-KEM is published as an RFC, it becomes a new
  suite id. Existing ciphertexts stay readable under their own ids.

ML-KEM decapsulation keys live behind the signer (P037). A new `decapsulate`
operation under `DomainPolicy` mirrors `derive_shared_secret`; callers never
hold the private key.

**Backend (decided `2026-11-28`).** RustCrypto `ml-kem` is the only Orbiplex
ML-KEM implementation, for generated and derived keys alike. ML-KEM private
keys are stored and derived as 64-byte FIPS 203 seeds (`d || z`). `aws-lc-rs`
keeps TLS and ML-DSA, including `PqdsaKeyPair::from_seed`. Tests cross-check
encapsulation against `aws-lc-rs` and FIPS 203 vectors.

### 4. Algorithm agility contract

- Every ciphertext and signature format names a versioned algorithm id.
  Readers dispatch through a registry, as the Sealer `CiphersuiteId` registry
  does; an unknown id is a typed refusal, never a fallback.
- Writers emit only the current profile. Readers accept the current id plus
  listed legacy ids for a dated read-only window.
- Between Orbiplex nodes, the signed peer handshake covers each side's
  supported suites, so a stripped hybrid offer is detected. The negotiated
  TLS group and session suite appear in diagnostics.
- A machine-readable crypto inventory lists every algorithm id with its
  format, primitive, owner and wave. A test fails when a new id constant is
  missing from it.

### 5. Identity continuity

`node-id` and participant identifiers remain Ed25519 `did:key` (P014, P059). A
`pq-key-binding.v1` record, signed by the identity key, binds ML-KEM keys and
later ML-DSA keys, with its own rotation. **Inference.** A binding signed with
Ed25519 stays trustworthy after Ed25519 falls only if it was anchored earlier,
for example in a succession chain or an Agora admission receipt; P104-004
chooses the anchor. A new identity format is a separate normative decision and
is out of scope.

### 6. Scenario: sealing an AD mailbox message

```mermaid
sequenceDiagram
    participant A as Sender node
    participant D as Directory or advertisement
    participant S as Sender signer
    participant M as Matrix homeserver
    participant B as Recipient node
    A->>D: Fetch recipient pq-key-binding.v1
    A->>A: Verify binding under recipient node-id
    A->>A: Encapsulate x25519-mlkem768@v1, derive AES-256-GCM key
    A->>M: Store x25519-mlkem768+a256gcm@v1 envelope
    B->>M: Fetch envelope
    B->>S: Decapsulate under DomainPolicy (recipient's own signer)
    S-->>B: Shared secret only
    B->>B: Open AEAD; unknown suite id is refused
```

A recorded envelope now needs both X25519 and ML-KEM-768 broken, and a later
compromise of either node's static key does not open earlier messages.

## Invariants

- New writes in a `now`-wave format use the hybrid suite; a classical write
  happens only under an explicit, dated, visible legacy permission.
- Symmetric keys are at least 256 bits.
- PQ private keys never leave the signer.
- An unknown algorithm id is refused, never replaced by a default.
- PQ adoption does not change `node-id` or participant identifiers.

## Trade-offs

### Decision record

- **Options considered.** (A) Wait until 2030. (B) Pure PQ now. (C) Hybrid
  confidentiality now, signatures after published composite profiles. (D) Wait
  for X-Wing or HPKE with ML-KEM to become RFCs.
- **Decision.** (C). (A) leaves stored ciphertext exposed while the recording
  clock runs. (B) bets on young implementations without a classical floor. (D)
  delays the stored formats that matter most; versioned ids keep a later switch
  to a published hybrid KEM cheap.
- **Consequences.** Short term: larger envelopes, one new primitive, signer
  work and dual-read windows. Long term: one agility mechanism serves every
  later algorithm change.
- **ML-KEM backend (`2026-11-28`).** Options: `aws-lc-rs` alone (no safe
  seed-based generation; unsafe FFI is forbidden), two backends (`aws-lc-rs`
  for random keys, RustCrypto for derived ones), or RustCrypto `ml-kem` alone.
  Decision: RustCrypto `ml-kem` alone. One primitive keeps one implementation,
  seeds replace expanded keys at rest, and P059 derivation needs no workaround;
  the cost is one new pinned dependency.

### Further trade-offs

Sizes grow: an ML-KEM-768 encapsulation key is 1,184 bytes and a ciphertext
1,088 bytes; an X25519MLKEM768 TLS client share is 1,216 bytes. An ML-DSA-65
public key is 1,952 bytes and a signature 3,309 bytes, so signature migration
costs far more space than key agreement. `aws-lc-rs` is already present and
FIPS-oriented but is C and assembly. RustCrypto `ml-kem` is pure Rust and adds a
dependency, but it is the only safe route to seed-derived ML-KEM keys and lets
the signer store 64-byte seeds instead of 2,400-byte expanded keys. Keeping the
primitive behind `node:crypto` lets the backend change without touching
formats.

## Failure Modes and Mitigations

| Failure | Required behavior |
| --- | --- |
| ML-KEM implementation or cryptanalytic break | Hybrid keeps X25519 strength; suite id allows replacement |
| X25519 break by a quantum computer | ML-KEM component keeps recorded `now`-wave data confidential |
| Hybrid offer stripped between Orbiplex nodes | Signed supported-suite list detects it; Orbiplex-to-Orbiplex TLS refuses classical groups |
| Peer without a PQ key binding | Refuse new `now`-wave writes after the dated cutoff; before it, write v1 only under visible legacy permission |
| Binding forged after Ed25519 falls | Bindings are anchored before use; unanchored bindings are not trusted for new writes |
| Data already sealed under v1 | Cannot be fixed retroactively; re-seal where Orbiplex controls storage, expire v1 items where retention allows, state the residual exposure |
| Envelope exceeds relay or homeserver limits | Measure in P104-005/006; cap recipients per vault entry; refuse with a typed reason |
| Backend API churn | Wrapped in `node:crypto`; known-answer and negative vectors guard behavior |
| Provider initialization order selects `ring` | Provider installed at process start; production graph checked for `ring` as a TLS provider |

## Open Questions

1. **Seed-deterministic PQ keys — resolved on `2026-11-28`.** `aws-lc-rs`
   derives ML-DSA keys from seeds but not ML-KEM keys; RustCrypto `ml-kem` is
   the single ML-KEM backend (section 3 and the decision record).
2. **Distribution of PQ public keys.** Default: a separate signed binding
   record referenced from the advertisement, keeping `node-advertisement.v1`
   lean as P014 requires.
3. **Legacy cutoff.** Default: a dated cutoff after which `now`-wave formats
   refuse classical writes; before it, status shows `classical-exposure`.
4. **Mailbox AEAD.** Default: keep AES-256-GCM; switching to
   XChaCha20-Poly1305 is orthogonal and recorded in S023 if chosen.
5. **Composite signature profile.** Default: ML-DSA-65 + Ed25519 after the
   LAMPS composite draft is published, with per-family schema version bumps
   rather than a global switch.

## Next Actions

Close P104-001 and P104-002 first; they need no new format. Then build the
hybrid KEM and signer operations (P104-003, P104-004) and migrate the two
stored formats (P104-005, P104-006). Session v2 and PQ role keys follow.
Signature migration waits for its external gate.

## Implementation Recommendations

- Put `x25519-mlkem768@v1` in `node:crypto` beside the existing X25519 KDF,
  reusing its zero-output and empty-material checks; do not add a second
  crypto crate.
- Use the `aws-lc-rs` already in the lock file for TLS and ML-DSA. Add
  RustCrypto `ml-kem` as the single ML-KEM backend (section 3); pin and review
  it in P104-003.
- Extend the P037 signer with `decapsulate`, mirroring `derive_shared_secret`
  and its `DomainTag` policy, rather than giving callers key material.
- Reuse the Sealer registry pattern for suite dispatch and typed refusal.
- Pair every format change with positive, negative and cross-version vectors:
  v1 readable, v2 written, unknown refused.

## Implementation Tracker

All rows are planned. Documentary adoption is not runtime completion.

| ID | Task | Status | Depends on | Acceptance / owners |
| --- | --- | --- | --- | --- |
| P104-001 | Crypto inventory and agility baseline | todo | — | Inventory of every algorithm id with format, primitive, owner and wave; a test fails on an unlisted id constant; IR 8547 dates verified against the report; vector sources chosen. Node crypto owner |
| P104-002 | Hybrid TLS by construction | todo | — | `aws-lc-rs` installed as process provider at daemon and tool start, before any client; `reqwest` no longer falls back to `ring`; Orbiplex-to-Orbiplex TLS requires X25519MLKEM768; external servers get it first with an X25519 fallback; negotiated group in diagnostics; tests against classical-only and hybrid servers; no `ring` TLS provider in the production graph. `network` owner |
| P104-003 | Hybrid KEM primitive `x25519-mlkem768@v1` | todo | P104-001 | Combiner as in section 3; known-answer vectors plus negative cases (zero X25519 output, malformed ciphertext, wrong key length); constant-time comparisons; RustCrypto `ml-kem` pinned and reviewed as the backend behind `node:crypto`, keys stored as 64-byte seeds and cross-checked against `aws-lc-rs` encapsulation. Node crypto owner |
| P104-004 | Signer KEM operations and PQ key binding | todo | P104-003 | ML-KEM keys held by the signer; `decapsulate` under `DomainPolicy`; `pq-key-binding.v1` schema signed by the Ed25519 identity, with rotation and a chosen anchor; publication route decided (OQ2). P037 signer and identity owners |
| P104-005 | AD Matrix mailbox v2 | todo | P104-003, P104-004 | `x25519-mlkem768+a256gcm@v1` written with per-message ephemeral keys; v1 read-only for a dated window; legacy write policy applied (OQ3); size measured against homeserver limits; v1 items expired where AD controls retention. S023 owner |
| P104-006 | Agora vault key wrap v2 | todo | P104-003, P104-004 | `x25519-mlkem768-hkdf-sha256+xchacha20-poly1305@v1` per recipient; v1 read-only; recipient count capped by measured relay limits. S008 owner |
| P104-007 | Peer session v2 | todo | P104-003, P104-004 | 3DH plus ML-KEM-768 bound into HKDF with the transcript; signed supported-suite list; downgrade and mixed-version tests; v1 coexistence window dated. P014 / `network` owner |
| P104-008 | PQ participant, nym and routing role keys | todo | P104-001, P104-003 | New derivation purposes from the existing root; recovery from the mnemonic reproduces PQ keys; vectors. P059 owner |
| P104-009 | Composite signature profile | deferred | P104-001 | Starts when `draft-ietf-lamps-pq-composite-sigs` is published as an RFC; composite ML-DSA-65 + Ed25519 for long-lived artifacts, SLH-DSA co-signature for root ceremonies, per-family schema `alg` widening plan. Signer and normative owners |
| P104-010 | Contact PSI exposure bound | todo | — | Transcript retention bounded and documented; exposure recorded in S025; PQ PSI remains a research item. S025 owner |
| P104-011 | Convergence review and closeout | todo | P104-002, P104-005, P104-006, P104-007 | Inventory shows every `now`-wave row on hybrid suites; legacy windows dated and visible; residual v1 exposure stated. Node crypto owner |

P104-001 through P104-006 form the first slice. P104-009 cannot start before
its external gate, and no row claims compliance with a regulatory deadline.
