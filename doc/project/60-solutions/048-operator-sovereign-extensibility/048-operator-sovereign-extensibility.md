# Operator-Sovereign Extensibility

Based on:

- `doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`
- `doc/project/40-proposals/049-json-e-middleware-transformer-executor.md`
- `doc/project/40-proposals/069-corpus.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/40-proposals/081-horizontal-protocol-primitives.md`
- `doc/project/60-solutions/015-host-owned-module-store/015-host-owned-module-store.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`
- `doc/project/60-solutions/038-corpus/038-corpus.md`
- `doc/project/60-solutions/044-inquirium/044-inquirium.md`
- `doc/project/60-solutions/047-agent/047-agent.md`

Related schemas:

- `limit-classification.v1`
- `enum-classification.v1`
- `dispatch-classification.v1`
- `inquirium-resource-profile.v1`
- `inquirium-federated-resource-profile.v1`
- `operator-resource-envelope.v1`
- `operator-resource-envelope-revocation.v1`
- `nse-hook-offer.v1`
- `nse-hook-decision.v1`
- `nse-policy-table.v1`
- `nse-select-turn-order-table.v1`
- `nse-middleware-evidence.v1`
- `daemon.nse-offer-resolution-trace.v1`
- `operator-experiment-package.v1`
- `operator-extension-activation.v1`
- `operator-extension-session-activation.v1`
- `operator-extension-session-deactivation.v1`
- `operator-extension-revocation.v1`
- `operator-extension-transition.v1`
- `operator-extension-conformance-report.v1`
- `operator-extension-refusal-code.v1`
- `operator-extension-refusal.v1`
- `operator-extension-inspection.v1`
- `operator-effective-policy-inspection-input.v1`
- `operator-effective-policy-inspection.v1`
- `operator-extension-loose-import.v1`
- `operator-extension-import-receipt.v1`
- `operator-extension-conformance-run.v1`
- `operator-extension-conformance-run-result.v1`
- `operator-extension-safe-mode-action.v1`
- `capability-derived.v1`
- `operator-guard-hook.v1`
- `operator-attention-budget.v1`
- `semantic-registry-binding.v1`
- `semantic-registry-inspection.v1`
- `dator-dispatch-entry.v1`
- `corpus-semantic-entry.v1`
- `arca-strategy-entry.v1`
- `agent-semantic-entry.v1`
- `inquirium-operation-descriptor.v1`
- `federated-envelope-declaration.v2`
- `node-extension-posture.v1`
- `node-extension-federation-publication.v1`
- `node-extension-posture-evaluation.v1`
- `corpus-reasoning-room-policy.v3`
- `corpus-reasoning-inference-flow-binding.v1`
- `agent.inference-flow-binding.v1`
- `agent.inference-flow-inspection.v1`
- `agent.inference-passage-input.v1`
- `agent.inference-passage-product.v1`
- `agent.inference-passage-trace.v1`
- `agent.inference-terminal-selection.v1`
- `corpus-turn-order-offer.v1`
- `corpus-turn-order-decision.v1`

## Status

Implemented post-MVP solution.

The V1 authority model, package lifecycle, resource envelopes, Natural Selection
Engine (NSE) policy hooks, semantic registries, derived capabilities, guard hooks,
attention policy, inspection surfaces, federation posture, and packaged Agent and
Corpus vertical are implemented and refusal-tested. The optional WASM NSE backend
is deliberately outside this solution and is specified by Proposal 087.

## Date

2026-08-23

## Executive Summary

Operator-Sovereign Extensibility is the Node stratum through which a node operator
may install, activate, inspect, narrow, and revoke local policy extensions without
creating a second source of authority.

Many producers may propose a typed decision. Exactly one host-owned validator for
the owning hook decides whether the proposal is contained by the exact offer and
current authority. Executability, signatures, package installation, and successful
conformance are necessary evidence; none of them authorizes an effect by itself.

