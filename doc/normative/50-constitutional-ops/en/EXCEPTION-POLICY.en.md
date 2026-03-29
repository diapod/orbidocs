# DIA Exception Policy

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-EXC-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. II, IX, X, XIV, XVI of the DIA Constitution; `AUTONOMY-LEVELS.en.md`; `ENTRENCHMENT-CLAUSE.en.md` |

---

## 1. Purpose of the Document

The Constitution requires every exception to have an identifier, rationale, risk
level, owner, expiry time, and fail-closed return point. This document turns that
principle into an operational procedure: it defines the exception data model,
exception types, the minimum approval path, and monitoring of side effects.

The goal of the exception policy is not to make rules easier to bypass, but to
make the exception a **first-class audit object**.

---

## 2. General Rule

1. An exception is permissible only when it:
   - does not violate the non-negotiable core,
   - is limited in scope and time,
   - has an owner responsible for its effects,
   - has an explicit disable condition,
   - leads to a defined fail-closed state.
2. An exception may not become the default mode or a permanent feature of the
   architecture.
3. An exception MUST NOT suspend the ban on demanding humiliation, self-abasement,
   or emotional dependency as a condition of access to critical goods, help,
   protective procedures, or basic system resources.
4. A frequently repeated exception is a signal that a rule, contract, or new
   operational path is missing.

---

## 3. Minimum Exception Data Model

Every exception MUST contain at least:

```yaml
exception:
  policy_id: "DIA-EXC-001"
  exception_id: "EXC-[federation]-[timestamp]-[nonce]"
  type: "ordinary" # ordinary | emergency | injunction
  owner: "[role or identifier of the responsible node]"
  requester: "[initiator]"
  scope: "[which roles, resources, data, or procedures are covered by the exception]"
  reason: "[business / ethical / safety rationale]"
  risk_level: "medium" # low | medium | high | critical
  constitutional_basis: ["XIV.3", "XIV.4"]
  created_at: "[timestamp]"
  expiry: "[timestamp]"
  fail_closed_target: "[return state]"
  approvals: []
  monitoring:
    metrics: []
    review_at: "[timestamp]"
  rollback_conditions: []
  status: "active" # proposed | active | suspended | expired | rolled_back
```

The fields `approvals`, `monitoring.metrics`, and `rollback_conditions` may not be
empty for exceptions with stakes `high` or `critical`.

---

## 4. Types of Exceptions

### 4.1. Ordinary Exception (`ordinary`)

An exception for situations that are not real-time crises but require a temporary
departure from the default rule.

Examples:

- temporary increase of an agent's cost limit,
- temporary extension of routing scope,
- manual retention of an older component version for compatibility reasons.

### 4.2. Emergency Exception (`emergency`)

An exception activated under time pressure when delay can increase harm or make it
impossible to protect a person.

Examples:

- activation of A3 mode,
- temporary bypass of part of the workflow during a blackout,
- emergency securing of a whistleblower's communication channel.

### 4.3. Protective / Constitutional Exception (`injunction`)

An exception in the form of an interim measure used to suspend an action that may
be unconstitutional or may threaten irreversible harm.

Examples:

- suspension of a federation policy,
- holding publication until a ruling is issued,
- freezing the privileges of a public-trust role.

---

## 5. Approval Procedure

### 5.1. Ordinary Exception

1. The initiator creates an exception record with the full data model.
2. The exception must be approved by at least two roles, one of which is not the
   direct beneficiary of the exception.
3. For `high` and `critical` exceptions, multisig and an explicit indication of
   monitoring metrics apply.
4. After approval, the exception gains the status `active`.

### 5.2. Emergency Exception

1. It may be activated by an operator or automatically by a defined trigger.
2. Activation creates the exception record immediately or no later than together
   with the first action trace.
3. The maximum lifetime of an emergency exception is a federation parameter, but
   after expiry the system MUST return to the fail-closed state.
4. Post-hoc review is mandatory and must begin no later than 72 hours after
   activation, unless the federation is still in crisis mode.

### 5.3. Protective / Constitutional Exception

1. It is activated by an ad-hoc panel or another procedural body authorized by
   the Constitution.
2. It must indicate the irreversible harm that is threatened.
3. It expires automatically after the full ruling or when `expiry` is reached.
4. It may not be extended without a new decision and a new trace of rationale.

---

## 6. Monitoring and Automatic Rollback

Every exception MUST have:

- side-effect indicators,
- a review deadline,
- conditions for automatic suspension,
- conditions for automatic rollback.

An exception MUST be automatically suspended or rolled back if:

1. a signal of harm or abuse associated with the exception appears,
2. the exception exceeds `expiry`,
3. the mandatory review has not been performed,
4. the condition that justified activation has disappeared,
5. the exception begins to function as a permanent architectural backdoor,
6. the exception begins to condition access to help, protective procedures, or
   critical goods on humiliation, self-abasement, or emotional dependency.

---

## 7. Exception Health Metrics

Every federation should measure at least:

- the number of active exceptions per period,
- average lifetime of an exception,
- the percentage of exceptions that are extended,
- the percentage of exceptions that ended in rollback,
- the share of `emergency` and `injunction` exceptions,
- the share of exceptions associated with harm, incident, or appeal.

A high exception rate or its steady increase is a signal that the system is
drifting toward management by exception instead of management by contract.

---

## 8. Relation to Other Documents

- **Constitution Art. XIV**: this document operationalizes the exception data
  model and procedure.
- **`AUTONOMY-LEVELS.en.md`**: A3 activation is an emergency exception.
- **`ENTRENCHMENT-CLAUSE.en.md`**: an interim measure is a protective /
  constitutional exception.
- **`NORMATIVE-HIERARCHY.en.md`**: the exception policy is a Level 3 document.
