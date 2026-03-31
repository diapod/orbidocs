# Console Participant Identity Create and Import

Based on:

- `doc/project/40-proposals/014-node-transport-and-discovery-mvp.md`
- `doc/project/40-proposals/007-pod-identity-and-tenancy-model.md`
- `doc/project/40-proposals/017-organization-subjects-and-org-did-key.md`
- `doc/project/30-stories/story-000.md`

This memo captures one UI and runtime direction for participant identity handling
in Orbiplex Node.

The identity flows described here are available through both the CLI launcher and
the Node UI. Neither surface is authoritative over the other; both invoke the same
underlying daemon capability.

The key distinctions are:

- `node-id` is created automatically at first daemon open and is not operator-
  managed,
- participant identity is always an explicit operator action — created fresh or
  imported from backup — never silently auto-generated,
- organization identity is an explicit operator action, with custody automatically
  granted to the existing operator participant,
- and both surfaces should expose these actions at the level of identity lifecycle,
  not at the level of raw identifier strings.

## Baseline

At first daemon open, only the `node-id` is created automatically:

- one durable local `node-id`, deterministically derived from local key material.

Participant identity is **not** created automatically. The node starts in an
unconfigured state with respect to participant identity. The operator must either
create a fresh participant or import one from backup before the node is usable for
procurement, settlement, or any workflow that requires an accountable subject.

This design is intentional. Automatic participant creation would prevent an
operator from restoring a known identity from backup on first run. A node that
silently creates a new participant forces a conflict between the auto-generated
identity and the backed-up one.

If a participant identity already exists when the daemon opens, it is loaded and
displayed as-is. No new participant is created. In MVP, at most one local
participant is held per node.

## MVP identity scope

For hard MVP, the console manages exactly two identity subjects:

1. **Participant identity** — created or imported explicitly by the operator on
   first use; serves as the node operator participant; at most one local
   participant is held per node in MVP; if one already exists it is shown but
   no creation or import action is offered again.
2. **Organization identity** — created explicitly by the operator; the existing
   operator participant automatically becomes the custodian of the created org.

This is a deliberate MVP constraint. It keeps the identity surface minimal while
enabling the org-bound buying flow from `story-006` without requiring multi-
participant management or explicit custody assignment in the console.

Beyond MVP, additional participant identities may be created or imported on the
same node — for example, to support tenancy or role separation. That extension
is outside the scope of this memo.

**Note on operator role assignment:** In MVP, the operator role is implicit —
the daemon treats the sole existing participant as the operator participant
without any explicit role designation or stored assignment fact. This is a
deliberate shortcut enabled by the single-participant constraint: uniqueness
implies operator status. It is not a general contract. Once multiple
participants may coexist on one node, an explicit activation mechanism will be
required — that design belongs to Scenario C and the multi-participant identity
workstream.

## Console responsibility

The console exposes three identity flows:

1. `Create Participant` — first-run path; creates a fresh local participant
2. `Import Participant` — first-run path; restores a participant from BIP39 backup
3. `Create Organization` — available once a participant identity exists

Both `Create Participant` and `Import Participant` are only offered when no
participant identity is present. Once a participant exists, the console shows it
as read-only in MVP and does not offer creation or import again.

The console should **not** expose a low-level action such as:

- `Create Participant ID`

because `participant-id` is not primary operator input. It is a canonical
identifier derived from created or imported identity material.

## Create Participant

`Create Participant` means:

- generate fresh local participant identity material,
- derive canonical `participant:did:key:...`,
- persist the local binding in the node,
- expose the resulting participant as the operator participant for settlement,
  policy, and workflow surfaces.

This action is only available when no participant identity exists on the node.

The operator may provide optional host-local metadata such as:

- `nickname`,
- local `label`,
- optional `note`.

That metadata is convenience state for the node UI and operator tooling. It is
not the accountable identity itself and should not redefine the canonical
`participant-id`.

## Create Organization

`Create Organization` means:

- generate fresh local organization identity material,
- derive canonical `org:did:key:...`,
- persist the local org binding in the node,
- automatically assign the existing operator participant as custodian of the
  created org,
