# Memarium HOWTO

This document leads operators and middleware authors through the basic
Memarium path: selecting a space, preparing authority, writing or reading,
inspecting quarantine, declassifying, archiving, and handling Crisis findings.

It is not a second domain-model specification. Contracts and the closed error
vocabulary belong to [Solution 002](../../project/60-solutions/002-memarium/002-memarium.md),
while conceptual answers belong to the [Memarium FAQ](../faq/memarium-faq.en.md).

## Before performing an operation

Establish four things:

1. **Space** – Personal, Community, Public, or Crisis.
2. **Classification** – an explicit `classification.v1`, separate from the payload.
3. **Caller** – operator, local module, or delegate bound to a concrete subject.
4. **Effect** – write, read, promote, forget, declassify, quarantine, archive,
   or resolve a Crisis finding.

If one of these cannot be established, do not replace it with a default. Missing
authority or classification is a refusal or quarantine state, not permission.

## 1. Choose the space

| Space | Use it when | Do not use it as |
| :--- | :--- | :--- |
| Personal | material belongs to the operator's memory and should remain local | a drawer for module data that nobody classified |
| Community | material belongs to a concrete community and carries `community_id` | shorthand for "several people" or a Room |
| Public | material may be public after crossing the appropriate egress gate | an automatic destination for unlabeled data |
| Crisis | material has constitutional emergency significance | a general alert queue or log store |

Community replication is bounded to a shared, verified federation. Sharing
outside it requires explicit promotion and ordinary artifact transport; Room
membership does not widen the space policy.

## 2. Enable and inspect Memarium

Memarium is an in-process daemon subsystem. A typical configuration enables the
subsystem and its rebuildable read sidecar. After changing configuration, run:

```sh
cargo run -p orbiplex-node-daemon -- check-config \
  --data-dir "$ORBIPLEX_DATA_DIR"
```

Then start the daemon and inspect its normal operator status. When Memarium is
disabled or storage cannot open, the host capability returns
`memarium_unavailable` or `storage_unavailable`; do not bypass the gate by
writing directly to files.

## 3. Grant the caller a minimal passport

A module needs a passport matching all of the following:

- `capability_id`, for example `memarium.write`;
- caller binding;
- grant, for example `memarium/write`;
- space and optional `community_id`;
- optional `entry_kind`;
- the current fresh revocation view.

The full preview → sign and install → verify flow is documented in
[Memarium Capability Passport Issuance](../memarium-passport-issuance.md).
A bundled publisher template is only a recommendation. It becomes executable
authority only when local policy issues or installs a passport.

After installation, verify the passport through the operator surface or launcher:

```sh
orbiplex-node-launcher capability-passport-verify \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --file ./memarium-passport.json
```

## 4. Write a classified entry

Use the canonical
[`write-entry.memarium-host-api.json`](../../schemas/examples/write-entry.memarium-host-api.json)
example as the starting point. Do not remove `classification` or move it into
`attributes`. Set `ORBIPLEX_DOCS` to the root of the `orbidocs/` checkout before
running the command; the daemon may run from a different workspace.

```sh
# Run this assignment from the root of the orbidocs checkout.
export ORBIPLEX_DOCS="$PWD"

curl -sS -X POST \
  "$ORBIPLEX_NODE/v1/host/capabilities/memarium.write" \
  -H "X-Orbiplex-Authtok: $MODULE_AUTHTOK" \
  -H 'Content-Type: application/json' \
  --data @"$ORBIPLEX_DOCS/doc/schemas/examples/write-entry.memarium-host-api.json"
```

A successful response carries `status: "ok"` and a stable entry or fact id.
Repetition under the same canonical key should converge to the same effect; do
not derive idempotency from a clock or descriptive label.

### Write a fact instead of an entry

A fact is an append-only event or assertion. Use `op: "write_fact"` and an
explicit `fact_kind`. An entry is a material memory item, while a fact describes
history, a decision, or a relationship. Do not overwrite a fact to "fix state" –
append a correcting fact and let the read model compose the current view.

## 5. Read entries or facts

Reads also cross the passport gate:

```json
{
  "op": "query_facts",
  "request": {
    "space": "personal",
    "query": {
      "fact_kind": "example.fact.v1",
      "any_tag": ["example"],
      "limit": 50,
      "order_by": "created-at-asc"
    }
  }
}
```

