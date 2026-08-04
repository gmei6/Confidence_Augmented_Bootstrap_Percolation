#include "twocascade/girg.hpp"

#include <algorithm>
#include <cmath>
#include <limits>
#include <map>
#include <set>
#include <unordered_map>
#include <utility>

std::vector<Point2D> sample_torus_points(int n, std::mt19937_64& rng) {
    std::vector<Point2D> points(static_cast<size_t>(std::max(n, 0)));
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    for (int i = 0; i < n; ++i) {
        points[i].x = dist(rng);
        points[i].y = dist(rng);
    }
    return points;
}

std::vector<double> sample_powerlaw_weights(int n, double tau, double w_min, std::mt19937_64& rng) {
    std::vector<double> weights(static_cast<size_t>(std::max(n, 0)));
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    double exponent = -1.0 / (tau - 1.0);
    for (int i = 0; i < n; ++i) {
        double u = dist(rng);
        weights[i] = w_min * std::pow(u, exponent);
    }
    return weights;
}

double girg_pair_probability(const Point2D& a, const Point2D& b, double wa, double wb,
                              int n, double alpha_g) {
    double dx = std::fabs(a.x - b.x);
    dx = std::min(dx, 1.0 - dx);
    double dy = std::fabs(a.y - b.y);
    dy = std::min(dy, 1.0 - dy);
    double d2 = dx * dx + dy * dy;
    if (d2 == 0.0) {
        return 0.0; // coincident points are skipped, not a saturating edge (matches the Python `continue`).
    }
    double base = (wa * wb) / (static_cast<double>(n) * d2);
    // The model is min(1, base^alpha_g) -- the clamp goes AFTER the power, not
    // before it. For alpha_g > 0 the two orders coincide (x -> x^alpha_g is
    // increasing, so it maps [0,1] onto [0,1] and fixes 1), which is why the
    // earlier `if (base >= 1) return 1; return pow(base, alpha_g);` form passed
    // every production-regime test. It is WRONG for alpha_g <= 0, where the
    // power is decreasing: base < 1 then gives base^alpha_g > 1 (must clamp to
    // 1, the old form returned the un-clamped >1 value) and base > 1 gives
    // base^alpha_g < 1 (must NOT be forced to 1, the old form returned 1).
    // Production rejects alpha_g <= 0 at the CLI (main.cpp), but the direct
    // kernel is documented as the exact enumeration of the definition for ALL
    // alpha_g, and both fallback paths in sample_girg_adjacency_bkl route
    // alpha_g <= 0 here -- so the definition has to actually hold. Overflow is
    // benign: pow -> +inf clamps to 1.0.
    return std::min(1.0, std::pow(base, alpha_g));
}

std::vector<std::vector<int>> sample_girg_adjacency_direct(
    const std::vector<Point2D>& points,
    const std::vector<double>& weights,
    double alpha_g,
    IUniformSource& u) {
    int n = static_cast<int>(points.size());
    std::vector<std::vector<int>> adj(n);
    if (n < 2) {
        return adj;
    }

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double p = girg_pair_probability(points[i], points[j], weights[i], weights[j], n, alpha_g);
            if (u.next() < p) {
                adj[i].push_back(j);
                adj[j].push_back(i);
            }
        }
    }

    for (auto& nbrs : adj) {
        std::sort(nbrs.begin(), nbrs.end());
    }
    return adj;
}

// --- Variant B: BKL weight-layer x geometry-cell bucket sampler -------------
//
// Ported from twocascade.girg's b140e01 revision (the Python implementation,
// superseded there only because numpy's vectorized O(n^2) constant beat the
// Python-INTERPRETER constant of this algorithm's per-cell bookkeeping at
// n=10000 -- not because the algorithm is asymptotically worse). C++ removes
// that interpreter overhead almost entirely, which is the whole point of
// porting this rather than just the direct kernel.
//
// The model is p_ij = min(1, (w_i w_j / (n d_ij^2))^alpha), strictly positive
// at every distance, so a spatial index that only looks at nearby cells would
// sample a DIFFERENT model (losing the long-range tail). Nothing here
// truncates: every pair still gets evaluated at its exact p_ij, either
// directly (deepest level, or once an upper bound saturates to 1) or via
// geometric-skip rejection against an upper bound p_bar that only shrinks the
// number of pairs VISITED, never which distribution is sampled.
//
// Levels l = 2..L carry grids of 2^l cells per side. A pair of points is
// handled at the coarsest level at which their cells are non-touching
// (Chebyshev cell distance >= 2, torus-wrapped); pairs still touching at the
// deepest level L are enumerated directly. Cell distance is monotone in l (a
// child pair's distance is at least 2*parent - 1), so the set of levels at
// which two cells touch is a prefix {2..l*-1} and l* is unique -- the two
// cases below (non-touching-at-some-level, still-touching-at-L) are disjoint
// and cover every pair exactly once.

