# Engaging with Prof. Dhara's Research — An Honest Strategy

> **Purpose.** A practical guide for connecting the Two-Channel Cascade project to Prof. Souvik
> Dhara's research in a way that strengthens the advising relationship *and* survives expert
> scrutiny. Written as a corrective to an AI-generated "applications" document that bridged the
> project to three of his papers with confident but partly fabricated mathematics. The goal here is
> real engagement done accurately and lightly — not a machinery transplant.

---

## 1. The goal, stated honestly

The underlying instinct is good: showing an advisor you've engaged with their work builds rapport and
situates your project inside their research program. That is worth doing. The question is *how*.

The thing that lands with a sharp probabilist is evidence you have **read and understood** his work
accurately. The thing that damages credibility fastest is a **forced or incorrect connection** — and
a domain expert spots both immediately. So the entire strategy reduces to one rule:

> **Connect only where the connection is real, and state it only as accurately as you can defend it.**

Done right, this costs an afternoon of reading and a few correct sentences. Done wrong — inserting
derivations you can't verify — it actively signals the opposite of engagement: that you ran his
papers through a model instead of reading them.

---

## 2. The principle: genuine engagement beats inserted machinery

There are two distinct ways a project can "connect to" an advisor's work, and they are not equally
valuable or equally safe:

1. **Methodological borrowing** — actually using a theorem, assumption set, or technique from a paper
   as a tool in your own analysis. High value, but only honest where the models genuinely align.
2. **Dialect and framing** — describing your results in the vocabulary of his research program
   (critical window, finite-size scaling, universality class) so he recognizes the language and sees
   where your problem sits. Lower stakes, cheap, and almost always the right move for a 10-week
   undergraduate project.

Your project supports a small amount of (1) and a comfortable amount of (2). It does **not** support
mapping your cascade onto his metric-geometry or random-matrix work — those are analogies at best.
Pursue (2) freely, (1) only where noted below, and decline the rest.

---

## 3. What actually builds the relationship

**Speak the critical-window dialect — correctly.** Your `μ=0` baseline *is* the bootstrap
percolation of Janson, Łuczak, Turova & Vallier (2012). Dhara's critical-window program is the
natural home for the finite-size-scaling questions you're already asking (Q3). Framing your
transition-width study (Weeks 6–7) in this language is, per your own §6, "the cheapest way to speak
Dhara's dialect." It is accurate, natural, and requires no new mathematics.

**Cite the right papers in the right places.** The two genuinely relevant anchors are already in your
tracker §13: the 2017 critical-window paper (configuration model, finite third moment) and the 2021
scale-free critical-percolation paper. Cite these as the *lineage* your finite-size questions belong
to — not as tools you apply. One accurate citation in the right place beats a page of forced ones.

**Ask one genuinely good question.** Advisors remember students who ask the question that shows they
understood the *boundary* of the theory. Your strongest card is that your transition is the bootstrap
(`r ≥ 2`) analogue — first-order, by the Janson dichotomy — rather than the continuous `r = 1`
critical-window picture his machinery is built for. Asking how (or whether) that machinery transfers
is flattering, substantive, and honest about the gap. See §5 for phrasings.

**Read one paper properly.** The 2017 critical-window paper is closest to you. An afternoon of real
reading lets you reference it correctly in conversation, which is worth more than any inserted
derivation. If it comes up and you can speak to it accurately, that *is* the payoff.

**Borrow scaffolding only if you reach the stretch.** If Q2 resolves toward a configuration-model
variant (Week 8), his moment-assumption framework is the legitimate scaffolding for building a valid
critical network, and citing it is genuine methodological use — the strongest signal of all. Keep it
in your back pocket; don't build it in now.

---

## 4. An honest map of where his work touches your project

So the correct connections are on record (and the incorrect ones stay off it):

**Genuine touchpoints.**

- *Lineage.* Your baseline is Janson; Dhara's critical-window line is where the finite-size-scaling
  questions (Q3) live. The 2017 paper is the conceptual anchor.
- *Dialect.* The transition-width exponent `ν` (width `~ n^{-1/ν}`) is your bridge to his language.
  It's a simulation-and-curve-fit measurement you'd make regardless; the framing is what connects it.
- *Conditional tool.* If you pivot to a configuration model, his moment assumptions give you a valid
  critical degree sequence, and the `τ ∈ (3,4)` vs `τ ∈ (2,3)` split gives you two named
  universality classes to organize results around.

**Honest non-connections (do not present these as applied).**

- The metric-geometry results (Gromov–Hausdorff–Prokhorov convergence, diameter scaling) are not
  tools for your project. At most they are a distant analogy.
- The "tiny giant" `Θ(√n)` phenomenon in the `τ ∈ (2,3)` scale-free paper is *connectivity*
  percolation (effectively `r = 1`), not `r ≥ 2` bootstrap. The "sudden emergence" is a conceptual
  parallel for cascade takeoff — nothing more. Don't claim a shared mechanism.
