# JSON-e and JSON-e Flows FAQ

## What problem do JSON-e and JSON-e Flow solve?

They cover the space between hard-coded host behavior and a general-purpose
middleware process. JSON-e turns an explicitly projected JSON context into another
JSON value. JSON-e Flow adds a small, static sequence of host-interpreted steps around
that transformation. Together they let an operator or middleware package author build
inspectable adapters without introducing another process, port, private API, or
ambient scripting runtime.

The canonical design is [Proposal 049](../../project/40-proposals/049-json-e-middleware-transformer-executor.md).
For configuration and runnable examples, see the [JSON-e and JSON-e Flows
HOWTO](../howto/json-e-and-json-e-flows-howto.en.md).

## What is the difference between JSON-e and JSON-e Flow?

`json_e` is a pure data transformer:

```text
projected context -> JSON-e template -> schema-gated JSON value
```

`json_e_flow` is a bounded host-owned passage:

```text
projected context -> render/validate/call/extract/... -> response
```

JSON-e evaluates templates. The flow runtime interprets a static list of steps and
owns every effect. A template cannot turn itself into a flow by rendering a capability
name or a new step.

## Where do they sit in the architecture?

They are middleware executor classes in the [Middleware
solution](../../project/60-solutions/019-middleware/019-middleware.md). A concrete
configuration is still a first-class middleware component: it has its own ids,
bindings, limits, trace identity, package provenance, and operator lifecycle.

They do not replace domain organs. Inquirium still owns model inquiry, Sensorium owns
enaction and signals, Memarium owns facts, Artifact Delivery owns delivery, and Agent
owns agent lifecycle. JSON-e may shape values for those boundaries; JSON-e Flow may
cross them only through admitted host capabilities.

The implementation currently has one operational asymmetry: `middleware-runtime`
implements both executors, while the daemon directly registers operator-configured
providers only through `middleware_json_e_flow_services`. A pure transformation can
be embedded through the runtime executor; to deploy equivalent behavior as a daemon
provider today, use an effect-free flow with `render`, `validate`, and `respond`.

## Does a JSON-e template have authority?

No. It sees only fields selected by the operator-owned `context_projection`, plus the
explicitly exposed helper functions. It cannot read files, open sockets, spawn a
process, mutate storage, inspect daemon internals, or invoke a capability.

This is a security property, not merely an implementation convenience. Values present
in the original request are not automatically visible to the template.

## Does `allowed_calls` grant a flow permission to perform an effect?

No. `allowed_calls` admits only the static shape of a `call` step. The host still
checks the invoking component, current hook, capability passport or grant, local
policy, request size, timeout, and revocation state before performing the effect.

Some capability families add another explicit layer. For example,
`inquirium.generate` requires a matching `inference_grants` entry, while `agent.*`
calls require matching `agent_grants`. A flow cannot widen either grant through
rendered data.

## Which step kinds does JSON-e Flow support?

The current profile supports six static kinds:

| Kind | Responsibility |
| :--- | :--- |
| `render` | Evaluate a JSON-e template into a named flow value. |
| `validate` | Validate a named value against a host-known contract. |
| `call` | Ask the host to invoke one literal, allowlisted capability. |
| `extract` | Select a subvalue from a prior named result. |
| `respond` | Return a named value to the caller. |
| `fail` | End with an explicit controlled failure. |

There are no dynamic steps, capability names selected from input, ambient loops, or
arbitrary code in the current profile.

## When should I use pure JSON-e?

Use it for deterministic value construction: normalization, field selection,
annotations, routing decisions, small rewrites, and schema-shaped responses. It is a
good fit when the behavior can be reviewed as a data transformation and needs no
effect, retry, long-lived state, or private integration.

## When should I use JSON-e Flow?

Use it when the transformation remains short and static but needs a few host-owned
effects, such as calling Inquirium, invoking a Sensorium directive, writing a Memarium
fact, publishing a workflow-step completion, or sending an artifact through Artifact
Delivery.

If the definition grows into dynamic orchestration, broad branching, substantial
domain policy, repeated loops, or mutable scratch state, move to a code-backed
middleware. Raising limits until JSON-e Flow resembles a programming language makes
the behavior harder to review without restoring the tools of a real language.

## Is JSON-e Flow a workflow engine?

No. It is a bounded passage owned by one middleware invocation. It does not own a
domain workflow, scheduling, provider discovery, distributed consensus, or durable
business state. Durable waiting and resumption are delegated to the host's bounded
deferred-operation mechanism; domain history remains with the domain component.

## How are deferred host-capability responses handled?

