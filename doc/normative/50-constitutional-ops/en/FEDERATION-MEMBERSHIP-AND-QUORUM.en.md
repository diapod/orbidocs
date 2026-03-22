# DIA Federation Membership and Quorum

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-FED-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. VI.6, VII.10, XIII.6, XV, XVI of the DIA Constitution; `ENTRENCHMENT-CLAUSE.en.md`; `NORMATIVE-HIERARCHY.en.md` |

---

## 1. Purpose of the Document

The Constitution and the entrenchment clause operate on the notion of a
"federation," but without an operational definition of federation status,
voting rights, and quorum rules, the system remains vulnerable to two
pathologies:

- **deadlock through dead federations** - lack of response is mistaken for a real
  veto,
- **capture through multiplication of facade federations** - one center of control
  tries to artificially increase the number of votes.

This document defines the minimum model of federation membership, federation
statuses, activity criteria, quorum rules, and rules for loss of voting and veto
rights.

---

## 2. General Principles

1. In inter-federation governance, only **voting-eligible federations** count.
2. **One active voting-eligible federation = one vote**. Capital, node count,
   traffic, revenue, computing power, or infrastructure position do not increase
   vote weight.
3. Voting and veto rights arise from **living procedural responsibility**, not
   from the historical fact that a federation once existed.
4. How a position is produced **inside** a federation is a matter of local policy,
   but the external vote MUST leave a trace, an owner of the process, and a
   signature of the proper role or roles.
5. Federations under **common control** may not multiply influence merely through
   organizational partition. In high-stakes and constitutional matters they are
   treated as **one voting block** until they demonstrate genuine procedural
   independence.

---

## 3. Minimum Federation Record

Every federation participating in inter-federation governance MUST publish at
least the following record:

```yaml
federation_record:
  federation_id: "FED-[slug]"
  status: "candidate" # candidate | active | dormant | suspended | retired
  governance_endpoint: "[URI or channel for receiving formal decisions]"
  fallback_contact: "[backup channel]"
  governance_keys: []
  policy_refs: []
  heartbeat_at: "[timestamp]"
  last_notice_ack_at: "[timestamp]"
  last_governance_action_at: "[timestamp]"
  declared_common_control: []
  effective_from: "[timestamp]"
  owner_roles: []
  status_reason: "[reason for the current status]"
```

The minimum federation record is an audit object. Absence of a current record
means there is no basis to retain `active` status.

---

## 4. Federation Statuses

| Status | Meaning | Voting right | Veto right |
| :--- | :--- | :--- | :--- |
| `candidate` | Federation registered, interoperable, in the entry or probationary period | no | no |
| `active` | Federation procedurally alive and eligible to participate in inter-federation governance | yes | yes, if the given procedure provides for it |
| `dormant` | Federation temporarily inactive, non-responsive, or failing activity criteria | no | no |
| `suspended` | Federation temporarily excluded from voting because of an incident, injunction, or another procedural decision | no | no |
| `retired` | Federation sunset or one that explicitly left governance | no | no |

The statuses `candidate`, `dormant`, `suspended`, and `retired` are not an
ontological punishment: a federation may still exist, route traffic, or provide
local services, but it does not participate in inter-federation vote counting
until it regains qualification.

---

## 5. Criteria for Obtaining and Retaining `active` Status

A federation obtains or retains `active` status only when it jointly:

1. publishes a current federation record,
2. has a functioning `governance_endpoint` and `fallback_contact`,
3. has sent a valid heartbeat within the `heartbeat_ttl` window,
4. has acknowledged at least one formal notice or performed at least one
   auditable governance action within the `activity_ttl` window,
5. is not covered by an active procedural suspension,
6. is not in an unresolved common-control dispute requiring aggregation of its
   vote with another federation.

A `candidate` status may be raised to `active` after all the above conditions are
met and the probation period `candidate_min_age` has ended.

---

## 6. Status Transitions

### 6.1. `candidate` -> `active`

Transition occurs after:

1. publishing the minimum federation record,
2. at least one valid heartbeat,
3. at least one acknowledgement of a formal notice,
4. completion of the probation period.

### 6.2. `active` -> `dormant`

Transition occurs automatically or procedurally when at least one of the
following conditions appears:

1. heartbeat expired,
2. the federation failed to acknowledge `missed_notice_limit` consecutive formal
   notices,
3. `governance_endpoint` and `fallback_contact` are unavailable for the full
   notice window,
4. the federation record is stale or inconsistent and was not repaired within the
   remediation window.

### 6.3. `active` or `dormant` -> `suspended`

Transition occurs when:

1. there is an active interim measure or injunction,
2. there is a security incident concerning governance keys,
3. there is a hard signal of capture, false identity representation, or
   manipulation of the voting process.

### 6.4. `dormant` or `suspended` -> `active`

Reactivation requires:

