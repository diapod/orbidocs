# Contact Catalog

`Contact Catalog` is a node-attached domain catalog for opt-in private contact
discovery. It lets a user publish a route candidate for an external contact
handle, such as an email address or phone number, without turning Seed Directory
into a people directory and without publishing raw `phone/email -> participant`
maps.

Status: `hard-MVP done` (the broader solution remains `partial` for
post-MVP privacy/federation expansion)

Date: `2026-05-16`

Hard-MVP tracker status: `100% implemented`. All `Must Implement`
capabilities in the Solution 025 sidecar belong to that historical baseline.
P058-022–028 below are planned extensions and corrective gates. The hard-MVP
evidence predates them.

## Executive Summary

Contact Catalog answers one narrow question:

```text
Given a contact handle I already know, is there a safe Orbiplex route candidate
for requesting contact with the handle controller?
```

The MVP profile is intentionally conservative:

```text
remote caller
  -> rate-limited invitation-only digest lookup
  -> route candidate
  -> contact-request.v1 over Artifact Delivery / INAC
  -> recipient-local consent
  -> capability-passport.v1 for messaging-receive
```

The catalog owns contact-domain admission and lookup policy. Seed Directory only
discovers Contact Catalog providers through the `contact-catalog` capability.
The Node daemon does not learn phone or email semantics; it supervises the
middleware, exposes host capabilities, and transports artifacts through existing
planes.

The solution-level Seed Directory boundary is defined separately in
`doc/project/60-solutions/031-seed-directory/031-seed-directory.md`.

## Context and Problem Statement

Proposal 058 defines Contact Catalog as a domain catalog separate from Seed
Directory. Story 010 uses it to let Daniel message Marcin by an email address
Daniel already knows.

The implementation must preserve three boundaries:

- local address-book data stays local and may contain raw handles;
- Contact Catalog records contain opt-in claims, lookup indexes, route
  candidates, expiry, revocation, and admission evidence;
- Seed Directory advertises providers and capability evidence, not people.

## Must Implement

