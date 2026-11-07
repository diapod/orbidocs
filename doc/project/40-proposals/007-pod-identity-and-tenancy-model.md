# Pod Identity and Tenancy Model

Based on:
- `doc/project/40-proposals/006-pod-access-layer-for-thin-clients.md`
- `doc/project/20-memos/pod-backed-thin-clients.md`
- `doc/normative/50-constitutional-ops/pl/ROOT-IDENTITY-AND-NYMS.pl.md`

## Status

Proposed (Draft)

## Date

2026-03-21

## Executive Summary

This proposal defines the minimum identity model needed once Orbiplex extends
beyond the MVP and supports `pod`-backed users who participate through thin
clients hosted by a serving node.

It is not a prerequisite of the networking MVP. Proposal `014` now treats the
first useful Node as a one-operator-participant system with explicit role split
between `node-id` and `participant-id`, while `pod-user-id` remains an additive
later identity layer rather than a day-one baseline requirement.

The key decision is simple:

1. hosted-user identity must be distinct from serving-node identity,
2. client/device identity must be distinct from hosted-user identity,
3. responsibility, reputation, and sanctions must attach to different layers,
4. migration and anti-Sybil controls must preserve continuity without collapsing all
   hosted users into the operator or all devices into independent persons.

## Context and Problem Statement

The existing identity model already distinguishes:

- `root-identity`,
- `anchor-identity`,
- `node-id`,
- `nym`,
- `station-id` / delegated station.

That model is enough when a node is primarily an operator-controlled participant with
delegated devices.

The `pod` model changes the picture. A serving node may now host multiple human users
who are neither the node operator nor merely one more device of the operator. If the
system does not name that layer explicitly, several pathologies follow:

- hosted-user reputation collapses into operator reputation,
- multiple hosted users of one node look like one actor,
- one user's multiple devices look like many actors,
- device compromise is over-escalated to the entire user or host,
- migration between `pod` hosts breaks participation continuity,
- anti-Sybil logic either becomes too weak or punishes legitimate multi-user hosting.

## Goals

- Introduce a first-class hosted-user identity layer for `pod`.
- Preserve separation between host responsibility and user participation.
- Preserve separation between user identity and device/session identity.
- Keep continuity compatible with the existing `root / anchor / node / nym / station`
  model.
- Define where reputation, policy, and sanctions should attach by default.
- Make room for both local-only and federated portability profiles.

## Non-Goals

- This proposal does not define full UI flows for identity recovery.
- This proposal does not mandate one global attestation regime for all federations.
- This proposal does not define every schema field needed for implementation.
- This proposal does not itself define compensation or billing for hosting.

## Decision

Once Orbiplex introduces hosted multi-user participation, it should adopt a layered
identity model for `pod` participation with at least
the following distinct identities:

1. `node-id` - the serving infrastructure actor,
2. `pod-user-id` - the hosted human participant,
3. `client-instance-id` - the concrete client/device/session endpoint,
4. optional `nym` - the public-facing pseudonymous presentation layer.

`pod-user-id` MUST NOT be treated as merely a local operator-owned account.
`client-instance-id` MUST NOT be treated as an independent participant by default.

## Proposed Model

### 1. Identity stack

The recommended stack is:

- `root-identity` or other deep continuity source, where available,
- `anchor-identity`, where continuity is portable and attestable,
- `node-id` for the serving node,
- `pod-user-id` for the hosted user,
- `client-instance-id` for each concrete app install / device / session lineage,
- optional public `nym` mapped to either `pod-user-id` or a scoped participation role.

Not every federation must expose or require all layers, but the semantics must remain
separable.

### 2. `pod-user-id`

`pod-user-id` is the key addition in this proposal.

It identifies a hosted participant across:

- multiple client instances,
- reconnects,
- policy decisions,
- user-scoped exports,
- migration to another `pod` host or fuller participation profile.

At minimum, `pod-user-id` should have:

