# Host-Owned Module Store

Based on:
- `doc/project/40-proposals/044-host-owned-generic-module-store.md`
- `doc/project/30-stories/story-009-bielik-blog-arca.md`
- `doc/project/60-solutions/node.md`
- `doc/project/60-solutions/arca.md`

## Status

Implemented thin slice in `orbiplex-node`.

## Date

2026-04-18

## Summary

The host-owned module store is a local Node capability that lets supervised
middleware modules persist small JSON records without forcing the daemon to
learn module-specific schemas.

It is a durability primitive, not a domain model. The Node owns:

- module scoping from the module authtok binding,
- append-only persistence and checkpoint replay,
- tombstone semantics,
- stable local HTTP host capability endpoints.

The module owns:

- `record_kind`,
- `record_id`,
- `payload`,
- interpretation and validation of payload semantics.

## Runtime Surface

The daemon exposes four module-authtok protected calls:

```text
POST /v1/module/store/records/put
POST /v1/module/store/records/get
POST /v1/module/store/records/list
POST /v1/module/store/records/delete
```

Each request carries `schema_version = "v1"` and one of:

```text
module_store_put
module_store_get
module_store_list
module_store_delete
```

as `capability_id`.

## Record Contract

Operator-visible records have this shape:

```json
{
  "record_kind": "workflow-template",
  "record_id": "story-009/blog-draft",
  "owner_participant_id": "participant:did:key:z6Mk...",
  "payload": {},
  "created_at": "2026-04-18T08:00:00Z",
  "updated_at": "2026-04-18T08:00:00Z"
}
```

The effective key is `(module_id, record_kind, record_id)`. The module never
sends `module_id`; the host derives it from the host capability binding.

## Persistence

The Node daemon persists mutations as `daemon/module-store-record.v1` records.
The stream id is derived from the effective key and encoded safely for the
commit log. Replay folds the stream into a live `BTreeMap` projection:

- put/upsert inserts the latest record,
- delete writes a tombstone and removes the live projection,
- checkpoint capture includes the live projection,
- replay after checkpoint applies tail records over that projection.

This keeps module store state aligned with the rest of daemon-owned runtime
state without adding a module-specific table.

## Story-009 Use

For Arca, the immediate use is a local workflow template store:

```text
record_kind = workflow-template
record_id   = story-009/bielik-blog
payload     = Arca-owned workflow-template JSON
```

This closes Step 0's local persistence substrate: Arca can keep templates in a
host-owned store while the daemon remains ignorant of Arca's template schema.
Dator or Agora can still publish selected templates later, but publication is a
separate catalog/federation concern.

## Boundaries

Use this store for:

- small module-local control records,
- workflow templates,
- local projections/cursors,
- operator preferences or module configuration facts.

Do not use it for:

- large artifacts,
- public federation,
- rich search,
- secrets requiring a sealer/passport gate,
- protocol-visible catalogs.

## Implementation Notes

The first implementation lives in `orbiplex-node`:

- `middleware/src/module_store.rs` defines typed request/response contracts,
- `daemon/src/endpoint_context.rs` owns live projection operations,
- `daemon/src/endpoint_routes.rs` exposes the four host capability endpoints,
- `daemon/src/state_checkpoint.rs` persists and replays the live projection,
- daemon tests cover replay upsert/tombstone behavior,
- middleware tests cover typed contract validation and serde roundtrip.

## Deferred

- JSON Schema gate files for the new module-store wire contracts.
- Generic operator UI for inspecting module store records.
- Optional schema-gated record kinds.
- Explicit publish/export path from module store records to Agora or Dator.
