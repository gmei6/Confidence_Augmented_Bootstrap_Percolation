# <span id="page-0-0"></span>ON r-TO-p NORMS OF RANDOM MATRICES WITH NONNEGATIVE ENTRIES: ASYMPTOTIC NORMALITY AND $\ell_{\infty}$ -BOUNDS FOR THE MAXIMIZER

BY SOUVIK DHARA<sup>1,a</sup>, DEBANKUR MUKHERJEE<sup>2,b</sup> AND KAVITA RAMANAN<sup>3,c</sup>

<sup>1</sup>School of Industrial Engineering, Purdue University, <sup>a</sup>sdhara@purdue.edu

<sup>2</sup>H. Milton Stewart School of Industrial and Systems Engineering, Georgia Institute of Technology, <sup>b</sup>debankur.mukherjee@isye.gatech.edu

<sup>3</sup>Division of Applied Mathematics, Brown University, <sup>c</sup>kavita ramanan@brown.edu

For an  $n \times n$  matrix  $A_n$ , the  $r \to p$  operator norm is defined as

$$||A_n||_{r \to p} := \sup_{x \in \mathbb{R}^n : ||x||_r \le 1} ||A_n x||_p \quad \text{for } r, p \ge 1.$$

For different choices of r and p, this norm corresponds to key quantities that arise in diverse applications including matrix condition number estimation, clustering of data, and construction of oblivious routing schemes in transportation networks. This article considers  $r \to p$  norms of symmetric random matrices with nonnegative entries, including adjacency matrices of Erdős-Rényi random graphs, matrices with positive sub-Gaussian entries, and certain sparse matrices. For 1 , the asymptotic normality,as  $n \to \infty$ , of the appropriately centered and scaled norm  $||A_n||_{r \to p}$  is established. When  $p \ge 2$ , this is shown to imply, as a corollary, asymptotic normality of the solution to the  $\ell_p$  quadratic maximization problem, also known as the  $\ell_p$  Grothendieck problem. Furthermore, a sharp  $\ell_{\infty}$ -approximation bound for the unique maximizing vector in the definition of  $||A_n||_{r\to p}$  is obtained, and may be viewed as an  $\ell_{\infty}$ -stability result of the maximizer under random perturbations of the matrix with mean entries. This result, which may be of independent interest, is in fact shown to hold for a broad class of deterministic sequences of matrices having certain asymptotic expansion properties. The results obtained can be viewed as a generalization of the seminal results of Füredi and Komlós (1981) on asymptotic normality of the largest singular value of a class of symmetric random matrices, which corresponds to the special case r = p = 2 considered here. In the general case with 1 , spectral methods are no longer applicable, and so a newapproach is developed involving a refined convergence analysis of a nonlinear power method and a perturbation bound on the maximizing vector, which may be of independent interest.

## 1. Introduction.

1.1. Problem statement and motivation. For any  $n \times n$  square matrix  $A_n$  and  $r, p \ge 1$ , the  $r \to p$  operator norm of  $A_n$  is defined as

$$(1.1)$$

For different values of r and p, the  $r \to p$  operator norm represents key quantities that arise in a broad range of disciplines. For example, when p = r = 2, this corresponds to the largest singular value of the matrix  $A_n$ , which has been studied extensively for decades. On the other

Received August 2020; revised December 2023.

MSC2020 subject classifications. Primary 60B20, 15B52; secondary 15A60, 15A18.

Key words and phrases. Random matrices, r-to-p norms, asymptotic normality,  $\ell_{\infty}$  perturbation bound, Boyd's power method, inhomogeneous variance profile, Grothendiek  $\ell_p$  problem.

hand, when p is the Hölder conjugate of r, that is, p = r/(r-1), and  $A_n$  has nonnegative entries and  $A_n^T A_n$  is irreducible, then we will see (in Proposition 2.11 and Section 9) that this problem reduces to the famous  $\ell_r$  Grothendieck problem [28], Section 5, which has inspired a vibrant line of research in the optimization community. Two special cases of the  $\ell_r$ Grothendieck problem, namely when r=2 and  $r=\infty$ , relate to spectral partitioning [15, 20] and correlation clustering [13], respectively, and the case of general  $r \in (2, \infty)$  can be viewed as a smooth interpolation between these two clustering criteria. Further, this problem is also related to finding ground states in statistical physics problems. Another interesting special case is when p = r, which has been a classical topic; see [42, 51] for general inequalities involving the  $p \to p$  norm, [26] for applications of these norms to matrix condition number estimation, which is crucial for computing perturbations of solutions to linear equations, and [9, 27] for algorithms to approximate such norms. Other prime application areas are: construction of oblivious routing schemes in transportation networks for the  $\ell_p$  norm [4, 17, 24, 40], and data dimension reduction or sketching of these norms, with applications to the streaming model and robust regression [29]. Understanding the computational complexity of calculating  $r \to p$  norms has generated immense recent interest in theoretical computer science. We refer the reader to [28] for a detailed account of the applications, approximability results, and Grothendieck-type inequalities for this norm. In general, this problem is NP-hard; even providing a constant-factor approximation algorithm for this problem is hard [4, 6, 25]. However, for the case considered in this article, namely matrices with nonnegative entries and 1 , this problem can be solved in polynomial time [4, 9]. The cases whenp=1 and  $r\geq 1$  are equivalent to the cases  $p\leq \infty$  and  $r=\infty$  [29], Lemma 8. These cases are trivial for nonnegative matrices and hence, we do not consider them in this article.

The analysis of this norm for random matrices is motivated from a statistical point of view. Indeed, asymptotic results on spectral statistics and eignevectors form the bedrock of methods in high-dimensional statistics (see [10, 48, 50] for a sample of the vast literature in this area). Further, it is worth mentioning the seminal work of Füredi and Komlós [21], where asymptotic normality of the largest eigenvalue was first established for matrices with i.i.d. entries. Subsequently, this result has been extended to adjacency matrices of sparse Erdős–Rényi random graphs [18], stochastic block model [46], and rank-1 inhomogeneous random graphs [12]. In the context of general  $r \to p$  norms for random matrices, the p > r case has received much attention. For matrices with bounded mean-zero independent entries, asymptotic bounds on the  $2 \to p$  norm was established in [3] for  $2 \le p < \infty$ . For  $1 < r \le 2 \le p < \infty$  and matrices having i.i.d. entries,  $||A_n||_{r \to p}$  is known to concentrate around its median [32]. Furthermore, in this regime, refined bounds on the expected  $r \to p$  norm of centered Gaussian random matrices have been obtained in [23] and later extended to log-concave random matrices with dependent entries in [45].

Another quantity of considerable interest is the maximizing vector in (1.1). For example, in the p=r=2 case, eigenvectors of adjacency matrices of graphs are known to play a pivotal role in developing efficient graph algorithms, such as spectral clustering [44, 49], spectral partitioning [15, 20, 31, 39], PageRank [38], and community detection [34, 35]. Eigenvectors of random matrices can be viewed as perturbations of eigenvectors of the expectation matrix, in the presence of additive random noise in the entries of the latter. The study of eigenvector perturbation bounds can be traced back to the classical Rayleigh–Schrödinger theory [41, 43] in quantum mechanics, which gives asymptotic perturbation bounds in the  $\ell_2$ -norm, as the signal to noise ratio increases. Nonasymptotic perturbation bounds in the  $\ell_2$ -norm were derived later in a landmark result [14], popularly known as the Davis–Kahan sin  $\Theta$  theorem. When the perturbation is random, the above deterministic results typically yield suboptimal bounds. Random perturbations of low-rank matrices has recently been analyzed in [37]. However, norms that are not unitary-invariant, such as the  $\ell_{\infty}$ -norm, as considered in this paper,

are typically outside the scope of the above works, although they are of significant interest in statistics and machine learning. The  $\ell_{\infty}$ -norm bounds in the case of low-rank matrices have been studied recently in [1, 11, 16, 19, 33, 52], and [1, 19, 36] contain extensive discussions on such perturbation bounds on eigenvectors (or singular vectors) and their numerous applications in statistics and machine learning.

- 1.2. Our contributions. Fix  $1 . We now elaborate on the two main results of the current article, namely asymptotic normality of a suitably scaled and centered version of <math>||A_n||_{r\to p}$ , and approximation of the corresponding maximizing vector.
- (1) Asymptotic normality. Given a sequence of symmetric nonnegative random matrices  $(A_n)_{n\in\mathbb{N}}$ , our first set of results establishes asymptotic normality of the scaled norm  $\|\bar{A}_n\|_{r\to p}:=n^{-(\frac{1}{p}-\frac{1}{r})}\|A_n\|_{r\to p}$  when  $1< p\le r<\infty$ . Specifically, let  $A_n$  have zero diagonal entries and independent and identically distributed (i.i.d.) off-diagonal entries subject to the symmetry constraint that have mean  $\mu_n$ , variance  $\sigma_n^2>0$ . Under certain moment bounds on the distribution of the matrix entries, and a control on the asymptotic sparsity of the matrix sequence, expressed in terms of conditions on the (relative) rates at which  $\sigma_n^2$  and  $\mu_n$  can decay to zero, it is shown in Theorem 2.2 that as  $n\to\infty$ ,

(1.2) 
$$\frac{1}{\sigma_n} (\|\bar{A}_n\|_{r \to p} - \alpha_n(p, r)) \xrightarrow{d} Z \sim \text{Normal}(0, 2),$$

where  $\xrightarrow{d}$  denotes convergence in distribution, and

(1.3) 
$$\alpha_n(p,r) := (n-1)\mu_n + \frac{1}{2}\left(p-1 + \frac{1}{r-1}\right)\frac{\sigma_n^2}{\mu_n}.$$

An extension of the above result for random matrices with inhomogeneous variance profile is also provided in Theorem 2.9. In this case, however, the matrix is required to be dense.

A result of this flavor appears to have first been established in the seminal work of Füredi and Komlós [21] for the special case r = p = 2, where  $\|\bar{A}_n\|_{2\to 2} = \|A_n\|_{2\to 2}$  represents  $\lambda_1^{(n)}$ , the largest eigenvalue of  $A_n$ . Using spectral methods, it is shown in [21], Theorem 1, that under the assumption that  $A_n$  is a symmetric  $n \times n$  random matrix with zero diagonal entries, independent, uniformly bounded off-diagonal entries having a common positive mean  $\mu > 0$  and variance  $\sigma^2 > 0$  (with  $\mu$ ,  $\sigma$  not depending on n), the limit (1.2) holds with r =p=2,  $\sigma_n=\sigma$ , and  $\alpha_n(2,2)=(n-1)\mu+\sigma^2/\mu$ , which coincides with the definition in (1.3), when one sets  $\mu_n=\mu$  and  $\sigma_n^2=\sigma^2$ . Even for the case p=r=2, our result extends the asymptotic normality result of Füredi and Komlós [21] in three directions: it allows for (a) sequences of possibly sparse matrices  $(A_n)_{n\in\mathbb{N}}$ , that is, with  $\mu_n\to 0$ ; (b) independent and identically distributed (i.i.d.) off-diagonal entries satisfying suitable moment conditions, but with possibly unbounded support; (c) independent entries with possibly different variances, having a dense variance profile. Throughout, the assumption that the diagonal entries are identically zero is only made for simplicity of notation; the result of [21] also allows for the diagonal entries to be drawn from another independent sequence of entries with a different common positive mean and uniformly bounded support on the diagonal, and an analogous extension can also be accommodated in our setting; see Remark 2.3. Moreover, we do not necessarily identify the optimal level of sparsity, see Remark 2.1 for an elaboration of this point.

It is worth mentioning two interesting aspects of the limit in (1.2). Consider the setting where  $\mu_n = \mu > 0$  and  $\sigma_n^2 = \sigma^2 > 0$ , as considered in [21]. First, note that while  $\|\mathbb{E}[\bar{A}_n]\|_{r\to p} = (n-1)\mu$ , and  $\|\bar{A}_n\|_{r\to p}/\|\mathbb{E}[\bar{A}_n]\|_{r\to p}$  converges in probability to 1, the centering  $\alpha_n(p,r)$  is strictly larger than  $(n-1)\mu$  by a  $\Theta(1)$  asymptotically nonvanishing

amount. Second, whereas the centering  $\alpha_n(p,r)$  for  $\|\bar{A}_n\|_{r\to p}$  is  $\Theta(n)$ , the Gaussian fluctuations of  $\|\bar{A}_n\|_{r\to p}$  are only  $\Theta(1)$ , having variance 2. Both these properties also hold for the case r=p=2 analyzed in [21], and the second property can be seen as a manifestation of the rigidity phenomenon for eigenvalues of random matrices. This has subsequently been shown to occur in a variety of other random matrix models, but there is a priori no reason to expect this to generalize to the nonspectral setting of a general  $r\to p$  norm. While spectral methods can be used in the case p=r=2, they are no longer applicable in the general  $r\to p$  norm setting. Thus, we develop a new approach, which also reveals some key reasons for these phenomena to occur, and brings to light when the shift and rigidity properties will fail when considering sparse sequences of matrices (see Remark 2.4).

(2) Approximation of the maximizing vector. Our second set of results are summarized in Theorem 2.6, which provides an  $\ell_{\infty}$ -approximation of the maximizing vector for matrices with i.i.d. entries, and Theorem 2.8, which extends this to random matrices with inhomogeneous variance profiles. These results rely on Proposition 5.3, which states an approximation result for the maximizer of the  $r \to p$  norm, for arbitrary (deterministic) sequences of symmetric matrices satisfying certain asymptotic expansion properties.

It is not hard to see that the maximizing vector for the  $r \to p$  norm of the expectation matrix is given by  $n^{-1/r}\mathbf{1}$ , the scaled n-dimensional vector of all 1's. Thus, the maximizing vector  $\mathbf{v}_n$  corresponding to the random matrix can be viewed as a perturbation of  $n^{-1/r}\mathbf{1}$ , and our result can be thought of as an entrywise perturbation bound of the maximizing vector for the expectation matrix. In contrast with the p=r=2 case, the unavailability of spectral methods for the general  $1 case makes the problem significantly more challenging, which led us to develop a novel approach to characterize the <math>\ell_{\infty}$ -approximation error for a sequence of deterministic matrices satisfying some general conditions.

1.3. Notation and organization. We write [n] to denote the set  $\{1,2,\ldots,n\}$ . We use the standard notation of  $\stackrel{\mathbb{P}}{\to}$  and  $\stackrel{d}{\to}$  to denote convergence in probability and in distribution, respectively. Also, we often use the Bachmann–Landau notation  $O(\cdot)$ ,  $o(\cdot)$ ,  $\Theta(\cdot)$  for asymptotic comparisons. For two positive deterministic sequences  $(f(n))_{n\geq 1}$  and  $(g(n))_{n\geq 1}$ , we write  $f(n) \ll g(n)$  (respectively,  $f(n) \gg g(n)$ ), if f(n) = o(g(n)) (respectively,  $f(n) = \omega(g(n))$ ). For a positive deterministic sequence  $(f(n))_{n\geq 1}$ , a sequence of random variables  $(X(n))_{n\geq 1}$  is said to be  $O_{\mathbb{P}}(f(n))$  and  $o_{\mathbb{P}}(f(n))$ , if the sequence  $(X(n)/f(n))_{n\geq 1}$  is tight and  $X(n)/f(n) \stackrel{\mathbb{P}}{\to} 0$  as  $n \to \infty$ , respectively. For two sequences of real-valued random variables  $(X_n)_{n\geq 1}$  and  $(Y_n)_{n\geq 1}$ , we will write  $X_n \lesssim Y_n$  if there exists some constant c > 0, such that  $\mathbb{P}(X_n \leq cY_n) \to 1$  as  $n \to \infty$ . Normal $(\mu, \sigma^2)$  is used to denote normal distribution with mean  $\mu$  and variance  $\sigma^2$ . For two vectors  $\mathbf{x} = (x_i)_i \in \mathbb{R}^n$  and  $\mathbf{y} = (y_i)_i \in \mathbb{R}^n$ , define the " $\star$ " operation as the entrywise product given by  $\mathbf{z} = \mathbf{x} \star \mathbf{y} = (x_iy_i)_i \in \mathbb{R}^n$ . Define 1 to be the n-dimensional vector of all 1's,  $J_n := \mathbf{11}^T$ , and  $I_n$  to be the n-dimensional identity matrix. Also, 1 $\{\cdot\}$  denotes the indicator function.

The rest of the paper is organized as follows. In Section 2 we state the main results and discuss their ramifications. Section 3 provides a high-level outline of the proofs of the main results. In Section 4 we introduce the basics of the nonlinear power method, which will be a key tool for our analysis, and present some preliminary results. Sections 5 and 6 concern the approximation of the maximizing vector in the deterministic and random cases, respectively. Section 7 presents a two-step approximation of the  $r \to p$  norm and in particular, identifies a functional of the underlying random matrix that is "close" to the  $r \to p$  norm. In Section 8 we prove the asymptotic normality of this approximating functional. Finally, in Section 9, we end by exploring the relation between the  $r \to p$  norm and the  $\ell_p$  Grothendieck problem. Some of the involved but conceptually straightforward calculations are deferred to the Appendix.

- <span id="page-4-0"></span>**2. Main results.** In this section we present our main results. Section 2.1 describes results for random matrices with i.i.d. entries (except possibly the diagonal entries), whereas Section 2.2 states extension of the main results when the matrix entries can have inhomogeneity in their variances. Finally, in Section 2.3 we discuss the implications of our results in two important special cases.
- 2.1. *Matrices with i.i.d. entries*. We start by stating a general set of assumptions on the sequence of random matrices.

ASSUMPTION 1. For each  $n \ge 1$ , let  $F_n$  be a distribution supported on  $[0, \infty)$  and having finite mean  $\mu_n$  and variance  $\sigma_n^2$ . Let  $A_n = (a_{ij}^n)_{i,j=1}^n$  be a symmetric random matrix such that:

- (i)  $(a_{ij}^n)_{i,j=1,i< j}^n$  are i.i.d. random variables with common distribution  $F_n$ . Also,  $a_{ii}^n=0$  for all  $i\in [n]$ .
  - (ii)  $\mu_n = O(1), \mu_n = \omega(\frac{\log^{2/3} n}{n^{1/3}}), \sigma_n \ge n^{-\frac{1}{2} + c_0}$  for some constant  $c_0 > 0$ , and  $\frac{\sigma_n^2}{\mu_n} = O(1)$ .
  - (iii) There exists  $c < \infty$ , such that  $\mathbb{E}[|a_{12}^n \mu_n|^k] \le \frac{k!}{2} c^{k-2} \sigma_n^2$  for all  $k \ge 3$ .

REMARK 2.1. Observe that Assumption 1(ii) is trivially satisfied in the dense regime, where  $\mu_n = \mu$  and  $\sigma_n^2 = \sigma$  are fixed constants, which was the setting considered by Füredi and Komlós in [21]. The weaker conditions imposed in Assumption 1(ii) show that our approach also covers a broad class of sparse matrices. However, the conditions on the sparsity of the matrices are not necessarily optimal, and identifying optimal conditions is beyond the scope of this article. The reasons are elaborated below. The lower bound on  $\sigma_n$  in Assumption 1(ii) is required when we apply existing asymptotic results for second largest eigenvalues of random matrices [30] to approximate the operator norm (see the proof of Lemma 8.1), and the condition on  $\mu_n$  is required in the proof of Lemma 6.1 (to establish well-connectedness), in the approximation step in Lemma 8.3, and in the proof of Theorem 2.2. Indeed, this assumption is used in the strongest form in the final step of the proof of Theorem 2.2; see the two displays below (8.15). The moment conditions in Assumption 1(iii) guarantee concentration of certain relevant polynomials of the matrix elements, which we use to approximate the operator norm. At first sight, they may appear restrictive, but such conditions frequently arise in the literature (cf. [2, 30]), for example, when applying Bernstein's inequality.

2.1.1. Asymptotic normality of the  $r \to p$  norm. Our first main result provides a central limit theorem for the  $r \to p$  norms of random matrices satisfying Assumption 1. Theorem 2.2 is proved in Section 8.2.

THEOREM 2.2. Fix any  $1 . Consider the sequence of random matrices <math>(A_n)_{n \in \mathbb{N}}$  satisfying Assumption 1 and define  $\bar{A}_n := n^{-(\frac{1}{p} - \frac{1}{r})} A_n$ . Then, as  $n \to \infty$ ,

(2.1) 
$$\frac{1}{\sigma_n} (\|\bar{A}_n\|_{r \to p} - \alpha_n(p, r)) \xrightarrow{d} Z \sim \text{Normal}(0, 2),$$

where

(2.2) 
$$\alpha_n(p,r) = (n-1)\mu_n + \left(p - 1 + \frac{1}{r-1}\right) \frac{\sigma_n^2}{2\mu_n}.$$

REMARK 2.3. The assumption that  $a_{ii}^n = 0$  in Theorem 2.2 is not a strict requirement. In fact, one can assume  $a_{ii}^n$ 's to be independent of  $a_{ii}^n$ 's and to be i.i.d. from some distribution  $G_n$ 

<span id="page-5-0"></span>with nonnegative support, mean  $\zeta_n = \Theta(\mu_n^2)$ , variance  $\rho_n^2 = \Theta(\sigma_n^2)$ , and satisfying the moment condition in Assumption 1(iii) with  $\mu_n$  and  $\sigma_n$  replaced by  $\zeta_n$  and  $\rho_n$ , respectively. Then (2.1) holds with

(2.3) 
$$\alpha_n(p,r) = (n-1)\mu_n + \zeta_n + \left(p - 1 + \frac{1}{r-1}\right) \frac{\sigma_n^2}{2\mu_n}.$$

All our proofs go through verbatim in this case, except for a minor modification to Lemma 8.1, which is addressed in Lemma 8.2. However, assuming the diagonal entries to be 0 saves significant additional notational burden and computational complications. For that reason, we will assume  $a_{ii}^n = 0$  throughout the rest of the paper.

REMARK 2.4. As briefly mentioned in the Introduction, an intriguing fact to note from Theorem 2.2 is that although  $\|\bar{A}_n\|_{r\to p}$  is concentrated around  $\|\mathbb{E}[\bar{A}_n]\|_{r\to p}$ , on the CLT scale, there is a nontrivial further O(1) shift  $\alpha_n(p,r)$  in the mean. This is consistent with [21] for the case p=r=2. As we will see in the proof of Theorem 2.2 in Section 8.2, this additional constant shift arises from a Hessian term when we perform the Taylor expansion of a suitable approximation of  $\|A_n\|_{r\to p}$ . It is also worth noting that, if  $\sigma_n^2 \ll \mu_n$  (e.g., when  $F_n$  is an exponential distribution with mean  $\mu_n\to 0$ ), this additional shift vanishes, and thus there may be no shift for certain asymptotically sparse matrix sequences.

REMARK 2.5. There are two noteworthy phenomena about the asymptotic variance of  $\|A_n\|_{r\to p}$ . First, the asymptotic variance does not depend on p, r beyond the scaling factor  $n^{\frac{1}{p}-\frac{1}{r}}$ . Second, if p=r and we are in the dense setting (i.e.,  $\mu_n=\mu>0$  and  $\sigma_n=\sigma>0$ ), the asymptotic variance is a  $\Theta(1)$  quantity, although the mean is  $\Theta(n)$ . The latter is analogous to the rigidity phenomenon for the largest eigenvalue of random matrices. In the  $2\to 2$  norm case when the  $a_{ij}^n$  are uniformly bounded, this constant order of the asymptotic variance can be understood from the application of the bounded difference inequality (see [47], Corollary 2.4, Example 2.5, which considers the case when  $a_{ij}^n$  are Bernoulli). However, as we see in [47], Example 2.5, in order to bound the expected change in the operator norm after changing one entry of the matrix, the fact that  $\ell_2$  is a Hilbert space is crucial, and this method does not generalize directly for  $\ell_p$  spaces with  $p \neq 2$ . Nevertheless, as we have shown in Theorem 2.2, the variance still turns out to be  $\Theta(1)$  for the general p=r case in the dense setting.

