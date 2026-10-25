# P026-012b-r1: private commitment and activation corrections

Status: accepted correction design; implementation and qualification pending.
Basis: P026-012b review F-01 through F-12; P066 ownership; P073 lifecycle.

## Frozen corrections

New emissions use supplied-input-manifest v3, outcome v4, private product/read
successors, intent v2 and controller execution provenance v2. Historical versions
keep their readers and meanings; historical evidence is unchanged. Private
commitments are domain-separated HMAC-SHA256 with exactly 64 lowercase hex digits
under `hmac-sha256:`. No second hash is applied. Private result handles use that
algorithm label too. The public fixed template uses ordinary SHA-256. The v3
manifest still has its independently verifiable unkeyed canonical manifest hash.

Intent v2 declares `cost/mode: unmetered`. Its compute budget has no monetary
zero field. Lowering to the existing P073 budget uses its internal zero sentinel;
this grants no financial cap, free execution or no-egress guarantee. Local HTTP
can proxy a paid provider. Consent must state this explicitly.

List is a read-only P066 projection: approved is distinct from active and no
inspection consumes or activates consent. Only a current authenticated holder
may activate at first use, after holder admission. Proposals and activations
reserve under a short owner lock, perform P066 I/O outside it and revalidate before
publication. Policy validation under the Agent registry uses only current RAM
witnesses. A concurrent in-progress reservation refuses with an explicit conflict;
retry after publication returns the same frozen proposal/activation.

After final admission, the exact manifest is retained after the transport returns,
including timeout/error/non-completed/invalid-response paths. It records an
admitted possible disclosure, not proof that a provider received bytes. There is
no outcome on failure. A storage failure refuses and cannot promise a durable
receipt; a crash between transport and this write remains outside qualification.
No owner I/O enters the final admission/send interval. Output contracts are denied
explicitly in this single-inference profile; a second dispatch has a distinct
conflict. Abort is only for a claim that has not committed.

Dependencies deserialize strictly. Product/receipt dependencies come from the
sealed manifest and reads return the retained outcome's set. The owner reserves
the `agent:assessment:` namespace for closed materialization, including an
interrupted spawn-before-bind. Request-body detection is extra defence.

## Clarifications

Within this profile an approval ref and activation are one-to-one: 012a's frozen
descriptor includes its unique activation, boot and launch; 012b's unique Agent/
binding descriptor is consumed once. Replay does not create another activation,
and archive recovery cannot activate it. Dependency refs name these approvals,
with the exact descriptors and witnesses required; the strings grant nothing.

Committed private products belong to the binding and launch. A new current
session of the same launch may read them after fresh admission. A passage losing
its session before commit cannot commit through reconnect. This is fresh product
issuance, not revival of a stale passage or its context.

The shared assessment observation renderer intentionally uses User/Postamble
HostObservation on the generic Q-02 path too. Its retained evidence stays valid
for its pinned source; a new run can have a different prompt. Lifecycle commands
retain P073's local-control/record-owner authority; in this implementation the
closed Agent is created by local-control. They convey no assessment authority.

The metadata history remains an explicit P073 projection/retention limitation;
this revision adds a direct product index, not a new retention service or implicit
history eviction. The 32 active-grant/8-attempt bounds do not constitute a bound
on all historical metadata. Retention work precedes widening 012c.

## Acceptance

Use one ordinary daemon, real Agora, actual ChannelJson caller, browser/P066 and
the local deterministic adapter, with no acceptance feature or models. Repeat
the closed matrix on the new wire. Additionally prove repeated approved listing
leaves consumption absent, first holder use consumes once, and a post-admission
adapter error leaves a durable manifest without an outcome, including restart.
Keep native failure/lock/clock/fence/legacy-reader proofs separate. Qualify normal
and optimized, loose and safely extracted; retain failed attempts. Only measured
results may update the tracker and ledger. No merge or push.
