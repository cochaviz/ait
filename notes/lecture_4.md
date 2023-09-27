# Learning

## Why Learning

1. Some model might not be available. In this case, it can be built up over time
   by some other algorithm. An example would be to train a deep learning model;
   there is no _specific_ version of the model available to the programmers, but
   we can adapt a general model to our specific purposes.

2. ...

3. Not understanding the problem.

## What is learning

While there are many approaches to learning, some of which might be more
useful/correct in certain contexts than others. Here, we focus on **learning as
induction**. How to use induction to learn is then dependent on the technique
that is used to implement some agent.

Thus, while were are not explicitly building a model, we provide information to
some statistical model to then make decisions. It is therefore important to
decided what kind of information we should provide the model for it to make the
right decision. Not only that, we also have to quantify what is the right
decision.

We can split the space of what is the 'right' decision into two philosophies,
the **Idealistic** and **Pragmatic** approach. The idealistic attempts to stay
true to the way the world works, making observations and then using statistical
models to learn. The pragmatic approach, however, simply considers "whatever
improves the performance".

While the idealistic perspective would have great accuracy, the tractability,
however, is at odds. As the world is incredibly complex, the search space for
hypothesis (often denoted as $H$) is also _huge_. Therefore, assumptions often
need to be made, which brings most, if not any, model somewhere in between the
two extremes.

## Formalizing Learning

- Learning in Bayesian Networks can take a couple of forms:
  1. **Bayesian Learning**: Is done by computing the posterior $P(H|o)$ which
     uses the prior $P(h)$ and can be used in a weighted variant (utility) to
     determine the best 'action', $V(a) = \sum_h P(H|d)u(a, h)$
  2. **Maximum Likelihood**: The most likely hypothesis, $h_{ML}$ will be
     $h_{ML} = \argmax_h P(d|h)$. Then we can select and action according to
     $V(a) = u(a, h_{ML})$. It is, however, prone to overfitting.
  3. **Maximum A Posteriori (MAP)**: Which is just the **ML**, but also taking
     into consideration the prior of the hypothesis: $h_{MAP} = \argmax_h P(d|h)P(h)$.
