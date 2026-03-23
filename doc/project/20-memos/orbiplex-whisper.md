# Orbiplex Whisper

`Orbiplex Whisper` could be a privacy-bounded social signal exchange layer attached to the Node.

The point is not generic chat between nodes. The point is to let nodes exchange weak signals in the form of "I heard that..." without prematurely treating them as confirmed facts. This would support early pattern correlation, social-signal detection, and safe association bootstrapping for people who may be experiencing the same problem without yet knowing about one another.

Examples include:

- workers in a large global company seeing similar retaliation or organizational abuse patterns,
- users of a Pod ecosystem experiencing the same harmful moderation or service failure pattern,
- geographically distributed communities reporting the same emerging safety or dignity risk,
- repeated emergency-health failures where an ambulance team refuses transport for severe abdominal pain and the affected person later experiences intestinal bleeding, suggesting a systemic triage or refusal problem rather than an isolated accident.

`Whisper` should therefore operate on the level of:

- rumor,
- pattern,
- correlated signal,
- and only later, if warranted, confirmed or procedurally reviewed cases.

It should not start as a raw fact bus.

For onion-style relay, forwarding nyms, or transport-level anonymity, keep a separate outbound privacy capability in mind. `Whisper` should express privacy intent and routing posture on the outgoing artifact, while some egress-side module or relay capability may realize optional anonymous forwarding at the transport layer. `Orbiplex Anon` in `doc/project/20-memos/orbiplex-anon.md` is one possible provider of that capability, not a semantic dependency of `Whisper`.

For v1, keep anti-Sybil controls simpler than full semantic duplicate detection. The healthier near-term baseline is:

- bounded rumor budgets,
- bounded forwarding budgets,
- bounded derived-nym depth,
- and local policy gates on publication or forwarding.

Do not require hard semantic-equivalence checks for "the same rumor" yet. That path is likely expensive, ambiguous, and easy to get wrong early.

## Candidate lifecycle

One plausible lifecycle is:

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
- risk grade.

It should avoid raw personally identifying material by default.

It should not blindly anonymize names of companies, organizations, hospitals, ambulance operators, or other institutions when those entities are plausibly part of the harmful pattern itself and do not need protection. The protective default is for users and affected people, not for potential sources, carriers, or transmitters of systemic harm.

### 2. `whisper-interest`

A receiving node may decide that the signal appears relevant to its operator or user. At that point it may:

- notify the local user/operator as a rumor or early signal,
- register interest without disclosing the underlying person or case,
- advertise that it is willing to participate in further correlation.

This is important: relevance signaling should not require immediate disclosure.

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

## Likely future contracts

If promoted, this probably needs at least:

- `whisper-signal.v1`
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

Promote to: proposal when threshold policy, bootstrap mechanics, disclosure classes, and the first data contracts are specified.
