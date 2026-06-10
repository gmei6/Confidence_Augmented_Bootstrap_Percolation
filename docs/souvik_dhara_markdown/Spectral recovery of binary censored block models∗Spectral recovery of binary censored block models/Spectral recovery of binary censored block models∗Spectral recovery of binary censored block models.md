# Spectral recovery of binary censored block models\*

Souvik Dhara<sup>†</sup>, Julia Gaudio<sup>‡</sup>, Elchanan Mossel<sup>†</sup>, Colin Sandon<sup>†</sup>

#### Abstract

Community detection is the problem of identifying community structure in graphs. Often the graph is modeled as a sample from the Stochastic Block Model, in which each vertex belongs to a community. The probability that two vertices are connected by an edge depends on the communities of those vertices. In this paper, we consider a model of censored community detection with two communities, where most of the data is missing as the status of only a small fraction of the potential edges is revealed. In this model, vertices in the same community are connected with probability p while vertices in opposite communities are connected with probability q. The connectivity status of a given pair of vertices  $\{u,v\}$  is revealed with probability  $\alpha$ , independently across all pairs, where  $\alpha = t^{\log(n)}/n$ . We establish the information-theoretic threshold  $t_c(p,q)$ , such that no algorithm succeeds in recovering the communities exactly when  $t < t_c(p,q)$ . We show that when  $t > t_c(p,q)$ , a simple spectral algorithm based on a weighted, signed adjacency matrix succeeds in recovering the communities exactly.

While spectral algorithms are shown to have near-optimal performance in the symmetric case, we show that they may fail in the asymmetric case where the connection probabilities inside the two communities are allowed to be different. In particular, we show the existence of a parameter regime where a simple two-phase algorithm succeeds but *any* algorithm based on the top two eigenvectors of the weighted, signed adjacency matrix fails.

### 1 Introduction

The problem of detecting community structure is an important question in the study of networks. The canonical formulation of this problem is made via the *stochastic block model* (SBM), where each vertex is a member of one of K communities, and vertices create an edge independently based on their latent community assignments. The objective is to recover the latent community assignments based on the observed network. One may be interested in exact, partial, or weak recovery. When the average degree scales as  $\Theta(\log n)$ , such that the graph is connected with high probability, one is often interested in recovering the community assignments exactly. Previous literature gives us precise characterization on when the exact recovery problem is efficiently solvable and when it is information theoretically impossible [3, 5, 12, 15]. See the survey [1] for an overview.

Popular approaches for community detection in the stochastic block model include spectral algorithms and semidefinite programming. Given the adjacency matrix representation of the graph, spectral algorithms use properties of the eigenvalues and eigenvectors of the matrix in order to infer the communities [4, 7, 16, 17]. Other approaches are based on the "non-backtracking" matrix of the graph [6, 12]. Semidefinite programming approaches [9, 10, 14] are typically a relaxation of the maximum likelihood estimator, which is NP-hard to compute directly.

In this paper, we study the community detection problem when we only have partial knowledge about the graph. The information about the status of an edge between each pair of vertices is *censored* independently, i.e., an edge between a pair of vertices can be present, absent or censored. A precise description is given below in Definition 2.1. This model is referred to as the *Censored Stochastic Block Model* (CSBM). Abbe, Bandeira, Bracher, and Singer [2] were the first to address the exact recovery problem on CSBM when the within community edge probability p and the between community edge probability p satisfy p+q=1. They show that the Maximum Likelihood Estimator (MLE) achieves exact recovery up to the information theoretic threshold. However, the MLE turns out to be equivalent to the Max-Cut problem and is thus NP-hard to compute. For this reason, [2]

<sup>\*</sup>A full version of the paper can be accessed at arXiv:2107.06338

<sup>&</sup>lt;sup>†</sup>Department of Mathematics, Massachusetts Institute of Technology

<sup>&</sup>lt;sup>‡</sup>Department of Industrial Engineering and Management Sciences, Northwestern University

Emails: sdhara@mit.edu, julia.gaudio@northwestern.edu, elmos@mit.edu, csandon@mit.edu

Acknowledgement: S.D., E.M and C.S. are partially supported by Vannevar Bush Faculty Fellowship ONR-N00014-20-1-2826. E.M. and C.S. are partially supported by NSF award DMS-1737944. E.M. is partially supported by Simons Investigator award (622132) and by ARO MURI W911NF1910217. Part of this work was completed while J.G. was at the Department of Mathematics, Massachusetts Institute of Technology.

