# Messaging Middleware Implementation Notes

Date: `2026-05-17`

## Runtime Boundaries

`messaging-core` is the pure domain layer. It owns typed envelope validation,
queue-state names, refusal classes, mailbox-resolution DTOs, and
`messaging-receive@v1` scope matching.

`messaging-service` is the supervised middleware. It owns Maildir bodies,
SQLite indexes, outbound queue transitions, `contacts` membership, pending
facts, and service status. It calls host capabilities for authority decisions
and side effects outside the messaging domain.

`daemon` is the host and authority layer. It owns signing, Capability Binding,
revocation view checks, Artifact Delivery, notification dispatch, local
participant-handle evidence, Memarium, and Pseudonym Vault recovery mirroring.

`node-ui` is a thin operator surface. It renders daemon-proxied messaging
state and forwards compose/action requests.

## Disabled-by-Default Service

The bundled messaging service remains disabled by default. Enabling it starts a
loopback supervised HTTP service and injects the standard host capability
environment variables into the child process.

## Local Data

The service stores data under its module data directory:

```text
storage/messaging/
  index.sqlite
  maildir/
    <mailbox-id>/{tmp,new,cur}
    drafts/{tmp,new,cur}
```

Outbound compose writes the body to the `drafts` Maildir before queueing the
Layer 2 row. SQLite stores the digest, size, routing metadata, state, host
delivery ids, retry diagnostics, and draft path.

## Outbound Processor

`POST /v1/messaging/outbox/process` runs a bounded deterministic batch. The
daemon may call the same endpoint from a small service loop. The endpoint is
idempotent: it advances only rows whose state and retry time allow progress.

Host capability failures are classified as retryable unless the host returns a
schema, conflict, or scope refusal. Retryable rows keep `last_error` and
`next_attempt_at`.

## Inbound Policy

Inbound admission validates `message-envelope.v1`, validates any inline passport
against the message, verifies `passport-ref` through `capability.passport.lookup`
when host capabilities are configured, asks the daemon to resolve the local
mailbox, and then applies the `contacts` policy gate. A first valid receive
passport tied to an accepted contact request may project membership. Otherwise a
missing active membership is refused as `contacts-policy-denied`.

The refusal response is intentionally generic. It must not reveal whether a
public handle exists locally or which participant owns it.

## Facts and Recovery

Layer 3 fact writes go through `memarium.write`. On failure, the fact is stored
in `pending_facts` and service status becomes `degraded`. Replay is explicit and
idempotent through `POST /v1/messaging/pending-facts/replay`.

Recovery mirroring is host-owned. The service requests
`identity.messaging-recovery.mirror` for membership and receive-passport
reference records. The daemon persists those records in a durable local
recovery mirror table; sealed Pseudonym Vault startup replay is still a later
layer. The messaging service can accept replayed records through its recovery
endpoint or startup replay path.

## Verification

The MVP+ acceptance set is:

- schema-gate validates message envelopes, fact schemas, and host capability
  DTOs;
- service tests cover inbound idempotency, outbox processing, pending facts,
  and reindex;
- daemon tests cover passport lookup, participant handle ownership,
  mailbox-resolution fallback, and `mailbox.open`;
- UI smoke loads `/admin/messaging`, queues compose, lists inbox/outbox, and
  opens a message detail through a notification action.
