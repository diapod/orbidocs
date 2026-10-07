# Operator task packs HOWTO

The complete implemented walkthrough lives with its Node owners:
[English HOWTO](https://github.com/diapod/node/blob/master/docs/operations/TASK-PACKS.en.md)
and [Polish HOWTO](https://github.com/diapod/node/blob/master/docs/operations/TASK-PACKS.pl.md).
Its command examples are checked by the actual CLI parser in both languages;
they do not authorize effects when validated.

The procedure covers package inspection, pinned qmail image preparation,
conformance and activation, restrictive local binding choices and profile diffs,
readiness, exact offer approval, one local or queued remote task, HIL per mutation,
verification/destruction evidence, pause/resume, recovery, withdrawal and revocation.
It reuses existing APIs rather than describing candidate commands as available.

Package provenance, local trust and current execution authority remain separate.
Proposal [094](../../project/40-proposals/094-operator-task-packs-for-bounded-problem-solving.md)
owns the bounds and decisions; [Story 013](../../project/30-stories/story-013-qmail-task-pack.md)
owns the qmail reference. The owner-refusal gate preserves historical native and
physical evidence classes and does not adopt the proposal or declare alpha ready.
Known journal capacity and unsupported relay migration recovery are explicit in
the walkthrough, not hidden behind an automatic retry.
