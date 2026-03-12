# Root Identity and Nyms in DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ROOT-ID-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. III.1-9, VII.4-8, XV, XVI of the DIA Constitution; `PROCEDURAL-REPUTATION-SPEC.en.md`; `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`; `IDENTITY-ATTESTATION-AND-RECOVERY.en.md` |
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
- the **main derived identity** anchored in root identity,
- the **durable node identity** as a public pseudonym of accountability,
- the **cryptographic pseudonyms** used in communication and governance,
- the **identity-assurance level** from which admissible influence is derived.

In this model, weakness or strength is not a property of `root-identity`
itself, but of the attestation of the identity source. The same subject may
therefore move from `weak` to `strong` attestation without losing
`anchor-identity`, `node-id`, or durable nyms.

This document defines that model.

---

## 2. Core Principles

1. In swarm communication, **nyms participate**, not civil root identity.

2. Root identity is used for **anchoring, attesting, and, if necessary, controlled unsealing** of derived identities, not for continuous exposure in the protocol.

3. **The greater the influence over others, sensitive data, reputation, or governance decisions, the higher the required identity-assurance level and the broader the required procedural disclosure.**

4. Multiple `node-id` values or nyms derived from one root identity **must not, by themselves, multiply influence**. Anti-Sybil logic counts the anchor source, not the number of masks.

5. One human or one entity may act through many devices and many agents, but this does not automatically mean many independent reputational identities.

6. The system prefers **operational pseudonymity and procedural openness**, not anonymity without accountability nor full civil transparency as the default.

7. `IAL` serves primarily as an **eligibility gate** for role classes, decisions, and action scopes. A federation MAY grant a more strongly verified identity a slight fixed procedural leverage, but never in the form of a reputation multiplier and never above `1%` of the total decision power of a given mechanism.

---

## 3. Conceptual Model

### 3.1. Identity Layers

| Layer | Meaning | Default visibility |
| :--- | :--- | :--- |
| `root-identity` | Root identity of a person or entity | private / procedurally disclosable only |
| `anchor-identity` | Main derived identity: stable cryptographic fingerprint anchored in `root-identity` | private / selectively disclosable |
| `node-id` | Durable, public node identity and main pseudonym of accountability | public |
| `nym` | Ephemeral or contextual cryptographic pseudonym used by a `node-id` | public or federation-scoped |
| `station-id` | Concrete device / host acting under delegation from a nym or node | public or selectively disclosed |
| `agent-id` | Process or runtime instance acting within station permissions | local / technical |

### 3.2. Relations

```text
root-identity
  -> attests one or many anchor-identity
anchor-identity
  -> derives or attests one or many node-id
node-id
  -> may issue one or many nyms
  -> may delegate one or many station-id
nym
  -> may delegate one or many station-id
station-id
  -> may run one or many agent-id
```

### 3.3. Source-of-Influence Rule

Reputational influence, role eligibility, and anti-Sybil limits default to the **`node-id` anchored in `anchor-identity`**, not to the raw number of nyms, stations, or processes.

---

## 4. Root Identity

`root-identity` means the source, extra-protocol identity of a natural person, legal person, or another recognized subject of accountability.

`root-identity` may be attested through sources with different evidentiary
strength:

- `weak` - low-friction sources with limited evidentiary power, such as a
  verified phone number,

- `strong` - sources with stronger evidentiary power and legal or organizational
  anchoring, such as eID, a qualified signature, or a formal registry.

It may be attested through:

- a verified phone number or an equivalent telecom channel,

- a state or supranational eID system,
- a qualified signature,
- a trusted profile / ePUAP,
- the mObywatel application and a QR-based or equivalent official channel,
- controlled multisig attestations by nodes with non-zero procedural reputation,
- another federation-accepted method, provided it ensures auditability and revocability.

`root-identity` is not public by default. Its role is to:

- issue attestations for `anchor-identity`,
- enable limited unsealing when the stakes are high,
- limit multiplication of influence through cheap identity creation.

The mapping of concrete methods to `weak` / `strong` classes and to maximum
`IAL` is defined by `ATTESTATION-PROVIDERS.en.md`.

---

## 5. Anchor Identity, Node Identity, and Nyms

### 5.1. Anchor Identity (`anchor-identity`)

