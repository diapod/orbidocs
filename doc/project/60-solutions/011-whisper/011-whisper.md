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

Transport qualification on 2026-10-19 is owned by P035-007/009/010, not Whisper:
34 Matrix/five SQLite cases at clean Node `1bc523a6` / Orbidocs `5993f7d0` qualify
confidence-0.5 gossip and the permitted `whisper-signal.v1`, `whisper-trace.v1`
and `whisper-threshold-reached.v1` families, exact author bytes, independent room
history, local-time admission, restart and carrier replay. Both Node and unmodified
Synapse full-PDU gates pass; fresh retrieval from the adopted local retained store
requalifies identically. Evidence:
`node:docs/evidence/matrix-opaque-envelope/2026-10-19-room-recovery-full/README.md`.
This does not qualify all Whisper/issuance flows, elevate signal epistemic status,
prove homeserver federation or imply independent backups/production readiness.

## Certified contextual authorship

The accepted P015 phase-1 profile has a separately qualified 2026-11-04 path:
local Vault nym, recipient-encrypted AD/INAC certification, protected host review/
signing, no-JS UI and contextual signals/thresholds on SQLite and admitted
Synapse. It counts council-admitted participant sources, not nyms or source
nodes. Ordinary confidence0.5 publication, status/expiry/reset, trusted late time,
privacy, restart/replay and full-PDU acceptance are covered by A30/B31 plus six
separate conformance obligations. Exact loose/extracted and fresh primary/
secondary qualification results match. Evidence: `node:docs/evidence/matrix-opaque-envelope/2026-11-04-whisper-authorship/README.md`.

This is a bounded source-specific composition with operator-only payload; it does
not renew the historical node-counting M4 scope. Host/Vault owns keys and signing,
the optional issuer owns policy, AD owns ciphertext delivery, Agora owns immutable
admission facts, and the contextual evaluator owns current eligibility and the
first-emission latch. Matrix time trusts the authenticated admitted homeserver;
PDU signatures/hashes/size are checked in acceptance. Optional stay-ready runtime,
other P015/P081 consumers, rooms/opt-in, Anon, LLR/ADC, federation and global/release
readiness remain outside this qualification. Component status remains partial.

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

<a id="planned-assessment-exposure-in-curation"></a>

### Local Assessment Exposure in Curation