Send the document to `POST /v1/host/capabilities/memarium.read`. Add
`community_id` for Community. Use an explicit bounded `limit`; the SQLite
projection accelerates the query but does not widen read authority.

## 6. Handle a quarantined record

List pending facts first:

```sh
orbiplex-node-launcher memarium quarantine list \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --limit 50
```

Then make one explicit decision:

```sh
orbiplex-node-launcher memarium quarantine accept \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --fact-id 'fact:personal:...' \
  --reason 'Source and classification verified.'
```

or:

```sh
orbiplex-node-launcher memarium quarantine reject \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space personal \
  --fact-id 'fact:personal:...' \
  --reason 'Classification provenance cannot be verified.'
```

Acceptance and rejection are policy facts. They do not remove the source
record. Repeating a terminal decision must be idempotent or return an explicit
conflict, not produce a second independent decision.

## 7. Permit narrower egress through declassification

Declassify only for a concrete surface and topic class. The safest default is
`one-shot`; use TTL only when repeated effects are genuinely part of policy.

```sh
orbiplex-node-launcher memarium declassify \
  --data-dir "$ORBIPLEX_DATA_DIR" \
  --space community \
  --community-id wroclaw-mutual-aid \
  --entry-kind resource-note \
  --fact-id 'fact:community:...' \
  --from-tier Community \
  --to-tier Public \
  --surface agora \
  --topic-class mutual-aid \
  --reason 'Reviewed for this public projection.'
```

Do not expect an ordinary context-free read to expose a lower
`effective_tier`. The contextual egress adapter composes the trail for its exact
surface and current revocation view.

## 8. Forget or promote material

`memarium.forget` and `memarium.promote` are separate host capabilities because
they change availability or the policy envelope. Before invoking either, verify:

- the space permits this transition;
- the passport covers the exact target;
- Community forget carries a valid `governance_ref`;
- Public forget leaves the required tombstone;
- Crisis is not treated as ordinary operator retention.

Promotion creates a new provenance fact. It does not mutate a record in place
and cannot be a side effect of Room, Agora, or Artifact Delivery.

## 9. Prepare a backup and archival handoff

The local operator starts a backup through:

```http
POST /v1/memarium/backups
```

After success, inspect its manifest:

```http
GET /v1/memarium/backups/{backup_id}
```

An archivist handoff uses:

```http
POST /v1/memarium/archival/handoffs
```

Retrieval starts through:

```http
POST /v1/memarium/archival/retrievals
```

Backup builds a complete staging bundle before atomic promotion. Handoff
preflights every package and uses Artifact Delivery. Partial failure remains
visible in append-only facts; do not turn it into an apparent global success.

## 10. Inspect and resolve a Crisis finding

Read status through `memarium.crisis_status` or the Node's operator view. Then
follow the appropriate section of the
[Crisis Detectors Runbook](../runbooks/crisis-detectors.md). Forced resolution
is justified only after the operator understands the source condition and
provides a bounded reason.

`memarium.crisis_resolve` appends an `operator-forced` fact. It does not remove
`crisis-detected`, and the detector may report the problem again after a full
false → true cycle.

## 11. Diagnose by error class

| Status | Check first |
| :--- | :--- |
| `passport_lookup_failed` | whether the passport was installed, not merely issued |
| `binding_mismatch` | caller identity and `allowed_callers` |
| `revocation_stale` | revocation sources and their freshness budget |
| `classification_missing` | the first-class `classification` field |
| `quarantined` | the queue and any existing operator decision |
| `space_policy_violation` | encryption, retention, and space rules |
| `storage_unavailable` | storage state and read-sidecar diagnostics |

`reason` is for people; automation should use `status`, `retryable`, and the
correlation id. Retry only errors explicitly classified as retryable.

## 12. Exercise the acceptance path

Story 005 covers a classified private AD/INAC path that touches Memarium.
Component tests cover the four spaces, policy facts, observer rules, archival,
Crisis, and sidecar rebuild. After operator configuration changes, run at least:

```sh
cargo test -p orbiplex-node-memarium
cargo test -p orbiplex-node-memarium-runtime
cargo test -p orbiplex-node-memarium-read-sidecar
cargo test -p orbiplex-node-daemon memarium
```

The final check should answer three questions: was the effect authorized before
the write, did the source fact remain immutable, and can the operator recover
the decision cause without reading secrets from logs?