- stable identifier semantics,
- host-local continuity,
- exportability,
- revocation / suspension state,
- optional linkage to stronger identity roots.

The baseline preserves pseudonymous operation. `pod-user-id` becomes mappable to
`anchor-identity` only when a stronger federation profile explicitly selects that
accountability mode.

Device authorization for a hosted user MUST require the hosted user's own key
material, not only the serving node's key. Otherwise `pod-user-id` collapses into
a host-owned sub-identity of the operator instead of remaining a distinct
participant layer.

That requirement does not imply widening the transport handshake. The healthier
layering is:

- node-scoped session establishment first,
- hosted-user or participant authorization later over that encrypted channel.

In other words, a future `pod` implementation should prefer a participant-scoped
bind artifact such as `participant-session.v1` or `participant-bind.v1`, carried
over the live `node↔node` session, instead of embedding hosted-user identity into
`peer-handshake.v1`.

The first schema seed for that later bind layer now lives in:

- `doc/schemas/participant-bind.v1.schema.json`

The first concrete consumer of that bind should live in the pod access layer as:

- `doc/schemas/client-instance-attachment.v1.schema.json`

The next minimal lifecycle companion should be:

- `doc/schemas/client-instance-detachment.v1.schema.json`

The first recovery-oriented companion should then be:

- `doc/schemas/client-instance-recovery.v1.schema.json`

### 3. `client-instance-id`

`client-instance-id` identifies the concrete endpoint used by a hosted user.

It exists for:

- session management,
- local-device trust decisions,
- anomaly detection,
- device compromise handling,
- per-device revocation,
- bounded forensic analysis.

Default rule:
- many `client-instance-id` values under one `pod-user-id` do not create many votes,
  many reputations, or many independent persons.

This follows the same structural logic as `station-id` under an existing `node-id`.

The first detach artifact should therefore terminate or invalidate one concrete
`client-instance-id` without automatically escalating to `pod-user-id` or `node-id`.

The first recovery artifact should likewise restore one concrete client path
without silently rewriting the higher responsibility layers.

### 4. Responsibility boundaries

By default:

- `node-id` carries hosting responsibility,
- `pod-user-id` carries participation responsibility,
- `client-instance-id` carries endpoint responsibility.

Examples:

- abusive data retention by the host is a `node-id` / operator problem,
- repeated harmful participation by a hosted user is primarily a `pod-user-id`
  problem,
- stolen phone or session token is initially a `client-instance-id` incident.

Escalation across layers is allowed, but not automatic. The system should move upward
only on evidence of broader compromise or broader abuse.

### 5. Reputation attachment

Default reputation behavior should be:

- hosting reputation attaches to `node-id`,
- user participation reputation attaches to `pod-user-id`,
- device trust signals attach to `client-instance-id` but do not become public
  reputation by default.

Reputation transfer across pod hosts is never automatic in the baseline. It requires
review or an explicit import policy so that migration preserves continuity without
turning hosting history into an ambient trust grant.

This prevents two opposite errors:

- punishing every hosted user for operator failure,
- letting one operator multiply influence by hosting many pseudonymous users with no
  aggregation logic.

### 6. Public presentation and pseudonymy

A hosted user may need one or more public-facing pseudonyms.

The baseline rule should be:

- public rooms and protocol events may show `nym` rather than `pod-user-id`,
- one `pod-user-id` may hold multiple scoped public `nym`s at once,
- the serving node must still maintain a procedural mapping from that public face to
  the hosted identity,
- federations may restrict how many simultaneously active public `nym`s one hosted
  user may maintain in sensitive roles.

Scopes are the accountability boundary. This keeps public participation workable
without losing internal accountability.

### 7. Portability profiles

Federations should be able to support at least two portability models:

#### Host-local portability

`pod-user-id` is stable only inside one serving node, but export can mint a migration
bundle for another host.

#### Federated portability

