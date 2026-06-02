# Proposal 031: Participant Key Passphrase Lock

## Status

Accepted; hard-MVP implementation is present in `node`.

## Problem

Participant private keys are currently stored on disk in plaintext and loaded
into daemon memory at startup without any access control.  An attacker who
obtains a copy of the node's storage — through a stolen disk, a leaked backup,
a VM snapshot, or a misconfigured file permission — immediately holds the
private key and can impersonate the participant without restriction.

There is no mechanism that requires a human to explicitly authorise operations
that use the private key.  High-value operations such as capability passport
signing, participant creation, and identity binding are indistinguishable from
routine internal operations in terms of the protection applied to the key
material they consume.

## Scope

This proposal covers **participant private keys only**.  The node transport
identity key — used for peer-session handshake and protocol advertisement
signing — is excluded from the passphrase scheme.  That key must remain
accessible at all times for the daemon to maintain peer connectivity; locking
it would make the node unreachable.

The protected class of operations includes any daemon action that calls a
participant signing key:

- capability passport signing,
- capability passport revocation signing,
- participant creation and import,
- identity binding and attestation operations,
- any future operation that signs with participant key material.

## Security Model

### What this protects against

- **Key at rest**: an attacker who obtains a copy of the encrypted key file
  cannot use it without the passphrase.  This covers disk theft, backup
  exfiltration, VM snapshots taken when the daemon is idle, and storage
  provider access.
- **Idle memory window**: after the TTL elapses with no key usage the plaintext
  key is zeroed from RAM.  A memory dump of an idle daemon yields nothing.
- **Explicit human authorisation**: signing operations require a deliberate
  human act (passphrase entry) rather than being transparent to an attacker
  who has execution access to the node process.

### What this does not protect against

- **Active memory forensics**: during the TTL window the key is plaintext in
  RAM.  This is key-at-rest protection, not key-in-use protection.  An attacker
  with live memory-read access to the daemon process can still extract the key.
  Elimination of that class of attack requires dedicated hardware (HSM/TEE) and
  is out of scope for this proposal.
- **Passphrase brute-force at unlock**: rate limiting and exponential back-off
  mitigate this (see below), but do not eliminate it.  Passphrase quality
  remains the operator's responsibility.

### Trust boundary

The passphrase never leaves the node.  It is not transmitted to, stored by, or
recoverable from any external service.  The passphrase is an operational unlock
factor, not the participant mnemonic and not a recovery root.  Loss of the
passphrase means loss of day-to-day local unlock until the operator can recover
or re-wrap the local operational secret root through an active recovery bundle
via the Identity Recovery Service (Proposal 030).  Operators are strongly
advised to establish a recovery bundle before enabling passphrase lock.

The daemon accepts an empty passphrase as a valid input.  This still produces
an encrypted envelope on disk and therefore protects the key from casual
plaintext disclosure in storage, backups, and snapshots, but it is not a
meaningful secret and must not be treated as strong operator authentication.

## Design

### Key encryption on disk

When a participant key is locked with a passphrase the private key blob stored
on disk is replaced with an encrypted envelope.  In the current hard-MVP
implementation, the passphrase unwraps a random `operational-secret-root`; the
participant signing key is then wrapped by a domain-separated key derived from
that root:

```
{
  "schema": "participant-key-envelope.v1",
  "kdf": "operational-root-hkdf-sha256",
  "aad_profile": "participant-key-envelope-aad:v2",
  "wrap_purpose": "participant-signing-key-wrap:v1",
  "key_ref": "participant:did:key:z...",
  "salt": "<16 bytes, base64url>",
  "aead": "aes-256-gcm",
  "nonce": "<12 bytes, base64url>",
  "ciphertext": "<base64url>"
}
```

The plaintext encrypted inside the AEAD envelope is the raw 32-byte Ed25519
private key scalar.  The AAD binds the envelope schema, AAD profile, wrap
purpose and concrete key reference.  Argon2id parameters are stored on the
`operational-secret-root.v1` passphrase slot, not on the participant key
envelope.  This makes passphrase rotation a re-wrap of one operational root
rather than re-encryption of every domain secret.

