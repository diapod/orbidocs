# DIA Agent Autonomy Gradient

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-AUTON-LEVELS-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. II.3-4, II.8, V.10, V.13 of the DIA Constitution |

---

## 1. Purpose of the Document

The Constitution (Art. II.3) requires that "the greatest power of the system pass
through the human." At the same time, Art. V.10 requires an agent to have a kill
switch, limits, and an explicit trust mode. This document defines **four levels of
agent autonomy**, operationalizing these principles without creating a narrow
human-in-the-loop bottleneck for every operation.

The autonomy gradient allows a human to **set the frame**, not click "OK" on every
step. Power passes through the human because the human defines the gradient.

---

## 2. Levels of Autonomy

### A0 - Proposal (Propose & Wait)

| Parameter | Value |
| :--- | :--- |
| **Description** | The agent prepares a proposal. It takes no action without explicit approval from the operator. |
| **Default when** | Decisions that change policies, contracts, permissions, publications, or sensitive data. Any action with irreversible or hard-to-reverse effects. |
| **Reporting** | The proposal is shown to the operator with rationale, options, and risk assessment. |
| **Reversal** | Not applicable - the action was not taken. |
| **Examples** | Editing a public document; changing a node policy; sending a message on behalf of the user; escalating a case; modifying an agent contract. |

### A1 - Act & Notify

| Parameter | Value |
| :--- | :--- |
| **Description** | The agent takes action but immediately informs the operator. The operator can reverse the action within a defined time window. |
| **Default when** | Actions with low risk and high reversibility that require speed but are not routine. |
| **Reporting** | Immediate notification with a description of the action, rationale, and reversal instructions. |
| **Reversal** | Possible within a defined window (default: a federation parameter, e.g. 15 minutes). After the window expires, the action is treated as approved. |
| **Examples** | Routing a task to another node; updating a memarium cache; answering a low-stakes network query; logging a sensorium event. |

### A2 - Act Within Budget

| Parameter | Value |
| :--- | :--- |
| **Description** | The agent acts autonomously within an explicitly defined budget: limits of time, token cost, scope of operations, and number of actions. It reports after the fact. |
| **Default when** | Routine, repeatable operations with a predictable scope and low unit risk. |
| **Reporting** | Aggregate report (periodic or after the budget is exhausted) with metrics: number of actions, cost, deviations from the norm. |
| **Reversal** | Individual actions may be hard to reverse, but the budget limits the scale of harm. |
| **Budget limits** | Defined in the agent contract: `max_cost`, `max_time`, `max_actions`, `scope_whitelist`, `scope_blacklist`. Exceeding any limit -> automatic stop and operator notification. |
| **Examples** | Answering routine queries; aggregating sensorium data; maintaining a memarium index; monitoring node health metrics. |

### A3 - Emergency Mode

| Parameter | Value |
| :--- | :--- |
| **Description** | The agent acts at maximum speed in a situation of direct danger to life or sudden serious harm. It leaves a full trace. Post-hoc review is mandatory. |
| **Activated when** | Only when the conditions of Art. II.8 are met: direct danger to life or sudden, direct, and serious harm to health. |
| **Reporting** | Full, unredacted trace of all actions, stored locally and (if possible) replicated. |
| **Reversal** | Not the priority during the crisis. After the crisis -> mandatory review and possible correction. |
| **Time limits** | A3 mode has a defined maximum duration (a federation parameter). After it expires, the agent automatically returns to level A0 (fail-closed). |
| **Activation** | Automatic (based on sensorium signals or crisis-pattern detection) or manual (operator). Automatic activation requires a separate confirmation in the log. |
| **Examples** | Coordinating aid during a blackout; alert about threat to life; first-contact medical triage; securing a whistleblower's communication channel under direct threat. |

---

## 3. Rules for Assigning Levels

### 3.1. Agent Contract

Each agent declares in its contract (Art. V.10):

```yaml
autonomy:
  max_level: A2           # Maximum level the agent is designed for
  default_level: A1       # Default level at startup
  emergency_capable: true # Whether the agent is capable of A3
  budget:
    max_cost_tokens: 1000
    max_time_seconds: 3600
    max_actions_per_cycle: 50
    scope_whitelist:
      - "memarium.read"
      - "memarium.index"
      - "sensorium.aggregate"
    scope_blacklist:
      - "policy.modify"
      - "reputation.vote"
      - "publish.*"
```

