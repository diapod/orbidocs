# Root Identity and Nyms in DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-ID-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. III.1-9, VII.4-8, XV, XVI of the DIA Constitution; `PROCEDURAL-REPUTATION-SPEC.en.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md` |
| `mechanism status` | the data model and assurance levels are normative; concrete eID integrations remain deployment parameters |

---

## 1. Purpose of the Document

The Constitution simultaneously requires:

- protection of privacy and minimal disclosure,
- resistance to Sybil attacks and influence multiplication through cheap identities,
- higher accountability thresholds for roles with greater power,
- procedural ability to disclose when the stakes are high.

What is still missing is a shared model that separates:

- the **root identity** of a person or entity,
- the **cryptographic pseudonyms** used in communication and governance,
- the **identity-assurance level** from which admissible influence is derived.

This document defines that model.

---

## 2. Core Principles

1. In swarm communication, **nyms participate**, not civil root identity.

2. Root identity is used for **anchoring, attesting, and, if necessary,
   controlled unsealing** of nyms, not for continuous exposure in the protocol.

3. **The greater the influence over others, sensitive data, reputation, or
   governance decisions, the higher the required identity-assurance level and the
   broader the required procedural disclosure.**

4. Multiple nyms derived from one root identity **must not, by themselves,
   multiply influence**. Anti-Sybil logic counts the anchor source, not the number
   of masks.

5. One human or one entity may act through many devices and many agents, but this
   does not automatically mean many independent reputational identities.

6. The system prefers **operational pseudonymity and procedural openness**, not
   anonymity without accountability nor full civil transparency as the default.

---

## 3. Conceptual Model

### 3.1. Identity Layers

| Layer | Meaning | Default visibility |
| :--- | :--- | :--- |
| `root-identity` | Root identity of a person or entity | private / procedurally disclosable only |
| `nym` | Cryptographic pseudonym participating in communication, reputation, and roles | public or federation-scoped |
| `station-id` | Concrete device / host acting under delegation from a nym or node | public or selectively disclosed |
| `agent-id` | Process or runtime instance acting within station permissions | local / technical |

### 3.2. Relations

```text
root-identity
  -> attests one or many nyms
nym
  -> may delegate one or many station-id
station-id
  -> may run one or many agent-id
```

### 3.3. Source-of-Influence Rule

Reputational influence, role eligibility, and anti-Sybil limits default to the
**nym anchored in root identity**, not to the raw number of stations or processes.

---

## 4. Root Identity

`root-identity` means the source, extra-protocol identity of a natural person,
legal person, or another recognized subject of accountability.

It may be attested through:

- a state or supranational eID system,
- a qualified signature,
- a trusted profile / ePUAP,
- the mObywatel application and a QR-based or equivalent official channel,
- controlled multisig attestations by nodes with non-zero procedural reputation,
- another federation-accepted method, provided it ensures auditability and
  revocability.

`root-identity` is not public by default. Its role is to:

- issue attestations for nyms,
- enable limited unsealing when the stakes are high,
- limit multiplication of influence through cheap identity creation.

---

## 5. Nyms

A `nym` is the cryptographic pseudonym participating in the system. The nym:

- signs communication or points to the signing key,
- accumulates reputation,
- holds roles,
- is subject to procedural sanctions,
- is visible to other participants.

### 5.1. Types of Nyms

| Type | Use | Property |
| :--- | :--- | :--- |
| `persistent_nym` | long-term participation in a federation | long-lived |
| `federation_nym` | activity within a particular federation | limited by federation context |
| `role_nym` | a role with special weight (e.g. panel, oracle) | limited to the role |
| `case_nym` | case, report, ad-hoc panel | one-off / short-lived |

### 5.2. Rules

1. A nym MUST have a visible provenance record: whether it is directly anchored,
   delegated from another nym, or attested by a federation.

2. A federation MAY limit the number of active nyms from one anchor source in
   particular role classes.

3. A nym used for higher-stakes roles MUST have the assurance level appropriate
   to that role (section 7).

4. Resetting a nym does not automatically reset the history of accountability if
   there are grounds to infer a common anchor source or sanction evasion.

---

## 6. Stations, Devices, and Delegation

One nym or one public node identity may act through many network stations.

### 6.1. Station Delegation

Each station SHOULD have:

- its own `station-key`,
- its own `station-id`,
- a delegation certificate signed by the nym key or node identity key,
- a permission scope (`scope`),
- a validity window (`valid_from`, `valid_until`),
- revocability.

### 6.2. Rules

1. Multiple stations under one nym **do not create multiple independent votes or
   multiple independent reputations**, unless a separate procedure grants them
   distinct subjecthood.

2. Compromise of one station SHOULD, by default, lead to revocation of that
   station certificate, not to rotation of the entire nym or root identity,
   unless there are signs of wider compromise.

3. Operational traces and incident analysis MAY be carried out at the
   `station-id` level even if the primary reputation is calculated at the nym
   level.

---

## 7. Identity Assurance Levels

### 7.1. Levels

| Level | Name | Source of assurance | Default admissible influence |
| :--- | :--- | :--- | :--- |
| `IAL0` | unanchored pseudonym | no external attestation | low; no high-trust roles |
| `IAL1` | community-anchored pseudonym | sponsor / invite / basic attestation | limited operational participation |
| `IAL2` | multisig pseudonym | `k-of-n` attestation by nodes with procedural reputation | medium influence, lower-risk roles |
| `IAL3` | strongly anchored pseudonym | eID, qualified signature, ePUAP, mObywatel, or equivalent | high influence, most public-trust roles |
| `IAL4` | legally / constitutionally unsealable pseudonym | strong anchoring + controlled disclosure procedure | highest-stakes roles and cases |

