# Proposal 038: Key Roles and Key Use Taxonomy

Based on:
- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/032-key-delegation-passports.md`
- `doc/project/40-proposals/036-memarium.md`
- `doc/project/40-proposals/037-generic-signing-service.md`
- `doc/project/60-solutions/sealer.md`

## Status

Draft

## Date

2026-04-15

## Executive Summary

Orbiplex uses several kinds of cryptographic keys, each serving a different
semantic role. Some keys identify infrastructure, some identify participants or
organizations, some delegate limited authority to proxy keys, and some protect
shared community memory. Treating them as one generic "key" blurs ownership,
storage, revocation, audit, and user-facing meaning.

This proposal defines a taxonomy of key roles and their intended use. It keeps
the trusted core small: Signer owns authenticity operations, Sealer owns
authenticated encryption over bytes, key backends own storage and unlock, and
artifact-specific layers own canonicalization and policy semantics.

Key decisions:

1. A `node identity key` identifies and authenticates a Node as infrastructure.
2. A `node AEAD key` is symmetric authenticated-encryption material owned by a
   Node installation, available without operator unlock, used for sealing
   node-local at-rest material.
3. A `participant key` identifies a human or participant actor and anchors
   consent, authorship, and capability issuance.
4. An `org key` identifies an organization-level subject and anchors
   organization-scoped governance artifacts.
5. A `proxy key` is a delegated key with bounded grants for a participant or
   organization principal; it is not a new principal.
6. A `community key` is symmetric or derivable AEAD material for a bounded
   community key domain and epoch.
7. A `global community key` for encryption is explicitly rejected. Global
   community material intended for everyone is public; it needs signatures,
   provenance, content addressing, and governance, not a shared secret.
8. `key_ref` identifies key material or a key generation line; `info` remains a
   per-operation derivation context. Signer and Sealer treat both as opaque.

## Context and Problem Statement

Recent Signer, Sealer, Memarium, Passport, and key-delegation work introduced
several key-bearing concepts:

- node identity keys used for transport handshake, advertisements, and node
  self-signing,
- participant keys used for capability passports, revocations, and authored
  records,
- organization identifiers and future organization governance keys,
- proxy keys delegated through `key-delegation.v1`,
- symmetric AEAD keys needed by Sealer for Memarium spaces and future
  community key distribution,
- derived keys and shared secrets exposed through Signer for X25519 DH and
  future AEAD derivation.

Without a shared taxonomy:

- `key_ref` naming becomes inconsistent,
- audit logs lose human meaning,
- Passport scopes risk mixing issuer, caller, proxy, and encryption roles,
- Sealer might accidentally learn domain-specific key grammar,
- Memarium might treat public global data as if it needed group encryption,
- community key rotation and revocation become hidden in ad-hoc context fields.

The system needs one document describing what each key role is, what it is for,
where it is stored, who controls it, how it is referenced, and what it must not
be used for.

## Goals

- Define the user-facing and protocol-facing meaning of each key role.
- Establish stable naming conventions for `key_ref` families without requiring
  Signer or Sealer to parse them.
- Clarify which keys are identity keys, delegation keys, transport keys,
  symmetric encryption keys, or derivation roots.
- Describe how these keys are used by Memarium, Sealer, Signer, Passport, and
  future community key distribution.
- Make explicit that a global community encryption key is a non-goal.

## Non-Goals

- This proposal does not specify a full MLS, TreeKEM, sender-key, or pairwise
  group-key distribution protocol.
- This proposal does not redesign existing `KeyRef` enum shapes in
  `signer-core`.
- This proposal does not define hardware-backed key storage or HSM support.
- This proposal does not define new cryptographic primitives.
- This proposal does not require Sealer to parse `key_ref` strings.
- This proposal does not introduce a single global community encryption key.

## Decision

### 1. `key_ref` Is a Reference, Not a Parser Contract for Signer or Sealer

`key_ref` identifies key material, a key generation, or a derivation root. It
MUST NOT contain secret material. It MAY contain human-readable structure for
audit and operator diagnosis.

Signer and Sealer treat `key_ref` as opaque:

- they propagate it,
- they include safe audit tags or stable references in audit events,
- they pass it to the relevant key backend or `KeySource`,
- they reject unknown references only through backend or policy results.

The key backend or `KeySource` owns interpretation of key-reference grammar. A
future parser MAY live in a dedicated key-reference conventions module, but it
MUST NOT become part of Sealer's cryptographic core.

Recommended convention:

```text
key:<family>:<subject-or-scope>:<optional-domain>:epoch:<n>:<role>
```

Examples:

```text
key:node:self:ed25519
key:node:self:epoch:1:aead
key:participant:primary:ed25519
key:org:did-key:z6MkOrg:governance:ed25519
key:proxy:did-key:z6MkProxy:participant:did-key:z6MkPrincipal:ed25519
key:community:alpha:space:community:epoch:12:aead
key:community:alpha:domain:curation:topic:ai-safety:epoch:3:aead
```

The exact string syntax is a convention for key backends, operators, audit, and
Passport scopes. It is not an invitation for every component to parse key names.

### 2. `info` Is Per-Operation Derivation Context

`key_ref` answers:

> Which key generation or derivation root is being used?

`info` answers:

> In which operation context is that key being derived or used?

For Sealer, `info` SHOULD remain available even when epoch is explicit in
`key_ref`. It is useful for binding AEAD key derivation to:

- ciphersuite id,
- caller hash,
- Memarium entry id,
- AAD profile,
- transcript hash,
- operation kind,
- application artifact family.

Examples:

```text
key_ref = key:community:alpha:space:community:epoch:12:aead
info    = memarium.entry.v1 || entry_id || aad_hash
```

```text
key_ref = key:community:global:domain:curation:topic:ai-safety:epoch:3:aead
info    = curation.review-note.v1 || artifact_hash || reviewer_group_hash
```

The invariant is:

```text
key_ref = generation identity
info    = operation diversifier
```

### 3. Node Identity Key

A Node identity key identifies and authenticates one Orbiplex Node as infrastructure.

Primary uses:

- signed peer handshakes,
- node advertisements,
- capability advertisements,
- node-side acceptance in node/operator binding,
- node-self revocation or self-assertion where the protocol profile requires
  the node rather than the participant to sign.

Properties:

- canonical subject id: `node:did:key:...`,
- typical algorithm: Ed25519 for signatures,
- may be converted or derived for X25519 session establishment where the
  protocol profile permits it,
- controlled by the local daemon installation,
- not a human consent key.

What it must not be used for:

- issuing participant consent,
- signing capability passports as a participant,
- authorizing community membership,
- encrypting arbitrary application payloads directly.

User-facing meaning:

> This machine/runtime is the same Node that previously advertised, handshook,
> or accepted a binding.

### 3bis. Node AEAD Key

A Node AEAD key is symmetric authenticated-encryption material controlled by one
Orbiplex Node installation. It is distinct from the Node identity key (§3):
the identity key answers "which Node", the AEAD key answers "which material at
rest is this Node's own".

Primary uses:

- sealing constitutional seed entries in the Memarium crisis space on first
  start, before any operator unlock has occurred,
- sealing autonomic crisis facts produced by node-side detectors
  (federation availability, sealer readiness, revocation view freshness,
  storage integrity),
- sealing future node-local at-rest material that is owned by the Node as
  infrastructure and does not require operator-gated access.

Properties:

- symmetric AEAD material (suite chosen by Sealer; typical: AES-256-GCM or
  XChaCha20-Poly1305),
- canonical reference: `key:node:self:epoch:<n>:aead`,
- generated at first daemon startup alongside the Node identity key,
- stored in the local key backend without passphrase protection,
- available to the Node process throughout its lifetime without operator action,
- rotated by epoch bump; prior epochs retained in the key backend for
  existing-ciphertext opening.

Adversary model:

- protects against filesystem, backup, or remote-storage adversaries that can
  read the data directory but do not execute the Node process,
- does NOT protect against an adversary who executes the Node process (the
  Node has the key in memory whenever it runs),
- does NOT protect against an adversary who obtains the key backend unlocked
  (key backend protection is a separate layer and out of scope for this
  proposal).

What it must not be used for:

- protecting operator emergency notes, recovery phrases, or other operator-held
  secrets (those use an operator-held AEAD key that stays locked until sealer
  unlock; see §4 and forthcoming operator-notes scope),
- protecting participant-authored material (use Participant Key §4 or derived
  participant-scoped AEAD),
- protecting community-shared material (use Community Key §7),
- signing anything (Node AEAD is symmetric; signatures use Node identity §3 or
  Participant §4),
- encrypting public material that needs provenance and governance (public
  material is public: signed, addressed, governed — not encrypted with a
  per-node symmetric key).

User-facing meaning:

> This material is the Node's own at-rest data, readable whenever this Node
> runs, not readable from backups or exfiltrated files alone.

Relation to operator keys (§4 and derivatives):

A single Memarium space MAY host material sealed with different key roles.
The Memarium crisis space is the canonical example:

- constitutional seed entries use `key:node:self:epoch:1:aead`, auto-applied on
  first start,
- autonomic crisis facts use `key:node:self:epoch:1:aead`, written by
  node-side detectors,
- future operator-entered crisis notes use
  `key:operator:crisis:memarium:epoch:1:aead`, gated by sealer unlock.

Each writer chooses the appropriate role for its adversary model. The space
policy (mandatory encryption) is enforced uniformly on all writes regardless
of the writer's chosen role.

### 4. Participant Key

A participant key identifies a participant actor. In most user-facing flows this
is the key with which a person consents, authors, delegates, revokes, or accepts
responsibility.

Primary uses:

- capability passport issuance,
- key delegation issuance,
- issuer-signed revocations,
- authored Agora records,
- participant-scoped consent artifacts,
- future Memarium authored facts where human authorship matters.

Properties:

- canonical subject id: `participant:did:key:...`,
- typical algorithm: Ed25519,
- may be passphrase-protected through the participant key envelope,
- may delegate bounded actions to proxy keys,
- should be treated as high-value identity material.

What it must not be used for:

- routine high-volume signing when a scoped proxy key is available,
- direct group-content encryption,
- node transport identity,
- silent background actions that should be operator-visible.

User-facing meaning:

> This participant consented, authored, delegated, or revoked.

### 5. Organization Key

An organization key identifies an organization-level subject. It is not merely a
participant key with a different label; it represents governance authority for an
organization profile.

Primary uses:

- organization-scoped governance artifacts,
- organization service offers or policy claims,
- council or operator-group decisions when the profile accepts an organization
  subject,
- future threshold or multi-signer governance profiles.

Properties:

- canonical subject id: `org:did:key:...` or a future organization DID profile,
- may be backed by one key in early MVP profiles,
- should be designed to evolve toward threshold, rotation, and governance logs,
- may delegate bounded actions to proxy keys.

What it must not be used for:

- representing an individual participant's personal consent,
- hiding the accountable human or governance process behind an opaque org label,
- replacing profile-specific authority checks.

User-facing meaning:

> This organization, under its declared governance model, made this assertion.

### 6. Proxy Key

A proxy key is a delegated operational key. It acts on behalf of a principal
participant or organization only within explicit grants.

Primary uses:

- signing capability passports under `signing/capability` grants,
- signing issuer revocations when a delegation profile permits it,
- future module-specific or service-specific signing with bounded grants,
- reducing exposure of primary participant or organization keys.

Properties:

- canonical key id: `did:key:...`,
- delegation artifact: `key-delegation.v1`,
- compact proof: `issuer_delegation` embedded in signed artifacts,
- grant shape: map of `grant_type -> target[]`,
- revocable separately from the principal key.

Example grant:

```json
{
  "signing/capability": ["network-ledger", "seed-directory"]
}
```

Future Sealer and Memarium grants may reuse the same grammar:

```json
{
  "sealer/open": ["key:community:alpha:space:community:epoch:12:aead"],
  "memarium/read": ["community"]
}
```

What it must not be used for:

- becoming a new sovereign participant or organization,
- receiving broader authority than the principal had,
- silently bypassing revocation, expiry, or profile-specific policy,
- carrying encryption secrets inside the delegation proof.

User-facing meaning:

> This operational key was allowed to perform this bounded action for the
> principal.

### 7. Community Key

A community key is symmetric or derivable AEAD material for a bounded community
key domain and epoch. It protects shared non-public "we" material: not purely
personal, not public, and not necessarily crisis-only.

Primary uses:

- encrypted Memarium community-space entries,
- encrypted curation notes before public release,
- private working-group knowledge,
- local mutual-aid or care-circle records,
- crisis or emergency community materials scoped to a small trusted group,
- archive handoff packages when the archivist should not receive broad domain
  access.

Properties:

- symmetric AEAD material or a derivation root,
- addressed through `key_ref`,
- versioned by explicit epoch,
- distributed through a separate community key distribution protocol,
- authorized through Passport or local policy,
- stored in a local key backend once installed.

Recommended `key_ref` examples:

```text
key:community:wroclaw-mutual-aid:space:community:epoch:7:aead
key:community:alpha:space:community:epoch:12:write
key:community:alpha:space:community:epoch:12:read
key:community:global:domain:curation:topic:ai-safety:epoch:3:aead
key:community:global:domain:crisis:region:pl:epoch:2:aead
```

Community keys are managed by a community key manager, not by Sealer itself.
Sealer only receives a `key_ref`, `suite`, plaintext or ciphertext, and AAD.

What it must not be used for:

- public global knowledge,
- participant identity,
- node identity,
- capability issuance,
- replacing Passport authorization,
- one-key-fits-all global community encryption.

User-facing meaning:

> Members of this bounded community domain and epoch can read or write this
> protected shared material according to policy.

### 8. Community Key Distribution Is a Separate Layer

A Passport may say:

> Caller X may receive or use key domain Y.

It does not answer:

> How did the epoch secret for Y arrive in X's key backend?

Community key distribution is a separate layer above Signer/Sealer and below
Memarium policy. It may start with pairwise wrapping using X25519 DH and later
move to MLS, TreeKEM, or another group key agreement protocol.

Initial artifact families may include:

```text
community-key-epoch.v1
community-key-package.v1
community-key-revocation.v1
```

The important invariant is that a new membership epoch produces a new
`key_ref`. Audit logs should make rotation visible without reconstructing hidden
KDF context.

### 9. No Global Community Encryption Key

Orbiplex should not introduce a global community encryption key.

If material is intended for the whole global community, then it is effectively
public within the system. It needs:

- signatures,
- provenance,
- content addressing,
- curation history,
- reputation and procedural trust,
- transparent revocation or correction records where relevant.

It does not need a single shared secret.

The phrase "global community key" should be avoided for encryption. If a global
layer needs key-related governance, call it a key fabric or registry:

```text
global community key fabric
global community key-domain registry
global community access-policy registry
```

Such a fabric governs many bounded key domains. It is not itself an encryption
key.

## Memarium Examples

### Example 1: Local Community Memory

A local mutual-aid group stores trusted procedures and contacts in Memarium's
community space:

```text
community_id = wroclaw-mutual-aid
space        = community
key_ref      = key:community:wroclaw-mutual-aid:space:community:epoch:7:aead
```

Memarium stores:

- local procedures,
- trusted contacts,
- verified resource notes,
- coordination summaries.

Access path:

1. Caller presents or references a valid Passport for `memarium/read` and
   `sealer/open` in the relevant community scope.
2. Verifier checks Passport, caller binding, revocation state, and grant target.
3. Sealer opens bytes using `key_ref` and caller-supplied AAD.
4. Audit records caller, `key_ref`, passport id and digest, AAD hash, and
   result.

### Example 2: Public Knowledge With Private Review

The global community prepares a public knowledge artifact through a private
review domain:

```text
key_ref = key:community:global:domain:curation:topic:ai-safety:epoch:3:aead
```

Memarium stores private review notes under the curation key. Once approved, the
public result is emitted as a signed, content-addressed public artifact. The
public artifact is not encrypted with a global shared key.

### Example 3: Write-Only Middleware

A middleware module may be allowed to record sealed observations but not read
history:

```json
{
  "sealer/seal": ["key:community:alpha:space:community:epoch:12:write"],
  "memarium/write": ["community"]
}
```

The module can append sealed facts, but no `sealer/open` or `memarium/read`
grant is present.

### Example 4: Crisis Domain With Small Membership

A regional crisis group protects sensitive operational procedures:

```text
key_ref = key:community:global:domain:crisis:region:pl:epoch:2:aead
```

This is a community key domain under the global community fabric, not a global
community encryption key. Compromise of one regional crisis domain must not
expose unrelated global community material.

### Example 5: Archive Handoff

Memarium prepares an archive package for a trusted archivist:

```text
key_ref = key:community:alpha:space:community:epoch:12:archive
```

The archivist receives only the package-specific or archive-role key material
needed by the handoff policy. The archivist does not receive broad read access
to the entire community space.

## Relationship to Passport

Passport is the authorization and consent credential. It may authorize:

- key use,
- key receipt,
- key rotation,
- community key distribution,
- Sealer open/seal operations,
- Memarium read/write operations.

Passport must not carry the community key secret. A Passport answers "who may";
the key distribution layer answers "how the secret arrived"; the key backend
answers "where the secret lives"; Sealer answers "can these bytes be opened
with this `key_ref` and AAD".

Recommended grant families:

```text
signing/capability
sealer/seal
sealer/open
sealer/derive-aead-key
memarium/read
memarium/write
memarium/index
memarium/cache
memarium/promote
memarium/forget
community/key-receive
community/key-rotate
community/key-distribute
```

Wildcard grants (`"*"`) are allowed only for explicit operator/root,
daemon-internal, break-glass, or test profiles. Ordinary community member
Passports should enumerate grants and targets.

## Relationship to Signer and Sealer

Signer owns authenticity operations:

- sign bytes,
- unlock/lock signing keys,
- derive raw X25519 shared secrets where policy allows,
- audit caller, domain, key reference, and payload hash.

Sealer owns confidentiality operations:

- seal bytes,
- open bytes,
- bind AAD,
- produce or consume encryption envelopes,
- audit caller, suite, key reference, AAD hash, envelope digest, and result.

Neither Signer nor Sealer owns community membership, Passport semantics,
Memarium space policy, or group key distribution. Those are higher-layer
contracts.

## Open Questions

1. Should organization keys in MVP be single Ed25519 keys only, or should the
   first organization profile already model threshold governance?
2. Should community key domains use pairwise X25519 wrapping first, or should
   the first protocol artifact be shaped to match future MLS concepts from the
   beginning?
3. Which Memarium spaces require separate read/write/archive key roles in MVP,
   and which can begin with one AEAD role per epoch?

## Implementation Specifics

### CallerBinding Ownership

`CallerBinding` SHOULD live in a dedicated crate, tentatively
`caller-binding`, not in `capability`.

Rationale:

- `capability` should remain an artifact and credential crate. It should know
  how to parse, sign, verify, and evaluate Passport-like credentials, but it
  should not depend on host-local caller resolution.
- `CallerIdentity` is a host-capability runtime concept shared by Signer,
  Sealer, daemon HTTP dispatch, and supervised modules.
- Binding an incoming `CallerIdentity` to a module id, subject id, DID key, or
  proof-of-possession record is a local host-auth concern, not a Passport
  artifact concern.

Recommended dependency direction:

```text
signer-core        -> CallerIdentity type
caller-binding     -> CallerIdentity selectors + subject/key bindings
capability         -> Passport artifacts and verification primitives
sealer-core        -> Sealer request/response + opaque key refs
daemon/runtime     -> composes caller-binding + capability + sealer/signer
```

The verifier that authorizes a Sealer or Signer operation may compose all of
these crates, but the artifact crate should not import the local runtime bridge.

### Tightened `capability-passport.v1` Scope for Key-Use Authorization

Key-use authorization tightens `capability-passport.v1` before external
compatibility commitment. Existing draft v1 shapes that do not satisfy the
typed `scope` requirements below are implementation drafts, not stable wire
contracts.

There is no `capability-passport.v2` introduced here. The v1 label is kept
across documentation, schema, and code: one discriminator, one artifact
family, new tighter rules for key-use passports.

Decision summary:

```text
schema                            = "capability-passport.v1"
scope.allowed_callers             = top-level scope (one set per passport)
scope.profiles[]                  = list of typed profile objects
profile.profile                   = profile discriminator inside the object
profile.max_revocation_staleness_seconds
                                  = per-profile
