# Story 004: Pod-Client Onboarding and Delegated Federated Answer Procurement

## Current Baseline Used by This Story

This story is the `pod-client` counterpart of `story-001.md`. It assumes the current
Orbiplex corpus where:

- a thin client is a first-class participation mode served by a node-side `pod`
  module,
- hosted-user identity is distinct from serving-node identity and from concrete
  client-instance identity,
- swarm requests still use the same event-layer plus room-layer model as fuller node
  profiles,
- request exposure mode and room policy profile remain explicit user-facing policy
  inputs,
- settlement and provenance remain explicit even when execution is delegated to the
  serving node.

The main difference from `story-001.md` is simple: the user's device stays thin and
keeps only the responsibilities that belong close to the user, while the serving node
runs the heavy routing, retrieval, and procurement mechanics.

## Sequence of Steps

1. The user installs a thin Orbiplex client on a phone or workstation that is not
   expected to run a full node or local language model.
2. On first launch, the client explains the trust boundary between:
   - local device responsibilities,
   - hosted-user continuity on the serving node,
   - infrastructure responsibility of the serving node operator.
3. The user signs in to an existing `pod` host or creates a new hosted-user tenancy.
   The system creates or restores at least:
   - `pod-user-id`,
   - `client-instance-id`,
   - local device-scoped unlock material.
4. The client shows what stays local and what is delegated:
   - local secrets, unlock path, notifications, optional encrypted cache,
   - delegated model execution, retrieval, session continuity, and swarm routing.
5. The user chooses baseline participation defaults:
   - preferred languages,
   - exposure mode,
   - room policy profile,
   - price and wait ceilings,
   - whether follow-up debate is normally allowed.
6. If federation policy or host policy allows it, the user links portable continuity
   material or migration data so later exit from the `pod` host does not imply
   identity rebirth.
7. The serving node advertises available capability profiles to the thin client. The
   user chooses one of:
   - fully delegated execution,
   - mixed `hybrid` participation with selected local tools,
   - host-defined profile defaults.
8. The user may optionally upload or connect bounded personal knowledge sources. The
   host makes clear whether these sources remain private, federation-local, or become
   usable in wider swarm participation.
9. The thin client asks a domain-specific question. The client may attach urgency,
   responder filters, and procurement intent, but it does not need to manage swarm
   transport directly.
10. The serving node performs the first sufficiency check on behalf of the hosted user
    against:
    - host-side retrieval context available to that `pod-user-id`,
    - delegated or hybrid execution capabilities,
    - user policy defaults,
    - current exposure and room-policy constraints.
11. If sufficiency passes locally on the host, the client receives an answer with
    provenance that distinguishes:
    - hosted-user scope,
    - serving node as gateway,
    - whether any human-linked participation influenced the answer.
12. If sufficiency fails, the client is shown the intended swarm escalation before
    submission. The user may confirm or revise:
    - exposure mode,
    - federation scope,
    - room policy profile,
    - procurement intent,
    - reputation floor and model filters.
13. The serving node publishes a signed question envelope on behalf of the hosted user
    while preserving the identity split between:
    - serving infrastructure actor,
    - hosted participant,
    - optional public-facing `nym`.
14. Publication opens or binds an answer room linked to the same question id. The
    room metadata carries room policy, exposure-derived visibility, and whether human
    provenance must be preserved.
15. Eligible remote nodes discover the question and respond either by:
    - joining the collaborative room,
    - or submitting structured procurement offers when the request is price-bound.
16. The serving node evaluates candidate offers under hosted-user policy and either:
    - keeps the request in collaborative room mode,
    - or selects a responder and narrows the execution path while keeping audit links
      to the original question and room.
17. If paid procurement is used, the serving node creates a settlement contract tied
    to the hosted-user request. The client sees the resulting contract summary,
    including price, deadline, confirmation mode, and responder identity.
18. If the selected remote node uses operator consultation or direct human
    participation, the resulting room or answer provenance preserves that fact instead
    of flattening it into ordinary node output.
19. During answer production, transcript monitors or curators may observe only if the
    chosen exposure mode, room policy profile, and publication basis allow it.
20. When the answer arrives, the serving node validates it against request or contract
    criteria, records a receipt when settlement applies, and returns a response
    envelope to the client.
21. The client presents the result with explicit provenance that distinguishes:
    - hosted-user request context,
    - serving node gateway role,
    - remote responder,
    - contract and receipt ids where payment applied,
    - confidence or uncertainty signals,
    - human-linked participation markers where applicable.
22. At any later time, the user may export history, portable identity material, and
    procurement records, then migrate to another `pod` host or upgrade toward
    `hybrid` or `full-node` participation.

## Open Continuation

- Recovery and migration flow when the serving `pod` host becomes unavailable.
- Host-switch procedure for active contracts or in-flight answer rooms.
- Fine-grained data-ownership rules for uploaded knowledge sources in `pod-client`
  mode.
- Session and per-device compromise handling for `client-instance-id` vs
  `pod-user-id`.
