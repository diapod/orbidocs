# Orbiplex Root Component Map

Status: Living architecture map
Scope: Root-level map of major Orbiplex components, host-owned primitives,
protocol substrates, node-attached organs, and proposal-backed horizon areas.
Last synchronized: 2026-07-13

This diagram is intentionally not a runtime flow diagram. It shows broad
component containment, attachment, and stratum membership. Edges mean
"architecturally related to", "hosted by", or "uses as a substrate" rather
than "calls synchronously" or "sends data to".

The map is synchronized against the current proposal and solution catalogs. The
solution sidecar files under `doc/project/60-solutions/*/*-caps.edn` are the
primary source for solution components and coarse status. Proposal documents
under `doc/project/40-proposals/` are represented either through promoted
solution components or, when no solution component exists yet, in the
proposal-backed horizon box.

``` mermaid
flowchart TB
  subgraph AccessSurfaces["Access, Client, and Operator Surfaces"]
    UI["Node UI<br/>HTMX / Tauri-hosted shell"]
    AssistantChannel["Inquirium Assistant Channel<br/>advise-first inquiry surface"]
    Control["Control CLI / API clients<br/>operator automation"]
    PodClients["Pod-backed thin clients<br/>hosted user access"]
    APIProjection["API Surface Projection<br/>aggregated OpenAPI + surface catalog"]
  end

  subgraph NodeRuntime["Node Host Runtime Stratum"]
    Daemon["Daemon<br/>host runtime, lifecycle, dispatch"]
    LocalReadiness["Local Readiness Gate<br/>bootstrap + signed config admission"]
    CapabilityRegistry["Capability Registry<br/>core ids + policy sidecars"]
    Gate["Capability Binding<br/>caller binding + passport authorization"]
    Notifications["Notifications<br/>operator + user notification plane"]
    InteractionBroker["Interaction Broker<br/>host-mediated interaction control plane"]
  end

  subgraph HostPrimitives["Host-Owned Runtime Primitives"]
    BoundedServer["Bounded Local Server Runtime<br/>bounded listeners + child lifecycle"]
    ModuleStore["Host-Owned Module Store<br/>signed package activation"]
    MiddlewareHost["Middleware Host<br/>extension lifecycle + routing"]
    Scheduler["Replay Scheduler<br/>bounded periodic/manual jobs"]
    Deferred["Bounded Deferred Operations<br/>long-running operation lifecycle"]
    TemporalStorage["Temporal Storage Convention<br/>events + projections + compaction"]
  end

  subgraph IdentitySecurity["Identity, Authority, and Privacy Stratum"]
    NodeTransport["Transport + Discovery<br/>WSS sessions, peer governor, succession"]
    TLS["TLS Trust Policy<br/>TOFU/pinned/federated trust"]
    PseudonymVault["Pseudonym Vault + Key Roles<br/>participant, nym, routing-subject roles"]
    KeyPassports["Key Delegation Passports<br/>delegated signing authority"]
    Signer["Signer<br/>generic signing surface"]
    Sealer["Sealer<br/>AEAD key + envelope surface"]
    CapabilityAdvertisement["Capability Advertisement<br/>public capability surfaces"]
    AgoraAuthority["Agora Authority<br/>protected namespace policy"]
  end

  subgraph DataAndRelationship["Local Data, Memory, and Relationship Stratum"]
    Memarium["Memarium<br/>local memory organ"]
    Classification["Classification<br/>policy labels + propagation"]
    Relationship["Local Relationship Layer<br/>contact/trust substrate"]
    ContactCatalog["Contact Catalog<br/>private contact discovery"]
    Room["Room<br/>generic subject-addressed room primitive"]
    SemanticIndex["Semantic Index<br/>node-local retrieval projection"]
    Corpus["Corpus<br/>topic-routed collaborative reasoning"]
  end

  subgraph DeliveryMessaging["Delivery, Messaging, and Artifact Movement"]
    ArtifactDelivery["Artifact Delivery<br/>host-owned delivery + admission"]
    INAC["INAC<br/>private/direct artifact transport"]
    Messaging["Messaging Middleware<br/>personal message delivery"]
    ContactAttestation["Contact Attestation<br/>relationship proof surface"]
    RawSignal["Raw Signal Access<br/>declared raw-context access"]
  end

  subgraph MiddlewareOrgans["Node-Attached Organs and Middleware Modules"]
    AgoraLocal["Agora Service<br/>local topic relay + projections"]
    Dator["Dator<br/>provider catalog + service dispatch"]
    Arca["Arca<br/>buyer workflow orchestration"]
    SharedOfferCatalog["Shared Offer Catalog<br/>federated offers over Agora"]
    Monus["Monus<br/>host-granted local observation"]
    Whisper["Whisper<br/>social-signal intake + threshold bootstrap"]
    Anon["Anon<br/>nym / privacy surface"]
    Sensorium["Sensorium<br/>local enaction stratum + workbench"]
    Inquirium["Inquirium<br/>bounded model inquiry organ"]
    Ferment["Ferment<br/>developer/tooling surface"]
  end

  subgraph MarketAndSettlement["Service Exchange, Procurement, and Settlement"]
    ServiceOffers["Service Offer / Order Contracts<br/>offer-order-procurement bridge"]
    Procurement["Procurement Lifecycle<br/>requests, offers, acceptance, delivery"]
    Ledger["Host Ledger / ORC Settlement<br/>accounts, holds, transfers, receipts"]
    Escrow["Supervised Escrow<br/>dispute windows + partial release"]
    Gateway["Gateway Receipts<br/>fiat/credit bridge audit trail"]
  end

  subgraph FederationSubstrates["Federated Shared Substrates"]
    SeedDirectory["Seed Directory<br/>peer + capability catalog"]
    Agora["Agora<br/>topic-addressed record substrate"]
    SharedCatalogNetwork["Shared Offer Catalog Network<br/>offer publication + listener"]
    Harness["Multi-Node Federation Harness<br/>trace explorer + smoke topology"]
  end

  subgraph ProposalHorizon["Proposal-Backed Horizon / Not Yet Root Runtime Components"]
    AgentOrgan["Agent Orchestration Organ<br/>bounded stateful agents"]
    WorkflowCatalog["Workflow + Service Schema Catalogs<br/>templates, schemas, task types"]
    Reputation["Membership + Reputation Bootstrap<br/>public adjudication + sanctions"]
    Recovery["Identity Recovery Service<br/>recovery service + client recovery"]
  end

  UI --- Daemon
  UI --- AssistantChannel
  AssistantChannel --- Inquirium
  Control --- Daemon
  PodClients --- Daemon
  APIProjection --- Daemon

  Daemon --- LocalReadiness
  Daemon --- CapabilityRegistry
  Daemon --- Gate
  Daemon --- Notifications
  Daemon --- InteractionBroker
  Daemon --- Inquirium

  Daemon --- BoundedServer
  Daemon --- ModuleStore
  Daemon --- MiddlewareHost
  Daemon --- Scheduler
  Daemon --- Deferred
  Daemon --- TemporalStorage

  Gate --- CapabilityRegistry
  Gate --- KeyPassports
  Gate --- Signer
  Gate --- Sealer
  Gate --- CapabilityAdvertisement

  Daemon --- NodeTransport
  NodeTransport --- TLS
  NodeTransport --- SeedDirectory
  NodeTransport --- INAC
  NodeTransport --- CapabilityAdvertisement
  NodeTransport --- PseudonymVault

  PseudonymVault --- KeyPassports
  PseudonymVault --- Messaging
  PseudonymVault --- Anon

  MiddlewareHost --- RawSignal
  MiddlewareHost --- AgoraLocal
  MiddlewareHost --- Memarium
  MiddlewareHost --- Dator
  MiddlewareHost --- Arca
  MiddlewareHost --- Monus
  MiddlewareHost --- Whisper
  MiddlewareHost --- Anon
  MiddlewareHost --- Sensorium
  MiddlewareHost --- Ferment
  ModuleStore --- MiddlewareHost
  BoundedServer --- MiddlewareHost

  Memarium --- Classification
  Memarium --- SemanticIndex
  Memarium --- Corpus
  ContactCatalog --- Relationship
  Messaging --- ContactCatalog
  Messaging --- ContactAttestation
  Room --- Messaging
  Room --- Corpus
  Relationship --- Reputation

  ArtifactDelivery --- INAC
  ArtifactDelivery --- AgoraLocal
  ArtifactDelivery --- Messaging
  ArtifactDelivery --- MiddlewareHost
  RawSignal --- Memarium

  Dator --- ServiceOffers
  Arca --- Procurement
  SharedOfferCatalog --- ServiceOffers
  ServiceOffers --- Procurement
  Procurement --- Ledger
  Ledger --- Escrow
  Ledger --- Gateway
  Dator --- SharedOfferCatalog
  Arca --- SharedOfferCatalog

  AgoraLocal --- Agora
  AgoraLocal --- AgoraAuthority
  AgoraAuthority --- CapabilityRegistry
  SharedOfferCatalog --- SharedCatalogNetwork
  SharedCatalogNetwork --- Agora
  SeedDirectory --- CapabilityAdvertisement
  Harness --- NodeTransport
  Harness --- Agora

  Inquirium --- AgentOrgan
  Inquirium --- Sensorium
  Inquirium --- Corpus
  AgentOrgan --- Deferred
  AgentOrgan --- Scheduler
  WorkflowCatalog --- Arca
  WorkflowCatalog --- Dator
  Recovery --- PseudonymVault
  Recovery --- NodeTransport
  Reputation --- CapabilityRegistry

  classDef done fill:#e8f5e9,stroke:#2e7d32,color:#102a13
  classDef partial fill:#fff8e1,stroke:#f9a825,color:#302500
  classDef mvp fill:#e0f2f1,stroke:#00796b,color:#102725
  classDef planned fill:#e3f2fd,stroke:#1565c0,color:#0d2238
  classDef draft fill:#f3e5f5,stroke:#6a1b9a,color:#26102f
  classDef convention fill:#eceff1,stroke:#455a64,color:#102027

  class Gate,CapabilityRegistry,Signer,Sealer,CapabilityAdvertisement,Memarium,AgoraLocal,Whisper,RawSignal,ModuleStore,BoundedServer,MiddlewareHost,Scheduler,Deferred,ArtifactDelivery,TemporalStorage,Relationship,SharedOfferCatalog,APIProjection,Room,Sensorium,Inquirium,AssistantChannel,AgentOrgan,Corpus done
  class Daemon,UI,Arca,Dator,INAC,KeyPassports,InteractionBroker partial
  class Monus,Anon,SemanticIndex planned
  class Classification,AgoraAuthority,WorkflowCatalog,Reputation,Recovery draft
  class TLS,SeedDirectory,ContactCatalog,PseudonymVault,Messaging mvp
  class TemporalStorage convention

  click UI "../../project/60-solutions/001-node-ui/001-node-ui.md" "Orbiplex Node UI"
  click Daemon "../../project/60-solutions/000-node/000-node.md" "Orbiplex Node"
  click LocalReadiness "../../project/40-proposals/050-local-readiness-gate.md" "Local Readiness Gate"
  click CapabilityRegistry "../../project/60-solutions/037-capability-registry/037-capability-registry.md" "Capability Registry"
  click Gate "../../project/60-solutions/006-capability-binding/006-capability-binding.md" "Capability Binding"
  click Notifications "../../project/60-solutions/039-notifications/039-notifications.md" "User and Operator Notifications"
  click InteractionBroker "../../project/60-solutions/035-interaction-broker/035-interaction-broker.md" "Interaction Broker"
  click BoundedServer "../../project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md" "Bounded Local Server Runtime"
  click ModuleStore "../../project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md" "Host-Owned Module Store"
  click MiddlewareHost "../../project/60-solutions/019-middleware/019-middleware.md" "Middleware"
  click Scheduler "../../project/60-solutions/020-scheduler/020-scheduler.md" "Replay Scheduler"
  click Deferred "../../project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md" "Bounded Deferred Operations"
  click TemporalStorage "../../project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md" "Temporal Storage Convention"
  click NodeTransport "../../project/40-proposals/014-node-transport-and-discovery-mvp.md" "Node Transport and Discovery MVP"
  click TLS "../../project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md" "TLS Trust Policy"
  click PseudonymVault "../../project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md" "Pseudonym Vault and Key Roles"
  click KeyPassports "../../project/60-solutions/014-key-delegation-passports/014-key-delegation-passports.md" "Key Delegation Passports"
  click Signer "../../project/40-proposals/037-generic-signing-service.md" "Generic Signing Service"
  click Sealer "../../project/60-solutions/005-sealer/005-sealer.md" "Sealer"
  click CapabilityAdvertisement "../../project/60-solutions/007-capability-advertisement/007-capability-advertisement.md" "Capability Advertisement"
  click AgoraAuthority "../../project/60-solutions/021-agora-authority/021-agora-authority.md" "Agora Authority"
  click Memarium "../../project/60-solutions/002-memarium/002-memarium.md" "Memarium"
  click Classification "../../project/60-solutions/018-classification/018-classification.md" "Classification"
  click Relationship "../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md" "Local Relationship Layer"
  click ContactCatalog "../../project/60-solutions/025-contact-catalog/025-contact-catalog.md" "Contact Catalog"
  click Room "../../project/60-solutions/036-room/036-room.md" "Room"
  click SemanticIndex "../../project/60-solutions/022-semantic-index/022-semantic-index.md" "Semantic Index"
  click Corpus "../../project/60-solutions/038-corpus/038-corpus.md" "Corpus"
  click ArtifactDelivery "../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md" "Artifact Delivery"
  click INAC "../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md" "Inter-Node Artifact Channel"
  click Messaging "../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md" "Messaging Middleware"
  click ContactAttestation "../../project/40-proposals/061-contact-attestation-service.md" "Contact Attestation Service"
  click RawSignal "../../project/60-solutions/013-raw-signal-access/013-raw-signal-access.md" "Raw Signal Access"
  click AgoraLocal "../../project/60-solutions/008-agora/008-agora.md" "Agora"
  click Dator "../../project/60-solutions/004-dator/004-dator.md" "Dator"
  click Arca "../../project/60-solutions/003-arca/003-arca.md" "Arca"
  click SharedOfferCatalog "../../project/60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md" "Shared Offer Catalog"
  click Monus "../../project/60-solutions/009-monus/009-monus.md" "Monus"
  click Whisper "../../project/60-solutions/011-whisper/011-whisper.md" "Whisper"
  click Anon "../../project/60-solutions/010-anon/010-anon.md" "Anon"
  click Sensorium "../../project/60-solutions/030-sensorium/030-sensorium.md" "Sensorium"
  click Ferment "../../project/60-solutions/012-ferment/012-ferment.md" "Ferment"
  click ServiceOffers "../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md" "Service Offers and Orders"
  click Procurement "../../project/40-proposals/011-federated-answer-procurement-lifecycle.md" "Procurement Lifecycle"
  click Ledger "../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md" "Gateway and Escrow MVP"
  click Escrow "../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md" "Supervised Escrow"
  click Gateway "../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md" "Gateway Receipts"
  click SeedDirectory "../../project/60-solutions/031-seed-directory/031-seed-directory.md" "Seed Directory"
  click Agora "../../project/60-solutions/008-agora/008-agora.md" "Agora"
  click SharedCatalogNetwork "../../project/60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md" "Shared Offer Catalog"
  click Harness "../../project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md" "Multi-Node Federation Harness"
  click Inquirium "../../project/60-solutions/044-inquirium/044-inquirium.md" "Inquirium"
  click AssistantChannel "../../project/60-solutions/045-inquirium-assistant-channel/045-inquirium-assistant-channel.md" "Inquirium Assistant Channel"
  click AgentOrgan "../../project/60-solutions/047-agent/047-agent.md" "Agent"
  click WorkflowCatalog "../../project/40-proposals/029-workflow-template-catalog.md" "Workflow Template Catalog"
  click Reputation "../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md" "Membership and Reputation Bootstrap"
  click Recovery "../../project/40-proposals/030-identity-recovery-service.md" "Identity Recovery Service"
```

