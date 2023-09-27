# Bayesian Networks and Inference

Core to the idea of an intelligent agent is that the agent somehow manages to
solve a task for which the solution is not explicitly embedded into the agent.
If we told the agent explicitly what to do, it would simply be a front for some
deterministic algorithm. The lack of determinism therefore implies the need for
the agent to handle uncertainty. Therefore, we need to be able to formally
represent uncertainty.

More formally, an issue arises when an agent attempts to determine whether it
will be able to complete a task. It might guarantee a certain outcome, _given_
that a whole host of events do, or do not, take place. This just kicks the can
down the road, as we then have to guarantee whether the dependencies for the
result are also satisfied. This leads to something called the **qualification
problem**.

Combining some fundamental intuition about probability and the issue of the
qualification problem, we can look at events as a chain of probabilistic
dependencies. One way of structuring such dependencies is in something called a
**Bayesian Network**.

## Representing Knowledge in an Uncertain Domain

A Bayesian Network is a data structure that encapsulates the full joint
probability distribution in a concise manner. Meaning it is nothing more than a
representation of a (possibly very complex) function. Let's take the example of
a patient having a cavity in their tooth, $P(Cavity)$ which might induce a
toothache and can be observed with a 'catch' (see @fig:cavity-graph).

```{.mermaid #fig:cavity-graph width=50% theme=neutral}
graph TD;
    Cavity-->Toothache;
    Cavity-->Catch;
    Weather;
```

There, we see how one random variable might influence two other random
variables. Furthermore, there is no need for all the nodes to be connected, a
forest is a valid instance of a Bayesian network (the weather is independent of
the cavity).

There is another assumption hidden in this graph, namely that $Toothache$ and
$Catch$ are **conditionally independent** given $Cavity$. Conditional
independence is formalized by the following relation.

$$
P(Catch \land Toothache | Cavity) = P(Catch | Cavity) \land P(Toothache | Cavity)
$$

A formal specification of a Bayesian Network (BN) can be characterized as
follows:

1. Each node corresponds to a random variable, which may be discrete or
   continuous.
2. A set of directed links or arrows connects pairs of nodes. If there is an
   arrow from node $X$ to node $Y$, $X$ is said to be a parent of $Y$. The graph
   has no directed cycles (and hence is a directed acyclic graph, or DAG).
3. Each node $X_i$ has a conditional probability distribution $P(X_i |
   Parents(X_i))$ that quantifies the effect of the parents on the node.

A more involved example would be the following, where an $Alarm$ might be
triggered by $Burglary$ or an $Earthquake$ which then proceeds to call John,
$JohnCalls$, or Mary, $MaryCalls$.

```{.mermaid width=50% theme=neutral #fig:alarm}
graph TD;
    Burglary ---> Alarm;
    Earthquake ---> Alarm;
    Alarm ---> JohnCalls;
    Alarm ---> MaryCalls;
```

