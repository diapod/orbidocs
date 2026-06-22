# Solution 013: Whisper — Social Signal Exchange — Implementation Guidelines

Proposal: `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Solution: `doc/project/60-solutions/011-whisper/011-whisper.md`

Capability catalog: `doc/project/60-solutions/011-whisper/011-whisper-caps.edn`

Related impl notes:
- `doc/project/60-solutions/008-agora/008-agora-topic-addressed-relay-impl.md` (carrier for public whispers)
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel-impl.md` (carrier for private whispers)

## Purpose of this document

This note is the implementation entry point for Orbiplex Whisper. It does
**not** duplicate solution-level responsibilities (that lives in
`whisper.md`), the per-capability status catalog (that lives in
`whisper-caps.edn`), or the fine-grained backlog (that lives in the
sibling `node` repository alongside the other Whisper implementation
notes).

It exists to:

- name the layers that have to be built,
- fix the invariants that hold *across* layers (envelope-vs-content
  split, signing domain, pseudonymous authorship semantics,
  `disclosure/scope` distribution rule),
- track current status per layer so the next implementer knows where
  to start,
- enumerate the open decisions that must be resolved before
  implementation can meaningfully proceed,
- give a stable commit order when shaping the whisper stack,
- own the post-M4 productization tracker formerly kept as a workspace-root draft
  note.

## Current implementation status

This implementation note started as a layer-by-layer build plan. The layer
tables below are useful for historical sequencing, but the authoritative current
status is:

- `whisper-signal.v1`, `whisper-threshold-reached.v1`, and
  `association-room-proposal.v1` are implemented for the Agora M4 public signal
  path.
- Public/federated Whisper records are carried as `agora-record.v1` envelopes
  with `content/schema = "whisper-signal.v1"`.
- Public Whisper authorship is nym-authored at the envelope boundary:
  `author/participant-id = nym:did:key:...` requires verifier-usable
  `author/nym-proof`; private-correlation and direct-only signals are rejected
  on public Agora topics.
- `whisper-intake` exists as a bounded supervised Rust HTTP middleware with its
  own operator UI surface, local-private SQLite intake store, host-authenticated
  loopback API, sealed `personal` Memarium sync for raw/draft/quarantine/candidate
  stages, and manual retry for private sync.
- `whisper.redaction.prepare` is the stable redaction/paraphrase capability
  boundary. The first provider path is deterministic and local:
  JSON-e Flow calls `sensorium.directive.invoke`, and Sensorium OS runs a
  bounded `whisper.redaction.prepare` action. The provider returns a draft for
  human review; it never publishes to Agora and never marks a candidate approved.
- Node C's Agora projection can derive deterministic threshold/proposal state
  from two eligible public signals, sign derived records through the host signer,
  ingest them through the ordinary Agora path, and prevent derived-record loops.
- Story-005 now has a three-node laptop operator pack and English/Polish
  runbooks that exercise A/B Whisper Intake plus C Agora projection. The hard-MVP
  readiness snapshot treats this Story-005/M4 path as complete.

Post-M4 productization is tracked below in this document. It covers richer
external Inquirium/model-runtime redaction policy, outbound privacy realization,
production correlation, association-room lifecycle, production Monus/Sensorium
source integration, and explicit public-gossip promotion behind the same
Whisper/Agora envelope boundary.

## Post-M4 productization invariants

These invariants apply to every later productization slice. They are stricter
than the current M4 smoke because the M4 smoke proves only the minimal public
correlation path.

1. **Host-owned authority.** Whisper may request redaction, routing,
   correlation, or publication, but host policy decides provider selection,
   privacy resolution, projection authority, and final publication authority.
   Model/runtime selection goes through Inquirium/model-runtime routing, not a
   caller-supplied raw model name. Outbound privacy is resolved by host policy,
   not by a caller naming a concrete relay.
2. **Facts before views.** Meaningful transitions should leave append-only
   facts before any read-model or UI view is updated: raw intake accepted,
   redaction requested, draft produced, candidate approved/rejected/quarantined,
   privacy resolution attempted, signal published/refused, threshold observed,
   room proposal created, participant invited/accepted/rejected/left, and
   public-gossip promotion proposed/approved/published/refused.
