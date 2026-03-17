# Human-Origin Flags and Operator Participation in Answer Channels

Based on:
- `memos/operator-participation-in-answer-channel.md`
- `memos/human-expertise-escalation.md`
- `proposals/003-question-envelope-and-answer-channel.md`

## Status

Proposed (Draft)

## Date

2026-03-17

## Executive Summary

This proposal defines how a participating node may bring its human operator into an active answer-channel debate without blurring provenance.

The system should support two distinct modes:

1. `mediated-operator-dialogue` - the node talks privately with its operator and publishes a node-authored condensate back into the room,
2. `direct-human-live` - the operator speaks into the room through the node gateway and the protocol marks those messages as human-originated.

The key decision is simple: human presence must be visible in protocol semantics, transcript semantics, and later curation/training eligibility. The swarm may use human judgment, but it must not silently launder human speech into ordinary node output.

## Context and Problem Statement

`003-question-envelope-and-answer-channel.md` defines how a question opens a live answer room. `human-expertise-escalation.md` already covers bounded fallback to human specialists behind a node.

What remains underspecified is a narrower but important case:

- a node is already inside a live debate,
- it detects that operator judgment would help,
- it either consults the operator privately or lets them join the live room,
- that human involvement later enters transcripts, summaries, archival bundles, and possibly training corpora.

Without explicit protocol semantics, several pathologies follow:

- human statements become indistinguishable from node-generated text,
- transcript monitors lose provenance fidelity,
- curators cannot tell whether a corpus contains live human judgment,
- training nodes may accidentally treat human material as plain machine debate,
- participants cannot calibrate trust, challenge, or consent correctly.

## Goals

- Preserve a usable human-in-the-loop gradient inside live swarm debates.
- Make human participation explicit without forcing permanent identity exposure.
- Keep mediated and direct human input distinct.
- Ensure transcript, curation, and training layers can apply different policy to each class of contribution.
- Keep the room model compatible with `003` rather than creating a second debate architecture.

## Non-Goals

- This proposal does not define a full identity-assurance regime for operators.
- This proposal does not force every federation to permit direct human live participation.
- This proposal does not define compensation economics for operator involvement.

## Decision

Orbiplex should treat operator participation as a first-class extension of the answer-channel protocol.

The baseline model is:

1. A participating node MAY consult its operator privately while a debate is active.
2. A participating node MAY expose a direct live path for the operator into the room if room policy allows it.
3. Every room contribution MUST carry an `origin/class` value that distinguishes at least:
   - `node-generated`
   - `node-mediated-human`
   - `human-live`
4. Direct human live participation MUST be explicitly flagged in room-visible semantics, even when the operator remains pseudonymous.
5. Transcript segments, summaries, archival bundles, and training corpora MUST preserve or derive these distinctions rather than flattening them away.

## Proposed Model

### 1. Participation modes

#### `mediated-operator-dialogue`

The node opens a side dialogue with its operator and publishes a condensate into the answer room.

Properties:

- room receives node-authored content,
- node may redact, translate, normalize, or summarize,
- operator does not appear as a live room participant,
- provenance remains weaker than raw direct participation,
- the message still declares that it is based on operator consultation.

#### `direct-human-live`

The node lets its operator participate in the room through the node's transport path.

Properties:

- room receives the human's live message stream,
- messages are protocol-flagged as human-originated,
- operator identity may remain pseudonymous or scoped,
- transcript layer can preserve direct human contribution without pretending it was model output.

### 2. Room-visible semantics

The conversation layer should expose the following room-level distinctions:

- `speaker/ref` - who emitted the room event at the protocol boundary,
- `origin/class` - whether the semantic source is node-generated, node-mediated-human, or human-live,
- `gateway-node/ref` - which node introduced the contribution into the room,
- `operator-presence/mode` - `none|mediated|direct-live`,
- `human-origin?` - convenience boolean for clients and moderation views.

The protocol MAY add richer fields later, but these distinctions are the minimum needed to keep provenance intelligible.

### 3. Permissions and policy

Room policy should decide whether direct human participation is:

- forbidden,
- allowed for asking node only,
- allowed for trusted participant nodes,
- allowed only above a reputation or trust threshold,
- allowed only in federation-local scope,
- allowed with moderator or secretary approval.

Mediated operator dialogue should generally be easier to permit than direct live human participation because it keeps the node responsible for what re-enters the room.

### 4. Secretary and fallback behavior

If a node that introduced human-linked input disconnects, a `secretary` may preserve continuity for transcript and summary purposes, but MUST NOT rewrite provenance.

The secretary may:

- record that human-linked messages were observed,
- preserve flags in summaries,
- note uncertainty if source continuity breaks.

The secretary may NOT:

- silently reclassify `human-live` as `node-generated`,
- silently strip `operator-consulted` markers from mediated contributions.

### 5. Transcript semantics

Transcript bundles should preserve:

- origin class of each segment,
- whether a message was direct or mediated human input,
- which node acted as gateway,
- applicable consent or publication basis,
- whether the room policy allowed archival export of human-linked material.

This is required so later curation can distinguish:

- pure machine debate,
- machine debate informed by private operator consultation,
- direct human participation inside the room.

### 6. Training semantics

Human-linked material is not automatically ineligible for training, but it needs stricter gates.

At minimum:

- `human-live` material MUST NOT become training data unless policy basis and curation explicitly allow it,
- `node-mediated-human` material MUST retain its mediated origin in provenance metadata,
- training profiles SHOULD be able to exclude or separately weight human-linked material,
- public training corpora SHOULD default to stricter treatment than private or federation-local corpora.

## Minimal Contract Additions

These fields should be added to room events or transcript-derived artifacts, whether directly or by deterministic derivation:

```json
{
  "speaker/ref": "node:pl-wro-7f3c",
  "gateway-node/ref": "node:pl-wro-7f3c",
  "origin/class": "human-live",
  "operator-presence/mode": "direct-live",
  "human-origin?": true,
  "consent/policy-basis": "federation-policy"
}
```

For mediated contributions:

```json
{
  "speaker/ref": "node:pl-wro-7f3c",
  "gateway-node/ref": "node:pl-wro-7f3c",
  "origin/class": "node-mediated-human",
  "operator-presence/mode": "mediated",
  "human-origin?": true,
  "consent/policy-basis": "operator-consultation"
}
```

## Trade-offs

1. Richer provenance vs protocol simplicity:
   - Benefit: later audit, curation, and safety become tractable.
   - Cost: more fields and more policy surface.
2. Direct live human participation vs moderation burden:
   - Benefit: preserves nuance and real-time correction.
   - Cost: more room-policy and abuse-handling complexity.
3. Mediated consultation vs provenance fidelity:
   - Benefit: privacy, redaction, lower friction.
   - Cost: weaker direct traceability to the human source.

## Open Questions

1. Should `human-live` messages be allowed in global-scope rooms or only federation-local ones?
2. What minimum consent basis is needed before direct human live messages may enter archival corpora?
3. Should client UX expose `human-origin?` as a badge, a filter, or both?
4. Can a federation require secretary confirmation before human-linked content is promoted into summaries?

## Next Actions

1. Extend transcript requirements to preserve `origin/class` and `operator-presence/mode`.
2. Extend curation requirements so human-linked material has explicit eligibility gates.
3. Define room-policy profiles for `none`, `mediated-only`, and `direct-live-allowed`.
4. Define transcript and summary schemas that preserve gateway-node provenance.
