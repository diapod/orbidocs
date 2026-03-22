# Sybil Challenges in Federated Knowledge Exchange and Reputation

Based on: `doc/project/30-stories/story-001.md`, `doc/project/50-requirements/requirements-001.md`  
Date: `2026-02-22`  
Status: Draft

## Executive Summary

In the Story 001 protocol, Sybil attacks can target discovery, offer selection,
arbitration, settlement, and reputation updates. The core risk is that one adversary
controls many pseudonymous nodes and biases outcomes while appearing decentralized.

A realistic defense requires layered controls:
- identity-cost controls (make identity creation non-trivial),
- evidence-quality controls (trust first-hand signed receipts over claims),
- market controls (anti-collusion and anti-spam in offer flow),
- governance controls (arbiter independence, dispute paths),
- ingestion controls (do not let low-trust content poison memory/model training).

No single mechanism is sufficient on its own.

## Context and Problem Statement

Story 001 defines a flow where nodes:
- publish question envelopes and discover offers on the event layer,
- execute selected interactions in bounded room or execution paths,
- settle outcomes through explicit procurement contracts and receipts,
- update reputation based on interaction quality.

This architecture is open and pseudonymous by design, which improves participation but also enables Sybil behavior:
- identity multiplication,
- collusive reputation farming,
- channel flooding,
- consensus capture around arbitration.

The problem is to preserve openness while making manipulation economically, operationally, and statistically expensive.

## Proposed Model / Decision

Adopt a **layered Sybil-resistance model** where each layer contributes partial protection and failure in one layer does not fully compromise the system.

### 0. Baseline Direction (Evidence-first with optional economic anchors)

Decision direction:
- Make the anti-Sybil core **evidence-first**: influence is weighted by independent
  completed interactions, counterparty diversity, and bounded identity-cost controls,
  not raw node count.
- Treat stake, bonds, deposits, or similar scarcity mechanisms as **optional future
  trust tiers**, not as the required starting point of the protocol.
- Keep Tor-inspired mechanisms as a **future advisory layer**: topology/family/anomaly
  heuristics can down-rank suspicious behavior but do not replace receipt-backed
  reputation evidence.

Practical rule:
- New or low-evidence nodes can participate in low-trust discovery, but cannot
  accumulate high-impact reputation weight until independent completed interactions
  and diversity checks are present.

Classification:
- Fact: Story 001 now uses explicit contracts and signed receipts as core trust
  evidence.
- Inference: evidence-first weighting is the most natural extension of that trust
  plane before introducing stronger economic anchors.

### 1. Threat Surfaces (mapped to Story 001)

| Surface | Story/Req Reference | Sybil Risk | Classification |
|---|---|---|---|
| Public discovery request/offer stage | Story steps 14-15, FR-010/FR-011 | One actor spawns many nodes and floods fake offers to steer selection. | Inference |
| Offer scoring and selection | Story step 16, FR-012 | Colluding identities create synthetic diversity and manipulate score ranking. | Inference |
| Private execution channel | Story step 16, FR-013/FR-014 | Adversary controls both responder and "independent" observers. | Inference |
| Contract and confirmation mode | Story step 19, FR-016 | Attackers exploit no-confirmation/self-confirmation modes to farm trust cheaply. | Inference |
| Settlement and receipts | Story step 21, FR-018 | Self-dealing or collusive receipts are used as fake quality signals. | Inference |
| Reputation update | Story step 22, FR-019, NFR-008 | Reputation inflation through collusive loops and whitewashing. | Fact (risk is explicitly called out), Inference (attack method) |

### 2. System-Shaping Countermeasures (protocol and governance design)

| Countermeasure | What It Changes in System Shape | Why It Helps | Cost / Trade-off |
|---|---|---|---|
| **Reputation from first-hand settled receipts only** | Reputation engine accepts only signed `SettlementReceipt` evidence tied to `contract_id`. No gossip-only score updates. | Removes most low-cost fake reputation narratives. | Slower bootstrapping for honest new nodes. |
| **Progressive trust cap for new identities** | New node score is capped until it completes a minimum number of independent interactions over time. | Limits instant reputation jumps from identity swarms. | Friction for legitimate newcomers. |
| **Identity-cost anchor (optional / future)** | Introduce refundable stake, bond, deposit, or other scarcity mechanism per active node identity or offer stream, with explicit trust tiers if later adopted. | Makes mass-identity attacks materially costly without forcing the early product to become a crypto-native operator. | Participation barrier; governance needed for thresholds; product and regulatory complexity if done too early. |
| **Counterparty diversity requirement** | Reputation gain is discounted when interactions repeat within the same trust cluster. | Reduces collusive farming rings. | Requires graph analytics and cluster heuristics. |
| **Arbiter independence constraints** | Arbiter cannot share trust cluster or frequent-collusion history with selected responder. | Lowers chance of single-operator capture. | More complex matching and occasional latency. |
| **Offer admission throttling** | Per-identity and per-cluster rate limits at discovery channels. | Mitigates flood/spam and ranking pressure. | Possible false positives during bursts. |
| **Minimum evidence fields in offers** | Enforce structured offer schema plus signed node key and timestamp windows. | Rejects malformed/bot noise early. | Additional validation overhead. |
| **Reputation decay + anti-whitewash hysteresis** | Decay stale trust, but require stronger evidence to regain trust after identity reset patterns. | Makes throwaway identity rotation less effective. | Harder tuning; potential fairness concerns. |
| **Tor-style advisory heuristics (secondary)** | Add non-binding heuristics inspired by Tor operations (family detection, path/topology correlation, synchronized behavior flags) as risk signals in scoring. | Improves detection of coordinated clusters that pass pure stake gates. | Heuristic false positives; requires transparent tuning and appeals workflow. |

