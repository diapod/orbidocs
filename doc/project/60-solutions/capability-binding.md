# Orbiplex Capability Binding

`Orbiplex Capability Binding` is the local authorization organ of an Orbiplex
Node. It sits above Sealer and Signer engines and below the daemon's
dispatch, composing three inputs into one deterministic outcome: a resolved
`CallerIdentity`, a `capability-passport.v1` carrying typed key-use profiles,
and a local `RevocationView`.

Capability Binding owns the binding step: caller → subject key → passport
match → freshness check → `Authorized` or `Denied`. It does not own passport
artifacts (that is the `capability` crate), it does not own caller
authentication (that is the daemon's HTTP authtok resolver or the in-process
caller registry), and it does not own cryptographic operations (that is
Sealer and Signer). The entire purpose is to keep passport semantics out of
the cryptographic services and out of the daemon's transport layer, so that
each layer stays readable on its own terms.

## Purpose

The component is responsible for the solution-level execution path of:

- resolving a `CallerIdentity` into a `CallerBinding` that names subject
  kind, subject id, and subject public keys,
- verifying `capability-passport.v1` signature, expiry, and issuer
  constraints,
- matching the requested `(grant_type, target, …)` against recognized
  profile objects in `scope.profiles[]`,
- enforcing `scope.allowed_callers` as the final caller check,
- enforcing revocation freshness with
  `effective_T_max = min(profile.max_revocation_staleness_seconds, local verifier T_max)`,
- producing a single auditable decision consumed by `SealerPolicy`,
  `SignerPolicy`, or any future passport-gated host capability adapter,
- never reading plaintext, never loading key material, never running AEAD
  or signature primitives.

## Scope

This document defines solution-level responsibilities of the capability
binding component.

It does not define:

- how a `CallerIdentity` is constructed (daemon HTTP authtok resolution or
  in-process caller registration remain outside this organ),
- the canonical JSON signing of `capability-passport.v1`
  (owned by the `capability` crate),
- the distribution, append-log, or storage of revocation artifacts
  (owned by the revocation feed consumer; this organ reads a pre-built
  local `RevocationView`),
- AEAD or digital signature primitives (Sealer and Signer concerns),
- key-reference grammar (Key backend / `KeySource` concern; see
  proposal 038 §`key_ref` Is a Reference).

The `RevocationView` is the local verifier's projection, not a network role.
It may include node-local revocations that are meaningful only for local
dispatch, local modules, or local host capabilities. Federated directories such
as Seed Directory are only distribution surfaces for revocation artifacts that
other nodes may need to observe; Capability Binding consumes the resulting
local view and does not care which source produced it.

## Must Implement

### CallerBinding and Resolver

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (§CallerBinding Ownership)

Responsibilities:

- define a `CallerBinding` value type containing at minimum:
  `binding_id`, `caller_label`, `caller_source_selector`, `subject_kind`,
  `subject_id`, `subject_keys: Vec<String>` (all `did:key:…` form),
  `issued_at`, optional `expires_at`,
- define a `CallerSubjectKind` enum covering
  `{HttpModule, InProcessModule, Operator, Participant, Node, Org}`,
- define a `CallerBindingResolver` trait with a single method
  `resolve(&self, caller: &CallerIdentity) -> Result<CallerBinding, BindingError>`,
- require resolvers to be pure functions of their input plus local host
  state (authtok binding registry for HTTP callers, in-process caller map
  for in-process callers),
- require `CallerBinding::subject_keys` to carry only public key material;
  binding artifacts MUST NOT embed secrets,
- distinguish `BindingError::Unknown`, `BindingError::Expired`, and
  `BindingError::Malformed` as non-opaque variants so that operator
  diagnostics can localize the failure without revealing caller
  credentials.

Status:

- `done` in the Node reference implementation. `orbiplex-node-caller-binding`
  defines the value type, resolver trait, explicit `BindingError` variants, and
  an in-memory resolver used by daemon dispatch tests and bootstrap wiring.

### Passport-Aware Verification Pipeline

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (§Tightened `capability-passport.v1` Scope for Key-Use Authorization,
  §Revocation Freshness),
- `doc/project/60-solutions/sealer.md`
  (§Passport-Aware Policy (Key-Use Authorization))

Responsibilities:

- define `PassportAuthorizationInput` with:
  `caller: CallerIdentity`,
  `operation: GrantRequest { grant_type, target, key_ref, suite, … }`,
  `passport: CapabilityPassport`,
  `revocation_view: RevocationView`,
  `local_t_max_seconds: u64`,
  `now_rfc3339: String`,
