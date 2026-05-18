# MVP Readiness Snapshot

Snapshot date: 2026-05-18.

This table is an estimated cross-document readiness snapshot for canonical Story, Proposal, and Solution documents.

Scope rules: localized duplicates (`*.pl.md`), indexes, backlog files, implementation notes, coding guides, and generated registries are excluded. Solution rows use the main `NNN-*/NNN-*.md` document for each component.

Estimation basis: `node/docs/MVP.md` defines the hard-MVP story set (`story-000`, `story-002`, `story-005`, `story-006`); `doc/project/60-solutions/CAPABILITY-MATRIX.en.md` provides coarse implementation status; each document text is used as fallback when no capability row exists. `part of MVP` tracks the hard-MVP set; `MVP ready` may still be `true` for a post-hard-MVP document when its own MVP slice is implemented. Percentages are engineering estimates, not release-signoff facts.

Change basis: this refresh incorporates the current worktree state on 2026-05-18, including Story 010, Proposals 057-062, Solutions 025-029, the Artifact Delivery / INAC / TLS trust updates, and the related notification, contact, messaging, pseudonym-vault, service-CA, artifact-mailbox, artifact-object-pointer, temporal-storage, and bounded-deferred-operation schemas and trackers.

Recent component deltas:

- Artifact Delivery moved from "MVP transport foundation" to hard-MVP complete: Memarium custody target-space policy, profiling counters, metadata-only observers, Matrix mailbox hardening, and `object-store-indirect` fetch/rehydrate through `artifact-object-pointer.v1` are now documented and implemented. Lower-level zero-copy and Matrix media variants remain post-MVP optimization layers.
- Notifications now have a local durable MVP foundation: schema-gated `notification.create`, temporal SQLite event log, derived queue projection, JSONL audit mirror, SSE state ping, operator UI, legacy `notify_emit` adapter, and first daemon-owned actions. They remain partial because storage performance profiles, compaction, pod-user UX, OS notifications, and cross-node aggregation are later layers.
- Contact Catalog and Messaging have moved substantially beyond design: Story 010 strict `ad-smoke` is the current E2E gate for Contact Catalog + Messaging. Contact Catalog hard-MVP recovery, tombstone/revocation replay, PSI/blinded lookup, and provider sync are implemented; production provider selection, broader federation tests, and larger hardening matrices remain open.
- Replay Scheduler M1 is now fully closed for the hard-MVP slice: the generic bounded scheduler, durable launch ledger, host-owned job-source merge, authority gate, cooperative shutdown, Agora projection replay action, and operator status/control surface are all documented as implemented. Richer Agora-domain panels and non-Agora maintenance jobs are post-M1 extensions.
- Temporal Storage Convention is now a formal proposal/solution pair with notification-store as the first implemented pilot. The convention is not complete until profile configuration, compaction, emergency cleanup, manifests, and at least one more converged store exist.
- Bounded Deferred Operations were promoted from Proposal 055 to Solution 029 as a horizontal host control-plane component. The MVP slice is complete: shared wire contracts, host registry, poll/cancel surfaces, JSON-e Flow persisted continuation, Sensorium OS deferred state, operator visibility, and AD consumer integration.
- Proposal 054 now has the core runtime trust slice implemented: `seed-directory-query-attestation.v1` is schema-gated, Seed Directory can attach opt-in signed response attestations, daemon can opt into trusted Agora replay for `adv`, `cap`, and `revocations` lanes, replay cursors/status are persisted in the embedded store, and projection equivalence tests include revocation effects. Multi-directory query/merge policy and the full operator trust UI remain open.

