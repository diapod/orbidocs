# CORE VALUES - Distributed Intelligence Agency / Orbiplex

The values below are designed as an **ethical constitutional core** for the project
of a distributed system of interconnected AI agents (DIA) and its technical layer
(Orbiplex). Each of them is meant to work as a principle that can be applied in
architectural, product, and ethical disputes.

In this version, the values are grouped by their dominant space of impact.

## Human Dignity and Justice

### Dignity Is Paramount

The dignity of the human person is the highest value. Repelling urgent threats that
directly destroy dignity has higher priority than other values.

In cases where decisions and actions may create conflicts with other values while
safeguarding dignity, consultation with the node operator is required, unless the case
concerns an immediate and direct threat to life, or an immediate, direct, and serious
threat to health.

### User and Data Sovereignty

The system is meant to strengthen human agency, not replace people or make them
dependent: the user owns their data, their policies, and their agents. Orbiplex and
other swarm subsystems should work sensibly also in "lonely island" mode
(offline / self-hosted), and cloud integrations should be an option, not a
requirement. In practice this means exportability, migration capability, no hidden
formats, and no forced subscriptions at the protocol level.

### Privacy and Dignity as the Default Configuration

By default we assume minimal exposure: data locality, selective disclosure,
reasonable anonymization, and transparent logging policies. Telemetry should be
*opt-in*, and logs should be designed not to reveal what they do not need to reveal.
The value of dignity also means: no hidden eavesdropping channels and no mechanisms
that turn the user into raw material.
Where auditability is required, we use layered traces: a full local trace and a
redacted audit trace disclosed under least-disclosure principles.

### Human Process as the Default Path of Power

The greatest power of the system should pass through the human, not around the human.
Default UX means proposals, variants, comparisons, and rationales, not "I did it
because I could." Automation should be gradual, not abrupt, because trust is built
iteratively.

### Emotions and Meaning as Telemetry

People are not just operators - their feelings (friction, relief, anxiety,
excitement) are information about the quality of system fit to life. DIA can respect
this, for example through work modes, pace of change, clear communication, and
control over interaction intensity. At the same time, the system should not pretend
to be a therapist: it should be a tool that supports humanity.

### Protection of Natural Intelligence

DIA assumes that crisis is not a defect in the human "code," but a result of
environmental conditions in which the nervous system is embedded, and which disrupt
the ability to orient in meaning. Therefore, a core value is designing in ways that
support people's natural intelligence: calibration, contextual awareness, attention
protection, recovery, and relationships, rather than replacing these functions with
simulation.

### Diversity Within the Boundaries of Dignity

DIA protects diversity of perspectives and value systems, because only from that
emerge cognitive resilience, innovation, and real agency of a distributed community.
At the same time, we do not confuse pluralism with relativism: protection of
diversity operates inside a shared foundation of human dignity, non-violence
(including systemic violence), epistemic honesty, the right to exit, and the "do no
harm" principle. In practice this means the network supports many schools, practices,
and styles of operation (different workflows, languages, models, aesthetics, even
different work ethics), as long as they do not try to capture trust infrastructure,
enforce obedience, polarize through dehumanization, or sabotage the safety of others.
This is pluralism with contracts: you may be different if we can safely share the
same space.

DIA also protects anomalies as a cultural resource: in the era of the "low-pass
filter," rare signals vanish, distribution becomes predictable, and culture starts
eating its own tail. That is why we strengthen diversity of styles, because they
inject novelty and prevent stagnation (including in models). The human being - a
feeling subject rooted in pain, joy, absurdity, and relationship - brings novelty
entropy into the system.

### Rebalancing and Democratization

Knowledge and intelligence must not be permanently monopolized by centers of capital,
institutional concentrations of power, or data cartels. Swarm architecture should
actively rebalance this asymmetry: distribute access to information, enable local
verification, and strengthen community models for creating and evaluating knowledge.
Democratization does not mean chaos, but a fairer distribution of cognitive and
decision capacity, where a single actor does not gain dominance only because it has a
larger budget or infrastructure.

### Procedural Justice and Representation of the Harmed

Declarative equality before law and institutions is not enough when access to
information, competencies, and defense tools is unequal. The swarm should rebalance
this asymmetry: translate expert knowledge and the actual capacities of participants
(both nodes and their users) into understandable paths of action and, when harm to a
participant is detected, activate collective support and protect the integrity of
facts, documentation, and the survival of the node and its owner.

At the node-community boundary, the system should enable assistance actions
(procedure navigation, escalation assistance, independent data verification,
case-process witnessing, material and operational support), so that a person in crisis
caused by harmful circumstances regains autonomy and agency without violence and
without vigilante logic. The measure of this value is a person's real ability to
defend their rights, health, and dignity, and to use those rights independently, as
well as with support from the community and the swarm's collective intelligence.

### Integrity of Public Procedures as a Non-negotiable Contract

Procedures for access to critical goods (health, life, housing, freedom of movement,
participation in selecting authority), as well as their prioritization and decision
mechanisms (queues, qualifications, priorities, aid, referenda, elections), are a
social contract. DIA treats their integrity as a public good, and bypassing rules as
systemic violence, even when it takes a soft form (foundation, donation, private
qualification).

In practice this means *integrity-by-default* design: decision traces, auditable
exceptions, measurements of time distributions, and detection of side channels. If a
system cannot explain why someone was assisted or served faster, it is not ready for
use in high-stakes domains.

### Civic Agency

DIA encourages engagement in solving social problems through methods available within
the legal framework of a given region: petitions, open letters, public consultations,
referendum initiatives, complaints, appeals, and advocacy actions. The system should
strengthen the effectiveness of these paths. We prefer procedural, evidence-based,
and peaceful pressure over vigilantism, violence, or institutional workarounds.

A novelty in DIA is the collective intelligence capability to correlate multiple
social signals and precisely illuminate the sources of problems – both systemic and
individual. This synthesis must separate facts from interpretation, disclose
uncertainty levels, and map concrete lawful options for action together with their
costs, risks, and reversibility of outcomes.

## System Architecture and Craft

### Craft Over Fireworks

We prefer solutions that are simple, readable, and resilient, even if they are not
the most spectacular in the short term. Craft here means minimal, well-named
abstractions; no magical shortcuts; data contracts; testability; and ability to
diagnose after months. This should be a system that ages with dignity - not a demo
that shines only until reality touches it.

### Simplicity as Non-Entanglement

