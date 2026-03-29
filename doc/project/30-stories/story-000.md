# Story 000: Two Nodes See Each Other

## Summary

As a node operator, I want to launch a node that generates its identity,
advertises itself, discovers another node, establishes an authenticated session,
and exchanges capabilities — so that I have end-to-end proof that the
foundation works.

## Current Baseline Used by This Story

This story is grounded in:

- the identity and transport design from Proposal 014 and the design notes,
- the conformance vectors from `networking-signing-conformance-vectors.md`,
- the node identity layering from `node-identity-layering-and-upgrade-path.md`,
- the key storage contract from GENYM section 9.

This story covers the **minimum vertical slice** of the Orbiplex node: identity,
transport, discovery, handshake, capability exchange, and liveness. Everything
above this layer (participants, questions, rooms, nyms, reputation) depends on
this story being complete and frozen.

## Sequence of Steps

### Step 1: Key Generation

The operator launches the daemon for the first time and then inspects the local
control surface:

```bash
orbiplex-node-daemon run --data-dir ./var/orbiplex-node
python3 tools/orbiplex-node-control.py --data-dir ./var/orbiplex-node status
```

On first open, the node generates a local Ed25519 keypair and computes the
canonical infrastructure and participation identities:

```
node:did:key:z6Mk...
participant:did:key:z6Mk...
```

Derivation follows a strict `did:key`-compatible Ed25519 fingerprint shape with
multicodec prefix `0xed01` and multibase `z` (base58btc). The derivation is
deterministic: the same key material always produces the same `node:did:key`
and `participant:did:key`.

The canonical public identity contract carries a resolver-friendly
`key/storage-ref` rather than inline secret material. The private key is stored
locally in a separate signing-key record and never leaves the backend.

Canonical identity contract:

```json
{
  "schema/v": 1,
  "node/id": "node:did:key:z6Mk...",
  "participant/id": "participant:did:key:z6Mk...",
  "key/alg": "ed25519",
  "key/public": "z6Mk...",
  "key/storage-ref": "local-file:identity/node-signing-key.v1.json"
}
```

### Step 2: Listen

The node starts listening on WSS (WebSocket Secure) on a configurable port
(default: 443).

TLS serves as carrier transport only (server authentication + channel
integrity). Node identity binding happens at the handshake layer, not at the
TLS layer.

### Step 3: Advertise

The node publishes a signed advertisement:

```
sign_input = "orbiplex-node-advertisement-v1\x00" ‖ CBOR_deterministic(payload)
```

Advertisement payload:

```yaml
advertisement:
  advertisement_id: "adv:..."
  node_id: "node:did:key:z6Mk..."
  sequence_no: 1
  advertised_at: "[ISO 8601]"
  expires_at: "[ISO 8601]"
  key_alg: "ed25519"
  key_public: "z6Mk..."
  endpoints:
    - endpoint_url: "wss://node1.example.com/peer"
      endpoint_transport: "wss"
      endpoint_role: "listener"
      endpoint_priority: 0
  transports_supported:
    - "wss"
```

Replacement rule: highest `sequence/no` wins. Publishing with
`sequence/no ≤ current` is
rejected.

### Step 4: Discover

The node reads a static seed peer list from its configuration:

```yaml
discovery:
  seed_peers:
    - node_id: "node:did:key:z6MkB..."
      endpoint_url: "wss://seed-01.example.com/peer"
      name: "seed-local"
```

The node maintains a local advertisement cache and a state-driven outbound
dialer. In this story there is still no seed directory: the dialer starts from
static seeds, caches signed advertisements, and then ranks connection attempts
using seed-floor policy plus cooldown/backoff state.

Endpoint selection:

1. Filter: reject unsupported transports.
2. Prefer: sender-advertised endpoint priority among compatible endpoints.
3. Try: probe first compatible, fallback to next.

### Step 5: Handshake

The initiator sends a `hello`, the responder replies with an `ack`. Two
messages, one round trip.

```
Initiator (Alice)                              Responder (Bob)
    │                                              │
    │  ── hello ──────────────────────────────────>│
    │  {id, from, to, ek, nonce, ts, caps, terms}  │
    │  + sig (Ed25519, Alice's IK)                 │
    │                                              │
    │  <────────────────────────────── ack ────────│
    │  {id, from, to, ek, nonce, ts,               │
    │   ack-of: Alice's hello id, caps, terms}     │
    │  + sig (Ed25519, Bob's IK)                   │
    │                                              │
    ╞══════════════════════════════════════════════╡
    │        session key derivation                │
    │  DH1 = X25519(EK_Alice, IK_Bob)              │
    │  DH2 = X25519(IK_Alice, EK_Bob)              │
    │  DH3 = X25519(EK_Alice, EK_Bob)              │
    │  SK = HKDF-SHA256(salt, ikm, info)           │
```

Domain separation:

```
sign_input = "orbiplex-peer-handshake-v1\x00" ‖ CBOR_deterministic(payload)
```

Schema:

```yaml
PeerHandshake:
  id: "[unique handshake id]"
  from: "node:did:key:z6MkA..."
  to: "node:did:key:z6MkB..."
  ek: "[32 bytes, raw X25519 ephemeral public key]"
  nonce: "[32 bytes random]"
  ts: "[unix timestamp]"
  ack-of: null           # present ONLY in ack
  caps: ["core/messaging"]
  terms: {}
```

The `ek` field is a raw 32-byte X25519 public key: not multicodec-prefixed, not
Ed25519, not `did:key`. It is single-use and does not constitute identity.

Ed25519 identity keys are converted to X25519 for DH1/DH2 via the standard
deterministic conversion (`crypto_sign_ed25519_pk_to_curve25519`). Fresh
ephemeral X25519 keys provide DH3 (forward secrecy).

### Step 6: Replay Guard

| Condition | Rejection |
| :--- | :--- |
| `ts` outside ±30s | `REJECT_CLOCK_SKEW` |
| `nonce` seen from the same `from` | `REJECT_REPLAY` |
| `ack-of` does not match pending hello | `REJECT_UNKNOWN_HANDSHAKE` |
| `to` ≠ my `did:key` | `REJECT_WRONG_RECIPIENT` |
| `sig` does not verify | `REJECT_BAD_SIGNATURE` |
| `from` on blocklist | `REJECT_BLOCKED` |
| `caps` without minimum (`core/messaging`) | `REJECT_INSUFFICIENT_CAPS` |

Nonce cache: per-peer LRU, TTL = 120s. Pending handshake timeout: 30s.

### Step 7: Signal Marker

After session establishment, each node sends a participant-scoped
`SignalMarkerEnvelopeV1` as the first signed application message over the
encrypted channel:

```
sign_input = "orbiplex-signal-marker-v1\x00" ‖ CBOR_deterministic(payload)
```

```yaml
signal_marker_envelope:
  message_id: "msg:..."
  protocol_version: "0.1.0"
  message_kind: "signal-marker-envelope.v1"
  sender_participant_id: "participant:did:key:z6MkA..."
  created_at: "[ISO 8601]"
  marker_ref: "signal-marker:..."
```

The signal marker is the thinnest possible application-layer handshake: "I am
here as this participant role, and the channel is usable."

### Step 8: Keepalive

The session is maintained via periodic `ping/pong` messages:

- interval: configurable (default: 30s)
- timeout: configurable (default: 90s, i.e. 3 missed pongs)
- missed pong → session degraded → reconnect attempt

## Acceptance Criteria

| # | Criterion | Verification |
| :--- | :--- | :--- |
| 1 | `node:did:key` deterministically derived from 32B seed | conformance vector |
| 2 | Advertisement signed, deterministic CBOR, domain sep `"orbiplex-node-advertisement-v1\x00"` | byte-exact vector from `networking-signing-conformance-vectors.md` |
| 3 | Handshake hello→ack with replay guard (`ts ±30s`, `nonce` cache, `ack-of` binding) | conformance vector |
| 4 | Session key derivation: `3×DH → HKDF-SHA256 → ChaCha20-Poly1305` | test: two processes on localhost, exchange encrypted signal-marker |
| 5 | `sequence/no` monotonically increasing; advertisement with lower or equal sequence is rejected as stale | test: cache seq=10, then publish seq=10 or seq=9 → reject |
| 6 | Keepalive: no pong within timeout → session degraded | test: kill one peer, observe timeout on the other |
| 7 | Canonical identity contract exports `key/storage-ref` only; secret key material remains in a separate local signing-key record | daemon export/load test + file inspection |
| 8 | Full action trace exists in `trace/network` and includes identity, handshake, session, capability, signal-marker, and keepalive events | log inspection after test run |

## What This Story Does NOT Cover

- **Hosted users and richer post-channel participant attachment** — Story 000
  stops at the one-operator-per-node baseline plus the first participant-scoped
  signal marker.
- **Seed directory** (HTTP API for `PUT/GET /adv/{did:key}`). Story 000 uses a
  static seed peer list. Seed directory is a separate story.
- **Nym, council, reputation** — higher layers.
- **Question routing and answer procurement** — this is Story 001.
- **Full peer governor policy** beyond the minimal `cold/hot/cooldown/blocked`
  runtime baseline and replay-driven blocking.
- **Bloom filter gossip** — future optimization.

## Architectural Significance

Story 000 freezes the **entire cryptographic and transport stack**. Conformance
vectors from this stage become the interoperability contract — every future
implementation (Rust, JVM, JS) must pass them. This is the minimal trusted core
in the runtime sense.

## References

- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/20-memos/node-identity-layering-and-upgrade-path.md`
- `doc/project/20-memos/networking-signing-conformance-vectors.md`
- `doc/project/50-requirements/requirements-006.md`
