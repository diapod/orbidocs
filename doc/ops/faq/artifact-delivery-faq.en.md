# Artifact Delivery FAQ

## What is Artifact Delivery?

Artifact Delivery is the host-owned delivery and inbound admission plane for
schema-bound artifacts. A component submits an `artifact-delivery-envelope.v1` through
`artifact.delivery.send`; the daemon validates it, checks outbound authority, resolves
recipients, selects transport adapters, records the delivery, and exposes status to the
operator.

For the full operational walkthrough and diagram, see [Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#what-is-artifact-delivery).

## Why does Artifact Delivery exist?

Artifact Delivery prevents every component from becoming its own transport owner.
Components express delivery intent; the host owns routes, adapter selection,
retry/recovery, inbound admission, acceptor ownership, and operator-visible status. This
keeps INAC, Agora, Matrix mailbox, object-store indirection, and domain acceptors
stratified instead of tangled in each middleware package.

For the rationale and boundary discussion, see [Artifact Delivery rationale in the
HOWTO](../howto/artifact-delivery-howto.en.md#what-is-the-rationale-behind-artifact-delivery).

## What components use Artifact Delivery?

The main layers are `artifact-delivery-core` for pure contracts and
routing/authorization logic, `artifact-delivery` for runtime ledgers, recovery and
admission, `ad-host` for daemon-composed adapters and acceptors, and daemon
routes/operator UI for status. Current adapters include Agora publish, INAC direct,
Matrix mailbox, object-store indirect, and node-local loopback where configured.

For the component-by-component map, see [components in the Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#what-components-use-artifact-delivery).

## How can middleware use Artifact Delivery?

Middleware uses Artifact Delivery in two directions. For outbound delivery it calls
`artifact.delivery.send` with an envelope and must pass the host outbound allow policy.
For inbound delivery it is registered as an acceptor, and the host invokes it only after
shared admission checks pass. Package installation does not grant AD authority by
itself.

For Rust, supervised HTTP, Sensorium OS Actions, and JSON-e Flow examples, see
[middleware usage in the Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#how-can-middleware-use-artifact-delivery).

## How is Artifact Delivery configured?

Configuration is host-owned. The key config groups are `artifact_delivery`
routes/allows, `artifact_delivery_adapters`, `inac_peer_transport`,
`artifact_delivery_recovery`, `artifact_delivery_acceptors`,
`artifact_delivery_profiling`, and `artifact_delivery_observers`. The envelope controls
one delivery request, not the authority model.

For the option-level reference, see [Artifact Delivery configuration
HOWTO](../howto/artifact-delivery-howto.en.md#how-is-artifact-delivery-configured).

## What data shapes are used by Artifact Delivery?

The primary public shapes are `artifact-delivery-envelope.v1`,
`artifact-delivery-result.v1`, `artifact-delivery-status.v1`,
`artifact-delivery-recovery.v1`, `deferred-operation.v1`,
`deferred-operation-status.v1`, `artifact-object-pointer.v1`, `inac-control.v1`, and
domain artifacts such as `agora-record.v1`, `contact-request.v1`, or `memarium-blob.v1`.

For links to generated schema docs and daemon-local admission shapes, see [data shapes
in the Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#what-data-shapes-are-used-by-artifact-delivery).

## How does Artifact Delivery decide routing?

Routing starts from `delivery/plan`: either a host route reference or inline stages.
Recipient selectors resolve into concrete targets, outbound policy is checked against
the resolved plan, and each target's adapter scheme selects the transport. Inbound
transport frames then re-enter the shared AD admission path before reaching one
authoritative acceptor.

For selector details and sequential examples, see [routing in the Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md#how-does-artifact-delivery-decide-routing).
