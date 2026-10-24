# Proposal 061: Contact Attestation Service

Status: Draft

## Purpose

The Contact Attestation Service proves control of an email address or phone
number for Orbiplex contactability flows. It issues contact-control passports:

- `email-control@v1` for email addresses,
- `phone-control@v1` for phone numbers.

These passports prove control of a contact channel. They are not legal identity
assurance and they do not imply that the channel holder is a particular civil
person.

They also do not unlock public-trust roles, governance, high-value marketplace
access, or reputation leverage by themselves. In membership bootstrap they are
only evidence for contactability, anti-spam policy, recovery paths, and
contact-catalog admission. Higher influence surfaces still require the relevant
entry profile, sponsorship, probation, reputation, IAL, and anti-collusion
checks.

## Role and Discovery

An attestation service is a role advertised through Seed Directory discovery.
The service operator may be the same deployment as a Seed Directory, but the
roles remain distinct:

- Seed Directory discovers attestation providers and may publish their
  capability passports.
- Attestation Service runs challenge delivery, redemption, and passport issue
  orchestration.
- Node/messaging clients request attestations only from an explicitly selected
  provider.

The capability ids are:

- `email-attestation` with wire name `role/email-attestation`;
- `phone-attestation` with wire name `role/phone-attestation`.

Both require passports in the MVP because they cause trusted contact-control
passports to be issued.

## OTP / Link Flow

1. The node sends `contact-attestation-request.v1` with the raw delivery target,
   subject identity, requested capability profile, and purposes.
2. The service creates a challenge with:
   - `challenge/id`;
   - random OTP code;
   - redemption link containing `challenge/id`;
   - expiry default of 24 hours;
   - attempt limit default of 5.
3. The service delivers both the link and one-time code through the selected
   contact channel.
4. The durable challenge row stores only an OTP verifier:
   `sha256(challenge_id || ":" || otp_code)`. It does not store the raw OTP
   as challenge state.
5. The node redeems the challenge with `challenge/id`, OTP code, and the
   original attestation request context.
6. On success, the service asks the host to issue an `email-control@v1` or
   `phone-control@v1` capability passport and returns
   `contact-attestation-result.v1`.

Challenge redemption is single-use. Expired, already redeemed, or attempt-limit
exhausted challenges fail terminally.

A valid redemption durably consumes its challenge before host passport issuance.
Concurrent requests cannot start another issuance. If a crash or failed/lost host
reply leaves its outcome unresolved, restart and repeated redemption MUST NOT
retry that issuance. The caller explicitly creates a fresh challenge and proves
control again. Consumed unresolved attempts do not occupy pending-challenge
quota; protected operator status reports them separately. This conservative
failure contract avoids issuing twice after an unknown effect.

### Separate-provider access

The provider operator MAY explicitly enable unauthenticated challenge creation
and redemption. This opt-in is disabled by default. It opens only
`POST /v1/attestation/challenges` and
`POST /v1/attestation/challenges/{challenge_id}/redeem`; the existing OTP, expiry,
attempt limits and pending-challenge quotas still apply. Discovery and provider
selection remain verified host operations. Public access grants neither passport
issuance authority nor a bypass of contact-control proof.

Status/debug and middleware lifecycle endpoints MUST always require their
respective operator tokens, including when no token is configured. An absent
authentication configuration fails closed. Startup MUST refuse missing, invalid,
empty or unreadable lifecycle and client/status token configuration before state
creation, listener binding or publication. Client/status auth remains configured
even when challenge/redeem is public. Health/readiness probes remain public.
Public challenge responses MUST NOT contain the delivered code or a debug link
carrying it. The local dev adapter may retain that information only behind the
authenticated operator status surface; reading it is a substituted delivery
boundary in synthetic acceptance, not real email/SMS delivery.

Node implements this explicit opt-in as
`ORBIPLEX_ATTESTATION_PUBLIC_CHALLENGES=true` in the service launch environment.
Only an explicit positive value (`1`, `true`, `yes`, `on`, case insensitive)
enables it. It MUST NOT be combined with the acceptance-only `always_accept`
policy: the service refuses that configuration before creating challenge state.
No provider token is distributed to participant nodes. This access decision was
adopted for P076-034 on 2026-10-23; the proposal's remaining production delivery
and federation qualification scope is unchanged.

### Bounded admission and retention (2026-10-24)

Public create/redeem MUST be bounded by a global pending-challenge limit, a
rate limit for the accepted remote TCP address and a durable daily attempt
budget per delivery adapter. Caller-declared subjects and forwarded-address
headers do not establish source identity. A proxy-specific trust policy would
be a separate decision. The source bucket map itself has bounded capacity and
idle retention; it refuses new sources when full instead of resetting active
depleted buckets through eviction.

