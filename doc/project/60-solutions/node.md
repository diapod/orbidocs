# Orbiplex Node

`Orbiplex Node` is the primary runtime component of the system. It participates in protocol flows, enforces room and policy constraints, preserves provenance, and acts as the main bridge between network-facing protocol semantics and local execution.

Node-scoped roles such as archivist, memarium provider, or sensorium provider are not assumed to be in-process features of a single monolith. They may be implemented as separate programs or processes, written in different languages, as long as they attach to the Node through explicit protocol and API contracts.

## Purpose

The Node is responsible for the solution-level execution path of:
- peer identity, handshake, and endpoint discovery,
- question room lifecycle,
- federated answer procurement,
- supervised local HTTP middleware services for bundled exchange and workflow modules,
- settlement policy coordination and disclosure trail exposure for paid procurement,
- local learning and knowledge promotion,
- archival handoff and retrieval,
- optional transcript observation and later curation/training handoff.

## Scope

This document defines solution-level responsibilities of the Node component.

It does not define:
- concrete module layout in an implementation repository,
- implementation details of Node-attached plugin or process roles,
- rich end-user UI,
- protocol-external payment execution,
- default direct mutation of base models.

## Must Implement

### Peer Identity, Discovery, and Session Baseline

Based on:
- `doc/project/40-proposals/002-comm-protocol.md`
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/50-requirements/requirements-006.md`

Related schemas:
- `node-identity.v1`
- `node-advertisement.v1`
- `peer-handshake.v1`
- `capability-advertisement.v1`
- `signal-marker-envelope.v1`

Responsibilities:
- generate or load a stable local node identity,
- derive and expose a stable `node:did:key`-shaped `node-id`,
- derive and expose a stable `participant:did:key`-shaped `participant-id`,
- resolve the signing key through `key/storage-ref` rather than inline secret material,
- publish or consume signed endpoint advertisements,
- establish signed peer handshakes and capability exchange over the baseline transport,
- publish and validate the first participant-scoped signed application envelope above the session layer,
- maintain keepalive and reconnect behavior for the first networked Node baseline.

Note:
- The v1 `node-id` is Node-local and intentionally uses a `did:key`-compatible Ed25519/base58btc fingerprint shape rather than claiming full support for the generic `did:key` method, DID Document expansion, or generic DID resolution.
- The persisted v1 identity contract should carry `key/storage-ref` only; the MVP resolver baseline is `local-file:identity/node-signing-key.v1.json`.
- The MVP baseline assumes one operator-participant per Node by default. `node-id` names the infrastructure role, while `participant-id` names the participation role; the two identifiers may share the same underlying `did:key` fingerprint in v1 without collapsing their protocol semantics.
- The networking slice should need only `node-id`, `participant-id`, and the signing or verification material for those roles. Higher identity layers such as `anchor-identity`, `pod-user-id`, `nym`, or federation continuity bindings belong above that slice rather than inside it.
- The v1 handshake stays node-scoped and uses fresh ephemeral X25519 session keys in `session/pub`; the static key-agreement contribution is derived from the Ed25519 `node:did:key` identity for the MVP baseline rather than being re-advertised as separate long-lived X25519 state.
- Participant authentication belongs to participant-scoped application artifacts carried over that encrypted node-to-node session, not to the handshake itself.
- The minimal explicit advertised core capability in v1 is `core/messaging`; successful baseline participation and signed-handshake ability are treated as protocol-native facts rather than mandatory advertised capabilities.
- `WSS/TLS` in v1 is only the carrier transport: TLS server authentication protects the endpoint and the channel, while peer identity still binds at the signed `peer-handshake.v1` layer; public endpoints should follow normal WebPKI hostname validation, and private trust roots remain deployment-local rather than protocol-visible.
- Key rotation is not a live continuity feature in the MVP baseline; a new Ed25519 key still means a new `node-id`, but the operational layer may already prepare a local signed overlap bundle and `succession` hint without assigning automatic discovery or trust continuity semantics.
- `node-advertisement.v1` may already carry a future-facing `succession` object, but the Node does not yet assign it active runtime continuity semantics in the MVP baseline.
- In the MVP baseline, thin clients or remote UI sessions are delegated operator sessions of that same participant role, not independent hosted users with their own continuity layer.

Status:
- `todo`

### Question Room Lifecycle

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/30-stories/story-004.md`
- `doc/project/50-requirements/requirements-001.md`

