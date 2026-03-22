# DIA Unsealing Case Model

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-UNSEAL-CASE-001` |
| `type` | Implementing act / data model |
| `version` | 0.1.0-draft |
| `date` | 2026-03-12 |

---

## 1. Purpose

This document defines the minimal shared `unseal_case` model for `U1-U3`
procedures, so that the evidentiary, appeal, and audit tracks speak one common
language of data.

It does not replace the thresholds or competencies defined in
`IDENTITY-UNSEALING-BOARD.en.md`, `ABUSE-DISCLOSURE-PROTOCOL.en.md`, and
`PANEL-SELECTION-PROTOCOL.en.md`; it gives them a shared case structure.

---

## 2. Scope

The `unseal_case` model covers:

- requests to descend `nym -> node-id`,

- requests to descend `node-id -> custodian_ref`,

- requests to descend `node-id -> root-identity`,

- appeals, reviews, and expiry of such decisions,

- minimal fields required for traceability, retention, and notifications.

---

## 3. Definitions

1. `unseal_case`

   A procedural case in which a participant or body requests descent from a more
   shielding identity layer to a less shielding one.

2. `requested_scope`

   The requested descent scope: `node_id`, `custodian_ref`, or `root_identity`.

3. `requestor_ref`

   The procedural identifier of the requesting party.

4. `affected_ref`

   The identifier of the affected party at the layer currently known to the
   system, such as `nym_id` or `node_id`.

5. `case_state`

   The lifecycle state of the case: `draft`, `submitted`, `screened`, `active`,
   `decided`, `appealed`, `stayed`, `expired`, `closed`.

---

## 4. Rules

1. Every unsealing case MUST have a single stable `case_id`.

2. Every case MUST declare `requested_scope` and `current_known_scope`.

3. Every case MUST point to its constitutional and implementing basis.

4. Every case MUST distinguish between:

   - signals,

   - indications,

   - evidence,

   - decisions,

   - enforcement effects.

5. Changing scope from `U1` to `U2` or `U3` MUST create a new decision in the same
   case, rather than overwrite history.

6. A case MUST have an explicit `appeal_window` and `expiry` if the decision is
   time-bounded.

---

## 5. Minimal Data Model

```yaml
unseal_case:
  case_id: "[stable case identifier]"
  policy_id: "DIA-UNSEAL-CASE-001"
  constitution_basis:
    - "Art. III"
    - "Art. X"
  source_documents:
    - "IDENTITY-UNSEALING-BOARD.en.md"
    - "ABUSE-DISCLOSURE-PROTOCOL.en.md"
  requested_scope: "[node_id | custodian_ref | root_identity]"
  current_known_scope: "[nym | node_id | custodian_ref]"
  case_state: "[draft | submitted | screened | active | decided | appealed | stayed | expired | closed]"
  requestor_ref: "[requestor procedural identifier]"
  affected_ref:
    kind: "[nym | node_id]"
    value: "[identifier]"
  federation_ref: "[federation identifier or null]"
  jurisdiction_refs:
    - "[jurisdiction identifier]"
  stake_level: "S2"
  evidence_level: "E2"
  current_signal:
    summary: "[brief summary of present signal]"
    observed_at: "[ISO 8601]"
    continuity_claim: false
  evidence_bundle_refs:
    - "[evidence bundle reference]"
  decision_refs:
    - "[decision reference]"
  sanction_refs:
    - "[sanction reference]"
  legal_notice_refs:
    - "[reference or []]"
  coi_check_ref: "[COI check reference]"
  panel_ref: "[panel or FSC quorum reference]"
  created_at: "[ISO 8601]"
  updated_at: "[ISO 8601]"
  appeal_window:
    opens_at: "[ISO 8601]"
    closes_at: "[ISO 8601]"
  expiry: "[ISO 8601 | null]"
  retention_profile: "[short | medium | long | legal_hold]"
```

---

## 6. Decisions Within the Case

Each case decision MUST be a separate record:

```yaml
decision_record:
  decision_id: "[decision identifier]"
  case_ref: "[case_id]"
  threshold_applied: "[U1 | U2 | U3]"
  outcome: "[approved | denied | partial | stayed]"
  scope_granted: "[node_id | custodian_ref | root_identity | none]"
  rationale: "[brief rationale]"
  signer_refs:
    - "[role or body]"
  decided_at: "[ISO 8601]"
  appealable_until: "[ISO 8601]"
  side_effect_refs:
    - "[sanction / notification / block]"
```

---

## 7. Retention Rules

1. An `unseal_case` MUST have a retention profile adequate to its stakes and
   effects.

2. Cases closed with denial and no further effects SHOULD have shorter retention
   than cases closed at `U2` or `U3`.

3. A `U3` decision record MUST be covered by at least `legal_hold` retention or an
   equivalent secured archive mode.

---

## 8. Relations to Other Documents

- `IDENTITY-UNSEALING-BOARD.en.md` defines thresholds `U1-U3` and competent bodies.

- `ABUSE-DISCLOSURE-PROTOCOL.en.md` defines the conditions for entering a case and
  the range of permitted disclosures.

- `PANEL-SELECTION-PROTOCOL.en.md` defines how a panel is formed if the case does
  not go directly to the `FSC`.

- `TRACE-MINIMUM.pl.md`, once created, should unify the minimal trace for
  `unseal_case` and `decision_record`.
