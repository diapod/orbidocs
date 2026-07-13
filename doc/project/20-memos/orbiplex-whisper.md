# Orbiplex Whisper

`Orbiplex Whisper` could be a privacy-bounded social signal and provenance
exchange layer attached to the Node.

The point is not generic chat between nodes. The point is to let nodes exchange weak signals in the form of "I heard that..." without prematurely treating them as confirmed facts. This would support early pattern correlation, social-signal detection, and safe association bootstrapping for people who may be experiencing the same problem without yet knowing about one another.

Examples of problem convergence include:

- workers in a large global company seeing similar retaliation or organizational abuse patterns,
- users of a Pod ecosystem experiencing the same harmful moderation or service failure pattern,
- geographically distributed communities reporting the same emerging safety or dignity risk,
- repeated emergency-health failures where an ambulance team refuses transport for severe abdominal pain and the affected person later experiences intestinal bleeding, suggesting a systemic triage or refusal problem rather than an isolated accident.

Examples of idea convergence include:

- independent inventors in different countries discovering the same technical approach without prior contact,
- artists or composers arriving at structurally similar works through separate creative paths,
- practitioners in unrelated fields developing parallel methods to a shared problem class,
- communities in different regions bootstrapping similar local solutions to unmet needs.

The second class — idea convergence — is as important as the first. Two or more
people who arrive at a similar idea independently, and who do not know each other
yet, may benefit from being brought together to create jointly rather than in
parallel. `Whisper` should therefore carry both polarities without conflating
them.

`Whisper` should therefore operate on the level of:

- rumor,
- pattern,
- correlated signal,
- and only later, if warranted, confirmed or procedurally reviewed cases.

It should not start as a raw fact bus.

## Message classes

The Whisper protocol family has two first-class message classes:

- `whisper-signal.v1` carries a weak social signal with `problem` or `idea`
  polarity and may participate in correlation, thresholding, and association
  bootstrap;
- `whisper-trace.v1` carries a bounded assertion that an artifact was created,
  handed to a transport, received, or held. It does not participate in social
  signal correlation or thresholding.

`public-gossip.v1` is not a third Whisper message class. It remains a separate,
explicit act of public publication. Neither a social signal nor a trace becomes
public gossip automatically.

## Signal polarity

A `whisper-signal` may carry one of two fundamental polarities:

- **problem** — the signal describes a distributed harm, failure, or dignity risk. The
  goal is early correlation and, where critical mass is reached, collective response
  or protective action.
- **idea** — the signal describes a convergent idea, creative discovery, or
  emerging approach. The goal is to find co-creators or collaborators who arrived at
  a similar place independently, and to propose an association room oriented toward
  joint creation rather than crisis response.

The two polarities share the same lifecycle (`whisper-signal` → `whisper-interest` →
`whisper-threshold-reached` → `association-room-proposal` → human opt-in) but differ
in tone, urgency, and the nature of the resulting room:

- problem signals use `signal/grade` as protective risk and urgency; idea
  signals use `signal/grade` as convergence strength or co-creation potential and
  never trigger emergency protocols solely by expressing an idea.
- problem signals protect the anonymity of affected people; idea signals may
  still prefer privacy in early phases to avoid premature priority conflicts or
  attribution pressure, but do not carry the same protective urgency.
- the association room proposed after a problem threshold is a support or coordination
  space; the one proposed after an idea threshold is a co-creation or
  collaboration space.

Both polarities must be first-class concepts in the signal schema.

For onion-style relay, forwarding nyms, or transport-level anonymity, keep a separate outbound privacy capability in mind. `Whisper` should express privacy intent and routing posture on the outgoing artifact, while some egress-side module or relay capability may realize optional anonymous forwarding at the transport layer. `Orbiplex Anon` in `doc/project/20-memos/orbiplex-anon.md` is one possible provider of that capability, not a semantic dependency of `Whisper`.

For v1, keep anti-Sybil controls simpler than full semantic duplicate detection. The healthier near-term baseline is:

- bounded rumor budgets,
- bounded forwarding budgets,
- bounded derived-nym depth,
- and local policy gates on publication or forwarding.

