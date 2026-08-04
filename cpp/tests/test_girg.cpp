#include "twocascade/girg.hpp"
#include "twocascade/rng.hpp"

#include <iostream>
#include <vector>
#include <cstdlib>
#include <set>
#include <cmath>
#include <limits>

#define TEST_ASSERT(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "Assertion failed at " << __FILE__ << ":" << __LINE__ << ": " << #cond << std::endl; \
            std::exit(1); \
        } \
    } while (0)

static std::vector<Point2D> make_points(int n, std::mt19937_64& rng) {
    return sample_torus_points(n, rng);
}

static void assert_symmetric_simple(const std::vector<std::vector<int>>& adj, const char* label) {
    int n = static_cast<int>(adj.size());
    for (int i = 0; i < n; ++i) {
        std::set<int> seen;
        for (int j : adj[i]) {
            TEST_ASSERT(j != i); // no self-loop
            TEST_ASSERT(seen.insert(j).second); // no duplicate neighbor
            bool found = false;
            for (int k : adj[j]) {
                if (k == i) { found = true; break; }
            }
            TEST_ASSERT(found); // edge i-j implies edge j-i
        }
    }
    (void)label;
}

// --- Variant A: direct kernel -----------------------------------------------

void test_direct_degenerate_sizes() {
    std::cout << "Running test_direct_degenerate_sizes..." << std::endl;
    for (int n : {0, 1}) {
        std::mt19937_64 rng = make_seeded_rng(3, 0);
        std::vector<Point2D> pts = make_points(n, rng);
        std::vector<double> w(n, 1.0);
        Mt19937UniformSource src(rng);
        auto adj = sample_girg_adjacency_direct(pts, w, 1.0, src);
        TEST_ASSERT(static_cast<int>(adj.size()) == n);
        for (auto& nbrs : adj) TEST_ASSERT(nbrs.empty());
    }
    std::cout << "test_direct_degenerate_sizes passed!" << std::endl;
}

void test_direct_complete_graph_coverage() {
    std::cout << "Running test_direct_complete_graph_coverage..." << std::endl;
    // Weights large enough to saturate p_ij == 1 for every pair at every
    // distance: the sampled graph must be exactly complete (no gaps, no
    // duplicate visits -- there is no randomness left to hide either bug).
    for (int n : {2, 3, 5, 17, 64, 200}) {
        std::mt19937_64 rng = make_seeded_rng(1, 0);
        std::vector<Point2D> pts = make_points(n, rng);
        std::vector<double> w(n, 1e9);
        Mt19937UniformSource src(rng);
        auto adj = sample_girg_adjacency_direct(pts, w, 1.0, src);
        for (int i = 0; i < n; ++i) {
            TEST_ASSERT(static_cast<int>(adj[i].size()) == n - 1);
        }
        assert_symmetric_simple(adj, "direct-complete");
    }
    std::cout << "test_direct_complete_graph_coverage passed!" << std::endl;
}

void test_direct_coincident_points_skipped() {
    std::cout << "Running test_direct_coincident_points_skipped..." << std::endl;
    // Three coincident points + one distinct point, weights saturating p=1.
    // dist_sq == 0 must be a skip, not a probability-1 edge (matches the
    // Python oracle's `continue`); only vertex 3 (distance > 0) connects.
    std::vector<Point2D> pts = {{0.25, 0.25}, {0.25, 0.25}, {0.25, 0.25}, {0.75, 0.75}};
    std::vector<double> w(4, 1e9);
    ConstantUniformSource src(0.0); // accept every non-skipped pair
    auto adj = sample_girg_adjacency_direct(pts, w, 1.0, src);
    TEST_ASSERT(adj[0].size() == 1 && adj[0][0] == 3);
    TEST_ASSERT(adj[1].size() == 1 && adj[1][0] == 3);
    TEST_ASSERT(adj[2].size() == 1 && adj[2][0] == 3);
    std::set<int> nbrs3(adj[3].begin(), adj[3].end());
    TEST_ASSERT((nbrs3 == std::set<int>{0, 1, 2}));
    std::cout << "test_direct_coincident_points_skipped passed!" << std::endl;
}

