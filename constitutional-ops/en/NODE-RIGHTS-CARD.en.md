# DIA Node Rights and Duties Card

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-NODE-CARD-001` |
| `type` | Extract from the Constitution - onboarding material |
| `version` | 0.1.0-draft |
| `source` | Art. II, III, XV, XVI of the DIA Constitution |

---

## Your Rights as a Node

| Right | What it means | Constitution |
| :--- | :--- | :--- |
| **Right to exit** | You may leave the federation at any time, without coercion, without losing access to your own data, and without hidden penalties. | Art. III.4 |
| **Right to privacy** | Telemetry is off by default. Your data is local. Disclosure is selective and as a rule requires your consent, with a procedural exception for ongoing or severe abuse under Art. III.9 and Art. X. | Art. III.7, III.8, III.9, Art. X |
| **Right to inspect** | You can audit your agents' interactions, decision traces, and action histories. | Art. XV.2 |
| **Right to appeal** | You may challenge any reputation decision or sanction through an appeals procedure. | Art. XV.2, XVI.2 |
| **Right to safety** | The system protects you against harassment, doxxing, sabotage, and economic coercion. | Art. XV.2 |
| **Right to local autonomy** | You may run a "quiet" node: privately, locally, without participating in public spaces. | Art. III.6 |
| **Right to fork** | You may copy specifications, policies, and open components without asking a center for permission. | Art. III.5 |
| **Right to data sovereignty** | You are the owner of your data, policies, agents, and local memory spaces. Export in open formats is guaranteed. | Art. III.1, III.3 |

## Your Duties as a Node

| Duty | What it means | Constitution |
| :--- | :--- | :--- |
| **Do no harm** | Do not take actions intentionally harmful to people, infrastructure, or the integrity of memory and evidence. | Art. XV.4 |
| **Be epistemically honest** | Mark speculation. Do not falsify evidence. Do not manipulate reputation. | Art. XV.3 |
| **Cooperate at the protocol level** | Respect contracts, protocol versions, and limits. | Art. XV.3 |
| **Maintain operational hygiene** | Take care of keys, updates, and basic node security. | Art. XV.3 |
| **Be ready to help** | Within your means, without an obligation of transactional settlement. | Art. XV.3 |

## Hierarchy of Values (When Values Conflict)

```text
Human dignity and safety
  > Sovereignty and privacy
    > Verifiability and transparency
      > Agency and autonomy
        > Effectiveness and optimization
          > Convenience and aesthetics
```

Source: Art. XIV.1. In case of conflict at the same level, the tests of
reversibility, proportionality, and publicity apply (Art. XIV.2).

## Enforcement Is Graduated

```text
Warning -> Restriction of privileges -> Reputational quarantine -> Routing cutoff
```

Every sanction leaves a trace, provides a path of appeal, and opens a route back
after repair (Art. XVI.1-2).

---

**Full Constitution:** `../CONSTITUTION.en.md`  
**Values and interpretation:** `../core-values/CORE-VALUES.en.md`  
**Project vision:** `../VISION.pl.md`  
**Agent autonomy gradient:** `AUTONOMY-LEVELS.en.md`

---
---

# Decision Index - From Situation to Article

The table below maps the most common operational situations to the relevant
articles of the Constitution and key principles. It serves as a "router" - it does
not replace reading the Constitution, but it helps locate the right norm quickly.

## User Rights and Sovereignty

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 1 | The user wants to take their data and leave | III.3, III.4 | Export in open formats, without coercion or hidden penalties |
| 2 | The user wants to run a node offline | III.2, III.6 | The system MUST work meaningfully local-first and self-hosted |
| 3 | The user wants to fork the project | III.5 | Right to fork: specifications, policies, open components |
| 4 | Someone enabled telemetry without the user's consent | III.7 | Telemetry is off by default; it requires clear, revocable consent |

## Agents and Autonomy

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 5 | An agent made a decision without the user's knowledge | II.3, II.4, V.10 | Power passes through the human; proposals and options are the default |
| 6 | An agent exceeded budget / time / scope | V.10, AUTONOMY-LEVELS.en.md | An agent MUST have a kill switch and limits on permissions, time, and cost |
| 7 | An agent escalated its own permissions | V.13, AUTONOMY-LEVELS.en.md | Zero self-authorize; an agent error may not automatically escalate privileges |
| 8 | An agent acts in a life-threatening situation | II.8, IX.3, AUTONOMY-LEVELS.en.md | It MAY act faster, but it leaves a trace and is subject to review |

## Funding and Capture

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 9 | A sponsor demands privileged access to data | VIII.2 | Prohibited - funding does not buy access to data, routing, or governance |
| 10 | One dependency became critical (model, infra, funding) | VIII.5 | Mandatory diversification plan |
| 11 | Tension between funding and constitutional integrity | VIII.7 | Constitutional integrity takes precedence |
| 12 | Revenue model based on addicting the user | VIII.3, II.7 | Dopamine-driven UX and retention-based economics are prohibited |

## Reputation and Governance

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 13 | A node challenges a reputation decision | XV.5, XVI.2 | Counter-evidence or demonstration of procedural error; right to appeal |
| 14 | Failure to disclose a conflict of interest | VII.6 | COI-by-default: no declaration = no data, not no conflict |
| 15 | A person simultaneously acts as party and arbiter | VII.3 | Critical powers MUST be separated across roles |
| 16 | A high-stakes decision | VII.9 | Multisig + independent red team |

## Safety and Crisis

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 17 | Suspected Sybil / DoS / prompt injection | IX.1, IX.2 | Threat modeling is part of the architecture, not decoration |
| 18 | Crisis situation (blackout, conflict) | IX.3, IX.4 | Crisis mode: higher rigor, redundancy, locality, trace quality |
| 19 | Node partially cut off from the network | IX.5 | A node SHOULD preserve the ability to operate in partial isolation |
| 20 | Need for emergency cache (shelter, food, triage) | IX.6, IX.7 | Memarium may maintain crisis spaces |

## Whistleblowers and Publication

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 21 | Someone wants to report abuse anonymously | X.1, X.2 | Default anonymity, metadata minimization, signal triage |
| 22 | A whistleblower is exposed to retaliation | X.3 | Swarm care is part of the infrastructure, not a moral gesture |
| 23 | A credible signal of ongoing or concealed severe abuse appears | III.9, X.4-X.8 | No general investigation without a present-day signal; once the threshold is met, full case history, infrastructure sanctions, and appeal procedure become possible |
| 24 | Publication of high-stakes material is under consideration | X.10 | Adversarial review, evidence thresholds, redaction of sensitive data |
| 25 | Escalation of corrective actions | X.9 | Stepwise: verification -> correction -> notice -> audit -> publication |

## Changes and Exceptions

| # | Situation | Articles | Principle / Action |
| :--- | :--- | :--- | :--- |
| 26 | Someone proposes an exception to a rule | XIV.3, XIV.4 | An exception requires: policy-id, reason, risk-level, expiry, owner, fail-closed |
| 27 | An exception generates signals of harm or abuse | XIV.5 | Automatic suspension of the exception until clarification |
| 28 | A proposal to amend the Constitution | XIII.7-XIII.11, XVI.5, XVI.6, XVI.10 | Explicit rationale, impact analysis, reversibility; during the founding period, the founders' decision has decisive force |
| 29 | A local policy tries to bypass the Constitution | XVI.7 | Impermissible without a formal constitutional amendment |