- implement the six-step pipeline verbatim:

  ```text
  1. binding = CallerBindingResolver::resolve(input.caller)
  2. verify passport signature, issuer chain, issuer_delegation proof,
     expires_at vs now
  3. select matching profile(s) from passport.scope.profiles[]:
       OR over recognized profiles; at least one must authorize
       the (grant_type, target, …) request on its own terms
  4. require one top-level caller match:
       there MUST exist allowed_caller in
       passport.scope.allowed_callers[] such that
       binding.subject_keys overlaps allowed_caller.subject_key,
       binding.caller_label matches allowed_caller.label when present,
       and binding.subject_kind matches allowed_caller.kind when present
     profiles MUST NOT override caller binding
  5. effective_T_max = min(matched_profile.max_revocation_staleness_seconds,
                           input.local_t_max_seconds)
     if now - revocation_view.checked_at > effective_T_max:
         return Denied(RevocationStale)
     if revocation_view contains passport.passport_id:
         return Denied(Revoked)
  6. emit AuthorizationDecision::Authorized { matched_profile,
                                              effective_t_max,
                                              audit_fields }
     or AuthorizationDecision::Denied(reason)
  ```

- return a typed `AuthorizationDecision` with non-opaque `Denied` variants:
  `RevocationStale`, `Revoked`, `NoProfileMatched`,
  `AllowedCallersMismatch`, `PassportExpired`, `PassportSignatureInvalid`,
  `BindingMismatch`, `PolicyDenied`,
- forbid combining fields across profiles: OR composition means "one
  recognized profile, on its own, authorizes the operation". A single
  operation MUST NOT be authorized by matching different required fields
  in different profiles.

Status:

- `done` in the Node reference implementation. `orbiplex-node-capability-binding`
  implements `PassportAuthorizationInput`, `RevocationView`,
  `ProfileRegistry`, OR-composition over recognized profiles, allowed-caller
  enforcement, strict revocation freshness, and typed denial reasons.

### Service Policy Adapters

Based on:
- `doc/project/60-solutions/sealer.md` (§Caller-Scoped Policy and Audit)

Responsibilities:

- provide a `SealerPolicy` adapter that wraps the verification pipeline
  and produces `Allowed`/`Denied` outcomes consumable by
  `sealer-service::SealerEngine`,
- provide a `SignerPolicy` adapter with the same shape for
  `signer-service`,
- keep each service free of passport parsing, revocation math, or caller
  binding logic,
- translate `AuthorizationDecision` variants into the service-appropriate
  error types:
  - `RevocationStale` → `SealerError::RevocationStale`,
  - `Revoked` / `PassportExpired` / `PassportSignatureInvalid`
    → `SealerError::Denied(reason)`,
  - `NoProfileMatched` / `AllowedCallersMismatch` / `BindingMismatch`
    → `SealerError::Denied(reason)`.

Status:

- `deferred` — the production path intentionally uses a daemon dispatch-layer
  gate for Sealer and Memarium instead of injecting passport semantics into
  `SealerPolicy` / `SignerPolicy` adapters. Add adapters only when a second
  embedding needs engine-local policy composition.

### Audit Surface

Based on:
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
  (§`info` vs. `derivation_info`)

Responsibilities:

- emit audit events containing at minimum:
  `caller_label`, `caller_source_digest` (authtok digest for HTTP callers),
  `subject_id`, `passport_id`,
  `passport_digest` (SHA-256 over canonical JSON), `grant_type`, `target`,
  `key_ref`, `derivation_info_hash`, `matched_profile`,
  `revocation_freshness_seconds`, `decision`,
- NEVER emit plaintext, raw AAD, key material, or raw `derivation_info`
  bytes,
- delegate the sink through an injected `AuthorizationAuditSink` trait so
  that each host service routes authorization events through its own
  pipeline (`SealerAuditSink` for Sealer, `SignerAuditSink` for Signer),
- record denied decisions with the same event schema as allowed decisions;
  `decision` is the discriminator, not the event class.

Status:

- `done` in the Node reference implementation. `AuthorizationAuditSink` records
  a uniform `AuditFields` event for authorized and denied decisions, including
  synthetic pre-pipeline denial events for missing passport lookups.

### Error Model

Responsibilities:

- keep `BindingError`, `VerificationError`, and `AuthorizationDecision`
  variants non-opaque: authorization failures are diagnostic, not
  confidentiality-bearing,
- document explicitly that unlike Sealer's `OpenFailed` (which is opaque
  by design as a confidentiality invariant), authorization errors
  distinguish `RevocationStale` from `Revoked` from `AllowedCallersMismatch`
  from `NoProfileMatched` because these are operator-diagnostic conditions
  that reveal no key material or plaintext,
- fail closed for recognized profiles: any absent required field or malformed
  required field MUST produce `Denied(…)`, never `Allowed`,
- treat unknown profile discriminators as non-authorizing: they MAY coexist
  with recognized profiles, but they MUST NOT grant access; if no recognized
  profile authorizes the request, return `Denied(NoProfileMatched)`.

Status:

- `done` in the Node reference implementation. Binding and authorization
  failures remain non-opaque operator diagnostics, unknown profiles are
  non-authorizing, and malformed recognized profiles fail closed.

## May Implement

### Binding Cache

Binding resolution MAY be cached with a short TTL to avoid per-request
registry lookup, keyed by `(caller_label, caller_source_digest)`. Cache
entries MUST be invalidated on binding registry change and MUST respect
`CallerBinding::expires_at` if present.

Status:

- `optional`

