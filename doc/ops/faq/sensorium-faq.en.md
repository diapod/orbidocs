# Sensorium FAQ

## What is Sensorium?

Sensorium is the node organ for local sensorimotor contact with the world. It admits
observations, mediates bounded directives, records their outcomes, and hides connector
mechanics behind host-owned capabilities. It is the boundary at which a local signal
becomes an admitted node fact and an intended effect becomes a policy-checked action.

Sensorium is not the whole middleware system, an LLM runtime, or a generic remote
procedure-call bus. Model inquiry belongs to Inquirium. Distribution belongs to
Artifact Delivery. A connector integrates one class of external reality without
becoming the authority that decides who may use it.

For an operational path from configuration to invocation, see the [Sensorium
HOWTO](../howto/sensorium-howto.en.md).

## Why is Sensorium an organ rather than just another connector API?

The organ is the stable semantic boundary; connectors are replaceable mechanisms.
Callers ask Sensorium to admit a signal or perform an allowlisted action. The host
then applies identity, capability, sensitivity, timing, consent, and audit policy
before choosing a connector. This prevents every device, operating-system adapter,
or Workbench backend from inventing its own authority model.

The term **connector** names the hosted component. An **adapter** is an implementation
technique inside a connector or host runtime. Documentation should not use the words
as interchangeable architectural roles.

## What are Observation, Directive, Action, and Outcome?

An **Observation** is an admitted, time-bounded representation of a signal. A
connector proposes a candidate; Sensorium assigns host-owned admission metadata and
places the result in the local read model.

A **Directive** is an issuer-bound request to perform one `action_id` with typed
parameters and a bounded timing policy. It expresses intent, not permission.

An **Action** is the operator-allowlisted behavior named by that `action_id`. Its
catalog entry defines parameter shape, limits, availability, result contract, and the
connector route hidden below Sensorium Core.

An **Outcome** is the audit fact produced for a directive. It records completion,
refusal, failure, or timeout and may refer to admitted observations or artifacts. It
is not automatically another observation and is not a public event stream.

## What is a Sensorium Interface?

A Sensorium Interface is an explicitly published, bounded projection of an enacted
representation or effect surface. It is a resource with separate grants, lifecycle,
classification, cursor, and revocation semantics. It can expose, for example, a
temperature batch, a Workbench terminal screen, or a constrained control method.

