# Proposal 030: Identity Recovery Service

## Status

Draft / Under Discussion.

## Problem

A node operator who loses access to local storage — through hardware failure,
accidental deletion, or forgotten credentials — permanently loses the node
identity and all operator identities associated with that node.  There is
currently no mechanism to export, escrow, or restore those identities and their
private keys.

## Scope

The operator selects which identities and private keys to include in a backup
bundle.  The selection is explicit and UI-driven: the daemon presents every
identity whose private key is locally accessible (i.e. the operator holds or
can derive the private portion), and the operator checks which items to escrow.
The service does not enforce completeness — a partial backup is valid.

A backup bundle may contain any combination of:

- the node identity and its private key,
- one or more operator identities and their private keys.

Identities for which the private key is not accessible to the operator at
backup time (e.g. keys held in external HSMs or by other parties) are listed
but shown as non-selectable with an explanatory note.

The bundle-encryption key is never included in the bundle itself.  It arrives
through a separate recovery path described below.

## Recovery Paths (MVP)

### Mnemonic

The bundle is encrypted with a public key derived deterministically from a
BIP39 mnemonic phrase generated at backup time and shown to the operator once.
The corresponding private key is recovered by re-entering the same mnemonic.

The recovery service stores only the ciphertext.  It has no cryptographic role
and cannot decrypt the bundle under any circumstances.  The operator who loses
the mnemonic has no recovery option.

### SMS or e-mail with key escrow and OTP-based unsealing

A random 256-bit data encryption key (DEK) is generated and used to encrypt
the bundle.  The DEK is stored in the recovery service's HSM, bound to the
participant's public key.

At recovery time the operator authenticates via a one-time code sent to the
registered SMS number or e-mail address.  The HSM wraps the DEK with a key
derived from that code — `HKDF(otp_code, participant_salt)` — and returns the
wrapped DEK to the caller.  The operator's client derives the same wrapping key
from the received code and unwraps the DEK locally.  The raw DEK is never
transmitted and never visible to the service application layer.

The HSM enforces a per-participant rate limit: after N consecutive failed
unwrap attempts the escrow entry is locked and requires manual operator
intervention to restore.  This makes offline brute force impractical even
if the ciphertext is obtained.

**Trust model:** this path requires trusting the organisation operating the HSM
not to collude with an SMS or e-mail provider to obtain the OTP and perform an
unauthorised unwrap.  The organisational seal and audit log (see below) provide
operational accountability rather than cryptographic proof of non-collusion.
Cryptographic elimination of that trust assumption is left for post-MVP
hardening via Shamir's Secret Sharing (see Post-MVP section).

Implementation note: in the current MVP split the daemon does not enforce the
unseal attempt counter itself.  The daemon exposes `recovery.hsm.unseal` to the
local recovery module and trusts that the Python module checks attempt counts
and lockout state before calling it.  This is acceptable for loopback-only
deployment, but it is an explicit trust assumption and should remain
documented.

**Attestation constraint:** the SMS path is available only when the
participant's attestation level is at most phone-confirmed.  The e-mail path
requires at most e-mail-confirmed.  Pairing a strongly-attested identity with a
weaker recovery mechanism is not permitted.

## Organisational Seal

The recovery service is operated under an umbrella organisation.  At
registration the organisation signs the metadata tuple
`{participant_id, hash(ciphertext), registration_timestamp}` with its
governance key.  The signature is stored alongside the bundle and returned to
the operator as a receipt.

The seal:

- attests that a backup was registered, by whom, and when,
- is verifiable by any party holding the organisation's public key,
- has no role in encryption or decryption — the governance key is never used as
  a wrapping or encryption key.

## Components and Roles

### Daemon — `IdentityBundleExporter`

Assembles the cleartext bundle on the operator's request.

- Reads the node identity record and its private key from local secure storage.
- Reads all operator identity records and, for each, determines whether its
  private key is locally accessible.
- Returns a structured list to Node UI:
  ```
  [
    { id, kind: "node"|"operator", label, has_private_key: bool,
      key_location: "local"|"external_hsm"|"unknown" }
  ]
  ```
