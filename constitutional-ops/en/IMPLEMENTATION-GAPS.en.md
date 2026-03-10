# Implementation Gaps in the DIA Constitutional Layer

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-CONST-GAPS-001` |
| `type` | Architectural review / backlog of implementing documents |
| `version` | 0.1.0-draft |
| `date` | 2026-03-10 |

---

## Purpose of the Document

This document collects the gaps that remain after completion of the Constitution
and the first documents under `constitutional-ops/`. It has no normative force;
it serves to organize the next implementation steps.

---

## Recently Closed

### `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`

Closed on `2026-03-10` by document `DIA-FED-001`, which defines:

- the statuses of active, dormant, suspended, and retired federations,
- the minimum activity criteria,
- electorate snapshot, quorum, and decision classes,
- the rules for losing veto rights by a dead federation.

---

## Priority A - Required Before Real Governance Goes Live

### 1. `PROCEDURAL-REPUTATION-SPEC.en.md`

**Why it is missing:** the ad-hoc panel and role screening assume the existence
of "high procedural reputation," but do not define its components or the method
of calculation.

**What it must define:**

- sources of procedural reputation signals,
- weight of contracts, incidents, appeals, and corrections,
- conditions for lowering and regaining reputation,
- definition of an "active node" for reputation purposes.

### 2. `PANEL-SELECTION-PROTOCOL.en.md`

**Why it is missing:** the constitutional defense procedure assumes panel
selection by drawing, but does not specify the randomness source,
anti-manipulation seeding, or the method for resolving disputes about veto and
eligibility.

**What it must define:**

- source of entropy and its audit,
- eligibility of panelists,
- procedure for exclusions and vetoes,
- retry logic under conflict of interest.

---

## Priority B - Required Before Higher-Stakes Autonomy and Sensorium

### 4. `EMERGENCY-ACTIVATION-CRITERIA.en.md`

**Why it is missing:** the autonomy gradient defines A3, but does not define the
catalog of triggers, minimum confidence thresholds, or rules for allowing
automatic activation.

**What it must define:**

- classes of triggers for A3,
- minimum thresholds of signal credibility,
- relation sensorium -> trigger -> operator,
- default TTLs and mandatory review.

### 5. `SENSITIVE-DATA-REDUCTION.en.md`

**Why it is missing:** publication, whistleblowers, exceptions, and onboarding
refer to redaction of sensitive data, but there is no shared standard of
redaction and disclosure.

**What it must define:**

- classes of sensitive data,
- levels of redaction,
- rules of selective disclosure,
- minimum audit traces without deanonymization.

---

## Priority C - Required Before Federation-Scale Expansion

### 6. `ROLE-REGISTRY.en.md`

**Why it is missing:** the Constitution and supplements use notions such as
"public-trust role," "operator," "red team," and "panel," but they do not have a
shared role registry.

**What it must define:**

- catalog of base roles,
- minimum permissions and forbidden role combinations,
- screening requirements,
- paths of rotation and substitutability.

### 7. `TRACE-MINIMUM.en.md`

**Why it is missing:** agent autonomy, exceptions, reputation, and constitutional
defense require action traces, but they do not yet have a shared minimum schema.

**What it must define:**

- required trace fields,
- relation trace -> audit -> appeal,
- retention classes,
- trace versioning and signatures.

---

## Final Note

The most critical gaps have been partially closed by `EXCEPTION-POLICY.en.md`
and `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`. The next logical step is to
specify **how procedural reputation is calculated** and **how the ad-hoc panel is
drawn**, because without that the governance layer remains philosophically sound
but still too soft operationally in disputed matters.