void test_direct_output_is_symmetric_simple_graph() {
    std::cout << "Running test_direct_output_is_symmetric_simple_graph..." << std::endl;
    std::mt19937_64 rng = make_seeded_rng(12, 0);
    std::vector<Point2D> pts = make_points(400, rng);
    std::vector<double> w = sample_powerlaw_weights(400, 2.5, 0.245, rng);
    Mt19937UniformSource src(rng);
    auto adj = sample_girg_adjacency_direct(pts, w, 1.2, src);
    TEST_ASSERT(adj.size() == 400);
    assert_symmetric_simple(adj, "direct-random");
    std::cout << "test_direct_output_is_symmetric_simple_graph passed!" << std::endl;
}

// --- Variant B: BKL bucket sampler ------------------------------------------

void test_bkl_degenerate_sizes() {
    std::cout << "Running test_bkl_degenerate_sizes..." << std::endl;
    for (int n : {0, 1}) {
        std::mt19937_64 rng = make_seeded_rng(3, 0);
        std::vector<Point2D> pts = make_points(n, rng);
        std::vector<double> w(n, 1.0);
        Mt19937UniformSource src(rng);
        auto adj = sample_girg_adjacency_bkl(pts, w, 1.2, src);
        TEST_ASSERT(static_cast<int>(adj.size()) == n);
    }
    std::cout << "test_bkl_degenerate_sizes passed!" << std::endl;
}

void test_bkl_complete_graph_coverage() {
    std::cout << "Running test_bkl_complete_graph_coverage..." << std::endl;
    for (int n : {2, 3, 5, 17, 64, 200, 999}) {
        std::mt19937_64 rng = make_seeded_rng(1, 0);
        std::vector<Point2D> pts = make_points(n, rng);
        std::vector<double> w(n, 1e9);
        Mt19937UniformSource src(rng);
        auto adj = sample_girg_adjacency_bkl(pts, w, 1.2, src);
        for (int i = 0; i < n; ++i) {
            TEST_ASSERT(static_cast<int>(adj[i].size()) == n - 1);
        }
        assert_symmetric_simple(adj, "bkl-complete");
    }
    std::cout << "test_bkl_complete_graph_coverage passed!" << std::endl;
}

void test_bkl_output_is_symmetric_simple_graph() {
    std::cout << "Running test_bkl_output_is_symmetric_simple_graph..." << std::endl;
    std::mt19937_64 rng = make_seeded_rng(12, 0);
    std::vector<Point2D> pts = make_points(400, rng);
    std::vector<double> w = sample_powerlaw_weights(400, 2.5, 0.245, rng);
    Mt19937UniformSource src(rng);
    auto adj = sample_girg_adjacency_bkl(pts, w, 1.2, src);
    TEST_ASSERT(adj.size() == 400);
    assert_symmetric_simple(adj, "bkl-random");
    std::cout << "test_bkl_output_is_symmetric_simple_graph passed!" << std::endl;
}

// Independent restatement of the model's pair probability, written straight
// from the definition p_ij = min(1, (w_i w_j / (n d_ij^2))^alpha) rather than
// from girg_pair_probability's control flow. Its whole job is to be an ORACLE
// for the alpha <= 0 branch, where the pre-clamp form min(1, x)^alpha and the
// correct post-clamp form min(1, x^alpha) genuinely disagree.
static double oracle_pair_probability(const Point2D& a, const Point2D& b,
                                       double wa, double wb, int n, double alpha) {
    double dx = std::fabs(a.x - b.x);
    dx = std::min(dx, 1.0 - dx);
    double dy = std::fabs(a.y - b.y);
    dy = std::min(dy, 1.0 - dy);
    double d2 = dx * dx + dy * dy;
    if (d2 == 0.0) return 0.0; // coincident points are skipped, not saturated
    double ratio = (wa * wb) / (static_cast<double>(n) * d2);
    double powered = std::pow(ratio, alpha);
    return powered < 1.0 ? powered : 1.0;
}

