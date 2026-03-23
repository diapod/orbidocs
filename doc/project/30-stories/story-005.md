# Story 005: Whisper Rumor Intake, Redaction, and Thresholded Association Bootstrap

## Current Baseline Used by This Story

This story assumes the current Orbiplex corpus where:

- `Orbiplex Whisper` is a Node-attached social-signal exchange layer rather than a
  generic chat system,
- rumors are weaker than evidence and must remain marked as such throughout the
  exchange path,
- the Node may expose model-backed helper services to attached modules,
- some outbound privacy or relay capability may exist for relayed or onion-like
  forwarding, but is not required for all Whisper traffic,
- a separate local module such as `Orbiplex Monus` may prepare candidate rumors
  from accumulated user or Sensorium-adjacent signals before they reach Whisper,
- Node-attached roles may live in separate processes and communicate through
  explicit contracts rather than one in-process monolith.

This story does not assume semantic duplicate detection for rumors. The baseline for
v1 is simpler:

- bounded rumor budgets,
- bounded forwarding budgets,
- bounded derived-nym depth,
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
5. The module asks the Node for an internal model-backed assistance session using a
   contract appropriate for:
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
   - risk grade,
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
    - sanitized rumor text,
    - rumor nym,
    - topic or issue class,
    - context facets,
    - confidence,
    - disclosure scope,
    - routing intent,
    - and forwarding limits such as hop TTL.
    If the draft came from `Orbiplex Monus`, the source class should say so
    explicitly instead of collapsing it into a generic local-derived category.
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
17. Whisper itself does not push bytes onto the network. It returns a publication
    result plus routing intent to the Node.
18. The Node validates the final outgoing artifact against the relevant data contract
    and moves it to the outbound communication queue.
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
    a threshold event is recognized.
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

## Example Signal Classes

- Workers in the same large company reporting similar retaliation or organizational
  abuse patterns.
- Users in a Pod ecosystem hitting the same harmful moderation or service-failure
  pattern.
- A repeated emergency-health pattern where an ambulance team refuses transport for
  severe abdominal pain and, hours later, the affected person experiences intestinal
  bleeding. If several nodes observe similarly structured signals, the value lies in
  recognizing that the failure may be systemic rather than accidental.

## Open Continuation

- Exact structure of `whisper-signal`, `whisper-interest`, and
  `association-room-proposal`.
- Exact budget policy for rumor creation and rumor forwarding.
- Exact derived-nym and hop-TTL semantics for relayed Whisper traffic.
- Whether federation-scoped thresholding should require trust-tier diversity or only
  distinct participating nodes.
- Which parts of the bootstrap process belong in Whisper itself and which should move
  into a later dedicated association module.
