# DIA Universal Basic Compute Specification

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-UBC-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | `0.1.0-draft` |
| `basis` | Art. XII.11-13 of the DIA Constitution; `SWARM-ECONOMY-SUFFICIENCY.en.md`; `ROOT-IDENTITY-AND-NYMS.en.md`; `IDENTITY-UNSEALING-BOARD.en.md`; `FIP-MEMBERSHIP-AND-QUORUM.en.md` |
| `mechanism status` | the minimal model of PoP, UBC allocation, and settlement is normative; limit profiles are concretized by `UBC-LIMIT-PROFILES.en.md`; cross-federation recognition may run through federations or the minimal `FIP` bridge/registry |

---

## 1. Purpose of the Document

The Constitution grants verified personhood in the network the right to a
non-withdrawable minimum of compute resources needed for communication,
orientation, and access to emergency and care modes. What is still missing is an
implementing document that defines:

- the minimal Proof-of-Personhood model without default de-anonymization,
- the rules for granting `universal_basic_compute`,
- limited portability across federations, including the minimal `FIP` bridge/registry,
- the minimal funding and settlement trace for that minimum.

This document operationalizes those obligations.

---

## 2. General Rule

1. `Universal Basic Compute` (`UBC`) is a floor of participation and protection,
   not a reward for status, reputation, or capital.
2. The lack of current reputational or economic contribution MUST NOT by itself
   cut a person off from the basic ability to communicate with the swarm, orient
   themselves in their situation, and use emergency and care modes.
3. Access to `UBC` and its protective modes MUST NOT be conditioned on humiliation,
   self-abasement, emotional dependency, or arbitrary personal favor from an
   operator.
4. Eligibility for `UBC` is grounded in a constitutionally admissible
   `Proof-of-Personhood`, by default without full de-anonymization.
5. A local federation MAY grant a broader `UBC` profile, but it may not go below
   the minimum defined in this document.
6. Cross-federation recognition of `Proof-of-Personhood` is limited by default and
   may run through federations or the minimal `FIP` bridge/registry:
   - emergency modes MUST be available without limit,
   - communication MUST be available under a limited profile,
   - care modes MUST be available under a limited profile.
7. Federations MAY broaden cross-federation recognition and raise limits, and the
   `FIP` bridge MAY guarantee only the minimum portability profile; neither path may
   narrow recognition below the above minimum.
8. `UBC` may not be used as a hidden path to constitutional advantage,
   privileged high-stakes routing, or bypass of reputation requirements.

---

## 3. Core Terms

| Term | Meaning |
| :--- | :--- |
| `proof_of_personhood_attestation` | an attestation that a subject corresponds to one verified person, without requiring public disclosure of root identity |
| `ubc_allocation` | an allocation of minimal compute resources and the corresponding access modes |
| `ubc_settlement` | a periodic record of federation funding and settlement of `UBC` |
| `portability_profile` | a profile describing what scope of `UBC` is honored locally and cross-federation |
| `limited_communication` | a communication profile with explicit limits of volume, frequency, or throughput |
| `limited_care` | a care/support profile with explicit limits of volume or frequency |
| `emergency_unlimited` | absence of limiting quota for emergency modes under a valid `proof_of_personhood_attestation` |
| `fip_pop_bridge` | the minimal `FIP` registry/bridge that recognizes cross-federation PoP for the minimum `UBC` portability profile |

`Proof-of-Personhood` may be realized, among others, through:

- cryptographic multisig attestations without de-anonymization,
- federation attestations,
- mechanisms recognized by the Federation of Sealed Chambers,
- functionally equivalent hybrids.

---

## 4. Minimal Data Model

### 4.1. `proof_of_personhood_attestation`

```yaml
proof_of_personhood_attestation:
  attestation_id: "[unique identifier]"
  subject_ref: "[stable anonymous handle of the person]"
  issuer_scope: "federation" # federation | fip_bridge | hybrid
  issuer_ref: "[federation or FIP bridge]"
  issuer_federation_id: "[issuing or recognizing federation]"
  bridge_ref: "[optional reference to the FIP bridge]"
  attestation_method: "cryptographic_vouching" # cryptographic_vouching | federation_attestation | sealed_chambers_recognition | fip_bridge_recognition | hybrid
  assurance_scope: "proof_of_personhood"
  deanon_not_required: true
  uniqueness_scope: "federation" # federation | trans_federation_limited | trans_federation_extended
  valid_from: "[timestamp]"
  valid_until: "[timestamp]"
  portability_profile:
    trans_federation_default:
      emergency: "unlimited"
      communication: "limited"
      care: "limited"
    bridge_minimum_supported: true
    federation_extension_allowed: true
  evidence_ref: "[reference to evidence package or procedure]"
  revocation_ref: "[optional reference to revocation procedure]"
```

### 4.2. `ubc_allocation`

