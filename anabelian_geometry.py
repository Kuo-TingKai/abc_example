"""
Anabelian Geometry - Belyi Maps and Monodromy Implementation

This module implements the simplest computable example of Anabelian Geometry
using Belyi maps and monodromy groups for the hyperbolic curve P^1 \\ {0,1,∞}.
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, simplify, latex, factor
from itertools import permutations, product
import networkx as nx


class BelyiMap:
    """
    Belyi map implementation for Anabelian Geometry.
    
    A Belyi map is a rational function that ramifies only at 0, 1, and ∞.
    It corresponds to finite covers and permutation group data through monodromy.
    """
    
    def __init__(self, degree=2):
        """
        Initialize Belyi map of given degree.
        
        Args:
            degree: Degree of the Belyi map
        """
        self.degree = degree
        self.z = symbols('z')
    
    def simple_belyi_map(self):
        """
        Simple Belyi map: f(z) = z^2
        
        Returns:
            sympy expression: The Belyi map
        """
        return self.z**2
    
    def ramification_data(self, f):
        """
        Compute ramification data for a Belyi map at 0, 1, ∞.
        
        Args:
            f: Belyi map as sympy expression
            
        Returns:
            dict: Ramification data at each point
        """
        from sympy import diff, solve, limit
        
        # Compute derivative
        f_prime = diff(f, self.z)
        
        # Find critical points (where f' = 0)
        critical_points = solve(f_prime, self.z)
        
        ramification = {}
        
        # Check ramification at 0
        f_at_0 = f.subs(self.z, 0)
        if f_at_0 == 0:
            # Find multiplicity of zero at z=0
            multiplicity = 0
            temp_f = f
            while temp_f.subs(self.z, 0) == 0:
                multiplicity += 1
                temp_f = temp_f / self.z
            ramification[0] = multiplicity
        
        # Check ramification at 1
        f_at_1 = f.subs(self.z, 1)
        if f_at_1 == 1:
            # Find multiplicity of zero at z=1 for f(z) - 1
            multiplicity = 0
            temp_f = f - 1
            while temp_f.subs(self.z, 1) == 0:
                multiplicity += 1
                temp_f = temp_f / (self.z - 1)
            ramification[1] = multiplicity
        
        # Check ramification at ∞
        # Transform z -> 1/w and check behavior at w=0
        w = symbols('w')
        f_inf = f.subs(self.z, 1/w)
        if limit(f_inf, w, 0) == float('inf'):
            ramification[float('inf')] = self.degree
        
        return ramification
    
    def monodromy_group(self, degree=3):
        """
        Generate monodromy group data for degree 3-4 permutation triples.
        
        Args:
            degree: Degree of the cover
            
        Returns:
            list: List of valid permutation triples (σ₀, σ₁, σ∞)
        """
        # Generate all permutation triples of given degree
        S_n = list(permutations(range(1, degree + 1)))
        valid_triples = []
        
        for sigma_0 in S_n:
            for sigma_1 in S_n:
                for sigma_inf in S_n:
                    # Check if σ₀ σ₁ σ∞ = 1 (identity)
                    composition = self.compose_permutations(
                        self.compose_permutations(sigma_0, sigma_1), sigma_inf
                    )
                    if composition == tuple(range(1, degree + 1)):
                        valid_triples.append((sigma_0, sigma_1, sigma_inf))
        
        return valid_triples
    
    def compose_permutations(self, sigma1, sigma2):
        """
        Compose two permutations: σ₁ ∘ σ₂
        
        Args:
            sigma1, sigma2: Permutations as tuples
            
        Returns:
            tuple: Composed permutation
        """
        if len(sigma1) != len(sigma2):
            raise ValueError("Permutations must have same degree")
        
        result = []
        for i in range(len(sigma1)):
            # σ₁(σ₂(i+1)) = σ₁(sigma2[i])
            result.append(sigma1[sigma2[i] - 1])
        
        return tuple(result)
    
    def permutation_cycles(self, sigma):
        """
        Find cycles in a permutation.
        
        Args:
            sigma: Permutation as tuple
            
        Returns:
            list: List of cycles
        """
        visited = set()
        cycles = []
        
        for i in range(1, len(sigma) + 1):
            if i not in visited:
                cycle = []
                j = i
                while j not in visited:
                    visited.add(j)
                    cycle.append(j)
                    j = sigma[j - 1]
                if len(cycle) > 1:
                    cycles.append(cycle)
        
        return cycles
    
    def dessin_denfant(self, sigma_0, sigma_1, sigma_inf):
        """
        Generate dessin d'enfant (child's drawing) from monodromy data.
        
        Args:
            sigma_0, sigma_1, sigma_inf: Monodromy permutations
            
        Returns:
            networkx.Graph: Dessin d'enfant graph
        """
        G = nx.Graph()
        
        # Add vertices (sheets of the cover)
        degree = len(sigma_0)
        for i in range(1, degree + 1):
            G.add_node(i, color='white')
        
        # Add edges based on σ₁ (black vertices)
        for i in range(1, degree + 1):
            j = sigma_1[i - 1]
            G.add_edge(i, j, color='black')
        
        return G
    
    def plot_dessin(self, G, title="Dessin d'enfant", save_path=None):
        """
        Plot dessin d'enfant graph.
        
        Args:
            G: NetworkX graph
            title: Plot title
            save_path: Path to save the plot (optional)
        """
        plt.figure(figsize=(10, 8))
        
        # Use spring layout for better visualization
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=500, alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.6, width=2)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dessin plot saved to: {save_path}")
        else:
            plt.show()


class MonodromyExplorer:
    """
    Explore monodromy groups and their properties.
    """
    
    def __init__(self):
        self.belyi = BelyiMap()
    
    def explore_degree_3_monodromy(self):
        """
        Explore degree 3 monodromy groups.
        """
        print("=== Degree 3 Monodromy Groups ===\n")
        
        triples = self.belyi.monodromy_group(degree=3)
        
        print(f"Found {len(triples)} valid permutation triples:")
        
        for i, (sigma_0, sigma_1, sigma_inf) in enumerate(triples[:5]):  # Show first 5
            print(f"\nTriple {i+1}:")
            print(f"  σ₀ = {sigma_0}")
            print(f"  σ₁ = {sigma_1}")
            print(f"  σ∞ = {sigma_inf}")
            
            # Find cycles
            cycles_0 = self.belyi.permutation_cycles(sigma_0)
            cycles_1 = self.belyi.permutation_cycles(sigma_1)
            cycles_inf = self.belyi.permutation_cycles(sigma_inf)
            
            print(f"  Cycles: σ₀={cycles_0}, σ₁={cycles_1}, σ∞={cycles_inf}")
            
            # Generate dessin
            dessin = self.belyi.dessin_denfant(sigma_0, sigma_1, sigma_inf)
            self.belyi.plot_dessin(dessin, f"Dessin {i+1}: σ₀={sigma_0}, σ₁={sigma_1}, σ∞={sigma_inf}", 
                                 save_path=f"plots/dessin_{i+1}.png")
    
    def analyze_simple_belyi(self):
        """
        Analyze the simple Belyi map f(z) = z^2.
        """
        print("=== Simple Belyi Map Analysis: f(z) = z^2 ===\n")
        
        f = self.belyi.simple_belyi_map()
        print(f"Belyi map: f(z) = {f}")
        
        # Compute ramification data
        ramification = self.belyi.ramification_data(f)
        print(f"Ramification data: {ramification}")
        
        # Plot the function
        z_values = np.linspace(-2, 2, 1000)
        f_values = z_values**2
        
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(z_values, f_values, 'b-', linewidth=2)
        plt.axhline(y=0, color='r', linestyle='--', alpha=0.7, label='y=0')
        plt.axhline(y=1, color='g', linestyle='--', alpha=0.7, label='y=1')
        plt.xlabel('z')
        plt.ylabel('f(z)')
        plt.title('Belyi Map f(z) = z²')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(z_values, f_values, 'b-', linewidth=2)
        plt.axhline(y=0, color='r', linestyle='--', alpha=0.7)
        plt.axhline(y=1, color='g', linestyle='--', alpha=0.7)
        plt.axvline(x=0, color='orange', linestyle='--', alpha=0.7, label='z=0')
        plt.axvline(x=1, color='purple', linestyle='--', alpha=0.7, label='z=1')
        plt.xlabel('z')
        plt.ylabel('f(z)')
        plt.title('Ramification Points')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(-0.5, 1.5)
        plt.ylim(-0.5, 2)
        
        plt.tight_layout()
        plt.savefig("plots/belyi_map_analysis.png", dpi=300, bbox_inches='tight')
        print("Belyi map analysis plot saved to: plots/belyi_map_analysis.png")


def demonstrate_anabelian_geometry():
    """
    Demonstrate Anabelian Geometry with Belyi maps and monodromy.
    """
    print("=== Anabelian Geometry: Belyi Maps and Monodromy ===\n")
    
    explorer = MonodromyExplorer()
    
    # Analyze simple Belyi map
    explorer.analyze_simple_belyi()
    
    # Explore degree 3 monodromy
    explorer.explore_degree_3_monodromy()
    
    return explorer


if __name__ == "__main__":
    demonstrate_anabelian_geometry()
