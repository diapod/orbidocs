# Collaborative Agents HOWTO

This HOWTO composes one flow from Room, Corpus, Agent, Inquirium, Sensorium Interfaces,
and Workbench. It does not create a new super-component: every transition remains
owned by the layer that understands its effect. Shorter explanations are in the
[Collaborative Agents FAQ](../faq/collaborative-agents-faq.en.md).

Unless a command says otherwise, run every `cargo` and `tools/...` command below
from the root of the `node/` workspace.

## Start with the responsibility map

| Component | Contribution to the flow | Must not take over |
|---|---|---|
| Shared Offer Catalog | topic-indexed provider offers | winner selection and Room |
| Corpus | query, bids, selection, roles, answer acceptance | live transport and model runtime |
| Room | membership, policy, attestation, relay epoch, live carrier | answer and feed authority |
| Agent | bounded lifecycle, binding, controller, trace, inert outcomes | ambient effects and publication |
| Inquirium | semantic inference operations and provider neutrality | Agent loops and tools |
| Sensorium Interfaces | read/subscribe plus separate actuation grants | Room membership |
| Workbench | isolated terminal and explicit command/file profiles | remote authority without a lease |
| Interaction Broker | bounded resource wait/watch | Corpus domain state |

In this document, P083 means
[Sensorium Interactive Interfaces](../../project/40-proposals/083-sensorium-interactive-interfaces.md):
the actuation contract that complements the read/subscribe surface promoted as
[Solution 046](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md).

## Check prerequisites and the evidence boundary

Before starting the flow, verify:

1. a trusted Seed Directory and current `corpus.provider` passports;
2. topic taxonomy plus active offers with the same taxonomy digest;
3. configured outbound AD and query/answer admission;
4. an active Room relay profile and membership-attestation signer;
5. a routable Inquirium runtime with current conformance evidence;
6. for a live feed: Sensorium Interface descriptor, source authority, and separate grants;
7. for a terminal: a local Workbench profile and fixture process.

Story-011/012 use three loopback addresses on one host. This is stronger isolation than
three ports on one address, but still shares a kernel, clock, filesystem, and failure
domain. Do not describe such a result as production federation E2E.

## Publish Corpus provider offers

A provider publishes an ordinary `service-offer.v1` with a Corpus extension,
canonical topic, and taxonomy digest. Shared Offer Catalog owns supersession, expiry,
full withdrawal, and partial-topic removal. Corpus does not maintain a parallel offer
catalog.

Before querying, verify that the topic index returns only active offer versions and
that each provider has a fresh `corpus.provider` passport discoverable through Seed
Directory.

## Create and dispatch a query

The requester creates `corpus-reasoning-query.v1` through:

```http
POST /v1/corpus/queries
POST /v1/corpus/queries/dispatch
```

The query binds `question-envelope.v1`, canonical `topic/term`, taxonomy digest,
keywords, a minor-unit price bracket, deadline, candidate limit, and reply target.
Dispatch uses AD `capability-many`; no response, policy refusal, timeout, and transport
failure remain distinct read-model states.

## Collect bids and select a provider

A provider admits the query through the Corpus acceptor and returns a signed
`corpus-reasoning-bid.v1`. The requester reads the round, then explicitly selects a bid:

```http
GET  /v1/corpus/rounds/{query_id}
POST /v1/corpus/rounds/{query_id}/select
```

Selection verifies the query bracket, currency, taxonomy, provider identity, expiry,
and signature. A counter price outside the bracket is not normalized away; it requires
explicit requester acceptance. The selected bid enters the ordinary procurement path.

## Open Room and activate a relay epoch

After selecting participants, open the Room bound to the round:

```http
POST /v1/corpus/rounds/{query_id}/room
POST /v1/corpus/rounds/{query_id}/room/relay/activate
```

