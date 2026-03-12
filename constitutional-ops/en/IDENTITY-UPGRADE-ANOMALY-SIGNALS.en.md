# Identity Upgrade Anomaly Signals in DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ID-UPGRADE-ANOM-001` |
| `type` | Implementing act / signals and review |
| `version` | 0.1.0-draft |
| `date` | 2026-03-12 |

---

## 1. Purpose

This document defines the minimal catalog of anomaly signals for attestation
upgrade, especially `phone -> strong`, so that federations can detect takeover,
identity laundering, and bypass of accountability thresholds.

---

## 2. General Rule

Identity upgrade is not just a field change in a record. It is a change in the
quality of anchoring that may unlock higher-stakes roles and permissions.
Therefore, upgrade must be treated as a risky operation and covered by anomaly
checks.

---

## 3. Signal Classes

| Code | Class | Example | Minimum response |
| :--- | :--- | :--- | :--- |
| `A1` | device / station churn | sudden rotation of many `station-id` values or nyms | increased monitoring |
| `A2` | fresh recovery | recent use of the recovery track before upgrade | soft hold or manual review |
| `A3` | key reset | recent change of `node-key` or station keys | manual review |
| `A4` | geographic anomaly | activity pattern from distant locations within a short time | soft hold or manual review |
| `A5` | network anomaly | unusual change of ASN, network, proxy, or channel | increased monitoring |
| `A6` | identity dispute | active case, appeal, or takeover signal | block upgrade until clarified |
| `A7` | attestation-source churn | fresh phone-number or `weak` source change | cooldown restart or manual review |
| `A8` | abuse signal | open incident, sanction bypass, false attestation | block upgrade |

---

## 4. Response Levels

- `monitor` - log the signal without blocking,
- `soft_hold` - temporary hold on the upgrade pending extra verification,
- `manual_review` - decision by a human or procedural panel required,
- `hard_block` - no upgrade until the case is closed.

---

## 5. Minimum Profile for `phone -> strong`

The default federation profile should require:

- `phone_upgrade_cooldown = 14 days`,
- absence of `A6` and `A8`,
- `manual_review` for `A2`, `A3`, or `A7`,
- at least `soft_hold` for `A4`,
- aggregation of `A1-A5` signals within one time window.

---

## 6. Relations to Other Documents

- `ATTESTATION-PROVIDERS.en.md` - defines when anomaly signals are required.
- `IDENTITY-ATTESTATION-AND-RECOVERY.en.md` - defines upgrade and the attestation chain.
- `UNSEAL-CASE-MODEL.en.md` - may serve as the shared case model if upgrade turns into a procedural dispute.
