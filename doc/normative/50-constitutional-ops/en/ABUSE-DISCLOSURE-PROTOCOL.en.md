# DIA Conditional Disclosure of Accountability for Abuse Protocol

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ABUSE-DISC-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. III.9, Art. X.4-10, Art. XVI.1-3 of the DIA Constitution |
| `date` | 2026-03-12 |

---

## 1. Purpose of the Document

This document defines the conditions, scope, and procedure of conditional disclosure
of accountability for ongoing or severe abuse in DIA. Its purpose is not
investigation of the past as such, but protection of people, the community, and
infrastructure against continued, concealed, or severe harm.

The document specifies:

- threshold for entering a case,
- evidentiary standard,
- roles and co-signing requirement,
- scope of permissible disclosure,
- classes of infrastructure sanctions,
- the relation between infrastructure sanctions and `nym -> node-id` thresholds,
- mode of appeal,
- conditions for legal notification.

---

## 2. Base Principle

1. Without a credible present-day signal, no general investigation of the user's or
   operator's past is conducted.

2. A credible present-day signal includes at least one of the following:
   - continuation of abuse,
   - concealment of traces or evidence,
   - retaliation, intimidation, or attempted deanonymization,
   - a pattern of violence, corruption, or sabotage,
   - persistence of severe abuse effects,
   - continued benefit from earlier abuse.

3. Once the condition in item 2 is met, the system MAY examine the full genesis of
   the case and the entire chain of actions, including historical ones, provided this
   remains related to the case.

4. The greater the governing role, access to sensitive data, or influence over
   others' reputation, routing, and safety, the stricter the accountability standard
   and the longer the permissible assessment horizon.

---

## 3. Stakes and Evidence Thresholds

### 3.1. Stake Level (`stake-level`)

| Level | Meaning | Procedural effect |
| :--- | :--- | :--- |
| `S0` | no meaningful harm or relation to the community | no case |
| `S1` | low harm, no durable effects | observation or local correction |
| `S2` | real harm to procedures, reputation, or individual people | review and possible protective limitations |
| `S3` | severe harm, a pattern of abuse, or significant risk to people or infrastructure | disclosure and infrastructure sanctions may occur |
| `S4` | direct threat to life, health, freedom, or system integrity | immediate isolation and possible legal notification |

### 3.2. Evidence Level (`evidence-level`)

| Level | Meaning | Minimum standard |
| :--- | :--- | :--- |
| `E0` | rumor | no action beyond signal registration |
| `E1` | clue | single signal without independent confirmation |
| `E2` | substantiation | at least two converging signals or one artifact requiring verification |
| `E3` | hard evidence | auditable artifact or two independent sources, one of which is a material trace |
| `E4` | high evidence | multi-source auditable material, coherent in time, authorship, and integrity |

### 3.3. Decision Rules

1. Entering the full history of a case requires at least `S2` and `E2`.

2. Disclosure of identity, facts, or responsibility outside the internal track
   requires at least `S3` and `E3`.

3. Legal notification requires at least `S3` and `E3` if the case concerns a severe
   act violating people, the community, infrastructure, or the integrity of evidence
   or procedures, in particular violence, serious corruption, fraud, theft, extortion,
   retaliation against a whistleblower, deanonymization, or sabotage. For all other
   cases, the default threshold is `S4` and `E3`, unless the applicable law requires a
   lower threshold for mandatory notice.

4. For public-trust roles and operators with access to data or routing, the threshold
   for entering the full history of a case may be lowered to `S2` and `E2`, but the
   threshold for external disclosure remains no lower than `S3` and `E3`.

---

## 4. Roles and Co-Signing Requirement

1. Every case MUST have at least the following roles assigned:
   - `Triage`,
   - `Evidence`,
   - `RedTeam`.

2. External disclosure, `S3+` sanctions, or legal notification require co-signing by
   at least two of the following three roles:
   - `Evidence`,
   - `RedTeam`,
   - `Governance` or `Legal`, if the role exists in the federation.

3. A person with a conflict of interest, dependency relation, personal dispute, or
   financial interest in the case MUST be recused.

4. Absence of the `Legal` role does not block the case, but it does block legal
   notification, unless the federation is under a statutory duty to notify.

5. Descent `nym -> node-id` for infrastructure sanctions is permitted at the
   `U1` threshold defined in `IDENTITY-UNSEALING-BOARD.en.md` and does not yet
   constitute unsealing of `root-identity`.

