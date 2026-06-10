# **LARGE DEVIATION FOR UNIFORM GRAPHS WITH GIVEN DEGREES**

BY SOUVIK DHARA1,a AND SUBHABRATA SEN2,b

<sup>1</sup>*Department of Mathematics, Massachusetts Institute of Technology,* <sup>a</sup>*[sdhara@mit.edu](mailto:sdhara@mit.edu)* <sup>2</sup>*Department of Statistics, Harvard University,* <sup>b</sup>*[subhabratasen@fas.harvard.edu](mailto:subhabratasen@fas.harvard.edu)*

Consider the random graph sampled uniformly from the set of all simple graphs with a given degree sequence. Under mild conditions on the degrees, we establish a large deviation principle (LDP) for these random graphs, viewed as elements of the graphon space. As a corollary of our result, we obtain LDPs for functionals continuous with respect to the cut metric, and obtain an asymptotic enumeration formula for graphs with given degrees, subject to an additional constraint on the value of a continuous functional. Our assumptions on the degrees are identical to those of Chatterjee, Diaconis and Sly (*Ann. Appl. Probab.* **21** (2011) 1400–1435), who derived the almost sure graphon limit for these random graphs.

**1. Introduction.** In a seminal paper, Chatterjee and Varadhan [\[15\]](#page-24-0) initiated a study of large deviations for random graphs, and introduced a novel framework that synergizes the classical theory of large deviations with the theory of dense graph limits (Lovász [\[33\]](#page-25-0)). They embedded Erdos–Rényi random graphs into the space of graphons, equipped with the cut- ˝ metric, and derived an LDP for the corresponding sequence of probability measures. As an important consequence, this yields LDPs for continuous functionals in the cut-metric topology, for example, subgraph counts, largest eigenvalue, etc. Their result resolved a longstanding open question regarding large-deviations for sub-graph counts of dense Erdos–Rényi ˝ random graphs. This area has witnessed rapid developments subsequently—we refer the interested reader to Chatterjee's Saint-Flour lecture notes [\[11\]](#page-24-0) for a detailed history of these problems and an elaborate description of recent breakthroughs.

Numerous scientific applications naturally motivate the study of graphs with topological constraints, such as a fixed number of edges, triangles etc. (see, e.g., [\[17,](#page-24-0) [38,](#page-25-0) [49\]](#page-26-0)). The desire to understand typical properties of constrained graphs motivates the study of random graphs, sampled uniformly, subject to these constraints. Natural examples include the Erdos–Rényi ˝ uniform random graph with a constrained number of edges, random regular graphs [\[27\]](#page-25-0), etc. In statistical physics parlance, these can be thought of as microcanonical ensembles, whereas unconstrained graphs, like Erdos–Rényi, correspond to canonical ensembles [ ˝ [20,](#page-25-0) [44\]](#page-26-0). A rigorous study of constrained graphs often turns out to be extremely challenging—in fact, even enumerating the total number of graphs, subject to combinatorial constraints, is exceedingly nontrivial, and has attracted significant attention recently in probability, combinatorics and statistical physics (see, e.g., [\[2,](#page-24-0) [31,](#page-25-0) [40–42,](#page-25-0) [46,](#page-26-0) [48\]](#page-26-0)). The study of large deviations in this context is of natural interest—indeed, this has deep, natural connections to the problem of counting graphs with atypical properties, subject to the topological constraints. Recently, Dembo and Lubetzky [\[18\]](#page-25-0) initiated a study of large deviations for constrained random graphs, and derived an LDP for dense Erdos–Rényi uniform random graphs, conditioned to have a fixed ˝ number of edges.

In this paper, we study the uniform random graph with a given degree sequence. The degrees are assumed to scale linearly in the number of vertices, so that we have a dense random

Received January 2020; revised April 2021. *[MSC2020 subject classifications.](https://mathscinet.ams.org/mathscinet/msc/msc2020.html)* 60C05, 05C80.

<span id="page-1-0"></span>graph. Such random graphs are used extensively in physics [44] and statistics [5], and have a rich history in combinatorics [2, 6, 47]. In general, this model is intractable to theoretical analysis. In fact, characterizing the first order asymptotics of simple functionals like triangle counts is challenging in this case. In a breakthrough paper, Chatterjee, Diaconis and Sly [14] derived that, under fairly mild conditions (see Assumption 1), these random graphs converge almost surely in the cut-metric, and identified the limit. Our main result, Theorem 2, establishes an LDP for uniform random graphs under identical conditions as [14]. This general theorem has two important corollaries. The first corollary (Corollary 4) yields LDPs for continuous functionals such as subgraph counts. The second corollary (Corollary 5) yields the convergence of the microcanonical partition function. Further, it provides the asymptotic count of graphs with given degrees, subject to an additional constraint on the value of a continuous functional, in terms of a variational formula.

Conceptually, the problem under consideration is significantly more challenging than the Erdős–Rényi case, due to the absence of edge-independence in these models. Further, in sharp contrast to the setting of Dembo and Lubetzky [18], the number of degree constraints grows linearly with the number of vertices in the graph. To overcome this issue, we crucially exploit a deep idea put forth in [14]—these random graphs may be sampled using appropriate inhomogeneous random graphs, conditioned to have the desired degrees (see Section 4.1, and in particular (4.9)). Unfortunately, even with access to this ingredient, one still faces substantial technical obstacles due to the inhomogeneity of the unconstrained model. Our proofs require a very delicate understanding of the cut-topology, and deviate significantly from the established techniques for the dense Erdős–Rényi model. To the best of our knowledge, this is the first instance where an LDP has been derived in inhomogeneous settings. Finally, we remark that requisite analytic properties of the candidate rate function, such as lower-semicontinuity, are not obvious here, and require careful analysis.

The rest of the paper is organized as follows: In Section 1.1, we set up the framework necessary to state our main result. The statement of the main result and its corollaries is provided in Section 1.2. In Section 1.3, we discuss the relevant literature and collect some open problems surfacing from our work. Section 2 derives important analytic properties of the rate function. In Section 3, we prove a large deviation upper bound for inhomogeneous random graphs. The proof of Theorem 2 is completed in Section 4. Finally, we prove Corollaries 4 and 5 in Section 5.

### 1.1. Definitions and concepts.

1.1.1. *Graphons and the cut metric*. A graphon is a measurable function  $W:[0,1]^2 \mapsto [0,1]$  that is symmetric, that is, W(x,y) = W(y,x) for all  $x,y \in [0,1]$ . To define the cut metric, let  $\mathcal{M}$  denote the set of all bijective, Lebesgue measure preserving maps  $\phi:[0,1] \mapsto [0,1]$ . The cut distance between two graphons  $W_1$  and  $W_2$  is given by

(1.1) 
$$d_{\square}(W_1, W_2) = \sup_{S, T \subset [0,1]} \left| \int_{S \times T} (W_1(x, y) - W_2(x, y)) \, \mathrm{d}x \, \mathrm{d}y \right|,$$

and the cut metric is given by

(1.2) 
$$\delta_{\square}(W_1, W_2) = \inf_{\phi \in \mathcal{M}} d_{\square}(W_1, W_2^{\phi}),$$

where  $W^{\phi}(x,y) = W(\phi(x),\phi(y))$ . See [9], Lemma 3.5, for equivalent definitions of the cut metric. Setting  $\mathscr{W}$  to denote the space of all graphons, define the equivalence relation  $W_1 \sim W_2$  if  $\delta_{\square}(W_1,W_2)=0$ , and consider the quotient space  $\mathscr{W}=\mathscr{W}/_{\sim}$ . By [33], Corollary 8.14,  $W_1 \sim W_2$  if and only if  $W_1^{\phi}=W_2^{\psi}$  for measure preserving transformations  $\phi$ ,  $\psi$ . Also, note that  $(\mathscr{W},\delta_{\square})$  is a compact metric space [33], Theorem 9.23. Henceforth, for any  $W\in\mathscr{W}$ , we always write  $\mathscr{W}$  to denote the equivalence class of W in  $\mathscr{W}$ .

<span id="page-2-0"></span>DEFINITION 1 (Empirical graphon). For a graph  $G_n$  with vertex set  $[n] = \{1, ..., n\}$  and edge set  $E(G_n)$ , the empirical graphon  $W^{G_n}$  is given by

(1.3) 
$$W^{G_n}(x,y) = \begin{cases} 1 & \text{if } (i,j) \in E(G_n), (x,y) \in \left[\frac{i-1}{n}, \frac{i}{n}\right) \times \left[\frac{j-1}{n}, \frac{j}{n}\right), \\ 0 & \text{otherwise.} \end{cases}$$

DEFINITION 2 (Graph convergence).  $(G_n)_{n\geq 1}$  is said to converge in  $(\tilde{\mathcal{W}}, \delta_{\square})$  if their empirical graphons converge.

DEFINITION 3 (Subgraph densities). For a finite simple graph H = (V(H), E(H)) with V(H) = [k], the subgraph density of H in W is defined as

(1.4) 
$$t(H, W) := \int_{[0,1]^k} \prod_{(i,j)\in E(H)} W(x_i, x_j) \prod_{i=1}^k dx_i.$$

Note that  $t(H, W^{\phi}) = t(H, W^{\psi})$  for measure preserving transformations  $\phi$ ,  $\psi$ , and thus  $t(H, \cdot)$  is well defined on  $\tilde{\mathcal{W}}$ . We write  $t(H, \tilde{\mathcal{W}})$  to denote the subgraph density of  $\tilde{\mathcal{W}} \in \tilde{\mathcal{W}}$ . Also, [9], Theorem 3.7, shows that  $t(H, \cdot)$  is Lipschitz continuous on  $(\tilde{\mathcal{W}}, \delta_{\square})$  for any finite simple graph H.

DEFINITION 4 (Degree distribution function). For any  $W \in \mathcal{W}$ , the degree distribution function is defined by

(1.5) 
$$\deg_W(\lambda) = \Lambda \left\{ x : \int_0^1 W(x, y) \, \mathrm{d}y \le \lambda \right\},\,$$

where  $\Lambda$  denotes the Lebesgue measure on [0,1], and  $\lambda \in [0,1]$ . Observe that  $\deg_W$  is well defined on  $\tilde{W}$ . We write  $\deg_{\tilde{W}}$  to denote the degree distribution function of  $\tilde{W} \in \tilde{W}$ .

DEFINITION 5 (Graphons away from boundary). A graphon W is said to be away from boundary if there exists an  $\eta > 0$  such that  $\eta < W(x, y) < 1 - \eta$ . A sequence  $(W_n)_{n \ge 1}$  is said to be away from boundary if for all  $n \ge 1$ , the above holds for some  $\eta > 0$  (independent of n).

1.1.2. Uniform graphs with given degrees. Consider a sequence of degree sequences  $(d^n)_{n\geq 1}$ ,  $d^n=(d^n_i)_{i\in [n]}$ . Without loss of generality, we will assume that the degree sequence is nonincreasing, that is,  $d^n_1\geq \cdots \geq d^n_n$ . For clarity of notation, we will simply write  $d^n_i=d_i$ , and  $d^n=d$ , and suppress the dependence of the degrees on n. Let  $G_{n,d}$  denote the uniformly chosen random graph with degree sequence d.

Of course, not all sequences d are valid degree sequences of simple graphs. Such sequences are called graphical, and they are characterized by the celebrated Erdős–Gallai theorem [22]. This theorem establishes that d is graphical if and only if  $\sum_{i \in [n]} d_i$  is even and for all  $k \in [n]$ 

(1.6) 
$$\sum_{i=1}^{k} d_i \le k(k-1) + \sum_{i=k+1}^{n} \min\{d_i, k\}.$$

Thus  $G_{n,d}$  is defined whenever (1.6) holds. Chatterjee, Diaconis and Sly [14] obtained the graphon limit of  $G_{n,d}$  when the degrees converge, and the degree sequence lies in the interior of an asymptotic Erdős–Gallai boundary (1.6). We state below the precise assumptions from [14], which will also be the underlying assumption for our large deviation result.

<span id="page-3-0"></span>ASSUMPTION 1. The degree sequence  $d^n$  satisfies the following:

(1) There exists a nonincreasing function  $D:[0,1] \mapsto [0,1]$  such that

(1.7) 
$$\lim_{n \to \infty} \left( \left| \frac{d_1}{n} - D(0) \right| + \left| \frac{d_n}{n} - D(1) \right| + \frac{1}{n} \sum_{i=1}^n \left| \frac{d_i}{n} - D\left(\frac{i}{n}\right) \right| \right) = 0.$$

(2) There exist constants  $0 < c_1 < c_2 < 1$  such that,  $\forall x \in [0, 1], c_1 \le D(x) \le c_2$ , and

(1.8) 
$$\int_{x}^{1} \min\{D(y), x\} dy + x^{2} - \int_{0}^{x} D(y) dy > 0.$$

We write  $\mathbb{P}_{n,d}$  to denote the probability measure on  $\mathscr{W}$  associated to the empirical graphon of  $G_{n,d}$ , and write  $\tilde{\mathbb{P}}_{n,d}$  to denote the corresponding push forward measure on  $(\mathscr{W}, \delta_{\square})$ . The following was proved in [14], Theorem 1.1.

PROPOSITION 1 ([14], Theorem 1.1). Under Assumption 1, almost surely  $\bigotimes_{n\geq 1} \tilde{\mathbb{P}}_{n,d}$ ,  $(G_{n,d})_{n\geq 1}$  converges to the graphon  $W_D$  in the cut-metric, as  $n\to\infty$ , where  $W_D$  is given by

(1.9) 
$$W_D(x, y) := \frac{e^{\beta(x) + \beta(y)}}{1 + e^{\beta(x) + \beta(y)}},$$

where  $\beta:[0,1] \mapsto \mathbb{R}$  is the unique function satisfying  $D(x) = \int_0^1 \frac{e^{\beta(x)+\beta(y)}}{1+e^{\beta(x)+\beta(y)}} dy$ , for all  $x \in [0,1]$ .

Note that, under Assumption 1,  $\|\beta\|_{\infty} < \infty$ , which follows using [14], Lemma 4.1. Thus,  $W_D$  is away from the boundary for any degree function D satisfying Assumption 1 in the sense of Definition 5.

- 1.2. Main results. Our main result, Theorem 2, stated below, derives a LDP for the sequence of probability measures  $\tilde{\mathbb{P}}_{n,d}$ . To this end, for the convenience of the reader, we start with recalling the formal notion of a large deviation principle (LDP). Let  $\mathcal{X}$  be a Polish space with Borel sigma-algebra  $\mathcal{B}$ . Let  $I: \mathcal{X} \to [0, \infty]$  be a lower semicontinuous function. A sequence of probability measures  $(\mathbb{P}_n)_{n\geq 1}$  on  $(\mathcal{X}, \mathcal{B})$  satisfies a large deviation principle (LDP) with speed  $s_n \nearrow \infty$  and good rate function I if:
  - (i) for all  $\alpha \ge 0$ , the level sets  $\{x : I(x) \le \alpha\}$  are compact,
  - (ii) for any closed set  $F \subset \mathcal{X}$  and open set  $U \subset \mathcal{X}$

(1.10) 
$$\limsup_{n \to \infty} \frac{1}{s_n} \log \mathbb{P}_n(F) \le -\inf_{x \in F} I(x) \quad \text{and}$$

$$\liminf_{n \to \infty} \frac{1}{s_n} \log \mathbb{P}_n(U) \ge -\inf_{x \in U} I(x).$$

Next, we introduce the candidate rate function in our context. For W,  $W_0 \in \mathcal{W}$  with  $0 < W_0 < 1$  a.s., we define

$$I_{W_0}(W) = \frac{1}{2} \int_{[0,1]^2} \left[ W(x,y) \log \left( \frac{W(x,y)}{W_0(x,y)} \right) + \left( 1 - W(x,y) \right) \log \left( \frac{1 - W(x,y)}{1 - W_0(x,y)} \right) \right] dx dy$$

$$= \frac{1}{2} \sup_{a} \int_{[0,1]^2} \left[ a(x,y) W(x,y) - \log \left( W_0(x,y) e^{a(x,y)} + 1 - W_0(x,y) \right) \right] dx dy,$$

<span id="page-4-0"></span>where the supremum over a in the final term ranges over all functions in  $L^2([0,1]^2)$  satisfying a(x,y)=a(y,x) for all  $(x,y)\in [0,1]^2$  (for a proof of this variational characterization, see [11], Lemma 5.2). When W takes values 0 or 1, we use the convention that  $x\log x=0$  to define the integrand in the first equality of (1.11). Unlike the rate function for the Erdős-Rényi random graph in [15], (7), the function  $I_{W_0}(\cdot)$  is not well-defined on the quotient space  $\tilde{W}$ , that is,  $I_{W_0}(W_1)$  is not necessarily equal to  $I_{W_0}(W_2)$ , for  $W_1 \sim W_2$ . To produce a valid candidate, we use the notion of a lower semicontinuous envelope. Let  $\mathbb{B}_{\square}(\tilde{W},\eta):=\{g:\delta_{\square}(\tilde{W},\tilde{g})\leq \eta\}$ , and define

(1.12) 
$$J_{W_0}(\tilde{W}) = \sup_{\eta > 0} \inf_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta)} I_{W_0}(g).$$

Note that  $J_{W_0}$  is well defined on  $\tilde{\mathcal{W}}$ . Further,  $J_{W_0}$  is lower semicontinuous on  $(\tilde{\mathcal{W}}, \delta_{\square})$  (see Lemma 6), that is, the lower level sets  $\{\tilde{W}: J_{W_0}(\tilde{W}) \leq \alpha\}$  are closed, and therefore compact due to the compactness of  $(\tilde{\mathcal{W}}, \delta_{\square})$ . Thus,  $J_{W_0}$  is a good rate function.

Next recall the definition of  $W_D$  from (1.9). The degree distribution function of  $W_D$  is the inverse of D, that is,

(1.13) 
$$\mu_D([0,\lambda]) = \deg_{\tilde{W}_D}(\lambda) = \Lambda\{x : D(x) \le \lambda\}.$$

Define

(1.14) 
$$J_D(\tilde{W}) = \begin{cases} J_{W_D}(\tilde{W}) & \text{if } \deg_{\tilde{W}}(\lambda) = \mu_D([0, \lambda]), \forall \lambda \in [0, 1], \\ \infty & \text{otherwise.} \end{cases}$$

Using [8], Theorem 2.16, (see also (4.13) below),  $\{\tilde{W}: \deg_{\tilde{W}}(\lambda) = \mu_D([0,\lambda]), \forall \lambda \in [0,1]\}$  is closed in  $(\tilde{W}, \delta_{\square})$ —this establishes that  $J_D$  is also a good rate function. Given this candidate rate function, we state our main result.

THEOREM 2. Under Assumption 1, the sequence of probability measures  $(\tilde{\mathbb{P}}_{n,d})_{n\geq 1}$  on  $(\tilde{\mathcal{W}}, \delta_{\square})$  satisfies a LDP with speed  $n^2$  and good rate function  $J_D$  defined in (1.14).

For the particular case of a random d-regular graph, Assumption 1 holds when  $d = \lfloor np \rfloor$  for some  $p \in (0,1)$  (see [14], Remark 3), and thus Proposition 1 and Theorem 2 are applicable. In this case,  $W_D = p$ , and we will show that the LDP rate function simplifies (see Lemma 9 for a proof). Define

(1.15) 
$$J_p(\tilde{W}) = \begin{cases} I_p(W) & \text{if } \deg_{\tilde{W}}(\lambda) = \mathbb{1}\{p \le \lambda\}, \forall \lambda \in [0, 1], \\ \infty & \text{otherwise.} \end{cases}$$

Note that  $I_p(W_1) = I_p(W_2)$  for any  $W_1 \sim W_2$ , thus  $I_p$  is well defined on  $(\widetilde{W}, \delta_{\square})$ . The following corollary states the corresponding LDP for the random regular graph. Let  $p \in (0, 1)$  and  $d = \lfloor np \rfloor$ . Consider the degree sequence  $d = d\mathbf{1}$ , and for this case simply denote the probability measure associated to the random regular graph by  $\tilde{\mathbb{P}}_{n,d}$ .

COROLLARY 3. The sequence of probability measures  $(\tilde{\mathbb{P}}_{n,d})_{n\geq 1}$  on  $(\tilde{\mathbb{W}}, \delta_{\square})$  satisfies a LDP with speed  $n^2$  and good rate function  $J_p$  defined in (1.15).

As the main application of their LDP, Chatterjee and Varadhan [15] derived the LDPs for subgraph counts of Erdős–Rényi random graphs. Under the constraint on the number of edges, Dembo and Lubetzky [18] also proved LDP results for subgraph counts. Below we state the corresponding results for  $G_{n,d}$ .

<span id="page-5-0"></span>Let  $\tau : \widetilde{\mathcal{W}} \mapsto \mathbb{R}$  be bounded and continuous with respect to  $\delta_{\square}$ . The LDP statement for  $\tau$  below will directly imply the LDP for subgraph counts of  $G_{n,d}$ , using the continuity of subgraph densities. Define the rate function

(1.16) 
$$\phi_{\tau}(D,r) = \inf\{J_D(\tilde{W}) : \tau(\tilde{W}) \ge r\}.$$

Also, denote  $\tilde{\mathcal{W}}_0 = \{\tilde{W} \in \tilde{\mathcal{W}} : \deg_{\tilde{W}} \equiv \mu_D\}$  and

$$(1.17) l_{\tau}(D) = \tau(\tilde{W}_D), r_{\tau}(D) = \sup\{r : \{\tilde{W} \in \tilde{W}_0 : \tau(\tilde{W}) \ge r\} \ne \emptyset\}.$$

Let  $\tau_{n,d}$  be the value of  $\tau$  computed on the empirical graphon of  $G_{n,d}$ . Below we state the LDP result for  $\tau_{n,d}$ :

COROLLARY 4. Let  $\tau$  be a bounded, continuous function on  $(\tilde{W}, \delta_{\square})$ . Then the following are true:

- (1) The function  $\phi_{\tau}(D, \cdot)$  is left continuous, zero on  $[0, l_{\tau}(D)]$ , and finite, strictly positive on  $(l_{\tau}(D), r_{\tau}(D)]$ .
  - (2) Let r be any right continuity point of  $\phi_{\tau}(D,\cdot)$ . Then, under Assumption 1,

(1.18) 
$$\lim_{n \to \infty} \frac{1}{n^2} \log \mathbb{P}(\tau_{n,d} \ge r) = -\phi_{\tau}(D, r).$$

(3) Let  $F_{\star,r}$  be the set of minimizers in (1.16). Under Assumption 1, for all  $\varepsilon > 0$ , there exists  $C = C(\varepsilon, \tau, D, r) > 0$  such that

(1.19) 
$$\limsup_{n \to \infty} \frac{1}{n^2} \log \mathbb{P}(\delta_{\square}(W^{G_{n,d}}, F_{\star,r}) \ge \varepsilon | \tau_{n,d} \ge r) \le -C.$$

Chatterjee and Diaconis [13] used the LDP for Erdős–Rényi random graphs to evaluate the limit of the partition function associated with exponential random graphs [13], Theorem 3.1. In a related direction, setting  $\mathcal{G}_{n,d}$  to be the set of all simple graphs on n vertices with degree sequence d, we consider the probability measure on  $\mathcal{G}_{n,d}$  defined by

(1.20) 
$$\mathbb{P}_{n,d,\tau}(G) = e^{n^2(\tau(\tilde{W}^G) - Z_{n,\tau})}, \quad \forall G \in \mathcal{G}_{n,d},$$

where  $\tau$  is a bounded continuous function on  $(\tilde{W}, \delta_{\square})$ , and  $Z_{n,\tau} = \frac{1}{n^2} \log \sum_{G \in \mathcal{G}_{n,d}} e^{n^2 \tau (\tilde{W}^G)}$ . We will refer to  $Z_{n,\tau}$  as the microcanonical partition function. Its limiting value is naturally associated with the enumeration problem of graphs with given degrees and constrained subgraph counts (see (1.23) below). Our next corollary derives the limit of the microcanonical partition function. To this end, define the entropy function

(1.21) 
$$h_e(W) = \frac{1}{2} \int_{[0,1]^2} [W(x, y) \log(W(x, y)) + (1 - W(x, y)) \log(1 - W(x, y))] dx dy.$$

Finally, let  $N_{n,\tau}(\boldsymbol{d},r)$  denote the number of graphs  $G \in \mathcal{G}_{n,\boldsymbol{d}}$  with  $\tau(\tilde{W}^G) \geq r$ .

COROLLARY 5. Let  $\tau$  be a bounded continuous function on  $(\tilde{W}, \delta_{\square})$ . Under Assumption 1,

(1.22) 
$$Z_{\tau} = \lim_{n \to \infty} Z_{n,\tau} = \sup_{\tilde{W} \in \tilde{\mathcal{W}}} \left( \tau(\tilde{W}) - J_D(\tilde{W}) \right) + h_e(W_D).$$

*Moreover, for any continuity point r of*  $\phi_{\tau}(D, \cdot)$ *,* 

(1.23) 
$$\lim_{n \to \infty} \frac{1}{n^2} \log N_{n,\tau}(\boldsymbol{d}, r) = -\phi_{\tau}(D, r) + h_e(W_D).$$

## <span id="page-6-0"></span>1.3. *Discussion*.

*The variational problem*. Corollary [4](#page-5-0) characterizes the probability of a rare event in terms of a variational problem [\(1.16\)](#page-5-0). From the perspective of large deviation theory, the natural follow-up question concerns the structure of *Gn,<sup>d</sup>* , conditioned on the rare event. Using [\(1.19\)](#page-5-0), this conditional structure corresponds to the minimizers of [\(1.16\)](#page-5-0). The variational problem [\(1.16\)](#page-5-0) has attracted significant attention in the Erdos–Rényi case. For instance, it is ˝ now understood that in the so-called replica symmetric regime, conditioned on the upper tail event for triangle counts, the graph is close to an Erdos–Rényi with a higher edge density ˝ [\[34\]](#page-25-0). Note that the replica symmetric regime is no longer tenable under exact constraints, such as a fixed number of edges, triangles, degrees, etc. In a set of related papers, [\[28–30,](#page-25-0) [41\]](#page-25-0) study the structure of the minimizer under constraints on the edge, triangle or star counts, and discover intriguing characteristics of the minimizers. However, to the best of our knowledge, this problem has not been studied under degree constraints. We expect this case to be considerably more challenging than the prior settings.

A careful reader has noticed that Corollary [4\(](#page-5-0)2) holds when *r* is a continuity point of *φτ (D,*·*)*. For Erdos–Rényi random graphs, the continuity of this function has been estab- ˝ lished, when *τ* represents a subgraph density, the largest eigenvalue, etc. [\[11,](#page-24-0) [34\]](#page-25-0). Their proof is perturbative, and the idea does not generalize to the setting with given degrees. In fact, *φτ (D,*·*)* could be degenerate in constrained spaces. For example, the largest eigenvalue of random *d*-regular graphs equals *d*, and thus the rate function is degenerate. More generally, a deterministic function of the degrees, for example, any *k*-star density, is constant in this case, and gives rise to degenerate rate functions.

*Counting graphs with given degrees and subgraph densities*. Counting graphs with given degrees has been studied extensively in combinatorics [\[2,](#page-24-0) [32,](#page-25-0) [37,](#page-25-0) [46\]](#page-26-0). For example, [\[2\]](#page-24-0), Theorem 1.4, evaluates the leading asymptotics of the number of graphs with given degrees, and expresses it in terms of an entropy. Corollary [5](#page-5-0) yields a formula for the asymptotic number of graphs with given degrees and a specified subgraph count. However, this description is completely implicit, and explicit solutions for general degree sequences could be significantly challenging.

*The sparse regime*. The breakthrough result of Chatterjee and Varadhan [\[15\]](#page-24-0) completely resolved the question of large deviations for subgraph counts of dense Erdos–Rényi random ˝ graphs. The corresponding question for sparse Erdos–Rényi random graphs ˝ *G(n,p)* with *p* → 0 has intrigued researchers in probability and combinatorics for a long time. For any fixed graph *H* and *δ >* 0, the infamous upper tail problem sought to understand the probability that the number of copies of *H* in *G(n,p)* exceeds *(*1 + *δ)* times its expectation. Perhaps surprisingly, it is even difficult to come up with a good general guess as to what the correct order of the exponential rate of decay is. This can be observed in a class of counter-examples to the DeMarco–Kahn upper tail conjecture, constructed by Sileikis and Warnke [ ˘ [43\]](#page-25-0). To address this challenging question, Chatterjee and Dembo [\[12\]](#page-24-0) initiated the theory of nonlinear large deviations. They establish that for any fixed subgraph *H* and *δ >* 0, the upper tail probability reduces to a variational problem on the space of weighted graphs whenever *p* → 0, *p* ≥ *n*−*αH* . Remarkably, the variational problem was solved in the special case where *H* is a clique by Lubetzky and Zhao [\[35\]](#page-25-0) shortly thereafter. Subsequently, Bhattacharya, Ganguly, Lubetzky and Zhao [\[3\]](#page-24-0) resolved this question for all fixed subgraphs. Following the initial breakthrough of Chatterjee and Dembo [\[12\]](#page-24-0), the exponent *αH* was improved considerably by Eldan [\[21\]](#page-25-0). Recently, Cook and Dembo [\[16\]](#page-24-0), Augeri [\[1\]](#page-24-0), and Harel, Mousset and Samotij [\[26\]](#page-25-0) have further improved the bounds on *αH* , deriving the optimal exponent for certain specific subgraphs such as cycles, cliques, regular graphs etc.

<span id="page-7-0"></span>These exciting recent developments have dramatically improved our understanding of the upper tail problem on sparse Erdős–Rényi random graphs. It would be fascinating to answer this question for sparse random graphs with a given degree sequence. In fact, the simpler question of enumeration of all graphs with a given degree sequence is not very well understood at present. We believe these questions furnish a fertile ground for future research. After the first version of this paper was posted online, there have been recent interesting developments for sparse d-regular random graphs. For  $n^{1-\varepsilon(H)} \ll d \ll n$  (where  $\varepsilon(H)$  is explicit), Bhattacharya and Dembo [4] resolved the upper tail problem for subgraphs H having a regular two-core. Recently, Gunby [24] considered general subgraphs H, solving the upper tail problem when some subgraph  $H' \subset H$  has average degree greater than 4.

Follow up works on LDP for block models. Since the first version of this article was submitted for publication, the second author, in collaboration with C. Borgs, J. Chayes, J. Gaudio and S. Petti [7] proved the LDP for block-constant base graphons  $W_0$  (with rational block lengths) avoiding the "away from the boundary" condition. They further identify a "reentrant phase transition" phenomenon in the corresponding upper tail variational problem. This LDP was extended to block-constant base graphons (with possibly irrational block lengths) in the work of Grebík and Pikhurko [23].

**2. Properties of the rate function.** Recall the definition of  $J_{W_0}$  from (1.12). In this section, we will prove some elementary facts about  $J_{W_0}$ , that will be crucial in our proofs. Throughout, we denote  $\tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta) = \{\tilde{W}' : \delta_{\square}(\tilde{W}, \tilde{W}') \leq \eta\}$  and  $\mathbb{B}_{\square}(\tilde{W}, \eta) = \{W' : \tilde{W}' \in \tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta)\}$ . We first prove the lower semicontinuity of our rate function.

LEMMA 6. The function  $J_{W_0}(\tilde{W}) = \sup_{\eta>0} \inf_{W' \in \mathbb{B}_{\square}(\tilde{W}, \eta)} I_{W_0}(W')$  is well defined on the space  $\tilde{W}$ . Moreover,  $J_{W_0}$  is lower semicontinuous on  $(\tilde{W}, \delta_{\square})$ .

PROOF. For any  $W_1 \sim W_2$ , it follows that  $\{W' : \delta_{\square}(\tilde{W}_1, \tilde{W}') \leq \delta\} = \{W' : \delta_{\square}(\tilde{W}_2, \tilde{W}') \leq \delta\}$ , and therefore  $J_{W_0}$  is well defined on  $\tilde{\mathscr{W}}$ . Define the function  $H : \tilde{\mathscr{W}} \mapsto [0, \infty]$  by  $H(\tilde{W}') = \inf_{g: \delta_{\square}(\tilde{W}', \tilde{g}) = 0} I_{W_0}(g)$ . Now,

$$(2.1) \quad J_{W_0}(\tilde{W}) = \sup_{\eta > 0} \inf_{W' \in \mathbb{B}_{\square}(\tilde{W}, \eta)} I_{W_0}(W') = \sup_{\eta > 0} \inf_{\tilde{W}' \in \tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta)} H(\tilde{W}') = \liminf_{\tilde{W}' \to \tilde{W}} H(\tilde{W}'),$$

and it is a standard fact in analysis that the function obtained by taking pointwise  $\liminf$  of a function must be lower semicontinuous. This completes the proof.  $\square$ 

The next result shows that the relative entropy between W and  $W_0$  is zero if and only if they are in the same equivalence class.

LEMMA 7. 
$$J_{W_0}(\tilde{W}) = 0$$
 if and only if  $\delta_{\square}(\tilde{W}, \tilde{W}_0) = 0$ .

PROOF. The sufficiency part is obvious. To see the necessity, assume  $J_{W_0}(\tilde{W})=0$ . In this case, there exists  $(g_n)_{n\geq 1}\subset \mathscr{W}$  with  $\delta_{\square}(\tilde{g}_n,\tilde{W})\to 0$  such that  $I_{W_0}(g_n)\to 0$ . Using Taylor expansion, one immediately obtains

(2.2) 
$$\frac{1}{2} \int_{[0,1]^2} \left[ g_n(x,y) \log \left( \frac{g_n(x,y)}{W_0(x,y)} \right) + \left( 1 - g_n(x,y) \right) \log \left( \frac{1 - g_n(x,y)}{1 - W_0(x,y)} \right) \right] dx dy$$
$$\geq \int_{[0,1]^2} \left( g_n(x,y) - W_0(x,y) \right)^2 dx dy.$$

<span id="page-8-0"></span>Next, using Cauchy–Schwarz inequality,  $\|g_n - W_0\|_{L_1} \to 0$ , and consequently  $\delta_{\square}(\tilde{g}_n, \tilde{W}_0) \to 0$ . Thus,  $\delta_{\square}(\tilde{W}, \tilde{W}_0) \leq \delta_{\square}(\tilde{g}_n, \tilde{W}) + \delta_{\square}(\tilde{g}_n, \tilde{W}_0) \to 0$  as  $n \to \infty$ . This completes the proof.  $\square$ 

Next we will prove that if we have a sequence  $W_0^n$  converging to  $W_0$  in  $L_1$ , then the corresponding rate functions converge as well.

LEMMA 8. Suppose that  $\|W_0^n - W_0\|_{L_1} \to 0$ , and that  $(W_0^n)_{n \ge 1}$  is away from boundary. Then,  $J_{W_0^n}(\tilde{W}) \to J_{W_0}(\tilde{W})$  uniformly over  $W \in \mathcal{W}$ , as  $n \to \infty$ .

PROOF. Let  $\eta > 0$  be such that  $\eta < W_0^n < 1 - \eta$  for all  $n \ge 1$ . By taking limit as  $n \to \infty$ , we also have that  $\eta < W_0 < 1 - \eta$  almost surely. Thus, using the Lipschitz continuity of the log function, it follows that for all x, y,

$$(2.3) \quad \max\left\{\left|\log\left(\frac{W_0^n(x,y)}{W_0(x,y)}\right)\right|, \left|\log\left(\frac{1-W_0^n(x,y)}{1-W_0(x,y)}\right)\right|\right\} \le c\left|W_0^n(x,y)-W_0(x,y)\right|,$$

for some constant c > 0. Now,

$$|I_{W_0^n}(W) - I_{W_0}(W)|$$

$$= \left| \int_{[0,1]^2} W(x,y) \log \left( \frac{W_0^n(x,y)}{W_0(x,y)} \right) + (1 - W(x,y)) \log \left( \frac{1 - W_0^n(x,y)}{1 - W_0(x,y)} \right) dx dy \right|$$

$$\leq c \int_{[0,1]^2} |W_0^n(x,y) - W_0(x,y)| dx dy = c \|W_0^n - W_0\|_{L_1}.$$

The proof now follows upon using the definition of the rate function, and noting the bound in the final term of (2.4) is uniform over  $W \in \mathcal{W}$ .  $\square$ 

We finally conclude this section by showing that for the special case of random regular graphs, the relative entropy reduces to the form given in (1.15).

LEMMA 9. Fix  $W \in \mathcal{W}$  and  $p \in (0, 1)$ . Then,  $J_p(\tilde{W}) = \sup_{\eta > 0} \inf_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta)} I_p(g) = I_p(W)$ .

PROOF. By [11], Corollary 5.1, whenever  $d_{\square}(W_n, W) \to 0$ , we have

(2.5) 
$$\liminf_{n \to \infty} I_p(W_n) \ge I_p(W).$$

Now let us denote  $I(\eta) := \inf_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta)} I_p(g)$ . Then  $I(0) = \inf_{g : \delta_{\square}(\tilde{g}, \tilde{W}) = 0} I_p(g) = I_p(W)$ , since  $I_p(W_1) = I_p(W_2)$  whenever  $W_1 \sim W_2$ . Also,  $I(\eta) \leq I(0)$ . Thus, in order to complete the proof, we need to show that  $I(0) = \sup_{\eta > 0} I(\eta)$ , that is, for all  $\varepsilon > 0$ ,  $\exists \eta(\varepsilon) > 0$  such that  $I(\eta) > I(0) - \varepsilon$  for all  $\eta \in (0, \eta(\varepsilon))$ . Suppose that this does not hold. Using [9], (3.15), there exists  $\varepsilon > 0$  and  $\eta_n \to 0$  such that  $I(\eta_n) \leq I(0) - \varepsilon$  for all  $n \geq 1$ . This implies that there exist  $(g_n)_{n \geq 1} \subset \mathscr{W}$  and  $(\phi_n)_{n \geq 1} \subset \mathscr{M}$  such that  $d_{\square}(W, g_n^{\phi_n}) \leq \eta_n$ , but  $I_p(g_n) < I(\eta_n) + \varepsilon/2 < I(0) - \varepsilon/2$  for all  $n \geq 1$ . Since  $I_p(g_n) = I_p(g_n^{\phi_n})$ , it follows that  $I_p(g_n^{\phi_n}) < I(0) - \varepsilon/2$ . Now, using (2.5), we have that  $I_p(W) < I(0) - \varepsilon/2$  which yields a contradiction because  $I(0) = I_p(W)$ .  $\square$ 