1. a fresh federation record,
2. a fresh heartbeat,
3. confirmation of the ability to receive notices,
4. removal of the cause of suspension or dormancy,
5. a reactivation trace with `reason` and `effective_from`.

### 6.5. `dormant` -> `retired`

Transition occurs after exceeding `retired_after` or through an explicit
statement of exit from inter-federation governance.

---

## 7. Voting-Eligible Federation

For the purposes of quorum and veto counting, a **voting-eligible federation** is
exclusively a federation that:

- has status `active`,
- is included in the electorate snapshot created at the opening of the given
  decision process (`electorate_snapshot`),
- has not been grouped with another federation into a single voting block due to
  common control.

The electorate snapshot MUST contain:

```yaml
electorate_snapshot:
  decision_id: "[identifier of the process]"
  created_at: "[timestamp]"
  eligible_federations: []
  grouped_blocks: []
  quorum_base: 0
  decision_class: "ordinary" # ordinary | high_stake | entrenched_core
```

Once the snapshot is created, the quorum base for that process does not change.
Changes of federation status affect **subsequent** processes; they do not
recalculate a process already opened.

---

## 8. Decision Classes and Quorum

### 8.1. Basic Rule

Silence is not a vote. `abstain` counts toward quorum, but not toward the
`yes/no` majority, unless a given procedure states otherwise.

### 8.2. Decision Classes

| Decision class | Quorum | Condition for adoption |
| :--- | :--- | :--- |
| `ordinary` | at least `floor(N/2) + 1` voting blocks from the snapshot | more `yes` than `no` |
| `high_stake` | at least `ceil(2N/3)` voting blocks from the snapshot | at least `ceil(2N/3)` explicit `yes` votes |
| `entrenched_core` | `N` out of `N` voting blocks from the snapshot | every eligible `active` must cast an explicit `yes`; `no`, `abstain`, or silence means lack of consent |

Interpretation:

- `N` means the number of voting blocks in the electorate snapshot,
- a voting block may represent one federation or a group of federations covered
  by the common-control rule,
- if `N = 0`, the inter-federation process may not be opened,
- this document does not remove the additional requirements from
  `ENTRENCHMENT-CLAUSE.en.md`; it only defines **who** counts toward unanimity.

---

## 9. Timeouts and Minimum Parameters

The parameters below are defaults and may be tightened by federations, but may
not be weakened below the indicated minimum:

| Parameter | Default | Minimum / maximum |
| :--- | :--- | :--- |
| `heartbeat_ttl` | 30 days | max 45 days |
| `activity_ttl` | 90 days | max 120 days |
| `candidate_min_age` | 30 days | min 14 days |
| `missed_notice_limit` | 2 | min 2 |
| `notice_window` | 7 days | min 72 hours |
| `ordinary_vote_window` | 14 days | min 7 days |
| `high_stake_vote_window` | 30 days | min 14 days |
| `retired_after` | 180 days | min 90 days |

A federation may be more cautious, but it may not keep "active" federations
without a heartbeat for half a year or reduce the entry period to zero.

---

## 10. Loss of Veto Right by a Dead Federation

1. A federation that does not have `active` status at the moment the electorate
   snapshot is created **has no veto right**.
2. A federation that lost `active` status does not block subsequent
   constitutional or ordinary processes merely because it historically belonged
   to the federation set.
3. A federation that remains silent in a process requiring unanimity may block
   **that concrete process** if it was `active` in the snapshot, but after
   crossing `missed_notice_limit` it moves to `dormant` and loses veto in later
   processes.
4. An explicit exit from inter-federation governance acts immediately for the
   future: the federation moves to `retired` and is no longer counted toward
   quorum.

The rule is simple: **veto belongs to living responsibility, not to its shadow**.

---

## 11. Common Control and Vote Multiplication

The following count at minimum as signals of common control:

- a shared governance key,
- the same dominant decision-making role,
- the same source of funding or the same entity able to unilaterally force
  decisions,
- lack of real separation of trace, responsibility, and appeals procedure.

If there is a credible dispute about common control:

1. the federations are temporarily grouped into one voting block in matters of
   `high_stake` and `entrenched_core`,
2. the dispute is tracked as a COI-by-default problem,
3. restoration of separate votes requires proof of procedural separateness.

This rule does not serve to build a center. It serves to prevent capital or an
organizational apparatus from buying itself additional votes by multiplying
facades.

---

## 12. Relation to Other Documents

- **Constitution Art. VI.6 and VII.10**: this document operationalizes federated
  growth without loss of local autonomy and scaling through local accountability.
- **Constitution Art. XIII.6**: federation statuses implement procedures of
  sunset, handover, and archiving.
- **Constitution Art. XVI**: the document defines the quorum base and the
  participants of amendment and enforcement processes.
- **`ENTRENCHMENT-CLAUSE.en.md`**: the document specifies which federations count
  toward unanimity and veto.
- **`NORMATIVE-HIERARCHY.en.md`**: the federation membership and quorum policy is a
  Level 3 document.