namespace {

struct WeightGroup {
    std::vector<int> indices;
    double max_weight = 0.0;
};

int cell_coord(double v, int m) {
    int c = static_cast<int>(v * m);
    if (c >= m) c = m - 1;
    if (c < 0) c = 0;
    return c;
}

// Minimum distance along one axis between cell index a and cell index b, on
// an m-cell torus. Cells are half-open intervals of width 1/m: two cells at
// wrapped index distance k are separated by at least (k-1)/m, zero when they
// touch (k<=1). The wrap is what makes cells on opposite edges of the unit
// square neighbours; getting it wrong here shows up as a deficit of exactly
// those long-range edges (RISKS.md #2).
double torus_cell_gap(int a, int b, int m) {
    int d = std::abs(a - b);
    d = std::min(d, m - d);
    return d > 1 ? static_cast<double>(d - 1) / m : 0.0;
}

int torus_cheb(int a, int b, int m) {
    int d = std::abs(a - b);
    return std::min(d, m - d);
}

// True iff (bx,by) < (ax,ay) in lexicographic (tuple) order -- matches
// Python's direct tuple comparison used to visit each unordered cell pair
// exactly once.
bool cell_lex_less(int bx, int by, int ax, int ay) {
    return bx < ax || (bx == ax && by < ay);
}

// CSR-style bucket layout for one level's m x m grid: point_ids sorted by
// cell id, offsets[c]..offsets[c+1) gives the span for cell c = cy*m + cx.
// Flat arrays, no per-cell heap allocation or hash lookup for the point
// buckets themselves (§5.5 CSR-for-cache-locality guidance; RISKS.md #6 flags
// unordered_map specifically as a thing to avoid on the hot path).
struct LevelBuckets {
    int m = 0;
    std::vector<int> offsets;   // size m*m + 1
    std::vector<int> point_ids; // size n, sorted by cell id
};

LevelBuckets build_level_buckets(int n, int m, const std::vector<int>& cx, const std::vector<int>& cy) {
    LevelBuckets lvl;
    lvl.m = m;
    size_t num_cells = static_cast<size_t>(m) * static_cast<size_t>(m);
    lvl.offsets.assign(num_cells + 1, 0);
    std::vector<int> cell_id(n);
    for (int i = 0; i < n; ++i) {
        int cid = cy[i] * m + cx[i];
        cell_id[i] = cid;
        lvl.offsets[static_cast<size_t>(cid) + 1] += 1;
    }
    for (size_t c = 0; c < num_cells; ++c) {
        lvl.offsets[c + 1] += lvl.offsets[c];
    }
    lvl.point_ids.resize(n);
    std::vector<int> cursor(lvl.offsets.begin(), lvl.offsets.end() - 1);
    for (int i = 0; i < n; ++i) {
        int cid = cell_id[i];
        lvl.point_ids[static_cast<size_t>(cursor[cid])] = i;
        cursor[cid] += 1;
    }
    return lvl;
}

std::pair<const int*, const int*> cell_span_by_id(const LevelBuckets& lvl, int cid) {
    const int* begin = lvl.point_ids.data() + lvl.offsets[cid];
    const int* end = lvl.point_ids.data() + lvl.offsets[cid + 1];
    return {begin, end};
}

// Split one cell's point indices into weight layers. Layer t holds
// w in [2^t w_min, 2^(t+1) w_min); the bound returned per group is the
// group's ACTUAL max weight (tighter than the layer ceiling, still a valid
// upper bound). Grouping by weight layer exists so one heavy vertex cannot
// inflate the acceptance bound p_bar for its whole cell (RISKS.md-adjacent:
// this is what test_degree_distribution_matches_reference in the Python
// suite exists to catch if dropped).
//
// DETERMINISM: the container is std::map, NOT std::unordered_map, and that is
// load-bearing rather than stylistic. The (ga, gb) loop in the sampler draws
// from `u` in group order, so group order fixes the RNG consumption order and
// therefore the sampled graph. unordered_map's iteration order is unspecified
// and varies with the standard-library implementation (and, in principle, with
// its hash seed), which would make the same (config, seed) produce a DIFFERENT
// graph under a different toolchain -- a direct violation of the constitution's
// "every run is deterministic given (config, seed)". Ordering by the integer
// layer key makes the traversal implementation-independent. Cells hold ~4
// points at the deepest level, so the red-black tree costs nothing measurable
// against the pair work it feeds.
std::vector<WeightGroup> cell_layer_groups(const int* begin, const int* end,
                                            const std::vector<double>& w, double w_min) {
    std::map<int, WeightGroup> groups;
    for (const int* it = begin; it != end; ++it) {
        int i = *it;
        double wi = w[i];
        int t = (wi > w_min) ? static_cast<int>(std::floor(std::log2(wi / w_min))) : 0;
        auto& g = groups[t];
        g.indices.push_back(i);
        if (wi > g.max_weight) g.max_weight = wi;
    }
    std::vector<WeightGroup> out;
    out.reserve(groups.size());
    for (auto& kv : groups) { // ascending layer key: deterministic across toolchains
        out.push_back(std::move(kv.second));
    }
    return out;
}

} // namespace

