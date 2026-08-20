# Middleware FAQ

## What are middleware types?

Middleware is hosted extension behavior owned by explicit contracts. The main execution
types are in-process Rust, pure JSON-e, JSON-e Flow, command/stdio, unmanaged local HTTP
JSON, `channel_json` supervision, Sensorium connector middleware, and middleware-hosted
Inquirium runtime adapters. The old supervised `http_local_json` executor is retired:
its config and package forms are rejected, and no runtime implementation remains.
Distribution is a separate axis: a middleware can be factory-bundled,
profile-distributed, or operator-installed regardless of execution type.

For the detailed type descriptions, registration shapes, and examples, see [Middleware
HOWTO](../howto/middleware-howto.en.md#what-are-middleware-types).
For the boundary between the pure evaluator and host-owned flow steps, see the
[JSON-e and JSON-e Flows FAQ](json-e-and-json-e-flows-faq.en.md).

## When should a module use `channel_json`?

Use `channel_json` for an eligible supervised module whose loopback listener exists
only so the Node host can attach, invoke, observe, or expose a host-mediated operator
surface. The module initiates one authenticated session to the daemon's shared
listener; it does not receive durable authority or a replay queue from that session.

Keep an intentional product, peer, browser, or provider listener when it is part of
the component contract. Mixed modules migrate only their host-control plane and keep
the product listener explicit. Never register the same semantic route through both
transports as an implicit fallback. New supervised modules and packages must use
`channel_json`; a retained product HTTP listener is configured as a separate domain
surface, not as the middleware executor.

Bundled modules make current ownership visible through `factory_executor` and
`product_listener_retained`. All 18 bundled modules use `channel_json`; a host-only
module has no factory port. Eight modules retain separately owned product listeners.
Daemon configurations, persisted settings, loose config artifacts, and package
manifests that name `http_local_json` are rejected before effects with an explicit
migration diagnostic. Node never silently converts them. Stale listener keys in a
channel-only bundled module subtree are likewise rejected rather than ignored.

Python modules should reuse the standard channel adapter instead of implementing
WebSocket framing. See [Authoring a channel module](../howto/middleware-howto.en.md#authoring-a-channel-json-module).

For Inquirium, the model-runtime catalog may select `channel_json` with a module id,
declared invoke path, and timeout. This changes transport only: `runtime/ref`, model
binding, policy, and response validation remain host-owned.

## What happens when required middleware disappears?

The Node does not keep routing calls to a consumer whose required provider is gone.
It resolves exact capability-and-contract-digest dependencies, marks affected
consumers non-routable, drains and stops them in dependent-first order, and reports
`dependency_unavailable`. A dedicated reconciliation loop resumes consumers
provider-first only when the exact requirements are observed ready again; reading
health/status never starts or stops a component. A same-named but
contract-mismatched or incorrectly pinned provider is not a recovery.

For a transient channel loss, the supervisor injects the bounded reconnect grace into
the child. Current generated profiles use 1 second; a standalone Python runtime with
the variable absent retries for 0 seconds. Grace exhaustion or a failed application
heartbeat terminates and cleans the child before the configured restart policy runs.
No in-flight request is replayed transparently.

This lifecycle transition cleans up typed host-local resources. Durable, external,
and federated effects retain their own transaction, journal, compensation,
supersession, or approval semantics. Process shutdown is never presented as undo of
such an effect. See [Declaring component dependencies and effect recovery](../howto/middleware-howto.en.md#declaring-component-dependencies-and-effect-recovery).

## What is Role Middleware?

Role Middleware is not an execution type. It is a specialization pattern: a middleware
component receives a role-shaped request and dispatches it to behavior selected by role,
capability, or service identity. It can be implemented as supervised channel JSON, JSON-e Flow,
or another registered middleware form.

For concrete supervised channel JSON and JSON-e Flow examples, see [Role Middleware in the
Middleware HOWTO](../howto/middleware-howto.en.md#what-is-role-middleware).

## Where can middleware attach to the node data path?

The current peer-message chains are `pre-input`, `inbound-peer`, `pre-send`, and
`post-chain` observers. Other middleware surfaces include claimed local routes,
role/service dispatch, host capability bridges, broadcast handling, operator UI
surfaces, and read-only observer/audit hooks. The important rule is that each attachment
has its own request contract and allowed decisions; there is no single universal
interceptor contract.

For the complete hook map, decisions, examples, and compatibility notes, see [Middleware
hook
HOWTO](../howto/middleware-howto.en.md#where-can-middleware-attach-to-the-node-data-path).

## How does one supervised middleware distinguish calls from multiple hooks?

A supervised channel middleware may reuse one declared invoke path for multiple
registrations, but the path is not the semantic discriminator. The middleware should
inspect the request envelope, especially `chain_kind`, `envelope_kind`, and the
schema-specific payload shape. Separate paths are often clearer operationally, but
even then the envelope remains the source of truth.

For request examples and branching sketches, see [multiple-hook dispatch in the
Middleware
HOWTO](../howto/middleware-howto.en.md#how-does-one-supervised-middleware-distinguish-calls-from-multiple-hooks).

## Where are distribution and packaging rules described?

Execution type and distribution model are separate. The same middleware behavior can be
compiled into the node, shipped as a profile definition, or installed as an operator
package. Distribution changes trust posture and lifecycle, not the runtime contract by
itself.

For the distribution model reference, see [Distribution models in the Middleware
HOWTO](../howto/middleware-howto.en.md#distribution-models).
