# Node Middleware Init and Capability Reporting

This memo captures one missing extension-host contract for Orbiplex Node:
middleware modules should not remain opaque after startup.

When the Node starts and binds a middleware executor or plugin-process surface, it
should emit a host-owned `middleware-init` message. After receiving it, the module
should report:

- module name,
- short module description,
- offered capabilities,
- and optional implementation-local notes.

## Why this matters

Without an init/report handshake:

- the host cannot tell what newly attached modules actually provide,
- operator tooling sees only executor ids or local process config,
- capability routing becomes guesswork,
- and extension surfaces drift toward black-box plugin folklore.

The goal is not rich orchestration yet. The goal is simple visibility and a stable
minimum contract.

## Proposed shape

### Host-owned init message

The Node should emit a local init artifact such as:

- `middleware-init`

It should include at least:

- middleware contract version,
- host/runtime version,
- executor id,
- executor transport kind,
- optional `node-id`,
- and any narrow host capabilities the module may rely on.

### Module report

The module should return one report such as:

- `middleware-module-info-report`

It should include at least:

- module name,
- module description,
- offered capabilities.

## Semi-open capability catalog

Capability identifiers exposed by middleware modules should be semi-open.

This means:

1. some capability classes are constrained,
2. some remain open-ended.

### `base` capability class

Capabilities in the `base` class should require a stable output or behavior
contract.

Examples:

- a redaction module returning one redaction artifact shape,
- a routing policy module returning one route proposal shape,
- a transcript monitor returning one transcript-derived shape.

`base` capabilities therefore need:

- a stable capability id,
- and a reference to the expected output contract.

### `other` capability class

Capabilities in the `other` class remain open-ended.

They still need:

- a stable capability id,
- a short description,
- and output compatible with the generic middleware host contract.

But they do not need a special protocol-level output shape in MVP.

## Placement in the architecture

This contract belongs in two places:

1. `orbidocs`
   - as the canonical semantic contract,
2. `node`
   - as the implementation-facing host and runtime documentation.

The canonical rule should live in `orbidocs`, because it is part of the Node
extension model rather than one repository-specific coding trick.

The implementation specifics should also live in:

- `node/middleware/README.md`
- and typed Rust contracts under `node/middleware`

because the host/runtime details are repository-local.

## MVP boundary

This memo does **not** require:

- dynamic network-wide module discovery,
- capability negotiation across the federated network,
- or automatic loading of arbitrary plugin classes.

It only requires that once a Node binds a local middleware module, the host can ask:

- who are you,
- what do you do,
- and which capability ids should the host attach to you.
