![](_page_0_Figure_0.jpeg)

Electron. J. Probab. **27** (2022), article no. 103, 1–29. ISSN: [1083-6489](https://imstat.org/journals-and-publications/electronic-journal-of-probability/) <https://doi.org/10.1214/22-EJP821>

### **Global lower mass-bound for critical configuration models in the heavy-tailed regime**\*

Shankar Bhamidi† Souvik Dhara‡ Remco van der Hofstad§ Sanchayan Sen¶

#### **Abstract**

We establish the global lower mass-bound property for the largest connected components in the critical window for the configuration model when the degree distribution has an infinite third moment. The scaling limit of the critical percolation clusters, viewed as measured metric spaces, was established in our prior work with respect to the Gromov-weak topology. Our result extends those scaling limit results to the stronger Gromov-Hausdorff-Prokhorov topology under slightly stronger assumptions on the degree distribution. This implies the distributional convergence of global functionals such as the diameter of the largest critical components. Further, our result gives a sufficient condition for compactness of the random metric spaces that arise as scaling limits of critical clusters in the heavy-tailed regime.

**Keywords:** global lower mass-bound; critical configuration model; heavy-tailed degrees. **[MSC2020 subject classifications:](https://ams.org/mathscinet/msc/msc2020.html)** 60C05; 05C80.

Submitted to EJP on May 8, 2020, final version accepted on July 3, 2022.

E-mail: [sanchayan.sen1@gmail.com](mailto:sanchayan.sen1@gmail.com)

<sup>\*</sup>The authors are grateful to two anonymous referees for their careful reading and many comments and suggestions on an earlier version of the paper. SB was partially supported by NSF grants DMS-1613072, DMS-1606839, and ARO grant W911NF-17-1-0010. SD and RvdH were supported by the Netherlands Organisation for Scientific Research (NWO) through Gravitation Networks grant 024.002.003. In addition, RvdH was supported by VICI grant 639.033.806. SD also thanks Elchanan Mossel for supporting his research through Vannevar Bush Faculty Fellowship (ONR-N00014-20-1-2826), Simons Investigator award (622132). SS has been supported in part by the Infosys foundation, Bangalore, and by MATRICS grant MTR/2019/000745 from SERB. SD thanks Eindhoven University of Technology, where a major part of this work was done.

<sup>†</sup>Department of Statistics and Operations Research, University of North Carolina.

E-mail: [bhamidi@email.unc.edu](mailto:bhamidi@email.unc.edu)

<sup>‡</sup>Simons Institute for the Theory of Computing, University of California, Berkeley.

E-mail: [dharasouvik1991@gmail.com](mailto:dharasouvik1991@gmail.com)

<sup>§</sup>Department of Mathematics and Computer Science, Eindhoven University of Technology.

E-mail: [bhamidi@email.unc.edu](mailto:bhamidi@email.unc.edu)

<sup>¶</sup>Department of Mathematics, Indian Institute of Science.

#### 1 Introduction

Any finite, connected graph  $\mathscr C$  can be viewed as a metric space with the distance between points given by  $a\mathrm{d}(\cdot,\cdot)$  for some constant a>0, where  $\mathrm{d}(\cdot,\cdot)$  is used as a generic notation to denote the graph-distance (i.e., number of edges in the shortest path between vertices). There is a natural probability measure  $\mu$  associated to the metric space  $(\mathscr C,a\mathrm{d})$  given by  $\mu(A)=|A|/|\mathscr C|$  for any  $A\subset\mathscr C$ , where |A| denotes the number of vertices in A. We denote this metric measure space by  $(\mathscr C,a)$ . Fix any  $\delta>0$  and define the  $\delta$ -lower mass of  $(\mathscr C,a)$  by

$$\mathfrak{m}(\delta) := \frac{\inf_{u \in \mathscr{C}} \left| \{ v \in \mathscr{C} : ad(v, u) \le \delta \} \right|}{|\mathscr{C}|}.$$
(1.1)

<span id="page-1-0"></span>Thus,  $\mathfrak{m}(\delta)$  is the least *mass* in any  $\delta$ -neighborhood of a vertex in  $(\mathscr{C}, a)$ . For a sequence  $(\mathscr{C}_n, a_n)_{n \geq 1}$  of graphs viewed as metric measure spaces, the global lower mass-bound property is defined as follows:

**Definition 1** (Global lower mass-bound property [5]). For  $\delta>0$ , let  $\mathfrak{m}_n(\delta)$  denote the  $\delta$ -lower mass of  $(\mathscr{C}_n,a_n)$ . Then  $(\mathscr{C}_n,a_n)_{n\geq 1}$  is said to satisfy the global lower mass-bound property if and only if  $\sup_{n\geq 1}\mathfrak{m}_n(\delta)^{-1}<\infty$  for any  $\delta>0$ . When  $(\mathscr{C}_n)_{n\geq 1}$  is a collection of random graphs,  $(\mathscr{C}_n,a_n)_{n\geq 1}$  is said to satisfy the global lower mass-bound property if and only if  $(\mathfrak{m}_n(\delta)^{-1})_{n>1}$  is a tight sequence of random variables for any  $\delta>0$ .

The aim of this paper is to prove the global lower mass-bound property for largest connected components of random graphs with given degrees (configuration model) at criticality, when the third moment of the empirical degree distribution tends to infinity (Theorem 1.5). Informally speaking, the global lower mass-bound property ensures that all the small neighborhoods of vertices in the 'large' critical component have mass bounded away from zero, so that the component does not have any light spots and the total mass is well-distributed over the whole component. This has several interesting consequences in the theory of critical random graphs. Our main motivation comes from the work of Athreya, Löhr, and Winter [5], who have shown that the global lower massbound property can be used to prove Gromov-Hausdorff-Prokhorov (GHP) convergence of random metric spaces. In a previous paper [7], we have studied the critical percolation clusters for the configuration model in the heavy-tailed universality class. We have proved that the ordered vector of components converges in distribution to suitable random objects in the Gromov-weak topology. The global lower mass-bound in this paper shows that the result of [7] in fact holds with respect to the stronger GHP-topology. One motivating reason for proving the GHP-convergence is that it yields the scaling limit of global functionals like the diameter of large critical components. Finding the scaling limit for the diameter of critical components is a daunting task even for the Erdős-Rényi random graph. Nachmias and Peres [31] estimated the tail probabilities of the diameter, but showing a distributional convergence result was a difficult question, until the seminal paper by Addario-Berry, Broutin and Goldschmidt [2] that proved the GHP-convergence for critical Erdős-Rényi random graphs. As a corollary of Theorem 1.5, we also get distributional convergence of the suitably rescaled diameter of the critical percolation clusters in the heavy-tailed regime (Theorem 1.9), where the scaling limit and exponents turn out to be different than those for the Erdős-Rényi case.

We will further discuss the applications and the scope of this work as well as its technical contributions after stating our results in Section 1.3. We start by defining the configuration model and state the precise assumptions.

#### 1.1 The configuration model

Consider a non-increasing sequence of degrees  $d=(d_i)_{i\in[n]}$  such that  $\ell_n=\sum_{i\in[n]}d_i$  is even. For notational convenience, we suppress the dependence of the degree sequence on n. The configuration model on n vertices having degree sequence d is constructed as follows [6,11]:

Equip vertex j with  $d_j$  stubs, or half-edges. Two half-edges create an edge once they are paired. Therefore, initially we have  $\ell_n = \sum_{i \in [n]} d_i$  half-edges. Pick any one half-edge and pair it with another uniformly chosen half-edge from the remaining unpaired half-edges and keep repeating the above procedure until all the unpaired half-edges are exhausted.

Let  $CM_n(d)$  denote the graph constructed by the above procedure. Note that  $CM_n(d)$  may contain self-loops or multiple edges. Given any degree sequence, let  $UM_n(d)$  denote the graph chosen uniformly at random from the collection of all simple graphs with degree sequence d. It can be shown that the conditional law of  $CM_n(d)$ , conditioned on it being simple, is the same as  $UM_n(d)$  (see e.g. [23, Proposition 7.13]).

#### 1.2 Main results

Fix a constant  $\tau \in (3,4)$ , which will denote the power-law exponent of the asymptotic degree distribution of  $\mathrm{CM}_n(d)$ . Throughout this paper we will use the shorthand notation

$$\alpha = 1/(\tau - 1), \quad \rho = (\tau - 2)/(\tau - 1), \quad \eta = (\tau - 3)/(\tau - 1).$$
 (1.2)

We use the standard notation of  $\stackrel{\mathbb{P}}{\to}$  and  $\stackrel{d}{\to}$  to denote convergence in probability and in distribution, respectively. Also, we use a generic notation C to denote a positive universal constant whose exact value may change from line to line. We use Bachmann–Landau asymptotic notation  $o(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ ,  $O(\cdot)$ , O(

We first state the general assumptions that are used to prove scaling limits for critical configuration models with heavy-tailed degree distributions as identified previously in [7,16]:

<span id="page-2-0"></span>**Assumption 1.1** (General assumptions). For each  $n \ge 1$ , let  $d = d_n = (d_1, \dots, d_n)$  be a degree sequence satisfying  $d_1 \ge d_2 \ge \dots \ge d_n$ . We assume the following about  $(d_n)_{n \ge 1}$  as  $n \to \infty$ :

(i) (High-degree vertices) For each fixed i > 1,

<span id="page-2-2"></span><span id="page-2-1"></span>
$$n^{-\alpha}d_i \to \theta_i,$$
 (1.3)

where  $\boldsymbol{\theta} = (\theta_1, \theta_2, \dots) \in \ell^3_{\downarrow} \setminus \ell^2_{\downarrow}$ , where  $\ell^p_{\downarrow} := \{(x_i)_{i \geq 1} : x_1 \geq x_2 \geq \dots \text{ and } \sum_i x_i^p < \infty \}$ .

(ii) (Moment assumptions) Let  $D_n$  denote the degree of a typical vertex, i.e., a vertex chosen uniformly at random from the vertex set [n], independently of  $\mathrm{CM}_n(d)$ . Then,  $D_n$  converges in distribution to some discrete random variable D and

$$\mathbb{E}[D_n] = \frac{1}{n} \sum_{i \in [n]} d_i \to \mu := \mathbb{E}[D], \qquad \mathbb{E}[D_n^2] = \frac{1}{n} \sum_{i \in [n]} d_i^2 \to \mu_2 := \mathbb{E}[D^2], \tag{1.4}$$

$$\lim_{K \to \infty} \limsup_{n \to \infty} n^{-3\alpha} \sum_{i=K+1}^{n} d_i^3 = 0.$$
 (1.5)

(iii) Let  $n_1$  be the number of degree-one vertices. Then  $n_1 = \Theta(n)$ , which is equivalent to assuming that  $\mathbb{P}(D=1) > 0$ .

<span id="page-3-5"></span>**Remark 1.2.** As important examples, Assumption 1.1 was shown to hold when the degree distribution is power-law with exponent  $\tau \in (3,4)$  [16, Section 2]. More precisely, if F is a distribution function on the nonnegative integers satisfying  $[1-F](x)=(1+o(1))Cx^{-(\tau-1)}$  as  $x\to\infty$ , then Assumptions 1.1(i), 1.1(ii) are satisfied when (a)  $d_i=[1-F]^{-1}(i/n)$ , and when (b)  $d_i$  are the order statistics of an i.i.d. sample from F (we add a dummy half-edge to vertex 1 if  $\sum_{i\in[n]}d_i$  is odd). Assumptions 1.1(iii) is also satisfied in these examples if F has non-zero mass at 1.

We further assume that the configuration model lies within the critical window of the phase transition, i.e., for some  $\lambda \in \mathbb{R}$ ,

<span id="page-3-1"></span>
$$\nu_n = \frac{\sum_{i \in [n]} d_i(d_i - 1)}{\sum_{i \in [n]} d_i} = 1 + \lambda n^{-\eta} + o(n^{-\eta}).$$
 (1.6)

Denote the *i*-th largest connected component of  $\mathrm{CM}_n(\boldsymbol{d})$  by  $\mathscr{C}_{\scriptscriptstyle(i)}$ , breaking ties arbitrarily. For each  $v \in [n]$  and  $\delta > 0$ , let  $\mathcal{N}_v(\delta)$  denote the  $\delta n^\eta$  neighborhood of v in  $\mathrm{CM}_n(\boldsymbol{d})$  in the graph distance. For each  $i \geq 1$ , define

<span id="page-3-2"></span>
$$\mathfrak{m}_{i}^{n}(\delta) = \inf_{v \in \mathscr{C}_{(i)}} n^{-\rho} |\mathcal{N}_{v}(\delta)|. \tag{1.7}$$

Our goal is to prove the global lower mass-bound property for the critical components  $\mathscr{C}_{(i)}$ . For  $\mathrm{CM}_n(d)$  satisfying Assumption 1.1 and (1.6), it was shown in [16, Theorem 1] that

$$(n^{-\rho}|\mathscr{C}_{(i)}|)_{i>1} \xrightarrow{d} (\xi_i)_{i>1}, \tag{1.8}$$

<span id="page-3-7"></span>with respect to the  $\ell_{\downarrow}^2$ -topology, where the  $\xi_i$ 's are non-degenerate random variables with support  $(0,\infty)$ . Therefore, it is enough to rescale by  $n^{\rho}$  in (1.7) instead of the component sizes as given in (1.1). In order to prove tightness of  $\mathfrak{m}_i^n(\delta)$ , we will need a further technical assumption on the degrees.

<span id="page-3-3"></span>**Assumption 1.3.** Let  $V_n^*$  be a vertex chosen in a size-biased manner with sizes being  $(d_i/\ell_n)_{i\in[n]}$ , i.e.,  $\mathbb{P}(V_n^*=i)=d_i/\ell_n$ , and let  $D_n^*$  be the degree of  $V_n^*$ . There exist constants  $c_0>0$  and  $c_1>1$  such that for all  $n\geq 1$ ,

$$\mathbb{P}(l < D_n^* \le c_1 l) \ge \frac{c_0}{l^{\tau - 2}} \quad \text{for} \quad 1 \le l < d_1.$$
 (1.9)

<span id="page-3-6"></span><span id="page-3-4"></span>**Remark 1.4.** Assumption 1.3 says that the mass distribution in the tail of  $D_n^*$  is well-behaved in the sense that we have a uniform (over n) lower bound of the form (1.9). Such lower bounds can be used to obtain tail-bounds on the heights of branching processes; see Proposition 4.7 below. (See also [1, Theorem 1.3].) It can be easily shown that Assumption 1.3 holds in the examples discussed in Remark 1.2 by observing that the size-biased distribution is a power-law with exponent  $\tau-1$ .

The following theorem is the main result of this paper:

<span id="page-3-0"></span>**Theorem 1.5** (Global lower mass-bound for  $\mathrm{CM}_n(d)$ ). Suppose that Assumptions 1.1, 1.3 and the criticality condition (1.6) hold. Then, for each fixed  $i \geq 1$ ,  $(\mathscr{C}_{(i)}, n^{-\eta})_{n \geq 1}$  satisfies the global lower mass-bound, i.e., for any  $\delta > 0$ , the sequence  $(\mathfrak{m}_i^n(\delta)^{-1})_{n \geq 1}$  is tight.

By [24, Theorem 1.1], under the condition (1.4) in Assumption 1.1,

$$\liminf_{n \to \infty} \mathbb{P}(CM_n(\mathbf{d}) \text{ is simple}) > 0. \tag{1.10}$$

This immediately implies the following:

**Theorem 1.6** (Global lower mass-bound for UMn(d))**.** Under Assumption [1.1,](#page-2-0) [1.3](#page-3-3) and [\(1.6\)](#page-3-1), the largest components of UMn(d) also satisfy the global lower mass-bound property.

Next we state another important corollary, which says that the global lower massbound property is also satisfied by critical percolation clusters in CMn(d) and UMn(d). To this end, let us assume that

<span id="page-4-1"></span>
$$\lim_{n \to \infty} \frac{\sum_{i \in [n]} d_i (d_i - 1)}{\sum_{i \in [n]} d_i} = \nu > 1.$$
 (1.11)

In this regime, CMn(d) is supercritical in the sense that there exists a unique giant component whp for ν > 1, and when ν < 1, all the components have size oP(n) [\[26,](#page-28-1)[30\]](#page-28-2). Percolation refers to deleting each edge of a graph independently with probability 1 − p. The critical window for percolation on CMn(d) in the heavy-tailed setting was studied in [\[7,](#page-27-1)[16\]](#page-27-5), and is defined by the values of p given by

<span id="page-4-2"></span>
$$p_c(\lambda) = \frac{1}{\nu_n} + \frac{\lambda}{n^{\eta}} + o(n^{-\eta}).$$
 (1.12)

Let C(i)(pc(λ)) denote the i-th largest component of the graph obtained by percolation with probability pc(λ) on the graph CMn(d). Then the following result holds:

<span id="page-4-3"></span>**Theorem 1.7** (Global lower mass-bound for critical percolation)**.** Under Assumptions [1.1\(](#page-2-0)i), [1.1\(](#page-2-0)ii), [1.3,](#page-3-3) [\(1.11\)](#page-4-1) and [\(1.12\)](#page-4-2), (C(i)(pc(λ)), n<sup>−</sup><sup>η</sup> )n≥<sup>1</sup> satisfies the global lower mass-bound property, for each fixed i ≥ 1. This result also holds for percolation on UMn(d).

Let G<sup>n</sup> denote the graph obtained by doing percolation with edge retention probability pc(λ) (defined in [\(1.12\)](#page-4-2)) on CMn(d). Let d <sup>p</sup> = (d p i )i∈[n] denote the degree sequence of Gn. By [\[19,](#page-27-7) Lemma 3.2], the conditional law of Gn, conditionally on d p , is same as the law of CMn(d p ). Thus, Theorem [1.7](#page-4-3) follows from Theorem [1.5](#page-3-0) if we can show that the percolated degree sequence d p satisfies (with possibly different parameters) Assumptions [1.1](#page-2-0) and [1.3](#page-3-3) with high probability when the original degree sequence (di)i∈[n] satisfies Assumptions [1.1\(](#page-2-0)i), [1.1\(](#page-2-0)ii), [1.3,](#page-3-3) and also [\(1.6\)](#page-3-1) holds for d p if further the percolation probability is given by [\(1.12\)](#page-4-2). The verification of these assumptions are provided in Section [5.](#page-21-0)

**Remark 1.8.** It is worthwhile to point out that Theorem [1.5](#page-3-0) can be proved when the C(i) 's are endowed with a more general measure rather than the counting measure. To be precise, for any sequence of vertex weights (wv)v∈[n] , the component C(i) can be equipped with the measure µ(i)(A) = P <sup>v</sup>∈<sup>A</sup> wv/ P v∈C(i) wv, for any A ⊂ C(i) . Then Theorem [1.5](#page-3-0) can also be proved using identical methods as in this paper, with the additional assumptions that

$$\lim_{n \to \infty} \frac{1}{\ell_n} \sum_{i \in [n]} d_i w_i = \mu_w, \quad \max \left\{ \sum_{i \in [n]} d_i w_i^2, \sum_{i \in [n]} d_i^2 w_i \right\} = O(n^{3\alpha}).$$

These additional assumptions are required when we apply the results from [\[16\]](#page-27-5) (see [\[16,](#page-27-5) Theorem 21]). We adopted the simpler version of the counting measure here because it relates directly to [\[7,](#page-27-1) Theorem 2.1].

#### <span id="page-4-0"></span>**1.3 Discussion**

**Scaling limit of critical percolation clusters** We write n <sup>−</sup><sup>η</sup>C(i)(pc(λ)) to denote the i-th largest component of CMn(d, pc(λ)), viewed as a measured metric space with the metric being the graph distance re-scaled by n η , and the measure being proportional to the counting measure. Athreya, Löhr, and Winter [\[5\]](#page-27-0) showed that the global lower mass-bound property forms a crucial ingredient to prove convergence of random metric spaces such as  $n^{-\eta}\mathscr{C}_{(i)}(p_c(\lambda))$  with respect to the Gromov-Hausdorff-Prokhorov (GHP) topology on the space of compact metric spaces. The other key ingredient is the scaling limit for  $n^{-\eta}\mathscr{C}_{(i)}(p_c(\lambda))$  with respect to the Gromov-weak topology, which was established in [7, Theorem 2.1]. The Gromov-weak topology is an analogue of finite-dimensional convergence, since it considers distances between a finite number of sampled points from the underlying metric space. Thus, global functionals such as the diameter are not continuous with respect to this topology. Indeed, it may be the case that there is a long path of growing length, that has asymptotically negligible mass. In our context, the problem could arise due to paths of length much larger than  $n^{\eta}$ . The global lower mass-bound property ensures that the components have sufficient mass everywhere. This forbids the existence of long thin paths, when the total mass of the component converges. For this reason, Gromov-weak convergence and global lower mass-bound together imply GHP-convergence when the support of the limiting measure is the entire limiting space [5, Theorem 6.1]. For formal definitions of the Gromov-weak topology, and the GHP-topology on the space of compact measured metric speaes, we refer the reader to [5, 8, 22].

Following the above discussion, the next theorem is a direct consequence of Theorem 1.7, [7, Theorem 2.3] and [5, Theorem 6.1]: Let  $\mathbb{M}$  denote the space of measured compact metric spaces equipped with the GHP-topology, and let  $\mathbb{M}^{\mathbb{N}}$  denote the product space with the associated product topology.

<span id="page-5-0"></span>**Theorem 1.9** (GHP convergence of critical percolation clusters). There exists a sequence of measured metric spaces  $(\mathcal{M}_i)_{i\geq 1}=((M_i,\mathrm{d}_i,\mu_i))_{i\geq 1}\in\mathbb{M}^\mathbb{N}$  such that, under Assumptions 1.1(i), 1.1(ii), 1.3, (1.11) and (1.12), as  $n\to\infty$ ,

$$(n^{-\eta}\mathscr{C}_{(i)}(p_c(\lambda)))_{i\geq 1} \stackrel{d}{\to} (\mathscr{M}_i)_{i\geq 1} \quad \text{in } \mathbb{M}^{\mathbb{N}}. \tag{1.13}$$

Moreover, the results also hold for  $UM_n(\mathbf{d}, p_c(\lambda))$ .

The exact description of the space  $\mathcal{M}_i$  can be found in [7]. It is worthwhile mentioning a recent work by Conchon-Kerjan and Goldschmidt [15] which is closely related to Theorem 1.9. Conchon-Kerjan and Goldschmidt [15] deduce scaling limits for the vector of components in GHP-topology for critical configuration models having i.i.d power law degrees with exponent  $\tau \in (3,4)$ . In Remarks 1.2 and 1.4, we noted that Assumptions 1.1(i), 1.1(ii), and 1.3 hold when the degrees are i.i.d samples from a power-law distribution with exponent  $\tau \in (3,4)$ . Therefore, Theorem 1.9 implies that the conditional law of  $(n^{-\eta}\mathscr{C}_{(i)}(p_c(\lambda)))_{i\geq 1}$ , conditioned on the i.i.d degree sequence, converges to the law of  $(\mathcal{M}_i)_{i\geq 1}$  in  $\mathbb{M}^\mathbb{N}$  for almost every realization of the i.i.d degree sequence. Hence, Theorem 1.9 gives a quenched result whereas [15] proves an annealed result. The method of [15] relies on an alternative approach showing convergence of the height processes corresponding to the components. The associated limiting object was studied in [21], which interestingly turns out to have a quite different description than those in [7,8].

**Scaling limit of maximal distances** For any metric space (X, d) and a point  $x \in X$ , define the radius of x in X and the diameter of X by

$$\operatorname{Rad}(x,X) = \sup_{y \in X} \operatorname{d}(x,y) \quad \text{and} \quad \operatorname{diam}(X) = \sup_{x \in X} \operatorname{Rad}(x,X) = \sup_{x,y \in X} \operatorname{d}(x,y). \tag{1.14}$$

An important corollary of Theorem 1.9 is the convergence of the radius and the diameter of the critical components: Let  $V_{n,i}$  be a uniformly chosen vertex in  $\mathscr{C}_{(i)}(p_c(\lambda))$ , where  $(V_{n,i})_{i\geq 1}$  is an independent collection conditionally on  $(\mathscr{C}_{(i)}(p_c(\lambda)))_{i\geq 1}$ . Similarly, using

the notation of the scaling limits in Theorem 1.9, let  $V_i$  be chosen from  $M_i$  according to the measure  $\mu_i$  and let  $(V_i)_{i>1}$  be an independent collection conditionally on  $(\mathcal{M}_i)_{i>1}$ .

<span id="page-6-0"></span>**Corollary 1.10** (Convergence of radius and diameter). *Under* Assumptions 1.1(i), 1.1(ii), 1.3, (1.11) and (1.12), as  $n \to \infty$ ,

$$\frac{\left(n^{-\eta}\operatorname{Rad}(V_{n,i},\mathscr{C}_{(i)}(p_c(\lambda)))\right)_{i\geq 1}}{d} \cdot \left(\operatorname{Rad}(V_i,\mathscr{M}_i)\right)_{i\geq 1}, 
\left(n^{-\eta}\operatorname{diam}(\mathscr{C}_{(i)}(p_c(\lambda)))\right)_{i\geq 1}}{d} \cdot \left(\operatorname{diam}(\mathscr{M}_i)\right)_{i\geq 1},$$
(1.15)

with respect to the product topology, where  $(\mathcal{M}_i)_{i\geq 1}$  is given by Theorem 1.9. Moreover, the result also holds for  $\mathrm{UM}_n(d)$ .

Proving scaling limits for the diameter of the critical tree-like objects is often a difficult task. In [32], Szekeres proved that, for the uniform random rooted labelled tree on m vertices, the diameter, rescaled by  $\sqrt{m}$ , converges in distribution. Szekeres also provided an explicit formula for the density of the limiting distribution in [32, Page 395, (12)]. Szekeres' method was based on generating functions. Łuczak [28] also considered enumeration of trees with diameter  $\gg \sqrt{m}$ . On the other hand, Aldous [3] (see [3, Section 3.4]) noted that the GHP-convergence can be used as an effective tool to prove scaling limit results for the diameter. This is the motivating idea behind Corollary 1.10. Aldous [3] also raised a natural question whether it is possible to obtain an explicit formula from a result such as Corollary 1.10. In a recent paper, Wang [33] showed that it is indeed possible to get such a formula for the Brownian tree. In the context of Corollary 1.10, the difficulty is two-fold: First, the critical components have surplus edges. For the scaling limits of critical Erdős-Rényi random graphs, Miermont and Sen [29] recently gave a breadth-first construction, which yields an alternative description of the scaling limit of the radius function from a fixed point (rescaled by  $n^{1/3}$ ). However, the description for the diameter and an explicit formula such as the one by Wang [33] is still an open question. Second, the scaling limit in Corollary 1.10 is in the heavy-tailed universality class. Even for p-trees (see [14]) that satisfy  $p_i/(\sum_i p_i^2)^{1/2} \to \beta_i > 0$ , with  $(\beta_i)_{i \ge 1} \in \ell^2_{\downarrow} \setminus \ell^1_{\downarrow}$ , obtaining an explicit description for the limiting distribution of the diameter is an interesting question.

Compactness of the limiting metric space The limiting spaces  $\mathcal{M}_i$  are constructed by tilting the distribution of an inhomogeneous continuum random tree (ICRT), and then identifying a Poisson number of vertices to create cycles. This object is well-defined as a metric measure space for  $\theta \in \ell^3_{\downarrow} \setminus \ell^2_{\downarrow}$ . However, it may not be compact for all  $\theta \in \ell^3_{\downarrow} \setminus \ell^2_{\downarrow}$ . It is interesting to find an explicit criterion for the compactness of the limiting objects  $\mathcal{M}_i$  in terms of the underlying parameters.

Indeed, in the context of compactness of ICRTs, Aldous, Miermont, and Pitman [4, Section 7] state an additional condition, which was conjectured to be necessary and sufficient for the compactness of ICRTs. This conjectured was recently proved in [10]. In the context of critical random graphs, a recent paper by Broutin, Duquesne, and Wang [13] shows that the following criterion, analogous to [4], is sufficient for the almost sure compactness of  $\mathcal{M}_i$ :

$$\Psi_{\theta}(u) \le C \left[ \sum_{i \le i_0} \theta_i(u\theta_i) + \sum_{i \ge i_0} \theta_i(u\theta_i)^2 \right] = C \left[ u \sum_{i \le u^2} \frac{1}{i} + u^2 \sum_{i \ge u^2} \frac{1}{i^{3/2}} \right] \le C[u \log u + u], \tag{1.16}$$

and thus (1.17) cannot hold.

<span id="page-6-1"></span>**Note:** The condition (1.17) does not hold for all  $\theta \in \ell_{\downarrow}^3 \setminus \ell_{\downarrow}^2$ . Indeed, take  $\theta_i = i^{-1/2}$ . For  $u \in (\theta_2^{-1}, \infty)$ , let  $i_0 = i_0(u)$  be such that  $\theta_{i_0}^{-1} < u \le \theta_{i_0+1}^{-1}$ , i.e.,  $\sqrt{i_0} < u \le \sqrt{i_0+1}$ . Then,

$$\int_{1}^{\infty} \frac{\mathrm{d}u}{\Psi_{\theta}(u)} < \infty, \quad \text{where} \quad \Psi_{\theta}(u) = \sum_{i \ge 1} \theta_{i} (\mathrm{e}^{-u\theta_{i}} - 1 + u\theta_{i}). \tag{1.17}$$

<span id="page-7-0"></span>Our GHP convergence from Theorem 1.9 indirectly yields a sufficient condition for the compactness of the limiting metric space almost surely, by considering an asymptotic version of Assumption 1.3: Suppose  $\theta \in \ell_{\perp}^3 \setminus \ell_{\perp}^2$  and there exist constants  $c_0 > 0$  and  $c_1 > 1$ such that

$$x^{\tau-2} \times \sum_{i=1}^{\infty} \theta_i \mathbb{1} \{x < \theta_i \le c_1 x\} \ge c_0 \quad \text{for all } x \in (0, \theta_1).$$
 (1.18)

<span id="page-7-1"></span>The fact that (1.18) is a sufficient condition for the compactness of  $\mathcal{M}_i$  follows immediately from Theorem 1.9 and the following proposition:

<span id="page-7-2"></span>**Proposition 1.11.** Consider any  $\theta \in \ell^3_{\downarrow} \setminus \ell^2_{\downarrow}$  such that (1.18) holds. Then there exists a sequence of degree sequences satisfying Assumptions 1.1(i), 1.1(ii), 1.3, and (1.11).

We will prove Proposition 1.11 in Appendix B. A natural question is how the conditions in (1.17) and (1.18) compare. We argue below that, in fact, (1.18) is strictly stronger than (1.17).

Recall that C>0 is a generic notation for a constant whose value can be different in different expressions. We first show that (1.18) implies (1.17). Suppose  $\theta_i > \theta_{i+1}$ . Then

$$\theta_{i+1}^{\tau-2} \sum_{j=1}^{i} \theta_j \ge \theta_{i+1}^{\tau-2} \sum_{j=1}^{\infty} \theta_j \cdot \mathbb{1} \left\{ \theta_{i+1} < \theta_j \le c_1 \theta_{i+1} \right\} \ge c_0, \tag{1.19}$$

<span id="page-7-3"></span>where the last step uses (1.18). Now, for  $u \in (\frac{1}{\theta_i}, \frac{1}{\theta_{i+1}}]$ 

$$\Psi_{\theta}(u) \ge C \left[ \sum_{k=1}^{i} u\theta_{k}^{2} + \sum_{k=i+1}^{\infty} u^{2}\theta_{k}^{3} \right] \ge Cu\theta_{i+1} \sum_{k=1}^{i} \theta_{k} 
= \frac{Cu\theta_{i+1}^{\tau-2} \sum_{k=1}^{i} \theta_{k}}{\theta_{i+1}^{\tau-3}} \ge \frac{Cuc_{0}}{\theta_{i+1}^{\tau-3}} \ge Cc_{0}u^{\tau-2}.$$
(1.20)

<span id="page-7-5"></span>Thus,  $\int_{\theta_1^{-1}}^{\infty} \frac{\mathrm{d}u}{\Psi_{\theta}(u)} \leq C \int_{\theta_1^{-1}}^{\infty} u^{-(\tau-2)} \mathrm{d}u < \infty$ , since  $\tau > 3$ . This yields (1.17). To see that the implication is strict, take  $\theta_i = (i^{\alpha} \log(i+2))^{-1}$ . Then

<span id="page-7-4"></span>

$$\theta_{i+1}^{\tau-2} \sum_{i=1}^{i} \theta_{j} \le \left( (i+1)^{\alpha} \log(i+3) \right)^{-(\tau-2)} \sum_{i=1}^{i} j^{-\alpha} \le \frac{C}{\log^{\tau-2} i},\tag{1.21}$$

which tends to zero as  $i \to \infty$ . However, as we have seen in (1.19), (1.18) would imply that the left side of (1.21) is bounded away from zero. Thus, (1.18) does not hold in this case. To see that (1.17) does hold, note that  $\theta_i \geq \theta_i' := i^{-\alpha'}$  for all large enough i, where  $\alpha' = \frac{1}{\tau'-1}$  and  $3 < \tau' < \tau$ . Then  $(\theta_i')_{i \ge 1}$  satisfies (1.18). Therefore, a computation similar to (1.20) yields, for  $u \in (\frac{1}{\theta_i}, \frac{1}{\theta_{i+1}}]$ ,

$$\Psi_{\theta}(u) \ge Cu\theta_{i+1} \sum_{k=1}^{i} \theta_k \ge Cu\theta'_{i+1} \sum_{k=1}^{i} \theta'_k \ge \frac{Cu}{(\theta'_i)^{\tau-3}}.$$
 (1.22)

Since  $u \leq (i+1)^{\alpha} \log(i+3)$ , we can choose  $\delta > 0$  such that  $u^{1+\delta} \leq Ci^{\alpha'} = C/\theta'_i$ . Therefore,  $\Psi_{\theta}(u) \geq Cu^{1+(\tau-3)(1+\delta)}$ . Thus, (1.17) follows.

**Proof ideas and technical motivation for this work** The proof of Theorem [1.5](#page-3-0) consists of two main steps, that form the key ideas in the argument. The first step is to show that the neighborhoods of the high-degree vertices, called hubs, have mass ΘP(n ρ ). Secondly, any small εn<sup>η</sup> neighborhood contains a hub with high probability. These two facts, summarized in Propositions [2.1](#page-8-0) and [2.2](#page-8-1) below, together ensure that the total mass of any neighborhood of C(i) of radius εn<sup>η</sup> is bounded away from zero. These two facts were proved in [\[8\]](#page-27-8) in the context of rank-one inhomogeneous random graphs. However, the proof techniques are completely different here. The main advantage in [\[8\]](#page-27-8) was that the breadth-first exploration of components could be dominated by a branching process with mixed Poisson progeny distribution that is independent of n. This allows one to use existing literature to estimate the probabilities that a long path exists in the branching process. However, such a technique is specific to rank-one inhomogeneous random graphs and does not work in the cases where the above stochastic domination does not hold. This was one of the technical motivations for this work. Moreover, the final section contains results about exponential tail-bounds for the number of edges in large critical components (Proposition [4.1\)](#page-12-0), as well as a coupling of the neighborhood exploration with a branching process with stochastically larger progeny distribution (Section [4.2\)](#page-14-0), which are both interesting in their own right.

**Organization of this paper** The rest of this paper is organized as follows: In Section [2,](#page-8-2) we state two key propositions, the first involving the total mass of small neighborhoods, and the second involving a bound on the diameter of a slightly subcritical CMn(d). The proof of Theorem [1.5](#page-3-0) is completed in Section [2.](#page-8-2) In Section [3,](#page-9-0) we derive the required bounds on the total mass of small neighborhoods. In Section [4,](#page-11-0) we obtain bounds on the diameter of the connected components after removing the high-degree vertices. In Section [5,](#page-21-0) we prove Assumptions [1.1,](#page-2-0) [1.3](#page-3-3) for the percolated degree sequence, which allows us to conclude Theorem [1.7.](#page-4-3)

#### <span id="page-8-2"></span>**2 Proof of the global lower mass-bound**

In this section, we first state the two key ingredients in Propositions [2.1](#page-8-0) and [2.2,](#page-8-1) and then complete the proof of Theorem [1.5.](#page-3-0) The proofs of Propositions [2.1](#page-8-0) and [2.2](#page-8-1) are given in the subsequent sections. The first ingredient shows that hub i has sufficient mass close to it with high probability:

<span id="page-8-0"></span>**Proposition 2.1.** Assume that Assumptions [1.1](#page-2-0) and [\(1.6\)](#page-3-1) hold. Recall that Nv(δ) denotes the δn<sup>η</sup> neighborhood of v. For each fixed i ≥ 1 and ε<sup>2</sup> > 0, there exists δi,ε<sup>2</sup> > 0 and ni,ε<sup>2</sup> ≥ 1 such that, for any δ ∈ (0, δi,ε<sup>2</sup> ] and n ≥ ni,ε<sup>2</sup> ,

<span id="page-8-4"></span>
$$\mathbb{P}(|\mathcal{N}_i(\delta)| \le \theta_i \delta n^{\rho}) \le \frac{\varepsilon_2}{2^{i+1}}.$$
(2.1)

Next, we need some control on the diameter of the graph after removing the hubs. Denote by G >K n the graph obtained by removing the vertices [K] = {1, . . . , K} having the largest degrees and the edges incident to them from CMn(d). Note that G >K n is a configuration model conditionally on its degree sequence. Let ∆>K denote the maximum of the diameters of the connected components of G >K n . The following proposition shows that, for large K, ∆>K is small with high probability:

<span id="page-8-1"></span>**Proposition 2.2.** Assume that Assumptions [1.1,](#page-2-0) [1.3](#page-3-3) and [\(1.6\)](#page-3-1) hold. Then, for any ε1, ε<sup>2</sup> > 0, there exists K = K(ε1, ε2) and n<sup>0</sup> = n0(ε1, ε2) such that for all n ≥ n0,

<span id="page-8-3"></span>
$$\mathbb{P}\left(\Delta^{>\kappa} > \varepsilon_1 n^{\eta}\right) \le \frac{\varepsilon_2}{4}.\tag{2.2}$$

We now prove Theorem [1.5](#page-3-0) assuming Propositions [2.1](#page-8-0) and [2.2:](#page-8-1)

Proof of Theorem 1.5. Fix  $i \geq 1$  and  $\varepsilon_1, \varepsilon_2 > 0$ . For a component  $\mathscr{C} \subset \mathrm{CM}_n(d)$ , we write  $\Delta(\mathscr{C})$  to denote its diameter. Let us choose K and  $n_0$  so that (2.2) holds for all  $n \geq n_0$ . In view of Proposition 2.1, let  $\delta_0 = \min\{\varepsilon_1, \delta_{1,\varepsilon_2}, \ldots, \delta_{K,\varepsilon_2}\}/2$ , and  $n'_0 = \max\{n_0, n_{1,\varepsilon_2}, \ldots, n_{K,\varepsilon_2}\}$ . Thus, for all  $n \geq n'_0$ , (2.1) is satisfied for all  $i \in [K]$ . Define

$$F_1 := \{ \Delta^{>K} < \varepsilon_1 n^{\eta} / 2 \}, \quad F_2 := \{ \Delta(\mathscr{C}_{(i)}) > \varepsilon_1 n^{\eta} / 2 \}.$$
 (2.3)

Notice that, on the event  $F_1 \cap F_2$ , it must be the case that one of the vertices in [K] belongs to  $\mathscr{C}_{(i)}$ , and that the union of the neighborhoods of [K] of radius  $\lceil \varepsilon_1 n^{\eta}/2 \rceil + 1 \approx \varepsilon_1 n^{\eta}/2$  covers  $\mathscr{C}_{(i)}$ . Therefore, given any vertex  $v \in \mathscr{C}_{(i)}$ ,  $\mathcal{N}_v(\varepsilon_1)$  contains at least one of the neighborhoods  $(\mathcal{N}_j(\varepsilon_1/2))_{j \in [K]}$ . This observation yields that

$$\inf_{v \in \mathscr{C}_{(i)}} n^{-\rho} |\mathcal{N}_v(\varepsilon_1)| \ge \min_{j \in [K]} n^{-\rho} |\mathcal{N}_j(\varepsilon_1/2)| \ge \min_{j \in [K]} n^{-\rho} |\mathcal{N}_j(\delta_0)|. \tag{2.4}$$

<span id="page-9-1"></span>Thus, for all  $n > n'_0$ ,

$$\mathbb{P}\Big(F_1 \cap F_2 \cap \Big\{ \inf_{v \in \mathscr{C}_{(i)}} n^{-\rho} |\mathcal{N}_v(\varepsilon_1)| \le \theta_K \delta_0 \Big\} \Big) 
\le \sum_{j \in [K]} \mathbb{P}\Big(|\mathcal{N}_j(\delta)| \le \theta_j \delta_0 n^{\rho}\Big) \le \sum_{j=1}^K \frac{\varepsilon_2}{2^{j+1}} \le \frac{\varepsilon_2}{2},$$
(2.5)

where the one-but-last step follows from Proposition 2.1. Further, on the event  $F_2^c$ ,  $|\mathcal{N}_v(\varepsilon_1)| = |\mathscr{C}_{(i)}|$  for all  $v \in \mathscr{C}_{(i)}$ . Moreover, using (1.8), it follows that  $n^{-\rho}|\mathscr{C}_{(i)}|$  converges in distribution to a random variable with strictly positive support. Using the Portmanteau theorem, the above implies that for any  $\delta_0' > 0$ , there exists  $\tilde{n}_0 = \tilde{n}_0(\varepsilon_2, \delta_0')$  such that, for all  $n \geq \tilde{n}_0$ ,

$$\mathbb{P}\left(n^{-\rho}|\mathscr{C}_{(i)}| \le \delta_0'\right) \le \frac{\varepsilon_2}{4}.\tag{2.6}$$

Therefore

<span id="page-9-2"></span>
$$\mathbb{P}\left(F_2^c \cap \left\{ \inf_{v \in \mathscr{C}_{(i)}} n^{-\rho} | \mathcal{N}_v(\varepsilon_1) | \le \delta_0' \right\} \right) \le \frac{\varepsilon_2}{4}. \tag{2.7}$$

Now, using (2.5) and (2.7), together with Proposition 2.2, it follows that, for any  $n \ge \max\{n'_0, \tilde{n}_0\}$ , and K chosen as above,

$$\mathbb{P}\left(\inf_{v\in\mathscr{C}_{(i)}} n^{-\rho} |\mathcal{N}_v(\varepsilon_1)| \le \min\{\delta_0', \theta_K \delta_0\}\right) \le \varepsilon_2. \tag{2.8}$$

This completes the proof of Theorem 1.5.

#### <span id="page-9-0"></span>3 Lower bound on the total mass of neighborhoods of hubs

In this section, we prove Proposition 2.1.

*Proof of Proposition 2.1.* Let us denote the component of  $\mathrm{CM}_n(d)$  containing vertex i by  $\mathscr{C}(i)$ . Consider the breadth-first exploration of  $\mathscr{C}(i)$  starting from vertex i, given by the following exploration algorithm [16]:

<span id="page-9-3"></span>**Algorithm 1** (Exploring the graph). The algorithm carries along vertices that can be alive, active, exploring and killed, and half-edges that can be alive, active or killed. We sequentially explore the graph as follows:

(S0) At stage l=0, all the vertices and the half-edges are alive, and only the half-edges associated to vertex i are active. Also, there are no exploring vertices except i.

- (S1) At each stage l, if there is an exploring vertex, take an active half-edge e of an exploring vertex v and pair it uniformly to another alive half-edge f. Kill e, f. If f is incident to a vertex v' that has not been discovered before, then declare all the half-edges incident to v' (if any) active, except f. If degree(v') = 1 (i.e. the only half-edge incident to v' is f) then kill v'. Otherwise,  $declare\ v'$  to be active and larger than all other vertices that are alive. After killing e, if v does not have another active half-edge, then kill v also. If there is no exploring vertex at the beginning of stage l, we pick the oldest active half-edge, declare the corresponding vertex to be exploring, and then execute the same process as above.
- (S2) Repeat (S1) until there is no active half-edges left.

Call a vertex discovered if it is either active or killed. Let  $\mathscr{V}_l$  denote the set of vertices discovered up to time l and  $\mathcal{I}_i^n(l) := \mathbb{1}\{j \in \mathscr{V}_l\}$ . Define the exploration process by

<span id="page-10-2"></span>
$$S_n(l) = d_i + \sum_{j \neq i} d_j \mathcal{I}_j^n(l) - 2l = d_i + \sum_{j \neq i} d_j \left( \mathcal{I}_j^n(l) - \frac{d_j}{\ell_n} l \right) + \left( \frac{1}{\ell_n} \sum_{j \neq i} d_j^2 - 2 \right) l.$$
 (3.1)

Note that the exploration process keeps track of the number of active half-edges. Thus,  $\mathscr{C}(i)$  is explored when  $S_n$  hits zero. Moreover, since one edge is explored at each step, the hitting time of zero is the total number of edges in  $\mathscr{C}(i)$ . Define the re-scaled version  $\bar{S}_n$  of  $S_n$  by  $\bar{S}_n(t) = n^{-\alpha} S_n(|tn^{\rho}|)$ . Then, by Assumption 1.1 and (1.6),

$$\bar{S}_n(t) = \theta_i - \frac{\theta_i^2 t}{\mu} + n^{-\alpha} \sum_{j \neq i} d_j \left( \mathcal{I}_j^n(tn^\rho) - \frac{d_j}{\ell_n} tn^\rho \right) + \lambda t + o(1). \tag{3.2}$$

The convergence of this exploration process was considered in [16, Theorem 8] except for the fact that the exploration process started at zero in [16]. However, using identical arguments to [16, Theorem 8], it can be shown that

$$\bar{S}_n \stackrel{d}{\to} S_{\infty},$$
 (3.3)

<span id="page-10-0"></span>with respect to the Skorohod  $J_1$ -topology, where

$$S_{\infty}(t) = \theta_i - \frac{\theta_i^2 t}{\mu} + \sum_{j \neq i} \theta_j \left( \mathcal{I}_j(t) - \frac{\theta_j t}{\mu} \right) + \lambda t, \tag{3.4}$$

with  $\mathcal{I}_j(s) := \mathbb{1}\left\{\xi_j \leq s\right\}$  and  $\xi_j \sim \operatorname{Exponential}(\theta_j/\mu)$  independently of each other.

Let  $h_n(u)$  (respectively  $h_\infty(u)$ ) denote the first hitting time of  $\bar{S}_n$  (respectively  $S_\infty$ ) of u. More precisely,

$$h_n(u) := \inf \left\{ t : \bar{S}_n(t) \le u \text{ or } \lim_{t' \to t} \bar{S}_n(t') \le u \right\},\tag{3.5}$$

and define  $h_{\infty}(u)$  similarly by replacing  $\bar{S}_n(t)$  by  $\bar{S}_{\infty}(t)$ . Note that, by [16, Lemma 36], the distribution of  $h_{\infty}(u)$  does not have any atoms and therefore, for any  $\varepsilon_2 > 0$ , there exists  $\beta_{\varepsilon_2,i} > 0$  such that

$$\mathbb{P}(h_{\infty}(\theta_i/2) \le \beta_{\varepsilon_2,i}) \le \frac{\varepsilon_2}{2^{i+1}}.$$

Now we use the following fact:

<span id="page-10-1"></span>**Fact 3.1.** Let  $(X_n(t))_{t\geq 0} \stackrel{d}{\to} (X(t))_{t\geq 0}$  in Skorohod  $J_1$ -topology and let  $h(X_n)$  (respectively h(X)) denote the hitting time to zero of  $X_n$  (respectively X). Then,

$$\liminf_{n \to \infty} \mathbb{P}(h(X_n) > a) \ge \mathbb{P}(h(X) > a) \quad \text{for all } a > 0.$$
 (3.6)

*Proof.* Let  $(f_n)_{n\geq 1}$  be such that  $h(f_n)\leq a$  for all  $n\geq 1$  and  $f_n\to f$  in the Skorohod  $J_1$ -topology as  $n\to\infty$ . Now,  $h(f_n)\leq a$  implies that  $\inf_{t\in [0,a]}f_n(t)\leq 0$ . Using [34, Theorem 13.4.1], it follows that  $\inf_{t\in [0,a]}f(t)\leq 0$  and thus  $h(f)\leq a$ . Therefore, we have shown that  $\{f\colon h(f)\leq a\}$  is a closed set in the Skorohod  $J_1$ -topology, and therefore  $\{f\colon h(f)>a\}$  is an open set. The proof follows using the Portmanteau theorem [9, Theorem 2.1 (iv)].  $\square$ 

Using (3.3) and Fact 3.1, there exists  $n_{i,\varepsilon_2} \geq 1$  such that, for all  $n \geq n_{i,\varepsilon_2}$ ,

$$\mathbb{P}(h_n(\theta_i/2) \le \beta_{\varepsilon_2,i}) \le \frac{\varepsilon_2}{2^i}.$$
(3.7)

<span id="page-11-1"></span>Our first goal is to show that there exists a  $\delta_{i,\varepsilon}$  such that for any  $\delta \in (0,\delta_{i,\varepsilon_2}]$ ,

$$\sum_{k \in \mathcal{N}_i(\delta)} d_k \le \theta_i \delta n^{\rho} \quad \Longrightarrow \quad h_n(\theta_i/2) \le \beta_{\varepsilon_2, i}. \tag{3.8}$$

Recall that  $\mathcal{N}_v(\delta)$  denotes the  $\delta n^\eta$  neighborhood of v in  $\mathrm{CM}_n(d)$ . To prove (3.8), let  $\partial(j)$  denote the set of vertices at distance j from i. Let  $E_{j1}$  denote the total number of edges between vertices in  $\partial(j)$  and  $\partial(j-1)$ , and let  $E_{j2}$  denote the number of edges within the vertices in  $\partial(j-1)$ . Define  $E_j=E_{j1}+E_{j2}$ . Fix any  $\delta<2\beta_{\varepsilon_2,i}/\theta_i$ . Note that if  $\sum_{k\in\mathcal{N}_i(\delta)}d_k\leq\theta_i\delta n^\rho$ , then the total number of edges in  $\mathcal{N}_i(\delta)$  is at most  $\theta_i\delta n^\rho/2$ . Thus there exists  $j\leq\delta n^\eta$  such that  $E_j\leq\theta_i\delta n^\rho/2\delta n^\eta=\theta_i n^\alpha/2$ . This implies that  $S_n$  must go below  $\theta_i n^\alpha/2$  before exploring all the vertices in  $\mathcal{N}_i(\delta)$ . This is because we are exploring the components in a breadth-first manner and  $\overline{S}_n$  keeps track of the number of active half-edges, which in turn are the potential connections to vertices at the next level. Since one edge is explored in each time step, and we rescale time by  $n^\rho$ , this implies that

$$h_n(\theta_i/2) \le \frac{1}{2} n^{-\rho} \sum_{k \in \mathcal{N}_i(\delta)} d_k \le \theta_i \delta/2 \le \beta_{\varepsilon_2, i}. \tag{3.9}$$

Therefore, for all  $n \geq n_{i,\varepsilon_2}$ ,

<span id="page-11-2"></span>
$$\mathbb{P}\left(\sum_{k \in \mathcal{N}_i(\delta)} d_k \le \theta_i \delta n^{\rho}\right) \le \mathbb{P}(h_n(\theta_i/2) \le \beta_{\varepsilon_2, i}) \le \frac{\varepsilon_2}{2^i}.$$
 (3.10)

Finally, to conclude Proposition 2.1 from (3.10), we use the result from [16, Lemma 22] that, for any T > 0,

$$\sup_{u \le T} \left| \sum_{i \in [n]} \mathcal{I}_i^n(un^\rho) - un^\rho \right| = o_{\mathbb{P}}(n^\rho). \tag{3.11}$$

This implies that the difference between the number of edges and the number of vertices explored up to time  $un^{\rho}$  is  $o_{\mathbb{P}}(n^{\rho})$  uniformly over  $u \leq T$ . The proof of Proposition 2.1 now follows.

#### <span id="page-11-0"></span>4 Diameter after removing hubs

Throughout the remainder of the paper, we fix the convention that C, C', C'' > 0 etc. denote constants whose value can change from line to line. Recall the definition of the graph  $\mathcal{G}_n^{>K}$  from Proposition 2.2. If we keep on exploring  $\mathcal{G}_n^{>K}$  in a breadth-first manner using Algorithm 1 and ignore the cycles created, then we get a random tree. The idea is to couple neighborhoods in  $\mathcal{G}_n^{>K}$  with a suitable branching process such that the progeny distribution of the branching process dominates the number of children of each vertex in the breadth-first tree. Therefore, when there is a long path in  $\mathcal{G}_n^{>K}$  that makes the diameter large, that long path must be present in the branching process

as well under the above coupling. In this way, the question about the diameter of G >K n reduces to the question about the height of a branching process. To estimate the height suitably, we use a recent beautiful proof technique by Addario-Berry [\[1\]](#page-26-1) which allows one to relate the height of a branching process to the sum of inverses of the associated breadth-first random walk.

In Section [4.1,](#page-12-1) we establish tail bounds for the number of edges within components. This allows us to formulate the desired coupling in Section [4.2.](#page-14-0) In Section [4.3,](#page-15-0) we analyze the breadth-first random walk to show that it is unlikely that the height of the branching process is larger than εn<sup>η</sup> . These bounds are different from those derived in [\[1\]](#page-26-1) since our branching process depends on n and there is a joint scaling involved between the distances and the law of the branching process.

#### <span id="page-12-1"></span>**4.1 Asymptotics for the number of edges**

For a graph G, let E(G) denote the number of edges in G.

<span id="page-12-0"></span>**Proposition 4.1.** Suppose that Assumption [1.1](#page-2-0) and [\(1.6\)](#page-3-1) hold. For all ε ∈ (0, 4−τ τ−1 ), and sufficiently large n,

$$\mathbb{P}(\mathcal{E}(\mathscr{C}(i)) > n^{\rho + \varepsilon}) \le C e^{-C' n^{\varepsilon/2}},\tag{4.1}$$

for some absolute constants C, C<sup>0</sup> > 0 and all i ∈ [n].

The proof of Proposition [4.1](#page-12-0) relies on concentration techniques for martingales. We start by defining the relevant notation. Consider exploring CMn(d) with Algorithm [1,](#page-9-3) and let the associated exploration process be defined in [\(3.1\)](#page-10-2). Let us denote the degree of the vertex found at step l by d(l) . If no new vertex is found at step l, then d(l) = 0. Also, let F<sup>l</sup> denote the sigma-algebra containing all the information revealed by the exploration process up to time l. Thus,

$$S_n(0) = d_i$$
, and  $S_n(l) = S_n(l-1) + (d_{(l)} - 2)$ . (4.2)

Using the Doob-Meyer decomposition, one can write

$$S_n(l) = S_n(0) + M_n(l) + A_n(l), (4.3)$$

where M<sup>n</sup> is a martingale with respect to (Fl)l≥1. The drift A<sup>n</sup> and the quadratic variation hMni of M<sup>n</sup> are given by

$$A_n(l) = \sum_{j=1}^{l} \mathbb{E} \left[ d_{(j)} - 2 | \mathscr{F}_{j-1} \right], \quad \langle M_n \rangle(l) = \sum_{j=1}^{l} \text{Var} \left( d_{(j)} | \mathscr{F}_{j-1} \right). \tag{4.4}$$

We will show that for any ε ∈ (0, ε0), the following two lemmas hold:

<span id="page-12-2"></span>**Lemma 4.2.** Suppose that Assumption [1.1](#page-2-0) and [\(1.6\)](#page-3-1) hold. For all ε ∈ (0, 4−τ τ−1 ), and sufficiently large n,

$$\mathbb{P}(n^{-(\alpha+\varepsilon)}M_n(n^{\rho+\varepsilon}) > 1) \le Ce^{-C'n^{\varepsilon}},\tag{4.5}$$

for some absolute constants C, C<sup>0</sup> > 0.

<span id="page-12-3"></span>**Lemma 4.3.** Suppose that Assumption [1.1](#page-2-0) and [\(1.6\)](#page-3-1) hold. For all fixed K ≥ 1, ε ∈ (0, 4−τ τ−1 ), and sufficiently large n,

$$\mathbb{P}\left(n^{-(\alpha+\varepsilon)}A_n(n^{\rho+\varepsilon}) \ge -C\sum_{i=1}^K \theta_i^2\right) \le Ce^{-C'n^{\varepsilon/2}},\tag{4.6}$$

for some absolute constants C, C<sup>0</sup> > 0.

Proof of Proposition 4.1 subject to Lemmas 4.2, 4.3. Throughout, we write  $t_n:=n^{\rho+\varepsilon}$ . Note that we can choose  $K\geq 1$  such that  $\sum_{i=1}^K \theta_i^2$  is arbitrarily large since  $\pmb{\theta}\notin \ell^2_\downarrow$ . Thus, if  $n^{-(\alpha+\varepsilon)}M_n(t_n)\leq 1$  and  $n^{-(\alpha+\varepsilon)}A_n(t_n)\leq -C\sum_{i=1}^K \theta_i^2$ , then  $n^{-(\alpha+\varepsilon)}S_n(t_n)<0$ , and therefore  $\mathscr{C}(i)$  must be explored before time  $t_n$ , and thus  $\mathrm{E}(\mathscr{C}(i))\leq t_n$ . As a result, Lemmas 4.2 and 4.3 together complete the proof of Proposition 4.1.

*Proof of Lemma 4.2.* First note that  $\frac{4-\tau}{\tau-1}+\rho=2\alpha<1$  and therefore  $t_n=o(n)$ . Thus, uniformly over  $j\leq t_n$ ,

$$\operatorname{Var}(d_{(j)}|\mathscr{F}_{j-1}) \le \mathbb{E}[d_{(j)}^2|\mathscr{F}_{j-1}] = \frac{\sum_{j \notin \mathscr{V}_{j-1}} d_j^3}{\ell_n - 2j + 2} \le \frac{\sum_{j \in [n]} d_j^3}{\ell_n - 2t_n + 2} \le Cn^{3\alpha - 1},\tag{4.7}$$

so that, almost surely,

<span id="page-13-1"></span>
$$\langle M_n \rangle (t_n) \le t_n C n^{3\alpha - 1} = C n^{2\alpha + \varepsilon}.$$
 (4.8)

Also,  $d_{(j)} \leq Cn^{\alpha}$  almost surely. We can now use Freedman's inequality [20, Proposition 2.1] which says that if  $Y(k) = \sum_{j \leq k} X_j$  with  $\mathbb{E}[X_j | \mathcal{F}_{j-1}] = 0$  (for some filtration  $(\mathcal{F}_j)_{j \geq 1}$ ) and  $\mathbb{P}(|X_j| \leq R, \ \forall j \geq 1) = 1$ , then, for any a, b > 0,

$$\mathbb{P}(Y(k) \ge a, \text{ and } \langle Y \rangle(k) \le b) \le \exp\left(\frac{-a^2}{2(Ra+b)}\right).$$
 (4.9)

<span id="page-13-0"></span>We apply (4.9) with  $a = n^{\alpha + \varepsilon}$ ,  $b = Cn^{2\alpha + \varepsilon}$  and  $R = Cn^{\alpha}$ . Note that  $\langle M_n \rangle(t_n) \leq b$  almost surely by (4.8). It follows that

$$\mathbb{P}(M_n(t_n) > n^{\alpha + \varepsilon}) \le \exp\left(-\frac{n^{2\alpha + 2\varepsilon}}{2C(n^{\alpha}n^{\alpha + \varepsilon} + n^{2\alpha + \varepsilon})}\right) \le Ce^{-C'n^{\varepsilon}},\tag{4.10}$$

and the proof follows.

Proof of Lemma 4.3. Note that

$$\mathbb{E}\left[d_{(i)} - 2|\mathscr{F}_{i-1}\right] = \frac{\sum_{j \notin \mathscr{V}_{i-1}} d_j^2}{\ell_n - 2i + 1} - 2$$

$$= \frac{1}{\ell_n} \sum_{j \in [n]} d_j(d_j - 2) - \frac{1}{\ell_n} \sum_{j \in \mathscr{V}_{i-1}} d_j^2 + \frac{(2i - 1) \sum_{j \notin \mathscr{V}_{i-1}} d_j^2}{\ell_n(\ell_n - 2i + 1)}$$

$$\leq \lambda n^{-\eta} - \frac{1}{\ell_n} \sum_{j \in \mathscr{V}_{i-1}} d_j^2 + \frac{(2i - 1)}{(\ell_n - 2i + 1)^2} \sum_{j \in [n]} d_j^2 + o(n^{-\eta})$$
(4.11)

uniformly over  $i \leq t_n$ . Therefore, for all sufficiently large n,

<span id="page-13-2"></span>
$$A_{n}(t_{n}) = \sum_{j=1}^{t_{n}} \mathbb{E}\left[d_{(j)} - 2|\mathscr{F}_{j-1}\right] \leq \lambda t_{n} n^{-\eta} - \frac{1}{\ell_{n}} \sum_{i=1}^{t_{n}} \sum_{j \in \mathscr{V}_{i-1}} d_{j}^{2} + \frac{Ct_{n}^{2}}{\ell_{n}} + o(n^{\alpha + \varepsilon})$$

$$= \lambda n^{\alpha + \varepsilon} - \frac{1}{\ell_{n}} \sum_{i=1}^{t_{n}} \sum_{j \in \mathscr{V}_{i-1}} d_{j}^{2} + o(n^{\alpha + \varepsilon}),$$
(4.12)

where in the second step we have used  $\sum_{i\in[n]}d_i^2/\ell_n=O(1)$ , and in the last step we have used that  $t_n^2/\ell_n=O(n^{2\rho+2\varepsilon-1})=o(n^{\alpha+\varepsilon})$  for  $\varepsilon<1+\alpha-2\rho=\frac{4-\tau}{\tau-1}$ . Let us denote the second term in (4.12) by (A). To analyze (A), define the event

$$\mathcal{A}_n := \{ \exists j : d_j > n^{\alpha - \varepsilon/2}, j \notin \mathcal{V}_{t_n/2} \}. \tag{4.13}$$

<span id="page-14-1"></span>Then, for all sufficiently large n,

$$\mathbb{P}(\mathcal{A}_n) \le \sum_{j: d_i > n^{\alpha - \varepsilon/2}} \left( 1 - \frac{d_j}{\ell_n - 2t_n} \right)^{t_n} \le n e^{-Cn^{\varepsilon/2}}.$$
 (4.14)

<span id="page-14-2"></span>On the event  $\mathcal{A}_n^c$ ,

$$(\mathbf{A}) = \frac{1}{\ell_n} \sum_{i=1}^{t_n} \sum_{j \in [n]} d_j^2 \mathbb{1}\{j \in \mathcal{V}_{i-1}\} \ge \frac{1}{\ell_n} \sum_{i=\frac{t_n}{L}+1}^{t_n} \sum_{j=1}^{K} d_j^2 \ge C n^{\alpha+\varepsilon} \sum_{j=1}^{K} \theta_j^2. \tag{4.15}$$

Combining (4.12), (4.14) and (4.15) now completes the proof.

#### <span id="page-14-0"></span>4.2 Coupling with branching processes

Recall that  $\mathscr{C}(i)$  is the connected component in  $\mathrm{CM}_n(d)$  containing vertex i. Define the event  $\mathcal{K}_n := \{\mathrm{E}(\mathscr{C}(i)) > n^{\rho+\varepsilon}\}$ . Proposition 4.1 implies that the probability of  $\mathcal{K}_n$  happening is exponentially small in n. On the event  $\mathcal{K}_n^c$ , we can couple the breadth-first exploration starting from vertex i with a suitable branching process. Let  $n_k$  denote the number of vertices of degree k and consider the branching process  $\mathcal{X}_n(i)$  starting with  $d_i$  individuals, and the progeny distribution  $\bar{\xi}_n$  given by

$$\mathbb{P}\left(\bar{\xi}_n = k\right) = \bar{p}_k = \begin{cases} \frac{(k+1)n_{k+1}}{\ell_n} & \text{for } k \ge 1, \\ \frac{n_1 - 2n^{\rho + \varepsilon}}{\ell_n} & \text{for } k = 0, \end{cases}$$
(4.16)

<span id="page-14-3"></span>where  $\underline{\ell}_n = \ell_n - 2n^{\rho+\varepsilon}$ . Note that, at each step of the exploration, we have at most  $(k+1)n_{k+1}$  half-edges that are incident to vertices having k further unpaired half-edges. Further, on the event  $\mathcal{K}_n^c$ , we have at least  $\underline{\ell}_n$  choices for pairing. Therefore, the number of active half-edges discovered at each step in the breadth-first exploration of the neighborhoods of i is stochastically dominated by  $\bar{\xi}_n$ . This proves the next proposition, which we state after setting up some further notation. Recall that  $\mathcal{G}_n^{>i-1}$  denotes the graph obtained by deleting vertices in [i-1] and the associated edges from  $\mathrm{CM}_n(d)$ . Let  $\partial_i(r)$  denote the number of vertices at distance r from vertex i in the graph  $\mathcal{G}_n^{>i-1}$ . Let  $\bar{\xi}_n(i)$  denote the random variable with the distribution in (4.16) truncated in such a way that  $\{d_1,\ldots,d_{i-1}\}$  are excluded from the support. More precisely,

$$\mathbb{P}(\bar{\xi}_n(i) = k) = \begin{cases}
0 & \text{for } k > d_i, \\
\frac{(k+1)}{L} \# \{ j \ge i : d_j = k+1 \} & \text{for } 1 \le k \le d_i, \\
\frac{n_1 - 2n^{\rho + \varepsilon}}{L} & \text{for } k = 0,
\end{cases}$$
(4.17)

<span id="page-14-4"></span>where  $L=\underline{\ell}_n-\sum_{j=1}^{i-1}d_j$  is the appropriate normalizing constant. Let  $\mathcal{X}_{n,\mathrm{res}}(i)$  denote the branching process starting with  $d_i$  individuals and progeny distribution  $\bar{\xi}_n(i)$  and let  $\bar{\partial}_i(r)$  denote the number of individuals in generation r of  $\mathcal{X}_{n,\mathrm{res}}(i)$ . Then the above stochastic domination argument immediately yields the next proposition:

<span id="page-14-5"></span>**Proposition 4.4.** Suppose that Assumption 1.1 and (1.6) hold. Let  $K_n$  be as described in Lemma A.1 below. For all  $r \ge 1$ ,  $1 \le i \le K_n$ ,  $\varepsilon \in (0, \frac{4-\tau}{\tau-1})$  and  $n \ge 1$ ,

$$\mathbb{P}(\partial_i(r) \neq \emptyset) < \mathbb{P}(\bar{\partial}_i(r) \neq \emptyset) + \mathbb{P}(\mathbb{E}(\mathscr{C}(i)) > n^{\rho + \varepsilon}). \tag{4.18}$$

Before proceeding with the next section in which we investigate  $\mathbb{P}(\bar{\partial}_i(r) \neq \varnothing)$ , we estimate the expectation and variance of the progeny distribution in the branching

process  $\mathcal{X}_{n,\mathrm{res}}(i)$  using Assumptions 1.1, 1.3, and (1.6). Using  $\sum_i \theta_i^2 = \infty$ , we can choose  $i_2(\lambda)$  (depending only on  $\lambda$ ) such that

<span id="page-15-2"></span>
$$\frac{1}{\mu} \sum_{i=1}^{i_2(\lambda)} \theta_i^2 \ge 5\lambda. \tag{4.19}$$

<span id="page-15-1"></span>Also the normalizing constant in (4.17) satisfies

$$L = \ell_n (1 + o(n^{-\eta})) \tag{4.20}$$

uniformly over  $1 \leq i \leq K_n$ . To see this, first observe that  $\underline{\ell}_n = \ell_n - 2n^{\rho+\varepsilon} = o(n^{-\eta})$  since  $\varepsilon < 1 - \rho - \eta = \frac{4-\tau}{\tau-1}$ . Also,  $\frac{1}{\ell_n} \sum_{j \leq i} d_j = O(d_1 K_n n^{-1}) = o(n^{2\alpha-1}) = o(n^{-\eta})$ , as  $K_n = o(n^\alpha)$  by Assumption 1.3 and Lemma A.1 and  $2\alpha - 1 = -\eta$ . Hence, (4.20) follows. Now using Assumption 1.1 and (1.6), note that there exists  $N_\lambda \geq 1$  such that for all  $n \geq N_\lambda$  and  $i_2(\lambda) \leq i \leq K_n$ ,

$$\mathbb{E}\left[\bar{\xi}_{n}(i)\right] = \frac{1}{L} \sum_{j \geq i} d_{j}(d_{j} - 1) = \frac{1}{\ell_{n}} \sum_{j \geq i} d_{j}(d_{j} - 1) + o(n^{-\eta})$$

$$= 1 + \lambda n^{-\eta} - \frac{1}{\ell_{n}} \sum_{j < i} d_{j}(d_{j} - 1) + o(n^{-\eta})$$

$$\leq 1 + \lambda n^{-\eta} - \frac{1}{2\ell_{n}} \sum_{j < i} d_{j}^{2} + o(n^{-\eta})$$

$$\leq 1 - \left(Cn^{-2\alpha} \sum_{j < i} d_{j}^{2}\right) n^{-\eta} + o(n^{-\eta}),$$
(4.21)

<span id="page-15-6"></span>where the third step uses (1.6), the penultimate step uses the fact that  $d_i \geq 2$  so that  $\sum_{j < i} d_j \leq \sum_{j < i} d_j^2/2$  for  $i \leq K_n$ , and the last step uses (4.19). Thus, for  $n \geq N_\lambda$  and  $i_2(\lambda) \leq i \leq K_n$ ,

$$\mathbb{E}\left[\bar{\xi}_n(i)\right] \le 1 - \beta_i^n n^{-\eta} \quad \text{where} \quad \beta_i^n = C n^{-2\alpha} \sum_{j < i} d_j^2. \tag{4.22}$$

<span id="page-15-3"></span>The estimate in (4.22) will be crucial in the next section.

#### <span id="page-15-0"></span>4.3 Estimating heights of trees via random walks

We will prove the following theorem in this section:

<span id="page-15-4"></span>**Theorem 4.5.** Suppose that Assumptions 1.1, 1.3, and (1.6) hold. Fix  $\varepsilon > 0$ . Then, for all  $i_2(\lambda) \le i \le K_n$  (where  $i_2(\lambda)$  and  $K_n$  are given by (4.19) and Lemma A.1 respectively) and  $n \ge N_{\lambda}$ ,

$$\mathbb{P}(\bar{\partial}_i(\varepsilon n^{\eta}) \neq \varnothing) \le \frac{Cd_i}{n^{\alpha}} e^{-\frac{\varepsilon \beta_i^n}{2}},\tag{4.23}$$

for some constant  $C = C(\varepsilon, \lambda) > 0$ .

Define  $\mathcal{X}_n^1(i)$  to be the Galton-Watson tree starting with one offspring and progeny distribution  $\bar{\xi}_n(i)$  and let  $\bar{\partial}_i^1(r)$  denote the number of individuals in generation r of  $\mathcal{X}_n^1(i)$ . The crucial ingredient for the proof of Theorem 4.5 is the following:

<span id="page-15-5"></span>**Proposition 4.6.** Under identical conditions as in Theorem 4.5, for all  $n > N_{\lambda}$ ,

$$\mathbb{P}(\bar{\partial}_{i_2(\lambda)}^1(\varepsilon n^{\eta}) \neq \varnothing) \le \frac{C}{n^{\alpha}},\tag{4.24}$$

for some constant  $C = C(\varepsilon, \lambda) > 0$ .

Proof of Theorem 4.5 using Proposition 4.6. Let  $M_r$  denote the number of children at generation r of  $\mathcal{X}_{n,res}(i)$ , and note that

$$\mathbb{P}(\bar{\partial}_i(\varepsilon n^{\eta}) \neq \varnothing) \le \mathbb{E}[M_{\varepsilon n^{\eta}/2}] \times \mathbb{P}(\bar{\partial}_i^1(\varepsilon n^{\eta}/2) \neq \varnothing). \tag{4.25}$$

Now, using (4.22),

$$\mathbb{E}[M_{\varepsilon n^{\eta}/2}] \le d_i (1 - \beta_i^n n^{-\eta})^{\varepsilon n^{\eta}/2} \le d_i e^{-\frac{\varepsilon \beta_i^n}{2}}, \tag{4.26}$$

and  $\bar{\xi}_n(i) \leq \bar{\xi}_n(i-1) \leq \cdots \leq \bar{\xi}_n(i_2(\lambda))$ , where  $\leq$  denotes stochastic domination. Thus,

$$\mathbb{P}(\bar{\partial}_{i}(\varepsilon n^{\eta}) \neq \varnothing) \leq d_{i} e^{-\frac{\varepsilon \beta_{i}^{n}}{2}} \times \mathbb{P}(\bar{\partial}_{i_{2}(\lambda)}^{1}(\varepsilon n^{\eta}/2) \neq \varnothing), \tag{4.27}$$

and the proof of Theorem 4.5 follows using Proposition 4.6.

The rest of this section is devoted to the proof of Proposition 4.6. We leverage some key ideas from [1]. Define the breadth-first random walk  $s_n$  by  $s_n(0) = 1$  and

<span id="page-16-1"></span>
$$s_n(u) = s_n(u-1) + \zeta_u - 1, (4.28)$$

where  $(\zeta_u)_{u\geq 1}$  are i.i.d. observations from the distribution of  $\bar{\xi}_n(i_2(\lambda))$ . Let  $\sigma:=\inf\{u:s_n(u)=0\}$  and for  $t=0,1,\ldots,\sigma$ , define the function

$$H_n(t) := \sum_{u=0}^{t-1} \frac{1}{s_n(u)}.$$
 (4.29)

A remarkable fact observed in [1, Proposition 1.7] states that the height of a tree with breadth-first exploration process  $s_n$  is at most  $3H_n(\sigma)$ . Thus Proposition 4.6 can be concluded directly from the following estimate:

<span id="page-16-4"></span><span id="page-16-0"></span>**Proposition 4.7.** Under identical conditions as in Theorem 4.5, for all  $n \geq N_{\lambda}$ ,

$$\mathbb{P}(H_n(\sigma) > \varepsilon n^{\eta}) \le \frac{C}{n^{\alpha}},\tag{4.30}$$

for some constant  $C = C(\varepsilon, \lambda) > 0$ .

In what follows, we fix  $\delta>0$  such that  $\delta n^\alpha+2 < d_{i_2(\lambda)}/100$  for all  $n\geq N_\lambda$ . Define  $I_l:=[2^{l-1},2^{l+1})$  for  $l\geq 1$ . Let  $\mathbb{P}_x$  denote the law of the random walk  $s_n$ , starting from x and satisfying the recurrence relation in (4.28). Let  $\sigma_{nl}:=\min\{t\geq 1:s_n(t)\notin I_l\}$  and  $r_{nl}:=\min\{t\geq 1:\sup_{x\in I_l}\mathbb{P}_x(\sigma_{nl}>t)\leq 1/2\}$ . We first obtain the following bound on  $r_{nl}$ : Lemma 4.8. Under identical conditions as in Theorem 4.5, there exists  $n_\star\geq 1$  depending only on  $(d_i\,;\,i\in[n],n\geq 1)$  such that for all  $n\geq n_\star$  and all  $l\geq 1$  satisfying  $2^{l+1}\leq \delta n^\alpha$ , we have  $r_{nl}\leq C2^{(\tau-2)l}$  for some (sufficiently large) constant C>0.

<span id="page-16-3"></span>*Proof.* By (4.17),  $\mathbb{P}(\bar{\xi}_n(i_2(\lambda)) = j) = (1 + o(1))\mathbb{P}(D_n^* = j + 1)$  uniformly over  $1 \le j \le d_{i_2(\lambda)}$ . Thus, by Assumption 1.3,

$$\mathbb{P}\left(\frac{u}{c_1} < \bar{\xi}_n(i_2(\lambda)) \le u\right) \ge Cu^{-(\tau - 2)},\tag{4.31}$$

<span id="page-16-2"></span>for all  $c_1 \leq u \leq \delta n^{\alpha}$ .

Next, in order to estimate  $\sigma_{nl}$ , we bound  $\sup_{x \in I_l} \mathbb{P}_x(s_n(t) \in I_l)$  using an upper bound on Lévy's concentration function due to Esseen [18], that we describe now. For a random variable Z, define Lévy's concentration function

$$Q(Z,L) := \sup_{x \in \mathbb{R}} \mathbb{P}(Z \in [x, x+L)). \tag{4.32}$$

<span id="page-17-0"></span>By [18, Theorem 3.1], for any u > 0,

$$Q(s_n(t), u) \le \frac{Cu}{\left(t \times \mathbb{E}[|\zeta_1 - \zeta_2|^2 \mathbb{1}\{|\zeta_1 - \zeta_2| \le u\}]\right)^{1/2}},$$
(4.33)

where  $\zeta_1$  and  $\zeta_2$  are i.i.d. realizations from the distribution of  $\bar{\xi}_n(i_2(\lambda))$ . To get an upper bound on the right side of (4.33), we first observe that for any random variable Y supported on  $\mathbb{Z}_{>0}$ ,

$$\mathbb{E}[Y^{2}\mathbb{1}\{Y \le u\}] = \sum_{1 \le y \le u} y^{2}\mathbb{P}(Y = y) = \sum_{1 \le y \le u} \sum_{1 \le x \le y} y\mathbb{P}(Y = y)$$

$$= \sum_{1 \le x \le u} \sum_{x < y \le u} y\mathbb{P}(Y = y) \ge \sum_{1 \le x \le u} x\mathbb{P}(x \le Y \le u).$$
(4.34)

Now, it follows from (4.17) and Assumption 1.1 (iii) that  $\liminf_{n\to\infty} \mathbb{P}(\bar{\xi}_n(i_2(\lambda))=0)>0$ . Similarly, using (4.17) and Assumption 1.1 (ii), we can choose an integer  $j_\star>c_1$  such that  $\liminf_{n\to\infty} \mathbb{P}(\bar{\xi}_n(i_2(\lambda))-1=j_\star)>0$ . Let  $n_\star$  be such that

$$\inf_{n > n_{\star}} \mathbb{P}\left(\bar{\xi}_n(i_2(\lambda)) = 0\right) > 0 \text{ and } \inf_{n > n_{\star}} \mathbb{P}\left(\bar{\xi}_n(i_2(\lambda)) - 1 = j_{\star}\right) > 0. \tag{4.35}$$

Then for any  $n \geq n_{\star}$  and  $c_1 \leq u \leq \delta n^{\alpha}$ ,

<span id="page-17-1"></span>
$$\mathbb{E}[|\zeta_{1} - \zeta_{2}|^{2} \mathbb{1} \{|\zeta_{1} - \zeta_{2}| \leq u\}] \geq \sum_{1 \leq x \leq u} x \mathbb{P}(x \leq |\zeta_{1} - \zeta_{2}| \leq u)$$

$$\geq \sum_{1 \leq x \leq u/c_{1}} x \mathbb{P}(x \leq \zeta_{1} \leq u) \mathbb{P}(\zeta_{2} = 0) \geq Cu^{4-\tau},$$
(4.36)

where the penultimate step uses the fact that if  $x \le \zeta_1 \le u$  and  $\zeta_2 = 0$ , then  $x \le |\zeta_1 - \zeta_2| \le u$ , and the final step follows using (4.31) and the first inequality in (4.35). Thus, (4.33) yields, for  $n > n_*$  and any l > 1 satisfying  $c_1 < 2^{l+1} < \delta n^{\alpha}$ ,

$$\sup_{x \in I_l} \mathbb{P}_x(\sigma_{nl} > t) \le \sup_{x \in I_l} \mathbb{P}_x(s_n(t) \in I_l) \le Q(s_n(t), 2^{l+1}) \le \frac{C2^l}{(t2^{l(4-\tau)})^{1/2}},\tag{4.37}$$

which is at most 1/2 by choosing  $t = C2^{l(\tau-2)}$  for some large constant C > 0. Finally, for all  $n \ge n_\star$  and  $l \ge 1$  satisfying  $2^{l+1} < c_1$ ,

$$\sup_{x \in I_l} \mathbb{P}_x(\sigma_{nl} > t) \le \mathbb{P}(\bar{\xi}_n(i_2(\lambda)) - 1 \ne j_\star)^t \le \exp(-Ct),$$

where the last step uses the second inequality in (4.35). This in particular implies that  $r_{nl} \leq C$  for all  $n \geq n_{\star}$  and  $l \geq 1$  satisfying  $2^{l+1} < c_1$ . This completes the proof.

We now decompose the possible values of the random walk (4.28) starting from  $s_n(0)=1$  into different scales. Recall that  $I_l:=[2^{l-1},2^{l+1})$ . At each time t, the scale of  $s_n(t)$ , denoted by  $\mathrm{scl}(s_n(t))$ , is an integer. Let  $\mathrm{scl}(s_n(0))=1$ . Suppose that  $\mathrm{scl}(s_n(u))=l$  for some u>0. A change of scale occurs when  $s_n$  leaves  $I_l$ , i.e., at time  $T:=\inf\{t>u:s_n(t)\notin I_l\}$ , and the new scale is given by  $\mathrm{scl}(s_n(T))=l'$ , where l' is such that  $s_n(T)\in[2^{l'-1},2^{l'})$ . Now, the next change of scale occurs at time  $T':=\inf\{t>T:s_n(t)\notin I_{l'}\}$ , and the scale remains the same until T', i.e.,  $\mathrm{scl}(s_n(t))=l'$  for all  $T\leq t< T'$ . Define

$$H_{nl}(t) := \sum_{u \in [0,t), \ \text{scl}(s_n(u)) = l} \frac{1}{s_n(u)}, \quad \text{so that} \quad H_n(t) = \sum_{l \ge 1} H_{nl}(t). \tag{4.38}$$

Global lower mass-bound for heavy-tailed critical configuration models

Let  $T_{nl}(t) := \#\{u \in [0, t) : scl(s_n(u)) = l\}$ , and note that

$$2^{l-1}H_{nl}(t) \le T_{nl}(t) \le 2^{l+1}H_{nl}(t). \tag{4.39}$$

Therefore, for any x > 0,

<span id="page-18-5"></span>
$$\mathbb{P}\left(H_{nl}(\sigma) \ge \frac{xr_{nl}}{2^{l-1}}\right) \le \mathbb{P}(T_{nl}(\sigma) \ge xr_{nl}). \tag{4.40}$$

The next lemma estimates  $\mathbb{P}(T_{nl}(\sigma) \geq xr_{nl})$ :

<span id="page-18-3"></span>**Lemma 4.9.** For all  $n \ge 1$ ,  $l \ge 1$ , and x > 0,

$$\mathbb{P}(T_{nl}(\sigma) \ge xr_{nl}) \le C2^{-l-C'x},\tag{4.41}$$

for some absolute constants C, C' > 0.

<span id="page-18-0"></span>*Proof.* Let us first show that for any  $l \geq 2$ ,

$$\mathbb{P}(T_{nl}(\sigma) \neq 0) < 2^{-(l-1)}. (4.42)$$

For any  $t\geq 0$ , let  $\mathcal{F}_t$  denote the sigma-field generated by  $(\zeta_u)_{u=0}^t$ , where we take  $\zeta_0=1$ . Note that if  $T_{nl}(\sigma)\neq 0$ , then  $s_n(u)$  hits  $2^{l-1}$  before hitting zero. For H>1, let  $\gamma_H:=\min\{t:s_n(t)\geq H, \text{ or } s_n(t)=0\}$ . Since  $\mathbb{E}[\zeta_u-1]<0$  by (4.22),  $(s_n(t))_{t\geq 0}$  is a supermartingale with respect to the filtration  $(\mathcal{F}_t)_{t\geq 0}$ . Consequently, an application of the optional stopping theorem yields

$$H\mathbb{P}(s_n(\gamma_H) \ge H) \le \mathbb{E}[s_n(\gamma_H)] \le \mathbb{E}[s_n(0)] = 1, \tag{4.43}$$

<span id="page-18-4"></span>and therefore,

$$\mathbb{P}(s_n(\gamma_H) \ge H) \le \frac{1}{H}.\tag{4.44}$$

Thus, (4.42) follows by taking  $H=2^{l-1}$  together with the fact that  $T_{nl}(\sigma)\neq 0$  implies that  $s_n(\gamma_H)\geq H$ .

Next, we define  $U_n(t,[a,b))$ -the number of upcrossings of an interval [a,b) by  $s_n$  up to time t-to be the supremum of all integers k such that there exist times  $(u_j,t_j)_{j=1}^k$  satisfying  $0 \le u_1 < t_1 < u_2 < \dots < t_k \le t$ , and  $s_n(u_j) < a < b \le s_n(t_j)$  for all  $j \in [k]$ . We will use the following simple fact (see [1, Proposition 3.2]): for any positive integers k, z, a, b with 0 < z < a < b,

$$\mathbb{P}_z(U_n(\sigma, [a, b)) \ge k) \le \left(\frac{a-1}{b}\right)^k. \tag{4.45}$$

<span id="page-18-1"></span>Next define  $\operatorname{visit}(l,t)$  to be the number of visits to scale l upto time t, i.e., this is the supremum over  $k \in \mathbb{N}$  such that one can find  $(u_j,t_j)_{j=1}^k$  with  $u_1 < t_1 < \cdots < u_k < t_k \le t$  satisfying  $\operatorname{scl}(s_n(u_j)) \ne l$  but  $\operatorname{scl}(s_n(t_j)) = l$ . For the random walk  $s_n$  started at  $s_n(0) = 1$ , we set  $\operatorname{visit}(1,0) = 1$  and  $\operatorname{visit}(l,t) = 0$  if  $s_n$  does not enter scale l before time t. Further, define  $M_{nl} = \operatorname{visit}(l,\sigma)$  (the total number of visits to scale l) and  $t_{jl} = \#\{t < \sigma : \operatorname{scl}(s_n(t)) = l, \operatorname{visit}(l,t) = j\}$  (the time spent at scale l during the j-th visit). Note that, if  $T_{nl}(\sigma) \ne 0$  occurs, then  $M_{nl} \ge 1$ , and  $T_{nl}(\sigma) = \sum_{j=1}^{M_{nl}} t_{jl}$ . Thus, for any  $m \ge 2$  and  $x \in \mathbb{Z}_{\ge 2}$ ,

<span id="page-18-2"></span>
$$\mathbb{P}(T_{nl}(\sigma) > 5xr_{nl}) = \mathbb{P}(\sum_{j=1}^{M_{nl}} t_{jl} > 5xr_{nl}) \le \mathbb{P}(M_{nl} > m) + \mathbb{P}(\sum_{j=1}^{m} t_{jl} > 5xr_{nl}).$$
(4.46)

Now,  $M_{nl}>m$  implies that  $T_{nl}(\sigma)\neq 0$ , and after the first visit to scale l, the walk comes back to scale l at least m times before hitting zero. In any of the subsequent visits, if  $s_n$  enters scale l from below (this can only happen for  $l\geq 3$ ), then that would imply an upcrossing of the interval  $[2^{l-2},2^{l-1})$  has taken place. Otherwise, if  $s_n$  enters scale l from above in any of the subsequent visits, then it must be the case that while leaving the scale l during the previous visit, the walk went from scale l to a higher scale. This yields an upcrossing of  $[2^l,2^{l+1})$ . Therefore, for any  $l\geq 3$ ,  $M_{nl}>m$  implies that  $T_{nl}(\sigma)\neq 0$ , and after the first visit to scale l and before hitting zero, either at least m/2 many upcrossings of  $[2^{l-2},2^{l-1})$  have taken place, or at least m/2 many upcrossings of  $[2^l,2^{l+1})$  have taken place. Thus, using (4.42), (4.45), and the strong Markov property, for any  $l\geq 3$ ,

$$\mathbb{P}(M_{nl} > m) \le \frac{C}{2^{l+m/2}}.\tag{4.47}$$

<span id="page-19-0"></span>Next, by the definition of  $r_{nl}$  given right above Lemma 4.8,  $\mathbb{P}_z(t_{jl} > kr_{nl}) \leq 2^{-k}$  for any z > 0, which implies that  $\lfloor t_{jl}/r_{nl} \rfloor$  can be stochastically dominated by a Geometric(1/2) random variable. Using the strong Markov property, it follows that for any z > 0, under  $\mathbb{P}_z$ ,  $\sum_{j=1}^m \lfloor t_{jl}/r_{nl} \rfloor$  is stochastically dominated by  $\sum_{i=1}^m g_i$ , where  $(g_i)_{i \geq 1}$  is an i.i.d. collection of Geometric(1/2) random variables. Thus, for any z > 0,

$$\mathbb{P}_z\left(\sum_{j=1}^m t_{jl} \ge (k+m)r_{nl}\right) \le \mathbb{P}_z\left(\sum_{j=1}^m \left\lfloor \frac{t_{jl}}{r_{nl}} \right\rfloor > k\right) \le \mathbb{P}\left(\sum_{i=1}^m g_i > k\right)$$
$$= \mathbb{P}(\operatorname{Bin}(k, 1/2) < m) \le e^{-(k-2m)^2/2k},$$

for  $2m \leq k$ , where the last step follows using standard concentration inequalities such as [27, Theorem 2.1]. Consequently, using (4.42) and the strong Markov property,  $\mathbb{P}\left(\sum_{j=1}^m t_{jl} \geq (k+m)r_{nl}\right) \leq 2^{-(l-1)} \cdot \mathrm{e}^{-(k-2m)^2/2k}$  for  $2m \leq k$ . Combining this with (4.46) and (4.47), and taking k=4x and m=x yields

$$\mathbb{P}(T_{nl}(\sigma) > 5xr_{nl}) \le C2^{-l-C'x} \tag{4.48}$$

for any  $l \geq 3$ . The proofs for l = 1 and l = 2 follow similar steps. This completes the proof of Lemma 4.9.

We are now ready to prove Proposition 4.7.

Proof of Proposition 4.7. Recall the definition of  $s_n$  from (4.28) starting from one, so that  $s_n(0) = 1$ . Fix  $\delta > 0$ . We first estimate the probability of the event  $\mathcal{B}_n$  that  $s_n$  hits  $\delta n^{\alpha}/2$  before hitting zero. Let  $\gamma := \min\{t : s_n(t) \geq \delta n^{\alpha}/2, \text{ or } s_n(t) = 0\}$ . By (4.44),

$$\mathbb{P}(\mathcal{B}_n) = \mathbb{P}\left(s_n(\gamma) \ge \frac{\delta n^{\alpha}}{2}\right) \le \frac{2}{\delta n^{\alpha}}.$$
(4.49)

Let  $m:=\max\{l\geq 1: 2^{l+1}\leq \delta n^{\alpha}\}$ . On  $\mathcal{B}_n^c$ ,  $H_{nl}(\sigma)=0$  for l>m. Thus, for any sequence of positive numbers  $(b_l)_{l>1}$ ,

<span id="page-19-1"></span>
$$\mathbb{P}\left(H_n(\sigma) \ge \sum_{l=1}^m \frac{b_l r_{nl}}{2^{l-1}}\right) \le \frac{2}{\delta n^{\alpha}} + \mathbb{P}\left(H_n(\sigma) \ge \sum_{l=1}^m \frac{b_l r_{nl}}{2^{l-1}}, \text{ and } \mathcal{B}_n^c \text{ occurs}\right) \\
\le \frac{2}{\delta n^{\alpha}} + \mathbb{P}\left(H_{nl}(\sigma) \ge \frac{b_l r_{nl}}{2^{l-1}} \text{ for some } 1 \le l \le m\right).$$
(4.50)

Using (4.40) and Lemma 4.9, (4.50) yields

<span id="page-19-2"></span>
$$\mathbb{P}\left(H_n(\sigma) \ge \sum_{l=1}^m \frac{b_l r_{nl}}{2^l}\right) \le \frac{2}{\delta n^{\alpha}} + \sum_{l=1}^m \mathbb{P}(T_{nl}(\sigma) \ge b_l r_{nl}) \le \frac{2}{\delta n^{\alpha}} + C \sum_{l=1}^m 2^{-l - C' b_l}.$$
 (4.51)

Letting  $b_l = \frac{1}{C'}(m-l+1+2\log_2(m-l+1))$  for  $1 \le l \le m$ , and using Lemma 4.8,

<span id="page-20-0"></span>
$$\sum_{l=1}^{m} \frac{b_{l} r_{nl}}{2^{l-1}} \leq C \sum_{l=1}^{m} \left( m - l + 1 + 2 \log_{2}(m - l + 1) \right) 2^{l(\tau - 3)}$$

$$= C \sum_{j=1}^{m} \frac{(j + 2 \log_{2} j) 2^{(m+1)(\tau - 3)}}{2^{j(\tau - 3)}} \leq C (\delta n^{\alpha})^{\tau - 3} \sum_{j=1}^{m} \frac{(j + 2 \log_{2} j)}{2^{j(\tau - 3)}}$$

$$\leq C n^{\eta} \delta^{\tau - 3}, \tag{4.52}$$

where we have used  $\sum_{j=1}^{\infty} \frac{(j+2\log_2 j)}{2^{j(\tau-3)}} < \infty$  in the last step; the bound in (4.52) holds for all  $n \ge n_{\star}$ , where  $n_{\star}$  is as in Lemma 4.8. Also,

$$\sum_{l=1}^{m} 2^{-l-C'b_l} = \sum_{l=1}^{m} 2^{-(m+1)} (m-l+1)^{-2} \le \frac{4}{\delta n^{\alpha}} \sum_{l=1}^{\infty} \frac{1}{l^2}.$$
 (4.53)

<span id="page-20-1"></span>Thus, the claim in Proposition 4.7 follows for  $n \ge n_{\star}$  by combining (4.52) and (4.53) with (4.51). We conclude that the claimed bound holds for  $n \ge N_{\lambda}$  by choosing a larger constant C on the right side of (4.30).

#### 4.4 Proof of Proposition 2.2

Let us now complete the proof of Proposition 2.2 using Proposition 4.4 and Theorem 4.5. We take  $K_n$  as in Lemma A.1 so that the results in Section 4.3 hold. Note that these bounds work for  $i_2(\lambda) \leq i \leq K_n$ , and we will use path counting arguments from [7,25] to bound the diameter for  $i > K_n$ . Define  $\mathscr{C}_{\mathrm{res}}(i)$  to be the connected component containing vertex i in the graph  $\mathcal{G}_n^{>i-1} = \mathrm{CM}_n(d) \setminus [i-1]$ . Note that if  $\Delta^{>K} > \varepsilon n^\eta$ , then there exists a path of length  $\varepsilon n^\eta$  in  $\mathrm{CM}_n(d)$  avoiding all the vertices in [K]. Suppose that the minimum index among vertices on that path is  $i_0$ . Then  $\mathrm{diam}(\mathscr{C}_{\mathrm{res}}(i_0)) > \varepsilon n^\eta$ . Therefore,  $\Delta^{>K} > \varepsilon n^\eta$  implies that either there exists  $i \in (K, K_n)$  satisfying  $\mathrm{diam}(\mathscr{C}_{\mathrm{res}}(i)) > \varepsilon n^\eta$ , or  $\mathrm{diam}(\mathrm{CM}_n(d) \setminus [K_n]) > \varepsilon n^\eta$ . We will use the following lemma first to complete the proof of Proposition 2.2 and prove the lemma subsequently:

<span id="page-20-2"></span>**Lemma 4.10.** Under Assumptions 1.1 and 1.3, for any  $\varepsilon > 0$ ,  $\lim_{n \to \infty} \mathbb{P}(\operatorname{diam}(\mathrm{CM}_n(d) \setminus [K_n]) > \varepsilon n^\eta) = 0$ , where  $K_n$  as in Lemma A.1.

Proof of Proposition 2.2. As defined earlier around (4.17),  $\partial_i(r)$  denotes the number of vertices at distance r from the vertex i in the graph  $\mathcal{G}_n^{>i-1}$ . Recall the definition of  $\bar{\partial}$  in Proposition 4.4. Thus, Proposition 4.4 and Theorem 4.5 together with Lemma 4.10, yield that

$$\mathbb{P}\left(\Delta^{>K} > \varepsilon n^{\eta}\right) \leq \sum_{i \in (K,K_n)} \mathbb{P}(\bar{\partial}_i(\varepsilon n^{\eta}/2) \neq \varnothing) + \mathbb{P}(\operatorname{diam}(\operatorname{CM}_n(\boldsymbol{d}) \setminus [K_n]) > \varepsilon n^{\eta}) 
\leq C \sum_{i \in (K,K_n)} \left(\frac{d_i}{n^{\alpha}}\right) e^{-\varepsilon \beta_i^n/4} + o(1),$$
(4.54)

where the last line tends to zero if we first take  $n\to\infty$  and then take  $K\to\infty$  using Assumption 1.3 and Lemma A.1 below. Thus the proof of Proposition 2.2 follows.  $\Box$ 

Proof of Lemma 4.10. Let  $d' := (d'_i; i \in [n] \setminus [K_n])$ , where  $d'_i$  denotes the degree of i in  $\mathrm{CM}_n(d) \setminus [K_n]$ . Note that  $\mathrm{CM}_n(d) \setminus [K_n]$  is again distributed as a configuration model conditionally on its degree sequence d', with the criticality parameter

$$\nu_n' = \frac{\sum_{i>K_n} d_i'(d_i'-1)}{\sum_{i>K_n} d_i'} \le \frac{\sum_{i>K_n} d_i(d_i-1)}{\ell_n - 2\sum_{i=1}^{K_n} d_i} \le 1 - R_n n^{-\eta}, \quad R_n = \omega(\log n), \tag{4.55}$$

where the penultimate step follows using  $d_i' \leq d_i$  and  $\ell_n' := \sum_{i>K_n} d_i' = \ell_n - 2\sum_{i=1}^{K_n} d_i$ , and the last bound follows from the definition of  $K_n$  given in Lemma A.1 (ii) and an argument identical to that in (4.21). Let  $\mathbb{P}'(\cdot)$  denote the probability measure conditionally on d'. We will use path-counting techniques for subcritical configuration models. An argument similar to the one given in [25, Lemma 6.1] shows that for any  $l \geq 1$ , conditional on d', the expected number of paths of length l starting from vertex l is at most

$$\frac{\ell'_n d'_i(\nu'_n)^{l-1}}{\ell'_n - 2l + 3} \le {\ell'_n}^2 (\nu'_n)^{l-1}.$$

Thus, for any  $i > K_n$ ,

<span id="page-21-1"></span>
$$\mathbb{P}'(\exists \text{ path of length at least } \varepsilon n^{\eta} \text{ from } i \text{ in } \mathrm{CM}_n(\mathbf{d}) \setminus [K_n]) \leq C\ell_n'^2 \sum_{l>\varepsilon n^{\eta}} (\nu_n')^l, \qquad \textbf{(4.56)}$$

Thus, for  $i > K_n$ , the probability in (4.56) is at most

$$Cn^{2}(1 - R_{n}n^{-\eta})^{\varepsilon n^{\eta}}/(R_{n}n^{-\eta}) \le Cn^{2+\eta}e^{-\varepsilon R_{n}} = o(1/n),$$
 (4.57)

since  $R_n \gg \log n$ . Therefore,

$$\mathbb{P}'(\exists i > K_n : \exists \text{ path of length at least } \varepsilon n^{\eta} \text{ from } i \text{ in } \mathrm{CM}_n(d) \setminus [K_n]) = o(1),$$
 (4.58)

and the proof of Lemma 4.10 follows.

# <span id="page-21-0"></span>5 Verification of the assumptions for percolated degrees: Proof of Theorem 1.7

Let  $\mathcal{G}_n$  denote the graph obtained by performing percolation with edge retention probability  $p_c(\lambda)$  (defined in (1.12)) on  $\mathrm{CM}_n(d)$ . Let  $d^p = (d_i^p)_{i \in [n]}$  denote the degree sequence of  $\mathcal{G}_n$ . By [19, Lemma 3.2], the law of  $\mathcal{G}_n$ , conditionally on  $d^p$ , is the same as the law of  $\mathrm{CM}_n(d^p)$ . Thus, it is enough to show that if the original degree sequence  $(d_n\,,\,n\geq 1)$  satisfies Assumptions 1.1(i), 1.1(ii) and 1.3, then we can construct  $(d^p\,,\,n\geq 1)$  on the same probability space so that Assumption 1.1, (1.6), and Assumption 1.3 are satisfied almost surely (with possibly different parameters), since then the claim in Theorem 1.7 will follow from Theorem 1.5.

First, note that  $\mathbb{E}[d_i^p] = d_i p_c(\lambda)(1+o(1))$ . Also, given  $\mathrm{CM}_n(d)$ , changing the status of an edge (deleted or retained) can change  $d_i^p$  by at most 2 when the edge is incident to i. There are at most  $d_i$  choices for such an edge. Thus, the bounded difference inequality [27, Corollary 2.27] implies, for each fixed  $i \geq 1$ , and for any  $\varepsilon > 0$ ,

$$\mathbb{P}(|d_i^p - d_i p_c(\lambda)| > \varepsilon d_i p_c(\lambda)) \le 2e^{-\frac{\varepsilon^2}{4} d_i p_c^2(\lambda)}. \tag{5.1}$$

In particular, for each  $i\geq 1$ ,  $n^{-\alpha}d_i^p\stackrel{d}{\longrightarrow}\theta_i/\nu$  as  $n\to\infty$ , which verifies Assumption 1.1 (i). Next, let  $M_r^p=\sum_{i\in[n]}(d_i^p)_r$  and  $M_r=\sum_{i\in[n]}(d_i)_r$ , where  $(x)_r:=x(x-1)\cdots(x-r+1)$ . To verify the moment conditions in Assumption 1.1 (ii), note that (1.5) holds for  $d^p$  since  $\sum_{i>K}(d_i^p)_3\leq\sum_{i>K}(d_i)_3$ . We will show that

$$M_1^p = (1 + O_{\mathbb{P}}(n^{-1/2}))p_c(\lambda)M_1 \quad \text{and} \quad M_2^p = (1 + O_{\mathbb{P}}(n^{\frac{3\alpha}{2}-1}))p_c(\lambda)^2M_2. \tag{5.2}$$

<span id="page-21-2"></span>Using (5.2), the first and second moment assumptions in Assumption 1.1 (ii) holds for the percolated degree sequence. The estimate (5.2) also shows that (1.6) holds. Indeed,

$$\frac{M_2^p}{M_1^p} = \frac{p_c(\lambda)M_2}{M_1}(1 + O_{\mathbb{P}}(n^{\frac{3\alpha}{2}-1})) = 1 + \nu\lambda n^{-\eta} + o(n^{-\eta}),\tag{5.3}$$

<span id="page-21-3"></span>

where the last step follows using (1.11), (1.12), and the fact that  $-1 + 3\alpha/2 < -1 + 2\alpha = -n$ .

It remains to prove (5.2). Since  $\frac{1}{2}\sum_{i\in[n]}d_i^p$  has a binomial distribution with parameter  $\ell_n/2$  and  $p_c(\lambda)$ , the first asymptotics follows from Chebyshev's inequality. For the asymptotics of  $M_2^p$ , we use the following construction of  $\mathcal{G}_n$  from [19].

<span id="page-22-2"></span>**Algorithm 2.**  $d^p = (d_i^p)_{i \in [n]}$  can be generated as follows:

- (S0) Sample  $R_n \sim \text{Bin}(\ell_n/2, p_c(\lambda))$ .
- (S1) Conditionally on  $R_n$ , sample a uniform subset of  $2R_n$  half-edges from the set of  $\ell_n$  half-edges. Let  $I_j^{(i)}$  denote the indicator that j-th half-edge of i is selected. Then  $d_i^p = \sum_{j=1}^{d_i} I_j^{(i)}$  for all  $i \in [n]$ .

Using the above construction, note that

$$M_2^p = \sum_{i \in [n]} \sum_{1 \le j_1 \ne j_2 \le d_i} I_{j_1}^{(i)} I_{j_2}^{(i)}.$$
(5.4)

Let  $\mathbb{P}_1(\cdot) = \mathbb{P}(\cdot|R_n)$  and similarly define  $\mathbb{E}_1[\cdot]$ ,  $\mathrm{Var}_1(\cdot)$ , and  $\mathrm{Cov}_1(\cdot,\cdot)$ . Then,

<span id="page-22-0"></span>
$$\mathbb{E}_{1}[M_{2}^{p}] = \sum_{i \in [n]} \sum_{1 \le j_{1} \ne j_{2} \le d_{i}} \mathbb{P}_{1}(I_{j_{1}}^{(i)} = 1, I_{j_{2}}^{(i)} = 1) = \sum_{i \in [n]} \sum_{1 \le j_{1} \ne j_{2} \le d_{i}} \frac{\binom{\ell_{n} - 2}{2R_{n} - 2}}{\binom{\ell_{n}}{2R_{n}}}$$

$$= \sum_{i \in [n]} \sum_{1 \le j_{1} \ne j_{2} \le d_{i}} \frac{2R_{n}(2R_{n} - 1)}{\ell_{n}(\ell_{n} - 1)} = (1 + O_{\mathbb{P}}(n^{-1/2}))p_{c}(\lambda)^{2}M_{2}, \tag{5.5}$$

where the last step follows using  $R_n = (1 + O_{\mathbb{P}}(n^{-1/2}))p_c(\lambda)\ell_n/2$ .

Next, recall that a collection of random variables  $(X_1, \ldots, X_t)$  is called negatively associated if for every index set  $I \subset [k]$ ,

$$Cov(f(X_i, i \in I), g(X_i, i \in I^c)) \le 0,$$
(5.6)

<span id="page-22-3"></span>for all functions  $f: \mathbb{R}^{|I|} \mapsto \mathbb{R}$  and  $g: \mathbb{R}^{t-|I|} \mapsto \mathbb{R}$  that are component-wise non-decreasing ([17, Definition 3]). Then, conditionally on  $R_n$ ,  $I_j^{(i)}$ ,  $j=1,\ldots,d_i$ ,  $i\in [n]$  are negatively associated (cf. [17, Theorem 10]), which yields the almost sure bound

$$\operatorname{Var}_{1}(M_{2}^{p}) \leq \sum_{i \in [n]} \sum_{1 \leq j_{1} \neq j_{2} \leq d_{i}} \operatorname{Var}_{1}(I_{j_{1}}^{(i)}I_{j_{2}}^{(i)}) + \sum_{i \in [n]} \sum_{\substack{1 \leq j_{1} \neq j_{2} \leq d_{i} \\ 1 \leq j_{3} \neq j_{4} \leq d_{i} \\ |\{j_{1}, j_{2}\} \cap \{j_{3}, j_{4}\}| = 1}} \operatorname{Cov}_{1}(I_{j_{1}}^{(i)}I_{j_{2}}^{(i)}, I_{j_{3}}^{(i)}I_{j_{4}}^{(i)}),$$

$$(5.7)$$

since the contribution of  $|\{j_1,j_2\}\cap\{j_3,j_4\}|=0$  can be ignored due to negative association. Also,  $\mathrm{Var}_1(I_{j_1}^{(i)}I_{j_2}^{(i)})\leq 1$  and  $|\mathrm{Cov}_1(I_{j_1}^{(i)}I_{j_2}^{(i)},I_{j_3}^{(i)}I_{j_4}^{(i)})|\leq (\mathrm{Var}_1(I_{j_1}^{(i)}I_{j_2}^{(i)})\mathrm{Var}_1(I_{j_3}^{(i)}I_{j_4}^{(i)}))^{1/2}\leq 1$ . Therefore,

$$\operatorname{Var}_{1}(M_{2}^{p}) \leq \sum_{i \in [n]} d_{i}^{2} + 4 \sum_{i \in [n]} d_{i}^{3} = O(n^{3\alpha}).$$
 (5.8)

Thus, for any A > 0,

<span id="page-22-1"></span>
$$\mathbb{P}(|M_2^p - \mathbb{E}_1[M_2^p]| > An^{3\alpha/2}) = \mathbb{E}[\mathbb{P}_1(|M_2^p - \mathbb{E}_1[M_2^p]| > An^{3\alpha/2})] \le \frac{\mathbb{E}[\operatorname{Var}_1(M_2^p)]}{A^2n^{3\alpha}}, (5.9)$$

which can be made arbitrarily small by choosing A>0 large. Thus, we conclude the asymptotics of  $M_2^p$  in (5.2) by using (5.5) and (5.9).

Finally, we need to show convergence in distribution of empirical measure of  $d^p$  to finish verifying Assumptions 1.1 (ii) and (iii). Let  $n_k^p = \#\{i: d_i^p = k\}$ , and  $n_{\geq k}^p = \sum_{r \geq k} n_r^p$ . It suffices to show that

$$\frac{n_{\geq k}^p}{n} \xrightarrow{d} \mathbb{P}(D^p \geq k) \quad \text{for all } k \geq 1, \tag{5.10}$$

<span id="page-23-1"></span>where  $D^p$  satisfies  $(D^p \mid D = l) \sim \text{Bin}(l, 1/\nu)$ , for all  $l \geq 1$ . Let  $V_n$  be a uniformly chosen vertex and  $D_n^p = d_{V_n}^p$  and  $D_n = d_{V_n}$ . By the construction in Algorithm 2,

$$\mathbb{P}(D_n^p = k \mid D_n = l, R_n) = \frac{\binom{l}{k} \binom{\ell_n - l}{2R_n - k}}{\binom{\ell_n}{2R_n}} = (1 + o(1)) \binom{l}{k} \left(\frac{2R_n}{\ell_n}\right)^k \left(1 - \frac{2R_n}{\ell_n}\right)^{l - k} \\
= (1 + o_{\mathbb{P}}(1)) \binom{l}{k} \left(\frac{1}{\nu}\right)^k \left(1 - \frac{1}{\nu}\right)^{l - k}, \tag{5.11}$$

where in the final step we have used that  $R_n = p_c(\lambda)\ell_n/2(1+o_{\mathbb{P}}(1))$  and  $p_c(\lambda) = \nu^{-1}(1+o(1))$ . Thus,

$$\mathbb{E}\left[\frac{n_k^p}{n} \mid R_n\right] = \mathbb{P}(D_n^p = k \mid R_n) \xrightarrow{d} \mathbb{P}(D^p = k). \tag{5.12}$$

<span id="page-23-0"></span>Moreover, note that  $d_i^p = \sum_{j=1}^{d_i} I_j^{(i)}$ , and the definition of negative association in (5.6) allows us to conclude negative correlation between increasing functions of  $I_j^{(i)}$  that depend on disjoint sets of indices. Therefore,

$$\operatorname{Var}\left(n_{\geq k}^{p} \mid R_{n}\right) = \operatorname{Var}\left(\sum_{i: d_{i} \geq k} \mathbb{1}_{\left\{d_{i}^{p} \geq k\right\}} \mid R_{n}\right) \leq \sum_{i: d_{i} \geq k} \operatorname{Var}\left(\mathbb{1}_{\left\{d_{i}^{p} \geq k\right\}} \mid R_{n}\right) \leq n, \tag{5.13}$$

and thus  $\mathbb{E}[\operatorname{Var}(n_{>k}^p/n\mid R_n)]=O(1/n)$ . This together with (5.12) yields (5.10).

We finally verify that Assumption 1.3 holds with high probability. Let the constants  $c_1$  and  $c_0$  be as in Assumption 1.3. Let  $c_1' := 9c_1\nu$ . It is enough to show that there exists a deterministic constant  $c_0' > 0$  such that

<span id="page-23-4"></span>
$$\mathbb{P}\Big(\frac{1}{n}\sum_{i\in[n]}d_i^p\mathbb{1}\{l < d_i^p \le c_1'l\} \ge \frac{c_0'}{l^{\tau-2}} \quad \text{for all} \quad 1 \le l \le d_1/c_1'\Big) \to 1 \quad \text{as} \quad n \to \infty. \tag{5.14}$$

<span id="page-23-2"></span>Write  $\sum_*$  for  $\sum_{i:8l < d_i p_c(\lambda) \le 8c_1 l}$ . Then, for  $1 \le l \le d_1/c_1'$  and all large n,

$$\frac{1}{n} \sum_{i \in [n]} \mathbb{E} \left[ d_i^p \mathbb{1} \{ l < d_i^p \le c_1' l \} \right] \ge \frac{1}{n} \sum_{*} \mathbb{E} \left[ d_i^p \mathbb{1} \{ l < d_i^p \le c_1' l \} \right] 
= \frac{1}{n} \sum_{*} \mathbb{E} \left[ d_i^p \mathbb{1} \{ l < d_i^p \} \right],$$
(5.15)

where the last step uses the fact that when  $d_i p_c(\lambda) \leq 8c_1 l$ , we have  $d_i^p \leq d_i \leq 8c_1 l/p_c(\lambda) \leq c_1' l$  for all large n. Let  $X_i \sim \text{Bin}(\lfloor d_i/2 \rfloor, p_c(\lambda))$ . Then  $d_i^p$  is stochastically larger than  $X_i$ . Using (5.15), we see that for  $1 \leq l \leq d_1/c_1'$  and all large n,

<span id="page-23-3"></span>
$$\frac{1}{n} \sum_{i \in [n]} \mathbb{E} \left[ d_i^p \mathbb{1} \left\{ l < d_i^p \le c_1' l \right\} \right] \ge \frac{1}{n} \sum_* \mathbb{E} \left[ X_i \cdot \mathbb{1} \left\{ l < X_i \right\} \right] 
\ge \frac{1}{n} \sum_* \mathbb{E} \left[ X_i \right] \mathbb{P} \left( X_i > l \right) \ge \frac{1}{n} \sum_* \mathbb{E} \left[ X_i \right] \mathbb{P} \left( X_i \ge \lfloor \lfloor d_i / 2 \rfloor p_c(\lambda) \rfloor \right) 
\ge \frac{1}{n} \sum_* \mathbb{E} \left[ X_i \right] \cdot \frac{1}{2} \ge \frac{C}{n} \sum_* d_i \ge \frac{C'}{l^{\tau - 2}},$$
(5.16)

where the third step uses  $l < d_i p_c(\lambda)/8 \le \lfloor \lfloor d_i/2 \rfloor p_c(\lambda) \rfloor$ , and the final step follows using Assumption 1.3.

Now let  $F_1 := \sum_{i \in [n]} d_i^p \mathbb{1}\{l < d_i^p \le c_1'l\}$  and  $F_2 := \mathbb{E}[F_1|\mathrm{CM}_n(\boldsymbol{d})]$ . We will apply the bounded difference inequality from [27, Corollary 2.27]. Given the graph  $\mathrm{CM}_n(\boldsymbol{d})$ , if we keep one extra edge in the percolated graph, then  $F_1$  can change by at most  $2c_1'l$ . Thus, for any  $\varepsilon > 0$ ,

<span id="page-24-1"></span>
$$\mathbb{P}\Big(|F_1 - F_2| > \frac{n\varepsilon}{l^{\tau - 2}} \mid \mathrm{CM}_n(\boldsymbol{d})\Big) \le 2\exp\left(-\frac{n^2\varepsilon^2}{l^{2(\tau - 2)}(2c_1'l)^2 \cdot \frac{\ell_n}{2}}\right) \le 2e^{-C\varepsilon^2 nl^{-2(\tau - 1)}}. \tag{5.17}$$

<span id="page-24-2"></span>Also, we can apply concentration inequalities such as [12, Lemma 2.5] to conclude that

$$\mathbb{P}\left(|F_2 - \mathbb{E}[F_2]| > \frac{n\varepsilon}{l^{\tau - 2}}\right) \le 2e^{-C\varepsilon^2 n l^{-2(\tau - 1)}}.$$
(5.18)

Combining (5.17) and (5.18) together with (5.16) shows that there exists an  $\varepsilon_0 > 0$  such that (5.14) holds if we replace "for all  $1 \le l \le d_1/c_1'$ " by "for all  $1 \le l \le n^{\varepsilon_0}$ ." For  $l \ge n^{\varepsilon_0}$ , we use (5.1) together with a union bound to complete the proof of (5.14).

#### A A technical lemma

<span id="page-24-0"></span>**Lemma A.1.** Let  $\beta_i^n = n^{-2\alpha} \sum_{j=1}^{i-1} d_j^2$ . Then Assumption 1.1(i), (1.5), and Assumption 1.3 imply the following:

<span id="page-24-5"></span>(i) For all  $\varepsilon > 0$ 

$$\lim_{K \to \infty} \limsup_{n \to \infty} \sum_{i > K} \left( \frac{d_i}{n^{\alpha}} \right) \times e^{-\varepsilon \beta_i^n} = 0.$$
 (A.1)

(ii) There exists a sequence  $(K_n)_{n\geq 1}$  with  $K_n\to\infty$ , and  $K_n=o(n^\alpha)$  such that  $\beta_{K_n}^n>\log^3 n$  for all large n.

*Proof.* We will use  $C_0, C_1, \ldots$  etc. as generic notation for positive constants that do not depend on n. Recall Assumption 1.3. Let  $\theta_{i,n} := n^{-\alpha}d_i$ ,  $i \in [n]$ . We first claim that Assumption 1.3 implies

$$\min_{2 \le i \le n} \theta_{i,n}^{\tau - 2} \sum_{j=1}^{i-1} \theta_{j,n} \ge C_0.$$
(A.2)

<span id="page-24-3"></span>To see this, let  $1 = i_1 < i_2 < i_3 < \dots$  be the indices such that  $d_{i_{k-1}} = d_{i_{k-1}+1} = \dots = d_{i_k-1} > d_{i_k}$  for  $k \ge 2$ . Then for  $k \ge 2$ ,

$$\frac{1}{\ell_n} \sum_{i=1}^{i_k-1} d_i = \mathbb{P}(D_n^* > d_{i_k}) \ge \mathbb{P}(d_{i_k} < D_n^* \le c_1 d_{i_k}) \ge c_0 (d_{i_k})^{-(\tau-2)},$$

and consequently,

$$\min_{k} \theta_{i_{k},n}^{\tau-2} \sum_{j=1}^{i_{k}-1} \theta_{j,n} \ge C_{0}.$$
(A.3)

<span id="page-24-4"></span>If  $i_k > i \ge i_{k-1}$ , then  $\theta_{i,n}^{\tau-2} \sum_{j=1}^{i-1} \theta_{j,n} = \theta_{i_{k-1},n}^{\tau-2} \sum_{j=1}^{i-1} \theta_{j,n} \ge \theta_{i_{k-1},n}^{\tau-2} \sum_{j=1}^{i_{k-1}-1} \theta_{j,n}$ . Thus we conclude (A.2) from (A.3).

Next, define

$$f_n(x) := \begin{cases} \frac{1}{\theta_{i+1,n}}, & \text{if } \sum_{j=1}^{i-1} \theta_{j,n} \le x < \sum_{j=1}^{i} \theta_{j,n} \text{ for some } i \in [n-1], \\ 0, & \text{if } x \ge \sum_{j=1}^{n-1} \theta_{j,n}, \end{cases}$$
(A.4)

and

$$g_n(x) := \begin{cases} \sum_{j=1}^i \theta_{j,n}^2 \,, & \text{if } \sum_{j=1}^{i-1} \theta_{j,n} \le x < \sum_{j=1}^i \theta_{j,n} \text{ for some } i \in [n], \\ 0 \,, & \text{if } x \ge \sum_{j=1}^n \theta_{j,n} \,. \end{cases}$$
 (A.5)

Since  $\sum_{j=1}^{i} \theta_{j,n} \leq 2 \sum_{j=1}^{i-1} \theta_{j,n}$  for  $2 \leq i \leq n$ , we have, using (A.2),  $\theta_{i+1,n}^{\tau-2} \sum_{j=1}^{i-1} \theta_{j,n} \geq C_0/2$ . Therefore,  $f_n(x)^{-(\tau-2)} \times 2x \geq C_0$  for any  $\theta_{1,n} \leq x < \sum_{j=1}^{n-1} \theta_{j,n}$ , and consequently,

$$f_n(x) \le C_1 x^{\frac{1}{\tau - 2}}$$
 for  $\theta_{1,n} \le x < \sum_{j=1}^{n-1} \theta_{j,n}$ . (A.6)

Next, for  $i \in [n-1]$ ,

$$\sum_{j=1}^{i} \theta_{j,n}^{2} \ge \sum_{j=1}^{i} \theta_{j,n} \theta_{j+1,n} = \theta_{1,n} \theta_{2,n} + \int_{\theta_{1,n}}^{\sum_{j=1}^{i} \theta_{j,n}} \frac{\mathrm{d}x}{f_{n}(x)} \\
\ge C_{2} \int_{\theta_{1,n}}^{\sum_{j=1}^{i} \theta_{j,n}} \frac{\mathrm{d}x}{x^{1/(\tau-2)}} \ge C_{3} \left(\sum_{j=1}^{i} \theta_{j,n}\right)^{\frac{\tau-3}{\tau-2}} - C_{4}.$$
(A.7)

<span id="page-25-0"></span>Therefore

$$g_n(x) \ge C_3 x^{\frac{\tau-3}{\tau-2}} - C_4$$
 for  $0 \le x < \sum_{j=1}^{n-1} \theta_{j,n}$ . (A.8)

Now,

$$\sum_{i=K}^{n-1} \theta_{i,n} e^{-\varepsilon \sum_{j=1}^{i} \theta_{j,n}^{2}} = \int_{\sum_{j=1}^{K-1} \theta_{j,n}}^{\sum_{j=1}^{n-1} \theta_{j,n}} e^{-\varepsilon g_{n}(x)} dx \le C_{5} \int_{\sum_{j=1}^{K-1} \theta_{j,n}}^{\infty} e^{-\varepsilon C_{3} x^{\frac{\tau-3}{\tau-2}}} dx,$$
 (A.9)

and the above integral is finite for each fixed  $K \ge 1$ . By Assumption 1.1(i),  $\sum_{j=1}^{K-1} \theta_{j,n} \to \sum_{j=1}^{K-1} \theta_j$  as  $n \to \infty$ , which diverges if we take  $K \to \infty$ . Thus, the proof of (A.1) follows.

We next prove Lemma A.1(ii). Let  $K_n := \lceil n^{\alpha/2} \rceil$ . Suppose that  $\beta_{K_n}^n \leq \log^3 n$ . Using (A.8), it follows that

$$\log^3 n \ge \beta_{K_n}^n \ge C_3 \left(\sum_{j=1}^{K_n} \theta_{j,n}\right)^{\frac{\tau-3}{\tau-2}} - C_4, \tag{A.10}$$

and an application of (A.2) yields

$$C_4 + \log^3 n \ge C(\theta_{K_n+1,n})^{-(\tau-3)} \implies \theta_{K_n,n} \ge \frac{C'}{(\log n)^{\frac{3}{\tau-3}}}.$$
 (A.11)

Therefore,  $\sum_{i=1}^{K_n} \theta_{i,n}^3 \ge C'^3 K_n (\log n)^{-9/(\tau-3)}$ . Thus, if  $\beta_{K_n}^n \le \log^3 n$  for infinitely many n, then

$$\liminf_{n \to \infty} n^{-3\alpha} \sum_{i \in [n]} d_i^3 \ge \liminf_{n \to \infty} \sum_{i=1}^{K_n} \theta_{i,n}^3 = \infty.$$
 (A.12)

On the other hand, Assumption 1.1(i) and (1.5) imply that  $\sup_n n^{-3\alpha} \sum_{i \in [n]} d_i^3 < \infty$ . This leads to a contradiction. Thus the claim in Lemma A.1 (ii) also follows.

#### <span id="page-26-3"></span>**B Degree sequence satisfying compactness criterion**

In this section, we prove Proposition [1.11.](#page-7-2)

Proof of Proposition [1.11.](#page-7-2) Define d (1,n) := (d (1,n) i )i∈[n] with d (1,n) i := dn <sup>α</sup>θie for i ∈ [n]. Let d (2,n) = (d (2,n) i )i∈[n] be such that, for some 0 < K<sup>1</sup> < K<sup>2</sup> < ∞,

$$K_1\left(\frac{n}{i}\right)^{\alpha} \le d_i^{(2,n)} \le K_2\left(\frac{n}{i}\right)^{\alpha}, \quad \text{for } i \in [n],$$
 (B.1)

<span id="page-26-4"></span>and Assumption [1.1\(](#page-2-0)ii) and [\(1.11\)](#page-4-1) are satisfied. The idea is to change the high-degree vertices of d (2,n) by those of d (1,n) . To this end, let

$$i_{\scriptscriptstyle (1,n)} := \max \left\{ i \geq 1 \colon d_i^{\scriptscriptstyle (1,n)} \geq (\frac{n}{\log n})^\alpha \right\} \quad \text{and} \quad i_{\scriptscriptstyle (2,n)} := \max \left\{ i \geq 1 \colon d_i^{\scriptscriptstyle (2,n)} \geq (\frac{n}{\log n})^\alpha \right\}.$$

For two finite sequences (xi) and (y<sup>j</sup> ), we write Sort-Merge((xi),(y<sup>j</sup> )) as the sequence obtained by concatenating (xi) and (y<sup>j</sup> ) and then sorting the sequence in a nonincreasing order. We define

$$\boldsymbol{d}^{(n)} = (d_i^{(n)}) := \mathsf{Sort}\text{-}\mathsf{Merge}\Big((d_i^{(1,n)})_{i=1}^{i_{(1,n)}}, (d_i^{(2,n)})_{i=i_{(2,n)}+1}^n\Big). \tag{B.2}$$

<span id="page-26-5"></span>Note that i(1,n) → ∞. Also,

$$\infty > \sum_{i=1}^{\infty} \theta_i^3 \ge \sum_{i=1}^{i_{(1,n)}} \theta_i^3 \ge i_{(1,n)} \theta_{i_{(1,n)}}^3 \ge i_{(1,n)} \left(\frac{1}{2 \log n}\right)^{3\alpha}, \tag{B.3}$$

and therefore i(1,n) ≤ C(log n) <sup>3</sup>α. Further, it follows from [\(B.1\)](#page-26-4) that i(2,n) ≤ K 1/α 2 (log n). Therefore, the degree sequence in [\(B.2\)](#page-26-5) has length n(1 + o(1)).

Since i(1,n) → ∞, Assumption [1.1](#page-2-0) (i) is satisfied by (d (n) )n≥1. Also, for each fixed K ≥ 1,

$$n^{-3\alpha} \sum_{i>K} (d_i^{(n)})^3 \le \sum_{i>K} 8\theta_i^3 + n^{-3\alpha} \sum_{i>K} (d_i^{(2,n)})^3,$$
(B.4)

and thus [\(1.5\)](#page-2-2) holds. Next, it can be easily checked that the remaining conditions in Assumption [1.1\(](#page-2-0)ii) and [\(1.11\)](#page-4-1) hold for (d (n) )n≥<sup>1</sup> by making use of the fact that (d (2,n) )n≥<sup>1</sup> satisfies Assumption [1.1\(](#page-2-0)ii) and [\(1.11\)](#page-4-1).

Finally we have to verify that (d (n) )n≥<sup>1</sup> satisfies Assumption [1.3.](#page-3-3) It suffices to show that there exist C > 1 and C <sup>0</sup> > 0 such that for all n ≥ 1,

$$\sum_i d_i^{\scriptscriptstyle (n)} \mathbb{1} \left\{ l < d_i^{\scriptscriptstyle (n)} \leq C l \right\} \geq C' n / l^{\tau - 2} \quad \text{for} \quad 1 \leq l < d_1^{\scriptscriptstyle (n)} \, .$$

This can be proved in a straightforward way by using [\(1.18\)](#page-7-1), [\(B.1\)](#page-26-4), and the definition of d (n) given in [\(B.2\)](#page-26-5). We omit the details.

#### <span id="page-26-1"></span>**References**

- [1] Louigi Addario-Berry, Most trees are short and fat, Probab. Theory Relat. Fields **173** (2019), no. 1-2, 1–26. [MR3916103](https://mathscinet.ams.org/mathscinet-getitem?mr=3916103)
- <span id="page-26-0"></span>[2] Louigi Addario-Berry, Nicolas Broutin, and Christina Goldschmidt, The continuum limit of critical random graphs, Probab. Theory Relat. Fields **152** (2012), no. 3, 367–406. [MR2892951](https://mathscinet.ams.org/mathscinet-getitem?mr=2892951)
- <span id="page-26-2"></span>[3] David Aldous, The continuum random tree II: an overview, Stochastic Analysis: Proc. Durham Symp. Stochastic Analysis, 1990 (M T Barlow and N H Bingham, eds.), London Mathematical Society Lecture Note Series, Cambridge University Press, Cambridge, 1991, pp. 23–70. [MR1166406](https://mathscinet.ams.org/mathscinet-getitem?mr=1166406)

- <span id="page-27-13"></span>[4] David Aldous, Gregory Miermont, and Jim Pitman, The exploration process of inhomogeneous continuum random trees, and an extension of Jeulin's local time identity, Probab. Theory Relat. Fields **129** (2004), no. 2, 182–218. [MR2063375](https://mathscinet.ams.org/mathscinet-getitem?mr=2063375)
- <span id="page-27-0"></span>[5] Siva Athreya, Wolfgang Löhr, and Anita Winter, The gap between Gromov-vague and Gromov– Hausdorff-vague topology, Stoch. Proc. Appl. **126** (2016), no. 9, 2527–2553. [MR3522292](https://mathscinet.ams.org/mathscinet-getitem?mr=3522292)
- <span id="page-27-2"></span>[6] Edward A Bender and E. Rodney Canfield, The asymptotic number of labeled graphs with given degree sequences, J. Combin. Theory Ser. A **24** (1978), no. 3, 296–307. [MR0505796](https://mathscinet.ams.org/mathscinet-getitem?mr=0505796)
- <span id="page-27-1"></span>[7] Shankar Bhamidi, Souvik Dhara, Remco van der Hofstad, and Sanchayan Sen, Universality for critical heavy-tailed random graphs: Metric structure of maximal components, Electron. J. Probab. **25** (2020), no. 47, 1–57. [MR4092766](https://mathscinet.ams.org/mathscinet-getitem?mr=4092766)
- <span id="page-27-8"></span>[8] Shankar Bhamidi, Remco van der Hofstad, and Sanchayan Sen, The multiplicative coalescent, inhomogeneous continuum random trees, and new universality classes for critical random graphs, Probab. Theory Relat. Fields **170** (2018), no. 1, 387–474. [MR3748328](https://mathscinet.ams.org/mathscinet-getitem?mr=3748328)
- <span id="page-27-16"></span>[9] Patrick Billingsley, Convergence of Probability Measures, John Wiley & Sons, Inc., 1999. [MR1700749](https://mathscinet.ams.org/mathscinet-getitem?mr=1700749)
- <span id="page-27-14"></span>[10] Arthur Blanc-Renaudie, Compactness and fractal dimensions of inhomogeneous continuum random trees, Probab. Theory Relat. Fields (2022), 1–31.
- <span id="page-27-3"></span>[11] Béla Bollobás, A probabilistic proof of an asymptotic formula for the number of labelled regular graphs, European J. Combin. **1** (1980), no. 4, 311–316. [MR0595929](https://mathscinet.ams.org/mathscinet-getitem?mr=0595929)
- <span id="page-27-21"></span>[12] Christian Borgs, Jennifer T. Chayes, Souvik Dhara, and Subhabrata Sen, Limits of sparse configuration models and beyond: Graphexes and Multi-Graphexes, Ann. Probab. **49** (2021), no. 6, 2830–2873. [MR4348680](https://mathscinet.ams.org/mathscinet-getitem?mr=4348680)
- <span id="page-27-15"></span>[13] Nicolas Broutin, Thomas Duquesne, and Minmin Wang, Limits of multiplicative inhomogeneous random graphs and lévy trees: limit theorems, Probab. Theory Relat. Fields **181** (2021), no. 4, 865–973. [MR4344135](https://mathscinet.ams.org/mathscinet-getitem?mr=4344135)
- <span id="page-27-12"></span>[14] Michael Camarri and Jim Pitman, Limit distributions and random trees derived from the birthday problem with unequal probabilities, Electron. J. Probab. **5** (2000), 1–18. [MR1741774](https://mathscinet.ams.org/mathscinet-getitem?mr=1741774)
- <span id="page-27-10"></span>[15] Guillaume Conchon-Kerjan and Christina Goldschmidt, The stable graph: the metric space scaling limit of a critical random graph with i.i.d. power-law degrees, [arXiv:2002.04954](https://arXiv.org/abs/2002.04954) (2020). [MR4043223](https://mathscinet.ams.org/mathscinet-getitem?mr=4043223)
- <span id="page-27-5"></span>[16] Souvik Dhara, Remco van der Hofstad, Johan S. H. van Leeuwaarden, and Sanchayan Sen, Heavy-tailed configuration models at criticality, Ann. Inst. H. Poincaré (B) Probab. Statist. **56** (2020), no. 3, 1515–1558. [MR4116701](https://mathscinet.ams.org/mathscinet-getitem?mr=4116701)
- <span id="page-27-20"></span>[17] Devdatt Dubhashi, Volker Priebe, and Desh Ranjan, Negative dependence through the FKG inequality, Basic Research in Computer Science (BRICS) (1996).
- <span id="page-27-18"></span>[18] C. G Esseen, On the concentration function of a sum of independent random variables, Zeitschrift für Wahrscheinlichkeitstheorie und Verwandte Gebiete **9** (1968), no. 4, 290–308. [MR0231419](https://mathscinet.ams.org/mathscinet-getitem?mr=0231419)
- <span id="page-27-7"></span>[19] Nikolaos Fountoulakis, Percolation on sparse random graphs with given degree sequence, Internet Math. **4** (2007), no. 1, 329–356. [MR2522948](https://mathscinet.ams.org/mathscinet-getitem?mr=2522948)
- <span id="page-27-17"></span>[20] David A Freedman, On tail probabilities for martingales, Ann. Probab. **3** (1975), no. 1, 100–118. [MR0380971](https://mathscinet.ams.org/mathscinet-getitem?mr=0380971)
- <span id="page-27-11"></span>[21] Christina Goldschmidt, Bénédicte Haas, and Delphin Sénizergues, Stable graphs: distributions and line-breaking construction, [arXiv:1811.06940](https://arXiv.org/abs/1811.06940) (2018).
- <span id="page-27-9"></span>[22] Andreas Greven, Peter Pfaffelhuber, and Anita Winter, Convergence in distribution of random metric measure spaces (Λ-coalescent measure trees), Probab. Theory Relat. Fields **145** (2009), no. 1, 285–322. [MR2520129](https://mathscinet.ams.org/mathscinet-getitem?mr=2520129)
- <span id="page-27-4"></span>[23] Remco van der Hofstad, Random Graphs and Complex Networks, vol. 1, Cambridge University Press, Cambridge, 2017. [MR3617364](https://mathscinet.ams.org/mathscinet-getitem?mr=3617364)
- <span id="page-27-6"></span>[24] Svante Janson, The probability that a random multigraph is simple, Comb. Probab. Comp. **18** (2009), no. 1-2, 205–225. [MR2497380](https://mathscinet.ams.org/mathscinet-getitem?mr=2497380)
- <span id="page-27-19"></span>[25] Svante Janson, Susceptibility of random graphs with given vertex degrees, J. Combin. **1** (2010), no. 3-4, 357–387. [MR2799217](https://mathscinet.ams.org/mathscinet-getitem?mr=2799217)

- <span id="page-28-1"></span>[26] Svante Janson and Malwina J. Luczak, A new approach to the giant component problem, Random Struct. Algor. **34** (2009), no. 2, 197–216. [MR2490288](https://mathscinet.ams.org/mathscinet-getitem?mr=2490288)
- <span id="page-28-8"></span>[27] Svante Janson, Tomasz Łuczak, and Andrzej Rucinski, Random Graphs., Wiley, New York, 2000. [MR1782847](https://mathscinet.ams.org/mathscinet-getitem?mr=1782847)
- <span id="page-28-4"></span>[28] Tomasz Łuczak, The number of trees with large diameter, J. Aust. Math. Soc. Series A. Pure Mathematics and Statistics **58** (1995), no. 3, 298–311. [MR1329866](https://mathscinet.ams.org/mathscinet-getitem?mr=1329866)
- <span id="page-28-6"></span>[29] Grégory Miermont and Sanchayan Sen, On breadth-first constructions of scaling limits of random graphs and random unicellular maps, Random Struct. Algorithms.
- <span id="page-28-2"></span>[30] Michael Molloy and Bruce Reed, A critical-point for random graphs with a given degree sequence, Random Struct. Algor. **6** (1995), no. 2-3, 161–179. [MR1370952](https://mathscinet.ams.org/mathscinet-getitem?mr=1370952)
- <span id="page-28-0"></span>[31] Asaf Nachmias and Yuval Peres, Critical random graphs: Diameter and mixing time, Ann. Probab. **36** (2008), no. 4, 1267–1286. [MR2435849](https://mathscinet.ams.org/mathscinet-getitem?mr=2435849)
- <span id="page-28-3"></span>[32] G Szekeres, Distribution of labelled trees by diameter, Combinatorial Mathematics X (Berlin, Heidelberg) (Louis Reynolds Antoine Casse, ed.), Springer Berlin Heidelberg, 1983, pp. 392– 397.
- <span id="page-28-5"></span>[33] Minmin Wang, Height and diameter of Brownian tree, Electron. Commun. Probab. **20** (2015), no. 88, 1–15. [MR3434205](https://mathscinet.ams.org/mathscinet-getitem?mr=3434205)
- <span id="page-28-7"></span>[34] Ward Whitt, Stochastic-Process Limits: An Introduction to Stochastic-Process Limits and Their Application to Queues, Springer-Verlag, New York, 2002. [MR1876437](https://mathscinet.ams.org/mathscinet-getitem?mr=1876437)

# **Electronic Journal of Probability Electronic Communications in Probability**

## **Advantages of publishing in EJP-ECP**

- Very high standards
- Free for authors, free for readers
- Quick publication (no backlog)
- Secure publication [\(LOCKSS](http://en.wikipedia.org/wiki/LOCKSS)<sup>1</sup> )
- Easy interface [\(EJMS](https://vtex.lt/services/ejms-peer-review)<sup>2</sup> )

# **Economical model of EJP-ECP**

- Non profit, sponsored by [IMS](http://en.wikipedia.org/wiki/Institute_of_Mathematical_Statistics)<sup>3</sup> , [BS](http://en.wikipedia.org/wiki/Bernoulli_Society)<sup>4</sup> , [ProjectEuclid](https://projecteuclid.org/)<sup>5</sup>
- Purely electronic

# **Help keep the journal free and vigorous**

- Donate to the IMS open access fund<sup>6</sup> [\(click here to donate!\)](https://imstat.org/shop/donation/)
- Submit your best articles to EJP-ECP
- Choose EJP-ECP over for-profit journals

<sup>1</sup>LOCKSS: Lots of Copies Keep Stuff Safe <http://www.lockss.org/>

<sup>2</sup>EJMS: Electronic Journal Management System: <https://vtex.lt/services/ejms-peer-review/>

<sup>3</sup> IMS: Institute of Mathematical Statistics <http://www.imstat.org/>

<sup>4</sup>BS: Bernoulli Society <http://www.bernoulli-society.org/>

<sup>5</sup>Project Euclid: <https://projecteuclid.org/>

<sup>6</sup> IMS Open Access Fund: <https://imstat.org/shop/donation/>