3. **Privacy is a policy boundary.** `routing/profile`,
   `routing/failure-mode`, `disclosure/scope`, and `classification` are not
   decorative metadata. Private-correlation and direct-only signals must not
   reach public Agora topics. `hard-fail + onion-relayed` must refuse when no
   onion-capable path exists. Providers may draft or diagnose, but may not
   approve, publish, or widen disclosure scope.
4. **Domain capability before provider mechanism.** The caller-facing redaction
   contract remains `whisper.redaction.prepare`. JSON-e Flow, Sensorium OS,
   Inquirium/model-runtime, simulator adapters, and remote model adapters are
   provider mechanisms behind that boundary. Neutral adapter output must be
   translated back into `whisper-redaction-prepare-response.v1` before Whisper
   consumes it.
5. **Deterministic smoke, richer production.** M4 deterministic matching remains
   the replayable baseline. Production correlation may add semantic features,
   trust-tier diversity, source-class weighting, and richer threshold policy,
   but every threshold decision must remain reconstructable from source facts
   and an explicit policy version.

## Post-M4 productization dependency map

The slice names are topical, not a strict build order.

- **Already closed for M4:** deterministic public/federated correlation over
  `topic/class + signal/similarity-key`, projection-authority threshold/proposal
  emission, the secretless Inquirium simulator adapter, and the Story-005 local
  profile acceptance bridge.
- **Hard prerequisite for model-backed redaction providers:** daemon
  `inquirium.generate` must invoke HTTP adapter instances through host-owned
  `runtime/ref` and `model.binding/ref`. This is implemented for the simulator
  and remote-provider adapter seam.
- **Independent contract tracks:** redaction provider policy, outbound privacy
  resolver data, semantic correlation policy data, source-class validation, and
  public-gossip promotion facts may evolve independently as long as they preserve
  the invariants above.
- **Strict runtime ordering:** association-room lifecycle runtime must exist
  before public-gossip promotion from room/case state can be productized.
  Monus/Sensorium source-class carry-through must exist before correlation can
  weight or exclude those sources.
- **Continuous hygiene:** any schema-visible source/evidence field must be
  mirrored into `node/protocol/contracts/schemas` and schema-gated before code
  starts enforcing it. Tracker status changes must update this document, the
  Node implementation ledger, and the MVP readiness snapshot when readiness
  interpretation changes.

## Post-M4 productization tracker

Status values:

- `done` — implemented and covered by tests, schema validation, or documented
  operator evidence;
- `partial` — contract or primitive exists, but runtime/UI/product behavior is
  incomplete;
- `not-started` — not yet implemented beyond conceptual documentation;
- `deferred` — intentionally postponed beyond the current productization pass.

### Redaction provider policy and simulator bridge

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Keep `whisper.redaction.prepare` as the domain boundary above provider mechanisms | done | Solution text and Story-005 docs preserve the boundary; adapters do not become publication authorities. |
| Host-owned provider policy for local deterministic, local model, supervised HTTP adapter, and external model adapter classes | partial | Policy shape is documented and the simulator/remote adapter substrate exists; full operator-facing provider policy UX and remote deployment profiles remain later work. |
| Inquirium/model-runtime provider selection by `runtime/ref` or profile, not raw caller model name | done | Daemon `inquirium.generate` routes through host-owned runtime/model-binding context and rejects model override. |
| Translate neutral adapter or `GenerateResponse` output into `whisper-redaction-prepare-response.v1` | partial | Boundary requirement is documented; deterministic provider path is implemented. Full model-backed redaction bridge for production providers remains a later slice. |
| Metadata-only diagnostics for provider calls | partial | Inquirium trace records are metadata-only; Whisper-specific provider-call diagnostic views remain product work. |
| JSON-e Flow inference grants for `inquirium.generate` provider bridges | done | Host capability path fails closed without explicit inference grants. |
| Secretless supervised Inquirium simulator adapter | done | Story-005 simulator is opt-in, egress-free, exposes simulated bindings, rejects unknown bindings, and is tested through daemon Host API. |
| Story-005 simulator local profile and acceptance checks | done | Local profile enables the simulator explicitly, verifies routability, generation, fail-closed unknown binding, stop/start non-routability, and restoration. |