2.1.2. The maximizing vector. The second main result is an  $\ell_{\infty}$ -approximation of the maximizing vector in (1.1). To this end, let  $\mathbb{P}_0$  be any probability measure on  $\prod_n \mathbb{R}^{n \times n}$ , such that its projection on  $\mathbb{R}^{n \times n}$  has the same law as  $A_n$ . The following theorem quantifies the proximity of the maximizing vector to 1. Theorem 2.6 is proved at the end of Section 6. An analogue of Theorem 2.6 will later be proved for general deterministic sequence of matrices (see Proposition 5.3). For a sequence of events  $(E_n)_{n\geq 1}$  with  $E_n$  being an event involving  $A_n$ , we say that  $(E_n)_{n\geq 1}$  occurs  $\mathbb{P}_0$ -eventually almost surely if  $E_n$  occurs for all large enough n,  $\mathbb{P}_0$ -almost surely.

THEOREM 2.6. Suppose Assumption 1 holds. Also, let

(2.4) 
$$\mathbf{v}_n := \underset{\mathbf{x} \in \mathbb{R}^n : \|\mathbf{x}\|_r \le 1}{\arg \max} \|A_n \mathbf{x}\|_p$$

and **1** denote the *n*-dimensional vector of all ones. Then the following hold:

<span id="page-6-0"></span>(a) For 1 ,

$$(2.5) \|\mathbf{v}_n - n^{-1/r}\mathbf{1}\|_{\infty} \le \frac{6p}{r-p} n^{-\frac{1}{r}} \sqrt{\frac{\log n}{n\mu_n} \times \frac{\sigma_n^2}{\mu_n}}, \mathbb{P}_0 \text{ eventually almost surely.}$$

(b) For  $p = r \in (1, \infty)$ ,

$$(2.6) \|\mathbf{v}_n - n^{-1/r}\mathbf{1}\|_{\infty} \leq \frac{60r}{r-1} n^{-\frac{1}{r}} \sqrt{\frac{\log n}{n\mu_n} \times \frac{\sigma_n^2}{\mu_n}}, \mathbb{P}_0 \text{ eventually almost surely.}$$

REMARK 2.7. We will see in Section 5 that the vector bound for the p < r case holds when  $A_n^T A_n$  is irreducible and  $A_n$  has concentrated row sums. These two properties, and hence the result in (2.5) is established (in Proposition 5.3) under a weaker set of assumptions than Assumption 1.

2.2. Matrices with inhomogeneous variance profile. We now consider random matrices having an inhomogeneous variance profile. In this case, to prove the asymptotic normality result we need the matrix to be dense (i.e., the matrix entries have asymptotically nonvanishing mean and variance). This is because our proof uses an upper bound on the second largest eigenvalue of the matrix, recently established in [2], which requires the matrix to be dense. The  $\ell_{\infty}$ -approximation of the maximizing vector, however, still holds for analogous sparse matrices.

We start by stating the set of assumptions on the sequence of random matrices that are needed for the  $\ell_{\infty}$ -approximation of the maximizing vector.

ASSUMPTION 2. For each fixed  $n \ge 1$ , let  $A_n = (a_{ij}^n)_{i,j=1}^n$  be a symmetric random matrix such that:

- (i)  $(a_{ij}^n)_{i,j=1,i< j}^n$  is a collection of independent random variables with  $a_{ij}^n$  having distribution  $F_{ij}^n$  supported on  $[0,\infty)$ , mean  $\mu_n$  and variance  $\sigma_n^2(i,j)$ . Also,  $a_{ii}^n=0$  for all  $i\in [n]$ .
  - (ii) There exists a sequence  $(\bar{\sigma}_n)_{n\in\mathbb{N}}\subset(0,\infty)$ , and constants  $c_*,c^*\in(0,\infty)$  such that

$$c_* \leq \liminf_{n \to \infty} \min_{1 \leq i < j \leq n} \frac{\sigma_n(i, j)}{\bar{\sigma}_n} \leq \limsup_{n \to \infty} \max_{1 \leq i < j \leq n} \frac{\sigma_n(i, j)}{\bar{\sigma}_n} \leq c^*.$$

- (iii)  $\mu_n$  and  $\bar{\sigma}_n$  satisfies Assumption 1(ii) by replacing  $\sigma_n$  by  $\bar{\sigma}_n$ .
- (iv) There exists c > 0, such that

(2.7) 
$$\max_{1 \le i \le j \le n} \mathbb{E}[|a_{ij}^n - \mu_n|^k] \le \frac{k!}{2} c^{k-2} \bar{\sigma}_n^2 \quad \text{for all } k \ge 3.$$

THEOREM 2.8. Suppose  $A_n$  is a symmetric random matrix satisfying Assumption 2. Also, as in (2.4), recall that

$$v_n := \underset{\boldsymbol{x} \in \mathbb{R}^n: \|\boldsymbol{x}\|_p \le 1}{\arg \max} \|A_n \boldsymbol{x}\|_p.$$

Then  $\mathbf{v}_n$  satisfies the same approximations as in (2.5) and (2.6), but with  $\sigma_n$  replaced by  $\bar{\sigma}_n$ .

Theorem 2.8 is proved at the end of Section 6. Next, we state the asymptotic normality result.

<span id="page-7-0"></span>THEOREM 2.9. Fix any  $1 . Consider the sequence of random matrices <math>(A_n)_{n \in \mathbb{N}}$  satisfying Assumption 2 and define  $\bar{A}_n := n^{-(\frac{1}{p} - \frac{1}{r})} A_n$ . Also assume that  $\liminf_{n \to \infty} \bar{\sigma}_n > 0$ . Then as  $n \to \infty$ ,

(2.9) 
$$\frac{n^2}{2\sqrt{\sum_{i < j} \sigma_n^2(i, j)}} (\|\bar{A}_n\|_{r \to p} - \alpha_n(p, r)) \xrightarrow{d} Z \sim \text{Normal}(0, 2),$$

where

(2.10) 
$$\alpha_n(p,r) = (n-1)\mu_n + \left(p - 1 + \frac{1}{r-1}\right) \frac{\sum_{i < j} \sigma_n^2(i,j)}{n^2 \mu_n}.$$

Theorem 2.9 is proved in Section 8.2.

Similar to Remark 2.3, the zero diagonal entry is not a strict requirement in Theorem 2.9. The expression of  $\alpha_n(p,r)$  in (2.10) can be suitably updated to accommodate nonnegative random diagonal entries.

# 2.3. Special cases.

Adjacency matrices of Erdős–Rényi random graphs. Let  $ER_n(\mu_n)$  denote an Erdős–Rényi random graph with n vertices and connection probability  $\mu_n$ . As an immediate corollary to Theorems 2.2 and 2.6, we obtain the asymptotic normality for adjacency matrices of certain sequences of  $ER_n(\mu_n)$  graphs.

COROLLARY 2.10. Fix any  $1 and let <math>A_n$  denote the adjacency matrix of  $ER_n(\mu_n)$ . For  $\mu_n = \omega(n^{-\frac{1}{3}}\log^{2/3}n)$ , the vector bounds in (2.5) and (2.6), and the asymptotic normality result in (2.1) hold with  $\sigma_n^2 = \mu_n(1 - \mu_n)$ .

Grothendieck's  $\ell_r$ -problem. We now investigate the behavior of the  $\ell_r$  quadratic maximization problem, also known as the  $\ell_r$  Grothendieck problem. For any  $n \times n$  matrix  $A_n$ , the  $\ell_r$  Grothendieck problem concerns the solution to the following quadratic maximization problem. For  $r \geq 2$ , define

$$(2.11) M_r(A_n) := \sup_{\|\boldsymbol{x}\|_r < 1} \boldsymbol{x}^T A_n \boldsymbol{x}.$$

In general, finding  $M_r(A_n)$  is NP-hard [28]. However, in the case of a matrix A with non-negative entries, for which  $A^TA$  is irreducible, Proposition 2.11 below states that the  $\ell_r$  Grothendieck problem is a special case of the  $r \to p$  norm problem.

PROPOSITION 2.11. Let A be a symmetric matrix with nonnegative entries such that  $A^TA$  is irreducible. Then for any  $r \ge 2$ ,  $M_r(A) = ||A||_{r \to r^*}$ , where  $r^* = r/(r-1)$  is the Hölder conjugate of r.

Proposition 2.11 is proved at the end of Section 9. Together with Theorem 2.2, this immediately yields the limit theorem for  $\bar{A}_n := n^{-(1-\frac{2}{r})} A_n$  stated in the corollary below.

COROLLARY 2.12. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of random matrices satisfying the assumptions of Theorem 2.2. Then for any fixed  $r \in [2, \infty)$ , as  $n \to \infty$ , the asymptotic normality result in (2.1) holds for  $M_r(\bar{A}_n)$  with  $p = r^* = r/(r-1)$ .

## **3. Proof outline.** The proof of Theorem 2.2 consists of three major steps:

Step 1: Approximating the maximizing vector. The first step is to find a good approximation for a maximizing vector  $\mathbf{v}_n$  for  $||A_n||_{r\to p}$ , as defined in (2.4). As stated in Theorem 2.6, we

<span id="page-8-0"></span>can precisely characterize the  $\ell_{\infty}$  distance between  $v_n$  and  $n^{-1/r}\mathbf{1}$ , the scaled vector of all ones in  $\mathbb{R}^n$ . In fact we work with a general *deterministic* sequence of symmetric nonnegative matrices (see Proposition 5.3). When p < r, the required  $\ell_{\infty}$ -bound follows whenever the row sums are approximately the same, which we call *almost regularity* (see Definition 5.1). We actually have a short and elementary proof when p < r. The proof for the case p = r is more complicated and requires that the entries of  $A_n^T A_n$  be of order  $n\mu_n^2$ . We call the latter property, which is stated more precisely in Definition 5.2, *well-connectedness*.

Step 2: Approximating the  $r \to p$  norm. The next step is to construct a suitable approximation of  $||A_n||_{r\to p}$ . With the strong bound in Theorem 2.6, a natural choice would be to approximate  $||A_n||_{r\to p}$  by  $||A_n n^{-1/r} \mathbf{1}||_p$ . However, such an approximation turns out to be insufficient on the CLT-scale. To this end, we use a nonlinear power iteration for finding  $r \to p$  norms, introduced by Boyd [9]. We start the power iteration from the vector  $\mathbf{v}_n^{(0)} := n^{-1/r} \mathbf{1}$ . We show that the rate of convergence of this power-method depends on the proximity of  $\mathbf{v}_n^{(0)}$  to  $\mathbf{v}_n$  (which we now have from Theorem 2.6), and the second largest eigenvalue of  $A_n$  (for which we use existing results from [2, 18, 30]). Our ansatz is that after only one step of Boyd's nonlinear power iteration, we arrive at a suitable approximation of  $||A_n||_{r\to p}$ . For any  $k \ge 1$ ,  $t \in \mathbb{R}$ , and  $\mathbf{x} = (x_1, \dots, x_n)$ , define  $\psi_k(t) := |t|^{k-1} \operatorname{sgn}(t)$ , and  $\Psi_k(\mathbf{x}) = (\psi_k(x_i))_{i=1}^n$ . Then we show that (see Proposition 7.1) the quantity

(3.1) 
$$||A_n||_{r\to p} \approx \eta(A_n) := \frac{||A_n \Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))||_p}{||\Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))||_r},$$

where  $r^* := r/(r-1)$  denotes the Hölder conjugate of r, provides the required approximation to  $||A_n||_{r\to p}$ . As in Step 1, we also first show this approximation for a deterministic sequence of matrices satisfying certain conditions, and then show that the random matrices we consider almost surely satisfy these conditions.

Step 3: Establishing asymptotic normality. The final step is to prove the asymptotic normality of the sequence  $\{\eta(A_n)\}_{n\in\mathbb{N}}$ . This is a nonlinear function, and as it turns out, the state-of-the-art approaches to prove CLT do not apply directly in our case. For that reason, we resort to an elementary approach using the Taylor expansion to obtain the limit law. Loosely speaking, we show that

$$\eta(A_n) \approx n^{\frac{1}{p} - \frac{1}{r} - 1} \sum_{i,j} a_{ij}^n + \frac{1}{2} \left( p - 1 + \frac{1}{r - 1} \right) n^{\frac{1}{p} - \frac{1}{r}} \sum_{i,j} (a_{ij}^n - \mu)^2,$$

which after appropriate centering and scaling yields the CLT result as stated in Theorem 2.2.

## 4. Preliminaries.

4.1. Boyd's nonlinear power method. We start by introducing the nonlinear power iteration method and stating some preliminary known results, along with a rate of convergence result that will be crucial for our treatment. The framework for nonlinear power iteration was first proposed by Boyd [9]. It has also been used in [4] to obtain approximation algorithms for the  $r \to p$  norm of matrices with strictly positive entries.

Henceforth, we fix  $n \in \mathbb{N}$ , and for notational simplicity, omit the subscript n, for example, using A to denote  $A_n$ , etc. Let A be an  $n \times n$  matrix with nonnegative entries. For any  $x \neq 0$ , define the function  $f(x) := ||Ax||_p / ||x||_r$ , and set  $\gamma := \sup_{x \neq 0} f(x)$ . If a vector v is a local maximum (or, more generally, critical point) of the function f, then since f is smooth, the gradient of f must vanish at that point. This critical point can further be written as the solution to a fixed point equation. Now, if there is a unique positive critical point, the fixed point

<span id="page-9-0"></span>equation may potentially be used to construct an iteration that converges to the maximum, starting from a suitable positive vector. In fact, under suitable assumptions, this convergence can be proved to be geometrically fast. The above description is briefly formalized below. For q > 1,  $t \in \mathbb{R}$  and  $x \in \mathbb{R}^n$ , define

(4.1) 
$$\psi_q(t) := |t|^{q-1} \operatorname{sgn}(t), \qquad \Psi_q(\mathbf{x}) := (\psi_q(x_i))_{i=1}^n,$$

where sgn(t) = -1, 1, and 0, for t < 0, t > 0, and t = 0, respectively. Taking the partial derivative of f with respect to  $x_i$ , we obtain, for  $x \neq 0$ ,

$$(4.2) \quad \frac{\partial f(\mathbf{x})}{\partial x_i} = \|\mathbf{x}\|_r^{-2} [\|A\mathbf{x}\|_p^{-(p-1)} \langle \Psi_p(A\mathbf{x}), A_i^T \rangle \|\mathbf{x}\|_r - \|\mathbf{x}\|_r^{-(r-1)} \psi_r(x_i) \|A\mathbf{x}\|_p],$$

where  $A_i$  denotes the *i*th column of A. Equating (4.2) to zero for i = 1, ..., n, yields

(4.3) 
$$\|\mathbf{x}\|_{r}^{r} A^{T} \Psi_{p}(A\mathbf{x}) = \|A\mathbf{x}\|_{p}^{p} \Psi_{r}(\mathbf{x}).$$

Now, let u with  $||u||_r = 1$  be a (normalized) solution to (4.3) and set  $\gamma(u) := ||Au||_p$ . Then straightforward algebraic manipulations show that

(4.4) 
$$\Psi_{r^*}(A^T\Psi_p(A\boldsymbol{u})) = (\gamma(\boldsymbol{u}))^{p(r^*-1)}\boldsymbol{u},$$

where recall that  $r^* = r/(r-1)$ . We denote the operator arising on the left-hand side of (4.4) as follows:

(4.5) 
$$Sx := \Psi_{r^*} (A^T \Psi_p (Ax)), \qquad Wx := \frac{Sx}{\|Sx\|_r} \quad \text{for } x \neq \mathbf{0}.$$

Then (4.4) implies

$$(4.6) Su = (\gamma(u))^{p(r^*-1)}u, Wu = u,$$

where the last equality uses the fact that  $\|\mathbf{u}\|_r = 1$ . Thus, any solution to (4.4) is a fixed point of the operator W. The following lemma proves uniqueness of this fixed point among all nonnegative vectors, which can be viewed as a generalization of the classical Perron-Frobenius theorem. The uniqueness in Lemma 4.1 was established for matrices with strictly positive entries in [4], Lemma 3.4. Below we show that their proof can be adapted to matrices with nonnegative entries when  $A^T A$  is irreducible.

LEMMA 4.1. Assume that  $A^T A$  is irreducible. Then (4.4) has a unique solution  $\mathbf{v}$  among the set of all nonnegative vectors. Further,  $\mathbf{v}$  has all positive entries.

PROOF. First note that the maximizer of  $||Ax||_p/||x||_r$  over  $x \neq 0$  (which always exists) satisfies (4.4). Also, all entries of such a maximizer are nonnegative. To see this, if x has a negative entry, then the value of  $||Ax||_p$  can be strictly increased by replacing the negative entry by its absolute value, without changing  $||x||_r$ .

Next, we show that, when  $A^T A$  is irreducible, any nonzero, nonnegative vector satisfying (4.4) must have strictly positive entries. This, in particular, will also prove that v has all positive entries. We argue by contradiction. Let x be a nonzero, nonnegative vector satisfying (4.4) and suppose,  $i \in [n]$  be such that  $x_i = 0$ . Then, by (4.4) and (4.6) we have

