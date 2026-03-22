# Story 001: Swarm Node Onboarding and Federated Answer Procurement

## Current Baseline Used by This Story

This story is grounded in the current documentation set, not only in the older MVP
notes. In particular, it assumes:

- a proxy-friendly communication baseline over `WSS/443`, with direct or relay paths
  as transport optimizations rather than hard dependencies,
- a split between:
  - durable signed question publication on an event layer,
  - live answer discussion on a room/conversation layer,
- explicit user-facing exposure mode:
  - `private-to-swarm`
  - `federation-local`
  - `public-call-for-help`
- explicit room policy profile:
  - `none`
  - `mediated-only`
  - `direct-live-allowed`
- transcript and provenance semantics that can preserve human-linked participation,
  room scope, and later archival/training eligibility,
- an MVP settlement path that still uses explicit contracts and receipts, while the
  concrete payment rail remains outside the protocol core.

This story follows the `full-node` / `hybrid` path. A `pod-client` path exists in the
current design corpus, but is not the main line here.

## Sequence of Steps

1. The user installs an Orbiplex client and chooses a participation profile that is
   capable of running as a `full-node` or `hybrid` node.
2. On first launch, the application explains the boundary between:
   - local responsibilities on the user's machine,
   - delegated or network-facing responsibilities of the node runtime.
3. The user provides a node name, specialization set, preferred languages, and
   default request constraints such as maximum price, maximum wait time, and whether
   follow-up discussion is normally allowed.
4. The user chooses default privacy and participation policy for outbound requests:
   - exposure mode (`private-to-swarm`, `federation-local`, or `public-call-for-help`),
   - room policy profile (`none`, `mediated-only`, or `direct-live-allowed` where allowed).
5. The application creates or restores a dedicated operational settlement profile for
   participation flows. It warns that this profile is for node operations, not for
   the user's personal finances. The user may optionally provide a payout destination
   or billing reference for later surplus settlement.
6. The user is shown a list of compatible models and capability profiles. They may
   choose local models, delegated execution, or a mixed profile if the node runs in
   `hybrid` mode.
7. The user is prompted to add local directories or knowledge sources for indexing.
   If multiple specializations are selected, the user may map sources to specific
   domains.
8. The application begins model download or preparation, then starts local ingestion
   of configured content into retrieval/indexing components used by the local
   orchestrator.
9. The node establishes outbound connectivity to the swarm using the current baseline
   transport profile:
   - proxy-friendly `WSS/443`,
   - direct or relay path as available,
   - event-layer and room-layer capability appropriate to the federation profile.
10. After model readiness and initial ingestion, the user asks a domain-specific
    question through the local assistant, for example: `How should we handle STM
    failures in Clojure under load?`
11. The local node first performs a sufficiency check against:
    - local retrieval context,
    - available models,
    - user constraints,
    - current policy profile.
12. If local sufficiency passes, the node answers locally and returns the result with
    traceable local provenance.
13. If local sufficiency fails, the node opens a swarm request. The user may confirm
    or adjust:
    - exposure mode,
    - urgency,
    - whether follow-up debate is allowed,
    - model filters (`require` / `exclude`),
    - minimum responder reputation,
    - reward or procurement intent.
14. The node publishes a signed question envelope onto the event layer. The envelope
    carries at least:
    - stable `question/id`,
    - sender identity and federation scope,
    - TTL,
    - question text and tags,
    - delivery scope and response-channel id,
    - responder filters and reward intent.
15. Publication of the question envelope opens or binds a live answer room identified
    by the question id. The room metadata declares at least:
    - delivery scope,
    - room policy profile,
    - whether operator consultation and direct live human participation are allowed,
    - whether human provenance must be preserved in summaries and transcripts.
16. Eligible remote nodes discover the envelope and respond on the allowed path:
    - by joining the live answer room for collaborative discussion,
    - and, when procurement mode is enabled, by emitting structured offers containing
      price, deadline, length bounds, specialization fit, node identity, and
      reputation evidence.
17. The local node scores incoming offers deterministically according to current
    procurement policy. It may either:
    - continue in an open collaborative room if that best matches the request,
    - or select one responder and narrow execution to a smaller room / execution path
      linked to the original question id.
18. If the selected responder needs human help and room policy allows it, that node
    may:
    - consult its operator privately and publish `node-mediated-human` input,
    - or let the operator join as `human-live`.
    In either case, provenance semantics are preserved instead of flattening human
    input into ordinary node output.
19. Before paid execution begins, the asking node performs funding and settlement
    prechecks. If procurement terms require settlement, it creates an explicit
    procurement contract with acceptance criteria such as:
    - deadline,
    - answer shape or format,
    - length bounds,
    - confirmation mode (`arbiter-confirmed`, `self-confirmed`, or explicit no-confirmation for zero-price cases).
20. During discussion and answer production, transcript monitors or secretaries may
    observe the room only if room policy and exposure mode allow it. If they do,
    captured material preserves:
    - message provenance,
    - origin class,
    - room scope,
    - consent or policy basis,
    - redaction state where applicable.
21. When an answer or accepted summary arrives, the local node validates it against
    contract or request criteria. If required confirmation is present, settlement
    completes and a signed receipt is recorded.
22. The node updates local and publishable evidence for reputation, procurement
    history, and later audit. At minimum, the result remains linked to question,
    contract, room, and selected responder.
23. The application returns the result to the user with provenance metadata that may
    include:
    - source node,
    - room or question id,
    - contract id when payment applied,
    - confidence or uncertainty signal,
    - indication of whether human-linked participation influenced the answer.
24. If the interaction produced high-value discussion and policy allows it, later
    layers may promote the room output into transcript, curation, archival, or
    specialization flows - but only through explicit post-processing and policy gates,
    not as an ambient side effect of ordinary chat history.

## Open Continuation

- Retry paths when no acceptable responder or summary emerges.
- Dispute and appeal flow when settlement or answer acceptance is contested.
- Long-term reputation evidence model and anti-Sybil aggregation.
- Pod-backed client variant of the same story.