---

## 5. Case Data Model

Every case MUST have a minimum record:

| Field | Description |
| :--- | :--- |
| `case-id` | stable case identifier |
| `opened-at` | time when the case was opened |
| `present-signal` | type of present-day signal |
| `stake-level` | stakes assessment `S0-S4` |
| `evidence-level` | evidence assessment `E0-E4` |
| `role-risk` | relation of the case to role and power over others |
| `scope-justification` | justification of data scope and retrospection |
| `coi-check` | result of conflict-of-interest check |
| `multisig-by` | roles and people co-signing the decision |
| `disclosure-scope` | disclosure level `D0-D4` |
| `sanction-level` | infrastructure sanction level |
| `appeal-window` | time window for appeal |
| `retention-class` | material retention class |
| `jurisdiction` | potentially applicable jurisdiction |
| `notification-mode` | legal notification mode or `none` |

---

## 6. Disclosure Scope (`disclosure-scope`)

| Level | Meaning |
| :--- | :--- |
| `D0` | no disclosure outside the case team |
| `D1` | internal disclosure with identity redacted |
| `D2` | federation-level disclosure with pseudonymous attribution and risk description |
| `D3` | identifying disclosure inside the community if necessary for protection of people or infrastructure |
| `D4` | identifying disclosure plus legal notification under section 10 |

1. Scope of disclosure MUST be case-related, proportional, and minimal.

2. Disclosure of personal, relational, or lifestyle material without direct relation
   to the assessed abuse is prohibited.

3. The mere fact of holding a public-trust role does not cancel the principle of
   minimal disclosure; it only increases the scope of accountability and the
   requirement of procedural transparency.

---

## 7. Infrastructure Sanctions (`sanction-level`)

| Level | Meaning |
| :--- | :--- |
| `I0` | no sanction |
| `I1` | warning and monitoring |
| `I2` | permission restriction or suspension of a specific function |
| `I3` | reputational quarantine or role suspension |
| `I4` | routing cut-off, federation block, or node isolation |

1. A sanction MUST correspond to `stake-level`, reversibility of harm, and quality of
   evidence.

2. `I4` requires at least `S3`, `E3`, and co-signing under section 4.

3. A sanction may be imposed before external publication if protection of people or
   integrity of evidence requires it.

---

## 8. Retention and Data

1. Case data may be collected only to the extent necessary for signal verification,
   protection of people, preservation of evidence integrity, and performance of legal
   duties.

2. Retention classes:
   - `R0` - dismissed case: 90 days,
   - `R1` - closed case without severe sanction: 2 years,
   - `R2` - case with `I3-I4` sanction: 7 years,
   - `R3` - case under legal hold or legal track: until end of proceedings + 7 years.

3. Material beyond the scope of the case MUST be redacted or deleted without undue
   delay.

4. Data correlates may be used only when their relation to the case is explicitly
   described in `scope-justification`.

---

## 9. Appeal Mode

1. A person covered by disclosure or sanction MUST receive:
   - description of the allegation,
   - information about the evidentiary material to the extent that it does not harm the
     victim, whistleblower, or integrity of the case,
   - deadline and appeal path.

2. Minimum `appeal-window` is 14 days, unless a direct threat requires earlier
   isolation.

3. The appeal is heard by a new composition, excluding people who participated in the
   original decision.

4. An appeal may be based only on:
   - counter-evidence,
   - demonstration of procedural error,
   - demonstration of conflict of interest in the case team,
   - demonstration of disproportionality of disclosure scope.

---

## 10. Jurisdictional Notifications

1. `notification-mode = none` is the default value.

2. Legal notification is permissible only when all of the following hold:
   - the act meets the threshold under section 3.3,
   - an applicable jurisdiction can be indicated,
   - notification does not violate a stronger duty to protect the victim,
     whistleblower, or ongoing proceedings,
   - the decision has been co-signed under section 4.

3. A federation SHOULD prefer the mode of documented transfer of material to the
   competent authority over public announcement if this better protects people and
   case integrity.

4. Every notification MUST leave a trace containing:
   - `jurisdiction`,
   - `legal-basis`,
   - `notified-at`,
   - `notified-by`,
   - `payload-hash`.

---

## 11. Final Principle

This protocol is not for punishing a past biography as such. It is for detecting and
limiting abuse that continues, is being concealed, still benefits the perpetrator, or
remains relevant to the safety of people and the integrity of the community.