`pod-user-id` is tied to a portable continuity layer, such as an `anchor-identity` or
federation-recognized delegated continuity record, allowing migration without semantic
rebirth.

The second model is stronger, but the first is still useful as long as migration does
not become hidden lock-in.

### 8. Anti-Sybil and aggregation

The system must not assume that many hosted users on one node are always one person,
but it also must not assume they are always independent.

Therefore anti-Sybil logic should be able to consider:

- shared host,
- shared attestation source,
- suspiciously coupled device behavior,
- coordinated creation and voting patterns,
- shared continuity roots where visible to authorized procedure.

This should produce bounded aggregation or additional review, not blanket identity
collapse.

### 9. Minimal contract sketch

```json
{
  "serving-node/id": "node:pl-wro-7f3c",
  "pod-user/id": "pod-user:did:key:z6MkhaXgBZDvotDkL5257faiztiGiC2QtKLGpbnnEGta2doK",
  "client-instance/id": "client:ios-a13-82d1",
  "public-nym/id": "nym:amber-river",
  "anchor-identity/ref": null,
  "hosted-tenancy/scope": ["chat", "memory:private", "swarm:participate"],
  "reputation/subject": "pod-user/id",
  "device-trust/subject": "client-instance/id",
  "host-responsibility/subject": "serving-node/id"
}
```

These exact fields may change, but the semantic split should remain.

## Trade-offs

1. Cleaner accountability vs more identity complexity:
   - Benefit: responsibility and sanctions become much more precise.
   - Cost: more identifiers and more mapping logic.
2. Portability vs privacy minimization:
   - Benefit: users can migrate and preserve continuity.
   - Cost: stronger continuity can also increase correlation risk.
3. Anti-Sybil rigor vs hosted-user accessibility:
   - Benefit: harder to farm influence through cheap clients.
   - Cost: some legitimate hosted-user setups may face additional review.

## Failure Modes and Mitigations

### 1. Hosted-user collapse into operator identity

Failure:
- every action of a hosted user is treated as if the node operator personally did it.

Mitigation:
- mandatory `pod-user-id` layer,
- separate reputation and sanction semantics,
- explicit host-vs-user trace fields.

### 2. Device multiplication as fake pluralism

Failure:
- one hosted user opens many clients and appears as many independent voices.

Mitigation:
- `client-instance-id` subordinate to `pod-user-id`,
- aggregation of influence at `pod-user-id`,
- anomaly review for suspicious device fan-out.

### 3. Host hides hosted-user portability

Failure:
- user cannot leave without losing continuity.

Mitigation:
- migration bundle or portable continuity contract,
- explicit export requirement,
- policy-level prohibition on opaque host-only tenancy.

### 4. Over-escalation from device compromise

Failure:
- one stolen phone destroys the whole hosted identity or entire node.

Mitigation:
- device-level revocation first,
- layered escalation only on evidence,
- session and device trace separation.

Device/session restrictions, rate limits, and attachment revocation are the
sanctions allowed at `client-instance-id` level. Broader reputation sanctions attach
to `pod-user-id` or a higher subject, not to the device identifier.

## Open Questions

No unresolved questions remain for this proposal slice. The decisions below
record the approved defaults.

Resolved 2026-07-04:

1. `pod-user-id` is mappable to `anchor-identity` only in stronger federation
   profiles. The baseline preserves pseudonymous operation unless a stronger
   accountability profile is explicitly selected.
2. One `pod-user-id` may hold multiple scoped public `nym`s at once. The scopes
   are the accountability boundary and must remain visible in the relevant
   artifacts.
3. Reputation transfer across `pod` hosts is allowed only through review or an
   explicit import policy. There is no automatic cross-host reputation transfer
   in the baseline.
4. Device/session restrictions, rate limits, and attachment revocation are the
   sanctions allowed at `client-instance-id` level only. Broader reputation
   sanctions must attach to the appropriate higher subject.
