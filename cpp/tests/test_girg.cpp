#include "twocascade/girg.hpp"
#include "twocascade/rng.hpp"

#include <iostream>
#include <vector>
#include <cstdlib>
#include <set>
#include <cmath>

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
    std::cout << "test_girg_pair_probability_bounds passed!" << std::endl;
}

int main() {
    test_direct_degenerate_sizes();
    test_direct_complete_graph_coverage();
    test_direct_coincident_points_skipped();
    test_direct_output_is_symmetric_simple_graph();
    test_girg_pair_probability_bounds();
    std::cout << "All GIRG tests passed!" << std::endl;
    return 0;
}