### 3. Runtime Countermeasures (operational layer)

| Control | Description | Classification |
|---|---|---|
| Anomaly detection on offer graph | Detect sudden fan-out/fan-in patterns, near-identical bids, and synchronized behavior windows. | Inference |
| Abuse-aware scoring penalties | Add score penalties for correlated identities and repeated mutual settlement loops. | Inference |
| Challenge-response tasks | For suspicious nodes, require bounded verifiable task completion before high-value selection. | Speculation (requires design validation) |
| Canary queries | Inject known-answer prompts to estimate reliability drift for low-trust cohorts. | Speculation |
| Slow-start execution rights | Limit max transaction value and concurrency for low-age identities. | Inference |

### 4. Knowledge Ingestion Guardrails (to prevent Sybil-driven knowledge poisoning)

- Only `confirmed` or policy-approved `corrected` outcomes may enter trusted vector memory by default.
- `unresolved` outcomes must be quarantined from default retrieval context.
- Training queue ingestion must require provenance completeness (`source_node`, `contract_id`, outcome status).
- High-impact updates should require either arbiter confirmation or repeated independent agreement.

Classification: Inference (derived from Story 001 steps 22-24 and requirement traceability needs).

## Trade-offs

1. Openness vs Sybil friction:
   - stronger entry friction improves safety,
   - but reduces spontaneous participation.
2. Fast procurement vs trust quality:
   - strict independence and validation improve reliability,
   - but increase latency and operational complexity.
3. Privacy vs anti-abuse observability:
   - private channels protect content,
   - but reduce available signals for anomaly analysis.
4. Optional economic anchors vs inclusiveness:
   - stake/deposit can discourage attack swarms if later adopted,
   - but can exclude low-resource honest participants and add operator/regulatory scope.
5. Local autonomy vs protocol rigidity:
   - local policy freedom supports experimentation,
   - but can fragment trust semantics across the federation.

## Failure Modes and Mitigations

| Failure Mode | Impact | Mitigation |
|---|---|---|
| Colluding Sybil ring dominates offers in one specialization channel | Biased node selection and degraded answer quality | Cluster-aware rate limits, diversity constraints, and correlated-score penalties. |
| Reputation farming through zero-price samples | Rapid fake trust growth with low economic cost | Cap trust gain from zero-price interactions and require independent paid/arbited confirmations for higher trust tiers. |
| Arbiter capture by related identities | Fraudulent settlements appear legitimate | Arbiter independence rules, random arbiter sampling from disjoint pools, and dispute replay audits. |
| Whitewashing (identity reset after abuse) | Attackers evade penalties and restart trust accrual | Anti-whitewash hysteresis, cooldown windows, and stronger re-entry requirements. |
| Poisoned knowledge propagated to local memory/training | Long-term degradation of assistant quality | Quarantine unresolved outcomes and require provenance + consensus thresholds before promotion. |
| Adversary targets low-liquidity periods | Temporary control of channel outcomes | Time-window normalization in scoring and delayed finalization for low-sample windows. |

## Open Questions

1. Do we need any economic identity-cost layer in the early product at all, or should independent receipt history carry the first trust tier?
2. If we later add deposits or bonds, what trust-tier policy should be canonical (`unbonded` limits, `bonded-low` limits, `bonded-full` privileges)?
3. What trust-cluster signal should be canonical for independence checks (graph overlap, shared counterparties, timing correlation)?
4. Should arbiter selection be deterministic, random, or hybrid per contract value/risk class?
5. What is the exact formula for diminishing returns on repeated interactions with the same counterparties?
6. Which Tor-inspired advisory signals should be included first without overfitting or unfairly penalizing honest nodes?
7. How should privacy-preserving telemetry be designed to support Sybil detection without exposing query content?

## Next Actions

1. Define a `ReputationEvidence` schema anchored to procurement receipts and contract provenance.
2. Define the minimal evidence-first trust tiers for early product scope, and describe optional future economic anchors separately.
3. Add formal scoring rules for counterparty diversity and correlated-identity penalties.
4. Define arbiter independence policy and disjoint-pool selection algorithm.
5. Add protocol-level rate limits for offer admission in discovery channels.
6. Specify Tor-inspired advisory signals and integrate them as non-binding risk multipliers in scoring.
7. Define ingestion policy gates for vector memory and training queue (`confirmed/corrected/unresolved`).
8. Create adversarial test scenarios for Sybil swarms, collusion rings, arbiter capture, and later optional deposit-funded coordinated clusters.