REMARK 1. In a recent preprint, Markering [36] derives a tractable form for the lower semicontinuous envelope  $J_{W_0}(\cdot)$  by showing that  $\sup_{\eta>0}\inf_{g\in\mathbb{B}_{\square}(\tilde{W},\eta)}I_{W_0}(g)=\inf_{\phi\in\mathscr{M}}I_{W_0}(g^{\phi})$  for any  $W_0$  such that  $\log W_0$ ,  $\log(1-W_0)\in L_1$ .

<span id="page-9-0"></span>**3.** An upper bound for inhomogeneous random graphs. In this section, we obtain a large deviation upper bound for inhomogeneous random graphs. Let  $\mathcal{W}^{(r)} \subset \mathcal{W}$  denote the space of block constant graphons with r equal-sized blocks, that is, for any  $g \in \mathcal{W}^{(r)}$ , we have  $g(x, y) = g_{ij}$  for all  $x, y \in [\frac{i-1}{r}, \frac{i}{r}) \times [\frac{j-1}{r}, \frac{j}{r})$ . To generate inhomogeneous random graphs on n vertices, we take  $g \in \mathcal{W}^{(n)}$  of the following special form with zeroes on the diagonal:

(3.1) 
$$g(x, y) = \begin{cases} g_{ij}, & x, y \in \left[\frac{i-1}{n}, \frac{i}{n}\right) \times \left[\frac{j-1}{n}, \frac{j}{n}\right), i \neq j, \\ 0 & \text{otherwise.} \end{cases}$$

