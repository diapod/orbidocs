# Identity Recovery Service

A node operator may lose access to the node's identity and the operator's own
identity — through hardware failure, lost storage, or forgotten credentials.
Without a recovery path this is permanent.

A future recovery service would let a participant export an encrypted bundle of
all node and operator identities (including their private keys, except the
bundle-encryption key itself) and later restore them through a trusted channel.

For OTP-based recovery the service must also persist the delivery target
(e-mail address or phone number).  Without that field the service can store the
ciphertext but cannot initiate the challenge flow later.

## What the bundle contains

- node identity and its private key,
- all operator identities and their private keys.

The bundle-encryption key is not included in the bundle — it is the key that
seals the bundle and must arrive through a separate recovery path.

## Recovery paths (MVP)

### Mnemonic

The bundle is encrypted with the participant's public key.  The corresponding
private key is derived deterministically from a BIP39 mnemonic phrase given to
the user at backup time.  The recovery service stores only the ciphertext — it
has no role in the cryptographic model and cannot decrypt under any
circumstances.

Recovery: user provides the mnemonic → derives private key → decrypts bundle.

The recovery service is a pure vault here: it provides storage and an
authenticity signature, nothing more.

### SMS or e-mail with Shamir's Secret Sharing (2-of-3)

A random 256-bit data encryption key (DEK) is generated, used to encrypt the
bundle, and then split into three shares using Shamir's Secret Sharing at a
2-of-3 threshold:

- **share_1** — derived from the one-time code delivered to the user via SMS or
  e-mail at recovery time.  The recovery service never sees the code itself.
- **share_2** — held by the recovery service, stored in an HSM associated with
  the participant's public key.  The HSM enforces a per-participant rate limit
  and lockout after N failed attempts, making offline brute force impractical.
- **share_3** — reserved for post-MVP local backup (see below).

Recovery: user authenticates via SMS or e-mail → service's HSM releases a
DEK wrapper bound to the OTP-derived key material → the client combines the
received code with the returned wrap material → DEK is reconstructed → bundle
is decrypted.

**Why SSS eliminates the SPOF:** the recovery service holds only share_2.
Without share_1 — which only arrives through the SMS or e-mail channel at
recovery time — share_2 is useless.  Conversely, an attacker who intercepts
the SMS or e-mail code has only share_1, which is equally useless without
share_2.  The service and the channel must be simultaneously compromised for
the bundle to be at risk.

**Attestation constraint:** the SMS path requires that the participant's
attestation level is at most phone-confirmed.  The e-mail path requires at most
e-mail-confirmed.  A more strongly attested participant should use the mnemonic
path.  This prevents downgrading security by pairing a strong identity with a
weak recovery mechanism.

## Organisational seal

The recovery service is operated under an umbrella organisation.  At backup
time the organisation signs the metadata tuple `{participant_id,
hash(ciphertext), timestamp}` with its own key.  This signature:

- provides an authenticity and registration timestamp,
- is stored alongside the bundle,
- does not participate in the encryption model — the organisation's key is never
  used to encrypt or decrypt anything.

The seal gives the service authority to attest that a backup was registered and
when, without granting it any cryptographic power over the bundle contents.

## Post-MVP extensions

**share_3 — local backup.**  The third SSS share is given to the user at backup
time and stored locally (e.g. in a password manager or printed QR code).  With
share_3 available, the user can reconstruct the DEK together with either
share_1 or share_2 alone, making recovery possible even if the service is
temporarily unreachable.

**Federated fallback.**  Multiple service nodes operated under the umbrella
organisation each hold a copy of `Encrypt(org_pubkey, share_2)`.  A quorum
(e.g. 2-of-3 nodes) must agree before share_2 is released.  This provides
geographic and organisational redundancy without weakening the cryptographic
model.

## Open questions

- Key ceremony for the organisation's signing key: HSM, threshold signing, or
  multi-party ceremony?
- Retention policy: how long does the service keep bundles for inactive
  participants?
- Revocation: can a participant invalidate an old bundle after re-keying?

Promote to: requirements document and proposal when identity lifecycle
(issuance, rotation, revocation) is designed.
