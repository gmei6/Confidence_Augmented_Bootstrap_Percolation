#include "twocascade/girg.hpp"

#include <algorithm>
#include <cmath>
#include <limits>

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
    if (base >= 1.0) {
        return 1.0;
    }
    return std::pow(base, alpha_g);
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

// G1 placeholder: the BKL bucket algorithm lands in G2. Until then, route
// through the direct kernel so main.cpp's --girg-variant bkl path is legal
// (if slow) rather than a link error, and so the eventual guards this
// function needs (alpha_g <= 0, degenerate weights) already have a single
// well-tested fallback target to delegate to.
std::vector<std::vector<int>> sample_girg_adjacency_bkl(
    const std::vector<Point2D>& points,
    const std::vector<double>& weights,
    double alpha_g,
    IUniformSource& u) {
    return sample_girg_adjacency_direct(points, weights, alpha_g, u);
}
