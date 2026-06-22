# Story 005: Whisper Rumor Intake, Redaction, and Thresholded Association Bootstrap

## Current Baseline Used by This Story

This story assumes the current Orbiplex corpus where:

- `Orbiplex Whisper` is a Node-attached social-signal exchange layer rather than a
  generic chat system,
- rumors are weaker than evidence and must remain marked as such throughout the
  exchange path,
- the Node may expose Inquirium/model-backed helper services to attached modules,
- some outbound privacy or relay capability may exist for relayed or onion-like
  forwarding, but is not required for all Whisper traffic,
- a separate local module such as `Orbiplex Monus` may prepare candidate rumors
  from accumulated user or Sensorium-adjacent signals before they reach Whisper,
- acute Sensorium-detected emergencies should still prefer local help-mode or
  emergency escalation rather than default Whisper publication,
- Node-attached roles may live in separate processes and communicate through
  explicit contracts rather than one in-process monolith.
- `Orbiplex Agora` is the durable public/federated record substrate for accepted
  public records, not the semantic owner of Whisper.
- `public-gossip.v1` is the low-friction public weak-signal payload, while
  `whisper-signal.v1` is the Whisper-specific content-body schema used when a
  whisper disclosure posture permits public/federated publication.
- private/direct or `private-correlation` whispers do not belong on public Agora
  topics; they should use direct node exchange, INAC, invitation-tokened transfer,
  or another bounded private channel, with Memarium as the local memory surface.
- threshold-crossed public or durable Whisper state may be represented as accepted
  Agora records and replayed into projections, but private raw rumor text remains
  local unless a later consent transition explicitly changes the disclosure scope.
- threshold/proposal records are public meta-signals and coordination records, not
  `public-gossip.v1`; public gossip requires a separate publication decision after
  opt-in association or another explicit human/collective policy transition.
- `association-room-proposal.v1` is a possible precursor to public gossip, not a
  prerequisite; `public-gossip.v1` can also be published independently on a
  public weak-signal path.
- Agora M4 uses `whisper-signal.v1` directly for the public/federated smoke rather
  than substituting generic public gossip; `public-gossip.v1` remains a simpler
  weak-signal payload for non-Whisper public streams.

This story does not assume semantic duplicate detection for rumors. The baseline for
v1 is simpler:

- bounded rumor budgets,
- bounded forwarding budgets,
- bounded derived-nym depth,
- explicit `topic/class` plus optional deterministic `signal/similarity-key` for
  fixture-grade thresholding,
- and no hard semantic-equivalence gate for "the same rumor".

## Sequence of Steps

1. A user or operator writes a sensitive social signal into the Node UI or Pod UI,
   or a local module such as `Orbiplex Monus` prepares a candidate rumor draft from
   accumulated wellbeing or Sensorium-adjacent signals. The input is explicitly
   marked as a rumor-style submission rather than as a confirmed report,
   attestation, or governance complaint.
2. The UI sends the content to the serving Node with an input classification such as:
   - `input-kind = rumor`
   - optional privacy preference
   - optional urgency
   - optional local-only draft intent.
3. The Node receives the input on its normal ingress path. During ingress handling,
   the input is recognized as Whisper-eligible traffic and routed into the Whisper
   workflow if the Whisper module is installed.
4. The Whisper workflow opens a bounded local task for rumor preparation rather than
   immediately publishing the raw text.
5. The module asks the Node for an internal Inquirium/model-backed assistance
   session using a contract appropriate for:
   - anonymization,
   - paraphrase,
   - idiolect flattening,
   - and privacy/risk review.
6. The user is shown an interactive draft-revision flow. The goal is to help produce
   a version that:
   - preserves the core social signal,
   - removes avoidable personally identifying material,
   - preserves names of companies, organizations, hospitals, ambulance operators,
     or similar institutions when they are plausibly part of the harmful pattern
     and do not require protective anonymization,
   - weakens recognizable idiolect,
   - and makes the rumor safer to exchange.
7. The original raw text remains local to the Node or Pod context. It is not placed
   on the network-facing Whisper path by default.
8. The user reviews the sanitized version and either:
   - accepts it,
   - asks for another redaction/paraphrase pass,
   - or cancels publication.
   In a stricter Monus-assisted automatic mode, local policy may allow publication
   without interactive approval, but only under explicit opt-in, budget, and audit
   constraints.
