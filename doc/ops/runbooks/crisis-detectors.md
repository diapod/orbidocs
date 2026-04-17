# Crisis Detectors Runbook

This runbook defines the operator contract for Memarium crisis detector facts.
Detectors write append-only facts in the crisis space; `memarium.crisis_status`
derives the active view, and `memarium.crisis_resolve` records an operator
force-resolution fact. A force-resolution does not erase the detection history.

## Current Implementation Contract

The reference Node daemon currently enables all four detectors by default when
Memarium is enabled. `memarium.crisis_status` reports disabled detector ids from
runtime config so operators can distinguish "quiet because healthy" from "quiet
because disabled".

Default detector timing:

- evaluation tick: `60s`,
- jitter max: `10s`,
- status lookback: `90d`,
- lifecycle broadcast capacity: `256`,
- sealer locked threshold: `21600s` (`6h`),
- zero usable peers threshold: `1800s` (`30m`),
- Seed Directory poll failure threshold: `900s` (`15m`),
- storage anomaly quiet window: `86400s` (`24h`).

Resolution semantics:

- detector facts are edge-triggered: one active `crisis-detected` fact per
  detector condition,
- automatic recovery writes `crisis-resolved` with
  `resolution_kind = "autodetected"`,
- operator force-resolution writes `crisis-resolved` with the
  `operator-forced` tag and preserves the operator reason,
- after operator force-resolution, the detector suppresses re-detection while
  the same condition remains continuously true; it may detect again only after
  a full true -> false -> true condition cycle.

## sealer-operator-unavailable

What it means: the operator-controlled sealer master path is unavailable long
enough that normal encrypted writes or opens may be blocked.

Current trigger: the daemon observes the active sealer master version as
unknown or locked for at least
`memarium.crisis.detectors.sealer_locked_prolonged.locked_threshold_seconds`
(`21600s` by default). The detector does not directly inspect unlock attempts,
rate-limit counters, or envelope corruption; those are operator diagnostics.

Operator must check: sealer master initialization, unlock state, rate-limit
state, host filesystem permissions, and whether recent `sealer.unlock` attempts
failed because of a bad passphrase or corrupted envelope.

Force-resolve only when: the sealer can seal and open a fresh test payload under
the expected operator key path, and the failure window is understood.

Do not force-resolve when: the active master is still locked, uninitialized, or
the unlock failure reason is unknown.

## federation-unavailable

What it means: the node has observed zero usable peers and repeated Seed
Directory poll failures beyond the configured threshold.

Current trigger: both conditions must hold at the same time:

- usable peer count is zero for at least
  `memarium.crisis.detectors.federation_unavailable.peer_zero_threshold_seconds`
  (`1800s` by default),
- Seed Directory revocation-source polling has reported an error for at least
  `memarium.crisis.detectors.federation_unavailable.seed_directory_fail_threshold_seconds`
  (`900s` by default).

Operator must check: local network reachability, seed endpoints, peer quality
scorecards, dialer backoff state, local clock skew, and whether the node is
intentionally isolated.

Force-resolve only when: at least one expected federation path is reachable or
the isolation is an intentional maintenance condition.

Do not force-resolve when: the node is still unable to reach seeds and peers
needed for the operator's active safety or recovery posture.

## revocation-freshness-stale

What it means: the revocation view is older than the accepted freshness budget,
so passport authorization may be operating on stale revocation knowledge.

Current trigger: the detector evaluates the aggregate revocation view freshness
against the daemon's Memarium revocation freshness budget. Per-source errors
are diagnostics for the operator; they are not themselves the trigger unless
they make the aggregate view stale beyond budget.

Operator must check: local revocation source diagnostics, static-file refresh
errors, Seed Directory revocation feed health, and the configured staleness
budget.

Force-resolve only when: revocation diagnostics show a fresh successful check
or the stale source has been explicitly removed from the active trust path.

Do not force-resolve when: the latest successful revocation check is still older
than the budget or any configured source is failing in a way that changes trust
semantics.

## storage-integrity-warning

What it means: a storage integrity anomaly was observed in a path that can
affect Memarium, capability, sealer, or lifecycle evidence.

Current trigger: the storage runtime reports at least one anomaly within
`memarium.crisis.detectors.storage_integrity_warning.anomaly_quiet_window_seconds`
(`86400s` by default), after removing configured `ignored_kinds`.

Operator must check: storage audit logs, filesystem health, recent power-loss or
disk errors, JSONL/projector consistency, and whether any append-only stream
needs repair from a trusted backup.

Force-resolve only when: the storage audit has been inspected and the affected
stream is either repaired or proven not to affect the current decision surface.

Do not force-resolve when: the storage audit has not been read. This detector is
not an alert to dismiss; it is a demand to inspect the evidence base.