`anchor-identity` is the main derived identity obtained from `root-identity`. It has the character of a stable cryptographic fingerprint or attestation that:

- is not publicly disclosed to other participants by default,
- allows the system to recognize the common anchor source behind many `node-id` values or nyms,
- enables continuity of accountability despite rotation of public masks,
- forms the basis for `IAL` calculation and anti-Sybil control.

If the technical implementation allows `node-id` to be safely derived directly from `root-identity`, a federation MAY omit a separate `anchor-identity` artifact, but semantically it must still preserve this layer as the distinction between root identity and the public node identifier.

The detailed method of first attestation, recovery-phrase use, the role of
`salt`, and memory of prior attestation is defined in
`IDENTITY-ATTESTATION-AND-RECOVERY.en.md`.

### 5.2. Node Identity (`node-id`)

`node-id` is the durable, public node identity and the main pseudonym of accountability in the swarm. It is the `node-id` that:

- accumulates the primary procedural and operational reputation,
- serves as the basic unit of trust routing and anti-Sybil control,
- may delegate stations and issue contextual nyms,
- has a **custodian**, identified procedurally by a persistent nym, an anchor record, or, when the stakes are high, through the unsealing track to `root-identity`.

`node-id` should be derived from a key or certificate controlled by `anchor-identity`, but it does not need to reveal `anchor-identity` itself.

`custodian_ref` should be understood as a durable procedural identifier of the
custodian of `node-id`: more stable than an ordinary ephemeral nym, yet weaker
and more shielding than `root-identity`. By default, it is not equal to
`anchor-identity`, although the audit track may link it to an anchor record or,
when the stakes are highest, to `root-identity`.

### 5.3. Nyms

A `nym` is an ephemeral or contextual cryptographic pseudonym delegated by a `node-id` for communication, transactions, payments, disputes, actions, or other purposes. The nym:

- signs communication or points to the signing key,
- may accumulate local or time-bounded reputation,
- holds contextual roles,
- is subject to procedural sanctions,
- is visible to other participants.

The cryptographic issuer of a nym is the `node-id`, while the accountability
issuer is the custodian of that `node-id`. This means the protocol sees the nym
as a mask issued by `node-id`, while the audit track may, if the stakes require
it, link that act of issuance to `custodian_ref`, and exceptionally also to
`root-identity`.

By default, a `nym` is not the main unit of influence in the system. Durable influence, anti-Sybil logic, and primary accountability remain attached to `node-id` and, indirectly, to the common anchor source.

### 5.4. Types of Nyms

| Type | Use | Property |
| :--- | :--- | :--- |
| `persistent_nym` | longer communication or operational relationship | long-lived, but secondary to `node-id` |
| `federation_nym` | activity within a particular federation | limited by federation context |
| `role_nym` | a role with special weight (e.g. panel, oracle) | limited to the role |
| `case_nym` | case, report, ad-hoc panel | one-off / short-lived |
| `transaction_nym` | transaction, payment, short exchange act | ephemeral |

### 5.5. Rules

1. A `node-id` MUST have a visible provenance record: whether it is derived from `anchor-identity`, attested by a federation, or delegated from another accountable subject.

2. A nym MUST have a visible provenance record: whether it is issued by a `node-id`, delegated from another nym, or attested by a federation.

3. A federation MAY limit the number of active `node-id` values or nyms from one anchor source in particular role classes.

4. A `node-id` used for higher-stakes roles MUST have the assurance level appropriate to that role (section 7).

5. A nym used for a higher-stakes role MUST be delegated from a `node-id` that satisfies the `IAL` threshold appropriate to that role.

6. Resetting a nym does not automatically reset the history of accountability if there are grounds to infer a common anchor source or sanction evasion.

---

## 6. Stations, Devices, and Delegation

One `node-id` may act through many network stations.

### 6.1. Station Delegation

Each station SHOULD have:

- its own `station-key`,
- its own `station-id`,
- a delegation certificate signed by the `node-id` key or an authorized nym delegated by `node-id`,
- a permission scope (`scope`),
- a validity window (`valid_from`, `valid_until`),
- revocability.

### 6.2. Rules

1. Multiple stations under one `node-id` **do not create multiple independent votes or multiple independent reputations**, unless a separate procedure grants them distinct subjecthood.

