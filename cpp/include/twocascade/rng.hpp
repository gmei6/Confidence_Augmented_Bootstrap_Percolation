#ifndef TWOCASCADE_RNG_HPP
#define TWOCASCADE_RNG_HPP

#include <vector>
#include <array>
#include <random>
#include <stdexcept>
#include <cstdint>
#include <algorithm>

/**
 * @brief SplitMix64 RNG finalizer.
 * Used for robust deterministic hashing of seeds to avoid initialization correlation.
 */
struct SplitMix64 {
    uint64_t state;
    
    explicit SplitMix64(uint64_t seed) : state(seed) {}
    
    uint64_t next() {
        state += 0x9e3779b97f4a7c15ULL;
        uint64_t z = state;
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
        z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        return z ^ (z >> 31);
    }
};

/**
 * @brief Thread-safe, order-independent RNG initialization.
 * 
 * Seeding Contract:
 * 1. Base seed is hashed first via SplitMix64 to obtain sm_base.next().
 * 2. This base hash is added to the trial_index and passed to a second SplitMix64 sm.
 * 3. sm generates 512 bits of high-entropy seeding material to fully populate std::seed_seq.
 * 4. This ensures that parallel trials are completely deterministic and uncorrelated, even
 *    if the runner allocates consecutive base seeds across sweep cells.
 * 
 * @param base_seed Root seed of the simulation cell.
 * @param trial_index Index of the current simulation trial.
 * @return std::mt19937_64 Seeded Mersenne Twister engine.
 */
inline std::mt19937_64 make_seeded_rng(uint64_t base_seed, uint64_t trial_index) {
    SplitMix64 sm_base(base_seed);
    SplitMix64 sm(sm_base.next() + trial_index);
    
    std::array<uint32_t, 16> seed_values;
    for (int i = 0; i < 8; ++i) {
        uint64_t val = sm.next();
        seed_values[2 * i] = static_cast<uint32_t>(val & 0xFFFFFFFFULL);
        seed_values[2 * i + 1] = static_cast<uint32_t>(val >> 32);
    }
    std::seed_seq seq(seed_values.begin(), seed_values.end());
    return std::mt19937_64(seq);
}

/**
 * @brief Samples node-level susceptibility parameters f_i ~ Beta(alpha, beta).
 * 
 * Guard details:
 * - If mean_fear is 0.0 or 1.0, short-circuits directly to point masses at 0.0 or 1.0.
 * - For mean_fear inside (0, 1), draws two Gamma(alpha, 1) and Gamma(beta, 1) values.
 * - If both Gamma draws underflow to 0.0 due to small shape parameters near boundaries
 *   (e.g., alpha, beta << 1), falls back to a Bernoulli trial yielding 1.0 with
 *   probability mean_fear (the correct asymptotic limit as concentration kappa -> 0).
 */
inline std::vector<double> sample_individual_fears(int n, double mean_fear, double concentration, std::mt19937_64& rng) {
    if (mean_fear < 0.0 || mean_fear > 1.0) {
        throw std::invalid_argument("mean_fear must be in [0, 1]");
    }
    if (concentration <= 0.0) {
        throw std::invalid_argument("concentration (kappa) must be positive");
    }
    
    std::vector<double> fears(n, 0.0);
    if (n == 0) return fears;
    
    if (mean_fear == 0.0) {
        return fears;
    }
    if (mean_fear == 1.0) {
        std::fill(fears.begin(), fears.end(), 1.0);
        return fears;
    }
    
    double alpha = mean_fear * concentration;
    double beta = (1.0 - mean_fear) * concentration;
    
    std::gamma_distribution<double> dist_a(alpha, 1.0);
    std::gamma_distribution<double> dist_b(beta, 1.0);
    std::uniform_real_distribution<double> u_dist(0.0, 1.0);
    
    for (int i = 0; i < n; ++i) {
        double x = dist_a(rng);
        double y = dist_b(rng);
        if (x + y == 0.0) {
            // Fallback to Bernoulli trial for small shape parameter underflow
            fears[i] = (u_dist(rng) < mean_fear) ? 1.0 : 0.0;
        } else {
            fears[i] = x / (x + y);
        }
    }
    return fears;
}

#endif // TWOCASCADE_RNG_HPP
