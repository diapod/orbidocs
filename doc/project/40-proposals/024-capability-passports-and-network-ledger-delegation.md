# Proposal 024: Capability Passports and Network Ledger Delegation

Based on:
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/40-proposals/021-service-offers-orders-and-procurement-bridge.md`
- `doc/project/40-proposals/023-federated-offer-distribution-and-catalog-listener.md`
- `doc/project/20-memos/participant-assurance-levels.md`
- `doc/project/60-solutions/node.md`

## Status

Draft

## Date

2026-03-31

## Executive Summary

The current Node runtime can trust local sovereign operators and can project
participant assurance levels, but it cannot yet delegate infrastructure
capabilities from one trusted Node to another through one portable,
verifiable artifact.

This proposal introduces `capability-passport.v1` as that general delegation
artifact.

The decisions of this proposal are:

1. infrastructure capabilities delegated to other Nodes must be expressed as a
   signed `capability-passport.v1` artifact rather than as ad-hoc config,
2. passport signing proves issuer consent, while authority is interpreted by the
   concrete capability profile; infrastructure profiles such as
   `network-ledger` require a local participant whose derived assurance level is
   `sovereign-operator`,
3. the signing format is deterministic canonical JSON with the `signature`
   field omitted from the signed payload,
4. `network-ledger` is the first concrete delegated infrastructure capability,
5. network settlement must use a dedicated async adapter layer rather than
   extending the synchronous local `SettlementLedger` trait,
6. hard-MVP discovery for delegated infrastructure capabilities is static
   config pinned by a trusted sovereign issuer, not gossip or dynamic
   marketplace discovery.
7. publisher-signed capability templates for built-in modules are signed
   recommendations, not executable authorization grants,
8. capability identifiers must distinguish formal global names from
   identity-anchored sovereign names so private or deployment-local capability
   namespaces do not collide.

This keeps the stratification clean:

- local settlement remains a small synchronous write/read core,
- network settlement becomes a separate async adapter boundary,
- trust delegation is modeled once and can later be reused for `escrow`,
  `oracle`, or other attached infrastructure roles.

## Context and Problem Statement

The current settlement rail is deployment-local. Each Node rebuilds ORC account
balances from its own append-only `LedgerFact` stream and treats that local
ledger as the source of truth.

That is sufficient for hard-MVP single-deployment operation, but not for a
multi-Node shape where one Node should act as a trusted infrastructure service
for others, such as:

- a shared network ledger,
- a settlement escrow,
- a dispute oracle,
- or any future bounded infrastructure role.

Without one explicit delegation artifact:

- Node-to-Node trust for infrastructure roles lives in configuration folklore,
- remote capabilities cannot be audited as signed facts,
- the same trust problem will be re-solved separately for every role.

The current transport and identity proposals already define:

- canonical `node:did:key:...`,
- canonical `participant:did:key:...`,
- sovereign operators as a special trust class orthogonal to ordinary
  identity assurance.

What is missing is one general artifact that says:

> this sovereign operator, on this issuing Node, delegates this infrastructure
> capability to that target Node, under this scope, until this expiry.

## Goals

- Define `capability-passport.v1` as the general signed delegation artifact for
  infrastructure capabilities.
- Freeze the canonical signing rules for the passport.
- Freeze the minimum verification algorithm used by receiving Nodes.
- Define `network-ledger` as the first concrete capability delegated through a
  passport.
- Freeze `NetworkLedgerAdapter` as an async boundary distinct from the
  synchronous local settlement trait.
- Freeze static-config bootstrap for the first hard-MVP network-ledger
  deployment profile.
- Freeze the sovereign capability-id syntax and the corresponding wire-
  advertisement projection.

## Non-Goals

- This proposal does not define dynamic capability discovery, gossip, or
  marketplace-based routing for infrastructure roles.
- This proposal does not define the message format or request/response
  framing for remote settlement operations. It only freezes the delegation
  artifact, the adapter boundary, and the transport choice (peer channel).
  The ledger wire protocol — typed message pairs, correlation IDs, and
  serialization contract — is a separate future specification.
- This proposal does not redefine `node-identity.v1` or participant/org
  identity contracts.
- This proposal does not define organization-level multisig issuance of
  passports. One sovereign operator is sufficient for hard-MVP.
- This proposal does not define passport transparency logs or revocation
  gossip. Revocation is local-policy driven in this phase.

## Decision

### 1. `capability-passport.v1` as the General Delegation Artifact

Infrastructure capabilities delegated to another Node MUST be expressed as one
portable signed artifact:

- `schema = "capability-passport.v1"`
- `passport_id = "passport:capability:..."`
- `node_id = "node:did:key:..."` of the target Node receiving the capability
- `capability_id = "network-ledger"` or another stable capability name
- optional `capability_profile = { ... }` carrying human-readable display
  metadata and content-addressed machine schema references
- `scope = { ... }` capability-specific parameters
- `issued_at` RFC 3339
- `expires_at` RFC 3339 or `null`
- `issuer/participant_id = "participant:did:key:..."`
- `issuer/node_id = "node:did:key:..."`
- `revocation_ref = null | "node:did:key:..."`
- optional `issuer_delegation = { ... }` when the passport is signed by a
  scoped proxy key (see Proposal 032)
- `signature = { "alg": "ed25519", "value": "..." }`

The passport is an auditable delegated or consent fact. It does not itself
create trust out of nothing. Trust derives from profile-specific local policy:
for infrastructure delegation, policy recognizes the issuing participant as a
sovereign operator and accepts its delegation authority; for consent profiles,
policy may require additional counter-signatures or attestations.

`capability_profile`, when present, is part of the signed passport payload. It
may include:

- `display/name`,
- `description`,
- `lang`,
- `doc/ref`,
- optional `doc/url` as a human convenience mirror,
- `schema/id`,
- `schema/ref`,
- `schema/media-type`.

`schema/ref` is a content-addressed Orbiplex reference to a
`capability-schema.v1` artifact. Receivers use it to fetch a machine-readable
contract over the Node-to-Node peer protocol or another local cache, not as a
trust shortcut. Trust still comes from passport verification and local policy.

### 2. Signing Authority Is Profile-Scoped

Every capability passport is signed by a participant issuer, but not every
passport profile has the same authority rule.

For high-impact infrastructure profiles such as `network-ledger`,
`seed-directory`, `escrow`, or `oracle`, only a participant whose derived
assurance level is `sovereign-operator` may issue a valid capability passport.
This does not mean that `IAL5` replaces ordinary identity proofing. It means
that infrastructure delegation is governed by software-pinned sovereign trust,
not by phone or government-ID attestation.

Other profiles may define narrower consent semantics. For example,
`node-primary-operator` is a virtual operator-binding capability: the participant
passport means "I consent to be the primary operator of this Node", and the
binding becomes effective only when the target Node also signs an acceptance
artifact.

Issuer verification therefore proceeds in two stages:

1. parse `issuer/participant_id` from the passport,
2. apply the authority rule for the specific `capability_id`.

If the issuer does not satisfy the profile-specific policy, the passport MUST be
rejected even if the signature is cryptographically valid. For `network-ledger`
and the other critical infrastructure profiles listed above, that policy is
still sovereign-operator issuance.

### 2a. Publisher-Signed Capability Templates for Built-In Modules

Built-in modules MAY be distributed with publisher-signed capability templates.
A template is a signed statement of software intent, not an executable
authorization grant.

The template answers:

- which built-in module or package asks for a host capability,
- which `capability_id` and profile it expects,
- which minimal scope it requests,
- which package or component digest the request belongs to,
- who published that recommendation.

The local Node MUST NOT treat a publisher template as authority to use a host
capability. Host capability use still requires either:

- a local capability passport issued or accepted by local operator policy, or
- an externally fetched executable passport whose issuer is explicitly trusted
  by local policy for that exact capability and scope.

Resolution order is:

1. local deny or local disable wins and stops resolution,
2. local executable passport wins over any publisher template,
3. configured external passport sources MAY be queried only when local policy
   names the source and trusts the issuer for the requested capability/scope,
4. publisher templates MAY be used to recommend or auto-issue a local passport
   only when local policy enables that behavior,
5. otherwise the request is denied as missing authorization.

This lets a packaged built-in module declare "I normally need
`memarium.write` for the community space" without giving the software publisher
standing authority over a local Node's Memarium. Local configuration remains the
point where authority enters the system.

If auto-issuance is enabled for built-ins, the Node signs or accepts a local
passport derived from the template and records the template id and digest in
audit metadata. Revoking or replacing the local passport immediately shadows the
template. A local deny also shadows the template, even if the package is still
installed.

Externally fetched executable passports are acceptable only through
operator-configured sources such as an organization policy server, a static
deployment bundle, or a community governance issuer. A module MUST NOT fetch its
own host-capability passport from the network and present it as a bootstrap
authority path. That would collapse the separation between software identity and
local authority.

### 3. Canonical Signing Format

The signed bytes are the deterministic UTF-8 bytes of the passport encoded as
canonical JSON with:

- object keys sorted lexicographically,
- arrays left in original order,
- no insignificant whitespace,
- the top-level `signature` field omitted entirely from the canonical payload,
- the top-level `issuer_delegation` field omitted when present. It carries a
  separate principal signature and is verified as a separate proof.

The signature algorithm is Ed25519.

The signing and verification algorithm is:

1. clone the passport payload without `signature`,
2. serialize it into canonical JSON,
3. sign those bytes with the issuer participant's Ed25519 key, or with the
   delegated proxy key named by an inline `issuer_delegation` proof,
4. encode the signature as base64url without padding,
5. store it under `signature.value`,
6. set `signature.alg = "ed25519"`.

The verifier repeats the same canonicalization. Direct passports verify the
Ed25519 signature against the public key recoverable from
`issuer/participant_id`. Delegated passports first verify `issuer_delegation`
against that participant identity, then verify the passport signature against
`issuer_delegation.proxy_key`.

### 4. `network-ledger` as the First Delegated Infrastructure Capability

The first concrete use of `capability-passport.v1` is the `network-ledger`
capability.

Semantics:

- the target Node named in `node_id` is authorized to act as a settlement
  ledger authority for the receiving deployment profile,
- that Node's local `LocalOrcLedger` remains the actual source of truth for
  balances and holds,
- remote Nodes interact with it through a network adapter boundary rather than
  through their own local ledger state.

The capability-specific `scope` for `network-ledger` MAY be empty in hard-MVP.
Future phases MAY add fields such as:

- allowed account namespaces,
- top-up policy refs,
- maximum hold lifetime,
- accepted receipt classes.

Receivers MUST tolerate unknown `scope` keys and MUST validate only the fields
they understand.

### 4a. Sovereign Capability Identifiers

Capability ids now distinguish two classes:

- formal global ids without `@`, such as `network-ledger`,
- sovereign ids anchored in an identity, such as
  `audio-transcription@participant:did:key:z...`.

A sovereign id may also be informal, indicated by a leading `~` on the
capability name:

- `~audio-transcription@participant:did:key:z...`

This gives three stable wire-level intentions:

| Form | Meaning |
| :--- | :--- |
| `network-ledger` | formal global capability id |
| `audio-transcription@participant:did:key:...` | sovereign formal capability |
| `~audio-transcription@participant:did:key:...` | sovereign informal capability |

Rules:

- formal capability ids MUST NOT contain `@`,
- sovereign capability ids MUST contain exactly one `@`,
- the identity suffix after `@` is the anchor and may currently be
  `participant:did:key:...`, `node:did:key:...`, or `org:did:key:...`,
- the `~` informal marker applies only to sovereign capability names.

This preserves backward compatibility for all existing formal ids while
letting operators or organizations anchor private capability families in their
own identity instead of the global bare-name namespace.

### 4b. Wire Advertisement Projection for Sovereign Capabilities

Capability passports keep the full sovereign id, but capability advertisements
use a shorter wire name:

- `audio-transcription@participant:did:key:z...`
  advertises as `sovereign/audio-transcription`,
- `~audio-transcription@participant:did:key:z...`
  advertises as `sovereign-informal/audio-transcription`.

Because the wire name alone is not enough to reconstruct the full sovereign
capability id, `CapabilityAdvertisementV1` must also carry:

- `anchor_identities = { "audio-transcription": "participant:did:key:z..." }`

Receivers therefore interpret sovereign wire advertisements from the pair:

- short wire name in `capabilities/core`,
- matching anchor entry in `anchor_identities`.

Formal well-known capabilities still use their stable mapped wire names such as
`core/network-ledger` or `role/offer-catalog`. Unknown formal capabilities may
be advertised as bare formal names without `@`.

### 5. Async `NetworkLedgerAdapter` Boundary

The synchronous local settlement trait is intentionally not extended for remote
operations.

Instead, network settlement is modeled as a separate async adapter boundary:

```rust
#[async_trait]
pub trait NetworkLedgerAdapter: Send + Sync {
    async fn balance(&self, account_id: &AccountId) -> Result<OrcBalance, LedgerError>;
    async fn submit_hold(&self, spec: HoldSpec) -> Result<HoldId, LedgerError>;
    async fn release_hold(&self, hold_id: &HoldId) -> Result<(), LedgerError>;
    async fn apply_top_up(
        &self,
        receipt: GatewayReceiptRecord,
    ) -> Result<TopUpApplyOutcome, LedgerError>;
}
```

Hard-MVP includes two implementations:

- `LocalNetworkLedgerAdapter` — delegates to the local `LocalOrcLedger`,
- `RemoteNetworkLedgerAdapter` — talks to a trusted ledger Node over the
  existing inter-node WebSocket peer channel, not a separate HTTP service.

Ledger operations are expressed as typed message pairs (request + response)
on an established peer session. The peer channel is the only transport surface
for network ledger operations. This avoids a second port, reuses existing peer
authentication, and keeps capability routing within the capability model:
the `network-ledger` capability is announced in `CapabilityAdvertisementV1`,
the passport is verified post-handshake via `capability-passport-present.v1`,
and ledger messages flow on the same connection.

The local settlement write path remains append-only and synchronous inside one
Node. The network adapter is the layer that absorbs latency, retries, and
partial failure.

### 6. Static Config Discovery for Hard-MVP

The initial network-ledger deployment profile uses static configuration:

```toml
[settlement]
mode = "network"

