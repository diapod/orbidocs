# Participant Assurance Levels

Based on:

- `doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/20-memos/console-participant-identity-create-and-import.md`

This memo defines the assurance level model for `participant:did:key:...` subjects
in Orbiplex Node. It establishes the four-level credibility hierarchy, the
append-only verification fact contract, the sovereign operator trust anchor
pattern, and the privacy boundary that keeps PII out of the fact log.

This model is a prerequisite for downstream consumers — procurement policy,
capability access control, and federated trust presentation — that need a stable
assurance level contract to design against.

## Motivation

Not all participants are equally credible. An anonymous key with no external
verification carries different weight than a participant whose phone number has
been confirmed, or one whose government-issued identity has been attested, or one
whose public key is an explicitly pinned infrastructure trust anchor.

The assurance level is not a reputation signal — it is a structural property of
the identity binding itself: how strongly is this `participant:did:key:...`
anchored to a verifiable real-world entity?

Downstream systems — procurement eligibility, capability policy gates, federation
onboarding, escrow authorization — may require a minimum assurance level as a
precondition. That contract must be defined once, at the identity layer, rather
than reimplemented ad hoc by each consumer.

## Relationship to NIST SP 800-63 and eIDAS

This model is structurally parallel to established identity assurance frameworks,
adapted to the Orbiplex trust model.

**NIST SP 800-63-3** defines three Identity Assurance Levels:

- IAL1: claimed identity, no real-world verification required,
- IAL2: evidence-based verification, remote or in-person identity proofing,
- IAL3: in-person or supervised remote verification, physical or biometric evidence.

**eIDAS** (EU regulation 910/2014 and its 2.0 revision) defines three assurance
levels for electronic identification:

- Low: limited confidence in the claimed identity,
- Substantial: substantial confidence, typically multi-factor authentication,
- High: high confidence, multi-factor with physical presence or equivalent.

The Orbiplex assurance levels map approximately as follows:

| Orbiplex level     | NIST SP 800-63 | eIDAS          | Basis                                    |
| :----------------- | :------------- | :------------- | :--------------------------------------- |
| `Unknown`          | below IAL1     | below Low      | key exists, no binding verified          |
| `PhoneVerified`    | IAL1–IAL2      | Low–Substantial | possession factor confirmed              |
| `GovIdVerified`    | IAL2           | Substantial–High | real-world identity proofed             |
| `SovereignOperator`| above IAL3     | above High     | explicit governance trust anchor         |

The mapping is approximate. Phone verification is a possession factor (something
you have), not a full identity proofing step — so it falls between IAL1 and IAL2
depending on implementation strength. Government ID verification reaches IAL2 or
eIDAS Substantial assuming the verification method is robust; High or IAL3 would
require additional physical-presence or biometric evidence, which is out of scope
for MVP. Sovereign operator trust is an out-of-band governance designation that
sits above any verification hierarchy.

## Assurance Levels

```
SovereignOperator  >  GovIdVerified  >  PhoneVerified  >  Unknown
```

### Unknown

No verification has been performed. The participant is identified only by their
`participant:did:key:...` value. Self-declared metadata such as `nickname` or
`label` does not elevate this level.

This is the default state for every newly created or imported participant.

### PhoneVerified

The participant's phone number has been confirmed via an active verification
step (for example, SMS OTP). This establishes that the operator controlling the
participant key also controls the claimed phone number at the time of
verification.

This level does not bind the participant to a real-world legal identity. It is a
possession-factor confirmation, not an identity proofing step.

### GovIdVerified

The participant has been bound to a government-issued identity record: a country
code and a national identification number (for example, PL + PESEL, DE + personal
ID, or similar). Verification must be performed against an authoritative source or
a delegated attester.

This level provides a binding between the cryptographic participant and a
legal-identity-level real-world entity. It is the strongest level achievable
through claim verification.

### SovereignOperator

The participant's public key appears in the node's sovereign operator list — a
statically configured or compiled-in set of explicitly pinned trusted keys. This
designation is a governance decision, not a verification outcome.

Sovereign operator status is not derived from any verification fact. It overrides
the claim-based hierarchy entirely. A sovereign operator with no verified phone
or government ID still holds the highest assurance level, because the trust
anchor is the explicit key pinning, not the verification chain.

## Assurance Level as a Derived Property

The assurance level is **not stored**. It is **computed** by the projector from:

1. the set of `ParticipantVerificationFact` events for the participant,
2. the sovereign operator list from node configuration.