Do not require hard semantic-equivalence checks for "the same rumor" yet. That path is likely expensive, ambiguous, and easy to get wrong early.

## Trace statements

`whisper-trace.v1` provides a deliberately weaker and cheaper provenance
statement than a receipt or attestation. The enclosing signature identifies the
author of the assertion; it does not prove that the asserted event happened, that
the author possesses the artifact, that delivery succeeded, or that the content
is true. Independently verifiable facts may be linked through bounded
`evidence/refs` without being copied into the trace.

The allowed v1 trace kinds are:

- `artifact-created` — the author asserts that the artifact was created;
- `artifact-dispatched` — the author asserts that it was handed to an outbound
  transport, not that it reached a recipient;
- `artifact-received` — the author asserts that it was received;
- `artifact-held` — the author asserts that it held the artifact at
  `trace/occurred-at`; the statement does not promise continued possession.

The default disclosure mode is `digest-only`: SHA-256, byte length, and optional
media type or content schema. This is data minimization, not anonymity. A digest
of predictable or low-entropy content can still enable guessing and cross-context
correlation, so classification and disclosure policy must apply even when no
content bytes are present.

`digest-and-content` additionally carries bounded inline bytes. It requires a
sender-host-validated `consent/ref` bound to the exact artifact digest, disclosure
scope, author or represented subject, and validity window. The v1 schema caps
inline content at 32 KiB; local and federation policy may lower that cap but must
not raise it above the wire maximum. Runtime validation must decode the bytes and
verify both declared size and digest before signing, forwarding, or accepting the
trace.

Public or federation-scoped traces use the ordinary signed Agora envelope and the
topic prefix `ai.orbiplex.whisper-traces/<trace-kind>`. Private or direct traces
reuse Artifact Delivery and INAC. No trace-specific transport is needed.

## Candidate lifecycle

The social-signal lifecycle, which does not apply to trace statements, is:

1. `whisper-signal`
2. `whisper-interest`
3. `whisper-threshold-reached`
4. `association-room-proposal`
5. optional human/operator opt-in into a dedicated room or procedure

### 1. `whisper-signal`

A node emits a bounded marker roughly meaning:

- "I heard that something like this is happening"
- "this may matter for a certain type of participant"
- "this is not yet a confirmed claim"

The signal should be normalized and redacted. It should prefer:

- problem class,
- context facets,
- rough organizational or geographical scope,
- time window,
- confidence,
- disclosure scope,
- source class,
- signal grade.

It should avoid raw personally identifying material by default.

It should not blindly anonymize names of companies, organizations, hospitals, ambulance operators, or other institutions when those entities are plausibly part of the harmful pattern itself and do not need protection. The protective default is for users and affected people, not for potential sources, carriers, or transmitters of systemic harm.

### 2. `whisper-interest`

A receiving node may decide that the signal appears relevant to its operator or user. At that point it may:

- notify the local user/operator as a rumor or early signal,
- register interest without disclosing the underlying person or case,
- advertise that it is willing to participate in further correlation.

The notification step is local attention routing, not disclosure. Its generic
contract is tracked in Proposal 057
(`doc/project/40-proposals/057-user-and-operator-notifications.md`).

This is important: relevance signaling should not require immediate disclosure.

Interest advertisement is eligibility, not a delivery entitlement. If a popular
topic has many interested nodes, the origin node should send only to a small,
policy-bounded set chosen by topic match, private transport support, intake
capacity, trust / assurance, diversity, and local egress budget.

A receiving node that stores a private whisper may also become a bounded holder
and redistributor when the original whisper policy, local Memarium policy, and
operator settings allow it. Such a node may advertise holder availability in
Agora, but the announcement should be a privacy-preserving availability hint
(topic class, accepted private transport, capacity, assurance class, optional
opaque token), not a public shadow copy of the private whisper or its raw
keywords.

The holder can also skip Agora and offer the whisper directly to a trusted peer:
"I hold a private whisper for this coarse topic class and disclosure scope." The
peer may request it by default policy, ask the operator, or use a bounded advisory
LLM / automation path to decide. The offer should reveal only enough metadata to
support that decision, not the whisper text or reconstructive keywords.

