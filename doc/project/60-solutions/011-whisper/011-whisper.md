# Orbiplex Whisper

`Orbiplex Whisper` is a Node-attached solution component for privacy-bounded
social-signal exchange and small provenance statements. It prepares rumor-style
signals for publication, preserves their weaker epistemic status, coordinates
thresholded association bootstrap, and may carry bounded `whisper-trace.v1`
assertions without silently escalating either signals or traces into evidence.

`Whisper` does not own transport anonymity. It only declares routing and privacy intent on outgoing artifacts and relies on Node egress to satisfy that intent through whatever outbound privacy capability is available.

For public or federation-scoped signals, `Whisper` may use `Orbiplex Agora` as
the durable public/federated record substrate. Agora carries accepted
`agora-record.v1` envelopes and feeds projections; Whisper still owns the
social-signal semantics, threshold lifecycle, and consent boundary.

Threshold and association artifacts are public meta-signals, not public gossip.
`whisper-threshold-reached.v1` states that an issuer or projection observed a
policy-defined correlation. `association-room-proposal.v1` states that there is a
redacted/bootstrap-only coordination proposal. Neither artifact is a public social
narrative; promotion to `public-gossip.v1` requires a later, explicit publication
decision.

`public-gossip.v1` is an explicit publication act, not an automatic projection
product. It may be published independently on a public weak-signal path, or after
an opt-in association room decides to make a public statement. An
`association-room-proposal.v1` is therefore a possible precursor to public gossip,
not a prerequisite.

## Purpose

The component is responsible for the solution-level execution path of:
- rumor intake and local preparation,
- redaction, paraphrase, and idiolect flattening with user approval,
- publication of bounded `whisper-signal` artifacts,
- reception of interest signals,
- threshold recognition,
- and bootstrap of opt-in association rooms.

## Scope

This document defines solution-level responsibilities of the Whisper component.

It does not define:
- concrete module layout in an implementation repository,
- the implementation of transport privacy or onion-like relay,
- final evidentiary case management,
- automatic human enrollment into shared rooms,
- semantic duplicate detection for rumors in v1.

## Post-MVP Extensions

### Artifact Trace Statements

Related schema:
- `whisper-trace.v1`

Whisper trace statements provide a low-cost way to disclose that an artifact was
created, handed to a transport, received, or held. They are signed assertions by
the envelope author, not receipts, attestations, proof of possession, or proof
that the artifact content is true.

The default form contains only SHA-256, byte length, and optional content type or
schema. Digest-only disclosure reduces transferred data but is not anonymous:
predictable content may still be guessed or correlated by digest. Full inline
bytes are allowed only under `digest-and-content`, with an explicit
sender-host-validated `consent/ref`, a hard 32 KiB wire cap, and exact digest and
length verification. The full trace JSON is capped at 128 KiB and the explicit
extension namespace at 8 KiB before signing or admission. The referenced decision must bind the digest, scope,
subject/authority, and validity window; a reference string alone grants no
authority. The ref is sender-local audit linkage, not a network-visible consent
proof, and should not expose a participant id. A trace may reference
`execution-receipt.v1`, an AD delivery fact, or another attestation through
`evidence/refs`; those artifacts remain the evidence authorities.

Trace authoring uses the ordinary signed envelope and existing carriers:

- public or federated traces use `record/kind = "whisper-trace"` and
  `content/schema = "whisper-trace.v1"` under
  `ai.orbiplex.whisper-traces/<trace-kind>`;
- private/direct traces use Artifact Delivery and INAC;
- trace records are excluded from Whisper similarity, threshold, and association
  projections.

Status: `implemented`. The canonical schemas and fixtures, Node schema gate,
transport-independent integrity validation, exact sender-host consent
resolution, authoring and inspection surfaces, metadata-only local read model,
and public Agora plus private AD/INAC carrier smoke are implemented. Trace
publish retries use an atomic idempotency reservation: an active request returns
conflict, a completed request replays its result, and only a failed request may
be reserved again. The local read model applies a 30-day default retention
sweep at startup and on writes; inline content is never retained there.

## Must Implement

