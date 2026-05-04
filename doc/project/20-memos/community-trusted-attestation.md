# Community-Trusted Attestation

Based on:

- `doc/project/20-memos/participant-assurance-levels.md`
- `doc/project/20-memos/reputation-signal-v1-invariants.md`
- `doc/project/40-proposals/041-agora-ingest-attestation.md`
- `doc/project/60-solutions/021-agora-authority/021-agora-authority.md`

## Status

Seed memo

## Date

2026-05-01

## Purpose

This memo records a possible future assurance level derived from community
reputation rather than from a phone, national identity document, or static
sovereign-operator designation.

## Memo

Consider adding an attestation level named `community-trusted` or
`community-entrusted`. The level would mean that a participant or organization
has reached a high community trust threshold, for example an approximate top 1%
of the relevant community. The exact threshold should be configurable per
community or federation rather than hard-coded globally.

This status should not be recomputed ad hoc during every authorization check.
Instead, reputation results should be published as signed, periodically updated
facts, for example once per day, under an Agora namespace such as
`ai.orbiplex.reputation`. Writes to that namespace should require trusted
authority, because downstream access policies may depend on these reputation
snapshots.

Future access policies may combine assurance levels through threshold rules,
for example:

- at least 3 identities with `community-trusted` attestation,
- at least 2 identities with `national-id` attestation and 1 identity with
  `community-trusted` attestation.

## Boundary

`community-trusted` is not the same kind of signal as `phone-confirmed` or
`national-id`. Phone and national-id attestations bind the identity to external
evidence. `community-trusted` is a derived social/governance status based on
reputation computation and publication authority.

The authorization layer should therefore treat it as a time-bounded derived
status with an explicit publisher, timestamp, community scope, and freshness
requirement.

## Open Questions

- Is the threshold global, federation-local, or community-local?
- Is `community-trusted` a stable attestation, a daily computed status, or a
  cached projection over reputation facts?
- Which authority is allowed to publish reputation snapshots for a community?
- How are appeals, decay, stale snapshots, and reputation-source capture
  handled?
- Should the canonical name be `community-trusted` or `community-entrusted`?

