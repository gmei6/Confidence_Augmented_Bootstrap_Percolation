#include <random>
#include <vector>

#include "twocascade/engine.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>

CascadeResult run_cascade(const CSRGraph &graph,
                          const std::vector<double> &individual_fears, int r,
                          const std::vector<int> &seed_indices,
                          std::mt19937_64 &rng, bool record_history,
                          int window_len, const std::vector<double> &weights,
                          CascadeBuffers &buffers) {
  // 1. Validation
  if (window_len < 1) {
    throw std::invalid_argument("window_len must be >= 1");
  }

  std::vector<double> weights_to_use = weights;
  if (weights_to_use.empty()) {
    weights_to_use.assign(window_len, 1.0 / window_len);
  } else {
    if (static_cast<int>(weights_to_use.size()) != window_len) {
      throw std::invalid_argument("Length of weights must match window_len");
    }
    double sum = 0.0;
    for (double w : weights_to_use) {
      if (w < 0.0) {
        throw std::invalid_argument("All weights must be non-negative");
      }
      sum += w;
    }
    if (std::abs(sum - 1.0) > 1e-9) {
      throw std::invalid_argument("Weights must sum to 1.0");
    }
  }

  int n = graph.n;
  if (n < 0) {
    throw std::invalid_argument("graph.n cannot be negative");
  }

  // 2. Buffer Reset and Shock Application
  buffers.reset(n);

  for (int idx : seed_indices) {
    if (idx >= 0 && idx < n) {
      buffers.failed[idx] = 1;
    } else {
      throw std::invalid_argument("Seed index out of graph bounds");
    }
  }

  for (int idx : seed_indices) {
    int start = graph.row_offsets[idx];
    int end = graph.row_offsets[idx + 1];
    for (int j = start; j < end; ++j) {
      int neighbor = graph.column_indices[j];
      buffers.failed_neighbor_count[neighbor] += 1;
    }
  }

  // Re-filter active solvent nodes list to exclude the failed seeds
  buffers.solvent_nodes.clear();
  for (int i = 0; i < n; ++i) {
    if (buffers.failed[i] == 0) {
      buffers.solvent_nodes.push_back(i);
    }
  }

  // Calculate total failed nodes post-shock (ignores duplicates in
  // seed_indices)
  int total_failed = 0;
  for (int i = 0; i < n; ++i) {
    if (buffers.failed[i] != 0) {
      total_failed++;
    }
  }

  int rounds_completed = 0;
  std::vector<int> history;
  if (record_history) {
    history.push_back(total_failed);
  }

  // Seed the rolling failures per round history
  int initial_failures = static_cast<int>(seed_indices.size());
  std::vector<int> failures_per_round;
  failures_per_round.reserve(window_len);
  failures_per_round.push_back(initial_failures);

  auto is_any_positive = [](const std::vector<int> &vec) {
    for (int val : vec) {
      if (val > 0)
        return true;
    }
    return false;
  };

  // 3. Simulation loop
  while (is_any_positive(failures_per_round)) {
    if (total_failed == n) {
      break;
    }

    // Calculate global fear (using truncated, un-renormalized weights for early
    // rounds)
    double global_fear = 0.0;
    for (int k = 1; k <= window_len; ++k) {
      if (k <= static_cast<int>(failures_per_round.size())) {
        global_fear += weights_to_use[k - 1] *
                       failures_per_round[failures_per_round.size() - k];
      }
    }
    global_fear /= (n == 0 ? 1.0 : static_cast<double>(n));

    // --- Evaluation Phase ---
    buffers.newly_failing_nodes.clear();
    std::uniform_real_distribution<double> u_dist(0.0, 1.0);

    for (int idx : buffers.solvent_nodes) {
      bool fails_by_solvency = buffers.failed_neighbor_count[idx] >= r;

      double fear_failure_probability = individual_fears[idx] * global_fear;
      bool fails_by_fear = (fear_failure_probability > 0.0 &&
                            u_dist(rng) < fear_failure_probability);

      if (fails_by_solvency || fails_by_fear) {
        buffers.newly_failing_nodes.push_back(idx);
      }
    }

    // --- Update Phase (simultaneous update) ---
    for (int idx : buffers.newly_failing_nodes) {
      buffers.failed[idx] = 1;
    }

    for (int idx : buffers.newly_failing_nodes) {
      int start = graph.row_offsets[idx];
      int end = graph.row_offsets[idx + 1];
      for (int j = start; j < end; ++j) {
        int neighbor = graph.column_indices[j];
        buffers.failed_neighbor_count[neighbor] += 1;
      }
    }

    int new_failures = static_cast<int>(buffers.newly_failing_nodes.size());

    // Append new failures to rolling history
    if (failures_per_round.size() == static_cast<size_t>(window_len)) {
      for (size_t k = 0; k < failures_per_round.size() - 1; ++k) {
        failures_per_round[k] = failures_per_round[k + 1];
      }
      failures_per_round.back() = new_failures;
    } else {
      failures_per_round.push_back(new_failures);
    }

    // Halting check: has the window cleared out?
    if (failures_per_round.size() == static_cast<size_t>(window_len)) {
      bool all_zero = true;
      for (int val : failures_per_round) {
        if (val != 0) {
          all_zero = false;
          break;
        }
      }
      if (all_zero) {
        break;
      }
    }

    total_failed += new_failures;
    rounds_completed += 1;
    if (record_history) {
      history.push_back(total_failed);
    }

    // Filter out the failed nodes from the solvent list
    buffers.solvent_nodes.erase(
        std::remove_if(buffers.solvent_nodes.begin(),
                       buffers.solvent_nodes.end(),
                       [&buffers](int i) { return buffers.failed[i] != 0; }),
        buffers.solvent_nodes.end());
  }

  double final_failed_fraction =
      (n == 0) ? 0.0 : (static_cast<double>(total_failed) / n);

  return CascadeResult{final_failed_fraction, total_failed, rounds_completed,
                       history};
}