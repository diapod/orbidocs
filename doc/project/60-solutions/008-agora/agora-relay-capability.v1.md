# Capability scope: `agora.relay`

## Purpose

Metadata carried in the `scope` field of a `capability-passport.v1` for the
`agora.relay` capability. It describes the relay's public reachability,
federation role, supported transports, and topic coverage.

The capability passport answers: "this Node is officially authorized by the
operator to offer an Agora relay with this externally visible shape." It is
separate from the middleware module report, which only says that the supervised
process can provide the `agora.relay` capability locally.

## Shape

| Field | Type | Required | Description |
|---|---|---|---|
| `endpoint` | string, URL | yes | Public HTTP API base URL for the Agora relay. |
| `role` | enum: `canonical`, `cache`, `origin`, `local` | yes | Relay role. `local` claims durable local admission, not Matrix distribution. |
| `canonical_topics` | string array | when `role = canonical` | Topic keys for which the relay is authoritative. Empty for non-canonical roles. |
| `relay_domain` | string | yes | Domain used for Matrix room alias resolution. Retained for shape compatibility in local mode; it does not claim a Matrix alias there. |
| `transport` | string array | yes | Supported transport. `matrix` denotes Matrix distribution; `http` with `role = local` denotes the local relay API only. Future value: `peer-message`. |
| `api_version` | string | yes | Agora HTTP API version. Current value: `1`. |

## Discovery

Other nodes query the Seed Directory for the passport-backed capability:

```http
GET /cap?capability=agora.relay
```

The response includes advertisements whose passport scope follows this shape.
A discovering node can filter by `role`, `transport`, or specific
`canonical_topics` before deciding which relay to contact.

## Example

```json
{
  "endpoint": "https://relay.example.org:47991",
  "role": "canonical",
  "canonical_topics": ["ai.orbiplex.proposals/035"],
  "relay_domain": "example.org",
  "transport": ["matrix"],
  "api_version": "1"
}
```

## Operational notes

An explicitly configured `local-sqlite` service reports `role = local`,
`transport = ["http"]` and no canonical topics. Its ingest receipt attests
only to the local SQLite admission. Remote discovery, peer connectivity and
delivery need their own evidence; HTTP reachability is not Matrix federation.
Missing Matrix credentials never select this mode implicitly.

If the passport is absent, Agora may still operate as a local relay. The
absence only means it is not discoverable as an officially authorized network
relay through the Seed Directory.