(4.7) 
$$(S\mathbf{x})_i = 0 \implies (A^T (\Psi_p(A\mathbf{x}))_i = \sum_{i=1}^n a_{ji} \left| \sum_{k=1}^n a_{jk} x_k \right|^{p-1} = 0.$$

<span id="page-10-0"></span>In fact, we have

$$(4.8) \qquad (S\mathbf{x})_i = 0 \quad \Longrightarrow \quad (A^T A\mathbf{x})_i = \sum_{j=1}^n a_{ji} \left(\sum_{k=1}^n a_{jk} x_k\right) = 0,$$

since all the elements of A and x are nonnegative, if  $A^T \Psi_p(Ax) = 0$ , then  $\Psi_2(A^T \Psi_2(Ax)) = 0$  as well. Observe that (4.8) implies  $x_j = 0$  for all  $j \in [n]$  for which there exists  $j' \in [n]$  with  $a_{j'i} > 0$  and  $a_{j'j} > 0$ . Repeating the above with i replaced by any such j, we conclude that  $x_j = 0$ . Continuing in this way and using the irreducibility of  $A^T A$ , it follows that  $x_j = 0$  for all j = 1, ..., n, which this leads to a contradiction. Thus, x must have strictly positive entries.

To show uniqueness, let  $u \neq v$  be two nonnegative nonzero vectors satisfying (4.4) with  $\|u\|_r = \|v\|_r = 1$ . Further, without loss of generality, assume that  $\|Au\|_p \leq \|Av\|_p$ . By the above argument, both u and v have all positive entries. Then there must exist  $\theta \in (0, 1]$  such that  $u - \theta v$  has a zero coordinate. Let  $\theta$  be the smallest such number. Define  $U := \{k : u_k - \theta v_k = 0\}$ , and note that  $u_j - \theta v_j > 0$  for all  $j \in U^c$ . Since  $\|u\|_r = \|v\|_r$  and  $u \neq v$ , it follows that  $U^c \neq \emptyset$ .

CLAIM 1. There exists  $k \in U$  such that

$$(S\boldsymbol{u})_k > (S\boldsymbol{\theta}\boldsymbol{v})_k = \theta^{\frac{p-1}{r-1}} (S\boldsymbol{v})_k.$$

PROOF. First, note that since  $A^TA$  is irreducible, there exists  $k_1 \in U$ ,  $k_2 \in [n]$ , and  $k_3 \in U^c$ , such that both  $a_{k_1k_2}$  and  $a_{k_2k_3}$  are positive. Therefore, the inequalities  $u_{k_3} > \theta v_{k_3}$ ,  $a_{k_2k_3} > 0$ ,  $u_i \ge \theta v_i$  for all  $i \in [n]$  (the latter holds by the minimality of  $\theta$ ), and the nonnegativity of A, u, and v yield

$$(4.10) \quad \big(\Psi_p(A\boldsymbol{u})\big)_{k_2} > \big(\Psi_p\big(A(\theta\boldsymbol{v})\big)\big)_{k_2} \quad \text{and} \quad \big(\Psi_p(A\boldsymbol{u})\big)_i \geq \big(\Psi_p\big(A(\theta\boldsymbol{v})\big)\big)_i \quad \text{for all } i \in [n].$$

This, together with the fact that  $a_{k_1k_2} > 0$ , implies  $(A^T \Psi_p(A \boldsymbol{u}))_{k_1} > (A^T \Psi_p(A(\theta \boldsymbol{v})))_{k_1}$ , and by (4.5), (4.9) holds with  $k = k_1$ .  $\square$ 

Now fix some  $k \in U$  satisfying (4.9). Then, using (4.4), one observes that

(4.11) 
$$\gamma(\mathbf{u})^{p} = \frac{(S\mathbf{u})_{k}^{r-1}}{u_{k}^{r-1}} > \frac{\theta^{p-1}(S\mathbf{v})_{k}^{r-1}}{(\theta v_{k})^{r-1}} = \theta^{p-r} \gamma(\mathbf{v})^{p}.$$

Since  $p \le r$  and  $\theta \in (0, 1]$ , this yields  $||A\boldsymbol{u}||_p = \gamma(\boldsymbol{u}) > \gamma(\boldsymbol{v}) = ||A\boldsymbol{v}||_p$ , which contradicts the initial assumption that  $||A\boldsymbol{u}||_p \le ||A\boldsymbol{v}||_p$ . This proves the uniqueness.  $\square$ 

The (nonlinear) power iteration for finding  $\gamma$  consists of the following iterative method: Let  $\mathbf{v}^{(0)}$  be a vector with positive entries and  $\|\mathbf{v}^{(0)}\|_r = 1$ . Then for  $k \ge 0$ , define

$$v^{(k+1)} := Wv^{(k)}.$$

In general, the above iteration may not converge to the global maximum  $\gamma$ . However, as the following result states, if in addition to having nonnegative entries, the matrix  $A^TA$  is irreducible, then the iteration must converge to the unique positive fixed point.

PROPOSITION 4.2 ([9], Theorem 2). Fix any  $1 . Let A be a matrix with nonnegative entries such that <math>A^TA$  is irreducible. If  $\mathbf{v}^{(0)}$  has all positive entries, then  $\lim_{k\to\infty} \|A\mathbf{v}^{(k)}\|_p = \gamma$ .

<span id="page-11-0"></span>4.2. Rate of convergence. Due to Lemma 4.1, henceforth we will reserve the notation  $\mathbf{v}$  to denote the unique maximizer in (1.1) having positive entries and  $\|\mathbf{v}\|_r = 1$ . The notation  $\gamma = \gamma(\mathbf{v}) = \|A\mathbf{v}\|_p$  denotes the operator norm  $\|A\|_{r \to p}$ . Next, we will study the rate of convergence of  $\mathbf{v}^{(k)}$  to  $\mathbf{v}$ . Specifically, we obtain a fast convergence rate once the approximating vector comes within a certain small neighborhood of the maximizing vector. The rate of convergence result builds on the line of arguments used in the proof of [9], Theorem 3. However, as it turns out, since we are interested in the asymptotics in n, the rate obtained in [9] does not suffice (see, in particular, [9], equation 16), and we need the sharper result stated in Proposition 4.3.

Recall for any  $x, y \in \mathbb{R}^n$ , we write  $x \star y = (x_i y_i)_i$ . Define the linear transformation

$$(4.13) Bx := |v|^{2-r} \star A^T (|Av|^{p-2} \star (Ax)),$$

and the inner product

$$(4.14) [x, y] := \langle |v|^{r-2} \star x, y \rangle.$$

When  $A^T A$  is irreducible, v has all positive entries by Lemma 4.1, and thus (4.13) and (4.14) are well defined for all  $p, r \ge 1$ . Observe that this inner product induces a norm, which will henceforth be referred to as the "v-norm":

(4.15) 
$$||x||_{v} := [x, x]^{1/2} = (|v|^{r-2}, |x|^{2})^{1/2}.$$

It is worthwhile to note that  $\|\mathbf{v}\|_{\mathbf{v}}^2 = \|\mathbf{v}\|_r^r$  and  $[B\mathbf{v}, \mathbf{v}]^2 = \|A\mathbf{v}\|_p^p$ . The following fact is immediate.

FACT. The operator B is symmetric and positive semi-definite with respect to the inner product in (4.14).

Fact 4.2 implies that the eigenspace of B has n orthonormal basis vectors and n nonnegative eigenvalues corresponding to the Rayleigh quotient

(4.16) 
$$\frac{[Bx,x]}{[x,x]} = \frac{\langle |Av|^{p-2}, |Ax|^2 \rangle}{\langle |v|^{r-2}, |x|^2 \rangle}.$$

Henceforth, we will refer to (4.16) as the v-Rayleigh quotient to emphasize the dependence on v. Using (4.4), note that  $Bv = \gamma^p v$ , and hence,  $\gamma^p$  is an eigenvalue of B. Let  $\lambda_2 \ge \lambda_3 \ge \cdots \ge \lambda_n$  be the other eigenvalues. In fact, as shown in the proof of [9], Theorem 3,  $\gamma^p$  is the largest eigenvalue of B and is simple.

Now, recall that the convergence rate of the classical (linear) power iteration for the largest eigenvalue of matrices depends on the the ratio between the largest and the second largest eigenvalues. As it is stated in the proposition below, in the nonlinear case, this rate depends on the ratio of the largest and second largest eigenvalues of the operator B.

PROPOSITION 4.3. Let A be an  $n \times n$  matrix with nonnegative entries such that  $A^TA$  is irreducible and 1 . Also let <math>y have all positive entries. There exists  $\varepsilon_0 = \varepsilon_0(p,r) > 0$  and C = C(p,r) > 0, both independent of n, such that if  $\|y - v\|_{\infty} \le \varepsilon$ , then

(4.17) 
$$\|Wy - v\|_{v} \le (1 + C\varepsilon) \frac{(p-1)\lambda_{2}}{(r-1)\gamma^{p}} \|y - v\|_{v}.$$

Consequently, if for some  $k \ge 1$  and  $\varepsilon \le \varepsilon_0$ ,  $\boldsymbol{v}^{(k)}$  has all positive entries and  $\|\boldsymbol{v}^{(k)} - \boldsymbol{v}\|_{\infty} \le \varepsilon$ , then

(4.18) 
$$\| \boldsymbol{v}^{(k+1)} - \boldsymbol{v} \|_{\boldsymbol{v}} \le (1 + C\varepsilon) \frac{(p-1)\lambda_2}{(r-1)\nu^p} \| \boldsymbol{v}^{(k)} - \boldsymbol{v} \|_{\boldsymbol{v}}.$$

<span id="page-12-0"></span>REMARK 4.4. It is worthwhile to point out that the convergence rate of the nonlinear power method depends on quantities in terms of the v-norm, which depends on the maximizer v. Thus it might not be clear why this gives a useful rate of convergence. However, as we will see in Lemma 7.3, the  $\ell_{\infty}$ -bound on the maximizing vector in the nonlinear case, stated in Proposition 5.3, enables us to obtain the desired rate of convergence result.

PROOF OF PROPOSITION 4.3. For any two fixed vectors x,  $h \in \mathbb{R}^n$ , and a function f, let us denote the directional derivative of f at x as

$$\delta f(\mathbf{x}; \mathbf{h}) := \lim_{\varepsilon \to 0} \frac{1}{\varepsilon} (f(\mathbf{x} + \varepsilon \mathbf{h}) - f(\mathbf{x})),$$

whenever the limit exists. Recall that  $x \star y$  denotes the vector  $(x_i y_i)_i$ . Now, fix 1 . First, note that for a vector <math>x with all positive entries,  $\delta \Psi_p(x; h) = (p-1)\Psi_{p-1}(x) \star h$ , and therefore,

(4.19) 
$$\delta S(\mathbf{x}; \mathbf{h}) = (r^* - 1)\Psi_{r^* - 1}(A^T \Psi_p A \mathbf{x}) \star (A^T ((p - 1)\Psi_{p - 1}(A \mathbf{x}) \star A \mathbf{h}))$$
$$= \frac{p - 1}{r - 1}\Psi_0(A^T \Psi_p(A \mathbf{x})) \star S \mathbf{x} \star L(\mathbf{x}; \mathbf{h}),$$

where  $\Psi_0(z) = (1/z_i)_i$  for a vector z with all positive entries and  $L(x; h) := A^T(\Psi_{p-1}(Ax) \star Ah)$ . Here, due to the irreducibility of  $A^TA$ , note that  $A^T\Psi_p(Ax)$  has all positive entries whenever x does. Also, for  $g(x) := \|Sx\|_r$ , using (4.5) and (4.19), we see that

$$\delta g(\boldsymbol{x}; \boldsymbol{h}) = \frac{1}{r} \frac{1}{\|S\boldsymbol{x}\|_r^{r-1}} \langle r\Psi_r(S\boldsymbol{x}), \delta S(\boldsymbol{x}; \boldsymbol{h}) \rangle$$

$$= \frac{p-1}{r-1} \frac{1}{\|S\boldsymbol{x}\|_r^{r-1}} \langle A^T \Psi_p(A\boldsymbol{x}), \Psi_0(A^T \Psi_p(A\boldsymbol{x})) \star S\boldsymbol{x} \star L(\boldsymbol{x}; \boldsymbol{h}) \rangle$$

$$= \frac{p-1}{r-1} \frac{1}{\|S\boldsymbol{x}\|_r^{r-1}} \langle S\boldsymbol{x}, L(\boldsymbol{x}; \boldsymbol{h}) \rangle = \frac{p-1}{r-1} \frac{1}{\|S\boldsymbol{x}\|_r^r} \langle W\boldsymbol{x}, L(\boldsymbol{x}; \boldsymbol{h}) \rangle.$$

Now observe that since  $Wx ||Sx||_r = Sx$ ,

(4.21) 
$$\delta W(\mathbf{v}, \mathbf{h}) \| S \mathbf{v} \|_r + W(\mathbf{v}) \delta g(\mathbf{v}; \mathbf{h}) = \delta S(\mathbf{v}; \mathbf{h}).$$

Therefore, from (4.19) and (4.20) it follows that

$$(4.22) \delta W(\boldsymbol{v}; \boldsymbol{h}) = \left(\frac{p-1}{r-1}\right) \frac{1}{\|S\boldsymbol{v}\|_r^{r-1}} \left[ |W\boldsymbol{v}|^{2-r} \star L(\boldsymbol{v}; \boldsymbol{h}) - W\boldsymbol{v} \langle W\boldsymbol{v}, L(\boldsymbol{v}; \boldsymbol{h}) \rangle \right],$$

where we have used the fact that v and Wv have nonnegative entries Now,  $\delta W(v;\cdot)$  is a linear transformation. Clearly,  $\delta W(v;v)=0$  since  $L(v;v)=\Psi_r(Sv)$ . Further, it follows that the eigenvectors of  $\delta W(v;\cdot)$  corresponding to the nonzero eigenvalues coincide with the eigenvectors of B defined in (4.13) corresponding to  $\lambda_2,\ldots,\lambda_n$  given by (4.16). This follows since  $Bh=\lambda h$  for some nonzero  $\lambda\neq\gamma$  implies that  $L(v;h)=\lambda|v|^{r-2}\star h$ , which together with  $Wv\propto v$  yields that

$$\langle W\mathbf{v}, L(\mathbf{v}; h) \rangle \propto \langle \mathbf{v}, |\mathbf{v}|^{r-2} \star \mathbf{h} \rangle = [\mathbf{v}, \mathbf{h}] = 0.$$

Thus the second term in (4.22) is zero. Also the first term in (4.22) is proportional to v, which yields the equality of the eigenvectors. In fact, the eigenvalues of  $\delta W(v;\cdot)$  are given by  $\frac{p-1}{r-1}\gamma^{-p}\lambda_i$ . Since the Rayleigh coefficients in (4.16) are computed with respect to the  $\|\cdot\|_v$  norm, we have

$$(4.24)$$

<span id="page-13-0"></span>Now, for  $t \in [0, 1]$ , define  $y_t = v + t(y - v)$ . Note that  $y_t$  has all positive entries, since v has positive entries, and y. Thus, the same expression as (4.22) holds for  $\delta W(y_t; h)$ , with v replaced by  $y_t$ . Now,  $||y_t - v||_{\infty} \le ||y - v||_{\infty} \le \varepsilon$ , for any  $t \in [0, 1]$ . Using the fact that  $(1 + \varepsilon)^a = 1 + O(\varepsilon)$ , it follows that there exists a constant  $C < \infty$  and  $\varepsilon_0 > 0$  both depending only on p, r, such that for all  $\varepsilon \le \varepsilon_0$ ,

$$\delta W(\mathbf{y}_t; \mathbf{h}) \le (1 + C\varepsilon)\delta W(\mathbf{v}; \mathbf{h}).$$

Now, observe that

$$\delta W(\mathbf{y}_t; \mathbf{y} - \mathbf{v}) = \frac{\mathrm{d}}{\mathrm{d}t} (W \mathbf{y}_t),$$

and therefore, using (4.6) and the fact that  $y_0 = v$  and  $y_1 = y$ , we obtain

(4.26) 
$$W\mathbf{y} - \mathbf{v} = W\mathbf{y} - W\mathbf{v} = \int_0^1 \delta W(\mathbf{y}_t; \mathbf{y} - \mathbf{v}) \, \mathrm{d}t.$$

Thus, (4.24) and (4.25) implies that

(4.27) 
$$\|Wy - v\|_{v} \le (1 + C\varepsilon) \frac{(p-1)\lambda_{2}}{(r-1)\gamma^{p}} \|y - v\|_{v},$$

and the proof follows.  $\square$ 

**5.** An  $\ell_{\infty}$ -approximation of the maximizer. Given an  $n \times n$  nonnegative matrix  $A_n = (a_{ij}^n)$  and  $V \subseteq [n]$ , we write

(5.1) 
$$d_n(i, V) := \sum_{i \in V} a_{ij}^n, \quad i = 1, \dots, n.$$

Also, we simply write  $d_n(i) = d_n(i, [n])$ . When  $A_n$  is the adjacency matrix of a graph on n vertices,  $d_n(i)$  represents the (out)-degree of vertex i.

DEFINITION 5.1 (Almost regular). A sequence of matrices  $(A_n)_{n\in\mathbb{N}}$  is called  $(\varepsilon_n, \mu_n)_{n\in\mathbb{N}}$  almost regular if there exists an  $n_0 \ge 1$  such that for all  $n \ge n_0$ 

(5.2) 
$$\max_{i \in [n]} |d_n(i) - n\mu_n| \le n\mu_n \varepsilon_n.$$

In order to show the proximity of the maximizing vector to  $n^{-1/r}\mathbf{1}$  for the p=r case, we need another asymptotic property in addition to the almost regularity defined above.

DEFINITION 5.2 (Well-connected). For a constant  $C^* \in (0, \infty)$ , a sequence of matrices  $(A_n)_{n \in \mathbb{N}}$  is called  $(C^*, \mu_n)_{n \in \mathbb{N}}$  well-connected if there exists an  $n_0 \ge 1$ , such that for all  $n \ge n_0$  and  $i, j \in [n], \sum_{k \in [n]} a_{ik}^n a_{kj}^n \ge C^* n \mu_n^2$ .

When  $A_n$  is an adjacency matrix, the well-connected property ensures that there are sufficiently many 2-hop paths between any two sets of vertices. We now state the main result of this section:

PROPOSITION 5.3. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of symmetric matrices with nonnegative entries, such that  $A_n^TA_n$  is irreducible for all  $n\in\mathbb{N}$ . Assume that there exists  $(\varepsilon_n)_{n\in\mathbb{N}}\subset (0,\infty)$  with  $\varepsilon_n\to 0$ , and  $(\mu_n)_{n\in\mathbb{N}}\subset (0,1)$ , such that  $(A_n)_{n\in\mathbb{N}}$  is  $(\varepsilon_n,\mu_n)_{n\in\mathbb{N}}$  almost regular. For each  $n\in\mathbb{N}$ , let  $\mathbf{v}_n$  be the maximizing vector for  $\|A_n\|_{r\to p}$ , as defined in (2.4). Then there exists an  $n_0\geq 1$ , such that the following hold:

<span id="page-14-0"></span>(a) For  $1 , and for all <math>n \ge n_0$ ,

(5.3) 
$$\|\mathbf{v}_n - n^{-1/r}\mathbf{1}\|_{\infty} \leq \frac{2p}{r-p} n^{-\frac{1}{r}} (\varepsilon_n + O(\varepsilon_n^2)).$$

(b) For  $p = r \in (1, \infty)$ , further assume that  $(A_n)_{n \in \mathbb{N}}$  is  $(C^*, \mu_n)_{n \in \mathbb{N}}$  well-connected for some constant  $C^* > 0$ . Then for all  $n \ge n_0$ ,

(5.4) 
$$\|\mathbf{v}_n - n^{-1/r}\mathbf{1}\|_{\infty} \le \frac{10r}{C^*(r-1)} \varepsilon_n n^{-\frac{1}{r}}.$$

We prove Proposition 5.3(a) and (b) in Sections 5.1 and 5.2, respectively.

5.1. Maximizer for the case p < r. Given a maximizing vector  $\mathbf{v}_n$  for  $||A_n||_{r \to p}$  as in (2.4), define

(5.5) 
$$m_n := \min_{i=1,\dots,n} v_{n,i}, \text{ and } M_n := \max_{i=1,\dots,n} v_{n,i}.$$

Let  $(\varepsilon_n, \mu_n)_{n \in \mathbb{N}}$  with  $\varepsilon_n \to 0$  be as in the statement of Proposition 5.3. Suppose we can show that, for all sufficiently large n, and for some  $C \in (0, \infty)$ ,

(5.6) 
$$\frac{m_n}{M_n} \ge 1 - C\varepsilon_n + O(\varepsilon_n^2).$$

Then,  $1 = \sum_{i} v_{n,i}^r \le n M_n^r$ , so that  $M_n \ge n^{-1/r}$ . Also, (5.6) yields

$$1 = \sum_{i=1}^{n} v_{n,i}^{r} \ge n m_{n}^{r} \ge n M_{n}^{r} (1 - rC\varepsilon_{n} + O(\varepsilon_{n}^{2})).$$

Together, this shows that

$$\|\mathbf{v}_n - n^{-1/r}\mathbf{1}\|_{\infty} \le Cn^{-\frac{1}{r}}(\varepsilon_n + O(\varepsilon_n^2)).$$

Thus, to show Proposition 5.3, it is enough to prove (5.6) with  $C = \frac{2p}{r-p}$ .

Recall Definition 5.1 and the associated notation in (5.1). Using (4.6), (4.5), and (4.1), together with  $r^* - 1 = 1/(r - 1)$ , and the fact that  $A_n$  is nonnegative and symmetric, we can use (5.1) and (5.2) to conclude that for any j,

$$(Sv_{n})_{j} = (\Psi_{r}^{*}(A_{n}^{T}\Psi_{p}(A_{n}v_{n})))_{j} = |(A_{n}^{T}\Psi_{p}(A_{n}v_{n}))_{j}|^{\frac{1}{r-1}}$$

$$\leq \left(\sum_{i=1}^{n} a_{ij}^{n} (M_{n}d_{n}(i))^{p-1}\right)^{\frac{1}{r-1}}$$

$$\leq \left(\sum_{i=1}^{n} a_{ji}^{n} (M_{n}n\mu_{n}(1+\varepsilon_{n}))^{p-1}\right)^{\frac{1}{r-1}}$$

$$\leq ((M_{n}n\mu_{n})^{p-1}(1+\varepsilon_{n})^{p-1}n\mu_{n}(1+\varepsilon_{n}))^{\frac{1}{r-1}}$$

$$\leq (M_{n}^{p-1}(n\mu_{n})^{p})^{\frac{1}{r-1}}(1+\varepsilon_{n})^{\frac{p}{r-1}}$$

$$= M_{n}^{\frac{p-1}{r-1}}(n\mu_{n})^{\frac{p}{r-1}}\left(1+\frac{p}{r-1}\varepsilon_{n}+O(\varepsilon_{n}^{2})\right).$$

A similar computation yields the following lower bound: For any i,

$$(5.8) (Sv_n)_i \ge m_n^{\frac{p-1}{r-1}} (n\mu_n)^{\frac{p}{r-1}} \left(1 - \frac{p}{r-1}\varepsilon_n + O(\varepsilon_n^2)\right).$$

<span id="page-15-0"></span>Now, take any  $i_0$  and  $j_0$  such that  $m_n = v_{n,i_0}$  and  $M_n = v_{n,j_0}$ . Since by (4.6),  $\mathbf{v}_n$  satisfies  $S\mathbf{v}_n \propto \mathbf{v}_n$ , we must have  $\frac{(S\mathbf{v}_n)_{i_0}}{m_n} = \frac{(S\mathbf{v}_n)_{j_0}}{M_n}$ , and consequently, (5.7) with  $j = j_0$  and (5.8) with  $i = i_0$  together imply that

$$(5.9) M_n^{\frac{p-1}{r-1}-1} \left(1 + \frac{p}{r-1}\varepsilon_n + O(\varepsilon_n^2)\right) \ge M_n^{\frac{p-1}{r-1}-1} \left(1 - \frac{p}{r-1}\varepsilon_n + O(\varepsilon_n^2)\right),$$

which in turn implies

$$M_n^{\frac{p-r}{r-1}} \ge m_n^{\frac{p-r}{r-1}} \left( 1 - \frac{2p}{r-1} \varepsilon_n + O(\varepsilon_n^2) \right).$$

Thus, using the fact that 1 , we have

$$(5.10) \quad \left(\frac{m_n}{M_n}\right)^{\frac{r-p}{r-1}} \ge \left(1 - \frac{2p}{r-1}\varepsilon_n + O(\varepsilon_n^2)\right) \quad \Longrightarrow \quad \frac{m_n}{M_n} \ge \left(1 - \frac{2p}{r-p}\varepsilon_n + O(\varepsilon_n^2)\right).$$

This completes the proof of (5.6) with C = 2p/(r-p), and hence Proposition 5.3(a) follows.  $\Box$ 

5.2. Maximizer for the case p=r. We now prove Proposition 5.3(b), which entails establishing the bound in (5.4) under both the almost-regularity and well-connected conditions on  $(A_n)_{n\in\mathbb{N}}$ . The basic idea again is to show that if a vector  $\mathbf{v}_n$  satisfies  $S\mathbf{v}_n \propto \mathbf{v}_n$ , then the ratio of its maximum and minimum must be converging to 1 as  $n\to\infty$ . However, when p=r, one can see that the exponents of  $M_n$  and  $m_n$  in equations (5.7) and (5.8) become zero, and consequently the method used in Section 5.1 fails. The key insight to deal with this issue is to define two sets of vertices: one consisting of all vertex indices i such that  $v_{n,i}$  is suitably large, and the other with  $v_{n,i}$ 's suitably small. Due to the well-connectedness property, we can ensure that each vertex from one of these sets must be connected to a certain number of vertices from the other set in 2-hop paths. In that case, we show that if  $M_n/m_n$  is not close to 1, then the ratio  $(S\mathbf{v})_i/v_i$  will be very different for the vertices for which  $v_i$  is minimum and maximum, respectively. This leads to a contradiction.

For any  $r \in [2, \infty)$ ,  $r^* \in (1, 2]$  and further, by [29], Lemma 8, and the symmetry of  $A_n$ ,  $A_n$ ,  $\|A_n\|_{r \to r} = \|A_n^T\|_{r^* \to r^*} = \|A_n\|_{r^* \to r^*}$ . Thus, to study the asymptotics of  $\|A_n\|_{r \to r}$ , it suffices to consider the case  $r \in (1, 2]$ . Let  $n_0 \in \mathbb{N}$  be the maximum of the  $n_0$  specified in the definitions of the almost-regularity and well-connected conditions and fix  $n \ge n_0$ . Also, as in the proof of Proposition 5.3(a), define  $m_n$  and  $M_n$  as in (5.5). Note that it suffices to show that for  $\Delta_n := (M_n - m_n)/2$ ,

$$\frac{\Delta_n}{M_n} \le \frac{5r\varepsilon_n}{C^*(r-1)},$$

which is just a restatement of (5.6). To this end, define  $V_n := \{i : v_{n,i} \ge M_n - \Delta_n\}$ , and note that  $M_n - \Delta_n = m_n + \Delta_n$ .

In the rest of the proof, we will obtain upper and lower bounds on each coordinate of  $Sv_n = \Psi_{r^*}(A_n^T \Psi_r(A_n v_n))$ . Using the definition of  $V_n$ , we have for each  $k \in [n]$ ,

$$(5.12) (A_{n} \mathbf{v}_{n})_{k} \leq M_{n} \sum_{j \in V_{n}} a_{kj}^{n} + (M_{n} - \Delta_{n}) \sum_{j \notin V_{n}} a_{kj}^{n} = M_{n} \sum_{j \in [n]} a_{kj}^{n} - \Delta_{n} \sum_{j \notin V_{n}} a_{kj}^{n},$$

$$(5.12) (A_{n} \mathbf{v}_{n})_{k} \geq (m_{n} + \Delta_{n}) \sum_{j \in V_{n}} a_{kj}^{n} + m_{n} \sum_{j \notin V_{n}} a_{kj}^{n} = m_{n} \sum_{j \in [n]} a_{kj}^{n} + \Delta_{n} \sum_{j \in V_{n}} a_{kj}^{n}.$$

Take any  $i_0$  and  $j_0$  such that  $m_n = v_{n,i_0}$  and  $M_n = v_{n,j_0}$ . We will use the following elementary fact: For all  $l \in (0, 1]$  and  $x \in [0, 1]$ ,

(5.13) 
$$(1-x)^l \le 1 - \frac{lx}{2} and (1+x)^l \ge 1 + \frac{lx}{2}.$$

<span id="page-16-0"></span>Then, by (5.12), (4.1), the fact that  $r - 1 \in (0, 1]$  and (5.13), we have

$$\frac{(A_n^T \Psi_r(A_n \mathbf{v}_n))_{j_0}}{M_n^{r-1}} \leq \frac{1}{M_n^{r-1}} \sum_{k \in [n]} a_{kj_0}^n \left[ M_n \sum_{j \in [n]} a_{kj}^n - \Delta_n \sum_{j \notin V_n} a_{kj}^n \right]^{r-1} \\
= \sum_{k \in [n]} a_{kj_0}^n \left( \sum_{j \in [n]} a_{kj}^n \right)^{r-1} \left[ 1 - \frac{\Delta_n}{M_n} \frac{\sum_{j \notin V_n} a_{kj}^n}{\sum_{j \in [n]} a_{kj}^n} \right]^{r-1} \\
\leq \sum_{k \in [n]} a_{kj_0}^n \left( \sum_{j \in [n]} a_{kj}^n \right)^{r-1} \left[ 1 - \frac{r-1}{2} \frac{\Delta_n}{M_n} \frac{\sum_{j \notin V_n} a_{kj}^n}{\sum_{j \in [n]} a_{kj}^n} \right].$$

Also, since  $A_n$  in  $(C^*, \mu_n)$  well-connected, Definition 5.2 and the symmetry of  $A_n$  imply

(5.15) 
$$\sum_{j \notin V_n} \sum_{k \in [n]} a_{kj_0}^n a_{kj}^n \ge C^* n \mu_n^2 (n - |V_n|),$$

and similarly,

(5.16) 
$$\sum_{j \in V_n} \sum_{k \in [n]} a_{ki_0}^n a_{kj}^n \ge C^* n \mu_n^2 |V_n|.$$

Using the  $(\varepsilon_n, \mu_n)_{n \in \mathbb{N}}$  almost regularity of  $A_n$  and substituting (5.15) in (5.14), we obtain

$$\frac{(A_n^T \Psi_r(A_n \mathbf{v}_n))_{j_0}}{M_n^{r-1}} \leq (n\mu_n (1+\varepsilon_n))^{r-1} \sum_{k \in [n]} a_{kj_0}^n \left[ 1 - \frac{r-1}{2} \frac{\Delta_n}{M_n} \frac{\sum_{j \notin V_n} a_{kj}^n}{\sum_{j \in [n]} a_{kj}^n} \right] 
\leq (n\mu_n (1+\varepsilon_n))^r - \frac{r-1}{2} \frac{\Delta_n}{M_n} (n\mu_n (1+\varepsilon_n))^{r-2} \sum_{j \notin V_n} \sum_{k \in [n]} a_{kj_0}^n a_{kj}^n 
\leq (n\mu_n (1+\varepsilon_n))^r - \frac{C^*(r-1)}{2} \frac{\Delta_n}{M_n} (n\mu_n (1+\varepsilon_n))^{r-2} n\mu_n^2 (n-|V_n|).$$

Similarly, using almost regularity and (5.16) we obtain

$$\frac{(A_{n}^{T}\Psi_{r}(A_{n}\mathbf{v}_{n}))_{i_{0}}}{m_{n}^{r-1}} \geq \sum_{k \in [n]} a_{ki_{0}}^{n} \left(\sum_{j \in [n]} a_{kj}^{n}\right)^{r-1} \left[1 + \frac{r-1}{2} \frac{\Delta_{n}}{m_{n}} \frac{\sum_{j \in V_{n}} a_{kj}^{n}}{\sum_{j \in [n]} a_{kj}^{n}}\right] \\
\geq \sum_{k \in [n]} a_{ki_{0}}^{n} \left(\sum_{j \in [n]} a_{kj}^{n}\right)^{r-1} \left[1 + \frac{r-1}{2} \frac{\Delta_{n}}{M_{n}} \frac{\sum_{j \in V_{n}} a_{kj}^{n}}{\sum_{j \in [n]} a_{kj}^{n}}\right] \\
\geq \left(n\mu_{n}(1-\varepsilon_{n})\right)^{r} + \frac{C^{*}(r-1)}{2} \frac{\Delta_{n}}{M_{n}} (n\mu_{n})^{r-2} \frac{(1-\varepsilon_{n})^{r-1}}{1+\varepsilon_{n}} n\mu_{n}^{2} |V_{n}|.$$

Since  $\mathbf{v}_n$  satisfies  $S\mathbf{v}_n \propto \mathbf{v}_n$ , we must have  $\frac{(A_n^T \Psi_r(A_n \mathbf{v}_n))_{j_0}}{M_n^{r-1}} = \frac{(A_n^T \Psi_r(A_n \mathbf{v}_n))_{i_0}}{m_n^{r-1}}$ . Thus, combining (5.17) and (5.18), we get for large enough n,

(5.19) 
$$\frac{C^*(r-1)}{2} \frac{\Delta_n}{M_n} (n\mu_n)^{r-2} n\mu_n^2 \left[ (1+\varepsilon_n)^{r-2} \left( n - |V_n| \right) + \frac{(1-\varepsilon_n)^{r-1}}{1+\varepsilon_n} |V_n| \right] \\ \leq (n\mu_n)^r \left[ (1+\varepsilon_n)^r - (1-\varepsilon_n)^r \right].$$

<span id="page-17-0"></span>Next, using  $\varepsilon_n \to 0$ , (5.13) and the fact that  $r \in (1, 2]$ , we can lower bound the left-hand-side of (5.19) as follows:

$$\frac{C^{*}(r-1)}{2} \frac{\Delta_{n}}{M_{n}} (n\mu_{n})^{r-2} n \mu_{n}^{2} \left[ (1+\varepsilon_{n})^{r-2} (n-|V_{n}|) + \frac{(1-\varepsilon_{n})^{r-1}}{1+\varepsilon_{n}} |V_{n}| \right] \\
\geq \frac{C^{*}(r-1)}{2} \frac{\Delta_{n}}{M_{n}} (n\mu_{n})^{r-2} n \mu_{n}^{2} \left[ n - |V_{n}| + (1-2r\varepsilon_{n}) |V_{n}| \right] \\
= \frac{C^{*}(r-1)}{2} \frac{\Delta_{n}}{M_{n}} (n\mu_{n})^{r-2} n \mu_{n}^{2} \left[ n - 2rn\varepsilon_{n} \right] \\
\geq \frac{C^{*}(r-1)}{2} \frac{\Delta_{n}}{M_{n}} (n\mu_{n})^{r} \left[ 1 - 2r\varepsilon_{n} \right].$$

Therefore, using (5.20) and Definition 5.2 in (5.19) shows that for large enough n,

$$\frac{\Delta_n}{M_n} \le \frac{2}{C^*(r-1)(1-2r\varepsilon_n)} \left(2r\varepsilon_n + o(\varepsilon_n)\right) \le \frac{5r\varepsilon_n}{C^*(r-1)}.$$

This proves (5.11), and hence, completes the proof of Proposition 5.3(b).  $\square$ 

- **6.** Approximation of the maximizer for random matrices. In this section, we show that the assumptions in Proposition 5.3 are satisfied almost surely by the sequence of random matrices of interest. This will complete the proofs of Theorems 2.6 and 2.8. Let  $\mathbb{P}_0$  be any probability measure on  $\prod_n \mathbb{R}^{n \times n}$ , such that its projection on  $\mathbb{R}^{n \times n}$  has the same law as  $A_n$ , as defined in Assumption 1.
- 6.1. Random matrices are almost regular and well-connected. In Lemmas 6.1 and 6.2, we verify the almost regularity and well-connectedness conditions for the homogeneous and inhomogeneous instances of the random matrix sequences, respectively.

LEMMA 6.1. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of random matrices satisfying Assumptions 1(i), (iii). Also, suppose that

(6.1) 
$$\varepsilon_n = 3 \left( \frac{\log n}{n\mu_n} \times \frac{\sigma_n^2}{\mu_n} \right)^{1/2}.$$

- 1. Suppose that  $\sigma_n^2 \geq \frac{9c^2 \log n}{2n}$ , where c is as in Assumption 1(iii). Then  $(A_n)_{n \in \mathbb{N}}$  is  $(\varepsilon_n, \mu_n)_{n \in \mathbb{N}}$  almost regular,  $\mathbb{P}_0$ -almost surely.
- 2. If Assumption 1(ii) is satisfied, then for any constant  $C^* \in (0, 1)$ ,  $(A_n)_{n \in \mathbb{N}}$  is also  $(C^*, \mu_n)_{n \in \mathbb{N}}$  well-connected,  $\mathbb{P}_0$ -almost surely.

PROOF. Verification of almost regularity. First, note that  $\sum_{j \in [n] \setminus \{i\}} \mathbb{E}[(a_{ij}^n - \mu_n)^2] \le n\sigma_n^2$  and Assumption 1(iii) provides the moment conditions required for Bernstein's inequality (see [8], Corollary 2.11). Therefore, using the fact that  $(a_{ij}^n)_{i < j}$  are i.i.d. as well as the union bound, and then applying [8], Corollary 2.11, for both the upper and lower tails, we conclude that for all sufficiently large n,

$$(6.2) \qquad \mathbb{P}(\exists i : |d_n(i) - n\mu_n| > n\mu_n \varepsilon_n) \le n \mathbb{P}(|d_n(1) - n\mu_n| > n\mu_n \varepsilon_n)$$

$$\le 2n \exp\left(-\frac{n^2 \mu_n^2 \varepsilon_n^2}{2(n\sigma_n^2 + cn\mu_n \varepsilon_n)}\right),$$

<span id="page-18-0"></span>where c is as given in Assumption 1(iii). Since

$$cn\mu_n\varepsilon_n = 3c\left(n^2\mu_n^2 \times \frac{\log n}{n\mu_n} \times \frac{\sigma_n^2}{\mu_n}\right)^{1/2} = 3c\sigma_n\sqrt{n\log n} \le \frac{n\sigma_n^2}{2},$$

and  $\frac{n^2 \mu_n^2 \varepsilon_n^2}{3n\sigma_n^2} = 3\log n$ , this implies

$$\mathbb{P}(\exists i : |d_n(i) - n\mu_n| > n\mu_n \varepsilon_n) \le \exp(-3\log n + \log n) = n^{-2},$$

which is summable in n. Thus the almost regularity holds  $\mathbb{P}_0$ -almost surely due to the Borel–Cantelli lemma.

Verification of well-connectedness. Note that it suffices to prove the following claim.

CLAIM 2. Define the sequence  $(\varepsilon'_n)_{n\geq 1}$  as

(6.3) 
$$\varepsilon_n' := \frac{\sigma_n^2}{\mu_n^3} \frac{(\log n)^2}{n}.$$

Then for all  $i, j \in [n], |\sum_k a_{ik} a_{kj} - n\mu_n^2| \le n\mu_n^2 \sqrt{\varepsilon_n'}, \mathbb{P}_0$ -almost surely.

PROOF. First, note that  $\varepsilon_n' \to 0$  as  $n \to \infty$  since  $\frac{\sigma_n^2}{\mu_n} = O(1)$ ,  $\sqrt{n}\mu_n = \omega(\log n)$  by Assumption 1(ii). Next, for each fixed  $i, j \in [n]$ , note that

$$\mathbb{E}\left[\sum_{k} a_{ik} a_{kj}\right] = (n-2)\mu_n^2, \qquad \mathbb{E}\left[\sum_{k} a_{ik}^2 a_{kj}^2\right] = (n-2)(\sigma_n^2 + \mu_n^2)^2.$$

By [8], Corollary 2.11, under Assumption 1, we have for all large enough n,

$$\mathbb{P}\left(\left|\sum_{k} a_{ik} a_{kj} - n\mu_n^2\right| > n\mu_n^2 \sqrt{\varepsilon_n'}\right) \le 2 \exp\left[-\frac{n^2 \mu_n^4 \varepsilon_n'}{2(n(\sigma_n^2 + \mu_n^2)^2 + c'' n\mu_n^2 \sqrt{\varepsilon_n'})}\right],$$

where c'' is a constant that depends only on the constant c in Assumption 1(iii). The proof of the claim is completed by observing that since  $\varepsilon'_n \to 0$  as  $n \to \infty$ , and  $\mu_n$  and  $\sigma_n^2/\mu_n$  are upper bounded by some fixed finite positive constant K, we have for all large enough n,

$$\frac{n^2 \mu_n^4 \varepsilon_n'}{2(n(\sigma_n^2 + \mu_n^2)^2 + c'' n \mu_n^2 \sqrt{\varepsilon_n'})} \ge \frac{n^2 \mu_n^4}{2n(K \mu_n + \mu_n^2)^2} \frac{\sigma_n^2}{\mu_n^3} \frac{(\log n)^2}{n} \ge \frac{(\log n)^2 \sigma_n^2}{8K^2 \mu_n}.$$

This completes the verification of  $\mathbb{P}_0$ -almost sure well-connectedness.  $\square$ 

The next lemma states the version of Lemma 6.1 in the inhomogeneous variance case.

LEMMA 6.2. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of random matrices that satisfies Assumption 2. Also, suppose that  $\varepsilon_n=3(\frac{\log n}{n\mu_n}\times\frac{\tilde{\sigma}_n^2}{\mu_n})^{1/2}$ . Then  $(A_n)_{n\in\mathbb{N}}$  is  $(\varepsilon_n,\mu_n)_{n\in\mathbb{N}}$  almost regular,  $\mathbb{P}_0$ -almost surely. Moreover, for any constant  $C^*\in(0,1)$ , it is also  $(C^*,\mu_n)_{n\in\mathbb{N}}$  well-connected  $\mathbb{P}_0$ -almost surely.

PROOF OF LEMMA 6.2. The proof follows verbatim the proof of Lemma 6.1 once  $\sigma_n$  is replaced by  $\bar{\sigma}_n$ .  $\square$ 

PROOFS OF THEOREMS 2.6 AND 2.8. Note that Claim 2 also implies that  $A_n^T A_n$  is irreducible. Thus, Theorems 2.6 and 2.8 are immediate from Proposition 5.3, and Lemmas 6.1 and 6.2, respectively.  $\Box$ 

<span id="page-19-0"></span>**7.** Approximating the  $r \to p$  norm. The purpose of this section is to identify a good approximation for  $||A_n||_{r\to p}$  that is sufficiently explicit. We use the power iteration method described in Section 4 starting with initial vector  $\mathbf{v}_n^{(0)} = n^{-1/r}\mathbf{1}$ . Then after one iteration, we get the vector  $\mathbf{v}_n^{(1)}$  which, by (4.12) and (4.5), is given explicitly by

(7.1) 
$$v_n^{(1)} = \frac{\Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))}{\|\Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))\|_r}.$$

Then define the quantity

(7.2) 
$$\eta_n(A_n) := \|A_n \mathbf{v}_n^{(1)}\|_p = \frac{\|A_n \Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))\|_p}{\|\Psi_{r^*}(A_n^T \Psi_p(A_n \mathbf{1}))\|_r},$$

