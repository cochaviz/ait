# Quantification of Objectives and Reward Hacking

- AI can be viewed as a model that is optimized according to a function that
  reflects 'intelligent behavior. (Backpropagation, Reinforcement Learning,
  Genetic Algorithms, etc.)

## Fitness and Quantification

- This 'fitness' has to be adjusted based on the problem at hand. For example,
  - Sum of squared errors for regression.
  - _Cross-entropy_ for classification (i.e. difference between two probability
    distributions).

- Because we want to compute how our 'current' model compares to previous ones,
  we want the function to be quantifiable. That is, quantifiable in both input
  and output. ==(not quite the right use of quantifiable)==

- Quantifying is hard because you embed assumptions about the problem you are
  trying to solve in the data you supply to the algorithm, and _the algorithm is
  only as good as the data you supply it with_.

## Reward Hacking

- **Reward Hacking**, or the **Inner Alignment** problem:

> The objective function admits some clever “easy” solution that formally
> maximizes it but perverts the spirit of the designer’s intent (i.e. the
> objective function can be “gamed”)

- **Goodhart's law** puts this behavior into perspective and reminds us that
  this is similar to human behavior:

> Any observed statistical regularity will tend to collapse once pressure is
> placed upon it for control purposes.
>
> When a measure becomes a target, is ceases to be a good measure.

- Several reasons could exist for an agent not displaying the expected/desired
  behavior that are associated with reward hacking:

  1. The objective function is wrong.
  2. The objective function is not properly evaluated (implementation or other
     practical issue besides the mathematical basis).
  3. The objective is 'correct', but the agent could not learn the 'correct
     behavior'.

- All these concepts might be responsible for agents acting out. It's important
  to consider that _someone_ has to then take responsibility for these problems.

## Meaningful Human Control over AI

> _Humans_ not computers and their algorithms should ultimately remain in
> control of, and thus be _morally responsible_ for relevant decisions.

- One approach to ensure humans can still bear responsibility to these systems,
  is to consider the **tracking** and **tracing** conditions:

> **Tracking**: The human-AI system (consisting of human agents, AI agents,
> infrastructures, etc.) should be able to track the relevant moral reasons of
> the relevant human agent(s) and be responsive to these reasons.
>
> **Tracing**: The system’s behavior should be traceable to at least one human in the
> system design history or use context who can appreciate the capabilities
> of the system and their own role as morally responsible.

- Tracking and tracing can be further quantified into the following properties:
  1. The system has an explicit moral operational design domain (moral-ODD) and
     adheres to its boundaries.
  2. Humans and AI agents have appropriate and mutually compatible
     representations of each other and the task context.
  3. The agents’ responsibility should be commensurate with their ability and
     authority to control the system.
