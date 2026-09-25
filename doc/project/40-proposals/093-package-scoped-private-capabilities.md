# Proposal 093: Package-Scoped Private Capabilities

Based on:

- `doc/project/40-proposals/024-capability-passports-and-network-ledger-delegation.md`
- `doc/project/40-proposals/072-capability-registry.md`
- `doc/project/40-proposals/080-multiplexed-middleware-channel-executor.md`
- `doc/project/40-proposals/085-operator-sovereign-extensibility-and-experiment-packages.md`
- `doc/project/60-solutions/006-capability-binding/006-capability-binding.md`
- `doc/project/60-solutions/019-middleware/019-middleware.md`
- `doc/project/60-solutions/028-temporal-storage-convention/028-temporal-storage-convention.md`
- `doc/project/60-solutions/037-capability-registry/037-capability-registry.md`
- `doc/project/60-solutions/048-operator-sovereign-extensibility/048-operator-sovereign-extensibility.md`
- `node:DEV-GUIDELINES.md` (Data and Contracts; Avoid Entanglement #5; Review #1, #2,
  #3, #5, #6, #7, #10, #11, #12, #14, #15, #16; Rust-Specific #5, #11)

Amends:

- P072 §1 identifier grammar: adds a fifth, package-anchored identifier shape and
  collapses the existing grammar copies into one.
- Solution 037: identifier kinds and admissible uses for package identifiers.
- Solution 048: activation-bound declarations, lifecycle, and caller edges for package
  capabilities. It narrows the "extension-defined capabilities" exclusion to its
  intended meaning – extensions still cannot mint primitive capabilities or host
  authority.

## Status

`draft`

## Date

`2026-09-25`

## Executive Summary

The capability registry is deliberately closed: establishing a new kind of host
authority requires a reviewed change to `node:capability/capability-registry.v1.json`.
That rule is correct and this proposal keeps it. It leaves one gap. Behaviour that an
extension package *provides* – a review service, a domain transform, a bounded query –
has no name in the authority system. It is either anonymous or it must enter the global
registry, which is the wrong place for one operator's extension.

This proposal adds a third kind of capability identifier beside registered and sovereign
ones: a **package capability**, anchored to the admitted signing key and package name of
a signed package, carrying its **exposure scope in its namespace**:

```text
review@pkg:did:key:z6MkAuthority…/acme-review       package-internal
review@node-pkg:did:key:z6MkAuthority…/acme-review  grantable to local components
review@peer-pkg:did:key:z6MkAuthority…/acme-review  grantable to remote peers
```

Three separations carry the design:

1. **A behaviour name is not host authority.** A package capability's implementation
   reaches host resources only through base capabilities its activation was actually
   granted. Authority still originates in the checked-in registry.
2. **Scope is not a grant.** The namespace scope can only cause refusal. A call is
   authorized by a current activation, host-attested caller evidence, and – for peers –
   a verified `capability-passport.v1` presented with every request.
3. **A signature is not current consent.** A passport proves who issued it; every
   request rechecks revocation, the issuing operator binding, expiry, the overlay, and
   the contract.

Execution is crash-safe by construction. A durable `started` record is the admission
point; it is written before any effect and ordered against lifecycle transitions. After
it, the outcome is `completed`, `unknown`, or a terminal resolution derived from the
provider's declared effect recovery. A timeout after start is never reported as a safe
refusal and never authorizes re-execution. An `unknown` invocation is resolved only by
provider evidence bound to that exact invocation, or by the operator. Callers learn
outcomes through a read-only status query that never starts work.

## Context and Problem Statement

### The registry is closed by construction

`capability-registry.v1` is compiled into the Node and loaded once into a process-wide
static (`node:capability/src/registry.rs`, `capability_registry()`). Admission is the
context-free `capability_admission_for_use(id, use)`, called from 38 sites. It does not
know which package, activation, or operator is involved – which is why it is a sound
allow-set for base authority, and why it cannot host per-package names without a
separate, context-carrying layer.

### Extension behaviour is already named informally

Middleware module reports declare offered capabilities
(`node:middleware/src/module_report.rs`, `MiddlewareOfferedCapability`) with a `class`
of `Base` or `Other`. An `Other` identifier is validated only as non-empty. It cannot
become routable, because host-route admission requires the checked-in registry. The
fail-closed promise of P072 holds, but such an identifier is neither rejected at report
admission nor usable for anything.

### P085 derived capabilities are the wrong home

P085 §9 derived capabilities are intersections of base capabilities and never create a
new callable surface. A package capability does create a new callable surface, so it
must not live under §9.

### Findings that constrain the design

- **The identifier grammar exists in four copies with three character sets.** The
  protocol validator (`node:protocol/src/lib.rs`, `validate_canonical_capability_id`)
  admits lowercase letters, digits, `.`, `-`, `_`, `/`. The passport schema
  (`capability-passport.v1`) admits lowercase letters, digits, `_`, `/`, `-`. The
  capability parser and the registry shape validator (`node:capability/src/lib.rs`,
  `node:capability/src/registry.rs`) admit upper- and lowercase letters, digits, `-`,
  `_`, `/`. Each copy carries its own list of anchor prefixes. Adding a fifth shape to
  four divergent copies would multiply the divergence.
- **Identifier kind is inferred from a string heuristic.** `is_sovereign_capability` is
  `capability_id.contains('@')` and has nine callers, contrary to DEV-GUIDELINES Review
  #5. Protocol validation of capability advertisements runs first and restricts anchors
  to participant, node, and org, so an unknown `@`-shape does not pass advertisement
  ingress today. The registry admission that follows then skips every `@` identifier
  with `continue`. The defect is the inference, not an open gate: every new `@`-shape
  silently takes the sovereign branch wherever the protocol validator does not stand in
  front of it.
- **The component contract digest is opaque.** `middleware-component-contract.v1`
  binds providers and requirers by the exact pair `(capability/ref, contract/digest)`
  (P080), and P085 fixes its format as `sha256:<base64url-no-pad>`. No document defines
  which bytes the digest covers.
- **`package_ref` is not bound to the signing authority.** Package references have the
  form `extension-package:<name>`; two authorities can ship the same reference. The
  admitted authority is the key in `trusted_signing_keys` that verified the package
  signature (`node:operator-extension-service/src/lib.rs`).
- **Sovereign wire names deliberately omit the anchor.** `sovereign_wire_name` returns
  `sovereign/{name}` so Seed Directory can query one name across anchors. Package
  capabilities are not discovered by name and must not reuse that projection.

## Goals

- Give extension-provided behaviour a stable name that grants, policy, traces, and
  refusal corpora can refer to.
- Let the operator expose it to local components and remote peers, each only under
  explicit, attributable grants.
- Keep the checked-in registry the sole origin of host authority.
- Make exposure scope visible in every identifier and impossible to widen silently.
- Make invocation crash-safe: no effect without a durable record, no re-execution after
  an uncertain outcome.
- Reuse existing primitives: capability passports and their revocation, P085 activation
  generations and journal, the P080 component contract and graph, `capability-schema.v1`
  presentation, and the effect recovery declarations of the component contract.

## Non-Goals

- Advertisement or Seed Directory discovery of package capabilities.
- Public namespace allocation; package identifiers are namespaced by their authority.
- Grant delegation by a holder, and delegated grant issuers.
- Author-identity anchors that survive signing-key rotation.
- A package capability carrying a signing domain, federated discovery, or registry-level
  passport eligibility.
- Replacing P085 derived capabilities.

## Terminology

- **Base capability** – admitted by the checked-in registry (bare dotted or `core/*`).
- **Sovereign capability** – `name@participant|node|org:did:key:…`, per P072.
- **Package capability** – `name@<scope-ns>:did:key:…/<package>`, defined here.
- **Scope** – exposure class `package`, `node`, or `peer`, encoded as `pkg`, `node-pkg`,
  `peer-pkg`.
- **Provider** – the node and package component that serves a package capability.
- **Contract** – the `package-capability-contract.v1` document naming the input and
  output schemas; its digest is the `contract/digest`.
- **Requirement edge** – an operator-approved `(consumer activation, capability id,
  contract digest)` triple in a consumer's activation plan.
- **Admission point** – the durable `started` record of one invocation.
- **Suspension** – a package capability is absent from the current overlay, but grants
  bound to it remain valid.
- **Retirement** – terminal revocation; a tombstone voids earlier grants.
- **Reconciliation evidence** – the provider's answer from its durable journal about
  one invocation, bound to that invocation's caller, request digest, and execution
  context.
- **Protected-until** – the instant, fixed at admission, until which a record guarantees
  at-most-once execution for its identifier.

## Resolved Decisions

Recorded on `2026-09-25`.

1. **Anchor.** Version 1 anchors on the admitted signing key. Stable author identity is
   later work. The existing trust model is reused; key rotation requires new identifiers
   and new grants.
2. **Namespace tokens.** `pkg`, `node-pkg`, `peer-pkg`.
3. **Discovery.** No advertisement in version 1. Discovery is through the grant, so the
   package catalogue is not disclosed and the first release does not depend on a
   publication policy.
4. **Issuers.** No delegated issuers in version 1. Every grant is signed by the current
   operator, which keeps verification and termination simple.
5. **Presentation.** The passport is presented with every invocation, so each request
   is self-contained. A cache may hold only the result of signature verification; the
   currency of the grant is checked on every request.
6. **Defaults.** A working start profile calibrated by measurement (§12). Results may be
   dropped early under capacity pressure; replay protection may not. `started` and
   unresolved `unknown` records follow their own retention rule, and a configuration
   change never shortens protection already promised.
7. **Reconciliation.** The component contract gains an optional
   `reconciliation/operation`. Automatic resolution is allowed only from evidence that is
   read-only, bound to the exact invocation, never inferred from `not-found`, and never
   a substitute for output validation or an authorization to compensate (§9).
8. **Status query.** `package-capability.status.request` is part of version 1: a
   read-only contract over the host journal that never starts the provider or
   reconciliation and works after the original admission window while the record and a
   current grant exist (§13).

## Proposed Model / Decision

### 1. Three kinds of capability names

| kind | origin | stands for | may be used for |
| :--- | :--- | :--- | :--- |
| base | checked-in registry | a kind of host authority | the six P072 uses |
| derived (P085 §9) | operator overlay | an intersection of base grants | nothing new |
| **package** | signed package, current activation | behaviour the package provides | dispatch and host route, within scope |

### 2. One grammar, and scope in the namespace

```text
capability-id         = registered-id / sovereign-id / package-capability-id
package-capability-id = name "@" scope-ns ":" authority "/" package-name
scope-ns              = "pkg" / "node-pkg" / "peer-pkg"
authority             = "did:key:z" base58btc-ed25519-key
name                  = [a-z0-9] *[a-z0-9_/-]
package-name          = [a-z0-9] *[a-z0-9-]
```

The `name` character set is the strict intersection of the four existing copies, so no
identifier valid today in all four becomes invalid. One parser in
`orbiplex-node-capability` becomes the only implementation; the protocol validator, the
registry shape check, and the passport schema pattern are generated from or checked
against it. The identifier is its own wire form.

**Options considered for carrying scope:**

| option | assessment |
| :--- | :--- |
| a declaration field only | Rejected. A new version could widen `node` to `peer` under an unchanged identifier. |
| a sigil in the name, like `~` | Rejected. Adds a glyph and hides exposure in the least-read part. |
| **the namespace token** | Chosen. Exposure is read first, is part of identity, and is checkable by parsing. |

A grant for `review@node-pkg:…` can therefore never reach peers: widening exposure
produces a different identifier and requires new grants.

**Reconciliation with DEV-GUIDELINES Review #5.** The scope token has exactly two
permitted uses, both of which can only refuse: a deny-only reach filter, and a
commitment check against the signed declaration's `capability/scope` (the pattern P072
uses for `surfaces`). Parsing a `peer-pkg` identifier admits nothing.