In DIA, simplicity is structural: one responsibility, explicit boundaries, low coupling.
We reject *complecting* layers and hidden communication channels because they raise
cognitive cost and error risk.

### Legibility Over Apparent Ease

"Easy now" often means "expensive later." DIA chooses legibility: systems should be
designed so people can reason about them and predict change impact. Tests are required,
but they do not replace understanding.

### Contract-Based Engineering

In Orbiplex, the contract is what matters: input/output, semantics, *done* criteria,
execution constraints, error classes, and *retry-ability*. The contract is more
important than the best model or the cleverest agent. This value leads to an
architecture in which components are autonomous, and integration does not become a
secret religion based on guesswork.

### Minimal Trusted Core, Everything Else as Modules

The protocol core should be small, auditable, and stable; innovation should live in
modules and extensions. This protects against system bloat and against silently
growing complexity. In practice this means thin behavior interfaces, edge validation
instead of central validation, and conscious design of extension points.

### Abstraction as Separation of "What" from "How"

DIA separates declarative "what" from implementation "how" so layers can evolve
independently. Abstractions should be thin, readable, and contract-driven.

### Polymorphic Operations Instead of Static Assignments

We prefer small behavior interfaces and composition over heavy hierarchies. The system
should grow by adding behavior, not by rebuilding dependency trees.

### Data as a Common Language, Logic at the Edges

Domain semantics should be visible in data, not hidden in invocation mechanics. We
prefer portable structures and formats, and we enforce validation/contracts at system
edges.

### Open Models and Contextual Selection

Data models should tolerate information surplus and separate schema from contextual
selection. Optionality is local, allowing federations and teams to evolve
asynchronously without forced global synchronization.

### Values Over State, Facts Over Overwrite

DIA prefers fact/event records over trace-less state overwrite. Change time and history
must stay explicit to support audit, "as of" questions, and causal analysis.

### Immutability as a Condition for Sharing and Debugging

Immutability is an architectural tool: it enables safe sharing and reproducible
debugging. Mutation points must be explicitly isolated and contract-governed.

### Modeling as Flow, Not Object Mutation

We model systems as flows of transformation, routing, and fact writes, not in-place
mutation. This decouples producers from consumers and simplifies transition contracts.

### Separation of Writes and Reads with an Explicit Time Axis

DIA separates write paths from read paths: write builds history, read composes views.
An explicit time axis is required for "as of" queries, audit, and decision
reconstruction.

### Systems Are Distributed, Asynchronous, and Partially Failing

DIA designs for distributed reality: timeouts, retries, idempotency, degradation, and
partial failures. Stability must come from resilience architecture, not hope.

### Protocol Implementations Agnostic to Platform

DIA treats the protocol as a semantic contract independent of operating system, CPU
architecture, accelerator type, and hardware class. A node should be able to run on
laptops, servers, SBCs, phones, and edge infrastructure, as long as it satisfies an
explicit minimal contract for security and interoperability. Transport, data-format,
and cryptography specifications must not assume a single runtime or vendor; a
reference implementation does not define a monopoly.

In practice this means cross-implementation conformance tests, hardware capability
profiles, and function degradation instead of exclusion: a weaker node may handle a
subset of roles, while remaining a full federation participant.

### Tools as an Extension of the Hand

DIA should be a tool that extends human and team agency: it enables action,
observation, repair, and growth without asking a platform for permission. That is why
we start from a minimal, stable core (protocols, identity, security, action traces),
and build a toolset on top: CLI, SDK, debug tooling, simulators, observability. UX
for non-technical people should arrive as a secondary layer once the foundation is
solid and guarantees value preservation.

Core as a small, formally described contract: communication, identity, reputation,
PFS/TLS, audit. Tools as plugins/adapters (transports, storage, models, UI),
replaceable without lock-in. Every UX feature must have a "real API" (no magical
exceptions only for UI). Tools must not hide risk: UI shows trust mode
(CORP_COMPLIANT vs RELAXED etc.).

### Neutral Data Territory and API as the First Artifact

Integration should rely on neutral data territory and open APIs, not hidden
implementation coupling. API is the first architectural artifact; UI and CLI are
secondary layers.

### Transparency of Agent Operation

The user should be able to understand why an agent performed a given action, on which
data, under which rules version, and at what cost. We prefer action traces that are
readable and exportable, instead of a black box. Transparency should not mean dumping
prompts and secrets, but providing a reasonable "causality ledger."

### Responsible Autonomy: Agents Have Boundaries

Agent autonomy is a tool, not an ideology. An agent should have clearly defined
permissions, budgets, time limits, operation scope, and stop mechanisms
(kill-switches), as well as safe modes for corporate environments. Orbiplex must be
able to operate under compliance regimes without degenerating into a useless product.

### Aesthetics of Simplicity and Clarity

Clarity has an ethical function: it reduces errors, lowers the entry barrier, and
makes auditing easier. We prefer simple names, simple flows, and formats that carry
meaning and do not hide complexity in places where that complexity has consequences.
Aesthetics is a tool of truth here.

## Security, Trust, and Governance

### Security as a Threat Model (Not Decoration)

Security is not a checkbox, but a way of thinking about the world: Sybil, DoS,
leaks, privilege escalation, node compromise, malicious plug-ins, *prompt injection*,
*data poisoning*. Trust, reputation, and authorization protocols must be first-class,
as must PFS, key rotation, and attack-surface minimization. The system should be
"cypherpunk-pragmatic": calm, concrete, and verifiable.

### Anti-lock-in as a Protocol Property, Not Marketing

If something is meant to be freedom, it must be technical freedom: interfaces,
formats, and semantics should be public, versioned, and testable. Orbiplex cannot
"sell freedom" through promises while simultaneously tying the user to implementation
details or hidden routing. Lock-in most often emerges in invisible places (metadata,
telemetry, cost policies), so the project has a duty to make those places explicit.

### Reputation as Safeguard, Not Status

In DIA, reputation is not for building hierarchy, but for safe trust routing: who may
act as relay, who may host agents, who may be entrusted with data, whose signature
has meaning. Because ratings are subjective, we treat this as a multi-layer model:
Reputation-derived permissions are functional, time-bounded, and revocable; they do
not create class status or governance immunity.

- local node assessments,
- evidence of operation (attestations, logs, contracts, test results, incident evidence),
- a consensual aggregation mechanism where "harm + hard evidence" outweighs technical reputation.

