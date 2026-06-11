#ifndef TWOCASCADE_GRAPH_HPP
#define TWOCASCADE_GRAPH_HPP

#include <vector>
#include <random>
#include <cmath>
#include <string>
#include <fstream>
#include <stdexcept>
#include <limits>
#include <algorithm>

struct CSRGraph {
    int n;
    std::vector<int> row_offsets;
    std::vector<int> column_indices;
};

inline CSRGraph convert_to_csr(const std::vector<std::vector<int>>& adj) {
    CSRGraph graph;
    graph.n = static_cast<int>(adj.size());
    graph.row_offsets.resize(graph.n + 1, 0);
    
    int total_edges = 0;
    for (int i = 0; i < graph.n; ++i) {
        total_edges += static_cast<int>(adj[i].size());
    }
    graph.column_indices.reserve(total_edges);
    
    for (int i = 0; i < graph.n; ++i) {
        graph.row_offsets[i] = static_cast<int>(graph.column_indices.size());
        for (int neighbor : adj[i]) {
            graph.column_indices.push_back(neighbor);
        }
    }
    graph.row_offsets[graph.n] = static_cast<int>(graph.column_indices.size());
    return graph;
}

inline CSRGraph sample_gnp_adjacency(int n, double p, std::mt19937_64& rng) {
    if (n < 0) {
        throw std::invalid_argument("n must be non-negative");
    }
    if (p < 0.0 || p > 1.0) {
        throw std::invalid_argument("p must be in [0, 1]");
    }
    
    std::vector<std::vector<int>> adj(n);
    if (n == 0 || p == 0.0) {
        return convert_to_csr(adj);
    }
    
    if (p == 1.0) {
        for (int v = 0; v < n; ++v) {
            adj[v].reserve(n - 1);
            for (int w = 0; w < n; ++w) {
                if (v != w) {
                    adj[v].push_back(w);
                }
            }
        }
        return convert_to_csr(adj);
    }
    
    double log_one_minus_p = std::log(1.0 - p);
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    
    int row = 1;
    int column = -1;
    
    while (row < n) {
        double u = dist(rng);
        double one_minus_u = 1.0 - u;
        if (one_minus_u <= 0.0) {
            one_minus_u = std::numeric_limits<double>::epsilon();
        }
        
        double jump_double = std::log(one_minus_u) / log_one_minus_p;
        // Avoid undefined behavior casting double to int or overflowing column + 1 + jump
        double max_jump = std::min(static_cast<double>(n) * n,
                                   static_cast<double>(std::numeric_limits<int>::max() - n - 2));
        if (jump_double > max_jump) {
            jump_double = max_jump;
        }
        
        int geometric_jump = static_cast<int>(jump_double);
        column = column + 1 + geometric_jump;
        
        while (column >= row && row < n) {
            column = column - row;
            row += 1;
        }
        
        if (row < n) {
            adj[row].push_back(column);
            adj[column].push_back(row);
        }
    }
    
    // Sort neighbors for a canonical, deterministic CSR layout (reference.py does not sort; engine is order-independent)
    for (int i = 0; i < n; ++i) {
        std::sort(adj[i].begin(), adj[i].end());
    }
    
    return convert_to_csr(adj);
}

inline CSRGraph load_graph_from_file(const std::string& filepath) {
    std::ifstream infile(filepath);
    if (!infile.is_open()) {
        throw std::runtime_error("Could not open graph file: " + filepath);
    }
    
    int n = 0;
    int m = 0;
    if (!(infile >> n >> m)) {
        throw std::runtime_error("Failed to read header from graph file");
    }
    if (n < 0 || m < 0) {
        throw std::runtime_error("Negative size or edge count in graph file header");
    }
    
    std::vector<std::vector<int>> adj(n);
    int u = 0;
    int v = 0;
    for (int i = 0; i < m; ++i) {
        if (!(infile >> u >> v)) {
            throw std::runtime_error("Failed to read edge " + std::to_string(i) + " from graph file");
        }
        if (u < 0 || u >= n || v < 0 || v >= n) {
            throw std::runtime_error("Invalid node indices in edge: " + std::to_string(u) + " " + std::to_string(v));
        }
        if (u == v) {
            throw std::runtime_error("Self-loop detected in edge: " + std::to_string(u) + " " + std::to_string(v));
        }
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    
    // Sort neighbors for a canonical, deterministic CSR layout (reference.py does not sort; engine is order-independent)
    for (int i = 0; i < n; ++i) {
        std::sort(adj[i].begin(), adj[i].end());
    }
    
    return convert_to_csr(adj);
}

#endif // TWOCASCADE_GRAPH_HPP