The existing SQLite write transaction reserves pending admission and adapter
budget before the external effect. Delivery budgets also apply in private mode.
An unknown or failed delivery reply MUST NOT automatically refund an attempt;
SMTP/SMS may have produced a billable effect. Budget state survives restart and
its UTC high-water mark survives pruning. Clock rollback cannot reopen spent
windows. Admission refusal invokes no delivery adapter.

The host client and original payload are checked before redemption reservation;
expiry is part of its CAS. The admission timestamp is observed after acquiring
the SQLite writer; time spent waiting for a writer cannot extend the OTP lease.
The reservation commits before host I/O. A proven pre-effect refusal is `redemption-not-attempted`.
After reservation the outcome stays conservatively unknown on transport,
validation or persistence failure, including a crash before actual dispatch.
Neither restart, the dev `always_accept` error path nor a delivery-error cleanup
may erase that consumption. The OTP may already have been redeemed concurrently
before a provider reports its delivery error.

Bounded write-side cleanup replaces expired challenge/target/request/dev OTP data
with redacted terminal tombstones atomically. Unknown-redemption status includes
these tombstones; reads do not perform cleanup. Audit and tombstone retention is
separate from pending quota. Implementation defaults and startup instructions
live in `node:attestation-service/README.md`.

| Follow-up | Status | Evidence boundary |
| :--- | :--- | :--- |
| F-02 global/source/adapter budgets and retention | done | Focused concurrency, reopen, UTC/rollback, lost delivery reply and cleanup tests; no real SMTP/SMS or production exposure qualification |
| F-03 redemption preflight and expiry CAS | done | Known non-attempt stays unconsumed; a real fixture host's lost reply remains single-use after reopen |
| F-04 fail-fast token configuration | done | Configuration refuses before bind; public create/redeem cannot access lifecycle or status |

These changes retain the historical synthetic P076-034 evidence with its original
source pins. The initial combined focused suite passed 28 tests; it does not
enlarge that candidate's measured scope or establish production readiness. A final review
added two real writer/provider-barrier regressions; the resulting 30-test suite
also proves expiry across writer contention and preservation of concurrent
redemption after a lost delivery reply.

### Local acceptance mode

Implementations MAY expose an operator/test-only `always_accept` provider policy,
defaulting to `false`. When enabled, the provider treats each structurally valid
email or phone attestation request as already confirmed and asks the host to
issue the corresponding contact-control passport during challenge creation.

This mode exists for local acceptance profiles such as Story-010. It bypasses
only delivery-channel proof. It MUST NOT bypass host passport issuance,
capability/passport checks, provider discovery, or Contact Catalog admission.
Production deployments MUST keep it disabled.

## Artifacts

### `contact-attestation-request.v1`

Acquisition-side request from a node to the attestation service. It contains
only the raw contact handle needed for delivery and the Orbiplex subject that
will receive the passport.

### `contact-attestation-result.v1`

Return artifact carrying the issued passport plus contact digest and challenge
metadata. The result does not carry the OTP transcript.

## Runtime

The runtime is a supervised `channel_json` middleware with a separately owned bounded
attestation product HTTP API. It is still opt-in in bundled node config: the seed
fragment is present, but the operator must enable the `attestation_service`
middleware setting before the daemon starts it. The
bundled opt-in config selects the local/dev delivery adapter explicitly, so a
developer node can run the Story-010 flow without SMTP or SMS credentials.

The service supports three delivery modes:

- `dev` stores the redemption link and OTP in service-local debug state;
- `smtp` sends email challenges through an operator-configured SMTP relay;
- `webhook` sends phone challenges to an operator-configured SMS provider
  webhook.

The debug view is a local/dev adapter artifact, not production challenge state.
Production deployments should select `smtp` for email and `webhook` for phone,
provide credentials through secret files when possible, and keep the debug
adapter disabled. If both a direct secret environment variable and its `_FILE`
variant are configured, the `_FILE` value wins; loaded file secrets are trimmed
and unreadable or empty files are treated as no configured secret rather than
falling back to the direct environment value.

The service never owns signing keys. Passport issue goes through host capability
`capability.passport.issue`.

Implemented MVP endpoints:

- `GET /v1/attestation/status`;
- `POST /v1/attestation/challenges`;
- `POST /v1/attestation/challenges/{challenge_id}/redeem`.

The bundled node config keeps the service disabled by default and injects the
standard host capability bridge environment when enabled. Operator policy knobs
include the default 5-attempt challenge limit, 24-hour TTL, pending-challenge
quotas per handle and participant (participant equality uses a canonical JCS
subject digest, never substring matching over request JSON), the
default-disabled `always_accept` local
acceptance mode, and delivery audit retention. The runtime
records delivery audit rows without storing raw OTP values in the durable
challenge table.

Seed Directory advertisement remains a role-discovery concern: providers should
advertise `role/email-attestation` and/or `role/phone-attestation` with
capability passports, while clients keep the provider selection explicit.
