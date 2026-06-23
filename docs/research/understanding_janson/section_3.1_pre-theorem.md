The main results begin by defining three critical values.

$$t_c := \left(  \frac{(r-1)!}{np^r}  \right)^{\frac{1}{r-1}}$$

This is the critical \"time\" value in the reformulation. If the graph
can continue to percolate past $t_c$, then the graph will either almost
percolate or percolate. If the graph doesn't get past $t_c$, then it'll
die out.

$$a_c := \left( 1-\frac1r \right) \cdot t_c$$

This is the critical initial value. If we begin with more than $a_c$
initially active nodes, then we'll percolate/almost percoalte w.h.p. If
we have less than $a_c$ initially active nodes, then w.h.p the graph
won't percolate.

$$b_c := n \cdot \frac{(pn)^{r-1}}{(r-1)!} \cdot e^{-pn}$$

This is the number of nodes that'll never activate, meaning the number
of nodes that have less than r edges. So unless the nodes within the
$b_c$ are in the initially active set, they'll never be activated.

The paper then gives examples for when $r = 2$ and how the equations
simplify for this value. In addition, the paper rewrites equation 3.1 to
display as

$$n \cdot \frac{(pt_c)^r}{r!} = \frac{t_c}{r}$$

The standard assumption is also introduced, where
$n^{-1} \ll p \ll n^{-\frac1r}$. On a high level, this ensure that the
graph is interesting. Meaning, the graph is sparse enough so that a
trivially small $a$ won't cause complete percolation. It also means that
the graph is well connected enough so that percolation is possible. This
is the \"sweet spot\" as it's where the graph is most interesting.

The assumptions imply:

$t_c \to \infty$. So as $n \to \infty$, the critical threshold for the
graph to percolate past also approaches $\infty$.

$p t_c \to 0$. This means that the expected number of marks any inactive
node will have at time $t_c$ tends to $0$; concretely
$\mathbb{E}[M_i(t_c)] = p t_c \to 0$. This is what justifies the Poisson
approximation below. (That $t_c$ is the bottleneck where most graphs die
out is a separate fact, coming from minimizing
$\bar f(t) = n(tp)^r/r! - t$, whose global minimum sits at $t_c$; see §6,
§8.) Mathematically, this allows us to confirm two things. First, the probability that a node is
activated, i.e., a node has received $r$ or more marks, is originally
modeled with $\pi (t) = P [Binom(t, p ) \geq r]$. Since $p t_c$
approaches zero, then so does $p t \to 0$. Then for the range where the
graph is at risk of not percolating, we can use an Poisson
approximation. Hence, we have
$\pi (t) = P [Binom(t, p) \geq r] \sim P [Poiss(t \cdot p ) \geq r]$.
Further more, when calculating $P [Poiss(t \cdot p ) \geq r]$, we get
$\sum_{j \geq r}^\infty \frac{(pt)^j}{j!} \cdot e^{-pt} = e^{-pt} \cdot \sum_{j \geq r}^\infty \frac{(pt)^j}{j!}$.
Now since $pt \to 0$, $e^{-pt} \to e^{-0} \to 1$. So
$\sum_{j \geq r}^\infty \frac{(pt)^j}{j!}$. And since $pt_c \to 0$, all
terms outside the first are negligible. Writing this out,
$\frac{(pt)^r}{r!} + \frac{(pt)^{r+1}}{(r+1)!} +\frac{(pt)^{r+2}}{(r+2)!} + ...$
becomes $\frac{(pt)^r}{r!}$ as all other terms are negligible.

$t_c / n \to 0$ The portion of nodes that are activate at the critical
threshold are small relative to n. This is what allows the graph to say
that we either have $A^* = n - o(n)$ or $A^* = n$ or $A^* = o(n)$. If
$t_c$ was too close to $n$, then all outcomes would be the same. Having
$t_c / n \to 0$ allows us to have these distinct outcomes. Moreover,
this will later allow us to have the doubly exponential phase.

$a_c \to \infty$, this is $t_c$ but with a constant factor in front of
it. We need $a_c \to \infty$ in order for us to have the deterministic
threshold, rather than a random outcome. Looking at the case when we do
not have $a_c \to \infty$, we see that the outcome is random.

$\frac{a_c}{n} \to 0$ further specifies $a_c$. However, I don't think
that this result is all that interesting, as we have already established
that $\frac{t_c}{n} \to 0$, and given that $t_c \geq a_c$, this doesn't
find anything new.