We denote the collection of graphons in (3.1) by  $\mathscr{W}_{IRG}^{(n)}$ . Given any graphon  $W \in \mathscr{W}$ , consider the random graph  $G_n = G_n(W)$  on vertex set [n] obtained by keeping an edge between vertices i and j with probability W((i-1)/n,(j-1)/n). Let  $\mathbb{P}_{n,W}$  denote the probability measure on  $\mathscr{W}$  induced by the empirical graphon of  $G_n(W)$ , and let  $\tilde{\mathbb{P}}_{n,W}$  denote the corresponding measure on  $\widetilde{\mathscr{W}}$ . The following proposition derives the LDP upper bound for  $\mathbb{P}_{n,W_0^n}$  where  $W_0^n \in \mathscr{W}_{IRG}^{(n)}$ . Recall  $\tilde{\mathbb{B}}_{\square}(\tilde{W},\eta) = \{\tilde{W}': \delta_{\square}(\tilde{W},\tilde{W}') \leq \eta\}$  and  $\mathbb{B}_{\square}(\tilde{W},\eta) = \{W': \tilde{W}' \in \tilde{\mathbb{B}}_{\square}(\tilde{W},\eta)\}$ . For any  $W_0^n \in \mathscr{W}_{IRG}^{(n)}$ , the value in the diagonal blocks  $[\frac{i-1}{n},\frac{i}{n}) \times [\frac{i-1}{n},\frac{i}{n})$  is zero. Nevertheless, we say that  $(W_0^n)_{n\geq 1}$  with  $W_0^n \in \mathscr{W}_{IRG}^{(n)}$  is away from the boundary if there exists some fixed  $\eta > 0$  such that  $\eta < W_0^n(x,y) < 1-\eta$  in the nondiagonal blocks for all  $n \geq 1$ .

PROPOSITION 10. Fix  $\varepsilon > 0$ . Let  $W_0^n \in \mathcal{W}_{IRG}^n$  be such that  $\|W_0^n - W_0\|_{L_1} \to 0$ , and further assume that  $(W_0^n)_{n\geq 1}$  is away from boundary. Then, there exists  $\eta(\varepsilon) > 0$  such that for all  $\eta \in (0, \eta(\varepsilon))$ 

(3.2) 
$$\limsup_{n\to\infty} \frac{1}{n^2} \log \tilde{\mathbb{P}}_{n,W_0^n} (\tilde{\mathbb{B}}_{\square}(\tilde{W},\eta)) \leq -\inf_{f\in \mathbb{B}_{\square}(\tilde{W},4\varepsilon)} I_{W_0}(f) + \varepsilon.$$

REMARK 2. Proposition 10 proves LDP upper bound for inhomogeneous random graphs under the stated conditions. A matching lower bound can be derived following the arguments of [15], which shows that  $(\tilde{\mathbb{P}}_{n,W_0^n})_{n\geq 1}$  satisfies LDP with speed  $n^2$  and rate function  $J_{W_0}$ . For the constrained case, additional challenges arise in the proof of the lower bound which we deal with in Section 4.3.

Let  $\mathcal{M}_n$  be the set of permutations of [n]. For  $\sigma_n \in \mathcal{M}_n$ , let  $G_n^{\sigma_n}$  denote the graph with vertices relabelled according to the permutation  $\sigma_n$ . In the special case of Erdős–Rényi random graphs with  $W_0^n \equiv p$ , the distribution of  $G_n^{\sigma_n}$  is the same for all  $\sigma_n \in \mathcal{M}_n$ . This is a crucial ingredient in the LDP upper bound proof of Chatterjee and Varadhan [15], since the cut-metric also optimizes over all relabellings (see [15], Lemma 2.5). For general  $W_0^n$ , the distribution of  $G_n^{\sigma_n}$  depends on  $\sigma_n \in \mathcal{M}_n$ , and one needs to optimize the upper bound over all the n! relabellings, which grows with n. The argument for Erdős–Rényi random graph does not generalize for such an optimal relabelling. To this end, we proceed in two steps:

- (S1) We replace  $W_0^n$  by a block constant graphon  $g_r \in \mathcal{W}^{(r)}$  with fixed number of blocks that is "close" to  $W_0^n$ . The error due to such an operation is small when r is large, as we prove in Lemma 11.
- (S2) The next step is the key conceptual ingredient. If the base graphon  $g_r$  is a block constant, we can restrict ourselves to a finite number of relabellings without incurring significant error. Thus we only need to optimize over this finite set. We prove this in Lemma 12.

We formalize (S1) and (S2) in Sections 3.1 and 3.2 respectively. Finally, we complete the proof of Proposition 10 in Section 3.3.

<span id="page-10-0"></span>3.1. Replacing base graphon by block constants. The following statement allows us to replace  $W_0^n$  by a block constant graphon with fixed number of blocks in our LDP upper bound.

LEMMA 11. Let  $W_0^n \in \mathcal{W}_{IRG}^{(n)}$  be such that  $\|W_0^n - W_0\|_{L_1} \to 0$ , and  $(W_0^n)_{n \geq 1}$  is away from boundary. There exists  $(g_r)_{r \geq 1} \subset \mathcal{W}$  that is away from boundary such that  $g_r \in \mathcal{W}^{(r)}$ , and for all  $\varepsilon > 0$  (sufficiently small), there exists  $N_0 = N_0(\varepsilon)$  such that for all  $n \geq r \geq N_0$ ,  $W \in \mathcal{W}$  and  $\eta > 0$ 

$$\left| \frac{1}{n^2} \log \mathbb{P}_{n, W_0^n} \left( \mathbb{B}_{\square}(\tilde{W}, \eta) \right) - \frac{1}{n^2} \log \mathbb{P}_{n, g_r} \left( \mathbb{B}_{\square}(\tilde{W}, \eta) \right) \right| < \varepsilon.$$

PROOF. Define, for all  $(x, y) \in \left[\frac{i-1}{r}, \frac{i}{r}\right) \times \left[\frac{j-1}{r}, \frac{j}{r}\right]$ ,

(3.4) 
$$g_r(x,y) = g_{ij} = r^2 \int_{\left[\frac{i-1}{r}, \frac{i}{r}\right) \times \left[\frac{j-1}{r}, \frac{j}{r}\right)} W_0(u,v) \, \mathrm{d}u \, \mathrm{d}v.$$

Using [11], Proposition 2.6,  $\|g_r - W_0\|_{L_1} \to 0$  as  $r \to \infty$ , and thus it follows that for all  $\varepsilon > 0$ , there exists  $N_0$  such that, for all  $r, n \ge N_0$ ,  $\|g_r - W_0^n\|_{L_1} < \varepsilon$ . Also, since  $W_0$  is away from the boundary, so is  $(g_r)_{r \ge 1}$ . Now, note that

$$(3.5) \qquad \mathbb{P}_{n,W_0^n}(\mathbb{B}_{\square}(\tilde{W},\eta)) = \int_{\mathbb{B}_{\square}(\tilde{W},\eta)} e^{\log \frac{d\mathbb{P}_{n,W_0^n}}{d\mathbb{P}_{n,g_r}}} d\mathbb{P}_{n,g_r}.$$

Let  $(w_{uv})_{1 \le u < v \le n}$  be the block constant values of  $W_0^n$ . Thus, for  $I_{uv} \in \{0, 1\}$ , and  $n \ge r$ ,

(3.6) 
$$\log \left[ \frac{d\mathbb{P}_{n,W_0^n}}{d\mathbb{P}_{n,g_r}} (I_{uv})_{u < v} \right] = \sum_{1 \le i \le j \le r} \sum_{\substack{u < v \\ \frac{u-1}{r} \in \left[\frac{i-1}{r}, \frac{i}{r}\right), \frac{v-1}{n} \in \left[\frac{j-1}{r}, \frac{j}{r}\right)}} \left( I_{uv} \log \left( \frac{w_{uv}}{g_{ij}} \right) + (1 - I_{uv}) \log \left( \frac{1 - w_{uv}}{1 - g_{ij}} \right) \right).$$

Thus, for any  $(I_{uv})_{u < v}$ ,

$$\frac{1}{n^{2}} \left| \log \frac{d\mathbb{P}_{n,W_{0}^{n}}}{d\mathbb{P}_{n,g_{r}}} (I_{uv})_{u < v} \right| \\
\leq \frac{1}{n^{2}} \sum_{1 \leq i \leq j \leq r} \sum_{\substack{u = 1 \\ \frac{u-1}{n} \in \left[\frac{i-1}{r}, \frac{i}{r}\right), \frac{v-1}{n} \in \left[\frac{j-1}{r}, \frac{j}{r}\right)}} \left( \left| \log \left(\frac{w_{uv}}{g_{ij}}\right) \right| + \left| \log \left(\frac{1 - w_{uv}}{1 - g_{ij}}\right) \right| \right) \\
\leq C \left\| W_{0}^{n} - g_{r} \right\|_{L_{1}} < C\varepsilon,$$

for some constant C > 0, and for all  $n \ge r \ge N_0$ , where in the last step we have used the Lipschitz continuity of log on  $[c_1, c_2]$  with  $0 < c_1 < c_2 < \infty$ , and the fact that  $(g_r)_{r \ge 1}$  and  $(W_0^n)_{n \ge 1}$  are away from the boundary. Now, (3.5) yields that

$$(3.8) \mathbb{P}_{n,W_0^n}(\mathbb{B}_{\square}(\tilde{W},\eta)) \leq e^{C\varepsilon n^2} \mathbb{P}_{n,g_r}(\mathbb{B}_{\square}(\tilde{W},\eta)).$$

Thus the proof follows by replacing  $C\varepsilon$  by  $\varepsilon$ .  $\square$ 

<span id="page-11-0"></span>3.2. Approximation of relabelled graphs. Recall that  $G_n^{\sigma_n}$  is obtained from the graph  $G_n$  by relabelling the vertices with the permutation  $\sigma_n \in \mathcal{M}_n$ . The next result shows that, for all large enough n, we can construct a finite set of relabellings which can be used to approximate the distributions of  $G_n^{\sigma_n}$  for all  $\sigma_n \in \mathcal{M}_n$ . Recall the definition of  $\mathcal{M}$  from Section 1.1.1.

