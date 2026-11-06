# Pseudonym Vault and Key Roles

`Pseudonym Vault and Key Roles` is the solution-level identity component that
turns Proposal 059 into runtime responsibilities for participant role derivation,
private nym continuity, cryptographic routing-subject continuity, and
role-aware recovery.

Status: `hard-mvp-done`

Date: `2026-05-17`

## Executive Summary

This component owns one narrow identity-storage boundary:

```text
participant mnemonic / recovery root
  -> stable participant signing identity
  -> participant role derivation
  -> participant/recovery-wrap
  -> recovery/import-only vault unwrap

operational-secret-root
  -> participant-signing-key-wrap
  -> proxy-key-wrap
  -> participant/vault-wrap operational profile
  -> ciphertext-only pseudonym-vault.v1 snapshots
  -> private nym and routing-subject seed recovery

sealer-master
  -> separate Argon2id envelope tier, optionally step-up protected
```

The MVP profile is intentionally conservative:

- keep `orbiplex-participant-seed-v1` stable;
- keep the participant root implicit behind recovery, genesis, and import flows
  rather than the normal pseudonym hot path;
- derive `participant/dh` and `participant/recovery-wrap` without changing the
  public participant id, while `participant/vault-wrap` names the operational
  vault-key scope rather than a mnemonic-root hot-path key;
- keep `participant/dh` local-only and never publish it as a standing discovery
  artifact;
- store nym and `routing:did:key:...` seeds inside a private encrypted vault;
- use `operational-vault-key` as the default local write profile so creating
  nyms or routing subjects does not require the mnemonic/recovery root;
- use one random `operational-secret-root` as the local domain-wrap root for
  participant signing, proxy signing, and pseudonym-vault operational wraps;
- keep `sealer-master` outside that root as a stronger tier, while coordinating
  standard and step-up passphrase rotation through the participant
  `set-passphrase` flow;
- reject seed-derived vault wrap profiles (`root-only` and
  `root+local-passphrase`) in greenfield local storage; recovery uses sealed
  bundles instead of mnemonic-only pseudonym derivation;
- synchronize only opaque `pseudonym-vault.v1` snapshots;
- accept only single-writer linear vault updates;
- reject participant recovery-recipient leakage in pseudonymous or routing
  metadata.

## Context and Problem Statement

Proposal 059 closes the gap between stable participant signing and recoverable
pseudonymous operation. Before this component, Orbiplex had a stable participant
seed path and public nym / routing-subject artifacts, but no coherent runtime
owner for private nym seed storage, routing-subject seed storage, encrypted
vault sync, or role-aware participant recovery.

The solution must preserve four boundaries:

- participant signing identity remains backward compatible;
- `participant/vault-wrap` is private storage material, not a public wire
  identity; in the hard-MVP implementation, local writes are wrapped by an
  operational vault secret rather than by repeatedly deriving from the recovery
  root;
- `route:...` stays an advisory routing identifier, while
  `routing:did:key:...` is a cryptographic routing subject;
- public envelopes must not reveal `nym -> participant` or
  `routing-subject -> participant` linkage through recovery metadata.

## Must Implement

