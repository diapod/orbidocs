# Memarium FAQ

Memarium is the Node's local memory organ, not a general database interface.
The answers below concentrate on boundaries: what is a fact, what is a
projection, who may cause an effect, and when missing authority must end in a
refusal.

Operator procedures are documented in the [Memarium HOWTO](../howto/memarium-howto.en.md).

## How is Memarium different from an ordinary document store?

A store primarily answers "where should these bytes be saved?". Memarium
answers a harder question: "in which memory space may this fact be retained,
under which classification, retention, forgetting rule, and audit trail?".

Memarium therefore does not grant ambient authority merely because code runs
inside the Node process. Writes, reads, promotions, forgetting, and
declassification cross explicit contracts and policy gates.

## How should I choose a memory space?

- **Personal** holds the Node owner's memory. It is encrypted and does not
  leave the Node without an explicit export.
- **Community** holds shared community knowledge. It requires a `community_id`,
  a community key, and governance appropriate to that community.
- **Public** holds material intended for public use or publication. A public
  space does not remove classification or provenance requirements.
- **Crisis** holds emergency material. It has a constitutional retention
  minimum and separate rules for resolving an active finding.

A space is a policy envelope, not a separate database. Moving material between
spaces is a new, auditable transition rather than a label change on an existing
record.

## Why does Memarium require a passport?

A passport is an external, signed, and revocable representation of authority.
It binds a caller to a capability, memory space, artifact class, and – where
needed – a community id or egress surface.

Without a passport, the daemon would either trust code merely because it runs
"inside", or duplicate operator, module, and delegate recognition in every
domain engine. The first choice creates ambient authority; the second
complects layers. Memarium uses a third arrangement: the gate authorizes and
the engine executes.

The complete architectural rationale, including A0/A1/A2 separation, revocable
delegation, causal audit, and Crisis authority, is retained in
[Solution 002](../../project/60-solutions/002-memarium/002-memarium.md#why-the-passport-gate-is-architectural).

## Does the HTTP token replace the passport?

No. The token authenticates the channel and lets the host identify the caller.
The passport answers a different question: whether that caller may perform this
operation over this scope. Valid authentication without a matching passport
ends in `passport_lookup_failed` or a more specific refusal.

## Is classification part of the payload?

Classification is a separate first-class `classification.v1` contract. It
must not be hidden in `attributes`, `fields`, or document prose. This lets an
egress adapter derive the permitted projection for an exact surface, topic,
and time without guessing the producer's intent.

A missing required classification does not mean "public". In strict mode it
means refusal. A controlled migration mode may stamp Personal and quarantine
the record, but that exception is measured and has explicit retirement gates.

## Does declassification modify the stored fact?

No. `memarium.declassify` appends a separate policy fact. The source tier,
payload, and history stay immutable. A declassification is bound to a surface,
topic class, use mode, time, and current revocation view.

Consequently, "this fact may be published to Agora" does not mean "the fact is
public everywhere". A one-shot grant is consumed before the effect, and a
missing fresh revocation view makes the exception inert.

## How do `forget`, quarantine, and declassification differ?

- **Forget** removes availability according to the space policy. Personal may
  permit immediate forgetting, Community requires a governance ref, Public
  leaves a tombstone, and Crisis is restricted.
- **Quarantine** prevents use until an operator decides. Acceptance and
  rejection are separate facts and do not rewrite history.
- **Declassification** permits narrower use on a named surface. It is neither
  deletion nor a general lowering of the source tier.

## Can a Memarium observer block a message?

No. Post-chain and phase observers are observational paths: they can see the
effective payload and dispatch result, but cannot change the decision, payload,
or outcome. An observation write failure may degrade diagnostics, but does not
become a hidden second admission system.

When an effect requires an authoritative write before execution, the caller
must invoke explicit `memarium.write` rather than rely on an observer.

## Is the SQLite sidecar the source of truth?

No. Append-only entry and fact streams remain authoritative. The SQLite
sidecar is a rebuildable projection that accelerates point reads and policy
views. Startup performs catch-up, while stream scanning remains the correctness
path when the sidecar is disabled or requires rebuilding.

Do not repair Memarium by editing the sidecar directly. Such a change creates
no fact, crosses no policy gate, and disappears on rebuild.

## Does Memarium replicate automatically between Nodes?

Not as a general mechanism. Public artifacts may be carried through Agora and
archival material through Artifact Delivery, but those are explicit handoffs
with classification and provenance. Community material does not cross a
federation boundary merely because the parties share a Room or group.

Full automatic federated Memarium replication remains outside the v1 contract.
The carrier does not become the owner of memory policy.

## Who may resolve a Crisis-space finding?

A detector may append `crisis-detected` and an automatic `crisis-resolved` when
the condition actually clears. Forced resolution through
`memarium.crisis_resolve` is an operator action, requires a reason, and does not
erase finding history.

Clicking "resolved" does not repair the underlying condition. The operator
should first verify the condition described by the
[detector runbook](../runbooks/crisis-detectors.md), then append an explicit
resolution fact.

## Where should I look for the cause of a refusal?

Clients should interpret the stable `status` field, not parse the human
`reason`. Common classes include missing or invalid passports, a stale
revocation view, a space policy violation, quarantine, absent
declassification, and storage failure. The response and audit decision share
one cause and correlation id; diagnostics should not be reconstructed from
loose logs.

The complete closed status vocabulary belongs to
[Solution 002](../../project/60-solutions/002-memarium/002-memarium.md).
