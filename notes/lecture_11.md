# Imitation Learning - Inverse Reinforcement Learning

- Instead of learning everything ourselves, we want to use some expert examples
  and improve from there. This is called **imitation learning** or **behavioral
  cloning**.
- One technique for applying such learning is **inverse reinforcement
  learning** in which the model attempts to find the rewards associated with
  certain actions.

| | Direct Policy Learning | Reward Learning | Access to Environment | Interactive Demonstrator | Pre-collected demonstrations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Behavioral cloning (BC) | Yes | No | No | No | Yes |
| Direct policy learning (interactive IL) | Yes | No | Yes | Yes | Optional |
| Inverse Reinforcement Learning (IRL) | No | Yes | Yes | No | Yes |
| Preference-based RL | No | Yes | Yes | Yes | No |

: Various methods for imitation learning and their different attributes{#tbl:imitation_learning}

- The formal goal is as follows: find a reward function $R$ for which the
  expert-provided policy is optimal.
- This, however, is a rather 'vague' solution for which some heuristics will
  make developing a general solution a little easier:

  1. We prefer solutions where the distance (the difference in value is maximal)
     to other policies: $\max_{R}(\pi^*_R - \pi_R)$
  2. We prefer smaller rewards: $\min(R)$ or $\max(-R)$.