## Reading Notes

1. The diagram is a map of responsibility boundaries, not a message-flow trace.
   It intentionally groups several proposal details behind promoted solution
   components where the solution now owns the architectural surface.
2. `Daemon` is the local host runtime. It owns lifecycle, dispatch,
   supervision, local APIs, and the host-owned composition boundary.
3. `Capability Binding`, `Capability Registry`, `Key Delegation Passports`,
   `Signer`, and `Sealer` are shown as separate authority strata. Authorization,
   policy naming, delegated authority, signing, and sealing should not collapse
   into one hidden helper.
4. `Host-Owned Runtime Primitives` are reusable mechanisms that component authors
   should check before creating private infrastructure: bounded servers, module
   store, middleware host, replay scheduler, deferred operations, and temporal
   storage conventions.
5. `Middleware Host` is the attachment stratum for node-attached organs and
   bundled modules. It is not only a plugin loader; it owns routing, lifecycle,
   raw-signal declaration, module reports, host capability calls, and supervised
   local HTTP boundaries.
6. `Artifact Delivery` is the host-owned delivery and admission plane. `INAC` is
   underneath it as a private/direct transport adapter, while Agora-backed
   publishing remains a federated substrate path.
7. `Agora Service` is the local node-attached module/adapter. `Agora` is the
   federated topic-addressed record substrate. Keeping them separate prevents
   local relay/projection details from becoming protocol semantics.