### 3. The anchor binds the verifying key and the package name

At activation, `authority` must equal the `did:key` of the key that verified the package
signature and is present in the host's trusted package-signing keys, and `package-name`
must equal the name part of the package's `package_ref`. Both are compared, never
trusted as labels (DEV-GUIDELINES Review #3). Two authorities cannot collide on a
name, and one authority cannot anchor another of its packages' names.

### 4. A package capability names behaviour, never authority

The declaration lists the base capabilities its implementation requires. They must be a
subset of the base capabilities the operator actually **granted** to this activation in
its P085 plan; registry eligibility for `Dispatch` is necessary but not sufficient. The
provider's own host calls continue to run under the activation's grant set.

The overlay entry has no eligibility flags. Advertisement, registry passport
eligibility, signing domain, and federated discovery are unrepresentable rather than
`false`.

### 5. The declaration reuses the component contract

A package capability is provided by exactly one supervised component whose
`middleware-component-contract.v1` contains a `provides[]` entry
`{capability/ref: <package capability id>, contract/digest: <digest of §6>}`. The
declaration refers to that entry and to the `effects` ids an invocation may produce;
it does not restate them. P080 graph resolution and P093 grants therefore use one
digest, and recovery semantics come from the existing effect declarations – including
`journal/ref`, `compensation/operation`, and `approval/policy-ref` – rather than from a
bare four-valued enum.

The **recovery class of an invocation** is the most restrictive class among its
referenced effects, ordered `irreversible-external > compensatable >
transactional-withheld > ephemeral-revertible`. An empty effect list declares a
read-only operation. This aggregate selects the conservative recovery path; it does
not replace the individual effect declarations. Completion or abandonment evidence
must cover the whole invocation, not merely one effect of its highest class.

Effects of the classes `transactional-withheld`, `compensatable`, and
`irreversible-external` may declare an optional `reconciliation/operation` in the
component contract: a read-only, time-bounded query that reports, from the provider's
durable journal, what became of one invocation (§9). A package capability whose
recovery class is `transactional-withheld` must declare it, because its correctness
claim – nothing visible before a durable commit – can only be checked through it. This
amends `middleware-component-contract.v1`.

### 6. The contract digest and package-bound schemas

`contract/digest` for a package capability is frozen as:

```text
sha256:<base64url-no-pad>( JCS-v1( package-capability-contract.v1 document ) )
```

The contract document names the input and output schemas as package members by path and
digest. Each schema digest is taken over the JCS bytes of the schema document. Schemas
are package-bound: they are covered by the package digest, and no schema is fetched from
outside the package or the Node's canonical schema set.

Reference resolution is bounded. A `$ref` may point only into the same document, to
another package schema listed in the contract's `refs` map (path plus digest), or to a
canonical schema id known to the Node schema gate. URLs and filesystem paths outside the
package are refused. Schema bytes, reference depth, and schema count are capped. Schemas
are compiled once at activation; compilation failure refuses the activation.

Validation points:

- the provider host validates input before the admission point, so a malformed request
  never starts;
- the provider host validates output before recording `completed`; an invalid output is
  never released, the invocation becomes `unknown` with local cause
  `output-contract-violation`, and the provider is marked degraded;
- a calling node obtains the contract document and schemas as `capability-schema.v1`
  artifacts through `capability.schema.present`, verifies them against `contract/digest`,
  caches them by digest, and validates the output before releasing it to its local
  consumer.

### 7. Reach, caller evidence, and requirement edges

| scope \\ caller | same-package | local-component | remote-peer |
| :--- | :---: | :---: | :---: |
| `pkg` | reach | – | – |
| `node-pkg` | reach | reach | – |
| `peer-pkg` | reach | reach | reach |

Reach is necessary, never sufficient. Caller evidence is produced by the host from its
own session bindings, never from request payload:

- **same-package** – the host attests the calling component and its activation from the
  supervised channel session; admission requires that component to belong to the
  declaring package under the entry's current activation. A matching anchor alone is not
  evidence.
- **local-component** – the host attests the calling component or binding and its
  current activation, plus the exact requirement edge `(consumer activation, capability
  id, contract digest)` approved in that activation's plan. A current consumer fence
  alone is not evidence.
- **remote-peer** – the authenticated session node plus a passport verified as in §8.

### 8. Peer grants are capability passports, presented with every request

A peer grant is a `capability-passport.v1` with these rules for package identifiers:

- `capability_id` is a `peer-pkg` identifier; `pkg` and `node-pkg` identifiers are
  refused in passports;
- the issuer is the provider node's current operator under a live
  `node-operator-binding`, and `issuer_delegation` is absent;
- `node_id`, the holder, is the calling node and differs from the issuer node;
- `expires_at` is required;
- `scope` carries `contract/digest`.

Every request carries the passport. Signature verification may be cached by passport
digest. Everything else is checked on every request: holder equals the authenticated
session node, exact identifier and contract digest, expiry, passport revocation, that
the issuing binding is still the current binding, and the tombstone watermark.

Binding the contract digest rather than the package digest is deliberate: a rebuild
that keeps the contract keeps the grant; a contract change makes it stop resolving.

### 9. Invocation journal and outcomes

The provider records invocations in one append-only journal, following the Temporal
Storage Convention. It is also the idempotency store, so recovery has one source of
truth (DEV-GUIDELINES Review #11).

**Admission point.** Admission (§11) ends by durably appending a `started` record. That
append happens while holding a read gate on the activation generation, after rechecking
that the generation is still the admitting one. P085 transitions hold the write gate
across their durable commit and the overlay publication (§10). Every `started` record
therefore precedes or follows every lifecycle transition, and a record cannot exist for
a generation that was already revoked.

- **Before the admission point**, any lifecycle change, readiness loss, or grant change
  refuses the request. Nothing has started.
- **After it**, the invocation runs under its admitting generation. A later revocation
  prevents new starts; it does not abort started work. Safe mode stops providers, and
  started work then resolves through its recovery class. Budgets bound how long started
  work may run.

The `started` record freezes the admitting package digest, provider, contract digest,
referenced effect declarations, recovery class, effective deadline, and retention
promises, directly or through immutable retained references. Recovery never looks up
these meanings in the current overlay: an upgrade or removal must not reinterpret an
unfinished invocation. Referenced recovery material remains available until resolution.

**Outcome state machine.** A record exists only from the admission point on; refusals
are not invocations.

| from | event | recovery class | to |
| :--- | :--- | :--- | :--- |
| `started` | provider returned valid output | any | `completed` |
| `started` | provider output failed the contract | any | `unknown` |
| `started` | no outcome (deadline or crash) | read-only | `aborted` |
| `started` | no outcome | `ephemeral-revertible` | `unknown`, pending confirmed disposal |
| `started` | no outcome | any other | `unknown` |
| `unknown` | bound reconciliation evidence | see the resolution table | `completed` or `aborted` |
| `unknown` | invalid output, with no effects possible | read-only | `aborted` |
| `unknown` | all declared ephemeral resources confirmed disposed | `ephemeral-revertible` | `aborted` |
| `unknown` | operator resolution | `transactional-withheld` | `completed` or `aborted` |
| `unknown` | operator resolution | `compensatable` | `completed`, `compensated`, or `aborted` |
| `unknown` | operator resolution under the declared approval policy | `irreversible-external` | `completed` or `aborted` |

`completed`, `aborted`, and `compensated` are terminal. A timeout after start is never
`refused` and never permits re-execution. On restart, every `started` record without an
outcome is moved by this table before new invocations are admitted, and nothing is
executed again.

**Evidence-bound reconciliation.** A host recovery worker may resolve an `unknown`
invocation without the operator, only from evidence that satisfies four conditions:

1. **Read-only.** The evidence comes from the declared `reconciliation/operation`,
   which is read-only, runs under its own time budget, and never re-runs the original
   work. A provider that declares none is resolved by the operator.
2. **Bound.** The evidence names the `invocation/id`, authenticated `caller`,
   `request/digest`, capability identifier, contract digest, and admitting activation
   generation, and the host requires every field to equal the journal's `started`
   record. It also covers the exact recorded `effect/refs` set and comes through the
   authenticated recovery binding of the recorded provider. Echoing correct identifiers
   is not proof of provenance, and a bare "done" is not evidence.
3. **Absence proves nothing.** `not-found` means the entry may not exist yet, may have
   been lost, or may be unreachable; it is never read as `aborted`.
4. **Commit is not output.** Evidence of a committed effect resolves the effect, not the
   result. It releases no output that did not pass contract validation, and it never
   authorizes compensation.

| evidence state | `transactional-withheld` | `compensatable` | `irreversible-external` |
| :--- | :--- | :--- | :--- |
| `committed` | `completed` | `completed` | `completed` |
| `abandoned` (no covered effect became visible, and future execution of this identifier is permanently fenced) | `aborted` | `aborted` | stays `unknown`, operator |
| `pending` | stays `unknown`, retry later | same | same |
| `not-found` | stays `unknown`, retry later | same | same |
| `unavailable` or timed out | stays `unknown`, retry later | same | same |
| any field unbound or mismatched | stays `unknown`; provider degraded; operator diagnostic | same | same |

A `completed` reached through evidence carries `result/status: retained` only when a
validated output is retained, and `unavailable` otherwise. `output/digest` is present
only if the host previously validated that output; commit evidence alone cannot supply
or invent it. A partial commit remains `unknown`, and a fence against future execution
does not undo effects that already happened. `abandoned` does not resolve
`irreversible-external` automatically, because an external system may have acted
beyond what the provider journaled; the operator decides under the declared approval
policy. `compensated` is only ever an operator resolution. Reconciliation attempts back
off, are bounded in number, and then escalate to the operator resolution queue under the
P085 operator-attention policy.

Resolution is a conditional journal transition from the still-current nonterminal
state. Concurrent provider replies, reconciliation, and operator resolutions cannot
overwrite a terminal outcome. Safe mode never starts a provider merely to reconcile;
unavailable recovery evidence leaves the record `unknown` for operator handling.

### 10. Lifecycle: suspension, retirement, and the P085 journal

The overlay is a projection of the P085 lifecycle journal. A transition commits its
lifecycle facts – and, for revocation, the tombstones – in one transaction. The overlay
is rebuilt from the committed journal and published while the write gate is still held.
A crash between commit and publication is repaired at startup by rebuilding from the
journal; an in-memory `Arc` swap provides read consistency, the journal provides
durability.

| event | overlay entry | existing grants | new invocations | started invocations | tombstone |
| :--- | :--- | :--- | :--- | :--- | :--- |
| activate, first | added | – | admitted | – | – |
| activate, same contract digest | replaced | continue | admitted | continue under the admitting generation | – |
| activate, changed contract | replaced | stop resolving (contract mismatch), not voided | admitted with grants for the new contract | continue under the admitting generation | – |
| activate, capability no longer declared | removed | suspended | refused | continue | – |
| rollback | restored to the earlier set | grants for the restored contract resolve again | admitted | continue | – |
| safe mode, enter | all package entries removed | suspended | refused | providers stop; resolved by §9 | – |
| safe mode, exit | restored if still activated | resume | admitted | – | – |
| session activation expiry | removed | suspended | refused | resolved by §9 | – |
| daemon restart | rebuilt from the journal | unchanged | admitted after recovery | resolved by §9 | – |
| revoke (terminal) | removed | voided below the watermark | refused | continue under the admitting generation | written in the revoke transaction |
| reinstall after revoke | added under a new activation | earlier grants stay void | admitted with new grants | – | watermark retained |

Suspension preserves grants because the operator may restore the capability; retirement
voids them because terminal revocation cannot be rolled back. For local consumers,
removal from the overlay is a dependency lifecycle transition (DEV-GUIDELINES Review
#16): the capability becomes non-routable, bounded work drains, and dependents observe
`dependency_unavailable`.

### 11. Admission order

Local and peer invocations share one order. No write, enqueue, or dispatch happens
before step 9 (DEV-GUIDELINES Review #1).

1. Check `issued-at` against the replay window (§12); local and peer requests both
   carry it.
2. Parse the identifier; refuse anything outside the caller's reach.
3. Resolve the overlay entry; compare the declared scope with the identifier.
4. Compare `contract/digest`.
5. Verify caller evidence (§7) and, for peers, the passport (§8).
6. Apply the replay decision (§12).
7. Validate input against the contract (§6).
8. Check provider readiness and contract compatibility in the P080 graph.
9. Reserve the budget, take the generation read gate, recheck the generation and
   current authorization, then atomically check the invocation key and admission floor
   and append `started` only if absent and still admissible. A concurrent winner yields its recorded state or a fingerprint
   conflict; release the unused reservation and do not dispatch again. Release the gate.
10. Dispatch; record the outcome; respond.

**Refusals are not an installation oracle.** Every refusal before step 5 completes is
returned to a peer as `unavailable`. A peer that passed step 5 holds a valid grant and
may learn `busy`, `deadline-exceeded`, `invocation-id-conflict`, or `invalid-input`.
`stale-request` depends only on the request's own timestamp and is visible at step 1.
Local operator diagnostics keep the precise cause.

### 12. Idempotency contract

- **Key.** `(caller, invocation/id)` everywhere: in the journal, in the replay
  decision, and in every invocation fact. `caller` is a host-derived tagged reference:
  `{"kind":"node","ref":<authenticated peer node id>}` for peers, or
  `{"kind":"component","ref":<local component ref>}` / `{"kind":"binding","ref":<local binding ref>}`
  for local calls. These variants are disjoint; using only the host node id for local
  calls would conflate different components. Caller identity is never taken from the
  request payload.
- **Request fingerprint.** `request/digest` is taken over the JCS bytes of
  `{capability/id, contract/digest, issued-at, deadline, input}`. The passport is
  authorization evidence, not request content, and is excluded. The same key with a different
  fingerprint is refused as `invocation-id-conflict`.
- **Replay window.** Requests carry `issued-at`. A request outside
  `[now − replay window, now + clock skew]` is refused as `stale-request`. At admission
  the host computes `protected-until = issued-at + replay window + clock skew` from the
  configuration then in force and stores it in the record. A later configuration change
  never shortens a protection already promised. Any request that could still match a
  record is either answered from it or refused as stale. After `protected-until`, the
  provider no longer guarantees at-most-once for that identifier; callers must not
  reuse invocation identifiers.
- **Window growth and cleanup.** A wider window or clock rollback must not make a
  purged request new again. The journal retains a monotonic `admission/not-before`
  timestamp per capability. Before deleting a resolved record, cleanup atomically
  advances that floor to at least the deleted record's `issued-at`. An absent key with
  `issued-at <= admission/not-before` is refused as `stale-request`, even if today's
  wider window would admit it. Existing records still follow the replay rules. Floors
  survive restart and capability reactivation; they are not ordinary evictable cache
  entries. This deliberately prefers refusing an old first attempt to repeating an
  effect whose record is gone.
- **Record retention.** A record is kept at least until `protected-until`. A record in
  `started` or an unresolved `unknown` is kept until it is resolved, whatever its
  `protected-until`, because it is the only evidence that an effect may have happened;
  after resolution it is kept at least for the result retention period, so the caller
  can observe the resolution through a status query (§13).
- **Capacity.** The journal is bounded by record count and bytes, but a protected or
  unresolved record is never evicted. When such records exhaust capacity, new
  invocations are refused as `busy` and the operator sees a capacity diagnostic.
- **Result retention.** Outputs are retained for a bounded period from completion,
  never longer than the record, up to a per-result size and a node-wide byte budget.
  Under capacity pressure a retained output may be dropped early; replay protection may
  not. A replay or status query of a `completed` invocation returns the retained output
  or, once it is gone, `completed` with `result/status: unavailable` – explicitly
  without re-execution.
- **Replay decisions.** A replay of `refused` is admitted afresh, since nothing started;
  for that reason resending a request is not a status read (§13). A replay of
  `started` reports `started` without dispatch; `completed` returns its recorded result.
  `aborted` and `compensated` are terminal for their identifiers; a retry uses a new
  identifier. `unknown` returns `unknown` until reconciliation or an
  operator resolution records a terminal outcome. Every replay rechecks the grant, so a
  holder whose grant was revoked cannot collect a result.

**Working start profile.** The values below are a hypothesis to be calibrated by
measurement, not a confirmed production profile. They let the mechanism be implemented
and tested without claiming that the numbers are settled.

| parameter | starting value |
| :--- | ---: |
| default replay window ceiling | 1 h |
| clock skew allowance | 60 s |
| result retention from completion | 15 min, never beyond the record |
| maximum retained result | 256 KiB |
| node-wide retained-result budget | 64 MiB |

Calibration measures the retry-delay distribution, the result-size distribution, and
journal growth at the target invocation rate (`P093-039`).

### 13. Status query

`package-capability.status.request` is part of version 1. It gives callers an
unambiguously read-only way to learn what happened to an invocation, without resending
input and without any possibility of starting work. Resending the original request is
not a substitute: a replay of a previously refused request is admitted afresh and may
start execution.

A status query:

- carries `capability/id`, `contract/digest`, `invocation/id`, and `request/digest`,
  plus the passport for peers; it never carries input;
- is authorized exactly like an invocation – reach, overlay entry, contract digest,
  caller evidence, and a current grant – and is answered only for the caller recorded
  under its own key; a different `request/digest` under the same key is refused as
  `invocation-id-conflict`;
- reads only the host journal: it never dispatches to the provider, never runs
  reconciliation, and never changes a record;
- remains answerable after the original request's admission window has closed, for as
  long as the record exists and the caller still holds a current grant;
- returns the recorded state – `started`, `completed`, `aborted`, `compensated`, or
  `unknown` – with `result/status` for `completed`, `output/digest` when known from
  validated output, and the output itself while it is retained;
- returns `not-found` when no record exists under the caller's key, which does not prove
  that the invocation never ran: the record may have aged out or never been written.

### 14. Responsibility split

- **Solution 037** owns identifier kinds and admissible uses: one grammar, closed kinds,
  base admission refusing package identifiers, package identifiers limited to dispatch
  and host route, and passport *shape* acceptance of `peer-pkg` identifiers.
- **Solution 048** owns activations: declarations in packages, anchor and scope checks,
  the overlay as a projection of the P085 journal, suspension and retirement, tombstones,
  and requirement edges in activation plans.
- **The P093 core** owns invocation: caller evidence, admission order, journal, outcomes,
  recovery, evidence-bound reconciliation, idempotency, status queries, and the peer
  message families. It uses the existing passport verification and will be promoted
  into a solution when implemented.

## Concrete Sequence

```mermaid
sequenceDiagram
    autonumber
    actor OpP as Operator of provider P
    participant P as Node P (provider)
    participant C as Node C (caller)
    OpP->>P: activate acme-review (plan: review@peer-pkg:…, required base granted)
    P->>P: verify key and package name, scope commitment, provides entry, schemas
    P->>P: commit activation in P085 journal; publish overlay under write gate
    OpP->>P: issue capability-passport.v1 (holder C, review@peer-pkg:…, contract/digest, expires_at)
    P-->>C: passport delivered out of band or via capability.passport.present
    P-->>C: capability.schema.present (contract and schemas by digest)
    C->>P: package-capability.invoke.request (passport, id, contract/digest, issued-at, input)
    P->>P: window, reach, entry, contract, passport, replay, input, readiness
    P->>P: read gate: recheck generation, append started
    P->>P: dispatch; validate output; record completed
    P--xC: invoke.response lost (completed, output, output/digest)
    Note over C,P: C asks for status instead of resending input
    C->>P: package-capability.status.request (passport, id, contract/digest, request/digest)
    P->>P: reach, entry, contract, passport; read journal only
    P-->>C: status.response (completed, retained output, output/digest)
    C->>C: validate output against cached schema, release to consumer
    OpP->>P: revoke acme-review
    P->>P: write gate: commit revoke and tombstone; publish overlay without entry
    C->>P: new invoke
    P-->>C: refused: unavailable
```

## Trade-offs

- **One grammar costs a migration.** Four copies collapse into one parser; the
  migration touches the protocol validator, the registry, the passport schema, and nine
  heuristic call sites. That is also the fix for the existing drift.
- **Scope in identity is rigid.** Changing exposure means new identifiers and grants –
  the intended security property.
- **Key-anchored namespaces follow key rotation.** Accepted for version 1.
- **The generation gate serializes lifecycle transitions behind in-flight admissions.**
  A transition waits for starts that are appending their record. The wait is bounded by
  one durable append per concurrent start, and a pending-transition flag that holds
  back new admissions prevents starvation.
- **Uncertain outcomes need operator work unless the provider can prove them.**
  Effectful invocations can end in `unknown`. Evidence-bound reconciliation removes most
  of that work, but only for providers that declare a reconciliation operation, and
  never for `abandoned` external effects. That is the truthful cost of those effects.
- **Reconciliation raises the contract bar for providers.** A `transactional-withheld`
  provider must expose a read-only, invocation-keyed status of its own journal.
- **A second message family.** The status query adds `package-capability.status.*`
  beside `package-capability.invoke.*`; in exchange, observing an outcome can never start
  work.
- **Start-profile numbers are provisional.** Implementation proceeds on a hypothesis;
  calibration may change retention and budgets before production use.
- **Every request carries its passport.** Requests are larger; in exchange they are
  self-contained and never depend on session state for authorization.

## Failure Modes and Mitigations

| failure mode | mitigation |
| :--- | :--- |
| Effect happens but no record exists | `started` is durable before dispatch; restart resolves every unfinished record by its recovery class. |
| Timeout after start treated as safe | Outcome derives from the recovery class; `refused` exists only before the admission point. |
| Retry re-executes an uncertain effect | Replay returns `unknown` until resolution; `aborted` is terminal for its identifier. |
| Same invocation id reused with different input | Request fingerprint mismatch refuses as `invocation-id-conflict`. |
| Capacity pressure evicts replay protection | Protected records are never evicted; new work is refused as `busy`. |
| Result lost after completion | Bounded retention, then `completed` with `result/status: unavailable`, never re-execution. |
| Revocation races admission | The generation gate orders every `started` record against every transition. |
| Crash between journal commit and overlay publication | Overlay rebuilt from the journal at startup. |
| Upgrade silently changes the contract | Grants bind `contract/digest`; mismatch stops resolution. |
| Suspended capability loses its grants | Only terminal revocation writes a tombstone; suspension preserves grants. |
| A component impersonates another package | Caller evidence comes from host session bindings, never from payload. |
| A package anchors another package's name | Activation compares the package name as well as the verifying key. |
| A declaration claims authority not granted | `required_base` must be a subset of the activation's granted base capabilities. |
| Provider returns output outside its contract | Output validated before release; invocation becomes `unknown`; provider degraded. |
| A schema references remote material | Bounded package-internal and canonical resolution only; activation refuses otherwise. |
| A peer probes installation state | Uniform `unavailable` before caller evidence is verified. |
| A new identifier shape is added later | One closed `CapabilityId` with exhaustive matching. |
| A configuration change shortens promised protection | `protected-until` is fixed in each record at admission. |
| A wider window resurrects a purged request | Durable admission floors advance atomically with record cleanup; an absent key below the floor is stale. |
| Concurrent retries both pass the initial lookup | The journal atomically checks the key and appends one `started`; only its winner dispatches. |
| Recovery uses an upgraded or removed declaration | Each start retains its admitting recovery context, independent of the current overlay. |
| Unresolved records are evicted | `started` and unresolved `unknown` records are kept until resolved; capacity pressure refuses new work instead. |
| Retained results exhaust memory | Per-result size cap and node-wide budget; results are dropped before any protection is. |
| A provider answers reconciliation with a bare "done" | Evidence must bind caller, request digest, identifier, contract, and generation; unbound evidence leaves `unknown` and degrades the provider. |
| `not-found` is read as "never ran" | `not-found` never resolves `unknown`, and in status responses it is explicitly not proof of non-execution. |
| A still-running or partially committed invocation is resolved as abandoned | `abandoned` requires both absence of visible covered effects and a permanent execution fence; partial or pending work stays `unknown`. |
| Commit evidence releases an unvalidated output | Evidence resolves the effect only; output is released only after contract validation. |
| A status query starts work | Status is a separate read-only family that never dispatches or reconciles. |

## Security and Privacy

- Authority originates only in the checked-in registry and in grants made at activation.
- Authorization precedes every effect; missing authority denies.
- The anchor, the calling component, and the grant are all verified evidence, never
  labels or payload claims.
- Remote refusals are uniform before caller evidence is verified.
- Grants are bounded in time, bound to an exact identifier and contract, signed by the
  current operator, and ended by passport revocation, binding change, or tombstone.
- No discovery surface discloses package capabilities to ungranted peers.
- Invocation facts record identifiers, digests, caller node, outcome, and timing; input
  and output payloads are retained only as bounded results, never in traces.

## Open Questions

None blocks implementation. The start-profile values of §12 are a measurement
hypothesis, and their calibration is tracked as `P093-039` rather than left open.

## Next Actions

1. Review this draft.
2. Land Phase 0 independently; it removes the four-copy grammar drift and the
   `contains('@')` heuristic, which are defects regardless of this proposal.
3. Define `package-capability-contract.v1`, `package-capability-declaration.v1`,
   `package-capability-invoke.v1`, `package-capability-invoke-result.v1`,
   `package-capability-status.v1`, `package-capability-status-result.v1`,
   `package-capability-reconciliation-evidence.v1`, `package-capability-invocation.v1`,
   and `package-capability-tombstone.v1` with positive and negative fixtures, mirrored
   into `node:protocol/contracts`; update `capability-passport.v1`; and amend
   `middleware-component-contract.v1` with the optional `reconciliation/operation`.
4. Update solutions 037 and 048 as phases complete, and the Node implementation ledger
   when work starts.

## Implementation Recommendations

The recommendations follow the Node layering (DEV-GUIDELINES, Layering #2 and #5). The
grammar belongs to `orbiplex-node-capability`, which owns P072. Pure invocation types –
evidence, admission, the outcome table, the replay decision – belong in a new
`orbiplex-node-package-capability-core` (L0). The overlay projection is built by
`orbiplex-node-operator-extension-service`, which owns activations and the P085 journal.
The invocation journal and dispatcher live in the daemon, which owns authority,
sessions, and effects. The network layer depends only on the grammar.

The Rust below fixes shapes and invariants, not final names.

### R1. One grammar, one closed identifier type

```rust
/// Parsed capability identifier: the only grammar in the workspace.
///
/// Replaces `is_sovereign_capability` and the three other grammar copies.
/// Every consuming site matches exhaustively and must decide what a new
/// shape means.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum CapabilityId {
    Registered(RegisteredCapabilityId),
    Sovereign(SovereignCapabilityId),
    Package(PackageCapabilityId),
}

impl std::str::FromStr for CapabilityId {
    type Err = CapabilityIdError;
    fn from_str(raw: &str) -> Result<Self, Self::Err> { /* single parser */ }
}

/// Canonical form; `parse(display(x)) == x` is a property test.
impl std::fmt::Display for CapabilityId { /* … */ }
```

- The protocol validator and the registry shape check call this parser. A test
  generates identifiers and asserts that the passport schema pattern and the parser
  agree, so the schema cannot drift again.
- Newtypes (`CapabilityName`, `PackageName`, `DidKey`) are validated at construction
  (Data and Contracts #5, #8).

### R2. Identifier parts stay separate fields

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct PackageCapabilityId {
    name: CapabilityName,
    scope: PackageCapabilityScope,
    anchor: PackageAnchor,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct PackageAnchor {
    /// `did:key` of the admitted package-signing key.
    authority: DidKey,
    /// Must equal the name part of the package's `package_ref`.
    package: PackageName,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum PackageCapabilityScope {
    Package,
    Node,
    Peer,
}
```

The string composes scope and owner; the type keeps them apart (Avoid Entanglement #5).

### R3. Reach is a table that can only refuse

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CallerClass {
    SamePackage,
    LocalComponent,
    RemotePeer,
}

impl PackageCapabilityScope {
    /// Deny-only reach check. `true` admits nothing by itself.
    #[must_use]
    pub const fn reaches(self, caller: CallerClass) -> bool {
        match (self, caller) {
            (Self::Package | Self::Node | Self::Peer, CallerClass::SamePackage)
            | (Self::Node | Self::Peer, CallerClass::LocalComponent)
            | (Self::Peer, CallerClass::RemotePeer) => true,
            (Self::Package, CallerClass::LocalComponent | CallerClass::RemotePeer)
            | (Self::Node, CallerClass::RemotePeer) => false,
        }
    }
}
```

Exhaustive, without a catch-all (Rust-Specific #11). A test enumerates all nine cells.

### R4. Caller evidence is host-attested

```rust
/// Produced only by the daemon from its own session bindings.
pub enum CallerEvidence {
    SamePackage {
        component: ComponentRef,
        activation: ActivationRef,
    },
    LocalComponent {
        component: ComponentRef,
        activation: ActivationRef,
        edge: RequirementEdge,
    },
    RemotePeer {
        session_node: NodeId,
        passport: VerifiedPackagePassport,
    },
}

/// Operator-approved in the consumer's activation plan.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct RequirementEdge {
    pub consumer_activation: ActivationRef,
    pub capability: PackageCapabilityId,
    pub contract: ContractDigest,
}
```

Admission verifies every claim against current state: the component belongs to the
package and activation named, and the edge exists in that activation's approved plan.
The daemon never constructs evidence from request fields; a test sends a request whose
payload claims a different component and asserts refusal.

### R5. The overlay entry references the component contract

```rust
/// No eligibility flags: forbidden uses are unrepresentable.
#[derive(Debug, Clone)]
pub struct PackageCapabilityEntry {
    pub id: PackageCapabilityId,
    pub provider: ComponentRef,
    pub contract: ContractDigest,
    pub effects: Vec<EffectRef>,
    pub recovery: RecoveryClass,
    pub budget: InvocationBudget,
    pub replay_window: Duration,
    pub required_base: BTreeSet<RegisteredCapabilityId>,
    pub fence: ActivationFence,
}

/// Most restrictive class among the referenced effects; `ReadOnly` when none.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum RecoveryClass {
    ReadOnly,
    EphemeralRevertible,
    TransactionalWithheld,
    Compensatable,
    IrreversibleExternal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ActivationFence {
    pub package_ref: String,
    pub package_digest: String,
    pub generation: u64,
    pub operator_binding_ref: String,
}
```

`PackageCapabilityIndex::build` refuses the activation unless:

- the anchor key equals the verifying key and the anchor package name equals the
  `package_ref` name;
- the declared scope equals the identifier scope;
- the provider's component contract has `provides[]` with exactly this identifier and
  contract digest, and every referenced effect id exists in it;
- a `TransactionalWithheld` capability's provider declares `reconciliation/operation`;
- `required_base` is a subset of the base capabilities granted to this activation;
- the contract schemas compile under the bounded resolver (R11);
- no identifier repeats and none appears in the checked-in registry.

### R6. The overlay projects the journal behind a generation gate

```rust
/// Orders invocation admission points against lifecycle transitions.
pub struct GenerationGate {
    current: std::sync::RwLock<Arc<PackageCapabilityIndex>>,
    /// Set while a transition waits; new admissions wait behind it, so a
    /// transition cannot be starved by a stream of starts.
    transition_pending: std::sync::atomic::AtomicBool,
}

impl GenerationGate {
    /// Lifecycle side: the write guard spans the durable commit and the
    /// publication, so no start interleaves between them.
    pub fn transition<F>(&self, commit_and_rebuild: F) -> Result<(), LifecycleError>
    where
        F: FnOnce() -> Result<PackageCapabilityIndex, LifecycleError>;

    /// Invocation side: the read guard spans the generation recheck and the
    /// durable `started` append; it is released before dispatch.
    pub fn admit<F, T>(&self, expected: u64, append_started: F) -> Result<T, PackageCapabilityRefusal>
    where
        F: FnOnce(&PackageCapabilityIndex) -> Result<T, PackageCapabilityRefusal>;
}
```

Fairness of `std::sync::RwLock` is platform-dependent, so writer progress is explicit:
one lifecycle writer serializes transitions and owns `transition_pending` until its
write gate is released. Admissions check the flag again after acquiring the read gate;
if set, they release the gate and wait without holding it. Durable appends and waits
have deadlines; an append failure releases the reservation and never dispatches.
This bounds the transition's wait to the starts already appending. This adds no dependency.
At startup the index is rebuilt from the committed P085 journal before any admission.

### R7. The outcome state machine is a pure function

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InvocationState {
    Started,
    Completed { result: ResultRetention },
    Aborted,
    Compensated,
    Unknown { cause: UnknownCause },
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InvocationEvent {
    ProviderReturned,
    OutputContractViolated,
    NoOutcome,
    /// The host has confirmation for every declared ephemeral disposer.
    DisposalConfirmed,
    Reconciled(BoundEvidence),
    OperatorResolved(Resolution),
}

/// The tables in §9, exhaustively. A disallowed transition is a typed error
/// (DEV-GUIDELINES Review #10).
pub fn next_state(
    from: &InvocationState,
    event: &InvocationEvent,
    recovery: RecoveryClass,
) -> Result<InvocationState, InvalidInvocationTransition>;
```

Recovery at startup uses the recovery context frozen in each `started` record, never
`entry.recovery` from the current overlay. An ephemeral abort is recorded only after
its disposer confirms cleanup; failed or uncertain disposal leaves `unknown`. Startup
classification never redispatches the original operation; later bounded disposal and
reconciliation use only their declared recovery operations.

### R7a. Reconciliation evidence is bound before it is read

```rust
/// What the provider's `reconciliation/operation` returned. Untrusted until bound.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReconciliationEvidence {
    pub invocation: InvocationKey,
    pub request_digest: RequestDigest,
    pub capability: PackageCapabilityId,
    pub contract: ContractDigest,
    pub generation: u64,
    pub effect_refs: Vec<EffectRef>,
    pub state: EvidenceState,
    pub observed_at: OffsetDateTime,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EvidenceState {
    Committed,
    /// No covered effect became visible; future execution is permanently fenced.
    Abandoned,
    Pending,
    NotFound,
}

/// Evidence whose every binding field equals the journal's `started` record.
/// Only `bind` constructs it, so an unbound answer cannot reach `next_state`.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BoundEvidence(EvidenceState);

pub fn bind(
    record: &StartedRecord,
    provider: &AuthenticatedRecoveryProvider,
    evidence: ReconciliationEvidence,
) -> Result<BoundEvidence, EvidenceMismatch>;
```

`next_state` maps `BoundEvidence` through the resolution table of §9. `Pending` and
`NotFound` leave `unknown`; `Abandoned` leaves `unknown` for
`IrreversibleExternal`. `bind` checks the provider's authenticated binding and exact
effect coverage as well as the invocation fields. A transport failure or timeout of the
reconciliation call never produces evidence at all. The worker that calls
`reconciliation/operation` is a separate
host task with its own budget, backoff, and attempt bound; its escalation enters the
operator resolution queue.

### R8. The replay decision is a pure function

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ReplayDecision {
    Admit,
    Answer(RecordedOutcome),
    Conflict,
    Stale,
    CapacityExhausted,
}

pub fn replay_decision(
    record: Option<&InvocationRecord>,
    request_digest: &RequestDigest,
    issued_at: OffsetDateTime,
    now: OffsetDateTime,
    window: Duration,
    skew: Duration,
    admission_not_before: Option<OffsetDateTime>,
    capacity: JournalCapacity,
) -> ReplayDecision;
```

`Answer` covers `started`, `completed` (retained or `result/status: unavailable`),
`aborted`, `compensated`, and `unknown`. For an absent key, a timestamp at or below
`admission_not_before` yields `Stale`. `CapacityExhausted` is returned only for a new
key when every retained record is still protected or unresolved. The decision from a
snapshot is provisional: step 9 rechecks the key and fingerprint in the journal's
unique-key transaction, including the current admission floor, before creating a start.
Execution-budget exhaustion never blocks a read of an already recorded outcome;
ordinary bounded read admission still applies.

```rust
/// Retention promises, fixed at admission. Configuration changes never
/// rewrite them.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RecordRetention {
    pub protected_until: OffsetDateTime,
    /// Set on any terminal resolution; `None` while unresolved.
    pub result_until: Option<OffsetDateTime>,
}

/// A record may be evicted only when it is resolved, past `protected_until`,
/// and past its post-resolution window. Results are dropped independently,
/// earliest first under budget pressure.
pub const fn evictable(state: &InvocationState, retention: RecordRetention, now: OffsetDateTime) -> bool;
```

### R8a. A status query is a pure read of one record

```rust
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StatusView {
    Recorded { state: InvocationState, output_digest: Option<OutputDigest> },
    /// No record under the caller's key. Not proof that nothing ran.
    NotFound,
}

pub fn status_view(
    record: Option<&InvocationRecord>,
    request_digest: &RequestDigest,
) -> Result<StatusView, PackageCapabilityRefusal>;
```

The daemon calls it after the same reach, overlay, contract, caller-evidence, and grant
checks as an invocation (§11, steps 2–5), but it skips the admission window, the replay
decision, input validation, readiness, and the admission point. It holds no gate, takes
no budget reservation beyond a read, and has no path to a provider or to the
reconciliation worker.

### R9. Admission is pure over a snapshot

```rust
pub fn admit_package_invocation(
    index: &PackageCapabilityIndex,
    request: &InvocationRequest,
    evidence: &CallerEvidence,
    replay: ReplayDecision,
    now: OffsetDateTime,
) -> Result<AdmittedInvocation, PackageCapabilityRefusal>;
```

It performs steps 2 through 7 of §11 without I/O. Readiness, budget reservation, and the
`started` append (steps 8 and 9) are the daemon's, inside `GenerationGate::admit`.

### R10. Refusal is a closed vocabulary with its own remote projection

```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PackageCapabilityRefusal {
    StaleRequest,
    OutOfScope,
    UnknownCapability,
    ScopeCommitmentMismatch,
    ContractMismatch,
    CallerEvidenceInvalid,
    GrantMissing,
    GrantInvalid,
    GrantRevokedOrExpired,
    GrantHolderMismatch,
    GrantBindingStale,
    GrantVoidedByTombstone,
    InvocationIdConflict,
    InvalidInput,
    ActivationStale,
    ProviderUnavailable,
    CapacityExhausted,
    DeadlineExceeded,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RemoteRefusal {
    StaleRequest,
    Unavailable,
    Busy,
    DeadlineExceeded,
    InvocationIdConflict,
    InvalidInput,
}

impl PackageCapabilityRefusal {
    /// What a peer may learn. Everything that precedes successful caller
    /// verification collapses to `Unavailable`.
    #[must_use]
    pub const fn remote_projection(self) -> RemoteRefusal {
        match self {
            Self::StaleRequest => RemoteRefusal::StaleRequest,
            Self::OutOfScope
            | Self::UnknownCapability
            | Self::ScopeCommitmentMismatch
            | Self::ContractMismatch
            | Self::CallerEvidenceInvalid
            | Self::GrantMissing
            | Self::GrantInvalid
            | Self::GrantRevokedOrExpired
            | Self::GrantHolderMismatch
            | Self::GrantBindingStale
            | Self::GrantVoidedByTombstone
            | Self::ActivationStale
            | Self::ProviderUnavailable => RemoteRefusal::Unavailable,
            Self::InvocationIdConflict => RemoteRefusal::InvocationIdConflict,
            Self::InvalidInput => RemoteRefusal::InvalidInput,
            Self::CapacityExhausted => RemoteRefusal::Busy,
            Self::DeadlineExceeded => RemoteRefusal::DeadlineExceeded,
        }
    }

    #[must_use]
    pub const fn retryable(self) -> bool {
        matches!(
            self,
            Self::ProviderUnavailable | Self::CapacityExhausted | Self::DeadlineExceeded
        )
    }
}
```

`ProviderUnavailable` follows caller verification, but it still projects to
`Unavailable`: the holder learns only to retry later, which `retryable` expresses
locally. Every refusal is pre-admission; post-admission states are outcomes (R7).

### R11. Contract document, digest, and bounded resolution

```rust
pub fn contract_digest(document: &PackageCapabilityContract) -> ContractDigest {
    // sha256 over JCS-v1 bytes, rendered as sha256:<base64url-no-pad>
}

pub struct SchemaResolutionLimits {
    pub schema_bytes_max: u32,
    pub ref_depth_max: u8,
    pub schema_count_max: u16,
}

/// Resolves only same-document refs, package members listed in the contract
/// `refs` map, and Node canonical schema ids. Any other `$ref` refuses.
pub fn compile_contract(
    document: &PackageCapabilityContract,
    package: &VerifiedPackageMembers,
    canonical: &SchemaGate,
    limits: SchemaResolutionLimits,
) -> Result<CompiledContract, ContractCompileError>;
```

### R12. The passport validator gains a package branch

```rust
match self.capability_id.parse::<CapabilityId>()? {
    CapabilityId::Registered(id) => {
        capability_admission_for_use(id.as_str(), CapabilityRegistryUse::Passport)?;
    }
    CapabilityId::Sovereign(id) => validate_sovereign_passport(self, &id)?,
    CapabilityId::Package(id) => validate_package_passport_shape(self, &id)?,
}
```

`validate_package_passport_shape` requires `peer-pkg`, `expires_at`,
`scope["contract/digest"]`, a holder distinct from the issuer node, and no
`issuer_delegation`. The per-request currency checks of §8 live in P093 admission. The
signature-verification cache is keyed by passport digest, holds only the verification
result, and is bounded by count.

### R13. Data shapes

Contract, carried inside the package:

```json
{
  "schema": "package-capability-contract.v1",
  "schema/v": 1,
  "schema/dialect": "https://json-schema.org/draft/2020-12/schema",
  "input/schema": {"path": "schemas/review-request.json", "digest": "sha256:…"},
  "output/schema": {"path": "schemas/review-result.json", "digest": "sha256:…"},
  "refs": {"schemas/common.json": "sha256:…"}
}
```

Declaration, carried inside the package:

```json
{
  "schema": "package-capability-declaration.v1",
  "schema/v": 1,
  "capability/id": "review@peer-pkg:did:key:z6MkAuthority/acme-review",
  "capability/scope": "peer",
  "provider/component": "acme-review-service",
  "contract/digest": "sha256:…",
  "effect/refs": ["review-record-write"],
  "budget": {
    "timeout-ms": 30000,
    "request/bytes-max": 65536,
    "response/bytes-max": 262144,
    "concurrency-max": 4
  },
  "replay/window-ms": 3600000,
  "requires/capabilities": ["inquirium.generate"]
}
```

Invocation request:

```json
{
  "schema": "package-capability-invoke.v1",
  "schema/v": 1,
  "capability/id": "review@peer-pkg:did:key:z6MkAuthority/acme-review",
  "contract/digest": "sha256:…",
  "invocation/id": "package-invocation:01K…",
  "issued-at": "2026-09-25T12:00:00Z",
  "deadline": "2026-09-25T12:00:30Z",
  "passport": {},
  "input": {}
}
```

Invocation result:

```json
{
  "schema": "package-capability-invoke-result.v1",
  "schema/v": 1,
  "invocation/id": "package-invocation:01K…",
  "outcome": "completed",
  "result/status": "retained",
  "output": {},
  "output/digest": "sha256:…"
}
```

`outcome` is one of `refused`, `started`, `completed`, `aborted`, `compensated`, `unknown`.
`refused` requires `refusal/code` and forbids output fields. `completed` requires
`result/status`; `retained` requires `output` and `output/digest`, and `unavailable`
forbids `output` and carries `output/digest` only when a previously validated output
digest is known. A completion established solely from commit evidence may have neither
output nor its digest; a known digest is not discarded when the output expires. The
other outcomes forbid output fields. `started` is a read of an existing in-flight
invocation, never permission to dispatch it again.
Each exclusion has a negative fixture (DEV-GUIDELINES Review #9).

Invocation fact:

```json
{
  "schema": "package-capability-invocation.v1",
  "schema/v": 1,
  "caller": {"kind": "node", "ref": "node:did:key:z6MkCaller"},
  "invocation/id": "package-invocation:01K…",
  "request/digest": "sha256:…",
  "capability/id": "review@peer-pkg:…",
  "activation/generation": 7,
  "issued-at": "2026-09-25T12:00:00Z",
  "deadline": "2026-09-25T12:00:30Z",
  "protected-until": "2026-09-25T13:01:00Z",
  "result/retention-ms": 900000,
  "recovery/context": {
    "package/ref": "extension-package:acme-review",
    "package/digest": "sha256:…",
    "provider/component": "acme-review-service",
    "contract/digest": "sha256:…",
    "effect/refs": ["review-record-write"],
    "recovery/class": "transactional-withheld"
  },
  "event": "started",
  "recorded-at": "2026-09-25T12:00:01Z"
}
```

The recovery context pins immutable package and effect declarations retained as in §9.
Outcome facts identify the same invocation and append the new `event`, plus
`output/digest`, `resolution/ref`, or `cause` when known or required by that state;
they do not change the start's frozen context or retention promises.

Tombstone, written in the revoke transaction:

```json
{
  "schema": "package-capability-tombstone.v1",
  "schema/v": 1,
  "capability/id": "review@peer-pkg:…",
  "retired-at": "2026-09-26T08:00:00Z",
  "reason": "package-revoked",
  "revocation/ref": "operator-extension-revocation:01K…",
  "grants/void-before": "2026-09-26T08:00:00Z"
}
```

Status request and result:

```json
{
  "schema": "package-capability-status.v1",
  "schema/v": 1,
  "capability/id": "review@peer-pkg:did:key:z6MkAuthority/acme-review",
  "contract/digest": "sha256:…",
  "invocation/id": "package-invocation:01K…",
  "request/digest": "sha256:…",
  "passport": {}
}
```

```json
{
  "schema": "package-capability-status-result.v1",
  "schema/v": 1,
  "invocation/id": "package-invocation:01K…",
  "status": "completed",
  "result/status": "retained",
  "output": {},
  "output/digest": "sha256:…"
}
```

`status` is one of `started`, `completed`, `aborted`, `compensated`, `unknown`,
`not-found`, or `refused` with a `refusal/code` from the remote projection. The status
result follows the same output-field rules as the invocation result; `not-found`
forbids all output fields and makes no claim that execution never occurred. The status
request schema forbids `input`, so a status request cannot be mistaken for an
invocation.

Reconciliation evidence, returned by a provider's `reconciliation/operation`:

```json
{
  "schema": "package-capability-reconciliation-evidence.v1",
  "schema/v": 1,
  "invocation/id": "package-invocation:01K…",
  "caller": {"kind": "node", "ref": "node:did:key:z6MkCaller"},
  "request/digest": "sha256:…",
  "capability/id": "review@peer-pkg:…",
  "contract/digest": "sha256:…",
  "activation/generation": 7,
  "effect/refs": ["review-record-write"],
  "state": "committed",
  "observed-at": "2026-09-25T12:05:00Z"
}
```

Amended effect declaration in `middleware-component-contract.v1`:

```json
{
  "class": "transactional-withheld",
  "scope": "durable",
  "journal/ref": "acme-review:reviews",
  "reconciliation/operation": "acme-review.invocation-status"
}
```

`reconciliation/operation` is permitted for `transactional-withheld`, `compensatable`,
and `irreversible-external` effects and forbidden for `ephemeral-revertible`, with a
negative fixture for each forbidden combination.

### R14. Bounded stores

| store | owner | key | bound and cleanup |
| :--- | :--- | :--- | :--- |
| invocation journal (also idempotency) | daemon | `(caller, invocation/id)` | kept at least until the `protected-until` fixed at admission; `started` and unresolved `unknown` kept until resolved, then for the result retention period; retained recovery context follows the record; count and byte caps never evict such a record, and new work refuses as `busy` |
| admission floors | daemon, same journal | `capability/id` | monotonic, persisted atomically with cleanup; retained across restart and reactivation; count-bounded, with capacity refusal for new capabilities rather than eviction of a safety fence |
| retained results | daemon | same key | start profile: 15 min from completion, never beyond the record, 256 KiB per result, 64 MiB per node; dropped earliest first under pressure, then `result/status: unavailable` |
| reconciliation schedule | daemon | same key | only for `unknown` records; bounded attempts with backoff; removed on resolution or escalation |
| signature-verification cache | daemon | passport digest | count-bounded; holds only the verification result; flushed on trust-root change |
| schema cache on callers | daemon | schema digest | count- and byte-bounded; content-addressed, so never stale |
| tombstones | operator-extension service | `capability/id` | retained while any passport issued before the watermark can be unexpired |

### R15. Tests start from refusal, replay, and interruption

Following Review #14, every phase lands its refusal and replay cases before the happy
path counts as done. Beyond the cases listed per phase, interruption tests kill the
provider process between the `started` append and dispatch, between dispatch and the
outcome record, and between the outcome record and the response. After restart they
assert, for each recovery class, the outcome of §9, that nothing was dispatched twice,
and that a replay of the original request returns that outcome.

Further cases pin the reconciliation and status contracts: evidence with each binding
field altered stays `unknown`; `not-found` and `pending` never resolve; `abandoned`
never resolves `irreversible-external`; committed evidence without a validated output
yields `result/status: unavailable`; no evidence triggers compensation; a status query
never reaches the provider or the reconciliation worker, including for `unknown`
records; a status query after the admission window still answers while the record and
grant exist; `not-found` is returned without any claim about execution; shrinking the
replay window in configuration leaves existing `protected-until` values unchanged; and
result-budget pressure drops outputs while every protected and unresolved record
survives.

Also race identical and conflicting requests for the same key and prove exactly one
start and dispatch; replay `started` and `compensated`; isolate local component keys;
upgrade or remove the provider before restart and recover from the original context;
refuse partial-effect or unauthenticated reconciliation evidence; complete from commit
evidence without inventing an output digest; fail disposal without recording `aborted`;
and increase the replay window or roll back the clock after cleanup without readmitting
a purged request. Race terminal resolutions and prove they cannot overwrite each other.

## Implementation Tracker

Status legend: `[ ]` not started · `[~]` in progress · `[x]` done (with code evidence)
· `[d]` deliberately deferred out of this proposal's implementation scope.

Identifiers are stable; dependencies name the identifiers that must be done first.

### Phase 0 — Identifier foundation

Independent of the rest; it fixes existing defects.

- [ ] `P093-001` Single closed `CapabilityId` parser with the strict-intersection
  charset, canonical `Display`, and a round-trip property test. Depends on: –.
- [ ] `P093-002` Migrate the nine `is_sovereign_capability` callers to exhaustive
  matching; remove the heuristic. Depends on: `P093-001`.
- [ ] `P093-003` Route the protocol validator and the registry shape check through the
  parser; add a generated test that the passport schema pattern agrees with it.
  Advertisements keep refusing package identifiers. Depends on: `P093-001`.
- [ ] `P093-004` Base admission refuses package identifiers with a typed error; guard
  that the checked-in registry contains none. Depends on: `P093-001`.

### Phase 1 — Contract and declaration schemas

- [ ] `P093-010` `package-capability-contract.v1`, the frozen digest definition, and the
  bounded schema resolver with refusal tests for remote, filesystem, over-deep, and
  over-large references. Depends on: `P093-001`.
- [ ] `P093-011` `package-capability-declaration.v1` referencing the provider's
  `provides[]` entry and effect ids; positive and negative fixtures; Node mirror.
  Depends on: `P093-010`.
- [ ] `P093-012` Update `capability-passport.v1` to admit `peer-pkg` identifiers only,
  with negative fixtures for `pkg` and `node-pkg`; Node mirror. Depends on: `P093-003`.
- [ ] `P093-013` Amend `middleware-component-contract.v1` with the optional
  `reconciliation/operation` and its per-class rules; add
  `package-capability-reconciliation-evidence.v1`; negative fixtures for forbidden
  combinations; Node mirror. Depends on: `P093-011`.

### Phase 2 — Activation overlay (Solution 048)

- [ ] `P093-020` Declarations in `operator-experiment-package.v1`; activation enforces
  every R5 invariant. Depends on: `P093-011`, `P093-013`.
- [ ] `P093-021` Overlay as a projection of the P085 journal behind `GenerationGate`;
  startup rebuild before admission. Depends on: `P093-020`.
- [ ] `P093-022` Revoke writes tombstones in the same transaction. Depends on:
  `P093-021`.
- [ ] `P093-023` Requirement edges approved in consumer activation plans. Depends on:
  `P093-020`.
- [ ] `P093-024` Activation plan and inspection show package capabilities, their scope,
  required base capabilities, and recovery class. Depends on: `P093-020`.
- [ ] `P093-025` Lifecycle table of §10, one test per row, including crash between
  commit and publication. Depends on: `P093-022`.

### Phase 3 — Local invocation with journal and recovery

- [ ] `P093-030` Host-attested caller evidence for same-package and local-component
  calls; payload-claim refusal test. Depends on: `P093-021`, `P093-023`.
- [ ] `P093-031` Invocation journal with the admission point under the generation read
  gate, atomic unique-key admission, and immutable recovery context; define
  `package-capability-invocation.v1` and its Node mirror. Depends on: `P093-021`.
- [ ] `P093-032` Idempotency contract of §12: fingerprint, window, `stale-request`,
  `invocation-id-conflict`, `protected-until` fixed at admission, unresolved-record
  retention, protected-record capacity, and result retention with early eviction under
  the node budget; durable admission floors prevent resurrection after window growth
  or clock rollback. Depends on: `P093-031`.
- [ ] `P093-033` Outcome state machine and startup recovery from the recorded context,
  with no original-operation redispatch; confirmed disposal before ephemeral abort and
  conditional terminal transitions. Depends on: `P093-031`.
- [ ] `P093-034` Provider readiness and contract compatibility in the P080 graph before
  the admission point; provider loss as a dependency transition. Depends on: `P093-030`.
- [ ] `P093-035` Input validation before the admission point; output validation before
  release, with `output-contract-violation`. Depends on: `P093-010`, `P093-031`.
- [ ] `P093-036` Interruption tests of R15 for every recovery class, including a crash
  during reconciliation, concurrent retries, and recovery across upgrades. Depends on:
  `P093-032`, `P093-033`, `P093-035`, `P093-037`.
- [ ] `P093-037` Evidence-bound reconciliation worker: authenticated provider and exact
  effect-coverage binding checks, resolution table,
  backoff, attempt bound, escalation to the operator resolution queue; never compensates
  and never releases unvalidated output. Depends on: `P093-013`, `P093-033`.
- [ ] `P093-038` Local status query over the host journal with invocation-equivalent
  authorization and no provider or reconciliation path. Depends on: `P093-030`,
  `P093-032`.
- [ ] `P093-039` Measure retry-delay distribution, result-size distribution, and
  journal growth at the target invocation rate; calibrate the start profile and record
  the evidence. Depends on: `P093-032`.

### Phase 4 — Peer grants

- [ ] `P093-040` Package branch of passport shape validation and the per-request
  currency checks of §8; signature-verification cache. Depends on: `P093-012`,
  `P093-031`.
- [ ] `P093-041` Issuance by the current operator only. Depends on: `P093-040`.
- [ ] `P093-042` Grant termination by passport revocation, binding revocation or
  supersession, and tombstone watermark. Depends on: `P093-022`, `P093-040`.

### Phase 5 — Peer invocation

- [ ] `P093-050` `package-capability.invoke.*` family and schemas with outcome
  exclusion fixtures. Depends on: `P093-011`.
- [ ] `P093-051` Deny-only reach filter at the network boundary. Depends on:
  `P093-002`.
- [ ] `P093-052` Admission order of §11 with uniform pre-verification refusals.
  Depends on: `P093-040`, `P093-050`, `P093-032`.
- [ ] `P093-053` Caller-side contract and schema retrieval through
  `capability.schema.present`, and output validation before release. Depends on:
  `P093-010`, `P093-050`.
- [ ] `P093-054` Multi-daemon test: grant, invoke, lost response observed through a
  status query, revocation before and after the admission point, evidence-bound and
  operator `unknown` resolution, restart. Depends on: `P093-052`, `P093-055`,
  `P093-036`.
- [ ] `P093-055` `package-capability.status.*` family and schemas; a status request
  requires `contract/digest` and refuses `input`; status after the admission window;
  unknown output digest is not fabricated for an evidence-only completion.
  Depends on: `P093-038`, `P093-050`.

### Phase 6 — Module report tightening

- [ ] `P093-060` Validate `Other`-class offered capabilities as registered base
  identifiers or package identifiers in the reporting package's own namespace; reject
  all others at report admission. Depends on: `P093-002`, `P093-021`.

### Phase 7 — Deferred

- [d] `P093-070` Advertisement or Seed Directory publication of package capabilities.
- [d] `P093-071` Author-identity anchors resilient to key rotation.
- [d] `P093-072` Delegated grant issuers.
- [d] `P093-073` Public namespace governance, which remains with P072 Phase 5.