which will serve as an approximation for  $||A_n||_{r\to p}$ . We prove the following estimate:

PROPOSITION 7.1. Let  $(A_n)_{n\in\mathbb{N}}$ ,  $(\varepsilon_n)_{n\in\mathbb{N}}$ , and  $(\mu_n)_{n\in\mathbb{N}}$  satisfy the same conditions as those imposed in Proposition 5.3. Then there exists a constant  $C \in (0, \infty)$  (possibly depending on p and r) such that for all sufficiently large n,

$$\left|\|A_n \mathbf{v}_n\|_p - \eta_n(A_n)\right| \leq C \frac{\Lambda_2^2(n)\varepsilon_n}{\mu_n^2 n^{\frac{3}{2} + \frac{1}{r}}} \|A_n\|_{2 \to p},$$

where  $\eta_n$  is defined as in (7.2) and

(7.3) 
$$\Lambda_2^2(n) := \max_{\boldsymbol{x}: \langle \mathbf{1}, \boldsymbol{x} \rangle = 0, \ \boldsymbol{x} \neq \boldsymbol{0}} \frac{\|A_n \boldsymbol{x}\|_2^2}{\|\boldsymbol{x}\|_2^2}.$$

The rest of this section is organized as follows. First, we estimate the closeness of  $\mathbf{v}_n^{(1)}$  to  $\mathbf{v}_n$  in Proposition 7.2. In particular, we show that under the assumptions of Proposition 7.1 (equivalently, Proposition 5.3),  $\mathbf{v}_n$  can be approximated well by  $\mathbf{v}_n^{(1)}$ . This is then used to approximate the operator norm and complete the proof of Proposition 7.1.

PROPOSITION 7.2. Assume that the conditions of Proposition 5.3 are satisfied. Recall the definition of the  $\mathbf{v}$ -norm from (4.15). Then there exists a constant  $C_2 < \infty$ , possibly depending on p, r, such that for all sufficiently large n,

$$\|\boldsymbol{v}_n - \boldsymbol{v}_n^{(1)}\|_{\boldsymbol{v}_n} \leq C_2 \frac{\Lambda_2^2(n)\varepsilon_n}{n^2\mu_n^2},$$

where  $\Lambda_2(n)$  is as defined in (7.3).

The next lemma provides key ingredients for the proof of Proposition 7.2.

LEMMA 7.3. Assume that  $(A_n)_{n\in\mathbb{N}}$  satisfies the conditions of Proposition 5.3 and 1 . Then the following hold:

- (a)  $\lim_{n\to\infty} \mu_n^{-1} n^{-(1+\frac{1}{p}-\frac{1}{r})} ||A_n||_{r\to p} = 1;$
- (b)  $\max_{x:\|x\|_{v_n} \le 1} \|A_n x\|_p = (1 + o(1))n^{\frac{1}{2} \frac{1}{r}} \max_{x:\|x\|_2 \le 1} \|A_n x\|_p$ ;
- (c) Let  $\lambda_2(n)$  be the second largest eigenvalue corresponding to the  $\mathbf{v}$ -Rayleigh quotient defined in (4.16). Then

$$\lambda_2(n) \le 2\mu_n^{p-2} n^{\frac{p(r-1)}{r}-1} \Lambda_2^2(n).$$

<span id="page-20-0"></span>PROOF. (a) By Proposition 5.3 and the almost regularity condition in Definition 5.1, it follows that

$$||A_n||_{r\to p} = ||A_n \mathbf{v}_n||_p = ||A_n \mathbf{1}(n^{-1/r} + o(n^{-1/r}))||_p$$

$$= ||(n\mu_n + o(n\mu_n))(n^{-1/r} + o(n^{-1/r}))\mathbf{1}||_p$$

$$= \mu_n n^{1-1/r+1/p} + o(\mu_n n^{1-1/r+1/p}),$$

from which the claim in (a) follows.

(b) By (4.15) and Proposition 5.3, we have for all sufficiently large n and  $x \in \mathbb{R}^n$ ,

(7.4) 
$$\|\mathbf{x}\|_{\mathbf{v}_n} = \left(\sum_{i=1}^n |v_{n,i}|^{r-2} |x_i|^2\right)^{\frac{1}{2}} = n^{-\frac{r-2}{2r}} \|\mathbf{x}\|_2 (1 + o(1)).$$

This implies that

(7.5) 
$$\max_{\|\mathbf{x}\|_{\mathbf{v}_{n}} \leq 1} \|A_{n}\mathbf{x}\|_{p} = \max_{\mathbf{x} \neq 0} \frac{\|A_{n}\mathbf{x}\|_{p}}{\|\mathbf{x}\|_{\mathbf{v}_{n}}} = \max_{\mathbf{x} \neq 0} \frac{\|A_{n}\mathbf{x}\|_{p}(1 + o(1))}{n^{-\frac{r-2}{2r}}\|\mathbf{x}\|_{2}} = n^{\frac{r-2}{2r}} (1 + o(1)) \max_{\|\mathbf{x}\|_{2} \leq 1} \|A_{n}\mathbf{x}\|_{p},$$

which proves (b).

(c) Recall the inner product defined in (4.14) and that  $\gamma^p$  is the largest eigenvalue of B obtained from the v-Rayleigh quotient (4.16). Thus, by using the Courant–Fischer theorem [5], Corollary III.1.2, and further justifications given below, note that

$$\begin{split} \lambda_{2}(n) &= \min_{\boldsymbol{u} \neq 0} \max_{\boldsymbol{x}: [\boldsymbol{u}, \boldsymbol{x}] = 0} \frac{[\boldsymbol{B}\boldsymbol{x}, \boldsymbol{x}]}{[\boldsymbol{x}, \boldsymbol{x}]} \leq \max_{\boldsymbol{x}: [|\boldsymbol{v}_{n}|^{2-r}, \boldsymbol{x}] = 0} \frac{[\boldsymbol{B}\boldsymbol{x}, \boldsymbol{x}]}{[\boldsymbol{x}, \boldsymbol{x}]} \\ &= \max_{\boldsymbol{x}: \langle \boldsymbol{1}, \boldsymbol{x} \rangle = 0} \frac{[\boldsymbol{B}\boldsymbol{x}, \boldsymbol{x}]}{\|\boldsymbol{x}\|_{\boldsymbol{v}_{n}}^{2}} \\ &\leq n^{1 - \frac{2}{r}} \max_{\boldsymbol{x}: \langle \boldsymbol{1}, \boldsymbol{x} \rangle = 0} \frac{\langle |\boldsymbol{A}_{n}\boldsymbol{v}_{n}|^{p-2}, |\boldsymbol{A}_{n}\boldsymbol{x}|^{2} \rangle}{\|\boldsymbol{x}\|_{2}^{2}} \\ &\leq 2\mu_{n}^{p-2} n^{1 - \frac{2}{r} + (1 - \frac{1}{r})(p-2)} \max_{\boldsymbol{x}: \langle \boldsymbol{1}, \boldsymbol{x} \rangle = 0} \frac{\|\boldsymbol{A}_{n}\boldsymbol{x}\|_{2}^{2}}{\|\boldsymbol{x}\|_{2}^{2}} \\ &\leq 2\mu_{n}^{p-2} n^{\frac{p(r-1)}{r} - 1} \Lambda_{2}^{2}(n), \end{split}$$

where the second equality follows since for any x,  $[|v_n|^{2-r}, x] = 0$  if and only if  $\langle 1, x \rangle = 0$ , and the second and third inequalities follow from (7.4) and the almost regularity.  $\square$ 

Now we have all the ingredients to complete the proof of Proposition 7.2.

PROOF OF PROPOSITION 7.2. Note that for all large enough n,  $\|\mathbf{v}_n\|_{\infty} \leq 2n^{-1/r}$  by Proposition 5.3. Thus, for any  $\mathbf{x} \in \mathbb{R}^n$  with  $\|\mathbf{x}\|_{\infty} \leq 1$ , it follows that

$$(7.6)$$

<span id="page-21-0"></span>Then the vectors  $\mathbf{v}_n^{(0)} = n^{-1/r} \mathbf{1}$  and  $\mathbf{v}_n^{(1)}$  from (7.1) in the nonlinear power iteration satisfy (as justified below)

$$\begin{split} \| \boldsymbol{v}_{n} - \boldsymbol{v}_{n}^{(1)} \|_{\boldsymbol{v}_{n}} &\leq \left( 1 + o(1) \right) \frac{(p-1)\lambda_{2}}{(r-1)\|A_{n}\|_{r \to p}^{p}} \| \boldsymbol{v}_{n} - n^{-1/r} \boldsymbol{1} \|_{\boldsymbol{v}_{n}} \\ &\leq \left( 1 + o(1) \right) \frac{2(p-1)}{r-1} \frac{\Lambda_{2}^{2}(n)}{n^{2} \mu_{n}^{2}} \| \boldsymbol{v}_{n} - n^{-1/r} \boldsymbol{1} \|_{\boldsymbol{v}_{n}} \\ &\leq \left( 1 + o(1) \right) \frac{2^{2-\frac{2}{r}}(p-1)}{r-1} \frac{\Lambda_{2}^{2}(n)}{n^{2-\frac{1}{r}} \mu_{n}^{2}} \| \boldsymbol{v}_{n} - n^{-1/r} \boldsymbol{1} \|_{\infty} \\ &\leq C \frac{\Lambda_{2}^{2}(n) \varepsilon_{n}}{n^{2} \mu_{n}^{2}}, \end{split}$$

where the first inequality is due to Proposition 4.3 and the fact that  $||A_n||_{r\to p}^p = \gamma^p$ , the second inequality is due to Lemma 7.3(a) and Lemma 7.3(c), and the third inequality is due to (7.6). Proposition 7.2 then follows from an application of Proposition 5.3.  $\square$ 

PROOF OF PROPOSITION 7.1. Once again considering the vector  $\boldsymbol{v}^{(1)}$  in (7.1) obtained after the first step of the nonlinear power iteration and  $\eta_n(A_n) = \|A_n \boldsymbol{v}_n^{(1)}\|_p$ , from (7.2), we have

$$\begin{aligned} \|\|A_{n}\boldsymbol{v}_{n}\|_{p} - \eta_{n}(A_{n})\| &\leq \|\|A_{n}\boldsymbol{v}_{n}\|_{p} - \|A_{n}\boldsymbol{v}_{n}^{(1)}\|_{p} \| \\ &\leq \|A_{n}\boldsymbol{v}_{n} - A_{n}\boldsymbol{v}_{n}^{(1)}\|_{p} \\ &\leq \|\boldsymbol{v}_{n} - \boldsymbol{v}_{n}^{(1)}\|_{\boldsymbol{v}_{n}} \max_{\|\boldsymbol{x}\|_{\boldsymbol{v}_{n}} \leq 1} \|A_{n}\boldsymbol{x}\|_{p} \\ &\leq \|\boldsymbol{v}_{n} - \boldsymbol{v}_{n}^{(1)}\|_{\boldsymbol{v}_{n}} (1 + o(1)) n^{\frac{1}{2} - \frac{1}{r}} \max_{\|\boldsymbol{x}\|_{2} \leq 1} \|A_{n}\boldsymbol{x}\|_{p} \\ &\leq \|\boldsymbol{v}_{n} - \boldsymbol{v}_{n}^{(1)}\|_{\boldsymbol{v}_{n}} (1 + o(1)) n^{\frac{1}{2} - \frac{1}{r}} \|A_{n}\|_{2 \to p}, \end{aligned}$$