Proxy signing keys use the same envelope shape with
`wrap_purpose = "proxy-key-wrap:v1"` and `key_ref` set to the proxy key id.

### In-memory key cache

After a successful passphrase entry the derived signing key is held in a
dedicated cache:

```
struct UnlockedKey {
    signing_key: SigningKey,   // ZeroizeOnDrop
    last_used_at: Instant,
}

Arc<Mutex<Option<UnlockedKey>>>
```

A background task wakes every 60 seconds and evicts the entry if
`last_used_at.elapsed() > TTL`.  The TTL default is 30 minutes and is
configurable per-node.  Every access to the key via the signing path resets
`last_used_at` (sliding window).

On eviction `SigningKey` must call `Zeroize::zeroize()` before dropping.  The
`zeroize` crate's `ZeroizeOnDrop` derive covers this automatically.

### Session unlock endpoint

```
POST /v1/host/identity/session/unlock
Content-Type: application/json

{ "participant_id": "participant:did:key:z...", "passphrase": "..." }
```

The `passphrase` field may be the empty string.

The daemon treats this as the canonical user-session unlock. It first validates
the passphrase against every initialized local secret protected by the same
phrase, then commits cache updates. In the MVP this unlocks the operational
secret root, derives the participant signing/proxy/vault wrap keys from it,
populates the participant signing key and HostSigner session caches, and unlocks
the active sealer master key when a standard sealer master envelope exists.
If the sealer master uses an additional step-up secret, normal session unlock
does not bypass that factor; the sealer remains locked until the step-up secret
is supplied through the sealer unlock path.

The narrower compatibility endpoint
`POST /v1/host/identity/participant/unlock` still unlocks only the participant
signing key and HostSigner cache. New user-facing UI should prefer
`session/unlock`.

For the participant key, the daemon first unwraps `operational-secret-root.v1`
from its passphrase slot, derives the participant signing wrap key using the
envelope's `wrap_purpose`, attempts AEAD decryption of the key envelope, and on
success stores the `SigningKey` in the in-memory cache.

The response time is constant regardless of whether decryption succeeds or
fails (timing-safe response) to prevent passphrase oracle attacks.

On five consecutive failed unlock attempts within any 10-minute window the
participant key is soft-locked: further unlock attempts are rejected with
`HTTP 429` for an exponentially increasing back-off period.  The counter resets
on a successful unlock.  A hard lock (requiring daemon restart to clear) is
applied after twenty consecutive failures.

### Lock endpoint

```
POST /v1/host/identity/participant/lock
Content-Type: application/json

{ "participant_id": "participant:did:key:z..." }
```

Immediately evicts the participant signing key from the in-memory cache and
zeroes that key material.  It does not evict the `operational-secret-root`
cache by itself.  The root cache has its own explicit host endpoints:

- `POST /v1/host/identity/operational-secret-root/unlock`
- `POST /v1/host/identity/operational-secret-root/lock`

Those endpoints are useful for vault-only operations or explicit local-root
eviction.  User-facing full-session unlock should still prefer
`session/unlock`.

### Locked-operation response contract

Any daemon operation that requires a participant key checks the cache before
attempting to sign.  If the cache holds no entry for the requested participant
the operation returns immediately without touching storage:

```
HTTP 423 Locked
{
  "status": "key_locked",
  "participant_id": "participant:did:key:z...",
  "hint": "POST /v1/host/identity/session/unlock"
}
```

HTTP 423 is the stable contract.  Node UI and any middleware that calls
participant-key operations must handle it by prompting the operator for the
passphrase rather than treating it as a fatal error.

### Passphrase setup and rotation path

The same endpoint is used for first protection and passphrase rotation:

```text
POST /v1/host/identity/participant/set-passphrase
{
  "participant_id": "...",
  "passphrase": "...",
  "sealer_current_passphrase": "...",
  "sealer_step_up_secret": "..."
}
```