LEMMA 12. Suppose that  $W_0, W \in \mathcal{W}^{(r)}$  with  $r \geq 1$ . Then, for any  $\varepsilon > 0$ , there exists  $n_0 = n_0(r, \varepsilon)$ , and a finite set  $\mathcal{T} = \mathcal{T}(r, \varepsilon) \subset \mathcal{M}$  such that for all  $n \geq n_0$  and  $\sigma_n \in \mathcal{M}_n$ , there exists  $\tau \in \mathcal{T}$  satisfying

$$(3.9) \mathbb{P}_{n,W_0}(d_{\square}(W^{G_n^{\sigma_n}},W) \leq \varepsilon) \leq \mathbb{P}_{n,W_0}(d_{\square}(W^{G_n,\tau},W) \leq 2\varepsilon).$$

PROOF. We write  $A_i = [\frac{i-1}{r}, \frac{i}{r}]$  for  $i \in [r]$ . For a vertex  $v \in [n]$ , we say that v is in the interval  $A \subset [0, 1]$ , denoted by  $v \rightsquigarrow A$ , if  $[\frac{v-1}{n}, \frac{v}{n}) \subset A$ . Without loss of generality, we take  $n \geq r$ , so that any vertex can be in at most one  $A_i$ . Let  $C_{ij}(\sigma_n) = \{v : v \leadsto A_i, \sigma_n(v) \leadsto A_j\}$ . Thus, if we think of  $v \leadsto A_i$  as a vertex of type i, then  $|C_{ij}(\sigma_n)|$  counts the number of type i vertices that get mapped into  $A_j$  under the permutation  $\sigma_n$ . The basic idea of the proof is that since  $W_0$  and W are block constants, the distribution of  $d_{\square}(W^{G_n^{\sigma_n}}, W)$  and  $d_{\square}(W^{G_n^{\tau_n}}, W)$  remains the same if  $|C_{ij}(\sigma_n)| = |C_{ij}(\tau_n)|$  for all i, j. Thus, if  $\tau \in \mathscr{M}$  be such that the number of type-i vertices that get mapped to block j under  $\tau$  is approximately  $|C_{ij}(\sigma_n)|$ , then distributions of  $d_{\square}(W^{G_n^{\sigma_n}}, W)$  and  $d_{\square}(W^{G_n^{\sigma_n}}, W)$  are approximately close. Below, we make this intuition precise.

Fix  $t \in T$ , where

$$(3.10) T := \left\{ (t_{ij})_{i,j \in [r]} : t_{ij} \in (0,1), t_{ij} = t_{ji}, \sum_{i \in [r]} t_{ij} = \frac{1}{r}, \sum_{j \in [r]} t_{ij} = \frac{1}{r} \right\},$$

and let

(3.11) 
$$\mathcal{M}_n(\boldsymbol{t},\eta) = \left\{ \sigma_n \in \mathcal{M}_n : \frac{|C_{ij}(\sigma_n)|}{n} \in (t_{ij} - \eta, t_{ij} + \eta), \forall i, j \in [r] \right\}.$$

Thus,  $\mathcal{M}_n(t, \eta)$  identifies the class of permutations under which  $A_j$  consists roughly of  $nt_{ij}$  many type-i vertices (when  $\eta$  is small). Also, we write

(3.12) 
$$A_{ij} = \left[ \frac{i-1}{r} + \sum_{k=1}^{j-1} t_{ik}, \frac{i-1}{r} + \sum_{k=1}^{j} t_{ik} \right).$$

Now, consider  $\tau \in \mathcal{M}$  satisfying

(3.13) 
$$\tau(A_{ij}) = A_{ji}, \quad \forall i, j \in [r].$$

More precisely, we take  $\tau$  to be  $\tau(x) = c_{ij} + x$  for  $x \in A_{ij}$ , where  $c_{ij}$ 's are chosen so that (3.13) is satisfied. The map  $\tau$  can be understood as follows. The interval  $A_{ij}$  contains roughly  $nt_{ij}$  many type-i vertices, which are the only type-i vertices to get mapped to the interval  $A_j$ . Thus, under  $\tau$ ,  $A_j$  contains roughly  $nt_{ij}$  many type-i vertices. Note also that after  $\tau$  has been applied, the labels of vertices of type-i inside each block are "sorted" in increasing order.

Next, we claim that, for any  $\varepsilon > 0$ , there exists  $\eta_0 = \eta_0(\varepsilon) > 0$  and  $n_0 = n_0(r, \varepsilon)$  (independent of t) such that for any  $\eta \in (0, \eta_0)$ ,  $n \ge n_0$  and  $\sigma_n \in \mathcal{M}_n(t, \eta)$ , there exists a coupling between  $d_{\square}(W^{G_n^{\sigma_n}}, W)$  and  $d_{\square}(W^{G_n, \tau}, W)$  such that

$$(3.14) \mathbb{P}(|d_{\square}(W^{G_n^{\sigma_n}}, W) - d_{\square}(W^{G_{n,\tau}}, W)| > \varepsilon) = 0.$$

The proof of (3.14) goes as follows: Given any composition  $t \in T$ , we choose a "sorted" measurable bijection  $\tau$  given by (3.13). Then we fix  $\sigma_n$  which has approximate composition t.

<span id="page-12-0"></span>We re-arrange so that it is also in sorted form within blocks. Finally, we couple these sorted models.

We write  $\tau(v) \rightsquigarrow A_j$  if  $\tau([\frac{v-1}{n}, \frac{v}{n})) \subset A_j$ . Let  $C_{ij}(\tau) = \{v : v \rightsquigarrow A_i, \tau(v) \rightsquigarrow A_j\}$ . By construction,  $||C_{ij}(\tau)| - nt_{ij}| \le 1$ . Also, for any  $\sigma_n \in \mathcal{M}_n(t, \eta)$ ,  $||C_{ij}(\sigma_n)| - nt_{ij}| \le 2\eta n$ . Let  $n_{ij} = \min\{C_{ij}(\tau), C_{ij}(\sigma_n)\}$ . Thus  $A_j$  contains at least  $n_{ij}$  many type-i vertices, both under  $\sigma_n$  and  $\tau$ . Let  $\sigma_n^0 \in \mathcal{M}_n$  be such that  $\sigma_n^0$  permutes vertices within blocks  $A_j$  only, and  $\sigma_n^0$  sorts the different types of vertices within blocks in ascending order. More formally,  $\sigma_n^0$  satisfies:

- (1) For  $\sigma_n(u) \rightsquigarrow A_i$ , we have  $\sigma_n^0 \circ \sigma_n(u) \rightsquigarrow A_i$ .
- (2) For  $u \leadsto A_{i_1}$  and  $v \leadsto A_{i_2}$  with  $i_1 < i_2$ , we have  $\sigma_n^0 \circ \sigma_n(u) < \sigma_n^0 \circ \sigma_n(v)$ . (3) For  $u, v \leadsto A_i$  with u < v, we have  $\sigma_n^0 \circ \sigma_n(u) < \sigma_n^0 \circ \sigma_n(v)$ .

Now we couple the edges between  $n_{ij}$  many vertices between the blocks. More precisely,  $W^{G_n^{\sigma_n}}$  and  $W^{G_n,\tau}$  are coupled such that there is an edge between  $\sigma_n^0 \circ \sigma_n(u)$  and  $\sigma_n^0 \circ \sigma_n(v)$  if and only if  $W^{G_n,\tau}$  takes value 1 on  $\tau([\frac{u-1}{n},\frac{u}{n})) \times \tau([\frac{v-1}{n},\frac{v}{n}))$ . This indeed gives a coupling because an application of permutations such as  $\sigma_n^0$  which only permutes the vertices within blocks, does not change the distribution of  $d_{\square}(W^{G_n^{\sigma_n}}, W)$ . Note that this coupling does not specify the edges incident to at most  $2\eta n + 2$  many vertices. This can cause an error of at most  $3\eta$  in  $L_1$ -norm, and hence an error of at most  $3\eta$  in the cut-norm. Taking  $\eta(\varepsilon) = \varepsilon/3$ , the proof of (3.14) follows.

Finally, consider any finite set  $(t_{\alpha})_{\alpha} \subset T$  such that for any  $s \in T$ , there exists  $\alpha$  with  $\|s - t_{\alpha}\|_{\infty} < \eta$ . The proof follows by choosing a  $\tau$  satisfying (3.14) for each  $t_{\alpha}$ .  $\square$ 

3.3. Proof of Proposition 10. Fix  $\varepsilon > 0$ . Recall the setup of Proposition 10. Using Lemma 11, it suffices to prove that there exists  $\eta(\varepsilon) > 0$  such that for all  $\eta \in (0, \eta(\varepsilon))$ 

$$(3.15) \qquad \limsup_{n \to \infty} \frac{1}{n^2} \log \tilde{\mathbb{P}}_{n,g_r} (\tilde{\mathbb{B}}_{\square}(\tilde{W},\eta)) \le -\inf_{f \in \mathbb{B}_{\square}(\tilde{W},4\varepsilon)} I_{W_0}(f),$$

where  $g_r$  is chosen according to Lemma 11. First, note that

$$(3.16) \tilde{\mathbb{P}}_{n,g_r}(\tilde{\mathbb{B}}_{\square}(\tilde{W},\eta)) = \mathbb{P}_{n,g_r}(\mathbb{B}_{\square}(\tilde{W},\eta)).$$

Next, we recall a version of Szemerédi's regularity lemma from [11], Theorem 3.1, that will be crucial here (see [45] for the original formulation). There exists  $C(\varepsilon) > 0$  and a set  $\mathcal{W}(\varepsilon) \subset$  $\mathcal{W}$  with  $|\mathcal{W}(\varepsilon)| \leq C(\varepsilon)$  such that the following holds:

For any  $f \in \mathcal{W}$ , there exists  $\phi \in \mathcal{M}$  and  $h \in \mathcal{W}(\varepsilon)$  satisfying  $d_{\square}(f^{\phi}, h) < \varepsilon$ .

Moreover, for any  $h \in \mathcal{W}(\varepsilon)$ , there exists  $s \geq 1$  such that  $h \in \mathcal{W}^{(s)}$ . Without loss of generality, we can additionally assume that the elements of  $\mathcal{W}(\varepsilon)$  are graphons with blocks of equal size. To see this, note that we can approximate each element of  $\mathcal{W}(\varepsilon)$  in  $L_2$  by a graphon with equal-sized blocks (see [11], Proposition 2.6).

For empirical graphons corresponding to graphs, the above can be restated as below (see [11], Theorem 3.1(iii)): Recall that  $\mathcal{M}_n$  denotes the set of all permutations of [n], and  $G_n^{\sigma_n}$ denotes the graph obtained by relabelling the vertex i by  $\sigma_n(i)$ , for some  $\sigma_n \in \mathcal{M}_n$ . Also let us denote  $B_{\square}(W, \eta) = \{W' : d_{\square}(W, W') \leq \eta\}$ . Then, for any graph  $G_n$  on vertex set [n], there exists  $\sigma_n \in \mathcal{M}_n$  and  $h \in \mathcal{W}(\varepsilon)$  such that

$$(3.17) W^{G_n^{\sigma_n}} \in \mathbf{B}_{\square}(h, \varepsilon).$$

Let  $G_n$  be the random graph sampled from the probability distribution  $\mathbb{P}_{n,g_r}$ . We define  $B_{\square}(\mathcal{W}(\varepsilon), \varepsilon) = \{g \in \mathcal{W} : \min_{h \in \mathcal{W}(\varepsilon)} d_{\square}(g, h) < \varepsilon\},$  and note that the above version of the <span id="page-13-0"></span>regularity lemma implies that

$$\{W^{G_n} \in \mathbb{B}_{\square}(\tilde{W}, \eta)\}$$

$$\subseteq \{W^{G_n} \in \mathbb{B}_{\square}(\tilde{W}, \eta)\} \cap \left(\bigcup_{\sigma_n \in \mathcal{M}_n} \{W^{G_n^{\sigma_n}} \in \mathcal{B}_{\square}(\mathcal{W}(\varepsilon), \varepsilon)\}\right)$$

$$= \bigcup_{h \in \mathcal{W}(\varepsilon)} \bigcup_{\sigma_n \in \mathcal{M}_n} \{W^{G_n} \in \mathbb{B}_{\square}(\tilde{W}, \eta)\} \cap \{W^{G_n^{\sigma_n}} \in \mathcal{B}_{\square}(h, \varepsilon)\}.$$

Now,  $\mathcal{W}(\varepsilon)$  is a finite set. Therefore it is enough to show that

(3.19) 
$$\limsup_{n \to \infty} \frac{1}{n^2} \log \mathbb{P}_{n,g_r} \left( \bigcup_{\sigma_n \in \mathcal{M}_n} \left\{ W^{G_n} \in \mathbb{B}_{\square}(\tilde{W},\eta) \right\} \cap \left\{ W^{G_n^{\sigma_n}} \in \mathbb{B}_{\square}(h,\varepsilon) \right\} \right) \\ \leq -\inf_{f \in \mathbb{B}_{\square}(\tilde{W},4\varepsilon)} I_{W_0}(f),$$

where  $h \in \mathcal{W}(\varepsilon)$ . Let  $\eta < \varepsilon$ . If the event in (3.19) is empty, then the bound is trivial. In order for the event (3.19) to be nonempty, we must have that  $\delta_{\square}(\tilde{W}^{G_n}, \tilde{W}) \leq \eta < \varepsilon$  and  $\delta_{\square}(\tilde{W}^{G_n}, \tilde{h}) \leq \varepsilon$ , so that  $\delta_{\square}(\tilde{W}, \tilde{h}) \leq 2\varepsilon$ . Now, applying Lemma 12 yields that the left-hand side of (3.19) is at most

(3.20) 
$$\lim \sup_{n \to \infty} \frac{1}{n^2} \log \mathbb{P}_{n,g_r} \left( \bigcup_{\sigma_n \in \mathscr{M}_n} \left\{ W^{G_n^{\sigma_n}} \in \mathcal{B}_{\square}(h,\varepsilon) \right\} \right)$$

$$\leq \lim \sup_{n \to \infty} \frac{1}{n^2} \max_{\sigma_n \in \mathscr{M}_n} \log \mathbb{P}_{n,g_r} \left( \left\{ W^{G_n^{\sigma_n}} \in \mathcal{B}_{\square}(h,\varepsilon) \right\} \right)$$

$$\leq \lim \sup_{n \to \infty} \frac{1}{n^2} \max_{\tau \in \mathcal{T}} \log \mathbb{P}_{n,g_r} \left( \left\{ W^{G_n,\tau} \in \mathcal{B}_{\square}(h,2\varepsilon) \right\} \right),$$

where, in the second step, we have also used the fact that  $\log n! = o(n^2)$ . Since  $\mathcal{T}$  is a finite set, it is now enough to show that for each  $\tau \in \mathcal{T}$ 

$$(3.21) \qquad \limsup_{n \to \infty} \frac{1}{n^2} \log \mathbb{P}_{n,g_r} \left( W^{G_n,\tau} \in \mathcal{B}_{\square}(h,2\varepsilon) \right) \le -\inf_{f \in \mathbb{B}_{\square}(\tilde{W},4\varepsilon)} I_{W_0}(f).$$

Now, by [11], Lemma 5.4,  $B_{\square}(h, 2\varepsilon)$  is closed with respect to the weak topology. Thus we apply [11], Theorem 5.1. Although [11], Theorem 5.1, was stated for the constant graphon, an identical argument could be used to generalize this argument to block constant graphon  $g_r$ . Therefore, (3.21) is at most

$$(3.22) \quad -\inf_{\phi^{-1}\in\mathscr{M}}\inf_{f\in\mathcal{B}_{\square}(h^{\phi},2\varepsilon)}I_{g_{r}}(f)\leq -\inf_{f\in\mathcal{B}_{\square}(\tilde{h},2\varepsilon)}I_{g_{r}}(f)\leq -\inf_{f\in\mathcal{B}_{\square}(\tilde{W},4\varepsilon)}I_{g_{r}}(f).$$

Now, taking  $r \to \infty$ , using Lemma 8 (note that Lemma 8 is stated in terms of  $W_0^n$ , the desired conclusion follows upon substituting  $g_r$  in place of  $W_0^n$ ), the proof follows.

**4.** Large deviation for uniform graphs with given degree. In this section, we complete the proof of Theorem 2. Using the fact that  $(\tilde{W}, \delta_{\square})$  is a compact metric space, it is sufficient (see remarks associated to [19], Theorem 4.5.3, and [11], Lemma 4.1) to show that for any  $\tilde{W} \in \tilde{W}$ ,

(4.1) 
$$\lim_{\eta \to 0} \limsup_{n \to \infty} \frac{1}{n^2} \log \tilde{\mathbb{P}}_{n,d} (\tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta)) \leq -J_D(\tilde{W}),$$

and for any  $\eta > 0$ 