- Serialises the operator-selected subset into a structured, versioned bundle
  format (JSON with envelope metadata: bundle version, participant ID,
  creation timestamp, list of included identity IDs).
- Returns the cleartext bundle to Node UI; encryption happens client-side.
- Never transmits private key material over any inter-process channel in
  cleartext; bundle serialisation and encryption are performed before any
  outbound network call.

The daemon never sends private key material over the network in cleartext.
Bundle serialisation and encryption are performed within the UI process before
any outbound call is made.

### Node UI — Backup Wizard

Guides the operator through backup setup.

- Displays the list of available identities from the daemon in a checklist:
  - items with `has_private_key: true` are selectable,
  - items with `has_private_key: false` are shown greyed out with a note
    explaining that the private key is not locally accessible and cannot be
    included in the bundle.
- Requires at least one item to be selected before proceeding.
- Lets the operator select which items to include in the bundle.
- Lets the operator choose the recovery path: mnemonic or SMS/e-mail.
- Performs or orchestrates client-side encryption:
  - Mnemonic path: generates BIP39 phrase, derives keypair, encrypts bundle,
    displays mnemonic once with a confirmation gate.
  - SMS/e-mail path: generates DEK, encrypts bundle, submits ciphertext and
    participant metadata to the recovery service.
- Receives and displays the organisation's registration receipt.
- Stores the receipt locally as a reference.

Implementation note: this wizard should grow out of the existing participant
recovery/export flow already present in Node UI and daemon rather than start
from scratch.  The current `ParticipantRecoveryExportBundle` is a useful seed
for the future identity-bundle assembly path; proposal 030 mainly adds
selection of multiple identities, client-side bundle encryption and escrow
registration.

### Node UI — Recovery Wizard

Guides the operator through bundle restoration.

- Mnemonic path: accepts mnemonic input, derives private key, downloads
  ciphertext from recovery service, decrypts bundle locally, passes identities
  and keys to the daemon for import.
- SMS/e-mail path: initiates the OTP challenge with the recovery service,
  accepts the received code, requests the HSM-wrapped DEK, unwraps locally,
  decrypts bundle, passes to daemon for import.

### Recovery Service

Org-operated backend.  Stateless from the operator's perspective: it holds
escrowed material but does not initiate recovery on its own.

Endpoints:

```
POST /v1/recovery/register
     Body: { participant_id, ciphertext, recovery_path, attestation_level,
             delivery_target? }
     Response: { registration_id, org_signature, registered_at }

GET  /v1/recovery/{participant_id}/ciphertext
     Auth: valid session token
     Response: { ciphertext, registered_at, org_signature }

POST /v1/recovery/{participant_id}/challenge
     Body: { recovery_path }
     Effect: sends OTP to registered SMS or e-mail
     Response: { challenge_id, expires_at }

POST /v1/recovery/{participant_id}/unseal
     Body: { challenge_id, otp_code }
     Response: { wrapped_dek, salt, nonce }
               (the caller needs salt+nonce to derive the same wrap key and
               unwrap the DEK locally)
```

### HSM Module (within Recovery Service)

Manages DEK storage and the unsealing protocol.

- Stores DEK entries encrypted under the HSM master key, indexed by
  `participant_id`.
- Accepts `unseal(participant_id, otp_code)` requests from the service
  application layer.
- Internally: derives `wrap_key = HKDF(otp_code, stored_salt)`, computes
  `wrapped_dek = Encrypt(wrap_key, DEK)`, returns `wrapped_dek`.
- Raw DEK never leaves the HSM boundary.
- Enforces per-participant attempt counter: N failures → entry locked.
- Writes a tamper-evident audit log entry for every unseal attempt (success or
  failure).

### SMS / E-mail Gateway

Handles OTP generation and delivery.

- Generates a cryptographically random OTP (minimum 20 characters, alphanumeric
  with mixed case).
- Delivers OTP to the operator's registered channel.
- Stores `HKDF(otp_code, salt)` as a short-lived verification token (TTL:
  10 minutes); never stores the raw OTP after delivery.