### 3. `whisper-threshold-reached`

Once sufficiently many distinct and policy-eligible signals or interests align, the system may emit a threshold event.

The threshold should not be a naive count. It likely needs:

- distinct nodes,
- trust or evidence tier,
- diversity constraints,
- anti-Sybil rules,
- and perhaps a minimum spread across time or organizational facets.

### 4. `association-room-proposal`

Only after threshold crossing should the system propose a dedicated room or association path.

That room should not necessarily be created by one central authority. A better v1 default may be deterministic quorum bootstrap:

- a small witness/bootstrap set is chosen from participating nodes,
- those nodes publish the room proposal,
- and the room carries explicit policy, disclosure, and expiry assumptions.

This keeps bootstrap federated while avoiding "whoever got there first" chaos.

### 5. Human opt-in

The room itself may be bootstrapped automatically as a technical coordination space, but human enrollment should remain opt-in.

That means:

- no automatic joining of affected people,
- no automatic disclosure of identities to one another,
- no automatic elevation from rumor to evidence.

The local node may notify, invite, or ask for consent, but should not silently commit the user to a shared association space.

## Trusted peers first vs topic bus

The healthier v1 seems to be:

- trusted-peer or federation-scoped exchange first,
- open topic subscription later, if at all, and only for coarse aggregate notices.

An open subscription bus for early rumors creates obvious risks:

- deanonymization,
- inference attacks,
- Sybil poisoning,
- pattern laundering,
- mass harvesting of sensitive signals.

Because of that, v1 should likely restrict exchange to:

- trusted peers,
- federation-approved counterparties,
- or explicitly authorized correlation roles.

Later layers might allow topic-like subscription to aggregate notices such as:

- "a threshold has been reached for issue class X in scope Y"

but not to raw rumor traffic.

## Immediate local node behavior

Given a relevant `whisper-signal`, a node might reasonably do one or more of the following:

- notify the local user/operator that a relevant rumor exists,
- record bounded local interest,
- contribute an additional redacted signal,
- wait for threshold crossing,
- participate in deterministic bootstrap of a dedicated association room,
- expose a consent gate before disclosing more.

On the sending side, a likely v1 intake path is:

- UI accepts rumor text,
- Node classifies it as Whisper input,
- Whisper runs a local redaction and idiolect-flattening workflow,
- the user accepts or rejects the sanitized result,
- Whisper creates a bounded outgoing signal with a rumor nym and routing/privacy intent,
- Node egress satisfies that intent directly or through any installed outbound privacy or relay capability,
- Node validates the final outgoing artifact and only then emits it onto the network.

A future adjacent module such as `Orbiplex Monus` may also prepare Whisper drafts from locally aggregated wellbeing signals. In a semi-automatic mode the draft waits in UI for approval and optional editing. In a stricter automatic mode the Node may publish it without interactive approval only under explicit policy, budget, and audit constraints.

Not every Monus or Sensorium-originated concern should become a Whisper signal. If
the dominant need is immediate local help, emergency escalation, or welfare
intervention for one person, the healthier default is a local help-mode path rather
than network publication.

## Likely future contracts

If promoted, this probably needs at least:

- `whisper-signal.v1`
- `whisper-trace.v1`
- `whisper-interest.v1`
- `whisper-threshold-reached.v1`
- `association-room-proposal.v1`
- perhaps later `whisper-disclosure-request.v1`
- and `whisper-disclosure-decision.v1`

## Design invariants worth preserving

- rumor is not evidence,
- interest is possible without disclosure,
- thresholding is resistant to naive Sybil amplification,
- room bootstrap is explicit and auditable,
- no automatic human enrollment,
- no default raw fact broadcast,
- disclosure is policy-bounded and consent-aware.
- trace statements remain assertions rather than receipts or attestations,
- digest-only disclosure is not treated as anonymous or harmless,
- inline trace content requires exact, sender-host-validated consent and bounded
  integrity verification.

Promote to: proposal when threshold policy, bootstrap mechanics, disclosure classes, and the first data contracts are specified.
