#include "twocascade/graph.hpp"
#include "twocascade/rng.hpp"
#include "twocascade/engine.hpp"

#include <iostream>
#include <vector>
#include <cstdlib>

#define TEST_ASSERT(cond) \
    do { \
        if (!(cond)) { \
            std::cerr << "Assertion failed at " << __FILE__ << ":" << __LINE__ << ": " << #cond << std::endl; \
            std::exit(1); \
        } \
    } while (0)

void test_rng_seeding() {
    std::cout << "Running test_rng_seeding..." << std::endl;
    
    // Identical seeds and trials must produce identical streams from position 0
    std::mt19937_64 rng1 = make_seeded_rng(42, 0);
    std::mt19937_64 rng2 = make_seeded_rng(42, 0);
    for (int i = 0; i < 100; ++i) {
        TEST_ASSERT(rng1() == rng2());
    }
    
    // Different base seeds must produce different streams from position 0
    std::mt19937_64 a = make_seeded_rng(42, 0);
    std::mt19937_64 b = make_seeded_rng(43, 0);
    bool different_seed = false;
    for (int i = 0; i < 100; ++i) {
        if (a() != b()) {
            different_seed = true;
            break;
        }
    }
    TEST_ASSERT(different_seed);
    
    // Different trial indices must produce different streams from position 0
    std::mt19937_64 c = make_seeded_rng(42, 0);
    std::mt19937_64 d = make_seeded_rng(42, 1);
    bool different_trial = false;
    for (int i = 0; i < 100; ++i) {
        if (c() != d()) {
            different_trial = true;
            break;
        }
    }
    TEST_ASSERT(different_trial);

    // Seeding regression check: (42, 1) vs (43, 0) must differ
    // (these collided under the old base_seed + trial_index addition scheme)
    std::mt19937_64 e = make_seeded_rng(42, 1);
    std::mt19937_64 f = make_seeded_rng(43, 0);
    bool regression_differs = false;
    for (int i = 0; i < 100; ++i) {
        if (e() != f()) {
            regression_differs = true;
            break;
        }
    }
    TEST_ASSERT(regression_differs);
    
    std::cout << "test_rng_seeding passed!" << std::endl;
}

void test_gnp_generator() {
    std::cout << "Running test_gnp_generator..." << std::endl;
    std::mt19937_64 rng = make_seeded_rng(123, 0);
    
    // p = 0.0 -> no edges
    CSRGraph g_zero = sample_gnp_adjacency(100, 0.0, rng);
    TEST_ASSERT(g_zero.n == 100);
    TEST_ASSERT(g_zero.column_indices.empty());
    TEST_ASSERT(g_zero.row_offsets.size() == 101);
    for (int val : g_zero.row_offsets) {
        TEST_ASSERT(val == 0);
    }
    
    // p = 1.0 -> fully connected graph
    CSRGraph g_full = sample_gnp_adjacency(50, 1.0, rng);
    TEST_ASSERT(g_full.n == 50);
    TEST_ASSERT(g_full.column_indices.size() == 50 * 49);
    TEST_ASSERT(g_full.row_offsets.size() == 51);
    for (int i = 0; i <= 50; ++i) {
        TEST_ASSERT(g_full.row_offsets[i] == i * 49);
    }
    
    // Check no self-loops, symmetry, and sorted/duplicate-free rows in a random graph
    CSRGraph g_rand = sample_gnp_adjacency(100, 0.1, rng);
    TEST_ASSERT(g_rand.n == 100);
    for (int u = 0; u < 100; ++u) {
        int start = g_rand.row_offsets[u];
        int end = g_rand.row_offsets[u + 1];
        
        // Assert sorting and duplicate-free adjacency values
        for (int j = start; j < end; ++j) {
            int v = g_rand.column_indices[j];
            TEST_ASSERT(u != v); // No self-loops
            
            if (j > start) {
                int prev_v = g_rand.column_indices[j - 1];
                TEST_ASSERT(prev_v < v); // Strictly sorted and duplicate-free
            }
            
            // Check symmetry: edge (v, u) must also exist
            int start_v = g_rand.row_offsets[v];
            int end_v = g_rand.row_offsets[v + 1];
            bool found_symmetric = false;
            for (int k = start_v; k < end_v; ++k) {
                if (g_rand.column_indices[k] == u) {
                    found_symmetric = true;
                    break;
                }
            }
            TEST_ASSERT(found_symmetric);
        }
    }
    std::cout << "test_gnp_generator passed!" << std::endl;
}

void test_beta_generator() {
    std::cout << "Running test_beta_generator..." << std::endl;
    std::mt19937_64 rng = make_seeded_rng(999, 0);
    
    // mu = 0.0 -> all fears 0.0
    std::vector<double> fears_zero = sample_individual_fears(100, 0.0, 10.0, rng);
    for (double f : fears_zero) {
        TEST_ASSERT(f == 0.0);
    }
    
    // mu = 1.0 -> all fears 1.0
    std::vector<double> fears_one = sample_individual_fears(100, 1.0, 10.0, rng);
    for (double f : fears_one) {
        TEST_ASSERT(f == 1.0);
    }
    
    // Normal path statistical sanity check
    std::vector<double> fears_normal = sample_individual_fears(10000, 0.3, 50.0, rng);
    double sum = 0.0;
    for (double f : fears_normal) {
        TEST_ASSERT(f >= 0.0 && f <= 1.0);
        sum += f;
    }
    double sample_mean = sum / 10000.0;
    // Deterministic mean check (with seed 999, mean is approx 0.3)
    double diff = sample_mean - 0.3;
    if (diff < 0) diff = -diff;
    TEST_ASSERT(diff < 0.02);
    
    // Extreme small concentration underflow check
    std::vector<double> fears_underflow = sample_individual_fears(1000, 0.3, 1e-25, rng);
    int ones_count = 0;
    for (double f : fears_underflow) {
        TEST_ASSERT(f == 0.0 || f == 1.0);
        if (f == 1.0) ones_count++;
    }
    TEST_ASSERT(ones_count > 150 && ones_count < 450);
    
    std::cout << "test_beta_generator passed!" << std::endl;
}

