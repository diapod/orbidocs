# Authorization Locality

Based on:

- `doc/project/40-proposals/038-key-roles-and-key-use-taxonomy.md`
- `doc/project/60-solutions/capability-binding.md`
- `doc/project/60-solutions/sealer.md`

This memo explains one architectural decision that runs across Sealer,
Signer, Capability Binding, and any future passport-gated host
capability in Orbiplex: the **passport travels across the network, the
authorization decision does not**.

The decision is summarized in two lines in `capability-binding.md`
(§Host Capability Surface) and `sealer.md` (§Host Capability Surface).
This memo explains why those two lines are load-bearing and what they
imply for the system as a whole.

## Three roles, three locations

A capability passport in Orbiplex has three roles, each living in a
different place:

| Role      | What it does                                    | Where it lives                                |
| :-------- | :---------------------------------------------- | :-------------------------------------------- |
| Issuer    | Signs the passport, names scope and callers     | Wherever the issuer key is unlocked           |
| Bearer    | Presents the passport with a request            | Any node or module that needs access          |
| Verifier  | Resolves caller, matches scope, checks freshness | *Locally, at the node performing the action* |

The passport artifact itself is federated: it is a signed credential
that any verifier can read. The verifier, however, is always local to
the action it gates. It is not a network service; it is a function
that runs inside the process that holds the key material or that owns
the gated surface.

## Network-facing vs. internal plumbing

Orbiplex distinguishes two kinds of capability:

- **Network-facing capabilities** (e.g. `memarium.write`,
  `agora.submit`, `catalog.lookup`) appear in `CapabilityProfile`
  records, are discoverable through the Seed Directory, and cross the
  node boundary as part of protocol conversations.
- **Internal plumbing** (Sealer, Signer, Capability Binding, the
  `caller-binding` resolver) is local to the acting node. Some surfaces
  are reachable by supervised local modules through the daemon's own
  dispatch (in-process trait or authtok-resolved HTTP shim); others,
  such as Capability Binding itself, are consumed only as in-process
  composition layers.

Capability Binding, Sealer, and Signer belong to the second kind. They
do not appear in any advertisement, they are not addressable from
outside the node, and a remote caller never talks to them directly. They
are the machinery that network-facing capabilities use to answer a
request safely.

## Operational consequences

Five consequences follow from keeping the decision organ local:

1. **No authorization roundtrip on the hot path.** When a request
   reaches a passport-aware adapter for Sealer, Signer, or another
   gated surface, the verifier runs in-process against a locally
   maintained `RevocationView`. There is no blocking call to a remote
   authorization service, no TLS handshake, no retry budget. The check
   is local, deterministic, and bounded by local data access.

2. **Sovereign nodes can disagree safely.** Two nodes presented with
   the same passport MAY reach different decisions: they run
   different local policies, have different `T_max` configurations,
   and maintain different revocation views. The passport is the
   *evidence*; the decision is each node's own responsibility. This
   preserves federation autonomy without silently overriding local
   policy with remote intent.

3. **Discovery says "what", not "authorize".** The Seed Directory
   and `CapabilityProfile` advertisements tell a caller *which
   network-facing capabilities a node offers*. They do not bless any
   individual call. A node that advertises `memarium.write` is not
   promising to accept every write; it is promising that a write protocol
   exists and will be evaluated against local policy on arrival.

4. **No central authorization service to bring down.** Because
   decisions are local, there is no single point of failure for
   authorization. A partitioned node may continue to authorize local
   callers only while its local `RevocationView` still satisfies the
   configured freshness bound, or under an explicit degraded/offline
   profile. Revocation staleness is the only time-bounded coupling, and
   it fails *closed* through `SealerError::RevocationStale` rather than
   failing open or escalating to a remote check.

5. **Audit is local and forensic.** Every authorization decision is
   recorded by the acting node's own audit sink. Operators can
   reconstruct "why did this open succeed here?" without cross-node
   log correlation. The passport digest, caller source digest, subject
   id, and matched profile are all captured at the decision site.

## Where things live, practically

```text
Crosses the network:
  - CapabilityProfile advertisements
  - Seed Directory records
  - Capability passports (as signed credentials)
  - Revocation artifacts when they are published for federated consumption
  - AEAD envelopes (sealed bytes)

Stays local to the acting node:
  - CallerIdentity resolution (daemon authtok registry,
    in-process caller map)
  - CallerBinding records (public-key-only)
  - RevocationView (local projection of the revocation feed)
  - Node-local revocation decisions that affect only local dispatch
  - AuthorizationDecision values
  - SealerPolicy / SignerPolicy evaluation
  - Audit events
```

The line is sharp: artifacts cross the network, decisions do not.

## Revocation ontology

Revocation has two distinct layers:

1. A signed revocation artifact says that a capability passport or key
   delegation is no longer valid evidence.
2. A local `RevocationView` says what the acting node currently refuses to
   honor while making an authorization decision.

Those layers often compose, but they are not the same thing. A Node MAY keep a
node-local revocation in its local dispatch projection when the revoked artifact
only affects local modules, local UI, or local host capabilities. Such a
revocation does not need Seed Directory publication.

Seed Directory publication is for artifacts whose validity was, or may be,
relied on by other nodes. It is a federated distribution surface for revocation
artifacts, not the authority that makes local authorization decisions.

## Synthesis

Authorization in Orbiplex is not a service you ask. It is a *property*
of every network-facing capability: the capability owner composes
passport verification, caller binding, and revocation freshness into
one local decision at the point of action.

This is why Sealer and Capability Binding do not appear on the wire.
They are not network-facing capabilities; they are how such capabilities
stay honest.

## Promote when ready

Promote this memo to a requirements document when Orbiplex freezes:

- the stratification between network-facing capabilities and
  internal policy organs,
- the contract between a capability owner and the shared verifier
  pipeline,
- the federation rule that "passport evidence is shared, decision
  authority is not".