With `deferred_response_mode = "surface-to-caller"` (the default), a pending
`deferred-operation.v1` becomes a control-plane outcome. The current daemon stores the
original invocation and deferred step id. When a completed
`deferred-operation-status.v1` arrives, it re-evaluates the static flow and injects
that status at the matching call. Calls before the deferred step must therefore be
idempotent. The flow does not poll privately or choose retry cadence and TTL.

With `reject-as-failure`, any deferred response fails the synchronous passage as
`deferred-not-accepted`. See the [Bounded Deferred Operations
solution](../../project/60-solutions/029-bounded-deferred-operations/029-bounded-deferred-operations.md).

## Can a flow call a middleware service directly?

It should not. Call a stable host capability, not a provider's loopback endpoint or
private route. The daemon resolves the provider, applies policy, validates contracts,
and records the trace. Direct calls would couple the flow to one implementation and
bypass the host's authority boundary.

## Can JSON-e Flow use Inquirium and Sensorium Workbench together?

Yes, but the strata remain separate. Inquirium can produce advisory text or structured
intent. JSON-e Flow can render that result into a Sensorium directive. Sensorium and
Workbench then validate and execute only what their own policy permits. Model output
does not become execution authority merely because a template embeds it in a request.
The [Sensorium FAQ](sensorium-faq.en.md) explains the Action/Operation distinction and
the complete authority path.

## Can JSON-e Flow send or accept Artifact Delivery artifacts?

For outbound delivery, a flow can render an `artifact-delivery-envelope.v1` and call
`artifact.delivery.send` when the capability is statically allowed and authorized.

For inbound admission, the configured JSON-e Flow acceptor is intentionally pure: it
must return `InboundAdmissionResult` and must not declare host-capability calls. An
admission predicate that performs side effects would conflate deciding whether to
accept an artifact with acting on it. See the [Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#json-e-flows).

## Can a flow see raw input or prior component I/O?

Only through the explicit [Raw Signal Access](../../project/40-proposals/053-raw-signal-access.md)
contract. The concrete flow must declare `raw_signal_access`, local policy must permit
it, and `context_projection` must still map the allowed raw value into the authoring
context. Declaration, preservation, and projection are three separate gates.

Prefer a digest, classification, or narrow field projection whenever it satisfies the
use case. Trace records must not become a second storage path for secret-bearing input.

## Which JSON-e features and helpers are available?

The profile keeps JSON-e recognizable, including interpolation and bounded constructs
such as `$eval`, `$if`, `$switch`, `$match`, `$let`, `$map`, `$reduce`, `$merge`,
`$mergeDeep`, `$flatten`, and `$json`. The current host helper profile is
`orbiplex.json_e.helpers.basic.v1`, with explicitly selected helpers from
`sha256_json`, `sha256_text`, `default`, `has`, `pick`, and `idempotency_key`.

Helpers are pure and versioned. A helper profile must not silently change semantics;
output-changing behavior requires a new profile version and an explicit migration.

## How are failures classified?

The runtime distinguishes configuration and template loading, context projection,
evaluation, resource limits, output-contract validation, disallowed authority,
capability-call failures, deferred responses, and explicit flow rejection. This
separation matters operationally: editing a template cannot repair a revoked passport,
and retrying cannot repair an invalid output schema.

Every definition also carries byte, depth, collection, string, and time limits. A flow
adds total-step and loop-step budgets. Limits are part of the component contract, not
performance hints.

## How do I inspect and debug a flow?

Validate the whole node profile with `orbiplex-node-daemon check-config`, then use
`json-e-flow-dry-run` with explicit mock responses. Dry-run never calls real host
capabilities. At runtime, use `orbiplex-node-launcher json-e-flow-middleware`, the
`/operator/json-e-flow` page, or the daemon's trace endpoints. Retained traces expose
ids, digests, timings, step outcomes, and redacted diagnostics rather than raw payloads.

## How are JSON-e definitions distributed safely?

Flow definitions may live in operator configuration or in a middleware package. A
package can carry config fragments and examples, but it does not grant itself
authority. The operator still controls activation, package trust, context projection,
capability passports, grants, and local policy. Story-009 demonstrates a signed
package whose five role providers are in-process JSON-e Flows rather than supervised
HTTP services.

## When is code-backed middleware the better choice?

Choose code when the behavior needs streaming, persistent local state, non-trivial
algorithms, dynamic work graphs, rich retries, protocol adapters, OS integration, or
domain logic whose correctness deserves ordinary types and unit tests. JSON-e is the
least-power tool for data shaping; it is not a virtue to keep using it after the
problem has crossed that boundary.