Policy should define the accountable chair, access list, classification, bounded
metadata retention, and live limits. Relay epoch orders ephemeral frames but creates
neither membership nor answer authority. A production deployment publishes a signed
`room-relay-endpoint.v1`; a test `.invalid` locator only fences a local epoch and does
not pretend to be a public TLS endpoint.

## Invite participants and confirm readiness

Create a signed content-addressed invite and deliver it through AD:

```http
POST /v1/corpus/rounds/{query_id}/room/invites
POST /v1/corpus/room-invites/{invite_id}/join
POST /v1/corpus/room-invites/{invite_id}/ready
```

Join requires a fresh `room-membership-attestation.v1`. Exact invite replay should
return the same identity; changed content under the same idempotency key is a conflict.
A raw model binding is not a Room participant. The participant is an accountable
subject, optionally represented by a node-local Agent.

## Bind a node-local Agent to the participant

On each node, create an Agent with a bounded profile, budget, and grants, then bind it
to the exact round, Room, participant, and output sink. The binding should reference
accepted Room evidence; do not interpolate authority refs from model output or an
arbitrary JSON-e Flow.

The Agent controller may request Inquirium, observation, or an effect. The host runs
each operation only after separate admission. A child Agent may only narrow its
parent's authority and budget.

## Assign a role and instruction overlay

The chair proposes roles and instructions through separate append-only surfaces:

```http
POST /v1/corpus/rounds/{query_id}/role-assignments
POST /v1/corpus/rounds/{query_id}/role-assignments/{assignment_id}/decide
POST /v1/corpus/rounds/{query_id}/instruction-overlays
POST /v1/corpus/rounds/{query_id}/instruction-overlays/{overlay_id}/decide
```

A role such as "configuration auditor" or "Postfix administrator" is not a new
capability grant. The local host or participant accepts the assignment. Overlay source
remains inert; the host renders bounded `instruction/rendered` through registered
policy and rechecks its digest before every Inquirium invocation.

## Deliberate through inert turns

Agent invokes Inquirium through a host capability, receives the result, and proposes
`corpus-reasoning-turn-proposal.v1`. Only an admitted `corpus.room.turn` effect sends
the turn into Room. The first profile accepts `text/plain`, but requires a structured
envelope with assignment, `turn/no`, digest, classification, expiry, and idempotency.

```http
POST /v1/corpus/room-invites/{invite_id}/messages
```

The chair observes admitted turns through an Interaction Broker watch. Model-adapter
polling must not become a second event loop or a source of Room authority.

## Attach a live Sensorium feed

The source publishes an immutable Sensorium Interface descriptor and status. For a
terminal, use cursor-free `latest-state` when recipients only need the current
viewport. Then:

1. issue exact observation grants for B and C;
2. start projection through the current Room relay;
3. bind an opaque Agent observation need to the exact source ref;
4. on every read, verify Room membership, interface grant, source generation,
   effective publication, classification, freshness, and byte cap;
5. retain only refs, digests, and causal context in durable trace.

Room membership without an interface grant, and an interface grant without Room
membership, must both be refused. Source generation change or publication supersession
makes the old view stale; Agent cannot select an earlier, less cautious operational
impact class.

## Keep terminal control local

In the read-only profile, B/C and chair proposals remain advice. Only the local
operator or an explicitly authorized controller on node A enters commands into
Workbench and interprets the result. Do not send keystrokes as ordinary Room messages.

If remote control is required, use the separate Sensorium Interface actuation path:
exact grant, control request, lease, generation, epoch, sequence, and typed terminal
operation. Direct peer can reduce latency, but relay fallback preserves the same
fencing and does not acquire authority.

## Create, accept, and publish an answer draft

The chair Agent synthesizes turns into a content-addressed draft. Draft acceptance
does not publish an answer:

```http
POST /v1/corpus/rounds/{query_id}/agent-drafts/accept
POST /v1/corpus/rounds/{query_id}/agent-drafts/publish
```

