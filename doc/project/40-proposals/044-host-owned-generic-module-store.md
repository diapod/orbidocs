# Proposal 044: Host-Owned Generic Module Store

Based on:
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/40-proposals/029-workflow-template-catalog.md`
- `doc/project/40-proposals/033-workflow-fan-out-and-temporal-orchestration.md`
- `doc/project/60-solutions/arca.md`
- `doc/project/60-solutions/node.md`

## Status

Draft

## Date

2026-04-18

## Executive Summary

Middleware modules increasingly need small pieces of local durable state:
workflow templates, cursor positions, local projections, operator preferences,
and temporary coordination records. Requiring a new daemon field and endpoint
for every such need couples module semantics to the host runtime and turns the
Node into an accidental database schema for all modules.

This proposal introduces a **host-owned generic module store**: a small
module-scoped JSON record store exposed through the local host capability
channel. The host owns scoping, authentication, durability, replay, and
tombstones. The module owns the record semantics through an opaque
`record_kind`, `record_id`, and JSON `payload`.

The store is not a public catalog, not a rich query engine, and not a replacement
for artifacts or Agora. It is a local durability primitive that prevents
middleware-local state from forcing domain-specific daemon changes.

## Problem

Without a generic store, each local middleware persistence need tends to choose
one of three bad shapes:

1. add a daemon-specific Rust struct and endpoint for a module concern,
2. write files directly under module home with uneven replay and inspection,
3. use a public/federated substrate such as Agora for data that is merely local
   working state.

All three forms complect host responsibilities with module semantics. The host
should not know what an Arca workflow template means, but it should be able to
persist a module-scoped record safely and durably.

## Contract

### Addressing

Each record is addressed by:

- `module_id` — derived from the module host capability binding, not supplied
  by the caller;
- `record_kind` — opaque module-local namespace;
- `record_id` — opaque identifier within the kind.

The effective key is:

```text
(module_id, record_kind, record_id)
```

Modules cannot read or mutate records owned by another `module_id` through this
surface.

### Record Shape

```json
{
  "record_kind": "workflow-template",
  "record_id": "story-009/blog-draft",
  "owner_participant_id": "participant:did:key:z6Mk...",
  "payload": {
    "workflow_kind": "arca.blog-draft",
    "plan": {}
  },
  "created_at": "2026-04-18T08:00:00Z",
  "updated_at": "2026-04-18T08:00:00Z"
}
```

`owner_participant_id` is optional metadata for module-side filtering and
operator inspection. It is not an authorization decision by itself.

### Host Capability Surface

All calls are local, module-authtok protected, and use `POST` because the host
capability channel already treats requests as command envelopes.

```text
POST /v1/module/store/records/put
POST /v1/module/store/records/get
POST /v1/module/store/records/list
POST /v1/module/store/records/delete
```

#### Put

```json
{
  "schema_version": "v1",
  "capability_id": "module_store_put",
  "record_kind": "workflow-template",
  "record_id": "story-009/blog-draft",
  "owner_participant_id": "participant:did:key:z6Mk...",
  "payload": {}
}
```

Outcome:

- `stored`
- `rejected_invalid_record`
- `rejected_other`

#### Get

```json
{
  "schema_version": "v1",
  "capability_id": "module_store_get",
  "record_kind": "workflow-template",
  "record_id": "story-009/blog-draft"
}
```

Outcome:

- `found`
- `missing`
- `rejected_invalid_record`
- `rejected_other`

#### List

```json
{
  "schema_version": "v1",
  "capability_id": "module_store_list",
  "record_kind": "workflow-template",
  "owner_participant_id": "participant:did:key:z6Mk...",
  "limit": 100
}
```

Outcome:

- `listed`
- `rejected_invalid_query`
- `rejected_other`

`record_kind`, `owner_participant_id`, and `limit` are optional filters. The host
may clamp `limit`.

#### Delete

```json
{
  "schema_version": "v1",
  "capability_id": "module_store_delete",
  "record_kind": "workflow-template",
  "record_id": "story-009/blog-draft"
}
```

Outcome:

- `deleted`
- `missing`
- `rejected_invalid_record`
- `rejected_other`

Delete is a tombstone in the host commit log and removal from the live
projection.

## Persistence Model

The daemon persists each mutation as an append-only record:

```text
record_type = daemon/module-store-record.v1
stream     = state/module-store/{base64url(module_id + separator + kind + separator + id)}
```

Replay folds the log into the latest live projection. A tombstone removes the
projection key but remains in the log for audit and checkpoint correctness.

## Non-Goals

- No public federation. Public publication belongs to Agora, Dator, or another
  explicit catalog surface.
- No rich query language. The v1 query model is exact `record_kind`,
  exact `owner_participant_id`, and bounded list.
- No blob storage. Large outputs belong in host-owned artifacts or a module
  database.
- No module schema validation inside the host. Payload validation belongs to the
  module or to a future schema-gated record kind.
- No cross-module sharing by default.

## Story-009 Application

For story-009, Arca can use:

```text
record_kind = workflow-template
record_id   = story-009/bielik-blog
payload     = concrete or parameterized Arca workflow template
```

This gives Arca a local template store without making the Node know the Arca
template schema. A future Dator or Agora publication path can project selected
templates outward, but that is a separate publication decision.

## Open Questions

- Should v2 add schema-gated record kinds where the module declares a schema ref
  and the host verifies payload before write?
- Should operator UI expose records generically, or only through module-specific
  views?
- Should selected records be publishable to Agora as public facts with explicit
  topic and content schema?
