# Capability ID Registry

This document is the human-facing registry of capability IDs used across the
Node <-> Node and Node <-> Seed Directory trust and discovery surfaces.

It is not the full solution capability matrix. It is a narrower artifact that:

- maps each `capability_id` to its semantic meaning,
- shows the corresponding role or runtime class,
- records the wire-visible name,
- helps keep `orbidocs`, `node`, and passport contracts in sync.

## Scope

This registry covers capability IDs used as:

- identifiers in `capability-passport.v1`,
- identifiers in `capability-advertisement.v1`,
- routing or discovery predicates in the Node runtime.

It does not cover host-local capabilities such as `recovery.sign` or
`catalog.local.query`. Those belong to the host's local capability surface, not
to the federated capability ID registry.

## Assertion Layers

Capability advertising and capability passports are related, but not
interchangeable.

Use the following layers:

| Layer | Artifact | Meaning | Trust basis | Examples |
|---|---|---|---|---|
| Protocol-native capability | `capability-advertisement.v1` with a self-issued passport-form assertion | "this peer currently speaks this baseline protocol surface" | node signature, self-issued capability passport, and successful peer session | `core/messaging`, `core/keepalive` |
| Passport-backed capability | `capability-passport.v1` carried in advertisement or indexed by Seed Directory | "this node is authorized or accepted for this capability profile" | profile-specific passport policy, issuer signature, revocation checks | `network-ledger`, `seed-directory`, `escrow` |
| Federation-recommended service | passport-backed capability plus federation policy | "this passport-backed capability is recommended or safe under this federation's policy" | high-assurance issuer, federation allowlist, local policy | approved ledger, trusted seed directory, certified offer catalog |
| Sovereign/private capability | sovereign capability id, optionally passport-backed | "this node offers an identity-anchored capability outside the global bare-name namespace" | anchor identity plus optional passport and local policy | `audio-transcription@participant:did:key:...`, `~audio-transcription@participant:did:key:...` |
| Self-announced custom capability | `capability-advertisement.v1` with a self-issued passport-form assertion | "this node says it can do this; verify by protocol use or local policy" | node signature plus self-issued passport; no federation endorsement unless separately attached | experimental plugin, non-critical discovery hint |

Therefore:

- `capability-advertisement.v1` is the live discovery and routing view and may
  be exchanged directly without Seed Directory,
- `capability-passport.v1` is the durable authority, consent, or endorsement
  proof for capability profiles that require one,
- `capability-schema.v1` is the optional machine-readable contract for a
  capability profile and is referenced by content-addressed `schema/ref`,
- the Seed Directory indexes passport-backed capabilities for network discovery,
- and consumers must apply local policy before treating any advertised
  capability as trusted.

## Public Passport Classes

The registry distinguishes public network publication from closed deployment
catalogs.

For publicly broadcast capability passports:

| Class | Passport `capability_id` | Wire/query projection | Issuer expectation |
|---|---|---|---|
| Official / community-recognized | registered formal bare id, e.g. `network-ledger`, `seed-directory`, `offer-catalog` | stable mapped name such as `core/network-ledger`, `role/seed-directory`, `role/offer-catalog` | participant, organization, council, or federation key at the highest assurance required by the community policy |
| Compatible sovereign implementation | sovereign id without `~`, e.g. `offer-catalog@participant:did:key:...`, plus `capability_profile.compatible_with` | `sovereign/...` plus anchor-aware filtering | the anchoring identity or delegated signer; consumers verify the compatibility claim against schema/profile evidence and local policy |
| Custom / operator-authored | sovereign id with `~`, e.g. `~article-review@participant:did:key:...` or `~article-review@org:did:key:...` | `sovereign/...` plus anchor-aware filtering | the anchoring identity or delegated signer; consumers apply local endorsement and reputation policy; `schema/ref` describes the custom protocol |

A public custom service MUST NOT mint a new unanchored bare formal
`capability_id` and publish it as if it were a community-recognized capability.
It should either use an existing registered formal id or use a sovereign
identity-anchored id.

Closed operator-owned deployments are different. They may use a local Seed
Directory as a deployment catalog for a known set of formal capabilities, with
trust coming from explicit configuration, allowlisted node ids, and established
peer sessions rather than public federation endorsement. Story-009 uses this
closed-deployment rule for the `offer-catalog` passports on node B/C.

## Sources of Truth

This document should remain synchronized at least with:

- `node:capability/src/lib.rs`
- `orbidocs:doc/project/60-solutions/node.md`
- `orbidocs:doc/project/60-solutions/CAPABILITY-MATRIX.en.md`
- the relevant capability or attached-role proposals

If any of the following changes:

- `capability_id`,
- wire name,
- capability semantics,
- or the primary runtime owner,

then this registry should be updated as well.

## Capability Registry

| capability_id | Wire name | Class | Semantic role | Typical runtime owner | Passport in MVP | Notes |
|---|---|---|---|---|---|---|
| `network-ledger` | `core/network-ledger` | infrastructure | remote settlement-ledger authority for other nodes | settlement-capable Node | yes | This capability means ledger authority, not merely one hold or one policy. |
| `seed-directory` | `role/seed-directory` | infrastructure | catalog of capability passports, revocations, and advertisements used for bootstrap and discovery | Seed Directory service or embedded Node service | yes | This capability covers trusted catalog publication and lookup semantics. |
| `offer-catalog` | `role/offer-catalog` | domain role | federated offer surface used for responder-side fetch and discovery | Dator on the supply side, Arca on the demand/discovery side | yes, when delegated by passport | The capability is domain-level; implementations may split supply and observed/discovery concerns across modules. |
| `escrow` | `role/escrow` | attached supervisory role | supervisor of hold, release, refund, freeze, and dispute paths for settlement contracts | escrow supervisor node or attached service | yes | This capability governs the lifecycle of reserved funds for a contract, not full ledger authority. |
| `oracle` | `plugin/oracle` | attached role / plugin | bounded external judgment, verification, or adjudication surface | future oracle service | planned | At this stage it is a reserved identifier and extension direction rather than a full hard-MVP runtime slice. |

## Semantic Distinctions

### `network-ledger` vs `escrow`

- `network-ledger` answers: "who is the ledger authority?"
- `escrow` answers: "who supervises the conditional release of funds for this contract?"

These roles may be co-located, but they are not semantically identical.

### `offer-catalog`

`offer-catalog` is a domain capability, not the name of one concrete process.
In the current MVP:

- Dator owns the supply side and responder-side fetch,
- Arca owns the demand side, observed catalog, and discovery.

The capability remains singular even if the runtime realizes it through more than
one module.

## Next Actions

- Extend this registry when new stable inter-node capability IDs appear.
- Add a more precise `issuer -> consumer -> scope` table once attached-role
  passports start carrying richer `scope` semantics than the current MVP.