8. `Dator`, `Arca`, and `Shared Offer Catalog` form the current service-exchange
   plane. Service offers/orders bridge into procurement; procurement bridges into
   ledger/escrow/gateway contracts. The diagram shows that path even where the
   ledger rail is still represented primarily by proposals and schemas.
9. `Pseudonym Vault + Key Roles` is local/private identity machinery. It supports
   nym, routing-subject, and recovery-related flows without publishing the
   participant root or local-only DH material as standing discovery artifacts.
10. `Proposal-Backed Horizon` captures active proposal families that shape the
    architecture but are not yet root runtime components in the solution catalog.
    They should be promoted into solution components when their boundaries become
    stable enough.
11. Status coloring is coarse: green means solution-level `done` or equivalent;
    yellow means partial; blue means planned or MVP-ready/hard-MVP-done; purple
    means draft/proposal-backed horizon; gray marks architecture conventions.

## Component and Proposal Links

### Root Runtime and Client Surfaces

- [Orbiplex Node](../../project/60-solutions/000-node/000-node.md)
- [Orbiplex Node UI](../../project/60-solutions/001-node-ui/001-node-ui.md)
- [API Surface Projection](../../project/60-solutions/034-api-surface-projection/034-api-surface-projection.md)
- [Pod-Backed Access Layer for Thin Clients](../../project/40-proposals/006-pod-access-layer-for-thin-clients.md)