std::vector<std::vector<int>> sample_girg_adjacency_bkl(
    const std::vector<Point2D>& points,
    const std::vector<double>& weights,
    double alpha_g,
    IUniformSource& u) {
    int n = static_cast<int>(points.size());
    std::vector<std::vector<int>> adj(n);
    if (n < 2) {
        return adj;
    }

    // The upper-bound rejection scheme relies on x -> x^alpha_g being
    // increasing, which only holds for alpha_g > 0 (RISKS.md #3). No
    // production caller passes alpha_g <= 0 today; fall back to the exact
    // enumeration rather than be silently wrong if one ever does.
    if (alpha_g <= 0.0) {
        return sample_girg_adjacency_direct(points, weights, alpha_g, u);
    }

    double w_min = std::numeric_limits<double>::infinity();
    bool all_finite = true;
    for (double w : weights) {
        if (!std::isfinite(w)) {
            all_finite = false;
            break;
        }
        w_min = std::min(w_min, w);
    }
    // w_min <= 0 or a non-finite weight breaks the weight-layer key
    // floor(log2(w/w_min)) (undefined or unbounded) -- RISKS.md #4. Fall back
    // rather than mishandle the (currently out-of-regime) extreme case.
    if (!all_finite || !(w_min > 0.0)) {
        return sample_girg_adjacency_direct(points, weights, alpha_g, u);
    }

    // Aim for ~4 points per cell at the deepest level so direct enumeration
    // there stays linear in n. L >= 2: a 2x2 grid (level 1) has no
    // non-touching cells at all, so the recursion could not even start.
    int L = std::max(2, std::min(8, static_cast<int>(std::ceil(
        0.5 * std::log2(std::max(n / 4.0, 4.0))))));

    const double n_float = static_cast<double>(n);
    auto exact_p = [&](int i, int j) {
        return girg_pair_probability(points[i], points[j], weights[i], weights[j], n, alpha_g);
    };
    auto connect = [&](int i, int j) {
        adj[i].push_back(j);
        adj[j].push_back(i);
    };

    // --- non-touching cell pairs, level by level ----------------------------
    for (int lvl = 2; lvl <= L; ++lvl) {
        int m = 1 << lvl;
        int parent_m = m >> 1;

        std::vector<int> cx(n), cy(n);
        for (int i = 0; i < n; ++i) {
            cx[i] = cell_coord(points[i].x, m);
            cy[i] = cell_coord(points[i].y, m);
        }
        LevelBuckets buckets = build_level_buckets(n, m, cx, cy);

        // Per-level cache of weight-layer groups, keyed by cell id. Reset
        // every level (matches Python's group_cache = {} inside the loop).
        // unordered_map is safe HERE (unlike inside cell_layer_groups) because
        // this map is only ever point-queried by cell id -- it is never
        // iterated, so its unspecified traversal order cannot reach the RNG.
        std::unordered_map<int, std::vector<WeightGroup>> group_cache;
        auto groups_of = [&](int cell_id) -> const std::vector<WeightGroup>& {
            auto it = group_cache.find(cell_id);
            if (it != group_cache.end()) {
                return it->second;
            }
            auto span = cell_span_by_id(buckets, cell_id);
            auto groups = cell_layer_groups(span.first, span.second, weights, w_min);
            auto ins = group_cache.emplace(cell_id, std::move(groups));
            return ins.first->second;
        };

        for (int ax = 0; ax < m; ++ax) {
            for (int ay = 0; ay < m; ++ay) {
                int a_cid = ay * m + ax;
                if (buckets.offsets[a_cid] == buckets.offsets[a_cid + 1]) {
                    continue; // empty cell
                }

                int pax = ax >> 1;
                int pay = ay >> 1;

                // Candidates are children of the parent's 3x3 neighbourhood:
                // any cell outside that neighbourhood is handled at a coarser
                // level. A SET, not a nested loop straight into the pair
                // body: at lvl==2 the parent grid is 2x2, so (pax-1) mod 2
                // and (pax+1) mod 2 name the SAME parent, and a naive 3x3
                // sweep would visit -- and independently sample -- each
                // resulting candidate cell twice, roughly doubling long-range
                // edge probability for those pairs while leaving short-range
                // ones alone. That is exactly the class of bug this whole
                // port exists to avoid (RISKS.md #1 / b140e01 inline
                // comment); deduplicating through a set is the fix, not an
                // optimization.
                std::set<std::pair<int, int>> candidates;
                for (int dpx = -1; dpx <= 1; ++dpx) {
                    for (int dpy = -1; dpy <= 1; ++dpy) {
                        int qx = ((pax + dpx) % parent_m + parent_m) % parent_m;
                        int qy = ((pay + dpy) % parent_m + parent_m) % parent_m;
                        for (int bxc : {2 * qx, 2 * qx + 1}) {
                            for (int byc : {2 * qy, 2 * qy + 1}) {
                                candidates.insert({bxc, byc});
                            }
                        }
                    }
                }

                for (const auto& cand : candidates) {
                    int bx = cand.first;
                    int by = cand.second;
                    // Unordered pair, visit once: require (ax,ay) < (bx,by).
                    if (!cell_lex_less(ax, ay, bx, by)) {
                        continue;
                    }
                    // Cheb < 2 means still touching at this level: handled at
                    // a finer level, or (if lvl==L) by the deepest-level
                    // touching pass below. Cell distance is monotone in
                    // level, so this partition is a disjoint prefix -- every
                    // pair is handled exactly once across the whole function.
                    if (std::max(torus_cheb(ax, bx, m), torus_cheb(ay, by, m)) < 2) {
                        continue;
                    }
                    int b_cid = by * m + bx;
                    if (buckets.offsets[b_cid] == buckets.offsets[b_cid + 1]) {
                        continue; // empty
                    }

                    double gx = torus_cell_gap(ax, bx, m);
                    double gy = torus_cell_gap(ay, by, m);
                    double d_min_sq = gx * gx + gy * gy;
                    if (d_min_sq <= 0.0) {
                        continue; // unreachable: cheb>=2 forces a strictly positive gap
                    }

                    const auto& a_groups = groups_of(a_cid);
                    const auto& b_groups = groups_of(b_cid);
                    for (const auto& ga : a_groups) {
                        for (const auto& gb : b_groups) {
                            double base = (ga.max_weight * gb.max_weight) / (n_float * d_min_sq);
                            // Same min-after-power form as girg_pair_probability
                            // (identical here, since this branch only runs for
                            // alpha_g > 0 -- kept in one shape so the two copies
                            // of the formula cannot drift apart again).
                            double p_bar = std::min(1.0, std::pow(base, alpha_g));
                            long long na = static_cast<long long>(ga.indices.size());
                            long long nb = static_cast<long long>(gb.indices.size());

                            if (p_bar >= 1.0) {
                                for (int i : ga.indices) {
                                    for (int j : gb.indices) {
                                        if (u.next() < exact_p(i, j)) {
                                            connect(i, j);
                                        }
                                    }
                                }
                                continue;
                            }
                            if (p_bar <= 0.0) {
                                continue;
                            }

                            long long total = na * nb;
                            const double total_f = static_cast<double>(total);
                            double log1m = std::log1p(-p_bar);
                            long long pos = -1;
                            while (true) {
                                double uu = u.next();
                                if (uu <= 0.0) {
                                    break; // domain guard on log(0); vanishingly rare with a real RNG
                                }
                                // The geometric skip is unbounded above: for a
                                // tiny p_bar, log1m ~ -p_bar, so the quotient can
                                // exceed the range of long long and the cast
                                // would be UNDEFINED behaviour (not merely a
                                // wrong number) -- and NaN, if log1m were ever
                                // 0, would be UB too. Test the double BEFORE
                                // narrowing. This is exactly equivalent to the
                                // unclamped arithmetic: pos >= -1 always, so a
                                // skip of total or more can only land at or past
                                // `total`, which is the loop's own stop
                                // condition. The negated comparison also makes
                                // a NaN skip fall out through this branch.
                                double skip = std::floor(std::log(uu) / log1m);
                                if (!(skip < total_f)) {
                                    break;
                                }
                                pos += 1 + static_cast<long long>(skip);
                                if (pos >= total) {
                                    break;
                                }
                                int i = ga.indices[static_cast<size_t>(pos / nb)];
                                int j = gb.indices[static_cast<size_t>(pos % nb)];
                                if (u.next() < exact_p(i, j) / p_bar) {
                                    connect(i, j);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // --- touching cells at the deepest level, enumerated exactly -----------
    {
        int m = 1 << L;
        std::vector<int> cx(n), cy(n);
        for (int i = 0; i < n; ++i) {
            cx[i] = cell_coord(points[i].x, m);
            cy[i] = cell_coord(points[i].y, m);
        }
        LevelBuckets buckets = build_level_buckets(n, m, cx, cy);

        for (int ax = 0; ax < m; ++ax) {
            for (int ay = 0; ay < m; ++ay) {
                int a_cid = ay * m + ax;
                if (buckets.offsets[a_cid] == buckets.offsets[a_cid + 1]) {
                    continue;
                }
                auto a_span = cell_span_by_id(buckets, a_cid);

                for (int dx = -1; dx <= 1; ++dx) {
                    for (int dy = -1; dy <= 1; ++dy) {
                        int bx = ((ax + dx) % m + m) % m;
                        int by = ((ay + dy) % m + m) % m;
                        if (cell_lex_less(bx, by, ax, ay)) {
                            continue; // already visited from the other side
                        }
                        if (bx == ax && by == ay) {
                            for (const int* p1 = a_span.first; p1 != a_span.second; ++p1) {
                                for (const int* p2 = p1 + 1; p2 != a_span.second; ++p2) {
                                    if (u.next() < exact_p(*p1, *p2)) {
                                        connect(*p1, *p2);
                                    }
                                }
                            }
                            continue;
                        }
                        int b_cid = by * m + bx;
                        if (buckets.offsets[b_cid] == buckets.offsets[b_cid + 1]) {
                            continue;
                        }
                        auto b_span = cell_span_by_id(buckets, b_cid);
                        for (const int* p1 = a_span.first; p1 != a_span.second; ++p1) {
                            for (const int* p2 = b_span.first; p2 != b_span.second; ++p2) {
                                if (u.next() < exact_p(*p1, *p2)) {
                                    connect(*p1, *p2);
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    for (auto& nbrs : adj) {
        std::sort(nbrs.begin(), nbrs.end());
    }
    return adj;
}