void test_alpha_nonpositive_matches_independent_pair_probabilities() {
    std::cout << "Running test_alpha_nonpositive_matches_independent_pair_probabilities..." << std::endl;
    // RISKS.md #3: alpha_g <= 0 breaks the p_bar upper-bound rejection scheme's
    // monotonicity assumption, so sample_girg_adjacency_bkl falls back to
    // sample_girg_adjacency_direct there.
    //
    // This test USED to assert only `adj_direct == adj_bkl`, which is true BY
    // CONSTRUCTION (girg.cpp's alpha_g <= 0 branch literally returns
    // sample_girg_adjacency_direct(...)) and therefore proved nothing about
    // whether either variant computes the right probabilities. It missed a real
    // bug: girg_pair_probability clamped BEFORE the power, i.e. computed
    // min(1,x)^alpha, which for alpha < 0 is neither an upper bound nor the
    // model. Both variants agreed -- on the same wrong number.
    //
    // So the assertion is now against an INDEPENDENT evaluation of the
    // definition: with a constant-c source, an edge appears iff c < p_ij, so
    // the sampled edge set must equal the oracle's threshold set exactly. The
    // fallback identity is still checked, but as a secondary claim.
    const int n = 150;
    const double alpha = -1.0;
    std::mt19937_64 rng = make_seeded_rng(21, 0);
    std::vector<Point2D> pts = make_points(n, rng);
    std::vector<double> w = sample_powerlaw_weights(n, 2.5, 0.245, rng);

    for (double c : {1e-6, 0.5}) {
        std::set<std::pair<int, int>> expected;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (c < oracle_pair_probability(pts[i], pts[j], w[i], w[j], n, alpha)) {
                    expected.insert({i, j});
                }
            }
        }
        TEST_ASSERT(!expected.empty()); // a vacuous threshold set would prove nothing

        ConstantUniformSource src_a(c);
        ConstantUniformSource src_b(c);
        auto adj_direct = sample_girg_adjacency_direct(pts, w, alpha, src_a);
        auto adj_bkl = sample_girg_adjacency_bkl(pts, w, alpha, src_b);

        std::set<std::pair<int, int>> got_direct, got_bkl;
        for (int i = 0; i < n; ++i) {
            for (int j : adj_direct[i]) if (j > i) got_direct.insert({i, j});
            for (int j : adj_bkl[i]) if (j > i) got_bkl.insert({i, j});
        }
        TEST_ASSERT(got_direct == expected);
        TEST_ASSERT(got_bkl == expected);
        TEST_ASSERT(adj_direct == adj_bkl); // the fallback itself, now secondary
    }
    std::cout << "test_alpha_nonpositive_matches_independent_pair_probabilities passed!" << std::endl;
}

void test_bkl_degenerate_weights_fall_back_to_direct() {
    std::cout << "Running test_bkl_degenerate_weights_fall_back_to_direct..." << std::endl;
    // RISKS.md #4: w_min <= 0 or a non-finite weight breaks the weight-layer
    // key floor(log2(w/w_min)). Same determinism argument as above.
    std::mt19937_64 rng = make_seeded_rng(22, 0);
    std::vector<Point2D> pts = make_points(80, rng);
    std::vector<double> w_zero(80, 1.0);
    w_zero[0] = 0.0; // w_min == 0
    std::vector<double> w_inf(80, 1.0);
    w_inf[5] = std::numeric_limits<double>::infinity();

    for (const auto& w : {w_zero, w_inf}) {
        ConstantUniformSource src_a(0.2);
        ConstantUniformSource src_b(0.2);
        auto adj_direct = sample_girg_adjacency_direct(pts, w, 1.2, src_a);
        auto adj_bkl = sample_girg_adjacency_bkl(pts, w, 1.2, src_b);
        TEST_ASSERT(adj_direct == adj_bkl);
    }
    std::cout << "test_bkl_degenerate_weights_fall_back_to_direct passed!" << std::endl;
}

static long symmetric_difference_count(const std::vector<std::vector<int>>& a,
                                        const std::vector<std::vector<int>>& b) {
    std::set<std::pair<int, int>> ea, eb;
    for (size_t i = 0; i < a.size(); ++i) {
        for (int j : a[i]) {
            if (j > static_cast<int>(i)) ea.insert({static_cast<int>(i), j});
        }
    }
    for (size_t i = 0; i < b.size(); ++i) {
        for (int j : b[i]) {
            if (j > static_cast<int>(i)) eb.insert({static_cast<int>(i), j});
        }
    }
    long diff = 0;
    for (auto& e : ea) if (!eb.count(e)) ++diff;
    for (auto& e : eb) if (!ea.count(e)) ++diff;
    return diff;
}