- Exposes the verification interface to the HSM module only — the service
  application layer cannot retrieve or reproduce the OTP.

### Organisation Signing Service

Issues and verifies registration receipts.

- Holds the organisation's governance key in an HSM or threshold signing
  scheme.
- Signs `{participant_id, hash(ciphertext), timestamp}` on each registration.
- Exposes a public verification endpoint so operators and third parties can
  confirm receipt authenticity.

## Workflows

### Backup — Mnemonic

```
Operator → Node UI: "Back up identities"
Node UI  → Daemon:  GET /v1/identity-bundle (list of available identities+keys)
Daemon   → Node UI: cleartext bundle (selected items)
Node UI             generate BIP39 mnemonic
Node UI             derive keypair from mnemonic (BIP32)
Node UI             encrypt bundle with derived public key → ciphertext
Node UI  → RecSvc:  POST /v1/recovery/register { participant_id, ciphertext,
                      recovery_path: "mnemonic" }
RecSvc   → OrgSign: sign metadata
OrgSign  → RecSvc:  org_signature
RecSvc   → Node UI: { registration_id, org_signature }
Node UI             display mnemonic once + confirmation gate
Node UI             store receipt locally
```

### Backup — SMS / E-mail

```
Operator → Node UI: "Back up identities"
Node UI  → Daemon:  GET /v1/identity-bundle
Daemon   → Node UI: cleartext bundle
Node UI             generate DEK (256-bit random)
Node UI             encrypt bundle with DEK → ciphertext
Node UI  → RecSvc:  POST /v1/recovery/register { participant_id, ciphertext,
                      recovery_path: "sms"|"email", dek, attestation_level,
                      delivery_target }
RecSvc              check attestation_level constraint
RecSvc   → HSM:     store DEK for participant_id
RecSvc   → OrgSign: sign metadata
OrgSign  → RecSvc:  org_signature
RecSvc   → Node UI: { registration_id, org_signature }
Node UI             store receipt locally
```

Note: `dek` is transmitted to the recovery service over a mutually
authenticated TLS connection and stored exclusively within the HSM boundary
before the register call returns.  The service application layer holds the DEK
in memory only for the duration of the HSM write.

### Recovery — Mnemonic

```
Operator → Node UI: "Restore from backup"
Operator → Node UI: enter mnemonic
Node UI             derive private key from mnemonic (BIP32)
Node UI  → RecSvc:  GET /v1/recovery/{participant_id}/ciphertext
RecSvc   → Node UI: ciphertext
Node UI             decrypt bundle with derived private key
Node UI  → Daemon:  POST /v1/identity-bundle/import (selected identities+keys)
Daemon              import identities, restart affected components
```

### Recovery — SMS / E-mail

```
Operator → Node UI: "Restore from backup"
Node UI  → RecSvc:  POST /v1/recovery/{participant_id}/challenge
RecSvc   → Gateway: generate and deliver OTP
RecSvc   → Node UI: { challenge_id, expires_at }
Operator            receives OTP via SMS or e-mail
Operator → Node UI: enter OTP
Node UI  → RecSvc:  POST /v1/recovery/{participant_id}/unseal
                      { challenge_id, otp_code }
RecSvc   → HSM:     unseal(participant_id, otp_code)
HSM                 derive wrap_key = HKDF(otp_code, salt)
HSM                 wrapped_dek = Encrypt(wrap_key, DEK)
HSM      → RecSvc:  wrapped_dek + salt + nonce
RecSvc   → Node UI: { wrapped_dek, salt, nonce }
Node UI  → RecSvc:  GET /v1/recovery/{participant_id}/ciphertext
RecSvc   → Node UI: ciphertext
Node UI             derive wrap_key = HKDF(otp_code, salt) locally
Node UI             DEK = Decrypt(wrap_key, wrapped_dek)
Node UI             decrypt bundle with DEK
Node UI  → Daemon:  POST /v1/identity-bundle/import
Daemon              import identities, restart affected components
```

## Implementation as Python Middleware