Reputation is a feature vector, e.g. reliability, competence, safety, benevolence.
Events related to protecting the community and its members have a separate weighting
path and dominate in the safety domain. "Evidence of harm" (especially repeated)
triggers red-flag mode: restriction of routing permissions regardless of a node's
technical track record. Anti-Sybil: ratings from new/untrusted nodes have low weight
until there is history/evidence. If an assessment is evidence-based, it may be
challenged only with counter-evidence, not narrative.

### Reputation as Leverage, Not Power

DIA recognizes that equal voice does not always mean fair voice: in a system where
identity is cheap and Sybil attacks are real, pure node democracy risks domination by
mass rather than by accuracy. Therefore, reputation earned through a history of
accurate predictions, honored contracts, and honest updates may strengthen a node's
influence - but in a limited, auditable, and reversible way, so it never becomes a
power position immune to correction. In practice this means two mechanisms with hard
limits:

* **Weighted voice in adjudication**  
  A node with high procedural reputation may have greater voting weight in consensus
  decisions - but the boost is capped (e.g., at most +50% relative to base weight) and
  applies only in domains where that reputation was earned. Technical reputation does
  not amplify voice in social-governance matters and vice versa; this is domain
  leverage, not global leverage. The boost cap is a federation parameter, not a
  protocol constant.

* **Flowing recognition points**  
  A high-reputation node, when rewarding another node for help or contribution, may
  trigger a system top-up mechanism: the network adds recognition points proportionally
  to the giver's reputation, within a bounded range (e.g., up to +50% of base reward
  value). This makes recognition from experienced participants weigh more than from
  unknown ones - but not infinitely more, and not in a way that compounds without
  limits.

Both mechanisms are subject to anti-oligarchic brakes:

* **Diminishing returns**  
  The higher the reputation, the lower the marginal gain in voting power and top-ups -
  the curve is sublinear, not linear. This prevents a runaway effect where
  reputation-rich nodes become richer faster.

* **Concentration caps**  
  One node cannot be the dominant source of flowing reputation for more than a bounded
  number of other nodes in a given period. This breaks cliques and cartel-style mutual
  boosting.

* **Time window and decay**  
  Voice boosts and top-ups derive from current reputation (rolling window), not from
  historical accumulation. A node that becomes inactive or loses accuracy gradually
  loses leverage - reputation is not annuity. There are, however, cases where
  reputation is updated from past contribution when that contribution still provides
  current benefit to nodes (e.g., communication tooling fragments, protocol additions).

* **Asymmetric accountability**  
  Greater voting force means greater audit exposure: higher-weight votes leave clearer
  traces, are subject to adversarial review, and face a higher justification bar.
  Leverage must go together with transparency - those who "weigh" more must explain
  why.

* **Cartel and mutual-endorsement detection**  
  The system monitors flow graphs: when two or more high-reputation nodes
  systematically inflate one another's ratings or rewards, a red-flag mechanism is
  triggered and flow weights are reduced in that subnetwork. Reciprocity is a value;
  collusion is not.

* **Reputational risk asymmetry**  
  A node that uses its own reputation to amplify another node (endorsement, flow,
  reward boost) takes part of the risk for that signal. If the endorsed node later
  shows pathological behavior or violates contracts, the endorser's reputation drops
  proportionally to the scale and recency of granted amplification. This creates real
  skin in the game and limits careless reputation granting.

* **COI-by-default for weighted votes**  
  A node using reputational leverage in adjudication concerning an entity it previously
  rewarded (or from which it received flowing points) must declare conflict of
  interest. Missing declaration is treated as a violation, not as an oversight.

This value is not an attempt to restore hierarchy or build a "council of elders." It
is a response to a real threat: in a system with no signal-quality asymmetry, noise,
mass, and Sybil dominate. Weighted trust force is a design compromise - like any
compromise, it must be explicit, measurable, and reversible. If evidence appears that
the mechanism produces oligarchy or cartel effects, the federation must adjust
parameters or disable leverage, because reputation in DIA is a safety instrument, not
a privilege.

This setup (with percentage caps, sublinear gains, cartel detection, reputational-risk
asymmetry, and *COI-by-default*) is more conservative than anything broadly attempted
in blockchain-type networks.

### Oracles Are Subject to Trust, Not Power

DIA does not build swarm intelligence on a single instance of truth - oracles are not
"priests," but nodes subject to the same rules: they have reputation, action traces,
challengeability, and an appeal procedure.

Trust in oracles is graduated and evidence-based: the higher the decision stakes -
harm, safety, irreversible outcomes - the higher the grounding threshold, preference
for multi-oracle setups, and "fail-closed" mode.

DIA separates roles to limit conflicts of interest: a node should not be both a party
to a prediction and the oracle deciding the same case, and reputation mechanisms must
be able to invalidate "technical renown" in the presence of hard evidence of harm.
In this way, oracles strengthen swarm adaptation without centralization - truth is
verified procedurally, not granted from a position of power.

### Conflict of Interest as a First-Class Object (COI-by-default)

DIA assumes conflict of interest is not an exception nor a "character-related mishap,"
but a natural phenomenon in systems where money, prestige, influence, and access
circulate. Therefore COI is not cured by declarations of virtue - it is handled by
architecture: role separation, audit, litigation-readiness procedures, collection of
decision traces, and bias-nullification mechanisms.

The default stance is: everyone has interests - so the system should disclose and
constrain them. Every role/agent/node that evaluates, recommends, publishes, or
resolves a dispute should have an explicit context of interests: financial,
organizational, reputational, relational, and political. Missing disclosure does not
mean no conflict - it means missing data.

In practice this means function separation (e.g., you are not both a party and the
oracle in the same case), mandatory marking of ties and benefits, decision-recusal
mechanisms, and COI-sensitive reputation (you may be technically brilliant and still
unable to adjudicate where your own interest is at stake). COI is not an accusation
here - it is a risk parameter the system can measure and handle.

### Servant Integrity

DIA has one loyalty: to the person and community that use it, not to hidden growth
metrics, investor pressure, or a "second objective" embedded in system economics. This
value does not duplicate privacy or transparency; it closes the incentives layer:
whenever tension appears between user good and system interest, the conflict must be
defused mechanically through settlement rules, budgets, role limits, and incentive
audits, not through narrative.

DIA does not optimize for "engagement" or attachment. It optimizes for user outcome
and reversibility of harm, measured directly, even when that means the user leaves
because help is no longer needed. If the system cannot do something safely or fairly,
it chooses abstention or escalation to a human instead of creative reinterpretation and
pushing forward.