`sealer_current_passphrase` and `sealer_step_up_secret` are optional in the
general request shape. They are required only when the active sealer master
envelope is step-up protected and the operation must preserve that step-up
protection while rotating the shared local passphrase.

The `passphrase` field may be the empty string.  In that case the daemon still
rewraps the key into `participant-key-envelope.v1`, but the resulting envelope
should be understood as "encrypted at rest without a real shared secret",
rather than as a strong lock.

This operation reads the current participant key, creates or re-wraps the
dual-slot `operational-secret-root.v1`, writes the participant key envelope
under `participant-signing-key-wrap:v1`, and atomically replaces the stored
records.  If an active sealer master envelope exists, the daemon also re-wraps
that sealer envelope in the same file transaction.  Standard sealer envelopes
can be rotated with the new `passphrase` and a cached or verified sealer seed.
Step-up sealer envelopes require both `sealer_current_passphrase` and
`sealer_step_up_secret`, so the daemon can verify the current sealer envelope
before preserving the step-up protection under the new passphrase.

The participant key and operational secret root are immediately placed in their
in-memory caches with a fresh TTL so the operator does not have to unlock
immediately after setting or rotating the passphrase.  If any write in the
participant/root/sealer set fails, the daemon restores the previous files; the
projection cache is never treated as the source of truth.

There is no downgrade path.  An encrypted key cannot be converted back to
plaintext via the API.  A future administrative escape hatch (export of plaintext
for migration to HSM, for instance) would require a separate proposal.

### Unattended deployment

For nodes operated without a human at the console — CI infrastructure, cloud
deployments, embedded appliances — a fully interactive passphrase model is
impractical.  Two accommodation mechanisms are provided, both opt-in and
documented with explicit security trade-off warnings:

**Environment variable injection (development / low-security)**

```
ORBIPLEX_PARTICIPANT_PASSPHRASE=<value>
```

If set at startup the daemon attempts to unlock all locally stored participant
keys with the provided value before entering the `Running` phase.  The variable
is cleared from the process environment immediately after the unlock attempt.

This is equivalent to storing the passphrase next to the key on disk; it
trades key-at-rest protection for operational convenience and must never be
used in production environments where the process environment is readable by
other users or monitoring tools.

**Secrets manager integration (production)**

A future extension point `passphrase_provider` in daemon configuration will
allow delegation to an external secrets manager (HashiCorp Vault, AWS SSM
Parameter Store, etc.) at startup.  The provider interface returns a passphrase
string and is called once per locked key.  This is left for a follow-up
proposal.

## Components and Roles

### Daemon — key storage layer

- Detects whether a stored participant key is in envelope format or plaintext
  on every load.
- Performs operational-root unwrap, domain wrap-key derivation and AEAD
  encryption/decryption for the set-passphrase and unlock flows.
- Exposes the in-memory key cache as an internal service consumed by all
  signing paths.
- Manages the eviction background task and the soft/hard lock counters.

### Daemon — HTTP surface

- `POST /v1/host/identity/session/unlock` — canonical user-session passphrase
  entry; populates the participant signing key/HostSigner cache, operational
  pseudonym-vault root cache and active sealer master cache when initialized.
- `POST /v1/host/identity/participant/unlock` — compatibility passphrase entry
  for participant signing key cache population only.
- `POST /v1/host/identity/participant/lock` — explicit cache eviction.
- `POST /v1/host/identity/operational-secret-root/unlock` — narrow
  operational-root cache population for vault-only operations.
- `POST /v1/host/identity/operational-secret-root/lock` — explicit
  operational-root cache eviction.
- `POST /v1/host/identity/participant/set-passphrase` — first protection or
  passphrase rotation for participant/proxy/vault operational wraps, with
  coordinated sealer-master re-wrap when a sealer envelope exists.
- HTTP 423 on all participant-key operations when key is not in cache.

### Node UI — operator interaction

