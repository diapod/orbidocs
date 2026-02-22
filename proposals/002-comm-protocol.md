# Orbiplex Swarm Communications — Draft Notes (comm-proto)

This document summarizes the current decisions for **Orbiplex Swarm** node-to-node communication in a **mixed environment** (consumer networks + corporate networks with mandatory proxy/TLS inspection). It also includes an example handshake, a description of **Edge relaying** (routing by `node-id` with **no trust** in Edge), and a governance checklist for **`CORP_COMPLIANT`** mode.

---

## 1. Goals and constraints

### Goals
- **Reliable connectivity in mixed networks**, including strict corporate environments.
- **Optional real end-to-end confidentiality and PFS** even when transport is MITM’d by corporate proxy.
- **Sybil/DoS resistance** suitable for “hostile Internet” conditions.
- Clear separation between:
  - **Control-plane** (commands, coordination, small messages)
  - **Data-plane** (large payloads referenced by content hashes)

### Key constraints
- In corporate environments, **authorization is only via proxy** (PAC/NTLM/Kerberos is common).
- Therefore, **transport TLS may be inspected** (MITM). Transport-level “PFS” does **not** guarantee E2E privacy.
- If a client wants real confidentiality/PFS, it must be provided by **message-level E2E crypto**.

---

## 2. High-level architecture

### Node types
- **Edge nodes** (public backbone):
  - Publicly reachable (VPS), deployed across multiple regions/ASNs.
  - Provide **bootstrap / rendezvous / relay** services.
  - Apply strong **DoS controls** and admission policies.
- **Field nodes** (behind NAT/proxy):
  - Typically behind NAT or corporate proxy.
  - Maintain outbound connections to Edge nodes (most reliable path).

### Connectivity ladder (mixed networks)
1. **Outbound HTTPS/WSS over TCP 443 via system proxy** (most reliable in corp).
2. Opportunistic **direct TCP** when reachable.
3. Opportunistic **UDP hole punching (STUN)** when allowed.
4. **Relay via Edge** as the always-works fallback.

> In mixed environments, direct/NAT traversal is an optimization, not a dependency.

---

## 3. Identity model

### Base identity
- Each node has a long-term **`identity-key`** (Ed25519).
- **`node-id = H(pubkey)`** (or compatible stable derivation).
- All control-plane messages are **signed**.

### Session keys and continuity
- Nodes may use short-lived **session keys**:
  - `identity-key` signs a “session certificate” binding `session-pubkey` + validity window.
- Reputation attaches to the long-term identity; session keys reduce the blast radius of compromise.

---

## 4. Trust, Sybil, and DoS protections

### Sybil resistance (pragmatic)
Use at least one “cost of identity” mechanism:
- **Admission control (recommended for Orbiplex Swarm)**:
  - `invite/sponsor` tokens signed by existing trusted nodes.
  - Rate-limit sponsorship (per sponsor per epoch).
- Optional add-ons:
  - Lightweight **puzzle/PoW** for join/handshake bursts.
  - Deposit/stake mechanisms if you later anchor membership rules on-chain.

### DoS mitigation (“expensive before you believe”)
- **Pre-auth gate**: minimal parsing, tiny first-message limits, connection rate limits.
- **Before costly work**: require puzzle/PoW or invite token before allocating heavy resources.
- **Peer scoring and eviction**: hot/warm/cold pools; degrade/evict misbehaving peers.

---

## 5. Transport vs. end-to-end crypto

### Transport
- Primary: **HTTPS/WSS (TCP 443)**, proxy-compatible, long-lived sessions.
- TLS verification uses **system trust store** in corporate mode.

### End-to-end confidentiality / PFS (optional but crucial)
Because corporate proxy can MITM transport, real privacy requires:
- **E2E encryption at message layer** (AEAD).
- **PFS** via ephemeral ECDH (X25519) + frequent rekeying (time or message count).

---

## 6. Security profiles (client policy knob)

