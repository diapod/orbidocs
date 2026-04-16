# Orbiplex Root Component Map

Status: Draft  
Scope: Root-level map of major Orbiplex components and architectural strata.

This diagram is intentionally not a runtime flow diagram. It shows broad
component containment, attachment, and stratum membership. Edges mean
"architecturally related to" rather than "calls" or "sends data to".

``` mermaid
flowchart TB
  subgraph ClientSurfaces["Client and Operator Surfaces"]
    UI["Node UI<br/>control + inspection"]
    Control["Control CLI / API client<br/>operator automation"]
  end

  subgraph NodeRuntime["Node Runtime Stratum"]
    Daemon["Daemon<br/>host runtime + dispatch"]
    Gate["Host capability gate<br/>capability-binding"]
    PeerChain["PeerMessageChain<br/>protocol middleware"]
  end

  subgraph CoreCapabilities["Core Host Capabilities"]
    Signer["Signer<br/>signing surface"]
    Sealer["Sealer<br/>AEAD key + envelope surface"]
  end

  subgraph MiddlewareStratum["Node-Attached Middleware Stratum"]
    Middleware["Middleware attachment contract<br/>host-owned routing + lifecycle"]

    subgraph LocalMiddleware["Local / in-process middleware"]
      Memarium["Memarium<br/>local memory organ"]
    end

    subgraph BundledMiddleware["Bundled middleware"]
      Dator["Dator<br/>bundled HTTP-supervised<br/>provider catalog + offers"]
      Arca["Arca<br/>bundled HTTP-supervised<br/>buyer workflow orchestration"]
    end

    subgraph SupervisedHttpMiddleware["Other HTTP-supervised middleware"]
      Monus["Monus<br/>local observation module"]
      Whisper["Whisper<br/>rumor / signal intake"]
      Anon["Anon<br/>nym / privacy surface"]
    end
  end

  subgraph SharedSubstrate["Federated Shared Substrate"]
    AgoraClient["Agora Client<br/>local relay adapter"]
    Agora["Agora<br/>topic-addressed record substrate"]
    SeedDirectory["Seed Directory<br/>peer + capability catalog"]
  end

  UI --- Daemon
  Control --- Daemon
  Daemon --- Gate
  Daemon --- PeerChain
  Daemon --- Signer
  Daemon --- Sealer
  PeerChain --- Middleware
  Middleware --- Memarium
  Middleware --- Dator
  Middleware --- Arca
  Middleware --- Monus
  Middleware --- Whisper
  Middleware --- Anon
  Dator --- AgoraClient
  Arca --- AgoraClient
  Memarium --- AgoraClient
  AgoraClient --- Agora
  Daemon --- SeedDirectory

  click UI "../../../project/60-solutions/node-ui/" "Orbiplex Node UI"
  click Daemon "../../../project/60-solutions/node/" "Orbiplex Node"
  click Gate "../../../project/60-solutions/capability-binding/" "Capability Binding"
  click Signer "../../../project/40-proposals/037-generic-signing-service/" "Generic Signing Service"
  click Sealer "../../../project/60-solutions/sealer/" "Sealer"
  click Memarium "../../../project/60-solutions/memarium/" "Memarium"
  click Dator "../../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener/" "Dator / catalog listener"
  click Arca "../../../project/40-proposals/021-service-offers-orders-and-procurement-bridge/" "Arca / procurement bridge"
  click Monus "../../../project/60-solutions/monus/" "Monus"
  click Whisper "../../../project/60-solutions/whisper/" "Whisper"
  click Anon "../../../project/60-solutions/anon/" "Anon"
  click AgoraClient "../../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener/" "Agora-facing catalog listener"
  click Agora "../../../project/40-proposals/035-agora-topic-addressed-record-relay/" "Agora"
  click SeedDirectory "../../../project/40-proposals/025-seed-directory-as-capability-catalog/" "Seed Directory"
```

## Reading Notes

1. The diagram is a map of responsibility boundaries, not a message-flow trace.
2. The `Daemon` is the local host runtime. It owns dispatch, supervision, and
   host capability routing.
3. `Signer` and `Sealer` are core host capabilities exposed through the daemon.
4. `Middleware / PeerMessageChain` is the host-owned attachment stratum for
   modules that observe, enrich, publish, or orchestrate work without becoming
   hidden daemon internals.
5. `Memarium` is shown as local/in-process middleware because it may need
   co-lifecycle with the daemon and full message-flow observation.
6. `Dator` and `Arca` are shown as bundled middleware. In the hard-MVP shape
   they are also HTTP-supervised modules, but containment here uses packaging
   responsibility as the primary grouping.
7. `Monus`, `Whisper`, and `Anon` are shown as other HTTP-supervised middleware
   candidates until their final packaging contracts settle.
8. `Agora Client` is the local adapter shape for publishing to, or observing,
   the shared `Agora` substrate. It is separated from `Agora` itself to keep
   local integration concerns distinct from the federated record substrate.
9. Some middleware nodes currently link to proposal documents until dedicated
   solution pages exist.

## Component Links

- [Orbiplex Node](../../project/60-solutions/node.md)
- [Orbiplex Node UI](../../project/60-solutions/node-ui.md)
- [Capability Binding](../../project/60-solutions/capability-binding.md)
- [Generic Signing Service](../../project/40-proposals/037-generic-signing-service.md)
- [Sealer](../../project/60-solutions/sealer.md)
- [Memarium](../../project/60-solutions/memarium.md)
- [Dator / Federated Catalog Listener](../../project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md)
- [Arca / Procurement Bridge](../../project/40-proposals/021-service-offers-orders-and-procurement-bridge.md)
- [Monus](../../project/60-solutions/monus.md)
- [Whisper](../../project/60-solutions/whisper.md)
- [Anon](../../project/60-solutions/anon.md)
- [Agora](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [Seed Directory](../../project/40-proposals/025-seed-directory-as-capability-catalog.md)
