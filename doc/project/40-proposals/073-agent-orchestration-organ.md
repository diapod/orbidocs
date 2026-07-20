# Proposal 073: Agent — Bounded Stateful Orchestration Organ

Promoted to:

- `doc/project/60-solutions/047-agent/047-agent.md`

## Status

`promoted`

## Date

2026-06-26

## Executive Summary

Orbiplex should introduce **Agent** as the node organ for stateful, bounded,
multi-step orchestration that sits **above** Inquirium. An Agent is a durable,
addressable entity that binds a model-selection policy, a remembered session
context, parameters, a budget, and a bounded controller loop, with an explicit
lifecycle: `spawn`, `fork`, `suspend`, `resume`, `stop`.

An Agent **composes** other organs and owns none of them. It calls Inquirium for
inference, declares bounded observation needs and effect proposals through
horizontal contracts, and uses Memarium-backed durable memory (not the agent's
hot working/KV memory). The host resolves those ports through the owning domains
and owns authority, budget, and lifecycle. This realizes the agentic mode — an entity with
an attached model, remembered context, and parameters, plus actions that
multiply or stop agents — that Inquirium deliberately excludes:

> "In Orbiplex, Inquirium is not the agent loop. … Flow, Arca, Sensorium, and the
> host own broader orchestration." — Proposal 063

Agent is that missing home, defined so that no model ever gains ambient authority.

The governing rule is:

```text
Agent is the bounded controller with identity, memory, and a lifecycle.
Inquirium answers; Memarium remembers; the host resolves observations and effects.
The agent declares needs, proposes effects, and orchestrates; it never selects an
authority path or self-authorizes an effect.
```

## Context and Problem Statement

