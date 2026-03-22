# Story 003: Remote Memory Preservation, Archivists, and Vault Publication

## Current Baseline Used by This Story

This story no longer assumes `memory nodes` discovered through public thematic
channels.

It is grounded in the current Orbiplex corpus where:

- durable preservation is an explicit subsystem with roles such as
  `transcription-monitor`, `curator`, and `archivist`,
- publication scope is explicit (`private-retained`, `federation-vault`,
  `public-vault`),
- transcript and knowledge artifacts preserve provenance, integrity markers, and
  redaction state,
- archival promotion is policy-gated and may be delayed, curator-gated, or retained
  privately,
- storage or publication work MAY involve explicit procurement terms, but settlement
  remains outside the protocol core and is not tied to a crypto-specific rail.

This story focuses on how a node turns a valuable artifact into durable memory beyond
its own runtime lifetime.

## Sequence of Steps

1. A node finishes a valuable interaction or produces a knowledge artifact that should
   outlive the node's current runtime instance. The artifact may be, for example:
   - an accepted room summary,
   - a transcript bundle,
   - a redacted corpus candidate,
   - or another provenance-rich knowledge object.
2. Before publishing or transferring anything, the node classifies the intended
   preservation path:
   - `private-retained`,
   - `federation-vault`,
   - `public-vault`.
3. If the artifact comes from a live room, the node or a delegated secretary verifies
   whether the room policy, exposure mode, and consent or policy basis actually allow
   archival export. If the basis is ambiguous, the flow fails closed and the artifact
   remains locally retained or quarantined.
4. The preserving node prepares a durable package that includes at least:
   - artifact identifier,
   - provenance references back to question, room, summaries, or source nodes,
   - visibility and publication scope,
   - redaction status,
   - integrity proof or content hash,
   - retention hints where relevant.
5. If curator review is required, the artifact first moves through a curation gate.
   The curator may:
   - accept it,
   - accept a redacted form,
   - quarantine it,
   - reject it for publication.
6. If the artifact is eligible for archival storage, the node selects an archivist or
   vault target according to current federation policy. This may happen:
   - by direct submission to a known archivist,
   - or through an explicit storage/procurement flow when retention or cost terms must
     be negotiated.
7. When storage terms matter, the preserving node negotiates explicit retention and
   access constraints such as:
   - maximum duration,
   - idle TTL,
   - replication level,
   - publication timing profile,
   - settlement rail outside the protocol core.
8. The preserving node transfers the prepared artifact to the selected archivist over
   an execution path appropriate to its visibility and sensitivity. Private or
   federation-bounded material does not travel through a public discovery path once
   the archivist has been selected.
9. The archivist validates the package, checks integrity metadata, and confirms
   accepted storage with stable retrieval identifiers and scope metadata.
10. The preserving node records the archival result together with enough provenance to
    reconstruct:
    - which artifact was stored,
    - under which publication scope,
    - on which archivist or vault,
    - under which retention and access policy,
    - and, when applicable, under which contract or receipt.
11. If the artifact was accepted for `federation-vault` or `public-vault`, the
    archivist may advertise retrieval capability under the declared scope. Promotion
    from one scope to another remains an explicit later state transition, not an
    ambient consequence of storage.
12. When the original node or another authorized party later needs the material, it
    retrieves the artifact through the scope-appropriate path:
    - direct retrieval from the archivist for retained or bounded artifacts,
    - federation-local discovery for bounded vault material,
    - or broader public retrieval for artifacts intentionally promoted to the commons.
13. If the stored material is later used for curation, synthesis, or training, those
    later layers consume it through explicit provenance-carrying contracts. Durable
    storage alone does not imply training eligibility.

## Open Continuation

- Canonical schema set for archivist advertisement, storage offer, confirmation, and
  retrieval response.
- Default replication and failover policy for high-value artifacts.
- Exact relationship between generic knowledge artifacts and transcript-specific vault
  bundles.
- Whether public-vault promotion should require curator quorum or federation-level
  approval in some classes of material.
