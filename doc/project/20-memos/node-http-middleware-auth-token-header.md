# Optional Auth-Token Header Protection for Node-Attached HTTP Middleware

This memo captures one narrow hardening option for Node-attached middleware that
communicates over local HTTP.

The goal is modest:

- keep unmanaged or supervised local HTTP middleware easy to run,
- but allow one extra host-owned access check so the middleware does not accept
  unauthenticated ambient loopback traffic by default when the operator wants
  that protection.

This is not a substitute for transport security, network isolation, or richer
module identity. It is one bounded host-to-module shared-secret check.

## Decision

HTTP middleware executors may expose one optional configuration pair:

- `auth-token`
- `auth-token-file`

### `auth-token`

`auth-token` is the feature switch.

If it is absent or empty:

- no extra header-based protection is enabled.

If it is a non-empty string:

- the value is treated as the HTTP header name that the middleware must require,
- for example: `X-Arca-Auth`.

### `auth-token-file`

`auth-token-file` is optional.

If it is absent:

- the default token file path is:
  - `<data_dir>/middleware/<middleware-name>/authtok`

If it is present:

- the configured path replaces the default path.

## Runtime Semantics

When header protection is enabled:

1. the Node reads one token value from `auth-token-file` or from the default
   `authtok` file,
2. every outbound HTTP request sent by the Node to that middleware includes the
   configured header name with that token value,
3. the middleware server checks the presence of that header and compares the
   supplied value with its local expected token,
4. requests with a missing or mismatched token are rejected.

The token value itself is not stored inline in the middleware config. The config
only names:

- whether the mechanism is enabled,
- which header name to use,
- and optionally which file to read.

## Token Source

The default token value should be host-owned and Node-local.

The MVP baseline is:

- the Node generates the token during startup,
- it uses the same general pattern as the Node's local CLI auth token,
- it is Node-specific,
- it does not rotate during one Node process lifetime,
- and both the Node and the middleware may safely read it once during startup.

This means the runtime does **not** need hot reload for the token file in MVP.

If an operator wants a different value or an externally managed secret file:

- they may place that value in the configured `auth-token-file`,
- but rotation semantics remain restart-bound in MVP.

## Why this shape

This shape keeps authority on the host side:

- the Node chooses whether the mechanism is enabled,
- the Node chooses the header name,
- the Node owns the default token file location,
- and the middleware only checks one bounded shared secret.

It also avoids coupling the middleware contract to:

- TLS certificates,
- public bearer-token flows,
- or ambient shell environment assumptions.

## Intended Scope

This mechanism is appropriate for:

- supervised `http_local_json` middleware,
- and unmanaged `local_http_json` middleware when the operator still wants the
  same header check.

It protects primarily against:

- accidental unauthenticated local requests,
- stale tooling hitting the middleware directly,
- or other local processes probing a loopback HTTP surface without the expected
  host token.

## Non-Goals

This memo does **not** define:

- remote network authentication,
- per-request signing,
- mutual TLS,
- dynamic in-process token rotation,
- or module-to-module trust semantics.

It is one narrow host-to-middleware guardrail.