where the third inequality is due to Lemma 7.3 (b). Proposition 7.1 then follows on using Proposition 7.2 to bound  $\|\mathbf{v}_n - \mathbf{v}_n^{(1)}\|_{\mathbf{v}_n}$ .  $\square$ 

- **8. Asymptotic normality.** In this section we establish asymptotic normality of  $\eta_n(A_n)$  when  $A_n$  satisfies Assumption 1. We start in Section 8.1 with some preliminary results.
- 8.1. Almost-sure error bound on the CLT scale. First, recalling the definition of  $\Lambda_2(n)$  in (7.3), we prove the following lemma.

LEMMA 8.1. *Under Assumption* 1 *the following holds*:

(8.1) 
$$\Lambda_2(n) \leq 3\sqrt{n}\sigma_n + \mu_n$$
,  $\mathbb{P}_0$  eventually almost surely.

For the proof, it will be convenient to define the following centered version of  $A_n$ :

(8.2) 
$$A_n^0 := A_n - \mu_n \mathbf{1} \mathbf{1}^T + \mu_n I_n.$$

PROOF OF LEMMA 8.1. First observe that for all vectors x with  $\langle 1, x \rangle = 0$ , using (8.2), we can write

(8.3) 
$$||A_n \mathbf{x}||_2 = ||(A_n^0 + \mu_n \mathbf{1} \mathbf{1}^T - \mu_n I_n) \mathbf{x}||_2 \le ||A_n^0 \mathbf{x}||_2 + \mu_n ||\mathbf{x}||_2.$$

<span id="page-22-0"></span>Therefore, we have

(8.4) 
$$\Lambda_2(n) = \max_{\boldsymbol{x}: \langle 1, \boldsymbol{x} \rangle = 0, \boldsymbol{x} \neq \boldsymbol{0}} \frac{\|A_n \boldsymbol{x}\|_2}{\|\boldsymbol{x}\|_2} \le \max_{\boldsymbol{x}: \, \boldsymbol{x} \neq \boldsymbol{0}} \frac{\|A_n^0 \boldsymbol{x}\|_2}{\|\boldsymbol{x}\|_2} + \mu_n.$$

Also, note that the matrix  $H_n = (h_{ij}^n)_{1 \le i,j \le n}$  defined by  $H_n := A_n^0 / \sqrt{n}\sigma_n$  satisfies the conditions of [30], Assumption 2.3, namely:

- 1. For all  $i \in [n]$ ,  $h_{ii}^n = 0$ , and for all  $i, j \in [n]$  with  $i \neq j$ ,  $\mathbb{E}[h_{ij}^n] = 0$ ,  $\mathbb{E}[(h_{ij}^n)^2] = \frac{1}{n}$ .
- 2. Setting  $q_n = \sqrt{n}\sigma_n$ , by Assumption 1(iii), there exists a fixed constant  $c_1 > 0$  such that for all  $n \ge 1$  and  $k \ge 3$ ,

$$\mathbb{E}[|h_{ij}^n|^k] \leq \frac{\mathbb{E}[|a_{ij}^n - \mu_n|^k]}{n^{\frac{k}{2}}\sigma_n^k} \leq \frac{k!}{2} \frac{c^{k-2}\sigma_n^2}{n^{\frac{k}{2}}\sigma_n^k} \leq (c_1k)^{c_1k} \frac{1}{nq_n^{k-2}}.$$

Also,  $q_n \gg n^{c_0}$ , due to Assumption 1(ii) and further,  $q_n = O(\sqrt{n})$  since  $\sigma_n^2 = O(\mu_n) = O(1)$ .

Therefore, by [30], Theorem 2.9, for all sufficiently large n,

(8.5) 
$$\max_{\mathbf{x}: \mathbf{x} \neq 0} \frac{\|A_n^0 \mathbf{x}\|_2}{\|\mathbf{x}\|_2} \le 3\sqrt{n}\sigma_n,$$

which then implies (8.1) using (8.4).  $\square$ 

Below we state a general version of Lemma 8.1 that extends the result to the nonzero diagonal entries case.

LEMMA 8.2. Under Assumption 1 and the assumptions for nonzero diagonal entries in Remark 2.3, the following holds:

(8.6) 
$$\Lambda_2(n) \leq 3\sqrt{n}\sigma_n + \mu_n + \sqrt{2n(\zeta_n^2 + \rho_n^2)}, \quad \mathbb{P}_0$$
-eventually almost surely.

The proof of Lemma 8.2 follows verbatim from the proof of Lemma 8.1, except that the upper bound in (8.4) will be replaced by

$$\Lambda_2(n) = \max_{\boldsymbol{x}: \langle \mathbf{1}, \boldsymbol{x} \rangle = 0, \boldsymbol{x} \neq \boldsymbol{0}} \frac{\|A_n \boldsymbol{x}\|_2}{\|\boldsymbol{x}\|_2} \le \max_{\boldsymbol{x}: \, \boldsymbol{x} \neq \boldsymbol{0}} \frac{\|A_n^0 \boldsymbol{x}\|_2}{\|\boldsymbol{x}\|_2} + \mu_n + \left(\sum_{i=1}^n (a_{ii}^n)^2\right)^{\frac{1}{2}}.$$

Using standard concentration bounds [8], Corollary 2.11 (as used in (6.2)), we can bound  $\sum_{i=1}^{n} (a_{ii}^n)^2 \leq 2n(\zeta_n^2 + \rho_n^2)$ ,  $\mathbb{P}_0$ -eventually almost surely. Note that this step requires the moment conditions mentioned in Remark 2.3. The rest of the proof is identical to Lemma 8.1 since since  $A_n^0$  has zero diagonal entries and hence, is omitted.

Next, we prove a bound on the error while approximating  $||A_n||_{r\to p}$  by  $\eta_n(A_n)$ .

LEMMA 8.3. Under the conditions of Theorem 2.2, the following holds  $\mathbb{P}_0$ -almost surely:

$$||A_n||_{r\to p} = ||A_n \mathbf{v}_n||_p = \eta_n(A_n) + o(\sigma_n n^{\frac{1}{p} - \frac{1}{r}}),$$

where  $v_n$  is the maximizer vector in (2.4) and  $\eta_n(\cdot)$  is defined in (7.2).

PROOF. It suffices to show that  $\mathbb{P}_0$ -eventually almost surely,

(8.7) 
$$\left| \|A_n \mathbf{v}_n\|_p - \eta_n(A_n) \right| \le C \frac{\sigma_n^3}{\mu_n^2} n^{\frac{1}{p} - \frac{1}{r}} \sqrt{\frac{\log n}{n}},$$

for some constant C > 0, not depending on n. Indeed, if (8.7) holds, then Lemma 8.3 would follow immediately on observing that  $\sigma_n^2 = O(\mu_n)$  and  $\mu_n \gg \sqrt{(\log n)/n}$  by Assumption 1(ii).

To show (8.7), note that by Lemma 6.1, under Assumption 1 with associated constants  $(\mu_n)_{n\in\mathbb{N}}$ ,  $(\sigma_n)_{n\in\mathbb{N}}$ , (i) the sequence  $(A_n)_{n\in\mathbb{N}}$  is  $\mathbb{P}_0$ -almost surely  $(\varepsilon_n, \mu_n)_{n\in\mathbb{N}}$  almost regular in the sense of Definition 5.1 with  $\varepsilon_n = \Theta(\sqrt{\frac{\log n}{n\mu_n} \cdot \frac{\sigma_n^2}{\mu_n}})$  and (ii) for some constant  $c' \in (0,1)$ ,  $(c',\mu_n)_{n\in\mathbb{N}}$  well-connected in the sense of Definition 5.2. Also, note that the well-connectedness also implies that  $A_n^T A_n$  is irreducible. In particular, the conditions of Proposition 5.3 are satisfied and we can apply Proposition 7.1 along with Lemma 8.1 to conclude that

$$|\|A_{n}\mathbf{v}_{n}\|_{p} - \eta_{n}(A_{n})| \leq C_{1} \frac{(3\sqrt{n}\sigma_{n} + \mu_{n})^{2}}{\mu_{n}^{2}n^{3/2+1/r}} \sqrt{\frac{\log n}{n\mu_{n}} \cdot \frac{\sigma_{n}^{2}}{\mu_{n}}} \times \|A_{n}\|_{2 \to p}$$

$$\leq \frac{C_{2}n\sigma_{n}^{3}(1 + \frac{\mu_{n}}{\sqrt{n}\sigma_{n}})^{2}}{\mu_{n}^{3}n^{3/2+1/r}} \sqrt{\frac{\log n}{n}} \times \|A_{n}\|_{2 \to p}.$$

To conclude the proof, we establish the following:

CLAIM 3. For 
$$p \in [1,2]$$
, (i)  $||A_n||_{2\to p} = (1 + o_{\mathbb{P}}(1))\mu_n n^{\frac{1}{2} + \frac{1}{p}}$ , (ii) For  $p > 2$ ,  $||A_n||_{2\to p} \le C\sqrt{\mu_n} n^{\frac{1}{2} + \frac{1}{p}}$  for some constant  $C > 0$ .

PROOF. For  $1 \le p \le 2$ , the claim is immediate from Lemma 7.3(a). For p > 2, let  $a_i$  denote the *i*th row of  $A_n$ . Then  $\|a_i\|_2^2 = \sum_j a_{ij}^2$  is a sum of independent random variables. Using the law of large numbers,  $\|a_i\|_2^2 \le Cn\sigma^2$  with high probability. Therefore,

(8.8) 
$$\|A_n\|_{2\to p} = \max_{\boldsymbol{x}: \|\boldsymbol{x}\|_2 \le 1} \left( \sum_{i \in [n]} |\langle \boldsymbol{a}_i, \boldsymbol{x} \rangle|^p \right)^{\frac{1}{p}}$$

$$\le \max_{\boldsymbol{x}: \|\boldsymbol{x}\|_2 \le 1} \left( \sum_{i \in [n]} \|\boldsymbol{a}_i\|_2^p \|\boldsymbol{x}\|_2^p \right)^{\frac{1}{p}} \le C(n\mu_n)^{\frac{1}{2}} n^{\frac{1}{p}},$$

and this completes the proof of the claim.  $\Box$ 

Now observe that

$$\left| \|A_n \mathbf{v}_n\|_p - \eta_n(A_n) \right| \le C_1 \frac{\Lambda_2^2(n)\varepsilon_n}{\mu_n n^{1 - \frac{1}{p} + \frac{1}{r}}} \le C_2 \frac{\sigma_n^3}{\mu_n^2} n^{\frac{1}{p} - \frac{1}{r}} \sqrt{\frac{\log n}{n}},$$

 $\mathbb{P}_0$ -eventually almost surely, for constants  $C_1, C_2 > 0$ , where the first inequality is due to Proposition 7.1 and Claim 3, and the last step is due to Lemma 8.1 and the choice of  $\varepsilon_n$ . This completes the proof of (8.7).  $\square$ 

REMARK 8.4. While we do not believe that the upper bound on  $||A_n||_{2\to p}$  given in Claim 3 for the hypercontractive case (p>2) is tight, it is worthwhile to point out that the bound  $(1+o_{\mathbb{P}}(1))\mu_n n^{\frac{1}{2}+\frac{1}{p}}$  does not work in general if p>2. This can be seen from the following observation: Recall that 1 denotes the n-dimensional vector  $(1,1,\ldots,1)$  and  $e_i$  is the n-dimensional vector whose ith component is 1 and all other components are 0. Then note that for any fixed  $i \in [n]$ ,

$$\frac{\|A_n \mathbf{1}\|_p}{\|\mathbf{1}\|_2} = (1 + o_{\mathbb{P}}(1)) \mu_n n^{\frac{1}{2} + \frac{1}{p}} \quad \text{and} \quad \frac{\|A_n e_i\|_p}{\|e_i\|_2} = (1 + o_{\mathbb{P}}(1)) (n\mu_n)^{\frac{1}{p}}.$$

<span id="page-24-0"></span>Also,

$$\mu_n n^{\frac{1}{2} + \frac{1}{p}} \ll (n\mu_n)^{\frac{1}{p}}$$
 if and only if  $\mu_n \ll n^{-\frac{p}{2(p-1)}}$ .

Therefore, the vector  $e_i$  produces a larger norm value if  $\mu_n \ll n^{-\frac{p}{2(p-1)}}$ . As a side-note, this observation hints that if  $\mu_n$  scales as  $n^{-1/t}$  for some t > 2, then for all sufficiently large p, the maximizing vector for  $||A_n||_{2\to p}$  may not be close to 1.

8.2. Proof of asymptotic normality. We proceed with the proof of asymptotic normality using the Taylor expansion. Let  $\eta_{n,t}(A_n) := \eta_n(tA_n + (1-t)\mathbb{E}[A_n])$ . Thus,  $\eta_{n,1}(A_n) = \eta_n(A_n)$  and  $\eta_{n,0}(A_n) = \eta_n(\mathbb{E}[A_n])$ . Using the Taylor expansion of  $\eta_{n,t}(A_n)$  with respect to t, we obtain

(8.9) 
$$\eta_n(A_n) = \eta_n(\mathbb{E}[A_n]) + \frac{d}{dt}\eta_{n,t}(A_n)\Big|_{t=0} + \frac{1}{2}\frac{d^2}{dt^2}\eta_{n,t}(A_n)\Big|_{t=\xi}$$

for some  $\xi \in [0, 1]$ . The next proposition establishes asymptotics of the above derivative terms. Recall from (6.3) that

(8.10) 
$$\varepsilon_n' = \frac{\sigma_n^2}{\mu_n^3} \frac{(\log n)^2}{n}.$$

PROPOSITION 8.5. As  $n \to \infty$ ,