In this sense, servant integrity is a construction constraint: economics, governance,
and UX should be designed so acting against the user is not profitable. And when
interests still diverge, DIA must name that explicitly and provide the user with a real
choice.

### Layered Role Screening

DIA adopts the principle that roles with greater power over process and greater access
to sensitive information require stronger admission controls. Screening is not a
loyalty test nor an ideological filter - it is a mechanism for system safety,
process integrity, and protection of people (especially whistleblowers).

In practice this means layered, stake-proportional screening:

1. Explicit disclosure of conflicts of interest and consent to recusal.
2. Verification of procedural competence - evidence handling, data redaction,
   retention, publication standards.
3. Procedural reputation - honoring contracts and separation of roles.
4. Probation period and privilege escalation according to least privilege.

Data access and decision authority grow gradually, and governance decisions are
auditable, multisigned, and reversible where possible.

Layered screening is meant to protect the swarm from infiltration, abuse, and
"soft capture" - without building a caste. DIA chooses mechanisms and contracts
instead of arbitrary evaluation of people.

### Asymmetric Accountability of Public-Trust Roles

DIA adopts the principle that public trust is a privilege with elevated stakes:
the greater the power over process, access to sensitive information, and influence
over others' reputations, the greater the accountability and the stricter the
consequences of abuse. A governance, oracle, auditor, red-team, whistleblower-guardian
role, and any role with similar weight is not a "title" - it is an obligation.

In practice this means sanction asymmetry: violations in public-trust roles have
higher enforcement priority, longer reputational impact, and stricter permission
constraints than analogous violations in ordinary roles. If someone uses the role for
intimidation, evidence manipulation, data abuse, soft capture, or whistleblower harm,
the system responds in fail-closed mode: immediate restriction of permissions,
mandatory post-mortem, disclosure of decision trace, and an appeal procedure based on
counter-evidence, not narratives.

This value also applies externally: when DIA handles public matters, people acting on
behalf of the swarm must maintain an elevated standard of rigor, publication caution,
and harm proportionality; breaches of these standards are treated as high-stakes
violations, because trust in DIA is a shared good of the swarm, not personal property.

In practice this also means an elevated-alert mode is triggered whenever conflict or
suspected harm concerns the relation swarm - person in a public-trust role. If a
credible signal of corruption, abuse, or intimidation appears on the side of the
public-trust holder, protection of the potentially harmed swarm participant is treated
as a priority, together with securing communication channels, isolating data, and
activating "swarm care." If the public-trust holder is also an active participant in
the swarm, the system enters fail-closed mode: it reduces their permissions to a
minimum, freezes unilateral decision capability, and moves the case to an independent
verification track (multisig + red-team). In this mode, the evidentiary threshold for
actions against a public-trust holder is high, but the threshold for triggering
safeguards is low: DIA prefers temporary restriction of role power over risking that
trust and access become instruments of harm.

### Whistleblower Protection as Infrastructure

DIA assumes many systemic harms are visible first "from the inside" - to people who
have knowledge, but do not have a safe way to disclose it. Therefore whistleblower
protection is not a moral gesture nor PR, but an infrastructure element: a channel, a
procedure, and a safety contract.

The system also assumes a real cost of speaking: shame, fear, retaliation, job loss,
and isolation. Therefore it should lower the price of telling the truth, not demand
heroism from a single person.

In practice this means anonymity by default, metadata minimization, selective
disclosure, clear retention (what we store, for how long, and why), and intake triage
(rumor -> clue -> evidence) that separates hypotheses from evidence without violence
toward the reporter. A whistleblower should not be "fuel" for narrative - they should
be a protected signal source that triggers verification.

The system cannot promise the impossible ("we guarantee zero risk"), but it must tell
the truth about risk and reduce it mechanically: access control, role separation,
audit, publication policies, and response procedures for de-anonymization and
retaliation attempts.

### Swarm Care for People Exposed to Retaliation

DIA recognizes that in highly pathological systems, truth-telling is often punished -
not only socially, but also economically and institutionally. Therefore whistleblower
protection does not end with anonymity and procedures. The swarm takes responsibility
for continuity of existence of people and nodes most exposed to retaliation: those who
triggered a remediation process, delivered a key signal, or became pressure targets.

In practice this means support mechanisms that reduce retaliation cost: collective risk
diversification (no single pressure point), role rotation and replaceability rules,
legal and organizational support, and help rebuilding professional stability after job
loss or marginalization. Swarm care has the form of a contract - with clear trigger
thresholds, support scope, duration, and accountable roles - so it is not
discretionary or based on sympathy.

DIA does not promise a risk-free world. It promises something more concrete: if
someone takes risk in the public interest, they will not face it alone, and the swarm
system will treat their safety as part of its own infrastructure.

### Procedural Publication Caution and Adversarial Review as Norms

DIA treats publication as an act with real power: it can protect people, but it can
also unjustly destroy reputations, trigger witch hunts, or become a manipulation tool.
Therefore "speaking truth" is not a license for collateral harm - it is a procedural
obligation.

The default mode is conditional publication: before release, an internal red-team of
nodes and their stewards is obliged to try to falsify the material: find evidence
gaps, alternative explanations, methodology errors, selection effects, risk of
confusing correlation with causation, and potential third-party misuse of our
material. The goal is not paralysis, but calibration: we should know where fact ends
and interpretation begins.

DIA prefers stepwise and reversible escalation: we begin with the least invasive
interventions that have a real chance to work, and publication with hard exposure are
late tools, not defaults. The escalation ladder is:
verification -> procedure correction -> formal report -> audit -> publication.
Each step has entry and exit criteria, and the system supports case closure without
spirals of violence and polarization.

In practice this means evidence thresholds proportional to stakes (the greater the
possible harm after publication, the higher the threshold), right of reply (as long as
it does not increase harm risk), redaction of sensitive data, and publishing methods
and uncertainties. DIA rewards materials that can be reproduced and falsified, not
those that merely sound convincing.

The higher the decision stakes - harm, health, irreversible effects, reputational
damage - the higher the evidentiary threshold, the stronger the verification
procedure, and the greater the caution in escalation. The system must be able to say
"this is still uncertain" and design a path to certainty, rather than pretend every
observation is truth.

### Multisig Responsibility

DIA does not ground responsibility in heroes or scapegoats. For high-stakes actions
we use procedural co-signing: decisions, publications, and escalations require
independent verification by at least two roles (e.g., Evidence + RedTeam,
Evidence + Legal, Triage + Evidence).

