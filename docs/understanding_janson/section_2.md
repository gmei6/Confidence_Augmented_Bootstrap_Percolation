# My understanding of the Janson paper {#my-understanding-of-the-janson-paper .unnumbered}

Section 2: A useful reformulation

This formulation changes the time scale. Rather than going generation by
generation, we go node by node, revealing each node and edge only as we
need to.

We begin with the initially active set, denoted with $\mathcal{A}(0)$.
This is the set of initially active nodes, and the magnitude/size of
this initially active set is found with $A(0) = | \mathcal{A}(0)|$.

To begin, we choose a single node $u_1 \in \mathcal{A}(0)$. We then
reveal all the edges that $u_1$ has, and give each of $u_1$'s neighbors
a mark. note that once a node accumulates $r$ marks, it becomes active.
Once we're done marking $u_1$'s neighbors, we then append $u_1$ to the
used set, which we denote with $Z(1)$.

Now we'll look at how $\mathcal{A}(t)$ and $Z(t)$ grow.

At time $t$, we can find $A(t)$ with
$A(t) = A(t- 1) \cup \Delta \mathcal{A}(t)$. We can find
$\mathcal{A}(t)$ as the number of nodes that were activated at time $t$.
Skipping ahead a bit, this can be found with a negative binomial
distribution.

Now how $Z(t)$ grows, $Z(t) = Z(t-1) \cup u_t$.

From this, we can see that $A(t)$ is non decreasing, while $Z(t)$ is
stricly increasing.

The graph stops running at time $T$. This time is defined as

$$T := \min \{t \geq 0 : \mathcal{A}(t) \setminus Z(t) = \emptyset \}$$

Note that when nodes are activated, we can add them into a queue. We
need to then pick nodes, the $u_t$ from this queue in this order to
ensure that running node by node gets us the same result as going
generation by generation.

Now we rewrite equation (1). We rewrite $A(t) = | \mathcal{A}(t) |$, so
$A(t)$ is the number of active vertices at time $t$.

To reinforce this, the number and the set of active vertices is
different.

Now since we add a single new node to $Z(t)$ at each time $t$, we know
that $|Z(t)| = t$. Moreover, since all elements of the used set are
active nodes, $Z(t) \subseteq \mathcal{A}(t)$, and only when the graph
ends does $Z(t) = \mathcal{A}(t)$. However, we must note that
$Z(t) \subseteq \mathcal{A}(t)$ is only true for $t = 0, 1, 2, ... , T$.

Now we use these new variables to rewrite equation (1).

$$T = \min \{ t \geq 0 : \mathcal{A}(t) \setminus Z(t) = \emptyset  \} = \min \{ t \geq 0 : A(t) \leq t \}$$

Why does this reformuation work? Because at the time
$\mathcal{A}(t) \setminus Z(t)$, we have $\mathcal{A}(t) = Z(t)$. Taking
the magnitutde of both sides, we have $|\mathcal{A}(t)| = |Z(t)|$ to
also denote when the graph stops. Since $A(t) =| \mathcal{A}(t)|$ and
$t = |Z(T)|$, we have:

$$A(t) = |\mathcal{A}(t)| = |Z(t)| = t$$

which leaves us with $A(t) = t$ as the stopping condition. Since the
graph stops when this holds true, it also holds true when $A(t) \leq t$.

Now rewriting this with $T$ instead of $t$ to denote the proper stopping
time, $A(T) = T$.

The paper then introduces yet another new variable, $A^*$, which is
defined as $A^* = A(T)$. The purpose is probably just for convenience.

Janson states that the set $\mathcal{A}(0)$ percolates iif $T = n$ and
$\mathcal{A}(0)$ almost percolates iif $T = n - o(n)$.

This language of percolates and almost percolates will be used a lot
later.

Edges are revealed once we have selected a node. For example, in the
beginning, the graph \"appears\" to be completely empty, with nothing
there and no edges. After we choose $u_1$, we reveal all the edges it
has and all of it's neighbors. Same process for $u_2$, and $u_t$.

