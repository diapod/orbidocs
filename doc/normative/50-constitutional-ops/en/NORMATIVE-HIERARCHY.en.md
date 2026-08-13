# Normative Hierarchy of DIA Documents

## Document Status

| Field | Value |
| :--- | :--- |
| `policy-id` | `DIA-NORM-HIER-001` |
| `type` | Supplement to the Constitution section "Normative Force and Interpretation" |
| `version` | 0.2.0-draft |
| `author` | DIA / Orbiplex |
| `date` | 2026-03-10 |

---

## 1. Purpose of the Document

This document specifies the normative hierarchy of documents in the DIA/Orbiplex
project, resolving ambiguity about the binding force of particular sources. It is a
proposed extension of the Constitution section "Normative Force and
Interpretation" (points 4-6).

---

## 2. Normative Hierarchy

Project documents form the following levels of normative force. A lower-level
document may not weaken, narrow, or reinterpret a higher-level document without a
formal procedure for amending the relevant higher level.

### Level 0 - Non-Negotiable Core

The clauses identified directly by the Constitution's "Non-Negotiable Core"
section. The canonical machine-readable list is maintained in
`doc/normative/40-constitution/constitution-index.v1.json`. Their amendment,
suspension, or narrowing reinterpretation requires the procedure described in
`ENTRENCHMENT-CLAUSE.en.md`, including unanimity of all federations participating in
the amendment process and independent adversarial review. The implementing act
defines the procedure but MUST NOT change the composition of Level 0.

### Level 1 - Constitution

The remaining articles of `doc/normative/40-constitution/en/CONSTITUTION.en.md`. Amendment requires the
procedure described in Art. XVI: explicit rationale, impact analysis,
description of reversibility, trace of the decision process, and a trial period
for high-stakes changes.

### Level 2 - Sources of Interpretation

The documents `doc/normative/30-core-values/en/CORE-VALUES.en.md` and
`doc/normative/20-vision/en/VISION.en.md`.

They serve to interpret the Constitution, but **do not create new obligations or
rights** beyond the constitutional framework. Sections in these documents are
divided into two categories:

- **`[value]`** - expression of an ethical or architectural principle; it has
  interpretive force when reading the Constitution.
- **`[mechanism - hypothesis]`** - description of a proposed mechanism (e.g.
  Creator Credits, attribution graph, reputation curves); it has no normative
  force until empirical validation and formal adoption by a federation.

Changing Level 2 documents requires an explicit rationale and a coherence review
against the Constitution, but **does not require the full constitutional
amendment procedure**.

`doc/normative/90-supplementary/en/ONTOLOGICAL-BASIS.en.md` is explanatory material
for the genealogy and coherence of values, but it is not an independent Level 2
source of interpretation and creates no rights, duties, or classifications of
persons. It may not serve as a worldview, loyalty, membership, identity, or
reputation test. In case of divergence, the Constitution and Level 2 sources prevail.

### Level 3 - Implementing Acts

Operational documents with binding force within federations:

- `AUTONOMY-LEVELS.en.md` - agent autonomy gradient
- `ABUSE-DISCLOSURE-PROTOCOL.en.md` - threshold, scope, and procedure of
  conditional disclosure of accountability for abuse
- `EXCEPTION-POLICY.en.md` - exception procedure, data model, and monitoring
- `FEDERATION-MEMBERSHIP-AND-QUORUM.en.md` - operational trust-root anchoring,
  definition of a voting-eligible federation, activity statuses, and the rules of
  quorum and veto
- `ROOT-IDENTITY-AND-NYMS.en.md` - model of root identity, nyms, assurance
  levels, and delegation across devices
- `IDENTITY-ATTESTATION-AND-RECOVERY.en.md` - first attestation, memory of
  prior attestation, recovery phrase, and reconstruction of `anchor-identity`
- `ATTESTATION-PROVIDERS.en.md` - mapping of attestation methods to `weak` /
  `strong` classes and maximum `IAL` levels
- `IDENTITY-UPGRADE-ANOMALY-SIGNALS.en.md` - minimum catalog of anomaly
  signals, responses, and review for attestation upgrade, especially `phone -> strong`
- `IDENTITY-UNSEALING-BOARD.en.md` - Federation of Sealed Chambers, thresholds
  `nym -> node-id` and `node-id -> root-identity`, quorum, and split knowledge
- `UNSEAL-CASE-MODEL.en.md` - the shared data model of an unsealing case for
  thresholds `U1-U3`
