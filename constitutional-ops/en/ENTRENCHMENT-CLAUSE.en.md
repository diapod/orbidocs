# Entrenchment Clause and Constitutional Defense Procedure of DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ENTRENCH-001` |
| `type` | Proposed supplement to Constitution Art. XVI |
| `version` | 0.1.0-draft |
| `basis` | Art. I, II, III, XIV, XVI of the DIA Constitution |

---

## 1. Purpose of the Document

The DIA Constitution declares its precedence over all other documents, policies,
and decisions (section "Normative Force and Interpretation", point 4). However,
it does not define:

- which articles are immutable (the non-negotiable core),
- what happens when a majority of federations wants to break the Constitution,
- who decides constitutional challenges and by what procedure.

This document closes those gaps by proposing an entrenchment clause and a minimal
defense procedure - without creating a permanent central organ.

---

## 2. Entrenchment Clause

### 2.1. Non-Negotiable Core

The following Constitution articles form the **non-negotiable core**:

| Article | Core content |
| :--- | :--- |
| **I.5** | No operational or financial goal may override the primacy of dignity, human safety, and the right to exit. |
| **II.1** | Human dignity is a supreme and non-negotiable value. |
| **II.2** | Protection of life and defense against direct, sudden, and serious harm to health have the highest operational priority. |
| **II.3** | The greatest power of the system MUST pass through the human, not around the human. |
| **III.1** | The user remains the owner of their data, policies, agents, and local memory spaces. |
| **III.2** | The system MUST operate meaningfully in local-first, offline, and self-hosted modes. |
| **III.3** | Export of data, policies, and histories MUST be possible in open formats. |
| **III.4** | The right to exit without coercion, without loss of access to data, without hidden penalties. |
| **III.5** | The right to fork. |
| **XIV.1** | Default hierarchy of values: dignity > sovereignty > verifiability > agency > effectiveness > convenience. |

### 2.2. Conditions for Amending the Non-Negotiable Core

Amending, suspending, removing, or narrowing the interpretation of any article in
the non-negotiable core requires **simultaneous** fulfillment of all the following
conditions:

1. **Unanimity of federations** - consent of all federations participating in the
   amendment process. One federation = one veto. No vote is not treated as
   consent.

2. **Independent adversarial review** - a red-team panel composed of at least
   three nodes with high procedural reputation, not being initiators of the
   change and having no conflict of interest regarding the subject of the change.
   The panel publishes a public rationale in support or opposition.

3. **Reflection period** - at least 90 days between formal submission of the
   proposal and the vote. During this period the proposal is publicly available
   and every node may submit counter-arguments.

4. **Impact analysis** - a written analysis covering: predicted effects on dignity,
   safety, sovereignty, and the right to exit; abuse scenarios; reversibility
   conditions.

5. **Transparency of the process** - the full trace of the decision process
   (proposal, arguments, counter-arguments, votes, rationales) is permanently
   archived and publicly accessible.

### 2.3. What the Entrenchment Clause Does Not Block

The entrenchment clause does not prevent:

- amendment of Constitution articles **outside** the non-negotiable core
  (procedure from Art. XVI),
- tightening the core (adding new guarantees),
- **expansive** reinterpretation of the scope of protection,
- creation of new articles so long as they do not weaken the core.

### 2.4. Founding Period

During the founding period referred to in Constitution Art. XIII.7-11 and Art.
XVI.10, the mechanism of federation unanimity and the ordinary blocking paths may
not paralyze founder decisions concerning the shape of the system, its
architecture, launch-order rules, and the text of the Constitution.

This does not suspend publicity or traceability. Every such decision MUST leave a
rationale, impact analysis, date, and scope of applicability. After the founding
period ends, the full procedure from section 2.2 applies without exception.

---

## 3. Constitutional Defense Procedure

### 3.1. Constitutional Challenge

Every federation, every node with the status of swarm citizen (Art. XV), and
every public-trust role may submit a **constitutional challenge** against:

- a federation policy,
- a governance decision,
- an implementing act,
- an action of a node, agent, or role,
- a proposal to amend the Constitution.

