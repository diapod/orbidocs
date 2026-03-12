# Federation of Sealed Chambers - Membership and Quorum

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-FIP-QUORUM-001` |
| `type` | Implementing act / membership and quorum |
| `version` | 0.1.0-draft |
| `date` | 2026-03-12 |

---

## 1. Purpose

This document defines the minimal rules of membership, activity, and quorum in
the Federation of Sealed Chambers (`FSC`), so that the unsealing track does not
rely on a single body or an accidental group of jurisdictionally adjacent chambers.

---

## 2. Relation to the General Federation

The `FSC` is a special-purpose federation. It does not replace the general
federation rules from `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`, but adds extra
requirements for bodies that want to participate in `U2-U3` unsealing.

If a conflict arises, the stricter requirements prevail for the `FSC`.

---

## 3. Chamber Statuses

A chamber may have the status:

- `candidate`,

- `active`,

- `restricted`,

- `suspended`,

- `retired`.

### 3.1. `candidate`

The chamber is undergoing screening, does not participate in `U3` quorum, and may
participate only in observational or test capacity.

### 3.2. `active`

The chamber meets activity, jurisdictional diversity, and security requirements.
It may participate in `U2-U3` quorum.

### 3.3. `restricted`

The chamber remains operational but has temporarily narrowed competencies, for
example only for `U2` or without the right to serve as lead chamber.

### 3.4. `suspended`

The chamber is temporarily excluded from quorum due to conflict of interest,
retaliation, suspected capture, or loss of operational capacity.

### 3.5. `retired`

The chamber has been withdrawn from the federation; it does not participate in new
cases, but may remain part of audits of earlier cases.

---

## 4. Minimal Conditions for `active` Status

1. at least `min_members = 3` qualified chamber members,

2. each of them has `IAL4`,

3. the chamber has IRL jurisdictional standing or a comparable legal contract,

4. the chamber maintains a secure intake channel and custody of secret shares,

5. the chamber passes periodic procedural audit,

6. the chamber is not under the dominant control of a single entity that also
   controls other chambers in the given quorum.

---

## 5. Quorum

### 5.1. For `U2`

The default quorum is `2 of 3` `active` or `restricted` chambers, of which at least:

- one chamber does not come from the requestor federation,

- one chamber does not come from the jurisdiction of the affected party.

### 5.2. For `U3`

The default quorum is `3 of 5` `active` chambers, with:

- at least three different jurisdictions,

- at least two different federations,

- no single controlling organization supplying more than one chamber to the quorum.

### 5.3. Emergency Mode

If `3 of 5` quorum cannot be formed, an emergency `3 of 4` mode is allowed, but
only if:

- one or more chambers are `suspended` due to retaliation, outage, or force majeure,

- diversity of at least three jurisdictions remains preserved,

- the decision is automatically flagged for ex post review.

---

## 6. Snapshot of Composition and Conflicts

1. Every `U2-U3` case MUST have an `fip_snapshot_id`.

2. The composition snapshot MUST freeze the list of eligible chambers at the time
   quorum is built.

3. A chamber with conflict of interest is excluded from the case, but does not
   thereby automatically lose global `active` status.

---

## 7. Minimal Data Model

```yaml
fip_chamber_record:
  chamber_id: "[chamber identifier]"
  status: "[candidate | active | restricted | suspended | retired]"
  federation_ref: "[federation identifier]"
  jurisdiction_ref: "[jurisdiction identifier]"
  qualified_member_refs:
    - "[IAL4 member identifier]"
  capabilities:
    can_lead_u2: true
    can_lead_u3: true
    can_hold_secret_share: true
  last_audit_at: "[ISO 8601]"
  suspension_reason: null
```

```yaml
fip_snapshot:
  fip_snapshot_id: "[snapshot identifier]"
  case_ref: "[case_id]"
  eligible_chambers:
    - "[chamber_id]"
  excluded_chambers:
    - chamber_id: "[identifier]"
      reason: "[COI | suspended | unreachable]"
  created_at: "[ISO 8601]"
```

---

## 8. Relations to Other Documents

- `IDENTITY-UNSEALING-BOARD.en.md` defines the role of the `FSC` and `U2-U3`
  thresholds.

- `ROLE-TO-IAL-MATRIX.en.md` defines the minimum `IAL4` for chamber members.

- `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md` remains the general federation act, but
  the `FSC` is its specialized tightening.
