# Solution 013: Whisper — Social Signal Exchange — Implementation Guidelines

Proposal: `doc/project/40-proposals/013-whisper-social-signal-exchange.md`

Solution: `doc/project/60-solutions/whisper.md`

Capability catalog: `doc/project/60-solutions/whisper-caps.edn`

Related impl notes:
- `doc/project/60-solutions/035-agora-topic-addressed-relay-impl.md` (carrier for public whispers)
- `doc/project/60-solutions/042-inter-node-artifact-channel-impl.md` (carrier for private whispers)

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
- give a stable commit order when shaping the whisper stack.

## Architectural posture

Whisper is **not** a transport; it is a **content kind plus an
authoring/reception pipeline** that rides on two distribution surfaces:

1. **Agora** (proposal 035) — for `disclosure/scope` values other than
   `private-correlation`; topic convention proposed:
   `whispers/<topic-class>` (open decision, see §Open Decisions).
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
| Agora kinds table (proposal 035 §3) | `whisper-signal.v1` + topic convention for `whispers/<topic-class>` | 🟡 partially documented in 035; topic convention is an open decision |
| Agora kinds table | `whisper-durable.v1` for threshold-promoted whispers | 🟡 mentioned in 013 §5, kind not yet registered |
| INAC `handles_artifact_kinds` (proposal 042 §4) | `whisper-signal.v1` handler + authorization modes allowed | ❌ not started (INAC itself not started) |
| Memarium observe rules | capture envelope byte-identically + action-trace for whisper lifecycle | ❌ not started |

## Layer 2 — Envelope builder and canonicalization

One authoring primitive that produces a signed `agora-record.v1`
envelope from validated whisper content:

```
build_whisper_envelope(
  content: WhisperSignalV1,            // schema-validated
  author: ParticipantOrNym,
  nym_cert_ref: Option<NymCertRef>,    // required when author is Nym
  topic_key: Option<String>,           // Some("whispers/<topic-class>") for Agora, None for INAC
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
| Matrix federation bridge for whisper topics | 🟡 generic bridge exists; topic-pattern allowlist for `whispers/*` not configured |

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

1. **Topic-key convention for Agora whispers.** Candidates:
   - `whispers/<topic-class>` (flat, simple, lets subject index
     group by class),
   - `whispers/<risk-grade>/<topic-class>` (allows risk-scoped
     topic ACL and retention),
   - `whispers/<federation-id>/<topic-class>` (scopes to
     federation explicitly; risk of over-leaking federation id).

   Decision lives in proposal 013 or 035 kinds table and in this
   document's §Layer 1.

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
   `whispers/*`. This lets public whispers start flowing.
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