5. Other swarm participants may see only a minimal continuity attestation for a
   `pod-user-id`, without host history. This preserves useful continuity while
   avoiding routine migration or hosting disclosure.

## Multiple local participants: prerequisite tracker — 2026-11-06

[P098](098-alpha-ui.md#8-participant-access-contract-memarium-and-whisper)
needs real local participants distinct from the operator, before its P/Q access
evidence is possible. The [console identity memo](../20-memos/console-participant-identity-create-and-import.md)
explicitly limits MVP to one participant and defers Scenario C. A Participant
caller type alone does not implement that extension. The following bounded local
workstream belongs here under identity/tenancy; it does not require full hosted-pod
portability, introduce a new human identity class, or redefine the one-participant
MVP retrospectively. P034's node/operator consent remains separate.

| ID | Item | Status | Dependencies | Deliverable and gate | Consumers (not prerequisites) |
|---|---|---|---|---|---|
| P007-LP-001 | Freeze multiple-local-participant ownership and activation | todo | Existing root/participant identity and S026 custody contracts | Define explicit create/import, local activation/deactivation and operator-role selection; uniqueness must no longer imply operator status. Bind each participant to their credential/session enrollment, Vault/key domains, nym and recovery roles, recipient identity and owner references. Freeze legacy sole-participant attribution, migration/rollback, quotas and deletion/retention without silently changing operator consent. Local activation is neither network `participant-bind.v1` nor a grant. Enumerate operator-selection call sites and assign explicit adapters/owners; this contract does not wait for P024's new verifier or P098. Freeze a versioned local-operator-role lookup and migration signal for the restricted local-primary adapter. Before the explicit-role model is activated, the legacy sole-participant rule is confined to the declared legacy model. After activation, only an explicit role binding identifies O; missing/corrupt role state never falls back to cardinality. Additional participants do not revoke O's role or existing allowed participant operations. | P007-LP-002; P024-009; P060-038 P095-013 |
| P007-LP-002 | Deliver independently owned local identities and custody | todo | P007-LP-001 | Implement supported provisioning/import and explicit activation of O, P and Q, with separate credentials, Vaults, keys, leases/cache namespaces, nyms, recovery state and recipient ownership. Replace implicit first/sole-participant selection in shared identity/key/recovery paths with owner-explicit selection; domain route/action adapters remain P060/P057/P015 work. Qualify restart, lock/unlock, switching, revocation, restore and cross-participant refusal using actual owner-created identities, not manually inserted fixture IDs. Keep operator management on its existing admitted path; no new unguarded participant endpoint is needed to test the foundation. Preserve explicit operator lookup across adding P/Q, restart and rollback; existing operator adapters consume that lookup even while independent participant domain adapters remain unavailable. Qualify role-port continuity with owner fixtures, without making the P098 screens a prerequisite. Revoking/changing the role invalidates affected context; restore must not silently re-enable legacy cardinality inference. | P024-010; P060-039; P057-020; P098 independent-participant profile |

## Next Actions

1. Keep `014` and `requirements-006` centered on the one-operator-per-node MVP while
   preserving explicit `node-id` vs `participant-id` role split.
2. Update `006` implementation requirements so `pod-user-id` and `client-instance-id`
   are explicit once `pod` moves from extension to active delivery track.
3. Define requirements for hosted-user export and migration bundles.
4. Define how `pod-user-id` interacts with public `nym` issuance and role thresholds.
5. Define federation policies for anti-Sybil aggregation of hosted users.
6. Define reputation transfer policy across `pod` hosts: review or explicit import
   only, never automatic.
7. Define the minimal continuity attestation exposed to other swarm participants for
   `pod-user-id`; it must not disclose host history by default.
8. Define sanctions scope explicitly: device/session restrictions, rate limits, and
   attachment revocation at `client-instance-id` level only; broader reputation
   sanctions attach to `pod-user-id` or a higher subject.
