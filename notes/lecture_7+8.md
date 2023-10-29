# Planning Under Transition Uncertainty

- As we have seen, and will see, Markov models can be categorized according to
  the presence of hidden states, and whether the transitions can be chosen or
  not (see @tbl:markov_models).

| _Markov Models_      | **Chosen transitions**    | **No chosen transitions**                          |
|----------------------|---------------------------|----------------------------------------------------|
| **No hidden states** | Markov Chain              | Markov Decision Process (MDP)                      |
| **Hidden states**    | Hidden Markov Model (HMM) | Partially Observable Markov Decision Process (MDP) |

: Classification of different Markov models {#tbl:markov_models}

## Sequential Decision Problems - Markov Decision Problems

- **Markov Decision Process (MPD)**: A fully observable, stochastic environment
  with a Markovian transition model, $P(s' | s, a)$ (only the current state has
  some relation with the next state), and additive rewards, according to a
  function $R(s)$.

- A set of actions might not provide a good solution as the problem is
  _stochastic_. The agent might take a wrong turn (note that the transition
  model is probabilistic), thus we give it a **policy**, $\pi$, that takes a
  state, $s$, and returns the next state: $s' = \pi(s)$.

- The optimal solution to an MPD is a policy, $\pi^*$, that returns the highest
  expected utility (remember, we cannot guarantee a sequence of events since
  they are stochastic).

- It's important to realize that this policy is learned and the quality of the
  policy (i.e. how well would it work in a real scenario) heavily depends on the
  quality of the reward function $R$.

### Utilities over Time

- An important consideration is whether there is a limited, finite, or infinite
  number of steps in which we can perform our (continued) task, i.e. a
  **finite-** or **infinite-horizon**. Consider the following.

- When studying the day before an exam, it is probably not very rewarding to
  spend a lot of time exactly what you're doing. You're better off learning past
  exams by hard until you fall asleep. If you would have kept up with the homework
  and studied incrementally, you can take your time to understand exactly what
  you're doing and the course will feel more rewarding (if you actually care about
  the subject, that is).

- If you would have an infinite amount of time, it does not matter what you do
  since you always have enough time to do anything.

- Finite horizon optimal solutions are **non-stationary**, while optimal
  solutions to infinite horizon problems are **stationary**.

- Of course, we could choose to simply add the utilities of the states in the
  sequence. Logically, however, it also makes sense to give lower reward to
  states further in the future. If we assume **stationary preferences**, our
  preferences stay the same over time, this implies exactly the two states
  above:

  1. **Additive Rewards**: $U_h([s_0, s_1, \ldots]) = R(s_0) + R(s_1) + \ldots$

  2. **Discounted Rewards**: $U_h([s_0, s_1, \dots]) = \gamma^0R(s_0) +
     \gamma^1R(s_1) + \ldots$

- Discounted rewards therefore encapsulate additive rewards since they are
  equivalent for $\gamma = 1$.

- There are some considerations to be made when considering infinite horizons
  without terminal states, as it seems the reward could approach infinity. To
  this, there are three solutions:

  1. _Use discounted rewards_. Rewards are bound when they are discounted
     according to the following relation: $U(\mathbf{s})=R_{max}/(1-\gamma)$,
     where $R_{max}$ is the maximum reward.
  2. _The assumption sucks and you have terminal states_. This, however, only
     holds if your agent is guaranteed to reach a terminal state at some point
     in time.
  3. _Take the average reward over a length of time_.

### Optimal Policies and the Utilities of States

- Now, for actually determining the optimal policy, we use an algorithm called
  **value iteration**.