```text
operator intent and signed package
  -> inert installation and conformance
  -> signed activation under the current operator binding
  -> host-built offer and current authority snapshot
  -> table, Rhai, or supervised evidence producer
  -> hook-owned admission and ordinary domain validation
  -> bounded decision, refusal, or inert proposal
```

The solution is cross-cutting. It does not replace Inquirium, Corpus, Agent,
Capability Registry, Middleware, or JSON-e Flow. Each of those components keeps
its own semantics and authority. This solution supplies shared lifecycle,
selection, narrowing, inspection, and invalidation mechanics beneath their owning
boundaries.

## Context and Problem Statement

Orbiplex needs to let operators change operational policy without recompiling the
Node for every experiment. That freedom is useful only when it does not turn a
policy file, script, middleware process, or package into ambient authority.

Before this solution, the repository contained several local policy mechanisms:
compile-time Inquirium limits, Rhai-backed NSE hooks, JSON-e orchestration,
middleware packages, domain-specific registries, and operator configuration. They
were individually useful but did not share one explicit answer to these questions:

- which limits may be changed and which remain pre-policy safety boundaries;
- how extension bytes become installed, conformant, active, revoked, and recovered;
- how several decision producers compose without admitting their own output;
- how current grants, conformance, trust, sanctions, and generations fence every
  use;
- how an operator inspects the effective result without exposing prompts, model
  output, secrets, or protected payloads;
- how a peer proves extension posture without gaining access to local policy or a
  fallback implementation.

The implemented architecture answers these questions with values, append-only
facts, monotonic intersections, and one admission boundary per semantic owner.

## Proposed Model / Decision

### Authority Does Not Follow Executability

An extension package is inert after installation. Activation requires current
operator authority, exact package identity, host compatibility, passing
conformance, and a signed activation plan. Every use rechecks the current package,
operator binding, activation generation, conformance report, safe-mode state,
revocation state, dependencies, grants, and domain authority.

No extension may:

- mint a primitive capability;
- widen a host-built offer;
- lower a risk floor;
- invent a Room, Corpus, Agent, Inquirium, or Sensorium transition;
- convert evidence into an effect;
- survive revocation through a cached or replayed binding;
- substitute a local implementation for a missing federated requirement.

### Limit Classes and Resource Envelopes

The limit-classification registry separates:

- normative invariants;
- boundary-safety limits enforced before policy;
- federated compatibility limits;
- operator-configurable operational limits;
- temporary unclassified limits with explicit review deadlines.

Inquirium exposes a closed 38-axis operational resource profile. Distributor
ranges define where signed envelopes may widen defaults. Unsigned local
configuration and task/session overlays remain tighten-only. Several active
envelopes intersect; lower maxima and higher minima win. Current-use permits bind
the exact profile and envelope digests and revalidate them when materialized.

### Natural Selection Engine

NSE separates three values:

1. a host-built offer containing the complete admitted decision space;
2. an untrusted producer proposal;
3. a typed decision created only by the shared hook-owned validator.

V1 implements deterministic table policy, a bounded Rhai backend, and supervised
middleware evidence. JSON-e Flow may consume an opaque admitted decision ref, but
does not execute a policy backend or construct a decision. All producers are
budgeted before execution, and required producer failure is a refusal rather than
an implicit defer.

The closed hook family covers Inquirium model and output policy, Corpus ordering,
bid, tie, and participant policy, and Agent step, fan-out, and effect-risk policy.
Each hook can only select, order, narrow, restrict, raise risk, or choose from
host-registered transforms according to its contract.

### Package Lifecycle

The daemon owns one lifecycle for executable and semantic package material:

```text
bytes staged
  -> digest and signature verified
  -> inert package committed
  -> package-specific conformance recorded
  -> durable or expiring session activation
  -> current-use validation
  -> rollback, revocation, expiry, or safe-mode deactivation
```

Installation and activation are separate transactions. Resumable staging is
bounded, verified bytes commit atomically, and failed staging is discarded. The
host, not package content, pins the conformance runner executable, working
directory, arguments, timeout, output bound, and digest. Durable activation and
revocation are signed; session activation is local, bounded, and deliberately does
not survive restart.

