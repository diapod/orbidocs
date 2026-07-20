# Inquirium

Based on:

- `doc/project/40-proposals/063-inquirium-model-inquiry-organ.md`
- `doc/project/40-proposals/064-inquirium-implementation-recommendations.md`
- `doc/project/40-proposals/055-bounded-deferred-operation-contract.md`
- `doc/project/60-solutions/018-classification/018-classification.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md`
- `node:model-runtime/README.md`

Related schemas:

- `model-runtime-catalog.v0.2.2`
- `inquirium.generate.request.v1`
- `inquirium.generate.response.v1`
- `inquirium.generate.output-envelope.v1`
- `inquirium.embed.request.v1`
- `inquirium.embed.response.v1`
- `inquirium.batch-embed.request.v1`
- `inquirium.batch-embed.response.v1`
- `inquirium.classify.request.v1`
- `inquirium.classify.response.v1`
- `inquirium.rerank.request.v1`
- `inquirium.rerank.response.v1`
- `inquirium.summarize.request.v1`
- `inquirium.summarize.response.v1`
- `inquirium.transform.request.v1`
- `inquirium.transform.response.v1`
- `inquirium.image-generate.request.v1`
- `inquirium.image-edit.request.v1`
- `inquirium.image.response.v1`
- `inquirium.train-adapt.request.v1`
- `inquirium.adapter.manifest.v1`
- `inquirium.adapter.response.v1`
- `inquirium.effect-intent.v1`

## Status

Implemented MVP solution.

The bounded inquiry organ, host policy boundary, runtime-adapter substrate,
conformance gate, direct data-plane pilot, and first local and remote provider
paths are implemented. Additional provider families, richer evaluator profiles,
and production trainer backends are additive extensions.

## Date

2026-07-13

## Executive Summary

Inquirium is the Node organ for bounded model inquiry. It gives workflows one
provider-neutral capability surface for generation, embedding, classification,
reranking, summarization, transformation, image work, and bounded model
adaptation without exposing provider protocols or granting models authority.

The governing split is:

```text
consumer intent
  -> Inquirium semantic operation and host policy
  -> model-runtime candidate and adapter-instance execution
  -> typed result, denial, artifact, or deferred outcome
```

`model-runtime` is the execution substrate, not the workflow-facing organ.
Adapters translate concrete provider protocols and process mechanics. The host
retains model selection, classification, grants, budgets, prompt assembly,
conformance, leases, persistence, and effect authority. Model output is
candidate evidence and never authorizes its own effects.

## Context and Problem Statement

Model runtimes differ in transport, lifecycle, model naming, context limits,
sampling controls, modalities, cost, locality, and egress behavior. Letting each
workflow or provider adapter own these semantics would duplicate policy and
couple the system to accidental implementation details.

Inquirium creates a stable semantic boundary above those mechanics. Consumers
request an operation and constraints. The host selects a routable runtime,
assembles policy-owned context, invokes the corresponding adapter instance, and
normalizes the result. New model providers can therefore be added without
changing workflow contracts, while new semantic operations begin in
`inquirium-core` rather than as provider-specific endpoints.

## Proposed Model / Decision

### Architectural Strata

1. `inquirium-core` owns substrate-free operation and policy data contracts.
2. `inquirium-host` owns pure admission, selection, prompt, budget, output, and
   returned-value effect-intent decisions.
3. The daemon composition root owns authenticated dispatch, concrete stores,
   supervision, transport invocation, leases, traces, and effect execution.
4. `model-runtime` owns runtime catalogs, adapter instances, lifecycle,
   capabilities, health, and conformance evidence.
5. Runtime adapters translate between neutral Inquirium requests and one model
   execution interface. They hold no ambient Orbiplex authority.

One adapter implementation may serve many configured adapter instances, and
one adapter instance may serve many model bindings and runtime candidates.
Selection is by `runtime/ref`; transport lifecycle is by
`adapter.instance/ref`; provider-facing model names belong to model bindings.

### Authority Boundary

Local control or an explicit inference grant is required before invocation.
`allowed_calls` is shape admission, not authority. Missing classification,
runtime support, conformance, grant, model binding, prompt content, lease, or
output-policy evidence fails closed.

Model-returned control values and plans are inert proposals. The host validates
and may forward them to an owning component, but Inquirium does not execute
tools, mutate relationships, publish artifacts, or run an agent loop merely
because a model requested it.

## Must Implement

### Semantic Operation Contracts

Responsibilities:

- expose operation-specific request and response contracts rather than one
  loose provider-shaped envelope;
- validate bounded inputs, outputs, parameters, classifications, and refs at
  the Inquirium boundary;
- keep provider-specific model names and controls in host-owned bindings;
- represent denial, degradation, invalid output, unsafe output, deferred work,
  and artifact output as typed values.

Status: `done`.

### Runtime Selection And Adapter Execution

Responsibilities:

- select only healthy, routable, policy-compatible runtime candidates;
- separate adapter implementation, adapter instance, model binding, runtime
  candidate, and runtime instance identities;
- supervise local adapter processes by adapter instance while routing semantic
  invocations by runtime candidate;
- require signed adapter manifests and explicit operator authorization for
  egress-capable adapters;
- support local deterministic, local HTTP, and supervised remote provider
  paths without making a transport shape part of operation semantics.

Status: `done`.

### Prompt, Context, And Output Policy

Responsibilities:

- assemble host-owned prompt layers monotonically across HostRoot, organ,
  operation, profile, model binding, and adapter instance;
- keep response locale independent from instruction locale;
- project bounded session memory from immutable facts while leaving summary
  production to another configured component or workflow;
- negotiate structured output with adapters while retaining host validation;
- enforce input/output rails, classification-aware egress, bounded repair, and
  a closed inert communication-control vocabulary.

