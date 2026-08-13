# Entrenchment Clause and Constitutional Defense Procedure of DIA

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-ENTRENCH-001` |
| `type` | Implementing act for the Constitution's "Non-Negotiable Core" section and Art. XVI |
| `version` | 0.2.0-draft |
| `basis` | Art. I, II, III, XIV, XVI of the DIA Constitution |

---

## 1. Purpose of the Document

The DIA Constitution itself defines the composition of the non-negotiable core and
the minimum properties of its protection. This document MUST NOT change that
composition. It defines the defense procedure: how to amend the core, submit a
constitutional challenge, and adjudicate a case without creating a permanent
central organ.

---

## 2. Entrenchment Clause

### 2.1. Non-Negotiable Core

The canonical source for the composition of the core is the Constitution's
"Non-Negotiable Core" section together with the machine-readable
`constitution-index.v1.json`. This act refers to clauses by stable identifiers and
MUST NOT maintain parallel quotations of their contents.

The core protects:

- the primacy of dignity, safety, and the passage of system power through the human,
- access to critical goods without systemic violence or humiliation,
- personal agency, locality, export, exit, and fork rights,
- the floor of user rights against operator sovereignty,
- redundant identity unsealing,
- the non-withdrawable UBC minimum,
- automatic expiry of the founding period and limits on founder authority,
- the constitutional hierarchy of values.

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

During the founding period referred to in Constitution Art. XIII.7-12 and Art.
XVI.13, founder decisions retain precedence only outside the non-negotiable core.
Founders MUST NOT suspend, remove, or narrow the protection of the core while
bypassing the procedure in section 2.2.

Every founder decision MUST leave a rationale, impact analysis, date, and scope of
applicability. Automatic expiry of the founding period MUST NOT depend on an ending
act or on consent from the organ whose authority expires.

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

- **Constitution, section "Non-Negotiable Core", and Art. XVI**: the Constitution
  defines the composition of the core and minimum properties of its protection;
  this act defines the procedure.
- **Constitution Art. XIII.7-12 and Art. XVI.13**: precedence of founder decisions
  MUST NOT include changing the core outside its proper procedure.
- **NORMATIVE-HIERARCHY.en.md**: Level 0 follows directly from the Constitution;
  this act is not the source of its composition.
- **Constitution Art. XIV**: interim measures are treated as exceptions subject to
  minimum requirements of identification and expiry.
- **Constitution Art. VII**: the ad-hoc panel is consistent with the principle of
  procedural (not charismatic) governance and separation of roles.
