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

The operator runs:

```bash
orbiplex-node keygen --out /etc/orbiplex/node.key
orbiplex-node identity show
```

The node generates a 32-byte Ed25519 seed, derives the keypair, and computes
the canonical node identity:

```
node:did:key:z6Mk...
```

Derivation follows `did:key` with multicodec prefix `0xed01` and multibase
`z` (base58btc). The identity is deterministic: the same seed always produces
the same `node:did:key`.

Key storage uses the `KeyStore` trait. The private key never leaves the backend.

```rust
trait KeyStore {
    fn sign(&self, message: &[u8]) -> Signature;
    fn public_key(&self) -> PublicKey;
    // no fn private_key() — key never leaves the backend
}
```

Key file format:

```json
{
  "schema/v": 1,
  "key/alg": "ed25519",
  "private_key_base64": "..."
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
  node_id: "node:did:key:z6Mk..."
  endpoints:
    - transport: "wss"
      host: "node1.example.com"
      port: 443
  capabilities:
    - "core/messaging"
  seq: 1
  ts: "[ISO 8601]"
  ttl: 3600
```

Wire format:

```
Wire = CBOR({
  "v":   1,
  "adv": raw_cbor_bytes(payload),
  "sig": signature
})
```

Version is covered by the signature (it is part of the domain separator) but
does not pollute the payload. Version in the wire envelope is a routing hint —
if someone tampers with it, signature verification fails.

Replacement rule: highest `seq` wins. Publishing with `seq ≤ current` is
rejected.

### Step 4: Discover

The node reads a static seed peer list from its configuration:

```yaml
discovery:
  seed_peers:
    - "node:did:key:z6MkB..."   # known peer
```

The node fetches the current advertisement for each seed peer. In this story,
the advertisement is obtained directly from the peer (no seed directory yet).

Endpoint selection:

1. Filter: reject unsupported transports.
2. Prefer: sender's ordering (hint), default QUIC > WSS > TCP.
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

After session establishment, each node sends a `signal-marker` as the first
application message. This announces capabilities and presence:

```
sign_input = "orbiplex-signal-marker-v1\x00" ‖ CBOR_deterministic(payload)
```

```yaml
signal_marker:
  from: "node:did:key:z6MkA..."
  capabilities:
    - "core/messaging"
  ts: "[ISO 8601]"
```

The signal marker is the thinnest possible application-layer handshake: "I am
here, and this is what I can do."

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
| 5 | `seq` monotonically increasing; advertisement with lower seq rejected | test: publish seq=2, then seq=1 → reject |
| 6 | Keepalive: no pong within timeout → session degraded | test: kill one peer, observe timeout on the other |
| 7 | Key storage via `KeyStore` trait, private key never leaves backend | API audit: no `fn private_key()` |
| 8 | Full action trace with timestamp and `autonomy_level: A2` | log inspection after test run |

## What This Story Does NOT Cover

- **`participant:did:key`** as a separate artifact (in MVP it shares the same
  key as `node:did:key`; enters in Story 001 with authorship in envelopes).
- **Seed directory** (HTTP API for `PUT/GET /adv/{did:key}`). Story 000 uses a
  static seed peer list. Seed directory is a separate story.
- **Nym, council, reputation** — higher layers.
- **Question routing and answer procurement** — this is Story 001.
- **Peer governor** (cold/warm/hot classification) — future optimization.
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