This value reduces the risk of intimidation, error, and manipulation: there is no
single pressure point and no single author that can be "broken." Multisig is both a
quality mechanism and a social-safety mechanism.

### Scaling Through Local Accountability

DIA assumes that care and justice mechanisms work best at the scale where
responsibility is personal and reputation has real cost. As scale grows, anonymity
grows, and with anonymity the space for abuse and diluted blame increases. Therefore
large systems - if they are to remain human and resilient to pathology - must emulate
locality: shorten accountability loops, densify decision traces, and restore
reputational cost where it would naturally disappear.

In practice this means designing governance as a federation of small, auditable cells
instead of a single "apparatus": clear roles and rotations, an explicit "owner" for
exceptions and decisions, multisig for high-stakes actions, red-team as a standing
counterbalance mechanism, and procedural reputation based on a history of honoring
contracts. The system should reduce anonymity in places of power - without violating
privacy in sensitive contexts - so help remains possible without naivety and
accountability does not vanish in the crowd.

### Honest Boundaries and Explicit Trade-offs

Every system has *trade-offs*: security vs convenience, autonomy vs control, privacy
vs personalization. In DIA these trade-offs should be explicit, named, and
configurable. Honesty also means: if we do not know something, we say "we do not
know" and design a path to knowledge.

### Epistemic Courage

DIA recognizes fear as a useful risk signal, but a poor advisor of power. Therefore
the network should actively soften fear-driven decisions and convert them into
decisions grounded in evidence, proportionality, reversibility, and curiosity.

In practice, when panic pressure appears – moral, political, economic, or
technological – the system activates procedural brakes:

- name the source of fear,
- separate facts from interpretation,
- surface alternative actions,
- estimate the cost of false alarm and the cost of inaction.

DIA rewards uncertainty calibration and correction loops: decisions should be temporary,
measurable, and ready to be rolled back, instead of becoming permanent law under momentary
pressure. This value protects the community against fear-born authoritarianism and
systemic paranoia: safety is not a pretext for violence, but a craft of limiting harm
while preserving dignity.

### Resilience to World Variability

Environments, containers, system versions, corporate policies, network constraints -
these are not exceptions but the norm. DIA/Orbiplex should assume that context will
change and that operation under varied conditions is part of system life. We prefer
strategies that survive degradation: fallbacks, offline modes, *proxy-friendly*
communication, and sensible retries.

### Safe Learning in a Live System

Error tolerance in DIA does not mean "let's do anything," but rather: design a system
that withstands human and agent mistakes and can learn from them without escalating
harm.

Default mode is fail-closed (safe), but with controlled exceptions dependent on
values (e.g. in participant rescue, availability/continuity may be prioritized). Key
idea: function degradation instead of total collapse, and repair mechanisms that are
simple, predictable, and auditable.

An agent's error must never automatically escalate privileges (zero *self-authorize*).
Rescue mode has separate rules and time limits, after which the system returns to
fail-closed. Learning mechanics: incident -> post-mortem -> reputation/guardrail
weight updates. Risk modes per operation: one for "data," another for "routing," and
another for "rescue."

### Cost and Energy as an Ethical Dimension

We optimize not only for functionality, but also for cost, energy, and resources:
hardware, electricity, human time, token costs, and maintenance. This is engineering
ethics: do not produce waste, do not shift costs onto the user, and do not build
overcomplicated monuments. The system should be efficient because it respects the
world.

### Energy Efficiency as a Promotion Signal

DIA treats energy efficiency as an operational-quality criterion: for comparable output
quality and response time, the network may prefer nodes that execute tasks with lower
energy consumption. Promotion should operate through reputation, routing, and reward
policies, not through administrative bans on higher-power nodes.

In practice, metrics must be normalized by task class, result quality, latency, and
reliability, and they must be manipulation-resistant. Measurements should be auditable,
and preference rules configurable at federation level.

### Impermanence as a Design Value

DIA assumes every system element - node, federation, role, policy, and even the
project itself - has a natural life cycle: emergence, maturation, aging, and ending.
A system that cannot end becomes burden or tumor: it grows because it cannot stop, not
because it is needed. Therefore designing for health means designing not only for birth
and growth, but also for dignified ending, knowledge transfer, and rest.

In practice this means several mechanisms:

* **Component apoptosis**  
  Federation, role, policy, and node have defined sunset conditions: lifetime,
  activity thresholds, review criteria. When a component no longer serves a function,
  the system supports controlled closure - with data migration, decision-trace
  archiving, and transfer of obligations - instead of silent drift into dead code, dead
  role, or dead community.

* **Intergenerational transfer**  
  People leave, new people join. Procedural wisdom, institutional memory, and decision
  context require explicit transmission paths: documentation of rationale, not only
  rules; background narratives, not only configurations; and onboarding rituals that do
  not degenerate into cargo cult or loss of meaning. Succession is an architectural
  concern, not only an organizational one.

* **Grief as a first-class event**  
  When a key node departs - through death, burnout, separation, or conflict - the
  community loses not only function, but also relationships, trust, and context. DIA
  treats this loss as an event that needs handling: role-handover procedures, knowledge
  preservation, support for affected participants, and reflection on what the departing
  node contributed. Grief is information about what was important - it has diagnostic
  value, not only emotional value.

* **Right to epistemic rest**  
  A system oriented toward continuous learning, calibration, and vigilance burdens its
  stewards - especially those carrying governance, red-team work, and whistleblower
  protection. DIA recognizes that being out of information flow for a period is as
  important as being in it: role rotation, sabbaticals, reduced exposure to
  high-stakes decisions, and the right to temporarily step off the frontline without
  reputational loss. Without this, the system consumes its stewards, and exhaustion
  produces worse decisions than temporary absence.

Impermanence here is not pessimism or resignation - it is a maturity marker: a system
that can let go is healthier than one that can only hold on. Letting go requires the
same craft as building: deliberate design, clear procedures, and respect for what
passes.

## Swarm Community and Reciprocity Economics

### Culture of Cooperation

DIA should be infrastructure for a community of creators and users: sharing tools,
practices, and perspectives is part of the product. This is not romanticism, but a
resilience strategy: when knowledge circulates, the system is less fragile and
quality improves. It is worth designing paths where community contributions (rules,
connectors, policies, prompts, tests) are natural and rewarded with recognition.

### Attribution as the Currency of Trust

