#ifndef TWOCASCADE_ENGINE_HPP
#define TWOCASCADE_ENGINE_HPP

#include "graph.hpp"
#include <vector>
#include <cstdint>
#include <random>

/**
 * @brief Represents the outcome of a single cascade simulation.
 * Mirrors twocascade.reference.CascadeResult fields and types.
 */
struct CascadeResult {
    double final_failed_fraction; // |A*| / n
    int total_failed;              // |A*|
    int rounds_completed;          // Number of rounds completed
    std::vector<int> history;      // Cumulative failed counts; index 0 is post-seed total count
};

/**
 * @brief Thread-safe execution buffers to avoid repeated memory allocations.
 * Reused across realizations within a single thread loop.
 */
struct CascadeBuffers {
    std::vector<uint8_t> failed;               // Status array: 0 for solvent, 1 for failed
    std::vector<int> failed_neighbor_count;    // Track solvency counter for each node
    std::vector<int> solvent_nodes;            // Active list of solvent node indices
    std::vector<int> newly_failing_nodes;      // Temporary storage for round failure collection
    
    /**
     * @brief Resets buffers to initial solvent state for a system of size n.
     * Keeps internal capacities intact to prevent reallocation.
     */
    void reset(int n) {
        failed.assign(n, 0);
        failed_neighbor_count.assign(n, 0);
        solvent_nodes.resize(n);
        for (int i = 0; i < n; ++i) {
            solvent_nodes[i] = i;
        }
        newly_failing_nodes.clear();
    }
};

/**
 * @brief Simulates a two-channel cascade until completion.
 * 
 * Implements simultaneous rounds judging solvency thresholds and global fear field.
 * 
 * Weights Contract:
 * - If weights is empty, defaults to uniform weights of 1.0 / window_len.
 * - If weights is non-empty, its length must match window_len, all entries must be
 *   non-negative, and they must sum to 1.0 within 1e-9 tolerance.
 * - Validation is performed internally; throws std::invalid_argument on failure.
 * 
 * @param graph CSR Graph representation.
 * @param individual_fears Susceptibility fears drawn at t=0.
 * @param r Activated neighbor threshold for solvency channel.
 * @param seed_indices Root shock index list.
 * @param rng Thread-local mt19937_64 generator.
 * @param record_history If true, compiles round-by-round cumulative failure history.
 * @param window_len Memory window length for global fear.
 * @param weights Normalized weights vector (defaults to uniform if empty).
 * @param buffers Reusable CascadeBuffers array.
 * @return CascadeResult 
 */
CascadeResult run_cascade(
    const CSRGraph& graph,
    const std::vector<double>& individual_fears,
    int r,
    const std::vector<int>& seed_indices,
    std::mt19937_64& rng,
    bool record_history,
    int window_len,
    const std::vector<double>& weights,
    CascadeBuffers& buffers
);

#endif // TWOCASCADE_ENGINE_HPP
