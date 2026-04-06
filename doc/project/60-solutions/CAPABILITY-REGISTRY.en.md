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
