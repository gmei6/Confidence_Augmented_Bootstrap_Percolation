#ifndef TWOCASCADE_GIRG_HPP
#define TWOCASCADE_GIRG_HPP

#include "graph.hpp"
#include <vector>
#include <cstdint>
#include <cmath>
#include <random>

/**
 * @brief A point on the unit torus [0,1) x [0,1).
 */
struct Point2D {
    double x;
    double y;
};

/**
 * @brief Injectable source of uniform draws on [0, 1).
 *
 * Both the GIRG kernel (direct, Variant A) and the bucket sampler (BKL,
 * Variant B) are written against this interface rather than std::mt19937_64
 * directly, so the SAME sampling code can be driven by a real generator in
 * production or by a fixed-value stub in tests. The stub is what makes the
 * "level-set identity" check possible: with every draw pinned to a constant
 * c, "does this sampler draw from the same distribution as the oracle"
 * becomes "do the two algorithms visit the exact same edge set at threshold
 * c" -- deterministic, and sensitive to off-by-one cell-boundary and
 * double-visited-cell-pair bugs that pure statistics need huge samples to
 * catch. Mirrors Python's `_ConstantRng` (tests/test_girg_fast_equivalence.py).
 */
struct IUniformSource {
    virtual double next() = 0;
    virtual ~IUniformSource() = default;
};

/**
 * @brief Real RNG-backed uniform source, wrapping a caller-owned mt19937_64.
 *
 * Does not own the generator: callers thread the same rng through graph
 * sampling and fear sampling within one trial (matching the existing
 * gnp/fear code's convention of a single per-trial rng), so this must not
 * take ownership or reseed it.
 */
class Mt19937UniformSource : public IUniformSource {
public:
    explicit Mt19937UniformSource(std::mt19937_64& rng) : rng_(rng) {}
    double next() override { return dist_(rng_); }

private:
    std::mt19937_64& rng_;
    std::uniform_real_distribution<double> dist_{0.0, 1.0};
};

/**
 * @brief Fixed-value uniform source: every draw returns the same constant c.
 *
 * Mirrors Python's `_ConstantRng`. c should be in (0, 1) for the geometric-skip
 * walk in the BKL sampler to terminate meaningfully; c <= 0.0 triggers the same
 * "u <= 0.0 -> stop" guard the real generator would need in the (measure-zero)
 * case of drawing exactly 0.0.
 */
class ConstantUniformSource : public IUniformSource {
public:
    explicit ConstantUniformSource(double c) : c_(c) {}
    double next() override { return c_; }

private:
    double c_;
};

/**
 * @brief Sample n points uniformly on the unit torus.
 * Draw order (x0, y0, x1, y1, ...) mirrors numpy's row-major fill of
 * rng.uniform(0, 1, (n, 2)); RNG-stream identity across languages is not a
 * goal (constitution §5.4), only the same marginal distribution.
 */
std::vector<Point2D> sample_torus_points(int n, std::mt19937_64& rng);

/**
 * @brief Sample n power-law weights w = w_min * u^(-1/(tau-1)), u ~ Uniform(0,1).
 * Same formula as twocascade.girg.sample_powerlaw_weights.
 */
std::vector<double> sample_powerlaw_weights(int n, double tau, double w_min, std::mt19937_64& rng);

/**
 * @brief Exact GIRG connection probability for one ordered pair on the torus.
 *
 * p_ij = min(1, (w_i * w_j / (n * d_ij^2))^alpha_g), with d the torus distance
 * (dx = min(|x_i-x_j|, 1-|x_i-x_j|), same for dy). Coincident points
 * (d_ij^2 == 0) return 0.0, matching the Python oracle's `continue` rather
 * than treating a collision as a saturating edge.
 *
 * Valid for ANY alpha_g: the clamp is applied AFTER the power, so this is the
 * literal definition rather than the (only-for-alpha_g>0 equivalent)
 * `min(1, base)^alpha_g`. That distinction matters because the two agree only
 * while x -> x^alpha_g is increasing; for alpha_g <= 0 the pre-clamp form both
 * over-reports (returns 1 where base > 1 should give base^alpha_g < 1) and
 * under-clamps (returns base^alpha_g > 1 where base < 1). The bucket
 * algorithm's upper-bound rejection scheme separately DOES require alpha_g > 0
 * for monotonicity and falls back to the direct kernel below otherwise (see
 * sample_girg_adjacency_bkl); the direct kernel itself is a plain enumeration
 * of the definition and is correct for every alpha_g.
 */
double girg_pair_probability(const Point2D& a, const Point2D& b, double wa, double wb,
                              int n, double alpha_g);

/**
 * @brief Variant A: direct O(n^2) GIRG adjacency kernel.
 *
 * Enumerates every ordered pair (i, j) with i < j exactly once, in row-major
 * order, evaluating girg_pair_probability and drawing one u.next() per pair --
 * same shape as twocascade.girg.sample_girg_adjacency_slow. This is the
 * exact-probability baseline: because every pair is visited independently and
 * exactly once, per-pair p_ij values are directly, deterministically
 * comparable against the Python oracle on shared points/weights (no RNG
 * involved in that comparison), and it is also the design template + oracle
 * for the BKL bucket algorithm's own correctness (Variant B falls back to
 * this for alpha_g <= 0 and for degenerate weight inputs).
 *
 * No dense n x n adjacency is ever materialized (constitution §I): output is
 * an adjacency list, built incrementally.
 */
std::vector<std::vector<int>> sample_girg_adjacency_direct(
    const std::vector<Point2D>& points,
    const std::vector<double>& weights,
    double alpha_g,
    IUniformSource& u);

/**
 * @brief Variant B: Bringmann-Keusch-Lengler weight-layer x geometry-cell
 * bucket sampler. Draws from exactly the same per-pair measure as
 * sample_girg_adjacency_direct, but does not evaluate every pair: cell pairs
 * whose minimum possible distance already bounds p_ij far below 1 are skipped
 * over geometrically rather than visited one at a time. See girg.cpp for the
 * full algorithm description (ported from twocascade.girg's b140e01 revision).
 *
 * Falls back to sample_girg_adjacency_direct for alpha_g <= 0 (the upper-bound
 * rejection scheme requires x -> x^alpha_g monotone increasing) and for
 * degenerate weights (w_min <= 0 or any non-finite weight, where the
 * weight-layer grouping floor(log2(w/w_min)) is undefined or unbounded).
 *
 * Deterministic given (points, weights, alpha_g, uniform-source stream) on ANY
 * conforming toolchain: every container whose traversal order feeds the RNG
 * (cell-pair candidates, weight-layer groups) is an ORDERED container. See the
 * determinism note on cell_layer_groups in girg.cpp.
 */
std::vector<std::vector<int>> sample_girg_adjacency_bkl(
    const std::vector<Point2D>& points,
    const std::vector<double>& weights,
    double alpha_g,
    IUniformSource& u);

#endif // TWOCASCADE_GIRG_HPP