### 3.2. The Operator May Lower, Never Raise

A node operator may set an agent to a **lower** level than the contract's
`max_level`. The operator may not set a higher one. Example: an agent with
`max_level: A2` may be restricted to A0, but an agent with `max_level: A1`
may not receive A2.

Rationale: autonomy level is an architectural constraint, not a convenience
parameter. An agent designed for A1 does not have the budget mechanisms required
by A2.

### 3.3. A Federation May Tighten

A federation may impose a `max_level` lower than the agent contract (e.g. in
`CORP_COMPLIANT` mode all agents are A0). It may not weaken the limits from the
contract.

### 3.4. Escalation Upward

An agent may not escalate its own level of autonomy (**zero self-authorize**,
consistent with Art. V.13). Escalation requires:

- **A0 -> A1 or A2**: operator decision.
- **Any -> A3**: operator or automatic crisis detection with an explicit log entry
  and mandatory post-hoc review.
- **A3 -> return**: automatic after expiration of the time limit (fail-closed to
  A0).

---

## 4. Matrix: Operation Type x Autonomy Level

The table below is the default. Federations may tighten it (move left), but may
not loosen it (move right).

| Operation category | Minimum level | Rationale |
| :--- | :--- | :--- |
| Policy / contract change | A0 | Irreversible, affects governance |
| Publication / external communication | A0 | High reputational stakes |
| Reputation vote | A0 | Affects trust routing |
| Modification of sensitive data | A0 | Privacy, dignity |
| Scoped privacy-preserving memory visibility change | contextual | May be delegated only when the operator has already approved the scope, subject, and reversal/audit model |
| Routing a task to another node | A1 | Reversible, but requires awareness |
| Updating cache / index | A2 | Routine, budgetable |
| Answering a routine query | A2 | Routine, budgetable |
| Sensorium aggregation | A2 | Routine, budgetable |
| Protection of life / crisis triage | A3 | Art. II.8 |

### 4.1. Remembered Operator Approvals

A0 means that human will is required before an action is taken. It does not
always require a fresh prompt for every occurrence of the same bounded action.
The operator may express that will as a remembered approval policy, analogous to
an agent whitelist, when all of the following are explicit:

- who may act (participant, agent, module, or operator-local identity),
- what class of data or action is covered,
- which autonomy level and budget apply after approval,
- how the decision is audited,
- how the approval can be revoked.

Example: `memarium.forget` is not one social action. Personal immediate forget
may be delegated to a privacy agent for a bounded subject and artifact class.
Public tombstone, community forget, and crisis-space forget remain governed or
operator-reviewed because they affect shared memory, public accountability, or
constitutional minimum material.

---

## 5. Audit and Monitoring

### 5.1. Decision Traces

Each action of an agent, regardless of level, generates a log entry with at
least:

- timestamp,
- `autonomy_level` at the moment of the action,
- `action_type`,
- `scope` (which resources were used),
- `cost` (if measurable),
- `justification` (for A1 and A3 - explicit; for A2 - available on request).

### 5.2. Budget Review (for A2)

An agent operating at A2 generates a budget report containing:

- usage of the cost limit (%),
- usage of the time limit (%),
- number of actions vs. limit,
- deviations from the norm (anomalies).

The report is available to the operator on request and is generated
automatically when >=80% of any limit is exhausted.

### 5.3. Post-Hoc Review (for A3)

After A3 ends, a review is mandatory and includes:

- the full action trace,
- assessment of whether A3 activation was adequate (whether the threat was real),
- assessment of proportionality of the actions taken,
- identification of side effects,
- recommendations for calibration of activation thresholds.

The review is documented and available for audit.

---

## 6. Relation to Other Documents

- **Constitution Art. II.3-4**: The autonomy gradient operationalizes the
  principle that "power passes through the human."
- **Constitution Art. V.10**: Autonomy levels extend the agent contract with an
  explicit `autonomy_level` parameter.
- **Constitution Art. V.13**: This document concretizes the ban on agents
  independently escalating privileges.
- **Constitution Art. IX**: A3 mode is the formalization of Art. II.8 and Art.
  IX.3.
- **Constitution Art. XIV**: Every use of A3 is a constitutional exception, even
  if it has a simplified activation path due to time pressure.