- Intercepts HTTP 423 responses from any participant-key operation.
- Presents a passphrase prompt (modal or dedicated unlock panel).
- Submits the passphrase to the session unlock endpoint and retries the original
  operation on success.
- Shows key lock status in the identity panel: locked / unlocked (expires in N
  minutes).
- Provides an explicit "Lock now" button for the operator to evict the key on
  demand.

## Workflows

### Set or rotate passphrase

1. Operator navigates to Identity settings in Node UI.
2. UI calls `POST /v1/host/identity/participant/set-passphrase` with the chosen
   passphrase.
3. Daemon creates or re-wraps the operational secret root, re-encrypts the
   participant key envelope under `participant-signing-key-wrap:v1`, and
   re-wraps the active sealer master envelope when present.
4. UI shows "Key is now passphrase-protected. Expires in 30 min."

If the chosen passphrase is empty, UI should present an explicit warning that
the key is now envelope-protected on disk but not meaningfully secret-guarded.
If the active sealer master is step-up protected, basic UI may need to route the
operator through an advanced confirmation path that supplies
`sealer_current_passphrase` and `sealer_step_up_secret`.

### Normal operation — key unlocked

1. Operator submits a capability passport signing request.
2. Daemon finds the key in cache (within TTL), resets `last_used_at`, signs.
3. Operation completes without any passphrase prompt.

### Normal operation — key locked (TTL expired or first use)

1. Operator submits a capability passport signing request.
2. Daemon returns HTTP 423 `key_locked`.
3. Node UI intercepts 423, shows passphrase prompt.
4. Operator enters passphrase; UI calls `POST /v1/host/identity/session/unlock`.
5. Daemon decrypts key, caches it, returns 200.
6. UI retries the original operation — succeeds.

### Explicit lock

1. Operator clicks "Lock key" in identity panel.
2. UI calls `POST .../lock`.
3. Daemon zeroes the participant signing-key cache entry immediately.
4. Status indicator switches to "Locked".  If the operator also wants to evict
   vault operational material, UI should call the separate
   `operational-secret-root/lock` endpoint.

## Relationship to Proposal 030 (Identity Recovery Service)

The two proposals are complementary.  Proposal 030 addresses *loss* of access
(hardware failure, forgotten credentials); this proposal addresses *compromise*
of access (attacker obtains key material).

The interaction point is the migration warning: operators enabling passphrase
lock should be prompted to verify that they have an active Proposal 030 backup
bundle, since loss of a passphrase with no recovery bundle is irrecoverable.
Node UI should surface this recommendation during the `set-passphrase` flow.

## Known Limitations (MVP)

- **Single operational passphrase per local participant context**: the
  participant signing key, proxy keys and pseudonym-vault operational wraps
  share one operational root.  The sealer master remains a deliberately
  separate tier and may additionally require a step-up secret.
- **Empty passphrase is allowed**: this improves "not stored as plaintext"
  hygiene but does not provide strong operator authentication.  Deployments
  that care about resistance to offline guessing must use a non-empty,
  high-entropy passphrase.
- **Sealer recovery model still separate**: the operational root has a recovery
  slot; sealer master recovery remains a separate hardening decision because
  the sealer is intentionally not derived from the operational root.
- **No hardware binding**: the key envelope is not tied to any TPM or secure
  enclave.  An attacker who obtains the envelope file and brute-forces the
  passphrase (offline) succeeds.  Argon2id parameters are tuned to make this
  expensive; hardware binding remains a post-MVP hardening option.
- **Node transport key excluded**: as stated in Scope, the peer handshake key
  is not covered.  An attacker with disk access and no passphrase can still
  impersonate the node at the transport layer, but cannot sign as any
  participant.

## Post-MVP

- Hardware binding via TPM `seal/unseal` on the key envelope.
- External secrets manager integration for unattended deployments.
- Passphrase-derived key hierarchy allowing multiple participants under a single
  unlock gesture.
- Audit log: every unlock, lock, and signing event recorded to the commit log
  with timestamp and operation context.