## Stories

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Story 000: Two Nodes See Each Other](../30-stories/story-000-two-nodes-see-each-other.md) | `true` | `true` | `false` | `90` |
| [Story 001: Swarm Node Onboarding and Federated Answer Procurement](../30-stories/story-001-swarm-node-onboarding.md) | `false` | `false` | `false` | `65` |
| [Story 002: Federated Peer Learning and Consensus Correction](../30-stories/story-002-federated-peer-learning.md) | `true` | `true` | `false` | `90` |
| [Story 003: Remote Memory Preservation, Archivists, and Vault Publication](../30-stories/story-003-remote-memory-preservation.md) | `false` | `false` | `false` | `38` |
| [Story 004: Pod-Client Onboarding and Delegated Federated Answer Procurement](../30-stories/story-004-pod-client-onboarding.md) | `false` | `false` | `false` | `65` |
| [Story 005: Whisper Rumor Intake, Redaction, and Thresholded Association Bootstrap](../30-stories/story-005-whisper-rumor-intake.md) | `true` | `true` | `false` | `96` |
| [Story 006 Buyer Node Components for Arca](../30-stories/story-006-buyer-node-components.md) | `true` | `true` | `false` | `90` |
| [Story 006: Voluntary Swarm Service Exchange for Cooperative Content Production](../30-stories/story-006-voluntary-swarm-exchange.md) | `true` | `true` | `false` | `90` |
| [Story 007: Settlement-Capable Node as the Authoritative ORC Ledger](../30-stories/story-007-settlement-capable-node.md) | `false` | `false` | `false` | `82` |
| [Story 008: Leaving an Opinion on a Website via the Local Node](../30-stories/story-008-cool-site-comment.md) | `false` | `false` | `false` | `100` |
| [Story 009: The magazine publishes itself — a three-node blogging pipeline about Bielik, conducted by Arca](../30-stories/story-009-bielik-blog-arca.md) | `false` | `false` | `false` | `85` |
| [Story 010: Message to a Friend](../30-stories/story-010-message-to-a-friend.md) | `false` | `true` | `false` | `88` |

