# Introduction

Not much needs to be said regarding the introduction of probabilistic machine
learning. However, one rule deserves special attention and a quick reminder is
therefore in place.

## Bayes' Rule

In short, Bayes' rule allows us to 'update' our current belief, i.e. the
probability of a state, $S$ given some possible actions, $a_0, \ldots, a_i$,
$P(S | a_0, \ldots, a_i)$, using observations. That is, by 'flipping' the
dependence, actions given the next state instead of the next state given
actions, we can relate actions and states.

Let me clarify by first providing Bayes' rule:

$$
P(S|a) = \frac{P(a|S)P(S)}{P(a)}
$$ {#eq:bayes-rule}

Instead of using $a$ for action, we can also use $o$ for observation. When
considering a classification example, this makes more sense. In that case, we
would like to 'learn' how certain attributes relate to classes (the states in
the previous example). This is done by making 'observations' in the form of
features and, since we already have the label, this results in _an observation
given some label_. Using Bayes' theorem (see @eq:bayes-rule), we can thus
determine the _label given some features_.

The example of actions and states applies when considering an **agent** acting
in an unfamiliar environment. Here, we consider $P(S)$ our **prior** belief, or
the belief before (prior to) the observation, and 'update' the belief by
considering our belief given some observations, $P(S|o)$.

This implies somehow that $P(o|S)$ is easier to determine than its inverse.
[...]