9. If the user accepts, Whisper creates a local reviewed rumor artifact containing at
   least:
   - the accepted sanitized text,
   - source-class and disclosure metadata,
   - signal grade,
   - local audit reference,
   - and local policy context.
10. Whisper checks local budget constraints before publication. At minimum, it checks:
    - rumor budget for the author scope in a time window,
    - forwarding budget if the rumor will later be relayed,
    - and a maximum derived-nym depth for future forwarding.
11. Whisper does not try to do hard semantic duplicate suppression in v1. If the user
    submits a very similar rumor later, the system may still publish it as long as
    local budget and policy allow it.
12. Whisper generates a bounded rumor nym for the outgoing signal. That nym is not
    the user's stable identity and is not reused as a general-purpose long-lived
    author identifier.
13. Whisper packages a network-facing `whisper-signal` artifact that may include:
    - infrastructure `sender/node-id`,
    - sanitized rumor text,
    - rumor nym,
    - envelope-level `author/nym-proof` carrying inline-first nym certificate
      material,
    - `nym` signature over the enclosing artifact/envelope,
    - topic or issue class,
    - context facets,
    - confidence,
    - disclosure scope,
    - routing intent,
    - and forwarding limits such as hop TTL.
    The backing `participant-id` remains local to the issuing or hosting side and
    is not required on the wire for peer-side validation of the pseudonymous
    artifact.
    If the draft came from `Orbiplex Monus`, the source class should say so
    explicitly instead of collapsing it into a generic local-derived category.
    If Sensorium materially informed the Monus draft, the artifact should preserve
    that distinction as well.
14. If the user or policy requested stronger sender privacy, Whisper sets routing and
    privacy intent on the outgoing artifact, such as:
    - `direct`
    - `relayed`
    - `onion-relayed`
15. If a suitable outbound privacy or relay capability is installed, Node egress may
    use it to realize that routing profile, including:
    - relay-capability discovery,
    - derived forwarding nyms,
    - bounded onion-like wrapping,
    - and relay selection under local policy.
16. If no suitable capability is available, the Node follows the requested failure mode:
    - `soft-fail`: continue with allowed non-anonymous transport,
    - `hard-fail`: refuse publication and tell the user the requested privacy posture
      could not be satisfied.
17. Whisper itself does not own network transport. It returns a publication result
    plus routing intent to the Node. If the selected disclosure scope is public or
    federation-scoped, the Node may wrap the final `whisper-signal.v1` content in
    an `agora-record.v1` envelope and submit it to an Agora relay. If the selected
    disclosure scope is private-correlation or direct-only, the Node must keep it
    off public Agora topics and use a private exchange path instead.
18. The Node validates the final outgoing artifact against the relevant data
    contract. For Agora publication, validation includes the `agora-record.v1`
    envelope, the `whisper-signal.v1` content schema, topic policy, authority or
    participation policy, and the disclosure-scope guard.
    The authored pseudonymous role remains explicit through the nym certificate and
    nym signature instead of collapsing publication into either a purely node-scoped
    signal or a participant-disclosing artifact.
19. One or more receiving nodes obtain the `whisper-signal`. Each receiving node
    evaluates it locally against its own operator or Pod context.
20. A receiving node may then:
    - notify its local user/operator as a rumor or weak signal,
    - register local interest without full disclosure,
    - or ignore the signal.
21. Interest registration does not yet imply that identities are shared. It means only
    that the node considers the rumor plausibly relevant and is willing to take part
    in further correlation.
22. When sufficiently many distinct and policy-eligible interests or signals align,
    a threshold event is recognized. In the M4 laptop smoke, the minimal rule is
    two distinct nodes publishing compatible public/federated `whisper-signal.v1`
    records in the same `topic/class`, with the same deterministic
    `signal/similarity-key`, within the configured time window through a shared
    Agora relay.
23. Threshold crossing does not automatically expose the involved people to one
    another. Instead it creates a basis for association bootstrap.
24. A small deterministic bootstrap set is selected from participating nodes. Those
    nodes create an `association-room-proposal` with:
    - initial room policy,
    - disclosure assumptions,
    - bootstrap expiry,
    - and moderation or witness expectations.
25. Local nodes then ask their users or operators whether they want to enter the next
    stage. Human enrollment remains opt-in; no one is silently added to the room.
26. If enough humans opt in under the room policy, the dedicated room appears and the
    previously isolated users can discover that their problem may be shared rather
    than purely individual.

## M4 Three-Node Smoke Target

