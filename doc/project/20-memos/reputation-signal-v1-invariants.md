# Reputation Signal v1 Invariants

`reputation-signal.v1` is a small append-only fact record. The schema captures
the portable shape; this note freezes the invariant card that strict consumers
should enforce on ingest.

## Invariants

1. `subject/kind = node` -> `subject/id` MUST be `node:did:key:...`
2. `subject/kind = participant` -> `subject/id` MUST be `participant:did:key:...`
3. `subject/kind = nym` -> `subject/id` MUST be `nym:did:key:...`
4. `signal/type` prefix = `procedural/*` -> `subject/kind` MUST NOT be `nym`
5. `signal/type` prefix = `contract/*` -> `subject/kind` MUST NOT be `nym`
6. `signal/type` prefix = `community/*` -> `subject/kind` MAY be `nym`
7. `signal/type` prefix = `incident/*` -> `subject/kind` MAY be `node`, `participant`, or `nym`
8. `recorded/at >= observed/at`
9. `weight ∈ (0.0, 1.0]`
10. `polarity ∈ { positive, negative }`

## Enforcement note

Standard JSON Schema can directly enforce:

- rules `1-7`,
- rule `9`,
- rule `10`.

Rule `8` is still mechanically verifiable, but not by vanilla draft-2020-12
schema alone, because it requires comparison of two timestamps. Consumers that
want strict ingest SHOULD enforce it in boundary tests or runtime validation.

## Domain model note

`signal/type` is the only source of truth for the domain:

- `procedural/...`
- `contract/...`
- `community/...`
- `incident/...`

There is no separate `domain` field in the record. This avoids a duplicated
field pair that could drift out of sync.

## Nym note

`nym` is a valid reputation subject only where the surrounding layer actually
permits pseudonymous reputation. This is why `community/*` and some
`incident/*` signals may target `nym:did:key:...`, while `procedural/*` and
`contract/*` do not.

This keeps the contract aligned with the governance boundary:

- governance and panel service run on stable `participant:did:key`
- pseudonymous reputation may still exist in the social layer

## Retention note

`retention/hint` is not a decay engine. It is only emitter intent:

- `ephemeral`
- `persistent`
- `epoch-scoped`

Consumers may ignore it in MVP read models, but keeping it in the base contract
prevents later decay logic from having to backfill intent after the fact.