void test_bkl_vs_direct_level_set_identity_high_threshold() {
    std::cout << "Running test_bkl_vs_direct_level_set_identity_high_threshold..." << std::endl;
    // TWICE-CORRECTED SCOPE -- recorded here because the first correction
    // (this test originally asserted exact identity at c in {1e-6,0.3,0.9})
    // was itself only PARTIALLY right, and the record needs to survive past
    // this session (okf/lessons.md: don't silently narrow, or re-widen, a
    // documented invariant without saying so).
    //
    // First correction (G2): RISKS.md #1 assumed a constant-c stub makes
    // direct and bkl agree "at literally every threshold c", the way it does
    // for C1's fast-vs-slow port. That is only true while every visited
    // cell-pair group has p_bar >= 1 (the exact-enumeration branch, tested
    // separately and reliably by test_bkl_complete_graph_coverage above).
    //
    // Second correction (G5, this fixture): "high c" is not by itself
    // sufficient either, and the reason is exact, not approximate. Once
    // p_bar < 1 for a group, bkl's geometric-skip branch accepts a candidate
    // pair iff u.next() < exact_p(i,j) / p_bar. Since p_bar < 1 by
    // construction of that branch, exact_p/p_bar > exact_p for any
    // exact_p > 0 -- so the skip branch's accept condition is PROVABLY WEAKER
    // than the direct kernel's u.next() < exact_p(i,j) at the SAME constant
    // u, for any c whatsoever, including c close to 1. A pair with a tiny
    // absolute exact_p can still cross a high c if its ratio to its own
    // group's (necessarily larger) upper bound is high enough. This was
    // missed in G2 because that session's one embedded fixture happened not
    // to contain such a pair at c in {0.9,0.95,0.99} -- fixture luck, not a
    // guarantee (confirmed by deriving a concrete counterexample against the
    // Python oracle during G5: n=200, c=0.9, a pair with exact_p ~ 0.054 and
    // group p_bar ~ 0.060, giving ratio ~0.90+ and one spurious bkl edge).
    //
    // So: exact identity holds ONLY in the p_bar>=1-forced regime (covered
    // separately, deterministically, by test_bkl_complete_graph_coverage).
    // Elsewhere, this test checks a BOUNDED small symmetric difference at
    // high c, not zero -- a real partition bug (a doubled or dropped cell
    // pair) still shows up as a LARGE, systematic difference (thousands of
    // edges, as seen at c=1e-6 during G2's investigation), so a tight bound
    // here still catches that failure mode while not asserting a false
    // exact-equality guarantee. The non-saturating regime's overall
    // correctness is covered by the (separate, required) statistical battery
    // in tests/test_cpp_girg_validation.py (G5): edge count, degree
    // histogram, distance-binned edges, all against the Python oracle under
    // real RNG.
    //
    // n=331 deliberately spans multiple non-power-of-two-friendly cell grids
    // across the level range (L is >=2 for n this size), exercising the
    // multi-level recursion rather than only the deepest level.
    std::mt19937_64 rng = make_seeded_rng(2026, 0);
    std::vector<Point2D> pts = make_points(331, rng);
    std::vector<double> w = sample_powerlaw_weights(331, 2.5, 0.245, rng);

    const long kMaxSymmetricDiff = 3; // small and fixed, not tuned per-c to pass
    for (double c : {0.9, 0.95, 0.99}) {
        ConstantUniformSource src_direct(c);
        ConstantUniformSource src_bkl(c);
        auto adj_direct = sample_girg_adjacency_direct(pts, w, 1.2, src_direct);
        auto adj_bkl = sample_girg_adjacency_bkl(pts, w, 1.2, src_bkl);
        long diff = symmetric_difference_count(adj_direct, adj_bkl);
        TEST_ASSERT(diff <= kMaxSymmetricDiff);
    }
    std::cout << "test_bkl_vs_direct_level_set_identity_high_threshold passed!" << std::endl;
}