profile composition               = OR over recognized profiles
old loose-scope semantics         = deprecated / invalid for key-use profiles
```

Verifiers MUST fail closed when a recognized profile requires a field that is
missing or has an unknown required shape. Unrecognized profile discriminators
MUST NOT grant access; a passport whose profiles are all unrecognized by the
local verifier is treated as unauthorized for key-use, not as silently
permissive.

Required semantics SHOULD evolve by introducing a new profile discriminator
(`...@v2`), not by adding authority-bearing unknown fields to an existing
profile. Unknown optional fields in a recognized profile MAY be ignored, but
they MUST NOT expand authority.

Full example (Wariant 1, profile discriminator inside each object):

```json
{
  "schema": "capability-passport.v1",
  "scope": {
    "allowed_callers": [
      {
        "kind": "http-module",
        "label": "agora-service",
        "subject_key": "did:key:z6Mk..."
      }
    ],
    "profiles": [
      {
        "profile": "sealer-access@v1",
        "grants": {
          "sealer/open": ["key:community:alpha:space:community:epoch:12:aead"]
        },
        "key_ref_prefixes": ["key:community:alpha:space:community:"],
        "max_revocation_staleness_seconds": 30
      },
      {
        "profile": "memarium-space-access@v1",
        "grants": {
          "memarium/read": ["community"]
        },
        "spaces": ["community"],
        "community_ids": ["wroclaw-mutual-aid"],
        "max_revocation_staleness_seconds": 300
      }
    ]
  }
}
```

#### Profile `sealer-access@v1`

Authorizes Sealer AEAD operations on bounded key references.

Required fields:

```text
profile                           = "sealer-access@v1"
grants                            = map of sealer grant-type -> target[]
  recognized grant types:
    "sealer/seal"
    "sealer/open"
    "sealer/derive-aead-key"
  target entries MUST be SealerKeyRef strings or the wildcard "*"
  (wildcard permitted only for operator/root/break-glass/test profiles)
