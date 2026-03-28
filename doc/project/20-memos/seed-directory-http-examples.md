# Seed Directory HTTP Examples

Based on:
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/50-requirements/requirements-006.md`
- `doc/schemas/node-advertisement.v1.schema.json`

## Status

Draft

## Date

2026-03-28

## Purpose

This memo freezes minimal HTTP request and response examples for the optional
seed-directory extension described in the Node networking MVP.

The goal is not to introduce a large REST surface. The goal is to remove
wire-level guesswork for the first implementation.

## Contract Shape

The minimal seed-directory contract stays narrow:

- `PUT /adv/{node-id}`
- `GET /adv/{node-id}`
- `GET /adv?since={cursor}`

The directory behaves as a signed cache:

- request bodies carry signed `node-advertisement.v1` artifacts,
- `GET /adv/{node-id}` returns the current stored advertisement artifact,
- `GET /adv?since={cursor}` returns a bounded batch wrapper,
- explicit delete remains unsupported.

## Example: Publish Or Replace

### Request

```http
PUT /adv/node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE HTTP/1.1
Host: seed-01.orbiplex.ai
Content-Type: application/json

{
  "schema/v": 1,
  "advertisement/id": "adv:01JQNODEADV001",
  "node/id": "node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "sequence/no": 17,
  "advertised-at": "2026-03-23T18:08:00Z",
  "expires-at": "2026-03-23T18:18:00Z",
  "key/alg": "ed25519",
  "key/public": "z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "federation/id": "fed:orbiplex-pl",
  "endpoints": [
    {
      "endpoint/url": "wss://node-01.docs.orbiplex.ai/peer",
      "endpoint/transport": "wss",
      "endpoint/role": "listener",
      "endpoint/priority": 0
    }
  ],
  "transports/supported": ["wss"],
  "signature": {
    "alg": "ed25519",
    "value": "GGxfc1fHLYqoUhSygpyHSl_yKuilR2YsCx1peziDLhGLXfO2YQz9IXGU4VMDWnh-Zwltk0D-JXnO1IeF1GZMAQ"
  }
}
```

### `201 Created`

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "status": "stored",
  "node/id": "node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "advertisement/id": "adv:01JQNODEADV001",
  "sequence/no": 17,
  "stored-at": "2026-03-23T18:08:03Z",
  "expires-at": "2026-03-23T18:18:00Z"
}
```

### `409 Conflict`

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "status": "conflict",
  "reason": "stale-sequence",
  "node/id": "node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "current/sequence-no": 17,
  "submitted/sequence-no": 16
}
```

## Example: Fetch By Node

### Request

```http
GET /adv/node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE HTTP/1.1
Host: seed-01.orbiplex.ai
Accept: application/json
```

### `200 OK`

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "schema/v": 1,
  "advertisement/id": "adv:01JQNODEADV001",
  "node/id": "node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "sequence/no": 17,
  "advertised-at": "2026-03-23T18:08:00Z",
  "expires-at": "2026-03-23T18:18:00Z",
  "key/alg": "ed25519",
  "key/public": "z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
  "federation/id": "fed:orbiplex-pl",
  "endpoints": [
    {
      "endpoint/url": "wss://node-01.docs.orbiplex.ai/peer",
      "endpoint/transport": "wss",
      "endpoint/role": "listener",
      "endpoint/priority": 0
    }
  ],
  "transports/supported": ["wss"],
  "signature": {
    "alg": "ed25519",
    "value": "GGxfc1fHLYqoUhSygpyHSl_yKuilR2YsCx1peziDLhGLXfO2YQz9IXGU4VMDWnh-Zwltk0D-JXnO1IeF1GZMAQ"
  }
}
```

### `404 Not Found`

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{
  "status": "not-found",
  "node/id": "node:did:key:z6Mkunknownpeer1111111111111111111111111111111"
}
```

## Example: Incremental Batch

### Request

```http
GET /adv?since=cur:01JQNODECUR001 HTTP/1.1
Host: seed-01.orbiplex.ai
Accept: application/json
```

### `200 OK`

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "items": [
    {
      "schema/v": 1,
      "advertisement/id": "adv:01JQNODEADV001",
      "node/id": "node:did:key:z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
      "sequence/no": 17,
      "advertised-at": "2026-03-23T18:08:00Z",
      "expires-at": "2026-03-23T18:18:00Z",
      "key/alg": "ed25519",
      "key/public": "z6MkwJFpvJVFe15ygGgYLTYuiPwfhkkDRkMG4eKQFT8g65yE",
      "endpoints": [
        {
          "endpoint/url": "wss://node-01.docs.orbiplex.ai/peer",
          "endpoint/transport": "wss",
          "endpoint/role": "listener",
          "endpoint/priority": 0
        }
      ],
      "transports/supported": ["wss"],
      "signature": {
        "alg": "ed25519",
        "value": "GGxfc1fHLYqoUhSygpyHSl_yKuilR2YsCx1peziDLhGLXfO2YQz9IXGU4VMDWnh-Zwltk0D-JXnO1IeF1GZMAQ"
      }
    }
  ],
  "next": "cur:01JQNODECUR002",
  "max-items": 100
}
```

## Notes

- The request body for `PUT` is the raw `node-advertisement.v1` artifact rather
  than a wrapper.
- `GET /adv/{node-id}` returns the raw current artifact for direct cache fill.
- `GET /adv?since={cursor}` uses a small wrapper because batches need both
  `items` and a continuation cursor.
- The memo does not yet freeze OpenAPI, headers such as `ETag`, or exact retry
  headers for rate limiting.