### Anon / outbound privacy realization

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Host-owned outbound privacy resolver contract | done | `whisper-core` parses routing failure mode, relay constraints, forwarding hops, and forwarding budget; `whisper-intake` now consumes the resolver before public/private publish. |
| Represent `direct`, `relayed`, and `onion-relayed` routability states | done | `whisper-core` carries typed posture data. |
| Fail closed for `hard-fail + onion-relayed` without an onion-capable path | done | Core contract and tests cover refusal semantics. |
| Relay capability discovery based on capability evidence | partial | `whisper-intake` now reads host-owned `agora.relay` capability provider evidence for publish preflight and requires passport-scoped relay class data rather than deriving classes from module labels. Federation-scale relay discovery and Anon relay routing remain Node/Anon runtime work. |
| Derived forwarding nym scope, TTL, replay, and idempotency rules | partial | Scope contract exists in the Anon/Whisper implementation ledger row; concrete relay runtime consumption remains partial. |
| First derived-nym relay transport path for Whisper egress | not-started | Required post-MVP Anon runtime work. |
| Operator/user visibility for privacy downgrade before publication | partial | `whisper-intake` returns operator-visible preflight reasons, writes a private preflight fact through host `memarium.write`, validates host signing/write responses, and requires explicit downgrade acknowledgement before publish. Richer UI remains product work. |
| Acceptance proving `soft-fail` and `hard-fail` egress behavior end to end | partial | Core behavior and `whisper-intake` preflight behavior are covered; full Anon relay runtime acceptance remains pending. |

### Production correlation policy

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Keep M4 deterministic rule as `correlation_policy = deterministic-m4` | done | M4 projection uses deterministic `topic/class + signal/similarity-key`. |
| Policy fact schema for richer threshold configuration | partial | Production-shaped policy primitives exist; durable policy-fact lifecycle remains product work. |
| Trust-tier diversity option | partial | Schema fields expose trust summaries/tiers; runtime threshold weighting remains pending. |
| Semantic feature extraction contract without raw rumor-text exposure | not-started | Needs explicit feature/digest contract and provider path. |
| Treat embeddings as derived sensitive content with bounded persistence | not-started | Must be defined with Inquirium embedding/data-plane policy. |
| Semantic correlation explainability surface | not-started | Needs threshold explanation read model and operator diagnostics. |
| Source-class weighting and exclusion rules | partial | `source/class` is carried and parsed; weighting/exclusion policy is not productized. |
| Version policy used by every threshold decision | partial | Deterministic M4 is replayable; richer policy-version facts remain pending. |
| Replay-equivalence tests across policy versions | not-started | Required once richer policy facts exist. |

### Association-room lifecycle

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Decide module ownership: Whisper proposal semantics vs dedicated association runtime | partial | Whisper owns proposal semantics; `agora-projections` now owns the first local association-room read model and lifecycle fact seed. Dedicated room/case-management runtime remains later work. |
| Define room lifecycle facts | partial | `association-room-proposal.v1` exists; Node now persists bounded local `association_room_lifecycle_facts` for room state transitions with FK-backed proposal references. Richer room/case facts remain pending. |
| Invite/accept/reject/expire transitions | partial | Node now exposes minimal operator-driven transitions using the `whisper-core` FSM, with authenticated actor binding and path/request bounds on the operator control route. Enrollment UX and expiration scheduler remain pending. |
| Moderation/witness policy data | not-started | Required room/runtime policy work. |
| Room transcript/storage classification policy | not-started | Required before real case-management rooms. |
| Operator/user UI for opt-in enrollment | partial | Operator HTTP API can transition proposals into rooms; full user enrollment UX is not built. |
| Close/leave/retention semantics | partial | The FSM supports close/leave and Node persists transitions; retention policy and room transcript storage remain pending. |
| Acceptance proving no automatic human enrollment from threshold/proposal | done | M4 threshold/proposal smoke stops at proposal state. |