max_revocation_staleness_seconds  = integer > 0
```

Optional fields:

```text
key_ref_prefixes                  = string[]
  additional constraint: every target MUST be empty, "*",
  or share a prefix with at least one entry in key_ref_prefixes
suites                            = CiphersuiteId[]
  if present, restricts the allowed AEAD suite on matched operations
```

Verifier rule: a `(grant_type, target, key_ref, suite)` request is authorized
by this profile iff `grants[grant_type]` contains `target`, `key_ref` matches
the prefix constraint if present, and `suite` matches the `suites` constraint
if present.

#### Profile `memarium-space-access@v1`

Authorizes Memarium space-level operations at a layer above Sealer.

Required fields:

```text
profile                           = "memarium-space-access@v1"
grants                            = map of memarium grant-type -> target[]
  recognized grant types:
    "memarium/read"
    "memarium/write"
    "memarium/index"
    "memarium/cache"
    "memarium/promote"
    "memarium/forget"
  target entries are Memarium space names (e.g. "community", "crisis")
  or the wildcard "*"
spaces                            = string[]
  enumerates the Memarium space names this profile applies to
max_revocation_staleness_seconds  = integer > 0
```

Optional fields:

```text
community_ids                     = string[]
  restricts the profile to a bounded set of community identifiers