// Counts uniform draws while passing a real RNG through. Every unit of pair
// work in either sampler consumes at least one draw -- the direct kernel draws
// exactly once per pair, and BKL draws once per geometric skip, once per
// candidate accepted by the skip, and once per exactly-enumerated pair -- so
// the draw count IS the visited-pair work, measured exactly and reproducibly
// rather than inferred from a wall clock.
class CountingUniformSource : public IUniformSource {
public:
    explicit CountingUniformSource(std::mt19937_64& rng) : rng_(rng) {}
    double next() override { ++count_; return dist_(rng_); }
    long long count() const { return count_; }

private:
    std::mt19937_64& rng_;
    std::uniform_real_distribution<double> dist_{0.0, 1.0};
    long long count_ = 0;
};

void test_bkl_pair_work_grows_slower_than_quadratically() {
    std::cout << "Running test_bkl_pair_work_grows_slower_than_quadratically..." << std::endl;
    // This test previously measured NOTHING that its name claims: it sampled at
    // two sizes and asserted only symmetry, with a comment about bounding
    // wall-clock growth that no code implemented. It now counts pair work
    // exactly, via the uniform-draw counter above.
    //
    // Wall clock is deliberately still not used (flaky on a shared machine);
    // real timings live in scripts/bench_girg.py's committed table. Draw counts
    // are deterministic given the seed, so the bounds below are pass/fail
    // facts about the algorithm, not machine-dependent thresholds.
    const int n_small = 2000;
    const int n_large = 8000;
    long long draws_small = 0, draws_large = 0;

    for (int n : {n_small, n_large}) {
        std::mt19937_64 rng = make_seeded_rng(77, 0);
        std::vector<Point2D> pts = make_points(n, rng);
        std::vector<double> w = sample_powerlaw_weights(n, 2.5, 0.245, rng);
        CountingUniformSource src(rng);
        auto adj = sample_girg_adjacency_bkl(pts, w, 1.2, src);
        TEST_ASSERT(static_cast<int>(adj.size()) == n);
        assert_symmetric_simple(adj, "bkl-scaling");
        (n == n_small ? draws_small : draws_large) = src.count();
    }

    const double pairs_large = 0.5 * static_cast<double>(n_large)
                             * static_cast<double>(n_large - 1);
    std::cout << "  bkl draws: n=" << n_small << " -> " << draws_small
              << ", n=" << n_large << " -> " << draws_large
              << " (full enumeration at n=" << n_large << " would be "
              << static_cast<long long>(pairs_large) << ")" << std::endl;

    TEST_ASSERT(draws_small > 0 && draws_large > 0);

    // (1) Absolute: BKL must visit far fewer pairs than full enumeration at the
    //     larger size. Measured: 527651 draws vs 31996000 pairs, a ratio of
    //     0.0165 (~1/61); 0.25 is the loose bound around it.
    TEST_ASSERT(static_cast<double>(draws_large) < 0.25 * pairs_large);

    // (2) Growth: a 4x increase in n costs strictly less than the 16x a
    //     quadratic algorithm would. Measured: 115509 -> 527651 draws, a growth
    //     of 4.57x. 10x is loose enough to survive fixture noise, tight enough
    //     that any regression to per-pair enumeration (which would land at
    //     exactly 16.0x) fails it.
    double growth = static_cast<double>(draws_large) / static_cast<double>(draws_small);
    std::cout << "  growth over 4x n: " << growth << "x (quadratic would be 16x)" << std::endl;
    TEST_ASSERT(growth < 10.0);

    // (3) Control: the direct kernel draws exactly once per pair, confirming
    //     the counter measures what the claim needs it to measure.
    {
        std::mt19937_64 rng = make_seeded_rng(77, 0);
        std::vector<Point2D> pts = make_points(n_small, rng);
        std::vector<double> w = sample_powerlaw_weights(n_small, 2.5, 0.245, rng);
        CountingUniformSource src(rng);
        sample_girg_adjacency_direct(pts, w, 1.2, src);
        TEST_ASSERT(src.count() == static_cast<long long>(n_small) * (n_small - 1) / 2);
    }
    std::cout << "test_bkl_pair_work_grows_slower_than_quadratically passed!" << std::endl;
}