2. Compromise of one station SHOULD, by default, lead to revocation of that station certificate, not to rotation of the entire `node-id`, `anchor-identity`, or `root-identity`, unless there are signs of wider compromise.

3. Operational traces and incident analysis MAY be carried out at the `station-id` level even if the primary reputation is calculated at the `node-id` level.

---

## 7. Identity Assurance Levels

### 7.1. Levels

| Level | Name | Source of assurance | Default admissible influence |
| :--- | :--- | :--- | :--- |
| `IAL0` | unanchored pseudonym | no external attestation | low; no high-trust roles |
| `IAL1` | community-anchored pseudonym | sponsor / invite / basic attestation | limited operational participation |
| `IAL2` | basic multisig pseudonym | `multisig-basic` or equivalent `k-of-n` attestation | medium influence, lower-risk roles |
| `IAL3` | strongly anchored pseudonym | eID, qualified signature, ePUAP, mObywatel, `multisig-audited`, or equivalent | high influence, most public-trust roles |
| `IAL4` | legally / constitutionally unsealable pseudonym | strong anchoring + controlled disclosure procedure | highest-stakes roles and cases |

### 7.2. Jurisdictions and Examples

In practice, `IAL3` and `IAL4` may be achieved through different means:

- **EU / Poland**:
  - mObywatel,
  - ePUAP,
  - qualified signature,
  - and, in the future, the European Digital ID.

- **Jurisdictions without mature eID infrastructure**:
  - `multisig-basic`,
  - `multisig-audited`,
  - federation identity ceremonies,
  - organizational or professional attestations.

A federation MUST document which mechanisms map to which `IAL` level.

### 7.2.a. `IAL` ceiling by attestation strength

1. A `weak` attestation SHOULD normally top out at `IAL1`, and only
   exceptionally at `IAL2` if the federation adds safeguards against takeover
   and influence multiplication.

2. A `strong` attestation may unlock `IAL3` and `IAL4`, according to federation
   policy and role requirements.

3. A `weak -> strong` upgrade SHOULD NOT create a new `anchor-identity` if the
   user can simultaneously:

   - prove control over the existing anchor,

   - provide a new strong attestation.

### 7.3. IAL as Gate, Not Multiplier

1. `IAL` is used to unlock classes of roles, decisions, and permissions, not to linearly amplify reputation.

2. A federation MUST NOT use `IAL` as a multiplier on reputation scores or as an open-ended amplifier of voting power.

3. A federation MAY grant higher-IAL identities a small fixed procedural bonus (`fixed_power_bonus`), but only if:

   - the bonus is described explicitly,

   - it does not exceed `0.01` (`1%`) of the total power of the given mechanism,

   - it does not bypass reputation thresholds or domain thresholds,

   - it can be audited and revoked.

---

## 8. Rule: Greater Influence -> Greater Requirements

### 8.1. General Rule

The greater a given `node-id` or nym's influence over:

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

In environments where strong state-backed eID does not exist or is not safe, the system MAY use an attestation model.

### 9.1. Multisig Profiles

The system distinguishes two profiles:

- `multisig-basic` - community fallback with lower evidentiary power,

- `multisig-audited` - stronger profile with attester audit and stricter
  procedural accountability.

### 9.2. `multisig-basic`

A pseudonym reaches `IAL2` when:

- it has been attested by at least `k` out of `n` nodes,
- the attesting nodes have non-zero procedural reputation,
- the attestations leave a trace, validity period, and scope,
- the attesters are not in an obvious conflict of interest or one tightly controlled cluster.

### 9.3. `multisig-audited`

A pseudonym may reach `IAL3` when, in addition to `multisig-basic`, there are:

- a visible registry of attesters and their accountability,

- a federation or jurisdiction diversity requirement,

- an auditable trace of the attestation process,

- a recusals and appeals procedure,

- the ability to degrade to `IAL2` if these conditions are lost.

### 9.4. Consequence for Attesters

False or grossly negligent attestation is a procedural signal against the attesters. The system does not treat attestation as symbolic virtue-signaling but as delegation of trust with consequences.

---

## 10. Unsealing and Disclosure

Root identity may be disclosed only:

- in accordance with Constitution Art. III.9 and Art. X,
- at high stakes,
- through a defined multi-role procedure,
- to the minimum extent necessary.

### 10.1. Rules

1. The mere existence of root identity does not mean others may automatically demand it.