Agora M4 uses this story as the production-shaped end-to-end smoke for public
Whisper correlation:

1. Node A has a local user who submits a sensitive weak signal.
2. Node B has a different local user who submits a similar weak signal.
3. Node C runs the Agora relay/server used as the public/federated substrate.
4. A and B perform local redaction through the supervised `whisper-intake`
   middleware path, store raw and intermediate material only in local/private
   Memarium state, and publish only sanitized public or federation-scoped
   `whisper-signal.v1` records to C, authored by bounded `nym:did:key:...`
   identities with inline-first nym proof.
5. C rejects a `private-correlation` whisper if it is submitted to the public relay
   path.
6. C stores accepted records idempotently and exposes them through Agora replay.
7. The public Whisper projection sees both compatible signals and emits one
   threshold state using the M4 rule: two distinct eligible nodes, same
   `topic/class`, same `signal/similarity-key`, bounded time window.
8. Final M4 closure emits deterministic projection-authority-signed
   `whisper-threshold-reached.v1` and `association-room-proposal.v1` records as
   issuer-scoped derived claims, with deterministic ids, source-kind exclusion,
   and derivation refs to prevent loops.
9. The threshold/proposal path does not enroll any human automatically and does
   not publish a public gossip narrative.
10. Operator surfaces expose relay state, projection state, rejection diagnostics,
   scheduler replay status, threshold state, and the association proposal without
   requiring daemon-log inspection.

This smoke is intentionally narrower than the complete future Whisper product. It
proves the public/federated correlation path and the consent boundary; it does not
require full onion routing, private holder redistribution, or final case-management
UX.

## Post-M4 Productization Contract

The post-M4 implementation tracker for this story lives in
`doc/project/60-solutions/011-whisper/011-whisper-impl.md`. Its closed slice adds
a secretless Inquirium simulator acceptance path and the production-shaped
Whisper contracts needed by later runtime work.

The simulator is not a daemon shortcut and not a story-specific model name. It is
an opt-in middleware-hosted Inquirium adapter, supervised as a local HTTP adapter
instance, selected through `runtime/ref`, and bound to the provider-facing
simulated model through host-owned `model.binding/ref`. This proves that Story
005 can consume model assistance through the same Inquirium/model-runtime route
that real local or remote providers will use.

The same productization slice keeps later Whisper work stratified. Core policy
data now has explicit source classes, routing failure modes, forwarding budgets,
outbound privacy resolution, correlation policy explanations, association-room
proposal transitions, and public-gossip promotion decisions. The remaining
`partial` and `not-started` productization tasks are tracked in the Whisper
implementation note so they stay with the solution rather than in a workspace
root draft file. Concrete UI and relay transports may implement those contracts
later without changing the M4 smoke semantics.

## Example Signal Classes

- Workers in the same large company reporting similar retaliation or organizational
  abuse patterns.
- Users in a Pod ecosystem hitting the same harmful moderation or service-failure
  pattern.
- A Monus-prepared weak signal built from accelerated speech, stress markers, and
  repeated mention of the same institution and event class in local Sensorium data.
- A repeated emergency-health pattern where an ambulance team refuses transport for
  severe abdominal pain and, hours later, the affected person experiences intestinal
  bleeding. If several nodes observe similarly structured signals, the value lies in
  recognizing that the failure may be systemic rather than accidental.

The last two examples should still be separated carefully:

- the institution-linked stress pattern is plausibly correlation-worthy and may fit
  Whisper,
- but a likely cardiac arrest with user inactivity should default to a local
  help-mode path rather than rumor publication.

## Open Continuation

- Exact production budget policy for rumor creation and rumor forwarding.
- Exact derived-nym and hop-TTL semantics for relayed or onion-like Whisper traffic.
- Whether production federation-scoped thresholding should require trust-tier
  diversity in addition to distinct participating nodes. M4 uses distinct nodes as
  the minimum deterministic smoke rule.
- Whether production similarity should use semantic matching, human/operator
  curation, or richer local policy. M4 intentionally uses an explicit
  `signal/similarity-key` only for deterministic smoke and contract tests.
- Which parts of the later human-room lifecycle belong in Whisper itself and which
  should move into a dedicated association module. M4 stops at the
  `association-room-proposal` and explicit opt-in boundary.
- Concrete production UI and relay transport implementations for the
  productization contracts: the post-M4 slice defines the data contracts and
  acceptance seams, while final operator/user workflows and real relay execution
  remain separate runtime/product layers.
