# Orbiplex Anon

`Orbiplex Anon` could be a separate privacy and relay module for Node-attached traffic that wants stronger sender obscurity than the default transport path provides.

It should not be treated as the same thing as `Orbiplex Whisper`.

- `Whisper` is about social-signal exchange semantics, rumor lifecycle, thresholding, and association bootstrap.
- `Anon` is about optional transport and forwarding privacy, including relay choice, derived nyms, hop-limits, and onion-like routing profiles.

This separation matters because not every private signal needs onion-style transport, and not every anonymous relay mechanism should inherit the semantics of social rumor exchange.

## Candidate role

`Anon` could provide:

- relay-capability discovery,
- optional onion-style wrapping across a bounded number of forwarding nodes,
- derived forwarding nyms with limited hop TTL,
- transport profiles such as:
  - `direct`
  - `relayed`
  - `onion-relayed`
- delivery policy support such as:
  - `soft-fail` if `Anon` is unavailable,
  - `hard-fail` if the caller requires anonymous relay and refuses plain transport.

## Relationship to Whisper

A future `Whisper` signal may carry transport intent like:

- anonymity requested,
- anonymity required,
- maximum hop count,
- acceptable relay classes,
- forwarding budget.

`Whisper` would not implement onion routing itself. Instead it would expose routing intent or routing policy, and the Node would satisfy that policy through `Anon` if the module is installed and suitable relay peers are available.

One likely use from Whisper is:

- `soft-fail`: anonymous relay preferred, but plain or trusted-peer forwarding still allowed if `Anon` is unavailable,
- `hard-fail`: anonymous relay required, and the rumor must not be sent if the requested relay posture cannot be satisfied.

This keeps layers cleaner:

- `Whisper` decides what privacy posture is desired for a rumor,
- `Anon` decides how to realize that posture at the transport level,
- Node decides whether the requested routing profile is satisfiable and whether to send, degrade, or reject.

## Candidate constraints

- bounded hop count,
- bounded derived-nym depth,
- replay resistance,
- no silent downgrade from required anonymous relay to plain transport,
- explicit audit trace of routing policy choice without exposing the route itself.

## Why keep it separate

Keeping `Anon` separate from `Whisper` makes it reusable for other Node-attached modules later:

- sensitive operator escalation,
- protected archival handoff,
- witness requests,
- federation-private routing experiments.

Promote to: proposal when relay discovery, hop semantics, derived nym rules, and transport failure policy are specified.