Related schemas:
- `question-envelope.v1`
- `answer-room-metadata.v1`
- `response-envelope.v1`

Responsibilities:
- open or bind a room to `question/id`,
- enforce exposure mode and room policy profile,
- preserve provenance across room outputs.

Status:
- `todo`

### Federated Answer Procurement

Based on:
- `doc/project/30-stories/story-001.md`
- `doc/project/40-proposals/011-federated-answer-procurement-lifecycle.md`
- `doc/project/50-requirements/requirements-001.md`

Related schemas:
- `service-offer.v1`
- `service-order.v1`
- `procurement-offer.v1`
- `procurement-contract.v1`
- `procurement-receipt.v1`
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

Responsibilities:
- expose standing service-offer discovery and buyer-side service-order ingress for
  marketplace-style exchange,
- own the bridge from `service-order.v1` into the currently executable
  selected-responder procurement substrate,
- collect and evaluate offers,
- select responders under policy,
- record contracts and receipts without coupling protocol semantics to crypto rails,
- expose the effective `gateway-policy` and `escrow-policy` context for paid procurement,
- suppress or degrade paid procurement paths when settlement disclosures mark a blocking or degraded state.

Status:
- `todo`

### Settlement Policy Coordination and Disclosure Trail

Based on:
- `doc/project/30-stories/story-007.md`
- `doc/project/40-proposals/016-supervised-prepaid-gateway-and-escrow-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/50-requirements/requirements-007.md`
- `doc/project/50-requirements/requirements-008.md`

