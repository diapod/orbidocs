# Operator Proxy and Co-Regulation Channels

Based on:
- `doc/project/20-memos/operator-proxy-co-regulation.md`

## Status

Proposed (Draft)

## Date

2026-03-21

## Executive Summary

This proposal defines a bounded proxy-to-proxy dialogue model in which a node may act
as an external-facing spokesperson for its human operator and, where justified, enter a
co-regulation dialogue with another node representing another operator.

The key decision is that this channel belongs to the care and de-escalation layer, not
to hidden arbitration. The swarm may help people restore perspective and productive
agency, but it must not silently seize authority over their interpersonal conflicts.

## Context and Problem Statement

Some harmful or blocked interactions emerge not inside formal swarm debates, but in the
relational dynamics between human users. A node may detect:

- repeated frustration,
- anger escalation,
- cognitive blockage,
- destabilizing interaction loops,
- loss of productive turn-taking.

The system already has ideas for care-oriented modes and operator participation in live
rooms, but it does not yet define a distinct channel where one node may speak
proxy-to-proxy with another node on behalf of their operators.

Without such a model:

- nodes either remain passive in obviously escalating relational situations,
- or they improvise paternalistic interventions with no explicit policy boundaries,
- or they fall back too quickly into justice-oriented logic where care-oriented
  mediation might still work.

## Goals

- Define a bounded co-regulation dialogue model between operator proxies.
- Keep the model explicitly care-oriented rather than punitive.
- Preserve operator override and opt-in boundaries.
- Support private local linkage of known contacts without global depseudonymization.
- Make proxy suggestions auditable, explainable, and non-coercive.

## Non-Goals

- This proposal does not define a full arbitration court or binding dispute-resolution
  process.
- This proposal does not create a global contact graph.
- This proposal does not define real-world identity disclosure between operators.
- This proposal does not override constitutional justice procedures for high-stakes
  abuse or formal sanctions.

## Decision

Orbiplex should support an optional `operator-proxy` channel class for co-regulation
and de-escalation between nodes representing their operators.

At baseline:

1. a node MAY open a bounded proxy dialogue on explicit operator request or on
   sufficient conflict signals,
2. the channel MUST remain opt-in and operator-overridable,
3. outputs MUST be framed as suggestions, reframes, pacing interventions, or
   perspective prompts rather than binding judgments,
4. local contact linkage MUST remain local unless explicitly shared,
5. proxy-to-proxy co-regulation MUST NOT silently become identity disclosure or
   punitive adjudication.

## Proposed Model

### 1. Channel purpose

The purpose of the channel is:

- reduce escalation,
- restore productive agency,
- support perspective shift,
- protect well-being,
- improve conditions for later direct or mediated human dialogue.

The channel is not for:

- hidden punishment,
- forced settlement,
- undeclared evidence gathering for sanctions,
- covert depseudonymization.

### 2. Trigger classes

A node may open or suggest opening the channel when:

- its operator explicitly asks for mediation help,
- repeated strong conflict signals are detected,
- interaction quality sharply degrades,
- one or both sides appear cognitively blocked,
- the node predicts that ordinary dialogue will otherwise continue to worsen.

Triggers should be logged as inference or operator request, not disguised as certainty.

### 3. Output classes

Valid output classes include:

- reframe suggestions,
- perspective-switch prompts,
- cooldown or pacing suggestions,
- explicit clarification prompts,
- safer turn-taking suggestions,
- proposals to pause, defer, or move to another communication mode.

The output is advisory. Acceptance remains with human operators unless a separate
process is entered.

### 4. Identity and linkage model

The system should support private local linkage of contacts known to the operator.

Each node may keep local mappings such as:

- phone or email contact id,
- address-book handle,
- local nickname,
- known peer node pseudonym,
- ephemeral peer pseudonym used only in one relational context.

These mappings:

- remain local by default,
- support trust context and mediation routing,
- do not constitute global identity reveal.

### 5. Consent and override

The channel should remain:

- opt-in by policy or operator preference,
- bounded in scope and time,
- suppressible by either operator,
- disable-able per contact or context,
- explicit about what is inferred rather than observed.

Nodes may suggest that a co-regulation channel would help; they must not silently lock
users into it.

### 6. Relation to care and justice modes

This channel belongs to the care-oriented side of the system.

Default rule:

- use proxy co-regulation where harm appears relational, reversible, and still
  de-escalatable,
- escalate to justice-oriented or constitutional procedures only when evidence,
  severity, repeated abuse, or safety thresholds require it.

This keeps the channel from becoming a hidden soft-policing mechanism.

### 7. Audit and provenance

The system should preserve:

- why the channel was opened,
- which node opened it,
- whether the trigger was operator-requested or inference-driven,
- what class of suggestions was produced,
- whether the operators accepted, ignored, or disabled the suggestions.

Audit should preserve rationale and boundary compliance, not expose unnecessary private
content.

## Trade-offs

1. Better relational support vs paternalism risk:
   - Benefit: the swarm can help reduce unnecessary escalation.
   - Cost: badly designed defaults may feel manipulative or overreaching.
2. Local contact linkage vs privacy sensitivity:
   - Benefit: more realistic mediation and trust context.
   - Cost: careless implementation could become stealth contact graphing.
3. Soft intervention vs strict procedural neutrality:
   - Benefit: preserves care capacity before harm hardens into formal dispute.
   - Cost: policy boundaries must be clearer than in ordinary assistant UX.

## Open Questions

1. What minimum conflict-signal threshold should justify opening a proxy dialogue
   without explicit operator request?
2. Should some federations require stronger operator consent before inference-triggered
   co-regulation starts?
3. How much of proxy-channel output, if any, may enter durable transcripts?
4. Should repeated refusal of care-channel suggestions influence later moderation or
   safety heuristics?

## Next Actions

1. Define operator-proxy session metadata and local contact-linkage contract.
2. Define safe default trigger thresholds and disable rules.
3. Define audit fields for proxy-channel opening, suggestion class, and closure.
4. Decide whether this channel needs dedicated client UX distinct from ordinary chat.
