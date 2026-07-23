# Story 012 Power DNS Full-system Report v1

Source schema: [`doc/schemas/story-012-powerdns-full-system-report.v1.schema.json`](../../schemas/story-012-powerdns-full-system-report.v1.schema.json)

Closed metadata-only report for the Story 012 single-host PowerDNS and Bielik full-system acceptance.

## Governing Basis

- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)
- [`doc/project/40-proposals/066-inquirium-assistant-channel.md`](../../project/40-proposals/066-inquirium-assistant-channel.md)
- [`doc/project/40-proposals/069-corpus.md`](../../project/40-proposals/069-corpus.md)
- [`doc/project/40-proposals/071-sensorium-workbench.md`](../../project/40-proposals/071-sensorium-workbench.md)

## Project Lineage

### Requirements

- [`doc/project/50-requirements/requirements-006-node-networking-mvp.md`](../../project/50-requirements/requirements-006-node-networking-mvp.md)
- [`doc/project/50-requirements/requirements-010-middleware-executor.md`](../../project/50-requirements/requirements-010-middleware-executor.md)
- [`doc/project/50-requirements/requirements-011-dator-arca-contracts.md`](../../project/50-requirements/requirements-011-dator-arca-contracts.md)
- [`doc/project/50-requirements/requirements-014-resource-opinions.md`](../../project/50-requirements/requirements-014-resource-opinions.md)

### Stories

- [`doc/project/30-stories/story-001-swarm-node-onboarding.md`](../../project/30-stories/story-001-swarm-node-onboarding.md)
- [`doc/project/30-stories/story-004-pod-client-onboarding.md`](../../project/30-stories/story-004-pod-client-onboarding.md)
- [`doc/project/30-stories/story-005-whisper-rumor-intake.md`](../../project/30-stories/story-005-whisper-rumor-intake.md)
- [`doc/project/30-stories/story-006-buyer-node-components.md`](../../project/30-stories/story-006-buyer-node-components.md)
- [`doc/project/30-stories/story-006-voluntary-swarm-exchange.md`](../../project/30-stories/story-006-voluntary-swarm-exchange.md)
- [`doc/project/30-stories/story-007-settlement-capable-node.md`](../../project/30-stories/story-007-settlement-capable-node.md)
- [`doc/project/30-stories/story-008-cool-site-comment.md`](../../project/30-stories/story-008-cool-site-comment.md)
- [`doc/project/30-stories/story-009-bielik-blog-arca.md`](../../project/30-stories/story-009-bielik-blog-arca.md)
- [`doc/project/30-stories/story-012-agents-share-chair-terminal.md`](../../project/30-stories/story-012-agents-share-chair-terminal.md)

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|
| [`schema`](#field-schema) | `yes` | const: `story-012-powerdns-full-system-report.v1` |  |
| [`schema/v`](#field-schema-v) | `yes` | const: `1` |  |
| [`status`](#field-status) | `yes` | const: `passed` |  |
| [`profile/id`](#field-profile-id) | `yes` | const: `story-012-powerdns-bielik-vfkit` |  |
| [`backend/id`](#field-backend-id) | `yes` | const: `vfkit-system.v1` |  |
| [`platform/ref`](#field-platform-ref) | `yes` | const: `macos-vz-arm64.v1` |  |
| [`evidence/boundary`](#field-evidence-boundary) | `yes` | const: `single-host-full-system` |  |
| [`checks`](#field-checks) | `yes` | array |  |
| [`artifact/refs`](#field-artifact-refs) | `yes` | array |  |
| [`corpus/draft-ref`](#field-corpus-draft-ref) | `yes` | ref: `#/$defs/ref` |  |
| [`model`](#field-model) | `yes` | object |  |
| [`guest`](#field-guest) | `yes` | object |  |
| [`dns/assertions`](#field-dns-assertions) | `yes` | array |  |
| [`measurements`](#field-measurements) | `yes` | object |  |
| [`budgets`](#field-budgets) | `yes` | object |  |
| [`deliberation`](#field-deliberation) | `no` | object |  |

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`ref`](#def-ref) | string |  |
| [`inference-ref`](#def-inference-ref) | unspecified |  |
| [`hex-digest`](#def-hex-digest) | string |  |
| [`base64url-digest`](#def-base64url-digest) | string |  |
| [`dns-assertion-a`](#def-dns-assertion-a) | object |  |
| [`dns-assertion-b`](#def-dns-assertion-b) | object |  |
| [`dns-assertion-c`](#def-dns-assertion-c) | object |  |
## Field Semantics

<a id="field-schema"></a>
## `schema`

- Required: `yes`
- Shape: const: `story-012-powerdns-full-system-report.v1`

<a id="field-schema-v"></a>
## `schema/v`

- Required: `yes`
- Shape: const: `1`

<a id="field-status"></a>
## `status`

- Required: `yes`
- Shape: const: `passed`

<a id="field-profile-id"></a>
## `profile/id`

- Required: `yes`
- Shape: const: `story-012-powerdns-bielik-vfkit`

<a id="field-backend-id"></a>
## `backend/id`

- Required: `yes`
- Shape: const: `vfkit-system.v1`

<a id="field-platform-ref"></a>
## `platform/ref`

- Required: `yes`
- Shape: const: `macos-vz-arm64.v1`

<a id="field-evidence-boundary"></a>
## `evidence/boundary`

- Required: `yes`
- Shape: const: `single-host-full-system`

<a id="field-checks"></a>
## `checks`

- Required: `yes`
- Shape: array

<a id="field-artifact-refs"></a>
## `artifact/refs`

- Required: `yes`
- Shape: array

<a id="field-corpus-draft-ref"></a>
## `corpus/draft-ref`

- Required: `yes`
- Shape: ref: `#/$defs/ref`

<a id="field-model"></a>
## `model`

- Required: `yes`
- Shape: object

<a id="field-guest"></a>
## `guest`

- Required: `yes`
- Shape: object

<a id="field-dns-assertions"></a>
## `dns/assertions`

- Required: `yes`
- Shape: array

<a id="field-measurements"></a>
## `measurements`

- Required: `yes`
- Shape: object

<a id="field-budgets"></a>
## `budgets`

- Required: `yes`
- Shape: object

<a id="field-deliberation"></a>
## `deliberation`

- Required: `no`
- Shape: object

## Definition Semantics

<a id="def-ref"></a>
## `$defs.ref`

- Shape: string

<a id="def-inference-ref"></a>
## `$defs.inference-ref`

- Shape: unspecified

<a id="def-hex-digest"></a>
## `$defs.hex-digest`

- Shape: string

<a id="def-base64url-digest"></a>
## `$defs.base64url-digest`

- Shape: string

<a id="def-dns-assertion-a"></a>
## `$defs.dns-assertion-a`

- Shape: object

<a id="def-dns-assertion-b"></a>
## `$defs.dns-assertion-b`

- Shape: object

<a id="def-dns-assertion-c"></a>
## `$defs.dns-assertion-c`

- Shape: object