void test_cascade_engine() {
    std::cout << "Running test_cascade_engine..." << std::endl;
    
    // Path graph: 0 - 1 - 2
    CSRGraph graph;
    graph.n = 3;
    graph.row_offsets = {0, 1, 3, 4};
    graph.column_indices = {1, 0, 2, 1};
    
    std::vector<double> fears = {0.0, 0.0, 0.0};
    std::mt19937_64 rng = make_seeded_rng(0, 0);
    CascadeBuffers buffers;
    
    // Case 1: Seed node 0, solvency threshold r = 2, window_len = 1
    // Node 1 only has 1 failed neighbor (0), so it should NOT fail.
    // Final failed set = {0}, rounds completed = 0
    CascadeResult res1 = run_cascade(graph, fears, 2, {0}, rng, true, 1, {}, buffers);
    TEST_ASSERT(res1.total_failed == 1);
    TEST_ASSERT(res1.rounds_completed == 0);
    TEST_ASSERT(res1.final_failed_fraction == 1.0 / 3.0);
    TEST_ASSERT(res1.history.size() == 1);
    TEST_ASSERT(res1.history[0] == 1);
    TEST_ASSERT(buffers.failed[0] == 1);
    TEST_ASSERT(buffers.failed[1] == 0);
    TEST_ASSERT(buffers.failed[2] == 0);
    
    // Case 2: Seed nodes 0 and 2, solvency threshold r = 2, window_len = 1
    // Node 1 has 2 failed neighbors (0, 2), so it fails.
    // Final failed set = {0, 1, 2}, rounds completed = 1
    CascadeResult res2 = run_cascade(graph, fears, 2, {0, 2}, rng, true, 1, {}, buffers);
    TEST_ASSERT(res2.total_failed == 3);
    TEST_ASSERT(res2.rounds_completed == 1);
    TEST_ASSERT(res2.final_failed_fraction == 1.0);
    TEST_ASSERT(res2.history.size() == 2);
    TEST_ASSERT(res2.history[0] == 2);
    TEST_ASSERT(res2.history[1] == 3);
    TEST_ASSERT(buffers.failed[0] == 1);
    TEST_ASSERT(buffers.failed[1] == 1);
    TEST_ASSERT(buffers.failed[2] == 1);
    
    // Case 3: Seed nodes 0 and 2, solvency threshold r = 2, window_len = 2
    // Testing early termination when all nodes fail (total_failed == n)
    // - Post-seed: failures_per_round = [2], total = 2
    // - Round 1: Node 1 fails. total becomes 3. failures_per_round = [2, 1]
    // - Next loop iteration: total_failed == n (3 == 3) fires, breaking out immediately.
    // rounds_completed must be exactly 1, and history size 2.
    CascadeResult res3 = run_cascade(graph, fears, 2, {0, 2}, rng, true, 2, {0.5, 0.5}, buffers);
    TEST_ASSERT(res3.total_failed == 3);
    TEST_ASSERT(res3.rounds_completed == 1);
    TEST_ASSERT(res3.history.size() == 2);
    TEST_ASSERT(res3.history[0] == 2);
    TEST_ASSERT(res3.history[1] == 3);
    
    // Case 4: Seed node 0, solvency threshold r = 2, window_len = 2
    // Testing intermediate quiet round halting (window_len > 1 contrast pair with Case 1)
    // - Post-seed: failures_per_round = [1], total = 1, history = [1]
    // - Round 1: Node 1 has 1 < r failed neighbors, so 0 failures.
    //   failures_per_round becomes [1, 0]. rounds_completed = 1, history = [1, 1].
    // - Round 2: 0 failures. failures_per_round becomes [0, 0]. Breaks before bookkeeping.
    // Expected: total_failed = 1, rounds_completed = 1, history = {1, 1}.
    CascadeResult res4 = run_cascade(graph, fears, 2, {0}, rng, true, 2, {0.5, 0.5}, buffers);
    TEST_ASSERT(res4.total_failed == 1);
    TEST_ASSERT(res4.rounds_completed == 1);
    TEST_ASSERT(res4.history.size() == 2);
    TEST_ASSERT(res4.history[0] == 1);
    TEST_ASSERT(res4.history[1] == 1);
    
    std::cout << "test_cascade_engine passed!" << std::endl;
}

int main() {
    test_rng_seeding();
    test_gnp_generator();
    test_beta_generator();
    test_cascade_engine();
    std::cout << "ALL C++ TESTS PASSED SUCCESSFULLY!" << std::endl;
    return 0;
}