Safe mode is a live-operator-only path that can deactivate packages and sessions,
restore defaults, and rebuild projections without invoking package code or NSE.
Lifecycle facts and authority mutations commit together, and terminal revocation
cannot be undone by rollback.

### Semantic Registries

The shared semantic-registry core provides:

- explicit distribution, federation, policy, operator, and request ceilings;
- monotonic set intersection with no default entry fallback;
- required revision, digest, implementation, and generation fencing for replay;
- immediate invalidation after capability, trust, sanction, conformance, package,
  or generation change;
- bounded prompt-free inspection and refusal diagnostics.

Dator, Corpus, Arca, Agent, and Inquirium own their domain entries. Shared registry
mechanics do not flatten domain meaning into one universal enum. Operator packages
may bind exact semantic entries; they cannot define a new domain operation merely
by naming one.

### Derived Capabilities and Guard Hooks

A derived capability is an intersection of current primitive capabilities and
restrictions. It is never registered as a new primitive capability, advertised to
peers, or accepted as a substitute for a missing base grant.

Guard hooks attach monotonic restrictions to a closed set of host admission
anchors. They may restrict grant sets, narrow bounded budgets, or raise risk. The
ordinary owning validator still runs. Missing authority, invalid guard semantics,
stale package state, or an empty effective grant set refuses use.

### Operator Attention

Signed attention budgets make operator focus an explicit bounded resource.
Availability windows, rolling prompt and group caps, repeat suppression, quiet
windows, and overflow policy may defer or deny ordinary questions. A separate
security lane never auto-approves. Equivalent questions retain independent facts
while sharing a host-derived semantic group identity that caller wording,
idempotency keys, and per-attempt refs cannot fragment.

### Federation Posture

A node publishes a signed projection of the exact extension registry posture it is
willing to disclose. Peer evaluation requires exact agreement on the complete
required entry set: every required ref, revision, implementation, and digest must
match current local policy. Missing, modified, revoked, substituted, or untrusted
entries refuse the federated operation. There is no fallback to a similarly named
local implementation.

Corpus Room policy V3 binds the exact publication and registry requirement set into
signed invitations. Federated Inquirium use additionally binds the authenticated
peer, posture, envelope and profile digests, operation registry entry, runtime,
operation, and host-selected experiment class at admission and use.

### Agent and Corpus Experiment Flow

The implemented multi-pass vertical lets an operator package provide a bounded
Agent inference Flow and a Corpus turn-order producer. Corpus owns Room membership,
role, overlay, policy-generation, visibility, classification, and expiry authority.
Agent owns passage lifecycle, budget, product lineage, and terminal selection.
Inquirium owns prompt framing, runtime admission, inference, and usage evidence.

Room prose remains inert. A passage input, product, trace, and terminal-selection
fact are separate values. Current Corpus authority is revalidated at passage
admission, invocation, product commit, and terminal selection. Products remain
unpublished until the owning consumer performs its own transition.

## Persistent Facts and Projections

The durable source of truth is append-only lifecycle, authority, refusal, decision,
and passage evidence. Rebuildable projections provide bounded operational reads.
The principal projections are:

- installed, conformant, active, session-active, revoked, and safe-mode package
  state;
- effective resource envelopes with per-axis provenance;
- current semantic registry entries and generation fences;
- current derived capability and guard decisions;
- rolling operator-attention usage;
- signed local and federated posture;
- effective-policy inspection, explanation, and graph views;
- Agent Flow and Corpus-bound passage state.

Projection reads never repair authority implicitly. Startup reconciliation either
rebuilds recognized state, retires stale generations, or marks a source unavailable.
An unavailable owner is not rendered as an empty permissive policy.

## Inspection and Diagnostics

The operator surface is intentionally prompt-free. It exposes refs, digests,
generations, status, bounded counts, decisive restrictions, source attribution,
nearest expiry, cache/store occupancy, and typed refusal provenance. It does not
return prompts, private reasoning, model output, signatures, secrets, or protected
artifact bytes.