[settlement.network_ledger]
node_id   = "node:did:key:z..."
endpoint  = "wss://ledger.example/peer"
passport  = "path/to/capability-passport.v1.json"
```

The `endpoint` field is the WebSocket peer listener address of the target
ledger Node — the same address type carried in `node-advertisement.v1`
endpoint entries. It is not an HTTP API address. Ledger operations are sent
as typed messages on the peer session established to that address.

At daemon startup the Node MUST:

1. load the passport,
2. verify the signature,
3. verify the issuer participant is sovereign under local policy,
4. verify `capability_id == "network-ledger"`,
5. verify that the target `node_id` matches the configured remote ledger node,
6. reject startup if verification fails.

This keeps failure explicit and early. If the remote ledger passport cannot be
trusted, the Node must not start in `settlement.mode = "network"`.

## Proposed Artifact Shape

### `capability-passport.v1`

Minimum fields:

- `schema`
- `passport_id`
- `node_id`
- `capability_id`
- `scope`
- `issued_at`
- `expires_at`
- `issuer/participant_id`
- `issuer/node_id`
- `revocation_ref`
- `signature`

Example:

```json
{
  "schema": "capability-passport.v1",
  "passport_id": "passport:capability:network-ledger:01hznx...",
  "node_id": "node:did:key:z6MkTargetLedgerNode",
  "capability_id": "network-ledger",
  "scope": {},
  "issued_at": "2026-03-31T19:20:00Z",
  "expires_at": null,
  "issuer/participant_id": "participant:did:key:z6MkSovereignOperator",
  "issuer/node_id": "node:did:key:z6MkIssuerNode",
  "revocation_ref": null,
  "signature": {
    "alg": "ed25519",
    "value": "kYcC7xR8..."
  }
}
```

## Verification Rules

A receiver MUST reject the passport if any of the following holds:

- the payload does not parse,
- required fields are empty,
- `schema != "capability-passport.v1"`,
- `passport_id` does not use the `passport:capability:` prefix,
- `signature.alg != "ed25519"`,
- the signature does not verify against `issuer/participant_id`,
- the issuer does not satisfy the policy for that `capability_id` (for
  `network-ledger`, this means sovereign under local policy),
- `expires_at` is present and already elapsed,
- the passport's `capability_id` does not match the role being configured.

Receivers MAY additionally reject passports by local policy, such as:

- disallowed `issuer/node_id`,
- disallowed `scope`,
- explicitly revoked `passport_id`,
- mismatched endpoint-to-node mapping.

## Implementation Notes

- A host capability such as `capability.passport.sign` is a suitable operator
  interface for passport issuance.
- A host capability such as `capability.passport.verify` is a suitable
  diagnostic surface for operators before startup or deployment.
- The canonical JSON encoder should live in a small auditable crate rather than
  inside the daemon.
- Passport signing should use the participant signing key, not the Node
  infrastructure signing key, because the delegating authority belongs to the
  sovereign participant role.
- `RemoteNetworkLedgerAdapter` connects to the target Node's peer listener
  over WSS and exchanges typed ledger message pairs on the established session.
  The `RemoteLedgerClient` trait MUST be async to support the correlation-ID
  request/response pattern over a message-oriented connection.
- Loopback operation (one Node acting as both ledger server and client) is a
  valid and recommended development configuration. The daemon dials its own
  peer endpoint; Tokio handles server and client tasks independently, so no
  deadlock occurs.

## Consequences

### Positive

- One auditable mechanism can later serve `network-ledger`, `escrow`, `oracle`,
  and similar roles.
- Trust in remote infrastructure roles becomes explicit and exportable.
- The local settlement core remains small and synchronous.
- Remote settlement enters the system through a narrow async adapter boundary.

### Negative

- Passport issuance introduces another operator-visible artifact to manage.
- Static config is operationally manual until dynamic discovery arrives.
- Revocation remains local-policy driven in hard-MVP.

## Alternatives Considered

### Extend `SettlementLedger` for remote calls

Rejected. Remote settlement has different failure modes and latency than the
local append-only ledger core. Mixing both into one synchronous trait would
smear network concerns across the local settlement write path.

### Reuse generic peer capability advertisement

Rejected for this phase. Advertisements are discovery-oriented and ephemeral,
while capability passports are governance-oriented and signed for durable
trust. The two artifacts serve different roles.

### Trust remote infrastructure only by endpoint URL

Rejected. Endpoint-only trust is operationally weak and not portable. A signed
passport ties capability delegation to canonical participant and Node identity.

## Open Questions

- Should future revocation use an append-only `capability-passport-revocation`
  fact or a short-lived denylist cache?
- Should `scope` for `network-ledger` stay opaque longer, or should the first
  hard-MVP include explicit account namespace constraints?
- Should future multi-sig issuance be modeled as multiple signatures on one
  passport or as a separate endorsement bundle?