```yaml
ubc_allocation:
  allocation_id: "[unique identifier]"
  subject_ref: "[stable anonymous handle of the person]"
  federation_id: "[allocating federation]"
  attestation_ref: "[proof_of_personhood_attestation]"
  recognition_source: "federation_local" # federation_local | federation_cross_recognition | fip_bridge
  recognition_ref: "[recognizing federation or FIP bridge]"
  measurement_period: "P30D"
  valid_from: "[timestamp]"
  valid_until: "[timestamp]"
  compute_unit: "[compute_credit / second / tokenized_quota / other unit]"
  portability_scope: "trans_federation_limited" # local | trans_federation_limited | trans_federation_extended
  guaranteed_modes:
    emergency:
      access: true
      limit_profile: "unlimited"
    communication:
      access: true
      limit_profile: "limited"
      limit_ref: "[limit profile]"
    care:
      access: true
      limit_profile: "limited"
      limit_ref: "[limit profile]"
  funding_policy_ref: "DIA-UBC-001"
  limit_policy_ref: "DIA-UBC-LIMITS-001"
  policy_annotations: {}
  created_at: "[timestamp]"
```

### 4.3. `ubc_settlement`

```yaml
ubc_settlement:
  settlement_id: "[unique identifier]"
  federation_id: "[federation]"
  period_start: "[timestamp]"
  period_end: "[timestamp]"
  compute_unit: "[unit]"
  beneficiary_count: 0
  total_allocated_compute: 0
  funding_sources:
    - source_class: "business_nodes" # business_nodes | high_margin_instances | surplus_recirculation | voluntary_operator_surplus | federation_reserve
      amount: 0
    - source_class: "surplus_recirculation"
      amount: 0
  emergency_usage: 0
  communication_usage: 0
  care_usage: 0
  policy_ref: "DIA-UBC-001"
  created_at: "[timestamp]"
```

---

## 5. Eligibility for `UBC`

1. The minimum condition of eligibility is a valid `proof_of_personhood_attestation`.
2. A federation MUST NOT require full de-anonymization as the ordinary condition of
   entering `UBC`, unless a constitutional exception applies under the relevant
   procedure.
3. A federation MAY require periodic refresh of the attestation, but may not use
   that process as a covert tool for excluding poor, weaker, or temporarily inactive
   operators.
4. The entry, refresh, or review procedure MUST NOT require humiliation,
   self-abasement, emotional dependency, or a gatekeeper's personal satisfaction as
   a condition of access.
5. `UBC` does not depend on reward balance, reputational standing, or commercial
   activity, although a federation may condition expanded limits on additional
   criteria.

---

## 6. Limited Cross-Federation Portability

### 6.1. Mandatory Minimum

If a federation or the `FIP` bridge/registry recognizes cross-federation
`proof_of_personhood_attestation`, it must provide at least:

1. unlimited access to emergency modes,
2. limited access to communication,
3. limited access to care/support modes.

### 6.2. Ban on Emergency Degradation

Emergency mode MUST NOT be subject to a volume limit that in practice prevents
calling for help, reporting violence, life-threatening danger, severe abuse, or
loss of basic safety.

### 6.3. Federation Extensions

A federation may:

1. raise communication limits,
2. raise care/support limits,
3. recognize a broader class of cross-federation attestations,
4. add local care modes,

provided it leaves a policy trace and does not weaken the minimum in 6.1-6.2.

The `FIP` bridge/registry:

1. MAY recognize cross-federation `Proof-of-Personhood` for the purpose of the minimum profile,
2. MUST NOT reduce limits below the minimum,
3. SHOULD NOT grant a profile broader than `bridge_minimum` unless it operates
   under an explicit federation extension.

---

## 7. Funding

1. `UBC` MUST have a public contribution model.
2. The minimum catalog of funding sources includes:
   - `business_nodes`,
   - `high_margin_instances`,
   - `surplus_recirculation`,
   - `voluntary_operator_surplus`.
3. A federation MAY add other sources, but may not hide them from audit.
4. Funding of `UBC` may not depend solely on voluntary donations if the federation
   declares a constitutional minimum.

---

## 8. Compliance Tests

The system does not satisfy this policy if it:

1. requires full de-anonymization as the ordinary condition of entry into `UBC`,
2. cuts a person with a valid `Proof-of-Personhood` off from emergency modes,
3. leaves no `ubc_allocation` or `ubc_settlement` trace,
4. conditions access on humiliation, self-abasement, emotional dependency, or
   arbitrary operator favor,
5. makes the basic allocation depend on reputation, balance, or capital position,
6. uses `UBC` as a hidden channel for buying constitutional advantage,
7. recognizes cross-federation PoP only nominally, without a real minimum of
   communication and care/support.

---

## 9. Relation to Other Documents

- **Constitution Art. XII.11-13**: PoP, non-withdrawable minimum compute, and the ban on hidden advantage.
- **`SWARM-ECONOMY-SUFFICIENCY.en.md`**: shared model of funding, surpluses, and concentration brakes.
- **`ROOT-IDENTITY-AND-NYMS.en.md`**: identity-anchoring layer without default publicity.
- **`IDENTITY-UNSEALING-BOARD.en.md`**: federationally recognized strong confirmation mechanisms without full identity publication.
- **`FIP-MEMBERSHIP-AND-QUORUM.en.md`**: the minimal structure and accountability of the specialized `FIP` federation.
- **`UBC-LIMIT-PROFILES.en.md`**: the canonical limit and portability profiles for `UBC`.
