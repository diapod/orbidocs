# Federation of Sealed Chambers and Identity Unsealing in DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-SEAL-BOARD-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. IV.6-9, Art. X.7-13, Art. XVI of the DIA Constitution; `ROOT-IDENTITY-AND-NYMS.en.md`; `ABUSE-DISCLOSURE-PROTOCOL.en.md`; `FIP-MEMBERSHIP-AND-QUORUM.en.md`; `UNSEAL-CASE-MODEL.en.md` |
| `mechanism status` | the governance and threshold model is normative; split-knowledge technique remains deployment-specific |

---

## 1. Purpose of the Document

This document defines:

- the Federation of Sealed Chambers as a distributed constitutional IRL organ,
- thresholds for descending `nym -> node-id`,
- thresholds for unsealing `node-id -> root-identity`,
- rules of redundancy, quorum, jurisdictional diversification, and split knowledge,
- the minimum audit trace and appeals track.

Its purpose is to enable accountability without creating a single point of pressure,
retaliation, or capture.

---

## 2. Basic Rule

1. Not every abuse requires knowing `root-identity`.

2. The default enforcement path is:

   - local measures at the `nym` level,

   - infrastructure sanctions at the `node-id` level.

3. `root-identity` may be discovered only when:

   - identification of `node-id` alone is insufficient to protect people, the
     community, or procedural integrity,

   - a legal obligation exists or the harm threshold is of the highest stake,

   - the decision passes through the Federation of Sealed Chambers.

4. No single chamber may be the sole holder of full unsealing capability.

---

## 3. Constitutional Model

### 3.1. Federation of Sealed Chambers

The Federation of Sealed Chambers (`FSC`) is a federation of independent IRL
chambers that:

- operate under a shared minimum constitutional standard,
- are distributed across jurisdictions,
- are subject to audit and conflict-of-interest rules,
- participate in unsealing root identity only through multi-chamber quorum.

### 3.2. Scope of Chamber Competence

A chamber may:

- receive and register unsealing requests,
- verify formal completeness and entry thresholds,
- co-decide on descent `node-id -> root-identity`,
- hold a share in split-knowledge material,
- maintain an audit trace of its decisions.

A chamber may not:

- independently conduct ordinary reputation disputes,
- replace ad-hoc panels or federation governance,
- unseal `root-identity` by itself,
- use identity material beyond the scope of a concrete procedure.

### 3.3. Redundancy

1. `FSC` SHOULD consist of many chambers globally.

2. Unsealing `root-identity` MUST require a small ad-hoc quorum composed of
   several chambers, not action by the entire federation at once.

3. The concrete minima for membership, statuses, and quorum are defined by
   `FIP-MEMBERSHIP-AND-QUORUM.en.md`.

4. A federation MAY tighten these minima, but may not loosen them.

---

## 4. Disclosure Thresholds

### 4.1. `U0` - no descent

The case remains at the `nym` level. Only local measures are allowed:

- rate limiting,
- contextual isolation,
- local mute,
- blocking of a single action,
- monitoring.

### 4.2. `U1` - procedural descent `nym -> node-id`

`U1` is the threshold for infrastructure sanctions and does not require knowing
`root-identity`.

Minimum threshold:

- `stake-level >= S2`,
- `evidence-level >= E2`,
- co-signature by at least two case roles.

Permitted effects:

- identification of `node-id`,
- identification of active nyms and stations linked to `node-id`,
- application of sanctions `I1-I4`,
- disclosure of `node-id` within internal or federation scope.

`U1` does not authorize access to `root-identity`.

### 4.3. `U2` - descent `node-id -> custodian_ref`

`U2` is the intermediate threshold for cases where identifying the procedurally
responsible subject is necessary, but primary identity is not yet required.

Here, `custodian_ref` means a durable procedural handle to the custodian of a
`node-id`, such as a `persistent_nym` or a federation-level `procedural_ref`.
It does not automatically mean `anchor-identity` or `root-identity`.

Minimum threshold:

- `stake-level >= S3`,

- `evidence-level >= E3`,

- COI control,

- multi-role co-signature,

- justification that `node-id` alone is insufficient.

Permitted effects:

- disclosure of `custodian_ref` to authorized parties,
- blocking of roles or permissions at the custodian level,
- preparation of an application to `FSC`.

### 4.4. `U3` - full unsealing `node-id -> root-identity`

`U3` is the highest threshold.

Minimum threshold:

- `stake-level >= S3` and `evidence-level >= E3` where a legal duty exists or a
  lasting harm cannot be stopped by infrastructure sanctions alone,

or

- `stake-level >= S4` and `evidence-level >= E3` in other cases.

Additionally required are:

- absence of a less invasive path to the goal,

- decision by `FSC` quorum,

- narrowly bounded disclosure scope,

- readiness for appeal.

---

## 5. Quorum and Diversification

### 5.1. Minimum Quorum

The default quorum for `U2` and `U3`, as well as chamber statuses and emergency
mode, are defined by `FIP-MEMBERSHIP-AND-QUORUM.en.md`. This document retains
only the rule that full unsealing cannot be performed by a single chamber or by
a quorum lacking jurisdictional and organizational diversity.

### 5.2. Recusals

A chamber must be recused when it:

- has a conflict of interest,
- is in a dependency relationship with the applicant or a party,
- belongs to the same tightly controlled group as another chamber in quorum,
- is subject to a credible signal of compromise.

### 5.3. Emergency Mode

If a chamber is unavailable, intimidated, or under retaliation:

- the case moves to a replacement quorum,
- the event is logged as `seal-body-disruption`,
- the federation activates operational and legal protection.

---

## 6. Split Knowledge

1. The mapping `node-id -> root-identity` SHOULD NOT be fully available to a
   single chamber.

2. The system SHOULD use a split-knowledge model, such as:

   - threshold encryption,

   - secret sharing,

   - multi-party escrow.

3. Compromise of a single chamber must not by itself enable disclosure of
   `root-identity`.

4. The technical implementation of split knowledge is replaceable, but MUST
   provide:

   - no single point of read access,

   - ability to rotate shares,

   - trace of share use,

   - ability to remove a chamber from the system.

---

## 7. Procedure Flow

### 7.1. Request

A request for descent `U2` or `U3` MUST contain:

- `case-id`,
- threshold `U`,
- necessity rationale,
- `stake-level` and `evidence-level`,
- COI check result,
- proposed disclosure scope,
- indication of less invasive means already used or rejected.

### 7.2. Formal Review

The intake chamber verifies:

- completeness,
- admissibility of the threshold,
- whether the case should stop at `U1`,
- whether an obvious conflict of interest or lack of basis exists.

### 7.3. Decision

1. `U1` may be decided within the federation without `FSC`.

2. `U2` may require one chamber as a procedural supervisor if federation policy
   so provides.

3. `U3` requires `FSC` quorum.

### 7.4. Scope of Disclosure

Even after a positive `U3` decision, disclosure MUST be:

- addressed to a specific recipient or class of recipients,
- limited to the minimum necessary,
- bounded by `expiry`,
- subject to trace of downstream use.

---

## 8. Data Model

### 8.1. Chamber Registry

```yaml
seal_chamber_record:
  chamber_id: "[identifier]"
  jurisdiction: "[jurisdiction]"
  federation_affiliation: "[federation or entity]"
  status: "active"              # active | suspended | compromised | retired
  public_key: "[public key]"
  trust_class: "constitutional"
  valid_from: "[ISO 8601]"
  valid_until: null
```

### 8.2. Descent Request

```yaml
identity_unsealing_request:
  request_id: "[identifier]"
  case_id: "[case]"
  threshold: "U3"              # U1 | U2 | U3
  target_nym: "[nym_id | null]"
  target_node_id: "[node_id | null]"
  requested_scope: "[custodian_ref | root_identity]"
  stake_level: "S3"
  evidence_level: "E3"
  less_invasive_means_checked: true
  coi_check: "pass"
  submitted_by: []
  submitted_at: "[ISO 8601]"
```

### 8.3. Quorum Decision

```yaml
seal_quorum_decision:
  decision_id: "[identifier]"
  request_id: "[reference]"
  chambers: []
  jurisdictions: []
  outcome: "approved"          # approved | denied | remand
  disclosure_scope: "root_identity"
  expiry: "[ISO 8601]"
  rationale_ref: "[reference]"
  signatures: []
```

---

## 9. Appeal

1. A `U3` decision MUST be appealable.

2. The appeal is heard by a new quorum without chambers that participated in the
   original decision.

3. The appeal may be based on:

   - counter-evidence,

   - procedural error,

   - conflict of interest,

   - disproportionate disclosure scope,

   - violation of quorum diversification rules.

---

## 10. Relation to Other Documents

- **`ROOT-IDENTITY-AND-NYMS.en.md`**: this document defines the layers `nym -> node-id -> root-identity`; this act defines who may descend between them and at what threshold.
- **`ABUSE-DISCLOSURE-PROTOCOL.en.md`**: `stake-level`, `evidence-level`, infrastructure sanctions, and legal notifications are the shared basis.
- **`IDENTITY-ATTESTATION-AND-RECOVERY.en.md`**: split knowledge and unsealing must remain consistent with prior-attestation memory and the integrity of `anchor-identity`.