### Stable Participant Role Derivation

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/20-memos/participant-seed-contract-v1.md`

Related schemas:

- `participant-key-envelope.v1`

Responsibilities:

- preserve the current `orbiplex-participant-seed-v1` signing path and known
  participant id vectors;
- derive role-specific material through versioned, domain-separated labels;
- expose `participant/signing`, `participant/dh`, and
  `participant/vault-wrap` as distinct purposes;
- keep `participant/dh` local-only: derivable on demand for controlled
  direct/sealed protocols, but not discoverable;
- expose `participant/recovery-wrap` as an internal-wrap purpose for local
  sealed recovery bundles;
- fail closed when only raw signing-key material is available and a recovery,
  import, genesis, or legacy-migration operation requires mnemonic or
  recovery-root material.

Status:

- `done` — Node derives the Proposal 059 role purposes while preserving the
  existing participant signing identity path. Pseudonym-vault and recovery
  bundle operations fail closed for raw signing-key-only participants when
  recovery-root material is actually required.

### Ciphertext-Only Pseudonym Vault

> **Cross-reference to Solution 032:** Solution 032 (Local Relationship
> Layer) extends `pseudonym-vault.v1` additively with `local-relationship`
> as an accepted plaintext inner-entry kind. The outer artifact remains
> ciphertext-only per this section. The forward-compat contract for
> unknown inner-entry kinds is: readers MAY ignore unknown kinds;
> importers/resealers MUST preserve unknown entries verbatim;
> `critical = true` entries fail closed on unknown kind; integrity
> violations always fail closed regardless of `critical` flag.
>
> This makes the vault the canonical home for sealed relationship state
> (classes, membership facts, pairwise nym bindings, predicate decisions
> audit). Recovery bundle (this solution §Role-Aware Participant Recovery
> Bundle) automatically includes relationship state with no further
> change to recovery semantics.

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- validate `pseudonym-vault.v1` only at import/export boundaries;
- keep the outer artifact ciphertext-only and free of participant, nym, and
  routing-subject public identifiers;
- enforce runtime crypto semantics that JSON Schema cannot fully express, such
  as valid salt, nonce length, non-empty ciphertext, AEAD integrity, and stable
  AAD profile;
- store snapshots with `vault/version` and `supersedes` lineage;
- reject rollback imports and concurrent higher-version conflicts;
- accept `local-relationship` inner-entry kind additively; preserve unknown
  inner-entry kinds verbatim on reseal (Solution 032 forward-compat rule).

Status:

- `done` — Node mirrors the schema, gates import/export, stores sealed
  snapshots under the identity storage boundary, seals new local writes with
  `operational-vault-key`, rejects legacy seed-derived wrap profiles, and
  enforces single-writer latest semantics with rollback and conflict rejection.
- `done for Solution 032 M1` — additive `local-relationship` inner-entry
  kind and forward-compat unknown-kind preservation rule are schema-gated and
  implemented in the Node pseudonym-vault crate. Daemon-owned relationship
  event-log storage remains Solution 032 M3 work.

### Local Nym and Routing-Subject Creation

Based on:

- `doc/project/40-proposals/015-nym-certificates-and-renewal-baseline.md`
- `doc/project/40-proposals/054-user-maintained-federated-seed-directory.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `nym-certificate.v1`
- `routing-subject-binding.v1`
- `pseudonym-vault.v1`

Responsibilities:

- create nyms from random per-nym local seeds stored inside the encrypted vault;
- create cryptographic routing subjects from random per-subject local seeds
  stored inside the encrypted vault;
- derive each nym and routing subject into separate signing and DH roles;
- write sealed accountability metadata for each private nym/routing subject:
  `custodian/ref` points to the local `node:id`, and `disclosure/class`
  defaults to `unsealing-only` unless a higher layer intentionally marks a
  routine-disclosable nym;
- keep advisory `route:...` identifiers out of the vault recovery model unless
  a future proposal explicitly elevates them to cryptographic subjects;
- reseal the vault after local pseudonym mutation.

Status:

- `done` — Node exposes local nym and `routing-subject` creation through the
  host identity control plane and persists the resulting private seeds only
  inside sealed vault snapshots. New writes use `operational-vault-key` by
  default, so the user wizard and messaging setup can create routing subjects
  without requiring the mnemonic after participant identity exists. Minting a
  second local nym/routing subject is gated on `recovery-bundle/current` so the
  latest vault-random snapshot is covered before further pseudonym expansion.

### Operational Unlock Root and Sealer Tiering

Based on:

- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/037-generic-signing-service.md`
- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`

Related schemas:

- `participant-key-envelope.v1`
- `pseudonym-vault.v1`

Responsibilities:

- maintain a random local `operational-secret-root` that is not the participant
  mnemonic or BIP39 root material;
- protect the root with a passphrase slot and a recovery slot so passphrase
  rotation re-wraps the root rather than every domain secret;
- derive named domain wrap keys from the root for participant signing,
  proxy/signer keys and pseudonym-vault operational wrapping;
- keep the sealer master key as a deliberately separate Argon2id envelope tier,
  optionally protected by an additional step-up secret;
