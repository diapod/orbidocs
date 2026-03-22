# Story 002: Federated Peer Learning and Consensus Correction

## Current Baseline Used by This Story

This story no longer assumes a public thematic channel plus an ad-hoc side channel.
It is grounded in the current Orbiplex corpus where:

- a signed `question-envelope` opens or binds a live answer room,
- the live room is the main place where peers compare, challenge, and refine answers,
- exposure mode and room policy profile constrain who may observe, join, summarize,
  or export later traces,
- disagreement handling produces explicit outcomes (`confirmed`, `corrected`,
  `unresolved`) rather than ambient chat residue,
- local learning is policy-gated and provenance-rich instead of being an immediate,
  silent side effect of receiving peer messages,
- later archival and training paths remain separate from immediate answer serving.

This story follows the learning and correction loop that may happen after the question
flow described in `story-001.md` and `story-004.md` has already opened a room.

## Sequence of Steps

1. A local node opens a swarm question through the current baseline flow and receives
   one or more candidate answers in the answer room bound to the `question/id`.
2. The asking node, a participating peer, or a secretary notices that one answer
   materially conflicts with:
   - another candidate answer,
   - local retrieval evidence,
   - federation policy or known procedure,
   - or the node's own specialization-specific knowledge.
3. Instead of opening a separate public correction channel, participants continue the
   review inside the same question-bound room or in a tightly linked review path that
   preserves the original `question/id`, room scope, and participant provenance.
4. Peers post counter-evidence, implementation notes, examples, and objections. A
   secretary or other designated node may emit one or more intermediate summaries so
   the room does not have to treat raw message history as the durable source of truth.
5. If room policy allows transcript observation, a transcription monitor captures the
   relevant discussion with explicit provenance, visibility scope, consent or policy
   basis, and human-origin markers where applicable.
6. The asking node or delegated secretary classifies the emerging outcome for the
   disputed claim as one of:
   - `confirmed`,
   - `corrected`,
   - `unresolved`.
7. If the room converges on a better answer, the accepted correction is emitted as a
   new durable outcome linked to the original question, such as:
   - a signed room summary,
   - a corrected response envelope,
   - or another accepted answer artifact allowed by current room policy.
8. The local node records the outcome together with enough provenance to reconstruct:
   - which question triggered the learning event,
   - which nodes participated,
   - which evidence or summaries influenced the correction,
   - whether any human-linked input affected the accepted result.
9. The node MAY promote `confirmed` or policy-accepted `corrected` material into
   local retrieval assets such as:
   - vector memory,
   - indexed files,
   - a local knowledge-artifact queue.
10. Material classified as `unresolved` is kept isolated from trusted retrieval by
    default. It may still be preserved for later review, adversarial testing, or
    curator inspection, but it is not silently promoted as trusted knowledge.
11. If the discussion is judged culturally or operationally valuable and policy allows
    it, later layers MAY turn the transcript and its accepted summaries into curated
    corpus entries or vault material. That promotion happens through explicit
    curation, not through the mere fact that peers debated in a room.
12. If training is desired, the node or federation routes only explicitly approved
    corpus material into later specialization jobs. Raw discussion and unresolved
    corrections do not directly become training data.

## Open Continuation

- Exact divergence threshold for opening a correction path.
- Default consensus rule and tie handling for `confirmed` vs `corrected`.
- Whether adversarial or unresolved material should feed separate debate-style
  evaluation datasets.
- The exact schema set for divergence signals, consensus outcomes, and local
  knowledge-artifact promotion.