The default view foregrounds material `requested -> effective` differences rather
than dumping every axis and registry entry. `inspect`, `explain`, and bounded
Mermaid `graph` views are projections of the same accepted value and must identify
the same deciding fact.

## Concrete Sequence

```text
operator signs package and activation plan
  -> daemon imports package as inert bytes
  -> host-owned conformance runner records an exact report
  -> lifecycle service commits activation generation
  -> domain host builds an offer from current authority
  -> configured producers return proposals or bounded evidence
  -> shared hook validator admits or refuses
  -> owning domain validator performs the ordinary transition
  -> prompt-free decision and lifecycle facts are retained
  -> revocation or policy change invalidates later use immediately
```

For a packaged Corpus/Agent run:

```text
package activation
  -> package Flow and turn-order producer become current
  -> Corpus builds the eligible-participant offer
  -> NSE returns contained order
  -> Agent admits bounded passages under current Corpus authority
  -> Inquirium produces content-addressed products
  -> Corpus or another consumer explicitly selects and publishes
  -> restart fences stale process authority
  -> package revocation refuses Flow and producer reuse
```

## Trade-offs

- The architecture has more explicit facts, digests, and generations than a
  conventional plugin API. That cost buys deterministic refusal, replay safety,
  and operator-visible causality.
- Exact federation agreement is less available than best-effort intersection. It
  prevents silent semantic substitution and makes incompatibility explicit.
- Current-use revalidation adds bounded read cost. Immutable projections and
  content-addressed identities keep the hot path predictable.
- A closed decision vocabulary evolves more slowly than arbitrary scripts. It also
  keeps decisions reviewable and prevents scripts from becoming hidden effects.
- Session activation is useful for experiments but is intentionally discarded on
  restart. Durable behavior requires the full signed lifecycle.

## Failure Modes and Mitigations

| Failure mode | Mitigation |
| :--- | :--- |
| Package bytes change after review | Content-addressed staging, exact package digest, pinned conformance inputs, and current-use identity checks. |
| A producer returns a wider or malformed decision | Shared hook validator refuses before the owning domain transition. |
| Cached authority survives revocation | Generation, package, conformance, grant, and operator-binding fences are checked on use. |
| One producer times out or fails | Required producer failure is typed refusal; advisory omission is explicit and bounded. |
| A package attempts to invent a capability | Derived sets only intersect registered primitive capabilities; no new dispatch identity is created. |
| An operator is flooded with equivalent questions | Host-derived semantic grouping, rolling caps, quiet windows, and bounded durable accounting. |
| A peer advertises a compatible-looking substitute | Exact required-entry agreement and signed posture; no name-based fallback. |
| Restart interrupts activation or a passage | Append-only facts, transactional authority mutations, generation journaling, and bounded recovery. |
| Inspection source is absent | Explicit `unavailable` source status rather than a permissive empty projection. |
| Extension behavior becomes unsafe | Live-operator safe mode deactivates authority without invoking extension code. |

## Security and Privacy

- Package signature is provenance, not effect authority.
- Conformance is evidence for one exact package and runner profile, not a permanent
  trust grant.
- Policy decisions are offer-contained and then revalidated by the owning domain.
- Loose-file import is disabled by default, root-confined, signed, and inert.
- Executable conformance inputs are host-owned, permission checked, and digest
  pinned.
- Federation discloses a bounded posture projection, not local policy contents.
- Traces and operator views are metadata-only and prompt-free.
- Safe mode and non-delegable operations require fresh local-control authority.
- Package revocation, trust loss, sanction, conformance loss, generation change,
  and grant loss fail closed.

## Acceptance Evidence

The solution is supported by unit, property, schema, dependency-direction,
process-level, multi-daemon, and hardware-VM evidence. The principal retained
vertical is the 2026-08-23 Story 012 macOS arm64 report. Its closed 31-check
validator proves:

- activation of the exact operator package before deliberation;
- use of the package-owned four-passage Flow and turn-order producer;
- separate solver and reviewer execution through real local model runtimes;
- content-addressed CandidatePlan and terminal-product lineage;
- ordinary HIL and Sensorium Interactive Interfaces claim/invoke/release;
- restart retirement of stale Flow and producer process authority;
- terminal package revocation and stale-authority refusal without fallback;
- no effect derived directly from Room prose;
- bounded prompt-free authority and product evidence.

Cross-domain tests cover Dator, Corpus, Arca, Agent, and Inquirium semantic
registries. A three-daemon suite covers signed posture publication, peer-side exact
agreement, modified-posture refusal, federation binding, restart, revocation, and
absence of local substitution.

## Open Questions

No V1 questions remain open. Portable WASM decision production is intentionally
specified and tracked by Proposal 087; it is not required for this solution's
implemented status.

## Next Actions

1. Preserve the closed refusal vocabularies, schema-family completeness gates,
   semantic-inventory checks, and dependency-direction guards as blocking CI.
2. Preserve the packaged Story 012 report as the combined package, Flow, Corpus,
   Agent, Inquirium, restart, and revocation regression boundary.
3. Keep effective-policy inspection cognitively bounded as additional domains and
   extension sources are added.
4. Implement Proposal 087 only through the existing offer, lifecycle, conformance,
   and hook-owned admission boundaries.

## Must Implement

- host-owned inert package installation, conformance, activation, rollback,
  revocation, session expiry, safe mode, and recovery;
- typed NSE offers, untrusted proposals, and hook-owned admitted decisions;
- monotonic resource envelopes, derived capabilities, guard hooks, and semantic
  registries;
- current-use fencing for operator, grant, conformance, generation, trust,
  sanction, posture, and package state;
- bounded prompt-free inspection and refusal diagnostics;
- exact federated posture agreement without semantic fallback;
- packaged Agent and Corpus multi-pass orchestration under ordinary domain
  authority.

All items above are implemented.

## May Implement

- additional closed policy hooks whose owning domain and admission validator are
  explicit;
- additional deterministic table predicates and host-registered transform
  profiles;
- new domain semantic registries built on the shared mechanics;
- additional supervised evidence producers;
- the WASM backend specified by Proposal 087.

## Out of Scope

- arbitrary plugin-defined capabilities or host calls;
- package-owned admission, publication, Room, Agent, Inquirium, or Sensorium
  authority;
- implicit package discovery, installation, activation, or fallback;
- general-purpose WASI, ambient filesystem, network, clock, randomness, process,
  thread, or device access for decision modules;
- unbounded operator views or prompt-bearing audit traces;
- interpreting peer posture as trust in arbitrary peer policy.

## Consumes

- fresh node-operator bindings and local-control authority;
- signed package, envelope, policy, and posture values;
- Capability Registry primitive eligibility;
- current grants, trust, sanctions, conformance, lifecycle, and domain facts;
- domain-owned offers from Inquirium, Corpus, Agent, Dator, and Arca;
- host-owned clocks, stores, runners, and bounded execution substrates.

## Produces

- inert installed package and conformance state;
- generation-fenced durable or session activation authority;
- admitted NSE decisions or typed refusals;
- effective resource profiles and semantic registry selections;
- derived capability and monotonic guard decisions;
- bounded operator-attention projections;
- signed local and federated extension posture;
- prompt-free effective-policy, explanation, graph, and authority traces;
- packaged Agent Flow and Corpus turn-order evidence.

## Related Capability Data

The machine-readable capability projection is maintained in:

- `doc/project/60-solutions/048-operator-sovereign-extensibility/048-operator-sovereign-extensibility-caps.edn`

## Implementation Recommendations

The complete rationale, resolved decisions, implementation guidance, phased
tracker, refusal criteria, and detailed evidence remain in Proposal 085. Treat that
proposal as the implementation record for this solution. New extension mechanisms
must add a typed contract and owning admission boundary rather than weakening a
V1 invariant or adding a hidden fallback.
