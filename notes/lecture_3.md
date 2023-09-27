# Maintaining a Belief over Time

## Introduction

- Changing the simple **sensor model** to a **transition model** by
  incorporating time steps, but no ability to which next state is the most
  likely (why? most probable is not most likely?).
- Different Types of models:
  - Hidden Markov Models
  - Kalman Filters
  - Dynamic Bayesian Networks
- Incorporating time can be important to, for example, take into account the
  rate of change (first derivative) when making decisions.

## Transition and Sensor Models

- **Markov assumption**: _"The current state depends on only a finite fixed number of
  previous states."_ Any system or process that satisfies this assumption is
  called a **Markov Process** or **Markov Chain**.
- The number of dependent prior states, $n$, is integrated into the so-called
  order, a so-called **$n$th-order Markdown Process**.
- Formally, a first-order Markov process is denoted as:

$$
P(X_t|X_{0:t-1}) = P(X_t|X_{t-1})
$$

- Important is that the underlying laws of the system do not change, therefore,
  the distributions are stationary over $t$.
- Another important assumption is that of the **sensor Markov assumption**
  (see @eq:sensor_markov_assumption). That is, the observable variable is only
  dependent on the hidden variable in the current time-step. Also called the
  observation model.

$$
P(E_t|X_{0:t}, E_{0:t-1}) = P(E_t|X_t)
$${#eq:sensor_markov_assumption}

- The process has to initialize with a prior probability at $t=0$, $P(X_0)$.
- Thus, we can denote the  complete joint probability distribution for a
  **first-order Markov Process** (see @eq:first_order_markov).

$$
P(X_{0:t}, E_{1:t}) = P(X_0) \prod^t_{i=1} P(X_i|X_{i-1})P(E_i|X_i)
$${#eq:first_order_markov}

- The accuracy of such a model depends on how 'reasonable' the Markov assumption
  is, and how closely the chain of causality resembles the real world (the
  probability that someone brings an umbrella might also be dependent on the
  amount of sun, instead of only whether it's raining.).
- There are two ways to improve the accuracy of a model (which are
  re-formulations of one-another):
  1. Increase the order of the Markov process model.
  2. Increase the set of state variables.

## Inference in Temporal Models

- Various methods for inference exist which can complement each other to improve
  accuracy of the model besides just answering queries.
  1. **Filtering**: Informs our agent about the distribution of the current
     hidden state based on the observations made until now, $P(X_t|e_{1:t})$.
  2. **Prediction**: Determine the distribution of the next hidden state based
     on the observations made until now, $P(X_{t+1}|e_{1:t})$.
  3. **Smoothing**: Determine the distribution of a  past hidden state, $0 \ge k
     \lt t$, based on the observations made until now, $P(X_k|e_{1:t})$.
  4. **Most likely explanation**: Determine the most likely sequence of events
     based on the observations made until now, $P(x_{1:t}|e_{1:t})$.
- Another technique called **Learning**, is based on **smoothing** combined with
  the **EM** algorithm.

### Filtering And Prediction

- The process of filtering (see @eq:filtering_markov) depends on prediction, (at
  least, based on the formulations mentioned above). ($\alpha$ is always a
  normalization constant).

$$
P(X_{t+1}|e_{1:t+1}) = \alpha P(e_{t+1}|X_{t+1}) \sum_{x_t} P(X_{t+1}|x_t) P(x_t|e_{1:t})
$${#eq:filtering_markov}

- They are two steps that are necessary for one another. Therefore, while they
  are separate queries, they could be considered two steps in the same process.
  To get $P(X_{t+1}|e_{1:t+1})$,
  
  1. Predict:
    $$
    P(X_{t+1}|e_{1:t}) = \sum_{x_{t-1}} P(X_t|x_{t-1}) P(x_{t-1})
    $$
  2. Filter:
    $$
    P(X_{t+1}|e_{1:t+1}) = \alpha P(e_{t+1}|X_{t+1}) P(X_{t+1}|e_{1:t})
    $$

- The initialization predict step could be considered as prediction with empty
  evidence (i.e. without evidence), $e_0$. In which case it reduces to the
  prior, $P(x_0|e_0) = P(x_0)$.
  $$
  \begin{split}
  P(X_1|e_0) &= \sum_{x_0}P(X_1|x_0)P(x_0|e_0) \\
             &= \sum_{x_0}P(X_1|x_0)P(x_0) \\
  \end{split}
  $$

### Smoothing

- With smoothing, we can essentially improve the model to take into account new
  observations, and can be described by @eq:smoothing_markov.

$$
\begin{split}
P(X_k|e_{1:t}) &= \alpha P(X_k|e_{1:k}) P(e_{k+1:t}|X_k) \\
               &= \alpha f_{1:k} \times b_{k+1:t}
\end{split}
$${#eq:smoothing_markov}

- The factors $f$ and $b$, implying forward and backward respectively, can
  then be described by @eq:filtering_markov and @eq:smoothing_backward
  respectively.

$$
\begin{gathered}
  P(e_{k+1:t}|X_k) = \sum_{x_{k+1}} P(e_{k+1}|x_{k+1}) P(e_{k+2:t}|x_{k+1}) P(x_{k_1}|X_k) \\
  \implies b_{k+1:t} = Backward(b_{k+2:t}, e_{k+1})
\end{gathered}
$${#eq:smoothing_backward}

- While smoothing would take $O(t)$ for a single time-step, and thus $O(t^2)$ for all
  timesteps, by saving the intermediate results, we can smooth the whole
  sequence in $O(t)$ by applying the **forward-backward algorithm**.

### Most-likely Sequence  

- Since the most-likely sequence is formed by the joint probability of all the
  hidden states, we cannot just apply smoothing and calculate the most likely
  hidden state based on that states prior.

$$
\begin{gathered}
\max_{x_1 \ldots x_t} P(x_1, \ldots, x_t, X_{t+1} | e_{1:t+1}) \\
= \alpha P(e_{t+1}|X_{t+1}) \max_{x_t}
 \left( P(X_{t+1}|x_t) \max_{x_1 \ldots
x_{t-1}} P(x_1, \ldots, x_{t-1}, x_t | e_{1:t}) \right)
\end{gathered}
$${#eq:most_likely_markov}

- The algorithm to compute the most likely sequence is also called the **Viterbi
  algorithm** (see @eq:most_likely_markov).

## Dynamic Bayesian Networks

- Dynamic Bayesian Networks (DBNs) are a generalization of the HMMs. Every HMM
  is a single-variable DBN; every discrete DBN is an HMM. **A DBN can have
  multiple 'sensors', while a HMM can have only one** (that is one observable).
- Exact inference in DBNs becomes intractable as their
  size grows. Thus, we use approximate inference. Specifically, **particle filtering**:

> First, a population of $N$ initial-state samples is created by sampling from
> the prior distribution $P(X_0)$. Then, the update cycle is repeated for each
> time step:
>
> 1. Each sample is propagated forward by sampling the next state value
>    $x_{t+1}$ given the current value $x_t$ for the sample, based on the
>    transition model $P(X_{t+1}|x_t)$.
> 2. Each sample is weighted by the likelihood it assigns to the new evidence,
>    $P(e_{t+1}| x_{t+1})$
> 3. The population is resampled to generate a new population of $N$ sample.
>    Each new sample is selected from the current population; the probability
>    that a particular sample is selected is proportional to its weight. The new
>    samples are unweighted.