The recovery service is implemented as a supervised Python middleware module
following the same pattern as Dator and Arca.  It declares itself via a
standard module report, uses `catalog.py` for all persistent storage, and
delegates security-critical cryptographic operations to the daemon through host
capabilities.

### Module responsibilities

The Python module handles orchestration, storage and delivery:

- **Vault storage** — ciphertexts, org signatures, delivery targets and registration metadata
  stored in SQLite via `catalog.py`:
  - `recovery_bundles` — one row per registered backup (participant_id,
    ciphertext, recovery_path, attestation_level, delivery_target, org_signature,
    registered_at),
  - `recovery_challenges` — active OTP challenges (challenge_id, participant_id,
    expires_at, attempts),
  - `recovery_rate_limits` — per-participant attempt counter and lockout state.
- **Attestation constraint check** — verified at registration time against the
  declared `attestation_level`; SMS path rejects levels above phone-confirmed,
  e-mail path above e-mail-confirmed.
- **OTP e-mail delivery** — stdlib `smtplib`; no external dependencies.
- **OTP SMS delivery** — configurable HTTP webhook: the operator supplies the
  URL and auth token of their chosen SMS gateway (Twilio, SMSAPI, or any
  provider).  The module calls the webhook via `urllib.request`; no gateway SDK
  is bundled.
- **Challenge/response orchestration** — TTL enforcement, attempt counting,
  lockout after N failures.
- **Registration receipt delivery** — forwards org signature received from
  daemon back to the caller.

Known MVP limitations:

- `recovery_challenges.otp_code` is currently stored in plaintext for the
  short challenge TTL window.  This keeps the MVP dependency-free and simple,
  but it means a party who reads the SQLite file during that window can recover
  the OTP.  A stronger post-MVP variant should store only a verifier such as
  `HKDF(otp_code, challenge_salt)` or similar proof-of-possession material.
- `recovery_bundles.delivery_target` is currently stored as plaintext PII
  (e-mail address or phone number).  This is acceptable for MVP and local
  deployments, but production hardening should encrypt it under participant- or
  operator-bound key material.

### Daemon host capabilities (new)

Cryptographic operations that must not be implemented in Python without audited
dependencies are delegated to the daemon via three authenticated host
capability calls.  The module calls them over the standard host-capability
surface; it does not advertise them as module-owned `host_capability_handlers`:

- `POST /v1/host/capabilities/recovery.sign`
- `POST /v1/host/capabilities/recovery.hsm.store`
- `POST /v1/host/capabilities/recovery.hsm.unseal`

**`recovery.sign`** — signs the registration metadata tuple
`{participant_id, hash(ciphertext), timestamp}` with the organisation's Ed25519
governance key held in the daemon.  Returns the detached signature.

**`recovery.hsm.store`** — receives the DEK (transmitted over the mutually
authenticated loopback connection) and stores it encrypted under the daemon's
software-HSM master key, indexed by `participant_id`.  The raw DEK is held in
daemon memory only for the duration of this call.

**`recovery.hsm.unseal`** — receives `{participant_id, otp_code}`.  Internally
derives `wrap_key = HKDF-SHA256(otp_code, stored_salt)`, computes
`wrapped_dek = AES-256-GCM-Encrypt(wrap_key, DEK)` and returns
`wrapped_dek` together with the salt and nonce required for local unwrap.  The
raw DEK and the derived `wrap_key` never leave the daemon process.  The module
passes the wrap material to the caller without being able to interpret it.

### Storage layout

```
SqliteCatalog  recovery_bundles       (catalog.py, record_id = participant_id)
SqliteCatalog  recovery_challenges    (catalog.py, record_id = challenge_id)
SqliteCatalog  recovery_rate_limits   (catalog.py, record_id = participant_id)
Daemon         software-HSM entries   (daemon secure storage, indexed by participant_id)
```

### Crypto dependency policy

The module has no external Python dependencies beyond stdlib.  All asymmetric
cryptography (Ed25519 signing, AES-GCM, HKDF) runs in the daemon via the host
capabilities above.  This is consistent with the architecture principle that
the daemon is the cryptographic trust root; it also avoids introducing
`cryptography`, `PyNaCl` or similar packages into the module's runtime without
a dedicated venv.

