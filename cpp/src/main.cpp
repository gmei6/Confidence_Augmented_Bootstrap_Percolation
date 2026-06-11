#include "twocascade/graph.hpp"
#include "twocascade/rng.hpp"
#include "twocascade/engine.hpp"

#include <iostream>
#include <string>
#include <vector>
#include <stdexcept>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <iomanip>

#ifdef _OPENMP
#include <omp.h>
#endif

// Helper to parse comma-separated weights
std::vector<double> parse_weights(const std::string& str) {
    std::vector<double> w;
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, ',')) {
        w.push_back(std::stod(token));
    }
    return w;
}

// Helper to load seed indices from seed.txt
std::vector<int> load_seeds_from_file(const std::string& filepath) {
    std::ifstream infile(filepath);
    if (!infile.is_open()) {
        throw std::runtime_error("Could not open seed file: " + filepath);
    }
    std::vector<int> seeds;
    int idx;
    while (infile >> idx) {
        seeds.push_back(idx);
    }
    return seeds;
}

// Helper to choose random seed indices without replacement
std::vector<int> choose_random_seed(int n, int seed_size, std::mt19937_64& rng) {
    std::vector<int> indices(n);
    for (int i = 0; i < n; ++i) {
        indices[i] = i;
    }
    for (int i = 0; i < seed_size; ++i) {
        std::uniform_int_distribution<int> dist(i, n - 1);
        int swap_idx = dist(rng);
        std::swap(indices[i], indices[swap_idx]);
    }
    indices.resize(seed_size);
    std::sort(indices.begin(), indices.end());
    return indices;
}

struct TrialOutcome {
    double failed_fraction;
    int rounds_completed;
};