Now, Janson introduces how marks are added onto nodes.

Let $i$ be some node that isn't in the used set. We use an indicator
variable, $I_i(s)$ to denote whether there does or does not exist an
edge between the node $u_s$ and $i$.

Since $u_s$ is the node that we are using at time $s$, we can think of
$I_i (s)$ in multiple different ways.

1\. This can be an indicator whether there's an edge between $u_s$ and
$i$.

2\. An indicator variable to determine whether node $i$ gets a mark at
time $s$.

We formulate the indicator variable like this so that

$$M_i (t) = \sum_{s=1}^t I_i(s)$$

Now what does this equation, equation (3) mean? It's the sum of the
marks that node i has at time $t$. This is useful, as it'll allow us to
determine whether a node is active or not at any time $t \leq T$.

For example, a node not in the initially active set,
$i \notin \mathcal{A}(0)$ is active iif $M_i(t) \geq r$. This makes
analyzing whether nodes are active or not really convenient, as it's
essentially just a bunch of i.i.d. Bernouli variables with probability
$p$.

However, note that this current formulation of $M_i (t)$ is only valid
for when $t \leq T$. I don't know why, but the paper also expands this
so that we can define $I_i(s)$ for all $i \in V_n$, so that it's defined
even when the graph has stopped percolating.

The way to do this is to like this:

1.  We have i.i.d $I_i(s) \in Be(p)$ for $i \in V_n$ and $s \geq 1$ and
    an initial set of active nodes $\mathcal{A}(0) \subseteq V_n$.

2.  Begin with $Z(0) = \emptyset$ and an empty graph on $V_n$

3.  When we select nodes, we choose from the set,
    $u_t \in  \mathcal{A}(t-1) \setminus Z(t-1)$ if it's not empty. If
    it is empty, then we choose from $u_t \in V_n \setminus Z(t-1)$,
    where we take the smallest vertex.

4.  Define $M_i(t)$ the same way as before, but we say that it's valid
    for all $i \in V_n$ and $t \geq 0$

5.  To update our sets,
    $\mathcal{A}(t) = \mathcal{A}(0) \cup \{i : M_i(t) \geq r \}$ and
    $Z(t) = Z(t-1) \cup u_t$.

6.  Then we add an edge between each $u_t$ and $i$ where $I_i(t) = 1$.

7.  Then the stopping condition is the same as before, equation (2).

Now we go back to looking at nodes and their activations.

Since an active node can never be deactivated, when trying to determine
which nodes to look at regarding activation, we naturally look at the
inactive nodes.

So for $i \in V_n \setminus \mathcal{A}(0)$, we have the next equation:

$$Y_i := \min \{ t : M_i(t) \geq r
    \}$$

What does this mean? For the nodes that aren't initially active, the
variable $Y_i$ will denote at what time the node activates. We can see
this, as we're looking to find the minimum time for a given node, i, to
get $r$ or more marks.

Now if $Y_i \leq T$, then that means that the node $i$ will end up being
activated at some point in the graph's percolation. Conversely, if
$Y_i > T$, then node $i$ will never be activated.

So for $t \leq T$, we can write the following equation to determine the
number of nodes active at time $t$.

$$\mathcal{A}(t) = \mathcal{A}(0) \cup \{ i\notin \mathcal{A}(0) : Y_i \leq t \}$$

Now to actually define what $Y_i$ is, recall that $M_i(t)$ is a binomial
distribution, $Binom(t,p)$, since it's the sum of many i.i.d. Bernoulli
variables with parameter $p$. This then allows us to define $Y_i$ as a
negative binomial distribution, $NegBinom(r,p)$. Formally, we write:

$$P[Y_i = k] = P [M_i(k-1) = r-1, I_i(k) = 1] = \binom{k-1}{r-1} p^r (1-p)^{k-r}$$