Status: `done`.

### Conformance And Operator Visibility

Responsibilities:

- persist host-owned conformance reports bound to the current canonical fixture
  digest and optional profile/host-class scope;
- keep candidates non-routable when required passing evidence is absent, stale,
  or failing;
- expose healthy and routable as separate operator-visible states;
- emit metadata-only, host-keyed traces without prompt, model output, vectors,
  image bytes, or protected context.

Status: `done`.

### Direct Data Plane And Artifact Outputs

Responsibilities:

- issue bounded, expiring, operation- and runtime-bound leases for artifact,
  object-store, query, and allowlisted local-file scopes;
- deny raw file leases to remote runtimes and validate canonical path
  containment fail-closed;
- use bounded deferred operations for long-running batch embedding and model
  adaptation;
- verify output digest and size before object-store publication and preserve
  lease, runtime, model-binding, and operation provenance.

Status: `done`.

### Budgets, Caching, And Effect Intents

Responsibilities:

- enforce token and cost budgets before and after provider work;
- make retries and structured-output repair visible to accounting;
- allow opt-in deterministic response caching only when stable model and policy
  snapshots are part of the key;
- return typed trace, transcript, budget-charge, and artifact-output intents to
  the daemon rather than performing hidden writes inside the policy stratum;
- compile model-authored candidate plans into inert, grant-checked Inquiry Flow
  values without scheduling them.

Status: `done`.

## May Implement

### Additional Runtime And Evaluator Profiles

Provider families, deterministic operation-specific caches, grammar/native
schema profiles, and signed evaluator critics may be added when they preserve
the same host authority and conformance boundary.

Status: `post-mvp`.

### Production Model Adaptation Backends

Concrete trainers may replace the deterministic reference behavior behind the
existing `train.adapt` admission, deferred execution, evaluation, and artifact
publication contract. A trainer does not receive publication authority.

Status: `post-mvp`.

### Operational Caution From Enacted Sources

P064 implements a post-MVP host prompt layer derived from daemon-validated P082
operational-context evidence. The mapping from the closed impact class to caution
text is deterministic, versioned, and non-droppable for feed-dependent passages;
publisher-authored summary text remains inert context. This adds neither an
Inquirium adapter field nor model authority, and missing or inconsistent context
fails collaborative-live invocation closed. Staleness is decided only by P082's
current source-generation and effective-publication predicate; Inquirium introduces
no context TTL. The optional summary is capped by P082 at 512 UTF-8 bytes before it
reaches prompt shaping.

Golden tests pin layer ordering and the instruction hash, while refusal and
monotonicity tests prove that local floors and multiple feeds cannot drop a
`production` or `critical` caution. The publisher summary is never interpolated into
the host-authored layer. Host-owned request metadata and the durable Inquirium trace
carry deterministic selection provenance: local policy ref, local floor, selected
class, and every source class paired with its exact operational-context digest. The
composition root passes that bounded trace projection directly instead of deriving it
from caller metadata or provider output. An audit can therefore distinguish a source
declaration from a stricter local elevation.

Status: `done post-mvp`.

## Trade-offs

The extra semantic layer adds explicit DTOs, manifests, catalog references, and
host validation. In return, workflows remain provider-neutral, policy stays
auditable, and local or remote models can be substituted without moving
authority into adapters. Some provider features arrive later because they must
first obtain a neutral contract and a fail-closed host path.

## Failure Modes And Mitigations

- **Unknown runtime or binding:** deny rather than selecting an ambient default.
- **New transport bypasses local-only policy:** use positive transport
  allowlists so unknown variants fail closed.
- **Adapter claims its own conformance:** accept only daemon-run, fixture-bound
  reports.
- **Caller overrides provider model identity:** reject host-owned binding-key
  overrides.
- **Prompt or output policy cannot be applied:** stop before egress or suppress
  release with a typed terminal result.
- **Lease escapes its scope:** canonicalize, bind, expire, and reject raw remote
  file access.
- **Cache corruption or stale affinity:** validate the cached result and fall
  back to a real invocation without weakening authority.
- **Model proposes an effect:** keep the proposal inert and hand it to the
  owning capability boundary only after independent admission.

## Open Questions

No unresolved question blocks the implemented MVP solution. New operation
families, evaluator authority, or provider-specific extensions require their
own proposal or an explicit revision of the implementation recommendations.

## Next Actions

1. Preserve the dependency-direction and conformance gates as new operations
   and adapters are added.
2. Productize local model provisioning according to Proposal 066 Decision 8.5.1
   and its post-MVP tracker, without changing the semantic contracts; concrete
   trainer deployments remain a separate product integration.
3. Implement durable agent loops in the Agent organ rather than extending
   Inquirium into an orchestration authority.

## Out Of Scope

- owning durable agent lifecycle or autonomous control loops;
- granting model-returned tool calls or plans effect authority;
- replacing Sensorium, Artifact Delivery, Memarium, Scheduler, or Agent;
- using provider sessions or caches as authoritative Orbiplex memory;
- making one provider API or implementation language the semantic contract.

## Consumes

- authenticated host capability calls and inference grants;
- runtime catalog, model binding, adapter manifest, and conformance data;
- classified context and host-owned prompt policy;
- leases, artifact refs, query refs, and budget state.

## Produces

- typed operation responses and denials;
- verified artifact descriptors and deferred-operation refs;
- metadata-only trace and accounting intents;
- inert control proposals and compiled Inquiry Flow values.

## Related Capability Data

- `044-inquirium-caps.edn`

## Implementation Recommendations

The implementation-specific contract, invariants, tracker, and extension rules
remain in
`doc/project/40-proposals/064-inquirium-implementation-recommendations.md`.
That document refines this solution; it does not define a separate component.