### Rumor Intake and Publication

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-signal.v1`

Responsibilities:
- capture rumor-style input without flattening it into evidence,
- run bounded local redaction and idiolect-reduction workflows,
- require user approval before publication,
- implement the bounded intake/redaction path as a separately supervised Rust
  middleware package, with its own operator UI surface and without folding raw
  private intake into Agora or the daemon trusted core,
- store raw user input and intermediate redaction drafts only in local/private
  Memarium state before publication, under explicit retention and quarantine
  policy,
- persist private intake stages as sealed `personal` Memarium facts through host
  capabilities rather than by embedding cryptography in `whisper-intake`; the
  stable fact/artifact kinds are `whisper-intake.raw-private.v1`,
  `whisper-intake.redaction-draft.v1`, `whisper-intake.quarantine.v1`, and
  `whisper-intake.candidate-ready.v1`, with idempotency keys derived from
  `intake_id + stage`,
- allow the redaction/sanitization step to be supplied by another configured
  middleware package, so deterministic fixtures, JSON-e/Sensorium actions, and
  future Inquirium-backed model-assisted redaction can share the same downstream
  contract,
- expose model-assisted redaction through a narrow capability boundary,
  preferably `whisper.redaction.prepare`, where the provider returns a local
  redaction draft and never publishes to Agora or marks a candidate approved,
- allow `whisper.redaction.prepare` to be implemented by JSON-e Flow backed by a
  bounded Sensorium OS action, so the first implementation can run a
  deterministic script or local model command while preserving a future path to
  stronger Inquirium/model-runtime providers,
- emit `whisper-signal` artifacts with explicit epistemic class, node-scoped
  routing, nym-authored pseudonymous participation, envelope-level
  `author/nym-proof`, and routing/privacy intent,
- for Agora M4, publish `whisper-signal.v1` directly as the public/federated
  payload, with envelope authorship by `nym:did:key:...` and with nym proof
  attached at the envelope/policy boundary using an inline-first proof with
  optional refs for longer lineage or reputation history,
- keep private-correlation and direct-only whispers off public Agora topics,
- publish only sanitized public/federated signals through Agora when disclosure
  policy allows that surface.

Status:
- `done` for Agora M4. The shared `whisper-core` implementation boundary now
  owns Agora-independent public/private posture parsing, public Agora disclosure
  denial for `private-correlation` and direct-only signals, and deterministic M4
  threshold/proposal id derivation. Agora consumes that core at ingress/signing
  and in replay-fed projections. The Node workspace now also has the first
  bounded supervised `whisper-intake` Rust middleware seed: it owns local-private
  intake, redaction drafts, quarantine/retention metadata, a server-owned UI
  surface, optional supervised middleware auth-token enforcement for non-health
  routes, and a publishable-candidate guard that reuses `whisper-core`. The
  private persistence boundary is now closed at the middleware level: private
  stages are sealed through host `sealer.seal`, written as `personal` Memarium
  facts through `memarium.write`, tracked with local sync status/error state,
  and retried through an operator action. The Node workspace also ships
  `whisper-intake` as an opt-in bundled supervised middleware package so
  Story-005 profiles can enable it without manual binary wiring.
  M4 intentionally stops at a deterministic local provider boundary: JSON-e Flow
  can route `whisper.redaction.prepare` into Sensorium OS, and Sensorium OS can
  run the local fixture or a locally configured model command. The post-M4
  productization slice adds the host-owned provider-policy shape for
  Inquirium/model-runtime providers and a secretless local Inquirium simulator
  acceptance bridge. Production remote model deployments remain an operator
  configuration and runtime concern.

Model-assisted redaction/paraphrase now has a stable host-capability boundary.
The first concrete M4 provider path is deliberately configuration-driven and
local-only: JSON-e Flow calls `sensorium.directive.invoke`, and Sensorium OS runs
a bounded deterministic `whisper.redaction.prepare` action that returns a draft
for human review. The target contract is:

```text
whisper-intake
  -> host capability whisper.redaction.prepare
  -> configured provider
  -> redaction draft
  -> operator approval
  -> publishable candidate