The [P013 profile and tracker](../../40-proposals/013-whisper-social-signal-exchange.md#assessment-exposure-profile)
bind rumor judgments to [P026's shared gate](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#6-assessment-exposure-and-sealed-rounds).
P013-AE-001 is `partial`; P013-AE-002 remains planned, separate from implemented
Whisper M4. The [P026 local checkpoint](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#local-pilot-evidence-checkpoint-2026-10-24)
qualifies withholding and later rendering of rumor-shaped credibility/rejection
extension fields through the shared view on a generic open resource reference.
That evidence does not introduce a standalone rumor-overlay admission schema or
qualify the complete real Whisper curation, propagation and attention workflow.
Reuse opinion identity/overlay validation and the Agora host's viewer projection;
do not add a Whisper-specific blind-vote store or hide ratings only in UI. The [review checkpoint](../../40-proposals/026-resource-opinions-and-discussion-surfaces.md#local-pilot-review-evidence-checkpoint-2026-10-24) requalifies the common local view and preserves the complete Whisper workflow exclusion.
Peer credibility, rationales, counts and popularity ordering remain withheld
consistently across curation, Agent, search and S039 attention surfaces.

Presentation policy never disables propagation controls, spam suppression or
urgent protective evidence. Rumor arrival counts are not assessment counts.
Optional sealed rounds reuse signed closure/outcomes but do not delay rumor
delivery awaiting quorum. Local hiding makes no claim about other relays or
the independence of a curation verdict. Use the shared negative/replay matrix
and Story-005/Agora fixtures, not a new transport or acceptance framework.

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

### Dormant-Fact Resonance

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/30-stories/story-014-dormant-contest-entry.md`

Responsibilities:
- resolve the versioned JSON decorrelation vocabulary (factory source plus
  local P091 layers) and validate `topic/class` against it;
- derive an epoch pull plan with decoys and pull complete coarse buckets;
- project fact–rumor link decisions and a local "My rumors" view;
- author related rumors that join an existing rumor context;
- hand confirmed contexts to association rooms with explicit sharing controls.

The feature owner and grouping task live in
[P013 dormant-fact resonance](../../40-proposals/013-whisper-social-signal-exchange.md#dormant-fact-resonance-2026-10-27).

Status:
- `future`

### Author Disclosure Conditions

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/30-stories/story-014-dormant-contest-entry.md`

Responsibilities:
- verify nym-signed embargo manifests and their protected-signal/admission
  bindings; recipients verify the public package without protected text;
- derive similarity keys from author-approved correlation descriptors under
  versioned grouping rules;
- keep protected material within the correlation scope under custody
  obligations;
- count distinct contextual sources per epoch and attest the result;
- release pre-redacted payloads after a release commit accepted by the case
  authority and, by default, the author's confirmation, at most once per
  concrete consented audience descriptor, independently of delivery routes;
- keep disclosure conditions separate from coordination thresholds.

The design and tracker live in
[P013 author disclosure conditions](../../40-proposals/013-whisper-social-signal-exchange/author-disclosure-conditions.md#author-disclosure-conditions).

Status:
- `future`

### Cooperative Interest Masking

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Responsibilities:
- keep one origin-tagged pull plan whose `need`, `decoy` and `cover` entries
  share one executor and one timing rule;
- send and accept bounded, motive-free cover requests through private Artifact
  Delivery under the minimal-trace profile;
- keep cover out of interest profiles, personal memory and source counts;
- support the measured comparison with independent decoys.

The design and tracker live in
[P013 cooperative interest masking](../../40-proposals/013-whisper-social-signal-exchange/cooperative-interest-masking.md#cooperative-interest-masking).

Status:
- `future`

### Historical Authorship of Long-Lived Rumors

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`
- `doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`

Responsibilities:
- keep certificate validity, retention, counting horizon and consent validity
  as separate periods;
- store portable admission receipts beside envelope bytes and verify
  historical authorship separately from current status;
- re-contact the author of an old rumor that meets a twin, instead of counting
  the old rumor again;
- keep one continuity key per case, ordered case events and a fresh case
  status, and support case-bound succession of a later nym, delivered only to
  the chosen audience.

The design and tracker live in
[P013 long-lived rumors](../../40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md#long-lived-rumors-and-historical-authorship).

The [private-case execution profile](../../40-proposals/013-whisper-social-signal-exchange/private-case-continuity.md)
separates private exchange Gate A from ordinary-v1 SQLite/Synapse continuity Gate B.
The bounded actual two-endpoint direct Gate A is now independently qualified:
production P037 offers, Memarium protected-signal custody, exact pending case
inbox before separately adopted S020 processing, refusal/fault/restart controls
and selected access-class privacy. Loose, extracted and fresh both-store results
agree. Evidence: `node:docs/evidence/private-case-continuity/2026-11-08-direct-gate-a/README.md`.
Ordinary-v1 SQLite/Synapse Gate B remains open. Synthetic-v2 case credentials and
fixture-signed private v1 signals do not qualify ordinary host/Vault authorship.
Memarium remains the protected-record owner; the case service owns ordered
results, and AD owns transport retry. Minimal AD traces exclude payload/domain
links; authorized receiver-local INAC transport metadata remains visible.
S023-002 scheduled/physical purge is separate. Current remaining composition is
indexed in `node:docs/integration/whisper-private-case-continuity.md`.

The portable receipt format and authenticated admission claim are owned by
[P035-019](../../40-proposals/035-agora-topic-addressed-record-relay.md#portable-admission-receipts-2026-10-27),
not by a second Whisper receipt implementation. The unchanged aggregate-only
promotion rule is in [implementation Layer 7](011-whisper-impl.md#layer-7-threshold-detection-and-durable-promotion).

[P013-LLR-009](../../40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md#portable-case-succession-verification)
plans bounded portable succession verification through those P015/P035 owners.
It keeps historical anchor proof, authentic succession and current case authority
separate, with zero-fetch acceptance and no disclosure of a private anchor merely
to complete a package. It applies P032's cross-artifact verification rule;
P076 is one qualified consumer example, not the owner of the Whisper profile.
The [family matrix](../../40-proposals/013-whisper-social-signal-exchange.md#portable-verification-profiles)
also covers signals, notices, embargo proofs and case control without adding
signatures to CIM's intentionally session-authenticated cover requests.

Status:
- `future`

### Shared Implementation Boundaries

The planned continuations share mechanisms according to
[P013's reuse dispositions](../../40-proposals/013-whisper-social-signal-exchange.md#implementation-reuse):
one epoch pull executor, one contextual contribution evaluator with separate
coordination/disclosure policies, one ordered case owner, and P015/P035 proof
verification. AD retains delivery and retry ownership. The recommendations also
identify small head-comparison and prepared-output reuse boundaries without
merging issuer custody, case authority or transport status. These are design
constraints for the existing trackers, not additional implemented capabilities.

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

- [Structured capability catalogue](011-whisper-caps.edn)

## Notes

Whisper intake/redaction is implemented as a supervised `channel_json` middleware
service with a separately owned intake/trace/operator HTTP surface. Shared, transport-independent
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

P090-006e adds opt-in `middleware-observed-result.v1` carriage around this
unchanged response. The host-owned sidecar binds exact bytes; the intake stores
the private result and draft atomically and verifies retained readback. Missing
ancestry remains unknown, including deterministic transformations of arbitrary
Sensorium input. This partial checkpoint does not grant publication authority
or claim the lifecycle complete. Private sync now seals the exact retained
wrapper under a separate descriptor-addressed idempotency key; it does not
rerun redaction. Manual draft writes clear the source association, including
identical-byte writes. Full Memarium transport/recovery qualification and
deferred/terminal recovery remain in the P090 tracker.
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

### Reviewed Harvester v3 continuation (2026-11-05)

P013-WEB and P078 common review own the approved minimized origin and exact
material inventory. Protected preview/sign v2 resolve an immutable current
review; callers cannot replace text, topic, polarity, origin or custody. AD owns
the finite claims and atomic preview-bound holds. First local publication checks
current review, bytes, generations and holds independently of signature creation.

The v3 receiver law covers every existing author class. New reviewed Harvester
production is derived-local; other producers remain v2 pending the named origin
migration follow-up. The epoch-aligned transitional profile stops new operations
for every producer at its end. Fixture qualification may close this milestone
without production adoption; named recipient support, accepted old-node cutoff
and feasible migration or accepted publication downtime remain rollout conditions.
Public gossip preserves exact per-record origin declarations and lineage coverage
under P013's versioned projector. This continuation is implemented in stages and
not yet qualified as a composed runtime milestone.


The separate composed-review qualification ends before protected authoring:
one local draft and exact restart/replay are verified, while fresh signed Gate
A/B and the full v3 window remain open. The independent P084 campaign gate keeps
those obligations missing. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-COMPOSED-REVIEW-20261105.md`.

### Custody prerequisite checkpoint (2026-11-06)

The current Sensorium campaign explicitly composes native AD prerequisites and
actual expiry-before-review/new-observation checks: 18/131 requirements verified,
113 missing. The new expiry path ends at a local reviewed draft; it performs no
key unlock, authoring sign or Whisper publication. Full signed Gate A/B, the
fixture-window end and recipient cutoff remain open. Production adoption and
global Whisper readiness are unchanged. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-NATIVE-EXPIRY-CAMPAIGN-20261106.md`.

### Issuer authority prerequisite checkpoint (2026-11-06)

The fresh ordinary encrypted-owner attempt reached full issuance request v2 but
refused before a terminal certificate. Separate bootstrap-v2 root authority now
preserves the original v1 signed scope. AD transport admission, local consent,
council certification and P082 recipient authorization remain independent; the
correction grants no publication or raw-original read. Component regressions
pass, while the new ordinary exchange and full signed two-backend qualification
remain open. The historical 18/131 campaign result is not relabelled for changed
runtime/schema bytes. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ISSUER-AUTHORITY-20261106.md`.

### First ordinary v3 certificate checkpoint (2026-11-06)

A fresh ordinary encrypted-owner fixture has issued a v3 certificate over all
four exact TLS/AD phases using separately signed bootstrap-v2 authority.
Independent native inspection verifies `A/issue` and `A/reference-readback`.
Together with fresh same-source R/C/W7/native inputs, the campaign is now
20/131 verified with 111 missing; ordinary/optimized results agree. Original
reports/refusals remain preserved, with process inventory added only in a
separately bound derived view. No Whisper was signed or published.

A separate 128 MiB capacity observation stopped after 2479 retains with an
untyped host cause; a complete DB/WAL copy passes integrity checks. It grants
no load/recovery credit. Full signed SQLite/Synapse, all-producer window-end,
recipient/privacy and remaining load/fault qualification remains open. Existing
P084/P078 and dependent owner trackers stay in progress. This does not adopt
production or renew historical evidence. See
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-FIRST-ISSUANCE-20261106.md`.


### Ordinary cohort scope (2026-11-07)

Exact A2 renewal and separate two-producer v2/v3 end-window controls pass. B and complete independent C/D remain open; successful producer prefixes preserve their refused parent status.
The parent campaign, full Gates A/B and production adoption stay open.
See `node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-ORDINARY-COHORT-20261107.md`.


### Receiver and closed-window checkpoint (2026-11-07)

Node runtime/capture `78911310` and Orbidocs `7a3a3b4f` independently re-execute
7/131 requirements (124 missing), identically with ordinary and optimized readers.
A issue, exact predecessor-bound A2 renew and B issue each publish reviewed v3
through the ordinary SQLite UI. C verifies one source across A/A2; actual A/B
reception produces a threshold and Room proposal after correcting the fixture's
effective exact consumer list. Operator status access is a separate authority
boundary from a supervised module's live channel.

The original R37 parent refuses during post-certificate-expiry S020 polling:
the selected D job is interrupted after 17231 ms against 9999 ms; its refresh
takes 14313 ms. This is not complete contribution-after-expiry qualification.
Separate 21 all-producer v2/v3 end-window refusals and a before-end-adopted,
after-end four-record C read pass native ordinary/optimized inspection. No failed
parent is relabelled, no historical runtime counts are added, and full Gates A/B
and production adoption remain open. A follow-up removes duplicate constructor
recovery in the existing single slot, preserving profile, capacity and media
guards; its native qualification remains open. Exact identities and limits:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-RECEPTION-WINDOW-20261107.md`.


### Exact-renew readiness checkpoint (2026-11-08)

The runtime056 R38 parent remains refused: A publishes reviewed v3, while A2's
exact renew records busy admission followed by original-request expiry. No
complete C/D or post-certificate-expiry contribution follows. A Python fixture
prerequisite now binds A's actual predecessor and observes fresh S020 status
before preparing A2, without changing a prepared deadline or any owner lease.
All 566 regressions and six focused normal/optimized controls pass; native
qualification of this orchestration change is still open. The independent
runtime789 seven-of-131 subset is not transferred to a new source. Exact scope:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-RENEW-READINESS-20261108.md`.


### Paused qualification checkpoint (2026-11-08)

R39 independently verifies 9/131 (122 missing) on retained runtime056 and
capture8b07, identically with ordinary/optimized readers. Exact A2 renew,
same-source and independent A/B reception, ordinary UI/receipts, all-producer
window refusals and historical C read pass. The complete post-certificate-expiry
proof correctly refuses: outer S020 success contains no-work and the retained
evaluation is stale. Unchanged public records do not establish that subclaim.
Work is paused at the owner's request; no new window or production adoption.
The original runtime and reader results remain unchanged. Resume basis:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-V3-RENEW-RECEPTION-20261108.md`.


### Fresh expiry checkpoint (2026-11-12)

R47 on runtime/capture Node `aa580ab20` and Orbidocs `c4ef2611` independently
verifies **10/131**, with 121 unverified rows and identical
ordinary/optimized campaign results, in the aligned fixture window
2026-11-12 16:40–16:50 UTC.
Exact A2 renew uses fresh predecessor status through S020. Independent receiver
C verifies one-source A/A2, two-source A/B and a fresh persisted evaluation after
certificate expiry plus adopted skew; D supplies source-owner status. End-window
refusals and historical read pass. S020 success or `no-work` alone is insufficient.

Historical refusals remain unchanged. Full Gates A/B, the milestone and production
adoption remain open; counts from different source campaigns are not added.
Measured scope, review corrections, original bindings and retention limits:
`node:docs/evidence/sensorium-web/SENSORIUM-WEB-REVIEW-AND-EXPIRY-20261112.md`.