An interface is not the connector and does not expose connector credentials. Local
Sensorium admission remains local by default; publication through Sensorium Interfaces
is a separate operator-visible decision. See [Solution 046: Sensorium
Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## What kinds of connectors exist?

Connector shape follows behavior rather than one closed taxonomy:

- observation-oriented connectors produce candidate signals;
- finite-action connectors perform bounded operations and return results;
- Sensorium OS is the reference connector for explicit operating-system action
  catalog entries;
- Sensorium Workbench manages stateful workspace, terminal, patch, and environment
  operations behind stronger grants and recovery rules;
- source adapters can project selected connector state into Sensorium Interfaces.

This list is explanatory, not an enum that third-party implementations must copy.
Each connector still declares concrete actions, contracts, limits, and status.

## What is the difference between `action_id` and `connector_id`?

`action_id` is the public semantic address, for example
`sensorium.workbench.file.read` or `whisper.redaction.prepare`. Consumers may place it
in `sensorium-directive.v1` after receiving authority to invoke Sensorium.

`connector_id` is a host-private routing detail. Ordinary middleware, JSON-e Flows,
Agents, and remote peers must not select it. If consumers depend on a connector id,
provider replacement becomes an API break and the host can no longer enforce one
policy boundary.

## How does Sensorium OS differ from Sensorium Workbench?

Sensorium OS executes finite, catalogued actions such as an allowlisted script with a
closed parameter and result contract. The action catalog, script digest, working
directory, environment, timeout, and output caps are operator-owned. The caller sends
parameters, not an executable or shell text.

Sensorium Workbench manages longer-lived resources: workspace roots, file snapshots,
terminal sessions, structured commands, artifacts, patches, and managed environments.
These operations have resource identities, event cursors, idempotency, recovery, and
often operator-only controls. Workbench is therefore a higher-risk specialization
below Sensorium Core, not a replacement for Sensorium OS.

## Can we call Workbench behaviors "Sensorium Workbench Actions"?

At the `sensorium-directive.v1` boundary they are actions identified by `action_id`.
Within Workbench, **operation** is the more precise term because many behaviors create
or transition a stateful resource: a terminal session, command, captured artifact, or
managed environment. Use "Workbench operation" in domain explanations and "action
id" when referring to Sensorium dispatch.

## Can Inquirium or an Agent execute a command directly?

No. Inquirium may propose structured intent; an Agent or JSON-e Flow may transform
that proposal into a directive. Sensorium and Workbench still validate the caller,
grants, `action_id`, parameters, command profile, workspace, timing, idempotency, and
current runtime state. Model output is evidence or advice, never execution authority.

An Agent, Corpus round, or Room workflow may use
`sensorium-workbench-tool-request.v1` to carry verified lineage. The wrapper does not
create additional authority; the daemon unwraps it into the ordinary Sensorium path.

## Can JSON-e or JSON-e Flow use Sensorium?

Yes. A JSON-e Flow may render a `sensorium-directive.v1` and call the literal
`sensorium.directive.invoke` capability. `allowed_calls` only admits that static call
shape. The host still checks the component's passport or grant and Sensorium still
checks the action catalog and connector-specific policy.

Pure JSON-e should only construct or normalize data. It cannot perform the effect on
its own. See the [JSON-e and JSON-e Flows
HOWTO](../howto/json-e-and-json-e-flows-howto.en.md).

## Does enabling a connector authorize its actions?

No. Process activation, capability registration, action-catalog authorization,
caller authority, and invocation admission are separate gates. A running connector
may expose no effective actions. Conversely, a catalog entry may be authorized but
temporarily unavailable because its runtime or isolation requirement is absent.

This separation is intentional: installation is not authority, and readiness is not
consent.

## How does interactive operator consent work?

The daemon owns the consent state machine and presents the question through the
operator-question and notification surfaces. A participant with an active node
operator binding may grant once, remember an exact command, remember a bounded argv
prefix, approve a Sensorium OS action-catalog entry, deny, or later revoke a durable
grant.

The host projects a granted decision into an adapter-specific sidecar. Workbench gets
command-profile deltas; Sensorium OS gets action-catalog deltas. The connector merges
that sidecar with its main configuration using the same validator as at startup.
Consent cannot widen network, credential-environment, timeout, output, workspace, or
other limits beyond the operator's policy.

Inspect and revoke durable decisions in `/operator/consents`. Sensorium OS catalog
authorization has its own operator view at `/operator/sensorium-os`.

## Are deferred Sensorium actions supported?

Yes. An action catalog entry declares whether it is `sync-only`, `async-only`, or
supports either mode. An asynchronous directive returns a
`deferred-operation.v1`; the host registry owns polling, expiry, cancellation, and
operator visibility. The connector owns the domain operation state but must not make
the caller invent a private polling loop.

Use `sensorium.operation.status` and, where the operation exposes a valid cancel path,
`sensorium.operation.cancel`. A deferred envelope is control-plane data, not the
action's domain result.

## Where do large results and files go?

Keep ordinary results bounded. A connector may return a small typed result and
artifact references. Large or durable bytes should move through the appropriate
artifact store and Artifact Delivery path rather than being copied into observations,
audit facts, terminal events, or JSON-e traces.

Workbench artifacts are digest- and size-checked before use. Publishing or delivering
them remains a separate decision. See the [Artifact Delivery
HOWTO](../howto/artifact-delivery-howto.en.md).

## Does Sensorium publish every observation to other nodes?

No. Observation admission builds a local read model. Local Agora projection is
optional and not the general remote-read contract. Explicit remote access belongs to
Sensorium Interfaces, where the operator publishes an exact source projection and
grants bounded read, subscription, or control methods.

Presence on a carrier, Room membership, or knowledge of an interface id never
replaces the current interface grant.

## How is the risk of a live environment communicated?

Workbench and other suitable sources publish a
`sensorium-operational-context.v1` with an impact class such as `research`,
`experimental`, `test`, `production`, or `critical`, plus a bounded summary. Sensorium
Interfaces propagate that immutable publication context so Agents, Corpus, Room, and
Inquirium consumers can choose a more conservative policy before reading or acting.

The context is evidence, not authority. A consumer may raise the effective risk class
but must not lower it. A changed source generation or superseded publication makes the
old context stale and causes the relevant path to fail closed.

## How should I diagnose a refused action?

Walk outward from authority to mechanics:

1. confirm the caller may invoke `sensorium.directive.invoke`;
2. inspect `sensorium.directive.list` and the effective action catalog;
3. check connector readiness and per-action availability;
4. verify parameters, timeout, idempotency key, workspace and command profile;
5. inspect operator consent or catalog sidecar diagnostics;
6. read the directive outcome through `sensorium.audit.read`;
7. for deferred work, inspect the common deferred-operation record.

Do not begin by calling the connector's private loopback endpoint. That bypasses the
same boundary whose refusal needs explaining.

## What is implemented today, and what remains intentionally incomplete?

Sensorium Core observation admission, local read model, directive dispatch, outcome
audit, Sensorium OS C1/C2 action execution, catalog authorization, operator consent,
and deferred actions are implemented. Sensorium Interfaces implements local
host-capability, authenticated direct-peer, local SSE, and WSS Room carrier paths.
Their coverage is deliberately asymmetric: SSE is a local observation adapter, Room
carries observation `latest-state` and the closed P083 actuation classes, while the
host-local and direct-peer paths expose separately authorized actuation.

Workbench has an implemented local and fixture-managed foundation, structured PTY,
file, patch, artifact, broker, consent, interface, and recovery paths. A pinned full
system image, production vfkit deployment evidence, the fully virtualized Workbench
adapter, and later Linux backends remain post-MVP work. Documentation and operator
policy must not describe those future backends as present isolation guarantees.

## Where are the canonical contracts?

Start with [Solution 030: Sensorium](../../project/60-solutions/030-sensorium/030-sensorium.md),
[Solution 042: Sensorium Workbench](../../project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md),
and [Solution 046: Sensorium Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).
The main design rationale remains in Proposals
[045](../../project/40-proposals/045-sensorium-local-enaction-stratum.md),
[048](../../project/40-proposals/048-sensorium-os-connector-action-classes.md),
[071](../../project/40-proposals/071-sensorium-workbench.md),
[082](../../project/40-proposals/082-sensorium-interfaces.md), and
[083](../../project/40-proposals/083-sensorium-interactive-interfaces.md).