- To explain this, we should first consider the **Bellman equation** (see
  @eq:bellman)

  $$
  U(s) = R(s) + \gamma \max_{a \in A(s)} \sum_{s'}P(s' | s,a)U(s')
  $${#eq:bellman}

- This rephrases the utility of a policy from _summation of rewards_ to the
  _utility of the current state plus the probabilistically weighted utility of
  the neighbor states_.

- To then discover the utilities of all $n$ states, we guess their initial
  probability and apply the **Bellman update** (see @eq:bellman_update) to
  iteratively approach the correct answer (see @fig:bellman_update).

  $$
  U_{i+1}(s) \leftarrow \gamma \max_{a \in A(s)} \sum_{s'} P(s'|s, a)U_i(s')
  $${#eq:bellman_update}

![(a) Graph showing the evolution of the utilities of selected states using
value iteration. (b) The number of value iterations $k$ required to guarantee an
error of at most $\epsilon = c \cdot R_{max}$, for different values of c, as a
function of the discount factor \gamma.](images/image.png){#fig:bellman_update}

## Partially Observable MDPs

- Instead of assuming al the information is available to us (i.e. we can
  directly observe which state we're in), we consider when this is not the case.
  Thus, we have **Partially Observable MDP**.

- Here, we add a **sensor model**, $P(e|s)$ similar to the HMM, and a **belief
  state**, $b(s)$. Then we can determine the next belief state, $b'$ as follows,

  $$
  b'(s')=\alpha\,P(e\,|\,s')\sum_{s}\,P(s'\,|\,s,a)\,b(s)
  $$

> The fundamental insight required to understand POMDPs is this: _the optimal
> action depends only on the agent’s current belief state_. That is, the optimal
> policy can be described by a mapping $\pi^*(b)$ from belief states to actions.

- Since we do not know the current state, it would also no make sense to
  base the optimal policy on the true current state.

- In conclusion, it means that an update on each time step would look as follows:

  1. Given the current belief state, $b$, execute the action $a=\pi^*(b)$.
  2. Receive the perceived evidence $e$.
  3. Set the current belief state to $\mathrm{Forward}(b, a, e)$.
  4. Go back to _1_.

- Now, the thing is that we don't know what evidence we will actually receive.
  Therefore, we should estimate what the possible evidence might be. Or, at
  least, have a method of determining how reliable our update method might be.

- Let's first return to the probability of finding evidence, $e$, with what we
  do know,

  $$
  \begin{align}
  P(e|a,b) &=\sum_{s'}P(e|a,s',b)P(s'|a,b) \\
           &=\sum_{s'}P(e|s')P(s'|a,b) \\
           &=\sum_{s'}P(e|s')\sum_{s}P(s'|s,a)b(s)
  \end{align}
  $$

- Then, we can determine the probability of finding that particular next belief,
  $b'$, from the $\rm{Forward}$ function.

  $$
  \begin{align}
  P(b'\mid b,a) &= P(b'\mid a,b) = \sum_{e}P(b'\mid e,a,b)P(e\mid a,b) \\
                &= \sum_{e}P(b'\mid e,a,b)\sum_{s'}P(e\mid s')\sum_{s}P(s'\mid s,a)b(s)
  \end{align}
  $${#eq:belief_transition}

- Furthermore, we can define a reward function for beliefs:
  $$
  \rho(b) = \sum_s b(s) R(s)
  $${#eq:belief_reward}

- In conclusion, if we consider @eq:belief_transition the **belief transition**
  and @eq:belief_reward the **belief reward**, we have essentially reduced the
  POMDP to a normal MDP.

### ==Value Iteration for POMDPs==

- Value iteration can be described by the following function:

  $$
  \alpha_{p}(s)=R(s)+\gamma\left(\sum_{s^{\prime}}P(s^{\prime}|\,s,a)\sum_{e}P(e|\,s^{\prime})\alpha_{p,e}(s^{\prime})\right)
  $${#eq:value_iteration}

## Monte Carlo Tree Search

- An important observation is that up until one we have tried to determine the
  optimal policy performing any action, a so-called **offline planning**
  strategy.

- **Monte Carlo Tree Search (MCTS)** is an example of an **online planning**
  strategy and attempts to determine the best action to take by considering the
  transition function inferred by the action, $R(a) = s$, as a tree and stochastically
  exploring it.

- Long story short, MCTS works according to the following algorithm starting
  from the root of the tree, i.e. the current state:

  1. **Selection:** Select a child node using a selection strategy until a node
     with unexplored children is reached or a terminal state is encountered.

  2. **Expansion:** If the selected node has unexplored children (i.e., possible
     moves from the current state), expand the tree by adding one or more child
     nodes corresponding to these unexplored moves.

  3. **Simulation (Rollout):** Simulate a random or heuristic playout using a
     **rollout policy** from the newly added node (or from the selected node if
     it was already a terminal state) until a terminal state is reached. This is
     essentially a random sampling phase and represents a possible outcome of
     the game from the current position.
  
  4. **Backpropagation:** Update the statistics of the nodes along the path from
     the newly expanded or simulated node to the root. This typically involves
     updating the visit count and the total accumulated reward (or score) of the
     nodes.
  
  5. **Repeat:** Repeat steps 1 to 4 for a fixed number of iterations or until a
     time limit is reached.

  6. **Action Selection:** After the specified number of iterations, or when a
     computational budget is exhausted, choose the best move from the root node
     based on the node visit counts or other relevant statistics. This is
     usually the child node with the highest visit count, indicating it has been
     explored the most and has shown promising results.

- The rollout policy has an incredible effect on the performance of the MCTS
  algorithm. One could consider a MCTS algorithm to be essentially a _policy
  improvement operator_. That is, you give it a policy, and MCTS makes it better
  by applying additional search.

- Pros and cons:
  - ($+$) Rapidly zooms in on promising regions
  - ($+$) Can be used to improve policies
  - ($+$) Basis of many successful applications
  - ($-$) Needle in the hay-stack problems
  - ($-$) Problems with high branching factor