- `ROLE-TO-IAL-MATRIX.en.md` - the minimum map of role classes to `IAL`
  thresholds and `fixed_power_bonus` rules
- `FIP-MEMBERSHIP-AND-QUORUM.en.md` - membership, activity, and quorum of the
  Federation of Sealed Chambers
- `MEMBERSHIP-AND-SPONSORSHIP-POLICY.en.md` - per-surface entry policy,
  sponsorship scope, probation, sponsor liability, newcomer slow-start, and
  anti-sponsor-ring constraints
- `PARTICIPANT-COVENANT.en.md` - short operational covenant for entering shared
  influence surfaces
- `PROCEDURAL-REPUTATION-SPEC.en.md` - specification of domains, signals, and
  calculation of procedural reputation
- `ADVOCACY-AND-SOLICITATION-POLICY.en.md` - opt-in requirements, disclosures,
  and sanctions for persuasion and solicitation surfaces
- `MARKETPLACE-ANTI-FRAUD-POLICY.en.md` - value caps, escrow expectations,
  anti-fraud rules, and reputation basis for marketplace surfaces
- `RAW-SIGNAL-POLICY.en.md` - raw-signal protection, style-transformation modes,
  meta-markers, and audit trace
- `UNIVERSAL-BASIC-COMPUTE.en.md` - minimal Proof-of-Personhood model,
  non-withdrawable minimum compute, limited cross-federation portability, and UBC settlement
- `UBC-LIMIT-PROFILES.en.md` - canonical UBC limit profiles, portability
  profiles, and the minimal FIP bridge/registry for cross-federation PoP
- `SWARM-ECONOMY-SUFFICIENCY.en.md` - sufficiency threshold, concentration brakes,
  surplus circulation, and barrier between reward and governance
- `PANEL-SELECTION-PROTOCOL.en.md` - procedure for eligibility, draw, veto, and
  replenishment of ad-hoc panel composition
- `REPUTATION-VALIDATION-PROTOCOL.en.md` - validation protocol for reputation
  mechanisms
- `ENTRENCHMENT-CLAUSE.en.md` - constitutional defense procedure and entrenchment
  clause
- other `policy-as-code` documents or implementing documents under
  `doc/normative/50-constitutional-ops/` that explicitly declare their type and constitutional
  basis

Implementing acts concretize the Constitution and the Sources of Interpretation.
They MAY **tighten** requirements but MUST NOT weaken any higher level.

### Level 4 - Federation Policies

Parameters, configurations, and local rules of individual federations. They
include:

- reputation thresholds,
- parameters of reward mechanisms,
- local role extensions,
- mode configurations (normal / crisis / support).

Federation policies are autonomous in the areas not covered by higher levels. A
federation may shape them freely as long as it does not violate Levels 0-3.

### Level 5 - Derived and Onboarding Materials

Supporting documents that **do not have their own normative force** but summarize,
map, or make it easier to work with higher-level documents. They include:

- `NODE-RIGHTS-CARD.en.md` - extract of node rights and duties together with a
  decision index,
- onboarding checklists,
- process maps,
- operational shortcuts and training materials.

A Level 5 document:

- may not create new obligations or rights,
- loses to the source document in case of conflict,
- should indicate the source of each claim by article or base document.

---

## 3. Conflict Resolution Rules

1. In case of conflict between levels, the higher level prevails.
2. In case of conflict within the same level, the procedure from Constitution Art.
    XIV applies (tests of reversibility, proportionality, and publicity).
3. In case of conflict between language versions of the same document, the Polish
    version prevails unless it is shown that the difference results from a
    translation error.
4. A lower-level document that in fact violates a higher level is **invalid to the
    extent of the violation** from the moment the violation is established, not
    from the moment of publication.

---

## 4. Procedure for Tagging Sections in the Sources of Interpretation

Each section of `doc/normative/30-core-values/en/CORE-VALUES.en.md` and
`doc/normative/20-vision/en/VISION.en.md` SHOULD contain in its header the tag:

```md
### Section Name `[value]`
```

or

```md
### Section Name `[mechanism - hypothesis]`
```

Untagged sections are treated by default as `[value]`, unless they describe a
specific algorithm, numeric parameter, or token scheme; in that case they are
defaulted to `[mechanism - hypothesis]`.

---

## 5. Entry into Force

This document enters into force after formal adoption in accordance with the
constitutional amendment procedure (Art. XVI), because it modifies the section
"Normative Force and Interpretation".