int main(int argc, char* argv[]) {
    // Parse arguments manually to avoid heavy CLI parsing library dependencies
    int n = 0;
    double p = -1.0;
    int r = 0;
    double mu = -1.0;
    double kappa = 50.0; // Sane default value to avoid validation failure if --kappa is omitted
    int seed_size = -1;
    int trials = 1;
    uint64_t base_seed = 0;
    int window_len = 1;
    std::vector<double> weights;
    std::string graph_file = "";
    std::string seed_file = "";
    bool dump_failed_set = false;
    std::string output_file = "";

    try {
        for (int i = 1; i < argc; ++i) {
            std::string arg = argv[i];
            if (arg == "--n" && i + 1 < argc) n = std::stoi(argv[++i]);
            else if (arg == "--p" && i + 1 < argc) p = std::stod(argv[++i]);
            else if (arg == "--r" && i + 1 < argc) r = std::stoi(argv[++i]);
            else if (arg == "--mu" && i + 1 < argc) mu = std::stod(argv[++i]);
            else if (arg == "--kappa" && i + 1 < argc) kappa = std::stod(argv[++i]);
            else if (arg == "--seed-size" && i + 1 < argc) seed_size = std::stoi(argv[++i]);
            else if (arg == "--trials" && i + 1 < argc) trials = std::stoi(argv[++i]);
            else if (arg == "--base-seed" && i + 1 < argc) base_seed = std::stoull(argv[++i]);
            else if (arg == "--window-len" && i + 1 < argc) window_len = std::stoi(argv[++i]);
            else if (arg == "--weights" && i + 1 < argc) weights = parse_weights(argv[++i]);
            else if (arg == "--graph-file" && i + 1 < argc) graph_file = argv[++i];
            else if (arg == "--seed-file" && i + 1 < argc) seed_file = argv[++i];
            else if (arg == "--dump-failed-set") dump_failed_set = true;
            else if (arg == "--output" && i + 1 < argc) output_file = argv[++i];
            else {
                std::cerr << "Unknown or incomplete argument: " << arg << "\n";
                return 1;
            }
        }

        // Precedence & validation rules
        if (!seed_file.empty() && seed_size != -1) {
            std::cerr << "Error: Both --seed-file and --seed-size provided. Only one must be used.\n";
            return 1;
        }

        if (dump_failed_set && trials > 1) {
            std::cerr << "Error: --dump-failed-set only supports exactly 1 trial.\n";
            return 1;
        }

        // Validate basic parameter limits
        if (graph_file.empty() && n <= 0) {
            std::cerr << "Error: --n must be positive when generating a random graph.\n";
            return 1;
        }
        if (graph_file.empty() && (p < 0.0 || p > 1.0)) {
            std::cerr << "Error: --p must be in [0, 1] when generating a random graph.\n";
            return 1;
        }
        if (r < 2) {
            std::cerr << "Error: --r must be >= 2.\n";
            return 1;
        }
        if (mu < 0.0 || mu > 1.0) {
            std::cerr << "Error: --mu must be in [0, 1].\n";
            return 1;
        }
        if (kappa <= 0.0) {
            std::cerr << "Error: --kappa must be positive.\n";
            return 1;
        }
        if (window_len < 1) {
            std::cerr << "Error: --window-len must be >= 1.\n";
            return 1;
        }
        if (trials < 1) {
            std::cerr << "Error: --trials must be >= 1.\n";
            return 1;
        }

        // Mode A: Dump Failed Set (Prong A cross-validation)
        if (dump_failed_set) {
            if (graph_file.empty() || seed_file.empty()) {
                std::cerr << "Error: --dump-failed-set requires both --graph-file and --seed-file.\n";
                return 1;
            }

            CSRGraph graph = load_graph_from_file(graph_file);
            std::vector<int> seeds = load_seeds_from_file(seed_file);
            
            // Seed a single deterministic RNG for validation
            std::mt19937_64 rng = make_seeded_rng(base_seed, 0);
            std::vector<double> fears = sample_individual_fears(graph.n, mu, kappa, rng);
            
            CascadeBuffers buffers;
            CascadeResult res = run_cascade(graph, fears, r, seeds, rng, false, window_len, weights, buffers);
            
            // Find sorted failed node list
            std::vector<int> failed_nodes;
            failed_nodes.reserve(graph.n);
            for (int i = 0; i < graph.n; ++i) {
                if (buffers.failed[i] != 0) {
                    failed_nodes.push_back(i);
                }
            }
            std::sort(failed_nodes.begin(), failed_nodes.end());
            
            for (size_t i = 0; i < failed_nodes.size(); ++i) {
                std::cout << failed_nodes[i] << (i + 1 == failed_nodes.size() ? "" : " ");
            }
            std::cout << "\n";
            return 0;
        }

        // Mode B: Standard/Sweep Simulation loop
        CSRGraph static_graph;
        std::vector<int> static_seeds;
        bool has_static_graph = !graph_file.empty();
        bool has_static_seeds = !seed_file.empty();

        if (has_static_graph) {
            static_graph = load_graph_from_file(graph_file);
            n = static_graph.n;
        }
        if (has_static_seeds) {
            static_seeds = load_seeds_from_file(seed_file);
        }

        // Validate seed size bounds when we are generating seeds randomly
        if (!has_static_seeds) {
            if (seed_size < 1 || seed_size > n) {
                std::cerr << "Error: --seed-size must satisfy 1 <= seed_size <= n (" << n << ").\n";
                return 1;
            }
        }

        int max_threads = 1;
#ifdef _OPENMP
        max_threads = omp_get_max_threads();
#endif
        std::vector<CascadeBuffers> thread_buffers(max_threads);
        std::vector<TrialOutcome> outcomes(trials);

        // Note: Exceptions thrown inside OMP parallel regions cannot propagate across
        // the parallel boundary and will call std::terminate. Parameters are pre-validated
        // outside this block to ensure safe execution.
#pragma omp parallel
        {
            int thread_id = 0;
#ifdef _OPENMP
            thread_id = omp_get_thread_num();
#endif
            CascadeBuffers& buffers = thread_buffers[thread_id];

#pragma omp for schedule(dynamic)
            for (int t = 0; t < trials; ++t) {
                std::mt19937_64 rng = make_seeded_rng(base_seed, t);
                
                // If graph is generated, build it per realization.
                // Binding run_graph as a const reference to avoid full CSRGraph copies.
                CSRGraph generated_graph;
                if (!has_static_graph) {
                    generated_graph = sample_gnp_adjacency(n, p, rng);
                }
                const CSRGraph& run_graph = has_static_graph ? static_graph : generated_graph;
                
                std::vector<int> run_seeds = has_static_seeds ? static_seeds : choose_random_seed(n, seed_size, rng);
                std::vector<double> fears = sample_individual_fears(run_graph.n, mu, kappa, rng);

                CascadeResult res = run_cascade(run_graph, fears, r, run_seeds, rng, false, window_len, weights, buffers);
                outcomes[t] = TrialOutcome{res.final_failed_fraction, res.rounds_completed};
            }
        }

        // Output results to stdout or file
        if (!output_file.empty()) {
            std::ofstream outfile(output_file);
            if (!outfile.is_open()) {
                throw std::runtime_error("Could not open output file: " + output_file);
            }
            outfile << std::fixed << std::setprecision(6);
            for (int i = 0; i < trials; ++i) {
                outfile << outcomes[i].failed_fraction << " " << outcomes[i].rounds_completed << "\n";
            }
        } else {
            std::cout << std::fixed << std::setprecision(6);
            for (int i = 0; i < trials; ++i) {
                std::cout << outcomes[i].failed_fraction << " " << outcomes[i].rounds_completed << "\n";
            }
        }

    } catch (const std::exception& e) {
        std::cerr << "Exception: " << e.what() << "\n";
        return 1;
    }

    return 0;
}
