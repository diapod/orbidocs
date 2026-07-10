# Nym Authorship Proof v1

Source schema: [`doc/schemas/nym-authorship-proof.v1.schema.json`](../../schemas/nym-authorship-proof.v1.schema.json)

Inline-first proof that a nym-authored Agora record is signed by a certified application-layer pseudonym whose certificate scope authorizes the record context.

## Governing Basis

- [`doc/project/40-proposals/035-agora-topic-addressed-record-relay.md`](../../project/40-proposals/035-agora-topic-addressed-record-relay.md)
- [`doc/project/40-proposals/013-whisper-social-signal-exchange.md`](../../project/40-proposals/013-whisper-social-signal-exchange.md)
- [`doc/project/60-solutions/011-whisper/011-whisper.md`](../../project/60-solutions/011-whisper/011-whisper.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `nym-authorship-proof.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`proof/suite`](#field-proof-suite) | `yes` | enum: `orbiplex.nym-ed25519-cert.v1` | Verification suite. M4 accepts Ed25519 nym keys certified by an inline council-issued nym certificate. Future suites may use threshold credentials or zero-knowledge attestations without changing the Agora envelope. |
| [`proof/mode`](#field-proof-mode) | `yes` | enum: `inline-certificate` | Inline-first mode: enough signed material is carried in the record to verify without an additional network lookup. |
| [`proof/audience`](#field-proof-audience) | `yes` | enum: `agora-ingest` | Audience binding. Prevents reusing an application nym certificate proof as an unrelated protocol credential. |
| [`proof/context`](#field-proof-context) | `yes` | object |  |
| [`nym/certificate`](#field-nym-certificate) | `yes` | ref: `#/$defs/nymCertificate` |  |
| [`scoped-claim/request`](#field-scoped-claim-request) | `no` | ref: `scoped-claim-request.v1.schema.json` | Optional P081 request binding this authorship evidence to one concrete Agora ingest candidate. It MUST appear together with scoped-claim/presentation. |
| [`scoped-claim/presentation`](#field-scoped-claim-presentation) | `no` | ref: `scoped-claim-presentation.v1.schema.json` | Optional P081 presentation verified before Agora applies its independent local publish policy. It MUST appear together with scoped-claim/request. |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`stringList`](#def-stringlist) | array |  |
| [`signature`](#def-signature) | object |  |
| [`nymCertificate`](#def-nymcertificate) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `nym-authorship-proof.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-proof-suite"></a>
## `proof/suite`

- Required: `yes`
- Shape: enum: `orbiplex.nym-ed25519-cert.v1`

Verification suite. M4 accepts Ed25519 nym keys certified by an inline council-issued nym certificate. Future suites may use threshold credentials or zero-knowledge attestations without changing the Agora envelope.

<a id="field-proof-mode"></a>
## `proof/mode`

- Required: `yes`
- Shape: enum: `inline-certificate`

Inline-first mode: enough signed material is carried in the record to verify without an additional network lookup.

<a id="field-proof-audience"></a>
## `proof/audience`

- Required: `yes`
- Shape: enum: `agora-ingest`

Audience binding. Prevents reusing an application nym certificate proof as an unrelated protocol credential.

<a id="field-proof-context"></a>
## `proof/context`

- Required: `yes`
- Shape: object

<a id="field-nym-certificate"></a>
## `nym/certificate`

- Required: `yes`
- Shape: ref: `#/$defs/nymCertificate`

<a id="field-scoped-claim-request"></a>
## `scoped-claim/request`

- Required: `no`
- Shape: ref: `scoped-claim-request.v1.schema.json`

Optional P081 request binding this authorship evidence to one concrete Agora ingest candidate. It MUST appear together with scoped-claim/presentation.

<a id="field-scoped-claim-presentation"></a>
## `scoped-claim/presentation`

- Required: `no`
- Shape: ref: `scoped-claim-presentation.v1.schema.json`

Optional P081 presentation verified before Agora applies its independent local publish policy. It MUST appear together with scoped-claim/request.

## Definition Semantics

<a id="def-stringlist"></a>
## `$defs.stringList`

- Shape: array

<a id="def-signature"></a>
## `$defs.signature`

- Shape: object

<a id="def-nymcertificate"></a>
## `$defs.nymCertificate`

- Shape: object