$b_c / n \to 0$ this is what allows us to say that the graph almost
percolate. Almost percolate implies that $A^* = n - o(n)$. Hence, the
fact that $b_c = o(n)$, is what allows this to be possible. $b_c$ is the
expected number of nodes that have less than $r$ edges, and thus can
never be activated unless they're in the initially active set. Here,
$b_c$ is key for identifying whether we percolate or almost percolate
when in the supercritical regime.

$p b_c \to 0$ This has 2 main purposes. The first is to allow us to have
a large window $b$ which includes $b_c$ that allows us to analyze how
the remaining nodes percolate. The second is that it allows us to
explicitly bound the time it'll take for the remaining parts of the
graph to percolate when we're in the supercritical regime. Since
$p b_c \to 0$, then $4p b_c < 1$. We then use $4p b_c$ to bound how long
it'll take for the graph to finish percolating.

Now the paper introduces:

$$\mathbb{E}[S_n (t_c)] = n \cdot \pi (t_c) \sim n \cdot \frac{(pt_c)^r}{r!} = \frac{t_c}{r}$$
To interpret this, the expected number of nodes can be modeled with
$n \cdot \pi(t_c)$, as we multiply the number of nodes and the
probability that a node is active at time $t_c$. Note that $S_n$
includes all nodes, meaning it also includes nodes in the intially
active nodes. Now we approximate this with the Poisson distribution, as
we model the $\pi (t_c)$ with a poisson distribution that simplifies to
$\frac{(pt_c)^r}{r!}$ due to the fact that $p t_c \to 0$, and that all
other terms such as
$\frac{(pt_c)^{(r+1)}}{(r+1)!} + \frac{(pt_c)^{(r+2)}}{(r+2)!} + ...$
are all negligible.

$$n - \mathbb{E}[S_n (n)] = 
    n ( 1 - \pi (n)) = 
    n \cdot \mathbb{P}[Bin(n, p) \leq r - 1] \sim n \cdot \mathbb{P}[Binom(n,p) = r-1]$$

This equation is used to later determine the number of inactive nodes
when the graph finishes percolating in the supercritical regime.
Regarding $n \cdot \mathbb{P}[Bin(n, p) \leq r - 1]$, this is
multiplying $n$, the total number of nodes, by the probability that they
have less than $r$ marks. This is then approximately equal to the
probability that a node has $r - 1$ marks, as the other terms are
insignificant in comparison.

