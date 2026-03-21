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

### `PROCEDURAL-REPUTATION-SPEC.en.md`

Closed on `2026-03-12` by document `DIA-PROC-REP-001`, which defines:

- reputation domains and signal types,
- the definition of an active node for reputation purposes,
- bootstrap and bootstrap restrictions,
- a portable evidence package instead of naked score transfer,
- cartel-detection hooks and connection to health metrics M1-M5.

### `PANEL-SELECTION-PROTOCOL.en.md`

Closed on `2026-03-12` by document `DIA-PANEL-SEL-001`, which defines:

- panelist eligibility,
- entropy source and auditable panel draw,
- COI, veto, and composition-replacement procedure,
- escalation to an inter-federation pool,
- panelist identity-disclosure levels and relation to appeal.

### `ABUSE-DISCLOSURE-PROTOCOL.en.md`

Closed on `2026-03-12` by document `DIA-ABUSE-DISC-001`, which defines:

- prohibition on general investigation without a credible present-day signal,
- conditions for entering the full case history,
- `stake-level` and `evidence-level` thresholds,
- multisig roles, disclosure scope, retention, appeal, and jurisdictional notifications.

### `ROOT-IDENTITY-AND-NYMS.en.md`

Closed on `2026-03-12` by document `DIA-ROOT-ID-001`, which defines:

- the separation of `root-identity`, `anchor-identity`, `node-id`, `nym`, `station-id`, and `agent-id`,
- identity assurance levels (`IAL0`-`IAL4`),
- the rule "greater influence -> greater disclosure and stronger confirmation",
- a multisig attestation model for jurisdictions without strong eID,
- limits on multiplying influence through many nyms from one anchor source.

### `IDENTITY-ATTESTATION-AND-RECOVERY.en.md`

Closed on `2026-03-12` by document `DIA-ID-REC-001`, which defines:

- first attestation of `root-identity`,
- memory of prior attestation for `anchor-identity`,
- the role of the recovery phrase, `salt`, and KDF parameters,
- reconstruction of `anchor-identity` without repeated full attestation,
- the procedure for identity-data update and revocation.

### `ATTESTATION-PROVIDERS.en.md`

Closed on `2026-03-12` by document `DIA-ATTEST-PROVIDERS-001`, which defines:

- the attestation-strength classes `weak` / `strong`,
- the default mapping from methods to maximum `IAL`,
- restrictions for phone numbers and other low-evidence sources,
- `weak -> strong` upgrade rules without loss of anchor continuity.

### `IDENTITY-UPGRADE-ANOMALY-SIGNALS.en.md`

Closed on `2026-03-12` by document `DIA-ID-UPGRADE-ANOM-001`, which defines:

- signal classes `A1-A8` for attestation upgrade,
- minimum response levels `monitor`, `soft_hold`, `manual_review`, `hard_block`,
- the default profile for `phone -> strong`,
- the relation between attestation upgrade and procedural dispute.


### `IDENTITY-UNSEALING-BOARD.en.md`

Closed on `2026-03-12` by document `DIA-SEAL-BOARD-001`, which defines:

- the Federation of Sealed Chambers as a redundant IRL organ,
- thresholds `U1-U3` for descent `nym -> node-id -> root-identity`,
- multi-chamber and cross-jurisdictional quorum,
- split knowledge for mapping `node-id -> root-identity`,
- appeal from full-unsealing decisions.

### `UNSEAL-CASE-MODEL.en.md`

Closed on `2026-03-12` by document `DIA-UNSEAL-CASE-001`, which defines:

- a shared `unseal_case` model for thresholds `U1-U3`,
- a separate decision record with scope, side effects, and appeal window,
- minimal fields for retention, COI, panel, and notifications,
- the rule that scope escalation does not overwrite case history.

### `ROLE-TO-IAL-MATRIX.en.md`

Closed on `2026-03-12` by document `DIA-ROLE-IAL-001`, which defines:

- the minimum map from role classes to `IAL0-IAL4`,
- the rule that `IAL` is mainly a gate, not an influence multiplier,
- the `fixed_power_bonus` cap of `<= 1%`,
- default minimums for panels, sealed chambers, and high-stake roles.

### `FIP-MEMBERSHIP-AND-QUORUM.en.md`

Closed on `2026-03-12` by document `DIA-FIP-QUORUM-001`, which defines:

- chamber statuses from `candidate` to `retired`,
- minimum conditions for `active` status,
- default quorum `2 of 3` for `U2` and `3 of 5` for `U3`,
- emergency mode, composition snapshot, and jurisdictional diversity rules.

### `SWARM-ECONOMY-SUFFICIENCY.en.md`

Closed on `2026-03-21` by document `DIA-SUFF-001`, which defines:

- the operational model of the sufficiency threshold and tapering band,
- permissible classes of concentration brakes and the anti-pyramid test,
- the minimal data model of federation economic policy,
- common circulation of surpluses and their destination classes,
- the barrier between economic reward and procedural power.

---

## Priority A - Required Before Real Governance Goes Live

After closing `PROCEDURAL-REPUTATION-SPEC.en.md`,
`PANEL-SELECTION-PROTOCOL.en.md`, and `ABUSE-DISCLOSURE-PROTOCOL.en.md`,
there is currently no open Class A gap. The minimum governance layer now has the
three implementing acts that were previously missing.

---

## Priority B - Required Before Higher-Stakes Autonomy and Sensorium

### 1. `EMERGENCY-ACTIVATION-CRITERIA.en.md`

**Why it is missing:** the autonomy gradient defines A3, but does not define the
catalog of triggers, minimum confidence thresholds, or rules for allowing
automatic activation.

**What it must define:**

- classes of triggers for A3,
- minimum thresholds of signal credibility,
- relation sensorium -> trigger -> operator,
- default TTLs and mandatory review.

### 2. `SENSITIVE-DATA-REDUCTION.en.md`

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

### 3. `ROLE-REGISTRY.en.md`

**Why it is missing:** the Constitution and supplements use notions such as
"public-trust role," "operator," "red team," and "panel," but they do not have a
shared role registry.

**What it must define:**

- catalog of base roles,
- minimum permissions and forbidden role combinations,
- screening requirements,
- paths of rotation and substitutability.

### 4. `TRACE-MINIMUM.en.md`

**Why it is missing:** agent autonomy, exceptions, reputation, and constitutional
defense require action traces, but they do not yet have a shared minimum schema.

**What it must define:**

- required trace fields,
- relation trace -> audit -> appeal,
- retention classes,
- trace versioning and signatures.

---

## Final Note

The most critical gaps of the governance layer have been closed by
`EXCEPTION-POLICY.en.md`, `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md`,
`PROCEDURAL-REPUTATION-SPEC.en.md`, `PANEL-SELECTION-PROTOCOL.en.md`, and
`ABUSE-DISCLOSURE-PROTOCOL.en.md`. The next logical step is to specify
**emergency activation criteria**, **sensitive-data redaction**, and the
**minimum action-trace schema**, so the implementing layer is equally coherent
outside disputes and governance.