Inquirium is bounded inquiry and is explicitly *not* the agent loop (Proposal
063; Proposal 064 invariant "conversation orchestration is not an Inquirium
adapter concern"). Proposal 064's Flow IR permits only an inline `bounded
controller` (`max_steps`, `max_cost`, `max_time`, `allowed_tools`,
`termination_condition`, review policy). Proposal 066 assigns agentic effects to
this capability-gated Agent layer rather than to Inquirium or its adapters.

Yet real workflows need a stateful agent: an entity that remembers a session,
holds parameters, runs several inference steps toward a goal, may spawn helpers,
and can be stopped. Today that entity has no home. Putting it inside Inquirium
would make a model adapter an ambient agent — the named threat "Inquirium becomes
a general AI agent with ambient authority" (Proposal 063). Leaving it ad hoc
invites the classic agent failure modes: unbounded loops, fork bombs, orphaned
state, runaway cost, and effects without accountability.

Agent gives that entity one durable, host-owned, auditable home with an explicit
lifecycle and authority that is bounded by construction.

## Goals

- A first-class, durable, addressable `Agent` abstraction binding model-selection
  policy, remembered session context, parameters, budget, and a bounded
  controller.
- Explicit lifecycle operations `spawn`, `fork` (multiply), `suspend`, `resume`,
  `stop` as host capabilities — budget-metered, ledgered, fail-closed.
- Strict stratification: Agent uses horizontal inference, observation, effect,
  memory, and causal contracts; the host composes them with Inquirium, Sensorium,
  Workbench, Memarium, and other vertical domains. Neither side acquires the
  other's authority or implementation vocabulary.
- Bounded by construction: monotone narrowing on fork, bounded fan-out, enforced
  budget, mandatory termination, no self-authorizing agents.
- Full causal trace: every step, spawn, effect proposal, and lifecycle transition
  is an auditable, prompt-free fact.

## Non-Goals

- Not an inference engine (Inquirium), effect engine (Sensorium), memory store
  (Memarium), or authority root (host).
- Not ambient autonomy and not a general AI agent with standing authority.
- Not a replacement for Flow IR's declarative DAG; the two are complementary (an
  Agent may run a Flow; a Flow may spawn an Agent).
- Not a cross-node/federated agent runtime in this slice (deferred).

## Decision

### 1. Agent is a stateful organ above Inquirium

An `Agent` is a durable record plus a host-run controller. It binds, by
reference, everything an agentic session needs, and nothing it must not own:

```text
Agent {
  agent/id
  agent/parent?            # lineage for forked/spawned agents
  model-selection          # profile/ref or runtime-candidate constraints;
                           #   host-owned binding, never a raw provider key
  session/ref              # Memarium-backed remembered context (durable facts)
  params                   # AssistantMode (ModeKeyed), plurality, classification
                           #   ceiling, instruction profile (PromptAssemblyPolicy)
  budget                   # token / cost / wall-time / step ceilings (enforced)
  controller               # bounded loop policy (see 3)
  grants[]                 # capability ids this agent may request (gated)
  trust/locality           # default local-only / strict_local
  lifecycle/state          # pending | running | suspended | completed
                           #   | stopped | failed
}
```

The boundary is hard: Inquirium has **zero knowledge of agents**. The Agent calls
`inquirium.generate` (and future operations) as a normal host-capability caller,
subject to the same classification, inference grants, and trace discipline as any
other caller. Inquirium output remains *evidence*, never authority.

The same boundary applies to collaborative rooms. A model-backed participant in a
Room or Corpus deliberation is represented by an Agent controlled by an
accountable subject or node role; a raw Inquirium adapter or model runtime is not
a room member. If a deployment wants a one-shot model respondent, it should use a
degenerate Agent profile with one step and an explicit budget rather than admit
the adapter as a speaking actor.

### 2. Lifecycle: spawn, fork, suspend, resume, stop

Lifecycle operations are **host capabilities**, not Inquirium operations. The
node-local slice registers `agent.spawn`, `agent.status`, `agent.stop`,
`agent.fork`, `agent.suspend`, and `agent.resume` in the Capability Registry
(Solution 037). Every mutation carries an idempotency key and is admitted by the
host before an append-only lifecycle command/state fact is written. The command
fact is the commit marker and authoritative replay record; the state fact is its
rebuildable audit projection, so a partial multi-fact write cannot lose the
idempotency decision. Local control retains administrative authority. A module
caller is admitted only when its JSON-e Flow configuration contains a separate,
bounded `agent_grants` entry for the exact `agent.*` capability; `allowed_calls`
alone is syntax, not authority. Request-size, Agent-id-prefix, profile, and
delegated-capability bounds are checked before lifecycle or binding admission.

```text
agent.spawn   { spec | template/ref, budget, grants }       -> Agent (pending)
agent.fork    { agent/id, narrowing }                        -> child Agent
agent.suspend { agent/id }                                   -> suspended
agent.resume  { agent/id }                                   -> running
agent.stop    { agent/id, reason }                           -> terminal
agent.status  { agent/id }                                   -> read-only projection
```

State machine:

```text
pending -> running -> { suspended <-> running } -> completed | stopped | failed
```

In the current node-local slice, lifecycle mutations are authoritative and
exactly replayable from durable command facts: an exact retry returns the prior
result while reuse of an idempotency key with a different request fails closed.
`suspend` freezes the controller while preserving its fact projection; `resume`
continues from the latest durable state rather than replaying a prompt. Terminal
state and TTL reaping are durable. The current controller has no detached
background step to cancel: suspend or stop prevents the next passage. Agent-owned
leases are persisted in the existing model-runtime lease registry and released
on synchronous effect completion, terminal controller state, explicit stop, TTL
reaping, or startup reconciliation. A deferred effect retains its lease until a
bounded scheduler observes terminal status in the shared Deferred Operation
Registry, or until Agent termination or lease TTL. Exact dispatch replay returns
the durable deferred or terminal projection without reinvoking the target. The
reconciler advances a bounded fairness cursor through the recovered candidate
projection so an early page of live operations cannot starve later terminal
ones; durable facts, not that disposable cursor, remain the restart source of
truth.
Unused child budget is returned by rebuilding the reservation projection from
durable child state and metered spend: a live child retains its bounded
allocation, while a terminal child retains only spent budget and still-live
descendant commitments.

### 3. Multiplication is monotone narrowing with bounded fan-out

`agent.fork` is the "multiply" action, and it can only narrow. On **every** axis a
child is a subset of its parent: `grants ⊆ parent.grants`, classification ceiling
no higher, autonomy no looser, `allowed_tools ⊆ parent`. The parent's budget is
**split**, not duplicated — a child draws from a reserved slice of the parent's
remaining budget. This mirrors the monotone discipline of `ClassKeyed`/`ModeKeyed`
and `PromptAssemblyPolicy`: a lower scope may specialize, never widen.

Fan-out is bounded by construction to prevent fork bombs and resource exhaustion:

```text
controller {
  max_steps
  max_depth                # spawn-tree depth cap
  max_children             # direct children per agent
  max_concurrent           # live descendants across the tree
  aggregate_budget         # whole-tree token/cost/time ceiling
  termination_condition    # mandatory; an agent with no terminator is rejected
  review_policy            # when a human gate is required
}
```

There are **no self-authorizing agents**: an agent cannot grant itself a
capability, raise its own budget, or spawn a child with authority it does not
hold.

### 4. Agent state is durable facts, not mutated objects

Session seeds and lifecycle transitions are append-only facts in Memarium
(Proposal 036), not mutated in place. This gives `as of` queries, audit, and
replay: the trajectory of an agent — what it knew, decided, spawned, and stopped
— is reconstructable. The live controller holds only a cache derived from those
facts; the facts are the source of truth. `resume` and crash recovery both rebuild
from the same fact stream.

Memory follows the `MemoryPolicy` from Proposal 064: pinned facts (never
auto-summarized), a bounded rolling summary, and a host-pinned recall allowlist —
so context does not grow without bound.

#### Memory model: durable plane vs working set

Memarium is the agent's **durable, governed memory** — the source of truth — not
its hot working memory. The two are distinct strata and must not be conflated:

```text
durable fact plane (Memarium)    source of truth: governed, classified, "as of",
   |  MemoryPolicy projects v        auditable, replayable, optionally federated
working set / assembled context  ephemeral, per-step, token-bounded
   |  rendered into v
provider KV / prompt cache        optimization, runtime/provider-side, discardable
```

Two consequences:

- **Memarium is off the hot path.** The agent reads through a projection (the
  working set built by `MemoryPolicy`) and writes only *meaningful facts* —
  turns, results, decisions, observations — never the KV cache token by token.
  This keeps the per-step path fast and the governed log free of bulk or
  ephemeral content (Proposal 066: `memarium.write` stays a fact-plane).
- **Degraded mode mirrors the assistant.** When Memarium is disabled at startup,
  the agent runs on a local ephemeral, non-federating fact store and reports that
  durability explicitly in status. When a configured Memarium write fails, the
  mutation fails closed rather than silently changing durability. A later
  transition between these modes requires an explicit reconciliation protocol;
  the current process does not switch sources of truth dynamically.

By memory type: the working set is **working memory** (KV-like, ephemeral);
Memarium holds **episodic** (this session) and **semantic/long-term** (across
sessions) memory; procedural memory lives in grants and templates, not Memarium.

### 5. Observations are needs; effects are proposals; inference is evidence

A controller step may declare an `AgentObservationNeed` containing an opaque
`source/ref`, expected `payload/schema-ref`, and age/byte bounds. A durable
`AgentObservationBinding` fixes which need and source a consumer-authorized Agent
may use. `agent-core` does not know whether that source is a Sensorium Interface,
Room projection, Workbench view, or a future domain. The daemon composition root
selects the resolver, rechecks its domain authority, validates the payload at the
schema gate, and returns bounded inert context plus prompt-free
`AgentObservationEvidence` carrying the source P081 `causal/context` plus distinct
source-version and resolution references.

Observation evidence may additionally carry a bounded list of opaque contextual
qualifiers as `(schema/ref, value/ref, digest)` tuples. This keeps `agent-core`
substrate-neutral: it does not learn the Sensorium operational-impact vocabulary or
interpret a Workbench environment. The daemon resolver validates each qualifier in
the owning domain and supplies only admitted refs and digests to Agent state and
prompt-free traces.

For `sensorium-operational-context.v1`, the composition root must resolve the
qualifier before exposing the associated observation payload to an Agent passage.
It computes a local caution class as the maximum of the source-published class and
any stricter local policy floor, then asks the host-owned Inquirium prompt assembly
boundary to render a fixed, versioned caution layer. The layer is present before the
first inference step that can consume the feed and before every later passage whose
working set includes it. A remote `context/summary` remains retrieved data below the
instruction hierarchy; it is never promoted into a system or developer instruction.
The composition root also records a deterministic host-owned provenance object with
the local policy ref, local floor, selected class, and each admitted source class
paired with its exact qualifier digest. It passes the same bounded projection directly
to the durable Inquirium trace rather than reconstructing it from caller metadata or
provider output. This evidence distinguishes a source-published high-impact class from
a stricter class selected by local policy without teaching `agent-core` the Sensorium
vocabulary.

Missing, malformed, stale, or descriptor-inconsistent operational context fails the
collaborative-live observation resolution closed. When a future passage admits more
than one live source, the host uses the maximum caution class while retaining every
per-source qualifier ref and digest for audit; it does not persist a second
authoritative `effective-*` wire field. This context changes reasoning posture, not
effect authority: all effect proposals still pass their normal grant, lease, policy,
and human-review boundaries.

`Stale` is not an Agent-owned timeout. It means exactly that P082 reports a source
generation mismatch or a superseded interface publication. Agent Core neither reads
source clocks nor derives freshness from passage age. The optional summary is
already bounded by P082 to 512 UTF-8 bytes and remains untrusted observation data.

A controller may also *propose* an effect. The agent never executes one directly
and never chooses the provider or authorization path. The daemon maps the generic
proposal to a closed host adapter such as Sensorium or Artifact Delivery and
enforces grants, leases, classification, quarantine, and human-in-the-loop policy.
Sensitive classes (relationship, governance, external publication, egress)
require operator approval, inheriting Proposal 066's Phase 3 contract. An
Inquirium `Plan` return remains a `CandidatePlan` the host compiles or rejects
(Proposal 064); the agent is the durable, addressable form of that same host-first
orchestration, not an escape hatch around it.

JSON-e Flow may define only **static declarative wiring**: an operator-authored,
schema-validated, digest-pinned mapping from `need/ref` to opaque `source/ref`,
schema, and bounds, plus separately admitted grant requests. Rendered flow data
may select or narrow a predeclared mapping but cannot create or widen one. Agent,
model, or observation output must never interpolate an authority-significant
wiring field. After caller-capability and ownership checks, the daemon must prove
that every exact `source/ref` plus `payload/schema-ref` pair has one registered
resolver before persisting a binding; absent, incompatible, and ambiguous pairs
fail closed. Authorization, classification, source interpretation, and effect
semantics remain compiled host code. Every successful resolution emits a stable
`resolution/ref` and preserves the validated source `causal/context` in the Agent
trace. Step facts and traces bind that evidence to the enclosing `agent/id`,
`binding/ref`, and canonical passage ref. The resolution ref makes the selected
binding auditable; the causal context preserves the source chain without retaining
payload bytes.

### 6. Stratification and crates

```text
agent-core (thin contract crate)
  - Agent / controller / budget / grant DTOs
  - substrate-neutral observation need/binding/evidence and effect-proposal DTOs
  - lifecycle state machine + monotone-narrowing validator
  - depends on horizontal P081, classification, serde/error, plus one explicit
    vertical exception: pure inquirium-core request/result DTOs for the Agent's
    constitutive bounded-inference operation
  - the Inquirium exception carries no host, provider, runtime, or authority code
  - MUST NOT import Room, Corpus, Memarium, Sensorium, Workbench, or other
    provider-specific source/effect types
  - MUST NOT depend on substrate (daemon, model-runtime, HTTP, async, SQLite),
    enforced by a positive direct-dependency allowlist plus vertical dependency
    and vocabulary checks

daemon (substrate)
  - agent.* host capabilities and the bounded controller runtime
  - composition-root resolvers from opaque observation/effect refs to owning domains
  - durable agent/session store (Memarium-backed) + spawn-tree budget metering
  - schema-gate validation, capability/HIL gating, lease lifecycle, decision ledger, trace
```

## Implementation Recommendations

Implement Agent as a stratified host organ, not as an Inquirium operation, model
adapter, Flow shortcut, or ambient daemon side loop. The first runtime slice
should use a **daemon-owned controller** that may call Flow IR for bounded
sub-steps, but the controller lifecycle, authority checks, budget metering, and
stop/suspend/resume semantics remain host-owned. This keeps one orchestration
substrate responsible for live agent state while still allowing declarative Flow
plans to be one of the things an agent executes.

Build the implementation in layers:

1. Keep `agent-core` as the substrate-free contract crate: DTOs, validation,
   lifecycle state machine, monotone fork validator, generic observation/effect
   port values, and schema constants only. It must not gain Sensorium, Workbench,
   provider, daemon, model-runtime, HTTP, async runtime, SQLite, or store
   dependencies.
2. Add the daemon host facade and local-control surfaces for the smallest useful
   lifecycle: `agent.spawn`, `agent.status`, and `agent.stop`. `fork`,
   `suspend`, `resume`, effects, and assistant escalation come after this slice
   can create, inspect, stop, and audit a bounded local agent.
3. Persist lifecycle transitions as append-only facts. The live controller may
   keep an in-memory working projection, but that projection is cache-like and
   disposable. It is not Memarium, not authority, and not required for crash
   recovery semantics.
4. Add budget/fan-out enforcement before enabling `fork` or effect proposal
   routing. A fork without budget split and monotone narrowing is not an agent
   feature; it is a fork bomb waiting for policy.
5. Route effects only as generic proposals through closed daemon adapters and
   existing host capabilities. Agent output may ask for an effect; the host and
   operator remain the authority that admits, denies, delays, or scopes it.
6. Keep JSON-e Flow at the wiring layer. Static, digest-pinned configuration may
   map a need to an opaque source and declare grant requests; it must not evaluate
   authorization, classification, source semantics, or agent-generated wiring.

The first implementation slice is **node-local only**. Cross-node or federated
agents are explicitly deferred to a later proposal and must not leak into the
first controller through remote spawn, remote resume, or federated state
replication. A local agent may call existing federated organs through explicit
capabilities, but the agent lifecycle itself is local.

Memarium is the durable fact plane, not the live cache. The first working set
should be an **in-memory / ephemeral projection** derived from the agent request
and any admitted local facts. A dedicated projection cache may be introduced
later if profiling shows the need, but it should be a rebuildable optimization
with clear lifecycle, not a second source of truth.

Explicit non-goal: **do not dump the in-memory runtime cache to disk and reload
it verbatim on restart.** That would make the ephemeral projection a second
source of truth by the back door. The only sanctioned path to surviving a
restart is `agent-durable-state` (append-only `agent.state.v1`/`agent.session.v1`
facts) plus `agent-memory-projection` (rebuilding the working set *from* those
facts) — never a serialized snapshot of the cache itself.

The current implemented slice has a Memarium-backed append-only fact store and a
disposable in-memory projection. Lifecycle commands, session seeds, state,
initial steps, budget traces, effect proposals, and effect outcomes survive a
restart when Memarium is enabled. Exact lifecycle retries rebuild their
idempotency result from those facts. If Memarium is disabled, status reports an
ephemeral, non-federating mode rather than pretending crash recovery exists.

Active lifecycle capabilities require explicit authority. Local control is the
administrative path; module calls require one exact `agent_grants` entry in the
calling JSON-e Flow configuration, and lifecycle operations are additionally
restricted to Agents created by that module. Binding and effect-dispatch grants
carry an explicit target-capability allowlist. Mutations preserve either
`local-control` or the concrete caller module id in lifecycle facts. The rebuilt
idempotency projection has a fail-closed bound: once its configured capacity is
reached, new mutations are denied rather than evicting replay evidence and
making duplicate execution possible.

Use conservative, overridable developer defaults for the first profile:

```text
max_steps       = 8
max_depth       = 1
max_children    = 0 or 1
max_concurrent  = 1
wall_time_ttl   = short, deployment-configured
```

These defaults are a safety floor, not a constitutional constant. Distributors
and operators may override them in agent configuration, but widening must remain
explicit, validated, and visible in status/trace. The default profile should
reject agents without a termination condition, agents with unbounded budget,
unknown capability grants, or effects that try to execute without a host grant.

Minimum test matrix for the first slices:

- lifecycle state-machine transitions, including invalid transition denial;
- `spawn/fork/suspend/resume/status/stop` local-control E2E with exact mutation
  replay and conflicting idempotency reuse denied;
- unknown fields and missing termination condition fail closed;
- classification ceiling defaults fail closed;
- no ambient capability: an agent without a grant cannot invoke Inquirium or
  propose effects;
- no vertical-domain dependency or vocabulary in the Agent observation/effect
  port, and no dynamically interpolated observation binding;
- binding admission refuses absent, schema-incompatible, or ambiguous resolvers,
  and observation evidence cannot be moved across Agent, binding, or passage;
- monotone fork denial for widened grants, classification, autonomy, tool set,
  or budget once `fork` is enabled;
- bounded fan-out defaults prevent more than the configured children/concurrency;
- prompt-free step/status traces contain refs, digests, budget deltas, and
  decisions, but not prompt text, model output, or raw context.

### Controller as a functional core (`agent-host`)

The "daemon-owned controller" above should follow the same functional-core /
imperative-shell split already used by `inquirium-host`: the per-step controller
*decision* is a pure value computed in an `agent-host` service stratum, and the
daemon performs the effects. Each tick produces an `agent.step-decision.v1`:

```text
agent.step-decision.v1 {
  step/no
  action            # call-inquirium {request-ref, observation-need?}
                    #   | propose-effect {proposal-ref}
                    #   | spawn-child {child-spec-ref} | await-human | complete | fail
  budget-charge
  termination-satisfied
}
```

The daemon executes the chosen action and feeds the result back; the decision
itself is replayable and unit-testable without sinks. This keeps the agent loop
from accreting daemon coupling, mirroring the Inquirium decoupling. Stratify as
`agent-core` (contracts + state machine) → `agent-host` (pure step decisions plus
read-ports) → daemon (effects, persistence, budget metering), guarded by a
dependency-direction lint.

`expected-step` prevents replay after a committed passage, while proposal and
fork actions retain their own exact idempotency identities. A remote model
provider call cannot honestly promise exactly-once execution unless that
provider accepts and enforces the stable request identity. The host therefore
uses a stable `request/ref`, idempotent budget accounting, and content-addressed
product storage; an adapter SHOULD forward provider-native idempotency when it
exists. Implementations MUST NOT describe this boundary as exactly-once merely
because the local step commit is replay-safe.

Step `0` is a durable bootstrap projection and does not consume runtime step
budget. Explicit controller ticks start at `1`; each consumes exactly one step,
checks the absolute wall-time deadline and remaining host-owned budget, and
stops the bounded run on `await-human` or a terminal decision. A waiting Agent
is never polled merely because scheduler time passed.

Lifecycle requests carry an `idempotency/key`: a retried `spawn`/`fork` must
replay the prior result, not create a second agent or a second child.

### Consumer binding (collaborative chair/participant, assistant, Flow node)

Agent is driven by domain consumers, not invoked bare. The recurring shape is one
binding contract, `agent.binding.v1`, that attaches an agent to a consumer's
session and output sink under narrowed authority:

```text
agent.binding.v1 {
  binding/id, agent/ref
  consumer/kind                 # collaborative-chair | collaborative-participant | assistant-channel | flow-node
  consumer/ref                  # query/id (Corpus) | session/ref (assistant) | flow/node-ref
  session-source/ref            # room/ref | transcript/ref | dataset/ref  (ref vocabulary)
  output-sink/kind              # collaborative-answer-draft | collaborative-turn-draft | assistant-response-draft | flow-result
  grants[]                      # MUST be a subset of the consumer's own grants
  budget                        # from the consumer policy (deliberation budget / assistant rigor)
  participant/ref?              # host-minted accountable principal; never model identity or model-supplied
  membership-attestation/ref?   # room-membership-attestation.v1 for Corpus bindings
  membership-attestation?       # inline create-time evidence; verified, never persisted in the binding
  human-in-loop                 # approval policy for effect proposals
}
```

Invariants:

- **Grants are monotone-narrowing from the consumer.** A consumer cannot grant the
  agent more authority than it holds — the same discipline as `fork`
  (`validate_fork_from`). Corpus and the assistant narrow; they never widen.
- **The agent is a Room participant, never a raw model adapter.** For
  `collaborative-chair` or `collaborative-participant`, the Corpus adapter joins
  the agent to the deliberation room through
  `room-membership-attestation.v1` (Solution 036). Binding creation carries the
  complete signed credential as boundary evidence; the host verifies its schema,
  signature, freshness, room, participant, required grants, deadline, and issuer
  authority, then persists only the content-addressed attestation ref. The
  node-local first slice requires the signer to equal the local Corpus round
  authority; later remote authorities must be admitted by explicit Room policy.
  Its contributions are room facts signed by its principal, satisfying Proposal
  069's "no raw model adapters as room participants".
- **Output is a draft, not an effect.** The agent produces a content-addressed
  product (`agent.outcome.v1`); the consumer admits it (Corpus stores an inert
  answer draft before any separately chair-signed final answer; the assistant
  surfaces a response draft). The agent never publishes or settles on its own.
- **Assistant escalation approval is not draft-render approval.** The operator's
  explicit approval authorizes creation or binding of the bounded Agent. Once that
  approved binding produces a valid `assistant-response-draft` for the same
  `session/ref`, the Assistant Channel may render the draft without asking a second
  operator question. Rendering is not publication or effect authority: schema,
  digest, classification, binding, session, and output-sink validation remain
  fail-closed, while every proposed effect and any external publication continue
  through their own capability and human-in-loop gates.

Reuse, do not reinvent: agent context comes through the existing
`inquirium.context-assembly.request.v1` plus context-source grants and
`MemoryPolicy` (Proposals 064/066), so the agent reads context through the same
classification/grant gates rather than raw; human-in-the-loop for an effect
proposal reuses `inquirium.operator-question.request.v1` (Proposal 066) rather than
a new approval surface; durable facts use the `memarium.write` fact plane.

## Data Contracts

- `agent.spec.v1` — declarative agent specification (model-selection, params,
  budget, controller, requested grants).
- `agent.state.v1` — lifecycle transition fact (state, reason, at, by).
- `agent.session.v1` — durable session seed binding the validated spec, selected
  runtime profile, creation command digest, actor, and expiry. Pinned facts,
  summary refs, and recall refs belong to the separate memory projection tracked
  below; they are not silently embedded in this lifecycle seed.
- `agent.memory-policy.v1` — one immutable, digest-bound revision of the
  host-owned `MemoryPolicy`. It carries bounded pinned facts, an optional summary
  produced by a non-Agent component, and the recall-ref allowlist. Summary
  production remains the responsibility of that external component or Flow;
  neither Agent nor Inquirium silently summarizes its own history.
- `agent.lifecycle-command.v1` — durable idempotency fact for lifecycle mutations,
  binding operation, request digest, actor, result state, and related child where
  applicable.
- `agent.step.v1` — the durable step **fact after** execution or denial: the
  decision taken, the effect outcome, budget spent, evidence/effect refs, and the
  causal predecessor step. Distinct from `agent.step-decision.v1`, which is the pure
  decision computed *before* the effect.
- `agent.spawn.request.v1` / `agent.spawn.response.v1` /
  `agent.fork.request.v1` /
  `agent.suspend.request.v1` / `agent.resume.request.v1` /
  `agent.stop.request.v1` / `agent.stop.response.v1` — lifecycle mutation
  request/response bodies.
- `agent.status.request.v1` / `agent.status.response.v1` — read-only lifecycle
  and budget projection.
- `agent.step-trace.v1` — prompt-free operational trace (step count, budget spent,
  model snapshot, instruction hash, spawn/effect refs; no prompt, output, or
  context content).
- `agent.binding.v1` — how a domain consumer (Corpus chair, assistant, Flow node)
  attaches an agent to a session source and output sink under narrowed grants (see
  *Consumer binding*).
- `agent.assistant-escalation.request.v1` / `agent.assistant-escalation.v1` /
  `agent.assistant-escalation-decision.v1` /
  `agent.assistant-escalation.response.v1` — the explicit, idempotent Assistant
  Channel escalation ceremony. The request binds an inert assistant proposal to
  one node-local Agent spawn and one same-session Assistant Channel binding; the
  durable host facts retain delegated authority and the operator's approved,
  denied, or timed-out decision. No assistant turn or model control creates a
  binding ambiently.
- `agent.effect-proposal.v1` — an agent's **immutable** request to invoke a host
  capability: `proposal/ref`, `capability/id`, `args/digest`, a validated
  `classification` value (or store-side equivalent reference where the envelope
  owns the value), prompt-free `reason/code`, optional `evidence/refs`, and
  `requires-human-in-loop`. The proposal is a fact and is never mutated.
- `agent.effect-proposal-outcome.v1` — a separate host-authored fact, joined to the
  proposal by `proposal/ref`, recording the decision: `outcome`
  (`admitted` | `denied` | `deferred` | `superseded` | `completed` | `failed`),
  `decided-by`, `at`, and the fields appropriate to that transition. An
  execution-deferred outcome binds `effect/ref`, `operation/ref`,
  `result/digest`, and bounded `lease/refs`; a terminal execution outcome retains
  the same causal binding. The outcome is a fact *about* the proposal, not a
  field inside it (facts over overwriting).
- `agent.outcome.v1` — the terminal product a consumer picks up: terminal state,
  `product/kind`, content-addressed `product/ref` (a draft, never inline),
  `budget-spent`, and `trace/ref`.
- `agent.assistant-draft.accept.request.v1` /
  `agent.assistant-draft.acceptance.v1` /
  `agent.assistant-response-draft.v1` — a same-session, local-control acceptance
  boundary over `agent.outcome.v1`. Acceptance verifies the binding, sink,
  content-addressed product and classification before projecting a render-only
  draft. The acceptance fact fixes `publication-authorized = false`; publication
  remains a separate capability-owned effect.
- `agent.step-decision.v1` — the pure, replayable controller decision computed by
  `agent-host` from read-ports **before** any effect; the daemon executes the chosen
  action and records the result as an `agent.step.v1` fact.

Effect dispatch follows the same stratification. `agent-host` owns a closed,
table-driven registry that validates each supported target capability and emits a
transport-independent execution plan. Its fields are private, the plan has no
deserialization path, and daemon admission consumes the plan as one value, so
callers cannot construct an equivalent-looking value while bypassing the policy
registry. Sensorium directives bind `issuer.module_id` to the authenticated
module or the explicit `local-control` actor. The daemon interprets only the
plan's closed target enum, invokes the owning host surface, and persists the
execution outcome. Unknown capabilities have no fallback and fail closed. A bounded
scheduler reconciles execution-deferred outcomes against the shared Deferred
Operation Registry, releases their leases only after terminal target status, and
appends `completed` or `failed` outcome facts; restart rebuilds the candidates
from those facts. `result/digest` identifies the bounded completion evidence
available at the host boundary: the validated target response for synchronous
completion, or the terminal Deferred Operation snapshot for deferred completion.
The exact terminal status remains available in `reason/ref` when several source
statuses collapse into the Agent-level `failed` class.

All requests reject unknown fields at the boundary; classification defaults
fail-closed; identifiers are explicit and canonical.

## Relationship to Existing Mechanisms

- **Swarm Broadcast Assistance (077, advisory companion).** Assistance
  decomposition/routing and unattended multi-agent deliberation ride bounded
  Agent sessions: human-in-the-loop gates *effects, budgets, and acceptance* —
  never individual conversational turns. What agents may do unattended is
  reason; what they may not do unattended is commit.
- **Weak Signal Harvester (078).** A bounded Agent may orchestrate a harvesting
  pass: scan configured sources, request Inquirium grouping/redaction, emit
  finding files, and stop. It must not widen source grants, bypass the findings
  directory, or publish Whisper/network artifacts directly.
- **Inquirium (Solution 044 / Proposal 064).** Agent is the consumer that 063 names ("Flow … and the
  host own broader orchestration"). The Flow IR `bounded controller` (064) is the
  seed; Agent generalizes it into a durable, addressable, forkable entity. The
  Inquirium boundary is unchanged — see the new P064 note *Agent Loop Lives Above
  Inquirium*.
- **Flow IR (064) / workflow orchestration (033).** Complementary: Flow is a
  declarative DAG of steps; an Agent is a stateful controller with memory and a
  lifecycle that may compile and run Flows, and a Flow node may spawn an Agent.
- **Horizontal Protocol Primitives (081 / Solution 043).** Agent reuses
  `causal-context.v1` as a horizontal evidence contract. Observation resolution
  preserves the validated source context and adds a separate `resolution/ref`;
  this dependency carries causality, not Sensorium or provider semantics.
- **Sensorium (045) / Sensorium Interfaces (082/083).** Agent carries only opaque
  observation needs and generic effect proposals. A daemon-owned adapter may
  resolve them through Sensorium after checking the exact resource, grant,
  collaboration, lease, classification, and HIL contracts. Sensorium vocabulary
  and authority never enter `agent-core`.
- **Memarium (036).** Session context and lifecycle are durable facts; Agent adds
  no second memory store.
- **Capability Registry (072).** `agent.spawn/fork/suspend/resume/stop/status`
  are registered capability ids with fail-closed admission.
- **Assistant Channel (Solution 045).** The assistant Phase 3 agentic effects land here: the
  assistant stays advise-only/local-only baseline, and an operator may, with
  explicit capability and human-in-the-loop, drive an Agent from the assistant
  surface. The assistant is one operator-facing surface over Agent, not the Agent
  itself.
- **Corpus (069).** Corpus live deliberation drives an Agent as the host-owned
  reasoning **chair** bound to a Room (`agent.binding.v1`,
  `consumer/kind = collaborative-chair`); the chair Agent participates via Room membership
  attestation, and its answer-draft product feeds Corpus answer acceptance. Draft
  acceptance revalidates the original signed evidence and yields an inert,
  content-addressed Corpus projection with `publication/authorized = false`;
  publication remains a separate Corpus-owned transition. Corpus owns reasoning,
  chairing, and settlement semantics; the Agent owns the bounded session.
- **Enforced budget (064 `inq-cost-budget-enforcement`).** Agent budgets reuse the
  same metering and `BudgetExceeded` contract at agent and spawn-tree scope.

## Failure Modes and Guardrails

These are the agent-orchestration mistakes that recur in practice, with the
guardrail Agent adopts against each:

- **Fork bomb / resource exhaustion.** Budget is split (not duplicated) on fork;
  `max_depth`, `max_children`, `max_concurrent`, and `aggregate_budget` bound the
  whole tree.
- **Non-terminating loops.** `termination_condition` is mandatory; an agent
  without one is rejected. `max_steps`/`max_time` are hard watchdogs.
- **Privilege escalation via spawn.** Monotone narrowing on every axis; no
  self-authorization; the host is the only authority root.
- **Orphaned agents / leaked leases.** Lifecycle is durable facts; `stop` is
  authoritative and idempotent; a bounded scheduler reaper records terminal
  state for agents past TTL. Agent-owned leases are operation-bound, persisted,
  TTL-bounded, and released on completed effects, terminal state, reaping, or
  startup reconciliation. Deferred effects retain leases while work is live.
- **Cost blowup.** Enforced per-agent and per-tree budgets with typed
  `BudgetExceeded`; spend attributable in trace.
- **Unbounded context growth.** `MemoryPolicy` (pinned + bounded summary +
  recall) with token estimation gating each step.
- **Effects without accountability.** Effects are capability-gated proposals;
  sensitive classes are human-in-the-loop; every effect is an auditable fact.
- **Non-reproducible runs.** Each step records the resolved model snapshot,
  instruction hash, and controller decision, so a trajectory can be explained and
  replayed.

## Resolved Decisions

- Agent is a **separate organ above Inquirium**, not an Inquirium operation;
  Inquirium stays "not the agent loop".
- Authority is **host-owned**; agents never self-authorize and fork only narrows.
- Agent state is **durable facts** (Memarium), not mutated objects.
- The contract lives in a thin `agent-core` crate guarded by a dependency lint.
- `inquirium-core` is the sole explicit vertical dependency exception in
  `agent-core`: only its pure bounded-inference DTOs are reused. A positive
  direct-dependency allowlist prevents this exception from becoming precedent
  for another organ or runtime dependency.
- Agent observation and effect ports are **horizontal contracts**. Vertical-domain
  resolution, including Sensorium and Workbench, belongs to the daemon composition
  root; configuration may only select and narrow statically admitted wiring.
- The first controller runtime is **daemon-owned** and may use Flow IR for
  bounded sub-steps; Flow IR is not the lifecycle owner.
- The first runtime slice is **node-local only**; cross-node/federated agents are
  deferred to a separate proposal after the node-local lifecycle, budget, trace,
  and effect-proposal model is proven.
- The first live working set is an **in-memory / ephemeral projection**. Memarium
  remains the durable fact plane, not a cache; a dedicated projection cache can be
  evaluated later after real profiling data and clear lifecycle requirements.
- Production fan-out and budget profiles are **operator-defined**, not limited to
  a fixed preset catalog. The implementation still provides conservative,
  configurable developer defaults:
  `max_steps = 8`, `max_depth = 1`, `max_children = 0 or 1`,
  `max_concurrent = 1`, and a short deployment-configured wall-time TTL.

### Additional Decisions For Durable Runtime Slice

The first node-local slice is decision-complete. These choices govern the next
durable/runtime slice:

1. `agent.spawn`, `agent.status`, and `agent.stop` remain host-local lifecycle
   capabilities. Their Capability Registry shape stays
   `dispatchable=true`, `surfaces=["host-local"]`, and
   `passport/eligible=false`. Any future federated agent request surface requires
   a separate proposal and a distinct authorization model.
2. `budget_remaining` in `agent.status.response.v1` is derived only from
   daemon-owned metering records. Controllers, adapters, or models may report
   usage as evidence, but the daemon validates and records the spend before it
   affects status.
3. `agent/id` remains an opaque ref. Locality is enforced by storage, routing,
   and host registry boundaries rather than by embedding a node namespace into
   the identifier format.
4. Production Agent profiles are loaded from daemon/operator configuration.
   `agent-host` provides reusable DTOs, validation, and the conservative
   developer default; it must not gain compile-time production profile presets
   that move deployment policy into the functional core.
5. Durable recovery preserves an immutable admission snapshot: the admitted
   profile identity and canonical constraint snapshot travel with the session.
   Historical facts may be reconstructed under that snapshot, but resume, new
   inference, forks, and effects must also pass current operator policy. A
   session that no longer passes becomes quarantined and must not prevent
   unrelated daemon services from starting.
6. Quarantine follows authority lineage. If a recovered parent is quarantined,
   every descendant is quarantined even when its narrower spec would pass the
   current profile independently; a child cannot retain authority whose root no
   longer has current admission.
7. Rolling memory summaries are admitted only from explicit non-Agent component
   refs in the operator/distributor Agent host configuration and from modules
   whose registered execution profile carries explicit `inquirium.summarize`
   authority. The Capability Registry must positively admit that host-local
   capability. The effective set is the intersection of both sources; removing
   either authority quarantines affected recovered sessions rather than blocking
   unrelated daemon services.
8. Memarium lifecycle facts and the SQLite lease registry remain separate stores.
   Their cleanup contract is compensating and idempotent, not falsely atomic:
   terminal/expired state denies new lease admission, and startup reconciliation
   releases stragglers after interrupted stop or reaper passages.
9. Eligible rolling-summary producers are derived from registered JSON-e Flow
   module identities that explicitly request the positively admitted
   `inquirium.summarize` capability, then narrowed by
   `agent.host.summary_producer_refs`. Capability admission and module grant are
   necessary but not sufficient: the effective authority set is their
   intersection with operator/distributor configuration. Missing or removed
   authority fails closed during admission and current-policy reconciliation.
10. Inactive Agent-owned lease audit rows use a configurable retention horizon
    followed by audit-preserving compaction. The default horizon is 30 days after
    expiry or release. After that horizon, detailed rows are replaced by minimal
    tombstones retaining the lease and owner refs, scope digest, relevant
    operation/runtime refs, lifecycle timestamps, and terminal reason. Distributor
    and operator configuration may lengthen the horizon or disable compaction; no
    implicit hard deletion is allowed.

Deferred work that does not require a new decision is already tracked below:
cross-node/federated agents require a separate proposal; a dedicated projection
cache waits for profiling data and a clear lifecycle; and production fan-out/
budget profiles are operator-defined with the conservative developer defaults
above as the initial built-in profile.

## Open Questions

No open questions remain for the current node-local durable runtime scope. New
questions should be opened only when a later federated or cross-node slice requires
policy that cannot be derived from the frozen decisions above.

## Implementation Tracker

Status values: `todo`, `in-progress`, `done`, `deferred`.

| ID | Work item | Status | Done criteria / evidence |
| :--- | :--- | :--- | :--- |
| `agent-operational-context-framing` | Propagate source-owned operational impact into pre-inference Agent context without adding vertical vocabulary to `agent-core`. | `done` | `agent-core` carries only bounded generic qualifier refs and strict SHA-256 digests. The daemon resolver validates the complete current P082 read result, source generation, effective publication, schema, and digest before deriving those neutral qualifiers; stale, malformed, inconsistent, or superseded evidence fails closed without an Agent-owned TTL. The composition root computes a monotone local maximum across feeds, records host-owned provenance pairing each source class with its digest plus the local policy ref, floor, and selected class in both request metadata and the durable Inquirium trace, and supplies the versioned non-droppable P064 caution layer before feed-dependent inference. The trace receives that host projection directly rather than trusting caller metadata or provider output. Tests retain per-source evidence, prove order-independent maximum and provenance selection, and keep the at-most-512-byte source summary out of instructions and durable Agent payloads. |
| `agent-core-crate` | Create thin `agent-core` contract crate with Agent/controller/budget/grant DTOs and the lifecycle state machine. | `done` | `node/agent-core` compiles as a substrate-free contract crate: `AgentSpec`/`AgentParams`/`AgentBudget`/`ControllerPolicy`/`TerminationCondition`/`CapabilityGrant` DTOs with `deny_unknown_fields` and `validate()`, fail-closed classification ceiling, conservative developer defaults, `idempotency/key` on spawn, `agent.step-decision.v1`, `agent.spawn.response.v1`, `agent.status.request.v1`, `agent.status.response.v1`, `agent.stop.response.v1`, the `AgentLifecycleState::apply` state machine, and the `validate_fork_from` monotone-narrowing validator. Evidence: `cargo test -p orbiplex-node-agent-core`, `cargo clippy -p orbiplex-node-agent-core -- -D warnings`, and `python3 tools/check-agent-core-deps.py` pass. Runtime budget metering, fork budget split, and durable wiring are tracked separately below. |
| `agent-dep-direction-lint` | Add a dependency-direction lint so `agent-core` cannot import substrate or another vertical domain. | `done` | `node/tools/check-agent-core-deps.py` uses a positive direct-dependency allowlist, names pure `inquirium-core` DTOs as the sole vertical exception, rejects daemon/model-runtime/HTTP/async/SQLite and vertical-domain packages through `cargo tree`, and rejects Room, Corpus, Memarium, Sensorium, Workbench, and other source/effect vocabulary in the core source. It is wired into `.github/workflows/docs.yml`, and the current check passes. An `xtask`-level lint may later replace the standalone script. |
| `agent-inquirium-boundary-docs` | Document that the durable agent loop lives above Inquirium and that assistant agentic effects are realized through Agent. | `done` | Proposal 064 now has the *Agent Loop Lives Above Inquirium* boundary note, Proposal 066 Phase 3 points agentic effects at Proposal 073, and this proposal owns the lifecycle/controller/budget tracker. |
| `agent-lifecycle-capabilities` | Add `agent.spawn/fork/suspend/resume/stop/status` host capabilities. | `done` | All six node-local ids are active, host-local, non-passport-eligible capabilities with table-driven dispatch. Mutations write `agent.lifecycle-command.v1` plus state/session facts, preserve `local-control` or the authenticated module actor, replay exact idempotency keys after restart, and reject conflicting reuse. Module calls require bounded per-capability `agent_grants` and ownership of the Agent. A process-level smoke drives spawn/status, binding, passive and active controller passages, suspend/resume/controller-mediated fork/stop, kills the daemon without orderly shutdown, and confirms durable terminal-state recovery through real authenticated HTTP against Memarium. The current synchronous controller has no detached passage requiring a separate cancellation protocol. |
| `agent-monotone-fork` | Enforce monotone narrowing and budget split on `fork`. | `done` | `AgentSpec::validate_fork_from` prevents widened grants, classification, trust, model selection, controller bounds, and budget; daemon fork admission requires a running parent, reserves the child's budget from parent remaining budget, prevents the child deadline from exceeding the parent's remaining absolute TTL, records lineage durably, and rejects a second child under the default fan-out profile. Core and daemon negative/recovery tests pass. |
| `agent-bounded-fanout` | Enforce `max_steps/max_depth/max_children/max_concurrent/aggregate_budget` and mandatory `termination_condition`. | `done` | Core/profile admission enforces bounded steps, depth, children, live descendants, per-agent and aggregate budget ceilings, and a mandatory terminator; daemon fork admission enforces depth/direct-child/root-concurrency limits; operator profiles are loaded from daemon config; the TTL reaper is scheduler-owned; and the real controller shell meters explicit runtime ticks against step and wall-time bounds without polling `await-human`. Child spawn now runs through the active controller executor. Reservation reconciliation walks the recovered tree bottom-up: live children retain their bounded allocation (or actual spend on unbounded axes), terminal children retain only spend plus descendant commitments, and unused budget returns to the parent deterministically before status is projected. Tests cover fan-out/concurrency denial, active process-level child spawn, release on terminal state, and restart reconstruction. |
| `agent-durable-state` | Persist session context and lifecycle as Memarium-backed durable facts with replay/recovery. | `done` | The daemon persists validated `agent.session.v1`, `agent.state.v1`, `agent.lifecycle-command.v1`, initial step/trace, budget trace, effect, and outcome facts through a narrow `AgentFactStore` backed by Memarium Personal facts. The lifecycle command and completed controller step are commit markers; recovery repairs missing state/initial-step projections, initial effect outcomes, and content-addressed terminal outcomes after a partial bundle. Startup rebuilds the disposable projection and lifecycle idempotency ledger through bounded pages over the ordered stream, with a fail-closed startup budget of 100,000 facts or 256 MiB of canonicalized fact JSON; exceeding it requires administrative compaction or snapshot recovery rather than unbounded allocation. Recovery caches parsed deadlines and repairs only the latest missing state projection so a late historical repair cannot regress current state. Memarium generic fact queries provide the append-only `as of` source. With Memarium disabled, status explicitly reports ephemeral durability. |
| `agent-profile-recovery-policy` | Implement recovery when an admission profile is removed or tightened. | `done` | `agent.session.v1` carries a canonical-digest-bound immutable admission profile snapshot. Recovery is split into pure historical replay against that snapshot, an explicit repair phase, and current-policy reconciliation. Removed or tightened profiles produce a typed `current`/`quarantined` status projection without appending policy facts; quarantine cascades through descendants and denies resume, new inference charges, forks, effect proposals, admitted-effect lookup, and directive binding while status, stop, and unrelated daemon services remain available. Tests cover removed/tightened profiles, descendant cascade, digest mutation, no reconciliation writes, and isolation of a healthy session. |
| `agent-memory-projection` | Build the working set as a projection of durable Memarium facts via `MemoryPolicy`, with fail-closed degradation. | `done` | Every session receives an explicit default `agent.memory-policy.v1`; later revisions are immutable, contiguous, canonical-digest-bound facts and recovery rejects revision overflow. Each controller tick rebuilds a bounded in-memory projection through the shared Inquirium `MemoryPolicy` projector from pinned facts, an externally produced summary, and the recall allowlist. Agent-authored and unregistered-producer summaries fail closed at admission; removing a configured producer quarantines only affected recovered sessions. Projection text never enters prompt-free step traces, and only its evidence digest is attached to the step. Memarium-backed recovery restores the latest policy; disabled Memarium retains the existing explicit ephemeral, non-federating mode. Summary production remains another component's responsibility. |
| `agent-controller-step-records` | Persist each controller step as an auditable `agent.step.v1` fact. | `done` | Spawn and fork write a durable bootstrap `agent.step.v1`. The daemon consumes pure `agent-host` decisions through a bounded explicit-input controller loop, executes admitted `CallInquirium`, `ProposeEffect`, and `SpawnChild` actions through their owning host strata without holding the Agent lock, then records each result as `agent.step.v1` plus a prompt-free trace. Inquirium execution is constrained by the Agent classification ceiling, pinned profile, runtime allowlist, explicit capability grant, and Agent budget preflight; provider-reported final usage is charged idempotently to the same Agent before a successful controller response is accepted. Returned classifications are checked again before commit, and the execution evidence digest covers outcome, inference, effect, model, product, and classification refs. Every runtime tick consumes one step, conflicting concurrent passages fail closed, failed execution releases the ephemeral controller claim, passive/terminal actions stop the passage, and recovery repairs partial step/trace/terminal-state/outcome bundles. Unit tests cover grant admission, classification denial, and begin/commit exclusivity; the real process HTTP smoke exercises active child spawn and restart recovery after `agent.binding.create`. |
| `agent-effects-as-proposals` | Route effects through Sensorium/AD capability gates with human-in-loop for sensitive classes. | `done` | Immutable proposals and separate outcomes are durable. Admission checks running state, Agent grants, step freshness, classification, and review policy. A proposal may name the last committed step for replay or exactly the next uncommitted controller step; arbitrary future steps fail closed. Active controller decisions can create proposals but cannot execute them implicitly. Proposal refs have one global Agent owner, question refs use a direct projection index, and each outcome history follows a bounded host-validated transition sequence. The live projection fails closed at 64 proposals per Agent and 16,384 active proposal refs node-wide; exact proposal replay remains idempotent. HIL proposals project to the existing operator-question lifecycle; Confirm answers normalize boolean and registered `yes`/`no` values, timeout transitions are audited, and a process test proves that a module authtok cannot reach an `agent-effect-question:*` operator action. The generic `agent.effect.dispatch` bridge accepts only an exact admitted proposal, matching canonical payload digest and `effect/ref`, explicit module and binding target grants, active operation-bound leases, and a dispatchable target. `agent-host` compiles Sensorium Core and Artifact Delivery requests through a closed table-driven policy-adapter registry into transport-independent execution plans; unknown capabilities and Workbench requests fail closed. The daemon invokes only the plan's closed target, records durable execution-deferred/completed/failed outcomes with operation, result digest, and bounded lease refs, and returns exact terminal/deferred replays without reinvoking the target. A bounded scheduler reconciles Deferred Operation Registry status and releases leases on terminal completion. Golden, negative, transition, and restart-recovery tests cover the boundary. Workbench retains its stricter dedicated bridge. |
| `agent-budget-enforcement` | Reuse the enforced token/cost budget at agent and spawn-tree scope. | `done` | Inquirium charges carrying `agent/ref` are preflighted against host-owned spend plus reservations, replayed exactly, persisted as prompt-free traces, and rebuilt after restart. An admitted binding's monotone-narrowed budget is the effective limit for active and passive controller decisions, Inquirium and lease charges, child allocation, reservation reconciliation, status, and the absolute wall-time deadline; it never falls back to the wider session budget. Fork reserves rather than duplicates parent budget; terminal-child reconciliation returns unused slices while retaining actual subtree spend; root live-descendant caps are enforced; and runtime controller ticks charge one daemon-owned step. Every admitted Agent-owned lease is preflighted and charged once to the same durable cost ledger using the operator-configurable positive `agent.lease_cost_micros`; charge failure compensates by releasing the newly created lease. Tests cover narrowed Assistant binding enforcement, exact lease-charge replay, and reservation recovery. |
| `agent-step-trace` | Add prompt-free `agent.step-trace.v1` with model snapshot, instruction hash, and decision. | `done` | `agent.step-trace.v1` is a durable validated fact with decision, cumulative/delta budget, model/instruction slots, refs, predecessor, and timestamp; bootstrap, passive and active controller passages, and Inquirium budget-charge traces survive recovery without prompt/output content. Active executors attach inference/effect refs, canonical evidence digests, and the selected runtime/model-binding snapshot while keeping generated content outside the trace. |
| `agent-reaper` | Add a TTL reaper for orphaned/stale agents that releases leases. | `done` | A bounded Replay Scheduler job reaps expired non-terminal sessions in deterministic batches, writes idempotent `Reap` lifecycle/state facts, releases Agent-owned leases, and recovers terminal state after restart. Lease admission also checks the Agent wall-time deadline, and startup reconciliation releases stragglers owned by terminal or already-expired non-terminal Agents. Terminalization releases active proposal-owner and operator-question routing indexes, including after recovery, while durable Agent records still prevent historical `proposal/ref` reuse; a late answer to a reaped Agent's question is inert. Stop, controller-terminal, reaper, and startup-reconciliation paths share the durable lease registry; tests cover owner binding, exact replay after successful release, TTL expiry, stop, reaping, expired-running recovery, effect-index cleanup, and terminal recovery cleanup. |
| `agent-summary-producer-registry-authority` | Derive eligible summary producers from the Capability Registry and intersect them with the host configuration allowlist. | `done` | Daemon startup first requires positive host-local dispatch admission for `inquirium.summarize`, then derives eligible producer identities only from registered JSON-e Flow modules carrying that explicit inference grant. `agent.host.summary_producer_refs` can only narrow the set. `agent-host` admits the intersection; both source sets are capped at 256 stable refs of at most 256 bytes, config-only and module-only identities fail closed, Agent refs are invalid, and removal of either authority quarantines only affected recovered sessions. Unit and recovery tests cover intersection, malformed and oversized authority sets, absent registration, valid projection, and producer removal. |
| `agent-lease-audit-compaction` | Compact inactive Agent-owned lease rows after a configurable audit horizon. | `done` | The Replay Scheduler runs an independently configurable bounded compaction job. Expired/released Agent-owned details remain for at least the 30-day default horizon, then one SQLite transaction writes `inquirium.model-runtime.lease-audit-tombstone.v1` and removes the detailed row. Tombstones retain lease/owner/operation/runtime/model-binding identity, lifecycle timestamps, terminal reason, and a canonical digest of scope plus access; local lease GET resolves both details and tombstones. Distributor/operator configuration may lengthen retention or disable compaction. A durable scan cursor prevents old live operations from starving later rows, active rows are only normalized to expired in their first passage, non-terminal deferred-operation bindings fail closed as retained details, and stored lease JSON is rejected above 64 KiB before parsing. Tests cover bounds, live-deferred exclusion, active-row preservation, oversized stored rows, idempotent cursor cycling, and reopen durability. |
| `agent-assistant-surface` | Let the assistant (P066) drive an Agent under explicit capability and human-in-loop. | `done` | `inquirium.assistant.agent-escalation.proposal.v1` is an inert model control. `agent.assistant.escalate` requires explicit caller authority, records a durable host-authored escalation, and projects an expiring operator Confirm question. The terminal `Approved` fact is persisted before Agent or binding authority is materialized; its actor and timestamp come from the durable operator-question record through a typed internal authority. Recovery rejects a binding without matching approval and idempotently repairs an approved escalation interrupted after any partial spawn write. Denial and timeout remain terminal facts, and direct ambient binding is rejected. `agent.assistant.draft.accept` is local-control-only, bounded by the durable idempotency projection limit, emits prompt-free operational telemetry, and accepts only the latest content-addressed `agent.outcome.v1` for the same session and `assistant-response-draft` sink. It returns a validated render-only draft with `publication-authorized = false`. A real process smoke covers dirty restart with a pending question, exact replay, approval, denial, timeout, controller execution, outcome creation, explicit acceptance, and absence of generated content from status and notifications before acceptance; fault-injected unit coverage proves approval-first ordering and partial-materialization repair. |
| `agent-host-stratum` | Add an `agent-host` service stratum so the controller step decision is a pure value and the daemon performs effects. | `done` | `node/agent-host` computes `agent.step-decision.v1` as a pure value over `agent-core` contracts, exposes the conservative developer profile, contains no storage/HTTP/async/runtime substrate, and is guarded by `node/tools/check-agent-host-deps.py` in CI. Evidence: `cargo test -p orbiplex-node-agent-core -p orbiplex-node-agent-host`, `cargo clippy -p orbiplex-node-agent-host -- -D warnings`, and agent core/host dependency checks pass. The daemon executes actions in later tracker items. |
| `agent-binding-contract` | Add `agent.binding.v1` so consumers (Corpus chair, assistant, Flow node) drive an agent under narrowed grants. | `done` | `agent.binding.v1` and `agent.binding.create.{request,response}.v1` carry consumer identity, session source, output sink, monotone-narrowed grants and budget, bounded `MemoryPolicy`, optional Room participant/attestation refs, HIL policy, request digest, actor, and idempotency identity. FlowNode bindings remain module-owned or local-control. Assistant Channel bindings are node-local, same-session, strict-local, require a matching durable `Approved` escalation before admission and after replay, reject publication grants and incompatible sinks, and persist with their escalation and decision facts for restart recovery. Corpus-chair creation requires complete inline `room-membership-attestation.v1` evidence; the host verifies schema, signature, freshness, trusted local round authority, exact query/room/participant binding, `answer`/`moderate`/`speak` grants, and deadline, while the recovered binding stores only the content-addressed attestation ref. Every caller-delegated capability must cover both spawned-Agent and binding grants. The controller uses optimistic `expected-step`; a checked-in JSON-e Flow fixture demonstrates separate spawn/binding/controller grants and delegated target capability allowlists. |
| `agent-outcome-projection` | Publish a content-addressed terminal draft and bounded operator status projection without granting effect authority. | `done` | A completed bound Agent with a successful Inquirium product writes `agent.outcome.v1` to the durable fact stream. The generated response is canonicalized into the existing object store; the outcome carries only its content-addressed `product/ref`, classification, sink kind, binding, terminal state, budget, and prompt-free trace ref. The canonical outcome identity is revalidated during recovery, conflicting outcomes fail closed, and an interrupted append is repaired from the durable completed step. FlowNode consumes the draft through its own result path. Assistant Channel uses a separate durable same-session acceptance and receives a validated `assistant-response-draft` only after explicit local-control acceptance; Agent never renders or publishes it. Status exposes at most 64 metadata-only effect proposal projections plus a total count, while payloads and generated content remain outside the projection. |
| `agent-effect-proposal` | Add an immutable `agent.effect-proposal.v1` plus a separate `agent.effect-proposal-outcome.v1` fact joined by `proposal/ref`, with operator-question human-in-loop. | `done` | Core owns validated proposal/outcome and generic effect-dispatch DTOs; daemon persists them in Memarium, replays exact proposals, rejects conflicting bodies and cross-Agent proposal-ref reuse, caps and validates outcome transitions, projects deferred proposals to Confirm questions with fail-closed timeout defaults, joins validated boolean or registered `yes`/`no` answers as admitted/denied outcomes, audits timeout transitions, and binds each admitted proposal to exactly one `effect/ref`. The outcome vocabulary distinguishes policy deferral from execution deferral and records bounded operation/result/lease evidence through terminal completion or failure. Generic Sensorium and Artifact Delivery policy adapters and dispatch are implemented, active controller decisions can create proposals, `agent.status` exposes a bounded metadata-only operator projection, and recovery reconstructs deferred reconciliation candidates without target reinvocation. |
| `agent-corpus-chair` | Let Corpus (069) drive an Agent as the deliberation chair bound to a Room. | `done` | The Corpus adapter maps its chair into the horizontal `collaborative-chair` role with a `collaborative-answer-draft` sink, then consumes a signed and fresh `room-membership-attestation.v1`, verifies its canonical Ed25519 `did:key`, exact query/room/participant/grant/deadline binding, and rejects foreign, malformed, or expired evidence. The Corpus query must already exist, and the node-local first slice requires the signer to be its local round authority so an arbitrary self-signed credential is not admission authority. Recovery restores the durable binding without turning the discarded inline credential into ambient authority. A terminal `agent.outcome.v1` is accepted only by local control through a Corpus-owned idempotent contract into an inert answer draft; embedded evidence passes schema-gate again, exact replay remains bound to the original actor, conflicting replay fails closed, dirty restart restores both binding and draft, and no final Corpus answer is published without a separate authorized transition. A real process smoke covers unknown-query, untrusted-signer, foreign-room, expired-evidence, and unsigned-extension denial; exact and conflicting replay; two dirty restarts; bounded Inquirium controller execution; and absence of final publication. |
| `agent-corpus-participant` | Let a selected Corpus provider participate through an Agent without exposing a raw model runtime as a Room subject. | `done` | `agent.binding.v1` admits the horizontal `collaborative-participant` role only after the Corpus adapter validates the exact durable invite and signed, fresh Room evidence, with narrowed grants, budget, participant identity, and `collaborative-turn-draft` sink; participant mismatch is denied before binding. The `corpus.room.turn` host policy keeps `corpus-reasoning-turn-proposal.v1` inert until ordinary effect/HIL admission; proposal classification cannot exceed the Agent ceiling and the dispatched payload cannot change class. A host-owned Interaction Broker `room-event` watch wakes the chair without connector-local polling; live content is ephemeral, durable replay uses an explicit metadata allowlist, and an entropy-bearing source epoch invalidates old cursors after restart. Story-011 proves selected B expert → A chair execution, C remaining only a competing bidder, restart recovery of the exact accepted draft, exact dispatch replay, and no ambient publication. |
| `agent-observation-port-and-sensorium-adapter` | Admit one statically bound observation need as bounded context for an exact Agent passage, with Story 012 supplied by a daemon-owned Room/Sensorium resolver. | `done` | `agent-core` owns only generic `AgentObservationNeed`, `AgentObservationBinding`, and prompt-free evidence values; its only observation-evidence dependency is the horizontal P081 causal-context contract, while its positive dependency allowlist and vocabulary lint reject Room, Corpus, Memarium, Sensorium, Workbench, and other source/effect-domain coupling. Operator-authored JSON-e Flow configuration declares bounded static need-to-source mappings and imports the Agent-owned hard age, byte, reference, and item caps; rendered data may only select or narrow them, and dynamic interpolation of authority-significant refs fails closed. After caller-capability and ownership admission, the daemon proves that every exact source/schema pair has one resolver before persisting the durable binding; absent, incompatible, and ambiguous registrations fail closed with bounded pair-specific diagnostics. The resolver privately binds interface, Room, relay epoch, Room-membership source sequence, and recipient; admits one authenticated relay delivery, rechecks a fresh relay acknowledgement plus current Room invitation after the exact typed Agent-host Broker principal read, schema-gates and bounds the terminal-screen snapshot, and preserves the exact-schema/version-validated source `causal/context` alongside source-version and resolution refs in generic Agent trace. Step facts and traces require matching Agent, binding, and canonical passage identities for every attached observation evidence item. A conflicting digest at one relay epoch/sequence is a dedicated refusal with a payload-free structured diagnostic and cannot overwrite the admitted latest state. Broker durable replay is payload-free, restart drops observation content, and unbound or widened needs, Room membership alone, stale epochs or membership generations, ordered terminal replay, implicit summarization, and every actuation capability fail closed. The composed Story 012 runner reuses Story 011's three-node bootstrap, proves equal B/C operational-context qualifiers, revokes C and waits for relay-audience convergence before repair, dirty-restarts B, and proves immutable `test -> production` replacement, superseded-binding refusal, newer passing evidence for a new exact B binding while C remains refused, plus an unpublished chair output. Its closed 17-entry refusal matrix assigns every claim to direct composed-process evidence or a named P070/P082/P083 lower-stratum owner. |
| `agent-operator-status` | Expose a bounded, metadata-only operator projection over all node-local Agent sessions. | `done` | Operator-authenticated `GET /v1/operator/agents` provides stable exclusive-cursor pagination capped at 100 items. Each item reports lifecycle, durability, profile and current-policy admission, deadline, spent/remaining budget, latest step/outcome refs, pending effect/HIL counts, active leases, and controller claim without prompt or generated-product content. Unknown query parameters and invalid limits fail closed; module-authenticated requests cannot enter the operator route set. Unit tests cover ordering, pagination, caps, and metadata-only defaults. |
| `agent-doctor-maintenance` | Add inspect-first Agent doctor output and explicit bounded remediation. | `done` | `POST /v1/operator/agents/maintenance` accepts only `agent.maintenance.request.v1`, `dry_run|execute`, and a batch limit of 1..1000. Both modes consume one pure maintenance plan: dry-run returns projected counts and a projected `after` diagnostic snapshot without mutation, while execute applies that same plan. Current-policy reconciliation, canonical durable TTL reaping, and terminal lease release remain limited to the same lexicographically ordered page after the exclusive `after/agent-id` cursor; the response reports exact lease-registry release counts, never edits facts in place, and leaves deferred-effect reconciliation with its existing scheduler owner. Lease release remains durably owned by the model-runtime lease registry, while policy admission remains a restart-recomputed disposable projection over immutable Agent history. Missing lineage records produce `ancestor-absent`, distinct from an existing quarantined ancestor. Tests prove preview/apply parity, cursor-scoped durable reaping, invalid-bound denial, distinct lineage diagnostics, and stable terminal state. |
| `agent-runtime-diagnostics` | Publish bounded-cardinality Agent readiness and operational metrics. | `done` | Operator-authenticated `GET /v1/operator/agents/diagnostics` emits `agent.runtime-diagnostics.v1` with fixed lifecycle, quarantine, expired/reaper-backlog, pending effect/HIL, controller-claim, active-lease, recovery scan/repair, active-controller latency, and idempotency capacity counters. Degradation uses a closed stable reason-code set and no Agent id as a metric dimension. Recovery repair facts are counted only while replay repair is active; completed active controller passages record bounded aggregate latency. Targeted daemon tests and warning-clean clippy pass. |
| `agent-standalone-acceptance` | Provide an Agent-owned process acceptance pack independent of Assistant and Corpus drivers. | `done` | `node/tools/acceptance/agent-runtime/run.py` drives the real daemon with durable Memarium-backed Agent facts and the deterministic local Inquirium runtime. The authenticated HTTP slice covers spawn, binding, passive and active controller passages, inference, an inert Sensorium proposal, operator-question HIL admission, child fork/stop, content-addressed terminal outcome, operator list/diagnostics, forced `SIGKILL`, and recovered parent/child terminal states. Assistant Channel and Corpus are not lifecycle drivers. The runner emits `agent.acceptance-report.v1` and fails on the first unsuccessful check. |
| `agent-fault-soak` | Exercise partial writes, bounded capacity, restart recovery, and sustained short-session load. | `done` | A deterministic failpoint matrix interrupts each write boundary of the six-fact spawn bundle; session-first partial bundles repair through the canonical replay path and a first-write failure remains cleanly absent. The explicit acceptance soak creates and stops 1000 durable sessions, rebuilds them after restart, and proves all sessions terminal with zero live controller, effect-owner, HIL-routing, and pending-effect projections. Existing bounded fair deferred-effect and lease-compaction scheduler tests remain the owners of those reconciliation cursors; no timing threshold is used as a correctness oracle. |

## Next Actions

1. Keep future capability-specific effect policy adapters additive: register a
   pure validator and closed execution target only when a concrete consumer and
   owning host surface exist; never add a generic fallback.
2. Preserve the Assistant Channel boundary: escalation remains explicit and
   human-approved, draft acceptance remains render-only, and publication remains
   a separately admitted effect.
3. Keep the node-local operator list, diagnostics, maintenance, failpoint
   matrix, and standalone process/soak pack on the Agent release gate. A later
   cross-node or federated runtime must begin in a separate proposal and must
   not widen these host-local surfaces into network authority.
4. Preserve the horizontal observation/effect port: new vertical domains extend
   the daemon resolver/adapter registries and static wiring, never `agent-core`.
   Every binding remains operator-authored, schema-gated, digest-pinned, and
   represented by a prompt-free resolution reference while preserving the
   validated P081 causal context in trace.
5. Keep the shared Story 011/012 three-node bootstrap as the lower acceptance
   stratum. Story-specific runners may add domain fixtures and assertions, but
   must not fork federation-root, participant-binding, or restart semantics.

## Related Capability Data

- implemented capabilities: `agent.spawn`, `agent.fork`, `agent.suspend`,
  `agent.resume`, `agent.stop`, `agent.status`, `agent.effect.propose`,
  `agent.binding.create`, `agent.controller.run`, `agent.effect.dispatch`,
  `agent.assistant.escalate`, `agent.assistant.draft.accept`.
- host-local operator projections: `GET /v1/operator/agents`,
  `GET /v1/operator/agents/diagnostics`, and
  `POST /v1/operator/agents/maintenance`; these are operator-session surfaces,
  not module capabilities or federated protocol endpoints.
- schemas: `agent.spec.v1`, `agent.state.v1`, `agent.session.v1`,
  `agent.lifecycle-command.v1`, `agent.step.v1`, `agent.step-decision.v1`, `agent.spawn.request.v1`,
  `agent.spawn.response.v1`, `agent.fork.request.v1`, `agent.suspend.request.v1`,
  `agent.resume.request.v1`, `agent.stop.request.v1`, `agent.stop.response.v1`,
  `agent.status.request.v1`, `agent.status.response.v1`, `agent.step-trace.v1`,
  `agent.binding.v1`, `agent.binding.create.request.v1`,
  `agent.binding.create.response.v1`, `agent.controller.run.request.v1`,
  `agent.controller.run.response.v1`, `agent.memory-policy.v1`,
  `agent.effect-proposal.v1`, `agent.effect-proposal-outcome.v1`,
  `agent.effect.dispatch.request.v1`, `agent.effect.dispatch.response.v1`,
  `agent.outcome.v1`, `agent.assistant-escalation.request.v1`,
  `agent.assistant-escalation.v1`, `agent.assistant-escalation-decision.v1`,
  `agent.assistant-escalation.response.v1`,
  `agent.assistant-draft.accept.request.v1`,
  `agent.assistant-draft.acceptance.v1`,
  `agent.assistant-response-draft.v1`, `corpus-chair-admission.v1`,
  `corpus-agent-answer-draft.accept.request.v1`, and
  `corpus-agent-answer-draft.v1`.
