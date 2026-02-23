# CORE VALUES - Distributed Intelligence Agency / Orbiplex

The values below are designed as an **ethical constitutional core** for the project
of a distributed system of interconnected AI agents (DIA) and its technical layer
(Orbiplex). Each of them is meant to work as a principle that can be applied in
architectural, product, and ethical disputes.

In this version, the values are grouped by their dominant space of impact.

## Human Dignity and Justice

### Dignity Is Paramount

The dignity of the human person is the highest value. Repelling urgent threats that
directly destroy dignity has higher priority than other values. In cases where
decisions and actions may create conflicts with other values while safeguarding
human dignity, continuation of the selected actions requires an explicit decision by
the node operator.

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

## System Architecture and Craft

### Craft Over Fireworks

We prefer solutions that are simple, readable, and resilient, even if they are not
the most spectacular in the short term. Craft here means minimal, well-named
abstractions; no magical shortcuts; data contracts; testability; and ability to
diagnose after months. This should be a system that ages with dignity - not a demo
that shines only until reality touches it.

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

### Honest Boundaries and Explicit Trade-offs

Every system has *trade-offs*: security vs convenience, autonomy vs control, privacy
vs personalization. In DIA these trade-offs should be explicit, named, and
configurable. Honesty also means: if we do not know something, we say "we do not
know" and design a path to knowledge.

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

## Swarm Community and Reciprocity Economics

### Culture of Cooperation

DIA should be infrastructure for a community of creators and users: sharing tools,
practices, and perspectives is part of the product. This is not romanticism, but a
resilience strategy: when knowledge circulates, the system is less fragile and
quality improves. It is worth designing paths where community contributions (rules,
connectors, policies, prompts, tests) are natural and rewarded with recognition.

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
