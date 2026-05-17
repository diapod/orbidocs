# Orbiplex Key Delegation Passports

`Orbiplex Key Delegation Passports` is a protocol-level solution component that decouples a participant's sovereign identity key from operational capability passport signing. A participant issues a scoped `key-delegation.v1` artifact authorizing a separate proxy key (`did:key`) to sign capability passports on their behalf within explicit grant boundaries.

The component uses an **inline proof model**: proxy-signed artifacts carry a self-contained `DelegationProof` embedding the delegation passport in compact form. Verifiers validate the proof inline without fetching the full delegation passport from a remote source. The full `key-delegation.v1` passport remains the canonical artifact for registration, operator management, local signing selection, publication, and revocation feeds.

## Purpose

The component is responsible for:

- defining the `key-delegation.v1` delegation passport contract,
- providing the `DelegationProof` compact inline proof form,
- supporting participant signing context with both `Direct` and `Delegated` variants,
- managing proxy key lifecycle (generate, import, store, list, delete),
- issuing delegation passports signed by the participant key,
- building proxy-signed capability passports with embedded delegation proofs,
- verifying proxy-signed artifacts through the inline verifier path,
- exposing Seed Directory `/key` endpoints for delegation discovery,
- maintaining separate delegation and passport caches with background sync,
- exposing operator surfaces for delegation management.

## Scope

This document defines solution-level responsibilities of the Key Delegation Passports component.

It does not define:
- multi-hop delegation chains beyond the MVP single-hop guard (`max_chain_depth = 0`),
- delegation-based authorization for non-signing capabilities in MVP,
- cross-federation delegation discovery beyond Seed Directory `/key` surface,
- Node UI delegation management views (deferred to later UI iteration).

## Must Implement

### Delegation Passport Contracts

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`

Related schemas:
- `key-delegation.v1`
- `capability-passport.v1`

Responsibilities:
- define `KeyDelegationPassport` with schema version, delegation id, principal and proxy keys, grants, max_chain_depth, and expiry,
- define `DelegationProof` as the compact inline proof form embedded in proxy-signed artifacts,
- define `KeyDelegationSignature` with canonical signing under domain `key-delegation.v1`,
- validate structural integrity: principal key derives to participant id, proxy key starts with `did:key:`, delegation id starts with `delegation:key:`,
- support grant matching for wildcard `*`, `signing/capability`,
  `signing/agora-record`, and `signing/messaging-send`,
- build canonical payloads excluding both `signature` and optional `issuer_delegation`.

Status:
- `done`

### Participant Signing Context with Delegation

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/037-generic-signing-service.md`

Related schemas:
- `key-delegation.v1`
- `capability-passport.v1`

Responsibilities:
- provide `ParticipantSigningContext` with `Direct` and `Delegated` variants,
- route capability passport and issuer-revocation signing through `sign_as_participant`,
- verify proxy-signed artifacts against embedded `DelegationProof` at the inline verifier boundary,
- fall back from delegated to direct signing when no active delegation or unlocked proxy key is available.

Status:
- `done`

### Proxy Key Lifecycle and Daemon Storage

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`

Related schemas:
- `key-delegation.v1`

Responsibilities:
- generate proxy Ed25519 keypairs and derive canonical `proxy:did:key:...` identifiers,
- store proxy private keys as plaintext or `ParticipantKeyEnvelope` when passphrase-protected,
- persist `ProxyKeyRecord` and `IssuedKeyDelegationRecord` through append-only facts, startup replay, and checkpoint capture,
- expose operator HTTP surfaces for proxy key create, import, list, and delete.

Status:
- `done`

### Delegation Issuance and Passport Integration

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`

Related schemas:
- `key-delegation.v1`
- `capability-passport.v1`

Responsibilities:
- build a `KeyDelegationPassport` from operator participant identity, local node identity, proxy key, grants, and expiry,
- sign the delegation passport with the participant key,
- when issuing a proxy-signed capability passport: resolve proxy key, resolve live delegation, verify grant coverage, build `DelegationProof`, sign with `ParticipantSigningContext::Delegated`,
- embed returned `issuer_delegation` in the capability passport,
- guard full-passport MVP: reject `max_chain_depth > 0` on registration and management surfaces.

