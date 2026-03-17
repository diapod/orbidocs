# Distributed Intelligence Agency Documentation

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
* `/stories` – user stories to be used as scenarios to create requirements

### Files

* `/CONSTITUTION.pl.md` – project's constitution (Polish)
* `/CONSTITUTION.en.md` – project's constitution (English)
* `/VISION.pl.md` – project vision (Polish)
* `/VISION.en.md` – project vision (English)
* `/AI-MANIFESTO.pl.md` – AI manifesto (Polish)
* `/AI-MANIFESTO.en.md` – AI manifesto (English)
* `/COLLABORATION.md` – basic collaboration guidelines
* `/AGENTS.md` – information for agents
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

### Proposals -> Requirements

| Proposal | Requirement |
|---|---|
| `/proposals/003-question-envelope-and-answer-channel.md` | `/requirements/requirements-004.md` |
| `/proposals/004-human-origin-flags-and-operator-participation.md` | `/requirements/requirements-004.md` |


### Values -> Constitution