- The `r`-to-`p` (operator-norm) random-matrix paper is a CLT for a different object. The
  "spectral interpretation of the panic channel" is a stretch-of-a-stretch; by the AI document's own
  admission it lands in an endpoint case where the paper's theorems don't apply. Leave it out unless
  you deliberately take it up as an independent exploration.

---

## 5. Ready-to-use material

**Framing sentences for the write-up / intro** (accurate and modest):

- "The `μ = 0` specialization of our model is the bootstrap percolation of Janson, Łuczak, Turova and
  Vallier (2012). We situate the finite-size behavior of the two-channel cascade boundary within the
  critical-window framework developed for configuration and scale-free graphs by Dhara, van der
  Hofstad and collaborators."
- "We characterize the transition-width exponent `ν` (width `~ n^{-1/ν}`) of the systemic-event
  boundary empirically, in the spirit of finite-size critical-window analyses, without claiming a
  matching rigorous result."

**Questions to bring to a meeting** (these are your tracker's open questions, framed to his
interests):

- *On the transition type:* "My boundary is the bootstrap `r ≥ 2` analogue, so it's first-order by
  the Janson dichotomy rather than the continuous `r = 1` critical-window picture. Is there a
  finite-size-scaling treatment for the first-order case, or does the critical-window machinery not
  transfer?"
- *On Q2 (model choice):* "Would you prefer I keep the cleanest possible Janson comparison on
  `G(n,p)`, or move to a configuration model where degree heterogeneity and targeted seeding become
  meaningful and the problem connects to your critical-window work?"
- *On Q3 (framing):* "Is a finite-size width-exponent framing of the cascade boundary of interest to
  you, and is it reasonable to probe empirically without a proof?"

---

## 6. What to avoid — the failure mode to learn from

The AI-generated "applications" document is a case study in pandering done wrong. Specific lessons:

- **Never present a formula you haven't checked against the source.** That document mis-transcribed
  the critical value `λ_c` from the scale-free paper (a stray factor of `α` and a mis-stated constant
  `B_α`) while attributing it confidently to a specific equation number. Presenting a wrong version
  of *his own* result is worse than not citing it.
- **Never let the model invent an error in his paper to cover its own.** The "improved" version
  asserted that the published paper contains a typo — almost certainly a rationalization of the
  AI's earlier transcription mistake. Telling your advisor his paper is wrong, on that basis, is a
  credibility catastrophe.
- **AI-generated citation tags are not citations.** Equation and theorem numbers produced by a model
  that cannot read the PDF carry no evidence of being correct. They make a document *look* grounded
  while remaining unverified.
- **Conceptual analogy is not methodological application.** A document that repeatedly says "this is
  a conceptual parallel" and "the theorem's assumptions do not directly hold" is telling you the
  connection isn't real. An expert reads that as padding.

---

## 7. Verification checklist (before you cite or claim anything about his work)

Run this before any of his results enters your write-up or a meeting:

1. **Did I read it in the actual paper?** Open the PDF and read the statement in context. If you
   can't point to the page, don't cite the formula.
2. **Can I defend it out loud?** If your advisor asked "where does this come from?", could you answer
   without the document? If not, it's not yours yet.
3. **Is it a tool or an analogy?** State it as whatever it actually is. Never dress an analogy up as
   an application.
4. **Is it the smallest accurate claim?** Prefer "this sits in the critical-window literature" over a
   specific borrowed equation you don't need.
5. **Would I stake my credibility on it?** If not, cut it. With this advisor, one correct, modest
   sentence outperforms a page of impressive-looking machinery.

---

## 8. Bottom line

Keep the goal; change the tactic. The version of engagement that strengthens the relationship is
small, accurate, and mostly framing: a couple of correct sentences placing your work in his
critical-window program, one good question that shows you understand where the theory stops, and — if
you have an afternoon — one of his papers actually read. That is real, defensible engagement.
Everything beyond it is risk without reward.

---

### References (from tracker §13 — trusted)

- Janson, Łuczak, Turova & Vallier (2012), "Bootstrap percolation on the random graph `G(n,p)`,"
  *Ann. Appl. Probab.* 22(5), 1989–2047. arXiv:1012.3535. *(Your `μ=0` benchmark.)*
- Dhara, van der Hofstad, van Leeuwaarden & Sen (2017), "Critical window for the configuration model:
  finite third moment degrees," *EJP* 22(16). arXiv:1605.02868. *(Primary citation anchor.)*
- Dhara, van der Hofstad & van Leeuwaarden (2021), "Critical percolation on scale-free random
  graphs," *Comm. Math. Phys.* 382, 123–171. arXiv:1909.05590. *(Secondary anchor.)*
- Bhamidi, Dhara, van der Hofstad & Sen (2022), "Global lower mass-bound for critical configuration
  models in the heavy-tailed regime," *EJP* 27(103). *(Configuration-model context, if Q2 pivots.)*
- Bhamidi, Dhara & van der Hofstad, "Multiscale genesis of a tiny giant for percolation on scale-free
  random graphs." *(Scale-free `τ ∈ (2,3)` percolation; analogy only, not a tool.)*