### 7.2. Jurisdictions and Examples

In practice, `IAL3` and `IAL4` may be achieved through different means:

- **EU / Poland**:
  - mObywatel,
  - ePUAP,
  - qualified signature,
  - and, in the future, the European Digital ID.

- **Jurisdictions without mature eID infrastructure**:
  - multisig attestations,
  - federation identity ceremonies,
  - organizational or professional attestations.

A federation MUST document which mechanisms map to which `IAL` level.

---

## 8. Rule: Greater Influence -> Greater Requirements

### 8.1. General Rule

The greater a given nym's influence over:

- human safety,
- sensitive data,
- the reputation of others,
- governance decisions,
- interim measures,
- disclosure and appeals procedures,

the higher MUST be:

- the identity-assurance level,
- the requirement to maintain current anchoring,
- the possibility of procedural unsealing,
- the quality of action traces.

### 8.2. Minimum Matrix

| Class of action / role | Default minimum level |
| :--- | :--- |
| ordinary communication and local participation | `IAL0` |
| sponsoring new nyms or admissions | `IAL1` |
| procedurally weighted vote, local federation operator, screening role | `IAL2` |
| ad-hoc panel, oracle, auditor, whistleblower guardian, sensitive-data operator | `IAL3` |
| highest-stakes roles with potential irreversible harm or controlled disclosure of others' identities | `IAL4` |

Federations may tighten this matrix but may not loosen it for high-stakes roles.

---

## 9. Multisig Attestations

In environments where strong state-backed eID does not exist or is not safe, the
system MAY use an attestation model.

### 9.1. Minimum Model

A pseudonym reaches `IAL2` when:

- it has been attested by at least `k` out of `n` nodes,
- the attesting nodes have non-zero procedural reputation,
- the attestations leave a trace, validity period, and scope,
- the attesters are not in an obvious conflict of interest or one tightly
  controlled cluster.

### 9.2. Consequence for Attesters

False or grossly negligent attestation is a procedural signal against the
attesters. The system does not treat attestation as symbolic virtue-signaling but
as delegation of trust with consequences.

---

## 10. Unsealing and Disclosure

Root identity may be disclosed only:

- in accordance with Constitution Art. III.9 and Art. X,
- at high stakes,
- through a defined multi-role procedure,
- to the minimum extent necessary.

### 10.1. Rules

1. The mere existence of root identity does not mean others may automatically
   demand it.

2. Disclosure of root identity outside the internal track requires the same or a
   higher level of rigor as disclosure of accountability for severe abuse.

3. A panel, audit process, or legal track may access root identity only when
   people cannot otherwise be protected, accountability cannot otherwise be
   resolved, or a legal duty cannot otherwise be fulfilled.

4. Unsealing leaves a separate audit trace with:
   `reason`, `scope`, `owner`, `legal_basis`, `expiry`.

---

## 11. Data Model

### 11.1. Root Identity Attestation

```yaml
root_identity_attestation:
  root_attestation_id: "[unique identifier]"
  subject_type: "human"          # human | organization
  assurance_level: "IAL3"
  method: "qualified_signature"  # eidas | mobywatel | epuap | multisig | other
  issuer: "[entity or procedure]"
  issued_at: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
  evidence_ref: "[reference to evidence or procedure]"
```

### 11.2. Nym

```yaml
nym_record:
  nym_id: "[public identifier]"
  nym_pubkey: "[public key]"
  root_attestation_ref: "[reference or null]"
  assurance_level: "IAL2"
  nym_type: "persistent_nym"
  federation_scope: null
  role_scope: []
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.3. Station Delegation

```yaml
station_delegation:
  station_id: "[station identifier]"
  station_pubkey: "[public key]"
  delegated_from_nym: "[nym_id]"
  scope: []
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
  delegation_sig: "[nym or node signature]"
```

---

## 12. Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Multiplying nyms from one source to increase influence | influence and thresholds counted against the anchor source; limits on active nyms for sensitive roles |
| Theft of one device | revoke `station_delegation`; analyze harm at the `station-id` level |
| False multisig attestations | negative procedural signals for attesters; revocation of the attestation |
| Abuse of identity-disclosure requests | separate unsealing trace, multisig requirement, and legal / constitutional basis |
| No interoperable eID available | fallback to multisig model and federation-defined `IAL` levels |
| Whitewashing by rotating a nym | linkage through root identity or common anchor source; continuity of accountability preserved |

---

## 13. Relation to Other Documents

- **Constitution Art. III.1-9**: this document concretizes privacy protection,
  minimal disclosure, and the conditions for procedural unsealing.
- **Constitution Art. VII.4-8**: this document specifies how identity-assurance
  level limits admissible influence and high-stakes roles.
- **`PROCEDURAL-REPUTATION-SPEC.en.md`**: reputation is assigned to the nym or
  public node identity, but anti-Sybil logic may aggregate influence back to the
  common anchor source.
- **`FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`**: shared federation control is
  analogous to a common anchor source behind many nyms; both mechanisms limit
  influence multiplication through formal splitting.
- **`PANEL-SELECTION-PROTOCOL.en.md`**: panel eligibility for higher-stakes roles
  SHOULD be based on the `IAL` level appropriate to the panel.
- **`ABUSE-DISCLOSURE-PROTOCOL.en.md`**: disclosure and unsealing of root identity
  must follow its thresholds and the principle of minimal disclosure.