### `CORP_COMPLIANT` (default for corporate environments)
- Must use **system proxy only** (PAC/NTLM/Kerberos).
- Must use **system trust store** (proxy MITM is treated as “legitimate”).
- E2E is **off or opportunistic** (depending on governance).
- Messages may be plaintext **for inspection/DLP**, but **critical commands should still be signed**.

### `E2E_PREFERRED`
- Still uses proxy and system trust store.
- Attempts E2E; falls back if peer cannot.

### `E2E_REQUIRED`
- Requires E2E; if peer cannot do E2E → no session.
- Uses ephemeral key exchange + rekey schedule to guarantee PFS at message level.

---

## 7. Message envelope (control-plane)

A minimal signed envelope (serialization: EDN/JSON; canonicalization required for signing):

```text
Envelope {
  v:            int
  from:         node-id
  to:           node-id | group-id | null
  ts:           unix-ms
  ttl_s:        int
  nonce:        bytes/uuid
  seq:          u64 (per-session monotonic)
  intent:       keyword/string (mini-protocol selector)
  body:         object (small)
  e2e:          { mode, kid, ciphertext, aad, tag } | null
  sig:          signature over canonical(envelope_without_sig)
}
```

- `nonce + ttl + seq` provide replay protection.
- If `e2e` is present, `body` may be empty and all payload moves into `ciphertext` (with `aad` carrying the signed metadata).

---

## 8. Example handshake (proxy-friendly transport + optional E2E)

This handshake assumes the transport channel is already established:
- **WSS over 443 via system proxy** to an Edge node.
- Edge only forwards; it does not interpret the E2E layer.

### 8.1. Step 1 — `HELLO` (identity + capabilities)
**A → Edge → B** (or to rendezvous first, then to B)

```json
{
  "v": 1,
  "from": "nodeA",
  "to": "nodeB",
  "ts": 1700000000000,
  "ttl_s": 30,
  "nonce": "c3b2...uuid",
  "seq": 1,
  "intent": "swarm/hello",
  "body": {
    "identity_pub": "ed25519:...",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600000,
    "capabilities": {
      "transport": ["wss443-proxy"],
      "e2e": ["preferred", "required"],
      "rekey": {"messages": 2048, "minutes": 30}
    }
  },
  "sig": "ed25519sig(identity over envelope)"
}
```

Notes:
- `session_pub` is ephemeral for E2E key agreement.
- `sig` authenticates identity and binds the ephemeral key to the long-term identity.

### 8.2. Step 2 — `HELLO_ACK` (peer agrees + returns its ephemeral key)
**B → Edge → A**

```json
{
  "v": 1,
  "from": "nodeB",
  "to": "nodeA",
  "ts": 1700000000500,
  "ttl_s": 30,
  "nonce": "a91e...uuid",
  "seq": 1,
  "intent": "swarm/hello-ack",
  "body": {
    "identity_pub": "ed25519:...",
    "session_pub": "x25519:...",
    "session_valid_until": 1700003600500,
    "e2e_mode": "preferred"
  },
  "sig": "ed25519sig(identity over envelope)"
}
```

### 8.3. Step 3 — derive session keys (E2E)
Both sides compute:

```text
shared_secret = X25519(A_session_priv, B_session_pub)
prk          = HKDF-Extract(salt = H(nodeA||nodeB||nonces), IKM = shared_secret)
keys         = HKDF-Expand(prk, info="orbiplex-e2e-v1", L=key_material)
tx_key, rx_key, ... (AEAD keys)
```

Then subsequent messages carry:

- `e2e.ciphertext = AEAD_Encrypt(tx_key, nonce=seq, aad=canonical(meta), plaintext=payload)`
- `sig` still covers the envelope meta + `e2e` fields (defense-in-depth, optional).

### Rekeying (PFS strengthening)
- Rekey periodically: **every N messages or T minutes**.
- Use a new ephemeral X25519 pair; repeat `HELLO`-style key update (or a smaller `KEY_UPDATE` intent).

---

## 9. Edge relaying (routing by node-id, no trust in Edge)

### 9.1. Model
- Edge is a **rendezvous + relay**, not a trusted party.
- Edge can:
  - route frames by `to` / `node-id`,
  - apply DoS controls,
  - maintain presence tables,
  - optionally provide “mailbox” buffering (bounded).