The submission must contain:

```yaml
constitutional_challenge:
  challenger_id: [identifier of the challenger]
  target: [identifier of the challenged document / decision / action]
  articles_violated: [list of Constitution articles]
  reasoning: [rationale - why the target violates the cited articles]
  evidence: [references to evidence]
  urgency: [normal | elevated | critical]
  date: [timestamp]
```

### 3.2. Ad-Hoc Panel (Instead of a Permanent Constitutional Court)

DIA does not create a permanent adjudicating organ - that would be a form of
centralization inconsistent with Art. VII. Instead:

**Panel appointment:**

1. After accepting the submission, the system draws **3 or more nodes** from the
   pool of nodes meeting the criteria:
   - high procedural reputation (not technical - Art. VII.4),
   - no conflict of interest with the subject of the case (COI-by-default, Art.
     VII.6),
   - no ties to the parties in the dispute.

2. The parties to the dispute may each raise **one veto** against the drawn nodes
   (with rationale), after which the draw is repeated for the rejected slots.

3. The panel works collegially; decisions are made by majority vote.

**Panel work:**

1. The panel has **30 days** to issue a ruling (`critical` mode - 7 days).
2. The panel examines conformity of the target with the Constitution, using the
   Sources of Interpretation (Level 2 of the normative hierarchy) and the rules
   of interpretation from the section "Normative Force and Interpretation."
3. The panel publishes a **rationale** containing: facts, legal analysis, ruling,
   and any recommendations.

**Effects of the ruling:**

- The ruling is **binding** until formal amendment of the Constitution.
- The ruling **does not create binding precedent** - each case is considered anew.
  This protects against "constitutional drift" through accumulation of
  interpretations.
- If the panel finds unconstitutionality, the target is **suspended** to the
  extent of the violation until repair or formal amendment of the Constitution.

### 3.3. Interim Measure (`injunction`)

In matters marked `critical` - when delay may cause irreversible harm - the
challenger may request an **interim measure**:

1. The request must indicate what harm is irreversible and why.
2. The decision on the interim measure is taken by **2 of 3** drawn panel members
   within **48 hours**.
3. The interim measure **suspends** the challenged action until the full ruling.
4. The interim measure is itself tracked as a constitutional exception and must
   contain `reason`, `risk-level`, `expiry`, and `owner`, in accordance with
   Constitution Art. XIV.

### 3.4. Appeal

A party dissatisfied with the ruling may file an appeal within 14 days. The
appeal is considered by a **new panel** (drawn again, excluding previous
members). The ruling of the second panel is final.

---

## 4. Threat Scenarios and System Responses

| Scenario | System response |
| :--- | :--- |
| Majority of federations votes to remove the right to exit | Entrenchment clause: requires unanimity + adversarial review + 90 days of reflection. One federation blocks. |
| Sponsor forces reinterpretation of Art. VIII through a federation policy | Constitutional challenge -> ad-hoc panel -> policy suspension. |
| Group of nodes tries to dominate the panel selection pool | COI-by-default criteria + party vetoes + procedural reputation (not technical) constrain capture. |
| Panel issues a biased ruling | Appeal to a new panel. Absence of binding precedent means a biased ruling does not permanently shape interpretation. |
| Crisis mode (Art. IX) is used to bypass the Constitution | Crisis mode does not suspend the non-negotiable core. Mandatory post-hoc review. |

---

## 5. Relation to Other Documents

- **Constitution Art. XVI**: This document is a proposed supplement to Art. XVI
  with points concerning the non-negotiable core and the defense procedure.
- **Constitution Art. XIII.7-11 and Art. XVI.10**: the founding period has
  procedural precedence over the full inter-federation path until its time clause
  expires.
- **NORMATIVE-HIERARCHY.en.md**: the entrenchment clause defines Level 0 of the
  hierarchy.
- **Constitution Art. XIV**: interim measures are treated as exceptions subject to
  minimum requirements of identification and expiry.
- **Constitution Art. VII**: the ad-hoc panel is consistent with the principle of
  procedural (not charismatic) governance and separation of roles.
