# Middleware FAQ

## What are middleware types?

Middleware is hosted extension behavior owned by explicit contracts. The main execution
types are in-process Rust, pure JSON-e, JSON-e Flow, command/stdio, unmanaged local HTTP
JSON, supervised HTTP, Sensorium connector middleware, and middleware-hosted Inquirium
runtime adapters. Distribution is a separate axis: a middleware can be factory-bundled,
profile-distributed, or operator-installed regardless of execution type.

For the detailed type descriptions, registration shapes, and examples, see [Middleware
HOWTO](../howto/middleware-howto.en.md#what-are-middleware-types).

## What is Role Middleware?

Role Middleware is not an execution type. It is a specialization pattern: a middleware
component receives a role-shaped request and dispatches it to behavior selected by role,
capability, or service identity. It can be implemented as supervised HTTP, JSON-e Flow,
or another registered middleware form.

For concrete supervised HTTP and JSON-e Flow examples, see [Role Middleware in the
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

## How does one HTTP middleware distinguish calls from multiple hooks?

A supervised HTTP middleware may reuse one endpoint for multiple registrations, but the
HTTP path is not the semantic discriminator. The middleware should inspect the request
envelope, especially `chain_kind`, `envelope_kind`, and the schema-specific payload
shape. Separate paths are often clearer operationally, but even then the envelope
remains the source of truth.

For request examples and branching sketches, see [multiple-hook dispatch in the
Middleware
HOWTO](../howto/middleware-howto.en.md#how-does-one-http-middleware-distinguish-calls-from-multiple-hooks).

## Where are distribution and packaging rules described?

Execution type and distribution model are separate. The same middleware behavior can be
compiled into the node, shipped as a profile definition, or installed as an operator
package. Distribution changes trust posture and lifecycle, not the runtime contract by
itself.

For the distribution model reference, see [Distribution models in the Middleware
HOWTO](../howto/middleware-howto.en.md#distribution-models).