- enforce the normative invariant: `sealer-master` MUST be randomly generated
  and MUST NOT be derived from participant mnemonic. It MAY be recoverable
  through a sealed recovery envelope bound to `participant/recovery-wrap`,
  optionally requiring `recovery_aux` or step-up policy;
- coordinate participant/root/sealer passphrase rotation atomically, requiring
  `sealer_current_passphrase` and `sealer_step_up_secret` when the active sealer
  envelope is step-up protected.

Status:

- `done` — Node uses `operational-secret-root.v1`
  for participant signing, proxy/signer and pseudonym-vault operational wraps;
  `session.unlock` populates the corresponding caches from one passphrase;
  `set-passphrase` re-wraps the operational root and also re-wraps an active
  sealer master envelope in the same file transaction. Step-up sealer envelopes
  keep their additional factor during passphrase rotation when the operator
  supplies `sealer_current_passphrase` and `sealer_step_up_secret`. Recovery
  bundle export includes the random sealer master as a
  `sealer-master-recovery.local.v1` record inside the sealed participant
  recovery payload; import re-wraps it under the target host's local passphrase
  and optional `sealer_step_up_secret`.

### Role-Aware Participant Recovery Bundle

Based on:

- `doc/project/40-proposals/030-identity-recovery-service.md`
- `doc/project/40-proposals/031-participant-key-passphrase-lock.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- export enough recovery material to restore participant role derivation and
  latest vault snapshots where policy allows export;
- support a sealed-local profile whose payload is wrapped by
  `participant/recovery-wrap` and whose import requires the mnemonic/recovery
  root supplied separately;
- include latest pseudonym-vault snapshots as recovery-export ciphertext blobs:
  export opens the source operational-vault snapshot through its recovery slot,
  re-seals the snapshot under a mnemonic-root-derived recovery-export secret,
  and import re-seals it again under the target host's operational-secret-root;
- include the active random `sealer-master` in the same sealed payload when it
  exists and is unlocked, so sealer recovery follows the same export freshness
  contract as vault-random nyms without deriving the master from mnemonic;
- restore the role tree and sealed vault snapshots without exposing participant
  linkage in public artifacts;
- support the seed+aux hardening profile as an optional recovery unwrap factor.

Status:

- `done` — Node has a role-aware participant recovery bundle import/export path
  that restores mnemonic-backed role derivation and latest sealed vault
  snapshots, supports sealed-local and sealed-local-seed-aux profiles, uses a
  recovery-export snapshot secret rather than carrying the source
  operational-secret-root, includes sealer-master recovery material as a
  sealed-payload-local record when an active master exists and is unlocked,
  requires a target local passphrase before importing vault snapshots or sealer
  recovery material on a fresh host, and fail-closes before mutating local
  identity when that target passphrase is missing.

### Pseudonymous and Routing Metadata Privacy Guard

Based on:

- `doc/project/40-proposals/042-inter-node-artifact-channel.md`
- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`
- `doc/project/60-solutions/008-agora/008-agora.md`

Related schemas:

- `artifact-delivery-envelope.v1`
- `agora-record.v1`
- `pseudonym-vault.v1`

Responsibilities:

- reject public or federated pseudonymous/routing envelopes that expose a
  participant recovery recipient;
- apply the same invariant to Artifact Delivery and Agora admission/signing
  paths;
- keep `participant:did:key:...` recovery recipients legal only in explicitly
  non-pseudonymous participant-scoped contexts;
- preserve diagnostic trace without logging vault plaintext or secret material.

Status:

- `done` — Node rejects participant recovery-recipient leakage for
  pseudonymous/routing Artifact Delivery and Agora paths and carries a negative
  vault leak fixture.

## May Implement

### Private Council Certificate Exchange