(4.2) 
$$\liminf_{n \to \infty} \frac{1}{n^2} \log \tilde{\mathbb{P}}_{n,d} (\tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta)) \ge -J_D(\tilde{W}).$$

<span id="page-14-0"></span>4.1. Key facts from Chatterjee, Diaconis and Sly [14]. Let us first recall a few key ingredients from [14], which were used to obtain the graphon limit of  $G_{n,d}$ . Let  $\hat{\beta} = (\hat{\beta}_i)_{i \in [n]}$  be the solution to the system of equations

(4.3) 
$$d_i = \sum_{j \neq i} \frac{e^{\hat{\beta}_i + \hat{\beta}_j}}{1 + e^{\hat{\beta}_i + \hat{\beta}_j}}, \quad \forall i \in [n].$$

Due to [14], Lemma 4.1,  $\hat{\beta}$  exists and  $\|\hat{\beta}\|_{\infty} \le C$  for some constant C > 0 for all sufficiently large n under Assumption 1. It is not obvious that Assumption 1 yields the conditions in [14], Lemma 4.1, but that too was shown in the first part of the proof of [14], Theorem 1.1, in Section 6.2. Next, for any  $i \ne j$ , define

(4.4) 
$$\hat{p}_{ij} = \frac{e^{\hat{\beta}_i + \hat{\beta}_j}}{1 + e^{\hat{\beta}_i + \hat{\beta}_j}},$$

and let  $\hat{G}_n$  be the random graph on vertex set [n] obtained by keeping an edge between vertices i and j with probability  $\hat{p}_{ij}$ , independently. Define

(4.5) 
$$W_{n,d}(x,y) = \begin{cases} \hat{p}_{ij} & \text{for } x, y \in \left[\frac{i-1}{n}, \frac{i}{n}\right) \times \left[\frac{j-1}{n}, \frac{j}{n}\right) \text{ and } i \neq j, \\ 0 & \text{otherwise.} \end{cases}$$

Since  $\|\hat{\boldsymbol{\beta}}\|_{\infty} \leq C$ , it follows that  $(W_{n,d})_{n\geq 1}$  is away from the boundary. Therefore, the results from Section 3 are applicable to  $(W_{n,d})_{n\geq 1}$ . Next, let  $D_n:[0,1]\mapsto [0,1]$  be the step function given by

(4.6) 
$$D_n(x) = \frac{1}{n} \sum_{i \neq i} \hat{p}_{ij} = \frac{d_i}{n}, \quad \forall x \in \left[ \frac{i-1}{n}, \frac{i}{n} \right) \text{ and } \forall i \in [n],$$

and the degree distribution function is given by

(4.7) 
$$\mu_{D_n}([0,\lambda)) = \Lambda\{x : D_n(x) \le \lambda\}.$$

By Assumption 1,  $||D_n - D||_{L_1} \to 0$ , and thus

$$\mu_{D_n} \xrightarrow{w} \mu_{D_n}$$

where  $\mu_D$  is defined in (1.13), where  $\stackrel{w}{\to}$  denotes the weak convergence of measures. Define  $\beta_n(x) = \sum_{i=1}^n \hat{\beta}_i \mathbb{1}\{x \in [\frac{i-1}{n}, \frac{i}{n})\}$ . Chatterjee, Diaconis and Sly [14], page 1430–1432, established that

(4.9) 
$$\|\beta_n - \beta\|_{L_1} \to 0, \qquad \|W_{n,d} - W_D\|_{L_1} \to 0,$$

where  $\beta$  and  $W_D$  are defined in Proposition 1. This fact is critical in our subsequent large deviation analysis.

Next, recall that  $\mathcal{W}_0 = \{W \in \mathcal{W} : \deg_{\tilde{W}} = \mu_D\}$  and define  $\mathcal{W}_0^n = \{W \in \mathcal{W} : \deg_{\tilde{W}} = \mu_{D_n}\}$ . Note that formally,  $\deg_{\tilde{W}}$  refers to a cumulative distribution function, and not to the associated probability measure. We use these notions interchangeably, and do not overload the notation henceforth. Given any graphon  $W_0^n \in \mathcal{W}_{\mathrm{IRG}}^{(n)}$ , recall the definition of the probability measure  $\mathbb{P}_{n,W_0^n}$  from Section 3. Note that, under  $\mathbb{P}_{n,W_{n,d}}$  with  $W_{n,d}$  given by (4.5), the probability of producing a particular graph with degree sequence d is given by  $\mathrm{e}^{\sum_{i \in [n]} \hat{\beta}_i d_i} / \prod_{i < j} (1 + \mathrm{e}^{\hat{\beta}_i + \hat{\beta}_j})$ . Therefore, the conditional law of  $\mathbb{P}_{n,W_{n,d}}$ , conditionally on degree sequence d, is uniform among all the graphs with degree sequence d. More formally,

$$(4.10) \qquad \mathbb{P}_{n,W_{n,d}}(\cdot|\mathscr{W}_0^n) = \mathbb{P}_{n,d}(\cdot).$$

<span id="page-15-0"></span>Next we quote a key lemma from [14] which will be used in the proof: Let  $(r_{ij})_{i\neq j}$  satisfy  $r_{ij} = r_{ji}$ ,  $r_{ii} = 0$  and  $\sum_{j\in[n]\setminus\{i\}} r_{ij} = d_i$ , and construct a random graph  $G_n$  on the vertex set [n] by keeping an edge between i and j with probability  $r_{ij}$ .

LEMMA 13 ([14], Lemma 6.2). For all sufficiently large n,  $G_n$  has degree sequence exactly  $\mathbf{d}$  with probability at least  $e^{-n^{7/4}}$ .

A direct corollary of Lemma 13 is the following:

$$(4.11) \mathbb{P}_{n,W_{n,d}}(\mathcal{W}_0^n) \ge e^{-n^{7/4}},$$

for all sufficiently large n. We are now ready to prove our LDP result.

4.2. Proof of the upper bound (4.1). Define the Lévy–Prokhorov distance [39] between two distribution functions  $F_1$ ,  $F_2$  supported on [0, 1] by

$$(4.12) d_{LP}(F_1, F_2) = \inf\{\varepsilon > 0 : F_2(\lambda - \varepsilon) - \varepsilon \le F_1(\lambda) \le F_2(\lambda + \varepsilon) + \varepsilon, \forall \lambda \in [0, 1]\}.$$

This distance can be naturally defined for any two probability measures supported on [0,1] (via their distribution functions), and induces a metric on this space. In fact,  $d_{LP}$  metrizes the weak convergence of probability measures on [0,1] (see [39]). Using [8], Theorem 2.16, it follows that

$$(4.13) d_{LP}(\deg_{\tilde{W}_1}, \deg_{\tilde{W}_2}) \le \left(2\delta_{\square}(\tilde{W}_1, \tilde{W}_2)\right)^{1/2}.$$

To prove (4.1), we will be assuming that  $\tilde{W} \in \tilde{\mathcal{W}}_0$ . If that is not the case, then the logarithm of probability in (4.1) is  $-\infty$  for all sufficiently large n and small  $\eta$ . To see this, suppose  $\tilde{W} \in \tilde{\mathcal{W}}$  is such that  $d_{LP}(\deg_{\tilde{W}}, \mu_D) = c > 0$ . Since  $d_{LP}(\mu_{D_n}, \mu_D) \to 0$  by (4.8), it follows that, for all sufficiently large n,  $d_{LP}(\deg_{\tilde{W}}, \mu_{D_n}) \ge c/2$ . Take  $\eta_0 = c^2/32$ . Now, for any  $\tilde{U} \in \tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta_0)$ 

$$\frac{c}{2} \leq d_{LP}(\deg_{\tilde{W}}, \mu_{D_n})$$

$$\leq d_{LP}(\deg_{\tilde{W}}, \deg_{\tilde{U}}) + d_{LP}(\deg_{\tilde{U}}, \mu_{D_n})$$

$$\leq \frac{c}{4} + d_{LP}(\deg_{\tilde{U}}, \mu_{D_n}),$$

for all sufficiently large n, where the final step follows from (4.13). Thus  $d_{LP}(\deg_{\tilde{U}}, \mu_{D_n}) \ge c/4$  for all  $\tilde{U} \in \tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta_0)$ , and thus  $\tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta_0)) = 0$ .

Therefore, we will assume that  $\deg_{\tilde{W}} = \mu_D$ . Note that,

$$(4.15) \qquad \tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{W},\eta)) = \mathbb{P}_{n,d}(\mathbb{B}_{\square}(\tilde{W},\eta))$$

$$= \frac{\mathbb{P}_{n,W_{n,d}}(\mathbb{B}_{\square}(\tilde{W},\eta) \cap \mathscr{W}_{0}^{n})}{\mathbb{P}_{n,W_{n,d}}(\mathscr{W}_{0}^{n})}$$

$$\leq e^{n^{7/4}}\mathbb{P}_{n,W_{n,d}}(\mathbb{B}_{\square}(\tilde{W},\eta)),$$

where the second equality follows from (4.10) and the last step follows from (4.11). Now, using Proposition 10, for any  $\varepsilon > 0$ , there exists  $\eta(\varepsilon) > 0$  such that for all  $\eta \in (0, \eta(\varepsilon))$ , we have

$$(4.16) \qquad \limsup_{n \to \infty} \frac{1}{n^2} \log \tilde{\mathbb{P}}_{n,d} \left( \tilde{\mathbb{B}}_{\square}(\tilde{W}, \eta) \right) \leq -\inf_{f \in \mathbb{B}_{\square}(\tilde{W}, 4\varepsilon)} I_{W_D}(f) + \varepsilon.$$

Consequently, (4.1) follows upon sending  $\eta \to 0$  and then  $\varepsilon \to 0$ .

<span id="page-16-0"></span>4.3. Proof of the lower bound (4.2). Fix  $\tilde{W} \in \tilde{\mathcal{W}}$  such that  $\deg_{\tilde{W}} = \mu_D$ , otherwise the rate function is  $-\infty$ , and the lower bound is trivial. Recall that  $\mathcal{W}_0 = \{W \in \mathcal{W} : \deg_{\tilde{W}} = \mu_D\}$ , and the definition of  $\hat{G}_n$  from Section 4.1. Define the event

$$\mathcal{E}_n = \{ \exists g \in \mathcal{W}_0 \text{ with } \delta_{\square}(\tilde{g}, \tilde{W}) \leq \eta \text{ such that } \delta_{\square}(\tilde{W}^{G_{n,d}}, \tilde{g}) \leq \eta \}.$$

Note that, if  $\mathcal{E}_n$  happens, then  $\delta_{\square}(\tilde{W}^{G_{n,d}}, \tilde{g}) \leq \eta$ , and therefore, by the triangle inequality,  $\delta_{\square}(\tilde{W}^{G_{n,d}}, \tilde{W}) \leq 2\eta$ . Next, note that for any collection of events  $(A_{\alpha})_{\alpha \in \mathcal{A}}$ ,  $\mathbb{P}(\bigcup_{\alpha \in \mathcal{A}} A_{\alpha}) \geq \max_{\alpha \in \mathcal{A}} \mathbb{P}(A_{\alpha})$ . Thus, we have

$$(4.17) \qquad \qquad \tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{W},2\eta)) \geq \tilde{\mathbb{P}}_{n,d}(\mathcal{E}_n) \geq \sup_{g \in \mathbb{B}_{\square}(\tilde{W},n) \cap \mathscr{W}_0} \tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{g},\eta)).$$

The lower bound on (4.17) may seem artificial at first, but its technical significance will become clear later in (4.31), (4.32), while proving the LDP lower bound in terms of the lower semicontinuous envelope  $J_{W_D}$ . Our focus will be to lower bound  $\tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{g},\eta))$ . The following lemma is a crucial ingredient which states that graphons with any fixed degree distribution function can be approximated by piecewise constant graphons with approximately the same degree function. We first state this lemma and complete the proof of the lower bound. The proof of the lemma is given at the end of this section. Recall the definition of  $\mathcal{W}_{\text{IRG}}^{(n)}$  from Section 3. For  $h_n \in \mathcal{W}_{\text{IRG}}^{(n)}$ , let  $(h_{ij})_{i,j \in [n]}$  be the values of  $h_n$  on the blocks  $S_{ij}$ , where  $S_{ij} := [\frac{i-1}{n}, \frac{i}{n}) \times [\frac{j-1}{n}, \frac{j}{n})$ . For any  $\sigma_n \in \mathcal{M}_n$ , we define the graphon  $h_n^{\sigma_n}$  by  $h_n^{\sigma_n}(x,y) = h_{\sigma_n(i)\sigma_n(j)}$  for all  $x, y \in S_{ij}$ ,  $i, j \in [n]$ .

LEMMA 14. Let  $g \in \mathcal{W}_0$ , that is,  $\deg_{\tilde{g}} = \mu_D$ . Further, let  $D_n$  be a step function of the form (4.6) such that  $\|D_n - D\|_{L_1} \to 0$ . There exist graphons  $(g_n)_{n\geq 1}$  and  $(\sigma_{0n})_{n\geq 1}$  with  $\sigma_{0n} \in \mathcal{M}_n$  such that  $\|g_n^{\sigma_{0n}} - g\|_{L_1} \to 0$ , and there exists an  $n_0$  (independent of g) such that for all  $n \geq n_0$ , we have  $\int_0^1 g_n(x, y) \, \mathrm{d}y = D_n(x)$ , and

(4.18) 
$$g_n(x, y) = \begin{cases} g_{ij}, & x, y \in \left[\frac{i-1}{n}, \frac{i}{n}\right) \times \left[\frac{j-1}{n}, \frac{j}{n}\right), i \neq j, \\ 0 & otherwise \end{cases}$$

where  $n^{-1} < g_{ij} < 1 - n^{-1}$ .

Next, since  $\|D_n - D\|_{L_1} \to 0$  by Assumption 1, using Lemma 14, we can construct a function  $g_n$  with  $\delta_{\square}(\tilde{g}_n, \tilde{g}) \to 0$  such that (4.18) holds, and  $\sum_{j \in [n] \setminus \{i\}} g_{ij} = d_i$  for all  $i \in [n]$ . Also let  $G_n$  denote the graph on vertex set [n], where an edge between vertices i and j are kept with probability  $h_{ij} = g_{\sigma_{0n}(i)\sigma_{0n}(j)}$ , independently, where  $\sigma_{0n} \in \mathcal{M}_n$  is given by Lemma 14. Let  $\mathbb{P}_{n,h_n}$  denote the distribution of  $W^{G_n}$ . By our construction in Lemma 14, we have that  $\|h_n - g\|_{L_1} \to 0$ . Using (4.10), we can write

$$\tilde{\mathbb{P}}_{n,d}(\tilde{\mathbb{B}}_{\square}(\tilde{g},\eta)) = \frac{\mathbb{P}_{n,W_{n,d}}(\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n})}{\mathbb{P}_{n,W_{n,d}}(\mathcal{W}_{0}^{n})} \geq \int_{\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n}} d\mathbb{P}_{n,W_{n,d}} d\mathbb{P}_{n,W_{n,d}}$$

$$= \int_{\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n}} e^{-\log\frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}}} d\mathbb{P}_{n,h_{n}}$$

$$= \mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n}) \frac{1}{\mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n})}$$

$$\times \int_{\mathbb{B}_{\square}(\tilde{g},\eta)\cap\mathcal{W}_{0}^{n}} e^{-\log\frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}}} d\mathbb{P}_{n,h_{n}}.$$

<span id="page-17-0"></span>Now, taking logarithms and using Jensen's inequality, the above is at least

(4.20) 
$$\log \mathbb{P}_{n,h_n} \left( \mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_0^n \right) \\ - \frac{1}{\mathbb{P}_{n,h_n} \left( \mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_0^n \right)} \int_{\mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_0^n} \log \frac{d\mathbb{P}_{n,h_n}}{d\mathbb{P}_{n,W_{n,d}}} d\mathbb{P}_{n,h_n}.$$

Denote the two terms above by (I) and (II) respectively. To deal with the term (I), we need the following lemma.

LEMMA 15. For any  $\eta > 0$ , as  $n \to \infty$ ,

$$(4.21) \mathbb{P}_{n,h_n}(\mathbb{B}_{\square}(\tilde{g},\eta)|\mathscr{W}_0^n) \to 1.$$

PROOF. We denote the random graph sampled according to probability measures  $\mathbb{P}_{n,h_n}(\cdot)$  by  $G_n$ ,  $h_n = g_n^{\sigma_{0n}}$ , and recall the definition of subgraph densities from Definition 3. Since  $\delta_{\square}(\tilde{g}_n, \tilde{g}) \to 0$ , it follows using [33] that  $t(F, g_n, Lemma\ 10.23) \to t(F, g)$  for any finite simple graph F. It is enough to show that,  $t(F, W^{G_n}) \to t(F, g)$  almost surely with respect to the measure  $\bigotimes_{n\geq 1} \mathbb{P}_{n,h_n}(\cdot|\mathcal{W}_0^n)$  for any fixed finite simple graph F, since then the proof will follow using [33], Lemma 10.32.

