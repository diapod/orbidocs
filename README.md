# Distributed Intelligence Agency Documentation

[![Orbidocs Schema Validation](https://github.com/diapod/orbidocs/actions/workflows/orbidocs-schema-validation.yml/badge.svg?branch=main)](https://github.com/diapod/orbidocs/actions/workflows/orbidocs-schema-validation.yml)

## Brand Identity

- Umbrella project / organization: **Distributed Intelligence Agency**
- System and protocol family: **Orbiplex**
- Website: https://distributed-intelligence.agency/
- Contact: team@distributed-intelligence.agency
- GitHub organization: https://github.com/orgs/diapod/

## Documentation structure

### Sections

* `/challenges` – what challenges we face
* `/constitutional-ops` – constitutional supplements, onboarding aids, and executable policy drafts
* `/core-values` – foundational values and ethical orientation
* `/memos` – quick notes and idea backlog to revisit later
* `/proposals` – proposals to be considered and implemented
* `/requirements` – requirement specifications for certain components
* `/schemas` – machine-readable protocol and artifact schemas
* `/stories` – user stories to be used as scenarios to create requirements

## Document Lifecycle

The default document flow in this repository is:

`memo -> proposal -> requirements -> schemas`

In practice, each stage serves a different purpose:

* `memos/` capture short idea seeds, rough intuitions, and design prompts before the model is stable.
* `proposals/` turn those ideas into architectural decisions or candidate operating models: problem statement, goals, decision, trade-offs, and open questions.
* `requirements/` translate stable proposal decisions into explicit behavioral and data contracts.
* `schemas/` encode the machine-readable parts of those contracts.

There are also two important side paths:

* `proposal -> proposal` when a broad architectural decision must be split into narrower sub-decisions before requirements can be written.
* `story -> requirements` when a user scenario is the best source of concrete system obligations.

Normative material follows a stricter path. When a proposal starts governing authority, identity, sanctions, disclosure, constitutional exceptions, or other high-stakes social rules, it should be promoted into `constitutional-ops/` rather than left only as an implementation proposal.

### Files

* `/CONSTITUTION.pl.md` – project's constitution (Polish)
* `/CONSTITUTION.en.md` – project's constitution (English)
* `/VISION.pl.md` – project vision (Polish)
* `/VISION.en.md` – project vision (English)
* `/AI-MANIFESTO.pl.md` – AI manifesto (Polish)
* `/AI-MANIFESTO.en.md` – AI manifesto (English)
* `/COLLABORATION.md` – basic collaboration guidelines
* `/AGENTS.md` – information for agents
* `/Makefile` – convenience target for schema validation
* `/schemas/transcript-segment.v1.schema.json` – JSON Schema for transcript segment artifacts
* `/schemas/transcript-bundle.v1.schema.json` – JSON Schema for transcript bundle artifacts
* `/schemas/answer-room-metadata.v1.schema.json` – JSON Schema for answer-channel room metadata and operator participation policy
* `/schemas/examples/` – coherent example artifacts for room metadata, transcript segments, and transcript bundles
* `/schemas/examples/invalid/` – negative validation vectors for room metadata, transcript segments, and transcript bundles
* `/scripts/validate-json-schemas.sh` – CLI validator wrapper for schemas and example artifacts
* `/core-values/CORE-VALUES.pl.md` – core values document (Polish)
* `/core-values/CORE-VALUES.en.md` – core values document (English)
* `/constitutional-ops/pl/NORMATIVE-HIERARCHY.pl.md` – proposed normative hierarchy of constitutional documents
* `/constitutional-ops/pl/NODE-RIGHTS-CARD.pl.md` – onboarding card and decision index for node operators
* `/constitutional-ops/pl/AUTONOMY-LEVELS.pl.md` – autonomy gradient for agents
* `/constitutional-ops/pl/EXCEPTION-POLICY.pl.md` – exception procedure and data model
* `/constitutional-ops/pl/FEDERATION-MEMBERSHIP-AND-QUORUM.pl.md` – federation eligibility, liveness, quorum and veto rules
* `/constitutional-ops/pl/ENTRENCHMENT-CLAUSE.pl.md` – entrenchment clause and constitutional defense procedure
* `/constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md` – root identity, cryptographic nyms, and identity assurance levels
* `/constitutional-ops/pl/IDENTITY-ATTESTATION-AND-RECOVERY.pl.md` – first attestation, attestation memory, recovery phrase, and anchor-identity reconstruction
* `/constitutional-ops/pl/ATTESTATION-PROVIDERS.pl.md` – mapping of identity-attestation methods to `weak` / `strong` classes and maximum `IAL`
* `/constitutional-ops/pl/IDENTITY-UPGRADE-ANOMALY-SIGNALS.pl.md` – anomaly signals and review thresholds for identity-attestation upgrades, especially `phone -> strong`
* `/constitutional-ops/pl/IDENTITY-UNSEALING-BOARD.pl.md` – Federation of Sealed Chambers, thresholds for unmasking, and multi-chamber root-identity unsealing
* `/constitutional-ops/pl/UNSEAL-CASE-MODEL.pl.md` – shared case model for `U1-U3` unsealing procedures
* `/constitutional-ops/pl/ROLE-TO-IAL-MATRIX.pl.md` – minimum mapping of role classes to identity assurance levels
* `/constitutional-ops/pl/FIP-MEMBERSHIP-AND-QUORUM.pl.md` – membership, activity, and quorum rules for the Federation of Sealed Chambers
* `/constitutional-ops/pl/PROCEDURAL-REPUTATION-SPEC.pl.md` – procedural reputation specification
* `/constitutional-ops/pl/PANEL-SELECTION-PROTOCOL.pl.md` – ad-hoc panel selection protocol
* `/constitutional-ops/pl/REPUTATION-VALIDATION-PROTOCOL.pl.md` – validation protocol for reputation mechanisms
* `/constitutional-ops/pl/ABUSE-DISCLOSURE-PROTOCOL.pl.md` – protocol for conditional disclosure of accountability for abuse
* `/constitutional-ops/pl/IMPLEMENTATION-GAPS.pl.md` – backlog of remaining constitutional implementation gaps
* `/constitutional-ops/en/NORMATIVE-HIERARCHY.en.md` – proposed normative hierarchy of constitutional documents (English)
* `/constitutional-ops/en/NODE-RIGHTS-CARD.en.md` – onboarding card and decision index for node operators (English)
* `/constitutional-ops/en/AUTONOMY-LEVELS.en.md` – autonomy gradient for agents (English)
* `/constitutional-ops/en/EXCEPTION-POLICY.en.md` – exception procedure and data model (English)
* `/constitutional-ops/en/FEDERATION-MEMBERSHIP-AND-QUORUM.en.md` – federation eligibility, liveness, quorum and veto rules (English)
* `/constitutional-ops/en/ENTRENCHMENT-CLAUSE.en.md` – entrenchment clause and constitutional defense procedure (English)
* `/constitutional-ops/en/ROOT-IDENTITY-AND-NYMS.en.md` – root identity, cryptographic nyms, and identity assurance levels (English)
* `/constitutional-ops/en/IDENTITY-ATTESTATION-AND-RECOVERY.en.md` – first attestation, attestation memory, recovery phrase, and anchor-identity reconstruction (English)
* `/constitutional-ops/en/ATTESTATION-PROVIDERS.en.md` – mapping of identity-attestation methods to `weak` / `strong` classes and maximum `IAL` (English)
* `/constitutional-ops/en/IDENTITY-UPGRADE-ANOMALY-SIGNALS.en.md` – anomaly signals and review thresholds for identity-attestation upgrades, especially `phone -> strong` (English)
* `/constitutional-ops/en/IDENTITY-UNSEALING-BOARD.en.md` – Federation of Sealed Chambers, thresholds for unmasking, and multi-chamber root-identity unsealing (English)
* `/constitutional-ops/en/UNSEAL-CASE-MODEL.en.md` – shared case model for `U1-U3` unsealing procedures (English)
* `/constitutional-ops/en/ROLE-TO-IAL-MATRIX.en.md` – minimum mapping of role classes to identity assurance levels (English)
* `/constitutional-ops/en/FIP-MEMBERSHIP-AND-QUORUM.en.md` – membership, activity, and quorum rules for the Federation of Sealed Chambers (English)
* `/constitutional-ops/en/PROCEDURAL-REPUTATION-SPEC.en.md` – procedural reputation specification (English)
* `/constitutional-ops/en/PANEL-SELECTION-PROTOCOL.en.md` – ad-hoc panel selection protocol (English)
* `/constitutional-ops/en/REPUTATION-VALIDATION-PROTOCOL.en.md` – validation protocol for reputation mechanisms (English)
* `/constitutional-ops/en/ABUSE-DISCLOSURE-PROTOCOL.en.md` – protocol for conditional disclosure of accountability for abuse (English)
* `/constitutional-ops/en/IMPLEMENTATION-GAPS.en.md` – backlog of remaining constitutional implementation gaps (English)

## Traceability Matrix

### Stories -> Requirements

| Story | Requirements |
|---|---|
| `/stories/story-001.md` | `/requirements/requirements-001.md` |
| `/stories/story-002.md` | `/requirements/requirements-002.md` |
| `/stories/story-003.md` | `/requirements/requirements-003.md` |

### Challenges -> Proposals

| Challenge | Proposal |
|---|---|
| `/challenges/001-licensing.md` | `/proposals/001-licensing-proposal.md` |
| `/challenges/002-sybil.md` | `/proposals/002-comm-protocol.md` |

### Memos -> Proposals

| Memo | Proposal |
|---|---|
| `/memos/swarm-broadcast-assistance.md` | `/proposals/003-question-envelope-and-answer-channel.md` |
| `/memos/swarm-question-channel-transports.md` | `/proposals/003-question-envelope-and-answer-channel.md` |
| `/memos/operator-participation-in-answer-channel.md` | `/proposals/004-human-origin-flags-and-operator-participation.md` |
| `/memos/client-simplicity.md` | `/proposals/006-pod-access-layer-for-thin-clients.md` |
| `/memos/pod-backed-thin-clients.md` | `/proposals/006-pod-access-layer-for-thin-clients.md` |
| `/memos/transcription-monitors-and-public-vaults.md` | `/proposals/008-transcription-monitors-and-public-vaults.md` |
| `/memos/swarm-communication-exposure-modes.md` | `/proposals/009-communication-exposure-modes.md` |
| `/memos/operator-proxy-co-regulation.md` | `/proposals/010-operator-proxy-co-regulation.md` |

### Proposals -> Proposals

| Proposal | Proposal |
|---|---|
| `/proposals/004-human-origin-flags-and-operator-participation.md` | `/proposals/005-operator-participation-room-policy-profiles.md` |
| `/proposals/006-pod-access-layer-for-thin-clients.md` | `/proposals/007-pod-identity-and-tenancy-model.md` |

### Proposals -> Requirements

| Proposal | Requirement |
|---|---|
| `/proposals/003-question-envelope-and-answer-channel.md` | `/requirements/requirements-004.md` |
| `/proposals/004-human-origin-flags-and-operator-participation.md` | `/requirements/requirements-004.md` |
| `/proposals/004-human-origin-flags-and-operator-participation.md` | `/requirements/requirements-005.md` |
| `/proposals/005-operator-participation-room-policy-profiles.md` | `/requirements/requirements-005.md` |
| `/proposals/008-transcription-monitors-and-public-vaults.md` | `/requirements/requirements-004.md` |
| `/proposals/009-communication-exposure-modes.md` | `/requirements/requirements-004.md` |
| `/proposals/009-communication-exposure-modes.md` | `/requirements/requirements-005.md` |

### Requirements -> Schemas

| Requirement | Schema |
|---|---|
| `/requirements/requirements-005.md` | `/schemas/transcript-segment.v1.schema.json` |
| `/requirements/requirements-005.md` | `/schemas/transcript-bundle.v1.schema.json` |

### Proposals -> Schemas

| Proposal | Schema |
|---|---|
| `/proposals/005-operator-participation-room-policy-profiles.md` | `/schemas/answer-room-metadata.v1.schema.json` |


### Values -> Constitution