### Contact Claim Admission

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`

Related schemas:

- `contact-claim.v1`
- `capability-passport.v1`

Responsibilities:

- accept `contact-claim.v1` only after validating contact-control evidence;
- require `email-control` or `phone-control` passport freshness for email and
  phone handles;
- reject raw handle publication in catalog records under the MVP profile;
- enforce purpose allowlists, expiry, revocation reference shape, and monotonic
  `sequence/no`;
- store admitted claims through `CatalogStore<ContactClaimRecord>` rather than a
  bespoke storage layer.

Status:

- `done` — Node `contact-catalog-core` validates canonical route-set
  `contact-claim.v1`, verifies
  participant/delegated participant signatures, rejects node-only signatures,
  evaluates `email-control@v1` / `phone-control@v1` passports, and checks
  passport signature, expiry, profile match, and revocation freshness before
  admission. It also owns shared lookup request/result DTOs and the normalized
  lookup-index helper used by consumer-side code. Normalized lookup indexes are
  versioned and domain-separated by contact kind before hashing, so
  `email`, `phone`, and future handle kinds do not share a raw digest namespace.

### Invitation-Only Lookup

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `contact-lookup-result.v1`
- `routing-subject-binding.v1`

Responsibilities:

- expose `/v1/contact-catalog/lookup` or an equivalent supervised middleware
  endpoint under `catalog_kind = "contact"`;
- apply rate limits before lookup execution. The baseline public invitation-only
  surface takes digest queries. Local administration and provider sync require
  authentication. Protected lookup additionally authenticates the Catalog
  before transmitting a lookup credential;
- return `contact-lookup-result.v1` as a route-set candidate or
  invitation-required result;
- never return raw `participant:did:key` by default;
- use opaque `contact-route:<digest>` invitation refs when the local
  contactability draft is participant-routed;
- emit no-match audit entries without storing or exposing raw queried handles.
- support host-composed Artifact Delivery `selector/kind = "contact-lookup"`
  without making Contact Catalog an AD payload resolver. In that integration,
  AD passes `selector/purpose = "contact-request/messaging"` to express that
  lookup is being used for a messaging contact request, not for full message
  delivery.

Status:

- `done` — Node `contact-catalog-service` exposes public invitation-only,
  blinded-digest and PSI-mode `POST /v1/contact-catalog/lookups`, returns
  `contact-lookup-result.v1` with `result/routes[]`, optional `route/id`
  mirrors, `routing-subject` / `contact-nym` / `invitation-route` / `node`
  route candidates, and `selected/route`, rate limits by client fingerprint +
  digest + purpose, rejects raw handle-like lookup inputs, writes redacted
  lookup audit without raw query values or root participant ids, and exposes
  redacted counters/recent policy events in service status. Node
  `contact-catalog-client` is the provider-free consumer adapter:
  it performs bounded HTTP lookups and parses canonical `contact-lookup-result.v1`
  without owning provider admission, provider sync, or storage. The daemon uses
  that client for AD `contact-lookup` and exposes the same consumer path as
  host capability `contact.lookup`, so a node may consume Contact Catalog
  providers even when it does not run `contact-catalog-service`. The daemon owns
  an opt-in supervised runtime on stable loopback and a
  `/v1/contact-catalog/status` proxy; a process smoke starts the real service
  binary and verifies readiness plus projection status through that proxy.

### Federation alias registration and lookup (planned) {#federation-alias-registration}

[P058-024](../../40-proposals/058-contact-catalog.md#federation-contact-alias)
extends Contact Claim Admission with an `alias` handle kind. The current
admission path accepts email and phone control proofs and rejects `other`.
Add the typed alias to the claim schema, admission verifier, normalized-index
helper and lookup client together. Use domain separation for alias indexes
over the federation ID and normalized alias. Keep the email and phone index
domains and their existing attestation profiles intact.

Use P058's versioned match key for the lookup index. Use its confusable
reservation key only for atomic registration. Keep generation high-water, release deadline and
conflict holds through restart and compaction. Serialize competing mutations at
the **allocation writer**. The **alias holder** signs route and release intents.
Check private membership, assurance, quota and lease at admission. Commit the
name, reservation key, quota and receipt together. An expired route stops discovery
while the allocation follows its
[P058 lease and membership lifecycle](../../40-proposals/058-contact-catalog.md#federation-contact-alias).
Reuse the S025 contact-control passport verifier privately for initial
eligibility. Verify issuer trust, profile, holder, validity and revocation
without admitting a public email or phone claim. On renewal or recovery
verify current membership and alias-key control for the same generation.
Use the signed expected lease revision in P058. Compare and advance it in
the same transaction as the new nominal expiry and idempotent receipt.
Verify normal rotation with the incumbent key's authorization and the new
key's proof of possession over one statement bound to the allocation,
generation, predecessor and replacement. A backup recovers the incumbent
key under S026. The writer has no administrative key-reset transition.

Send a signed reservation directly over a confidential channel authenticated
to the currently mandated writer, or seal the whole request to its verified,
purpose-bound encryption key before forwarding through another Catalog. If
encryption-key binding cannot be established, offer only a verified direct
channel. A signing-key advertisement alone cannot authorize encryption. Bind federation,
writer, policy revision, request ID, expiry, chosen alias control key and
intended operation. Authenticate the response to the claimant. An intermediary
may observe traffic timing but cannot read or alter the proposed name/route.
A delayed duplicate returns the same decision without allocating twice.

The writer necessarily learns the link between participant and alias. Restrict
that map and admission evidence to the writer's private store during the allocation, including
owner-only recovery and membership review, followed by a bounded, published
dispute period. Scope any active dispute retention and
erase the link when its purpose ends, including from recoverable backup copies
under a bounded expiry policy. Compromise within that window can reveal it.
Read replicas, witnesses and the public lookup proof receive no base identity,
membership attestations, sibling aliases or reusable participant key.

#### Discovering the writer and verifying a receipt (planned) {#alias-allocation-authority}

1. **Discover the endpoint through Seed Directory.** Reuse [P025 capability
   registration](../../40-proposals/025-seed-directory-as-capability-catalog.md)
   for a dedicated federated capability (proposed ID
   `contact-alias-allocation`) on the existing Contact Catalog service. The
   writer advertises this role using the existing signed advertisement and
   `capability-passport.v1`. Seed Directory joins the registration to the
   node's current endpoints. Ordinary `contact-catalog` registrations continue
   to serve lookup. The federation root retains its existing Seed Directory
   bootstrap entries. Moving the writer's endpoint requires no root edit.
   Register the formal ID and its discovery wire name in the Node capability
   registry before enabling public advertisement.
2. **Verify the mandate for this role.** Reuse the [S041 official-service
   endorsement](../041-federation-root/041-federation-root.md). The client
   verifies a current `federation-service-endorsement.v1` for the exact
   federation, node and allocation capability, including expiry and revocation.
   The endorsement signs `capability_id`. An endorsement for
   `contact-catalog` cannot promote an ordinary directory to writer, even if
   its advertisement says `authoritative: true`. A UI may display that flag
   as a derived result once the mandate and the policy below both verify.
3. **Verify the allocation under the active federation policy.** The active
   federation configuration must select an authenticated, versioned allocation
   policy. The initial policy identifies one designated writer by stable
   identity and defines the proof it accepts from that writer. Bind the
   receipt to the policy revision and verify the allocation fields above.
   Clients apply the selected proof rule without hard-coding a signature
   count or a server key. One observed provider, agreement among discovery
   responses, or an informational `policy_ref` on an endorsement cannot
   select the writer. Freeze the policy binding and receipt vectors under
   P058-024 before enabling writes. Quorum and unanimous approval are later
   policy choices. [P058 owns the allocation decision and tracker](../../40-proposals/058-contact-catalog.md#federation-contact-alias).

**Portable binding and fork handling (P058-024, planned).** Freeze these
signed inputs, canonical digests, freshness windows and size bounds before
Schema Gate. Reuse portable verification, signed conflict evidence and the
federation review procedure. Contact records remain private to their owners.
[P035](../../40-proposals/035-agora-topic-addressed-record-relay.md)
and [P051](../../40-proposals/051-swarm-membership-and-reputation-bootstrap.md).

| Producer | What the reader checks |
|---|---|
| Allocation writer | A signed transition commits federation, profile/policy revisions, alias match key, generation, operation, commit time, alias-specific control public key, log sequence and previous digest. Reserve a fresh control key for each new allocation. Distinguish exact retry and authorized control-key rotation (linked predecessor and holder authorization) from contradictory allocations. |
| Alias holder | A binding signed by the active alias key covers the allocation reference, federation, match key, generation, digest of the selected route and its verification key, purpose, binding revision and validity. Check the route endpoint controls that key before disclosing a receiver credential. |
| Catalog reader | After visibility admission return the permitted route plus the minimum portable evidence: allocation receipt/reference **and its verifiable material**, signed route binding and a fresh witnessed checkpoint with proofs of inclusion and current active state. Verify against locally trusted federation policy, expiry, revocations and known high-water. No fetch of the private enrollment record. A receipt reference alone cannot satisfy a first-contact read. |
| Independent witness | An authorized replica or a separately appointed Seed Directory witnesses opaque checkpoint commitments, verifies consistency with its retained head and exchanges signed heads independently. It gains no allocation power. Use hiding commitments for low-entropy names, no public per-name feed, routes, membership maps or enumerable proof API. |

**Key Transparency design basis.** Evaluate the CONIKS private name index,
authenticated prefix tree, signed epochs and holder checks against the
existing P035 evidence verifier. Compare the IETF KEYTRANS architecture and
protocol drafts for inclusion, consistency and monitoring. Pin the proof
suite, domain separation, index-key continuity across writer handover and
bounded verification vectors at Schema Gate. Keep VRF evaluation and openings
access-controlled to prevent name enumeration.
Compare these sources before freezing the profile.
[CONIKS](https://www.usenix.org/conference/usenixsecurity15/technical-sessions/presentation/melara),
[VRFs (RFC 9381)](https://www.rfc-editor.org/rfc/rfc9381.html),
[IETF KEYTRANS working documents](https://datatracker.ietf.org/wg/keytrans/documents/).

**Witness confirmation.** Federation policy names the witnesses, their
acceptance rule and checkpoint freshness. The pilot requires one designated
witness common to every accepted view, under separate operator control and
independent signing-key custody from the writer. Two keys or hosts under one
administrator do not qualify. Before signing, the witness checks the previous
head, valid transitions and holder authorization using private openings. It
persists its last accepted head across restart. A witness signature confirms
the verified allocation history. It does not establish civil identity. Without a fresh witnessed
proof first-contact disclosure stops: the pilot has one witness availability
dependency. Never fall back to writer-only confirmation.

A future 2-of-3 rule tolerates one unavailable witness if the other two
cooperate. Two quorums can intersect in just one dishonest signer. That rule
alone cannot ensure fork prevention against one equivocating witness. Require
an explicit fault model and an honest-intersection argument for any claimed
prevention; exchanging signed heads can detect conflicts after the fact.

**Private holder monitoring.** Each online holder checks its own inclusion,
current state and consistency against the last retained, independently
witnessed checkpoint each epoch. Compare every transition since that head to
authorized holder intents or valid policy events (such as expiry or membership
suspension). After an offline interval, verify the missing transitions in
bounded batches. Retain the cursor and report incomplete history if unavailable.
Seeing the original key again cannot clear a missing or contradictory epoch.
A mismatch raises a private alert with verifiable evidence for the existing
dispute path. An unavailable proof yields "monitoring incomplete". Holder
detection supplements mandatory witness confirmation.

**Selective omission (pilot risk).** A working writer can ignore one
holder's valid renewal while continuing to serve everyone else. The
service clock and witnessed history cannot prove receipt of an unlogged
intent. Keep the pending signed intent privately, retry it unchanged and
show "renewal unconfirmed" until the holder verifies the committed receipt.
If the name enters recovery, offer restoration and private P051 review.
A local send timestamp gives reviewers context but cannot veto expiry.
Record this limitation in the pilot threat model before enabling writes.
Stronger protection would require independent, timely receipt of valid
intents and a witness rule for outstanding receipts at expiry.

A witness given openings can learn alias-to-control-key links. Restrict the
openings to the transition check, discard them after validation and retain
only opaque heads and necessary consistency state. If a dispute requires a
specific opening, isolate it with access control and the published dispute
deadline, including bounded removal from backups. Test access, purge and
restore; keep the membership-to-alias enrollment map at the writer. Public
head exchange and holder alerts must not publish the names being monitored.

Two valid incompatible allocations for the same federation, match key and
generation, or incompatible signed heads at the same log position, are
evidence. Preserve both privately, quarantine the affected name (or pause the
unresolved branch if its extent is unknown), withhold new bindings, and notify
federation reviewers. Resolve by an authenticated, witnessed recovery decision
with notice/appeal. A later timestamp, majority of lookup replies or an
unsigned complaint cannot choose a winner or freeze a name.

**Writer replacement and outage.** Policy N+1 endorses the successor and
adopts a witnessed cutoff (sequence and digest) under N. Transfer and verify
live allocations, control public keys, index continuity, lease revisions and
nominal expiries, the service clock and each open window's baseline or
paused credit, membership suspensions, open disputes,
tombstones, holds and generation high-water before enabling writes. Fence the former writer.
Reissue current proofs on demand under N+1 with the same generations. Old
receipts prove only history unless included in the adopted state with fresh
current proof. If the cutoff cannot be reconciled, pause mutations and
affected reads. During an outage refuse reservations, releases and renewals.
A replica serves a binding only with fresh evidence of visibility,
witness confirmation, lease validity, membership and revocation. An outage
cannot authorize local extensions of signed read validity.

<a id="alias-service-clock"></a>

**One witnessed service clock (P058-024, freeze before Schema Gate).** Use
the allocation checkpoint itself as the sample ("tick"). Even with no holder
requests, the writer commits an empty transition through the same mandate,
fencing, durable log and independent witness path as a renewal or restoration.
It changes no lease. A read, process heartbeat, prepared write or witness
signature on an uncommitted candidate cannot advance the clock.

The allocation policy publishes the maximum gap `G` in positive whole
seconds. Schedule idle ticks more frequently than `G`. The same policy pins
the membership evidence and freshness limits used by both write operations.
Each tick binds its policy revision, predecessor, UTC time, cumulative
seconds and a commitment to the membership evidence used by the writer.
The witness checks the authenticated source revision, federation scope and
validity interval through a private opening. A cached proof for one member
cannot establish readiness for the federation. If the
writer cannot establish a fresh membership view for the served scope, the
clock stays still. Keep member identities out of the public checkpoint.
Each renewal or restoration still verifies the holder's current membership.

For consecutive committed ticks on the same verified chain and policy,
let `d` be the difference between their signed UTC times in whole seconds.
The witness checks the proposed time against its clock under the policy's
skew bound. Credit exactly `d` when `0 < d <= G`, membership evidence
covers the interval and there is no known interruption to the write path.
Otherwise credit zero. In particular, a gap longer than `G` earns zero
for the whole gap. After a known outage, lapse in evidence or writer/policy
handover, the first qualifying tick establishes a new baseline at the
previous cumulative value. Never backfill the gap. Reject time rollback,
a broken predecessor link or a counter inconsistent with the rule. Exact
replay adds nothing. A tick proves availability at its instant. Crediting
a short gap is a sampling assumption bounded by `G`; an unobserved brief
outage or selective omission of a holder's request can escape detection.

For each lease record the clock value at notice start, or at the committed
entry into recovery for that window. If the exact notice boundary falls
inside an unmeasured interval, anchor at the first witnessed reading at or
after the boundary. Never count earlier service toward that window. Expiry
requires nominal expiry and a clock delta of at least the configured notice
opportunity. Release after recovery requires the full recovery delta.
On membership suspension preserve credit already earned, and on reinstatement
anchor the remaining opportunity at a fresh reading. A notice becoming due
while suspended starts with zero credit on return. A new lease revision opens
its own windows. Replay and restart use the stored baselines. Clock credit
never refreshes read proofs.

**Acceptance for P058-024.** Discover the writer via two Seed Directories
across an endpoint move. Send the same encrypted intent through a forwarding
Catalog and inspect its view for private inputs. Confirm exact retry, refuse
wrong capability/expired mandate and withhold on stale policy. A separate
lookup endorsement survives withdrawal of the write mandate. Verify first
contact using only the returned evidence and local trust. Substitute a route,
withhold the independent proof or replay a superseded binding: no disclosure.
Present incompatible valid allocations to different replicas, compare signed
heads and observe quarantine and review. Also refuse a second incompatible
allocation appended within a single history. An exact replay and a valid route or
key rotation cause no quarantine. Replace the writer, then replay both sides
of the cutoff, including writes backdated by the old key. Check an unchanged
name, a held name and a disputed name before reopening. Exercise reads on
both sides of the outage freshness boundary.

Before enabling writes, exercise these P058-024 cases with a controlled clock:

- Renew at T-30 and keep the original anniversary. Renew after nominal expiry
  during an outage-extended notice and count a term from commit. Include a
  leap-day expiry. Concurrent distinct intents for one revision extend once.
  Replay the winner after restart and get the same receipt.
- Restore on the last eligible tick. Observe the same generation and a full
  new term from commit. At the exclusive recovery deadline refuse restore.
  Race renewal with expiry and membership loss. Release and reallocate at the
  hold boundary with one generation increment.
- Use two leases with different notice starts. Interrupt the writer and the
  witness in each window. Replay a checkpoint, fence and replace the writer
  and check both remaining durations. Reject clock rollback and double credit.
- With fixture `G = 60`, qualifying ticks at seconds 0, 60, 121 and 131
  yield cumulative values 0, 60, 60 and 70. Keep the writer and witness up
  but let membership evidence expire after 131. A heartbeat, a failed tick
  at 140 and the first qualifying tick at 150 leave the value at 70. At 160
  it reaches 80. Check notice and recovery windows across the lapse. A
  prepared tick interrupted before commit must leave the durable clock
  unchanged after restart. Replaying its prepared bytes proves no commit.
- Suspend for exclusion, cross the deadline during appeal, then reinstate
  with the remaining opportunity. Check stale replicas, final exclusion and
  voluntary departure directly into hold. A shared mailbox can qualify two
  distinct current members with separate bound proofs. Enforce each quota.
- Drop one renewal while other holders succeed. The holder sees an
  unconfirmed intent and can seek review; its local copy grants no extension.
  Check auto-renew opt-out, locked-key failure and one confirmation on retry.
- Recover on a replacement host through the [S026 alias-key gate](../026-pseudonym-vault-and-key-roles/026-pseudonym-vault-and-key-roles.md#alias-control-key-recovery).
  Repeat with every alias key copy missing. Verify the private UI before and
  after witnessed release, refusal just before the hold ends and ordinary
  competition at the boundary. Either eligible claimant can win the next
  generation. Check ordinary and reserved-name collision vectors independently.

Withhold the pilot witness past freshness and reject same-operator substitution.
Monitor both an unauthorized intermediate change reverted before reconnect
and a valid holder rotation. Verify private alerts and witness-data expiry.

#### Catalog verification for protected lookup (planned) {#catalog-ask-verifier}

Implement [P058-026](../../40-proposals/058-contact-catalog.md#per-identifier-discovery)
at the existing route-read boundary. Only open, eligible entries contribute PSI
match tokens. A protected lookup uses an explicitly selected confidential exact
request. The returned proof and route must pass the same policy checks when
the receiver is offline.

1. **Provision.** The issuer generates a random slip secret (16–32 exchange
   symbols, default 16). Derive a lookup credential and a receiver credential
   using distinct, versioned domain labels. The lookup derivation binds the
   trusted federation, identifier kind and canonical index using unambiguous
   framing. Its client-side salt/context is deterministic from those public
   inputs, independent of existence, mode, code revision or salt fetched for
   an entry. The receiver derivation binds its own audience, purpose and,
   for alias slips, the verified allocation generation. Specify the shared
   inputs for issuer and presenter and freeze KDF profiles and vectors before
   Schema Gate. A separately configured manual code belongs only at the receiver.
2. **Store and rotate.** Over an authenticated confidential channel the
   issuer provisions only the derived lookup credential to the Catalog.
   Store a fresh random salt per entry and revision, plus
   `HMAC-SHA-256(key=lookup_credential, message=framed_context)`.
   Frame the storage domain, federation, identifier kind and index, credential
   revision and salt unambiguously. The key is the high-entropy client-derived
   lookup credential. Discard that credential after computing the verifier.
   The public storage salt is not a secret key. Reuse the existing HMAC and
   constant-time comparison primitives. The 16-symbol minimum supplies about
   78 bits from uniform generation and keeps lookup work bounded.
   Commit mode, verifier, salt, profile and revision atomically. Rotate with
   a new secret and withdraw the old verifier. Reallocation starts without
   prior credentials. Revoke or replace each gate independently. Offer a
   two-gate card for sharing only after both updates commit. On partial
   failure show which update committed and offer withdrawal or retry.
   Keep presentation values outside sync, diagnostics and notifications.
3. **Read.** Submit only the lookup credential under the authenticated Catalog
   channel; treat this derived input as a bearer for this lookup until rotation.
   Compute and compare the storage verifier in constant time. Check the expected
   generation from a slip before returning a route. Bare alias searches use
   the current generation. Keep the raw slip secret, receiver proof and all
   raw or derived `once` material outside the Catalog. The stored verifier
   is never a valid presentation. Missing, hidden, wrong-code, retired and
   stale requests have equivalent external responses. Bound work for negative
   lookups, including absent entries, without a per-entry parameter endpoint.

A storage salt raises the cost of bulk guessing. It adds no secret entropy.
A three-character human code has at most 46,656 ASCII-folded possibilities.
Such codes can be used only in the separate receiver input. The issuer never
provisions them for Catalog lookup or exposes a public guessing transcript.
A Catalog compromise can expose routes and
permit lookup impersonation on its own surface. Its verifier or lookup bearer
cannot be used as receiver proof. Unknown or stale replicas forward privately
to a current authorized verifier or withhold the route.

**Acceptance.** With two identifiers and separate request gates, check
cross-entry/cross-purpose substitution, a stolen storage verifier, rotation
and pause across restart. A single generated slip configured at both gates
works; the lookup input alone fails at the receiver. With independent codes,
the UI requests the missing receiver input. Observe identical client derivation
for hidden, absent and recently rotated identifiers without parameter probes.
Freeze HMAC vectors with independent salts, revision and cross-entry replay
negatives. Test 15/16/32/33 symbols at the slip boundary. Type a manual code
that looks exactly like a generated value in the request-code field: no raw
or derived value reaches the Catalog.
Wrong-code attempts have bounded work. Exercise attempted guessing separately
from a valid-code prompt flood. Reserve bounded fair opportunities under
pressure, coalesce owner alerts and allow private per-code pause/rotation.
Absolute availability under total resource exhaustion is outside the guarantee.

#### Lookup privacy follow-ups (planned) {#lookup-privacy-follow-ups}

Use the [P058 privacy table](../../40-proposals/058-contact-catalog.md#per-identifier-discovery)
when selecting an endpoint. The service-side observations for the proposed
profiles are:

| Surface | On a miss | On a hit |
|---|---|---|
| Exact / invitation-only | Target or dictionary-recoverable normalized index. Raw inputs are rejected by the existing invitation-only endpoint. | Selected entry. |
| Blinded digest | Digest and request context. Guessability depends on the identifier space and key/oracle access. | Selected entry. |
| Open-only PSI | Blinded elements and protocol metadata. | Selected entry on presentation of its match token. |
| Protected lookup | Target or equivalent index even with an incorrect code. | Selected entry. |

- **P058-027 (PSI-128).** In Node's `contact-catalog-service::evaluate_psi`
  the service takes at most 128 candidate claims before token projection. Its
  success response does not certify completeness. Distinguish bounded
  *incomplete* from an authoritative miss end to end. First support explicit
  incomplete/refusal on overflow; any later pagination must be bounded,
  snapshot-consistent, non-enumerating for restricted entries and resumable.
  Count eligible distinct candidates, enforce current visibility, and never
  downgrade to plaintext lookup. Test 127, 128 and 129 unique open entries,
  a smaller client limit, duplicates and reversed insertion order. Put the
  target beyond the initial bound. Neither client nor UI reports absence
  unless the eligible set was covered. Check that hidden and protected entries
  contribute no tokens or observable counts.
- **P058-028 (caller–entry retention).** Current SQLite lookup audit rows
  persist both `auth_fingerprint` and `contact_index_digest`. Redacting raw
  handles leaves the pair linkable. Keep any joint key only in a bounded
  rate store until the published limit window ends. Keep independent per-entry
  and per-caller counters and aggregate durable audit without a joinable
  bucket, event ID or correlated per-request trace. Expire old paired rows
  through an explicit migration and prevent backup restore from reviving
  expired pairs. Use a controlled clock, successful and failed lookups, restart
  on either side of expiry, rotation and restore. Inspect the store, WAL,
  backup lifecycle, status, logs and exports for reconstructible links. Enforce
  the deadline after interrupted cleanup or restoring an older snapshot. Verify
  active limits still hold within the window. Network-level anonymity is a
  separate future decision.

### Contact Request Admission

Based on:

- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/40-proposals/057-user-and-operator-notifications.md`
- `doc/project/60-solutions/017-inter-node-artifact-channel/017-inter-node-artifact-channel.md`
- `doc/project/60-solutions/023-artifact-delivery/023-artifact-delivery.md`