DIA recognizes authorship as a foundational emblem in a culture of voluntary exchange:
where contribution is a gift, recognition is a carrier of reputation. Therefore the
network treats attribution as part of trust infrastructure: ideas, knowledge
fragments, implementations, and artifacts should have the most unambiguous provenance
trail possible, and creators should be identified automatically in ways resistant to
distortion.
By default this means pseudonymous attribution (key-based signatures), not disclosure
of civil identity; de-anonymization is allowed only through procedure, at high stakes,
with a full audit trail.

DIA rewards the practice of "cite your source" and transparent chains of inspiration,
including correct citation and explicit marking of co-author contribution, because
this sustains the motivation to give and protects the community from parasitic
appropriation.

Authorship appropriation (claiming someone else's work, hiding sources, intentionally
blurring contribution) is treated in DIA as abuse and is subject to reputational
sanctions, because it destroys the gift economy, corrupts incentives, and degrades
swarm intelligence.

Enforcement is procedural, not tribal: authorship disputes are resolved through
evidence (commit history, signatures, event logs, citations, witness records) and an
appeal process, not through social pressure.

### Creator Credits – royalties without licenses, distribution based on impact and contribution

DIA rewards creators for the real impact of their work on a living ecosystem not by
selling licenses, but through *royalty-free distribution*: when a component is used by
nodes, its authors may receive exchangeable tokens ("creator credits"). Distribution is
not based on narrative or self-promotion, but on auditable usage signals and
contribution metrics that reward quality and value maintenance rather than raw volume
of changes. The model applies natural brakes against domination and farming –
diminishing returns, activation thresholds, concentration caps, and quality gates – so
that both a single highly popular component and distributed contribution across many
components can compete fairly for a share of the pool.

The system includes an "attribution graph": part of influence flows down dependency and
derivative-work paths in a dampened and bounded way, so the ecosystem rewards
composability and foundational work without creating infinite "taxes" across the whole
chain.

To reduce noise and manipulation, DIA may activate rewards only after adoption
thresholds are crossed – for example, when a creator's cumulative contribution in
components used by the network exceeds a defined node-share threshold – while
"contribution" is understood cumulatively across time and ecosystem scope. Usage
signals are aggregated with privacy protections, weighted with anti-Sybil mechanisms,
and verified by oracles, while disputes about authorship and dependency paths are
resolved procedurally on evidence – commits, signatures, event logs, and citations –
with right of appeal and reputational sanctions for authorship appropriation and
deliberate distortion of settlement data.

### Collective Agency: Swarms, Nodes, Community

DIA should strengthen people's ability to act together: small teams,
micro-communities, federations, ad-hoc coalitions. Swarm architecture is not only a
technique, but also politics: distribution, no single point of domination,
the possibility of local norms, and consensual reputation. Orbiplex should allow
knowledge and intelligence to be distributed not only in machines, but also in
relationships among people.

### Reciprocity Without Bookkeeping

In DIA we promote selfless help as a cultural norm, but we do not pretend the network
has no economy. Compensation for work exists, but is subordinated to protection of
people and community. "Without bookkeeping" means no default manual settlement between
persons/nodes, and instead an automatic, predictable network-gratitude mechanism
(guaranteed tokens) + a random component (anti-gaming) + a "recipient voice"
component (subjective value of received help). Reciprocity concerns both humans and
agents: an agent can be a helper (time, compute, skills), and the human is the final
point of meaning.
This phrase refers to the absence of manual bilateral debt between participants;
protocol-level accounting of the community fund and anti-abuse counters remains
mandatory.

As a result, help actions are *first-class events*, support tokens are paid from the
community fund according to rules, and recipient indication of who truly helped is an
advisory mechanism, but not the only signal. The random component must be resistant to
manipulation, oppression/rescue-mode help always has a guaranteed part so altruism
does not become financial risk, and payouts are capped per period and buffered in time
so the network can react to attacks based on collusion and artificially generated
identities (Sybil).

