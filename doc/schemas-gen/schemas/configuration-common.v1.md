# P091 Configuration Common Contract v1

Source schema: [`doc/schemas/configuration-common.v1.schema.json`](../../schemas/configuration-common.v1.schema.json)

## Governing Basis

- [`doc/project/40-proposals/091-file-backed-configuration-and-explainable-composition.md`](../../project/40-proposals/091-file-backed-configuration-and-explainable-composition.md)

## Project Lineage

## Fields

| Field | Required | Shape | Description |
|---|---|---|---|

## Definitions

| Definition | Shape | Description |
|---|---|---|
| [`text`](#def-text) | string |  |
| [`reason`](#def-reason) | string |  |
| [`digest`](#def-digest) | string |  |
| [`counter`](#def-counter) | integer |  |
| [`jsonPointer`](#def-jsonpointer) | string |  |
| [`scopeKind`](#def-scopekind) | enum: `node`, `component`, `workflow`, `invocation` |  |
| [`view`](#def-view) | enum: `declared`, `resolved`, `active` |  |
| [`detailMode`](#def-detailmode) | enum: `values-only`, `with-derivation` |  |
| [`sourceClass`](#def-sourceclass) | enum: `compiled-default`, `distribution-default`, `module-declaration`, `node-declaration`, `operator-common`, `operator-component`, `workflow-overlay`, `invocation-override`, `admitted-constraint`, `legacy-operator` |  |
| [`contributorRole`](#def-contributorrole) | enum: `decisive`, `shadowed`, `equal`, `rejected` |  |
| [`applicationMode`](#def-applicationmode) | enum: `live-reload`, `component-reload`, `component-restart`, `node-restart`, `approval-required`, `provision-only` |  |
| [`applicationState`](#def-applicationstate) | enum: `provisioned`, `active`, `pending-reload`, `pending-restart`, `approval-required`, `application-rejected`, `descriptor-invalidated`, `unknown` |  |
| [`refusalCode`](#def-refusalcode) | enum: `missing-key`, `denied`, `unavailable-context`, `host-unavailable`, `unsupported-contract`, `invalid-source`, `source-conflict`, `descriptor-conflict`, `constraint-conflict`, `resolution-unavailable`, `invalid-target`, `limit-exceeded`, `persistence-failed`, `recovery-required` |  |
| [`refusal`](#def-refusal) | object |  |
| [`settingAddress`](#def-settingaddress) | object |  |
| [`descriptorAdmission`](#def-descriptoradmission) | unspecified |  |
| [`sourcePresence`](#def-sourcepresence) | unspecified |  |
| [`sourceSlot`](#def-sourceslot) | object |  |
| [`sourceBinding`](#def-sourcebinding) | object |  |
| [`settingDescriptor`](#def-settingdescriptor) | object |  |
| [`resolutionInputs`](#def-resolutioninputs) | object |  |
| [`resolution`](#def-resolution) | object |  |
| [`derivationContributor`](#def-derivationcontributor) | object |  |
| [`derivationEntry`](#def-derivationentry) | object |  |
| [`derivationDetail`](#def-derivationdetail) | object |  |
| [`derivationCarrier`](#def-derivationcarrier) | unspecified |  |
| [`derivation`](#def-derivation) | object |  |
| [`describeRequest`](#def-describerequest) | object |  |
| [`describeResponse`](#def-describeresponse) | object |  |
| [`disclosure`](#def-disclosure) | object |  |
| [`explainRequest`](#def-explainrequest) | object |  |
| [`explainResult`](#def-explainresult) | object |  |
| [`explainResponse`](#def-explainresponse) | object |  |
| [`declarationEdit`](#def-declarationedit) | unspecified |  |
| [`predictedImpact`](#def-predictedimpact) | object |  |
| [`changePlan`](#def-changeplan) | object |  |
| [`changePlanRequest`](#def-changeplanrequest) | object |  |
| [`changePlanResponse`](#def-changeplanresponse) | object |  |
| [`changeCommitRequest`](#def-changecommitrequest) | object |  |
| [`commitReceipt`](#def-commitreceipt) | object |  |
| [`changeCommitResponse`](#def-changecommitresponse) | object |  |
| [`activationApplyRequest`](#def-activationapplyrequest) | object |  |
| [`activationReceipt`](#def-activationreceipt) | object |  |
| [`activationApplyResponse`](#def-activationapplyresponse) | object |  |
| [`launchSnapshot`](#def-launchsnapshot) | object |  |
| [`offlineAdmission`](#def-offlineadmission) | unspecified |  |
| [`offlineRequest`](#def-offlinerequest) | object |  |
| [`offlineResponse`](#def-offlineresponse) | object |  |
## Field Semantics

## Definition Semantics

<a id="def-text"></a>
## `$defs.text`

- Shape: string

<a id="def-reason"></a>
## `$defs.reason`

- Shape: string

<a id="def-digest"></a>
## `$defs.digest`

- Shape: string

<a id="def-counter"></a>
## `$defs.counter`

- Shape: integer

<a id="def-jsonpointer"></a>
## `$defs.jsonPointer`

- Shape: string

<a id="def-scopekind"></a>
## `$defs.scopeKind`

- Shape: enum: `node`, `component`, `workflow`, `invocation`

<a id="def-view"></a>
## `$defs.view`

- Shape: enum: `declared`, `resolved`, `active`

<a id="def-detailmode"></a>
## `$defs.detailMode`

- Shape: enum: `values-only`, `with-derivation`

<a id="def-sourceclass"></a>
## `$defs.sourceClass`

- Shape: enum: `compiled-default`, `distribution-default`, `module-declaration`, `node-declaration`, `operator-common`, `operator-component`, `workflow-overlay`, `invocation-override`, `admitted-constraint`, `legacy-operator`

<a id="def-contributorrole"></a>
## `$defs.contributorRole`

- Shape: enum: `decisive`, `shadowed`, `equal`, `rejected`

<a id="def-applicationmode"></a>
## `$defs.applicationMode`

- Shape: enum: `live-reload`, `component-reload`, `component-restart`, `node-restart`, `approval-required`, `provision-only`

<a id="def-applicationstate"></a>
## `$defs.applicationState`

- Shape: enum: `provisioned`, `active`, `pending-reload`, `pending-restart`, `approval-required`, `application-rejected`, `descriptor-invalidated`, `unknown`

<a id="def-refusalcode"></a>
## `$defs.refusalCode`

- Shape: enum: `missing-key`, `denied`, `unavailable-context`, `host-unavailable`, `unsupported-contract`, `invalid-source`, `source-conflict`, `descriptor-conflict`, `constraint-conflict`, `resolution-unavailable`, `invalid-target`, `limit-exceeded`, `persistence-failed`, `recovery-required`

<a id="def-refusal"></a>
## `$defs.refusal`

- Shape: object

<a id="def-settingaddress"></a>
## `$defs.settingAddress`

- Shape: object

<a id="def-descriptoradmission"></a>
## `$defs.descriptorAdmission`

- Shape: unspecified

<a id="def-sourcepresence"></a>
## `$defs.sourcePresence`

- Shape: unspecified

<a id="def-sourceslot"></a>
## `$defs.sourceSlot`

- Shape: object

<a id="def-sourcebinding"></a>
## `$defs.sourceBinding`

- Shape: object

<a id="def-settingdescriptor"></a>
## `$defs.settingDescriptor`

- Shape: object

<a id="def-resolutioninputs"></a>
## `$defs.resolutionInputs`

- Shape: object

<a id="def-resolution"></a>
## `$defs.resolution`

- Shape: object

<a id="def-derivationcontributor"></a>
## `$defs.derivationContributor`

- Shape: object

<a id="def-derivationentry"></a>
## `$defs.derivationEntry`

- Shape: object

<a id="def-derivationdetail"></a>
## `$defs.derivationDetail`

- Shape: object

<a id="def-derivationcarrier"></a>
## `$defs.derivationCarrier`

- Shape: unspecified

<a id="def-derivation"></a>
## `$defs.derivation`

- Shape: object

<a id="def-describerequest"></a>
## `$defs.describeRequest`

- Shape: object

<a id="def-describeresponse"></a>
## `$defs.describeResponse`

- Shape: object

<a id="def-disclosure"></a>
## `$defs.disclosure`

- Shape: object

<a id="def-explainrequest"></a>
## `$defs.explainRequest`

- Shape: object

<a id="def-explainresult"></a>
## `$defs.explainResult`

- Shape: object

<a id="def-explainresponse"></a>
## `$defs.explainResponse`

- Shape: object

<a id="def-declarationedit"></a>
## `$defs.declarationEdit`

- Shape: unspecified

<a id="def-predictedimpact"></a>
## `$defs.predictedImpact`

- Shape: object

<a id="def-changeplan"></a>
## `$defs.changePlan`

- Shape: object

<a id="def-changeplanrequest"></a>
## `$defs.changePlanRequest`

- Shape: object

<a id="def-changeplanresponse"></a>
## `$defs.changePlanResponse`

- Shape: object

<a id="def-changecommitrequest"></a>
## `$defs.changeCommitRequest`

- Shape: object

<a id="def-commitreceipt"></a>
## `$defs.commitReceipt`

- Shape: object

<a id="def-changecommitresponse"></a>
## `$defs.changeCommitResponse`

- Shape: object

<a id="def-activationapplyrequest"></a>
## `$defs.activationApplyRequest`

- Shape: object

<a id="def-activationreceipt"></a>
## `$defs.activationReceipt`

- Shape: object

<a id="def-activationapplyresponse"></a>
## `$defs.activationApplyResponse`

- Shape: object

<a id="def-launchsnapshot"></a>
## `$defs.launchSnapshot`

- Shape: object

<a id="def-offlineadmission"></a>
## `$defs.offlineAdmission`

- Shape: unspecified

<a id="def-offlinerequest"></a>
## `$defs.offlineRequest`

- Shape: object

<a id="def-offlineresponse"></a>
## `$defs.offlineResponse`

- Shape: object