$$\frac{d}{dt} \eta_{n,t}(A_n) \Big|_{t=0} = (1 + o_{\mathbb{P}}(1)) n^{-1 + \frac{1}{p} - \frac{1}{r}} \sum_{i,j} (a_{ij}^n - \mathbb{E}[a_{ij}^n]),$$
(8.11)
$$\frac{d^2}{dt^2} \eta_{n,t}(A_n) = (1 + O_{\mathbb{P}}(\sqrt{\varepsilon_n'}))$$

$$\times \left[ p - 1 + \frac{1}{r-1} \right] \frac{n^{-1 + \frac{1}{p} - \frac{1}{r}}}{n\mu_n} \sum_{i=1}^n \left( \sum_{j=1}^n (a_{ij}^n - \mathbb{E}[a_{ij}^n]) \right)^2,$$

where  $\varepsilon'_n$  is as defined in (8.10) and the  $O_{\mathbb{P}}(\sqrt{\varepsilon'_n})$  is uniform over  $t \in [0, 1]$ .

The proof of Proposition 8.5 is deferred to Appendix 9. We now complete the proofs of Theorem 2.2 and Theorem 2.9.

PROOF OF THEOREM 2.2. Note that Lemma 8.3 ensures that  $\eta_n(A_n)$  approximates  $||A_n||_{r\to p}$  on the fluctuation scale, that is,

$$\left| \|A_n\|_{r \to p} - \eta_n(A_n) \right| = o\left(\sigma_n n^{\frac{1}{p} - \frac{1}{r}}\right)$$
  $\mathbb{P}_0$ -almost surely.

Thus, it is enough to prove (2.1) when  $||A_n||_{r\to p}$  is replaced with  $\eta_n(A_n)$ . The first term of the Taylor expansion of  $\eta_n(A_n)$  from (8.9) is

(8.12) 
$$\eta_n(\mathbb{E}[A_n]) = \mu_n(n-1)n^{\frac{1}{p}-\frac{1}{r}}.$$

Note that  $\sum_{i < j} (a_{ij}^n - \mu_n)$  is a sum of of iid random variables with total variation  $s_n^2 := \binom{n}{2} \sigma_n^2$ . By Assumption 1(iii), it follows that

(8.13) 
$$\frac{1}{s_n^3} \sum_{i < j} \mathbb{E}[|a_{ij}^n - \mu_n|^3] \le C \frac{n^2 \sigma_n^2}{n^3 \sigma_n^3} = O\left(\frac{1}{n\sigma_n}\right),$$

<span id="page-25-0"></span>which is o(1) since  $n\sigma_n \to \infty$  by Assumption 1(ii). Thus Lyapunov's condition [7], (27.16), is satisfied and we can apply the central limit theorem for triangular arrays [7], Theorem 27.3, to conclude that

(8.14) 
$$\frac{\sum_{i < j} (a_{ij}^n - \mu_n)}{s_n} = \frac{\sqrt{2} \sum_{i < j} (a_{ij}^n - \mu_n)}{\sqrt{n(n-1)}\sigma_n} \xrightarrow{d} \text{Normal}(0, 1).$$

Thus, Proposition 8.5 shows that the scaled second term on the right hand side of (8.9) is

$$(8.15) \qquad \frac{1}{\sigma_n n^{\frac{1}{p} - \frac{1}{r}}} \times \frac{\mathrm{d}}{\mathrm{d}t} \eta_{n,t}(A_n) \bigg|_{t=0} = \left(1 + o_{\mathbb{P}}(1)\right) \frac{2\sum_{i < j} (a_{ij}^n - \mu_n)}{n\sigma_n} \xrightarrow{d} \mathrm{Normal}(0,2).$$

To evaluate the third term on the right hand side of (8.9), first note that Proposition 8.5, together with Lemma A.1(iii) implies that for all  $\xi \in [0, 1]$ 

$$\frac{\mathrm{d}^2}{\mathrm{d}t^2} \eta_{n,t}(A_n) \bigg|_{t=\xi} = \Big( 1 + O_{\mathbb{P}} \Big( \sqrt{\varepsilon_n'} \Big) \Big) \Big( 1 + O_{\mathbb{P}} (n^{-1/2}) \Big) \Big( p - 1 + \frac{1}{r-1} \Big) \frac{\sigma_n^2}{\mu_n} n^{\frac{1}{p} - \frac{1}{r}}.$$

Now.

$$\frac{\sigma_n^2}{\mu_n} n^{\frac{1}{p} - \frac{1}{r}} \sqrt{\varepsilon_n'} \ll n^{\frac{1}{p} - \frac{1}{r}} \sigma_n \quad \Longleftrightarrow \quad \frac{\sigma_n^2}{\mu_n} \left( \frac{\log^2 n}{n \mu_n^2} \right)^{1/2} \ll 1 \quad \longleftarrow \quad \mu_n \gg \frac{\log^{2/3} n}{n^{1/3}},$$

which holds due to Assumption 1 (ii). Thus, we conclude that

(8.16) 
$$\frac{\mathrm{d}^2}{\mathrm{d}t^2} \eta_{n,t}(A_n) \bigg|_{t=\xi} = \left(p-1+\frac{1}{r-1}\right) \frac{\sigma_n^2}{\mu_n} n^{\frac{1}{p}-\frac{1}{r}} + o_{\mathbb{P}}\left(n^{\frac{1}{p}-\frac{1}{r}}\sigma_n\right).$$

To complete the proof of Theorem 2.2, substitute (8.12), (8.15), and (8.16) into (8.9).

We now turn to the proof of asymptotic normality in the dense, inhomogeneous case. First we will prove a version of Lemma 8.1 in this inhomogeneous case.

LEMMA 8.6. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of random matrices satisfying the conditions of Theorem 2.9. Then the following holds:

(8.17) 
$$\Lambda_2(n) \leq 3\sqrt{c^*n}\bar{\sigma}_n + \mu_n, \quad \mathbb{P}_0 \text{ eventually almost surely,}$$

where recall that  $c^* > 0$  is a constant defined in Assumption 2.

As shown below, the proof of this lemma follows on arguments similar to the ones used in Lemma 8.1, with the key difference that the bound on the  $2 \rightarrow 2$  norm of the centered random matrix needs a more careful treatment.

PROOF OF LEMMA 8.6. We first prove the following bound on the centered matrix  $A_n^0$  from (8.2):

$$\frac{\|A_n^0 \mathbf{x}\|_2}{\|\mathbf{x}\|_2} \le 3c^* \sqrt{n} \bar{\sigma}_n, \quad \mathbb{P}_0 \text{ eventually almost surely.}$$

To this end, note that the matrix  $H_n = (h_{ij}^n)_{1 \le i, j \le n}$  defined by  $H_n = A_n^0 / \sqrt{n} \bar{\sigma}_n$  has the following properties:

- 1. By Assumption 2(i),  $h_{ii}^n = 0$  for all  $i \in [n]$  and  $\mathbb{E}[h_{ij}^n] = 0$  for all  $i, j \in [n], i \neq j$ .
- 2. By Assumption 2(ii), for all sufficiently large n,

$$\frac{c_*}{n} \leq \min_{i,j} \mathbb{E}[(h_{ij}^n)^2] \leq \max_{i,j} \mathbb{E}[(h_{ij}^n)^2] \leq \frac{c^*}{n}.$$

<span id="page-26-0"></span>3. Also, by Assumption 2(iv), for all sufficiently large n, and every  $k \ge 3$ 

$$\mathbb{E}[|h_{ij}^n|^k] \leq \frac{\mathbb{E}[|a_{ij}^n - \mu_n|^k]}{n^{\frac{k}{2}} \bar{\sigma}_n^k} \leq \frac{c_k}{n^{k/2}}.$$

This shows that  $H_n$  satisfies the conditions in [2], Theorem 2.1, Remark 2.2. Further, by Geršgorin's circle theorem [22], the largest eigenvalue of the matrix  $(\mathbb{E}[(h_{ij}^n)^2])_{i,j}$  is bounded from above by  $2c^*\bar{\sigma}_n^2$ . An application of [2], Theorem 2.1, Remark 2.2, yields (8.17).

The next lemma proves a version of Lemma 8.3 in the inhomogeneous variance case.

LEMMA 8.7. Let  $(A_n)_{n\in\mathbb{N}}$  be a sequence of random matrices satisfying the conditions of Theorem 2.9. Then the following holds  $\mathbb{P}_0$ -almost surely:

$$||A_n \mathbf{v}_n||_p = ||A_n \mathbf{v}_n^{(1)}||_p + o(\bar{\sigma}_n n^{\frac{1}{p} - \frac{1}{r}}).$$

PROOF. The proof follows the proof of Lemma 8.3 verbatim, except that Lemma 8.6 must be used in place of Lemma 8.1.  $\Box$ 

PROOF OF THEOREM 2.9. Note that Lemma 8.7 ensures that under the conditions of Theorem 2.9,  $\eta_n(A_n)$  approximates  $||A_n||_{r\to p}$  on the fluctuation scale, that is,

$$\left| \|A_n\|_{r \to p} - \eta_n(A_n) \right| = o(\bar{\sigma}_n n^{\frac{1}{p} - \frac{1}{r}})$$
  $\mathbb{P}_0$ -almost surely.

The rest of proof follows the same steps as the proof of Theorem 2.2, if one uses  $\sum_{i < j} \sigma_n^2(i, j)$  in place of  $n^2 \sigma^2/2$ , the upper bound  $(c^* \bar{\sigma}_n)^2$  for the variances of the entries, and the CLT

(8.18) 
$$\frac{\sum_{i < j} (a_{ij}^n - \mu_n)}{\sqrt{\sum_{i < j} \sigma_n^2(i, j)}} \xrightarrow{d} \text{Normal}(0, 1),$$

in place of (8.14).  $\square$ 

**9. Relation to the \ell\_r Grothendieck problem.** We end this section with the proof of Proposition 2.11.

PROOF OF PROPOSITION 2.11. Let  $x^* \in \mathbb{R}^n$  be a maximizer of  $x^T A x$  with  $||x^*|| = 1$ . Then, using the method of Lagrange multipliers, there exists  $\kappa \in \mathbb{R}$  such that if  $g : \mathbb{R}^n \mapsto \mathbb{R}$  is the function given by

$$g(\mathbf{x}) = \mathbf{x}^T A \mathbf{x} - \kappa (\|\mathbf{x}\|_r^r - 1),$$

then  $x^*$  solves the equation

(9.1) 
$$\nabla g(\mathbf{x}) = 2A\mathbf{x} - \kappa r \Psi_r(\mathbf{x}) = 0.$$

where recall  $\Psi_r(x) = |x|^{r-1} \operatorname{sgn}(x)$ . Taking the inner product of  $x^*$  with the left-hand side of (9.1) evaluated at  $x = x^*$ , and using the fact that  $\langle x^*, \Psi_r(x^*) \rangle = ||x^*||_r = 1$ , it can be seen that

(9.2) 
$$M_r(A) = \sup_{\|x\|_r \le 1} x^T A x = (x^*)^T A x^* = \frac{\kappa r}{2}.$$

Now, fix any nonnegative solution y of (9.1). It follows that

(9.3) 
$$\Psi_{r^*}(A^T \mathbf{y}) = \left(\frac{\kappa r}{2}\right)^{\frac{1}{r-1}} \mathbf{y}$$

<span id="page-27-0"></span>and also, for  $r \ge 2$  and  $p = r^* = r/(r-1)$ ,

$$\Psi_{p}(A\mathbf{y}) = \left(\frac{\kappa r}{2}\right)^{p-1} \Psi_{p}(\Psi_{r}(\mathbf{y}))$$

$$\iff A^{T} \Psi_{p}(A\mathbf{y}) = \left(\frac{\kappa r}{2}\right)^{p-1} A^{T} \Psi_{p}(\Psi_{r}(\mathbf{y}))$$

$$\iff S\mathbf{y} = \Psi_{r*}(A^{T} \Psi_{p}(A\mathbf{y})) = \left(\frac{\kappa r}{2}\right)^{\frac{p-1}{r-1}} \Psi_{r*}(A^{T} \Psi_{p}(\Psi_{r}(\mathbf{y}))).$$

Choosing  $p = r^* = r/(r-1)$ , we have  $\Psi_p(\Psi_r(y)) = y$ , and thus

$$(9.5) S\mathbf{y} = \left(\frac{\kappa r}{2}\right)^{\frac{p-1}{r-1}} \Psi_{r^*}(A^T \mathbf{y}) = \left(\frac{\kappa r}{2}\right)^{\frac{p}{r-1}} \mathbf{y} \quad \text{due to } (9.3).$$

Therefore,  $Sy \propto y$ . Also, note that since  $r \geq 2$ , we have  $p = r^* \leq r$ . Thus, from Lemma 4.1, we know that  $Sx = \gamma^{\frac{p}{r-1}}x$  has a unique solution in x that has all positive entries when A is a symmetric matrix with nonnegative entries and  $A^TA$  is irreducible (see Proposition 4.2). Since the steps between (9.1) and (9.5) consist of implications in both directions, we conclude that (9.1) also has a unique positive solution  $x^*$  and for  $p = r^*$ ,

(9.6) 
$$||A||_{r \to p}^{\frac{p}{r-1}} = \left(\frac{\kappa r}{2}\right)^{\frac{p}{r-1}} \implies ||A||_{r \to p} = \frac{\kappa r}{2}.$$

Therefore, (9.2) yields that  $M_r(A) = ||A||_{r \to r^*}$  and the proof follows.  $\square$ 

#### APPENDIX: PROOF OF PROPOSITION 8.5

Throughout this appendix, we will omit sub-/superscript n. Also, we will repeatedly use the fact that row sums of the  $\mathbb{E}[A]$  matrix is  $(n-1)\mu = n\mu(1+o(1))$ . Recall

$$A_t = tA + (1 - t)\mathbb{E}[A] \quad \text{for } t \in [0, 1],$$

$$\bar{A} = A - \mathbb{E}[A],$$

$$\bar{d} = \bar{A}\mathbf{1},$$

$$\bar{m}_k = \langle \bar{d}^{\star k}, \mathbf{1} \rangle, \quad k \ge 1.$$

Define  $E_t := \Psi_p(A_t \mathbf{1})$ . We will now calculated the expression of the derivatives, along with the value of the first derivative at t = 0.

Derivatives of  $E_t$ . Since  $E_t = \Psi_p(A_t \mathbf{1})$ ,

(A.1) 
$$E'_{t} = (p-1)\Psi_{p-1}(A_{t}\mathbf{1}) \star \bar{\boldsymbol{d}},$$
 
$$E''_{t} = (p-1)(p-2)\Psi_{p-2}(A_{t}\mathbf{1}) \star \bar{\boldsymbol{d}}^{\star 2}.$$

At t = 0, we have

(A.2) 
$$E_0 = (n\mu)^{p-1} \mathbf{1} (1 + o(1)),$$
$$E'_0 = (p-1)(n\mu)^{p-2} \bar{\boldsymbol{d}} (1 + o(1)).$$

<span id="page-28-0"></span>Derivatives of  $F_t$ .  $F_t = A_t \Psi_p(A_t \mathbf{1}) = A_t E_t$ . Then,

(A.3) 
$$F'_{t} = \bar{A}E_{t} + A_{t}E'_{t}, \\ F''_{t} = 2\bar{A}E'_{t} + A_{t}E''_{t}.$$

At t = 0, we have

(A.4) 
$$F_0 = (n\mu)^p \mathbf{1} (1 + o(1)),$$
$$F_0' = (n\mu)^{p-2} [n\mu \bar{\boldsymbol{d}} + (p-1)\bar{m}_1 \mu \mathbf{1}] (1 + o(1)).$$

Derivatives of  $S_t$ .  $S_t = \Psi_{r'}(F_t)$ . Then

(A.5) 
$$S'_{t} = (r'-1)\Psi_{r'-1}(F_{t}) \star F'_{t}, \\ S''_{t} = \Psi_{0}(F_{t}) \star [(r'-2)S'_{t} \star F'_{t} + (r'-1)S_{t} \star F''_{t}],$$

where the second step follows by noting that

(A.6) 
$$F_{t} \star S'_{t} = F_{t} \star ((r'-1)\Psi_{r'-1}(F_{t}) \star F'_{t}) = (r'-1)\Psi_{r'}(F_{t}) \star F'_{t} = (r'-1)S_{t} \star F'_{t}$$
$$\implies F'_{t} \star S'_{t} + F_{t} \star S''_{t} = (r'-1)[F'_{t} \star S'_{t} + S_{t} \star F''_{t}].$$

At t = 0, we have

(A.7) 
$$S_0 = (n\mu)^{\frac{p}{p-1}} \mathbf{1} (1 + o(1)),$$
$$S_0' = (r'-1)(n\mu)^{\frac{p}{p-1}-2} [n\mu \bar{\boldsymbol{d}} + (p-1)\bar{m}_1\mu \mathbf{1}] (1 + o(1)).$$

Derivatives of  $s_t$ .  $s_t = ||S_t||_r$ 

$$s'_{t} = s_{t}^{-(r-1)} \langle F_{t}, S'_{t} \rangle,$$

$$s''_{t} = -(r-1) \frac{(s'_{t})^{2}}{s_{t}} + s_{t}^{-(r-1)} [\langle F'_{t}, S'_{t} \rangle + \langle F_{t}, S''_{t} \rangle]$$

$$= -(r-1) \frac{(s'_{t})^{2}}{s_{t}} + (r'-1) s_{t}^{-(r-1)} [\langle F'_{t}, S'_{t} \rangle + \langle S_{t}, F''_{t} \rangle],$$

$$s_{t}^{r-1} s'_{t} = \langle \Psi_{r}(S_{t}), S'_{t} \rangle = \langle F_{t}, S'_{t} \rangle$$

$$\implies (r-1) s_{t}^{r-2} (s'_{t})^{2} + s_{t}^{r-1} s''_{t} = \langle F'_{t}, S'_{t} \rangle + \langle F_{t}, S''_{t} \rangle.$$

At t = 0, we have

(A.9) 
$$s_0 = (n\mu)^{\frac{p}{r-1}} n^{\frac{1}{r}} (1 + o(1)),$$
$$s_0' = p(r'-1)(n\mu)^{\frac{p}{r-1}-1} n^{-1+\frac{1}{r}} \bar{m}_1 (1 + o(1)).$$

Derivatives of  $G_t$ .  $G_t = A_t S_t$ .

(A.10) 
$$G'_{t} = \bar{A}S_{t} + A_{t}S'_{t}, G''_{t} = 2\bar{A}S'_{t} + A_{t}S''_{t}.$$

At t = 0, we have

(A.11) 
$$G_0 = (n\mu)^{\frac{p}{r-1}+1} \mathbf{1} (1 + o(1)),$$

$$G'_0 = (n\mu)^{\frac{p}{r-1}-1} [n\mu \bar{\boldsymbol{d}} + p(r'-1)\bar{m}_1\mu \mathbf{1}] (1 + o(1)).$$

<span id="page-29-0"></span>Derivatives of  $g_t$ .  $g_t = ||A_t S_t||_p$ .

$$g_{t}' = g_{t}^{-(p-1)} \langle \Psi_{p}(G_{t}), G_{t}' \rangle,$$
(A.12)
$$g_{t}'' = -(p-1) \frac{(g_{t}')^{2}}{g_{t}} + g_{t}^{-(p-1)} [(p-1) \langle \Psi_{p-1}(G_{t}), (G_{t}')^{\star 2} \rangle + \langle \Psi_{p}(G_{t}), G_{t}'' \rangle],$$

where we have used

$$g_t^{p-1}g_t' = \langle \Psi_p(G_t), G_t' \rangle,$$

$$(p-1)g_t^{p-2}(g_t')^2 + g_t^{p-1}g_t'' = (p-1)\langle \Psi_{p-1}(G_t), (G_t')^{*2} \rangle + \langle \Psi_p(G_t), G_t'' \rangle.$$

At t = 0, we have

(A.13) 
$$g_0 = (n\mu)^{\frac{p}{p-1}+1} n^{\frac{1}{p}} (1+o(1)),$$
$$g_0' = (n\mu)^{\frac{p}{p-1}} n^{-1+\frac{1}{p}} (p(r'-1)+1) \bar{m}_1 (1+o(1)).$$

Therefore, at t = 0,

(A.14) 
$$\frac{d}{dt} \left( \frac{g_t}{s_t} \right) \Big|_{t=0} = n^{-1 + \frac{1}{p} - \frac{1}{r}} \bar{m}_1 (1 + o(1)).$$

**A.1. Auxiliary results.** We start by listing a few auxiliary results that will be used in the calculation of the second derivatives. Throughout the rest of the Appendix,  $\varepsilon$  will be given by (6.1). Note that due to Lemma 6.1, with high probability, uniformly for all  $t \in [0, 1]$ ,  $A_t \mathbf{1} = n\mu \mathbf{1}(1 + O(\varepsilon))$ , and hence, throughout this section we will use, without reference, that with high probability, uniformly for all  $t \in [0, 1]$ 

(A.15) 
$$E_{t} = (n\mu)^{p-1} \mathbf{1} (1 + O(\varepsilon)),$$

$$F_{t} = (n\mu)^{p} \mathbf{1} (1 + O(\varepsilon)),$$

$$S_{t} = (n\mu)^{\frac{p}{r-1}} \mathbf{1} (1 + O(\varepsilon)),$$

$$G_{t} = (n\mu)^{\frac{p}{r-1}+1} \mathbf{1} (1 + O(\varepsilon)).$$

LEMMA A.1. Let  $B_{\infty}(\varepsilon) := \{x \in \mathbb{R}^n : ||x - \mathbf{1}||_{\infty} \le \varepsilon\}$ . Then the following hold:

(i)  $\|\bar{\boldsymbol{d}}\|_{\infty} \lesssim \varepsilon n \mu$ , and

$$\sup_{\boldsymbol{x}\in B_{\infty}(\varepsilon)}\|\bar{A}\boldsymbol{x}-\bar{\boldsymbol{d}}\|_{\infty}\lesssim \varepsilon n\mu.$$

(ii) 
$$|\bar{m}_1| = |\langle \mathbf{1}, \bar{d} \rangle| = O_{\mathbb{P}}(n\sigma\sqrt{\log n})$$
, and 
$$\sup_{\mathbf{x}, \mathbf{y} \in B_{\infty}(\varepsilon)} |\langle \mathbf{x}, \bar{A}\mathbf{y} \rangle - \langle \mathbf{1}, \bar{d} \rangle| = O_{\mathbb{P}}(\varepsilon n^{3/2}\sigma).$$

(iii) 
$$\bar{m}_2 = \langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle = n^2 \sigma^2 (1 + O_{\mathbb{P}}(n^{-1/2}))$$
 and with high probability 
$$\sup_{\boldsymbol{x}, \boldsymbol{y}, \boldsymbol{z} \in B_{\infty}(\varepsilon)} |\langle \boldsymbol{x}, (\bar{A}\boldsymbol{y}) \star (\bar{A}\boldsymbol{z}) \rangle - \langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle| = O_{\mathbb{P}}(\varepsilon n^2 \sigma^2).$$

(iv) 
$$\sup_{\boldsymbol{x},\,\boldsymbol{y}\in B_{\infty}(\varepsilon)} \left| \langle \boldsymbol{x},\bar{A}(\boldsymbol{y}\star\bar{\boldsymbol{d}})\rangle - \langle \boldsymbol{1},\bar{\boldsymbol{d}}^{\star2}\rangle \right| = O_{\mathbb{P}}(\varepsilon n^2\sigma^2).$$

(v) 
$$\langle \mathbf{1}, (A_t \bar{\boldsymbol{d}})^{\star 2} \rangle = O_{\mathbb{P}}(n^3 \sigma^2)$$
, and uniformly for all  $t \in [0, 1]$ ,  

$$\sup_{\boldsymbol{x}, \boldsymbol{y} \in B_{\infty}(\varepsilon)} \langle \mathbf{1}, (A_t (\boldsymbol{x} \star (\bar{A} \boldsymbol{y})))^{\star 2} \rangle = O_{\mathbb{P}}(n^3 \sigma^4 \mu^{-1} (\log n)^2).$$

PROOF. (i) The first bound follows from Lemma 6.1. Also,

$$\sup_{\boldsymbol{x}\in B_{\infty}(\varepsilon)}\|\bar{A}\boldsymbol{x}-\bar{\boldsymbol{d}}\|_{\infty}\leq \varepsilon \max_{i}\sum_{j=1}^{n}|a_{ij}-\mu|\leq \varepsilon \max_{i}(d_{i}+n\mu)\lesssim \varepsilon n\mu.$$

(ii) The bound on  $\langle \mathbf{1}, \bar{d} \rangle$  follows using  $\text{Var}(\langle \mathbf{1}, \bar{d} \rangle) = O(n^2 \sigma^2)$  and Chebyshev's inequality. Let  $\mathbf{x} = \mathbf{1} + \varepsilon \mathbf{w}_x$  and  $\mathbf{y} = \mathbf{1} + \varepsilon \mathbf{w}_y$  with  $\|\mathbf{w}_x\|_{\infty} \le 1$  and  $\|\mathbf{w}_y\|_{\infty} \le 1$ . Then

(A.16) 
$$\langle \boldsymbol{x}, \bar{A}\boldsymbol{y} \rangle = \langle \boldsymbol{1}, \bar{A}\boldsymbol{1} \rangle + \varepsilon (\langle \boldsymbol{w}_{x}, \bar{A}\boldsymbol{1} \rangle + \langle \boldsymbol{1}, \bar{A}\boldsymbol{w}_{y} \rangle) + \varepsilon^{2} \langle \boldsymbol{w}_{x}, \bar{A}\boldsymbol{w}_{y} \rangle.$$

We have,

$$\mathbb{E}\left[\sum_{i}|d_{i}-n\mu|\right] \leq n\sqrt{\mathbb{E}\left[(d_{1}-n\mu)^{2}\right]} = n\sqrt{\sum_{j}\mathbb{E}(a_{ij}-\mu)^{2}} = O\left(n^{3/2}\sigma\right).$$

Thus,

(A.17) 
$$\sup_{\boldsymbol{w}_{x}\neq\boldsymbol{0},\|\boldsymbol{w}_{x}\|_{\infty}\leq1}|\langle\boldsymbol{w}_{x},\bar{A}\boldsymbol{1}\rangle|=\sum_{i}|d_{i}-n\mu|=O_{\mathbb{P}}(n^{3/2}\sigma),$$

$$\sup_{\boldsymbol{w}_{x},\boldsymbol{w}_{y}\neq\boldsymbol{0}}\left|\frac{\langle\boldsymbol{w}_{x},\bar{A}\boldsymbol{w}_{y}\rangle}{\|\boldsymbol{w}_{x}\|_{2}\|\boldsymbol{w}_{y}\|_{2}}\right|\leq\|\bar{A}\|_{2\to2}=O_{\mathbb{P}}(\sigma\sqrt{n}),$$

where the final step in the second inequality follows using (8.5). Also,  $\langle \mathbf{1}, \bar{A} \boldsymbol{w}_y \rangle = \langle \boldsymbol{w}_y, \bar{A} \mathbf{1} \rangle$ . Thus, plugging in the value of  $\varepsilon$ , Part (ii) follows from (A.16) and (A.17).

(iii) Note that 
$$\langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle = \sum_{i,j,k} (a_{ij} - \mu)(a_{ik} - \mu)$$
, and thus,

$$\mathbb{E}[\langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle] = \sum_{i,j,k} \mathbb{E}[(a_{ij} - \mu)(a_{ik} - \mu)] = (1 + O(1/n))n^2 \sigma^2,$$

$$\mathbb{E}[\langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle^{2}] = \sum_{\substack{i,j,k \\ i',j',k'}} \mathbb{E}[(a_{ij} - \mu)(a_{ik} - \mu)(a_{i'j'} - \mu)(a_{i'k'} - \mu)] = n^{4} \sigma^{4} (1 + O(1/n)).$$

Hence, we can conclude the asymptotics of  $\langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle$  using Chebyshev's inequality. Next, there exists  $\boldsymbol{w}_x$ ,  $\boldsymbol{w}_y$ ,  $\boldsymbol{w}_z \in \mathbb{R}^n$  such that  $\|\boldsymbol{w}_x\|_{\infty} \leq 1$ ,  $\|\boldsymbol{w}_y\|_{\infty} \leq 1$ ,  $\|\boldsymbol{w}_y\|_{\infty} \leq 1$ , and

(A.18) 
$$\langle x, (\bar{A}y) \star (\bar{A}z) \rangle$$

(A.19) 
$$= \langle \mathbf{1} + \varepsilon \boldsymbol{w}_{x}, (\bar{\boldsymbol{d}} + \varepsilon \bar{A} \boldsymbol{w}_{y}) \star (\bar{\boldsymbol{d}} + \varepsilon \bar{A} \boldsymbol{w}_{z}) \rangle$$

(A.20) 
$$= \langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle + \varepsilon [\langle \boldsymbol{w}_x, \bar{\boldsymbol{d}}^{\star 2} \rangle + \langle \mathbf{1}, \bar{\boldsymbol{d}} \star (\bar{\boldsymbol{A}} \boldsymbol{w}_y) \rangle + \langle \mathbf{1}, \bar{\boldsymbol{d}} \star (\bar{\boldsymbol{A}} \boldsymbol{w}_z) \rangle]$$

(A.21) 
$$+ \varepsilon^{2} [\langle \boldsymbol{w}_{x}, \bar{\boldsymbol{d}} \star \bar{A} \boldsymbol{w}_{y} \rangle + \langle \boldsymbol{w}_{x}, \bar{\boldsymbol{d}} \star \boldsymbol{w}_{z} \rangle] + \varepsilon^{3} \langle \boldsymbol{w}_{x}, (\bar{A} \boldsymbol{w}_{y}) \star (\bar{A} \boldsymbol{w}_{z}) \rangle,$$

where we bound, with high probability,

$$\begin{split} |\langle \boldsymbol{w}_{x}, \bar{\boldsymbol{d}}^{\star 2} \rangle| &\leq \langle \boldsymbol{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle \lesssim n^{2} \sigma^{2}, \\ |\langle \boldsymbol{1}, \bar{\boldsymbol{d}} \star (\bar{A} \boldsymbol{w}_{y}) \rangle| &\leq \|\bar{\boldsymbol{d}}\|_{2} \|\bar{A}\|_{2 \to 2} \|\boldsymbol{w}_{y}\|_{2} \lesssim n^{2} \sigma^{2}, \\ |\langle \boldsymbol{w}_{x}, \bar{\boldsymbol{d}} \star \bar{A} \boldsymbol{w}_{y} \rangle| &\leq \|\bar{\boldsymbol{d}} \star \boldsymbol{w}_{x}\|_{2} \|\bar{A}\|_{2 \to 2} \|\boldsymbol{w}_{y}\|_{2} \lesssim n^{2} \sigma^{2}, \\ |\langle \boldsymbol{w}_{x}, (\bar{A} \boldsymbol{w}_{y}) \star (\bar{A} \boldsymbol{w}_{z}) \rangle| &\leq |\langle \boldsymbol{1}, |(\bar{A} \boldsymbol{w}_{y}) \star (\bar{A} \boldsymbol{w}_{z})| \rangle| \leq \|\bar{A} \boldsymbol{w}_{y}\|_{2} \|\bar{A} \boldsymbol{w}_{z}\|_{2} \leq \|\bar{A}\|_{2 \to 2}^{2} n \lesssim n^{2} \sigma^{2}. \end{split}$$
 Therefore, Part (iii) follows.

<span id="page-31-0"></span>(iv) Note that

$$\langle \boldsymbol{x}, \bar{A}(\boldsymbol{y} \star \boldsymbol{\bar{d}}) \rangle = \langle \boldsymbol{1}, \bar{A}(\boldsymbol{y} \star \boldsymbol{\bar{d}}) \rangle + \varepsilon \langle \boldsymbol{w}_{x}, \bar{A}(\boldsymbol{y} \star \boldsymbol{\bar{d}}) \rangle$$
$$= \langle \boldsymbol{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle (1 + \varepsilon) + \varepsilon \langle \boldsymbol{w}_{x}, \bar{A}(\boldsymbol{y} \star \boldsymbol{\bar{d}}) \rangle.$$

Therefore, with high probability, uniformly for all  $x, y \in B_{\infty}(\varepsilon)$ ,

$$|\langle \boldsymbol{x}, \bar{A}(\boldsymbol{y} \star \bar{\boldsymbol{d}}) \rangle - \langle \boldsymbol{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle| \le \varepsilon \langle \boldsymbol{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle + \varepsilon \|\boldsymbol{w}_{x}\|_{2} \|\bar{A}\|_{2 \to 2} \|\boldsymbol{y} \star \bar{\boldsymbol{d}}\|_{2} \lesssim \varepsilon n^{2} \sigma^{2} = O_{\mathbb{P}}(\varepsilon \bar{m}_{2}),$$

where we have again used that  $\|\bar{A}\|_{2\to 2} \lesssim \sigma \sqrt{n}$ .

(v) Note that

$$\mathbb{E}[\langle \mathbf{1}, (A_t \bar{\boldsymbol{d}})^{\star 2} \rangle] = \sum_{i} \sum_{j,k,j',k'} \mathbb{E}[a_{ij}^t (a_{jk} - \mu) a_{ij'}^t (a_{j'k'} - \mu)].$$

We can only have a nonzero contribution from an expectation term only if  $\{j, k\}$  equals one of  $\{i, j\}$ ,  $\{i, j'\}$ ,  $\{j', k'\}$ , and,  $\{j', k'\}$  equals one of  $\{i, j\}$ ,  $\{i, j'\}$ ,  $\{j, k\}$ . This implies that i = k = k' or  $\{j, k\} = \{j', k'\}$ . In both cases, there are at most  $n^3$  choices of the indices, and each of the terms can be at most  $O(\sigma^2)$  (using Assumption 1 (iii) to bound the higher moments). Therefore, applying Markov's inequality yields

$$\langle \mathbf{1}, (A_t \bar{\boldsymbol{d}})^{\star 2} \rangle = O_{\mathbb{P}}(n^3 \sigma^2).$$

Next.

$$(A.23) A_t(\mathbf{x} \star (\bar{A}\mathbf{y})) = A_t \bar{\mathbf{d}} + \varepsilon A_t(\mathbf{w}_x \star \bar{\mathbf{d}}) + \varepsilon A_t(\bar{A}\mathbf{w}_y) + \varepsilon^2 A_t(\mathbf{w}_x \star (\bar{A}\mathbf{w}_y)).$$

Thus,

$$(A.24) \qquad \langle \mathbf{1}, (\varepsilon A_t(\boldsymbol{w}_x \star \bar{\boldsymbol{d}}))^{\star 2} \rangle \leq \varepsilon^2 \|A_t |\bar{\boldsymbol{d}}|\|_2^2 \lesssim \varepsilon^2 (n\mu)^2 \|\bar{\boldsymbol{d}}\|_2^2 = O_{\mathbb{P}}(n^3 \sigma^4 \log n).$$

Also,

$$\left| \left( \varepsilon A_t (\bar{A} \boldsymbol{w}_y) \right)_i \right| = \varepsilon \left| \sum_{j,k} a_{ij}^t \bar{a}_{jk} (\boldsymbol{w}_y)_k \right| = \varepsilon \left| \sum_k (\boldsymbol{w}_y)_k \sum_j a_{ij}^t \bar{a}_{jk} \right| \lesssim \varepsilon \sum_k \left| \sum_j a_{ij}^t \bar{a}_{jk} \right|,$$

and thus,

(A.25) 
$$\langle \mathbf{1}, (\varepsilon A_t(\bar{A}\mathbf{w}_y))^{\star 2} \rangle \leq \varepsilon^2 \sum_i \left( \sum_k \left| \sum_j a_{ij}^t \bar{a}_{jk} \right| \right)^2.$$

Taking expectation,

(A.26) 
$$\sum_{i} \mathbb{E}\left(\sum_{k} \left|\sum_{j} a_{ij}^{t} \bar{a}_{jk}\right|\right)^{2} \leq \sum_{i} \left(\sum_{k} \left[\sum_{j,j'} \mathbb{E}\left(a_{ij}^{t} \bar{a}_{jk} a_{ij'}^{t} \bar{a}_{j'k}\right)\right]^{1/2}\right)^{2},$$

where we have used the following fact:

FACT. For any collection of real-valued random variables  $\{X_1, X_2, \dots, X_n\}$ ,

$$\mathbb{E}\left(\sum_{k}|X_{k}|\right)^{2} \leq \left(\sum_{k}\left(\mathbb{E}\left[X_{k}^{2}\right]\right)^{1/2}\right)^{2}.$$

<span id="page-32-0"></span>Indeed, the above fact can be seen by using the Cauchy–Schwarz inequality. Now, the expectation terms in (A.26) can be nonzero only if j = j' or k = i. Thus, for any fixed i, when k = i, we have

$$\left[\sum_{i,j'} \mathbb{E}(a_{ij}^t \bar{a}_{ji} a_{ij'}^t \bar{a}_{j'i})\right]^{1/2} = O(n(\mu \sigma^2)^{1/2}),$$

and, when  $k \neq i$ ,

$$\left[\sum_{j,j':j=j'} \mathbb{E}(a_{ij}^t \bar{a}_{jk} a_{ij'}^t \bar{a}_{j'k})\right]^{1/2} = O((n\mu\sigma^2)^{1/2}).$$

Therefore, plugging the bounds in (A.26), we get

$$\sum_{i} \mathbb{E}\left(\sum_{k} \left| \sum_{i} a_{ij}^{t} \bar{a}_{jk} \right| \right)^{2} = O(n^{4} \mu \sigma^{2}),$$

and hence, from (A.25),

$$\langle \mathbf{1}, (\varepsilon A_t(\bar{A}\boldsymbol{w}_y))^{\star 2} \rangle = O_{\mathbb{P}}(n^3 \sigma^4 \mu^{-1} \log n).$$

Next,

(A.28) 
$$\langle \mathbf{1}, \left( \varepsilon^2 A_t (\mathbf{w}_x \star (\bar{A}\mathbf{w}_y)) \right)^{\star 2} \rangle \leq \varepsilon^4 \langle \mathbf{1}, \left( A_t (|\bar{A}|\mathbf{1}) \right)^{\star 2} \rangle$$

$$= O_{\mathbb{P}} (\varepsilon^4 n^5 \mu^2 \sigma^2) = O_{\mathbb{P}} (n^3 \sigma^4 \mu^{-1} (\log n)^2),$$

where  $|\bar{A}| = (|a_{ij} - \mu|)_{i,j}$ . Therefore, using (A.22), (A.24), (A.27), (A.28), and the fact that for any  $x_i \in \mathbb{R}$ , i = 1, 2, 3, 4,  $(x_1 + x_2 + x_3 + x_4)^4 \le 16(x_1^4 + x_2^4 + x_3^4 + x_4^4)$ , we get

(A.29) 
$$\sup_{x,y\in B_{\infty}(\varepsilon)} \left| \left\langle \mathbf{1}, \left( A_t(x\star(\bar{A}y)) \right)^{\star 2} \right\rangle \right| = O_{\mathbb{P}}(n^3\sigma^4\mu^{-1}(\log n)^2),$$

and the proof follows.  $\square$ 

- **A.2. Calculation of second derivatives at arbitrary point.** Our goal is to calculate  $\frac{d^2}{dt^2}(\frac{g_t}{s_t})$  at an arbitrary point  $t \in [0, 1]$ .
- A.2.1. *Derivative of*  $s_t$  *as given in* (A.8). The goal of this section is to prove the following lemma:

LEMMA A.2. Uniformly over  $t \in [0, 1]$ ,

$$|s'_t| \lesssim (n\mu)^{\frac{p}{r-1}-1} n^{\frac{1}{r}} \sqrt{\log n} \cdot \frac{\sigma^2}{\mu},$$

$$s''_t = (r'-1)(r'-1+p(p-1))(n\mu)^{\frac{p}{r-1}-2} n^{-1+\frac{1}{r}} \tilde{m}_2 (1+O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

To prove Lemma A.2, we need to calculate mainly three terms:  $\langle F_t, S_t' \rangle$ ,  $\langle F_t', S_t' \rangle$ , and  $\langle S_t, F_t'' \rangle$ . We will calculate the values of these terms in this section at an arbitrary point  $t \in [0, 1]$ . Let us denote by x, y, z etc. generic variable vectors in  $B_{\infty}(\varepsilon) := \{x \in \mathbb{R}^n : ||x - 1||_{\infty} \le \varepsilon\}$ , which can change values from line to line.

<span id="page-33-0"></span>Calculating  $\langle F_t, S'_t \rangle$ . From (A.6), note that

$$\begin{aligned} |\langle F_t, S_t' \rangle| &= (r'-1) |\langle S_t, F_t' \rangle| = (r'-1) |\langle S_t, \bar{A}E_t + A_t E_t' \rangle| \\ &\lesssim (n\mu)^{\frac{p}{r-1} + p - 2} [n\mu \langle \mathbf{x}, \bar{A}\mathbf{y} \rangle + \langle \mathbf{x}, \mathbf{z} \star \bar{\mathbf{d}} \rangle] \lesssim (n\mu)^{\frac{p}{r-1} + p - 1} \varepsilon n^{3/2} \sigma, \end{aligned}$$

where in the last step, we have used Lemma (A.1) and the fact that  $\langle x, z \star \bar{d} \rangle = \langle x \star z, \bar{A} \mathbf{1} \rangle$ . Calculating  $\langle F'_t, S'_t \rangle$ . Due to (A.5),

(A.30) 
$$\langle F'_t, S'_t \rangle = (r'-1) \langle F'_t, \Psi_{r'-1}(F_t) \star F'_t \rangle = (r'-1) \langle \Psi_{r'-1}(F_t), (\bar{A}E_t)^{*2} + (A_t E'_t)^{*2} + 2(\bar{A}E_t) \star (A_t E'_t) \rangle.$$

Using Lemma A.1(iii),

(A.31) 
$$\langle \Psi_{r'-1}(F_t), (\bar{A}E_t)^{\star 2} \rangle = (n\mu)^{\frac{p}{r-1}+p-2} \left[ \langle \mathbf{1}, \bar{\boldsymbol{d}}^{\star 2} \rangle + O_{\mathbb{P}}(\varepsilon n^2 \sigma^2) \right]$$
$$= (1 + O_{\mathbb{P}}(\varepsilon))(n\mu)^{\frac{p}{r-1}+p-2} \bar{m}_2.$$

Next, due to Lemma A.1(iii) and (v), uniformly for any  $x \in B_{\infty}(\varepsilon)$ ,

(A.32) 
$$\langle \mathbf{1}, (A_t(\mathbf{x} \star \bar{\mathbf{d}}))^{\star 2} \rangle = O_{\mathbb{P}} \left( n(\log n)^2 \frac{\sigma^2}{\mu} \bar{m}_2 \right).$$

Therefore,

(A.33) 
$$|\langle \Psi_{r'-1}(F_t), (A_t E_t')^{\star 2} \rangle| = O_{\mathbb{P}}((n\mu)^{\frac{p}{r-1} + p - 2} \bar{m}_2 \varepsilon'),$$

where  $\varepsilon' = \frac{\sigma^2}{\mu^3} \frac{(\log n)^2}{n}$  is as defined in (8.10). Finally,

$$|\langle \Psi_{r'-1}(F_t), (\bar{A}E_t) \star (A_t E_t') \rangle| \leq \max_{i} (\Psi_{r'-1}(F_t))_{i} \times \langle \mathbf{1}, |(\bar{A}E_t) \star (A_t E_t')| \rangle$$

$$\lesssim (n\mu)^{\frac{p}{r-1}-p} \langle \mathbf{1}, |(\bar{A}E_t) \star (A_t E_t')| \rangle$$

$$\leq (n\mu)^{\frac{p}{r-1}-p} \langle \mathbf{1}, (\bar{A}E_t)^{\star 2} \rangle^{1/2} \langle \mathbf{1}, (A_t E_t')^{\star 2} \rangle^{1/2}$$

$$= O_{\mathbb{P}}((n\mu)^{\frac{p}{r-1}+p-2} \bar{m}_2 \sqrt{\varepsilon'}).$$

Therefore, plugging the estimates in (A.30),

(A.35) 
$$\langle F_t', S_t' \rangle = (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'}))(r'-1)(n\mu)^{\frac{p}{r-1}+p-2}\bar{m}_2,$$

where we have used the fact that  $\sqrt{\varepsilon'} \gg \varepsilon$ .

Calculating  $\langle S_t, F_t'' \rangle$ . Note, using (A.3), we get that

$$\langle S_t, F_t'' \rangle = \langle S_t, 2\bar{A}E_t' + A_t E_t'' \rangle.$$

Now, due to (A.1), and Lemma A.1(iii) and (iv),

$$\langle S_t, \bar{A}E_t' \rangle = (p-1)\langle S_t, \bar{A}(\Psi_{p-1}(A_t\mathbf{1}) \star \bar{\mathbf{d}}) \rangle = (p-1)(n\mu)^{\frac{p}{p-1}+p-2}\bar{m}_2(1+O_{\mathbb{P}}(\varepsilon)),$$

and

$$\langle S_t, A_t E_t'' \rangle = (p-1)(p-2)(n\mu)^{\frac{p}{r-1}+p-2} \bar{m}_2 (1 + O_{\mathbb{P}}(\varepsilon)).$$

PROOF OF LEMMA A.2. Using (A.8) and the estimates derived in this section, we get that, uniformly over  $t \in [0, 1]$ ,

$$|s'_t| \lesssim (n\mu)^{\frac{p}{r-1}-1} n^{\frac{1}{r}} \sqrt{\log n} \cdot \frac{\sigma^2}{\mu},$$

$$s''_t = (r'-1)(r'-1+p(p-1))(n\mu)^{\frac{p}{r-1}-2} n^{-1+\frac{1}{r}} \bar{m}_2 (1+O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

<span id="page-34-0"></span>A.2.2. Derivative of  $g_t$  as given in (A.12). The goal of this section is to prove the following lemma:

LEMMA A.3. *Uniformly over*  $t \in [0, 1]$ ,

$$\begin{aligned} |g_t'| &\lesssim (n\mu)^{\frac{p}{r-1}} n^{\frac{1}{p}} \sqrt{\log n} \cdot \frac{\sigma^2}{\mu}, \\ g_t'' &= \left[ p - 1 + (r' - 1) \left( p(p-1) + \frac{1}{r-1} + 1 \right) \right] (n\mu)^{\frac{p}{r-1} - 1} n^{-1 + \frac{1}{p}} \bar{m}_2 (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})). \end{aligned}$$

Similar to Section A.2.1, the proof of Lemma A.3 requires three terms:  $\langle \Psi_p(G_t), G_t' \rangle$ ,  $\langle \Psi_{p-1}(G_t), (G_t')^{*2} \rangle$ ,  $\langle \Psi_p(G_t), G_t'' \rangle$ . We will calculate the values of these terms in this section at an arbitrary point  $t \in [0, 1]$ . Recall (A.15).

Calculating  $\langle \Psi_p(G_t), G'_t \rangle$ .

$$\langle \Psi_{p}(G_{t}), G'_{t} \rangle = \langle \Psi_{p}(G_{t}), \bar{A}S_{t} + A_{t}S'_{t} \rangle$$

$$= \langle \Psi_{p}(G_{t}), \bar{A}S_{t} \rangle + (r'-1)\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{r'-1}(F_{t}) \star F'_{t}) \rangle$$

$$= \langle \Psi_{p}(G_{t}), \bar{A}S_{t} \rangle + (r'-1)\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t} + A_{t}E'_{t})) \rangle.$$

Therefore, from Lemma A.1(ii),

$$\langle \Psi_p(G_t), \bar{A}S_t \rangle = (n\mu)^{\frac{p(p-1)}{r-1} + p - 1 + \frac{p}{r-1}} \langle \mathbf{x}, \bar{A}\mathbf{y} \rangle \lesssim (n\mu)^{\frac{p^2}{r-1} + p - 1} \varepsilon n^{3/2} \sigma.$$

Also,

$$\begin{aligned} |\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t} + A_{t}E'_{t}))\rangle| \\ &= |\langle \Psi_{r'-1}(F_{t}) \star (A_{t}\Psi_{p}(G_{t})), \bar{A}E_{t}\rangle| + |\langle \Psi_{r'-1}(F_{t}) \star (A_{t}\Psi_{p}(G_{t})), A_{t}E'_{t}\rangle| \\ &\lesssim (n\mu)^{\frac{p(p-1)}{r-1} + p - 1 + \frac{p}{r-1}} |\langle \mathbf{x}, \bar{A}\mathbf{y}\rangle| \\ &+ |\langle (A_{t}(\Psi_{r'-1}(F_{t}) \star (A_{t}\Psi_{p}(G_{t})))) \star \Psi_{p-1}(A_{t}\mathbf{1}), \bar{A}\mathbf{1}\rangle| \\ &\lesssim (n\mu)^{\frac{p^{2}}{r-1} + p - 1} \varepsilon n^{3/2} \sigma, \end{aligned}$$

where the last inequality uses Lemma A.1(ii) again.

Calculating  $\langle \Psi_{p-1}(G_t), (G_t')^{\star 2} \rangle$ . First, due to (A.10),

(A.38) 
$$\langle \Psi_{p-1}(G_t), (G'_t)^{\star 2} \rangle = \langle \Psi_{p-1}(G_t), (\bar{A}S_t)^{\star 2} + (A_t S'_t)^{\star 2} + 2(\bar{A}S_t) \star (A_t S'_t) \rangle.$$

Similar to (A.31), Lemma A.1(iii) yields

(A.39) 
$$\langle \Psi_{p-1}(G_t), (\bar{A}S_t)^{\star 2} \rangle = (n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 (1 + O_{\mathbb{P}}(\varepsilon)).$$

Now,

$$\langle \Psi_{p-1}(G_{t}), (A_{t}S'_{t})^{\star 2} \rangle$$

$$\lesssim \langle \Psi_{p-1}(G_{t}), (A_{t}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t} + A_{t}E'_{t})))^{\star 2} \rangle$$

$$\lesssim 2\langle \Psi_{p-1}(G_{t}), (A_{t}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t})))^{\star 2} + (A_{t}(\Psi_{r'-1}(F_{t}) \star (A_{t}E'_{t})))^{\star 2} \rangle$$

$$\leq (n\mu)^{\frac{p(p-2)}{r-1} + p-2} \langle \mathbf{1}, (A_{t}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t})))^{\star 2} + (A_{t}(\Psi_{r'-1}(F_{t}) \star (A_{t}E'_{t})))^{\star 2} \rangle.$$

where the last inequality uses (A.15) and the fact that each term of  $(A_t(\Psi_{r'-1}(F_t) \star (\bar{A}E_t)))^{*2}$  and  $(A_t(\Psi_{r'-1}(F_t) \star (A_tE_t')))^{*2}$  is nonnegative. We will calculate the two terms in (A.40) separately. For the first term, we can write

(A.41) 
$$\begin{aligned} |\langle \mathbf{1}, \left( A_t (\Psi_{r'-1}(F_t) \star (\bar{A}E_t)) \right)^{\star 2} \rangle| &= (n\mu)^{\frac{2p}{r-1}-2} |\langle \mathbf{1}, \left( A_t (\mathbf{x} \star (\bar{A}\mathbf{y})) \right)^{\star 2} \rangle| \\ &= O_{\mathbb{P}}((n\mu)^{\frac{2p}{r-1}} \varepsilon' \bar{m}_2), \end{aligned}$$

where  $\varepsilon'$  is defined in (8.10) and the last equality uses Lemma A.1(v). Next, using (A.1) for the second term in (A.40),

$$\begin{aligned} |\langle \mathbf{1}, \left( A_t \left( \Psi_{r'-1}(F_t) \star \left( A_t E_t' \right) \right) \right)^{\star 2} \rangle| &\lesssim (n\mu)^{\frac{2p}{r-1}-4} \sup_{\mathbf{x}, \mathbf{y} \in B_{\infty}(\varepsilon)} |\langle \mathbf{1}, \left( A_t \left( \mathbf{x} \star \left( A_t \left( \mathbf{y} \star \bar{\mathbf{d}} \right) \right) \right) \right)^{\star 2} \rangle| \\ &\lesssim (n\mu)^{\frac{2p}{r-1}-4} \left[ |\langle \mathbf{1}, \left( A_t^2 \bar{\mathbf{d}} \right)^{\star 2} \rangle| + \varepsilon^2 \langle \mathbf{1}, \left( A_t^2 |\bar{\mathbf{d}} | \right)^{\star 2} \rangle \right]. \end{aligned}$$

Now,

$$\mathbb{E}|\langle \mathbf{1}, (A_t^2 \bar{\mathbf{d}})^{\star 2} \rangle| = \sum_{i} \mathbb{E} \left( \sum_{j,k,l} a_{ij} a_{jk} (a_{kl} - \mu) \right)^2$$

$$= \sum_{i} \sum_{\substack{j,k,l \\ j',k',l'}} \mathbb{E} [a_{ij} a_{jk} (a_{kl} - \mu) a_{ij'} a_{j'k'} (a_{k'l'} - \mu)]$$

$$= O(n^5 \max(\mu^4 \sigma^2, \mu^2 \sigma^4)),$$

where, in the above sum, the expectation will be nonzero only if  $\{k, l\}$  is the same as one of  $\{i, j\}$ ,  $\{j, k\}$ ,  $\{i, j'\}$ ,  $\{j'k'\}$ ,  $\{k', l'\}$ , and,  $\{k', l'\}$  is the same as one of  $\{i, j\}$ ,  $\{j, k\}$ ,  $\{i, j'\}$ ,  $\{k, l\}$ ,  $\{j', k'\}$ . There are at most  $n^5$  such choices of indices and the main contribution comes from the case when there are 5 distinct indices. In that case, each term is at most  $O(\max(\mu^4\sigma^2, \mu^2\sigma^4))$ . Also, for the second term in (A.42), using Lemma A.1(i), we get

$$\mathbb{E}\left[\varepsilon^2 \langle \mathbf{1}, (A_t^2 | \bar{\boldsymbol{d}} |)^{\star 2} \rangle\right] \lesssim n^5 \mu^2 \sigma^4 \log^2 n.$$

Therefore, from (A.42), we get

$$|\langle \mathbf{1}, (A_t(\Psi_{r'-1}(F_t) \star (A_t E_t')))^{\star 2} \rangle| = O_{\mathbb{P}} \left( (n\mu)^{\frac{2p}{r-1}} \max \left\{ n\sigma^2, n\frac{\sigma^4}{\mu^2} \log^2 n \right\} \right)$$

$$= O_{\mathbb{P}} \left( (n\mu)^{\frac{2p}{r-1}} \bar{m}_2 \max \left\{ \frac{1}{n}, \frac{\sigma^2}{n\mu^2} \log^2 n \right\} \right)$$

$$= O_{\mathbb{P}} \left( (n\mu)^{\frac{2p}{r-1}} \bar{m}_2 \varepsilon' \right),$$

where  $\varepsilon'$  is given by (8.10). Thus, plugging in the estimates from (A.41) and (A.43) into (A.40), we get

(A.44) 
$$|\langle \Psi_{p-1}(G_t), (A_t S_t')^{*2} \rangle| = O_{\mathbb{P}}((n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 \varepsilon').$$

Finally, similar to (A.34), using (A.39) and (A.44), we can write that

$$\langle \Psi_{p-1}(G_t), (\bar{A}S_t) \star (A_t S_t') \rangle = O_{\mathbb{P}}((n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 \sqrt{\varepsilon'}).$$

Therefore, using (A.39), (A.44), and (A.45), we get that uniformly over  $t \in [0, 1]$ ,

(A.46) 
$$\langle \Psi_{p-1}(G_t), (G'_t)^{\star 2} \rangle = (n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

<span id="page-36-0"></span>Calculating  $\langle \Psi_p(G_t), G_t'' \rangle$ . Using (A.10),

$$\langle \Psi_{p}(G_{t}), G_{t}^{"} \rangle = \langle \Psi_{p}(G_{t}), 2\bar{A}S_{t}^{\prime} + A_{t}S_{t}^{"} \rangle$$

$$= 2(r^{\prime} - 1)\langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r^{\prime} - 1}(F_{t}) \star F_{t}^{\prime}) \rangle$$

$$+ \langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star [(r^{\prime} - 2)S_{t}^{\prime} \star F_{t}^{\prime} + (r^{\prime} - 1)S_{t} \star F_{t}^{\prime \prime}] \rangle.$$

As before, we will calculate the above terms separately.

$$\langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star F'_{t}) \rangle$$

$$= \langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t} + A_{t}E'_{t})) \rangle$$

$$= \langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t} + (p-1)A_{t}(\Psi_{p-1}(A_{t}\mathbf{1}) \star \bar{\mathbf{d}}))) \rangle$$

$$= \langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star (\bar{A}E_{t})) \rangle$$

$$+ \langle (p-1) \rangle \langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star (A_{t}(\Psi_{p-1}(A_{t}\mathbf{1}) \star \bar{\mathbf{d}}))) \rangle.$$

For the first term in (A.48), due to Lemma A.1(iii)

(A.49) 
$$\langle \Psi_p(G_t), \bar{A}(\Psi_{r'-1}(F_t) \star (\bar{A}E_t)) \rangle = (n\mu)^{\frac{p^2}{r-1} + p - 2} \langle \mathbf{x}, \bar{A}(\mathbf{y} \star (\bar{A}\mathbf{z})) \rangle$$

$$= (n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 (1 + O_{\mathbb{P}}(\varepsilon)).$$

For the second term in (A.48),

$$|\langle \Psi_{p}(G_{t}), \bar{A}(\Psi_{r'-1}(F_{t}) \star (A_{t}(\Psi_{p-1}(A_{t}\mathbf{1}) \star \bar{d})))\rangle|$$

$$= (n\mu)^{\frac{p^{2}}{r-1}+p-3} |\langle \mathbf{y} \star (\bar{A}\mathbf{x}), A_{t}(\mathbf{z} \star \bar{d})\rangle|$$

$$\leq (n\mu)^{\frac{p^{2}}{r-1}+p-3} [\langle \mathbf{1}, (\mathbf{y} \star (\bar{A}\mathbf{x}))^{\star 2}\rangle]^{1/2} [\langle \mathbf{1}, (A_{t}(\mathbf{z} \star \bar{d}))^{\star 2}\rangle]^{1/2}$$

$$\leq (n\mu)^{\frac{p^{2}}{r-1}+p-3} [\langle \mathbf{y}^{\star 2}, (\bar{A}\mathbf{x})^{\star 2}\rangle]^{1/2} \times [\langle \mathbf{1}, (A_{t}(\mathbf{z} \star \bar{d}))^{\star 2}\rangle]^{1/2}$$

$$\leq O_{\mathbb{P}}((n\mu)^{\frac{p^{2}}{r-1}+p-2} \bar{m}_{2} \sqrt{\varepsilon'}),$$

where in the last inequality, we have used Lemma A.1(iii) and (A.29). Therefore, (A.48) yields

(A.51) 
$$\langle \Psi_p(G_t), \bar{A}(\Psi_{r'-1}(F_t) \star F_t') \rangle = (n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

Next, from (A.5), note that

(A.52) 
$$S'_{t} \star F'_{t} = (r'-1)\Psi_{r'-1}(F_{t}) \star (F'_{t})^{\star 2},$$

and thus, each term in  $S'_t \star F'_t$  is nonnegative,  $\mathbb{P}_0$ -almost surely. Therefore, we can write using (A.35),

$$\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S'_{t} \star F'_{t}) \rangle = \langle (A_{t}\Psi_{p}(G_{t})) \star \Psi_{0}(F_{t}), S'_{t} \star F'_{t} \rangle$$

$$= (n\mu)^{\frac{p(p-1)}{r-1}} \langle \mathbf{1}, S'_{t} \star F'_{t} \rangle (1 + O_{\mathbb{P}}(\varepsilon))$$

$$= (r'-1)(n\mu)^{\frac{p^{2}}{r-1} + p - 2} \bar{m}_{2} (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

Also, from (A.3) we get

$$\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S_{t} \star F_{t}^{"}) \rangle$$

$$= 2\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S_{t} \star [\bar{A}E_{t}^{'}]) \rangle + \langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S_{t} \star [A_{t}E_{t}^{"}]) \rangle$$

$$= 2\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S_{t} \star [\bar{A}E_{t}^{'}]) \rangle$$

$$+ (p-1)(p-2)\langle \Psi_{p}(G_{t}), A_{t}(\Psi_{0}(F_{t}) \star S_{t} \star [A_{t}(\Psi_{p-2}(A_{t}\mathbf{1}) \star \bar{d}^{\star 2})]) \rangle$$

$$= p(p-1)(n\mu)^{\frac{p^{2}}{r-1}+p-2}\bar{m}_{2}(1+O_{\mathbb{P}}(\varepsilon)),$$

where in the last step, we have used Lemma A.1(iv) and that

$$\begin{split} &\langle \Psi_p(G_t), A_t \big( \Psi_0(F_t) \star S_t \star \left[ \bar{A} E_t' \right] \big) \rangle \\ &= (p-1) \langle \big( A_t \Psi_p(G_t) \big) \star \Psi_0(F_t) \star S_t, \bar{A} \big( \Psi_{p-1}(A_t \mathbf{1}) \star \bar{\mathbf{d}} \big) \rangle \\ &= (p-1) (n\mu)^{\frac{p^2}{r-1} + p - 2} \bar{m}_2 \big( 1 + O_{\mathbb{P}}(\varepsilon) \big). \end{split}$$

Plugging in the values from (A.51), (A.53), and (A.54) into (A.47),

$$\langle \Psi_{p}(G_{t}), G_{t}'' \rangle = (n\mu)^{\frac{p^{2}}{r-1} + p - 2} \bar{m}_{2} [2(r'-1) + (r'-2)(r'-1) + (r'-1)p(p-1)]$$

$$\times (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'}))$$

$$= (r'-1) \Big( p(p-1) + \frac{1}{r-1} + 1 \Big) (n\mu)^{\frac{p^{2}}{r-1} + p - 2} \bar{m}_{2} (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

PROOF OF LEMMA A.3. Using (A.12) and the estimates derived in this section, we get that uniformly over all  $t \in [0, 1]$ ,

$$|g'_{t}| \lesssim (n\mu)^{\frac{p}{p-1}} n^{\frac{1}{p}} \sqrt{\log n} \cdot \frac{\sigma^{2}}{\mu},$$

$$(A.56) \qquad g''_{t} = \left[ p - 1 + (r' - 1) \left( p(p-1) + \frac{1}{r-1} + 1 \right) \right]$$

$$\times (n\mu)^{\frac{p}{p-1} - 1} n^{-1 + \frac{1}{p}} \bar{m}_{2} (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})).$$

PROOF OF PROPOSITION 8.5. From (A.14), we can write

$$\frac{\mathrm{d}}{\mathrm{d}t} \eta_{n,t}(A_n) \bigg|_{t=0} = \frac{d}{dt} \left( \frac{g_t}{s_t} \right) \bigg|_{t=0} = n^{-1 + \frac{1}{p} - \frac{1}{r}} \bar{m}_1 (1 + o(1)).$$

Also, using (A.15) and Lemmas A.2 and A.3, we get

$$\frac{\mathrm{d}^2}{\mathrm{d}t^2}\eta_{n,t}(A_n) = \frac{d^2}{dt^2} \left(\frac{g_t}{s_t}\right) = \left[p - 1 + \frac{1}{r-1}\right] n^{-1 + \frac{1}{p} - \frac{1}{r}} \frac{\bar{m}_2}{n\mu} (1 + O_{\mathbb{P}}(\sqrt{\varepsilon'})). \quad \Box$$

**Funding.** The first author was partially supported by Vannevar Bush Faculty Fellowship ONR-N00014-20-1-2826, Simons—Berkeley Research Fellowship and Vannevar Bush Faculty Fellowship ONR-N0014-21-1-2887.

The second author was partially supported by NSF Grants CIF-2113027 and CPS-2240982.

The third author was partially supported by NSF Grants DMS-1954351 and DMS-2246838.

# REFERENCES

- <span id="page-38-0"></span>[1] ABBE, E., FAN, J., WANG, K. and ZHONG, Y. (2020). Entrywise eigenvector analysis of random matrices with low expected rank. *Ann*. *Statist*. **48** 1452–1474. [MR4124330](https://mathscinet.ams.org/mathscinet-getitem?mr=4124330)<https://doi.org/10.1214/19-AOS1854>
- [2] ALT, J., ERDOS˝ , L. and KRÜGER, T. (2021). Spectral radius of random matrices with independent entries. *Probab*. *Math*. *Phys*. **2** 221–280. [MR4408013](https://mathscinet.ams.org/mathscinet-getitem?mr=4408013)<https://doi.org/10.2140/pmp.2021.2.221>
- [3] BENNETT, G., GOODMAN, V. and NEWMAN, C. M. (1975). Norms of random matrices. *Pacific J*. *Math*. **59** 359–365. [MR0393085](https://mathscinet.ams.org/mathscinet-getitem?mr=0393085)
- [4] BHASKARA, A. and VIJAYARAGHAVAN, A. (2011). Approximating matrix *p*-norms. In *Proc*. *SODA'*11 497–511. SIAM, Philadelphia. <https://doi.org/110.1137/1.9781611973082.40>.
- [5] BHATIA, R. (1997). *Matrix Analysis*. *Graduate Texts in Mathematics* **169**. Springer, New York. [MR1477662](https://mathscinet.ams.org/mathscinet-getitem?mr=1477662) <https://doi.org/10.1007/978-1-4612-0653-8>
- [6] BHATTIPROLU, V., GHOSH, M., GURUSWAMI, V., LEE, E. and TULSIANI, M. (2019). Approximability of *p* → *q* matrix norms: Generalized Krivine rounding and hypercontractive hardness. In *Proceedings of the Thirtieth Annual ACM–SIAM Symposium on Discrete Algorithms* 1358–1368. SIAM, Philadelphia, PA. [MR3909552](https://mathscinet.ams.org/mathscinet-getitem?mr=3909552)<https://doi.org/10.1137/1.9781611975482.83>
- [7] BILLINGSLEY, P. (1995). *Probability and Measure*, 3rd ed. *Wiley Series in Probability and Mathematical Statistics*. Wiley, New York. [MR1324786](https://mathscinet.ams.org/mathscinet-getitem?mr=1324786)
- [8] BOUCHERON, S., LUGOSI, G. and MASSART, P. (2013). *Concentration Inequalities*: *A Nonasymptotic Theory of Independence*. Oxford Univ. Press, Oxford. [MR3185193](https://mathscinet.ams.org/mathscinet-getitem?mr=3185193) [https://doi.org/10.1093/acprof:oso/](https://doi.org/10.1093/acprof:oso/9780199535255.001.0001) [9780199535255.001.0001](https://doi.org/10.1093/acprof:oso/9780199535255.001.0001)
- [9] BOYD, D. W. (1974). The power method for *<sup>p</sup>* norms. *Linear Algebra Appl*. **9** 95–101. [MR0362876](https://mathscinet.ams.org/mathscinet-getitem?mr=0362876) [https://doi.org/10.1016/0024-3795\(74\)90029-9](https://doi.org/10.1016/0024-3795(74)90029-9)
- [10] BÜHLMANN, P. and VAN DE GEER, S. (2011). *Statistics for High-Dimensional Data*: *Methods*, *Theory and Applications*. *Springer Series in Statistics*. Springer, Heidelberg. [MR2807761](https://mathscinet.ams.org/mathscinet-getitem?mr=2807761) [https://doi.org/10.1007/](https://doi.org/10.1007/978-3-642-20192-9) [978-3-642-20192-9](https://doi.org/10.1007/978-3-642-20192-9)
- [11] CAPE, J., TANG, M. and PRIEBE, C. E. (2019). The two-to-infinity norm and singular subspace geometry with applications to high-dimensional statistics. *Ann*. *Statist*. **47** 2405–2439. [MR3988761](https://mathscinet.ams.org/mathscinet-getitem?mr=3988761) <https://doi.org/10.1214/18-AOS1752>
- [12] CHAKRABARTY, A., CHAKRABORTY, S. and HAZRA, R. S. (2020). Eigenvalues outside the bulk of inhomogeneous Erdos-Rényi random graphs. ˝ *J*. *Stat*. *Phys*. **181** 1746–1780. [MR4179787](https://mathscinet.ams.org/mathscinet-getitem?mr=4179787) [https://doi.org/10.](https://doi.org/10.1007/s10955-020-02644-7) [1007/s10955-020-02644-7](https://doi.org/10.1007/s10955-020-02644-7)
- [13] CHARIKAR, M. and WIRTH, A. (2004). Maximizing quadratic programs: Extending Grothendieck's inequality. In *Proc*. *FOCS'*04 54–60. <https://doi.org/10.1109/FOCS.2004.39>
- [14] DAVIS, C. and KAHAN, W. M. (1970). The rotation of eigenvectors by a perturbation. III. *SIAM J*. *Numer*. *Anal*. **7** 1–46. [MR0264450](https://mathscinet.ams.org/mathscinet-getitem?mr=0264450)<https://doi.org/10.1137/0707001>
- [15] DONATH, W. E. and HOFFMAN, A. J. (1973). Lower bounds for the partitioning of graphs. *IBM J*. *Res*. *Develop*. **17** 420–425. [MR0329965](https://mathscinet.ams.org/mathscinet-getitem?mr=0329965)<https://doi.org/10.1147/rd.175.0420>
- [16] ELDRIDGE, J., BELKIN, M. and WANG, Y. (2018). Unperturbed: Spectral analysis beyond Davis-Kahan. In *Algorithmic Learning Theory* 2018. *Proc*. *Mach*. *Learn*. *Res*. (*PMLR*) **83** 38. Proceedings of Machine Learning Research PMLR. [MR3857310](https://mathscinet.ams.org/mathscinet-getitem?mr=3857310)
- [17] ENGLERT, M. and RÄCKE, H. (2009). Oblivious routing for the *Lp*-norm. In *Proc*. 2009 50*th Annual IEEE Symposium on Foundations of Computer Science—FOCS* 2009 32–40. IEEE Comput. Soc., Los Alamitos, CA. [MR2648386](https://mathscinet.ams.org/mathscinet-getitem?mr=2648386)<https://doi.org/10.1109/FOCS.2009.52>
- [18] ERDOS˝ , L., KNOWLES, A., YAU, H.-T. and YIN, J. (2013). Spectral statistics of Erdos-Rényi graphs I: ˝ Local semicircle law. *Ann*. *Probab*. **41** 2279–2375. [MR3098073](https://mathscinet.ams.org/mathscinet-getitem?mr=3098073)<https://doi.org/10.1214/11-AOP734>
- [19] FAN, J., WANG, W. and ZHONG, Y. (2017). An *-*∞ eigenvector perturbation bound and its application to robust covariance estimation. *J*. *Mach*. *Learn*. *Res*. **18** 1–42. [MR3827095](https://mathscinet.ams.org/mathscinet-getitem?mr=3827095) [https://doi.org/10.5555/](https://doi.org/10.5555/3122009.3242064) [3122009.3242064](https://doi.org/10.5555/3122009.3242064)
- [20] FIEDLER, M. (1973). Algebraic connectivity of graphs. *Czechoslovak Math*. *J*. **23** 298–305. [MR0318007](https://mathscinet.ams.org/mathscinet-getitem?mr=0318007)
- [21] FÜREDI, Z. and KOMLÓS, J. (1981). The eigenvalues of random symmetric matrices. *Combinatorica* **1** 233–241. [MR0637828](https://mathscinet.ams.org/mathscinet-getitem?mr=0637828)<https://doi.org/10.1007/BF02579329>
- [22] GERŠGORIN, S. (1931). Über die abgrenzung der eigenwerte einer matrix. *Bull*. *Cl*. *Sci*. *Math*. *Nat*. *Sci*. *Math*. **6** 749–754.
- [23] GUÉDON, O., HINRICHS, A., LITVAK, A. E. and PROCHNO, J. (2017). On the expectation of operator norms of random matrices. In *Geometric Aspects of Functional Analysis*. *Lecture Notes in Math*. **2169** 151–162. Springer, Cham. [MR3645120](https://mathscinet.ams.org/mathscinet-getitem?mr=3645120)
- [24] GUPTA, A., HAJIAGHAYI, M. T. and RÄCKE, H. (2006). Oblivious network design. In *Proceedings of the Seventeenth Annual ACM–SIAM Symposium on Discrete Algorithms* 970–979. ACM, New York. [MR2373824](https://mathscinet.ams.org/mathscinet-getitem?mr=2373824)<https://doi.org/10.1145/1109557.1109665>

- <span id="page-39-0"></span>[25] HENDRICKX, J. M. and OLSHEVSKY, A. (2010). Matrix *p*-norms are NP-hard to approximate if *p* = 1*,* 2*,*∞. *SIAM J*. *Matrix Anal*. *Appl*. **31** 2802–2812. [MR2740634](https://mathscinet.ams.org/mathscinet-getitem?mr=2740634)<https://doi.org/10.1137/09076773X>
- [26] HIGHAM, N. J. (1987). A survey of condition number estimation for triangular matrices. *SIAM Rev*. **29** 575–596. [MR0917696](https://mathscinet.ams.org/mathscinet-getitem?mr=0917696)<https://doi.org/10.1137/1029112>
- [27] HIGHAM, N. J. (1992). Estimating the matrix *p*-norm. *Numer*. *Math*. **62** 539–555. [MR1174472](https://mathscinet.ams.org/mathscinet-getitem?mr=1174472) <https://doi.org/10.1007/BF01396242>
- [28] KHOT, S. and NAOR, A. (2012). Grothendieck-type inequalities in combinatorial optimization. *Comm*. *Pure Appl*. *Math*. **65** 992–1035. [MR2922372](https://mathscinet.ams.org/mathscinet-getitem?mr=2922372)<https://doi.org/10.1002/cpa.21398>
- [29] KRISHNAN, A., MOHANTY, S. and WOODRUFF, D. P. (2018). On sketching the *q* to *p* norms. In *Proc*. *Approximation*, *Randomization*, *and Combinatorial Optimization*. *Algorithms and Techniques*. *AP-PROX/RANDOM'*18. *LIPIcs*. *Leibniz Int*. *Proc*. *Inform*. **116** 15:1–15:20. Schloss Dagstuhl. Leibniz-Zent. Inform., Wadern. <https://doi.org/10.4230/LIPIcs.APPROX-RANDOM.2018.15>
- [30] LEE, J. O. and SCHNELLI, K. (2018). Local law and Tracy-Widom limit for sparse random matrices. *Probab*. *Theory Related Fields* **171** 543–616. [MR3800840](https://mathscinet.ams.org/mathscinet-getitem?mr=3800840)<https://doi.org/10.1007/s00440-017-0787-8>
- [31] MCSHERRY, F. (2001). Spectral partitioning of random graphs. In *Proc*. 42*nd IEEE Symposium on Foundations of Computer Science* (*Las Vegas*, *NV*, 2001) 529–537. IEEE Comput. Soc., Los Alamitos, CA. [MR1948742](https://mathscinet.ams.org/mathscinet-getitem?mr=1948742)
- [32] MECKES, M. W. (2004). Concentration of norms and eigenvalues of random matrices. *J*. *Funct*. *Anal*. **211** 508–524. [MR2057479](https://mathscinet.ams.org/mathscinet-getitem?mr=2057479) [https://doi.org/10.1016/S0022-1236\(03\)00198-8](https://doi.org/10.1016/S0022-1236(03)00198-8)
- [33] MITRA, P. (2009). Entrywise bounds for eigenvectors of random graphs. *Electron*. *J*. *Combin*. **16** Research Paper 131, 18. [MR2558268](https://mathscinet.ams.org/mathscinet-getitem?mr=2558268)<https://doi.org/10.37236/220>
- [34] NEWMAN, M. E. J. (2006). Finding community structure in networks using the eigenvectors of matrices. *Phys*. *Rev*. *E* (3) **74** 036104, 19. [MR2282139](https://mathscinet.ams.org/mathscinet-getitem?mr=2282139)<https://doi.org/10.1103/PhysRevE.74.036104>
- [35] NEWMAN, M. E. J. (2006). Modularity and community structure in networks. *Proc*. *Natl*. *Acad*. *Sci*. *USA* **103** 8577–8582. <https://doi.org/10.1073/pnas.0601602103>
- [36] O'ROURKE, S., VU, V. and WANG, K. (2016). Eigenvectors of random matrices: A survey. *J*. *Combin*. *Theory Ser*. *A* **144** 361–442. [MR3534074](https://mathscinet.ams.org/mathscinet-getitem?mr=3534074)<https://doi.org/10.1016/j.jcta.2016.06.008>
- [37] O'ROURKE, S., VU, V. and WANG, K. (2018). Random perturbation of low rank matrices: Improving classical bounds. *Linear Algebra Appl*. **540** 26–59. [MR3739989](https://mathscinet.ams.org/mathscinet-getitem?mr=3739989) [https://doi.org/10.1016/j.laa.2017.11.](https://doi.org/10.1016/j.laa.2017.11.014) [014](https://doi.org/10.1016/j.laa.2017.11.014)
- [38] PAGE, L., BRIN, S., MOTWANI, R. and WINOGRAD, T. (1999). The pagerank citation ranking: Bringing order to the web Technical Report. Stanford InfoLab.
- [39] POTHEN, A., SIMON, H. D. and LIOU, K.-P. (1990). Partitioning sparse matrices with eigenvectors of graphs. *SIAM J*. *Matrix Anal*. *Appl*. **11** 430–452. [MR1054210](https://mathscinet.ams.org/mathscinet-getitem?mr=1054210)<https://doi.org/10.1137/0611030>
- [40] RÄCKE, H. (2008). Optimal hierarchical decompositions for congestion minimization in networks. In *Proc*. *STOC'*08 255–264. ACM, New York. [MR2582666](https://mathscinet.ams.org/mathscinet-getitem?mr=2582666)<https://doi.org/10.1145/1374376.1374415>
- [41] RAYLEIGH BARON, J. W. S. (1896). *The Theory of Sound* **2**. Macmillan & Co, New York.
- [42] SCHNEIDER, H. and STRANG, W. G. (1962). Comparision theorems for supremum norms. *Numer*. *Math*. **4** 15–20. [MR0132070](https://mathscinet.ams.org/mathscinet-getitem?mr=0132070)<https://doi.org/10.1007/BF01386292>
- [43] SCHRÖDINGER, E. (1926). Quantisierung als eigenwertproblem. *Ann*. *Phys*. **385** 437–490. <https://doi.org/10.1002/andp.19263840404>
- [44] SHI, J. and MALIK, J. (2000). Normalized cuts and image segmentation. *IEEE Trans*. *Pattern Anal*. *Mach*. *Intell*. **22** 888–905. <https://doi.org/10.1109/34.868688>
- [45] STRZELECKA, M. (2019). Estimates of norms of log-concave random matrices with dependent entries. *Electron*. *J*. *Probab*. **24** 1–15. [MR4017125](https://mathscinet.ams.org/mathscinet-getitem?mr=4017125)<https://doi.org/10.1214/19-ejp365>
- [46] TANG, M. (2018). The eigenvalues of stochastic blockmodel graphs. Available at [arXiv:1803.11551](http://arxiv.org/abs/1803.11551).
- [47] VAN HANDEL, R. (2014). *Probability in High Dimension*. Princeton Univ. Press, Princeton. <https://doi.org/10.21236/ada623999>.
- [48] VERSHYNIN, R. (2018). *High-Dimensional Probability*: *An Introduction with Applications in Data Science*. *Cambridge Series in Statistical and Probabilistic Mathematics* **47**. Cambridge Univ. Press, Cambridge. [MR3837109](https://mathscinet.ams.org/mathscinet-getitem?mr=3837109)<https://doi.org/10.1017/9781108231596>
- [49] VON LUXBURG, U. (2007). A tutorial on spectral clustering. *Stat*. *Comput*. **17** 395–416. [MR2409803](https://mathscinet.ams.org/mathscinet-getitem?mr=2409803) <https://doi.org/10.1007/s11222-007-9033-z>
- [50] WAINWRIGHT, M. J. (2019). *High-Dimensional Statistics*: *A Non-asymptotic Viewpoint*. *Cambridge Series in Statistical and Probabilistic Mathematics* **48**. Cambridge Univ. Press, Cambridge. [MR3967104](https://mathscinet.ams.org/mathscinet-getitem?mr=3967104) <https://doi.org/10.1017/9781108627771>
- [51] WILF, H. S. (1970). *Finite Sections of Some Classical Inequalities*. *Ergebnisse der Mathematik und Ihrer Grenzgebiete* [*Results in Mathematics and Related Areas*], *Band* 52. Springer, New York. [MR0271762](https://mathscinet.ams.org/mathscinet-getitem?mr=0271762)
- [52] ZHONG, Y. (2017). Eigenvector under random perturbation: A nonasymptotic Rayleigh–Schrödinger theory. Available at [arXiv:1702.00139](http://arxiv.org/abs/1702.00139).