$$\sim b^{'}_c := n \cdot \frac{(pn)^{r-1}}{(r-1)!} \cdot (1-p)^n$$

This is when the we formally define the number of leftover nodes with
$b_c^{'}$. It's defined as the total number of nodes (n), multiplied by
the probability that any given node has $r - 1$ marks, which is what the
$\frac{(pn)^{r-1}}{(r-1)!}$ represents. The $(1-p)^n$ is leftover from
the binomial approximation, where the value is a leftover. Note that a
more accurate form would be to use $(1 - p)^{n-(r-1)}$, however, since
$r-1$ is a constant and $n \to \infty$, we can approximate
$(1-p)^n \sim (1-p)^{n-(r-1)}$.

If we are in the case where $p \ll n^{-1/2}$, we have
$(1-p)^n \sim e^{-np}$, and we have

$$n - \mathbb{E}[S_n(n) ] = n  (1 - \pi (n))  \sim b_c \sim b_c^{'}$$

The condition $p \ll n^{-1/2}$ is exactly what makes $(1-p)^n \sim e^{-np}$:
since $\log(1-p)^n = -np - np^2/2 - \cdots$, the higher-order terms vanish
precisely when $np^2 \to 0$, i.e. when $p \ll n^{-1/2}$ — independent of $r$.
Under the standard assumption this case always includes $r = 2$ (there
$n^{-1/r} = n^{-1/2}$), but not only $r = 2$: for $r \geq 3$ the condition
$p \ll n^{-1/2}$ is an extra restriction that may or may not hold (e.g.
$r=3,\ p=n^{-0.7}$ satisfies it; $r=3,\ p=n^{-0.4}$ does not).

If $p$ is larger, meaning that $p = \Omega (n^{-\frac{1}{2}  })$ (which under
the standard assumption forces $r \geq 3$), which means that $p$ grows no
slower than $n^{-1/2}$. This can be restated as
$n^{-\frac{1}{2}} = O(p)$, which means that $n^{-\frac{1}{2}}$ grows no
faster than $O(p)$. In this scenario, our approximation for $b_c^{'}$
might not be true. To have a statement that is universally accurate, we
write:

$$n - \mathbb{E}[S_n (n)] = n \cdot (1 - \pi (n)) = b_c + o (b_c + 1)$$

This can be interpreted as that there is some slight variation around
what $b_c$ is regarding the true value of the number of nodes that are
not activated. More specifically, the difference in our $b_c$ and the
real number of inactive nodes is accurate up to some error $o(b_c + 1)$,
which is negligible.

Now we shift our focus to $S(t)_{n-a}$. The results are similar to
$S(t)_n$, but with errors depending on $a$.

To calculate $b_c$, we are introduced to

$$np - \left(\log (n) + (r-1) \cdot \log (np) \right)
    \to 
    \begin{cases}
        -\infty \\
        \beta \\
        \infty 
    \end{cases}
    \Leftrightarrow
    b_c 
    \to
    \begin{cases}
        \infty  \\
        (r-1)! ^{-1} \cdot e ^{-\beta }  \\
        0
    \end{cases}$$

To interpret this, the LHS,
$np - \left(\log (n) + (r-1) \cdot \log (np) \right)$ rewritten to show
us what $b_c$ approaches as $n \to \infty$. To go through the steps,

$$\begin{aligned}
    b_c &= n \cdot \frac{(pn)^{r-1}}{(r-1)!} \cdot e^{-pn} \\
    \log (b_c) &= \log (n \cdot \frac{(pn)^{r-1}}{(r-1)!} \cdot e^{-pn}) \\
    &= \log(n) + \log (\frac{(pn)^{r-1}}{(r-1)!}) + \log (e^{-pn}) \\ 
    &= \log(n) + \log ((pn)^{r-1}) - \log ({(r-1)!})  -pn \\ 
    &= \log (n) + (r-1) \cdot \log(pn) - \log ({(r-1)!})  -pn 
\end{aligned}$$

$\text{Now we rearrange} \\$

$$\begin{aligned}
    \log (b_c) + \log ({(r-1)!}) &= \log (n) + (r-1) \cdot \log(pn)   -pn \\
    &= - (pn - \log (n) - (r-1) \cdot \log(pn))
\end{aligned}$$

$\text{Now we set } L = pn - \log (n) - (r-1) \cdot \log(pn)$

$$\begin{aligned}
    \log(b_c) + \log((r-1)!) &= -L \\ 
    \log(b_c)  &= -L - \log((r-1)!) \\
    e ^ {\log(b_c)}  &= e^{-L - \log((r-1)!)} \\
    b_c &= e^{-L} \cdot e^{-\log((r-1)!)} \\
    &= e^{-L} \cdot \frac{1}{(r-1)!}
\end{aligned}$$

With all of this done, the difference between L or
$np - (\log n + (r-1) \cdot \log (np))$ and $b_c$ is a constant factor
of $\log ((r-1)!)$. Because the shift is by $- \log ((r-1)!)$, we have
the equivalence. Now if we assume that $p \geq n^{-1}$, then near the
threshold $np \sim \log n$, so $\log(np) = \log\log n + o(1)$ and we may
replace $\log(np)$ by $\log\log n$ inside the expression (the assumption
$p \geq n^{-1}$ keeps $np \geq 1$). So we have

$$np - (\log n + (r-1) \log \log (n)) \to 
    \begin{cases}
        -\infty \\
        \beta \\
        \infty
    \end{cases}
    \Leftrightarrow 
    b_c
    \to 
    \begin{cases}
        \infty \\
        \frac{1}{(r-1)!} \cdot e^{-\beta} \\
        0
    \end{cases}$$

Now we interpret the equations. In order to be able to tell how many
nodes have $r - 1$ or less edges, it's difficult to initially see
whether $b_c$ will converge/diverge. Hence, we take the log and see if
$np$ or $\log n + (r-1) \log (np)$ is larger.

In the case where $np$ is smaller by a significant amount, so the whole
line $np - (\log n + (r-1) \log (np))$ diverges to $-\infty$, then
$b_c \to \infty$: the number of nodes with fewer than $r$ edges grows
without bound (though it stays $o(n)$, since $b_c/n \to 0$).

Similarly, if $np$ is larger by a significant amount and thus
$np - (\log n + (r-1) \log (np))$ diverges to $\infty$, then $b_c \to 0$
and w.h.p. there are no nodes with fewer than $r$ edges.

If instead $np - (\log n + (r-1) \log (np))$ converges to some constant
$\beta$, then $b_c \to (r-1)!^{-1} e^{-\beta}$, a finite positive value
giving the limiting expected number of nodes with fewer than $r$ edges.