Planned under [P015-001–003](../../40-proposals/015-nym-certificates-and-renewal-baseline.md#delivery-integration-tracker).
Local nym creation/key custody is not council certification. The host may expose
a thin applicant adapter that submits a signed issuance/renewal request through
AD/INAC and verifies a correlated reply before retaining it with local nym state.
The issuer owns issuance/refusal; this vault never exports private nym keys or
turns a delivery receipt into a certificate. Reuse existing privacy guards and
P081 certificate verification, with explicit bootstrap authority and bounded,
private request-to-nym metadata. P015 owns acceptor implementation and acceptance;
the existing local-creation baseline remains unchanged.

### Participant DH Local-Only Role

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- none yet

Responsibilities:

- derive `participant/dh` from the implicit participant root when controlled
  direct/sealed protocols need it;
- keep `participant/dh` out of Seed Directory records, node advertisements,
  capability advertisements, vault outer metadata, and recovery bundle
  metadata;
- expose only role-purpose catalog metadata that says the role exists and is
  local-only.

Status:

- `done` — Node exposes `participant/dh` only as a local role-purpose catalog
  row. It remains non-discoverable and outside vault outer metadata; operations
  that require role-root material still fail closed when only raw signing-key
  recovery is available.

### Recovery-Wrap Profile

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- none yet

Responsibilities:

- define `participant/recovery-wrap` separately from `participant/vault-wrap`;
- use it for local sealed recovery-bundle payloads;
- require mnemonic/recovery-root material separately when importing a
  sealed-local bundle;
- keep escrow, social recovery, and hardware custody out of this profile until
  separate procedures are designed.

Status:

- `done` — MVP implements `participant/recovery-wrap` as a local internal-wrap
  role for sealed recovery bundles, not as social recovery or escrow.

### Stronger Vault-Wrap Profiles

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- keep `operational-vault-key` as the default local write profile;
- reject `root-only` and `root+local-passphrase` local write/import requests as
  obsolete seed-derived wrap profiles;
- add future hardware-backed wrapping modes without changing the
  `pseudonym-vault.v1` outer contract;
- make profile selection explicit in the vault metadata and import policy.

Status:

- `done for hard-MVP` — Node implements `operational-vault-key` for default
  local writes and rejects seed-derived wrap profiles. The hard-MVP daemon
  stores the headless/file operational secret as a sealed local node-AEAD
  record; hardware-backed
  wrapping and platform keychain-backed operational secret providers remain
  deferred hardening.

### Multi-Device Vault Merge

Based on:

- `doc/project/40-proposals/059-participant-and-nym-key-role-derivation.md`

Related schemas:

- `pseudonym-vault.v1`

Responsibilities:

- replace single-writer latest snapshots with a conflict-resolving or
  operation-based model only after the merge semantics are designed;
- preserve rollback detection and AEAD integrity under any future merge model;
- avoid leaking plaintext item identifiers to the sync backend.

Status:

- `deferred`

## Out of Scope

- changing the stable `orbiplex-participant-seed-v1` participant signing path;
- deriving every nym or routing subject deterministically from the participant
  root;
- publishing `nym -> participant` or `routing-subject -> participant` linkage;
- treating advisory `route:...` identifiers as cryptographic subjects;
- publishing a standing participant DH discovery artifact;
- defining social recovery, threshold custody, or HSM-only operation;
- storing vault plaintext in network-visible artifacts.

## Consumes

- `orbiplex-participant-seed-v1` mnemonic/recovery material
- sealed local operational vault secret
- `participant-key-envelope.v1`
- `pseudonym-vault.v1` import snapshots
- local nym and routing-subject creation requests
- Artifact Delivery and Agora envelopes at privacy-guard boundaries

## Produces

- stable `participant:did:key:...` signing identities
- local `participant/dh` role material
- local `participant/vault-wrap` AEAD wrapping material backed by the
  operational vault secret for normal writes
- local `participant/recovery-wrap` AEAD wrapping material
- local `nym:did:key:...` signing and DH material
- local `routing:did:key:...` signing and DH material
- sealed `pseudonym-vault.v1` snapshots
- role-aware participant recovery bundles
- privacy rejection facts for participant recovery-recipient leakage

## Related Capability Data

- `026-pseudonym-vault-and-key-roles-caps.edn`

## Notes

This component is intentionally local-first. The public contracts expose
pseudonymous authorship and routing subjects; the private vault preserves the
secret continuity needed to operate those surfaces without making participant
linkage part of the wire protocol.

## Planned Whisper Case-Key Consumer

[P013-LLR-006](../../40-proposals/013-whisper-social-signal-exchange/long-lived-rumors.md#case-continuity-key-and-case-bound-succession)
owns the case continuity key commitment, uses and lifetime; S026 owns custody.
Reuse existing host keystore and recovery-bundle mechanisms. Generate one fresh
case key (closed Ed25519 Phase 1 profile), not a global identity or reusable nym
key; commit its public-key digest and authority in the anchor. Refuse missing or
mismatched keys rather than recovering through an issuer mapping.

The key expires no later than the anchor/evidence retention horizon and can be
erased earlier with an erasure fact. Recovery bundles include it only after
explicit opt-in explaining takeover and seizure risks; default bundles omit it.
P013-LLR-006 qualifies creation, key/anchor binding, expiry, deletion and recovery
inclusion/exclusion. LLR-007/008 own succession and ordered case effects; this
note is planned integration, not implementation evidence.

P035-019 freezes the minimum public manifest binding consumed here: certified
nym/profile, exact auxiliary-use tuple, case-key digest, canonical authority
principal and bounded lifetime. Its producer checks equality with the private
signal before a detached receipt. The manifest is not a Vault key export or a
full-body proof. P037 volatile admission-witness keys are independently random
host-owned keys and never enter participant recovery. LLR-006 custody and
opt-in case-key recovery remain unqualified by this admission slice.
The 2026-10-29 P035-019 A–E gate qualifies the synthetic manifest/receipt producer
and historical inspection only. It preserves this separation of volatile witness
custody from participant/case-key recovery; see
`node:docs/audits/ACCEPTANCE-P035-019-2026-10-29.md`.

The LLR-003 P036 custody profile owns separate per-entry payload DEKs, not nym,
participant or case-continuity keys. It reuses XChaCha20-Poly1305 and custody
fencing, stores erasure knowledge in the Memarium journal, and excludes DEKs from
built-in application backup. External backups and volume encryption remain unknown;
simultaneous provider/journal rollback is outside the claim. S026 case-key recovery
and LLR-009 succession retain their independent gates.

The 2026-10-30 independent LLR-003/P041-001 qualification passed for the bounded
custody/current-presenter profiles, with real P015-006 status/closure lifecycle
and synthetic v2 certificates. Exact source pins, isolated consumers, retention
and exclusions are recorded in `node:docs/audits/ACCEPTANCE-PORTABLE-CUSTODY-2026-10-30.md`.
This does not close P015-005, P036 parent scope, LLR-009 or release qualification.

The custody boundary review separates provider loss from permanent function loss:
explicit replacement preserves old erasure horizons, permits new capture, and
retains proof CAS when only keys were lost. Dedicated owner checkpoints avoid
replaying personal history. Current classification/egress and durable release
facts gate local private reads; detached export remains payload-free. Full custody
backup is the separate P036-005b adapter, not the selected-fact backup.

### Custody boundary requalification (2026-10-30)

Boundary review requalification at clean Node febf8b33 / Orbidocs 6eb1f6b6 passed 593
component tests, one existing ignored case, four cold custody consumers and six isolated
historical cases, scoped Clippy and 16 mutation refusals. Extracted replay and
both-store retrieval agree for bundle
4c2dba4a43c2d6670f3c9397aa5164955d5b216931a96057f9932bc8f1a19600. Dedicated checkpoints,
explicit provider replacement, current operator disclosure/private read, bounded local
observations and independent historical sequences are covered. P036-005b full backup and
publisher/key-destruction liveness remain separate. See
`node:docs/audits/ACCEPTANCE-PORTABLE-CUSTODY-REVIEW-2026-10-30.md`.

The prior dated qualification remains unchanged. This follow-up preserves the
bounded claim and does not close parent P036, P015-005 or LLR-009.


### Case-key custody refinement (2026-11-02)

The LLR-006 owner records prepared/exposed/bound and erase-requested/erased
transitions. Exposed state is durable before releasing a commitment. The provider
uses independent random encryption material without an operationalVaultRoot or
mnemonic recovery slot. Existing issuer keystore and custody-fence mechanics may
be shared; issuer no-export policy remains in its adapter. Case-key recovery is a
separate per-case opt-in projection, omitted by default. Whole-filesystem copies
including provider material are outside revocation guarantees. Tombstones survive
to the original case horizon. Missing keys refuse without replacement generation.
These are design requirements, not qualified runtime status.


### Case continuity custody candidate (LLR-006, 2026-11-02)

The case-key owner is separate from the root-recoverable operational Vault root.
It uses random per-case key material, dedicated owner checkpoints and public
lifecycle facts. Exposed precedes commitment release, author-byte binding precedes
first signed-signal release, and admission remains a separate fact. Managed recovery
omits these keys unless each case opted in; only an already encrypted critical
projection crosses the recovery snapshot. Import preserves the original horizon
and local erasure knowledge and removes the projection before local resealing.
Whole-filesystem snapshots and prior exports are outside that guarantee.

The actual v2 issuer remains P015-005. A disclosed synthetic certificate enters the
host's certified-authoring seam for bounded qualification; this does not finish
LLR-007/008/009. See the LLR-006 custody amendment and Node's separate acceptance.

The daemon reuses S020 for a rotary 60-second expiry sweep, with bounded scope and
key batches. Scheduler suspension or host sleep can delay physical unlink; owned
clock checks still forbid key use at the absolute horizon. Only completed removal
produces an erasure fact. This is managed-key lifecycle, not media sanitization.

LLR-006's bounded custody/composition gate passed on 2026-11-02; see its tracker
and `node:docs/audits/ACCEPTANCE-CASE-CUSTODY-2026-11-02.md`. This post-MVP result
uses synthetic v2 certificates at the certified-authoring seam and does not
qualify P015-005, ordered case history, current authority or transport.


### Accounted case recovery boundary (2026-11-02)

Managed Vault recovery defaults to `case-keys/policy: account`: optional case keys
never make an otherwise authentic nym snapshot expire. Its closed local result
accounts for included/imported/restored/present, expired, locally erased or lost
keys, and reports component integrity/provider failures. Explicit `require`
withholds incomplete output. Busy is bounded retryable refusal without a partial
bundle. Component-only retry requires the existing participant and does not
reseal nyms. Require is an output gate, not a distributed rollback promise.

New inner projections use a role-derived HKDF key and sealed.v2; exact sealed.v1
has read-only recovery support. Independent host audit reports failure even when
the provider cannot open; unavailable audit is explicit. Checkpoint repair bounds
replay, not cumulative storage: old generations remain until storage gains a
reviewed GC operation. An exposed digest can have escaped a preview, so preview
expiry alone does not authorize abandonment of its key.


The corrected recovery/succession boundaries passed separate pure and custody
gates on clean Node `57c40263` / Orbidocs `ce27aa02`: 278 and 376 scoped Rust tests,
two cold OS-denied consumers for custody, and equivalent extracted qualification.
See `node:docs/audits/ACCEPTANCE-SUCCESSION-CUSTODY-REVIEW-2026-11-02.md`.
This does not qualify the deferred successor caller or accepted/current case history.


### Adopted source workflow boundary (2026-11-05)

The daemon's explicit finite source role now leases the existing S026 operational
root per call for separately scoped encrypted case-workflow metadata and short
requester keys. Its host-owned operator API enforces session, active operator,
Schema Gate and current disclosure/private-route checks; AD remains the sole
transport retry owner. It accepts already signed native controls and persists
exact prepared packets and signature-checked results. Component tests use actual
Vault/P035/P037 with full/detached anchors and explicit authority/relay-ingress
fixtures. Complete case-key/successor signing composition, private source audience
delivery and independent cold/transport gates remain pending. This does
not add a recovery slot for case continuity keys or widen S026 hard-MVP closure.

The explicit native case recipient now supports a protected owned-nym audience.
Its configuration locates an existing custody profile/operation/principal, while
the current active local Vault independently proves key possession. The narrow
port opens only bounded PEX presentations, with framing before Vault access,
current key checks around AEAD/parsing and owned-clock checks after I/O. It reuses
the existing persisted key-use watermark and Ed25519-to-X25519 mechanism, without
exporting keys, accepting arbitrary DH requests or adding recovery slots. Read
possession does not require a current publication certificate and does not grant
case permission. Actual Vault and native recipient-owner component probes retain
explicit synthetic-certificate/delivered-frame limits; source audience workflows,
host signing composition and cold/transport qualification remain separate.


The source workflow's one-way audience owner now keeps exact prepared PEX packets
and encrypted accepted/status proof holds in that same finite Store, without
requester keys or return grants. It binds a verified exact presentation and reader
policy before sealing, and requires a current finite material-disclosure lease
before preparation/handoff. Receipt of transport custody remains historical data,
not recipient success or case permission. Full/detached, carried/referenced and
node/nym component composition uses the actual recipient decision; native
audience API and the real material-owner egress lease are now adopted as described
below, while independent transport/cold gates remain pending. This adds no Vault recovery slot or hard-MVP claim.


The native source's optional audience declaration binds independent trust and an
explicit node/nym end recipient to a one-way relay circuit. A transport-node
identity never stands in for a nym audience key. Finite canonical targets and
unique recipient/family choices are configuration prerequisites, not source API,
disclosure or current-case authority. The S026 workflow and Memarium disclosure
owner retain their separate decisions. The native operator API now adopts the
one-way source owner through audience-begin/prepare/handoff/read and the current
real Memarium disclosure lease. Exact nested presentation bytes and reader policy
freeze before sealing; saved replay avoids new resolution or resealing. Live
classification withdrawal and original material horizons can refuse new handoff
without hiding historical local custody facts. Actual native component coverage
uses Vault/Memarium/P035/P037/AD enqueue and a durable receiver, with explicit
authority/relay-ingress and receiver-key fixtures. Full host signing, native
private transport and OS-isolated acceptance remain open. This changes no
recovery policy, hard-MVP scope or tracker closure.


The native source operator API now adopts S026's existing owned-nym status-read
port. A closed custody selector locates an existing profile, certification and
principal; no secret or request clock crosses the route. The workflow freezes
its unsigned intent and reader/audience hint before the Vault-owned signature.
The authority still proves membership independently. Exact committed replay needs
no new nym key lease; this is separate from publication eligibility. Actual Vault
mint, native signing and AD enqueue have component coverage with synthetic
council discovery. Private status-response transport and registration/successor
signing composition remain separate unfinished LLR gates.


The explicit source role may now also adopt a separately configured recipient.
Requester responses stay with the source workflow; audience presentations go to
CaseKnowledge under independent trust, key possession and effect checks. The
existing S026 nym lease is installed in both adapters without exporting a key or
combining their stores. Owned-node and owned-nym recipients are explicit choices;
configuration is not proof of possession. Combined route/classification/custody
limits remain bounded. Actual dual-store startup and protected nym receipt through
the paired sink have component coverage, with explicit authority/ingress fixtures.
Native private transport, full signing composition and cold gates remain open;
S026 recovery and hard-MVP claims are unchanged.


### Existing-nym use lifecycle (2026-11-06)

Using an already owned nym is distinct from progressing its finite certificate
issuance workflow. Audience possession/opening, successor PoP, status-read proofs
and ordinary authoring must retain an observed-time floor without spending an
issuance checkpoint for every use. The protected host shares the custody-fence
clock law, preserves the legacy time floor and checks the actual active key and
current participant selection. The separate public fence is not another secret
store, an issuance fact, or current permission. Losing an established fence
refuses use rather than resetting time; whole-provider restoration remains beyond
the local rollback guarantee.

The same-S026 audience path now has a whole native operator component vector for
full/detached and carried/referenced presentation, real owned mint/recovery,
Memarium capture and local begin/prepare/handoff. Its one durable reception
survives restart without an extra AD delivery. Initial P035/authority/certificate
material is explicitly fixture-based. Independent ordinary-process cold/private
qualification, external end acknowledgement and the remaining LLR gates stay
open; no task or hard-MVP status changes here.