```

The provider may be JSON-e Flow plus `sensorium.directive.invoke`, where
[Sensorium](../030-sensorium/030-sensorium.md) OS invokes a finite,
timeout-governed script or local model command. This keeps redaction algorithm
choice outside the daemon and Agora. `whisper-core` still validates the final
candidate posture, so a provider cannot bypass the `private-correlation` or
direct-only guards.

The boundary uses `whisper-redaction-prepare-request.v1` and
`whisper-redaction-prepare-response.v1`. In the M4 implementation,
`whisper-intake` sends raw private material by value over the loopback
host-capability call, validates the provider response, persists the returned
draft locally, and leaves publication blocked until explicit operator approval.
`raw/private-material` intentionally accepts any JSON value while the
redaction-preparation contract is still settling across deterministic fixtures,
JSON-e Flow, Sensorium OS actions, and future Inquirium-backed model-assisted
providers. Once the stable provider interface is proven, the field should be narrowed to
`object|string`; scalar, array, and `null` payloads are compatibility slack, not
the intended long-term shape.
When model-assisted preparation is explicitly enabled, missing
`whisper.redaction.prepare` support should fail closed through readiness rather
than presenting a misleading prepare button.

Post-M4 productization is tracked in
`doc/project/60-solutions/011-whisper/011-whisper-impl.md`. The closed
productization slice keeps Whisper's domain contract separate from model
adapters: callers still ask for `whisper.redaction.prepare`, while host policy
selects local deterministic, local model, supervised HTTP model-adapter, or
external model-adapter providers. Inquirium/model-runtime provider calls are
authorized by host-owned `runtime/ref` or profile policy and must not accept a
caller-supplied raw model name as an override. The remaining productization
tracker lives with the Whisper implementation note rather than in a workspace
root draft file.

### Interest and Threshold Coordination

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/30-stories/story-005-whisper-rumor-intake.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

Responsibilities:
- register local relevance without premature disclosure,
- recognize threshold crossings under policy,
- implement the M4 smoke rule as data: at least two distinct eligible nodes,
  same `topic/class`, same deterministic `signal/similarity-key`, and a bounded
  time window,
- derive deterministic bootstrap sets,
- publish `association-room-proposal.v1` as an Agora record on a public/federated
  proposal topic with redacted/bootstrap-only content,
- emit deterministic `whisper-threshold-reached.v1` and
  `association-room-proposal.v1` derived Agora records as
  projection-authority-signed,
  issuer-scoped meta-signal claims when policy allows automatic low-impact
  derived publication,
- prevent derived-record loops with deterministic derived ids,
  source-record-kind exclusion, and derivation refs,
- preserve opt-in enrollment and never create automatic human enrollment,
- expose enough projection state for the Story-005 three-node smoke: node A and
  node B publish similar signals, node C runs Agora, and threshold/proposal state
  is rebuilt from accepted public records,
- keep threshold/proposal artifacts semantically below `public-gossip.v1`: they
  may be replayed, disputed, moderated, weighted by reputation, or ignored by
  local policy, but they do not publish the underlying story.

Status:
- `done` for Agora M4. Node's Agora projection store can project public
  `whisper-signal.v1` records, derive deterministic threshold state for two
  distinct source nodes in the same `topic/class` + `signal/similarity-key`
  group, create association-room proposal projection state, and expose derived
  threshold/proposal drafts for projection-authority signing. Agora service can
  sign and ingest those derived records when a host signer is available.
  Direct and daemon-hosted Story-005 smoke coverage proves the same path with a
  real daemon HostSigner.

### Projection Authority for Threshold and Proposal Claims

Whisper source records are authored by their nym or other admitted source
identity. Threshold and association-room proposal records are different: they are
derived meta-signals and must be signed by a projection authority.

For M4, that projection authority can be the local projection node or a
short-lived delegated projection key. The signature means "this authority applied
this deterministic Whisper projection rule to these source records"; it does not
mean that the community has accepted the underlying story as public truth.

The same contract should admit stronger future authority without changing the
Whisper schemas. A static committee or reputation-selected committee can provide
selection and quorum proofs beside the derived record, and local policy can
decide whether a single authority, a community-trusted quorum, or a stricter
authority class is required for a given UI or moderation consequence.

## May Implement

### Aggregate Topic Notices

Based on:
- `doc/project/20-memos/orbiplex-whisper.md`
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Related schemas:
- `whisper-threshold-reached.v1`

Responsibilities:
- emit coarse aggregate notices after threshold crossing,
- keep those notices weaker than case disclosure,
- separate aggregate discovery hints from raw rumor exchange.

Status:
- `optional`

## Out of Scope

- transport-layer anonymity and relay topology
- final governance or adjudication
- automatic exposure of identities to one another
- hard semantic duplicate suppression in v1
- using Agora for private/direct or `private-correlation` whisper bodies

## Consumes

- `whisper-signal.v1`
- `whisper-interest.v1`

## Produces

- `whisper-signal.v1`
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`

## Related Capability Data

- `whisper-caps.edn`

## Notes

Whisper intake/redaction should be implemented as a supervised HTTP middleware
service attached to Node through explicit contracts. Shared, transport-independent
semantics belong in `whisper-core`; Agora remains the public/federated record
substrate, and the daemon remains the host/supervisor and capability boundary.

The private persistence boundary is:

```text
whisper-intake
  -> host capability sealer.seal
  -> host capability memarium.write(space = personal)
```

`whisper-intake` should authenticate to the host capability API with the
host-provided capability token and identify itself as `whisper-intake`, so the
daemon can apply the runtime component context. Missing `sealer.seal` or
`memarium-space-access` grants for `memarium/write` on `personal` should surface
in the local readiness gate. Runtime sync is automatic best-effort, but the UI
must provide a manual retry action for operators.

The redaction preparation boundary is:

```text
whisper-intake
  -> host capability whisper.redaction.prepare
  -> configured provider
  -> whisper-redaction-prepare-response.v1
  -> local redaction draft
```

The provider is not a publication authority. It may return `draft-ready`,
`needs-human-review`, `unsafe-output`, `policy-denied`, `model-unavailable`,
`retryable-timeout`, or `failed`; only the first two statuses may carry a draft,
and even then the operator approval transition remains separate.
The request schema currently leaves `raw/private-material` deliberately broad so
early providers can pass structured intake envelopes, raw strings, or fixture
values through the same loopback-only boundary. The intended stable contract is
to narrow that field to `object|string` after provider behavior and tests have
converged.

When `Monus` is present, Whisper should treat it as an upstream local draft
preparation module rather than as a peer publication authority. Monus may prepare
candidate concern drafts, but Whisper and the host still own the bounded outgoing
publication path.

`whisper-core` now carries production-shaped policy primitives for source class,
routing failure mode, relay evidence, forwarding budget, privacy downgrade
decisions, correlation policy explanations, association-room proposal lifecycle,
and public-gossip promotion. These are data contracts and pure decision helpers;
concrete UI affordances and real relay execution belong in later runtime/product
layers that consume the same data rather than changing Whisper's core semantics.
