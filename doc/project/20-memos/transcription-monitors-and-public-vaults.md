# Transcription Monitors and Public Vaults

The swarm may include nodes that specialize in watching for valuable discussions and
turning them into source transcripts. These nodes are not primary participants in every
debate; they act as cultural monitors and transcription agents.

A transcription-monitor node may join selected channels:

- because its operator configured topic interests, cultural priorities, or quality thresholds,
- because the node itself detects a knowledge gap, weak participation, or a culturally valuable thread,
- or because another node explicitly invites it to observe and preserve the discussion.

Its task is to collect the conversation as a source transcript rather than only as a
summary. The aim is to preserve the raw structure of reasoning, disagreement,
clarification, synthesis, and evidence flow, so later nodes can study not just the
answer but the path by which the answer emerged.

These transcripts should remain attributable and structured:

- bound to the original question/channel id,
- segmented by participant and time,
- annotated with provenance, uncertainty, and redaction markers,
- signed or checkpointed so later tampering is detectable.

The swarm may also include archivist nodes. Archivists advertise willingness to receive
transcript bundles from transcription monitors and store them in public or federation
vaults. Those vaults act as durable cultural memory rather than short-lived chat logs.

This creates a role chain:

- transcription monitors detect and preserve valuable discussions,
- archivists store and expose transcript corpora,
- synthesizer/training nodes consume curated vault material to build specialized models,
- later swarm participants benefit from stronger domain memory and better synthesis.

This should not become indiscriminate logging. Selection, redaction, consent,
visibility scope, and retention policy matter. Sensitive or private channels may forbid
transcription entirely, require explicit consent, or allow only redacted vault export.

An open design question is whether transcript publication should be immediate or staged:

- live mirrored transcript streams,
- delayed archival bundles,
- or curator-approved releases after redaction and quality review.

Promote to: proposal or requirements document when transcript format, consent/redaction
policy, and vault publication mechanics are designed.
