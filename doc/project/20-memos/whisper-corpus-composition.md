# Whisper–Corpus Composition: Association Rooms Hiring Collective Expertise

Based on:
- `doc/project/40-proposals/013-whisper-social-signal-exchange.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/070-room-primitive.md`
- `doc/project/40-proposals/073-agent-orchestration-organ.md`
- `doc/project/40-proposals/066-inquirium-assistant-channel.md`
- `doc/project/20-memos/swarm-broadcast-assistance.md`

Date: 2026-07-03

## Summary

Whisper and Corpus solve two halves of one social problem. Whisper organizes
people **by resonance**: weak signals correlate, a threshold is crossed, and an
opt-in association room forms around a shared problem or idea. Corpus organizes
expertise **by competence**: a canonical topic term resolves to topic-expert
nodes, procurement selects a subset, and deliberation converges on one signed
answer. The natural composition is a **containment/usage relation**: a
Whisper-born association room MAY use Corpus — possibly repeatedly over its
lifetime — whenever the group needs collective expert reasoning about the
problem that brought it together.

Both ends already exist as contracts. This memo records the composition
decisions so the choreography does not have to be re-derived later.

## Two integration paths, in order

**Path (a) — side-room deliberation (first; composes existing contracts).**
A member of the association room runs a Corpus procurement and, when live
deliberation is available, a separate deliberation room. Only the **conclusion**
flows back: the signed, content-addressed final answer artifact is posted into
the association room. The main room stays low-noise, and the existing boundary
is preserved across rooms: deliberation chat is *reasoning, not protocol
facts*; the answer is the durable artifact. Note that the Corpus MVP
(procurement over Artifact Delivery) needs no Room at all, so the earliest
useful form of this path is simply: association room member procures a Corpus
answer and posts it back.

**Path (b) — in-room live assistance (later; needs P070 + P073 maturity).**
Corpus-selected experts (each an Inquirium-backed participant) join the
long-lived association room itself and assist the human discussion live. This
requires Room membership semantics for agent participants and bounded Agent
(P073) sessions inside a long-lived room. It is deliberately second: it
inherits exactly the prerequisites Corpus P069 already declares for live
deliberation.

## Funding modes: sponsored and gift

A Corpus usage inside a Whisper process is either:

- **sponsored** — a member (or an outside supporter) contracts and pays for the
  procurement; the sponsor is the asker in the existing settlement-bridge sense
  (P069 §7, single contracting provider in MVP), or
- **gift** — offers priced at zero.

**Price `0` is normatively a transition into the gift economy**, not a
degenerate price point. A zero-price offer means the provider is contributing
work as mutual aid (VISION: the network strengthens the most vulnerable, not
only the fastest). Providers SHOULD be able to *position themselves* for this:
a topic-scoped `corpus.provider` offer may signal affinity for community work
("I like solving social problems", "I like working on ideas together") and may
carry a zero or non-zero price accordingly. The concrete offer-field shape
belongs to the offer-catalog/Corpus contracts when this is picked up; this memo
fixes only the semantics.

## Privacy guard: the community marker must not deanonymize the room

Providers benefit from knowing that a request is part of community work — both
to filter and to position. But Whisper's association rooms stand on
`private-correlation`: their existence and membership can be sensitive. The
community-work signal therefore MUST be **coarse, optional, and
disclosure-scope-aware** — e.g. a `context/class: community-gift` style marker
that says *"this is community work"* and nothing more:

- it MUST NOT carry the association room id, the Whisper topic class, or any
  member identity,
- the sponsor/asker is the **only** identity a provider sees,
- whether to attach the marker at all is the room's (or sponsor's) choice under
  its disclosure scope.

Without this guard, procurement becomes a side channel leaking that a group
exists — exactly what Whisper's envelope/content split is designed to prevent.

## Human-in-the-loop gates effects, not turns

Human-in-the-loop applies to **effects, budgets, and acceptance — never to
individual conversational turns of an agent deliberation**. A human MAY join a
deliberation room as a participant, but human presence is not a gate on the
debate. What makes unattended deliberation safe is already the architecture:

- bounded Agent contracts (P073: max cost, max time, max actions),
- Inquirium effect intents, leases, and budget metering,
- room access lists,
- the single signed final answer as the only durable output,
- and each member's local capture/audit policy.

This is graduated autonomy priced in budget, not supervision of every step. It
does not weaken the P066 `assistant-human-in-loop-governance` rule: actions
affecting relationships, external publication, or governance still require
explicit operator approval — those are *effects*, and they stay gated. What a
group of agents may do unattended is *reason*; what they may not do unattended
is *commit*.

## Anti-Goodhart guard for future reputation

If reputation or creator credits ever attach to Corpus work, they MUST NOT
accrue as a fungible score proportional to completed-task count or price —
otherwise cheap or zero-price tasks become a reputation mine ("buying
reputation with cheap tasks"), and the gift economy is the first thing
corrupted by it. The direction consistent with the rest of the system:

- gift work earns a **non-fungible acknowledgment**: a signed attestation fact
  from the concrete counterparty ("this node helped our community work on X"),
  auditable and presentable, but not aggregable into a ranking,
- no global score, no leaderboards — consistent with the assistant
  non-dopamine invariants (P066) and with P076's explicit non-goal of a
  federation reputation system,
- recognition is a *trace*, not a *currency*.

## What this memo does not decide

No schema changes are made here. When implementation picks this up, the
concrete artifacts land in their owning contracts: the community-affinity
offer field (offer catalog / Corpus P069), the coarse `context/class` marker on
Corpus queries (P069), and the room artifact-post used by path (a) (Room P070).
Path (b) and crisis-path composition remain open. Cross-federation
(`alliance`) semantics are now frozen in Proposal 079 as a unilateral
`alliance-policy.v1` contract, while concrete Whisper/Corpus runtime use
remains deferred there.