- expose the resulting org subject to settlement, policy, and workflow surfaces.

The operator does not choose a custodian manually. The current operator participant
is the implicit custodian at creation time. This keeps the MVP flow simple and
consistent with the single-participant assumption.

The operator may provide optional host-local metadata such as:

- `display-name`,
- local `label`,
- optional `note`.

That metadata is convenience state for the node UI and operator tooling. It is
not the accountable org identity itself and should not redefine the canonical
`org-id`.

## Import Participant

`Import Participant` means:

- restore or bind participant identity material that already exists elsewhere,
- derive or verify the canonical `participant:did:key:...`,
- persist the local binding in the node,
- optionally attach host-local metadata such as `nickname`.

The first practical console flow for import uses a **BIP39 mnemonic phrase** as
the portable identity material carrier.

This should be understood as:

- import of participant identity through a BIP39-backed recovery path,
- not free-form operator entry of a participant id string.

The runtime derives the signing key deterministically from the BIP39 mnemonic and
verifies that the resulting `participant:did:key:...` matches the identity being
imported. A mismatch is a hard rejection with an explicit error shown to the
operator.

The precise BIP39 derivation path and key encoding are to be defined in a
dedicated cryptographic specification before this flow can be implemented.

## Host-local metadata

The node may optionally keep local metadata for each identity subject, such as:

- `nickname` or `display-name`,
- local `label`,
- optional `note`,
- optional tags for operator organization.

This metadata should be treated as:

- local,
- mutable,
- non-canonical,
- and non-authoritative outside the node that stores it.

In other words:

- `participant-id` and `org-id` are portable identities,
- `nickname` and `label` are local operator convenience.

## Why this split matters

If the console collapses identity creation into raw id creation, it mixes:

- cryptographic identity material,
- participant or org role establishment,
- custody assignment,
- tenancy semantics,
- and host-local operator labels.

That would make later multi-participant and organization-bound flows harder to
reason about and harder to audit.

Auto-creating a participant at daemon open creates an additional problem: an
operator restoring a node from backup would find a silently generated identity
competing with the backed-up one. Explicit first-run create or import removes
this conflict entirely.

The cleaner split is:

- automatic `node-id` only,
- explicit `Create Participant` or `Import Participant` on first run,
- explicit `Create Organization` with implicit custodian assignment,
- derived canonical ids in all cases,
- and optional local metadata layered above them.

## Relationship to `participant-bind.v1`

`participant-bind.v1` is a post-channel artifact: it establishes which
`participant:did:key:...` acts on a peer session after an encrypted WSS channel
is open. It is a network-level boundary, not a local activation mechanism.

**In MVP (single-participant), the local operator participant is implicitly
pre-admitted for all local operations** — procurement, settlement, capability
calls, and workflow surfaces — without requiring an explicit bind action in the
console. This is Scenario A: `participant-bind.v1` remains a network artifact
only; local identity readiness follows directly from create or import.

This keeps the MVP console flow simple: create or import once, participant is
immediately usable.

**Beyond MVP, when multiple participant identities may coexist on one node, a
separate explicit local activation step should be introduced** — distinct from
`participant-bind.v1` and named differently (for example `activate`, `make
primary`, or `enable for operations`). Reusing `participant-bind.v1` semantics
for local activation would conflate two unrelated operations: which participant
acts on a remote peer session versus which participant is enabled for local daemon
operations. That conflation would make both flows harder to reason about and
harder to audit. This is Scenario C.

The Scenario C design is deferred to the multi-participant identity workstream.

## Non-goals

This memo does not yet define:

- BIP39 derivation path and key encoding details for mnemonic import,
- multi-device continuity and key synchronization,
- hosted-user `pod-user-id` semantics,
- multi-participant management on one node beyond the MVP single-participant
  assumption,
- explicit custodian assignment or threshold custody for org identities,
- or schema-level create/import contracts.

Those should be defined later in a dedicated identity workstream once the console
flow is frozen as product direction.