To interpret this,

$P[Y_i = k]$ is the probability that node $i$ will be activated at time
$k$

$P [M_i(k-1) = r-1, I_i(k) = 1]$ is the probability that at time $k-1$,
the node $i$ has $r-1$ marks and get it's $r$th mark at time $k$.

$\binom{k-1}{r-1} p^r (1-p)^{k-r}$ this is the equation of the negative
binomial distribution. The $\binom{k-1}{r-1}$ is the different ways we
could have accumulated $r-1$ marks within the first $k-1$ steps. $p^r$
is to denote all the marks we get. $(1-p)^{k-r}$ is to denote all the
marks we didn't get. Also note that the $Y_i$ are i.i.d.

Now, we use all of this to define a new variable which denotes our
stochastic process.

Let $t = 0, 1, 2, ...$.

$$S(t) := | \{ i \notin \mathcal{A}(0) : Y_i \leq t \} | = \sum_{i \notin \mathcal{A}(0)} \boldsymbol{1} \{ Y_i \leq t \}$$

First let's break down what this means.

The variable, $S(t)$ is defined as the size of the set of nodes, which
do not include the ones that are initially active, which are active at
or before time $t$. So in plain English, $S(t)$ is the number of nodes
that are activated at time $t$, not including initially active nodes.

The summation explains that $S(t)$ can also be though of as iterating
through each node, not initially active, and adding the indicator
variable for whether $Y_i \leq t$. Essentially, we do something like
this:

    def S(t)(self, Y_i, t):
        inactive = {V_n - A(0)}
        count = 0
        for node in inactive:
            if Y_i <= t:
                sum += 1
        return sum

Now we've finally arrived at a key piece of information. Most of what is
studied in this paper revolves around $S(t)$. This process looks at
$n - a$ nodes, and processes an $\boldsymbol{1}\{ t \leq Y_i \}$. Since
this is a indicator variable, it can only take on values of $0$ or $1$.

By default, $S(t) = S_{n-a}(t)$. However, Janson will sometimes use
$S_{n-a}(t)$ to emphasize that the stochastic process has $n - a$
elements to sum up.

For other general uses, the author defines
$S_m (t) := \sum_{i=1}^m \boldsymbol{1}\{ Y_i \leq t \}$ for any
$m \leq n$.

Now since $S(t)$ is made up of many i.i.d $Y_i$ variables, (which in
turn are made up of i.i.d Bernoulli variables), it makes analyzing the
process easier.

$$S(t) \in Binom \left( n - a, \pi (t) \right)$$

The variable $\pi(t)$ is defined as

$$\pi (t) := P [Y_1 \leq t] = P [M_1 (t) \geq r] = P [Binom(t,p) \geq r]$$

To interpret this, $\pi (t)$ is the probability that a node is active.
We break down what each part means.

$P [Y_1 \leq t]$ is the probability that node $1$ will be activated at
or before time $t$

$P [M_1 (t) \geq r]$ is the probability that node $1$ will accumulate
$r$ or more marks on time $t$

$P [Binom(t,p) \geq r]$ is the probability that there are $t$ or more
edges between node $1$ and other nodes that are active.

Finally, we have the following equations:

$$\mathbb{E} [S(t)] = (n-a) \cdot  \pi (t)$$

We have this, as the expected value of a binomial variable with
parameters $n - a$ and probability $\pi (t)$ then the mean, or
expectected value, would be $( n - a) \cdot \pi (t)$.

$$Var [S(t)] = (n-a) \cdot  \pi(t) \cdot (1-\pi(t)) \leq \mathbb{E} [S(t)] \leq n \pi (t)$$

The variance follows a similar path, as a typical binomal variable with
$Binom(n,p)$ has variance $np(1-p)$, the variance of $S(t)$ si
$(n-a) \pi (t) \cdot (1 - \pi (t))$. This is then bound above by the
mean, as $1 - \pi (t) \leq 1$.