First,  $\mathbb{E}_{n,h_n}[t(F, W^{G_n})] = t(F, g_n) \to t(F, g)$ , and a standard argument using the bounded difference inequality (cf. [14], Lemma 6.1) yields for any  $\varepsilon > 0$ 

$$(4.22) \mathbb{P}_{n,h_n}(|t(F,W^{G_n}) - \mathbb{E}_{n,h_n}[t(F,W^{G_n})]| > \varepsilon) \le 2e^{-C\varepsilon^2 n^2},$$

for some constant C > 0. Now, recall that  $\sum_{j \neq i} g_{ij} = d_i$  by construction. We aim to apply Lemma 13.  $h_{ij}$  is obtained from  $g_{ij}$  by vertex relabelling, and thus Lemma 13 is also applicable to  $G_n$ . Thus, it follows that

$$\mathbb{P}_{n,h_{n}}(|t(F, W^{G_{n}}) - \mathbb{E}_{n,h_{n}}[t(F, W^{G_{n}})]| > \varepsilon | \mathscr{W}_{0}^{n})$$

$$= \frac{\mathbb{P}_{n,h_{n}}(\{|t(F, W^{G_{n}}) - \mathbb{E}_{n,h_{n}}[t(F, W^{G_{n}})]| > \varepsilon\} \cap \mathscr{W}_{0}^{n})}{\mathbb{P}_{n,h_{n}}(\mathscr{W}_{0}^{n})}$$

$$\leq \frac{\mathbb{P}_{n,h_{n}}(|t(F, W^{G_{n}}) - \mathbb{E}_{n,h_{n}}[t(F, W^{G_{n}})]| > \varepsilon)}{\mathbb{P}_{n,h_{n}}(\mathscr{W}_{0}^{n})} \leq 2e^{-Cn^{2}},$$

for some constant C > 0. Now the required almost sure convergence follows using the Borel–Cantelli lemma. This completes the proof.  $\Box$ 

Completing the proof of the lower bound. Note that, by Lemmas 13 and 15, the term (I) in (4.20) simplifies to

$$(4.24) (I) = \log \mathbb{P}_{n,h_n} (\mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_0^n) = \log \mathbb{P}_{n,h_n} (\mathcal{W}_0^n) + o(1) \ge -Cn^{7/4} = o(n^2),$$

for some constant C > 0. To analyze term (II), first note that

(4.25) 
$$\log \frac{d\mathbb{P}_{n,h_n}}{d\mathbb{P}_{n,W_{n,d}}} = \sum_{1 \le i \le j \le n} \left( I_{ij} \log \left( \frac{h_{ij}}{\hat{p}_{ij}} \right) + (1 - I_{ij}) \log \left( \frac{1 - h_{ij}}{1 - \hat{p}_{ij}} \right) \right),$$

where  $I_{ij} \sim \text{Ber}(h_{ij})$  independently, and  $\hat{p}_{ij}$  is defined in (4.4). By changing one  $I_{ij}$ , this quantity can change by at most

(4.26) 
$$\max_{i,j} \left| \log \left( \frac{h_{ij}}{\hat{p}_{ij}} \right) \right| + \left| \log \left( \frac{1 - h_{ij}}{1 - \hat{p}_{ij}} \right) \right| \le C \log n,$$

<span id="page-18-0"></span>using the condition from Lemma 14 that  $n^{-1} < g_{ij} < 1 - n^{-1}$ , and  $W_D$  (and thus also  $(W_{n,d})_{n \ge 1}$ ) is away from the boundary. Therefore, an application of the Azuma–Hoeffding inequality [10], Theorem 2.8, yields

$$(4.27) \qquad \mathbb{P}_{n,h_n}\left(\left|\log\frac{\mathrm{d}\mathbb{P}_{n,h_n}}{\mathrm{d}\mathbb{P}_{n,W_{n,d}}} - \mathbb{E}_{n,h_n}\left[\log\frac{\mathrm{d}\mathbb{P}_{n,h_n}}{\mathrm{d}\mathbb{P}_{n,W_{n,d}}}\right]\right| > \varepsilon_n n^2 \log n\right) \le 2\mathrm{e}^{-C'\varepsilon_n^2 n^2},$$

for some constant C' > 0 which depends on the constant in (4.26). We denote the event in (4.27) by  $A_n$ . Take  $\varepsilon_n = n^{-1/10}$ . Note that, on  $A_n^c$ ,

(4.28) 
$$\log \frac{d\mathbb{P}_{n,h_n}}{d\mathbb{P}_{n,W_n,d}} \leq \mathbb{E}_{n,g_n} \left[ \log \frac{d\mathbb{P}_{n,h_n}}{d\mathbb{P}_{n,W_n,d}} \right] + n^{19/10}.$$

Also note that, by (4.26), the log derivative  $\log \frac{d\mathbb{P}_{n,h_n}}{d\mathbb{P}_{n,W_n,d}}$  is at most  $Cn^2 \log n$ . Therefore,

$$(II) \leq \frac{1}{\mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_{0}^{n})} \int_{\mathcal{W}_{0}^{n}} \log \frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}} d\mathbb{P}_{n,h_{n}}$$

$$\leq \frac{1}{\mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_{0}^{n})} \left(\mathbb{E}_{n,h_{n}} \left[\log \frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}}\right] + n^{19/10}\right) \mathbb{P}_{n,h_{n}}(\mathcal{W}_{0}^{n})$$

$$+ \frac{(2Cn^{2}\log n)e^{-C'n^{9/5}}}{\mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta) \cap \mathcal{W}_{0}^{n})}$$

$$= \frac{1}{\mathbb{P}_{n,h_{n}}(\mathbb{B}_{\square}(\tilde{g},\eta)|\mathcal{W}_{0}^{n})} \left(\mathbb{E}_{n,h_{n}} \left[\log \frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}}\right] + o(n^{2})\right) + o(n^{2})$$

$$= (1 + o(1))\mathbb{E}_{n,h_{n}} \left[\log \frac{d\mathbb{P}_{n,h_{n}}}{d\mathbb{P}_{n,W_{n,d}}}\right] + o(n^{2}),$$

where the last-but-one step follows applying (4.24), and the last step use Lemma 15. Further, since  $||h_n - g||_{L_1} \to 0$ , we also have  $||h_n - g||_{L_2} \to 0$  since  $h_n$ , g takes values in a bounded interval [0, 1], and consequently, (4.25) yields that

(4.30) 
$$\lim_{n \to \infty} \frac{1}{n^2} \mathbb{E}_{n, h_n} \left[ \log \frac{\mathrm{d} \mathbb{P}_{n, h_n}}{\mathrm{d} \mathbb{P}_{n, W_{n, d}}} \right] = I_{W_D}(g).$$

See also [11], Lemma 5.7, for more details for proving an analogue of (4.30) with  $W_D = p$ . The argument here is identical. Thus, combining (4.24), (4.29) and (4.30), we have

(4.31) 
$$\liminf_{n\to\infty} \frac{1}{n^2} \log \widetilde{\mathbb{P}}_{n,d} (\widetilde{\mathbb{B}}_{\square}(\widetilde{g},\eta)) \ge -I_{W_D}(g).$$

Thus, (4.17) yields that

$$\lim_{n \to \infty} \inf \frac{1}{n^{2}} \log \tilde{\mathbb{P}}_{n,d} (\tilde{\mathbb{B}}_{\square}(\tilde{W}, 2\eta)) \geq \lim_{n \to \infty} \inf_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta) \cap \mathcal{W}_{0}} \frac{1}{n^{2}} \log \tilde{\mathbb{P}}_{n,d} (\tilde{\mathbb{B}}_{\square}(\tilde{g}, \eta))$$

$$\geq \sup_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta) \cap \mathcal{W}_{0}} \liminf_{n \to \infty} \frac{1}{n^{2}} \log \tilde{\mathbb{P}}_{n,d} (\tilde{\mathbb{B}}_{\square}(\tilde{g}, \eta))$$

$$\geq -\inf_{g \in \mathbb{B}_{\square}(\tilde{W}, \eta) \cap \mathcal{W}_{0}} I_{W_{D}}(g),$$

which concludes the proof of the lower bound in (4.2).

It remains to prove Lemma 14. To this end, we will need the following ingredient: For any Borel measurable function  $g:[0,1]\mapsto [0,1]$ , let  $m_g(z)=\Lambda(\{y:g(y)>z\})$ , where we recall that  $\Lambda$  is the Lebesgue measure.

<span id="page-19-0"></span>LEMMA 16. Let  $(f_n)_{n\geq 1}$  and f be such that  $f_n$ ,  $f:[0,1]\mapsto [0,1]$  are nonincreasing, Borel measurable functions. Suppose that  $\lim_{n\to\infty} m_{f_n}(z) = m_f(z)$  for all continuity points z of  $m_f$ . Then, as  $n\to\infty$ ,  $||f_n-f||_{L_1}\to 0$ .

PROOF. For any Borel measurable function  $g:[0,1] \mapsto [0,1]$ , the monotone rearrangement is defined as  $g^*(x) = \inf\{z : m_g(z) \le x\}$ . We will prove the following two facts about the monotone rearrangement:

FACT 1. If f is nonincreasing, then  $f^* = f$  almost surely.

FACT 2. If  $m_{f_n}(z) \to m_f(z)$  for all continuity points z of  $m_f$ , then  $f_n^* \to f^*$  almost surely, as  $n \to \infty$ .

Using Facts 1, and 2, it follows that  $f_n \to f$  almost surely. Thus the proof follows by the dominated convergence theorem.  $\square$ 

PROOF OF FACT 1. Since f is nonincreasing, we have that  $\{y : f(y) > f(x)\} \subset \{y : y \le x\}$ . This implies  $m_f(f(x)) = \Lambda(\{y : f(y) > f(x)\}) \le x$ , and thus  $f^*(x) = \inf\{z : m_f(z) \le x\} \le f(x)$ . Now, let x be a continuity point of f, and fix  $\varepsilon > 0$ . Then,  $m_f(f(x) - \varepsilon) = \Lambda(\{y : f(y) > f(x) - \varepsilon\}) > x$ . Now, since  $m_f$  is nonincreasing, whenever  $m_f(z) \le x$ , we have  $z > f(x) - \varepsilon$ . This implies that  $f^*(x) \ge f(x) - \varepsilon$ , and thus  $f^*(x) = f(x)$  whenever x is a continuity point of f. Now, the proof follows using the fact that any nonincreasing function can only have countably many points of discontinuity.  $\square$ 

PROOF OF FACT 2. First note that, whenever  $z_n \setminus z$ , we have  $m_f(z_n) \nearrow m_f(z)$ , and thus  $m_f$  is right-continuous. Next, for any  $z < f^*(x)$ , we have  $m_f(z) > x$ . Let z be a continuity point of  $m_f$ . Since  $m_{f_n}(z) \to m_f(z)$ , for all sufficiently large n, we have  $m_{f_n}(z) > x$ , and thus  $z \le \liminf_{n \to \infty} f_n^*(x)$ . Therefore,  $\liminf_{n \to \infty} f_n^*(x) \ge f^*(x)$ .

Next, let x be a continuity point of  $f^*$ , that is, for all  $\varepsilon > 0$ , there exists a  $\delta > 0$  such that  $f^*(x - \delta) < f^*(x) + \varepsilon$ . Define  $\xi = \limsup_{n \to \infty} f_n^*(x)$ . Then, there exists  $(n_k)_{k \ge 1} \subset \mathbb{N}$  such that for all  $k \ge 1$ ,  $f_{n_k}^*(x) > \xi - \varepsilon$ , and thus  $m_{f_{n_k}}(\xi - \varepsilon) > x$ . Now, since  $m_f$  has countably many points of discontinuity, we can choose  $\varepsilon > 0$  such that  $\xi - \varepsilon$  is a continuity point of  $m_f$ . This implies that  $m_f(\xi - \varepsilon) \ge x > x - \delta$ , and thus  $f^*(x - \delta) > \xi - \varepsilon$ . Thus,  $f^*(x) > \xi - 2\varepsilon = \limsup_{n \to \infty} f_n^*(x) - 2\varepsilon$ . The proof again follows using the fact that  $f^*$  can have only countably many points of discontinuity.  $\square$ 

PROOF OF LEMMA 14. Recall that  $\mathcal{W}_{IRG}^{(n)}$  denotes the collection of piecewise constant graphons defined below (3.1), and also that  $S_{ij} := [\frac{i-1}{n}, \frac{i}{n}) \times [\frac{j-1}{n}, \frac{j}{n})$ . For  $W \in \mathcal{W}_{IRG}^{(n)}$ , we write  $W_{ij}$  to denote the value of W on  $S_{ij}$ . In order to produce a block-constant graphon that is close to g and degree function exactly equal to  $D_n$ , we proceed via following steps.

Step 1: Approximation by block constant graphons. For  $1 \le i \ne j \le n$ , define

(4.33) 
$$g_{n1}(x, y) = n^2 \int_{S_{ij}} g(u, v) \, du \, dv, \quad \forall (x, y) \in S_{ij},$$

and  $g_{n1}(x, y) = 0$  otherwise. A standard argument implies that  $||g_{n1} - g||_{L_2} \to 0$  (see [11], Proposition 2.6). Since g is bounded, we also have  $||g_{n1} - g||_{L_1} \to 0$ .

Step 2:  $L_1$ -approximation of the degree function. Let  $\sigma_n$  be any permutation such that  $(\sum_{j\in[n]}g_{n1,\sigma_n(i)\sigma_n(j)})_{i\in[n]}$  is nonincreasing, and let  $g_{n2}$  take value  $g_{n1,\sigma_n(i)\sigma_n(j)}$  on  $S_{ij}$ . Since  $\|g_{n1}-g\|_{L_1}\to 0$ , it follows that  $\|g_{n2}^{\sigma_{0n}}-g\|_{L_1}\to 0$ , where  $\sigma_{0n}$  is the inverse permutation of  $\sigma_n$ . Let  $f_{n2}(x)=\int_0^1g_{n2}(x,y)\,\mathrm{d}y$ , which is now nonincreasing by our construction. Using

(4.13), we can now apply Lemma 16 with  $(f_{n2})_{n\geq 1}$  and D. Thus, we have  $||f_{n2}-D||_{L_1}\to 0$ . Recall that  $||D_n-D||_{L_1}\to 0$  by Assumption 1, and thus it follows that  $||f_{n2}-D_n||_{L_1}\to 0$ .

Step 3:  $L_{\infty}$ -approximation of the degree function. By Markov's inequality, there exists  $(\varepsilon_n)_{n\geq 1}$  with  $\varepsilon_n\to 0$  such that

$$\frac{|V_{\rm ex}|}{n} \to 0, \text{ where } V_{\rm ex} := \left\{ i : \left| \sum_{j \in [n]} g_{n2,ij} - d_i \right| > n\varepsilon_n \right\}.$$

Let  $g_{n3}(x, y) = \hat{p}_{ij}$  if  $(x, y) \in S_{ij}$  with  $i \in V_{\text{ex}}$  or  $j \in V_{\text{ex}}$ , and  $g_{n3}(x, y) = g_{n2}(x, y)$  otherwise. This changes at most  $2n|V_{\text{ex}}|$  block values of  $g_{2n}$ , and therefore,  $||g_{n3} - g_{n2}||_{L_1} \le 2|V_{\text{ex}}|/n \to 0$ . To compare the degree functions, note that for  $i \in V_{\text{ex}}$ , we have  $\sum_{j \in [n]} g_{n3,ij} = d_i$ , and for  $i \notin V_{\text{ex}}$ , we have  $|\sum_{j \in [n]} g_{n3,ij} - d_i| \le n\varepsilon_n + |V_{\text{ex}}|$ . Thus, if  $f_{n3}(x) = \int_0^1 g_{n3}(x, y) \, \mathrm{d}y$ , then  $||f_{n3} - D_n||_{L_\infty} \to 0$  by our construction.

Step 4: Truncation away from 0,1. Let  $\delta_n := \|f_{n3} - D_n\|_{L_\infty}$ . Define on  $S_{ij}$  for  $i \neq j$ ,

(4.35) 
$$g_{n4}(x,y) := \begin{cases} g_{n3}(x,y) & \text{if } \delta_n \le g_{n3}(x,y) \le 1 - \delta_n, \\ \frac{1}{n} & \text{if } g_{n3}(x,y) < \delta_n, \\ 1 - \frac{1}{n} & \text{if } g_{n3}(x,y) > 1 - \delta_n, \end{cases}$$

