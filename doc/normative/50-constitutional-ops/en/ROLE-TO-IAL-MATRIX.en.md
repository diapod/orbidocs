# DIA Role-to-IAL Matrix

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ROLE-IAL-001` |
| `type` | Implementing act / qualification matrix |
| `version` | 0.2.0-draft |
| `date` | 2026-03-31 |
| `changes` | Added `IAL5` row for software-anchored sovereign infrastructure roles. |

---

## 1. Purpose

This document maps DIA role classes to minimum identity assurance levels (`IAL`)
and indicates when `IAL` acts only as a gate and when it may grant a minimal
fixed `fixed_power_bonus`.

It does not change the higher-order rule: `IAL` does not replace procedural
reputation and does not dynamically multiply influence.

---

## 2. General Rules

1. `IAL` primarily acts as a gate to role and decision classes.

2. Higher `IAL` cannot by itself replace the required threshold of reputation,
   experience, or role screening.

3. Any `fixed_power_bonus` MUST be:

   - explicitly defined in federation policy,

   - fixed for the whole system or a given federation,

   - limited to `<= 1%`,

   - disableable for the highest-stake roles if a federation chooses a model with
     no premium whatsoever for stronger anchoring.

4. High-stake roles SHOULD require not only `IAL`, but also a probation period,
   procedural reputation, and conflict-of-interest checks.

5. The `IAL` ceiling also depends on the attestation class of the identity
   source. `Weak` sources should not by themselves unlock high-stakes roles,
   even if other local conditions are met.

---

## 3. Minimal Matrix

| Role class | Examples | Minimum `IAL` | `fixed_power_bonus` | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Basic participant | ordinary user, content author, observer | `IAL0` | `0%` | no high-stake role access |
| Node operator | custodians of ordinary `node-id`s | `IAL1` | `0%` | procedural durability is sufficient |
| Station / agent operator | hosting devices and agents | `IAL1` | `0%` | also depends on security hygiene |
| Payment / exchange participant | transactions, payments, settlement | `IAL1` | `0-0.25%` | federation may require a higher bar |
| Low-stake oracle | measurements and low-impact resolutions | `IAL2` | `0-0.25%` | only with additional audit |
| Whistleblower steward | intake and protected reporting channels | `IAL3` | `0%` | no premium preferred |
| Ordinary panelist | ad-hoc panel, medium-stake appeal | `IAL3` | `0-0.5%` | COI check required |
| High-stake panelist | cases with `U2` or heavy sanctions | `IAL3` | `0%` | `IAL4` chair recommended |
| FSC member | sealed chamber, unsealing quorum | `IAL4` | `0%` | no premium, only responsibility |
| High-stake oracle | health, liberty, high-damage impact | `IAL4` | `0%` | highest control required |
| High-stake governance | constitutional and structural roles | `IAL4` | `0%` | asymmetric accountability |
| Software-anchored sovereign infrastructure | protocol-level trust anchors shipped with software; designated sovereign operator keys | `IAL5` | `0%` | not obtained through attestation; assigned through software release governance; orthogonal to `IAL1`–`IAL4`; does not satisfy real-world identity requirements for other role classes |

---

## 4. Interpretive Rules

1. A federation MAY raise `IAL` thresholds for its own roles.

2. A federation MAY NOT lower thresholds for roles that fall within `U2`, `U3`,
   whistleblower protection, or high-stake governance.

3. If a role combines several functions, the highest required `IAL` applies.

4. If a case is inter-federation, the higher of the participating thresholds applies.

5. If the attestation source has class `weak`, a federation MAY NOT, through the
   matrix alone, assign a role level above the ceiling permitted by
   `ATTESTATION-PROVIDERS.en.md`.

---

## 5. Relations to Other Documents

- `ROOT-IDENTITY-AND-NYMS.en.md` defines identity layers and `IAL0-IAL4`.

- `PROCEDURAL-REPUTATION-SPEC.en.md` defines the reputation layer, which remains
  separate from `IAL`.
- `ATTESTATION-PROVIDERS.en.md` defines `weak` / `strong` classes and the `IAL`
  ceiling for attestation methods.

- `PANEL-SELECTION-PROTOCOL.en.md` and `IDENTITY-UNSEALING-BOARD.en.md` should use
  this matrix as the default minimum for panels and chambers.