void test_all_points_coincident_produces_no_edges() {
    std::cout << "Running test_all_points_coincident_produces_no_edges..." << std::endl;
    // Every pairwise distance is exactly 0 (d^2 == 0 is a skip, not a
    // saturating edge -- RISKS.md #2), so BOTH variants must produce an empty
    // graph even with weights large enough to saturate p to 1 everywhere a
    // distance were nonzero. This is the degenerate case where BKL's cell
    // grid collapses every point into the SAME cell at every level (there is
    // never a non-touching cell pair to route through the geometric-skip
    // path), so it also exercises "the deepest-level same-cell loop correctly
    // finds zero edges" rather than crashing or hanging.
    int n = 50;
    std::vector<Point2D> pts(n, Point2D{0.37, 0.61});
    std::vector<double> w(n, 1e9);

    ConstantUniformSource src_direct(0.0); // accept everything not skipped
    auto adj_direct = sample_girg_adjacency_direct(pts, w, 1.2, src_direct);
    for (auto& nbrs : adj_direct) {
        TEST_ASSERT(nbrs.empty());
    }

    ConstantUniformSource src_bkl(0.0);
    auto adj_bkl = sample_girg_adjacency_bkl(pts, w, 1.2, src_bkl);
    for (auto& nbrs : adj_bkl) {
        TEST_ASSERT(nbrs.empty());
    }
    std::cout << "test_all_points_coincident_produces_no_edges passed!" << std::endl;
}

void test_girg_pair_probability_bounds() {
    std::cout << "Running test_girg_pair_probability_bounds..." << std::endl;
    Point2D a{0.1, 0.1};
    Point2D b{0.9, 0.9}; // far apart on the torus (wraps to near)
    double p = girg_pair_probability(a, b, 1.0, 1.0, 1000, 1.2);
    TEST_ASSERT(p >= 0.0 && p <= 1.0);

    Point2D coincident{0.5, 0.5};
    double p_coincident = girg_pair_probability(coincident, coincident, 1e9, 1e9, 100, 1.2);
    TEST_ASSERT(p_coincident == 0.0);

    double p_saturating = girg_pair_probability(a, b, 1e12, 1e12, 10, 1.2);
    TEST_ASSERT(p_saturating == 1.0);

    // alpha_g <= 0: the clamp must be applied AFTER the power. These two cases
    // are hand-computable to exact doubles and are precisely the ones the old
    // clamp-before-power form got wrong, so they are a discriminator, not a
    // restatement of the implementation.
    //
    //   pts (0.1,0.1) and (0.2,0.1): dx = 0.1, dy = 0, d^2 = 0.01.
    //   n=10,   w=1: base = 1/(10*0.01)   = 10  > 1, base^-1 = 0.1  -> 0.1
    //                (old form: base >= 1 short-circuited to 1.0)
    //   n=1000, w=1: base = 1/(1000*0.01) = 0.1 < 1, base^-1 = 10   -> 1.0
    //                (old form: returned 10.0, not even a probability)
    Point2D near_a{0.1, 0.1};
    Point2D near_b{0.2, 0.1};
    double p_neg_big_base = girg_pair_probability(near_a, near_b, 1.0, 1.0, 10, -1.0);
    TEST_ASSERT(std::fabs(p_neg_big_base - 0.1) < 1e-12);
    double p_neg_small_base = girg_pair_probability(near_a, near_b, 1.0, 1.0, 1000, -1.0);
    TEST_ASSERT(p_neg_small_base == 1.0);

    // alpha_g == 0 is the boundary: every non-coincident pair has p == 1.
    TEST_ASSERT(girg_pair_probability(near_a, near_b, 1.0, 1.0, 10, 0.0) == 1.0);
    TEST_ASSERT(girg_pair_probability(near_a, near_b, 1.0, 1.0, 1000, 0.0) == 1.0);
    std::cout << "test_girg_pair_probability_bounds passed!" << std::endl;
}

int main() {
    test_direct_degenerate_sizes();
    test_direct_complete_graph_coverage();
    test_direct_coincident_points_skipped();
    test_direct_output_is_symmetric_simple_graph();
    test_girg_pair_probability_bounds();
    test_bkl_degenerate_sizes();
    test_bkl_complete_graph_coverage();
    test_bkl_output_is_symmetric_simple_graph();
    test_alpha_nonpositive_matches_independent_pair_probabilities();
    test_bkl_degenerate_weights_fall_back_to_direct();
    test_bkl_vs_direct_level_set_identity_high_threshold();
    test_bkl_pair_work_grows_slower_than_quadratically();
    test_all_points_coincident_produces_no_edges();
    std::cout << "All GIRG tests passed!" << std::endl;
    return 0;
}
