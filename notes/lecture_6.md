# Utilities and Decision Theory

- Decision theory, in its simplest form, deals with choosing among actions
  based on the desirability of their immediate outcomes.
- In essence, an agent could work according to the principle of **maximum
  expected utility**. The expected utility is given according to
  @eq:expected_utility. And the agent would then take the action, $a$, which
  would result in the highest expected utility given some evidence $\mathbf{e}$.

$$
\sum_s P(R(a) = s | a, \mathbf{e}) U(s)
$${#eq:expected_utility}

- In some sense, this is the most desirable any agent could do and could
  therefore be considered the foundation of AI. Even though the relation looks
  simple, it is essentially intractable for complex problems. The
  conditional probability requires a complete causal model of the environment,
  and $U$ requires perfect knowledge of the implications of one's actions which
  requires searching and planning.

## Utility Theory and Preferences

- To be able to make a decision, one needs to determine which outcome is better
  than another. We have to formalize the notion of **preferences**.

- Here, we use the notion of a **lottery** to indicate some undeterminable
  outcome based on a set of outcomes and their probabilities.

- We require the preferences to obey some constrains:

  - **Orderability**: Exactly one of $(A \succ B), (B \succ A), or (A \sim B)$
  holds.
  
  - **Transitivity**: $(A \succ B) \land (B \succ C) \implies (A \succ C)$

  - **Continuity**: An agent should be indifferent to an outcome that is the
    average of two, or one that equals the average:
    $A \succ B \succ C \implies \exists_p : [p, A; 1-p, C] \sim B$

  - **Substutability**: ==I'm not quite sure what this is supposed to mean other
    than:== Indefferences and preferences hold regardless of the complexity of a
    lottery: $A \sim B \implies [p, A; 1-p, C] \sim [p, B; 1-p, C]$.

  - **Monotonicity**: If a certain event has a higher probability of a
    preferred outcome, then the agent should choose that event:
    $A \succ B \implies (p > q \iff [p, A; 1-p, B] \succ [q, A; 1-q, B])$

  - **Decomposability**: Compound lotteries can be reduced to simpler ones. Also
    called the **no fun in gambling rule** as it shows that two consecutive
    lotteries can be compressed into a single equivalent lottery. ==The book
    contains a large mathematical relation, but I think the condition makes
    plenty of sense without it==.

- Assembling our set of preferences, we can, from it determine a utility
  function. At least, we can approximate our known preferences with a utility
  function.

### Utility Functions

- Utilty functons are, for the most part, normalized. That is, there is a worst,
  and best-case scenario based on the values $0$ and $1$ respectively.
- If we consider a utility function $U(s)$ where $s$ is a particular state, then
  we can determine the expected utility by @eq:expected_utility which can then
  be used to determine the action with the highest expected utility (see
  @eq:max_utility). ==Which I absolutely refuse to call the _rational way to
  choose the best action_==

$$
a^* = max_a \mathbb{E}[U(a|\mathbf{e})]
$${#eq:max_utility}

- Here, a problem is that our estimation will be biased. We will not be able to
  perfectly model the underlying utility function and the error in each
  'episode'[^1] will therefore be non-zero. Still, if we assume this to be zero,
  i.e. **nonbiased**, the error will have some distribution based on the action
  taken.
- As we are 'optimistic' and take the best possible action, there is a tendency
  to pick samples with higher utility. Therefore, the error will slowly increase
  as the number of 'episodes' pass. This is called the **optimizer's curse**.
- The optimizer's curse can be avoided by using an explicit probability model
  for the approximated expected utility given the true expected utility: $P(
  \mathbb{E}U | \widehat{\mathbb{E}U} )$.

[^1]: With episode, I mean successive estimations. They use the word episodic in
    the book, and I think using it this way makes sense. The book uses the
    variable $k$ to express this.

### The Value of Information

- Becuase, generally, not all information is available to an agent, it has to
  'ask questions' to its environment to gain more information.
- Therefore, one might wonder how to determine the best question to ask. One
  approach is consider the **value of perfect information** (see
  @eq:value_of_perfect_information).

$$
V P I_{\mathrm{e}}(E_{j})=\left(\sum_{k}P(E_{j}=e_{j k}|\mathbf{e})\ E U(\alpha_{e j k}|\mathbf{e},E_{j}=e_{j k})\right)-E U(\alpha|\mathbf{e})
$${#eq:value_of_perfect_information}

- In plain language, the formula (see @eq:value_of_perfect_information) works as
  follows: "if we know our expected utility at certain moment in time given some
  evidence, $\mathbf{e}$, what would some (possible) evidence(s), $E_j$, on
  average contribute to the expected utility?".