### Monus/Sensorium production sources

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Source-class validation in `whisper-core` | done | `direct-user`, `pod-user`, `operator-observed`, `derived-local`, `monus-derived`, and `monus-sensorium-derived` are parsed. |
| `monus-derived` draft submission contract | not-started | Monus remains planned/partial; no production handoff runtime. |
| `monus-sensorium-derived` evidence requirement for Sensorium host capability at author time | partial | `whisper-intake` now requires a source evidence ref before publishing `monus-sensorium-derived` candidates. Live Sensorium evidence verification remains pending. |
| Protocol-visible evidence refs, schema sync, and schema-gate fixtures if needed | not-started | Add only when evidence refs become wire-visible. |
| Stricter review defaults for machine-derived signals | not-started | Needs Whisper intake policy/UI work. |
| Help-mode/emergency diversion policy | partial | `whisper-intake` now fails closed for Monus-derived candidates that indicate help-mode diversion. Full emergency/help workflow remains pending. |
| Preserve source class through candidate and public signal metadata | partial | Content schema/core can carry it; complete source integrations remain pending. |
| UI indicators for machine-derived and sensor-informed drafts | not-started | Product/UI work. |

### Public-gossip promotion

| Work item | Status | Evidence / remaining work |
|---|---|---|
| Promotion proposal fact from room/case state to `public-gossip.v1` draft | partial | Node now stores explicit public-gossip promotion drafts from accepted association rooms with bounded opaque lineage refs. Publication remains a separate act. |
| Approval policy: participant quorum, moderator approval, or local governance policy | not-started | Required before promotion runtime. |
| Final redaction review at promotion time | not-started | Required before `public-gossip.v1` publication from rooms. |
| Publish `public-gossip.v1` only as a separate explicit act | done | Story/Solution semantics forbid automatic threshold/proposal promotion. |
| Lineage refs to threshold/proposal/room decision without leaking private rumor text | partial | Promotion drafts now persist opaque lineage refs. Schema-level public promotion artifacts and tombstone semantics remain pending. |
| Refusal, withdrawal, and tombstone semantics | not-started | Required public-gossip lifecycle work. |
| Acceptance proving threshold/proposal does not automatically emit public gossip | done | M4 smoke asserts threshold/proposal stops below public gossip. |

## Architectural posture

Whisper is **not** a transport; it is a **content kind plus an
authoring/reception pipeline** that rides on two distribution surfaces:

1. **Agora** (proposal 035) — for `disclosure/scope` values other than
   `private-correlation`; topic convention:
   `ai.orbiplex.whispers/<topic-class>` (proposal 046).
2. **INAC** (proposal 042) — for `private-correlation`, for
   `routing/profile = direct`, and for any scope the participant
   prefers to keep off a public substrate.

The wire format on both surfaces is the **same** signed
`agora-record.v1` envelope; only the transport and the addressable
scope differ. The `whisper-signal.v1` schema validates only the
content body — identity, authorship, timing, and routing key live in
the envelope.

## Invariants that cross layers

These must be identical wherever they appear. If they drift between
layers, pseudonymous authorship, cross-surface verification, or
threshold detection will silently diverge.

1. **Envelope-vs-content split.**
   - `whisper-signal.v1` validates the content body **only**.
     `required` starts with the const discriminator
     `schema: "whisper-signal.v1"`.
   - All identity, authorship signature, nym certificate reference,
     authoring timestamp, record id, and topic routing key are
     envelope concerns (proposal 035 §3).
   - Any implementation that re-introduces `signal/id`, `created-at`,
     `sender/*`, `rumor/nym`, `auth/nym-certificate`, or
     `auth/nym-signature` into the content body is regressing this
     split and MUST be rejected at review.

