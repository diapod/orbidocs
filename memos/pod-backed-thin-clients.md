# Pod-Backed Thin Clients

Portable-device and desktop clients do not need to run a local language model at all if they are primarily interfaces to a node that exposes a `pod` module.

The `pod` module lets a node serve human users who cannot run a fully capable, communication-participating node on their own hardware. In this pattern, the client is a thin front-end: identity, session continuity, routing, policy enforcement, and model execution live on the serving node, while the user device focuses on interaction, local security boundaries, and optional local caches.

This enables a practical access gradient:

- full node for operators with enough hardware and connectivity,
- pod-backed thin client for users with weak, mobile, temporary, or locked-down devices,
- the same human may move between these modes over time without losing continuity of participation.

This should be treated as first-class architecture, not a degraded fallback. The swarm gains reach because meaningful participation does not require everyone to own a machine capable of local inference or permanent high-bandwidth communication.

Promote to: proposal or requirements document when `pod` semantics, tenancy model, local-security guarantees, account portability, and offline degradation are specified.