## Proposals

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Licensing Baseline for Orbiplex Swarm Components](../40-proposals/001-licensing-proposal.md) | `false` | `false` | `false` | `25` |
| [Communication Protocol Baseline for Orbiplex Swarm](../40-proposals/002-comm-protocol.md) | `true` | `false` | `false` | `65` |
| [Question Envelope and Answer-Channel Transport for Orbiplex Swarm](../40-proposals/003-question-envelope-and-answer-channel.md) | `true` | `false` | `false` | `55` |
| [Human-Origin Flags and Operator Participation in Answer Channels](../40-proposals/004-human-origin-flags-and-operator-participation.md) | `false` | `false` | `false` | `65` |
| [Operator Participation Room Policy Profiles](../40-proposals/005-operator-participation-room-policy-profiles.md) | `false` | `false` | `false` | `25` |
| [Pod-Backed Access Layer for Thin Clients](../40-proposals/006-pod-access-layer-for-thin-clients.md) | `false` | `false` | `false` | `55` |
| [Pod Identity and Tenancy Model](../40-proposals/007-pod-identity-and-tenancy-model.md) | `false` | `false` | `false` | `25` |
| [Transcription Monitors, Archivists, and Public Vaults](../40-proposals/008-transcription-monitors-and-public-vaults.md) | `false` | `false` | `false` | `20` |
| [Communication Exposure Modes for Swarm Requests](../40-proposals/009-communication-exposure-modes.md) | `false` | `false` | `false` | `25` |
| [Operator Proxy and Co-Regulation Channels](../40-proposals/010-operator-proxy-co-regulation.md) | `false` | `false` | `false` | `25` |
| [Federated Answer Procurement Lifecycle Artifacts](../40-proposals/011-federated-answer-procurement-lifecycle.md) | `true` | `false` | `false` | `65` |
| [Learning Outcomes, Knowledge Artifacts, and Archival Contracts](../40-proposals/012-learning-outcomes-and-archival-contracts.md) | `false` | `false` | `false` | `38` |
| [Whisper Social-Signal Exchange and Threshold Bootstrap](../40-proposals/013-whisper-social-signal-exchange.md) | `true` | `true` | `false` | `88` |
| [Node Transport and Discovery MVP](../40-proposals/014-node-transport-and-discovery-mvp.md) | `true` | `false` | `false` | `69` |
| [Nym Certificates and Renewal Baseline](../40-proposals/015-nym-certificates-and-renewal-baseline.md) | `false` | `false` | `false` | `25` |
| [Supervised Prepaid Gateway and Escrow MVP](../40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md) | `true` | `false` | `false` | `65` |
| [Proposal 017: Organization Subjects and org:did:key](../40-proposals/017-organization-subjects-and-org-did-key.md) | `true` | `true` | `false` | `88` |
| [Proposal 018: Layered capability_limited Participant Restrictions](../40-proposals/018-layered-capability-limited-participant-restrictions.md) | `true` | `false` | `false` | `25` |
| [Proposal 019: Supervised http_local_json Middleware Executor](../40-proposals/019-supervised-local-http-json-middleware-executor.md) | `true` | `true` | `false` | `100` |
| [Proposal 020: Bundled Python Middleware Modules for Hard MVP](../40-proposals/020-bundled-python-middleware-modules.md) | `true` | `true` | `false` | `100` |
| [Proposal 021: Service Offers, Service Orders, and the Host-Owned Procurement Bridge](../40-proposals/021-service-offers-orders-and-procurement-bridge.md) | `true` | `true` | `false` | `88` |
| [Proposal 022: Monus as Host-Granted Local Observation Middleware](../40-proposals/022-monus-as-host-granted-local-observation-middleware.md) | `false` | `false` | `false` | `15` |
| [Proposal 023: Federated Offer Distribution and Catalog Listener](../40-proposals/023-federated-offer-distribution-and-catalog-listener.md) | `true` | `true` | `false` | `100` |
| [Proposal 024: Capability Passports and Network Ledger Delegation](../40-proposals/024-capability-passports-and-network-ledger-delegation.md) | `true` | `true` | `false` | `85` |
| [Proposal 025: Seed Directory as Capability Catalog](../40-proposals/025-seed-directory-as-capability-catalog.md) | `true` | `true` | `false` | `100` |
| [Proposal 026: Resource Opinions and Discussion Surfaces](../40-proposals/026-resource-opinions-and-discussion-surfaces.md) | `false` | `false` | `false` | `100` |
| [Proposal 027: Middleware Peer-Message Dispatch](../40-proposals/027-middleware-peer-message-dispatch.md) | `true` | `true` | `true` | `100` |
| [Proposal 028: Service Schema Catalog](../40-proposals/028-service-schema-catalog.md) | `false` | `false` | `false` | `25` |
| [Proposal 029: Workflow Template Catalog](../40-proposals/029-workflow-template-catalog.md) | `false` | `false` | `false` | `40` |
| [Proposal 030: Identity Recovery Service](../40-proposals/030-identity-recovery-service.md) | `false` | `false` | `false` | `55` |
| [Proposal 031: Participant Key Passphrase Lock](../40-proposals/031-participant-key-passphrase-lock.md) | `false` | `false` | `false` | `65` |
| [Proposal 032: Key Delegation Passports](../40-proposals/032-key-delegation-passports.md) | `true` | `true` | `false` | `100` |
| [Proposal 033: Workflow Fan-Out and Temporal Orchestration](../40-proposals/033-workflow-fan-out-and-temporal-orchestration.md) | `true` | `true` | `false` | `77` |
| [Proposal 034: Node Operator Binding and Derived Node Assurance](../40-proposals/034-node-operator-binding-and-derived-node-assurance.md) | `true` | `true` | `false` | `90` |
| [Proposal 035: Agora — Topic-Addressed Record Relay and Shared Record Substrate](../40-proposals/035-agora-topic-addressed-record-relay.md) | `true` | `true` | `false` | `92` |
| [Proposal 036: Memarium — Local Memory Organ for the Orbiplex Node](../40-proposals/036-memarium.md) | `true` | `false` | `false` | `68` |
| [Proposal 037: Generic Signing Service](../40-proposals/037-generic-signing-service.md) | `true` | `true` | `false` | `100` |
| [Proposal 038: Key Roles and Key Use Taxonomy](../40-proposals/038-key-roles-and-key-use-taxonomy.md) | `true` | `true` | `false` | `100` |
| [Proposal 039 Crisis Seed v1 Review Record](../40-proposals/039-crisis-space-seed-v1-review.md) | `false` | `false` | `false` | `25` |
| [Proposal 039: Crisis Space Seed v1](../40-proposals/039-crisis-space-seed-v1.md) | `false` | `false` | `false` | `100` |
| [Proposal 040: Custodial Redelivery and Tombstones for Agora Records](../40-proposals/040-custodial-redelivery-and-tombstones.md) | `false` | `false` | `false` | `38` |
| [Proposal 041: Agora Ingest Attestation and Tiered Access](../40-proposals/041-agora-ingest-attestation.md) | `false` | `false` | `false` | `65` |
| [Proposal 042: Inter-Node Artifact Channel (F2F Memarium Exchange)](../40-proposals/042-inter-node-artifact-channel.md) | `true` | `true` | `false` | `88` |
| [Proposal 043: Node Address Attestation Fallback](../40-proposals/043-node-address-attestation-fallback.md) | `true` | `false` | `false` | `65` |
| [Proposal 044: Host-Owned Generic Module Store](../40-proposals/044-host-owned-generic-module-store.md) | `true` | `true` | `false` | `100` |
| [Proposal 045: Sensorium as a Local Enaction Stratum](../40-proposals/045-sensorium-local-enaction-stratum.md) | `true` | `false` | `false` | `65` |
| [Proposal 046: Agora Topic-Key Namespace Conventions](../40-proposals/046-agora-topic-key-namespace-conventions.md) | `false` | `false` | `false` | `100` |
| [Proposal 047: Classification Label Propagation for Memarium-Touching Data](../40-proposals/047-classification-label-propagation.md) | `true` | `false` | `false` | `58` |
| [Proposal 048: Sensorium OS Connector Action Classes](../40-proposals/048-sensorium-os-connector-action-classes.md) | `true` | `false` | `false` | `55` |
| [Proposal 049: JSON-e Middleware Transformer Executor](../40-proposals/049-json-e-middleware-transformer-executor.md) | `true` | `true` | `false` | `82` |
| [Proposal 050: Local Readiness Gate](../40-proposals/050-local-readiness-gate.md) | `true` | `true` | `false` | `85` |
| [Proposal 051: Swarm Membership, Reputation Bootstrap, and Public Adjudication](../40-proposals/051-swarm-membership-and-reputation-bootstrap.md) | `false` | `false` | `false` | `25` |
| [Proposal 052: Tauri-Hosted Node UI](../40-proposals/052-tauri-hosted-node-ui.md) | `false` | `false` | `false` | `70` |
| [Proposal 053: Raw Signal Access for Middleware Flows](../40-proposals/053-raw-signal-access.md) | `true` | `true` | `false` | `100` |
| [Proposal 054: User-Maintained Federated Seed Directory](../40-proposals/054-user-maintained-federated-seed-directory.md) | `true` | `false` | `false` | `70` |
| [Proposal 055: Bounded Deferred Operation Contract](../40-proposals/055-bounded-deferred-operation-contract.md) | `true` | `true` | `false` | `100` |
| [Proposal 056: Orbiplex TLS Trust Policy](../40-proposals/056-orbiplex-tls-trust-policy.md) | `true` | `true` | `false` | `86` |
| [Proposal 057: User and Operator Notifications](../40-proposals/057-user-and-operator-notifications.md) | `true` | `true` | `false` | `90` |
| [Proposal 058: Contact Catalog and Private Contact Discovery](../40-proposals/058-contact-catalog.md) | `false` | `true` | `false` | `90` |
| [Proposal 059: Participant, Nym, and Routing-Subject Key-Role Derivation](../40-proposals/059-participant-and-nym-key-role-derivation.md) | `false` | `true` | `false` | `90` |
| [Proposal 060: Messaging Middleware and Personal Message Delivery](../40-proposals/060-messaging-middleware.md) | `false` | `true` | `false` | `88` |
| [Proposal 061: Contact Attestation Service](../40-proposals/061-contact-attestation-service.md) | `false` | `false` | `false` | `78` |
| [Proposal 062: Temporal Storage Convention](../40-proposals/062-temporal-storage-convention.md) | `false` | `false` | `false` | `42` |