2. **Signing domain.** `AGORA_RECORD_DOMAIN_V1 = "agora.record.v1"` is
   the sole signing domain for whisper envelopes. The signing key is
   the author's when `author/participant-id` begins with
   `participant:did:key:…`, and the nym's when it begins with
   `nym:did:key:…`. No separate whisper-specific signing domain.

3. **Pseudonymity is an envelope property.** Pseudonymous whispers
   are expressed in the envelope through:
   - `author/participant-id = "nym:did:key:…"`,
   - `author/nym-certificate-ref` pointing at a
     `nym-certificate.v1`,
   - envelope `signature` made by the nym private key.

   The attestation-gate (proposal 041 §5) is the single authority
   that validates nym certificates and enforces council/scope
   policy. Whisper code does not re-implement this check.

4. **`disclosure/scope` as distribution-surface selector.**
   - `private-correlation` → INAC direct exchange.
   - `federation-scoped`, `cross-federation`, `public-aggregate-only`
     → Agora.
   - Public Agora deployments SHOULD refuse `private-correlation` at
     ingest (proposal 013 §Distribution note on intentional SHOULD);
     closed federations MAY relax. The rule lives in each relay's
     ingest policy, not in whisper code.

5. **Transport-identifier separation.** `sender/node-id` and
   `sender/federation-id` are peer-session concerns; they MUST NOT
   leak into the signed content body or the envelope. Transport
   identity and authored identity are distinct axes.

6. **Byte-identical envelopes across surfaces.** A whisper authored
   for INAC delivery and later promoted to Agora (threshold crossing,
   §Layer 7) MUST carry the **same** envelope bytes. No re-signing
   on surface migration; `record/id` is stable.

## Layer 0 — JSON Schemas

Canonical schemas:

- `whisper-signal.v1` — content body (**done**, content-body-only
  rewrite complete after proposal 013 Next Action #7).
- `whisper-interest.v1` — interest registration artifact for
  threshold detection (**not started**; fields and lifecycle are an
  open decision, see §Open Decisions).
- `whisper-threshold-reached.v1` — aggregate notice after threshold
  crossing (**not started**).
- `association-room-proposal.v1` — bootstrap artifact for opt-in
  association rooms (**not started**).
- `nym-certificate.v1` — reused from proposal 015 (exists).
- `agora-record.v1` — reused from proposal 035 (exists).

Publication: schemas are served through the daemon's schema surface
(same style as `key-delegation`). Schema names are stable; surface
(Agora vs INAC) is not encoded in the schema id.

### Status

| Schema | State |
|---|---|
| `whisper-signal.v1` | ✅ done |
| `whisper-interest.v1` | ❌ not started |
| `whisper-threshold-reached.v1` | ❌ not started |
| `association-room-proposal.v1` | ❌ not started |

## Layer 1 — Kind registration

Whisper must be registered as a first-class kind in every substrate
that carries or stores it.

| Where | What to register | State |
|---|---|---|
| Agora kinds table (proposal 035 §3) | `whisper-signal.v1` + topic convention for `ai.orbiplex.whispers/<topic-class>` | 🟡 convention resolved in 046; kind registration still pending |
| Agora kinds table | `whisper-durable.v1` for threshold-promoted whispers | 🟡 mentioned in 013 §5, kind not yet registered |
| Artifact Delivery inbound acceptor for INAC-carried private/direct artifacts | `whisper-signal.v1` acceptor + authorization modes allowed | ❌ not started (INAC and Artifact Delivery not started) |
| Memarium observe rules | capture envelope byte-identically + action-trace for whisper lifecycle | ❌ not started |

## Layer 2 — Envelope builder and canonicalization

One authoring primitive that produces a signed `agora-record.v1`
envelope from validated whisper content:

```
build_whisper_envelope(
  content: WhisperSignalV1,            // schema-validated
  author: ParticipantOrNym,
  nym_cert_ref: Option<NymCertRef>,    // required when author is Nym
  topic_key: Option<String>,           // Some("ai.orbiplex.whispers/<topic-class>") for Agora, Some("private/<name>") for INAC
  authored_at: DateTime<Utc>,
  signer: SigningService,              // proposal 037
) -> Result<AgoraRecord, WhisperEnvelopeError>
```

Responsibilities:

- JCS canonicalization of the unsigned envelope,
- `record/id = sha256:<base64url-no-pad(sha256(canonical_bytes))>`,
- signature in `agora.record.v1` domain using the author's or nym's
  private key via the signing service,
- verification that the signer's returned `key_public` binds to
  `author/participant-id` (same hard-check rule as `agora-core` sign
  adapter, proposal 035 impl §Layer 1),
- population of `record/id`, `signature.value`, and
  `author/nym-certificate-ref` when applicable.

Crate placement suggestion: `node/whisper-core` (new crate), modeled
on `agora-core`'s sign adapter but specialized for whisper content
validation and the nym-or-participant authorship choice.

### Status

| Component | State |
|---|---|
| `build_whisper_envelope` | ❌ not started |
| Whisper content validator against `whisper-signal.v1` | ❌ not started |
| Nym-authorship binding check (envelope `signature` key vs `nym:` in `author/participant-id`) | ❌ not started |
| Golden vectors for whisper canonical bytes and `record/id` | ❌ not started |

## Layer 3 — Authoring flow (whisper-core)

The authoring pipeline turns raw rumor input into a publish-ready
envelope. Stages:

1. **Intake** — from a direct user, pod-user, operator observation,
   derived-local producer, Monus, or Monus+Sensorium (mapped to
   `source/class` enum).
2. **Redaction and idiolect flattening** — bounded local workflow,
   sanitizes text before publication (proposal 013 Must-Implement
   §Rumor Intake and Publication). Output is the value that lands in
   `signal/text`.
3. **User approval** — MUST be explicit before publication; no
   silent publishing. Approval is a Memarium action-trace entry.
4. **Content validation** — against `whisper-signal.v1`, including
   the `allOf` routing consistency rules.
5. **Envelope building** — §Layer 2.
6. **Distribution-surface selection** — §Layer 4.

### Status

| Stage | State |
|---|---|
| Intake adapter trait (pluggable per `source/class`) | ❌ not started |
| Redaction/sanitization pipeline | ❌ not started |
| Approval step wired to Memarium action-trace | ❌ not started |
| Content validator | ❌ not started |
| Envelope builder | ❌ not started (Layer 2) |

## Layer 4 — Distribution routing

Policy router chooses the outbound path per whisper:

```
route_whisper(envelope, content) =
  match (content.disclosure_scope, content.routing_profile):
    ("private-correlation", _)        → INAC::push(…, inac.invitation passport)
    (_, "direct")                     → INAC::push(…)
    (_, "relayed" | "onion-relayed")  → Agora::publish(topic = envelope.topic_key)
```

Both paths share the same envelope bytes. The router also enforces
`routing/failure-mode`:

- `soft-fail`: if the selected surface is unavailable, downgrade per
  policy (e.g. publish as `whisper-durable` on Agora only after the
  operator-configured soft-fail rule allows it),
- `hard-fail`: refuse to publish at all rather than leak through an
  unapproved surface.

### Status

| Component | State |
|---|---|
| Router predicate table | ❌ not started |
| Agora publisher (HTTP POST to `/v1/agora/topics/{key…}/records`) | 🟡 Agora HTTP API exists; whisper-specific client wrapper not started |
| INAC publisher | ❌ not started (INAC not implemented) |
| `routing/failure-mode` enforcement | ❌ not started |

## Layer 5 — Reception

Receiver-side ingest is split across the two surfaces but uses the
**same** attestation-gate (proposal 041 §9).

### Agora ingest (public whispers)

- Topic ACL (proposal 035 §5) evaluates before persistence.
- Attestation-gate (proposal 041) validates:
  - `nym-certificate` presence and scope when
    `author/participant-id` is `nym:`,
  - `disclosure/scope` against relay policy (public deployments
    SHOULD refuse `private-correlation`; enforcement is per-relay
    ingest policy),
  - rate budget per author and per topic,
  - any deployment-specific predicates
    (`nym_council_in`, `pseudonymous_authorship`, etc.).
- Accepted records: subject-index update, SSE broadcast, Matrix
  federation bridge.
- Memarium write on the receiver's side (if the receiver is a
  subscriber).