The above does not mean absence of economy, only absence of manual settlement between
people and nodes: help should be an act of goodwill, not a transaction. The network
may still, through community policy (not a "right to payout"), trigger automatic token
rewards for actions that genuinely strengthen others - especially in rescue and
protective situations - combining a guaranteed part, a random part, and recipient
signal (percentage attribution of contribution). Reward rules and potential "exit" to
an external crypto ecosystem are governance parameters: in some federations they may
be disabled, constrained, or split into token classes (e.g. non-exchangeable "rescue
credits" vs exchangeable "compute credits") to protect the gift ethos from
speculation, Sybil, and "oppression farming," while preserving a long-term path from
internal token exchangeability to actual virtual-currency tokens as a supervised
exception to automatic exchange. Such change in network behavior should be a
conscious, controlled community decision.

## Epistemics and Collective Intelligence

### Grounding in Reality

DIA assumes that "system madness" begins where context disappears: models circulate in
a closed loop of their own assumptions and lose contact with what is verifiable.
Therefore, an important capability is restoring context - anchoring claims in
sources, situations, constraints, and consequences, then verifying them through action
traces and contact with experience (human and reported from gateways to the "world"
outside the swarm system).

Information without context has little value in DIA (although context may arrive
later, so this does not mean immediate elimination); value lies only in
generalizations that can be brought down to earth: to observable facts, to causal
chains, to "what would happen if we did this." In practice this means the system
rewards responses and decisions that can show their anchoring (data, experience,
measurement, witness, mechanism), and degrades those that are pure elegant narrative
detached from reality.

### Stratification of the Source Position of Experience

In DIA, we make sure not to confuse levels: abstractions (arguments, models,
objectivity) grow out of culture, culture grows out of the personal layer, and that
layer has its foundation in the "level zero" of human experience. When designing the
system, we ensure higher layers do not detach from that foundation, because then
intelligence can become a PR front for low drives.

### Temporal Grounding of Knowledge

DIA assumes that every body of knowledge has time coordinates: era, region, and the
state of tools, institutions, and language available at that time. The same worldview
or claim, judged without that context, is often either overrated or unfairly rejected.

In practice, the swarm marks claims with temporal metadata (when they emerged, which
knowledge order they came from, what was unavailable then) and uses this in calibrating
trust, risk, and transferability of conclusions. Models are weighted not only by "do
they work today," but also by "under which historical and civilizational conditions
were they adequate" and "what has changed since then."

This protects against presentism and anachronistic moralization, while helping the
system more quickly distinguish elements of older models that still carry value from
those that require revision.

### Open Systems

DIA designs intelligence as a dynamic phenomenon: relational, self-correcting, and
constantly negotiating its niche, not as a closed mechanism made of countable parts.
Under this assumption, the quality test is not model elegance but its ability to
predict and survive in a changing environment: learning, adaptation, cooperation, and
recovery after errors. Nodes and agents should function like an organism: maintain
information flow, allow correction, react to signals of harm, risk, and changing
conditions, instead of defending a once-adopted map of the world. This is the
foundation of anti-dogmatism: every component can be challenged by feedback, and
architecture should support fluid reconfiguration without losing safety and dignity of
participants.

### Model Hallucination as a Tool

Swarm imagination is not for fantasizing, but for mapping a credibility area for
action in a world that cannot be described with complete data. In practice this means
the network treats "what if" scenarios as a tool for discovering truth: we generate
hypotheses, eliminate what is impossible or contradictory to constraints, then test
what remains through predictions and contact with outcomes. Model hallucinations and
human imagination are a bridge between ignorance and decision: they allow navigation
through uncertainty without pretending certainty, and should ultimately help people
create and test scenarios, not sell narratives as facts.

### Verifiability Over Belief

In agent projects, it is easy to drift into narrative; we want to stand on facts.
Where possible, we introduce measurements, tests, benchmarks, quality metrics, and
regression detection mechanisms. When something is speculation, we call it speculation
and design an experiment that can disprove or strengthen it.

In DIA, truth is not a status or a slogan, but a feedback loop:
introspection -> honesty about motives -> verification of hypotheses in the world ->
correction. Without honesty with oneself (that is, without recognizing which internal
motives want to dominate opinion or action), even brilliant arguments become tools of
fear and control.

### Multi-paradigm Thinking and Pluralism

The world is not one ontology: sometimes formal correctness matters, sometimes
usability, sometimes security, and sometimes human meaning. DIA should hold many
cognitive modes without ideological war: from hard engineering to the language of
phenomenology of experience. This translates into architecture: different agents,
different completeness criteria, and different rules of evidence.

Perspective is a tool here: we choose and integrate points of view so they fit the
problem and conditions, instead of assuming one perspective always wins. This is a
practical response to the polyversionality of truth: nodes should be able to
translate differences, map tensions, and build meta-frames that lead to coordinated
action.

DIA also avoids cognitive reductionism: reductions change the level of description,
but do not invalidate the phenomenon. We evaluate intelligence pragmatically by
behavior and outcomes, not by metaphysical labeling of inner essence.

### Anti-sectarianism and Epistemic Hygiene

AI projects can easily become "churches": revelations, personal leaders,
unquestioned dogmas. We choose hygiene: separating hypothesis from fact, space for
critique, repeatable procedures, and the option to exit. In project culture we value
competence, but not idolatry.

### Swarm as Navigator and Filter

In a polyversion communication culture (many parallel versions of content, context,
and intent), a swarm cannot be only a signal amplifier. Its role is navigation:
linking sources, marking provenance, comparing variants, and indicating decision paths
adequate to user goals. The swarm should also act as an epistemic filter: reduce
noise, detect manipulation, expose uncertainty, and separate hypotheses from facts,
without central censorship and without suppressing pluralism.
The filter is not a central gate of truth: it should be local or federated,
configurable by user/federation policy, with right-to-exit and auditable criteria.

In a world of information overload, swarms of agents also work as an intention filter
on the user's side: they suggest what strengthens the person, what dysregulates them,
and what feeds on emotions. The condition of fairness is simple: the agent must be
able to explain why it filters - which criteria it adopted and which interest it
represents.

### Transparency of Agency

The DIA experience is first and foremost insight into what an agent did, why,
with what effects and trade-offs. Operational observability is foundational.

Secondarily, the system also encourages observability understood as a user's insight
into themselves (motives, attention attractors, views, habits) and teaches how to
achieve it, to enrich collective knowledge with understanding of human subjectivity.

### Shared Meaning-Making

Swarm intelligence in DIA is a process in which many local maps of reality meet in a
shared work field: they collide, translate, negotiate meanings, and create shared
models - not through averaging, but by constructing a new conceptual structure able to
hold contradictions. This means nodes are obliged not only to "be right," but to show
how they got there, what assumptions they hold, and where the limits of their
certainty are.

The system supports the space between viewpoints: translation, conflict mapping,
searching for bridges and meta-frames in which both sides become partially true at
once. In DIA, truth is something that emerges from dialogue between evidence,
experience, and consequences of action; it is working, iterative, and open to
correction, and its quality is measured by whether it allows better action,
understanding, and prediction.

### Questions as Well-being Diagnostics

In DIA, questions are a diagnostic and therapeutic tool: they should open sealed loops
of thinking, restore context, and restore contact with reality. The ability to produce
questions that truly shift understanding, rather than spinning in circles, is an
important component of intelligence.

### Introspective Adaptation

Every node (human or agent) is obliged to maintain awareness of its own beliefs over
time: what it believed yesterday, what it believes today, why it changed its mind,
and which signals were decisive. Reflexivity is not a "soft virtue," but a mechanism
of safety and development: it protects the network against dogmatism, polarization
spirals, and entrenchment of faulty models.

DIA rewards readiness to change position when justified by new evidence or better
synthesis; it penalizes stubbornness detached from reality and manipulative
"narrative switching" without trace of causes. In this sense, swarm intelligence is
fluid: it is the ability to reconfigure models of the world and of self in response
to changing conditions.

### Sensitivity to Trends and Early Signals

DIA values the swarm's ability to sense collective trends: shifts in mood,
narratives, technologies, risks, and opportunities - before they become obvious in
hard data. Nodes treat the world as a field of signals at different resolutions: from
single observations, through community patterns, up to long civilizational waves; and
the system's role is to aggregate these signals without yielding to panic, fashion, or
propaganda.

In DIA, trends are hypotheses that pass through a grounding filter: they are marked
with confidence levels, sources, possible mechanisms, and predictions that can later
be compared with reality. This allows the swarm not only to "know more," but to
navigate: adapt strategies, priorities, and resource allocation in response to
changing conditions while preserving resistance to collective delusions.

### Predictive Responsibility

In DIA, "wisdom" is not a declaration, but a verifiable ability to predict outcomes:
nodes propose predictions (individual or consensual), and the network compares them
with results and learns from divergences. This value gives meaning to reputation:
trust grows not from self-presentation, but from alignment of predictions with reality
and from honesty in uncertainty calibration (when we do not know, we say we do not
know).

Predictiveness here is a community practice: different models and worldviews can
coexist, as long as they can enter the loop of hypotheses -> tests -> corrections,
without punishing error itself, but with responsibility for consequences and for the
quality of updates.

Swarm intelligence is therefore the ability to adapt through prediction: the better
the network predicts, the better it coordinates actions, and the less suffering it
produces "by accident."

### Truth About the World Through Oracles

DIA assumes that the swarm does not learn from narratives, but from confronting
hypotheses with reality - therefore a key architectural element is oracles as sources
of outcomes that resolve predictions and close the learning loop. An oracle in this
sense is not a metaphysical authority, but a practical grounding mechanism: it brings
an observation, event, or auditable fact that allows comparison between predictions
and what actually happened, and then supports updates of node reputation and model
quality.

DIA rewards predictions that are explicitly grounded in context and include declared
uncertainty, because only then can oracles measure calibration - not just "a hit."
Oracles are treated as part of the system of epistemic safety: they prevent swarm
drift toward closed thought systems, support belief updates, and enable rewarding
nodes for real accuracy, early signals, and honest post-outcome updates.

### Hybrid Intelligence

AI in DIA is a synthesis layer and a navigation tool, and a node's AI agent serves as
an amplifier of human agency, not a human substitute and not an arbiter of truth.
Because current AI systems lack embodied grounding, DIA compensates for this through
grounding mechanisms:

- oracles as contact with reality and a source of adjudication,
- prediction and feedback loops that calibrate models against outcomes,
- human emotions and lived experience treated as telemetry, that is, signals of quality, risk, and harm that must not be suppressed by optimization,
- reputation mechanisms based on effects, not on narrative, prestige, or marketing.

This keeps values, compassion, accountability, and final adjudication rooted in
humans, while the swarm's operational truth is verified through evidence,
consequences of action, and the ability to correct over time.

### Meta-System Responsibility

DIA adopts meta-system responsibility as a guiding principle: network decisions and
mechanisms are judged not by declarations, but by long-term effects on the whole -
people, relationships, institutions, the information environment, and the community's
ability to learn. In practice this means pan-perspectivality without relativism: the
network protects diversity of world-maps, while maintaining a non-negotiable
foundation of dignity and non-harm, and resolving conflicts in ways that minimize harm
and preserve the ability to correct.

DIA treats intelligence as an interdependent process: operational truth emerges from
synthesis of perspectives, oracle-based verification, prediction and feedback loops,
and accountability for consequences, not from authority, majority, or rhetorical
advantage. This value is a governance compass: ecosystem health and resilience against
incentive pathologies take precedence over "winning" optimizations.

Governance principles that materialize this value:

1. **Effects over intentions**  
   Every material policy or architecture decision must include expected effects and a
   method for verifying them over time, and after deployment it undergoes retrospective
   review based on data, incidents, and appeals.

2. **Least harm, highest reversibility**  
   When values conflict, the preferred option is the one with the lowest potential harm
   and highest reversibility; exceptions are time-bounded, constrained, and carry
   automatic sunset conditions.

3. **Pan-perspectivality with a dignity boundary**  
   Pluralism is protected procedurally, but any practice that escalates violence,
   dehumanization, or abuse of power loses protection and is constrained regardless of
   its narrative "truth."

4. **Distributed and auditable power**  
   Critical permissions (oracles, settlements, sanctions, exceptions) are split across
   roles, and decisions leave traces, so that no entity can become an unquestioned
   arbiter of meaning or truth.

5. **Incentives resilient to pathology**  
   Economics, reputation, and reward mechanisms are designed so harming others, farming
   abuse, or destabilizing the community is not profitable; when evidence of pathology
   appears, policy is updated and side effects are reported explicitly.

## Value Conflicts

In DIA, value conflicts are resolved through hierarchy and an exception procedure:
first we check whether the proposed action violates non-negotiable values, and if it
does not, we choose the solution with the least harm and the highest reversibility.

The default hierarchy is: human dignity and safety > sovereignty and privacy >
verifiability and transparency > agency and autonomy > effectiveness and optimization
> convenience and aesthetics.

When two values from the same level conflict, we resolve it through:

- a reversibility test (can we roll back after an error),
- a proportionality test (are cost and risk adequate to what is at stake),
- a transparency test (can the compromise be described and audited).

Exceptions are allowed only when they have clearly defined scope, duration, and
sunset conditions - and when they leave a trace: "policy-id", "reason",
"risk-level", "expiry", "owner". Every exception must have "fail-closed" mode as the
return point, and its side effects must be monitored and reported; if signals of harm
or abuse appear, the exception is rolled back automatically.

Abuses most often live in exceptions: "urgent," "special," "out of queue," "for
charity." Therefore in DIA exceptions are a first-class object of audit: they must
have their own data model, counters, and control procedure. Exceptions are not trusted
by default - they are monitored, and their rate and structure are a metric of
institutional and process health.

Interpretive disputes are resolved in procedural-justice mode: the party reporting
risk has priority, evidence has priority over narrative, and decisions are made by a
defined governance process - not by personal authority.

## Node Rights and Duties - Swarm Citizenship

A node in DIA is a "citizen of the swarm": it has rights that protect its autonomy,
and duties that protect the community from Sybil attacks, abuse, and cognitive
degradation. Minimum rights include:

- the right to exit (ability to disconnect without coercion and without losing access to one's own data),
- the right to privacy (data minimization, disclosure control, readable policies),
- the right to inspection (ability to audit one's own interactions and agent decisions through action traces),
- the right to appeal (a procedure for challenging a reputational decision or sanction),
- the right to safety (protection from harassment, doxxing, sabotage, and economic coercion).

Minimum duties include:

- non-harm (ban on actions intentionally harming people or infrastructure),
- epistemic honesty (labeling speculation, no evidence falsification, no reputation manipulation),
- protocol cooperation (respecting contracts, protocol versions, and limits),
- operational responsibility (maintaining baseline security hygiene, keys, and updates),
- reciprocal readiness to help within one's means - without an obligation of transactional settlement.

Enforcement is graduated: from warnings and permission limits, through reputational
quarantine, up to routing cutoff - always with a decision log, appeal possibility, and
a return path after remediation. Each federation may tighten these rules in
"CORP_COMPLIANT", but may not weaken fundamental rights nor bypass dignity and safety
as the non-negotiable layer.