Related schemas:
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`
- `gateway-receipt.v1`
- `ledger-hold.v1`

Responsibilities:
- ingest and expose the active settlement policy references relevant to paid procurement,
- retain auditable joins from procurement artifacts to settlement policies and later disclosure events,
- expose degraded, blocked, or manual-review-only settlement states as first-class operational facts,
- keep this visibility separate from protocol-external payment execution and fiat rail mechanics.

Status:
- `todo`

### Settlement-Capable Node Profile

The baseline Node does not automatically become a payment processor or escrow
authority just because it supports paid procurement.

Two deployment profiles are expected:

- `policy-consuming Node`:
  - consumes `gateway-policy.v1`, `escrow-policy.v1`, and
    `settlement-policy-disclosure.v1`,
  - gates paid procurement according to those artifacts,
  - preserves audit joins from procurement contracts and receipts,
  - does not itself execute fiat rail operations or supervise holds.
- `settlement-capable Node`:
  - does everything above,
  - additionally hosts or attaches trusted gateway and/or escrow services,
  - emits or serves settlement-facing artifacts such as `gateway-policy.v1`,
    `escrow-policy.v1`, `settlement-policy-disclosure.v1`,
    `gateway-receipt.v1`, and `ledger-hold.v1` through explicit contracts,
  - does not yet freeze a concrete MVP HA profile beyond one logical settlement
    authority and no split-brain behavior,
  - may later swap the storage backend to MariaDB or a similar replicated engine as
    long as one logical settlement authority and protocol-visible contract
    compatibility are preserved,
  - remains accountable through policy-bound roles rather than by collapsing the
    whole Node into one opaque settlement monolith.

In other words, settlement capability is a deployment profile layered onto the
Node, not the default meaning of `Orbiplex Node`.

### Story-006 Marketplace Deployment Roles

For the marketplace baseline from `story-006.md`, the minimal logical deployment
shape around Node should be made explicit:

- `buyer-orchestrator node`
  Roman-side Node hosting `Arca`, buyer-local workflow state, and local packaging.
- `provider nodes`
  service-providing Nodes hosting `Dator` and publishing standing offers.
- `gateway node`
  trusted ORC ingress/egress boundary emitting `gateway-receipt.v1`.
- `escrow supervisor node`
  trusted settlement authority creating and releasing `ledger-hold.v1`.
- `service-catalog role`
  bounded catalog ownership for remote observed offers and fetch/push exchange;
  in the preferred deployment this is owned by `Dator`, while
  `catalog-listener` remains a compatibility relay.
- `arbiter node`
  optional or policy-dependent role for `arbiter-confirmed` and dispute paths.

Hard MVP may co-locate `gateway`, `escrow`, `catalog`, and even `arbiter` into one
deployment, but their responsibilities should remain distinct at the protocol and
audit level.

### Supervised Local HTTP Middleware Services

Based on:
- `doc/project/40-proposals/019-supervised-local-http-json-middleware-executor.md`
- `doc/project/40-proposals/020-bundled-python-middleware-modules.md`
- `doc/project/50-requirements/requirements-010.md`
- `doc/project/50-requirements/requirements-011.md`
- `doc/project/30-stories/story-006.md`

Responsibilities:
- host the supervised `http_local_json` executor as a first-class daemon-owned
  middleware runtime,
- distribute `Orbiplex Dator` and `Orbiplex Arca` with the hard-MVP Node release,
- run both bundled modules as supervised Python middleware services rather than as
  unmanaged sidecars,
- attach those modules through the host-owned `http_local_json` connector/executor,
- expose `middleware.dator` and `middleware.arca` as operator-visible components
  with lifecycle, readiness, and restart state,
- delegate local standing offer lifecycle and participant-facing publication to
  `Dator`, while keeping outbound relay transport and peer-session routing in
  the daemon,
- expose host capabilities such as `offers.local.query` and
  `peer.session.establish` so middleware may compose daemon-local offers with
  middleware-owned observed offers without taking ownership of peer transport,
- keep bundled middleware under the same host-owned envelope and policy contracts
  as any future replaceable external module,
- remain the future host-granted capability surface for local modules such as
  `Orbiplex Monus`, including bounded memory/read-model access, local signal
  summaries, model-assisted draft shaping, and bounded publication requests
  without yielding direct transport or publication authority to the middleware.

Status:
- `done`

### Local Learning and Knowledge Promotion

Based on:
- `doc/project/30-stories/story-002.md`
- `doc/project/50-requirements/requirements-002.md`

Related schemas:
- `learning-outcome.v1`
- `knowledge-artifact.v1`

Responsibilities:
- classify outcomes as `confirmed`, `corrected`, or `unresolved`,
- promote only policy-accepted outcomes,
- keep unresolved material out of trusted retrieval by default.

Status:
- `todo`

### Archivist and Vault Handoff

Based on:
- `doc/project/30-stories/story-003.md`
- `doc/project/40-proposals/012-learning-outcomes-and-archival-contracts.md`
- `doc/project/50-requirements/requirements-003.md`

Related schemas:
- `archival-package.v1`
- `archivist-advertisement.v1`
- `retrieval-request.v1`
- `retrieval-response.v1`

Responsibilities:
- prepare archival packages,
- select archivists under policy,
- preserve publication scope, integrity, and retrieval provenance.

Status:
- `todo`

## May Implement

### Transcript Monitoring

Based on:
- `doc/project/40-proposals/008-transcription-monitors-and-public-vaults.md`
- `doc/project/50-requirements/requirements-004.md`
- `doc/project/50-requirements/requirements-005.md`

Related schemas:
- `transcript-segment.v1`
- `transcript-bundle.v1`

Responsibilities:
- observe only policy-allowed traffic,
- preserve consent and human-origin semantics,
- emit transcript artifacts suitable for curation.

Status:
- `optional`

## Consumes

- `question-envelope.v1`
- `retrieval-response.v1`
- `archivist-advertisement.v1`
- `gateway-policy.v1`
- `escrow-policy.v1`
- `settlement-policy-disclosure.v1`

## Produces

- `answer-room-metadata.v1`
- `response-envelope.v1`
- `learning-outcome.v1`
- `knowledge-artifact.v1`
- `archival-package.v1`

## Related Capability Data

- `node-caps.edn`

## Notes

Implementation-specific decomposition, file ownership, and delivery status belong in the concrete Node repository.

Role components attached to the Node may live in separate repositories, runtimes, or processes. This document defines what the Node must coordinate and expose, not that every role must be compiled into one binary.

Settlement-capable deployments may attach gateway or escrow roles as separate
services. The Node still remains the operator-facing coordination point for
policy context, disclosure trail visibility, and procurement gating.
