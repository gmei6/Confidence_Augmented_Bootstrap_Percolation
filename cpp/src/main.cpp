#include "twocascade/graph.hpp"
#include "twocascade/rng.hpp"
#include "twocascade/engine.hpp"
#include "twocascade/girg.hpp"

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

// --- GIRG cross-validation helpers (§5.4-adjacent, cpp-girg-plan G1/G5) -----
//
// These support a standalone "--girg-verify" mode used only by validation
// scripts (scripts/dump_girg_reference.py + tests/test_cpp_girg_validation.py),
// never by the runner's normal sweep path. They read points/weights dumped by
// the Python oracle so both languages sample/evaluate on IDENTICAL geometry
// and weights -- the only way to make the exact-probability check
// deterministic and the level-set identity check meaningful.

std::vector<Point2D> load_points_from_file(const std::string& filepath) {
    std::ifstream infile(filepath);
    if (!infile.is_open()) {
        throw std::runtime_error("Could not open points file: " + filepath);
    }
    std::vector<Point2D> points;
    double x, y;
    while (infile >> x >> y) {
        points.push_back({x, y});
    }
    return points;
}

std::vector<double> load_weights_from_file(const std::string& filepath) {
    std::ifstream infile(filepath);
    if (!infile.is_open()) {
        throw std::runtime_error("Could not open weights file: " + filepath);
    }
    std::vector<double> weights;
    double w;
    while (infile >> w) {
        weights.push_back(w);
    }
    return weights;
}

// Prints every pair's exact p_ij (i, j, p) at double precision, for the
// deterministic exact-probability parity check (implementation_plan.md's
// parity table, row 1). Deliberately O(n^2): the exact-probability check is
// meant to run on modest n where full enumeration is cheap.
void run_girg_probabilities_mode(const std::vector<Point2D>& points,
                                  const std::vector<double>& weights,
                                  double alpha_g,
                                  std::ostream& out) {
    int n = static_cast<int>(points.size());
    out << std::setprecision(17);
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double p = girg_pair_probability(points[i], points[j], weights[i], weights[j], n, alpha_g);
            out << i << " " << j << " " << p << "\n";
        }
    }
}