Related schemas:

- `contact-request.v1`
- `notification.v1`
- `notification-action.v1`
- `capability-passport.v1`

Responsibilities:

- register exactly one authoritative acceptor for `contact-request.v1`;
- turn accepted contact requests into durable user notifications with accept and
  reject actions;
- on acceptance, issue a narrow `messaging-receive` capability passport scoped
  to the accepted sender, recipient route, public handle reference, operation,
  expiry, and revocation reference;
- on rejection, record the local decision without minting authority.

An exact replay of a still-valid request returns its original contact decision.
For the same authenticated peer, sender and recipient route, a later signed
request can open a new explicit decision after the host confirms expiry or
revocation of the accepted receive consent. The request's signed issue time
must follow the previous accepted decision. Missing or stale authority
observations leave the previous decision in place.

The contact store atomically links one pending successor to the exact prior
decision. The first successor's request and notification identity survive
replay and restart. Prior accepted or rejected decisions remain readable by
their original IDs. A renewed decision requires explicit operator approval
on the existing contact. Startup and reciprocity leave it pending.

Status:

- `done for hard-MVP` — The daemon registers a default in-process Artifact Delivery
  acceptor target `contact.request`, persists `contact-request.v1` state, creates
  durable `contact-request.received` notifications, exposes host-owned
  accept/reject actions, and issues `messaging-receive@v1` passports on
  acceptance. Validation tests cover real participant signatures, expiry, bad
  purpose, bad signature, and redacted notification wording. Story 010 strict
  smoke exercises the operator notification accept path end-to-end; broader
  failure-matrix AD accept/reject tests remain post-MVP hardening.

