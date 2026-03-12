# DIA Panel Selection Protocol

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-PANEL-SEL-001` |
| `type` | Implementing act (Level 3 of the normative hierarchy) |
| `version` | 0.1.0-draft |
| `basis` | Art. VII.1-3, VII.6, XVI.3 of the DIA Constitution; `ENTRENCHMENT-CLAUSE.en.md` section 3.2; `PROCEDURAL-REPUTATION-SPEC.en.md`; `ROOT-IDENTITY-AND-NYMS.en.md` |
| `mechanism status` | `[mechanism - hypothesis]` for VRF entropy; eligibility and procedural rules are normative |

---

## 1. Purpose of the Document

The Constitution requires ad-hoc panels for constitutional challenges
(ENTRENCHMENT-CLAUSE 3.2), high-stakes disputes (Art. XVI.3), and adversarial
review (Art. VII.9). However, no specification exists for **how panelists are
selected** from the eligible pool.

This document defines:

- the eligibility criteria for panel service,
- the minimum identity-assurance level for panelists,
- the entropy source and draw mechanism,
- the veto procedure,
- escalation when the eligible pool is insufficient,
- identity disclosure levels for panelists,
- panel dissolution and replacement rules,
- the timeline for panel proceedings.

---

## 2. Design Principles

1. **Uniform draw, not reputation-weighted**. Reputation is a qualification gate,
   not a selection weight. Within the eligible pool, every node has an equal
   probability of selection. Reputation-weighted selection would create a de facto
   judiciary class, inconsistent with Art. VII.1 (governance without priests).

2. **COI-by-default** (Art. VII.6). Absence of conflict-of-interest disclosure
   means absence of data, not absence of conflict. The burden of proof lies with
   the candidate, not the challenger.

3. **Separation of roles** (Art. VII.3). A node may not simultaneously be a party,
   arbiter, and oracle in the same matter. A panelist who discovers a role conflict
   during proceedings MUST recuse immediately.

4. **Entropy over authority**. The draw seed is generated collectively; no single
   node controls the selection outcome.

5. **Proportional disclosure**. Identity exposure scales with the need: full for
   audit, pseudonymous for parties, opaque for the public.

---

## 3. Eligibility Criteria

A node is eligible for panel selection if **all** of the following hold:

| Criterion | Requirement | Source |
| :--- | :--- | :--- |
| Procedural reputation | `procedural.score >= panel_procedural_threshold` (default: 0.6) | `PROCEDURAL-REPUTATION-SPEC` section 13 |
| Identity assurance level | `assurance_level >= panel_identity_assurance_threshold` (default: `IAL3`) | `ROOT-IDENTITY-AND-NYMS` sections 7 and 8 |
| Active status | `status = active` (not `bootstrapping`, `inactive`, or `suspended`) | `PROCEDURAL-REPUTATION-SPEC` section 5 |
| Bootstrap complete | `bootstrap_remaining_days = 0` | `PROCEDURAL-REPUTATION-SPEC` section 7.3 |
| No COI | Passes the COI check for the specific case (section 4) | Art. VII.6 |
| No role conflict | Not a party, requester, target, or oracle in the same matter | Art. VII.3 |
| No prior service | Has not served on a panel in the same case (including appeal) | Section 11 |
| Federation membership | Is a member of the adjudicating federation (or the inter-federation pool, see section 8) | `FEDERATION-MEMBERSHIP-AND-QUORUM` |

Procedural reputation is therefore necessary but not sufficient. A node with high
reputation but too low an `IAL` level does not qualify for a high-stakes panel.

### 3.1. COI Check Procedure

1. Before draw, every node in the eligible pool receives a **blinded case
   summary** (parties anonymized, subject described at category level).

2. Each node MUST declare within `coi_declaration_window` (default: 24 hours;
   4 hours for `critical` cases):
   - "no conflict" (with cryptographic attestation), or
   - "conflict exists" (with category but not detail), or
   - no response (treated as undeclared COI -- node is excluded).

3. Nodes declaring conflict or failing to respond are excluded from the draw for
   that case. Non-response generates a negative `procedural` signal
   (`governance_inaction`) in `PROCEDURAL-REPUTATION-SPEC`.

4. A post-selection COI discovery triggers panel dissolution for the affected
   member (section 10).

### 3.2. Identity-Assurance Gate

1. Before selection, every panel candidate MUST disclose to the system its current
   `assurance_level` and a reference to its anchoring attestation.

2. For ordinary high-stakes panels, the default minimum level is `IAL3`.

3. For panels that may:

   - decide on identifying disclosure,

   - enter a legal-notification track,

   - adjudicate the highest-stakes cases involving public-trust roles,

   the federation SHOULD require `IAL4`.

4. Parties do not automatically receive panelists' root identities. `IAL` is an
   eligibility gate, not a mode of full disclosure.

---

## 4. Entropy Source and Draw Mechanism `[hypothesis]`

The draw uses a Verifiable Random Function (VRF) with a commit-reveal scheme to
prevent manipulation of the selection seed.

### 4.1. Commit Phase

1. After the eligible pool is established, all eligible nodes are invited to
   participate in seed generation.

2. Each participating node generates a random nonce and submits a commitment:
   `H(nonce || node_id)`.

3. Commitment window: `commit_window` (default: 24 hours; 4 hours for `critical`
   cases).

4. Minimum participation: at least `min_commit_participants` (default: 5) nodes
   must commit for the draw to proceed. Below this, see section 8 (escalation).

### 4.2. Reveal Phase

1. After the commit window closes, all committed nodes reveal their nonce.

2. Reveal window: `reveal_window` (default: 12 hours; 2 hours for `critical`
   cases).

3. Non-revealed commitments: the node is excluded from the draw, and a negative
   `procedural` signal (`protocol_violation`) is generated. The revealed nonces
   proceed without the missing ones.

4. If the number of revealed nonces drops below `min_commit_participants`, the
   draw restarts with a new commit phase.

### 4.3. Seed Construction

The draw seed is computed as:

```
seed = VRF_prove(
  sk_draw_coordinator,
  H(challenge_hash || heartbeat_hash || sort(revealed_nonces))
)
```

Where:

- `challenge_hash` = hash of the constitutional challenge record,
- `heartbeat_hash` = hash of the most recent federation heartbeat (provides
  temporal anchoring),
- `sort(revealed_nonces)` = lexicographically sorted concatenation of all
  revealed nonces,
- `sk_draw_coordinator` = signing key of the designated draw coordinator (a
  rotating role, not a permanent office).

The VRF proof is published alongside the seed, allowing any node to verify that
the seed was correctly derived.

### 4.4. Selection from the Pool

1. The eligible pool (post-COI exclusion) is sorted by a deterministic canonical
   order (e.g., lexicographic `node_id`).

2. The seed is used to generate `panel_size` (default: 3) + `reserve_count`
   (default: 2) indices via a deterministic PRNG seeded with the VRF output.

3. The first `panel_size` indices are the primary panelists; the remaining
   `reserve_count` are alternates.

4. The entire draw is reproducible: any node with the VRF proof and the eligible
   pool list can verify the selection.

---

## 5. Panel Composition

### 5.1. Default Composition

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `panel_size` | 3 | Minimum. Federations may increase (odd numbers only). |
| `reserve_count` | 2 | Alternates for veto replacements and attrition. |
| `max_panel_size` | 7 | Upper bound. More is not better; it increases coordination cost. |

### 5.2. Quorum

A panel is quorate when at least `ceil(panel_size / 2) + 1` members are active
(attending and participating). Loss of quorum triggers replacement from
alternates or, if alternates are exhausted, a partial redraw (section 10).

### 5.3. Decision Rule

Decisions are by simple majority vote. In case of a tie (even-sized panel after
attrition), the panel MUST request one additional member from the alternates or
a partial redraw. A tie is not resolved by a casting vote.

---

## 6. Veto Procedure

### 6.1. Right to Veto

Each party to the dispute may raise **one veto** against a drawn panelist.

### 6.2. Veto Process

1. After the panel composition is announced, each party has `veto_window`
   (default: 48 hours; 12 hours for `critical` cases) to exercise or waive
   their veto.

2. A veto MUST include a written justification. The justification is recorded
   but the right itself is unconditional: a party does not need to prove bias.

3. A vetoed panelist is replaced by the next alternate. If alternates are
   exhausted, a partial redraw (section 10.3) occurs for the vetoed slot.

4. Vetoed panelists receive no negative reputation signal. Being vetoed is not a
   procedural failing.

### 6.3. Limits

- Maximum one veto per party per panel composition.
- A veto may not be used against an alternate until that alternate replaces a
  primary member.
- Repeated veto abuse (pattern of vetoing to delay proceedings) may be flagged
  as a procedural signal, but this requires a separate determination by the
  panel itself.

---

## 7. Timeline

| Phase | Normal | Critical | Notes |
| :--- | :--- | :--- | :--- |
| COI declaration | 24h | 4h | Section 3.1 |
| Commit phase | 24h | 4h | Section 4.1 |
| Reveal phase | 12h | 2h | Section 4.2 |
| Veto window | 48h | 12h | Section 6.2 |
| **Total selection** | **~5 days** | **~1 day** | From challenge acceptance to seated panel |
| Panel deliberation | 30 days | 7 days | From seating to ruling |
| Interim measure | -- | 48h | From request to decision (2/3 panelists) |
| Appeal filing | 14 days | 7 days | From ruling publication |

All timelines are federation parameters. The rule "more cautious yes, more
permissive no" applies: federations may extend timelines but may not shorten
them below the defaults.

---

## 8. Escalation for Insufficient Pool

When the eligible pool is too small for a fair draw, the following tiers
activate in sequence:

### Tier 1: Threshold Relaxation

Lower `panel_procedural_threshold` by one step (e.g., 0.6 -> 0.5). Re-check
eligibility. This may be done at most once.

### Tier 2: Inter-Federation Pool

Request eligible nodes from allied federations. Inter-federation panelists:

- must meet the same COI and role-conflict criteria,
- receive a `foreign_panelist` designation in the proceedings record,
- are subject to the same disclosure rules (section 9),
- generate `procedural` signals in their home federation.

### Tier 3: Small Federation Override

For federations with fewer than `min_federation_pool_size` (default: 10)
eligible nodes:

- the panel is composed from the inter-federation pool by default,
- a local observer (non-voting) is added for federation context,
- the observer has no veto and no vote but may submit written context.

### Tier 4: Governance Escalation

If no panel can be composed after Tiers 1-3:

- the case is escalated to inter-federation governance,
- a temporary governance panel is formed from at least three federations,
- the escalation is recorded as a governance gap signal.

---

## 9. Identity Disclosure Levels

Panelist identity is disclosed at three levels, corresponding to three
audiences:

### 9.1. Audit Level (Full Disclosure)

Available to: designated auditors, appeals panels, and (if required) legal
proceedings.

Contents:

- full `node_id` and `custodian_ref`,
- COI declaration and attestation,
- VRF proof and draw verification data,
- cryptographic signature on the ruling.

`custodian_ref` does not automatically mean disclosure of `root-identity`. If
procedural integrity requires going below the `node-id` layer, the panel uses
the unsealing track defined in `ROOT-IDENTITY-AND-NYMS.en.md`.

### 9.2. Parties Level (Procedural Pseudonyms)

Available to: parties to the dispute.

Contents:

- procedural pseudonym (cryptographic, unique per case),
- role in the panel (presiding, member, alternate),
- COI exclusion basis (category, not detail),
- reputation domain score range (e.g., "above threshold"), not exact score.

### 9.3. Public Level (Opaque)

Available to: any observer.

Contents:

- number of panelists and alternates,
- confirmation that COI check was performed,
- procedural pseudonyms (non-linkable across cases),
- hash of the panel composition record,
- ruling and rationale (attributed to the panel as a body, not individuals).

### 9.4. Disclosure Override

In cases involving Art. X.4-X.8 (conditional disclosure of accountability for
abuse), the panel MAY decide to increase the disclosure level for specific
panelists if:

- the panelist is found to have an undisclosed COI related to the abuse,
- the increase is case-related, proportional, and limited (Art. III.9),
- the decision is co-signed by at least two panelists.

This override does not grant blanket deanonymization; it applies only to the
extent necessary for procedural integrity.

---

## 10. Panel Dissolution and Replacement

### 10.1. Grounds for Individual Replacement

A panelist is replaced when:

| Ground | Detection | Consequence |
| :--- | :--- | :--- |
| Post-selection COI discovery | Self-disclosure, party challenge, or audit | Immediate recusal; replacement from alternates |
| Inactivity timeout | No response within `inactivity_timeout` (default: 48h; 12h for `critical`) | Replacement from alternates |
| Collusion evidence | Signal from monitoring or party report | Replacement + negative `procedural` signal |
| Voluntary recusal | Panelist's own declaration | Replacement from alternates; no negative signal |

### 10.2. Individual Replacement Procedure

1. The affected slot is filled by the next unused alternate.
2. If all alternates are exhausted, a partial redraw (section 10.3) occurs.
3. The replacement panelist inherits the case materials but reviews them
   independently.
4. The timeline is extended by `replacement_extension` (default: 7 days;
   2 days for `critical`) to allow the replacement to review.

### 10.3. Partial Redraw

A partial redraw follows the same commit-reveal procedure (section 4) but only
for the vacated slot(s). The existing panelists are excluded from the pool.

### 10.4. Full Redraw

A full redraw (dissolution and reconstitution of the entire panel) occurs only
when:

- more than 50% of the panel composition is compromised (COI, collusion, or
  inactivity), or
- a systemic integrity concern makes the proceedings unreliable.

A full redraw resets the deliberation timeline. The previous panel's work
product is available to the new panel as reference but is not binding.

---

## 11. Relation to Appeal Procedure

The appeal panel (ENTRENCHMENT-CLAUSE 3.4) is composed using the same protocol,
with one additional constraint:

- **No prior service**: nodes that served on the original panel are excluded
  from the appeal pool.

All other rules (eligibility, COI, veto, escalation, disclosure) apply
identically.

---

## 12. Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Entropy manipulation | Commit-reveal with VRF proof; non-reveal penalized; seed requires collective input |
| Hidden COI | Post-selection COI discovery triggers replacement + severe `procedural` negative signal; Art. III.9 ensures privacy does not shield abuse |
| Veto abuse for delay | Maximum one veto per party; replacement is immediate from alternates |
| Small federation capture | Inter-federation pool fallback (Tier 2-3); local observer for context without vote |
| Panelist goes silent | Inactivity timeout with automatic replacement; timeline extension for replacement review |
| Collusion between panelists | Monitoring signals; collusion evidence triggers replacement and `procedural` sanction |
| Draw coordinator manipulation | VRF proof is publicly verifiable; coordinator is a rotating role |
| Insufficient eligible nodes globally | Tier 4 governance escalation; recorded as governance gap |

---

## 13. Federation Parameters

| Parameter | Default | Allowed range | Rule |
| :--- | :--- | :--- | :--- |
| `panel_size` | 3 | 3-7, odd only | More cautious yes, more permissive no |
| `reserve_count` | 2 | >= 2 | " |
| `panel_procedural_threshold` | 0.6 | >= 0.5 | " (shared with `PROCEDURAL-REPUTATION-SPEC`) |
| `panel_identity_assurance_threshold` | `IAL3` | `IAL2`-`IAL4` | " (shared with `ROOT-IDENTITY-AND-NYMS`) |
| `coi_declaration_window` | 24h | >= 12h | " |
| `coi_declaration_window_critical` | 4h | >= 2h | " |
| `commit_window` | 24h | >= 12h | " |
| `commit_window_critical` | 4h | >= 2h | " |
| `reveal_window` | 12h | >= 6h | " |
| `reveal_window_critical` | 2h | >= 1h | " |
| `min_commit_participants` | 5 | >= 3 | " |
| `veto_window` | 48h | >= 24h | " |
| `veto_window_critical` | 12h | >= 6h | " |
| `deliberation_days` | 30 | >= 14 | " |
| `deliberation_days_critical` | 7 | >= 5 | " |
| `inactivity_timeout` | 48h | >= 24h | " |
| `inactivity_timeout_critical` | 12h | >= 6h | " |
| `replacement_extension` | 7 days | >= 3 days | " |
| `replacement_extension_critical` | 2 days | >= 1 day | " |
| `min_federation_pool_size` | 10 | >= 7 | " |

---

## 14. Open Questions

1. **VRF implementation**: Which VRF scheme? ECVRF (RFC 9381) is a candidate,
   but the choice depends on the cryptographic stack. Currently a design
   parameter, not specified.

2. **Draw coordinator selection**: The coordinator is described as a rotating
   role. The rotation mechanism (round-robin, reputation-based, random) is not
   yet defined.

3. **Inter-federation trust for panel service**: When a node serves on another
   federation's panel, what trust assumptions apply? The reputation export
   package (`PROCEDURAL-REPUTATION-SPEC` section 8) provides evidence, but the
   trust model for inter-federation adjudication needs further specification.

4. **Deliberation protocol**: This document specifies composition but not the
   deliberation format (synchronous / asynchronous, structured debate,
   evidence submission rules). A separate `PANEL-DELIBERATION-PROTOCOL` may
   be needed.

5. **Compensation for panel service**: Should panelists receive compensation
   (token, reputation bonus, or other)? Current design: panel completion
   generates a positive `procedural` signal (`panel_completed`), which is the
   only incentive.

---

## 15. Relation to Other Documents

- **Constitution Art. VII.1-3**: This document operationalizes procedural
  governance by defining how adjudicating panels are composed without permanent
  organs or charismatic authority.
- **Constitution Art. VII.6**: COI-by-default is the eligibility baseline.
- **Constitution Art. VII.3**: Role separation is enforced through eligibility
  exclusions.
- **Constitution Art. XVI.3**: High-stakes decisions requiring independent
  verification use panels composed by this protocol.
- **Constitution Art. X.4-X.8, III.9**: Disclosure override (section 9.4) is
  grounded in the conditional disclosure framework; privacy does not shield
  abuse from procedural accountability.
- **`ENTRENCHMENT-CLAUSE.en.md` section 3.2**: This protocol is the mechanism
  referenced there for composing ad-hoc panels.
- **`PROCEDURAL-REPUTATION-SPEC.en.md`**: Provides the `procedural.score` and
  `panel_procedural_threshold` used for eligibility. Panel service generates
  `procedural` domain signals.
- **`ROOT-IDENTITY-AND-NYMS.en.md`**: Provides the `IAL` levels and the rule that
  higher influence requires stronger identity anchoring; a high-stakes panel may
  not rely on reputation alone.
- **`EXCEPTION-POLICY.en.md`**: Interim measures (section 7, `critical`
  timeline) are constitutional exceptions of type `injunction`.
- **`ABUSE-DISCLOSURE-PROTOCOL.en.md`**: Cases adjudicated under Art. X use
  panels composed by this protocol; disclosure levels (D0-D4) interact with
  panelist identity disclosure (section 9).
- **`AUTONOMY-LEVELS.en.md`**: Post-crisis A3 review may be conducted by a
  panel composed under this protocol.
- **`REPUTATION-VALIDATION-PROTOCOL.en.md`**: Panel proceedings generate
  `procedural` signals that feed into M1-M5 health metrics.
- **`NORMATIVE-HIERARCHY.en.md`**: This document is a Level 3 implementing act.