// Samples one GIRG adjacency (direct or bkl variant, real or constant-value
// RNG source) and prints its edge list (i j, i<j, sorted) -- for the
// sampled-graph-statistics and level-set-identity checks (parity table rows
// 2 and 3).
void run_girg_sample_mode(const std::vector<Point2D>& points,
                           const std::vector<double>& weights,
                           double alpha_g,
                           const std::string& variant,
                           const std::string& rng_source,
                           double constant_c,
                           uint64_t base_seed,
                           std::ostream& out) {
    std::mt19937_64 rng = make_seeded_rng(base_seed, 0);
    Mt19937UniformSource real_src(rng);
    ConstantUniformSource const_src(constant_c);
    IUniformSource& src = (rng_source == "constant")
        ? static_cast<IUniformSource&>(const_src)
        : static_cast<IUniformSource&>(real_src);

    std::vector<std::vector<int>> adj;
    if (variant == "direct") {
        adj = sample_girg_adjacency_direct(points, weights, alpha_g, src);
    } else if (variant == "bkl") {
        adj = sample_girg_adjacency_bkl(points, weights, alpha_g, src);
    } else {
        throw std::invalid_argument("Unknown --girg-variant: " + variant);
    }

    for (int i = 0; i < static_cast<int>(adj.size()); ++i) {
        for (int j : adj[i]) {
            if (j > i) {
                out << i << " " << j << "\n";
            }
        }
    }
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

    // GIRG cross-validation mode (cpp-girg-plan G1/G5) -- not used by the
    // normal sweep/simulation path, only by scripts/dump_girg_reference.py +
    // tests/test_cpp_girg_validation.py.
    std::string girg_verify = "";       // "probabilities" | "sample"
    std::string points_file = "";
    std::string weights_file = "";
    double alpha_g = 1.2;
    std::string girg_variant = "direct"; // "direct" | "bkl"
    std::string rng_source = "real";     // "real" | "constant"
    double constant_c = 0.0;

    // GIRG production graph source (cpp-girg-plan G4): --graph-type girg makes
    // the normal sweep/simulation loop below sample a GIRG internally, using
    // the BKL sampler (Variant B), instead of building/loading G(n,p).
    // Fear generation is unchanged (sample_individual_fears): at the gamma=0
    // scope this task targets, degree-dependent fear reduces exactly to the
    // existing global-kappa model (implementation_plan.md "Current state").
    std::string graph_type = "gnp"; // "gnp" | "girg"
    double tau = 2.5;
    double w_min = 1.0;

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
            else if (arg == "--girg-verify" && i + 1 < argc) girg_verify = argv[++i];
            else if (arg == "--points-file" && i + 1 < argc) points_file = argv[++i];
            else if (arg == "--weights-file" && i + 1 < argc) weights_file = argv[++i];
            else if (arg == "--alpha-g" && i + 1 < argc) alpha_g = std::stod(argv[++i]);
            else if (arg == "--girg-variant" && i + 1 < argc) girg_variant = argv[++i];
            else if (arg == "--rng-source" && i + 1 < argc) rng_source = argv[++i];
            else if (arg == "--constant-c" && i + 1 < argc) constant_c = std::stod(argv[++i]);
            else if (arg == "--graph-type" && i + 1 < argc) graph_type = argv[++i];
            else if (arg == "--tau" && i + 1 < argc) tau = std::stod(argv[++i]);
            else if (arg == "--w-min" && i + 1 < argc) w_min = std::stod(argv[++i]);
            else {
                std::cerr << "Unknown or incomplete argument: " << arg << "\n";
                return 1;
            }
        }

        // Mode C: GIRG cross-validation verify mode (short-circuits before the
        // n/p/r/mu validation below, which does not apply to this mode).
        if (!girg_verify.empty()) {
            if (points_file.empty() || weights_file.empty()) {
                std::cerr << "Error: --girg-verify requires --points-file and --weights-file.\n";
                return 1;
            }
            std::vector<Point2D> points = load_points_from_file(points_file);
            std::vector<double> girg_weights = load_weights_from_file(weights_file);
            if (points.size() != girg_weights.size()) {
                std::cerr << "Error: points-file has " << points.size() << " rows, "
                          << "weights-file has " << girg_weights.size() << " rows.\n";
                return 1;
            }

            std::ofstream out_stream;
            std::ostream* out = &std::cout;
            if (!output_file.empty()) {
                out_stream.open(output_file);
                if (!out_stream.is_open()) {
                    throw std::runtime_error("Could not open output file: " + output_file);
                }
                out = &out_stream;
            }

            if (girg_verify == "probabilities") {
                run_girg_probabilities_mode(points, girg_weights, alpha_g, *out);
            } else if (girg_verify == "sample") {
                run_girg_sample_mode(points, girg_weights, alpha_g, girg_variant,
                                      rng_source, constant_c, base_seed, *out);
            } else {
                std::cerr << "Error: unknown --girg-verify mode '" << girg_verify
                          << "' (expected 'probabilities' or 'sample').\n";
                return 1;
            }
            return 0;
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

        if (graph_type != "gnp" && graph_type != "girg") {
            std::cerr << "Error: --graph-type must be 'gnp' or 'girg', got '" << graph_type << "'.\n";
            return 1;
        }
        if (!graph_file.empty() && graph_type != "gnp") {
            std::cerr << "Error: --graph-file loads a static pre-generated graph; --graph-type "
                       << graph_type << " samples its own graph internally and cannot be combined "
                       << "with --graph-file.\n";
            return 1;
        }

        // Validate basic parameter limits
        if (graph_file.empty() && n <= 0) {
            std::cerr << "Error: --n must be positive when generating a random graph.\n";
            return 1;
        }
        if (graph_file.empty() && graph_type == "gnp" && (p < 0.0 || p > 1.0)) {
            std::cerr << "Error: --p must be in [0, 1] when generating a G(n,p) graph.\n";
            return 1;
        }
        if (graph_file.empty() && graph_type == "girg") {
            if (!(tau > 1.0)) {
                std::cerr << "Error: --tau must be > 1 for the GIRG power-law weight sampler.\n";
                return 1;
            }
            if (!(w_min > 0.0)) {
                std::cerr << "Error: --w-min must be positive.\n";
                return 1;
            }
            if (!(alpha_g > 0.0)) {
                // The BKL upper-bound rejection scheme requires x -> x^alpha_g
                // monotone increasing (RISKS.md #3); sample_girg_adjacency_bkl
                // itself falls back to the direct kernel for alpha_g <= 0, so
                // this is not a correctness gap, but production sweeps that
                // hit it silently lose the performance this port exists for
                // -- surface it instead.
                std::cerr << "Error: --alpha-g must be positive for --graph-type girg.\n";
                return 1;
            }
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
                    if (graph_type == "girg") {
                        std::vector<Point2D> girg_points = sample_torus_points(n, rng);
                        std::vector<double> girg_weights = sample_powerlaw_weights(n, tau, w_min, rng);
                        Mt19937UniformSource girg_src(rng);
                        generated_graph = convert_to_csr(
                            sample_girg_adjacency_bkl(girg_points, girg_weights, alpha_g, girg_src));
                    } else {
                        generated_graph = sample_gnp_adjacency(n, p, rng);
                    }
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