2. Disclosure of root identity outside the internal track requires the same or a higher level of rigor as disclosure of accountability for severe abuse.

3. A panel, audit process, or legal track may access root identity only when people cannot otherwise be protected, accountability cannot otherwise be resolved, or a legal duty cannot otherwise be fulfilled.

4. Unsealing leaves a separate audit trace with:
   `reason`, `scope`, `owner`, `legal_basis`, `expiry`.

---

## 11. Data Model

### 11.1. Root Identity Attestation

```yaml
root_identity_attestation:
  root_attestation_id: "[unique identifier]"
  subject_type: "human"          # human | organization
  attestation_strength: "strong" # weak | strong
  source_class: "qualified_signature"  # phone | eid | qualified_signature | registry | multisig | other
  assurance_level: "IAL3"
  method: "qualified_signature"  # eidas | mobywatel | epuap | multisig | other
  issuer: "[entity or procedure]"
  issued_at: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
  evidence_ref: "[reference to evidence or procedure]"
```

### 11.2. Anchor Identity

```yaml
anchor_identity_record:
  anchor_identity_id: "[stable derived identifier]"
  root_attestation_ref: "[reference]"
  derivation_method: "hash_binding"   # hash_binding | certificate | other
  recovery_record_ref: "[reference]"
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.3. Node Identity

```yaml
node_record:
  node_id: "[public node identifier]"
  node_pubkey: "[node public key]"
  anchor_identity_ref: "[reference]"
  assurance_level: "IAL2"
  custodian_ref: "[persistent_nym | procedural_ref]"
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.4. Nym

```yaml
nym_record:
  nym_id: "[public identifier]"
  nym_pubkey: "[public key]"
  node_ref: "[node_id]"
  anchor_identity_ref: "[reference or null]"
  assurance_level: "IAL2"
  nym_type: "persistent_nym"
  federation_scope: null
  role_scope: []
  valid_from: "[ISO 8601]"
  valid_until: "[ISO 8601]"
  revoke_at: null
```

### 11.5. Station Delegation

```yaml
station_delegation:
  station_id: "[station identifier]"
  station_pubkey: "[public key]"
  delegated_from_node: "[node_id]"
  delegated_from_nym: "[nym_id | null]"
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
| Multiplying `node-id` values or nyms from one source to increase influence | influence and thresholds counted against the anchor source; limits on active `node-id` values and nyms for sensitive roles |
| Theft of one device | revoke `station_delegation`; analyze harm at the `station-id` level |
| False multisig attestations | negative procedural signals for attesters; revocation of the attestation |
| Abuse of identity-disclosure requests | separate unsealing trace, multisig requirement, and legal / constitutional basis |
| No interoperable eID available | fallback to multisig model and federation-defined `IAL` levels |
| Whitewashing by rotating a `node-id` or nym | linkage through `anchor-identity` or common anchor source; continuity of accountability preserved |

---

## 13. Relation to Other Documents

- **Constitution Art. III.1-9**: this document concretizes privacy protection, minimal disclosure, and the conditions for procedural unsealing.
- **Constitution Art. VII.4-8**: this document specifies how identity-assurance level limits admissible influence and high-stakes roles.
- **`PROCEDURAL-REPUTATION-SPEC.en.md`**: reputation is assigned primarily to `node-id`, and locally also to nyms; anti-Sybil may aggregate influence to the level of a common anchor source.
- **`FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`**: shared federation control is analogous to a common anchor source behind many nyms; both mechanisms limit influence multiplication through formal splitting.
- **`PANEL-SELECTION-PROTOCOL.en.md`**: panel eligibility for higher-stakes roles SHOULD be based on the `IAL` level appropriate to the panel.
- **`ABUSE-DISCLOSURE-PROTOCOL.en.md`**: disclosure and unsealing of root identity must follow its thresholds and the principle of minimal disclosure.
- **`IDENTITY-ATTESTATION-AND-RECOVERY.en.md`**: this document defines first
  attestation, memory of prior attestation, the recovery phrase, and rules for
  reconstructing `anchor-identity`.
- **`IDENTITY-UNSEALING-BOARD.en.md`**: this document defines the Federation of
  Sealed Chambers, thresholds `nym -> node-id` and `node-id -> root-identity`,
  and the multi-chamber quorum for full unsealing.