This ensures the level is always consistent with the current fact history and
sovereign list. If a verification is revoked, the level drops immediately on next
projection. If a participant is added to or removed from the sovereign list, the
level updates on next daemon open or configuration reload.

Pseudocode:

```
fn compute_assurance_level(participant_id, verification_facts, sovereign_list):
    if participant_id in sovereign_list:
        return SovereignOperator
    if any GovIdVerificationConfirmed and not revoked for participant_id:
        return GovIdVerified
    if any PhoneVerificationConfirmed and not revoked for participant_id:
        return PhoneVerified
    return Unknown
```

## Verification Facts

Verification events are recorded in the stream `identity/participant-verification-fact.v1`
as append-only facts. The stream follows the same pattern as
`identity/participant-fact.v1`.

**Critical constraint: raw PII must not enter the fact log.**

The fact records only the attestation event — that a verification occurred, by
whom, and when — not the data that was verified. The raw phone number and the raw
government ID number are processed at the boundary and discarded. Only a
one-way hash is retained for deduplication and audit purposes.

```
ParticipantVerificationFact
  | PhoneVerificationConfirmed
  |   participant_id: String        // participant:did:key:z...
  |   phone_hash: String            // blake3(E.164-normalized number)
  |   verified_at: String           // RFC 3339
  |   verifier_ref: String          // "sms-otp-local" | "twilio" | ...
  |
  | GovIdVerificationConfirmed
  |   participant_id: String
  |   country_code: String          // ISO 3166-1 alpha-2, e.g. "PL"
  |   id_kind: String               // "pesel" | "nip" | "passport" | ...
  |   id_hash: String               // blake3(country_code || id_number)
  |   verified_at: String
  |   verifier_ref: String
  |
  | VerificationRevoked
      participant_id: String
      claim_kind: String            // "phone" | "gov-id"
      revoked_at: String
      reason: Option<String>
```

`blake3(country_code || id_number)` allows the node to verify a presented
credential against the stored hash without retaining the raw value. The hash
should be salted per-node to prevent cross-node correlation.

## Privacy Boundary and GDPR

The append-only fact log is incompatible with GDPR Article 17 (right to
erasure) if it contains raw personal data. Storing only hashes of PII is the
primary mitigation: the log retains no data from which the original value
can be reconstructed.

If the node needs to store retrievable PII for operational reasons (for example,
to pre-fill forms or to re-present data to the operator), that data must live in
a **separate, mutable store** outside the fact log, with:

- explicit retention policy,
- operator-accessible deletion path,
- no cross-node replication by default.

The existence of such a store and its schema is outside the scope of this memo
and should be defined in a dedicated privacy or data-retention document.

Sovereign operator trust requires no PII at all. It is purely a key-pinning
designation with no personal data involved.

## Sovereign Operator List

The sovereign operator list is a node-level configuration, not a fact in the log.
It is loaded at `Daemon::open()` alongside the fact history and passed into the
assurance level computation as an external parameter.

Recommended form in the node daemon TOML:

```toml
[identity]
sovereign_operators = [
    "participant:did:key:z6Mk...",
]
```

For keys whose trust is protocol-level rather than deployment-level (for example,
a designated Orbiplex Foundation infrastructure participant), the list may be
compiled into the binary as a compile-time constant. That decision is a
governance call, not an implementation detail.

The sovereign operator list must be treated as a security-sensitive
configuration artifact. Changes to it should be auditable at the deployment
level, equivalent to changing a TLS trust anchor.

## Downstream Consumers

The assurance level is a contract that the `identity` crate exposes for
consumption by other subsystems. Anticipated consumers include:

- **procurement policy** — minimum assurance level required to place an order,
- **capability access control** — certain host capabilities gated by assurance level,
- **federated trust presentation** — how this node presents its operator
  participant's assurance level to peers,
- **escrow and settlement authorization** — high-value operations may require
  `GovIdVerified` or higher,
- **onboarding gates** — federation admission may require a minimum level.

None of these downstream contracts are defined here. This memo establishes only
the identity-layer contract. Each consumer defines its own minimum level
requirement independently.

## What This Memo Does Not Define

- The verification protocol for phone confirmation (SMS OTP, carrier lookup, etc.).
- The verification protocol for government ID (document scan, registry API, etc.).
- The schema for the separate PII store, if one is introduced.
- The format or validation rules for national ID numbers by country.
- The hash salt derivation and storage strategy.
- Threshold or delegated custody of assurance-level claims.
- Cross-node or federated presentation of assurance levels.
- The governance process for adding or removing sovereign operator keys.

Those should be defined in dedicated documents as the relevant workstreams mature.