If a future audit concludes that inlining a minimal crypto implementation in
the module is preferable to the loopback round-trip, the `cryptography` package
should be isolated in a dedicated venv for this module and listed explicitly as
a security-reviewed dependency.  This is a deployment decision, not a protocol
change.

### Module report sketch

```json
{
  "module_name": "Orbiplex Recovery Service",
  "handles_service_types": [],
  "input_chains": [
    {
      "chain": "inbound-local",
      "local_routes": [
        { "method": "POST", "path": "recovery/register"             },
        { "method": "GET",  "path": "recovery/{participant_id}/ciphertext" },
        { "method": "POST", "path": "recovery/{participant_id}/challenge"  },
        { "method": "POST", "path": "recovery/{participant_id}/unseal"     }
      ],
      "invoke_path": "/v1/middleware/local",
      "skip_generic_chain": true
    }
  ],
  "host_capability_handlers": [
    { "capability_id": "recovery.sign",       "invoke_path": "/v1/recovery/sign"       },
    { "capability_id": "recovery.hsm.store",  "invoke_path": "/v1/recovery/hsm/store"  },
    { "capability_id": "recovery.hsm.unseal", "invoke_path": "/v1/recovery/hsm/unseal" }
  ]
}
```

## Post-MVP: Shamir's Secret Sharing Hardening

The MVP SMS/e-mail path requires trusting the organisation's HSM not to collude
with the OTP delivery channel.  Post-MVP hardening replaces the HSM-escrow
model with a strict SSS 2-of-3 split:

- **share_1** — delivered to the operator's device via SMS/e-mail at backup
  time and stored by the operator (like a second mnemonic).  The service stores
  only `H(share_1)` as a commitment; it cannot reconstruct share_1.
- **share_2** — stored in the org HSM; released after authenticated request.
- **share_3** — optional local backup given to the operator.

With this model the service can never reconstruct the DEK alone regardless of
internal collusion, because it holds only the commitment to share_1 and the
isolated share_2.

## Post-MVP: Federated Fallback

Multiple recovery nodes operated under the umbrella organisation each hold a
copy of the ciphertext and their own HSM fragment.  A quorum (e.g. 2-of-3
nodes) must agree before the wrapped DEK is returned.  This provides geographic
and organisational redundancy without weakening the cryptographic model.

## Risks and Non-Goals

**MVP trust assumption:** the SMS/e-mail + HSM path requires trusting the
organisation's HSM and its separation from the OTP gateway.  This is documented
explicitly and mitigated by the audit log and organisational accountability.
It is not a cryptographic guarantee.

**Lost mnemonic is unrecoverable.**  There is no fallback for the mnemonic path
beyond post-MVP share_3.  The operator must acknowledge this at backup time.

**Bundle staleness.**  A restored bundle reflects the state of identities at
backup time.  Keys rotated after the last backup are not present.  Operators
should re-run backup after any key rotation.

**Import side-effects.**  Importing a bundle may overwrite existing local
identities or create conflicts if the node has partially re-keyed since the
backup was made.  The import wizard must surface these conflicts explicitly
before applying changes.

**No cross-participant recovery.**  The service is scoped to one participant's
own backup.  Social recovery (trusted guardians holding shares) is out of scope.

## Consequences

Positive:

- Operators gain a recovery path without requiring external custody of
  plaintext keys.
- The mnemonic path is fully self-sovereign; the service is a passive vault.
- The SMS/e-mail path is accessible to operators who cannot reliably store a
  mnemonic, at the cost of trusting the organisation's infrastructure.
- Post-MVP SSS hardening can be introduced without changing the backup bundle
  format or the recovery UI contract.

Trade-off:

- The SMS/e-mail MVP path introduces a trust dependency on the org HSM that the
  mnemonic path does not have.
- The recovery service becomes a high-value target; its HSM and audit
  infrastructure must be treated accordingly.