### Host Runtime Primitives

- [Bounded Local Server Runtime](../../project/60-solutions/016-bounded-local-server-runtime/016-bounded-local-server-runtime.md)
- [Host-Owned Module Store](../../project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md)
- [Middleware](../../project/60-solutions/019-middleware/019-middleware.md)
- [Replay Scheduler](../../project/60-solutions/020-scheduler/020-scheduler.md)
- [Bounded Deferred Operations](../../project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md)
- [Temporal Storage Convention](../../project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md)

### Identity, Authority, and Policy

- [Node Transport and Discovery MVP](../../project/40-proposals/014-node-transport-and-discovery-mvp.md)
- [TLS Trust Policy](../../project/60-solutions/024-tls-trust-policy/024-tls-trust-policy.md)
- [Pseudonym Vault and Key Roles](../../project/60-solutions/026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md)
- [Key Delegation Passports](../../project/60-solutions/014-key-delegation-passports/014-key-delegation-passports.md)
- [Generic Signing Service](../../project/40-proposals/037-generic-signing-service.md)
- [Sealer](../../project/60-solutions/005-sealer/005-sealer.md)
- [Capability Binding](../../project/60-solutions/006-capability-binding/006-capability-binding.md)
- [Capability Advertisement](../../project/60-solutions/007-capability-advertisement/007-capability-advertisement.md)
- [Capability Registry](../../project/60-solutions/037-capability-registry/037-capability-registry.md)
- [Agora Authority](../../project/60-solutions/021-agora-authority/021-agora-authority.md)