#### Admission with recipient-issued invitations (planned)

Implement [P058-022/023](../../40-proposals/058-contact-catalog.md#recipient-issued-contact-invitations)
at the existing daemon-owned `contact.request` acceptor. Keep the supervised
Contact Catalog responsible for route discovery. Use the same validator,
logical-request deduplication, local decision store and notification path for
both a newly resolved and a cached route.

- Bind the private presentation to the receiver, purpose and exact signed
  request. Version and validate its carrier at Schema Gate before enabling
  this mode. Keep the receiver's presentation out of Catalog lookup, greeting,
  stored request JSON, notifications, URL query logs and traces. Keep a receiver-keyed verifier
  for the recipient-only manual code. Verify it inside the confidential,
  authenticated request channel in constant time, bound to the signed request
  digest, recipient and purpose. A public digest or observable HMAC transcript
  with a human code would permit offline guessing. For generated slips use
  only the receiver-scoped presentation with replay protection. A reference alone cannot redeem either kind.
- Apply the invitation check before any user-visible first-contact prompt,
  including an INAC approval prompt for this request. If the peer or transport
  cannot present the required proof privately at that boundary, refuse the
  attempt. A legacy path cannot downgrade the recipient's policy.
- For a reusable code, persist the admitted request and offer the existing
  accept/reject decision. For a single-use token, coordinate the local
  invitation record with [P076-039](../../40-proposals/076-limited-messaging-grants-decision.md#advance-contact-consent)
  using the durable decision and its exact request binding. Resume an
  interrupted redemption from that record. After successful issuance, update
  the private contact projection and hand off the committed passport through
  the existing owners.

### Local Contact Store

> **Ownership note (cross-reference to Solution 032):** With the
> introduction of the Local Relationship Layer (Solution 032), semantic
> relationship state — classes, memberships, relationship predicates,
> and pairwise relationship facts — moves to Solution 032. Raw handles,
> UX labels, and local address-book records stay in the daemon Local
> Contact Store. Contact Catalog retains only public discovery /
> route-set lookup state. The expected flow becomes:
> `Catalog lookup (public discovery) → Local Relationship annotation (private) → consumer policy (passport-gated)`.
>
> `local-contact.v1` schema is preserved unchanged. Its recovery bundle
> remains sealed through the Pseudonym Vault, while `local-relationship`
> vault entries carry relationship facts. Relationship classes such as
> `friends` are not a Catalog concept; Catalog never sees them.

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`
- `doc/project/30-stories/story-010-message-to-a-friend.md`
- `doc/project/60-solutions/032-local-relationship-layer/032-local-relationship-layer.md`

Related schemas:

- `local-contact.v1`

Responsibilities:

- store raw external handles, labels, and local address-book mappings locally;
- keep the store unpublished by default;
- persist user-level continuity data needed to restore local contacts after
  node recovery;
- expose only redacted or digest-bound references to network artifacts.

> Solution 032 does not make Contact Catalog the owner of private
> relationships. It only moves relationship classes, membership facts,
> predicates, and pairwise relationship facts out of Messaging/AD/Catalog
> into the Local Relationship Layer.

Status:

- `done for hard-MVP` — The daemon owns
  `<node-data-dir>/storage/local-contacts.sqlite` and exposes local
  create/list/get/patch/archive routes. Records now carry compatible `label`,
  explicit `labels[]`, `metadata {}`, UX/provenance fields, and an active
  pairwise contact-nym pointer. The store also maintains
  `local_contact_pairwise_mappings` with `active`, `rotated`, `revoked`, and
  `archived` lifecycle states so nym rotation is history-preserving. Raw handles
  remain daemon-local and are not emitted by Contact Catalog lookup, Seed
  Directory records, or shared lookup audit. Durable local recovery mirror
  records exist for messaging recovery; the local contact store can export and
  replay local-contact, pairwise-mapping, and messaging-recovery mirror records
  without reactivating revoked or archived pairwise mappings.
  `pseudonym-vault.v1` can carry a sealed
  `local-contact-recovery-bundle.v1`; vault import replays that bundle, and
  daemon startup replays the latest operational-vault-key sealed vault
  snapshot. Legacy root-only snapshots are migration/recovery inputs, not the
  normal hot-path profile. Explicit operator replay/export hooks accept
  `local_passphrase` for `root+local-passphrase` vaults without opening those
  vaults during unattended startup or weakening their wrap profile.

## May Implement

### Federated Contact Catalog Peer Fetch

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-claim.v1`

Responsibilities:

- use `ObservedCatalogStore<ContactClaimRecord>` only for communities that
  explicitly accept a private peer/fetch federation model;
- never expose a public anonymous dump of the contact catalog; ordinary clients
  use authenticated lookup, while bulk/list fetch is local-operator or
  trusted-provider sync only;
- let the host/daemon own discovery, trust policy, passport validation, auth
  material, and revocation freshness;
- use direct catalog-to-catalog HTTP as the data plane only after host policy
  has marked the provider trusted;
- implement reusable fetch/merge/replay mechanics in the generic catalog
  abstraction, while this service owns Contact Catalog runtime and privacy
  policy;
- preserve publisher and origin provenance;
- forbid raw contact handles, unsalted public hashes, and public-log-style
  contact projections in federated records;
- keep Agora out of the Contact Catalog propagation path.

Status:

- `done for hard-MVP` — `node/catalog::CatalogAdapter<T, F>` now has a generic
  `ObservedRecord<T>` fetch contract and Contact Catalog defines
  `RemoteContactClaimFilter`; `contact-catalog-service` uses a
  `RemoteContactCatalogHttpAdapter` to refresh trusted provider claims into a
  sidecar remote cache. `node/catalog` now also carries the generic
  `sync_catalog_provider(...)` mechanic for fetch, observed-record validation,
  loop guardrails, self-origin rejection when the daemon provides the local
  node id, sequence-aware merge, data-derived high-water metadata and counted
  outcomes. Contact Catalog exposes authenticated
  `GET /v1/contact-catalog/sync/claims` as the trusted provider snapshot
  contract and records provider sync state in the sidecar with last-run counts
  and cumulative totals.
  Provider tombstones are now part of the trusted-provider snapshot body and
  are cached durably; replay/restart hides remote claims whose sequence is
  covered by a cached tombstone, and sync status records a retryable/terminal
  failure class.
  Provider policy remains trusted-only for sync, but operators can now inspect
  discovered providers and set `trusted`, `uncertain`, or `blocked` from
  `/admin/contact-catalog` over the service policy endpoint. No Agora
  publication/relay path is introduced. Provider trust changes are durably
  audited with actor, a required reason capped at 1000 characters,
  previous/next state, passport hash and endpoint.
  Local tombstone facts are produced for operator-tombstoned and
  projection-revoked claims, exported through `tombstones[]`, and applied on
  active-only read paths after restart. Broader production federation matrices
  remain post-MVP hardening.

### Blinded or PSI Lookup

Based on:

- `doc/project/40-proposals/058-contact-catalog.md`

Related schemas:

- `contact-lookup-result.v1`

Responsibilities:

- replace or supplement public invitation-only digest lookup with stronger
  private discovery profiles once the cryptographic protocol is selected;
- keep the result artifact stable so clients do not depend on the lookup
  protocol internals.

Status:

- `done for hard-MVP` — `orbiplex-node-crypto::contact_psi` provides auditable
  Ristretto255 DH-PSI primitives, and the Contact Catalog service accepts
  `blinded-digest` and `psi` lookup modes with mode/index pairing, redacted
  audit, rate limiting and route-set responses. Hard-MVP PSI uses
  `POST /v1/contact-catalog/psi/evaluate` for bounded evaluated elements and
  candidate tokens, then `POST /v1/contact-catalog/lookups` with
  `lookup_mode = "psi"` plus `psi/match-token`. The service-local PSI server
  seed is stored as plain base64url in the service SQLite database; the
  hard-MVP security boundary is the local data-dir filesystem, and the seed is
  not emitted through status, audit or sync. Broader PSI failure matrices remain
  focused lower-level tests rather than a separate top-level E2E harness;
  Story-010 strict `ad-smoke` remains the E2E gate. Completeness beyond the
  candidate limit and caller–entry retention have [separate corrective
  gates](#lookup-privacy-follow-ups).

## Out of Scope

- becoming a global address book;
- storing raw personal address books in a network catalog;
- treating phone or email control as legal identity assurance;
- issuing general friend-class capabilities;
- owning messaging UI or mailbox storage beyond the contact-request acceptor;
- making Seed Directory contact-aware.

## Consumes

- `contact-claim.v1`
- `contact-request.v1`
- `capability-passport.v1`
- `routing-subject-binding.v1`
- Seed Directory capability provider records for `contact-catalog`,
  `email-control`, and `phone-control`

Contact Catalog provider discovery is capability-first. The daemon asks Seed
Directory for providers advertising the `contact-catalog` capability and applies
the same local multi-directory query policy used by Artifact Delivery and other
discovery consumers. Contact Catalog remains the domain lookup service after a
provider is selected; Seed Directory does not become contact-aware and does not
authorize message delivery by itself.

## Produces

- `contact-lookup-result.v1`
- notification records for `messaging.contact-request`
- `capability-passport.v1` under `messaging-receive`
- local audit facts about admission, lookup, no-match, acceptance, and rejection

## Notes

The default MVP path remains invitation-only digest lookup, and the runtime also
accepts `blinded-digest` and `psi` lookup modes for claims indexed with the
matching private mode. This keeps the common path simple while letting stricter
privacy mechanics evolve at the lookup edge without changing the route-candidate
contract.

Concrete crate/module ownership belongs in the Node implementation repository.
The implementation is a Rust supervised `channel_json` middleware with a separately
owned bounded Contact Catalog product HTTP service. It
links `orbiplex-node-catalog`, implements `ContactClaimRecord: CatalogRecord`,
and stores data under a middleware-owned SQLite database such as
`<node-data-dir>/storage/contact-catalog.sqlite`.