and  $g_{n4}(x, y) = 0$  on  $S_{ii}$  for all i. By construction,  $\|g_{n4} - g_{n3}\|_{L_{\infty}} \le \delta_n$  and hence  $\|f_{n4} - D_n\|_{L_{\infty}} \le \|f_{n4} - f_{n3}\|_{L_{\infty}} + \|f_{n3} - D_n\|_{L_{\infty}} \le 2\delta_n$ , where  $f_{n4}(x) = \int_0^1 g_{n4}(x, y) \, dy$ . Step 5: Producing a graphon with exact degree function  $D_n$ . We need the following:

FACT 3. Given any sequence  $a=(a_i)_{i\in[n]}$ , it is possible to find weights  $w=(w_{ij})_{i,j}$  with  $w_{ij}=w_{ji}$  for all i,j, such that  $\sum_{j\in[n]\setminus\{i\}}w_{ij}=a_i$ , and  $w_{ii}=0$  for all  $i\in[n]$ , and

$$(4.36) ||w||_{\infty} \le \frac{||a||_{\infty}}{n-2} + \frac{||a||_{1}}{(n-1)(n-2)}.$$

Let us first complete the proof of Lemma 14; the proof of Fact 3 is given subsequently. Note that  $D_n - f_{n4}$  is a step function with constant values in  $\left[\frac{i-1}{n}, \frac{i}{n}\right]$  for all i. We take  $a_i$  to be the value of  $n(D_n - f_{n4})$  on  $\left[\frac{i-1}{n}, \frac{i}{n}\right]$ . Now, we choose w according to Fact 3, and define

(4.37) 
$$g_{n5}(x, y) = \begin{cases} g_{n4}(x, y) + w_{ij} & \forall (x, y) \in S_{ij}, i \neq j, \\ 0 & \text{otherwise.} \end{cases}$$