### Data, Memory, Relationship, and Rooms

- [Memarium](../../project/60-solutions/002-memarium/002-memarium.md)
- [Classification](../../project/60-solutions/018-classification/018-classification.md)
- [Local Relationship Layer](../../project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md)
- [Contact Catalog](../../project/60-solutions/025-contact-catalog/025-contact-catalog.md)
- [Room](../../project/60-solutions/036-room/036-room.md)
- [Semantic Index](../../project/60-solutions/022-semantic-index/022-semantic-index.md)
- [Corpus](../../project/40-proposals/069-corpus.md)

### Delivery, Messaging, and Artifacts

- [Artifact Delivery](../../project/60-solutions/023-artifact-delivery/023-artifact-delivery.md)
- [Inter-Node Artifact Channel](../../project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md)
- [Messaging Middleware](../../project/60-solutions/027-messaging-middleware/027-messaging-middleware.md)
- [Contact Attestation Service](../../project/40-proposals/061-contact-attestation-service.md)
- [Raw Signal Access](../../project/60-solutions/013-raw-signal-access/013-raw-signal-access.md)

### Node-Attached Organs and Middleware Modules

- [Agora](../../project/60-solutions/008-agora/008-agora.md)
- [Dator](../../project/60-solutions/004-dator/004-dator.md)
- [Arca](../../project/60-solutions/003-arca/003-arca.md)
- [Shared Offer Catalog](../../project/60-solutions/033-shared-offer-catalog/033-shared-offer-catalog.md)
- [Monus](../../project/60-solutions/009-monus/009-monus.md)
- [Whisper](../../project/60-solutions/011-whisper/011-whisper.md)
- [Anon](../../project/60-solutions/010-anon/010-anon.md)
- [Sensorium](../../project/60-solutions/030-sensorium/030-sensorium.md)
- [Ferment](../../project/60-solutions/012-ferment/012-ferment.md)

### Exchange, Federation, and Proposal Horizon

- [Service Offers, Service Orders, and Procurement Bridge](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [Federated Answer Procurement Lifecycle](../../project/40-proposals/011-federated-answer-procurement-lifecycle.md)
- [Supervised Prepaid Gateway and Escrow MVP](../../project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md)
- [Seed Directory](../../project/60-solutions/031-seed-directory/031-seed-directory.md)
- [Multi-Node Federation Harness and Trace Explorer](../../project/40-proposals/074-multi-node-federation-harness-and-trace-explorer.md)
- [Inquirium](../../project/40-proposals/063-inquirium-model-inquiry-organ.md)
- [Agent](../../project/60-solutions/047-agent/047-agent.md)
- [Workflow Template Catalog](../../project/40-proposals/029-workflow-template-catalog.md)
- [Membership and Reputation Bootstrap](../../project/40-proposals/051-swarm-membership-and-reputation-bootstrap.md)
- [Identity Recovery Service](../../project/40-proposals/030-identity-recovery-service.md)