### Decision Cache

Full authorization-decision caching is NOT recommended in v1. Passport
semantics depend on revocation freshness, and caching decisions without
re-checking the revocation view would reintroduce the hazard that strict
`T_max` is there to prevent.

A narrow form — caching only the profile-match and signature-verify
results for a single passport canonical digest — MAY be implemented if
measured profiling shows passport parsing is hot. Revocation and freshness
checks MUST still run on every authorization.

Status:

- `future` (gated on profiling evidence)

## Out of Scope

- passport signing (capability crate concern),
- revocation artifact format, signing, or distribution (capability crate
  and revocation feed concerns),
- key-reference grammar parsing (Key backend / `KeySource` concern),
- cryptographic primitives (Sealer, Signer concerns),
- HTTP authtok lifecycle (daemon concern),
- in-process caller registry maintenance (daemon concern).

## Consumes

- `CallerIdentity` (reused from `signer-core`)
- `CapabilityPassport` (from `capability` crate)
- `CapabilityPassportPresent` (presentation wrapper, from `capability`)
- `DelegationProof` (when proxy-signed, from `capability`)
- `RevocationView` (locally maintained cache fed by the revocation feed
  consumer)
- local configuration: verifier `T_max`, allowed profile discriminators,
  allowed suite ids

## Produces

- `CallerBinding` values (public-key-only, never secret material)
- `AuthorizationDecision::{Authorized{matched_profile, effective_t_max},
  Denied(DenialReason)}`
- Audit events through the injected `AuthorizationAuditSink`
- Typed error values: `BindingError`, `VerificationError`

## Host Capability Surface

Capability Binding does not expose a hosted capability of its own. It is
an in-process composition layer consumed by `sealer-service`,
`signer-service`, and any future host capability that needs passport-gated
authorization.

It is NOT network-advertised. It does not appear in `CapabilityProfile`
advertisements, it does not participate in Seed Directory capability
discovery, and it does not cross the node boundary directly. Passport
artifacts themselves travel across node boundaries; the decision organ
does not.

Likewise, a local revocation decision for a host capability is not automatically
a Seed Directory event. Publishing a signed revocation artifact to a federated
directory is a separate operation, used only when other nodes may rely on the
artifact being revoked.

## Crate Boundary

### `caller-binding` crate

Defines:

- `CallerBinding` struct,
- `CallerBindingResolver` trait,
- `CallerSubjectKind` enum,
- `BindingError` with non-opaque variants,
- an `InMemoryCallerBindingResolver` suitable for the daemon's
  authtok-based registry (feature-gated so that bare consumers do not
  pull in the daemon's internal state).

Depends on: `signer-core` (for `CallerIdentity`, `CallerSource`).
Does NOT depend on `capability`.

Rationale: keep this crate a thin host-auth library so that test fixtures
needing only caller resolution do not pull in the full passport artifact
set.

### `capability-binding` crate

Defines:

- `PassportAuthorizationInput` value type,
- `AuthorizationDecision` with non-opaque `Denied` variants,
- `VerificationError`,
- the six-step verification pipeline (`authorize` function),
- `SealerPolicy` and `SignerPolicy` adapters (feature-gated per service),
- `AuthorizationAuditSink` trait with a no-op default implementation,
- canonical digest computation for `passport_digest` (SHA-256 over the
  canonical JSON produced by the `capability` crate).

Depends on: `caller-binding`, `capability`, `signer-core`.

Rationale: this is the composition layer. It is the only place where
caller resolution, passport verification, and revocation freshness come
together into one decision.

## Notes

Capability Binding is stratified between local host authentication
(daemon HTTP authtok resolution, in-process caller registration) and
cryptographic services (Sealer, Signer). Passport semantics live here;
the layers it connects stay free of passport knowledge.

The architectural rationale for keeping the decision organ local while
the passport artifact itself federates across nodes is captured in
`doc/project/20-memos/authorization-locality.md`.

The core operational invariant is that
`AuthorizationDecision::Authorized { … }` can only be produced when ALL of:

- the `CallerIdentity` resolves to a `CallerBinding` whose subject keys
  overlap `scope.allowed_callers[*].subject_key`,
- at least one recognized profile in `scope.profiles[]` authorizes the
  requested `(grant_type, target, …)` on its own terms,
- `now - revocation_view.checked_at <= effective_T_max`,
- `passport_id` is absent from the revocation view,
- passport signature, issuer chain, and expiry all verify.

Any weakening of those invariants must be explicit, named in a
`DenialReason` variant, and auditable. Implicit permissiveness is
forbidden.

Capability Binding does not try to be a policy engine. It evaluates
passport-gated authorization exactly as specified in proposal 038. Profiles
that go beyond the three standard ones (`sealer-access@v1`,
`memarium-space-access@v1`, `community-key-access@v1`) MAY be added by
registering additional profile evaluators, but each evaluator MUST remain
a pure function of its profile object plus the operation request, and MUST
NOT read shared mutable state.

Implementation-specific decomposition, file ownership, and delivery status
belong in the concrete Node repository's implementation ledger.