Recall the bounds from Step 4. Since  $\|a\|_{\infty} \leq 2n\delta_n$  and  $\|a\|_1 \leq n\|a\|_{\infty} \leq 2n^2\delta_n$ , we have from (4.36) that  $\|w\|_{\infty} \leq 5\delta_n$ . Thus,  $\|g_{n5} - g_{n4}\|_{L_{\infty}} \to 0$ , and moreover  $\int_0^1 g_{n5}(x,y) \, \mathrm{d}y = D_n(x)$ . However,  $g_{n5}$  can take values in  $[-5\delta_n, 1+5\delta_n]$ . Finally we define  $\delta_n' = \max\{n^{-1}, \delta_n\}$   $g_n = \delta_n'^{1/4} W_{n,d} + (1-\delta_n'^{1/4}) g_{n5}$ . Since  $W_{n,d}$  is away from boundary, it follows that  $g_n$  takes values in  $[\frac{1}{n}, 1-\frac{1}{n}]$  for all sufficiently large n, and also  $\int g_n(x,y) \, \mathrm{d}y = D_n(x)$ . This completes the proof of Lemma 14.  $\square$ 

PROOF OF FACT 3. Let us view w as a vector with its elements indexed by (j, k), j < k. We wish to find a solution of w in the equation Mw = a, where M is an  $n \times \binom{n}{2}$  matrix with entries  $m_{i,(j,k)} = \mathbb{1}\{i \in \{j,k\}\}$ . First let us find the inverse of  $MM^T$ . Indeed,

(4.38) 
$$(MM^T)_{uv} = \sum_{j < k} \mathbb{1} \{ u \in \{j, k\} \} \mathbb{1} \{ v \in \{j, k\} \} = \begin{cases} 1 & \text{if } u \neq v, \\ n - 1 & \text{if } u = v. \end{cases}$$

<span id="page-21-0"></span>Thus  $MM^T = (n-2)I + 11^T$ . An application of the Sherman–Morrison formula (see, e.g., [25]) yields that

$$(4.39) (MM^T)^{-1} = \frac{I}{n-2} - \frac{11^T}{2(n-1)(n-2)}.$$

Now,  $w = M^T (MM^T)^{-1}a$  is a solution to the equation Mw = a. Also, the (j, k)th column of M consists of 1 on the jth and kth entries and zero elsewhere. Hence, we observe that  $\|w\|_{\infty} \le 2\|a\|_{\infty}/(n-2) + \|a\|_1/(n-1)(n-2)$ , and the proof follows.  $\square$ 

#### 5. Proofs of Corollaries 4 and 5.

5.1. Large deviation for continuous functionals. In this section, we prove Corollary 4, leveraging the general techniques used in [15], Section 3, and [18], Section 3.2.

PROOF OF COROLLARY 4(1). Let  $\Gamma_{\geq r} = \{\tilde{W} : \tau(\tilde{W}) \geq r\}$ . This is a closed set, since  $\tau$  is continuous. Recall that  $\mathcal{W}_0 = \{W \in \mathcal{W} : \deg_{\tilde{W}} = \mu_D\}$  and  $\tilde{\mathcal{W}}_0 = \{\tilde{W} \in \tilde{\mathcal{W}} : W \in \mathcal{W}_0\}$ .  $\tilde{\mathcal{W}}_0$  is also a closed set by (4.13). Also,

(5.1) 
$$\phi_{\tau}(D,r) = \inf_{\tilde{W} \in \Gamma_{>r} \cap \tilde{\mathscr{W}}_{0}} J_{W_{D}}(\tilde{W}).$$

First, note that  $J_{W_D}(\tilde{W})=0$  if and only if  $\delta_{\square}(\tilde{W},\tilde{W}_D)=0$ , which follows directly from Lemma 7. Thus,  $\phi_{\tau}(D,r)=0$  for  $r\in[0,l_{\tau}(D)]$ . In this proof, let us henceforth assume  $r\in(l_{\tau}(D),r_{\tau}(D)]$ . It follows that  $\Gamma_{\geq r}\cap\tilde{\mathscr{W}}_0\neq\varnothing$  and  $J_{W_D}$  is finite on  $\Gamma_{\geq r}\cap\tilde{\mathscr{W}}_0$ . Consequently,  $\phi_{\tau}(D,r)<\infty$ . For the strict positivity, since  $\Gamma_{\geq r}\cap\tilde{\mathscr{W}}_0$  is compact and  $J_{W_D}(\tilde{W})$  is lower semicontinuous, the infimum in (5.1) is attained at some point  $\tilde{W}^{\star}$ . However, since  $\tau(\tilde{W}^{\star})\geq r>l_{\tau}(D)$ , it must be that  $\delta_{\square}(\tilde{W}_D,\tilde{W}^{\star})>0$  and thus  $J_{W_D}(\tilde{W}^{\star})>0$ . This shows that  $\phi_{\tau}(D,r)$  is strictly positive.

To prove the left-continuity of  $\phi_{\tau}$ , let  $\alpha < \infty$  be such that  $\phi_{\tau}(D, r') \leq \alpha$  for all r' < r. Recall that  $F_{\star,r} \subset \Gamma_{\geq r} \cap \tilde{\mathcal{W}}_0$  is the set of minimizers of (5.1), which is shown to be nonempty above, and let  $\tilde{W}_r \in F_{\star,r}$ . Note that  $J_{W_D}(\tilde{W}_{r'}) \leq \alpha$ ,  $\tau(\tilde{W}_{r'}) \geq r'$ , and further,  $\{\tilde{W}_{r'}: r' < r\}$  is precompact in  $(\tilde{\mathcal{W}}, \delta_{\square})$ . Take a subsequence along which as  $r' \nearrow r$ ,  $\tilde{W}_{r'} \to \tilde{W}$  in  $(\mathcal{W}, \delta_{\square})$ . Then, by the lower semicontinuity of  $J_{W_D}$ ,  $J_{W_D}(\tilde{W}) \leq \alpha$ , and by the continuity of  $\tau$ ,  $\tau(\tilde{W}) \geq r$ . Thus  $\phi_{\tau}(D, r) \leq \alpha$ . This proves the left-continuity of  $\phi_{\tau}(D, \cdot)$ .  $\square$ 

PROOF OF COROLLARY 4(2). Let  $\Gamma_{>r} = {\tilde{W} : \tau(\tilde{W}) > r}$ . Then Theorem 2 yields

(5.2) 
$$-\lim_{r'\searrow r} \phi_{\tau}(D,r) = -\inf_{\tilde{W}\in\Gamma_{>r}} J_{D}(\tilde{W}) \leq \liminf_{n\to\infty} \frac{1}{n^{2}} \log \mathbb{P}(\tau_{n,d} > r)$$
$$\leq \limsup_{n\to\infty} \frac{1}{n^{2}} \log \mathbb{P}(\tau_{n,d} \geq r) \leq -\phi_{\tau}(D,r).$$

Thus, if r is a right-continuity point of  $\phi_{\tau}(D,\cdot)$ , then all the inequalities above hold with equality and the proof follows.  $\square$ 

PROOF OF COROLLARY 4(3). Let  $\alpha = \phi_{\tau}(D, r)$ . Recall that  $\tilde{\mathbb{B}}_{\square}(\tilde{W}, \varepsilon)$  denotes the  $\varepsilon$  ball around  $\tilde{W}$  in  $(\tilde{W}, \delta_{\square})$ . Define  $\Gamma_{r,\varepsilon} = \Gamma_{\geq r} \cap (\bigcap_{\tilde{W} \in F_{\star,r}} \tilde{\mathbb{B}}_{\square}(\tilde{W}, \varepsilon)^c)$ . Note that

(5.3) 
$$\left\{\delta_{\square}(W^{G_{n,d}}, F_{\star,r}) \ge \varepsilon \text{ and } \tau_{n,d} \ge r\right\} = \left\{W^{G_{n,d}} \in \Gamma_{r,\varepsilon}\right\}.$$

<span id="page-22-0"></span>It is enough to show that

(5.4) 
$$\limsup_{n\to\infty} \frac{1}{n^2} \log \mathbb{P}(W^{G_{n,d}} \in \Gamma_{r,\varepsilon}) < -\alpha.$$

Since  $\Gamma_{r,\varepsilon}$  is a closed set, using Theorem 2, it is enough to show that  $\inf_{\tilde{W} \in \Gamma_{r,\varepsilon}} J_D(\tilde{W}) \leq \alpha$  yields a contradiction. Now, since  $\Gamma_{r,\varepsilon}$  is compact and  $J_D$  is lower semicontinuous,  $J_D(\tilde{W}_r) \leq \alpha$  for some  $\tilde{W}_r \in \Gamma_{r,\varepsilon}$ . Further,

$$(5.5) F_{\star,r} = \Gamma_{>r} \cap \{\tilde{W} : J_D(\tilde{W}) \le \alpha\},$$

so that  $\tilde{W}_r \in F_{\star,r}$ . Together with  $\tilde{W}_r \in \Gamma_{r,\varepsilon}$ , this yields a contradiction.  $\square$ 

5.2. Convergence of the microcanonical partition function. We now complete the proof of Corollary 5 in this section. We first need the following lemma:

LEMMA 17. Recall that  $G_{n,d}$  is the space of graphs with degree sequence d. Under Assumption 1, as  $n \to \infty$ ,

(5.6) 
$$\frac{1}{n^2} \log |\mathcal{G}_{n,d}| \to h_e(W_D)$$
$$= -\int_0^1 \beta(x) D(x) \, \mathrm{d}x + \frac{1}{2} \int_{[0,1]^2} \log(1 + \mathrm{e}^{\beta(x) + \beta(y)}) \, \mathrm{d}x \, \mathrm{d}y,$$

where  $h_e$  is defined in (1.21), and  $\beta$  is given by Proposition 1.

PROOF. Recall the definitions of  $\hat{\boldsymbol{\beta}}$ ,  $\hat{p}_{ij}$ ,  $\hat{G}_n$ ,  $W_{n,d}$ ,  $D_n$  and  $\beta_n$  from Section 4.1. Note that

(5.7) 
$$\mathbb{P}(\hat{G}_n = G) = \frac{e^{\sum_{i \in [n]} \hat{\beta}_i d_i}}{\prod_{i < j} (1 + e^{\hat{\beta}_i + \hat{\beta}_j})}, \quad G \in \mathcal{G}_{n,d}.$$

Thus, if  $d(\hat{G}_n)$  denotes the degree sequece of  $\hat{G}_n$ , then

(5.8) 
$$\mathbb{P}(\boldsymbol{d}(\hat{G}_n) = \boldsymbol{d}) = |\mathcal{G}_{n,\boldsymbol{d}}| \frac{e^{\sum_{i \in [n]} \beta_i d_i}}{\prod_{i < j} (1 + e^{\hat{\beta}_i + \hat{\beta}_j})}.$$

Now, using (4.9),  $\beta_n \to \beta$  in  $L_1$  and therefore

(5.9) 
$$\frac{1}{n^2} \log \prod_{i < j} (1 + e^{\hat{\beta}_i + \hat{\beta}_j})$$

$$= \frac{1}{n^2} \sum_{i < j} \log(1 + e^{\hat{\beta}_i + \hat{\beta}_j})$$

$$= \frac{1}{2} \int_{[0,1]^2} \log(1 + e^{\beta_n(x) + \beta_n(y)}) dx dy - \frac{1}{n^2} \sum_{i \in [n]} \log(1 + e^{2\hat{\beta}_i})$$

$$\rightarrow \frac{1}{2} \int_{[0,1]^2} \log(1 + e^{\beta(x) + \beta(y)}) dx dy,$$

where the second term in the third equality goes to zero by dominated convergence theorem. Moreover, using the fact that  $D_n \to D$  in  $L_1$  from Assumption 1, and that  $d_i < n$ ,  $\|\hat{\boldsymbol{\beta}}\|_{\infty} \le C$ , it follows that

(5.10) 
$$\frac{1}{n^2} \sum_{i \in [n]} \hat{\beta}_i d_i = \int_0^1 \beta_n(x) D_n(x) dx \to \int_0^1 \beta(x) D(x) dx.$$

<span id="page-23-0"></span>Now,

(5.11) 
$$h_{e}(W_{D})$$

$$= -\frac{1}{2} \int_{[0,1]^{2}} (W_{D}(x, y) \log(W_{D}(x, y))$$

$$+ (1 - W_{D}(x, y)) \log(1 - W_{D}(x, y))) dx dy$$

$$= -\int_{0}^{1} \beta(x) D(x) dx + \frac{1}{2} \int_{[0,1]^{2}} \log(1 + e^{\beta(x) + \beta(y)}) dx dy.$$

Now, turning back to (5.8), let us recall from Lemma 13 that  $\mathbb{P}(d(\hat{G}_n) = d)$  lies in  $(e^{-n^{7/4}}, 1)$ . Thus,

$$(5.12) \quad \frac{1}{n^2} \log |\mathcal{G}_{n,d}| = -\frac{1}{n^2} \sum_{i \in [n]} \hat{\beta}_i d_i + \frac{1}{n^2} \log \prod_{i < j} \left( 1 + e^{\hat{\beta}_i + \hat{\beta}_j} \right) + o(1) \to h_e(W_D),$$

where the last step follows from (5.11). The proof is now complete.  $\Box$ 

PROOF OF COROLLARY 5. We identify graphs with the corresponding empirical graphons— this naturally embeds  $\mathcal{G}_{n,d}$  into the space  $\widetilde{\mathscr{W}}$ . The image of  $\mathcal{G}_{n,d}$  under this embedding map is henceforth denoted as  $\widetilde{\mathcal{G}}_{n,d}$ . For any  $\widetilde{A} \subseteq \widetilde{\mathscr{W}}$ , define  $\widetilde{A}_n = \widetilde{A} \cap \widetilde{\mathcal{G}}_{n,d}$ , so that  $|\widetilde{A}_n| < \infty$  for all n. Observe that

(5.13) 
$$\tilde{\mathbb{P}}_{n,d}(\tilde{A}) = \frac{|\tilde{A}_n|}{|\mathcal{G}_{n,d}|}.$$

Therefore, using Theorem 2 together with Lemma 17, for any closed set  $\tilde{F} \subset \tilde{\mathscr{W}}$  and open set  $\tilde{U} \subset \tilde{\mathscr{W}}$ ,

(5.14) 
$$\limsup_{n \to \infty} \frac{1}{n^2} \log |\tilde{F}_n| \le -\inf_{\tilde{W} \in \tilde{F}} J_D(\tilde{W}) + h_e(W_D),$$

(5.15) 
$$\liminf_{n\to\infty} \frac{1}{n^2} \log |\tilde{U}_n| \ge -\inf_{\tilde{W}\in \tilde{U}} J_D(\tilde{W}) + h_e(W_D).$$

Fix  $\varepsilon > 0$ . Since  $\tau$  is bounded, there exists  $(a_i)_{i=1}^k$  such that the range of  $\tau$  is a subset of  $\bigcup_{i \in [k]} [a_i, a_i + \varepsilon]$ . Now, let  $\tilde{F}^{a_i} := \tau^{-1}([a_i, a_i + \varepsilon])$ , which is closed due to the continuity of  $\tau$ . Thus,

$$(5.16) e^{n^2 Z_{n,\tau}} \le \sum_{i \in [k]} e^{n^2 (a_i + \varepsilon)} |\tilde{F}^{a_i}| \le k \max_{i \in [k]} e^{n^2 (a_i + \varepsilon)} |\tilde{F}^{a_i}|.$$

Thus, (5.14) implies that

$$\limsup_{n \to \infty} Z_{n,\tau} \le \max_{i \in [k]} \left( a_i + \varepsilon - \inf_{\tilde{W} \in \tilde{F}^{a_i}} J_D(\tilde{W}) \right) + h_e(W_D)$$

$$\le \varepsilon + \max_{i \in [k]} \sup_{\tilde{W} \in \tilde{F}^{a_i}} \left( \tau(\tilde{W}) - J_D(\tilde{W}) \right) + h_e(W_D)$$

$$= \varepsilon + \sup_{\tilde{W} \in \tilde{W}} \left( \tau(\tilde{W}) - J_D(\tilde{W}) \right) + h_e(W_D),$$

where in the second step we have used the fact that  $\tau(\tilde{W}) \geq a$  for all  $\tilde{W} \in \tilde{F}^{a_i}$ . For the lower bound, let  $\tilde{U}^{b_i} = \tau^{-1}((b_i, b_i + \varepsilon))$  for  $i \leq l$  be such that  $\bigcup_{i \in [l]} (b_i, b_i + \varepsilon)$  covers the range of  $\tau$ . An identical computation to above yields that

(5.18) 
$$\liminf_{n \to \infty} Z_{n,\tau} \ge -\varepsilon + \sup_{\tilde{W} \in \tilde{\mathcal{W}}} \left( \tau(\tilde{W}) - J_D(\tilde{W}) \right) + h_e(W_D).$$

<span id="page-24-0"></span>The proof of (1.22) now follows by taking  $\varepsilon \to 0$ . To see (1.23), the continuity of  $\tau$ , together with (5.14) implies that

(5.19) 
$$\limsup_{n \to \infty} \frac{1}{n^2} \log N_{n,\tau}(\boldsymbol{d}, r) \le -\phi_{\tau}(D, r) + h_e(W_D).$$

Also,  $N_{n,\tau}(\boldsymbol{d},r)$  is at least the number of graphs with degree sequence  $\boldsymbol{d}$  and  $\tau(\tilde{W}) > r$ . Thus, (5.15) implies that

(5.20) 
$$\liminf_{n\to\infty} \frac{1}{n^2} \log N_{n,\tau}(\boldsymbol{d},r) \ge -\lim_{r'\searrow r} \phi_{\tau}(D,r) + h_e(W_D).$$

The proof of (1.23) is now complete using the right continuity of  $\phi_{\tau}(D, \cdot)$  at r.  $\square$ 

#### **REFERENCES**

- [1] AUGERI, F. (2018). Nonlinear large deviation bounds with applications to traces of Wigner matrices and cycles counts in Erdős–Rényi graphs. Available at arXiv:1810.01558.
- [2] BARVINOK, A. and HARTIGAN, J. A. (2013). The number of graphs and a random graph with a given degree sequence. *Random Structures Algorithms* 42 301–348. MR3039682 https://doi.org/10.1002/ rsa 20409
- [3] BHATTACHARYA, B. B., GANGULY, S., LUBETZKY, E. and ZHAO, Y. (2017). Upper tails and independence polynomials in random graphs. Adv. Math. 319 313–347. MR3695877 https://doi.org/10.1016/j.aim.2017.08.003
- [4] BHATTACHARYA, S. and DEMBO, A. (2021). Upper tail for homomorphism counts in constrained sparse random graphs. *Random Structures Algorithms* 59 315–338. MR4295566 https://doi.org/10.1002/rsa. 21011
- [5] BLITZSTEIN, J. and DIACONIS, P. (2010). A sequential importance sampling algorithm for generating random graphs with prescribed degrees. *Internet Math.* 6 489–522. MR2809836 https://doi.org/10. 1080/15427951.2010.557277
- [6] BOLLOBÁS, B. (1980). A probabilistic proof of an asymptotic formula for the number of labelled regular graphs. European J. Combin. 1 311–316. MR0595929 https://doi.org/10.1016/S0195-6698(80) 80030-8
- [7] BORGS, C., CHAYES, J., GAUDIO, J., PETTI, S. and SEN, S. (2020). A large deviation principle for block models. Available at arXiv:2007.14508.
- [8] BORGS, C., CHAYES, J. T., COHN, H. and GANGULY, S. (2021). Consistent nonparametric estimation for heavy-tailed sparse graphs. Ann. Statist. 49 1904–1930. MR4319235 https://doi.org/10.1214/20-aos1985
- [9] BORGS, C., CHAYES, J. T., LOVÁSZ, L., SÓS, V. T. and VESZTERGOMBI, K. (2008). Convergent sequences of dense graphs. I. Subgraph frequencies, metric properties and testing. Adv. Math. 219 1801–1851. MR2455626 https://doi.org/10.1016/j.aim.2008.07.008
- [10] BOUCHERON, S., LUGOSI, G. and MASSART, P. (2013). Concentration Inequalities: A Nonasymptotic Theory of Independence. Oxford Univ. Press, Oxford. MR3185193 https://doi.org/10.1093/acprof:oso/ 9780199535255.001.0001
- [11] CHATTERJEE, S. (2017). Large Deviations for Random Graphs. Lecture Notes in Math. 2197. Springer, Cham. MR3700183 https://doi.org/10.1007/978-3-319-65816-2
- [12] CHATTERJEE, S. and DEMBO, A. (2016). Nonlinear large deviations. Adv. Math. 299 396–450. MR3519474 https://doi.org/10.1016/j.aim.2016.05.017
- [13] CHATTERJEE, S. and DIACONIS, P. (2013). Estimating and understanding exponential random graph models. Ann. Statist. 41 2428–2461. MR3127871 https://doi.org/10.1214/13-AOS1155
- [14] CHATTERJEE, S., DIACONIS, P. and SLY, A. (2011). Random graphs with a given degree sequence. Ann. Appl. Probab. 21 1400–1435. MR2857452 https://doi.org/10.1214/10-AAP728
- [15] CHATTERJEE, S. and VARADHAN, S. R. S. (2011). The large deviation principle for the Erdős–Rényi random graph. European J. Combin. 32 1000–1017. MR2825532 https://doi.org/10.1016/j.ejc.2011. 03.014
- [16] COOK, N. and DEMBO, A. (2020). Large deviations of subgraph counts for sparse Erdős–Rényi graphs. Adv. Math. 373 107289. MR4130460 https://doi.org/10.1016/j.aim.2020.107289
- [17] DEL GENIO, C. I., KIM, H., TOROCZKAI, Z. and BASSLER, K. E. (2010). Efficient and exact sampling of simple graphs with given arbitrary degree sequence. *PLoS ONE* **5** 1–7. https://doi.org/10.1371/journal.pone.0010012

- <span id="page-25-0"></span>[18] DEMBO, A. and LUBETZKY, E. (2018). A large deviation principle for the Erdos–Rényi uniform random ˝ graph. *Electron*. *Commun*. *Probab*. **23** 13. [MR3873786](http://www.ams.org/mathscinet-getitem?mr=3873786)<https://doi.org/10.1214/18-ECP181>
- [19] DEMBO, A. and ZEITOUNI, O. (2010). *Large Deviations Techniques and Applications*. *Stochastic Modelling and Applied Probability* **38**. Springer, Berlin. [MR2571413](http://www.ams.org/mathscinet-getitem?mr=2571413) [https://doi.org/10.1007/](https://doi.org/10.1007/978-3-642-03311-7) [978-3-642-03311-7](https://doi.org/10.1007/978-3-642-03311-7)
- [20] DEN HOLLANDER, F., MANDJES, M., ROCCAVERDE, A. and STARREVELD, N. J. (2018). Ensemble equivalence for dense graphs. *Electron*. *J*. *Probab*. **23** 12. [MR3771749](http://www.ams.org/mathscinet-getitem?mr=3771749) [https://doi.org/10.1214/](https://doi.org/10.1214/18-EJP135) [18-EJP135](https://doi.org/10.1214/18-EJP135)
- [21] ELDAN, R. (2018). Gaussian-width gradient complexity, reverse log-Sobolev inequalities and nonlinear large deviations. *Geom*. *Funct*. *Anal*. **28** 1548–1596. [MR3881829](http://www.ams.org/mathscinet-getitem?mr=3881829) [https://doi.org/10.1007/](https://doi.org/10.1007/s00039-018-0461-z) [s00039-018-0461-z](https://doi.org/10.1007/s00039-018-0461-z)
- [22] ERDOS, P. and GALLAI, T. (1960). Graphen mit punkten vorgeschriebenen grades. *Mat*. *Lapok* (*N*.*S*.) **11** 264–274.
- [23] GREBÍK, J. and PIKHURKO, O. (2021). Large deviation principles for block and step graphon random graph models. Available at [arXiv:2101.07025](http://arxiv.org/abs/arXiv:2101.07025).
- [24] GUNBY, B. (2021). *Upper Tails of Subgraph Counts in Sparse Regular Graphs*. ProQuest LLC, Ann Arbor, MI. Thesis (Ph.D.)—Harvard University. [MR4314974](http://www.ams.org/mathscinet-getitem?mr=4314974)
- [25] HAGER, W. W. (1989). Updating the inverse of a matrix. *SIAM Rev*. **31** 221–239. [MR0997457](http://www.ams.org/mathscinet-getitem?mr=0997457) <https://doi.org/10.1137/1031049>
- [26] HAREL, M., MOUSSET, F. and SAMOTIJ, W. (2019). Upper tails via high moments and entropic stability. Duke Math. J., Available at [arXiv:1904.08212](http://arxiv.org/abs/arXiv:1904.08212).
- [27] JANSON, S., ŁUCZAK, T. and RUCINSKI, A. (2000). *Random Graphs*. *Wiley-Interscience Series in Discrete Mathematics and Optimization*. Wiley Interscience, New York. [MR1782847](http://www.ams.org/mathscinet-getitem?mr=1782847) [https://doi.org/10.1002/](https://doi.org/10.1002/9781118032718) [9781118032718](https://doi.org/10.1002/9781118032718)
- [28] KENYON, R., RADIN, C., REN, K. and SADUN, L. (2017). Multipodal structure and phase transitions in large constrained graphs. *J*. *Stat*. *Phys*. **168** 233–258. [MR3667360](http://www.ams.org/mathscinet-getitem?mr=3667360) [https://doi.org/10.1007/](https://doi.org/10.1007/s10955-017-1804-0) [s10955-017-1804-0](https://doi.org/10.1007/s10955-017-1804-0)
- [29] KENYON, R., RADIN, C., REN, K. and SADUN, L. (2017). The phases of large networks with edge and triangle constraints. *J*. *Phys*. *A* **50** 435001. [MR3718855](http://www.ams.org/mathscinet-getitem?mr=3718855)<https://doi.org/10.1088/1751-8121/aa8ce1>
- [30] KENYON, R., RADIN, C., REN, K. and SADUN, L. (2018). Bipodal structure in oversaturated random graphs. *Int*. *Math*. *Res*. *Not*. *IMRN* **2018** 1009–1044. [MR3801454](http://www.ams.org/mathscinet-getitem?mr=3801454)<https://doi.org/10.1093/imrn/rnw261>
- [31] KENYON, R. and YIN, M. (2017). On the asymptotics of constrained exponential random graphs. *J*. *Appl*. *Probab*. **54** 165–180. [MR3632612](http://www.ams.org/mathscinet-getitem?mr=3632612)<https://doi.org/10.1017/jpr.2016.93>
- [32] LIEBENAU, A. and WORMALD, N. (2017). Asymptotic enumeration of graphs by degree sequence, and the degree sequence of a random graph. Available at [arXiv:1702.08373.](http://arxiv.org/abs/arXiv:1702.08373)
- [33] LOVÁSZ, L. (2012). *Large Networks and Graph Limits*. *American Mathematical Society Colloquium Publications* **60**. Amer. Math. Soc., Providence, RI. [MR3012035](http://www.ams.org/mathscinet-getitem?mr=3012035)<https://doi.org/10.1090/coll/060>
- [34] LUBETZKY, E. and ZHAO, Y. (2015). On replica symmetry of large deviations in random graphs. *Random Structures Algorithms* **47** 109–146. [MR3366814](http://www.ams.org/mathscinet-getitem?mr=3366814)<https://doi.org/10.1002/rsa.20536>
- [35] LUBETZKY, E. and ZHAO, Y. (2017). On the variational problem for upper tails in sparse random graphs. *Random Structures Algorithms* **50** 420–436. [MR3632418](http://www.ams.org/mathscinet-getitem?mr=3632418)<https://doi.org/10.1002/rsa.20658>
- [36] MARKERING, M. (2020). The large deviation principle for inhomogeneous Erdos–Rényi random graphs. ˝
- [37] MCKAY, B. D. and WORMALD, N. C. (1990). Asymptotic enumeration by degree sequence of graphs of high degree. *European J*. *Combin*. **11** 565–580. [MR1078713](http://www.ams.org/mathscinet-getitem?mr=1078713) [https://doi.org/10.1016/S0195-6698\(13\)](https://doi.org/10.1016/S0195-6698(13)80042-X) [80042-X](https://doi.org/10.1016/S0195-6698(13)80042-X)
- [38] ORSINI, C., DANKULOV, M. M., COLOMER-DE SIMÓN, P., JAMAKOVIC, A., MAHADEVAN, P., VAHDAT, A., BASSLER, K. E., TOROCZKAI, Z., BOGUÑÁ, M. et al. (2015). Quantifying randomness in real networks. *Nat*. *Commun*. **6** 8627. <https://doi.org/10.1038/ncomms962>
- [39] PROKHOROV, Y. V. (1956). Convergence of random processes and limit theorems in probability theory. *Theory Probab*. *Appl*. **1** 157–214. <https://doi.org/10.1137/1101016>
- [40] RADIN, C. (2018). Phases in large combinatorial systems. *Ann*. *Inst*. *Henri Poincaré D* **5** 287–308. [MR3813217](http://www.ams.org/mathscinet-getitem?mr=3813217)<https://doi.org/10.4171/AIHPD/55>
- [41] RADIN, C. and SADUN, L. (2013). Phase transitions in a complex network. *J*. *Phys*. *A* **46** 305002. [MR3083277](http://www.ams.org/mathscinet-getitem?mr=3083277)<https://doi.org/10.1088/1751-8113/46/30/305002>
- [42] RADIN, C. and YIN, M. (2013). Phase transitions in exponential random graphs. *Ann*. *Appl*. *Probab*. **23** 2458–2471. [MR3127941](http://www.ams.org/mathscinet-getitem?mr=3127941)<https://doi.org/10.1214/12-AAP907>
- [43] ŠILEIKIS, M. and WARNKE, L. (2019). A counterexample to the DeMarco–Kahn upper tail conjecture. *Random Structures Algorithms* **55** 775–794. [MR4025388](http://www.ams.org/mathscinet-getitem?mr=4025388)<https://doi.org/10.1002/rsa.20859>

- <span id="page-26-0"></span>[44] SQUARTINI, T., DE MOL, J., DEN HOLLANDER, F. and GARLASCHELLI, D. (2015). Breaking of ensemble equivalence in networks. *Phys*. *Rev*. *Lett*. **115** 268701. [https://doi.org/10.1103/PhysRevLett.115.](https://doi.org/10.1103/PhysRevLett.115.268701) [268701](https://doi.org/10.1103/PhysRevLett.115.268701)
- [45] SZEMERÉDI, E. (1978). Regular partitions of graphs. In *Problèmes Combinatoires et Théorie des Graphes* (*Colloq*. *Internat*. *CNRS*, *Univ*. *Orsay*, *Orsay*, 1976). *Colloq*. *Internat*. *CNRS* **260** 399–401. CNRS, Paris. [MR0540024](http://www.ams.org/mathscinet-getitem?mr=0540024)
- [46] VAN DER HOORN, P., LIPPNER, G. and MOSSEL, E. (2019). Regular graphs with linearly many triangles. Available at [1904.02212](http://arxiv.org/abs/1904.02212).
- [47] WORMALD, N. C. (1999). Models of random regular graphs. In *Surveys in Combinatorics*, 1999 (*Canterbury*). *London Mathematical Society Lecture Note Series* **267** 239–298. Cambridge Univ. Press, Cambridge. [MR1725006](http://www.ams.org/mathscinet-getitem?mr=1725006)
- [48] YIN, M. (2015). Large deviations and exact asymptotics for constrained exponential random graphs. *Electron*. *Commun*. *Probab*. **20** 56. [MR3384114](http://www.ams.org/mathscinet-getitem?mr=3384114)<https://doi.org/10.1214/ECP.v20-4010>
- [49] YING, X. and WU, X. (2009). Graph generation with prescribed feature constraints. In *Proc*. *SIAM Int Conf Data Min* 966–977. <https://doi.org/10.1137/1.9781611972795.83>