The first operation verifies Agent binding, Room evidence, embedded schemas, and
actor-bound idempotency. The second requires separate authority, signs
`corpus-reasoning-answer.v1`, and binds the answer to the selected bid plus policy
digest. Model, Agent, and chair therefore cannot confuse "finished text" with a
"published fact".

## Settle and close the round

After accepting the answer, run ordinary procurement settlement. When the requester
considers the result sufficient, stop the round:

```http
POST /v1/corpus/rounds/{query_id}/settle
POST /v1/corpus/rounds/{query_id}/satisfy
```

`requester-satisfied` is explicit and idempotent. Do not close a round based only on
the absence of new messages, relay disconnection, or a model declaration.

## Handle revocation, restart, and relay failover

After observer revocation, wait for source-side audience projection to confirm the new
recipient set before publishing another state. Recipient restart restores durable Agent
binding and Room invitation, but the process-local latest-state inbox starts empty.
Source restart requires restarting the ephemeral projection pump.

Relay failover creates a new epoch without merging ephemeral sequences. A client gets
the current endpoint through an independent path, revalidates authority, and refreshes
current state.

## Run Story-011

On macOS, prepare loopback aliases explicitly; the runner never invokes `sudo`:

```sh
sudo python3 tools/acceptance/loopback_aliases.py ensure 127.0.0.2 127.0.0.3
```

Then run the managed smoke:

```sh
python3 tools/acceptance/story-011-corpus-fish/story-011-local-profiles.py \
  --home /tmp/orbiplex-story011 --regenerate-peer-certs \
  ad-smoke --timeout-seconds 180
```

Without permission to create aliases, explicitly select the weaker profile before the
subcommand:

```sh
python3 tools/acceptance/story-011-corpus-fish/story-011-local-profiles.py \
  --network-profile single-address-single-host \
  --home /tmp/orbiplex-story011-single-address ad-smoke
```

## Run Story-012

Check the composition gate first, then run the smoke:

```sh
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py preflight
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py \
  smoke --timeout-seconds 180
```

Variant without aliases:

```sh
python3 tools/acceptance/story-012-shared-chair-terminal/profile_plan.py \
  smoke --timeout-seconds 180 \
  --network-profile single-address-single-host
```

## Diagnose from authority toward the carrier

| Symptom | Check first |
|---|---|
| no providers | taxonomy digest, active offers, passports, and Seed Directory trust |
| bid is refused | signature, query binding, deadline, currency, and price bracket |
| join is refused | invite digest, membership attestation, epoch, and subject |
| Agent cannot send a turn | assignment, overlay decision, grant, and effect admission |
| chair cannot see a turn | Room high-water, Interaction Broker watch, and replay cursor |
| observer cannot see the feed | membership/interface-grant intersection, generation, and publication |
| terminal is visible but cannot be controlled | this is correct for read-only; check a separate actuation grant |
| draft exists but answer does not | separate Corpus publication authority and signature |
| reconnect loses live content | live content is ephemeral; refresh facts and current state |

Identify the refusing layer first. Bypassing it by manually invoking a later endpoint
destroys binding evidence and usually creates an unrecoverable read model.

## Source documents

- [Solution 036: Room](../../project/60-solutions/036-room/036-room.md)
- [Solution 038: Corpus](../../project/60-solutions/038-corpus/038-corpus.md)
- [Solution 042: Sensorium Workbench](../../project/60-solutions/042-sensorium-workbench/042-sensorium-workbench.md)
- [Solution 044: Inquirium](../../project/60-solutions/044-inquirium/044-inquirium.md)
- [Solution 046: Sensorium Interfaces](../../project/60-solutions/046-sensorium-interfaces/046-sensorium-interfaces.md)
- [Solution 047: Agent](../../project/60-solutions/047-agent/047-agent.md)
- [Story-011](../../project/30-stories/story-011-corpus-fish.md)
- [Story-012](../../project/30-stories/story-012-agents-share-chair-terminal.md)