Status:
- `done`

### Delegation-Aware Passport Verification

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`

Related schemas:
- `key-delegation.v1`
- `capability-passport.v1`

Responsibilities:
- verify proxy-signed capability passports through the inline `DelegationProof` without fetching the full delegation passport from a remote source,
- verify proof principal signature with `proof.principal_key`, derive to expected participant id, check expiry,
- verify the artifact signature with `proof.proxy_key`,
- check required grant at the domain-policy boundary,
- reject `max_chain_depth > 0` at verification time.

Status:
- `done`

### Seed Directory `/key` Delegation Endpoints

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`

Related schemas:
- `key-delegation.v1`

Responsibilities:
- expose `PUT /key/{delegation_id}` for delegation publication,
- expose `GET /key/{delegation_id}` for delegation fetch,
- expose `GET /key?proxy_key=...` for proxy-key lookup,
- expose `GET /key?participant_id=...&capability=...` for grant-aware discovery,
- flow delegation revocations through the same revocation feed as passport revocations, carrying `target_id` cleanly.

Status:
- `partial`

### Delegation Cache and Background Sync

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/025-seed-directory-as-capability-catalog.md`

Responsibilities:
- maintain a separate `DelegationCache` from `PassportCache` — related but not identical semantics,
- prefetch key delegations for local signing and operator views through background sync,
- invalidate delegation cache entries on delegation revocations,
- never pass `DelegationCache` into remote capability passport signature verification — proxy-signed artifacts verify from their embedded proof.

Status:
- `done`

### Operator Delegation Management Surfaces

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`

Related schemas:
- `key-delegation.v1`

Responsibilities:
- expose daemon HTTP endpoints for proxy key lifecycle, delegation issue/publish/revoke,
- expose optional schema exposure for `key-delegation.v1`,
- keep daemon contract stable before adding Node UI delegation views.

Status:
- `partial`

## May Implement

### Multi-Hop Delegation Chains

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`

Related schemas:
- `key-delegation.v1`

Responsibilities:
- support `max_chain_depth > 0` for chained proxy delegations beyond the MVP single-hop guard,
- validate chain depth, expiry monotonicity, and grant narrowing at each hop.

Status:
- `planned`

### Node UI Delegation Management

Based on:
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/60-solutions/001-node-ui/001-node-ui.md`

Responsibilities:
- provide operator-facing UI for proxy key and delegation lifecycle management,
- surface delegation cache state in component health views.

Status:
- `planned`

## Out of Scope

- multi-hop delegation chains beyond the MVP single-hop guard,
- delegation-based authorization for non-signing capabilities in MVP,
- cross-federation delegation discovery beyond Seed Directory `/key` surface,
- the `ParticipantKeyEnvelope` passphrase-lock contract itself (see Proposal 031).

## Consumes

- `key-delegation.v1`
- `capability-passport.v1`
- `capability-passport-revocation.v1`
- `participant-bind.v1`
- Seed Directory `/revocations` feed

## Produces

- `key-delegation.v1`
- `DelegationProof` (embedded in `capability-passport.v1`)
- proxy-key and delegation records in daemon state
- Seed Directory `/key` responses
- operator management HTTP surfaces

## Related Capability Data

- `014-key-delegation-passports-caps.edn`

## Implementation Resources

- `014-key-delegation-passports-coding-guide.md` — step-by-step implementation guide
- `014-key-delegation-passports-impl.md` — implementation guidelines and layered rollout
- `014-key-delegation-passports-impl-decisions.md` — implementation decisions and trade-offs

## Notes

This solution component implements the inline proof model from Proposal 032. The key design invariant: proxy-signed artifacts are self-contained. A verifier validates the embedded `DelegationProof` without fetching the full delegation passport. The full passport is only needed for registration, management, publication, and revocation — never for online signature verification.

The component lives primarily in the `capability` crate (delegation types, grant matching, inline verification), with daemon-side storage, Seed Directory `/key` persistence, and operator HTTP surfaces. The `max_chain_depth > 0` guard is explicit at every registration, management, and verification boundary — the path for multi-hop chains is structurally prepared but intentionally blocked in MVP.