considered the Semidefinite Programming (SDP) relaxation which was shown to work in a certain regime. Later, Hajek, Wu, and Xu [\[8,](#page-22-9) [10\]](#page-22-7) proved that, under this set up, the SDP relaxation actually works up to the information theoretic threshold.

The impressive line of work above leaves an important question open: what families of algorithms achieve exact recovery for the CSBM up to the information theoretic threshold? Given that semidefinite programming is less efficient than spectral approaches, the main question of this paper is:

Question: Are spectral algorithms information theoretically optimal for exact recovery of CSBMs?

It is important to note here the difference between purely spectral algorithms and algorithms that combine spectral algorithms with additional clean-up procedures. The results on exact recovery for the standard block model in [\[3,](#page-21-0) [15\]](#page-22-1) used spectral algorithms as the first step in a two stage procedure. In the usual uncensored stochastic block model, Abbe, Fan, Wang, and Zhong [\[4\]](#page-21-3) recently showed that the spectral algorithm is optimal, without need for a clean-up stage. It was not immediately clear whether the same would be true for the censored version that we consider, since observations are ternary (present, absent, censored) rather than binary (present, absent).

We are also interested in answering the spectral question in a more general setup than what was previously considered. First, previous results focused on the case that p + q = 1 which ensures that a present edge carries the same relative information as an absent edge. We see that this condition can be avoided. Second, we are also interested in cases where the edge probabilities within different communities are different. In our main results we show that:

- B spectral algorithms are optimal for the CSBM for all values of p, q above the information theoretic threshold, and
- B if the interconnection probabilities inside two communities are different, then spectral algorithms are sub-optimal in a regime of parameters.

The latter result is not a sign of a computational-statistical gap as we find a simple two stage algorithm that exactly recovers the communities in this case.

### 2 Model and main results

### 2.1 Model description. We start by defining the Censored Stochastic Block Model.

Definition 2.1. (Censored Stochastic Block Model (CSBM)) We have n vertices with labels given by σ<sup>0</sup> ∈ {±1} <sup>n</sup> := S. The vertices i with σ0(i) = +1 (resp. σ0(i) = −1) are said to be in Community 1 (resp. Community 2). The labels are generated independently, with

<span id="page-1-1"></span><span id="page-1-0"></span>
$$\mathbb{P}(\sigma_0(i) = +1) = \frac{1}{2} \quad and \quad \mathbb{P}(\sigma_0(i) = -1) = \frac{1}{2}.$$

Two vertices i 6= j are connected by an edge with probability p<sup>1</sup> if σ0(i) = σ0(j) = +1, p<sup>2</sup> if σ0(i) = σ0(j) = −1, and q if σ0(i) 6= σ0(j). Self-loops do not occur. Each edge status is revealed independently with probability α = <sup>t</sup> log <sup>n</sup>/<sup>n</sup> for a constant t > 0. The output is a graph with edge statuses given by {present, absent, censored}. We denote this censored model by CSBM(p1, p2, q, α). In the symmetric case where p<sup>1</sup> = p<sup>2</sup> = p, we denote the model by CSBM(p, q, α). For a visualization of the model, see Figure [1.](#page-2-0)

Objective. We observe a graph G from CSBM(p1, p2, q, t) with vertex labels removed (i.e., σ<sup>0</sup> is unknown), and edges labeled by {present, absent, censored}. An estimator σˆ is said to achieve exact recovery if

(2.1) 
$$\lim_{n \to \infty} \mathbb{P}(\exists s \in \{\pm 1\} : \hat{\sigma} = s\sigma_0) = 1.$$

We say that exact recovery is possible if there exists some estimator σˆ such that [\(2.1\)](#page-1-1) holds.

Next, we provide formal statements of the main results, along with the key conceptual contributions.

<span id="page-2-0"></span>![](_page_2_Picture_0.jpeg)

Figure 1: Blue and red vertices represent Community 1 and 2, respectively. Each pair of vertices is connected with probability  $p_1$ ,  $p_2$ , or q according to the communities of the vertices. The black graph is the sample that we see; vertex labels are absent, and edges may be present (solid line), absent (no line), or censored (dotted line).

<span id="page-2-6"></span>**2.2** Optimality of the spectral algorithm in the symmetric case. Consider the symmetric case  $p_1 = p_2 = p$  and  $p \neq q$ . Throughout, we assume that  $p, q \in (0, 1)$  and t > 0 are fixed. We will establish that the information-theoretic threshold for exact recovery is given by:

(2.2) 
$$t_c(p,q) := \frac{2}{(\sqrt{p} - \sqrt{q})^2 + (\sqrt{1-q} - \sqrt{1-p})^2}.$$

<span id="page-2-1"></span>Our first result shows that if  $t < t_c(p, q)$ , then any estimator fails to achieve exact recovery with high probability. THEOREM 2.1. If  $t < t_c(p, q)$ , then any estimator  $\hat{\sigma}$  satisfies  $\mathbb{P}(\hat{\sigma} = \sigma_0) = o(1)$ .

<span id="page-2-5"></span><span id="page-2-4"></span>![](_page_2_Figure_5.jpeg)

Figure 2: Contour plot for the region where exact recovery is impossible, i.e.,  $t < t_c(p, q)$  for t = 10, 20, 30. As t decreases the impossibility region expands.

Figure 2 illustrates the region  $t < t_c(p,q)$ . Next, we describe the success of a simple spectral algorithm for  $t > t_c(p,q)$ . To this end, we need a weighted version of the signed adjacency matrix. Let

(2.3) 
$$y = y(p,q) = \frac{\log\left(\frac{1-q}{1-p}\right)}{\log\left(\frac{p}{q}\right)},$$

and define the signed adjacency matrix as

<span id="page-2-2"></span>
$$A_{ij} = \begin{cases} 1 & \text{if } \{i, j\} \text{ is present} \\ -y & \text{if } \{i, j\} \text{ is absent} \\ 0 & \text{if } \{i, j\} \text{ is censored.} \end{cases}$$

<span id="page-2-3"></span>Note that y > 0 whenever  $p \neq q$ . Our next result shows that the spectral algorithm achieves exact recovery for  $t > t_c(p, q)$ .

THEOREM 2.2. Let  $u_1$  be the top eigenvector of A and define  $\hat{\sigma}_{Spec} = sign(u_1)$ . If  $t > t_c(p,q)$  and p > q, then there exists  $\eta = \eta(p,q) > 0$  and  $s \in \{\pm 1\}$  such that, with probability 1 - o(1),

<span id="page-3-2"></span>
$$s\sqrt{n}\min_{i\in[n]}\sigma_0(i)(u_1)_i\geq\eta.$$

Consequently,  $\hat{\sigma}_{Spec}$  achieves exact recovery for  $t > t_c(p,q)$ . If p < q, all conclusions hold if we replace A by -A.

The estimator  $\hat{\sigma}_{\text{Spec}}$  does not require additional clean-up steps. For the non-censored SBM, Abbe et. al. [4] established an analogous result using entrywise eigenvector perturbation analysis, which we will also use (see Proposition 5.1). The key distinction of our algorithm to that of Abbe. et. al. [4] lies in the fact that the observed graph admits a ternary encoding as opposed to a binary encoding. It is worthwhile to remark that the choice of y is important for the spectral algorithm to succeed up to the information theoretic threshold, and in fact, (2.3) is the only choice of y that works. Intuitively, y is the ratio of evidence provided by a present edge on a vertex's community as compared to an absent edge. More precisely, if we compute the log-likelihood ratio for a vertex to be in one community or the other, then it turns out to be a linear function of the number of present and absent edges to each community. In the symmetric case, the ratio of the coefficients corresponding to present and absent edges to Community y turns out to be y for both y = 1, when y + q = 1, i.e., in the special case considered in [2, 10], we have that y = 1, and the relative information provided by present and absent edges are equal. Therefore, Theorem 2.2 shows that the spectral algorithm with y = 1 would succeed in exact recovery in the model of [2, 10].

We conclude this section by showing that the error rate of the spectral algorithm is close to that of the best possible estimator. For an estimator  $\hat{\sigma}$ , we define the error rate as

(2.4) 
$$\operatorname{Err}(\hat{\sigma}) = \mathbb{E}\left[\min_{s \in \{-1, +1\}} \frac{1}{n} \sum_{i=1}^{n} \mathbb{1}_{\{\hat{\sigma}(i) \neq s\sigma_0(i)\}}\right].$$

To define the best estimator, we use a genie-aided approach. Suppose that we want to find the label of u. Now, in addition to the observed edge-labeled graph G, suppose a genie gives us  $(\sigma_0(v))_{v \in [n] \setminus \{u\}}$ . The genie-based estimator minimizes the probability of making an error given these observations. More precisely, the genie-based estimator  $\hat{\sigma}_{\text{Best}}$  is given by

(2.5) 
$$\hat{\sigma}_{\text{Best}}(u) := \operatorname*{argmax}_{r \in \{\pm 1\}} \mathbb{P}(\sigma_0(u) = r \mid G, (\sigma_0(v))_{v \in [n] \setminus \{u\}}).$$

The next result shows that the error rate of  $\hat{\sigma}_{\text{Spec}}$  is within a  $n^{o(1)}$  factor of the error rate of  $\hat{\sigma}_{\text{Best}}$ :

THEOREM 2.3. For any fixed t > 0, the spectral and genie-aided estimators satisfy

<span id="page-3-0"></span>
$$\mathrm{Err}(\hat{\sigma}_{\mathrm{Spec}}) = n^{o(1)} \mathrm{Err}(\hat{\sigma}_{\mathrm{Best}}) + O(n^{-3}) = n^{-(1+o(1))t/t_c(p,q)} + O(n^{-3}).$$

Therefore, the expected number of misclassified vertex-labels by the spectral algorithm is at most  $n^{o(1)}$  times that of the genie estimator. In particular, if  $t > t_c(p,q)$ , then this expected number is o(1) which is why exact recovery is achievable by the spectral algorithm.

REMARK 2.1. If p,q are unknown, then it is not difficult to estimate them. Indeed, if E,T respectively denote the number of edges and triangles in the graph then  $E = (1+o(1))\frac{tn\log n}{4}(p+q)$  and  $T = (1+o(1))\frac{t^3\log^3 n}{8}\left(pq^2+\frac{1}{3}p^3\right)$  with probability tending to 1. We can use these to find consistent estimator  $(\hat{p},\hat{q})$  of (p,q) and use the spectral algorithm with  $\hat{y} = y(\hat{p},\hat{q})$ . The conclusions of Theorem 2.2 and Theorem 2.3 still remain valid.

<span id="page-3-1"></span>2.3 Beating the spectral algorithm Theorems 2.2 and 2.3 strongly support the success of the spectral algorithm. We next provide results to show that there is room for improvement. First, Theorem 2.3 proves a  $n^{o(1)}$  relative discrepancy between the error rates of the spectral and the genie estimators, and therefore, the expected difference between misclassified vertices under these two algorithms may grow with n. We prove that with an additional clean-up step, one can in fact get a 1 + o(1) relative discrepancy between the error rates. Second, we consider the case where the connection probabilities within Community 1  $(p_1)$  and Community 2  $(p_2)$  differ. In this case, we show that the spectral algorithm does not always work up to the information-theoretic threshold.

Intuitively, if  $p_1 \neq p_2$ , then the relative information provided by present and absent edges are different for vertices in different communities. For this reason, it is not possible to find a common choice of encoding y which works well for vertices in both communities. We establish the failure of the spectral algorithm rigorously for  $p_1 = 1 - p_2$  and q = 1/2. On the other hand, an algorithm based on degrees and an additional clean-up step turns out to be near-optimal for any  $p_1, p_2, q$ .

We start by introducing the two-step estimator for which we need some notation. For a given vertex u and  $\sigma \in \mathcal{S}$ , let  $D = D(\sigma, u) = (D_i(\sigma, u))_{i=1}^4$  be the degree profile where  $D_1, D_2$  (resp.  $D_3, D_4$ ) are the number of present and absent edges to vertices in Community 1 (resp. Community 2). Note that  $D(\sigma, u)$  depends only on G and  $(\sigma(v))_{v \in [n] \setminus \{u\}}$ . Define  $\Gamma(u, \sigma, p_1, p_2, q)$  by

<span id="page-4-3"></span>(2.6) 
$$\Gamma(u, \sigma, p_1, p_2, q) = D_1(\sigma, u) \log \frac{p_1}{q} + D_2(\sigma, u) \log \frac{1 - p_1}{1 - q} + D_3(\sigma, u) \log \frac{q}{p_2} + D_4(\sigma, u) \log \frac{1 - q}{1 - p_2}$$

<span id="page-4-5"></span>DEFINITION 2.2. (TWO-STEP ESTIMATOR) Given an initial estimator  $\hat{\sigma}$ , a two-step estimator  $\hat{X}(\hat{\sigma})$  is computed as follows:

(2.7) 
$$\hat{X}(\hat{\sigma}, u) = \begin{cases} +1 & \text{if } \Gamma(u, \hat{\sigma}, p_1, p_2, q) \ge 0, \\ -1 & \text{otherwise.} \end{cases}$$

The function  $\Gamma(\cdot)$  is designed to mimic the workings of the genie estimator. In fact, we will later show that  $\hat{\sigma}_{\text{Best}}(u) = +1$  if and only if  $\Gamma(u, \sigma_0, p_1, p_2, q) \geq 0$  (see Proposition 6.1). Thus the two-step estimator treats the initial estimator as a proxy of the true community assignment and then does the same procedure as the genie estimator. The following result states that the two-step version of the spectral estimator has a sharper error rate in the symmetric case.

THEOREM 2.4. If  $p_1 = p_2 = p$  and  $p \neq q$ , then for any t > 0,

<span id="page-4-1"></span>
$$\operatorname{Err}(\hat{X}(\hat{\sigma}_{\text{Spec}})) = (1 + o(1))\operatorname{Err}(\hat{\sigma}_{\text{Best}}) + o(1/n).$$

Next, we show that, for  $p_1 \neq p_2$ , the two-step estimator based on degrees in the observed graph has similar strong recovery guarantees. Let  $\deg(i)$  be the number of present edges incident to vertex i. Define the degree-based estimator to be

<span id="page-4-0"></span>
$$\hat{\sigma}_{\text{Deg}}(i) = \operatorname{sign}\left(\operatorname{deg}(i) - \frac{t \log(n)}{4}(p_1 + p_2 + 2q)\right).$$

Let  $c_1 = (p_1, 1 - p_1, q, 1 - q)$ , and  $c_2 = (q, 1 - q, p_2, 1 - p_2)$  and define

(2.8) 
$$t_c(p_1, p_2, q) = \left[1 - \frac{1}{2} \min_{x \in [0, 1]} \sum_i (c_1)_i^x (c_2)_i^{1-x}\right]^{-1}.$$

When  $p_1 = p_2 = p$ , then it is elementary to check that the minimum in (2.8) is attained for x = 1/2 and therefore

$$(2.9) t_c(p, p, q) = t_c(p, q),$$

where  $t_c(p,q)$  is given by (2.2). We next provide success guarantees for  $\hat{X}(\hat{\sigma}_{\text{Deg}})$ .

THEOREM 2.5. If  $p_1, p_2, q \in (0,1)$  are distinct, then for any t > 0,

<span id="page-4-4"></span><span id="page-4-2"></span>
$$\operatorname{Err}(\hat{X}(\hat{\sigma}_{\operatorname{Deg}})) = (1 + o(1))\operatorname{Err}(\hat{\sigma}_{\operatorname{Best}}) + o(1/n).$$

Furthermore, if  $t > t_c(p_1, p_2, q)$ , then  $\hat{X}(\hat{\sigma}_{\text{Deg}})$  achieves exact recovery.

REMARK 2.2. If  $p_1$ ,  $p_2$ , and q are unknown, then one can estimate them as follows. First, classify each vertex according to whether its degree is above average. This procedure will result in an estimator  $\hat{\sigma}$  with at most  $n^{1-\varepsilon}$  errors on average, i.e.,  $\operatorname{Err}(\hat{\sigma}) = O(n^{-\varepsilon})$  for some  $\varepsilon > 0$ . Then we can estimate the parameters by counting revealed edges and non-edges between and within the estimated communities.

<span id="page-5-1"></span>![](_page_5_Figure_0.jpeg)

<span id="page-5-2"></span>Figure 3: The estimator  $\hat{X}(\hat{\sigma}_{\text{Deg}})$  achieves exact recovery in the gray regions, corresponding to  $t > t_c(p, 1-p, 1/2)$ . No spectral algorithm can achieve exact recovery in a neighborhood of the dotted lines, represented schematically by the light gray regions.

If  $p_1 = p_2$ , then  $\hat{\sigma}_{\text{Deg}}$  cannot achieve spectral recovery. In this sense, Theorem 2.4 and Theorem 2.5 are complementary. We next describe the failure of the spectral algorithm for  $p_1 = 1 - p_2$  and q = 1/2. Let us start by defining a version of the spectral algorithm which makes decisions based on arbitrary linear combinations of the top two eigenvectors of some encoding matrix.

DEFINITION 2.3. Given an encoding parameter  $y \in \mathbb{R}$ , threshold  $r \in \mathbb{R}$  and constants  $\gamma_1, \gamma_2 \in \mathbb{R}$ , let A be the signed adjacency matrix with entries  $A_{ij} \in \{-y, 0, 1\}$ . Let  $u_1$  and  $u_2$  be the two top eigenvectors of A. Then the spectral algorithm Spectral $(y, r, \gamma_1, \gamma_2)$  outputs the estimator

(2.10) 
$$\hat{\sigma}(i) = \text{sign}(\gamma_1(u_1)_i + \gamma_2(u_2)_i - r).$$

In other words, the spectral algorithm decides community assignments using a thresholding on a linear combination of the top two eigenvectors of some encoding matrix. Only the top two eigenvectors are included since the eigenvectors of A behave like noisy versions of the eigenvectors of the rank-2 matrix  $A^*$ . The following result states that even this more general algorithm fails in the antisymmetric CSBM for t sufficiently close to the recovery threshold.

<span id="page-5-0"></span>THEOREM 2.6. Let  $p_1 = p = 1 - p_2$  and q = 1/2. There exists  $\delta > 0$  such that if  $t < t_c(p, 1 - p, 1/2) + \delta$ , then, for any choice of  $y, r, \gamma_1, \gamma_2$ , the algorithm Spectral $(y, r, \gamma_1, \gamma_2)$  fails to achieve exact recovery with probability 1 - o(1).

Theorems 2.5 and 2.6 together show that there is a range of values of t where the spectral algorithm fails in exact recovery, but  $\hat{X}(\hat{\sigma}_{\text{Deg}})$  succeeds (see Figure 3). In other words, there is a strong separation between the spectral algorithm and the two-step procedure based on degrees. One can now see the failure of the spectral algorithm from a technical perspective. In this regime, the top two eigenvectors of the encoding matrix A are close to  $Au_1^*/\lambda_1^*$  and  $Au_2^*/\lambda_2^*$  respectively where  $u_i^*$  is the i-th largest eigenvector of the expectation matrix. If we imagine replacing  $u_1$  and  $u_2$  in (2.10) by their approximations, then the decision rule for the label of a vertex u is given by the sign of  $\sum_i z_i D_i - r_0$  for some coefficients  $\{z_i\}$  and threshold  $r_0$ , where  $D_i$  denotes the degree profile of u. Moreover, due to the choice of the encoding, the coefficients  $(z_1, z_2, z_3, z_4)$  satisfy  $\frac{z_1}{z_2} = \frac{z_3}{z_4} = y$ . The estimator that minimizes the error probability can also be shown to decide communities based on the sign of  $\sum_i z_i' D_i > r_0'$ , but in order to satisfy the additional condition  $\frac{z_1'}{z_2'} = \frac{z_3'}{z_4'} = y$ , one requires  $y(p_1,q) = y(p_2,q)$ , or  $p_1 = p_2$ . For this reason, the spectral algorithm is strictly less powerful than the best possible estimator and thus one cannot expect the spectral algorithm to work all the way up to the information theoretic threshold if  $y(p_1,q) \neq y(p_2,q)$ . Theorem 2.6 makes this intuition precise for  $p_1 = 1 - p_2$ .

**Organization.** The remainder of the paper is structured as follows. We start by setting up some preliminary notation in Section 3. In Section 4, we prove impossibility for the exact recovery problem in Theorem 2.1. Section 5 is devoted to entrywise perturbation analysis of the largest eigenvector of A and completing the proof of

Theorem 2.2. The error analysis for the spectral algorithm and the genie estimator will be provided in Section 6 and hence the proof of Theorem 2.3 will be completed. In Section 7, we analyze the two-step estimator for a general class of initial estimators. This allows us to complete proofs of Theorems 2.4 and 2.5. Finally, we conclude with a proof of Theorem 2.6 regarding failure of the spectral algorithm in Section 8. We provide proof ideas at the beginnings of Sections 4-8.

### <span id="page-6-0"></span>3 Notation and preliminaries

Let  $[n] = \{1, 2, ..., n\}$ . We often use the Bachmann–Landau notation o(1), O(1) etc. For two sequences  $(a_n)_{n\geq 1}$  and  $(b_n)_{n\geq 1}$ , we write  $a_n \approx b_n$  as a shorthand for  $\lim_{n\to\infty} \frac{a_n}{b_n} = 1$ . We write  $a_n \sim b_n$  if  $a_n$  and  $b_n$  are asymptotically equivalent, namely  $\lim_{n\to\infty} \frac{a_n}{b_n} \to c$  for some  $c\neq 0$ . Additionally, we write  $a_n\approx b_n$  if these sequences differ by a polylogarithmic factor asymptotically, namely there exists some constant c such that  $a_n = O\left(b_n\log^c(n)\right)$  and  $b_n = O\left(a_n\log^c(n)\right)$ . For random variables  $(X_n)_{n\geq 1}$ , we write  $X_n = o_{\mathbb{P}}(1)$  as a shorthand for  $X_n \to 0$  in probability. For a vector  $x\in\mathbb{R}^n$ , we define  $\|x\|_2 = (\sum_{i=1}^n x_i^2)^{1/2}$  and  $\|x\|_\infty = \max_i |x_i|$ . For a matrix  $M\in\mathbb{R}^{n\times d}$ , we use  $M_i$  to refer to its i-th row, represented as a row vector. Given a matrix M,  $\|M\|_2 = \max_{\|x\|_2 = 1} \|Mx\|_2$  is the spectral norm, and  $\|M\|_{2\to\infty} = \max_i \|M_i\|_2$  is the matrix  $2\to\infty$  norm. We use the convention that log denotes natural logarithm, and write  $\log^k(n)$  to mean  $(\log(n))^k$ . Finally,  $D_{\text{KL}}(p\|q)$  refers to the Kullback–Leibler divergence of two Bernoulli random variables with parameters p and q:

<span id="page-6-4"></span><span id="page-6-2"></span>
$$D_{\text{\tiny KL}}(p||q) = p \log \left(\frac{p}{q}\right) + (1-p) \log \left(\frac{1-p}{1-q}\right).$$

Let  $n_1(\sigma_0) = |\{v : \sigma_0(v) = +1\}|$  and  $n_2(\sigma_0) = |\{v : \sigma_0(v) = -1\}|$ . Note that since  $n_1(\sigma_0), n_2(\sigma_0)$  are marginally distributed as Bin  $(n, \frac{1}{2})$ , we have that for all  $\varepsilon \in (0, 1)$ ,

(3.1) 
$$\left| n_1(\sigma_0) - \frac{n}{2} \right| \le \varepsilon n \text{ and } \left| n_2(\sigma_0) - \frac{n}{2} \right| \le \varepsilon n$$

<span id="page-6-3"></span>with probability at least  $1 - 2\exp(-\varepsilon^2 n/6)$ . We will often use (3.1) with  $\varepsilon = n^{-\frac{1}{3}}$ . Additionally, let N(u) be the number of vertices whose connections to u are revealed:  $N(u) := \{v : \{u, v\} \text{ is revealed}\}$ . By [11, Corollary 2.4] for c > 1

$$(3.2) \mathbb{P}(N(i) \ge \log^c(n)) \le \exp(-\log^c(n)).$$

for all sufficiently large n. We will use (3.2) with  $c = \frac{5}{4}$  or c = 2. The following Poisson approximation will be used throughout.

LEMMA 3.1. Let  $\{W_i\}_{i=1}^m$  be i.i.d. from a distribution taking three values a, b, c and  $\mathbb{P}(W_i = a) = \alpha p$ ,  $\mathbb{P}(W_i = b) = \alpha(1 - p)$ , and  $\mathbb{P}(W_i = c) = 1 - \alpha$ . Let  $N_x := \#\{i : W_i = x\}$  for x = a, b, c. If  $m_1, m_2 = o(\log^{3/2} n)$ ,  $m = \frac{n}{2}(1 + O(\log^{-2} n))$  and  $\alpha = t \log n/n$ , then

$$M(m, m_1, m_2, p) := \mathbb{P}(N_a = m_1, N_b = m_2) \times P\left(\frac{tp \log n}{2}; m_1\right) P\left(\frac{t(1-p) \log n}{2}; m_2\right),$$

where  $P(\lambda; m)$  is the probability that a Poisson( $\lambda$ ) random variable takes value m.

The proof follows using Stirling's approximation; we provide the details in Appendix B.

# <span id="page-6-1"></span>4 Impossibility of exact recovery

In this section, we give the proof of Theorem 2.1. We first identify a sufficient condition under which any algorithm fails to achieve exact recovery (Proposition 4.1). The condition captures the idea that there are some graph instances that cannot be labeled correctly with confidence since there are multiple suitable labelings for these instances. If these graph instances are likely to occur, then the overall failure probability can be lower-bounded. Theorem 2.1 is then proven by finding a set of graphs that are difficult to label correctly.

**4.1 Sufficient condition for impossibility.** Recall that  $S = \{\pm 1\}^n$  is the space of possible values of  $\sigma$ . We write g as a generic notation to denote the observed value of the edge-labeled graph G consisting of present, absent and censored edges. Also, let  $\mathcal{G}$  be the space of all possible values of G. We write  $\mathbb{P}(\cdot|\sigma)$  to denote the probability distribution of  $\mathrm{CSBM}(p,q,t)$  when the community assignments are given by  $\sigma$ .

Since

$$\mathbb{P}(\hat{\sigma} \neq \sigma_0) = \sum_{g \in \mathcal{G}} \mathbb{P}(\hat{\sigma} \neq \sigma_0 \mid G = g) \mathbb{P}(G = g),$$

the estimator that maximizes the posterior probability  $\mathbb{P}(\hat{\sigma} = \sigma_0 \mid G = g)$  for all  $g \in \mathcal{G}$  also minimizes the error probability  $\mathbb{P}(\hat{\sigma} \neq \sigma_0)$ . This estimator is the Maximum A Posteriori (MAP) estimator. Thus, an optimal algorithm is devised by choosing uniformly at random among all MAP estimates, and we denote the corresponding estimator by  $\hat{\sigma}_{MAP}$ . Next, using the fact that  $\sigma_0$  is uniformly distributed on  $\mathcal{S}$ , we must have  $\mathbb{P}(\sigma_0 = \sigma | G = g) \propto \mathbb{P}(G = g | \sigma_0 = \sigma)$ . Then,

<span id="page-7-1"></span>(4.1) 
$$\operatorname*{argmax}_{\sigma} \mathbb{P} \left( \sigma_{0} = \sigma \mid G = g \right) = \operatorname*{argmax}_{\sigma} \mathbb{P} \left( G = g \mid \sigma_{0} = \sigma \right),$$

i.e., the MAP estimator coincides with the Maximum Likelihood estimator.

<span id="page-7-0"></span>In light of this equivalence, the following result identifies a condition where the MAP estimator fails with a given probability.

PROPOSITION 4.1. Fix  $\delta > 0$ . Suppose that there is  $\mathcal{G}' \subset \mathcal{G}$  with  $\mathbb{P}(G \in \mathcal{G}'|\sigma_0) \geq \delta$  such that the following holds for any  $g \in \mathcal{G}'$ : There are k pairs of vertices  $\{(u_i, v_i) : i \in [k]\}$  with opposite community label such that if  $\sigma'_0$  is obtained by swapping any one of the labels of  $u_i$  and  $v_i$ , then  $\mathbb{P}(G = g|\sigma_0) = \mathbb{P}(G = g|\sigma'_0)$ . Then, conditionally on  $\sigma_0$ , the MAP estimator  $\hat{\sigma}_{MAP}$  fails in exact recovery with probability at least  $\delta(1 - \frac{1}{k})$ .

*Proof.* By our underlying condition, whenever  $g \in \mathcal{G}'$ , the true assignment is such that swapping one of the community assignment of one of the pairs among  $\{(u_i, v_i) : i \in [k]\}$  results in an equiprobable assignment. In that case, the algorithm is incorrect with probability at least  $1 - \frac{1}{k}$ , due to (4.1). Therefore,

$$(4.2) \qquad \mathbb{P}(\hat{\sigma}_{\text{MAP}} \neq \sigma_0 \mid \sigma_0) \geq \mathbb{P}(\hat{\sigma}_{\text{MAP}} \neq \sigma_0 \mid G \in \mathcal{G}', \sigma_0) \mathbb{P}(G \in \mathcal{G}' \mid \sigma_0) \geq \delta \left(1 - \frac{1}{k}\right),$$

and the proof follows.

<span id="page-7-2"></span>REMARK 4.1. Additionally, Proposition 4.1 holds when  $\sigma_0$  is an assignment with equal community sizes, i.e.,  $n_1(\sigma_0) = n_2(\sigma_0)$ . In this case, observe that we can treat the assignment  $\sigma_0$  as though it were chosen uniformly at random from all  $\sigma$  satisfying  $n_1(\sigma) = n_2(\sigma)$ . To see this, consider applying a uniformly chosen random permutation to the vertices. The inference problem does not change; however, the MAP estimator again coincides with the Maximum Likelihood estimator, and one can use an identical argument as above.

### 4.2 Proof of impossibility of exact recovery

Proof. (Proof of Theorem 2.1). Throughout the proof, we condition on  $\sigma_0 \in \mathcal{S}$  such that  $n_1(\sigma_0), n_2(\sigma_0) = (1 + O(n^{-1/3}))\frac{n}{2}$ , which occurs with probability at least  $1 - 2\exp(-n^{1/3}/6)$  by (3.1). For convenience, we write  $n_1, n_2$  instead of  $n_1(\sigma_0), n_2(\sigma_0)$ . We will show that with high probability, there exist  $k = \omega(1)$  pairs of vertices  $\{(u_i, v_i) : i \in [k]\}$  with opposite communities such that swapping their labels results in an equiprobable graph instance. By Proposition 4.1, this would show that exact recovery fails with probability 1 - o(1) for any algorithm.

For j=1,2, let  $S_j$  be sets of  $\lfloor 2n_j/\log^2(n)\rfloor \asymp \lfloor n/\log^2(n)\rfloor$  randomly selected vertices from Community 1 and Community 2, respectively. Let  $S=S_1\cup S_2$ . Next, let S' be the set of all vertices in S whose connections to all other vertices in S are censored. We claim that  $|S'|>3n/2\log^2(n)$  with probability 1-o(1). To see this, observe that the expected number of revealed connections between vertices in S is at most  $\alpha(2n/\log^2(n))^2=4tn/\log^3(n)$ , so with high probability there are fewer than  $n/4\log^2(n)$  such connections. Therefore with high probability there are fewer than  $\lfloor n/2\log^2(n)\rfloor$  vertices with at least one neighbor in S, from which the claim follows.

Now, let  $m = \lfloor \sqrt{pq}t \log(n)/2 \rfloor$ ,  $m' = \lfloor \sqrt{(1-p)(1-q)}t \log(n)/2 \rfloor$ , and m'' = m+m'. Let  $\overline{p}_1$  be the probability that a vertex v in Community 1 has exactly m present edges and m' absent edges to vertices in each community, conditioned on  $v \in S'$ . By Lemma 3.1, we have

$$\overline{p}_1 = M(n_1 - \lfloor 2n_1/\log^2(n) \rfloor, m, m', p) \times M(n_2 - \lfloor 2n_2/\log^2(n) \rfloor, m, m', q)$$

$$\begin{split} & \approx \mathrm{e}^{-t\log n} \frac{\left(\frac{t^2pq\log^2 n}{4}\right)^m \left(\frac{t^2(1-p)(1-q)\log^2 n}{4}\right)^{m'}}{(m!)^2(m'!)^2} \\ & \approx n^{-t} \frac{\left(\frac{t^2pq\log^2 n}{4}\right)^m \left(\frac{t^2(1-p)(1-q)\log^2 n}{4}\right)^{m'}}{(2\pi)^2 \mathrm{e}^{-2m} m^{2m+1} \mathrm{e}^{-2m'} (m')^{2m'+1}} \\ & = \frac{n^{-t}}{4\pi^2 mm'} \mathrm{e}^{2m+2m'} \left(\frac{t^2pq\log^2 n}{4m^2}\right)^m \left(\frac{t^2(1-p)(1-q)\log^2 n}{4m'^2}\right)^{m'} \\ & \approx n^{-t} n^{\sqrt{pq}t + \sqrt{(1-p)(1-q)t}} \\ & = n^{-\left(\sqrt{p} - \sqrt{q}\right)^2 t/2 - \left(\sqrt{1-p} - \sqrt{1-q}\right)^2 t/2}. \end{split}$$

This implies that  $\overline{p}_1 = \omega(\log^2(n)/n)$  because  $[(\sqrt{p} - \sqrt{q})^2 + (\sqrt{1-p} - \sqrt{1-q})^2]t/2 < 1$  since  $t < t_c(p,q)$ . Repeating the calculation for the case that v is in Community 2, we conclude that the probability  $\overline{p}_2$  that a given vertex  $v \in S'$  has exactly m present edges and m' absent edges to vertices in each community is  $\omega(\log^2(n)/n)$ .

For  $v \in S'$ , let Y(v) be the indicator that v has exactly m present edges and m' absent edges to each community. Note that the random variables in the set  $\{Y(v)\}_{v \in S'}$  are mutually independent conditionally on S'. Finally, observe that if  $u \in S' \cap S_1$  and  $v \in S' \cap S_2$  satisfy Y(u) = Y(v) = 1, then switching the community labels of u and v results in an equiprobable outcome.

Let

$$Y_1 = \sum_{v \in S' \cap S_1} Y(v) \quad \text{and} \quad Y_2 = \sum_{v \in S' \cap S_2} Y(v).$$

It suffices to show that there is a function  $f(n) = \omega(1)$  such that  $Y_1, Y_2 \ge f(n)$  with probability 1 - o(1). We prove the claim for  $Y_1$ , and the proof for  $Y_2$  follows similary. Observe that conditioning on  $|S' \cap S_1|$ ,

$$\mathbb{E}[Y_1 \mid |S' \cap S_1|] = |S' \cap S_1| \cdot \overline{p}_1.$$

Fix  $\varepsilon > 0$ . By Chebyshev's inequality,

$$\mathbb{P}\left(Y_1 \leq (1-\varepsilon)|S' \cap S_1| \cdot \overline{p}_1 \mid |S' \cap S_1| = s\right) \leq \frac{\operatorname{Var}\left(Y_1 \mid |S' \cap S_1| = s\right)}{\varepsilon^2 s^2 \overline{p}_1^2} \leq \frac{s\overline{p}_1(1-\overline{p}_1)}{\varepsilon^2 s^2 \overline{p}_1^2} \leq \frac{1}{\varepsilon^2 s\overline{p}_1}.$$

Recall that  $|S'| > \frac{3n}{2\log^2(n)}$  with probability 1 - o(1). Therefore, using  $|S_2| = \lfloor n/\log^2 n \rfloor$ , we have  $|S' \cap S_1| > \frac{n}{2\log^2(n)}$  with probability 1 - o(1). We conclude that

$$\mathbb{P}\left(Y_1 \leq (1-\varepsilon)\frac{n}{2\log^2(n)}\overline{p}_1\right) \leq \mathbb{P}\left(Y_1 \leq (1-\varepsilon)|S' \cap S_1| \cdot \overline{p}_1 \mid |S' \cap S_1| > \frac{n}{2\log^2(n)}\right) + o(1)$$

$$\leq \frac{2\log^2(n)}{\varepsilon^2\overline{p}_1 n} + o(1).$$

Recalling that  $\overline{p}_1 = \omega(\log^2(n)/n)$ , we have shown that there is a function  $f(n) = \omega(1)$  such that  $\mathbb{P}(Y_1 \leq f(n)) = o(1)$ . Similarly, using  $\overline{p}_2 = \omega(\log^2(n)/n)$ , it holds that  $\mathbb{P}(Y_2 \leq f(n)) = o(1)$ . Applying Proposition 4.1 with  $\delta = 1 - o(1)$  and  $k = (f(n))^2$  completes the proof.

Remark 4.2. We could generalize this to an argument that recovery is impossible whenever  $t < t_c(p_1, p_2, q)$  by arguing that there will be vertices with degree profiles of

$$\left(\lfloor p_1^x q^{1-x} t \log(n)/2 \rfloor, \lfloor (1-p_1)^x (1-q)^{1-x} t \log(n)/2 \rfloor, \lfloor p_2^{1-x} q^x t \log(n)/2 \rfloor, \lfloor (1-p_2)^{1-x} (1-q)^x t \log(n)/2 \rfloor\right)$$

in both communities, where x takes on the value used in the computation of  $t_c(p_1, p_2, q)$ . The argument that this holds is largely analogous to that in the proof above, although one needs to use the fact that the criterion used to choose x implies that vertices in each community are approximately equally likely to have this community profile and then bound both probabilities by bounding the weighted geometric means of their obvious formulations with weights x and 1-x.

#### <span id="page-9-1"></span>5 Analysis of the spectral algorithm

Recall the signed adjacency matrix from Section 2.2. The key to establishing Theorem 2.2 is the method of entrywise eigenvector analysis of [4]. Let us denote  $A^* = \mathbb{E}[A \mid \sigma_0]$ , and let  $(u_k^*, \lambda_k^*)$  denote the k-th eigenvector-eigenvalue pair of  $A^*$ , where  $(\lambda_k^*)_k$  are arranged in non-decreasing order. Abbe et. al. [4] show that, under a set of general conditions,  $u_k \approx A u_k^* / \lambda_k^*$  in the  $\ell_{\infty}$ -norm. Results of this kind were also derived recently by Lei [13]. Thus, if we can show that the signs of  $A u_1^* / \lambda_1^*$  recover the communities with high probability (up to a global flip), and the magnitude of its entries are bounded away from zero, then the signs of  $u_1$  also recover the communities with high probability. More precisely, using the methods of [4, Theorem 2.1], we will establish the following result:

PROPOSITION 5.1. With probability  $1 - O(n^{-3})$  we have

<span id="page-9-3"></span><span id="page-9-0"></span>
$$\min_{s \in \{\pm 1\}} \left\| u_k - s \frac{A u_k^{\star}}{\lambda_k^{\star}} \right\|_{\infty} \le \frac{C}{\sqrt{n} \log \log n}$$

for  $k \in \{1, 2\}$ , where C = C(p, q, t) is a constant depending only on p, q, and t.

In Section 5.1, we will provide a main result of [4], specialized to our setting. In Section 5.2, we prove Proposition 5.1. With this result in hand, we provide the proof of Theorem 2.2 in Section 5.3.

<span id="page-9-2"></span>5.1 Prior work on entrywise eigenvector analysis. We start by reproducing [4, Theorem 2.1], specialized to the case where  $A^*$  is a rank-2 matrix and we wish to approximate a single eigenvector.

THEOREM 5.1. ([4, Theorem 2.1]). Let A be a symmetric random matrix and  $A^* = \mathbb{E}[A]$ . Suppose that the following conditions hold with some  $\gamma \in \mathbb{R}$  and  $\varphi : \mathbb{R} \to \mathbb{R}$ :

- <span id="page-9-5"></span>(i) (Incoherence)  $||A^{\star}||_{2\to\infty} \leq \gamma \Delta^{\star}$ , where  $\Delta^{\star} = (\lambda_1^{\star} - \lambda_2^{\star}) \wedge |\lambda_1^{\star}|$  and  $\gamma > 0$ .
- <span id="page-9-6"></span>(ii) (Row- and column-wise independence) For any  $m \in [n]$ , the entries in the m-th row and column of A are independent with others.
- <span id="page-9-8"></span>(iii) (Row concentration) Suppose  $\varphi(x)$  is continuous and non-decreasing in  $\mathbb{R}_+$  with  $\varphi(0) = 0$ ,  $\varphi(x)/x$  is non-increasing in  $\mathbb{R}_+$ , and  $\delta_1 \in (0,1)$ . For any  $m \in [n]$  and  $w \in \mathbb{R}^n$ ,

$$\mathbb{P}\left(|(A - A^*)_{m \cdot w}| \le \Delta^* \|w\|_{\infty} \varphi\left(\frac{\|w\|_2}{\sqrt{n} \|w\|_{\infty}}\right)\right) \ge 1 - \frac{\delta_1}{n}.$$

<span id="page-9-7"></span>(iv) (Spectral norm concentration) Let  $\kappa = |\lambda_1^{\star}|/\Delta^{\star}$ . Suppose  $32\kappa \max\{\gamma, \varphi(\gamma)\} \le 1$  and for some  $\delta_0 \in (0, 1)$ ,  $\mathbb{P}(\|A - A^{\star}\|_2 \le \gamma \Delta^{\star}) \ge 1 - \delta_0.$ 

Then with probability at least  $1 - \delta_0 - 2\delta_1$ ,

<span id="page-9-4"></span>
$$\min_{s \in \{\pm 1\}} \left\| u_k - s \frac{A u_k^{\star}}{\lambda_k^{\star}} \right\|_{\infty} \lesssim \kappa \left( \kappa + \varphi(1) \right) \left( \gamma + \varphi(\gamma) \right) \| u_1^{\star} \|_{\infty} + \gamma \frac{\|A^{\star}\|_{2 \to \infty}}{\Delta^{\star}}$$

for  $k \in \{1, 2\}$ , where  $\leq$  hides an absolute constant.

Next, we state the following two lemmas to verify the final two conditions in Theorem 5.1. The first is similar to [10, Theorem 9].

Lemma 5.1. There exists  $c_1 = c_1(p,q,t) > 0$  such that

<span id="page-9-9"></span>
$$\mathbb{P}\left(\|A - A^*\|_2 \ge c_1 \sqrt{\log(n)}\right) \le n^{-3}.$$

The following lemma is similar to [4, Lemma 7].

LEMMA 5.2. Let  $w \in \mathbb{R}^n$  be a fixed vector,  $\{X_i\}_{i=1}^n$  be independent random variables where  $\mathbb{P}(X_i = 1) = p_i$ ,  $\mathbb{P}(X_i = -y) = q_i$ , and  $\mathbb{P}(X_i = 0) = 1 - p_i - q_i$ . Let  $\beta \geq 0$ . Then

$$\mathbb{P}\left(\left|\sum_{i=1}^{n} w_{i} \left(X_{i} - \mathbb{E}[X_{i}]\right)\right| \geq \frac{\max\{1, y\}(2 + \beta)n}{1 \vee \log\left(\frac{\sqrt{n}\|w\|_{\infty}}{\|w\|_{2}}\right)} \|w\|_{\infty} \max_{i}\{p_{i} + q_{i}\}\right) \leq 2 \exp\left(-\beta n \max_{i}\{p_{i} + q_{i}\}\right).$$

The proofs of the above lemmas will be provided in Appendix A.

<span id="page-10-0"></span>**5.2** Proof of eigenvector approximation result. We start by determining the eigenvalues and eigenvectors of  $A^* = \mathbb{E}[A \mid \sigma_0]$ .

LEMMA 5.3. If  $n_1(\sigma_0), n_2(\sigma_0) \ge 1$ , then  $A^*$  has rank 2. If p > q, then with probability at least  $1 - 2 \exp(-n^{1/3}/6)$ , the eigenvalues of  $A^*$  are given by

<span id="page-10-1"></span>
$$\lambda_{1}^{\star} = \frac{(1+o(1))t\log n}{2\log\left(\frac{p}{q}\right)}\left(D_{\mathrm{KL}}\left(p\|q\right) + D_{\mathrm{KL}}\left(q\|p\right)\right), \quad \lambda_{2}^{\star} = \frac{(1+o(1))t\log n}{2\log\left(\frac{p}{q}\right)}\left(D_{\mathrm{KL}}\left(p\|q\right) - D_{\mathrm{KL}}\left(q\|p\right)\right)$$

and the corresponding eigenvectors  $u_1^*$  and  $u_2^*$  are respectively given by  $(u_1^*)_i = \frac{1+o(1)}{\sqrt{n}}$  if  $\sigma_0(i) = +1$ ,  $(u_1^*)_i = -\frac{1+o(1)}{\sqrt{n}}$  if  $\sigma_0(i) = -1$ , and the other eigenvector has  $(u_2^*)_i = \frac{1}{\sqrt{n}}$  for all i.

*Proof.* Recall the edges are revealed independently with probability  $\alpha = t \log n/n$ . Thus, for i, j such that  $\sigma_0(i) = \sigma_0(j)$ ,

<span id="page-10-2"></span>(5.1) 
$$A_{ij}^{\star} = \alpha \left( p - \frac{\log\left(\frac{1-q}{1-p}\right)}{\log\left(\frac{p}{q}\right)} (1-p) \right) = \frac{t \log n}{n \log\left(\frac{p}{q}\right)} D_{\text{KL}}(p||q),$$

and similarly, for  $\sigma_0(i) \neq \sigma_0(j)$ ,

<span id="page-10-3"></span>
$$A_{ij}^{\star} = \alpha \left( q - \frac{\log\left(\frac{1-q}{1-p}\right)}{\log\left(\frac{p}{q}\right)} (1-q) \right) = -\frac{t \log n}{n \log\left(\frac{p}{q}\right)} D_{\text{KL}}(q||p).$$

If  $n_1(\sigma_0) = n_2(\sigma_0) = \frac{n}{2}$ , it follows that

$$\lambda_{1}^{\star} = \frac{t \log n}{2 \log \left(\frac{p}{q}\right)} \left(D_{\text{\tiny KL}}\left(p \| q\right) + D_{\text{\tiny KL}}\left(q \| p\right)\right), \quad \lambda_{2}^{\star} = \frac{t \log n}{2 \log \left(\frac{p}{q}\right)} \left(D_{\text{\tiny KL}}\left(p \| q\right) - D_{\text{\tiny KL}}\left(q \| p\right)\right)$$

By (3.1) with e.g.  $\varepsilon = n^{-\frac{1}{3}}$ , we have that  $n_1(\sigma_0), n_2(\sigma_0) = (1 + o(1))n/2$  with probability at least  $1 - 2\exp(-n^{1/3}/6)$ . We now consider what happens to the eigenvalues of  $A^*$  when  $n_1(\sigma_0), n_2(\sigma_0)$  are perturbed.

More generally, let  $Z(a_1, a_2, b_1, b_2)$  denote an  $n \times n$  block matrix with blocks of size  $b_1 n$  and  $b_2 n$ , where the diagonal blocks take value  $a_1$  and the off-diagonal blocks take value  $a_2$ . Let  $\lambda$  be an eigenvalue of  $Z(a_1, a_2, b_1, b_2)$  and let  $\lambda'$  be the corresponding eigenvalue of  $Z(a_1, a_2, b'_1, b'_2)$ . Let  $E = Z(a_1, a_2, b'_1, b'_2) - Z(a_1, a_2, b_1, b_2)$ . By Weyl's inequality,

$$|\lambda - \lambda'| \le ||E||_2 \le ||E||_F \le \sqrt{(a_1 - a_2)^2 (|b_1 - b_1'| + |b_2 - b_2'|) n} = |a_1 - a_2| \sqrt{2|b_1 - b_1'| n}.$$

In particular, if  $\lambda = \Theta(\log(n))$ ,  $a_1, a_2 = \Theta(\frac{\log(n)}{n})$ , and  $|b_1' - b_1| = o(n)$ , then  $\lambda' = (1 + o(1))\lambda$ . We conclude that when  $n_1(\sigma_0), n_2(\sigma_0) = (1 + o(1))n/2$ , the eigenvalues of  $A^*$  are the same as the even communities case up to a 1 + o(1) factor.

Regarding the eigenvector  $u_1^*$ , its entries are given by  $\pm \frac{1}{\sqrt{n}}$  depending on community membership, in the case of  $n_1(\sigma_0) = n_2(\sigma_0) = n/2$ . When  $n_1(\sigma_0), n_2(\sigma_0) = (1 + o(1))n/2$ , then determining the entries of the eigenvector  $u_{1,i}^* \in \{x_1, x_2\}$  requires solving a system of the form

$$\begin{cases} n_1(\sigma_0)a_1x_1 + n_2(\sigma_0)a_2x_2 = \lambda_1x_1 \\ n_1(\sigma_0)a_2x_1 + n_2(\sigma_0)a_1x_2 = \lambda_1x_2 \end{cases}$$

Since  $n_1(\sigma_0), n_2(\sigma_0) = (1 + o(1))n/2$  and  $\lambda_1 = (1 + o(1))\lambda_1^*$ , the coefficients of the system are perturbed by a factor 1 + o(1) relative to the equal-sized communities case. Therefore, the eigenvector entries are also perturbed within a 1 + o(1) factor.  $\Box$ 

*Proof.* (Proof of Proposition 5.1). We will apply Theorem 5.1 by verifying its conditions. In this proof, we avoid writing the (1 + o(1)) terms for  $\lambda_1^{\star}, \lambda_2^{\star}$  in Lemma 5.3 since that does not affect the asymptotic computations. We give the proof first for the case p > q. By Lemma 5.3, it follows that

$$\Delta^{\star} = \lambda_1^{\star} - \lambda_2^{\star} = \frac{D_{\mathrm{KL}}\left(q\|p\right)}{\log\left(\frac{p}{q}\right)} t \log n \quad \text{and} \quad \kappa = \frac{D_{\mathrm{KL}}\left(p\|q\right) + D_{\mathrm{KL}}\left(q\|p\right)}{2D_{\mathrm{KL}}\left(q\|p\right)}.$$

Let

$$\gamma = \frac{c_1 \log \left(\frac{p}{q}\right)}{D_{\text{KL}}(q||p)t\sqrt{\log(n)}},$$

where  $c_1$  is the value from Lemma 5.1. Let

$$\varphi(x) = \frac{\max\{1,y\} \left(2t+4\right) \log \left(\frac{p}{q}\right)}{t D_{\mathrm{KL}}(q \| p)} \bigg(1 \vee \log \left(\frac{1}{x}\right)\bigg)^{-1}.$$

To check Condition (i), recall that  $||A^{\star}||_{2\to\infty} = \max_i ||A^{\star}_{i}||_2$ . Thus, by (5.1) and (5.2),

$$||A^{\star}||_{2\to\infty} \le \frac{t\log n}{\sqrt{n}\log\left(\frac{p}{q}\right)} \max\{D_{\text{KL}}(p||q), D_{\text{KL}}(q||p)\}.$$

On the other hand,  $\gamma \Delta^* = c_1 \sqrt{\log(n)}$ . Condition (i) therefore holds for n large enough. Condition (ii) holds since the entries  $\{A_{ij} : i \leq j\}$  are independent conditioned on the communities. The first requirement of Condition (iv) is satisfied for n sufficiently large since  $\gamma \to 0$  as  $n \to \infty$ ,  $\lim_{x\to 0} \varphi(x) = 0$  and  $\kappa = \Theta(1)$ . The second requirement is satisfied by Lemma 5.1, with  $\delta_0 = n^{-3}$ . Finally, to verify Condition (iii), fix m, and apply Lemma 5.2 with  $X_i = A_{mi}$ , and setting  $\beta = \frac{4}{t}$ . Note that  $p_i$  equals  $\alpha p$  or  $\alpha q$  depending on whether  $\sigma_0(i) = \sigma_0(m)$  or not, and let  $q_i = \alpha - p_i$  which equals to either  $\alpha(1-p)$  or  $\alpha(1-q)$ . Thus,  $\max_i(p_i + q_i) = \alpha$ . Then

$$\mathbb{P}\bigg(|(A - A^*)_m \cdot w| \le \frac{\max\{1, y\}(2t + 4)\log(n)}{1 \vee \log\left(\frac{\sqrt{n}||w||_{\infty}}{||w||_{2}}\right)} ||w||_{\infty}\bigg) \ge 1 - 2n^{-4}.$$

Observing

$$\frac{\max\{1,y\}(2t+4)\log(n)}{1\vee\log\left(\frac{\sqrt{n}\|w\|_{\infty}}{\|w\|_2}\right)}\|w\|_{\infty}=\Delta^{\star}\|w\|_{\infty}\varphi\left(\frac{\|w\|_2}{\sqrt{n}\|w\|_{\infty}}\right),$$

Condition (iii) holds with  $\delta_1 = 2n^{-3}$ . Applying Theorem 5.1, with probability at least  $1 - 5n^{-3}$ ,

<span id="page-11-1"></span>
$$\min_{s \in \{\pm 1\}} \left\| u_1 - s \frac{A u_1^*}{\lambda_2^*} \right\|_{\infty} \le \frac{C}{\sqrt{n} \log \log n},$$

where C depends only on p, q, and t.

In the case p < q, we replace A by -A. Replacing all instances of  $\log(p/q)$  by  $\log(q/p)$ , the proof follows verbatim.  $\square$ 

<span id="page-11-0"></span>**5.3** Success of the spectral algorithm. We will use the following concentration result which can be proved analogously to the Chernoff bound. The proof of this lemma is provided in Appendix A.

LEMMA 5.4. Let p, q, t be constants such that p > q and  $\alpha = t \log n/n$ . Suppose  $n_1, n_2 = (1 + o(1)) \frac{n}{2}$ . Let  $\{W_i\}_{i=1}^{n_1}$  be i.i.d. where  $\mathbb{P}(W_i = 1) = \alpha p$ ,  $\mathbb{P}(W_i = -y) = \alpha(1 - p)$ , and  $\mathbb{P}(W_i = 0) = 1 - \alpha$  and y is given by (2.3). Let  $\{Z_i\}_{i=1}^{n_2}$  be i.i.d. where  $\mathbb{P}(Z_i = 1) = \alpha q$ ,  $\mathbb{P}(Z_i = -y) = \alpha(1 - q)$ , and  $\mathbb{P}(Z_i = 0) = 1 - \alpha$ , independent of the  $W_i$ 's. For any  $\varepsilon \geq 0$ , we have the following:

$$\log \mathbb{P}\left(\sum_{i=1}^{n_1} W_i - \sum_{i=1}^{n_2} Z_i \le \varepsilon \log(n)\right)$$

$$\le \log(n) \left[ -\lambda \varepsilon - \frac{t}{2} \left( \left(\sqrt{p} - \sqrt{q}\right)^2 + \left(\sqrt{1-q} - \sqrt{1-p}\right)^2 \right) + o(1) \right].$$

*Proof.* (Proof of Theorem 2.2). Consider the case p > q. Let

$$C_n := \left\{ \left| n_1(\sigma_0) - \frac{n}{2} \right| \le n^{\frac{2}{3}}, \left| n_2(\sigma_0) - \frac{n}{2} \right| \le n^{\frac{2}{3}} \right\}.$$

Note that  $\mathbb{P}(\mathcal{C}_n^c) = o(1)$ , and indeed is much smaller. Therefore, it is sufficient to analyze events conditioned on  $\mathcal{C}_n$ . For any labeling  $\sigma$ , define  $J_i(\sigma) := \{j \in [n] \setminus \{i\} : \sigma(j) = +1\}$ . Let  $s \in \{\pm 1\}$  be such that  $\|u_1 - sAu_1^{\star}/\lambda_1^{\star}\|_{\infty}$  is minimized. Then, by Proposition 5.1, with probability 1 - o(1),

(5.3) 
$$\sqrt{n} \min_{i \in [n]} s\sigma_0(i)(u_1)_i \ge \sqrt{n} \min_{i \in [n]} \sigma_0(i) \frac{(Au_1^*)_i}{\lambda_1^*} - C(\log \log n)^{-1},$$

where we have used  $s^2 = 1$ . We now show that  $\sigma_0(i) \frac{(Au_1^*)_i}{\lambda_1^*}$  is bounded away from zero. By Lemma 5.3,  $(u_1^*)_i$  takes values  $\frac{(1+o(1))}{\sqrt{n}}$  or  $-\frac{(1+o(1))}{\sqrt{n}}$  depending on  $\sigma_0(i)$ , conditioned on  $\mathcal{C}_n$ . Thus, for each i,

<span id="page-12-3"></span><span id="page-12-2"></span>
$$\sigma_0(i) \frac{(Au_1^{\star})_i}{\lambda_1^{\star}} = \frac{2(1+o(1))\log\left(\frac{p}{q}\right)}{t\left(D_{\mathrm{KL}}(p\|q) + D_{\mathrm{KL}}(q\|p)\right)\sqrt{n}\log(n)} \bigg(\sum_{j \in J_i(\sigma_0)} A_{ij} - \sum_{j \notin J_i(\sigma_0)} A_{ij}\bigg).$$

Observe that for  $\varepsilon > 0$ ,

(5.4) 
$$\mathbb{P}\left(\sqrt{n}\sigma_{0}(i)\frac{(Au_{1}^{\star})_{i}}{\lambda_{1}^{\star}} \leq \frac{2\varepsilon\log\left(\frac{p}{q}\right)}{t\left(D_{\mathrm{KL}}(p\|q) + D_{\mathrm{KL}}(q\|p)\right)} \mid \mathcal{C}_{n}\right)$$

$$= \mathbb{P}\left(\sum_{j\in J_{i}(\sigma_{0})} A_{ij} - \sum_{j\notin J_{i}(\sigma_{0})} A_{ij} \leq \varepsilon\log(n) \mid \mathcal{C}_{n}\right).$$

By Lemma 5.4, if we have  $t > t_c(p,q)$  with  $t_c(p,q)$  given by (2.2), then there exists  $\varepsilon > 0$  so that

$$\mathbb{P}\bigg(\sum_{j\in J_i(\sigma_0)} A_{ij} - \sum_{j\notin J_i(\sigma_0)} A_{ij} \le \varepsilon \log(n) \mid \mathcal{C}_n\bigg) = o\bigg(\frac{1}{n}\bigg).$$

By a union bound and using (5.3), we conclude that there exists  $\eta = \eta(p,q) > 0$  such that with probability 1 - o(1),

(5.5) 
$$\sqrt{n} \min_{i \in [n]} s\sigma_0(i)(u_1)_i \ge \eta.$$

In the case p < q, we replace A by -A, and the proof follows verbatim.  $\Box$ 

REMARK 5.1. Note that Theorem 2.1 applies to the model considered by Hajek et. al. [10], where  $n_1 = n_2 = \frac{n}{2}$  (due to Remark 4.1). Additionally, the success of the spectral algorithm (Theorem 2.2) holds for this model. Therefore, Theorems 2.1 and 2.2 are directly comparable to [10] in the special case p + q = 1.

# <span id="page-12-1"></span>6 Asymptotic error of the genie estimator

In this section, we complete the proof of Theorem 2.3. In order to analyze the genie estimator, we first use the fact that the prior on  $\sigma_0(u)$  is uniform, so that

<span id="page-12-4"></span><span id="page-12-0"></span>
$$\hat{\sigma}_{\text{Best}}(u) = \operatorname*{argmax}_{r \in \{\pm 1\}} \mathbb{P}(G \mid \sigma_0(u) = r, (\sigma_0(v))_{v \in [n] \setminus \{u\}}).$$

In other words, the genie estimator may be interpreted as a Maximum Likelihood Estimator. Recall  $\Gamma(u, \sigma, p_1, p_2, q)$  from (2.6) and the notation  $D = D(\sigma, u) = (D_i(\sigma, u))_{i=1}^4$  for the degree profile from Section 2.3. We first derive an expression for the genie estimator for general CSBM with possibly arbitrary choices of  $p_1, p_2$ . This result will also be useful in the next section.

PROPOSITION 6.1. For any  $p_1, p_2, q \in (0, 1)$ , we have for all  $u \in [n]$ 

(6.1) 
$$\hat{\sigma}_{\text{Best}}(u) = \begin{cases} +1 & \text{if } \Gamma(u, \sigma_0, p_1, p_2, q) \ge 0\\ -1 & \text{otherwise.} \end{cases}$$

The proof is provided in Appendix C. In other words, the genie estimator decides community assignments based on the sign of a linear combination of the degree profiles. For  $p_1 = p_2 = p$ , it is not difficult to see that if y is given by (2.3), then we get the following cleaner expression in terms of the signed adjacency matrix:

(6.2) 
$$\Gamma(u, \sigma, p, p, q) = \left(\sum_{v \in J_u(\sigma)} A_{ij} - \sum_{v \notin J_u(\sigma)} A_{ij}\right) \log \frac{p}{q},$$

where  $J_u(\sigma) := \{v \in [n] \setminus \{u\} : \sigma(v) = +1\}$ . Thus, we see that in the symmetric case, the genie estimator decides the communities based on the sign of  $\sum_{v \in J_u(\sigma)} A_{ij} - \sum_{v \notin J_u(\sigma)} A_{ij}$ . From the proof of Theorem 2.2, we see that the spectral algorithm recovers  $\sigma_0(u)$  successfully if  $\sum_{v \in J_u(\sigma_0)} A_{ij} - \sum_{v \notin J_u(\sigma_0)} A_{ij} \ge \varepsilon \log n$  when p > q and  $\sum_{v \in J_u(\sigma_0)} A_{ij} - \sum_{v \notin J_u(\sigma_0)} A_{ij} \le -\varepsilon \log n$  when p < q where  $\varepsilon = o(1)$  (see (5.4)). Thus it intuitively makes sense that the error rates of  $\hat{\sigma}_{\text{Spec}}$  and  $\hat{\sigma}_{\text{Best}}$  should be close.

We proceed with an error analysis of the genie-based estimator in Section 6.1, which will be used to complete the proof of Theorem 2.3 in Section 6.2

<span id="page-13-0"></span>6.1 Error analysis of the genie-based estimator. Next we analyze the error rate of the genie-based estimator  $\hat{\sigma}_{\text{Best}}$ . Recall the error rate  $\text{Err}(\cdot)$  from (2.4) and  $t_c(p_1, p_2, q)$  from (2.8).

LEMMA 6.1.  $\operatorname{Err}(\hat{\sigma}_{\text{Best}}) = n^{-(1+o(1))t/t_c(p_1, p_2, q)}$ 

*Proof.* Let  $X := \frac{1}{n} \sum_{i \in [n]} \mathbb{1}_{\{\hat{\sigma}_{Best}(i) \neq \sigma_0(i)\}}$ . Then  $Err(\hat{\sigma}_{Best}) = \mathbb{E}[\min\{X, 1 - X\}]$ . Note that, since  $0 \le X \le 1$  almost surely, we have

<span id="page-13-1"></span>
$$\mathbb{E}[X] - \mathbb{E}[\min\{X, 1 - X\}] \le \mathbb{P}\left(X > \frac{1}{2}\right).$$

Therefore,

$$\mathbb{E}[X] - \mathbb{P}\left(X > \frac{1}{2}\right) \le \operatorname{Err}(\hat{\sigma}_{\text{\tiny Best}}) = \mathbb{E}[\min\{X, 1 - X\}] \le \mathbb{E}[X].$$

It suffices to show that  $\mathbb{E}[X] = n^{-(1+o(1))t/t_c(p_1,p_2,q)}$  and  $\mathbb{P}(X > 1/2) = o(\mathbb{E}[X])$ .

Computing  $\mathbb{E}[X]$ . Fix  $u \in [n]$  and let us compute  $\mathbb{P}(\hat{\sigma}_{\text{Best}}(u) \neq \sigma_0(u))$ . Estimating  $\sigma_0(u)$  is a binary Bayesian hypothesis testing problem, where the prior is given by  $\mathbb{P}(\sigma_0(u) = +1) = \mathbb{P}(\sigma_0(u) = -1) = \frac{1}{2}$ . We are given the observed edge-labeled graph G and  $\{\sigma_0(v) : v \in [n] \setminus \{u\}\}$ , which satisfies (3.1) with  $\varepsilon = n^{-\frac{1}{3}}$  with probability at least  $1 - 2\exp(-n^{1/3}/6) = 1 - n^{-\omega(1)}$ . The genie-based estimator performs a Maximum A Posteriori (MAP) decoding rule based on the observed degree profiles  $D = D(\sigma_0, u)$ . Let  $\mathcal{D} := \{d : d_i \leq \log^{5/4} n, \forall i \in [4]\}$ . By (3.2),

$$\mathbb{P}(\hat{\sigma}_{\text{Best}}(u) \neq \sigma_0(u)) = \frac{1}{2} \sum_{d \in \mathcal{D}} \min \left\{ \mathbb{P}(D = d \mid \sigma_0(u) = +1), \mathbb{P}(D = d \mid \sigma_0(u) = -1) \right\} + n^{-\omega(1)}.$$

Using Lemma 3.1,

$$\begin{split} \mathbb{P}(\hat{\sigma}_{\text{\tiny Best}}(u) \neq \sigma_0(u)) \\ & \asymp \frac{1}{2} \sum_{d \in \mathcal{D}} \min\{M(n_1, d_1, d_2, p_1) \times M(n_2, d_3, d_4, q), M(n_1, d_1, d_2, q) \times M(n_2, d_3, d_4, p_2)\} + n^{-\omega(1)} \\ & \asymp \sum_{d \in \mathcal{D}} \min\left\{P\Big(\frac{tp_1 \log n}{2}; d_1\Big)P\Big(\frac{t(1-p_1) \log n}{2}; d_2\Big)P\Big(\frac{tq \log n}{2}; d_3\Big)P\Big(\frac{t(1-q) \log n}{2}; d_4\Big), \\ & P\Big(\frac{tq \log n}{2}; d_1\Big)P\Big(\frac{t(1-q) \log n}{2}; d_2\Big)P\Big(\frac{tp_2 \log n}{2}; d_3\Big)P\Big(\frac{t(1-p_2) \log n}{2}; d_4\Big)\right\} + n^{-\omega(1)}. \end{split}$$

We can now use [5, Theorem 3] with  $c_1' = \frac{t}{2}(p_1, 1 - p_1, q, 1 - q)$ , and  $c_2' = \frac{t}{2}(q, 1 - q, p_2, 1 - p_2)$  to conclude that

(6.3) 
$$\mathbb{P}(\hat{\sigma}_{\text{Best}}(u) \neq \sigma_0(u)) = n^{-\Delta_t(c_1', c_2')(1 + o(1))} + n^{-\omega(1)},$$

<span id="page-14-3"></span>where

(6.4) 
$$\Delta_t(c_1', c_2') := \max_{x \in [0,1]} \sum_i \left( x(c_1')_i + (1-x)(c_2')_i - (c_1')_i^x (c_2')_i^{1-x} \right) = \frac{t}{t_c(p_1, p_2, q)}.$$

Thus, we have shown that, for any  $u \in [n]$ ,

(6.5) 
$$\mathbb{E}[X] = \mathbb{P}(\hat{\sigma}_{\text{Best}}(u) \neq \sigma_0(u)) = n^{-(1+o(1))t/t_c(p_1, p_2, q)}.$$

Computing  $\mathbb{P}(X > 1/2)$ . Note that

<span id="page-14-2"></span>(6.6) 
$$\mathbb{E}[X^2] = \frac{1}{n^2} \sum_{i \in [n]} \mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_0(i)) + \frac{1}{n^2} \sum_{i,j \in [n]: i \neq j} \mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_0(i), \ \hat{\sigma}_{\text{Best}}(j) \neq \sigma_0(j)).$$

Fix any  $i \neq j$  and let  $\mathscr{F}$  denote the minimum sigma-algebra with respect to which  $D(i, \sigma_0)$  and N(i) are measurable. Then the event  $\{\hat{\sigma}_{\text{Best}}(i) \neq \sigma_0(i)\}$  is measurable with respect to  $\mathscr{F}$ . Let  $\mathscr{B}$  be the event that  $\{i, j\}$  is revealed or there exists a v such that both  $\{i, v\}$  and  $\{v, j\}$  are revealed. Let us condition on  $\mathscr{F}$ . Let  $\hat{\sigma}'_{\text{Best}}(j)$  be the genie estimator computed on  $G \setminus (N(i) \cup \{i\})$ . On the event  $\mathscr{B}^c$ , we have that  $\hat{\sigma}_{\text{Best}}(j) = \hat{\sigma}'_{\text{Best}}(j)$ , as  $D(j, \sigma_0)$  remains identical on G and  $G \setminus (N(i) \cup \{i\})$ . Note that for all sufficiently large n, almost surely,

<span id="page-14-1"></span>
$$\mathbb{P}(\mathcal{B} \mid \mathscr{F}) \mathbb{1}_{\{|N(i)| \le \log^{5/4} n\}} \le \alpha (1 + \log^{5/4} n) \le \frac{\log^3 n}{n},$$

and therefore

$$\begin{split} \mathbb{P}(\hat{\sigma}_{\text{\tiny Best}}(j) \neq \sigma_0(j) \mid \mathscr{F}) \mathbb{1}_{\{|N(i)| \leq \log^{5/4} n\}} \leq \left( \mathbb{P}(\hat{\sigma}_{\text{\tiny Best}}(j) \neq \sigma_0(j), \mathcal{B}^c \mid \mathscr{F}) + \mathbb{P}(\mathcal{B} \mid \mathscr{F}) \right) \mathbb{1}_{\{|N(i)| \leq \log^{5/4} n\}} \\ \leq \mathbb{P}(\hat{\sigma}'_{\text{\tiny Best}}(j) \neq \sigma_0(j) \mid \mathscr{F}) \mathbb{1}_{\{|N(i)| \leq \log^{5/4} n\}} + \frac{\log^3 n}{n} \\ = n^{-(1+o(1))t/t_c(p_1, p_2, q)} + \frac{\log^3 n}{n}, \end{split}$$

where the expression in the last step can be computed using identical arguments as (6.5). Also,  $\mathbb{P}(|N(i)| > \log^{5/4} n) \le e^{-\log^{5/4} n}$  for all sufficiently large n. Therefore,

$$\begin{split} & \mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_{0}(i), \ \hat{\sigma}_{\text{Best}}(j) \neq \sigma_{0}(j)) \\ & \leq \mathbb{E}[\mathbb{P}(\hat{\sigma}_{\text{Best}}(j) \neq \sigma_{0}(j) \mid \mathscr{F})\mathbb{1}_{\{|N(i)| \leq \log^{5/4} n\}} \mathbb{1}_{\{\hat{\sigma}_{\text{Best}}(i) \neq \sigma_{0}(i)\}}] + \mathbb{P}(|N(i)| > \log^{5/4} n) \\ & \leq \Big(n^{-(1+o(1))t/t_{c}(p_{1},p_{2},q)} + \frac{\log^{3} n}{n}\Big) \mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_{0}(i)) + e^{-\log^{5/4} n} \\ & < n^{-\delta - (1+o(1))t/t_{c}(p_{1},p_{2},q)} \end{split}$$

for some fixed  $\delta > 0$ . Using (6.6), we have that  $\mathbb{E}[X^2] = n^{-\delta - (1+o(1))t/t_c(p_1, p_2, q)}$ , and by Markov's inequality,

$$\mathbb{P}(X > 1/2) = \mathbb{P}(X^2 > 1/4) < 4n^{-\delta - (1+o(1))t/t_c(p_1, p_2, q)} = o(\mathbb{E}[X]).$$

### <span id="page-14-0"></span>6.2 Comparing the spectral and genie estimators

*Proof.* (Proof of Theorem 2.3). We prove the claim for the case p > q; the case p < q follows by replacing A by -A. By Lemma 6.1 and (2.9), we have  $\operatorname{Err}(\hat{\sigma}_{\text{Best}}) = n^{-(1+o(1))t/t_c(p,q)}$ . To analyze the error rate of the spectral algorithm, fix  $\varepsilon > 0$  and let

$$\mathcal{B}_n := \left\{ \min_{s \in \{\pm 1\}} \left\| u_1 - s \frac{Au_1^{\star}}{\lambda_1^{\star}} \right\|_{L^2} \leq \frac{\varepsilon}{\sqrt{n}} \right\} \quad \text{and} \quad \mathcal{C}_n := \left\{ \left| n_1(\sigma_0) - \frac{n}{2} \right| \leq n^{\frac{2}{3}}, \left| n_2(\sigma_0) - \frac{n}{2} \right| \leq n^{\frac{2}{3}} \right\}.$$

Let  $s \in \{\pm 1\}$  be the sign for which  $\|u_1 - sAu_1^*/\lambda_1^*\|_{\infty}$  is minimized. By Lemma 5.1,  $\mathbb{P}(\mathcal{B}_n) = 1 - O(n^{-3})$ . If the spectral algorithm is not able to classify i correctly, then  $s\sigma_0(i)(u_1)_i \leq 0$ . This implies that, on  $\mathcal{B}_n$ , we have  $\sqrt{n}\sigma_0(i)Au_1^*/\lambda_1^* \leq \varepsilon$ . Using (3.1) and (5.4), for any  $i \in [n]$ ,

(6.7) 
$$\mathbb{P}(\hat{\sigma}_{\text{Spec}}(i) \neq s\sigma_0(i)) \leq \mathbb{P}((\mathcal{B}_n \cap \mathcal{C}_n)^c) + \mathbb{P}\left(\sum_{j \in J_i(\sigma_0)} A_{ij} - \sum_{j \notin J_i(\sigma_0)} A_{ij} \leq \varepsilon \log(n) \mid \mathcal{C}_n\right) \\ \leq O(n^{-3}) + n^{-(1+o(1))t/t_c(p,q)},$$

where the final step uses Lemma 5.4. The proof follows by taking an average over i.

### <span id="page-15-0"></span>7 Analysis of the two-step estimator

In order to establish Theorems 2.4 and 2.5, we introduce the notion of a good estimator. Consider the exact recovery problem on  $\text{CSBM}(p_1, p_2, q, t)$ , possibly with  $p_1 \neq p_2$ . We will show that, given a "good" initial estimator  $\hat{\sigma}$ , the clean-up procedure defined by  $\hat{X}(\hat{\sigma})$  produces an estimator that recovers  $\sigma_0$  exactly when  $t > t_c(p_1, p_2, q)$ , and otherwise compares favorably with the genie estimator. Recall the definition of  $N(u) = \{v : A_{uv} \neq 0\}$ , and define  $M(\hat{\sigma}, \sigma_0)$  to be the set of misclassified vertices under the optimal choice of the global flip, i.e.  $M(\hat{\sigma}, \sigma_0)$  is the smaller of

<span id="page-15-5"></span>
$$\{v : \hat{\sigma}(v) \neq \sigma_0(v)\}\$$
and  $\{v : -\hat{\sigma}(v) \neq \sigma_0(v)\}.$ 

<span id="page-15-1"></span>DEFINITION 7.1. We say that  $\hat{\sigma}$  is a good estimator if:

<span id="page-15-4"></span>(i) There exists  $L \geq 1$  (fixed) such that, for all sufficiently large n,

(7.1) 
$$\mathbb{P}(|N(u) \cap M(\hat{\sigma}, \sigma_0)| \le L) \ge 1 - o(1/n) \quad \forall u \in [n],$$

i.e., any vertex can have at most O(1) many misclassified neighbors.

<span id="page-15-2"></span>(ii) There exists a constant  $\varepsilon > 0$  such that, for all  $u \in [n]$ ,

$$\max_{d:||d||_1 \le \log^{5/4}(n)} \mathbb{P}\left(N(u) \cap M(\hat{\sigma}, \sigma_0) = \varnothing | D(\sigma_0, u) = d\right) = 1 - O(n^{-\varepsilon}),$$

i.e., vertices have a negligible probability of having a misclassified revealed neighbor/non-neighbor given the correct degree profile.

Note that Definition 7.1 (ii) implies that there exists  $(\varepsilon_n)_{n\geq 1}\subset (0,\infty)$  with  $\lim_{n\to\infty}\varepsilon_n=0$ , such that

(7.2) 
$$\mathbb{P}(\#\{i:N(i)\cap M(\hat{\sigma},\sigma_0)=\varnothing\} \ge (1-\varepsilon_n)n) \to 1,$$

i.e,  $\hat{\sigma}$  classifies all but o(n) many vertices correctly.

Comparing the two-step estimator  $X(\hat{\sigma})$  from (2.7) to the genie-based estimator (6.1), we see that a good estimator acts as a proxy for the true labels; just as the true labels are used to compute the genie-based estimator, so the good estimator labels are used by the two-step estimator. The next result provides recovery guarantees for good estimators.

<span id="page-15-3"></span>THEOREM 7.1. Suppose that  $\hat{\sigma}$  is a good estimator. If  $t > t_c(p_1, p_2, q)$ , then  $\hat{X}(\hat{\sigma})$  achieves exact recovery. Moreover, for any t > 0,

(7.3) 
$$\operatorname{Err}(\hat{X}(\hat{\sigma})) = (1 + o(1))\operatorname{Err}(\hat{\sigma}_{\text{Best}}) + o(1/n).$$

Given Theorem 7.1, it suffices to show that  $\hat{\sigma}_{\text{Spec}}$  and  $\hat{\sigma}_{\text{Deg}}$  are good estimators in order to establish Theorems 2.4 and 2.5. In Section 7.1, we prove Theorem 7.1, and in Section 7.2 we prove Theorems 2.4 and 2.5.

REMARK 7.1. In the case where  $p_1 = p_2$ , the clean up step is essentially just a way of removing noise.  $\hat{\sigma}_{\text{Spec}}$  is essentially just the primary eigenvector of A with some noise removed, which means that  $\hat{X}(\hat{\sigma}_{\text{Spec}})$  is a rounded version of  $A\hat{\sigma}_{\text{Spec}}$ , which can be viewed as the eigenvector with more noise removed. The result is an estimator which is similar to the eigenvector but with less susceptibility for its guess of a vertex's community to be influenced by atypicalities in its neighbors' degree profiles.

In the asymmetric case  $\hat{\sigma}_{\text{Deg}}$  is a significantly worse estimator because it does not take into account any information on the communities of the vertices a target vertex's edges are to. Nevertheless, it classifies vertices with a sufficiently high accuracy for the two step approach to work. Namely, the initial estimate provides good estimates of the vertices' degree profiles, such that the clean-up step correctly selects the most likely community for the vertices, given their initially estimated degree profiles.<sup>1</sup>

<span id="page-16-0"></span>7.1 Error rate guarantees for good estimators. Suppose we are given a good estimator  $\hat{\sigma}$ . Define  $V_{\text{good}} := \{i : N(i) \cap M(\hat{\sigma}, \sigma_0) = \varnothing\}$ . That is,  $V_{\text{good}}$  is the set of vertices whose neighbors are all correctly classified by  $\hat{\sigma}$ . We denote the rest as  $V_{\text{bad}} = [n] \setminus V_{\text{good}}$ . Note that if  $i \in V_{\text{good}}$ , then the two step estimator produces the same assignment for i as the genie estimator. The next lemma handles the case that  $i \in V_{\text{bad}}$  and the estimator  $\hat{X}(\hat{\sigma}, i)$  is incorrect.

<span id="page-16-3"></span>LEMMA 7.1. Let  $\hat{\sigma}$  be a good estimator. For any  $i \in [n]$ , we have

<span id="page-16-2"></span>
$$\mathbb{P}(\hat{X}(\hat{\sigma}, i) \neq \sigma_0(i), i \in V_{\text{bad}}) = o\left(\mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_0(i)) + 1/n\right).$$

Proof. Fix a vertex i, and recall the degree profile notation  $D(\sigma, i) = (D_k(\sigma, i))_{k=1}^4$ . Define  $\mathcal{D} := \{d \in \mathbb{Z}_+^4 : ||d||_1 \le \log^{5/4} n\}$ . By (3.2),  $\mathbb{P}(D(\sigma_0, i) \notin \mathcal{D}) = o(1/n)$ . First, we claim that for any  $d, d' \in \mathcal{D}$  satisfying  $||d - d'||_1 \le L$ ,

(7.4) 
$$\frac{\mathbb{P}\left(D(\sigma_0, i) = d'\right)}{\mathbb{P}\left(D(\sigma_0, i) = d\right)} \le c_0 \log^{2L} n,$$

where  $c_0 > 0$  is a constant that depends only on  $p_1$ ,  $p_2$ , q, t, and L. Indeed, by Lemma 3.1,

$$(1+o(1))\min\{A(d),B(d)\} \le \mathbb{P}(D(\sigma_0,i)=d) \le (1+o(1))\max\{A(d),B(d)\}$$

where

$$\begin{split} A(d) &:= P\Big(\frac{tp_1 \log n}{2}; d_1\Big) P\Big(\frac{t(1-p_1) \log n}{2}; d_2\Big) P\Big(\frac{tq \log n}{2}; d_3\Big) P\Big(\frac{t(1-q) \log n}{2}; d_4\Big) \\ B(d) &:= P\Big(\frac{tq \log n}{2}; d_1\Big) P\Big(\frac{t(1-q) \log n}{2}; d_2\Big) P\Big(\frac{tp_2 \log n}{2}; d_3\Big) P\Big(\frac{t(1-p_2) \log n}{2}; d_4\Big). \end{split}$$

Using  $||d - d'||_1 \le L$ , (7.4) now follows. Next, we set up some notation to complete the proof. Define  $S_0(i) \subset S$  to be the set of  $\sigma$  such that  $|N(i) \cap M(\sigma, \sigma_0)| \le L$ . By Definition 7.1 (i), we have that  $\mathbb{P}(\hat{\sigma} \notin S_0(i)) = o(1/n)$ . For every d, let

$$\overline{\sigma}(d,i) := \operatorname*{argmax}_{r \in \{\pm 1\}} \mathbb{P}(\sigma_0(i) = r \mid D(\sigma_0,i) = d)$$

be the most likely community assignment of i given the observed degree profile d of i. We set  $\overline{\sigma}(d,i)=+1$  if they are equally likely. Define  $\mathcal{B}(d,L):=\{d'\in\mathcal{D}:\|d-d'\|_1\leq L \text{ and } \overline{\sigma}(d',i)\neq\sigma_0(i)\}$ . In other words,  $\mathcal{B}(d,L)$  is the set of degree profiles near d on which even the best estimator makes a mistake. Note that if we have  $\hat{X}(\hat{\sigma},i)\neq\sigma_0(i),\ i\in V_{\text{bad}},\ \text{and }\hat{\sigma}\in\mathcal{S}_0(i),\ \text{then it must be the case that }D(\sigma_0,i)\ \text{has a degree profile }d\ \text{such that }\mathcal{B}(d,L)\neq\varnothing$ . Therefore, using Definition 7.1 (ii) and (7.4),

$$\begin{split} & \mathbb{P}(\hat{X}(\hat{\sigma}, i) \neq \sigma_0(i), i \in V_{\text{bad}}) \\ & \leq \mathbb{P}(\hat{X}(\hat{\sigma}, i) \neq \sigma_0(i), i \in V_{\text{bad}}, D(\sigma_0, i) \in \mathcal{D}, \hat{\sigma} \in \mathcal{S}_0(i)) + o(1/n) \\ & \leq \sum_{d \in \mathcal{D}: \mathcal{B}(d, L) \neq \varnothing} \mathbb{P}\left(i \in V_{\text{bad}}, D(\sigma_0, i) = d\right) + o(1/n) \end{split}$$

<span id="page-16-1"></span><sup>&</sup>lt;sup>1</sup>We could have used a spectral algorithm for the first step, but it would be harder to compute without giving any real advantage.

$$\leq \sum_{d \in \mathcal{D}: \mathcal{B}(d,L) \neq \varnothing} cn^{-\varepsilon} \mathbb{P}\left(D(\sigma_{0},i) = d\right) + o(1/n) 
= cn^{-\varepsilon} \mathbb{P}(D(\sigma_{0},i) \in \mathcal{D} \text{ and } \mathcal{B}(D(\sigma_{0},i),L) \neq \varnothing) + o(1/n) 
\leq cn^{-\varepsilon} \sum_{d': \overline{\sigma}(d',i) \neq \sigma_{0}(i)} \mathbb{P}(\|D(\sigma_{0},i) - d'\|_{1} \leq L) + o(1/n) 
\leq cn^{-\varepsilon} \sum_{d': \overline{\sigma}(d',i) \neq \sigma_{0}(i)} c_{0} \log^{2L}(n) \mathbb{P}(D(\sigma_{0},i) = d') + o(1/n) 
= cc_{0}n^{-\varepsilon} \log^{2L}(n) \times \mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_{0}(i)) + o(1/n) 
= o(\mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_{0}(i)) + 1/n)$$

Proof. (Proof of Theorem [7.1\)](#page-15-3). Fix i ∈ [n]. Recall that Vgood := {i : N(i) ∩ M(σ, σ ˆ <sup>0</sup>) = ∅}, and Vbad = [n] \ Vgood. Using Lemma [7.1,](#page-16-3) we have

$$\mathbb{P}(\hat{X}(\hat{\sigma}, i) \neq \sigma_0(i)) = (1 + o(1))\mathbb{P}(\hat{\sigma}_{\text{Best}}(i) \neq \sigma_0(i)) + o(1/n).$$

Taking an average over i and using Err(Xˆ(σˆ)) ≤ 1 n P <sup>i</sup>∈[n] <sup>P</sup>(Xˆ(σ, i <sup>ˆ</sup> ) <sup>6</sup><sup>=</sup> <sup>σ</sup>0(i)) and Err(σˆBest) = <sup>1</sup> n P <sup>i</sup>∈[n] <sup>P</sup>(σˆBest(i) <sup>6</sup><sup>=</sup> σ0(i)) + o(1/n) (see the argument after [\(6.5\)](#page-14-1)), the proof follows.

### <span id="page-17-0"></span>7.2 Good estimators

Proof. (Proof of Theorem [2.4\)](#page-4-1). Due to Theorem [7.1,](#page-15-3) it suffices to show that σˆSpec is a good estimator. We will first verify Definition [7.1](#page-15-1) [\(i\).](#page-15-4) Let L ≥ 1 be fixed (to be chosen later). For any V ⊂ [n], let

$$D_V(j) := \sum_{k \in V^c: k \sim j} A_{jk} - \sum_{k \in V^c: k \not\sim j} A_{jk}.$$

By the previous analysis (cf. [\(6.7\)](#page-15-5)),

(7.5) 
$$\mathbb{P}(\hat{\sigma}_{\text{Spec}}(j) \text{ misclassifies}) \leq \mathbb{P}(D_{\varnothing}(j) \leq \varepsilon \log n) + o(1/n),$$

where ε = o(1) but ε log n → ∞. Additionally, if |V | ≤ L for some fixed L ≥ 0, then D<sup>V</sup> (j) ≤ ε log n + O(L) ≤ 2ε log n for large enough n. Thus,

$$\begin{split} & \mathbb{P}(|N(i) \cap M(\hat{\sigma}_{\text{Spec}}, \sigma_{0})| > L) \\ & \leq \mathbb{P}(|N(i)| > \log^{5/4} n) + \mathbb{E}\left[\mathbb{P}\left(|N(i) \cap M(\hat{\sigma}_{\text{Spec}}, \sigma_{0})| > L \mid N(i), |N(i)| \leq \log^{5/4} n\right)\right] \\ & \leq \mathrm{e}^{-\log^{5/4} n} + \mathbb{E}\left[\sum_{j_{0}, \dots, j_{L} \in N(i)} \mathbb{P}\left(j_{0}, \dots, j_{L} \in N(i) \cap M(\hat{\sigma}_{\text{Spec}}, \sigma_{0}) \mid N(i), |N(i)| \leq \log^{5/4} n\right)\right] \\ & \leq \mathrm{e}^{-\log^{5/4} n} + \binom{\log^{5/4} n}{L+1} \mathbb{E}\left[\max_{j_{0}, \dots, j_{L}} \mathbb{P}\left(j_{0}, \dots, j_{L} \in N(i) \cap M(\hat{\sigma}_{\text{Spec}}, \sigma_{0}) \mid N(i), |N(i)| \leq \log^{5/4} n\right)\right], \end{split}$$

where we have applied [\(3.2\)](#page-6-3). Taking V = {j0, . . . , jL, i} yields

$$\mathbb{P}\big(j_0,\ldots,j_L \in N(i) \cap M(\hat{\sigma}_{\text{Spec}},\sigma_0) \mid N(i), |N(i)| \leq \log^{5/4} n\big) \ \leq \mathbb{P}\big(D_V(j_l) \leq 2\varepsilon \log n, \ \forall 0 \leq l \leq L \mid N(i), |N(i)| \leq \log^{5/4} n\big).$$

Now, note that D<sup>V</sup> (jl) for different l depend on disjoint sets of random variables. Thus, Lemma [5.4](#page-11-1) gives

$$\mathbb{P}(D_V(j_l) \le 2\varepsilon \log n, \ \forall 0 \le l \le L \mid N(i), |N(i)| \le \log^{5/4} n) \le n^{-c(L+1)},$$

for some constant c > 0. Therefore,

$$\mathbb{P}(|N(i) \cap M(\hat{\sigma}_{\text{Spec}}, \sigma_0)| > L) \le e^{-\log^{5/4} n} + (\log n)^{5(L+1)/4} n^{-c(L+1)} = o(1/n),$$

which verifies Definition 7.1 (i) by taking L to be a large fixed constant. To verify Definition 7.1 (ii), we can repeat the above argument for conditional probabilities with L=0. Indeed, for any d with  $||d||_1 \le \log^{5/4} n$ ,

$$\mathbb{P}(|N(i) \cap M| \ge 1 \mid D(\sigma_0, i) = d) \le (\log n)^{5/4} \cdot n^{-c},$$

and the proof follows.  $\Box$ 

*Proof.* (Proof of Theorem 2.5). Due to Theorem 7.1, it suffices to show that  $\hat{\sigma}_{\text{Deg}}$  is a good estimator. We have

(7.6) 
$$\mathbb{E}[\deg(j) \mid \sigma_0] = \begin{cases} \frac{t \log(n)}{2} (p_1 + q) & \text{if } \sigma_0(j) = +1, \\ \frac{t \log(n)}{2} (p_2 + q) & \text{if } \sigma_0(j) = -1. \end{cases}$$

Suppose  $p_1 > p_2$  without loss of generality. We bound

$$\mathbb{P}\left(\deg(j) < \frac{t \log(n)}{4} \left(p_1 + p_2 + 2q\right) \mid \sigma_0(j) = +1\right) \\
= \mathbb{P}\left(\deg(j) < \left(1 - \frac{p_1 - p_2}{2(p_1 + q)}\right) \mathbb{E}[\deg(j) \mid \sigma_0(j) = +1] \mid \sigma_0(j) = +1\right) \\
\leq \exp\left(-\frac{\mathbb{E}[\deg(j) \mid \sigma_0(j) = +1]}{2} \left(\frac{p_1 - p_2}{2(p_1 + q)}\right)^2\right) \\
= \exp\left(-\frac{t \log(n)(p_1 + q)}{4} \left(\frac{p_1 - p_2}{2(p_1 + q)}\right)^2\right) \\
= \exp\left(-\frac{t \log(n)(p_1 - p_2)^2}{16(p_1 + q)}\right).$$

Similarly,

$$\mathbb{P}\left(\deg(j) \ge \frac{t \log(n)}{4} (p_1 + p_2 + 2q) \mid \sigma_0(j) = -1\right) \\
= \mathbb{P}\left(\deg(j) \ge \left(1 + \frac{p_1 - p_2}{2(p_2 + q)}\right) \mathbb{E}[\deg(j) \mid \sigma_0(j) = -1] \mid \sigma_0(j) = -1\right) \\
\le \exp\left(-\frac{\left(\frac{p_1 - p_2}{2(p_2 + q)}\right)^2}{2 + \frac{p_1 - p_2}{2(p_2 + q)}} \mathbb{E}[\deg(j) \mid \sigma_0(j) = -1]\right) \\
= \exp\left(-\frac{t \log n(p_2 + q)}{2} \frac{\left(\frac{p_1 - p_2}{2(p_2 + q)}\right)^2}{2 + \frac{p_1 - p_2}{2(p_2 + q)}}\right) \\
= \exp\left(-\frac{t \log n(p_1 - p_2)^2}{4(p_1 + 3p_2 + 4q)}\right).$$

Therefore, we have shown that any given vertex j is misclassified with probability at most  $n^{-\beta}$ , where  $\beta > 0$  is a constant. Fix  $i \in [n]$ . We wish to take a union bound over  $j \in N(i)$  in order to bound the probability that some revealed neighbor of i is misclassified. However, if a vertex j is a neighbor of i, then its degree is inflated by 1. Since the discrepancy is negligible at the  $\log(n)$  scale, we may take  $\beta$  slightly smaller. Then, for any d such that  $\|d\|_1 \leq \log^{5/4} n$ ,

$$\mathbb{P}\left(N(i) \cap M(\hat{\sigma}_{\text{Deg}}, \sigma_0) \neq \varnothing \mid D(\sigma_0, i) = d\right) \le \log^{5/4}(n)n^{-\beta} \le n^{-\frac{\beta}{2}}$$

for n large enough, satisfying Definition 7.1 (ii).

Next, take  $L > \frac{2}{\beta}$ . By a Union Bound,

$$\mathbb{P}(|N(i) \cap M(\hat{\sigma}_{\text{Deg}}, \sigma_0)| \ge L) \le \binom{\log^{5/4}(n)}{L} n^{-\beta L} + n^{-\omega(1)}$$

$$\le \log^{5L/4}(n) n^{-\beta L} + n^{-\omega(1)} \le n^{-\frac{3}{2}},$$

for n large enough, which verifies Definition 7.1 (i).

### <span id="page-19-0"></span>8 Failure of the spectral algorithm

Similarly to the proof of Theorem 2.2, we apply the entrywise approach to analyze the eigenvectors of A. Any linear combination of  $u_1$  and  $u_2$  can then be approximated by A times a vector z that is constant on each community. Then we can characterize all spectral algorithms as thresholding weighted degree profiles by a *score* that depends on the vector z. Sufficiently close to the threshold, we exhibit certain degree profiles that are likely enough to occur, for which there is no way to pick the encoding value y or the weights z in order to separate the communities. Specifically, if we take the degree profile that is half way between the expected degree profiles for vertices in the two communities, there will always be a way to perturb it such that vertices with that degree profile are likely to exist in one community and the spectral algorithm classifies them as being in the other. Unlike in the symmetric case, the class of spectral algorithms considered here does not have enough degrees of freedom to allow correct separation of vertices with such degree profiles.

*Proof.* (Proof of Theorem 2.6). Throughout the proof, we will condition on  $\sigma_0$  satisfying  $\left|n_1(\sigma_0) - \frac{n}{2}\right| \leq n^{\frac{2}{3}}$  and  $\left|n_2(\sigma_0) - \frac{n}{2}\right| \leq n^{\frac{2}{3}}$ .

Let  $u_1$  and  $u_2$  be the top two eigenvectors of A. By Proposition 5.1 we have that with probability  $1 - O(n^{-3})$ ,

$$\left\| u_1 - s_1 \frac{Au_1^*}{\lambda_1^*} \right\|_{\infty} \le \frac{C}{\sqrt{n} \log \log n} \quad \text{and} \quad \left\| u_2 - s_2 \frac{Au_2^*}{\lambda_2^*} \right\|_{\infty} \le \frac{C}{\sqrt{n} \log \log n},$$

for some  $s_1, s_2 \in \{-1, 1\}$  and some constant C > 0. Then for any  $c_1, c_2$  we also have

$$\left\| c_1 u_1 + c_2 u_2 - A \left( \frac{s_1 c_1}{\lambda_1^*} u_1^* + \frac{s_2 c_2}{\lambda_2^*} u_2^* \right) \right\|_{\infty} \le \frac{C(|c_1| + |c_2|)}{\sqrt{n} \log \log n}.$$

By Lemma 5.3, the vector  $(\frac{s_1c_1}{\lambda_1^*}u_1^* + \frac{s_2c_2}{\lambda_2^*}u_2^*)$  will assign all vertices in Community 1 some value  $z_1$  and all vertices in Community 2 some other value  $z_2$ . We can assume without loss of generality that  $z_1^2 + z_2^2 = 1$ . We conclude that a spectral algorithm based on a linear combination of the top two eigenvectors will classify a vertex with degree profile  $(d_1, d_2, d_3, d_4)$  as being in one community if

$$z_1d_1 - yz_1d_2 + z_2d_3 - yz_2d_4 > r + \Omega\left(\log(n)/\log(\log(n))\right)$$

and the opposite community if

<span id="page-19-1"></span>
$$z_1d_1 - yz_1d_2 + z_2d_3 - yz_2d_4 < r - \Omega\left(\log(n)/\log(\log(n))\right)$$

for some threshold r. To show that the spectral algorithm fails for t sufficiently close to the threshold, it suffices to show that there is no choice of  $z_1$ ,  $z_2$  and y for which thresholding the score  $z_1d_1 - yz_1d_2 + z_2d_3 - yz_2d_4$  separates the communities successfully.

We will first show that

(8.1) 
$$r = (z_1 - yz_2)\sqrt{p/8t}\log(n) + (z_2 - yz_1)\sqrt{(1-p)/8t}\log(n) + o(\log(n))$$

and both y and  $z_1z_2$  are positive. We can then assume without loss of generality that  $z_1, z_2 > 0$  and the algorithm classifies a vertex as being in Community 1 if its score is larger than  $r + \Omega(\log(n)/\log(\log(n)))$ , and otherwise classifies it as being in Community 2. We will then show that there exist constants  $\delta > \delta' > 0$  such that there are vertices with degree profile

<span id="page-19-2"></span>
$$(8.2) \qquad \left(\sqrt{p/8}t\log(n) - \delta\log(n), \sqrt{(1-p)/8}t\log(n) - \delta'\log(n), \sqrt{(1-p)/8}t\log(n), \sqrt{p/8}t\log(n)\right)$$

<span id="page-20-2"></span>in Community 1 and vertices with degree profile

(8.3) 
$$\left( \sqrt{p/8}t \log(n), \sqrt{(1-p)/8}t \log(n), \sqrt{(1-p)/8}t \log(n) - \delta' \log(n), \sqrt{p/8}t \log(n) - \delta \log(n) \right)$$

in Community 2. In order to classify the former vertices correctly, the spectral algorithm would need to have  $y > \delta/\delta' - o(1)$  and to classify the later vertices correctly the algorithm would need to have  $y < \delta'/\delta + o(1)$ , but for large n those cannot both be true.

It remains to establish the claims regarding the threshold value, and the existence of common degree profiles. To this end, we compute the probability of a given degree profile for  $\sigma_0(i) = +1$  and  $\sigma_0(i) = -1$ . Given constants  $c_1$ ,  $c_2$ ,  $c_3$ , and  $c_4$ , set  $c'_1 = c_1 - t\sqrt{p/8}$ ,  $c'_2 = c_2 - t\sqrt{(1-p)/8}$ ,  $c'_3 = c_3 - t\sqrt{(1-p)/8}$ ,  $c'_4 = c_4 - t\sqrt{p/8}$ , and  $\epsilon = \min\{\sqrt{p/8}t, \sqrt{(1-p)/8}t, c_1, c_2, c_3, c_4\}$ . Computing the probability of given profiles using Lemma 3.1,

$$\mathbb{P}\left(D(\sigma_{0}, i) = \log(n)\left(c_{1}, c_{2}, c_{3}, c_{4}\right)\right) = \mathbb{P}\left(D(\sigma_{0}, j) = \log(n)\left(c_{4}, c_{3}, c_{2}, c_{1}\right)\right)$$

$$\times P\left(\frac{tp\log n}{2}; c_{1}\log n\right) P\left(\frac{t(1-p)\log n}{2}; c_{2}\log n\right) P\left(\frac{t\log n}{4}; c_{3}\log n\right) P\left(\frac{t\log n}{4}; c_{4}\log n\right)$$

$$= \frac{n^{-t}\left(\frac{t\log(n)}{2}\right)^{(c_{1}+c_{2}+c_{3}+c_{4})\log(n)}}{(c_{1}\log(n))!(c_{2}\log(n))!(c_{3}\log(n))!(c_{4}\log(n))!} \times p^{c_{1}\log(n)}(1-p)^{c_{2}\log(n)}(1/2)^{(c_{3}+c_{4})\log(n)}$$

$$\approx \frac{n^{-t}\left(\frac{et}{2}\right)^{(c_{1}+c_{2}+c_{3}+c_{4})\log(n)}}{c_{1}^{c_{1}\log(n)}c_{2}^{c_{2}\log(n)}c_{3}^{c_{3}\log(n)}c_{4}^{c_{4}\log(n)}} \times p^{c_{1}\log(n)}(1-p)^{c_{2}\log(n)}(1/2)^{(c_{3}+c_{4})\log(n)}$$

$$= \frac{n^{-t}\left[\left(\frac{e^{2}t^{2}p}{8}\right)^{(c_{1}+c_{4})}\left(\frac{e^{2}t^{2}(1-p)}{8}\right)^{(c_{2}+c_{3})}(2p)^{(c_{1}-c_{4})}\left(2(1-p)\right)^{(c_{2}-c_{3})}\right]^{\log(n)/2}}{n^{c_{1}\log(c_{1})}n^{c_{2}\log(c_{2})}n^{c_{3}\log(c_{3})}n^{c_{4}\log(c_{4})}}.$$

To bound (8.4), we will use the fact that for any a, b > 0,

(8.5) 
$$a\log(a) \le b\log(b) + (a-b)\log(eb) + \frac{(a-b)^2}{2\min(a,b)},$$

which follows from Taylor expansion and the fact that the second derivative of  $x \log(x)$  is at most  $1/\min(a, b)$  between a and b. Taking  $a = c_1$  and  $b = c_1 - c'_1 = t\sqrt{p/8}$ , in (8.5), we have

<span id="page-20-1"></span><span id="page-20-0"></span>
$$c_1 \log(c_1) \le t \sqrt{\frac{p}{8}} \log\left(t \sqrt{\frac{p}{8}}\right) + c_1' \log\left(et \sqrt{\frac{p}{8}}\right) + \frac{c_1'^2}{2\varepsilon}$$

and therefore

$$\frac{1}{n^{c_1 \log(c_1)}} \left( \operatorname{et} \sqrt{\frac{p}{8}} \right)^{c_1 \log(n)}$$

$$\geq \exp \left[ -\log(n) \left( t \sqrt{\frac{p}{8}} \log \left( t \sqrt{\frac{p}{8}} \right) + c_1' \log \left( \operatorname{et} \sqrt{\frac{p}{8}} \right) - c_1 \log \left( \operatorname{et} \sqrt{\frac{p}{8}} \right) \right) \right] n^{-\frac{c_1'^2}{2\varepsilon}}$$

$$= \exp \left[ -\log(n) \sqrt{\frac{p}{8}} \left( t \sqrt{\frac{p}{8}} + c_1' - c_1 \right) + t \log(n) \sqrt{\frac{p}{8}} \right] n^{-\frac{c_1'^2}{2\varepsilon}}$$

$$= e^{t \sqrt{\frac{p}{8}} \log(n)} n^{-\frac{c_1'^2}{2\varepsilon}}.$$

Similarly,

$$\frac{1}{n^{c_2 \log(c_2)}} \left( \operatorname{et} \sqrt{\frac{1-p}{8}} \right)^{c_2 \log(n)} \ge \operatorname{e}^{t\sqrt{\frac{1-p}{8}} \log(n)} n^{-\frac{c_2^2}{2\varepsilon}} 
\frac{1}{n^{c_3 \log(c_3)}} \left( \operatorname{et} \sqrt{\frac{1-p}{8}} \right)^{c_3 \log(n)} \ge \operatorname{e}^{t\sqrt{\frac{1-p}{8}} \log(n)} n^{-\frac{c_3^2}{2\varepsilon}} 
\frac{1}{n^{c_4 \log(c_4)}} \left( \operatorname{et} \sqrt{\frac{p}{8}} \right)^{c_2 \log(n)} \ge \operatorname{e}^{t\sqrt{\frac{p}{8}} \log(n)} n^{-\frac{c_4^2}{2\varepsilon}}.$$

Next, for simplicity, let us denote  $t_0 = t_c(p, 1 - p, 1/2)$ , and we use the fact that the minimum is attained in (6.4) for x = 1/2 when  $p_1 = 1 - p_2$  and q = 1/2. Substituting the above inequalities into (8.4), and denoting

<span id="page-21-5"></span>
$$Z_n = n^{-((c_1')^2 + (c_2')^2 + (c_3')^2 + (c_4')^2)/2\varepsilon} \times (2p)^{(c_1' - c_4')\log(n)/2} (2(1-p))^{(c_2' - c_3')\log(n)/2},$$

we obtain

(8.6) 
$$\mathbb{P}\left(D(\sigma_0, i) = \log(n) \left(c_1, c_2, c_3, c_4\right)\right) \gtrsim n^{-t} e^{t\sqrt{p/2}\log(n)} e^{t\sqrt{(1-p)/2}\log(n)} \times Z_n = n^{-t/t_0} \times Z_n,$$

where  $a_n \gtrsim b_n$  means there is some constant c such that  $a_n = \Omega(b_n \log^c(n))$ . When  $t = t_0$ , observe that  $\mathbb{P}(D(\sigma_0, i) = \log(n)(c_1, c_2, c_3, c_4))$  cannot be less than  $Z_n/n$  by more than a polylogarithmic factor. Let

$$c_1 = \sqrt{\frac{p}{8}}t_0 + \delta$$
,  $c_2 = c_3 = \sqrt{\frac{(1-p)}{8}}t_0$ ,  $c_4 = \sqrt{\frac{p}{8}}t_0$ .

If  $\delta > 0$  is sufficiently small, with high probability there will be vertices with degree profiles of

$$\log(n)(\sqrt{p/8}t_0 + \delta, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0)$$

in Community 1, since (8.6) is  $\omega\left(\frac{1}{n}\right)$ . In fact, the number of such vertices will be  $\Omega\left(n^{c}\right)$  with high probability for some c>0. A similar argument shows that for  $\delta>0$  small enough, there will additionally be vertices with degree profiles of

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0 - \delta, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0)$$

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0 + \delta, \sqrt{p/8}t_0)$$

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0 - \delta)$$

in Community 1 and vertices with degree profiles of

$$\log(n)(\sqrt{p/8}t_0 - \delta, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0)$$

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0 + \delta, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0)$$

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0 - \delta, \sqrt{p/8}t_0)$$

$$\log(n)(\sqrt{p/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{(1-p)/8}t_0, \sqrt{p/8}t_0 + \delta)$$

in Community 2, when  $t = t_0$ . If  $t = t_0 + \eta$  for  $\eta > 0$  sufficiently small, these degree profiles will still all exist with high probability. To classify the vertices with the above degree profiles correctly, we must use the decision rule given by (8.1), and both y and  $z_1z_2$  must be positive. Finally, since 4p(1-p) < 1, there exist  $\delta > \delta' > 0$  such that there are vertices with the required degree profiles (8.2) and (8.3), and thus the proof follows.

#### References

- <span id="page-21-2"></span>[1] E. Abbe. Community detection and stochastic block models: Recent developments. *Journal of Machine Learning Research*, 18(177):1–86, 2018.
- <span id="page-21-4"></span>[2] E. Abbe, A. S. Bandeira, A. Bracher, and A. Singer. Decoding binary node labels from censored edge measurements: Phase transition and efficient recovery. *IEEE Transactions on Network Science and Engineering*, 1(1):10–22, 2014.
- <span id="page-21-0"></span>[3] E. Abbe, A. S. Bandeira, and G. Hall. Exact recovery in the stochastic block model. *IEEE Transactions on Information Theory*, 62(1):471–487, 2016.
- <span id="page-21-3"></span>[4] E. Abbe, J. Fan, K. Wang, and Y. Zhong. Entrywise eigenvector analysis of random matrices with low expected rank. *Annals of Statistics*, 48(3):1452–1474, 2020.
- <span id="page-21-1"></span>[5] E. Abbe and C. Sandon. Community detection in general stochastic block models: Fundamental limits and efficient algorithms for recovery. In 2015 IEEE 56th Annual Symposium on Foundations of Computer Science (FOCS'15), pages 670–688, 2015.

- <span id="page-22-5"></span>[6] C. Bordenave, M. Lelarge, and L. Massoulié. Non-backtracking spectrum of random graphs: community detection and non-regular ramanujan graphs. In 2015 IEEE 56th Annual Symposium on Foundations of Computer Science (FOCS'15), pages 1347–1357. IEEE, 2015.
- <span id="page-22-2"></span>[7] P. Chin, A. Rao, and V. Vu. Stochastic block model and community detection in sparse graphs: A spectral algorithm with optimal rate of recovery. In Conference on Learning Theory, pages 391–423. PMLR, 2015.
- <span id="page-22-9"></span>[8] B. Hajek, Y. Wu, and J. Xu. Exact recovery threshold in the binary censored block model. In 2015 IEEE Information Theory Workshop-Fall (ITW), pages 99–103. IEEE, 2015.
- <span id="page-22-6"></span>[9] B. Hajek, Y. Wu, and J. Xu. Achieving exact cluster recovery threshold via semidefinite programming. IEEE Transactions on Information Theory, 62(5):2788–2797, 2016.
- <span id="page-22-7"></span>[10] B. Hajek, Y. Wu, and J. Xu. Achieving exact cluster recovery threshold via semidefinite programming: Extensions. IEEE Transactions on Information Theory, 62(10):5918–5937, 2016.
- <span id="page-22-10"></span>[11] S. Janson, T. Łuczak, and A. Rucinski. Random Graphs. Wiley, New York, 2000.
- <span id="page-22-0"></span>[12] F. Krzakala, C. Moore, E. Mossel, J. Neeman, A. Sly, L. Zdeborová, and P. Zhang. Spectral redemption in clustering sparse networks. Proceedings of the National Academy of Sciences, 110(52):20935–20940, 2013.
- <span id="page-22-11"></span>[13] L. Lei. Unified `2→∞ eigenspace perturbation theory for symmetric random matrices. arXiv preprint arXiv:1909.04798, 2019.
- <span id="page-22-8"></span>[14] A. Montanari and S. Sen. Semidefinite programs on sparse random graphs and their application to community detection. In Proceedings of the forty-eighth annual ACM symposium on Theory of Computing, pages 814–827, 2016.
- <span id="page-22-1"></span>[15] E. Mossel, J. Neeman, and A. Sly. Consistency thresholds for the planted bisection model. Electronic Journal of Probability, 21:1–24, 2016.
- <span id="page-22-3"></span>[16] M. E. Newman. Spectral methods for community detection and graph partitioning. Physical Review E, 88(4):042822, 2013.
- <span id="page-22-4"></span>[17] S.-Y. Yun and A. Proutiere. Accurate community detection in the stochastic block model via spectral algorithms. arXiv preprint arXiv:1412.7335, 2014.

### <span id="page-22-12"></span>A Supporting results for spectral algorithm analysis

In this section, we complete the proofs of Lemmas [5.1,](#page-9-4) [5.2,](#page-9-9) and [5.4.](#page-11-1)

Proof. (Proof of Lemma [5.1\)](#page-9-4). We use ideas from the proof of Theorem 9 in [\[10\]](#page-22-7). Throughout the proof, we condition on the realization of σ0, without writing so explicitly. We first bound E [kA − A?k2]. Let A<sup>0</sup> be an independent copy of A. By Jensen's inequality,

$$\mathbb{E}[\|A - A^{\star}\|_{2}] = \mathbb{E}[\|A - \mathbb{E}[A']\|_{2}] \le \mathbb{E}[\|A - A'\|_{2}].$$

Let R be a matrix of iid Rademacher random variables, and let ◦ denote the elementwise product. Then

$$\mathbb{E}[\|A - A'\|_2] = \mathbb{E}[\|(A - A') \circ R\|_2] \le 2\mathbb{E}[\|A \circ R\|_2].$$

Let D be a matrix with the same distribution as A ◦ R, so that E [kA ◦ Rk2] = E [kDk2]. Note that the entries of D are independent, and the distribution of Dij depends on whether σ0(i) = σ0(j). Let B be the matrix where Bij = 1 − y if Dij = y and Bij = y − 1 if Dij = −y, and is equal to zero otherwise. By definition, the matrix D + B has entries in {−1, 0, 1}. For i 6= j, we have

$$\mathbb{P}((D+B)_{ij}=1) = \mathbb{P}((D+B)_{ij}=-1) = \frac{1}{2}\alpha, \quad \mathbb{P}((D+B)_{ij}=0) = 1-\alpha,$$

regardless of the communities of i and j. The entries of D+B are independent. We decompose B into  $B=B^{(p)}+B^{(q)}$ , as follows. Set  $B_{ij}^{(p)}=0$  whenever  $\sigma_0(i)\neq\sigma_0(j)$  or i=j. Otherwise,

$$B_{ij}^{(p)} = \begin{cases} 1 - y & \text{with probability } \frac{1}{2}\alpha(1 - p) \\ y - 1 & \text{with probability } \frac{1}{2}\alpha(1 - p) \\ 0 & \text{otherwise.} \end{cases}$$

Similarly, set  $B_{ij}^{(q)} = 0$  whenever  $\sigma_0(i) = \sigma_0(j)$ . Otherwise,

$$B_{ij}^{(q)} = \begin{cases} 1 - y & \text{with probability } \frac{1}{2}\alpha(1 - q) \\ y - 1 & \text{with probability } \frac{1}{2}\alpha(1 - q) \\ 0 & \text{otherwise.} \end{cases}$$

Note that  $\mathbb{E}\left[B_{ij}^{(p)}\right] = \mathbb{E}\left[B_{ij}^{(q)}\right] = 0$ . Continuing,

$$\begin{split} \mathbb{E}\left[\|A \circ R\|_2\right] &= \mathbb{E}\left[\|D\|_2\right] \\ &= \mathbb{E}\left[\left\|D + B - B^{(p)} - B^{(q)}\right\|_2\right] \\ &\leq \mathbb{E}\left[\|D + B\|_2\right] + \mathbb{E}\left[\left\|B^{(p)}\right\|_2\right] + \mathbb{E}\left[\left\|B^{(q)}\right\|_2\right]. \end{split}$$

Let  $\overline{B}^{(p)}$  and  $\overline{B}^{(q)}$  be distributed as follows, independent of all other variables. Set  $\overline{B}_{ij}^{(p)} = 0$  whenever  $\sigma_0(i) = \sigma_0(j)$  (note that this is the opposite condition as for  $B^{(p)}$ ). Otherwise,

$$\overline{B}_{ij}^{(p)} = \begin{cases} 1 - y & \text{with probability } \frac{1}{2}\alpha(1 - p) \\ y - 1 & \text{with probability } \frac{1}{2}\alpha(1 - p) \\ 0 & \text{otherwise.} \end{cases}$$

Similarly, set  $\overline{B}_{ij}^{(q)}=0$  whenever  $\sigma_0(i)\neq\sigma_0(j)$  or i=j. Otherwise,

$$\overline{B}_{ij}^{(q)} = \begin{cases} 1-y & \text{with probability } \frac{1}{2}\alpha(1-q) \\ y-1 & \text{with probability } \frac{1}{2}\alpha(1-q) \\ 0 & \text{otherwise.} \end{cases}$$

Note that these distributions are symmetric and  $\mathbb{E}\left[\overline{B}_{ij}^{(p)}\right] = \mathbb{E}\left[\overline{B}_{ij}^{(q)}\right] = 0$  for all i, j. Applying Jensen's inequality again,

$$\begin{split} \mathbb{E}\left[\|A\circ R\|_2\right] &\leq \mathbb{E}\left[\|D-B\|_2\right] + \mathbb{E}\left[\left\|B^{(p)} + \mathbb{E}\left[\overline{B}^{(p)}\right]\right\|_2\right] + \mathbb{E}\left[\left\|B^{(q)} + \mathbb{E}\left[\overline{B}^{(q)}\right]\right\|_2\right] \\ &\leq \mathbb{E}\left[\|D-B\|_2\right] + \mathbb{E}\left[\left\|B^{(p)} + \overline{B}^{(p)}\right\|_2\right] + \mathbb{E}\left[\left\|B^{(q)} + \overline{B}^{(q)}\right\|_2\right]. \end{split}$$

Let X(r) denote the zero-diagonal matrix whose non-diagonal entries are i.i.d according to  $\mu(r) = \frac{r}{2}\delta_1 + \frac{r}{2}\delta_{-1} + (1-r)\delta_0$ . We have

$$\mathbb{E}\left[\|D - B\|_2\right] = \mathbb{E}\left[\|X(\alpha)\|_2\right]$$

$$\mathbb{E}\left[\left\|B^{(p)} + \overline{B}^{(p)}\right\|_2\right] = (1 - y)\mathbb{E}\left[\|X(\alpha(1 - p))\|_2\right]$$

$$\mathbb{E}\left[\left\|B^{(q)} + \overline{B}^{(q)}\right\|_2\right] = (1 - y)\mathbb{E}\left[\|X(\alpha(1 - q))\|_2\right].$$

For  $r \ge c_0 \frac{\log n}{n}$ ,

$$\mathbb{E}\left[\|X(r)\|_2\right] \le c_2 \sqrt{nr},$$

for  $c_2$  depending only on  $c_0$  (see e.g. [10, Theorem 9]). Putting everything together,

$$\mathbb{E}\left[\|A - A^{\star}\|_{2}\right] \leq 2\left[c_{2}(t)\sqrt{n\alpha} + (1 - x)c_{2}\left(t(1 - p)\right)\sqrt{n\alpha(1 - p)} + (1 - x)c_{2}\left(t(1 - q)\right)\sqrt{n\alpha(1 - q)}\right] \leq c_{3}(p, q, t)\sqrt{\log(n)},$$

for some constant  $c_3(p, q, t)$  depending only on p, q, and t. Applying Talagrand's concentration inequality for bounded Lipschitz functions as in the proof of [10, Theorem 9] concludes the proof.

*Proof.* (Proof of Lemma 5.2). We follow the proof of Lemma 7 in [4], deriving a Chernoff bound. Without loss of generality we may assume  $||w||_{\infty} = 1$ . Let  $S_n = \sum_{i=1}^n w_i(X_i - \mathbb{E}[X_i])$ . We prove the upper tail inequality first. For  $\lambda, r > 0$ ,

$$\mathbb{P}(S_n \ge r) = \mathbb{P}\left(e^{\lambda S_n} \ge e^{\lambda r}\right)$$

$$\le e^{-\lambda r} \mathbb{E}\left[e^{\lambda S_n}\right]$$

$$= e^{-\lambda r} \prod_{i=1}^n \mathbb{E}\left[e^{\lambda w_i(X_i - \mathbb{E}[X_i])}\right].$$

Computing the moment generating function,

$$\mathbb{E}\left[e^{\lambda w_i(X_i - \mathbb{E}[X_i])}\right] = e^{-\lambda w_i(p_i - q_i y)} \mathbb{E}\left[e^{\lambda w_i X_i}\right]$$
$$= e^{-\lambda w_i(p_i - q_i y)} \left(p_i e^{\lambda w_i} + q_i e^{-\lambda y w_i} + 1 - p_i - q_i\right)$$

Taking the logarithm and applying  $\log(1+x) \le x$  for x > -1 and  $e^x \le 1 + x + \frac{e^z}{2}x^2$  for  $|x| \le z$ ,

$$\log \left( \mathbb{E} \left[ e^{\lambda w_{i}(X_{i} - \mathbb{E}[X_{i}])} \right] \right)$$

$$= -\lambda w_{i}(p_{i} - q_{i}y) + \log \left( p_{i}e^{\lambda w_{i}} + q_{i}e^{-\lambda yw_{i}} + 1 - p_{i} - q_{i} \right)$$

$$\leq -\lambda w_{i}(p_{i} - q_{i}y) + p_{i} \left( e^{\lambda w_{i}} - 1 \right) + q_{i} \left( e^{-\lambda yw_{i}} - 1 \right)$$

$$\leq -\lambda w_{i}(p_{i} - q_{i}y) + p_{i} \left( \lambda w_{i} + \frac{e^{\lambda \|w\|_{\infty}}}{2} \left( \lambda w_{i} \right)^{2} \right) + q_{i} \left( -\lambda yw_{i} + \frac{e^{\lambda y\|w\|_{\infty}}}{2} \left( \lambda yw_{i} \right)^{2} \right)$$

$$= \frac{\lambda^{2}w_{i}^{2}}{2} \left( p_{i}e^{\lambda \|w\|_{\infty}} + q_{i}y^{2}e^{\lambda y\|w\|_{\infty}} \right)$$

$$\leq \frac{\lambda^{2}w_{i}^{2} \max\{1, y^{2}\} \exp\left(\lambda \cdot \max\{1, y\}\|w\|_{\infty}\right)}{2} (p_{i} + q_{i}).$$

Therefore, using  $||w||_{\infty} = 1$ ,

$$\log (\mathbb{P}(S_n \ge r)) \le -\lambda r + \frac{\lambda^2 ||w||_2^2 \max\{1, y^2\} \exp(\lambda \cdot \max\{1, y\})}{2} \max_i \{p_i + q_i\}.$$

Choose

$$\lambda = \frac{1}{\max\{1, y\}} \left( 1 \vee \log \left( \frac{\sqrt{n}}{\|w\|_2} \right) \right) > 0.$$

We then have

$$\exp\left(\lambda \cdot \max\{1, y\}\right) = e \vee \frac{\sqrt{n}}{\|w\|_2} \le \frac{e\sqrt{n}}{\|w\|_2}.$$

Note that  $||w||_2 \le \sqrt{n}||w||_{\infty} = \sqrt{n}$ . Using  $1 \lor \log x \le \sqrt{x}$  for  $x \ge 1$ ,

$$\lambda^2 \|w\|_2^2 \exp\left(\lambda \cdot \max\{1, y\}\right) \le \lambda^2 e \sqrt{n} \|w\|_2$$

$$\begin{split} &\leq \frac{1}{(\max\{1,y\})^2} \left(1 \vee \log\left(\frac{\sqrt{n}}{\|w\|_2}\right)\right)^2 e \sqrt{n} \|w\|_2 \\ &\leq \frac{en}{\max\{1,y^2\}}. \end{split}$$

Substituting,

$$\log (\mathbb{P}(S_n \ge r)) \le -\lambda r + \frac{en}{2} \max_{i} \{p_i + q_i\}.$$

Let  $r = \lambda^{-1}(2+\beta)n \cdot \max_i \{p_i + q_i\}$ , so that

$$\log \left( \mathbb{P}\left( S_n \ge r \right) \right) \le -(2+\beta)n \cdot \max_{i} \left\{ p_i + q_i \right\} + \frac{en}{2} \max_{i} \left\{ p_i + q_i \right\}$$

$$\le -\beta n \max_{i} \left\{ p_i + q_i \right\}.$$

By replacing w with -w we can obtain a lower tail bound. The proof is complete by a union bound.

*Proof.* (Proof of Lemma 5.4). The derivation is similar to Chernoff bound. Let  $\lambda < 0$  to be determined later. By Markov's inequality,

$$\begin{split} \mathbb{P}\bigg(\sum_{i=1}^{n_1} W_i - \sum_{i=1}^{n_2} Z_i &\leq \varepsilon \log(n)\bigg) &= \mathbb{P}\bigg(\exp\bigg(\lambda \sum_{i=1}^{n_1} W_i - \lambda \sum_{i=1}^{n_2} Z_i\bigg) \geq \exp\big(\lambda \varepsilon \log(n)\big)\bigg) \\ &\leq n^{-\lambda \varepsilon} \mathbb{E}\bigg[\exp\bigg(\lambda \sum_{i=1}^{n_1} W_i - \lambda \sum_{i=1}^{n_2} Z_i\bigg)\bigg]. \end{split}$$

Using  $\log(1+x) \le x$  for x > -1, we have

$$\log \left( \mathbb{E} \left[ e^{\lambda W_i} \right] \right) = \log \left( e^{\lambda} \alpha p + e^{-\lambda y} \alpha (1 - p) + 1 - \alpha \right)$$

$$\leq e^{\lambda} \alpha p + e^{-\lambda y} \alpha (1 - p) - \alpha$$

$$= \alpha \left( e^{\lambda} p + e^{-\lambda y} (1 - p) - 1 \right).$$

Similarly,

$$\log \left( \mathbb{E} \left[ e^{-\lambda Z_i} \right] \right) \le \alpha \left( e^{-\lambda} q + e^{\lambda y} (1 - q) - 1 \right).$$

Therefore, using  $n_1, n_2 = (1 + o(1)) \frac{n}{2}$ ,

$$\log \mathbb{P}\left(\sum_{i=1}^{n_1} W_i - \sum_{i=1}^{n_2} Z_i \le \varepsilon \log(n)\right)$$

$$\le -\lambda \varepsilon \log(n) + (1 + o(1)) \frac{n}{2} \alpha \left(e^{\lambda} p + e^{-\lambda y} (1 - p) + e^{-\lambda} q + e^{\lambda y} (1 - q) - 2\right)$$

$$= \log(n) \left[-\lambda \varepsilon + \frac{t}{2} \left(e^{\lambda} p + e^{-\lambda y} (1 - p) + e^{-\lambda} q + e^{\lambda y} (1 - q) - 2\right) + o(1)\right].$$

Set  $\lambda = \frac{1}{2} \log \left( \frac{q}{p} \right) < 0$ . Observe that  $e^{\lambda} = \sqrt{\frac{q}{p}}$ , and

$$e^{\lambda y} = \left(\frac{q}{p}\right)^{\frac{\log\left(\frac{1-q}{1-p}\right)}{2\log\left(\frac{p}{q}\right)}} = \sqrt{\frac{1-p}{1-q}}.$$

Therefore,

$$\log \mathbb{P}\bigg(\sum_{i=1}^{\frac{n}{2}} W_i - \sum_{i=1}^{\frac{n}{2}} Z_i \le \varepsilon \log(n)\bigg)$$

$$\leq \log(n) \left[ -\lambda \varepsilon + \frac{t}{2} \left( \sqrt{pq} + \sqrt{(1-p)(1-q)} + \sqrt{pq} + \sqrt{(1-p)(1-q)} - 2 \right) + o(1) \right]$$

$$= \log(n) \left[ -\lambda \varepsilon - \frac{t}{2} \left( (\sqrt{p} - \sqrt{q})^2 + \left( \sqrt{1-q} - \sqrt{1-p} \right)^2 \right) + o(1) \right].$$

#### <span id="page-26-0"></span>B Proof of Poisson approximation

*Proof.* (Proof of Lemma 3.1). To prove the claim, observe that under the assumptions on  $m, m_1, m_2$ , by Stirling's approximation and the fact that  $1 - e^{-x} \approx x$  as  $x \to 0$ ,

$$\frac{m!}{(m-m_1-m_2)!} \approx \frac{\mathrm{e}^{-m}m^{m+\frac{1}{2}}}{\mathrm{e}^{-m+m_1+m_2}(m-m_1-m_2)^{m-m_1-m_2+\frac{1}{2}}}$$

$$= \mathrm{e}^{-m_1-m_2} \frac{(m-m_1-m_2)^{m_1+m_2}}{(1-\frac{m_1+m_2}{m})^{m+\frac{1}{2}}}$$

$$\approx \frac{(m-m_1-m_2)^{m_1+m_2}}{(1-\frac{m_1+m_2}{m})^{\frac{1}{2}}}$$

$$\approx \left(\frac{n}{2}(1+O(\log^{-2}n))\right)^{m_1+m_2}$$

$$\approx \left(\frac{n}{2}\right)^{m_1+m_2},$$

where in the last step we have used  $m_1, m_2 = o(\log^{3/2} n)$  and the fact that  $(1+x)^l \approx 1 + lx$  when  $lx \to 0$ . Also,

$$(1-\alpha)^{m-m_1-m_2} \simeq e^{-\alpha(m-m_1-m_2)} \simeq e^{-t\log(n)/2}$$

Thus,

$$\mathbb{P}(N_a = m_1, N_b = m_2) = \frac{m!}{m_1! m_2! (m - m_1 - m_2)!} (\alpha p)^{m_1} (\alpha (1 - p))^{m_2} (1 - \alpha)^{m - m_1 - m_2}$$

$$\approx e^{-\frac{t \log n}{2}} \frac{(\frac{tp \log n}{2})^{m_1} (\frac{t(1 - p) \log n}{2})^{m_2}}{m_1! m_2!},$$

and thus the proof follows.  $\square$ 

### <span id="page-26-1"></span>C Proof of genie estimator characterization

Proof. (Proof of Proposition 6.1). Recall the definition of the degree profile above (2.6), and also, recall from (4.1) that the MAP estimator equals the MLE under a uniform prior. Fix  $u \in [n]$ , and let  $\sigma_1, \sigma_{-1} \in \mathcal{S}$  be such that  $\sigma_1(u) = +1, \sigma_{-1}(u) = -1$  and  $\sigma_1(v) = \sigma_{-1}(v)$  for all  $v \in [n] \setminus \{u\}$ . For a fixed edge-labeled graph g, suppose u has degree profile  $D(\sigma_1, u) = (d_1(u), d_2(u), d_3(u), d_4(u))$ . By definition,  $D(\sigma_1, u) = D(\sigma_{-1}, u)$ .

$$\mathbb{P}(G = g \mid \sigma_0 = \sigma_1) 
= Z \times \binom{n_1(\sigma_1) - 1}{d_1(u), d_2(u)} \binom{n_2(\sigma_1)}{d_3(u), d_4(u)} (\alpha p_1)^{d_1(u)} (\alpha (1 - p_1))^{d_2(u)} 
(\alpha q)^{d_3(u)} (\alpha (1 - q))^{d_4(u)} (1 - \alpha)^{n-1 - \sum_i d_i(u)},$$

where Z is not dependent on u. Similarly

$$\mathbb{P}(G = g \mid \sigma_0 = \sigma_{-1}) \\
= Z \times \binom{n_1(\sigma_{-1})}{d_1(u), d_2(u)} \binom{n_2(\sigma_{-1}) - 1}{d_3(u), d_4(u)} (\alpha q)^{d_1(u)} (\alpha (1 - q))^{d_2(u)}$$

$$(\alpha p_2)^{d_3(u)}(\alpha (1-p_2))^{d_4(u)}(1-\alpha)^{n-1-\sum_i d_i(u)}$$

.

Moreover, n1(σ−1) = n1(σ1) − 1 and n2(σ−1) = n2(σ1) + 1. Therefore, the binomial coefficients above are also equal and

$$\log \frac{\mathbb{P}(G = g \mid \sigma_0 = \sigma_1)}{\mathbb{P}(G = g \mid \sigma_0 = \sigma_{-1})} = d_1(u) \log \frac{p_1}{q} + d_2(u) \log \frac{1 - p_1}{1 - q} + d_3(u) \log \frac{q}{p_2} + d_4(u) \log \frac{1 - q}{1 - p_2}.$$

The genie estimator returns +1 if and only if the log likelihood ratio is non-negative. Hence, the proof of Proposition [6.1](#page-12-0) follows.