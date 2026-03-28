# Orbiplex Monus

`Orbiplex Monus` could be a Node-attached wellbeing and tension-observation module whose job is to notice signals important to a given user, weigh them over time, and optionally formulate candidate Whisper rumors from them.

The point is not diagnosis, hidden behavioral scoring, or paternalistic automation. The point is to help the user notice meaningful patterns early enough that they can decide whether a bounded social signal should be published through `Whisper`.

## Candidate role

`Monus` could aggregate and weigh local signals such as:

- repeated descriptions of pain, fear, overload, or perceived injustice in user conversations,
- recurring conflicts, friction, anxiety, or destabilization themes visible in local memory,
- Sensorium-originated signals relevant to wellbeing when a Node has an attached `Orbiplex Sensorium`,
- temporal patterns where multiple weak concerns align into something that no longer looks accidental or isolated.

Examples include:

- a Whisper draft prepared from accelerated speech, stress markers, and repeated mention of the same institution and event class, where a wearable or voice-oriented Sensorium contributes part of the local signal basis,
- a local emergency-help trigger when personal Sensorium reports cardiac arrest or comparable collapse and the user remains inactive across available communication channels.

## Relationship to Whisper

`Monus` should not replace `Whisper`.

- `Monus` is about local observation, weighing, and preparation of candidate concern signals.
- `Whisper` is about publication, bounded exchange, correlation, and association bootstrap.

One healthy boundary is:

- `Monus` produces a local draft or recommendation,
- `Whisper` turns that into a bounded outgoing artifact if policy allows it.
- when publication happens, `whisper-signal/source/class` should be able to say
  that the signal was `monus-derived`, instead of collapsing it into a generic
  local derivation bucket.

When Sensorium materially shaped the draft, a more explicit source class such as
`monus-sensorium-derived` is healthier than erasing that distinction.

## Boundary with local help mode

Not every serious Sensorium-originated signal should become a Whisper rumor.

Acute personal emergencies should prefer local help or escalation flows first. For
example:

- if personal Sensorium reports likely cardiac arrest,
- and the user remains inactive across available communication channels,

then the immediate default should be a local help-mode or emergency-assistance path,
not public or federated Whisper publication.

Whisper becomes relevant only when the problem is plausibly systemic, distributed,
or correlation-worthy across multiple nodes.

## Candidate operating modes

### 1. Semi-automatic mode

`Monus` prepares a rumor draft and puts it in front of the user in UI.

The user may then:

- accept it,
- edit it,
- discuss it with the Node model,
- or reject it.

This is likely the safest near-term baseline.

### 2. Automatic mode

`Monus` may publish through `Whisper` without interactive approval, but only when:

- the user explicitly opted into that mode,
- the policy profile allows it,
- the draft remains bounded and auditable,
- and rumor/publication budgets still allow it.

This mode should be treated as stricter and more exceptional than the semi-automatic one.

## Candidate constraints

- `Monus` should remain local-first.
- It should not publish by default merely because it can infer distress.
- It should keep an audit trace of why a candidate rumor was formed.
- It should preserve user override and opt-out.
- It should not hide the difference between user-authored rumor and monitor-derived rumor.

## Why this may matter

Some harms do not first appear as one clear event. They appear as repeated weak signals:

- worsening wellbeing,
- recurring conflict patterns,
- mounting fear,
- repeated service refusal,
- or a cluster of apparently minor anomalies.

`Monus` could help surface those patterns early enough that `Whisper` can correlate them with similar signals from elsewhere.

Promote to: proposal when local signal weighting, user consent modes, Monus-to-Whisper handoff, and Sensorium-assisted inputs are specified.