entry_kinds                       = string[]
  restricts the profile to a bounded set of Memarium entry kinds
```

Verifier rule: a `(grant_type, target_space, community_id, entry_kind)`
request is authorized by this profile iff `grants[grant_type]` contains
`target_space`, `spaces` contains the target space, `community_ids` contains
the community id if that field is present, and `entry_kinds` contains the
entry kind if that field is present.

#### Profile `community-key-access@v1`

Authorizes community key material reception, rotation, and distribution
decisions at a layer above Sealer.

Required fields:

```text
profile                           = "community-key-access@v1"
grants                            = map of community grant-type -> target[]
  recognized grant types:
    "community/key-receive"
    "community/key-rotate"
    "community/key-distribute"
  target entries are community identifiers or the wildcard "*"
community_ids                     = string[]
  enumerates the community identifiers this profile applies to
max_revocation_staleness_seconds  = integer > 0
```

Optional fields:

```text
key_domains                       = string[]
  restricts the profile to bounded key domains (e.g. "space:community",
  "domain:curation", "domain:crisis:region:pl")
epoch_range                       = { "min": integer, "max": integer }
  restricts the profile to a bounded epoch window
```

Verifier rule: a `(grant_type, community_id, key_domain, epoch)` request is
authorized by this profile iff `grants[grant_type]` contains the community id,
`community_ids` contains the community id, `key_domains` contains the key
domain if that field is present, and `epoch` falls inside `epoch_range` if
that field is present.

#### Composition Across Profiles

Multiple profiles in one passport compose by OR at the authorization layer:
at least one recognized profile must authorize the requested operation on its
own terms. Profiles do not combine fields across each other; a single
operation is not authorized by matching different required fields in
different profiles.

If two profiles both authorize the same operation with different
`max_revocation_staleness_seconds` values, the authorization carries the
profile-local `T_max` that matched. The effective `T_max` used at runtime is
then further constrained by the local verifier configuration:

```text
effective_T_max = min(profile.max_revocation_staleness_seconds,
                      local verifier T_max)
