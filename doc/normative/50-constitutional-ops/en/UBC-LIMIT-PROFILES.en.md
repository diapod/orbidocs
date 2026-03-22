# UBC Limit and Portability Profiles

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-UBC-LIMITS-001` |
| `type` | Implementing act / limit and portability profiles |
| `version` | `0.1.0-draft` |
| `basis` | Art. XII.10-13 of the DIA Constitution; `UNIVERSAL-BASIC-COMPUTE.en.md`; `FIP-MEMBERSHIP-AND-QUORUM.en.md` |
| `mechanism status` | the `bridge_minimum`, `trans_federation_limited`, and canonical limit profiles are normative; federations may extend them but not weaken them |

---

## 1. Purpose of the Document

`UNIVERSAL-BASIC-COMPUTE.en.md` defines the right to a minimum compute allocation,
but leaves open how exactly to describe:

- limit profiles for communication and care/support modes,
- portability profiles across federations,
- the minimal path of cross-federation `Proof-of-Personhood` recognition through
  the `FIP` bridge or registry.

This document closes that gap.

---

## 2. General Rule

1. A limit profile is a named data contract, not a local implementation custom.
2. A portability profile defines what minimum scope of `UBC` is honored locally,
   across federations, and through the minimal `FIP` bridge.
3. Cross-federation recognition may run:
   - through direct federation recognition,
   - through the minimal `FIP` registry/bridge,
   - through a combination of both paths.
4. The `FIP` bridge guarantees only the `bridge_minimum` profile unless a
   federation explicitly declares an extension.
5. A federation may raise limits or add profiles, but may not go below the
   minimum defined in this document.

---

## 3. Core Terms

| Term | Meaning |
| :--- | :--- |
| `ubc_limit_profile` | a named limit profile for a specific access mode |
| `ubc_portability_profile` | a named profile describing how `UBC` is honored locally and cross-federation |
| `bridge_minimum` | the minimum profile available when PoP is recognized through the `FIP` bridge |
| `federation_extension` | a profile that extends the minimum through an explicit federation decision |
| `fip_pop_bridge_record` | a record describing the minimal `FIP` bridge/registry for PoP recognition |

---

## 4. Canonical Limit Profiles

### 4.1. `emergency_unlimited`

Mandatory profile for emergency modes.

- `access = true`
- `volume_limit = none`
- `rate_limit = none`
- `hard_stop = forbidden`

### 4.2. `communication_limited`

Minimum profile for cross-federation communication.

- `access = true`
- `volume_limit = required`
- `rate_limit = allowed`
- `hard_stop = forbidden` for critical help-seeking paths

### 4.3. `care_limited`

Minimum profile for care/support modes.

- `access = true`
- `volume_limit = required`
- `rate_limit = allowed`
- `hard_stop = allowed` only after explicit quota exhaustion, never for emergency

### 4.4. `bridge_minimum`

Portability profile guaranteed by the `FIP` bridge.

- `emergency = emergency_unlimited`
- `communication = communication_limited`
- `care = care_limited`
- `expansion_authority = federation_only`

### 4.5. `trans_federation_extended`

A portability profile broader than the minimum, declared by a federation.

- it may raise communication limits,
- it may raise care/support limits,
- it may add local care modes,
- it MUST leave an explicit policy and profile-version trace.

---

## 5. Minimal Data Model

### 5.1. `ubc_limit_profile`

```yaml
ubc_limit_profile:
  profile_id: "[identifier]"
  mode: "communication" # emergency | communication | care
  profile_class: "limited" # unlimited | limited | extended
  access: true
  volume_limit:
    amount: 100
    unit: "messages_per_day"
  rate_limit:
    amount: 10
    unit: "messages_per_hour"
  hard_stop: false
  emergency_override: true
  policy_ref: "DIA-UBC-LIMITS-001"
```

### 5.2. `ubc_portability_profile`

```yaml
ubc_portability_profile:
  portability_profile_id: "[identifier]"
  scope: "trans_federation_limited" # local_only | trans_federation_limited | trans_federation_extended
  recognition_paths:
    federation_direct: true
    fip_bridge: true
  emergency_profile_ref: "emergency_unlimited"
  communication_profile_ref: "communication_limited"
  care_profile_ref: "care_limited"
  federation_extension_allowed: true
  policy_ref: "DIA-UBC-LIMITS-001"
```

### 5.3. `fip_pop_bridge_record`

```yaml
fip_pop_bridge_record:
  bridge_id: "[bridge/registry identifier]"
  operator_ref: "[FIP or a specialized FIP component]"
  recognized_attestation_refs:
    - "[proof_of_personhood_attestation]"
  guaranteed_portability_profile_ref: "bridge_minimum"
  extension_profile_refs: []
  audit_ref: "[reference to an audit or bridge snapshot]"
  created_at: "[timestamp]"
```

---

## 6. Compliance Rules

The system does not satisfy this policy if:

1. the `FIP` bridge claims PoP recognition but does not deliver the `bridge_minimum` profile,
2. a federation labels a profile as `trans_federation_limited` yet does not provide
   explicit limits for communication and care,
3. the emergency profile contains a `hard_stop` or a practical quota that blocks asking for help,
4. a federation extension removes one of the three minimum access classes,
5. the implementation uses local, implicit quotas instead of named profiles.

---

## 7. Relation to Other Documents

- **`UNIVERSAL-BASIC-COMPUTE.en.md`**: defines the right to `UBC` itself and the
  allocation/funding models.
- **`FIP-MEMBERSHIP-AND-QUORUM.en.md`**: defines the minimum structure and
  accountability of `FIP`.
- **Constitution Art. XII.10-13**: sets the bounds of the non-withdrawable floor
  and the ban on hidden advantage.
