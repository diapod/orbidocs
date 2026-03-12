# Identity Attestation Methods and Mapping in DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ATTEST-PROVIDERS-001` |
| `type` | Implementing act / attestation-method registry |
| `version` | 0.1.0-draft |
| `date` | 2026-03-12 |

---

## 1. Purpose

This document maps identity-attestation methods to:

- attestation-strength class (`weak` / `strong`),
- maximum `IAL`,
- operational limits,
- requirements for upgrade and refresh.

It does not create a new kind of `root-identity`. It defines only the quality of
attestation of the identity source.

---

## 2. General Rules

1. `weak` and `strong` are properties of attestation, not of personhood.

2. The same `anchor-identity` may have many attestations of different strength over time.

3. A `weak -> strong` upgrade SHOULD preserve `anchor-identity`, `node-id`, and
   `persistent_nym` if proof of continuity of control exists.

4. The maximum `IAL` of a method is the default ceiling; a federation may lower
   it, but should not raise it without an explicit validation procedure.

---

## 3. Default Mapping

| `source_class` | Example | Strength | Default max `IAL` | Notes |
| :--- | :--- | :--- | :--- | :--- |
| `phone` | phone number with OTP confirmation | `weak` | `IAL1` | may reach `IAL2` only with added federation safeguards |
| `multisig` | `k-of-n` vouching | `weak` or `strong` | `IAL2` by default | to `IAL3` only with a very strong attestation and audit model |
| `eid` | state or supranational eID | `strong` | `IAL3` | to `IAL4` only when paired with an unsealing track |
| `mobywatel` | official QR / state app channel | `strong` | `IAL3` | locally jurisdiction-dependent |
| `epuap` | trusted profile / official channel | `strong` | `IAL3` | depends on integration quality |
| `qualified_signature` | qualified signature | `strong` | `IAL4` | preferred for high-stakes roles |
| `registry` | formal registry data of an organization | `strong` | `IAL3` | to `IAL4` after meeting procedural requirements |
| `other` | local / experimental method | depends on validation | `IAL0-IAL2` | requires explicit federation documentation |

---

## 4. Special Rules for Phone Numbers

1. A verified phone number is convenient for entry, but SHOULD NOT by itself
   unlock high-stakes roles.

2. For `source_class = phone`, a federation SHOULD at minimum restrict:

- governance roles,
- panel roles,
- high-stakes oracle roles,
- operations requiring `U2` or `U3`.

3. A federation MAY allow `phone -> IAL2` only when there are additionally:

- a longer reputational maturation period,
- takeover-anomaly detection,
- influence-multiplication limits,
- the ability to downgrade quickly after a compromise signal.

---

## 5. Upgrade Rules

1. A `weak -> strong` upgrade requires, at the same time:

- control over the existing anchor,
- a new `strong` attestation,
- no hard identity dispute.

2. After the upgrade:

- `anchor-identity` remains the same,
- `node-id` may remain the same,
- ephemeral nyms and station certificates may be refreshed,
- the prior attestation remains in the audit chain as `superseded` or `expired`.

---

## 6. Relations to Other Documents

- `ROOT-IDENTITY-AND-NYMS.en.md` defines identity layers and `IAL` levels.
- `IDENTITY-ATTESTATION-AND-RECOVERY.en.md` defines attestation memory and upgrade.
- `ROLE-TO-IAL-MATRIX.en.md` defines which roles can be unlocked at a given `IAL`.