```

#### Schema Synchronization Expectation

The `capability-passport.v1` JSON Schema should remain the generic artifact
envelope schema, but it must be extended under the v1 discriminator with typed
definitions for the key-use scope fields introduced here:

- `scope.allowed_callers[]`
- `scope.profiles[]`
- standard profile objects: `sealer-access@v1`,
  `memarium-space-access@v1`, `community-key-access@v1`

The base schema may still allow other capability-specific `scope` keys for
non-key-use passports such as `network-ledger` or `node-primary-operator`.
Key-use verifiers, however, MUST semantically require both `allowed_callers`
and an authorizing recognized profile when evaluating Sealer, Memarium, or
community-key operations.

Schema sync is therefore a v1 schema update, not a `capability-passport.v2`
split. After changing the schema, regenerate schema docs and sync the schema
copy into the Node protocol contracts.

### Revocation Freshness

Revocation freshness MUST be strict for key-use paths.

Every Sealer or key-distribution authorization decision that depends on a
Passport or delegation MUST evaluate revocation state through a local
`RevocationView` with a configured maximum staleness:

```text
now - revocation_view.checked_at <= T_max
```

If the revocation view is older than `T_max`, the operation MUST fail closed.
This failure should be represented as a first-class error:

```text
SealerError::RevocationStale
```

The same concept may later be mirrored in Signer or community-key manager error
types, but Sealer should expose it directly because stale revocation on
`open`/`seal` is a confidentiality boundary failure, not merely a generic policy
denial.

The configured `T_max` MAY vary by profile:

- very low for crisis, care, key-distribution, and administrative domains,
- moderate for ordinary community Memarium reads,
- relaxed only for explicit offline or break-glass profiles.

Offline or degraded operation MUST be an explicit profile decision and MUST be
audited as degraded. It must not be the default fallback when revocation sync is
stale.

### Sealer KeyRef Type

Sealer SHOULD use its own key-reference type rather than extending
`signer-core::KeyRef` for AEAD material.

`signer-core::KeyRef` is shaped around signing and DH-capable identity keys:
primary participant, proxy key, and derived signing/DH purposes. Community AEAD
references are a different family: symmetric or derivable key generations,
often epoch-bearing and scoped to Memarium or community domains.

Recommended shape:

```rust
#[derive(Clone, Debug, Eq, PartialEq, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct SealerKeyRef(pub String);
```

Sealer still treats this value as opaque. A `KeySource` implementation may parse
it according to the conventions in this proposal, but `sealer-core` should not
embed the grammar.

Rationale:

- avoids coupling AEAD key naming to signing-key variants,
- keeps community epoch references readable on the wire,
- avoids overloading `KeyRef::Derived { purpose, index }` with string grammar
  hidden inside `purpose`,
- permits future signer and sealer key references to evolve independently.

If cross-service APIs need a generic union later, it should be introduced as a
higher-level host key reference, not by forcing Sealer into the Signer key enum.

### `info` vs. `derivation_info`

Use `info` internally near KDF code and `derivation_info` on public wire/API
surfaces.

Rationale:

- `info` is conventional terminology in HKDF and low-level derivation code.
- `derivation_info` is clearer in JSON and HTTP request bodies, where callers
  should understand that the field is not arbitrary metadata and not a key
  identifier.
- `key_ref` identifies the key generation; `derivation_info` diversifies use of
  that generation for a concrete operation.

Recommended mapping:

```text
wire DTO field:        derivation_info
sealer-core field:     derivation_info or info, depending on proximity to KDF
KeySource method arg:  info
audit field:           derivation_info_hash
```

Audit MUST NOT log raw `derivation_info` by default. It should log a digest
unless the profile explicitly classifies the value as public and safe.
