# Swarm Communication Exposure Modes

A user opening communication with the swarm should be able to choose the exposure level of the request instead of treating all requests as equally visible.

A minimal model has three modes:

- `private-to-swarm` - the issue is visible only to the minimum set of nodes, agents, and memory components needed to help. This is the default for sensitive, personal, medical, legal, or security-related matters.
- `federation-local` - the issue is visible within one federation or another bounded local scope. This is useful when context, trust, or shared norms matter more than global reach.
- `public-call-for-help` - the issue is intentionally exposed to the wider swarm in order to attract broad attention, diverse input, urgent support, or rare expertise.

These modes should affect routing, retention, summarization, notification policy, and what kinds of traces may be shared onward.

The user should be able to escalate or de-escalate exposure over time. A request may begin as `private-to-swarm`, move to `federation-local`, and become `public-call-for-help` only if the user consents or a separately defined high-stakes procedure justifies broader exposure.

Promote to: proposal or requirements document when user-facing communication modes, privacy scopes, and assistance routing are designed.