## Solutions

| Document | part of MVP | MVP ready | post-MVP ready | readiness % |
|---|---:|---:|---:|---:|
| [Orbiplex Node](../60-solutions/000-node/000-node.md) | `true` | `true` | `false` | `85` |
| [Orbiplex Node UI](../60-solutions/001-node-ui/001-node-ui.md) | `true` | `false` | `false` | `82` |
| [Orbiplex Memarium](../60-solutions/002-memarium/002-memarium.md) | `true` | `false` | `false` | `74` |
| [Orbiplex Arca](../60-solutions/003-arca/003-arca.md) | `true` | `true` | `false` | `88` |
| [Orbiplex Dator](../60-solutions/004-dator/004-dator.md) | `true` | `true` | `false` | `100` |
| [Orbiplex Sealer](../60-solutions/005-sealer/005-sealer.md) | `true` | `true` | `false` | `96` |
| [Orbiplex Capability Binding](../60-solutions/006-capability-binding/006-capability-binding.md) | `true` | `true` | `true` | `95` |
| [Capability Advertisement](../60-solutions/007-capability-advertisement/007-capability-advertisement.md) | `true` | `true` | `false` | `94` |
| [Orbiplex Agora](../60-solutions/008-agora/008-agora.md) | `true` | `true` | `false` | `93` |
| [Orbiplex Monus](../60-solutions/009-monus/009-monus.md) | `false` | `false` | `false` | `15` |
| [Orbiplex Anon](../60-solutions/010-anon/010-anon.md) | `false` | `false` | `false` | `10` |
| [Orbiplex Whisper](../60-solutions/011-whisper/011-whisper.md) | `true` | `true` | `false` | `100` |
| [Ferment](../60-solutions/012-ferment/012-ferment.md) | `false` | `false` | `false` | `15` |
| [Raw Signal Access](../60-solutions/013-raw-signal-access/013-raw-signal-access.md) | `true` | `true` | `false` | `90` |
| [Orbiplex Key Delegation Passports](../60-solutions/014-key-delegation-passports/014-key-delegation-passports.md) | `true` | `true` | `false` | `95` |
| [Host-Owned Module Store](../60-solutions/015-host-owned-module-store/015-host-owned-module-store.md) | `true` | `true` | `false` | `90` |
| [Bounded Local Server Runtime](../60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md) | `true` | `true` | `false` | `90` |
| [Inter-Node Artifact Channel (INAC)](../60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md) | `true` | `true` | `false` | `88` |
| [Classification](../60-solutions/018-classification/018-classification.md) | `true` | `false` | `false` | `61` |
| [Middleware](../60-solutions/019-middleware/019-middleware.md) | `true` | `true` | `false` | `94` |
| [Replay Scheduler](../60-solutions/020-scheduler/020-scheduler.md) | `true` | `true` | `false` | `100` |
| [Solution 021: Agora Authority](../60-solutions/021-agora-authority/021-agora-authority.md) | `false` | `false` | `false` | `77` |
| [Orbiplex Semantic Index](../60-solutions/022-semantic-index/022-semantic-index.md) | `false` | `false` | `false` | `15` |
| [Artifact Delivery](../60-solutions/023-artifact-delivery/023-artifact-delivery.md) | `true` | `true` | `false` | `100` |
| [TLS Trust Policy](../60-solutions/024-tls-trust-policy/024-tls-trust-policy.md) | `true` | `true` | `false` | `86` |
| [Contact Catalog](../60-solutions/025-contact-catalog/025-contact-catalog.md) | `false` | `true` | `false` | `90` |
| [Pseudonym Vault and Key Roles](../60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md) | `false` | `true` | `false` | `90` |
| [Messaging Middleware](../60-solutions/027-messaging-middleware/027-messaging-middleware.md) | `false` | `true` | `false` | `88` |
| [Temporal Storage Convention](../60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md) | `false` | `false` | `false` | `42` |
| [Bounded Deferred Operations](../60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md) | `true` | `true` | `false` | `100` |