- Edge must NOT be required to:
  - decrypt E2E payloads,
  - decide semantics of intents,
  - validate business logic.

### 9.2. Connection model
- Each Field node maintains 1–2 outbound sessions to Edge:
  - `edge_conn_id` assigned by Edge on connect.
  - Node registers presence: `(node-id -> edge_conn_id)`.

### 9.3. Relay routing algorithm (simplified)
On Edge:

```text
on frame(envelope):
  enforce_rate_limits(envelope.from, conn, ip/asn)
  if envelope.to is null:
     broadcast within allowed scope (rare; heavily limited)
  else:
     lookup dst = presence_table[envelope.to]
     if dst exists:
        forward(frame, dst)
     else:
        optionally queue in bounded mailbox OR return "peer/offline"
```

**Security properties**
- Edge sees metadata (unless you also wrap metadata), but cannot read payload under E2E.
- Integrity and authentication come from signatures and/or E2E AEAD.
- Replay protection is enforced by endpoints (nonce/seq/ttl), not by Edge.

### 9.4. Rendezvous / discovery
- Nodes can ask Edge for “who is currently present in namespace X?” (subject to policy).
- Edge responses are treated as **hints**; endpoints still authenticate peers via signatures.

---

## 10. `CORP_COMPLIANT` governance checklist (“what is allowed”)

Use this as a policy checklist for corporate governance / security review.

### Network egress / proxy
- [ ] Client uses **system proxy only** (PAC / OS proxy settings).
- [ ] No direct outbound connections unless explicitly permitted.
- [ ] Only standard ports: **TCP 443** (and optionally 80 for proxy discovery if required).
- [ ] DNS usage follows corporate policy (no custom resolvers unless allowed).

### TLS / certificates / inspection
- [ ] TLS verification uses **system trust store**.
- [ ] No certificate pinning that would bypass legitimate corporate TLS inspection (unless a separate approved profile exists).
- [ ] TLS versions follow corporate baseline (typically TLS 1.2+; prefer TLS 1.3).

### Content visibility / DLP
- [ ] Payload visibility is configurable:
  - `observable` (plaintext application payload) allowed for inspection/DLP.
  - `opaque` (E2E encrypted payload) only if governance explicitly allows it.
- [ ] Even in `observable`, **critical control-plane commands are signed** to prevent spoofing/replay.

### Authentication and identity
- [ ] Node identity uses cryptographic keys; keys are stored securely (OS keychain/keystore where possible).
- [ ] Key rotation supported (session keys, rekey).
- [ ] Admission control mode documented:
  - invites/sponsors, allowlists, or managed enrollment.

### Logging and audit
- [ ] Client logs are configurable and follow corporate retention rules.
- [ ] No sensitive plaintext is logged by default.
- [ ] Edge nodes provide operational metrics and audit trails for routing events (metadata only).

### Safety controls
- [ ] Rate limiting and abuse controls are in place on Edge and client.
- [ ] Graceful degradation: if E2E is disallowed by governance, system runs in `CORP_COMPLIANT` without breaking connectivity.
- [ ] Clear UI/CLI indication of the active security profile.

---

## 11. Practical recommendation (implementation order)
1. Define **canonical envelope** + signing + replay protection.
2. Implement **WSS/HTTP2 transport on 443 via system proxy**.
3. Implement **Edge presence + relay** (no-trust pipe).
4. Add **E2E mode** (preferred → required) with rekey schedule.
5. Add **admission control** (invite/sponsor) + DoS gates.
6. Add optional direct/UDP paths later (optimization only).

---

## Appendix: Why IRC is not the core bus here
IRC is useful as a **bootstrap/fallback bulletin board** (presence, endpoints, pubkeys), but not as the primary control-plane:
- weak identity and authorization model,
- limited delivery guarantees and backpressure,
- operational/security optics (often associated with legacy C2),
- not proxy-governance friendly as a primary corporate channel.

Use IRC/Matrix only as *bootstrap hints* if you want an “apocalypse fallback”.