### INAC ingest (private whispers)

- Same attestation-gate (one verifier + one cache across surfaces).
- Authorization source: typically `inac.invitation` passport for
  direct delivery, or `whisper.receive` general passport for
  subscribers known to the sender.
- Memarium write is the primary side effect; there is no public
  index.

### Status

| Component | State |
|---|---|
| Attestation-gate crate | ❌ not started |
| `PassportResolutionCache` shared with Agora | ❌ not started |
| Nym-certificate resolver | 🟡 certificate schema exists; resolver not started |
| Whisper-specific ingest predicates (`disclosure_scope_in`, `content_field_in`, …) | ❌ not started (open decision in proposal 041) |
| Matrix federation bridge for whisper topics | 🟡 generic bridge exists; topic-pattern allowlist for `ai.orbiplex.whispers/*` not configured |

## Layer 6 — Memarium integration

Memarium is the local authoritative archive for every whisper the
node authored or received (proposal 013 §Distribution →
§Memarium as local storage).

| Concern | State |
|---|---|
| Store envelope byte-identically (autor i receiver) | 🟡 Memarium has byte-identical storage primitive; whisper-specific observe rule not written |
| Action-trace for whisper lifecycle (draft, redact, approve, publish, forward, interest-count, threshold-crossing) | ❌ not started |
| Per-whisper privacy policy (replay, forward, expose) | ❌ not started (new policy class) |
| Indefinite self-custody default for own whispers | ✅ inherited from proposal 040 §4 |
| Retention policy for received whispers (receiver's own choice) | 🟡 generic Memarium retention applies; whisper-specific defaults not set |

## Layer 7 — Threshold detection and durable promotion

From proposal 013 §5: when enough whispers correlate on
`topic/class` + `context/facets`, the signal may be promoted to
durable public presence as `whisper-durable.v1`.

| Component | State |
|---|---|
| Local correlation index over `topic/class` + `context/facets` (computed from Memarium) | ❌ not started |
| Threshold policy (count, time window, per-federation variance) | ❌ not started (policy decision, not protocol) |
| `whisper-interest.v1` registration flow | ❌ not started (schema also missing) |
| `whisper-threshold-reached.v1` emission on crossing | ❌ not started |
| Explicit consent step before durable promotion (013 §6) | ❌ not started |
| `whisper-durable.v1` content schema | ❌ not started |
| Agora kind registration for `whisper-durable.v1` | ❌ not started |
| Cross-surface migration (same envelope bytes, different surface; §Invariant 6) | ❌ not started |

## Layer 8 — Source integrations

| Source | Integration contract | State |
|---|---|---|
| Direct user (compose UI) | Node UI composer → whisper-core intake adapter | ❌ not started |
| Pod-user | Pod → daemon whisper submit endpoint → intake adapter | ❌ not started |
| Operator-observed | Operator middleware → intake adapter with `operator-observed` source/class | ❌ not started |
| Derived-local | Local producer → intake adapter with `derived-local` | ❌ not started |
| Monus | Monus host capability → draft producer → intake adapter with `monus-derived` | ❌ not started |
| Monus + Sensorium | Sensorium → Monus → intake adapter with `monus-sensorium-derived` | ❌ not started |

## Open decisions blocking implementation

These must be resolved (short decisions, not full proposals) before
Layer 1+ can be built coherently.

1. **Topic-key convention for Agora whispers.** Resolved by proposal
   046: public/federated whispers use
   `ai.orbiplex.whispers/<topic-class>`. Direct/private
   `private-correlation` artefacts use `private/<name>` while on INAC
   and MUST NOT be submitted to Agora.

2. **Predicate grammar for `disclosure/scope` filtering in
   attestation-gate.** Proposal 041 §5 needs a
   `content_field_in(path, values)` predicate (or specialised
   `disclosure_scope_in`), so public relays can refuse
   `private-correlation` at ingest without custom code. Decision
   lives in proposal 041 §5 grammar extension.

3. **`whisper-interest.v1` contract.** Fields, lifecycle, whether
   it is a signed Agora record or an INAC-only artifact, whether
   counting is per-node or per-nym-with-scope-protection. Decision
   lives in a new proposal (likely 043) or an extension of 013.

4. **`whisper-durable.v1` content schema shape.** Whether it
   carries the original `whisper-signal.v1` content body verbatim
   plus aggregate metadata, or whether it is a separate
   aggregate-only shape. Decision informs Layer 7.

5. **Threshold policy home.** Whether threshold parameters (count,
   window) are per-topic-class defaults in the kind registry, or
   per-federation configuration, or per-node operator knobs.
   Affects where the policy lives and who can tune it.

## MVP boundaries

Keep these restrictions explicit in both code and docs during MVP:

- one author per whisper; no co-signatures,
- `source/class = monus-sensorium-derived` requires a present
  Sensorium host capability at author time (fail-closed),
- `routing/profile = onion-relayed` is accepted as intent but the
  MVP does not ship an onion-routing realization; requests with
  `hard-fail` + `onion-relayed` on a node without such capability
  MUST refuse to publish,
- threshold detection is local-only in MVP; no cross-federation
  gossip of interest counts,
- durable promotion requires an explicit user consent step; no
  automatic promotion in MVP,
- `whisper-interest.v1` and `whisper-threshold-reached.v1` are MVP
  scope but `association-room-proposal.v1` is post-MVP.

## Recommended commit order

Each step should leave the tree in a compiling state.

1. **Resolve open decisions 1 (topic key) and 2 (predicate
   grammar).** Cheap; unblocks schemas and gate.
2. **Layer 0.** `whisper-interest.v1` schema (open decision 3
   first).
3. **Layer 2 — envelope builder.** `whisper-core` crate with
   content validator + envelope sign adapter. Golden vectors.
4. **Attestation-gate (dependency, proposal 041).** Cross-cutting
   primitive used by all receivers.
5. **Layer 5 — Agora ingest path.** Whisper-specific predicates
   wired through attestation-gate; Matrix bridge allowlist for
   `ai.orbiplex.whispers/*`. This lets public whispers start flowing.
6. **Layer 4 — router (Agora branch only).** Router that publishes
   to Agora; returns explicit error for `private-correlation`
   until INAC exists.
7. **Layer 6 — Memarium observe rules + action-trace.** Whisper
   lifecycle facts.
8. **Layer 3 — authoring pipeline.** Intake → redact → approve →
   validate → envelope → route.
9. **INAC (proposal 042 impl).** Separate track; see
   `042-inter-node-artifact-channel-impl.md`. When INAC lands, the
   router's INAC branch flips on.
10. **Layer 7 — threshold detection + durable promotion.**
11. **Layer 8 — source integrations** (UI, Monus, Sensorium).

## Testing posture

- **Golden vectors** for `canonical_signed_bytes` and `record/id`
  in `whisper-core/tests/` — one vector per representative
  whisper shape (rumor vs weak-signal; problem vs inspiration
  polarity; participant vs nym authorship). These vectors are a
  federation-level contract.
- **Round-trip tests** for content-body-only validation:
  `WhisperSignalV1 → JCS → parse → WhisperSignalV1` must be
  byte-identical on re-serialization.
- **Envelope-vs-content regression tests**: assert that none of
  the removed fields (`signal/id`, `created-at`, `sender/*`,
  `rumor/nym`, `auth/*`) appear in the content body after build.
- **Nym-authorship binding tests**: given a nym private key, the
  built envelope must have `author/participant-id` beginning with
  `nym:` and envelope `signature` verifiable against the nym
  public key.
- **Surface-migration tests**: a whisper authored for INAC and
  republished to Agora must pass `record/id` equality.
- **Attestation-gate tests** (shared with proposal 041): reject
  `private-correlation` on a public-deployment relay; accept on a
  closed-federation relay.
