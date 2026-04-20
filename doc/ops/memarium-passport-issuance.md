# Memarium Capability Passport Issuance

Memarium passport issuance is the operator workflow for granting a local or
delegated module access to Memarium without ambient daemon authority. The
passport is the signed data contract; the dispatch gate consumes it before the
Memarium runtime sees the request.

This document intentionally separates two surfaces:

- `POST /v1/host/capabilities/capability.passport.issue` signs and returns a
  passport through the middleware host-capability contract. It does not by
  itself install the returned passport into the local dispatch source.
- `POST /v1/host/capabilities/capability.passport.sign` is the local operator
  control flow. It signs the passport, stores it in the daemon's issued-passport
  store, and refreshes the local dispatch passport source.

For the local Memarium MVP, "issue and install" means the second flow unless an
external operator tool explicitly persists the passport-present artifact and
reloads the daemon passport source.

## Three-Stage Flow

### Stage 1: Preview

The operator first prepares the scope and checks that it is minimal enough for
the intended module. Preview can be implemented in `orbictl` or UI by evaluating
the scope profile before signing.

Example scope:

```json
{
  "allowed_callers": [
    {
      "kind": "http-module",
      "label": "agora-service",
      "subject_key": "did:key:module:agora-service"
    }
  ],
  "profiles": [
    {
      "profile": "memarium-space-access@v1",
      "grants": {
        "memarium/read": ["community"],
        "memarium/write": ["community"]
      },
      "spaces": ["community"],
      "community_ids": ["wroclaw-mutual-aid"],
      "entry_kinds": ["procedure", "contact", "resource-note"],
      "max_revocation_staleness_seconds": 300
    }
  ]
}
```

### Stage 2: Sign And Install

Use the local operator control endpoint when the passport should become active
on this daemon immediately.

```http
POST /v1/host/capabilities/capability.passport.sign
X-Orbiplex-Authtok: <control-authtok>
Content-Type: application/json
```

```json
{
  "node_id": "node:did:key:z6Mk...",
  "capability_id": "memarium-space-access",
  "expires_at": "2027-04-19T12:00:00Z",
  "scope": {
    "allowed_callers": [
      {
        "kind": "http-module",
        "label": "agora-service",
        "subject_key": "did:key:module:agora-service"
      }
    ],
    "profiles": [
      {
        "profile": "memarium-space-access@v1",
        "grants": {
          "memarium/write": ["public"]
        },
        "spaces": ["public"],
        "entry_kinds": ["agora-record"],
        "max_revocation_staleness_seconds": 300
      }
    ]
  }
}
```

Successful response is a `capability-passport.v1` document. The daemon also
stores it in the issued-passport store and refreshes local dispatch lookup.

```json
{
  "schema": "capability-passport.v1",
  "passport_id": "passport:capability:memarium-space-access:01JR...",
  "node_id": "node:did:key:z6Mk...",
  "capability_id": "memarium-space-access",
  "scope": { "...": "..." },
  "issued_at": "2026-04-19T14:30:00Z",
  "expires_at": "2027-04-19T12:00:00Z",
  "issuer/participant_id": "participant:did:key:z6Mk...",
  "issuer/node_id": "node:did:key:z6Mk...",
  "issuer/delegation": null,
  "revocation_ref": null,
  "signature": {
    "alg": "ed25519",
    "value": "..."
  }
}
```

### Stage 3: Verify Active

First confirm that the daemon lists the issued passport:

```http
GET /v1/host/capabilities/capability.passports
X-Orbiplex-Authtok: <control-authtok>
```

Then make a real Memarium host-capability request as the module. Module calls
authenticate with `X-Orbiplex-Module-Authtok`; the passport itself is selected
from the dispatch passport source by `(caller_label, capability_id)`.

```http
POST /v1/host/capabilities/memarium.write
X-Orbiplex-Module-Authtok: <module-authtok>
Content-Type: application/json
```

```json
{
  "op": "write_entry",
  "request": {
    "space": "public",
    "artifact_kind": "agora-record",
    "tags": ["agora-record"],
    "attributes": {},
    "payload": {
      "encoding": "plaintext-json",
      "media_type": "application/json",
      "body": { "text": "public note" },
      "encryption": null
    },
    "occurred_at": null
  }
}
```

Expected success is `200 OK` with the written entry. A denied request returns a
stable Memarium reason code such as `no_profile_matched`, `revoked`, or
`revocation_stale`.

## Scope Constraints

`allowed_callers` binds a passport to local caller identity:

- `kind: "http-module"` for daemon-supervised middleware modules using
  `X-Orbiplex-Module-Authtok`;
- `kind: "operator"` or `kind: "participant"` for in-process/operator flows;
- `label` must match the local caller label used by dispatch lookup;
- `subject_key` must match the caller binding resolved by the daemon.

`memarium-space-access@v1` profile constraints:

- `grants`: operation namespace to allowed spaces, for example
  `"memarium/write": ["community"]`;
- `spaces`: allowed Memarium spaces;
- `community_ids`: optional, but required by HTTP target-bearing operations when
  `space == "community"`;
- `entry_kinds`: optional filter for entry-kind-bearing operations;
- `max_revocation_staleness_seconds`: maximum acceptable age of the revocation
  view for this profile.

## Denial Reasons

Memarium host-capability responses expose stable `status` codes. The most common
passport-flow failures are:

| Status | HTTP | Meaning |
| :--- | :--- | :--- |
| `passport_lookup_failed` | 403 | No passport was found for the caller and Memarium capability. |
| `passport_invalid` | 403 | The passport signature or structure failed validation. |
| `passport_expired` | 403 | The passport is outside its validity window. |
| `binding_mismatch` | 403 | The passport subject does not bind to the caller. |
| `allowed_callers_mismatch` | 403 | The caller is not present in `allowed_callers`. |
| `no_profile_matched` | 403 | No profile matched the requested grant and target axes. |
| `revocation_stale` | 503 | The revocation view is older than the accepted budget. |
| `revoked` | 410 | The passport id or delegated target id is revoked. |

Clients should branch on `status` and treat free-form `reason` as diagnostic
text only.

## Idempotency

`capability.passport.sign` is not content-addressed: repeated signing of the
same scope can produce a new `passport_id`. Operator tooling that needs retry
idempotency should persist the returned `passport_id` and treat subsequent
verification/listing as the source of truth.

## Revocation

Local revocation is recorded in the daemon's revocation source. Federated
revocations can arrive through configured revocation sources such as static
files or Seed Directory adapters. A Memarium request must be denied when the
selected passport id or delegation `target_id` is present in the effective
revocation view.

## Operational Checklist

1. Import or unlock the sovereign operator key.
2. Prepare the minimal `memarium-space-access@v1` scope.
3. Sign through `capability.passport.sign` when the passport should become
   active locally.
4. Verify the issued passport appears in `capability.passports`.
5. Exercise a real Memarium request with the module authtok.
6. Confirm negative cases for ungranted space, community id, and entry kind.

## See Also

- [Proposal 032: Key Delegation Passports](../project/40-proposals/032-key-delegation-passports.md)
- [Memarium solution](../project/60-solutions/memarium.md)
- [Memarium classification](./memarium-classification.md)
