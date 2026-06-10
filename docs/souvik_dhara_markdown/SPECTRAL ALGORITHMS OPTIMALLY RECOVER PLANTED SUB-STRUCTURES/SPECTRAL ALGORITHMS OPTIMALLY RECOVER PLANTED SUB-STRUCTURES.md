## SPECTRAL ALGORITHMS OPTIMALLY RECOVER PLANTED SUB-STRUCTURES

SOUVIK DHARA? , JULIA GAUDIO† , ELCHANAN MOSSEL‡ , COLIN SANDON

Abstract. Spectral algorithms are an important building block in machine learning and graph algorithms. We are interested in studying when such algorithms can be applied directly to provide optimal solutions to inference tasks. Previous works by Abbe, Fan, Wang and Zhong (2020) and by Dhara, Gaudio, Mossel and Sandon (2022) showed the optimality for community detection in the Stochastic Block Model (SBM), as well as in a censored variant of the SBM. Here we show that this optimality is somewhat universal as it carries over to other planted substructures such as the planted dense subgraph problem and submatrix localization problem, as well as to a censored version of the planted dense subgraph problem.

# 1. Introduction

Spectral algorithm are an important building block in machine learning and graph algorithms. We are interested in studying when such algorithms can be applied directly to provide optimal solutions. We study the applicability of such algorithm to the problem of finding dense matrix in a large structure. The problem of finding dense structure in a large matrix is an important machine learning task on network data. A canonical probabilistic formulation of this problem is made by "planting" a dense substructure hidden under random noise. More precisely, consider a symmetric n × n matrix X, and suppose there is an unknown subset S ? ⊂ [n] such that Xij ∼ P if i, j ∈ S ? and Xij ∼ Q otherwise, where P and Q are two distributions with different means. The goal is to recover S ? based on an observation of X. If P, Q are Bernoulli distributions, the corresponding problem is referred to as the planted dense subgraph problem (PDS), which is a generalization of the well-known planted clique problem [\[3,](#page-26-0) [15\]](#page-27-0). The case where P, Q are Normal distributions is known as the submatrix localization problem (SL) [\[13,](#page-27-1) [16\]](#page-27-2) in the high-dimensional statistics literature. The central questions in these areas are: (1) designing efficient algorithms for recovering the planted substructure, (2) finding parameter regimes when the recovery would be information theoretically impossible, as well as (3) showing parameter regimes where the recovery would be information theoretically possible, but known algorithms would fail (i.e. there is a computational versus statistical gap). We refer the reader to the survey of Wu and Xu [\[18\]](#page-27-3) for a detailed account on the recent developments on this topic and further references.

If the size of the planted subset is |S ? | = Θ(n), then there is no computational versus statistical gap, as shown by Hajek, Wu, and Xu [\[9,](#page-27-4) [10,](#page-27-5) [11,](#page-27-6) [12\]](#page-27-7). We will focus on this regime throughout the paper. In this case, semidefinite programming (SDP) relaxation of the Maximum-Likelihood estimator [\[10,](#page-27-5) [11\]](#page-27-6) recovers the hidden subset S ? in both the PDS and SL problems, up to the

<sup>(</sup> ? ) The Simons Institute for the Theory of Computing, University of California, Berkeley

<sup>(</sup> ) Department of Industrial Engineering and Management Sciences, Northwestern University

<sup>(</sup> ) Department of Mathematics, Massachusetts Institute of Technology

E-mail address: [dharasouvik1991@gmail.com,](mailto:dharasouvik1991@gmail.com)[julia.gaudio@northwestern.edu,](mailto:julia.gaudio@northwestern.edu) [elmos@mit.edu,](mailto:elmos@mit.edu) [csandon@comcast.net](mailto:csandon@comcast.net).

Acknowledgement: S.D., E.M., and C.S. were partially supported by Vannevar Bush Faculty Fellowship ONR-N00014-20-1-2826. S.D. was supported by Simons-Berkeley Research Fellowship. E.M. and C.S. were partially supported by NSF award DMS-1737944. E.M. was partially supported by Simons Investigator award (622132) and by ARO MURI W911NF1910217. J.G. was partially supported by NSF award CCF-2154100. Part of this work was completed while S.D and C.S. were at the MIT Mathematics Department.

information-theoretic thresholds. An algorithm based on degree-thresholding and voting is also optimal for exact recovery in the PDS model [9, Appendix A]; message-passing [12] is also optimal for the SL model.

Our main interest in this paper is in studying the following two aspects of these planted recovery problems:

- We are interested in the power of spectral algorithms, which are simple, efficient, and widely used.
- We consider a *censored* version of the planted dense subgraph problem. Here the statuses of some edges are unknown as is often the case in real network inference problems.

We note that some applications of spectral algorithms to the exact recovery problem use an additional combinatorial clean-up stage (see e.g. [5, 17, 19]), but we follow [1, 7] in studying spectral algorithms without a clean-up stage. This is partially motivated by the fact that most real applications of spectral algorithms do not include a combinatorial clean-up stage. Moreover, spectral algorithms are highly efficient; spectral decomposition can be computed in  $O(n^{\omega})$  time [4], and in fact, finding only the top eigenvectors using power-iteration on sparse random matrices takes only  $O(n \log^2 n)$  time; see Remark 2.1.

This gives rise to the following main questions that we address in this paper:

Are there simple spectral algorithms that are optimal for recovering planted substructures? If so, can we design optimal algorithms when additionally there is missing data?

### Our Contributions.

- (1) We first study spectral algorithms for PDS and SL models in the set up of Hajek, Wu and Xu [10, 11]. We show for the SL model, a simple spectral algorithm based on thresholding the top eigenvector of the underlying random matrix X succeeds in exact recovery up to the information theoretic threshold (Theorem 2.2). In the PDS model, a similar algorithm based on thresholding a suitable linear combination of the top two eigenvectors of the random matrix is optimal (Theorem 2.1).
- (2) Next we consider the recovery problem in the censored version when the information about the edge statuses are missing at random (see Definition 1.1). To the best of our knowledge, the PDS model with missing data had not been studied in the literature. We obtain the information theoretic threshold in the censored set up (see Theorem 1.4). The spectral algorithm based on X is not always optimal. To design an efficient spectral algorithm, we consider an operator called the signed adjacency matrix (see (2.1)), and show that a linear combination of the top two eigenvectors of this signed adjacency matrix can recover the PDS up to the information theoretic threshold (see Theorem 2.3). Our results focus on the parameter regimes where there are no computational versus statistical gaps, and handle more general censoring regimes than what was considered in prior work on spectral algorithms for community detection [7].

Our proofs follow a similar pattern for all models considered. Indeed our results and proofs show that the optimality of spectral algorithms is somewhat universal.

1.1. **Model description and objective.** We start by describing the models for the planted subgraph recovery problem, a version of this model with missing data, and the submatrix localization problem.

<span id="page-1-0"></span>**Definition 1.1** (PDS and Censored PDS model). In the *Planted Dense Subgraph Problem*, there are n vertices, labeled  $\{1, 2, ..., n\}$  and  $S^*$  is drawn uniformly at random from all size-K subsets of [n]. A pair of vertices  $\{i, j\}$  is connected with probability p if  $i, j \in S^*$ . Otherwise, the pair is connected with a different probability q. We refer to this as the PDS model, denoted by PDS(p, q, K).

In the Censored Planted Dense Subgraph Problem, we additionally have each edge status being revealed to us independently with probability  $\alpha$ . In this case, the output is a graph with edge statuses given by {present, absent, censored}. We denote this model by CPDS $(p, q, \alpha, K)$ .

**Definition 1.2** (SL model). In the Submatrix Localization (SL) Problem, we have an  $n \times n$  symmetric matrix A. As before,  $S^*$  is drawn uniformly at random from all size-K subsets of [n]. The entries of  $(A_{ij})_{i \leq j}$  are independent, and  $A_{ij} \sim \text{NORMAL}(\mu, 1)$  if  $i, j \in S^*$ , and  $A_{ij} \sim \text{NORMAL}(0, 1)$  otherwise. Throughout, we assume that  $\mu > 0$ . We denote this model by  $A \sim \text{SL}(\mu, K)$ .

**Objective.** Suppose  $S^*$  is unknown. We want to recover  $S^*$  exactly, i.e., we want to find an estimator  $\hat{S}_n \subset [n]$  such that

$$\lim_{n \to \infty} \mathbb{P}(\hat{S}_n = S^*) = 1. \tag{1.1}$$

<span id="page-2-4"></span>Throughout, we will assume that the parameters such as  $K, p, q, \alpha, \mu$  are known.

#### 1.2. Main results.

<span id="page-2-0"></span>The PDS problem. We will first consider spectral recovery on the PDS model for the regime where

$$p = \frac{a \log n}{n}, \quad q = \frac{b \log n}{n}, \quad K = \lfloor \rho n \rfloor, \quad a, b, \rho \text{ are fixed constants.}$$
 (1.2)

<span id="page-2-3"></span>To state the result, define

$$f(a,b) := a - \left(\frac{a-b}{\log a - \log b}\right) \log \left(\frac{\operatorname{e}a(\log a - \log b)}{a-b}\right),\tag{1.3}$$

for a, b > 0 such that  $a \neq b$ . Additionally, (for  $a, b \geq 0$ ) define f(a, 0) = a, f(0, b) = b, and f(a, a) = 0. The function f(a, b) is symmetric in its arguments. Our first main result is the following

<span id="page-2-2"></span>**Theorem 1.1.** Consider the PDS model with parameters given by (1.2). If  $\rho f(a,b) > 1$ , then there is a spectral algorithm that outputs  $\hat{S}_n$  such that  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

<span id="page-2-1"></span>The spectral algorithm is based on a linear combination of the top two eigenvectors of the adjacency matrix as described in Algorithm 2, and in particular, does not require additional combinatorial clean-up steps. Hajek et al. [10] showed that the recovery of  $S^*$  is information theoretically impossible if  $\rho f(a,b) < 1$ . Therefore, Theorem 2.1 shows that a spectral algorithm works up to the information theoretic threshold. The achievability and impossibility parameter regimes in the PDS model are summarized by Figure 1.

![](_page_2_Figure_15.jpeg)

Figure 1. Phase diagram for the PDS model, for  $\rho = \frac{1}{4}$ . In the green region, estimation of  $S^*$  is possible by a spectral algorithm, while in the blue region, it is information-theoretically impossible.

The SL problem. Next, we state the results about spectral recovery for the SL model when

<span id="page-3-1"></span>
$$\mu = a\sqrt{\frac{\log n}{n}}, \quad K = \lfloor \rho n \rfloor, \quad a, \rho \text{ are fixed constants.}$$
 (1.4)

<span id="page-3-2"></span>**Theorem 1.2.** Consider the SL model with parameters given by (1.4), and assume that  $\rho a^2 > 8$ . Then there is a spectral algorithm that outputs  $\hat{S}_n$  such that  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

The spectral algorithm for the SL model only needs to consider the top eigenvector of the underlying matrix (see Algorithm 3) as compared to top two eigenvectors for the PDS model. The fact that exact recovery of  $S^*$  is information theoretically impossible for  $\rho a^2 < 8$  was proven by Hajek et al. [11].

The CPDS problem. Next, we discuss multiple results about the censored model. To the best of our knowledge, this model was not studied in the prior literature. Interestingly, if  $p, q = \Omega(1)$ , then the naïve spectral algorithm based on the adjacency matrix with missing entries replaced by 0 does not lead to an optimal algorithm. Instead, we have to consider a spectral algorithm using a ternary encoding matrix called the signed adjacency matrix that encodes information about the labels {present, absent, censored}. However, the above naïve spectral algorithm turns out to be optimal when p, q = o(1).

The results for the CPDS model will be stated in terms of a Chernoff-Hellinger divergence, introduced by Abbe and Sandon [2].

**Definition 1.3** (Chernoff-Hellinger Divergence). Given two vectors  $\mu, \nu \in (\mathbb{R}_+ \setminus \{0\})^k$ , define

$$D_x(\mu, \nu) = \sum_{i \in [k]} \left[ x\mu_i + (1 - x)\nu_i - \mu_i^x \nu_i^{1 - x} \right] \quad \text{for } x \in [0, 1].$$

<span id="page-3-6"></span>The Chernoff–Hellinger divergence of  $\mu$  and  $\nu$  is defined as

$$\Delta_{+}(\mu,\nu) = \max_{x \in [0,1]} D_x(\mu,\nu). \tag{1.5}$$

Given  $p, q \in [0, 1]$ , we simply write  $\Delta_+(p, q)$  for  $\Delta_+((p, 1 - p), (q, 1 - q))$ . We also define  $\Delta_+(p, q)$  when  $|\{p, q\} \cap \{0, 1\}| \ge 1$  by taking the continuous extension, which yields  $\Delta_+(p, q) = |p - q|$  in these cases.

The first main result for the CPDS model is the following.

<span id="page-3-3"></span>**Theorem 1.3.** Consider the CPDS $(p,q,\alpha,K_n)$  model from Definition 1.1 with  $K_n = \lfloor \rho n \rfloor$ ,  $\alpha_n = t \log n/n$  for some fixed  $\rho, p, q \in (0,1)$  and t > 0. Suppose that  $t\rho\Delta_+(p,q) > 1$ . Then there is a spectral algorithm whose output  $\hat{S}_n$  satisfies  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

As remarked earlier, the spectral algorithm (Algorithm 4) in this case uses a signed adjacency matrix. The next result finds the information theoretic threshold for the CPDS model.

<span id="page-3-0"></span>**Theorem 1.4.** Consider the CPDS $(p, q, \alpha, K_n)$  model from Definition 1.1 with  $K_n = \lfloor \rho n \rfloor$  for some fixed  $\rho \in (0, 1)$ . Suppose that  $\min(p_n, q_n, 1 - p_n, 1 - q_n) = n^{-o(1)}$ , and

$$\limsup_{n \to \infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) < 1. \tag{1.6}$$

<span id="page-3-5"></span>Given the unlabeled observation G from  $CPDS(p, q, K, \alpha)$ , we have that any estimator  $\hat{S}_n$  satisfies  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 0$ .

<span id="page-3-4"></span>The achievability and impossibility parameter regimes in the CPDS model are summarized by Figure 2, in the case where p, q, t, and  $\rho$  are constants. Next, we relate the achievability conditions for the PDS and the CPDS problems. In particular, we prove the following.

<span id="page-4-0"></span>![](_page_4_Figure_2.jpeg)

Figure 2. Phase diagram for the CPDS model, for  $\rho = \frac{1}{4}$  and t = 100. In the green region, estimation of  $S^*$  is possible by a spectral algorithm, while in the blue region, it is information-theoretically impossible.

**Lemma 1.5.** Let a, b > 0 be constants. Suppose  $\alpha_n = \frac{t_n \log n}{n}$ ,  $\lim_{n \to \infty} p_n t_n = a$ , and  $\lim_{n \to \infty} q_n t_n = b$ , where  $p_n, q_n = o(1)$ . Then  $\lim_{n \to \infty} t_n \Delta_+(p_n, q_n) = f(a, b)$ .

In light of this lemma, we now have the following result for the CPDS problem that exhibits the identical recovery regime when  $p_n, q_n = o(1)$  as compared to the PDS problem in Theorem 1.1.

<span id="page-4-2"></span>Corollary 1.6. Consider the CPDS $(p_n, q_n, \alpha_n, K_n)$  model from Definition 1.1 with  $K_n = \lfloor \rho n \rfloor$ , where  $\rho \in (0, 1)$  is fixed. Let a, b > 0 be constants satisfying  $\alpha_n p_n = \frac{a \log n}{n}$ ,  $\alpha_n q_n = \frac{b \log n}{n}$ . Moreover, let  $p_n, q_n = o(1)$ . If  $\rho f(a, b) > 1$ , then there is a spectral algorithm that recovers  $S^*$  with probability 1 - o(1).

*Proof.* Let A' be the matrix where  $A'_{ij} = 1$  if the edge  $\{i, j\}$  is present and  $A'_{ij} = 0$  otherwise. That is, we encode both the censored and absent edges by 0. Observe that A' is distributed as the adjacency matrix of  $PDS(\frac{a \log n}{n}, \frac{b \log n}{n}, K_n)$ . The statement then follows from Theorem 1.1.

Finally, we consider the optimality of spectral algorithms under a more general parameter regime.

<span id="page-4-1"></span>**Theorem 1.7.** Consider the CPDS $(p_n, q_n, \alpha_n, K_n)$  model from Definition 1.1 with  $K_n = \lfloor \rho n \rfloor$ , where  $\rho \in (0, 1)$  is fixed. Let a, b > 0 be constants satisfying  $\alpha_n p_n = \frac{a \log n}{n}$ ,  $\alpha_n q_n = \frac{b \log n}{n}$ . Then the following hold:

- (1) If  $\liminf_{n\to\infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) > 1$ , then there is a spectral algorithm that recovers  $S^*$  with probability 1 o(1).
- (2) If  $\limsup_{n\to\infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) < 1$  and  $\min(1-p_n, 1-q_n) = n^{-o(1)}$ , then every algorithm fails to recover  $S^*$  with probability 1-o(1).

The following result follows directly from Theorem 1.7, complementing Corollary 1.6.

Corollary 1.8. Under the assumptions of Corollary 1.6, if  $\rho f(a,b) < 1$ , then every algorithm fails to recover  $S^*$  with probability 1 - o(1).

1.3. **Proof ideas.** We first give some intuition behind the success of spectral algorithms for estimating  $S^*$  for the PDS problem. The ideas for the SL problem are similar in spirit. Let  $A^* = \mathbb{E}[A]$  be the expected value of the adjacency matrix. Then  $A^*$  is a rank-2 matrix with two non-zero eigenpairs  $(\lambda_1^*, u_1^*)$  and  $(\lambda_2^*, u_2^*)$ , where  $\lambda_1^* \geq \lambda_2^*$ . Both eigenvectors are block eigenvectors, taking on one value on entries corresponding to  $S^*$ , and another value on entries corresponding to  $[n] \setminus S^*$ . Given the matrix A, we can compute its eigenpairs  $(\lambda_1, u_1), (\lambda_2, u_2), \ldots$ , where  $\lambda_1 \geq \lambda_2 \geq \cdots$ . Drawing on eigenvector perturbation theory, one might expect  $u_1, u_2$  to qualitatively behave like  $u_1^*, u_2^*$ . However, for the exact recovery problem, one needs a strong bound on the  $\ell_{\infty}$  norm, referred to as an entrywise

perturbation bound. That is, if it were the case that  $||u_1 - u_1^*||_{\infty}$  and  $||u_2 - u_2^*||_{\infty}$  were small, then we could threshold the values of  $u_1$  or  $u_2$  in order to accurately estimate  $S^*$ .

Unfortunately,  $u_1$  and  $u_2$  are not well enough approximated by  $u_1^*$  and  $u_2^*$  in an entrywise sense. On the other hand, work by Abbe, Fan, Wang and Zhong [1] identifies conditions under which an eigenvector  $u_i$  of a random matrix A is well-approximated by a different vector, namely the ratio  ${}^{Au_i^*}/\lambda_i^*$ . Such a ratio is often straightforward to analyze; in community detection scenarios, each entry of  ${}^{Au_i^*}/\lambda_i^*$  is a weighted summation of independent Bernoulli random variables. Abbe et al. [1] applied their entrywise eigenvector analysis technique in order to show optimality of a simple spectral algorithm for community detection in the SBM (see [1, Theorem 3.2]), in addition to other estimation problems involving matrices ( $\mathbb{Z}_2$ -synchronization and noisy matrix completion). Recently, Dhara, Gaudio, Mossel and Sandon [7] applied the entrywise eigenvector analysis technique to show that a spectral algorithm is optimal for the community detection problem in a censored symmetric stochastic block model, where one has two communities of approximately equal sizes and the edge densities inside the two communities are equal.

One important technical distinction in our work compared to the community detection literature is that in community detection, we seek to determine the communities up to a global flip of the community labels. On the other hand, in the PDS model, we need to specifically identify the vertices within the planted dense subgraph. The entrywise eigenvector analysis technique allows us to bound

$$\min_{s \in \{-1,1\}} \left\| su_i - \frac{Au_i^*}{\lambda_i^*} \right\|_{\infty}.$$

That is, we can show that  $u_i$  or  $-u_i$  is close to  $Au_i^*/\lambda_i^*$  in an entrywise sense, but the technique gives us no way to dissambiguate the two options. Moreover, we use a weighted combination  $u_1$  and  $u_2$  in the PDS algorithm, with weights  $c_1^*$  and  $c_2^*$ . We are able to show that

$$\min_{s_1, s_2 \in \{-1, 1\}} \left\| s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2 - A \left( \frac{c_1^{\star} u_1^{\star}}{\lambda_1^{\star}} + \frac{c_2^{\star} u_2^{\star}}{\lambda_2^{\star}} \right) \right\|_{\infty}$$

is small, so that the recovery performance of  $s_1c_1^*u_1 + s_2c_2^*u_2$  matches the recovery performance of  $A\left(\frac{c_1^*u_1^*}{\lambda_1^*} + \frac{c_2^*u_2^*}{\lambda_2^*}\right)$ , for those  $s_1, s_2$  which minimize the above expression. It remains to determine  $s_1$  and  $s_2$ , which amounts to determining the orientations of  $u_1$  and  $u_2$ . Given two choices for  $s_1$  and  $s_2$ , we obtain four candidate linear combinations, and therefore four candidates estimates of  $S^*$ . In order to determine which one is correct, we choose the one that maximizes the likelihood of the observed adjacancy matrix A. Since choosing the correct orientation amounts to maximizing the likelihood over a restricted number of candidates, we determine the regime where the Maximum Likelihood estimator succeeds in recovering the communities. In this regime, it suffices to show that  $S^*$  is one of the four candidates, with high probability.

The weights  $c_1^*$  and  $c_2^*$  cannot be arbitrary, but must be chosen correctly in order to achieve our optimal results. Using the insight that  $c_1^*u_1 + c_2^*u_2$  (in the correct orientation) behaves like  $v := A\left(\frac{c_1^*u_1^*}{\lambda_1^*} + \frac{c_2^*u_2^*}{\lambda_2^*}\right)$ , we choose the weights so that the vector v optimally recovers the planted dense subgraph. In particular, we choose the weights so that  $v_i = \frac{1}{\sqrt{K}} \sum_{j \in S^*} A_{ij}$ .

The spectral algorithm for the CPDS model is similar in spirit to the spectral algorithm for the PDS model. The key difference is that unlike in the PDS model, where each pair of vertices is associated with one of two possible observations (present, absent), each pair of vertices is associated with one of three possible observations (present, absent, censored). Therefore, the adjacency matrix must be encoded using three numeric values. The choice of encoding matrix in (2.1) is such that it balances the relative information contributed by revealed edges and non-edges. Recently, [7] studied spectral algorithms using such signed adjacency matrices for community detection on a censored version of the stochastic block model. It was shown that while the spectral algorithms using signed adjacency matrices are optimal when the within community edge probabilities are the same, it

may be the case that these spectral algorithms are sub-optimal when the within community edge probabilities are different (cf. [7, Theorem 2.6]). Note that the CPDS model would correspond to a censored stochastic block model, where the within community edge probabilities are different, and moreover, the community sizes are asymptotically unequal. The results in this paper show that these spectral algorithms are still optimal for the recovery problem in CPDS and in particular are in contrast with the counterexamples provided in [7, Theorem 2.6]. Finally, our analysis of the spectral algorithm in the censored case requires us to additionally show that the Maximum Likelihood Estimator (MLE) achieves exact recovery up to the information-theoretic threshold (see Lemma 4.1).

The proof for the impossibility of recovery follows by showing that the Maximum a Posteriori (MAP) estimator, which is an optimal estimator, would fail in recovering  $S^*$ . The idea is closely related to the analysis of the Censored SBM in [7]. We first show that the MAP and MLE are equivalent, and then identify a condition under which the MLE fails to determine  $S^*$ . The condition requires several pairs of vertices, such that if we swap their assignments, the likelihood of the observed graph does not change. If there are enough such pairs, then the MLE is likely to fail in determining  $S^*$ .

### 1.4. Discussion and future work. Our work leaves several directions for future work.

- (1) We focus on the case where  $K = \Theta(n)$ . While the entrywise eigenvector analysis method of [1] allows us to handle slightly sublinear K, it does not allow us to match existing results for SDPs in the PDS and SL problems. When  $K = \omega(n/\log n)$ , the SDP threshold matches the information-theoretic threshold with sharp constants [11]. On the other hand, when  $K = o(n/\log n)$ , then the SDP is order-wise suboptimal [11]. Finally, if  $K = \Theta(n/\log n)$ , then the SDP is suboptimal by a constant factor, though order-wise optimal [11]. It was conjectured that a spectral algorithm would require a stronger signal than the SDP algorithm. Comparing the performance of SDPs and spectral algorithms for sublinear K is an interesting avenue for future work.
- (2) In the CPDS model, can we consider a more general censoring distribution that can model the case where the edges' statuses are not missing at random?

**Organization.** The remainder of the paper is structured as follows. We start by setting up some preliminary notation below. In Section 2 we provide the main algorithms and state the main algorithmic results. The analyses of the spectral algorithms for PDS and CPDS are provided respectively in Sections 3 and 4. We prove the impossibility result for CPDS in Section 5, in addition to demonstrating the tightness of our results under a more general parameter regime. The spectral recovery in the SL problem is analyzed in Section 6.

**Notation.** For a vector  $x \in \mathbb{R}^n$ , we define  $||x||_2 = (\sum_{i=1}^n x_i^2)^{1/2}$  and  $||x||_\infty = \max_i |x_i|$ . For a matrix  $M \in \mathbb{R}^{n \times d}$ , we use  $M_i$  to refer to its i-th row, represented as a row vector. Given a matrix M,  $||M||_2 = \max_{||x||_2=1} ||Mx||_2$  is the spectral norm, and  $||M||_{2\to\infty} = \max_i ||M_i||_2$  is the matrix  $2 \to \infty$  norm. We use the convention that log denotes natural logarithm, and write  $\log^k(n)$  to mean  $(\log(n))^k$ . Finally, given two sequences  $\{s_n\}_{n=1}^\infty$  and  $\{r_n\}_{n=1}^\infty$ , we write  $s_n \asymp r_n$  when  $\lim_{n\to\infty} \frac{s_n}{r_n} = 1$ .

### 2. Main Algorithms

<span id="page-6-1"></span><span id="page-6-0"></span>2.1. **Spectral recovery of PDS.** We will first consider spectral recovery in the PDS model for the regime when the parameters are given by (1.2). The algorithm uses a linear combination of the top two eigenvectors of the adjacency matrix. Let us start by describing how to calculate the coefficients of this linear combination:

**Input:** An  $n \times n$  matrix B of rank 2, and a  $K \in \mathbb{N}$ .

Output: A pair of weights.

- 1: Find the top two eigenpairs of B, denoting them  $(\gamma_1, w_1)$  and  $(\gamma_1, w_2)$ , where  $\gamma_1 \geq \gamma_2$ .
- 2: Letting  $v_{S^*}$  be the vector whose first K entries are  $1/\sqrt{K}$  and whose other entries are 0, let  $c_1^*$ and  $c_2^{\star}$  be such that

$$\frac{c_1^* \log(n)}{\gamma_1} w_1 + \frac{c_2^* \log(n)}{\gamma_2} w_2 = v_{S^*}.$$

3: Return  $(c_1^*, c_2^*)$ .

Based on the weights above, we now describe the spectral algorithm:

### <span id="page-7-2"></span>**Algorithm 2** Spectral recovery in the PDS model

**Input:** Parameters a, b, and K; an adjacency matrix A of PDS model with parameters in (1.2).

Output: An estimate of the planted dense subgraph vertices.

- 1: Let B be the matrix where  $B_{ij} = \frac{a \log n}{n}$  when  $i, j \leq K$ , and  $B_{ij} = \frac{b \log n}{n}$  otherwise. 2: Apply Algorithm 1 to (B, K), obtaining the weights  $(c_1^{\star}, c_2^{\star})$ .
- 3: Compute the top two eigenpairs of A, denoting them  $(\lambda_1, u_1)$  and  $(\lambda_2, u_2)$ , where  $\lambda_1 \geq \lambda_2 \geq \cdots$ .
- 4: Let  $U = \{s_1 c_1^* u_1 + s_2 c_2^* u_2 : s_1, s_2 \in \{-1, 1\}\}.$
- 5: For each  $u \in U$  identify  $\hat{S}(u)$  as the set of vertices with the K largest entries in the vector u.
- 6: Return  $\hat{S}(u)$  which maximizes the likelihood  $\mathbb{P}(A|S^* = \hat{S}(u))$ , over  $u \in U$ .

To state the result, recall the definition of f from (1.3). The following result implies Theorem 1.1.

<span id="page-7-1"></span>**Theorem 2.1.** Consider the PDS model with parameters given by (1.2), and let  $\hat{S}_n$  be the output of Algorithm 2. If  $\rho f(a,b) > 1$ , then  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

As remarked earlier, the recovery of  $S^*$  is information-theoretically impossible if  $\rho f(a,b) < 1$  as shown in [10]. Hence, Theorem 2.1 proves optimality of Algorithm 2.

<span id="page-7-0"></span>Remark 2.1. To analyze the runtime of Algorithm 2, note that Steps 1 and 2 are not data-dependent, and can therefore be precomputed. The runtime then depends on Steps 3, 5, and 6. In order to compute the eigenpairs in Step 3, one can use the power method on the matrix A. Letting  $\lambda_1^*$  and  $\lambda_2^*$ be the eigenvalues of  $\mathbb{E}[A]$ , Weyl's inequality states that  $|\lambda_1 - \lambda_1^{\star}|, |\lambda_2 - \lambda_2^{\star}| \leq ||A - \mathbb{E}[A]||_2$ . In Lemma 3.3, we show that  $||A - \mathbb{E}[A]||_2 = O(\sqrt{\log n})$  with high probability. On the other hand, we will show that  $\lambda_1^{\star}, \lambda_2^{\star} = \Theta(\log n)$ . Therefore, the spectral gap of A, which is  $\delta \triangleq \frac{\lambda_1 - \lambda_2}{\lambda_1}$ , is  $\Theta(1)$ . Since the power method converges in  $O(\log(n)/\delta)$  iterations (see e.g. [8]), and each iteration requires  $O(n \log n)$ time for multiplication of A by a vector, the overall runtime of computing the top eigenvector of A is  $O(n \log^2(n))$ . To obtain the second eigenvector, we can deflate A by substracting  $\lambda_1 u_1 u_1^T$ . By similar analysis, the power method will require  $O(n \log^2(n))$  time to obtain the second eigenvector. Next, Step 5 requires sorting four vectors of length n, which can be done in  $O(n \log n)$  time. Step 6 requires counting the number of edges within each of the four estimated dense subgraphs. Given a sparse representation of A, this can be done in time  $O(n \log n)$ . Therefore, the overall runtime of Algorithm 2 is  $O(n \log^2(n))$ , significantly faster than what would be possible with standard SDP algorithms.

2.2. Spectral recovery for SL. Next, we consider a spectral algorithm based on only the top eigenvector of the underlying matrix, which is shown to be optimal.

### <span id="page-8-2"></span>Algorithm 3 Spectral submatrix localization

**Input:** Parameters  $\mu$  and K; a matrix  $A \sim SL(\mu, K)$ 

Output: An estimate of  $S^*$ 

- 1: Find the top eigenvector u of A.
- 2: Identify  $\hat{S}_{+}(u)$  as the set of vertices with the K largest entries in the vector u. Similarly, identify  $\hat{S}_{-}(u)$  as the set of vertices with the K smallest entries in the vector u.
- 3: Return  $\hat{S}(u) \in \left\{\hat{S}_{+}(u), \hat{S}_{-}(u)\right\}$  which maximizes the likelihood  $\mathbb{P}(A|S^{\star} = \hat{S}(u))$ .

The following theorem implies Theorem 1.2.

<span id="page-8-0"></span>**Theorem 2.2.** Consider the SL model with parameters given by (1.4). Let  $\hat{S}_n$  be the output of Algorithm 3. If  $\rho a^2 > 8$ , then  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

Using the fact from [11] that exact recovery of  $S^*$  is information theoretically impossible for  $\rho a^2 < 8$  (Corollary 6.2), Theorem 2.2 establishes optimality of Algorithm 3. In order to prove Theorem 2.2, we will use an entrywise eigenvector perturbation result akin to the proof of Theorem 2.1.

2.3. **Spectral recovery for CPDS.** We next describe a simple spectral algorithm that can recover the planted dense subgraph in the censored model up to the information theoretic boundary. Our spectral algorithm uses a *signed adjacency matrix* representation, denoted by A. We define

$$A_{ij} = \begin{cases} 1 & \text{if } \{i, j\} \text{ is present} \\ -y & \text{if } \{i, j\} \text{ is absent} \\ 0 & \text{if } \{i, j\} \text{ is censored} \end{cases}$$

$$(2.1)$$

<span id="page-8-4"></span><span id="page-8-1"></span>where

$$y(p,q) = \frac{\log \frac{1-q}{1-p}}{\log \frac{p}{q}}.$$
 (2.2)

for 0 < p, q < 1. Recently, Dhara, Gaudio, Mossel, and Sandon studied spectral algorithms on such signed adjacency matrices, to perform community detection on a censored version of the Stochastic Block Model [7]. Note that the CPDS model would correspond to a stochastic block model, where the edge probabilities inside community 1 is p, and the edge probabilities inside community 2 and between two communities are q. While [7] had shown that spectral algorithms based on the top two eigenvectors of a signed adjacency matrix may not work up to the information theoretic threshold (cf. [7, Theorem 2.6]), we will show that these algorithms are optimal for the CPDS model.

Let us now describe the spectral algorithm for recovery in the CPDS model.

### <span id="page-8-3"></span>Algorithm 4 Spectral recovery in the CPDS model

**Input:** Parameters  $p, q, \alpha$ , and K; a signed adjacency matrix A computed from an unlabeled observation of  $\text{CPDS}(p, q, \alpha, K)$ 

Output: An estimate of the planted dense subgraph vertices

- 1: Let B be the matrix where  $B_{ij} = \alpha (p y(p,q)(1-p))$  for  $i, j \leq K$ , and  $B_{ij} = \alpha (q y(p,q)(1-q))$  otherwise.
- 2: Apply Algorithm 1 to B, obtaining the weights  $(c_1^{\star}, c_2^{\star})$ .
- 3: Compute the top two eigenpairs of A, denoting them  $(\lambda_1, u_1)$  and  $(\lambda_2, u_2)$ , where  $\lambda_1 \geq \lambda_2 \geq \cdots$ .
- 4: Let  $U = \{s_1 c_1^* u_1 + s_2 c_2^* u_2 : s_1, s_2 \in \{-1, 1\}\}.$
- 5: For each  $u \in U$  identify  $\hat{S}(u)$  as the set of vertices with the K largest entries in the vector u.

6: Return  $\hat{S}(u)$  which maximizes the likelihood  $\mathbb{P}(A|S^* = \hat{S}(u))$ , over  $u \in U$ .

One can show that the runtime of Algorithm 4 is  $O(n \log^2(n))$ , by a similar analysis to that of Algorithm 2.

The following result implies Theorem 1.3.

<span id="page-9-0"></span>**Theorem 2.3.** Let  $K = \lfloor \rho n \rfloor$ , where  $\rho \in (0,1)$  is fixed. Suppose p,q are constants such that  $p,q \in (0,1)$  and  $\alpha = t \log n/n$ . Let  $\hat{S}_n$  be the output of Algorithm 4. If  $t\rho > 1/\Delta_+(p,q)$ , then  $\lim_{n\to\infty} \mathbb{P}(\hat{S}_n = S^*) = 1$ .

### 3. Analyzing spectral algorithms for PDS

<span id="page-9-1"></span>In this section, we analyze Algorithm 2 and complete the proof of Theorem 2.1. We apply the method of entrywise perturbation analysis of eigenvectors developed recently by Abbe, Fan, Wang, and Zhong [1]. We will show the following:

<span id="page-9-2"></span>**Lemma 3.1.** Let  $\rho \in (0,1)$  and  $a,b \ge 0$  be constants. Let  $A \sim PDS(p,q,K)$ , with parameters given by (1.2). Let  $c_1, c_2$  be constants. Then with probability  $1 - O(n^{-3})$ ,

$$\min_{s_1, s_2 \in \{-1, 1\}} \left\| s_1 c_1 u_1 + s_2 c_2 u_2 - \left( c_1 \frac{A u_1^{\star}}{\lambda_1^{\star}} + c_2 \frac{A u_2^{\star}}{\lambda_2^{\star}} \right) \right\|_{\infty} \le \frac{C}{\log \log(n) \sqrt{n}},$$
(3.1)

where  $C = C(a, b, \rho, c_1, c_2)$  is a constant depending on  $a, b, \rho, c_1, and c_2$ .

Given Lemma 3.1, we can analyze the output of Algorithm 2 by analyzing the vector  $Av_{S^*}$ , where  $Av_{S^*}$  is described in Algorithm 1.

Proof of Theorem 2.1. Since we are in the achievable regime of the PDS model (due to [10]), the Maximum A Posteriori (MAP) estimator recovers  $S^*$  with high probability. Since  $S^*$  is chosen uniformly at random from all size-K subsets of [n], then also the Maximum Likelihood estimator (MLE) recovers  $S^*$  with high probability. The success of the MLE implies that with high probability,

<span id="page-9-3"></span>
$$\mathbb{P}(A|S^*) > \max_{S \neq S^*} \mathbb{P}(A|S^* = S). \tag{3.2}$$

Recall that Algorithm 2 forms the set  $U = \{s_1c_1^*u_1 + s_2c_2^*u_2 : s_1, s_2 \in \{-1, 1\}\}$ , and chooses the element  $u \in U$  which maximizes the likelihood  $\mathbb{P}(A|S^* = \hat{S}(u))$ . In light of (3.2), it suffices to show that  $S^* \in \{\hat{S}(u) : u \in U\}$ .

Note that  $c_1^{\star}, c_2^{\star}$  are constants due to the scaling of  $(\lambda_1^{\star}, u_1^{\star}), (\lambda_2^{\star}, u_2^{\star})$  (cf. Lemma 3.2). Let  $s_1, s_2 \in \{-1, 1\}$  be such that

$$\left\| s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2 - A \left( \frac{c_1^{\star}}{\lambda_1^{\star}} u_1^{\star} + \frac{c_2^{\star}}{\lambda_2^{\star}} u_2^{\star} \right) \right\|_{\infty} \le \frac{C}{\log \log(n) \sqrt{n}}$$

This is possible by Lemma 3.1, with probability  $1 - O(n^{-3})$ , where C depends on a, b, and  $\rho$ . Multiplying through by  $\log(n)$ , we also obtain

$$\|\log(n) \left(s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2\right) - A v_{S^{\star}}\|_{\infty} \le \frac{C \log(n)}{\log \log(n) \sqrt{n}}$$

We first consider the case a > b > 0. As shown in the proof of [10, Theorem 3] along with [10, Lemma 2], we have that for all C' > 0,

$$\sqrt{K} \min_{i \in S^{\star}} (Av_{S^{\star}})_{i} \ge \rho \left( \frac{a - b}{\log(a) - \log(b)} \right) \log n + \frac{C' \log n}{\log \log(n)}$$

$$\sqrt{K} \max_{i \in [n] \setminus S^{\star}} (Av_{S^{\star}})_{i} \le \rho \left( \frac{a - b}{\log(a) - \log(b)} \right) \log n$$

with probability at least  $1 - n^{1-\rho f(a,b) + o(1)} = 1 - n^{-\Omega(1)}$ . Therefore, we have

$$\log(n)\sqrt{K}\min_{i\in S^{\star}}\left(s_{1}c_{1}^{\star}u_{1}+s_{2}c_{2}^{\star}u_{2}\right)_{i} \geq \rho\left(\frac{a-b}{\log(a)-\log(b)}\right)\log n + \frac{C'\log n}{\log\log(n)} - \frac{C\log(n)\sqrt{K}}{\log\log(n)\sqrt{n}}$$
$$\log(n)\sqrt{K}\max_{i\in[n]\backslash S^{\star}}\left(s_{1}c_{1}^{\star}u_{1}+s_{2}c_{2}^{\star}u_{2}\right)_{i} \leq \rho\left(\frac{a-b}{\log(a)-\log(b)}\right)\log n + \frac{C\log(n)\sqrt{K}}{\log\log(n)\sqrt{n}}$$

with probability  $1 - n^{-\Omega(1)}$ . Thus, we obtain

$$\min_{i \in S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i > \max_{i \in [n] \setminus S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i$$

with probability  $1 - n^{-\Omega(1)}$ . Therefore, with probability  $1 - n^{-\Omega(1)}$ , the K largest entries of  $s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2$  correspond to the planted dense subgraph  $S^{\star}$ .

If a > b = 0, then  $\max_{i \in [n] \setminus S^*} (Av_{S^*})_i = 0$ . Again applying [10, Lemma 2], we have that for all C' > 0,

$$\sqrt{K} \min_{i \in S^{\star}} (Av_{S^{\star}})_i \ge \frac{C' \log n}{\log \log(n)}$$

with probability at least  $1 - n^{1-\rho a + o(1)} = 1 - n^{1-\rho f(a,0) + o(1)} = 1 - n^{-\Omega(1)}$ .

If a < b, then the analysis of the entries of  $Av_{S^*}$  again appeals to [10, Lemma 2]. We then obtain

$$\max_{i \in S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i < \min_{i \in [n] \setminus S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i$$

with probability  $1 - n^{-\Omega(1)}$ . Therefore, with probability  $1 - n^{-\Omega(1)}$ , the K smallest entries of  $s_1c_1^*u_1 + s_2c_2^*u_2$  correspond to the planted dense subgraph  $S^*$ .

To prove Lemma 3.1, we need the following two results.

<span id="page-10-1"></span>**Lemma 3.2.** Let A be the adjacency matrix of a PDS with parameters satisfying (1.2), and let  $A^* = \mathbb{E}[A]$ . The eigenvalues of  $A^*$  satisfy  $\lambda_1^* = (1 + o(1))\theta_1 \log(n)$  and  $\lambda_2^* = (1 + o(1))\theta_2 \log(n)$  for some constants  $\theta_1, \theta_2$  depending on a, b, and  $\rho$ .

The following result is a special case of [10, Theorem 5].

<span id="page-10-0"></span>**Lemma 3.3.** Let A be the adjacency matrix of a PDS with parameters satisfying (1.2). There exists  $c_1(a, b, \rho)$  such that

$$\mathbb{P}\left(\|A - A^{\star}\|_{2} \ge c_{1}\sqrt{\log(n)}\right) \le n^{-3}.$$

*Proof of Lemma 3.1.* The result will follow by establishing

<span id="page-10-2"></span>
$$\min_{s \in \{-1,1\}} \left\| s u_1 - \frac{A u_1^*}{\lambda_1^*} \right\|_{\infty} \le \frac{C_1(a,b,\rho)}{\log \log(n)\sqrt{n}},\tag{3.3}$$

and

<span id="page-10-3"></span>
$$\min_{s \in \{-1,1\}} \left\| s u_2 - \frac{A u_2^*}{\lambda_2^*} \right\|_{\infty} \le \frac{C_2(a,b,\rho)}{\log \log(n) \sqrt{n}}.$$
(3.4)

In order to establish (3.3) and (3.4), it suffices to verify Assumptions 1-4 of [1, Theorem 2.1]. Letting  $\tau = \max\{a, b\}$ , we have

$$||A^{\star}||_{2\to\infty} = \sqrt{\rho n \left(\frac{a\log n}{n}\right)^2 + (1-\rho)n \left(\frac{b\log n}{n}\right)^2} \le \frac{\tau \log(n)}{\sqrt{n}}.$$

By Lemma 3.2, we have that

$$\Delta^{\star} \triangleq \min \left\{ (\lambda_1^{\star} - \lambda_2^{\star}), |\lambda_1^{\star}|, |\lambda_2^{\star}| \right\} = c \log(n),$$

for some  $c = c(a, b, \rho)$ . Let

$$\gamma = \frac{c_1 \sqrt{\log(n)}}{\Delta^*},$$

where  $c_1 = c_1(a, b, \rho)$  is the value from Lemma 3.3. Then  $\gamma \Delta^* = c_1 \sqrt{\log(n)}$ , which dominates  $\frac{\tau \log(n)}{\sqrt{n}}$  for n large enough. Therefore, Assumption 1 of [1, Theorem 2.1] holds.

The second assumption holds since the edges are independent, conditioned on the memberships of the vertices.

By Lemma 3.3,

$$\mathbb{P}(\|A - A^*\|_2 \le \gamma \Delta^*) \ge 1 - n^{-3}.$$

Additionally,

$$\kappa \triangleq \frac{\max\left\{|\lambda_1^{\star}|, |\lambda_2^{\star}|\right\}}{\Delta^{\star}}$$

is a constant by Lemma 3.2, and  $\gamma \to 0$  as  $n \to \infty$ . Therefore, the third assumption is verified. To verify the fourth assumption, choose

$$\varphi(x) = \frac{(2\tau + 4)\log(n)}{\Delta^* \max\{1, \log\left(\frac{1}{x}\right)\}}$$

Applying [1, Lemma 7], with  $p = \frac{\tau \log n}{n}$  and  $\alpha = \frac{4}{\tau}$ , we obtain that for a fixed vector  $w \in \mathbb{R}^n$  and  $m \in [n]$ ,

$$\mathbb{P}\left(|(A - A^{\star})_{m,\cdot}w| \le \frac{(2\tau + 4)\log(n)}{\max\left\{1, \log\left(\frac{\sqrt{n}||w||_{\infty}}{||w||_{2}}\right)\right\}} ||w||_{\infty}\right) \ge 1 - 2n^{-4}$$

$$\mathbb{P}\left(|(A - A^{\star})_{m,\cdot}w| \le \Delta^{\star} ||w||_{\infty}\varphi\left(\frac{||w||_{2}}{\sqrt{n}||w||_{\infty}}\right)\right) \ge 1 - 2n^{-4},$$

so that Assumption 4 is verified with  $\delta_1 = 2n^{-3}$ .

Proof of Lemma 3.2. Fix  $\epsilon > 0$ , and find  $\rho' \in [0,1]$  such that  $\rho'$  is rational and  $|\rho - \rho'| < \epsilon$ . Let s,t be the integers such that  $\rho' = \frac{s}{t}$  is the minimal representation of  $\rho'$  (i.e., s and t have no common factors). Let B be the adjacency matrix of a PDS with parameters satisfying (1.2) but with  $\rho$  replaced by  $\rho'$ , and let  $B^* = \mathbb{E}[B]$ . Then  $B^*$  has two eigenvectors that correspond to non-zero eigenvalues. The first eigenvector  $v_1^*$  of  $B^*$  has entries that take on two possible values, one on the first s entries, and one on the remaining t entries. Suppose  $\beta_1$  and  $\beta_2$  are the values, and note that these are both nonzero.

Let  $u_1^{\star}$  be the first eigenvector of  $A^{\star}$ , with distinct entries  $\alpha_1$  and  $\alpha_2$ . If  $\rho$  were itself rational, then we could let  $\rho' = \rho$ . If additionally n were such that  $\rho n = \lfloor \rho n \rfloor$ , then  $A^{\star}$  would be a scaled version of  $B^{\star}$ . In that case, we would obtain  $\frac{\alpha_2}{\alpha_1} = \frac{\beta_2}{\beta_1}$ . For general  $\rho$  and fixed n, we note that both  $\alpha_1$  and  $\alpha_2$  are continuous functions of  $\frac{K}{n}$ , and therefore

$$\left| \frac{\alpha_2}{\alpha_1} - \frac{\beta_2}{\beta_1} \right| \le f_n(\epsilon),$$

where  $\lim_{\epsilon \to 0} f_n(\epsilon) = 0$ .

Using  $A^*u_1^* = \lambda_1^*u_1^*$ , we obtain that for fixed n,

$$\lambda_1^{\star} \alpha_1 = \rho n \cdot \frac{a \log n}{n} \cdot \alpha_1 + (1 - \rho) n \cdot \frac{b \log n}{n} \cdot \alpha_2, \quad \lambda_1^{\star} = \log(n) \left( \rho a + (1 - \rho) b \frac{\alpha_2}{\alpha_1} \right)$$
$$\log(n) \left( \rho a + (1 - \rho) b \left( \frac{\beta_2}{\beta_1} - f_n(\epsilon) \right) \right) \leq \lambda_1^{\star} \leq \log(n) \left( \rho a + (1 - \rho) b \left( \frac{\beta_2}{\beta_1} + f_n(\epsilon) \right) \right).$$

Choosing a sequence  $\{\epsilon_n\}_{n=1}^{\infty}$  such that  $\epsilon_n \to 0$ , we obtain  $\lambda_1^* = (1 + o(1))\theta_1(a, b, \rho)\log(n)$ . A similar argument applies to  $\lambda_2^*$ .

#### 4. Analyzing spectral algorithms for censored PDS

<span id="page-12-0"></span>We first provide the proof of Lemma 1.5.

Proof of Lemma 1.5. There exists  $N_0$  such that for all  $n > N_0$ ,

$$t_n p_n \ge \frac{a}{2}, \ t_n q_n \ge \frac{b}{2}, \ \text{and} \ |t_n p_n - t_n q_n| \ge \frac{1}{2} |a - b|.$$

We may therefore assume without loss of generality that  $p_n, q_n > 0$  and furthermore that  $p_n \neq q_n$  when  $a \neq b$ , since these statements are true for n sufficiently large. Under the assumptions of the statement,

$$\Delta_{+}(p,q) = \max_{x \in [0,1]} xp + (1-x)q - p^{x}q^{1-x} + x(1-p) + (1-x)(1-q) - (1-p)^{x}(1-q)^{1-x}$$

$$\approx \max_{x \in [0,1]} xp + (1-x)q - p^{x}q^{1-x}$$

$$= \max_{x \in [0,1]} q + (p-q)x - q\left(\frac{p}{q}\right)^{x},$$

where the second step uses p, q = o(1).

We first consider the case a = b > 0. Then

$$\lim_{n \to \infty} t_n \Delta_+(p, q) = \lim_{n \to \infty} \max_{x \in [0, 1]} q_n t_n + (p_n t_n - q_n t_n) x - q_n t_n \left(\frac{p_n t_n}{q_n t_n}\right)^x = 0 = f(a, a).$$

Next, suppose  $a \neq b$ . Letting  $g(x) = q + (p - q)x - q\left(\frac{p}{q}\right)^x$ , we obtain

$$g'(x) = p - q - q \left(\frac{p}{q}\right)^x \log\left(\frac{p}{q}\right).$$

Setting  $g'(x^*) = 0$ , we obtain the relations

$$\left(\frac{p}{q}\right)^{x^*} = \frac{p-q}{q\log\left(\frac{p}{q}\right)}$$
$$x^* = \frac{1}{\log\left(\frac{p}{q}\right)}\log\left(\frac{p-q}{q\log\left(\frac{p}{q}\right)}\right).$$

Substituting, we obtain

$$\Delta_{+}(p,q) \approx q + \frac{(p-q)}{\log\left(\frac{p}{q}\right)}\log\left(\frac{p-q}{q\log\left(\frac{p}{q}\right)}\right) - \frac{p-q}{\log\left(\frac{p}{q}\right)}.$$
(4.1)

Multiplying through by  $t=t_n$  and using the fact that  $\lim_{n\to\infty} p_n t_n=a$ ,  $\lim_{n\to\infty} q_n t_n=b$ , we obtain

$$t\Delta_{+}(p,q) \approx b + \frac{a-b}{\log\left(\frac{a}{b}\right)}\log\left(\frac{a-b}{b\log\left(\frac{a}{b}\right)}\right) - \frac{a-b}{\log\left(\frac{a}{b}\right)}$$
$$= b + \frac{a-b}{\log a - \log b}\left(\log\left(\frac{a-b}{b\log\left(\frac{a}{b}\right)}\right) - 1\right)$$
$$= b + \frac{a-b}{\log a - \log b}\log\left(\frac{a-b}{eb(\log a - \log b)}\right)$$

$$= b - \frac{a - b}{\log a - \log b} \log \left( \frac{eb(\log a - \log b)}{a - b} \right)$$
$$= f(b, a)$$
$$= f(a, b),$$

since  $f(\cdot, \cdot)$  is symmetric in its arguments. Since f(a, b) is a constant, we conclude that  $\lim_{n\to\infty} t_n \Delta_+(p_n, q_n) = f(a, b)$ .

In the remainder of this section, we analyze Algorithm 4 and complete the proof of Theorem 2.3. The idea again is to apply the method of entrywise perturbation analysis of eigenvectors from [1]. The following results will be used to prove Theorem 2.3, Part (1).

<span id="page-13-0"></span>**Lemma 4.1.** Suppose the conditions identical to Theorem 2.3 hold. Then the MLE recovers the planted dense subgraph, with probability 1 - o(1).

<span id="page-13-1"></span>**Lemma 4.2.** Let  $c_1, c_2$  be constants. Then with probability  $1 - O(n^{-3})$ ,

$$\min_{s_1, s_2 \in \{-1, 1\}} \left\| s_1 c_1 u_1 + s_2 c_2 u_2 - \left( c_1 \frac{A u_1^{\star}}{\lambda_1^{\star}} + c_2 \frac{A u_2^{\star}}{\lambda_2^{\star}} \right) \right\|_{\infty} \le \frac{C}{\log \log(n) \sqrt{n}}, \tag{4.2}$$

where  $C = C(p, q, t, \rho, c_1, c_2)$ .

<span id="page-13-2"></span>**Lemma 4.3.** Fix 0 < q < p < 1 and let y = y(p,q) be as in (2.2). Let  $\{X_i\}_{i=1}^m$  be i.i.d. random variables, where  $X_i = 1$  with probability  $\alpha p$ ,  $X_i = -y$  with probability  $\alpha(1-p)$ , and  $X_i = 0$  with probability  $1 - \alpha$ . Then for all  $\epsilon > 0$ ,

<span id="page-13-3"></span>
$$\log \left( \mathbb{P}\left( \sum_{i=1}^{m} X_i \le \epsilon \log n \right) \right) \le -\alpha m \Delta_+(p,q) + \epsilon \log \left( \frac{p}{q} \right) \log(n). \tag{4.3}$$

Similarly, let  $\{Y_i\}_{i=1}^m$  be i.i.d. random variables, where  $Y_i = 1$  with probability  $\alpha q$ ,  $Y_i = -y$  with probability  $\alpha(1-q)$ , and  $Y_i = 0$  with probability  $1-\alpha$ . Then

<span id="page-13-4"></span>
$$\log \left( \mathbb{P} \left( \sum_{i=1}^{m} Y_i \ge -\epsilon \log n \right) \right) \le -\alpha m \Delta_+(p, q) + \epsilon \log \left( \frac{p}{q} \right) \log(n). \tag{4.4}$$

We now prove the first statement of Theorem 2.3.

Proof of Theorem 2.3. We first give the proof in the case p > q. Lemma 4.1 shows that (3.2) holds in this parameter regime. Therefore, as in the proof of Theorem 2.1, it suffices to show that there exist  $s_1, s_2 \in \{-1, 1\}$  such that the vector  $s_1c_1^*u_1 + s_2c_2^*u_2$  recovers the planted dense subgraph.

Let  $c_1^{\star}, c_2^{\star}$  be such that  $\frac{c_1^{\star} \log(n)}{\lambda_1^{\star}} u_1^{\star} + \frac{c_2^{\star} \log(n)}{\lambda_2^{\star}} u_2^{\star} = v_{S^{\star}}$  as in Algorithm 1. Choose  $s_1, s_2 \in \{-1, 1\}$  such that

$$\left\| s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2 - A \left( \frac{c_1^{\star}}{\lambda_1^{\star}} u_1^{\star} + \frac{c_2^{\star}}{\lambda_2^{\star}} u_2^{\star} \right) \right\|_{\infty} \le \frac{C}{\log \log(n) \sqrt{n}}.$$

This is possible by Lemma 4.2 with probability  $1 - O(n^{-3})$ , where C depends on p, q, t, and  $\rho$ . Multiplying through by  $\log(n)$ , we also obtain

$$\|\log(n) \left(s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2\right) - A v_{s^{\star}}\|_{\infty} \le \frac{C \log(n)}{\log\log(n)\sqrt{n}}$$

We now apply Lemma 4.3 with  $m = \rho n$ . In particular, if  $i \in S^*$ , then (4.3) applies and if  $i \notin S^*$  then (4.4) applies. Then

$$\alpha m \Delta_{+}(p,q) = t \rho \Delta_{+}(p,q) \log(n).$$

Since  $t\rho\Delta_+(p,q) > 1$ , there exists  $\epsilon > 0$  such that

$$\sqrt{K} \min_{i \in S^*} (Av_{S^*})_i \ge \epsilon \log(n), \quad \sqrt{K} \max_{i \notin S^*} (Av_{S^*})_i \le -\epsilon \log(n).$$

with probability  $1 - n^{-\Omega(1)}$ . Therefore,

$$\log(n)\sqrt{K}\min_{i\in S^{\star}}(s_1c_1^{\star}u_1 + s_2c_2^{\star}u_2)_i \ge \epsilon\log(n) - \frac{C\log(n)\sqrt{K}}{\log\log(n)\sqrt{n}}$$
$$\log(n)\sqrt{K}\max_{i\in[n]\backslash S^{\star}}(s_1c_1^{\star}u_1 + s_2c_2^{\star}u_2)_i \le -\epsilon\log(n) + \frac{C\log(n)\sqrt{K}}{\log\log(n)\sqrt{n}}.$$

with probability  $1 - n^{-\Omega(1)}$ . We conclude that with probability  $1 - n^{-\Omega(1)}$ .

$$\min_{i \in S^*} (s_1 c_1^* u_1 + s_2 c_2^* u_2)_i > \max_{i \in [n] \setminus S^*} (s_1 c_1^* u_1 + s_2 c_2^* u_2)_i.$$

Next, consider the case p < q (the equality case is ruled out since  $\Delta_+(p,p) = 1$ ). The only change is in the application of Lemma 4.3; if  $i \in S^*$ , then (4.4) applies and if  $i \notin S^*$  then (4.3) applies. We then conclude that with probability  $1 - n^{-\Omega(1)}$ ,

$$\max_{i \in S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i < \min_{i \in [n] \setminus S^{\star}} (s_1 c_1^{\star} u_1 + s_2 c_2^{\star} u_2)_i.$$

Proof of Lemma 4.1. As noted in the proof of Theorem 2.3 Part (1), it suffices to consider the case p > q. We first characterize the MLE. Given a signed adjacency matrix A and a set  $S \subseteq [n]$ , let

$$E_1^+(A,S) = |\{\{i,j\} : A_{ij} = 1, i, j \in S\}|, \quad E_1^-(A,S) = |\{\{i,j\} : A_{ij} = 1, \{i \notin S \text{ or } j \notin S\}\}|\}$$

$$E_y^+(A,S) = |\{\{i,j\} : A_{ij} = -y, i, j \in S\}|, \quad E_y^-(A,S) = |\{\{i,j\} : A_{ij} = -y, \{i \notin S \text{ or } j \notin S\}\}|\}.$$

Given this notation, we can write the log-likelihood as

$$\log \mathbb{P}(A|S^{\star})$$

$$= \log(\alpha p) E_1^+(A, S^*) + \log(\alpha (1-p)) E_y^+(A, S^*) + \log(\alpha q) E_1^-(A, S^*) + \log(\alpha (1-q)) E_y^-(A, S^*) + \log(1-\alpha) \left( \binom{n}{2} - E_1^+(A, S^*) - E_y^+(A, S^*) - E_1^-(A, S^*) - E_y^-(A, S^*) \right).$$

When taking the difference of log likelihoods below, the final term does not contribute. We obtain

$$\begin{split} &\log\left(\mathbb{P}(A|S^{\star})\right) - \log\left(\mathbb{P}(A|S^{\star} = S)\right) \\ &= \log(\alpha p) \left(E_{1}^{+}(A, S^{\star}) - E_{1}^{+}(A, S)\right) + \log(\alpha (1-p)) \left(E_{y}^{+}(A, S^{\star}) - E_{y}^{+}(A, S)\right) \\ &+ \log(\alpha q) \left(E_{1}^{-}(A, S^{\star}) - E_{1}^{-}(A, S)\right) + \log(\alpha (1-q)) \left(E_{y}^{-}(A, S^{\star}) - E_{y}^{-}(A, S)\right) \\ &= \log(p) \left(E_{1}^{+}(A, S^{\star}) - E_{1}^{+}(A, S)\right) + \log(1-p) \left(E_{y}^{+}(A, S^{\star}) - E_{y}^{+}(A, S)\right) \\ &+ \log(q) \left(E_{1}^{-}(A, S^{\star}) - E_{1}^{-}(A, S)\right) + \log(1-q) \left(E_{y}^{-}(A, S^{\star}) - E_{y}^{-}(A, S)\right) \\ &= \log\left(\frac{p}{q}\right) \left(E_{1}^{+}(A, S^{\star}) - E_{1}^{+}(A, S)\right) + \log\left(\frac{1-p}{1-q}\right) \left(E_{y}^{+}(A, S^{\star}) - E_{y}^{+}(A, S)\right). \end{split}$$

It follows that the MLE maximizes  $\log(\frac{p}{q})E_1^+(A,S) + \log(\frac{1-p}{1-q})E_y^+(A,S)$  over  $S \subseteq [n]$ , where  $|S| = \lfloor \rho n \rfloor$ . Let  $F = \{S \subseteq [n] : |S| = \lfloor \rho n \rfloor\}$  denote the set of feasible sets. By rearranging, we find that the MLE computes

$$\underset{S \subset E}{\operatorname{argmax}} \{ E_1^+(A, S) - y E_y^+(A, S) \}.$$

Since  $t\rho\Delta_+(p,q) > 1$ , it is possible to choose  $\epsilon$  satisfying

$$0 < \epsilon < \frac{t\rho\Delta_+(p,q) - 1}{\log\left(\frac{p}{q}\right)}.$$

First we will show that with high probability, the MLE will not select any  $S \in F$  such that  $0 < |S \setminus S^*| \le \frac{\epsilon}{t(1+y)}n$ . To this end, we will leverage the concentration of partial row sums of A. Let  $X_i = \sum_{j \in S^*} A_{ij}$ . Lemma 4.3 along with a union bound implies that

$$\mathbb{P}\left(\left\{\min_{i\in S^{\star}} X_{i} \leq \epsilon \log n\right\} \cup \left\{\max_{i\in S^{\star}} X_{i} \geq -\epsilon \log n\right\}\right) \leq n^{1+\epsilon \log\left(\frac{p}{q}\right) - t\rho\Delta_{+}(p,q)} = n^{-\Theta(1)}. \tag{4.5}$$

Comparing  $S^*$  with  $S \in F$ ,

$$E_{1}^{+}(A,S) - yE_{y}^{+}(A,S) - \left(E_{1}^{+}(A,S^{*}) - yE_{y}^{+}(A,S^{*})\right)$$

$$= \sum_{i \in S \setminus S^{*}, j \in S^{*} \cap S} A_{ij} + \sum_{i,j \in S \setminus S^{*}: i < j} A_{ij} - \sum_{i \in S^{*} \setminus S, j \in S \cap S^{*}} A_{ij} - \sum_{i,j \in S^{*} \setminus S: i < j} A_{ij}. \tag{4.6}$$

We can rewrite the first term of (4.6) as follows:

<span id="page-15-2"></span><span id="page-15-1"></span><span id="page-15-0"></span>
$$\sum_{i \in S \setminus S^{\star}, j \in S^{\star} \cap S} A_{ij} = \sum_{i \in S \setminus S^{\star}, j \in S^{\star}} A_{ij} - \sum_{i \in S \setminus S^{\star}, j \in S^{\star} \setminus S} A_{ij}. \tag{4.7}$$

Under the high probability event in (4.5), we have  $\sum_{i \in S \setminus S^*, j \in S^*} A_{ij} < -\epsilon \log n |S \setminus S^*|$ . In order to bound the second term of 4.7, we bound the number of non-zero entries in the summation. Let H be the graph on n vertices which contains an edge between i and j whenever the edge status is revealed. Then H is distributed as an Erdős-Rényi random graph with parameters n and  $t \log n/n$ . For two sets  $U, W \subseteq [n]$ , let r(U, W) denote the number of edges between U and W in H (where we double-count any edge connecting two vertices in the intersection  $U \cap W$ ). By [14, Corollary 2.3],

<span id="page-15-3"></span>
$$\left| r(U,W) - \frac{t \log n}{n} |U| \cdot |W| \right| = O\left(\sqrt{|U| \cdot |W| t \log(n)}\right),\tag{4.8}$$

for all U, W with high probability. Therefore, the number of revealed edge statuses between  $S \setminus S^*$  and  $S^* \setminus S$  is at most

$$\frac{t \log n}{n} \left( |S \setminus S^{\star}| \right)^2 + O\left( |S \setminus S^{\star}| \sqrt{\log n} \right).$$

In the worst case, all of the revealed statuses are nonedges, contributing -y. Combining these observations,

$$\sum_{i \in S \setminus S^{\star}, j \in S^{\star} \setminus S} A_{ij} \ge -y \left( \frac{t \log n}{n} \left( |S \setminus S^{\star}| \right)^{2} + O\left( |S \setminus S^{\star}| \sqrt{\log n} \right) \right).$$

under the high probability event (4.8). Therefore, we can bound (4.7) by

$$\sum_{i \in S \setminus S^{\star}, j \in S^{\star} \cap S} A_{ij} \le -\epsilon \log n |S \setminus S^{\star}| + y \left( \frac{t \log n}{n} \left( |S \setminus S^{\star}| \right)^{2} + O\left( |S \setminus S^{\star}| \sqrt{\log n} \right) \right),$$

under the high probability events (4.5) and (4.8). We can similarly analyze the third term in (4.6):

$$-\sum_{i \in S^{\star} \backslash S, j \in S \cap S^{\star}} A_{ij} = -\sum_{i \in S^{\star} \backslash S, j \in S^{\star}} A_{ij} + \sum_{i \in S^{\star} \backslash S, j \in S^{\star} \backslash S} A_{ij}$$

$$\leq -\epsilon \log n + \frac{t \log n}{n} \left( |S \backslash S^{\star}| \right)^{2} + O\left( |S \backslash S^{\star}| \sqrt{\log n} \right)$$

Finally, we bound the second and fourth terms in (4.6):

$$\sum_{i,j \in S \setminus S^{\star}: i < j} A_{ij} - \sum_{i,j \in S^{\star} \setminus S: i < j} A_{ij} \le \frac{1}{2} (1+y) \left( \frac{t \log n}{n} \left( |S \setminus S^{\star}| \right)^2 + O\left( |S \setminus S^{\star}| \sqrt{\log n} \right) \right).$$

Putting everything together, we bound (4.6):

$$E_1^+(A,S) - y E_y^+(A,S) - \left( E_1^+(A,S^\star) - y E_y^+(A,S^\star) \right)$$

$$\leq -2\epsilon |S \setminus S^{\star}| \log(n) + \frac{3}{2}(1+y) \left( \frac{t \log n}{n} \left( |S \setminus S^{\star}| \right)^{2} + O\left( |S \setminus S^{\star}| \sqrt{\log n} \right) \right)$$
$$= |S \setminus S^{\star}| \log n \left[ -2\epsilon + \frac{3}{2}(1+y) \frac{t}{n} |S \setminus S^{\star}| + O\left( \frac{1}{\sqrt{\log n}} \right) \right].$$

If  $|S \setminus S^*| \leq \frac{\epsilon}{t(1+y)}n$ , then the difference in objective values will be negative for large enough n. We conclude that with high probability, the MLE will not select such an S.

It remains to show that with high probability, the MLE will not select any  $S \in F$  such that  $|S \setminus S^{\star}| > \frac{\epsilon}{t(1+y)}n$ . Fix  $\frac{\epsilon}{t(1+y)}n < m \leq n$ , and let  $S \in F$  be such that  $|S \setminus S^{\star}| = m$ . Let  $N(m) = {m \choose 2} + m(K-m)$ . Let  $\{X_i\}_{i=1}^{N(m)}$  be i.i.d. random variables, where  $X_i = 1$  with probability  $\alpha p$ ,  $X_i = -y$  with probability  $\alpha (1-p)$ , and  $X_i = 0$  with probability  $1-\alpha$ . Also let  $\{Y_i\}_{i=1}^{N(m)}$  be i.i.d. random variables independent of the  $X_i$ 's, where  $Y_i = 1$  with probability  $\alpha q$ ,  $Y_i = -y$  with probability  $\alpha (1-p)$ , and  $Y_i = 0$  with probability  $1-\alpha$ . Examining (4.6), we see that the difference  $E_1^+(A,S) - yE_y^+(A,S) - (E_1^+(A,S^*) - yE_y^+(A,S^*))$  has the same distribution as  $\sum_{i=1}^{N(m)} Y_i - \sum_{i=1}^{N(m)} X_i$ . By Lemma 4.3,

$$\log \left( \mathbb{P}\left( \sum_{i=1}^{N(m)} X_i \le \delta \log n \right) \right) \le -\alpha N(m) \Delta_+(p,q) + \delta \log \left( \frac{p}{q} \right) \log(n)$$

and

$$\log \left( \mathbb{P}\left( \sum_{i=1}^{N(m)} Y_i \ge -\delta \log n \right) \right) \le -\alpha N(m) \Delta_+(p,q) + \delta \log \left( \frac{p}{q} \right) \log(n)$$

for any  $\delta > 0$ . Simplifying the bounds using  $N(m) = {m \choose 2} + m(K - m)$ , we obtain

$$\delta \log \left(\frac{p}{q}\right) \log(n) - \alpha N(m) \Delta_{+}(p,q) = -\Theta(n \log n).$$

It follows that

$$\mathbb{P}\left(\sum_{i=1}^{N(m)} Y_i - \sum_{i=1}^{N(m)} X_i \ge 0\right) \le e^{-\Theta(n\log n)},$$

which also implies that  $E_1^+(A,S) - yE_y^+(A,S) - \left(E_1^+(A,S^*) - yE_y^+(A,S^*)\right) < 0$  with probability at least  $1 - e^{-\Theta(n \log n)}$ .

On the other hand,  $|F| \leq 2^n$ . By a union bound, the probability that the MLE selects some S satisfying  $|S \setminus S^*| > \frac{\epsilon}{t(1+v)}n$  is at most

$$2^n e^{-\Theta(n\log n)} = o(1).$$

We conclude that with high probability, the MLE selects  $S^*$ .

Proof of Lemma 4.2. The result will follow by establishing

<span id="page-16-0"></span>
$$\min_{s \in \{-1,1\}} \left\| s u_1 - \frac{A u_1^*}{\lambda_1^*} \right\|_{\infty} \le \frac{C_1(p, q, t, \rho)}{\log \log(n) \sqrt{n}},\tag{4.9}$$

and

<span id="page-16-1"></span>
$$\min_{s \in \{-1,1\}} \left\| s u_2 - \frac{A u_2^*}{\lambda_2^*} \right\|_{\infty} \le \frac{C_2(p, q, t, \rho)}{\log \log(n) \sqrt{n}}.$$
(4.10)

In order to establish (4.9) and (4.10), it suffices to verify Assumptions 1-4 of [1, Theorem 2.1].

By a similar argument as the proof of Lemma 3.2, we have  $\Delta^* = c_1 \log(n)$ , for some  $c_1 = c_1(p, q, \rho, t)$ . It follows from [10, Theorem 5] that

$$\mathbb{P}\left(\|A - A^{\star}\|_{2} \le c_{2}\sqrt{\log n}\right) \ge 1 - n^{-3}$$

for some  $c_2 = c_2(p, q, \rho, t)$ . We have

$$||A^{\star}||_{2\to\infty} = \sqrt{\rho n \left(\alpha p - \alpha(1-p)y\right)^2 + (1-\rho)n \left(\alpha q - \alpha(1-q)y\right)^2} = \Theta\left(\frac{\log n}{\sqrt{n}}\right).$$

Let  $\gamma = \frac{c_2\sqrt{\log(n)}}{\Delta^*}$ . Then  $\gamma\Delta^*$  dominates  $||A^*||_{2\to\infty}$  for n large enough, verifying Assumption 1. The second and third assumptions hold by the same reasoning as the proof of Lemma 3.1. The fourth assumption is verified identically as in the proof of [7, Proposition 5.1].

Proof of Lemma 4.3. Let  $\lambda > 0$ . Exponentiating and applying the Markov inequality,

$$\begin{split} \mathbb{P}\left(\sum_{i=1}^{m} X_{i} \leq \epsilon \log n\right) &= \mathbb{P}\left(-\lambda \sum_{i=1}^{m} X_{i} \geq -\lambda \epsilon \log n\right) \\ &= \mathbb{P}\left(\exp\left(-\lambda \sum_{i=1}^{m} X_{i}\right) \geq \exp\left(-\lambda \epsilon \log n\right)\right) \\ &\leq n^{\lambda \epsilon} \mathbb{E}\left[\exp\left(-\lambda \sum_{i=1}^{m} X_{i}\right)\right] = n^{\lambda \epsilon} \left(\mathbb{E}[e^{-\lambda X_{1}}]\right)^{m}. \end{split}$$

Using  $\log(1+x) \le x$  for x > -1,

$$\log \left( \mathbb{E}[e^{-\lambda X_1}] \right) = \log \left( e^{-\lambda} \alpha p + e^{\lambda y} \alpha (1-p) + 1 - \alpha \right)$$
  
$$\leq \alpha \left( e^{-\lambda} p + e^{\lambda y} (1-p) - 1 \right).$$

Therefore,

$$\log \left( \mathbb{P} \left( \sum_{i=1}^{m} X_i \le \epsilon \log n \right) \right) \le \lambda \epsilon \log(n) + \alpha m \left( e^{-\lambda} p + e^{\lambda y} (1 - p) - 1 \right)$$

Set  $\lambda = (1 - x^*) \log \left(\frac{p}{q}\right)$ , where  $x^*$  is the minimizer of

$$p^{x}q^{1-x} + (1-p)^{x}(1-q)^{1-x}$$
(4.11)

over  $x \in [0,1]$ . We claim that  $0 < x^* < 1$ . Indeed, taking  $x \in \{0,1\}$  yields a value of 1, while  $x = \frac{1}{2}$  yields  $\sqrt{pq} + \sqrt{(1-p)(1-q)}$ , which is strictly less than 1 when  $p \neq q$ . Using continuity of  $p^x q^{1-x} + (1-p)^x (1-q)^{1-x}$  with respect to x, we conclude that  $x^* \in (0,1)$ . Next, using that

$$e^{-\lambda}p + e^{\lambda y}(1-p) = p^{x^*}q^{1-x^*} + (1-p)^{x^*}(1-q)^{1-x^*} = -\Delta_+(p,q) + 1,$$

we obtain

$$\log \left( \mathbb{P} \left( \sum_{i=1}^{m} X_i \le \epsilon \log n \right) \right) \le -\alpha m \Delta_+(p,q) + (1-x^*)\epsilon \log \left( \frac{p}{q} \right) \log(n)$$

$$\le -\alpha m \Delta_+(p,q) + \epsilon \log \left( \frac{p}{q} \right) \log(n).$$

Similarly,

$$\mathbb{P}\left(\sum_{i=1}^{m} Y_i \ge -\epsilon \log n\right) = \mathbb{P}\left(\lambda \sum_{i=1}^{m} Y_i \ge -\lambda \epsilon \log n\right)$$

$$\begin{split} &= \mathbb{P}\left(\exp\left(\lambda\sum_{i=1}^m Y_i\right) \geq \exp\left(-\lambda\epsilon\log n\right)\right) \\ &\leq n^{\lambda\epsilon}\mathbb{E}\left[\exp\left(\lambda\sum_{i=1}^m Y_i\right)\right] = n^{\lambda\epsilon}\left(\mathbb{E}[e^{\lambda Y_1}]\right)^m. \end{split}$$

and

$$\log \left( \mathbb{E}[e^{\lambda Y_1}] \right) = \log \left( e^{\lambda} \alpha q + e^{-\lambda y} \alpha (1 - q) + 1 - \alpha \right)$$
  
$$\leq \alpha \left( e^{\lambda} q + e^{-\lambda y} (1 - q) - 1 \right).$$

Set  $\lambda = x^* \log \left(\frac{p}{q}\right)$ . Then

$$e^{\lambda}q + e^{-\lambda y}(1-q) = p^{x^*}q^{1-x^*} + (1-p)^{x^*}(1-q)^{1-x^*} = -\Delta_+(p,q) + 1,$$

and we obtain

$$\log \left( \mathbb{P} \left( \sum_{i=1}^{m} Y_i \ge -\epsilon \log n \right) \right) \le -\alpha m \Delta_+(p,q) + x^* \epsilon \log \left( \frac{p}{q} \right) \log(n)$$
$$\le -\alpha m \Delta_+(p,q) + \epsilon \log \left( \frac{p}{q} \right) \log(n).$$

The proof of Lemma 4.3 is now complete.

#### 5. Impossibility of recovery for the CPDS model

<span id="page-18-0"></span>5.1. **Proof of Theorem 1.4.** We start by identifying a sufficient condition for impossibility of recovering the planted dense subgraph. Let S be the space of possible assignments of vertices to the dense subgraph, i.e., all possible subsets S of size K. Recall that  $S^* \in S$  is the true underlying dense subgraph, which is a uniform subset of size K. We write g as a generic notation to denote the observed value of the edge-labeled graph G consisting of present, absent and censored edges. Also, let G be the space of all possible values of G.

The optimal estimator of  $S^*$  is the Maximum A Posteriori (MAP) estimator. Given a realization  $g \in \mathcal{G}$ , the MAP estimator outputs  $\hat{S}_{MAP} \in \operatorname{argmax}_{\mathcal{S}} \mathbb{P}(S_0 = S|G = g)$ , choosing uniformly at random from the argmax set. Since  $S^*$  is uniformly distributed on  $\mathcal{S}$ , we have the following equality between sets:

$$\operatorname*{argmax}_{\mathcal{S}} \mathbb{P}(S^{\star} = S | G = g) = \operatorname*{argmax}_{\mathcal{S}} \mathbb{P}(G = g | S^{\star} = S);$$

i.e. the MAP estimator coincides with the Maximum Likelihood estimator. Due to the equivalence, we obtain the following condition for failure of the MAP estimator.

<span id="page-18-1"></span>**Proposition 5.1.** Fix  $\delta > 0$ . Suppose that there is  $\mathcal{G}' \subset \mathcal{G}$  with  $\mathbb{P}(G \in \mathcal{G}'|S^*) \geq \delta$  such that the following holds for any  $g \in \mathcal{G}'$ : There are k pairs of vertices  $\{(u_i, v_i) : i \in [k]\}$  with  $u_i \in S^*$  and  $v_i \notin S^*$  such that if  $\tilde{S}^* := (S^* \cup \{v_i\}) \setminus \{u_i\}$ , then  $\mathbb{P}(G = g \mid S^*) = \mathbb{P}(G = g \mid \tilde{S}^*)$ . Then, conditionally on  $S^*$ , the MAP estimator  $\hat{S}_{MAP}$  fails in exact recovery with probability at least  $\delta(1 - \frac{1}{k})$ .

*Proof.* By our underlying condition, whenever  $g \in \mathcal{G}'$ , the true assignment is such that swapping  $u_i$  and  $v_i$  from  $S^*$  results in an equiprobable assignment. In that case, the algorithm is incorrect with probability at least  $1 - \frac{1}{k}$ . Therefore,

$$\mathbb{P}(\hat{S}_{\text{MAP}} \neq S^{\star} \mid S^{\star}) \ge \mathbb{P}(\hat{S}_{\text{MAP}} \neq S^{\star} \mid G \in \mathcal{G}', S^{\star}) \mathbb{P}(G \in \mathcal{G}' \mid S^{\star}) \ge \delta\left(1 - \frac{1}{k}\right), \tag{5.1}$$

and the proof follows.

Next we complete the proof of the impossibility result. We will use the following Poisson approximation result:

<span id="page-19-1"></span>**Lemma 5.2.** Let  $\{W_i\}_{i=1}^m$  be i.i.d. from a distribution taking three values a, b, c and  $\mathbb{P}(W_i = a) = \alpha \psi$ ,  $\mathbb{P}(W_i = b) = \alpha(1 - \psi)$ , and  $\mathbb{P}(W_i = c) = 1 - \alpha$ . Let  $N_x := \#\{i : W_i = x\}$  for x = a, b, c. If  $\alpha = m^{o(1)-1}$  then the probability distribution of  $(N_a, N_b)$  is within a total variation distance of  $m^{o(1)-1}$  of the product of a Poisson distribution of mean  $\alpha \psi m$  and a Poisson distribution of mean  $\alpha(1 - \psi)m$ .

Proof. For each i, let  $\overline{W}_i$  be (1,0) if  $W_i = a$ , (0,1) if  $W_i = b$ , and (0,0) if  $W_i = c$ . Also, for each i let  $\widehat{W}_i$  be drawn from  $P(\alpha\psi) \times P(\alpha(1-\psi))$  where  $P(\lambda)$  is the Poisson distribution with mean  $\lambda$ . The probability distributions of  $\overline{W}_i$  and  $\widehat{W}_i$  are within a total variation distance of  $O(\alpha^2) = m^{o(1)-2}$  of each other. Furthermore, all of the  $\overline{W}_i$  and  $\widehat{W}_i$  are mutually independent. So, the probability distribution of  $(N_a, N_b)$  is within a total variation distance of  $O(\alpha^2 m) = m^{o(1)-1}$  of the probability distribution of  $\sum_i \widehat{W}_i$ , which is  $P(\alpha\psi m) \times P(\alpha(1-\psi)m)$ .

This allows us to finally prove Theorem 1.4.

Proof of Theorem 1.4. We will show that with high probability, there exist  $k = \omega(1)$  pairs of vertices  $\{(u_i, v_i) : i \in [k], u_i \in S^*, v_i \notin S^*\}$  such that swapping their labels results in an equiprobable graph instance. By Proposition 5.1, this would show that exact recovery fails with probability 1 - o(1) for any algorithm. First, due to (1.6), there exists a sufficiently small enough constant  $\delta > 0$  such that  $t\rho\Delta_+(p,q) < 1 - 2\delta$  for all sufficiently large values of n.

For j=1,2, let  $V_j$  be sets of  $2n^{1-\delta}$  randomly selected vertices from  $S^*$  and  $(S^*)^c$ , respectively. Let  $V=V_1\cup V_2$ . Next, let V' be the set of all vertices in V whose connections to all other vertices in V are censored. We claim that  $|V'|>3n^{1-\delta}$  with probability 1-o(1). To see this, observe that the expected number of revealed connections between vertices in V is at most  $\alpha\binom{4n^{1-\delta}}{2} \times 8n^{1-2\delta}t\log n$ , so with high probability there are fewer than  $n^{1-\delta}/2$  such connections. Therefore with high probability there are fewer than  $n^{1-\delta}$  vertices in V with at least one neighbor in V, from which the claim follows. Let

<span id="page-19-0"></span>
$$x^* = \underset{x \in [0,1]}{\operatorname{argmax}} \left( 1 - p^x q^{1-x} - (1-p)^x (1-q)^{1-x} \right)$$

so that  $\Delta_+(p,q) = 1 - p^{x^*}q^{1-x^*} - (1-p)^{x^*}(1-q)^{1-x^*}$ . For a vertex v, we call  $(d_1,d_2)$  its degree profile, where  $d_1$  (respectively  $d_2$ ) is the number of present edges (respectively absent edges) v has to the planted dense subgraph  $S^*$ . Consider the degree profile

$$d = (\lceil p^{x^*} q^{1-x^*} t \rho \log(n) \rceil, \lceil (1-p)^{x^*} (1-q)^{1-x^*} t \rho \log(n) \rceil) =: (d_1, d_2).$$
 (5.2)

We will show that there are vertices in  $S^*$  and  $(S^*)^c$  with the degree profile given by (5.2). For  $v \in S^*$  (respectively  $v \notin S^*$ ), let  $\overline{p}_1$  (respectively  $\overline{p}_2$ ) be the probability that v has degree profile d, conditioned on  $v \in V'$ . By Lemma 5.2, we have that  $\overline{p}_1$  is within  $n^{o(1)-1}$  of the probability of drawing d from a multidimensional Poisson distribution with mean  $(\alpha p(K-|V_1|), \alpha(1-p)(K-|V_1|))$  and  $\overline{p}_2$  is within  $n^{o(1)-1}$  of the probability of drawing d from a multidimensional Poisson distribution with mean  $(\alpha q(K-|V_1|), \alpha(1-q)(K-|V_1|))$ . So,

$$\min\{\overline{p}_1,\overline{p}_2\}$$

<span id="page-20-0"></span>
$$\sim \min \left\{ e^{-t\rho \log n} \frac{(t\rho p \log n)^{d_1}}{d_1!} \frac{(t\rho(1-p)\log n)^{d_2}}{d_2!}, e^{-t\rho \log n} \frac{(t\rho q \log n)^{d_1}}{d_1!} \frac{(t\rho(1-q)\log n)^{d_2}}{d_2!} \right\} \pm n^{o(1)-1}$$

$$\sim e^{-t\rho \log n} \min \left\{ \frac{(t\rho p \log n)^{d_1} (t\rho(1-p)\log n)^{d_2}}{2\pi e^{-d_1-d_2} d_1^{d_1+1/2} d_2^{d_2+1/2}}, \frac{(t\rho q \log n)^{d_1} (t\rho(1-q)\log n)^{d_2}}{2\pi e^{-d_1-d_2} d_1^{d_1+1/2} d_2^{d_2+1/2}} \right\} \pm n^{o(1)-1}$$

$$= \frac{e^{-t\rho \log n + d_1 + d_2}}{2\pi \sqrt{d_1 d_2}} \min \left\{ \left( \frac{t\rho p \log n}{d_1} \right)^{d_1} \times \left( \frac{t\rho(1-p)\log n}{d_2} \right)^{d_2}, \left( \frac{t\rho(1-p)\log n}{d_1} \right)^{d_2} \times \left( \frac{t\rho(1-q)\log n}{d_2} \right)^{d_2} \right\} \pm n^{o(1)-1}$$

$$\sim \frac{e^{-t\rho \log n + d_1 + d_2}}{2\pi \sqrt{d_1 d_2}} n^{o(1)} \min \left\{ \left( \frac{p}{q} \right)^{(1-x^*)d_1} \left( \frac{1-p}{1-q} \right)^{(1-x^*)d_2}, \left( \frac{q}{p} \right)^{x^* d_1} \left( \frac{1-q}{1-p} \right)^{x^* d_2} \right\} \pm n^{o(1)-1},$$

$$(5.3)$$

and moreover,

$$e^{-t\rho\log n + d_1 + d_2} \approx e^{-t\rho\log n[1 - p^{x^*}q^{1 - x^*} - (1 - p)^{x^*}(1 - q)^{1 - x^*})]} = n^{-t\rho \times \Delta_+(p,q)}.$$

Next, let  $f(x) = p^x q^{1-x} + (1-p)^x (1-q)^{1-x}$ . Since f attains its minimum at  $x^*$ , we have  $f'(x^*) = 0$  and therefore

$$p^{x^*}q^{1-x^*}\log\frac{p}{q} + (1-p)^{x^*}(1-q)^{1-x^*}\log\frac{1-p}{1-q} = 0.$$

Thus,

$$\left(\frac{p}{q}\right)^{(1-x^*)d_1} \left(\frac{1-p}{1-q}\right)^{(1-x^*)d_2}$$

$$= \exp\left((1-x^*)t\rho\log n\left[p^{x^*}q^{1-x^*}\log\frac{p}{q} + (1-p)^{x^*}(1-q)^{1-x^*}\log\frac{1-p}{1-q}\right] \pm o(\log(n))\right) = n^{o(1)}$$

and similarly,

$$\left(\frac{q}{p}\right)^{x^*d_1} \left(\frac{1-q}{1-p}\right)^{x^*d_2}$$

$$= \exp\left(-x^*t\rho\log n\left[p^{x^*}q^{1-x^*}\log\frac{p}{q} + (1-p)^{x^*}(1-q)^{1-x^*}\log\frac{1-p}{1-q}\right] \pm o(\log(n))\right) = n^{o(1)}.$$

Thus, (5.3) reduces to

$$\min\{\overline{p}_1, \overline{p}_2\} \approx \frac{n^{-\Delta_+ - o(1)}}{2\pi\sqrt{d_1 d_2}} \pm n^{o(1) - 1} \ge n^{2\delta - 1 + o(1)}$$

where the last step uses  $t\rho\Delta_+(p,q) \leq 1-2\delta$  for large n.

For  $v \in V'$ , let Y(v) be the indicator that v has exactly  $d_1$  present edges and  $d_2$  absent edges to S. Note that the random variables in the set  $\{Y(v)\}_{v \in V'}$  are mutually independent conditionally on V'. Finally, observe that if  $u \in V' \cap V_1$  and  $v \in V' \cap V_2$  satisfy Y(u) = Y(v) = 1, then switching the labels of u and v results in an equiprobable outcome.

Let

$$Y_1 = \sum_{v \in V' \cap V_1} Y(v) \text{ and } Y_2 = \sum_{v \in V' \cap V_2} Y(v).$$

It suffices to show that there is a function  $f(n) = \omega(1)$  such that  $Y_1, Y_2 \ge f(n)$  with probability 1 - o(1).

Similarly to the proof of [7, Theorem 2.1], we can show

$$\mathbb{P}\left(Y_1 \le (1 - \varepsilon)|V' \cap V_1| \cdot \overline{p}_1 \mid |V' \cap V_1| = s\right) \le \frac{1}{\varepsilon^2 s \overline{p}_1}.$$
 (5.4)

Recall that  $|V'| > \frac{3}{4}|V_1 \cup V_2|$  with probability 1 - o(1).  $|V_1| = |V_2| = |V_1 \cup V_2|/2$ , so with high probability  $|V_1 \cap V'| > n^{1-\delta}$  and  $|V_2 \cap V'| > n^{1-\delta}$ . Along with (5.4), this implies

<span id="page-21-0"></span>
$$\mathbb{P}\left(Y_1 \le (1-\varepsilon)n^{1-\delta}\overline{p}_1\right) \le \frac{n^{\delta-1}}{\varepsilon^2\overline{p}_1} + o(1).$$

Since  $\overline{p}_1 \ge n^{2\delta-1+o(1)}$ , we have shown that there is a function  $f(n) = \omega(1)$  such that  $\mathbb{P}(Y_1 \le f(n)) = o(1)$ . By a similar argument, it holds that  $\mathbb{P}(Y_2 \le f(n)) = o(1)$ . Applying Proposition 5.1 with  $\delta = 1 - o(1)$  and  $k = (f(n))^2$  completes the proof.

5.2. Sharpness in a general parameter regime: Proof of Theorem 1.7. We start by setting up a coupling argument that will be used in the proof.

<span id="page-21-1"></span>**Definition 5.1** (Reduced CPDS model). Given an instance of CPDS $(p, q, \alpha, K)$  and  $\alpha' \geq \alpha$ , suppose we independently add an absent edge between each pair of vertices whose connection was previously censored with probability  $\frac{\alpha'-\alpha}{1-\alpha}$ . We call this model a reduced CPDS model and denote it by CPDS' $(p, q, \alpha, \alpha', K)$ .

We observe the following:

<span id="page-21-2"></span>**Lemma 5.3.** The distribution of CPDS' $(p, q, \alpha, \alpha', K)$  is equal to that of CPDS $(p\alpha/\alpha', q\alpha/\alpha', \alpha', K)$ .

*Proof.* Clearly, the probability of present edges and censored edges are equal in both the models, and therefore, the probabilities of absent edges are also equal.  $\Box$ 

Since  $\text{CPDS}(p, q, \alpha, \alpha', K)$  is distributed as  $\text{CPDS}(p\alpha/\alpha', q\alpha/\alpha', \alpha', K)$ , any algorithm on the latter model would result in an algorithm in the former model via the reduction. In particular, the following gives a spectral algorithm for  $\text{CPDS}(p, q, \alpha, K)$  via reduction:

### <span id="page-21-3"></span>Algorithm 5 Reduced spectral recovery in the CPDS model

**Input:** Parameters  $p, q, \alpha, \alpha'$  ( $\alpha' \ge \alpha$ ) and K; an unlabeled observation  $A \sim \text{CPDS}(p, q, \alpha, K)$ .

Output: An estimate of the planted dense subgraph vertices.

- 1: Create a reduced CPDS instance  $A' \sim \text{CPDS}'(p, q, \alpha, \alpha', K)$  according to Definition 5.1.
- 2: If  $\alpha' = 1$ , then apply Algorithm 2 to A', obtaining an estimate  $\hat{S}$ . Otherwise, apply Algorithm 4 to A'.
- 3: Return  $\hat{S}$ .

Proof of Theorem 1.7. Recall (1.5). Using  $\alpha_n p_n = \frac{a \log n}{n}$ ,  $\alpha_n q_n = \frac{b \log n}{n}$ , and  $\alpha_n = \frac{t_n \log n}{n}$  we can simplify

<span id="page-21-4"></span>
$$\frac{\alpha_n n}{\log n} \Delta_+(p_n, q_n) = t_n \max_{x \in [0, 1]} \left( 1 - p_n^x q_n^{1-x} - (1 - p_n)^x (1 - q_n)^{1-x} \right) 
= \max_{x \in [0, 1]} t_n \left( 1 - \left( \frac{a}{t_n} \right)^x \left( \frac{b}{t_n} \right)^{1-x} - \left( 1 - \frac{a}{t_n} \right)^x \left( 1 - \frac{b}{t_n} \right)^{1-x} \right) 
= \max_{x \in [0, 1]} \left( t_n - a^x b^{1-x} - (t_n - a)^x (t_n - b)^{1-x} \right) 
:= \max_{x \in [0, 1]} g(t_n, x),$$
(5.5)

where we have denoted the expression inside the max as  $g(t_n, x)$ . Considering g as a function of t, note that  $\frac{\mathrm{d}g(t,x)}{\mathrm{d}t} = 1 - x(\frac{t-b}{t-a})^{1-x} - (1-x)(\frac{t-a}{t-b})^x \leq 0$ , by the weighted AM-GM inequality. Thus, g(t,x) is nonincreasing in t, and therefore,  $\max_{x \in [0,1]} g(t,x)$  is also nonincreasing in t. Also, for  $t,t' > \max\{a,b\}$ ,

$$|g(t,x) - g(t',x)| \le |t - t'| + (t-a)^x |(t-b)^{1-x} - (t'-b)^{1-x}| + (t'-b)^x |(t-a)^x - (t'-a)^x|.$$

Thus, for any  $t_n \to t > \max\{a,b\}$ , we have  $\max_{x \in [0,1]} g(t_n,x) \to \max_{x \in [0,1]} g(t,x)$ , and therefore  $\max_{x \in [0,1]} g(t,x)$  is continuous in t on the interval  $(\max\{a,b\},\infty)$ . To see that  $\max_{x \in [0,1]} g(t,x)$  is also continuous at  $t = \max\{a,b\}$ , let us assume without loss of generality that a > b. We will show that the  $\limsup_{t \to \infty} \max_{x \in [0,1]} g(t,x)$  and  $\liminf_{t \to \infty} \max_{x \in [0,1]} g(t,x)$  are equal. For any  $t \ge a$ 

$$\max_{x \in [0,1]} g(t,x) \le \max_{x \in [0,1]} \left( t - a^x b^{1-x} \right) = t - b \min_{x \in [0,1]} \left( \frac{a}{b} \right)^x = t - b.$$

Therefore,  $\limsup_{t \searrow a} \max_{x \in [0,1]} g(t,x) \le a-b$ . Also, for any fixed  $\varepsilon > 0$ ,

$$\max_{x \in [0,1]} g(t,x) \ge t - a^{\varepsilon} b^{1-\varepsilon} - (t-a)^{\varepsilon} (t-b)^{1-\varepsilon},$$

and therefore  $\liminf_{t\searrow a} \max_{x\in[0,1]} g(t,x) \geq a - b \left(\frac{a}{b}\right)^{\varepsilon}$ . Taking  $\varepsilon \to 0$ , we can conclude that  $\liminf_{t\searrow a} \max_{x\in[0,1]} g(t,x) \geq a - b$ , which proves the continuity of  $\max_{x\in[0,1]} g(t,x)$  at t=a. Next, by Lemma 1.5,

<span id="page-22-1"></span>
$$\lim_{t \to \infty} \max_{x \in [0,1]} g(t,x) = f(a,b). \tag{5.6}$$

To prove the first statement in Theorem 1.7, let  $\liminf_{n\to\infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) > 1$ . We consider the cases where  $\rho f(a, b) > 1$  and  $\rho f(a, b) \le 1$  separately.

If  $\rho f(a,b) > 1$  then by Theorem 1.1 there is a spectral algorithm that recovers the dense subgraph of  $\text{CPDS}(a \log(n)/n, b \log(n)/n, 1, K_n)$  with probability 1-o(1). By Lemma 5.3, the reduced spectral algorithm in Algorithm 5 recovers the dense subgraph of  $\text{CPDS}(a \log(n)/(\alpha_n n), b \log(n)/(\alpha_n n), \alpha_n, K_n) = \text{CPDS}(p_n, q_n, \alpha_n, K_n)$ .

If  $\rho f(a,b) \leq 1$  but  $\liminf_{n\to\infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n,q_n) > 1$ , then we claim that there must exist some fixed  $t_0 > \max\{a,b\}$  such that

$$t_0 \times \rho \Delta_+ \left(\frac{a}{t_0}, \frac{b}{t_0}\right) > 1$$
, and  $\alpha_n \le \frac{t_0 \log(n)}{n}$  for all sufficiently large  $n$ . (5.7)

<span id="page-22-0"></span>To prove (5.7), recall  $t_n = \alpha_n n/\log n$  and let  $t_0' = \limsup_{n \to \infty} t_n$ . Let us first show that  $t_0' < \infty$ . Indeed, if  $t_n = \alpha_n n/\log n$  and  $t_{n_k} \to \infty$  along some subsequence  $(n_k)_{k \ge 1}$ , then by (5.5) and (5.6), we must have that

$$\lim_{k \to \infty} \frac{\alpha_{n_k} n_k}{\log n_k} \times \rho \Delta_+(p_{n_k}, q_{n_k}) = \rho f(a, b).$$

This would yield a contradiction. To prove the first assertion in (5.7), let  $(n'_k)_{k\geq 1}$  be a subsequence such that  $t_{n'_k} \to t'_0$ . We have shown above that  $t\Delta_+(\frac{a}{t},\frac{b}{t}) = \max_{x\in[0,1]} g(t,x)$  is continuous for  $t\geq \max\{a,b\}$ . Thus

$$1 < \lim_{k \to \infty} \frac{\alpha_{n_k'} n_k'}{\log n_k'} \times \rho \Delta_+(p_{n_k'}, q_{n_k'}) = t_0' \times \rho \Delta_+\left(\frac{a}{t_0'}, \frac{b}{t_0'}\right).$$

Using the continuity of  $t\Delta_{+}(\frac{a}{t}, \frac{b}{t})$  again, we can pick  $t_0 > t'_0$  such that both the conditions in (5.7) are ensured. Thus, we assume (5.7) holds. Due to the first condition in (5.7), there is a spectral algorithm that recovers the dense subgraph of  $\text{CPDS}(a/t_0, b/t_0, t_0 \log(n)/n, K_n)$  by Theorem 1.3. The reduction in Definition 5.1, together with the second condition of (5.7) and Lemma 5.3, implies that there is also a reduced spectral algorithm (Algorithm 5) that recovers the dense subgraph of

$$CPDS(a \log(n)/(\alpha_n n), b \log(n)/(\alpha_n n), \alpha_n, K_n) = CPDS(p_n, q_n, \alpha_n, K_n).$$

To prove the second statement in Theorem 1.7, let  $\limsup_{n\to\infty} \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) < 1$ . We can set  $\alpha'_n = \min(\alpha_n, \log^2(n)/n)$ . In that case,

$$\lim_{n \to \infty} \left| \frac{\alpha_n n}{\log n} \times \rho \Delta_+(p_n, q_n) - \frac{\alpha'_n n}{\log n} \times \rho \Delta_+(p_n \alpha_n / \alpha'_n, q_n \alpha_n / \alpha'_n) \right| = 0.$$
 (5.8)

<span id="page-23-2"></span>To see this, let  $t'_n = \frac{\alpha'_n n}{\log n}$ . We will use the elementary analysis fact that a sequence  $(y_n)_{n\geq 1}$  converges to y if and only if for any subsequence there is a further subsequence that converges to y. Fix any subsequence  $(n_k)_{k\geq 1}$ . If  $\limsup_{k\to\infty} t_{n_k} < \infty$ , then  $t_{n_k} = t'_{n_k}$  and the limit in (5.8) holds trivially along  $(n_k)_{k\geq 1}$ . If  $\limsup_{k\to\infty} t_{n_k} = \infty$ , there is a further subsequence  $(m_k)_{k\geq 1} \subset (n_k)_{k\geq 1}$  such that  $\lim_{k\to\infty} t_{m_k} = \infty$ . In this case,  $t'_{m_k} \leq t_{m_k}$  and also  $\lim_{k\to\infty} t'_{m_k} = \infty$ . Since we have shown below (5.5) that  $t\Delta_+(a/t,b/t)$  is non-increasing in t, we have

$$\lim_{k \to \infty} \left| t_{m_k} \times \rho \Delta_+(a/t_{m_k}, b/t_{m_k}) - t'_{m_k} \times \rho \Delta_+(a/t'_{m_k}, b/t'_{m_k}) \right| = 0,$$

and (5.8) holds along  $(m_k)_{k\geq 1}$ . This proves (5.8). Thus, by Theorem 1.4 there is no algorithm that recovers the dense subgraph of  $\text{CPDS}(a\log(n)/(\alpha'_n n), b\log(n)/(\alpha'_n n), \alpha'_n, K_n)$  with nonvanishing probability. By the reduction in Definition 5.1 and Lemma 5.3, there is no algorithm that recovers the dense subgraph of  $\text{CPDS}(p_n, q_n, \alpha_n, K_n)$  with nonvanishing probability.

### 6. Spectral submatrix localization

<span id="page-23-0"></span>In this section, we will complete the proof of Theorem 1.2. We start by recalling the following result by Hajek, Wu, and Xu [12].

**Theorem 6.1** (Corollary 4, [12]). Recall the definition of exact recovery from (1.1). If

$$\lim_{n \to \infty} K\mu^2 = \infty \tag{6.1}$$

$$\liminf_{n \to \infty} \frac{(K-1)\mu^2}{\log \frac{n}{K}} > 4$$
(6.2)

$$\liminf_{n \to \infty} \frac{K\mu^2}{\left(\sqrt{2\log n} + \sqrt{2\log K}\right)^2} > 1,$$
(6.3)

then exact recovery is possible. If exact recovery is possible, then (6.1) holds, while (6.2) and (6.3) hold with non-strict inequality.

Note that (6.3) implies (6.1). We consider the regime where  $K = \lfloor \rho n \rfloor$  for a constant  $\rho = (0,1)$  and  $\mu = a\sqrt{\frac{\log(n)}{n}}$  for a constant a > 0. In this regime, (6.1) implies (6.2). Therefore, we have the following recovery condition.

<span id="page-23-1"></span>Corollary 6.2. Let  $\rho \in (0,1)$  and a > 0 be constants. Let  $K = \lfloor \rho n \rfloor$  and  $\mu = a\sqrt{\frac{\log n}{n}}$ , and let  $A \sim \mathrm{SL}(\mu, K)$ . If  $\rho a^2 > 8$ , then exact recovery is possible. If  $\rho a^2 < 8$  then exact recovery is impossible.

*Proof.* The result follows from examining (6.3):

$$\lim_{n \to \infty} \inf \frac{K\mu^2}{\left(\sqrt{2\log n} + \sqrt{2\log K}\right)^2} = \liminf_{n \to \infty} \frac{\rho a^2 \log(n)}{\left(\sqrt{2\log n} + \sqrt{2\log(\rho n)}\right)^2}$$

$$= \frac{\rho a^2}{(2\sqrt{2})^2} = \frac{\rho a^2}{8}.$$

<span id="page-23-5"></span><span id="page-23-4"></span><span id="page-23-3"></span>

In order to prove Theorem 2.2, we first prove an entrywise result akin to Lemma 3.1.

<span id="page-24-0"></span>**Lemma 6.3.** Let a > 0 and  $\rho \in (0,1)$  be constants. Let  $A \sim \operatorname{SL}(\mu, K)$ , where  $K = \lfloor \rho n \rfloor$  and  $\mu = a\sqrt{\frac{\log n}{n}}$ . Let  $(\lambda, u)$  be the top eigenpair of A. Similarly, let  $(\lambda^*, u^*)$  be the top eigenpair of  $A^* = \mathbb{E}[A|S^*]$ . Then with probability 1 - o(1),

$$\min_{s \in \{\pm 1\}} \left\| su - \frac{Au^*}{\lambda^*} \right\|_{\infty} \le \frac{C}{\sqrt{n \log n}},$$

where  $C = C(\rho, a) > 0$  is a constant.

*Proof.* As in the proof of Lemma 3.1, we verify the assumptions of [1, Theorem 2.1], using ideas from the proof of [1, Theorem 3.1]. Note that  $A^*$  is a rank-1 matrix, where  $\lambda^* = \mu K$ . Therefore  $\Delta^* = \lambda^*$  and  $\kappa = 1$ .

We have

$$||A^*||_{2\to\infty} = \sqrt{K\mu^2} = \mu\sqrt{K} = \Theta(\sqrt{\log n}).$$

Let  $\gamma = \frac{3\sqrt{n}}{\mu K}$ , so that  $||A^*||_{2\to\infty} \le \gamma \lambda^* = \Theta(\sqrt{n})$ , verifying the first assumption.

The second assumption is trivially satisfied.

To verify the third assumption, we apply [6, Theorem 2.11], which implies that for t > 0,

$$\mathbb{P}(\|A - A^*\|_2 \ge 2\sqrt{n} + t) \le 2e^{-t^2/4}$$

(see also [11, Lemma 25]). We set  $t = \sqrt{n}$ , so that  $2\sqrt{n} + t = \gamma \Delta^*$ , allowing us to take  $\delta_0 = 2e^{-n/4}$ . Set  $\varphi(x) = cx$  for a constant c > 0 to be determined, so that

$$32\kappa \max\{\gamma, \varphi(\gamma)\} = 32\max(1, c)\gamma = o(1).$$

To verify the fourth assumption, fix  $w \in \mathbb{R}^n$ . Note that

$$\Delta^* \|w\|_{\infty} \varphi\left(\frac{\|w\|_2}{\sqrt{n} \|w\|_{\infty}}\right) = \frac{c\Delta^* \|w\|_2}{\sqrt{n}}$$
$$= \frac{ca\sqrt{\log n} K \|w\|_2}{n}$$
$$\geq (1 - \epsilon)c\rho a\sqrt{\log n} \|w\|_2$$

for any  $\epsilon$ , for n sufficiently large. For each  $m \in [n]$ , we have  $(A - A^*)_{m, \cdot} w \sim \text{NORMAL}(0, ||w||_2^2)$ . Let  $Z \sim \text{NORMAL}(0, 1)$ . Then

$$\begin{split} \mathbb{P}\left(|(A - A^{\star})_{m, \cdot} w| \leq \Delta^{\star} \|w\|_{\infty} \varphi\left(\frac{\|w\|_{2}}{\sqrt{n} \|w\|_{\infty}}\right)\right) &\geq \mathbb{P}\left(|(A - A^{\star})_{m, \cdot} w| \leq (1 - \epsilon) c \rho a \sqrt{\log n} \|w\|_{2}\right) \\ &= \mathbb{P}\left(Z \|w\|_{2} \leq (1 - \epsilon) c \rho a \sqrt{\log n} \|w\|_{2}\right) \\ &\geq 1 - \frac{2}{(1 - \epsilon) c \rho a \sqrt{2\pi \log(n)}} e^{-(1 - \epsilon)^{2} c^{2} \rho^{2} a^{2} \log(n)/2} \\ &= 1 - \frac{2}{(1 - \epsilon) c \rho a \sqrt{2\pi \log(n)}} n^{-(1 - \epsilon)^{2} c^{2} \rho^{2} a^{2}/2} \end{split}$$

In the second inequality, we have used the fact that  $\mathbb{P}(Z > t) \leq \frac{1}{t\sqrt{2\pi}}e^{-t^2/2}$ . Therefore, we may take

$$\delta_1 = \frac{2}{(1 - \epsilon)c\rho a\sqrt{2\pi \log(n)}} n^{1 - (1 - \epsilon)^2 c^2 \rho^2 a^2 / 2}.$$

Set  $c > \frac{\sqrt{2}}{(1-\epsilon)\rho a}$  to ensure that  $\delta_1 = o(1)$ .

Finally, since  $\gamma = \Theta\left(\frac{1}{\sqrt{\log n}}\right)$ ,  $||A^*||_{2\to\infty} = \Theta(\sqrt{\log n})$ , and  $\Delta^* = \Theta(\sqrt{n\log n})$ , we have

$$\kappa(\kappa + \varphi(1))(\gamma + \varphi(\gamma)) \|u^{\star}\|_{\infty} + \frac{\gamma \|A^{\star}\|_{2 \to \infty}}{\Delta^{\star}} = \Theta\left(\frac{1}{\sqrt{n \log n}}\right)$$

The desired conclusion then follows from [1, Theorem 2.1].

We also need a Gaussian concentration result, such as the following variant of [11, Lemma 2].

<span id="page-25-0"></span>**Lemma 6.4.** Let  $\{Z_i\}_n$  be a sequence of (not necessarily independent) normal random variables, where  $Z_i \sim \text{NORMAL}(0,1)$ . Then

$$\max_{i \in [n]} Z_i \le \sqrt{2\log n}$$

with probability 1 - o(1).

Proof.

$$\begin{split} \mathbb{P}\left(\max_{i \in [n]} Z_i > \sqrt{2\log(n)}\right) &\leq \sum_{i \in [n]} \mathbb{P}\left(Z_i > \sqrt{2\log(n)}\right) \\ &= n \int_{\sqrt{2\log(n)}}^{\infty} \frac{1}{\sqrt{2\pi}} e^{-x^2/2} dx \\ &= \frac{n}{\sqrt{2\pi}} \int_{\sqrt{2\log(n)}}^{\infty} e^{-\log(n) - \sqrt{2\log(n)} \left(x - \sqrt{2\log(n)}\right) - \left(x - \sqrt{2\log(n)}\right)^2/2} dx \\ &\leq \frac{1}{\sqrt{2\pi}} \int_{\sqrt{2\log(n)}}^{\infty} e^{-\sqrt{2\log(n)} \left(x - \sqrt{2\log(n)}\right)} dx \\ &= \frac{1}{\sqrt{4\pi \log(n)}}. \end{split}$$

Proof of Theorem 2.2. Corollary 6.2 implies that the MAP estimator succeeds in recovering  $S^*$  with high probability. Therefore, it suffices to show that thresholding either u or -u successfully recovers  $S^*$ , with high probability.

Applying Lemma 6.3, let  $s^* \in \{\pm 1\}$  be such that

$$\left\| s^* u - \frac{Au^*}{\lambda^*} \right\|_{\infty} \le \frac{C}{\sqrt{n \log n}}.$$

This occurs with probability 1 - o(1).

For  $i \in [n]$ ,

$$\left(\frac{Au^{\star}}{\lambda^{\star}}\right)_{i} = \frac{1}{\mu K^{3/2}} \sum_{j \in S^{\star}} A_{ij} \sim \begin{cases} N\left(\frac{1}{\sqrt{K}}, \frac{1}{\mu^{2}K^{2}}\right) & i \in S^{\star} \\ N\left(0, \frac{1}{\mu^{2}K^{2}}\right) & i \not\in S^{\star}. \end{cases}$$

By Lemma 6.4,

$$\max_{i \notin S^*} \mu K \left( \frac{Au^*}{\lambda^*} \right)_i \le \sqrt{2 \log(n - K)}$$

with high probability. Similarly,

$$\min_{i \in S^\star} \mu K \left[ \left( \frac{Au^\star}{\lambda^\star} \right)_i - \frac{1}{\sqrt{K}} \right] \geq -\sqrt{2\log K}$$

with high probability. Combining these facts along with the entrywise bound, we conclude that with high probability,

$$\min_{i \in S^*} s^* u_i \ge \frac{1}{\sqrt{K}} - \frac{\sqrt{2 \log K}}{\mu K} - \frac{C}{\sqrt{n \log n}}$$
$$\max_{i \notin S^*} s^* u_i \le \frac{\sqrt{2 \log(n - K)}}{\mu K} + \frac{C}{\sqrt{n \log n}}.$$

We see that

$$\min_{i \in S^*} s^* u_i - \max_{i \notin S^*} s^* u_i \ge \frac{1}{\sqrt{K}} - 2 \frac{\sqrt{2 \log n}}{\mu K} - O\left(\frac{1}{\sqrt{n \log(n)}}\right)$$

$$= \frac{1}{\sqrt{K}} \left(1 - \sqrt{\frac{8 \log n}{\mu^2 K}}\right) - O\left(\frac{1}{\sqrt{n \log(n)}}\right)$$

$$= \frac{1}{\sqrt{K}} \left(1 - \sqrt{\frac{8n \log n}{a^2 \lfloor \rho n \rfloor \log n}}\right) - O\left(\frac{1}{\sqrt{n \log(n)}}\right)$$

$$= \frac{1}{\sqrt{K}} \left(1 - (1 + o(1))\sqrt{\frac{8}{\rho a^2}}\right) - O\left(\frac{1}{\sqrt{n \log(n)}}\right).$$

Since  $\rho a^2 > 8$  and  $K = \Theta(n)$ , we have

$$\min_{i \in S^*} s^* u_i - \max_{i \notin S^*} s^* u_i > 0$$

with high probability. We conclude that thresholding  $s^*u$  succeeds in recovering the communities with probability 1 - o(1).

### References

- <span id="page-26-2"></span>[1] E. Abbe, J. Fan, K. Wang, and Y. Zhong. Entrywise eigenvector analysis of random matrices with low expected rank. *Annals of Statistics*, 48(3):1452–1474, 2020.
- <span id="page-26-5"></span>[2] E. Abbe and C. Sandon. Community detection in general stochastic block models: Fundamental limits and efficient algorithms for recovery. In 2015 IEEE 56th Annual Symposium on Foundations of Computer Science, pages 670–688. IEEE, 2015.
- <span id="page-26-0"></span>[3] N. Alon, M. Krivelevich, and B. Sudakov. Finding a large hidden clique in a random graph. In *Proceedings of the Ninth Annual ACM-SIAM Symposium on Discrete Algorithms*, SODA '98, page 594–598, USA, 1998. Society for Industrial and Applied Mathematics.
- <span id="page-26-4"></span>[4] J. Banks, J. Garza-Vargas, A. Kulkarni, and N. Srivastava. Pseudospectral shattering, the sign function, and diagonalization in nearly matrix multiplication time. In 2020 IEEE 61st Annual Symposium on Foundations of Computer Science (FOCS), pages 529–540, 2020.
- <span id="page-26-1"></span>[5] A. Coja-Oghlan. A spectral heuristic for bisecting random graphs. Random Structures & Algorithms, 29(3):351–398, 2006.
- <span id="page-26-7"></span>[6] K. R. Davidson and S. J. Szarek. Local operator theory, random matrices and Banach spaces. *Handbook of the geometry of Banach spaces*, 1(317-366):131, 2001.
- <span id="page-26-3"></span>[7] S. Dhara, J. Gaudio, E. Mossel, and C. Sandon. Spectral recovery of binary censored block models. *Proceedings of the 2022 Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)*, 2022.
- <span id="page-26-6"></span>[8] D. Garber, E. Hazan, C. Jin, C. Musco, P. Netrapalli, A. Sidford, et al. Faster eigenvector computation via shift-and-invert preconditioning. In *International Conference on Machine Learning*, pages 2626–2634. PMLR, 2016.

- <span id="page-27-4"></span>[9] B. Hajek, Y. Wu, and J. Xu. Recovering a hidden community beyond the spectral limit in O(|E| log\*|V|) time. arXiv preprint arXiv:1510.02786, 2015.
- <span id="page-27-5"></span>[10] B. Hajek, Y. Wu, and J. Xu. Achieving exact cluster recovery threshold via semidefinite programming. IEEE Transactions on Information Theory, 62(5):2788–2797, 2016.
- <span id="page-27-6"></span>[11] B. Hajek, Y. Wu, and J. Xu. Semidefinite programs for exact recovery of a hidden community. In Conference on Learning Theory, pages 1051–1095. PMLR, 2016.
- <span id="page-27-7"></span>[12] B. Hajek, Y. Wu, and J. Xu. Information limits for recovering a hidden community. IEEE Transactions on Information Theory, 63(8):4729–4745, 2017.
- <span id="page-27-1"></span>[13] M. Kolar, S. Balakrishnan, A. Rinaldo, and A. Singh. Minimax localization of structural information in large noisy matrices. In J. Shawe-Taylor, R. Zemel, P. Bartlett, F. Pereira, and K. Weinberger, editors, Advances in Neural Information Processing Systems, volume 24, 2011.
- <span id="page-27-10"></span>[14] M. Krivelevich and B. Sudakov. Pseudo-random graphs. In More sets, graphs and numbers, pages 199–262. Springer, 2006.
- <span id="page-27-0"></span>[15] L. Kučera. Expected complexity of graph partitioning problems. Discrete Applied Mathematics, 57(2):193–212, 1995. Combinatorial optimization 1992.
- <span id="page-27-2"></span>[16] A. A. Shabalin, V. J. Weigman, C. M. Perou, and A. B. Nobel. Finding large average submatrices in high dimensional data. The Annals of Applied Statistics, 3(3):985–1012, 2009.
- <span id="page-27-8"></span>[17] V. VU. A simple SVD algorithm for finding hidden partitions. Combinatorics, Probability and Computing, 27(1):124–140, 2018.
- <span id="page-27-3"></span>[18] Y. Wu and J. Xu. Statistical problems with planted structures: Information-theoretical and computational limits, page 383–424. Cambridge University Press, 2021.
- <span id="page-27-9"></span>[19] S. Yun and A. Proutière. Accurate community detection in the stochastic block model via spectral algorithms. arXiv, abs/1412.7335, 2014.