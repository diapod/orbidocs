# Operator Participation Room Policy Profiles

Based on:
- `proposals/003-question-envelope-and-answer-channel.md`
- `proposals/004-human-origin-flags-and-operator-participation.md`

## Status

Proposed (Draft)

## Date

2026-03-17

## Executive Summary

This proposal defines three interoperable room-policy profiles for operator participation in live answer channels:

- `none`
- `mediated-only`
- `direct-live-allowed`

The point is to make federation and room behavior predictable. A node should know, before it invites or relays human input, whether the room allows no operator involvement, allows only mediated consultation, or allows direct live human presence with explicit provenance.

## Context and Problem Statement

`004-human-origin-flags-and-operator-participation.md` defines the semantics of human-linked input, but not the policy profiles a federation or room may advertise as defaults.

Without explicit profiles:

- nodes cannot reliably know whether direct human participation is permitted,
- room behavior becomes ad hoc and inconsistent across federations,
- transcript and archival policy becomes harder to automate,
- user-facing clients cannot set clear expectations before a human joins.

The system therefore needs a minimal, explicit, interoperable room-policy knob.

## Goals

- Keep room policy simple enough to interoperate across federations.
- Separate prohibition of direct live participation from prohibition of private operator consultation.
- Make the stricter policies default-friendly.
- Keep room-policy semantics orthogonal to identity and moderation details.

## Non-Goals

- This proposal does not define a full moderation workflow.
- This proposal does not define real-world identity disclosure.
- This proposal does not define archival eligibility in full detail; it only defines room participation profiles.

## Decision

Every answer room that supports operator-linked participation should expose a room-policy profile named from a stable finite set.

The normative v1 profiles are:

1. `none`
2. `mediated-only`
3. `direct-live-allowed`

Profiles may be tightened by local rules, but a room MUST NOT advertise one of these profiles and then silently behave as another.

## Profile Definitions

### 1. `none`

Meaning:

- direct live human participation is forbidden,
- node-mediated operator consultation is also forbidden as a room contribution source,
- room expects only node-generated participation.

Implications:

- nodes MUST NOT publish `node-mediated-human` or `human-live` messages into the room,
- transcript segments in the room SHOULD remain `node-generated` only,
- if a node needs human input, it must resolve it outside the room and re-open a different process under a compatible policy.

Use when:

- the room is intended for purely node-native debate,
- federation policy prohibits human-linked debate material in that scope,
- transcript purity matters more than flexibility.

### 2. `mediated-only`

Meaning:

- direct live human participation is forbidden,
- private operator consultation is allowed,
- the node may publish a condensate based on that consultation.

Implications:

- `node-mediated-human` messages are allowed,
- `human-live` messages are forbidden,
- clients SHOULD visibly distinguish mediated human-linked contributions from ordinary node-generated output,
- transcript and summary layers MUST preserve mediated provenance.

Use when:

- the federation wants human fallback without opening the room to live human presence,
- privacy, redaction, or moderation burden favor node-gated relay,
- operator consultation is useful but raw human participation is too costly or risky.

### 3. `direct-live-allowed`

Meaning:

- private operator consultation is allowed,
- direct live human participation is allowed,
- room messages may contain `node-generated`, `node-mediated-human`, and `human-live`.

Implications:

- direct human-origin flags are mandatory,
- room moderation and transcript policy must handle live human-linked input explicitly,
- archival and training policy will usually be stricter than for purely node-generated material.

Use when:

- the debate benefits from live nuance, questioning, or challenge,
- federation policy permits direct human participation in the declared scope,
- operator-presence benefits outweigh moderation and provenance costs.

## Default Recommendations

Recommended defaults:

- `private-to-swarm`: `mediated-only`
- `federation-local`: `mediated-only`
- `cross-federation`: `mediated-only`
- `global`: `none`

Rationale:

- `mediated-only` is the safest general-purpose default because it permits human judgment while preserving node responsibility at the room boundary,
- `global` should default to `none` because direct live human participation at global scope has the highest moderation, consent, and archival complexity,
- `direct-live-allowed` should be an explicit opt-in profile rather than an ambient default.

This is a recommendation, not a hard prohibition. Federations may choose stricter or looser defaults, but they should justify departures and surface them clearly.

## Policy Contract

At minimum, room metadata should expose:

```json
{
  "room-policy/profile": "mediated-only",
  "operator-consultation/allowed": true,
  "operator-direct-live/allowed": false,
  "summary/human-provenance-required": true,
  "transcript/human-origin-preserved": true
}
```

For `direct-live-allowed`, the minimum contract becomes:

```json
{
  "room-policy/profile": "direct-live-allowed",
  "operator-consultation/allowed": true,
  "operator-direct-live/allowed": true,
  "human-live/origin-flag-required": true,
  "summary/human-provenance-required": true,
  "transcript/human-origin-preserved": true
}
```

## Upgrade and Downgrade Rules

Rooms should treat policy-profile change as a meaningful state transition.

Rules:

1. A room MAY tighten policy at any time if moderation, abuse, or scope pressure requires it.
2. A room SHOULD NOT loosen policy silently once debate has started; clients and participants should see the transition.
3. If a room downgrades from `direct-live-allowed` to `mediated-only`, no further `human-live` messages may enter after the effective timestamp.
4. Historic transcript segments retain their original provenance even if room policy changes later.

## Trade-offs

1. Simple profile set vs local nuance:
   - Benefit: interoperability and predictable UX.
   - Cost: some federations may want finer-grained policy.
2. `mediated-only` default vs maximal openness:
   - Benefit: lower moderation and archival complexity.
   - Cost: some live nuance is lost.
3. `global -> none` default vs broad citizen deliberation:
   - Benefit: lower abuse surface.
   - Cost: less direct human presence in wide-scope debate.

## Open Questions

1. Should `direct-live-allowed` require stronger room moderators or secretary presence?
2. Should `global` rooms ever allow `direct-live-allowed` under exception profiles?
3. Should room profiles bind retention defaults as well, or remain strictly participation-only?

## Next Actions

1. Define room metadata schema and validation rules for `room-policy/profile`.
2. Bind transcript schema fields to these profiles.
3. Define client UX rules for displaying and filtering human-linked contributions.
4. Define federation override policy and exception logging for profile changes.