The **conditional probability table** (CPT) of $Alarm$ can be found in @tbl:cpt.
Since we are dealing with binary conditions (either $A$ happens or it doesn't),
$P(\not A)$ is implicit. In other cases, the sum of the probabilities in one row
should equal $1$ to be considered valid probabilities.

|   B   |   E   | P(A) |
| :---: | :---: | ---- |
|   t   |   t   | .95  |
|   t   |   f   | .94  |
|   f   |   t   | .29  |
|   f   |   f   | .001 |

: Conditional probability table (CPT) of the $Alarm$ event. Notice how
dependence increases the size of the table according to $2^n$, where $n$ is the
number of dependent variables. This is because we are dealing with Boolean
conditions. {#tbl:cpt}

## The Semantics of Bayesian Networks

As mentioned before, a BN is a representation of a joint distribution function.
Another way to interpret it, however, is to view it as an encoding of a
collection of conditional independence statements. Instead of focusing on how
one is dependent on another, we think about which events are _not_ dependent on
another.

A BN can be described and used according to the following relation, which stems
from the **chain rule**.

$$
P(x_1, \ldots, x_n) = \prod^n_{i=1} P(x_i|parents(X_i))
$$

That is, the probability of a certain set of outcomes for the events described
by the BN (i.e. the values of it's nodes) can be calculated by taking the
product of the probabilities of all these events given their respective
parent(s). The conditional probability used in the product series can then be
described by the aforementioned CPT.

This means that, even though the BN is technically equivalent to the joint
probability distribution, assuming the network is sparse (i.e. not all nodes are
connected to all other nodes) it is more efficient in terms of computation.
Consider the following: if a joint probability distribution of Boolean random
variables scales according to $2^n$ where $n$ is the number of random variables,
a BN scales according to $n2^k$ where $k$ is the average number of parents.

Formally, we can say that a node is conditionally independent of its
**non-descendents** given its parents. Furthermore, we can say that a node is
conditionally independent of the whole network given its parents, children, and
children's parents, also called its **Markov Blanket**. The more connected a BN
is, the bigger the average Markov Blanket of its nodes.

Instead of considering all combinations of events, we assume that some events
do not influence one another. At the core of the BN lies this assumption, and
one should therefore consider the balance between accuracy and computational
complexity.

## Efficient Representation of Conditional Distributions

Assumptions can be made about the interaction of parents and how they relate to
their children. We can assume logical or min/max statements, and from there
construct the complete CPT. An example would be a $Fever$ which could be caused
by the $Flu$, a $Cold$, or $Malaria$. We then assume that these relate to each
other in something called a **fuzzy OR** scenario, i.e. the relation tends to
that of a logical OR. This means that we would only need, for example, the
probability of someone to get a $Fever$ from the $Cold$ and the probability to
get a $Fever$ from the $Flu$ to determine what the combined probability (see
@eq:fever)

$$
\begin{gathered}
P(Fever | Cold, Flu, \neg Malaria) = \\
(1 - P(\neg Fever | Cold, \neg Flu, \neg Malaria) \cdot P(\neg Fever | \neg Cold, Flu, \neg Malaria))
\end{gathered}
$$ {#eq:fever}

Instead of using a CPT, we can also employ 'normal' probability density
functions (PDFs) to describe the probabilistic characteristics of a random
variable. While we could use discretization to work with continious random
variables, this often comes at a loss of accuracy and potentially unwieldy CPTs.
There are some considerations to make with regard to **hybrid networks** where
we find both discrete and continuous random variables. Most notably, when a
continuous parent has a discrete child, we have to create some threshold
function. The most interesting here is the so-called **logistic function** which
is often used in neural networks for the same purpose.

## $\bowtie$ Exact Inference

Now my friends, the time has come, to collect info and probably infer some. We
know how BNs work and how to construct them. Now, we would like to use our model
to infer information given some state, i.e. perform a query.

In this section, we will only discuss _exact_ inference. First, we discuss the
'easy' way, and then apply some optimization on top of that in the form of
memoization.

### Inference by Enumeration

Let's take the BN presented in @fig:alarm, and use the following query:
$P(Burglary\ |\ JohnCalls = true, MaryCalls =  true)$. Inference by enumeration
simply takes all the possible contexts in which John might call, and where Mary
might call and considers where this would have been caused by a burglary.

We can start solving our query using the following relation,

$$
P(X\ |\ e) = \alpha P(X, e) = \alpha \sum_y P(X, e, y)
$$

where $\alpha=\frac{1}{e}$.

Applying our query to the equation then gives,

$$
P(B\ |\ j, m) = \alpha P(B, j, m) = \alpha \sum_e \sum_a P(B, j, m, e, a)
$$

For the sake of simplicity, we only consider $B=true$, which can be rewritten to
the following when taking our BN as the joint function (i.e. substitute $P(B, j, m,
e, a$ with the characteristic of the BN).

$$
P(b\ |\ j, m) = \alpha \sum_e \sum_a P(b)P(e)P(a\ |\ b,e)P(j\ |\ a)P(m\ |\ a)
$$

Which can then be simplified as follows,

$$
P(b\ |\ j, m) = \alpha P(b) \sum_e P(e) \sum_a P(a\ |\ b,e)P(j\ |\ a)P(m\ |\ a)
$${#eq:enumeration}

and then be solved by looking up the respective values in the CPTs.

### Variable Elimination

One can imagine the previous algorithm to be suboptimal. Considering the time
complexity, we come to the conclusion that it runs in $\mathcal{O}(2^n)$.
Realizing your algorithm runs in exponential time is never a nice experience..
But, it's a great improvement considering calculating the straight joint
probability runs in $\mathcal{O}(n2^n)$.

One way in which we can improve the performance of the model, is by reusing past
calculations (memoization, if you know, you know). This dynamic programming
technique is called **variable elimination**. The idea is to solve the equation
from the bottom up (that is, when viewed as a syntax tree, we start at the
leaves and move up) so that we can re-use calculations we've made before.

[...]
