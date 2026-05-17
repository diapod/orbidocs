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

## Artifacts

### `contact-attestation-request.v1`

Acquisition-side request from a node to the attestation service. It contains
only the raw contact handle needed for delivery and the Orbiplex subject that
will receive the passport.

### `contact-attestation-result.v1`

Return artifact carrying the issued passport plus contact digest and challenge
metadata. The result does not carry the OTP transcript.

## MVP Runtime

The MVP runtime is a supervised local HTTP middleware. It is disabled by
default. It supports a local/dev delivery adapter that records the link and OTP
code in service-local debug state for integration testing. That debug view is a
local/dev adapter artifact, not production challenge state. Production SMTP/SMS
delivery providers are explicitly out of scope for this proposal slice.

The service never owns signing keys. Passport issue goes through host capability
`capability.passport.issue`.

Implemented MVP endpoints:

- `GET /v1/attestation/status`;
- `POST /v1/attestation/challenges`;
- `POST /v1/attestation/challenges/{challenge_id}/redeem`.

The bundled node config keeps the service disabled by default and injects the
standard host capability bridge environment when enabled.
