"""
Frobenioid Theory - Monoid Implementation

This module implements the simplest computable example of Frobenioid theory
using monoid-based Frobenioids as created by Mochizuki for manipulating heights.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx


class MonoidFrobenioid:
    """
    Monoid-based Frobenioid implementation.
    
    A Frobenioid abstracts divisor/line bundle data as a category.
    The simplest example uses monoid M = N with objects as integers
    and morphisms as multiplication.
    """
    
    def __init__(self, base_monoid=None, degree_function=None):
        """
        Initialize Frobenioid with base monoid and degree function.
        
        Args:
            base_monoid: Base monoid (default: natural numbers N)
            degree_function: Degree function for objects
        """
        if base_monoid is None:
            self.base_monoid = list(range(1, 21))  # First 20 natural numbers
        else:
            self.base_monoid = base_monoid
        
        if degree_function is None:
            # Default degree function: deg(p^n) = n
            self.degree_function = lambda n: n
        else:
            self.degree_function = degree_function
        
        # Store objects and morphisms
        self.objects = self.base_monoid
        self.morphisms = self._generate_morphisms()
    
    def _generate_morphisms(self):
        """
        Generate morphisms between objects.
        
        Morphisms represent multiplication by powers of prime p.
        For simplicity, we use multiplication by any element.
        
        Returns:
            dict: Dictionary mapping (source, target) to morphism data
        """
        morphisms = {}
        
        for source in self.objects:
            for target in self.objects:
                # Check if target = source * k for some k
                if target % source == 0:
                    multiplier = target // source
                    morphisms[(source, target)] = {
                        'multiplier': multiplier,
                        'degree': self.degree_function(multiplier)
                    }
        
        return morphisms
    
    def compose_morphisms(self, f, g):
        """
        Compose two morphisms f: A -> B and g: B -> C.
        
        Args:
            f: First morphism (source, target, multiplier)
            g: Second morphism (source, target, multiplier)
            
        Returns:
            tuple: Composed morphism (source, target, multiplier)
        """
        if f[1] != g[0]:  # Check if composition is valid
            return None
        
        source = f[0]
        target = g[1]
        multiplier = f[2] * g[2]
        
        return (source, target, multiplier)
    
    def degree_difference(self, source, target):
        """
        Compute degree difference between source and target objects.
        
        Args:
            source, target: Objects in the Frobenioid
            
        Returns:
            float: Degree difference
        """
        if (source, target) not in self.morphisms:
            return None
        
        morphism = self.morphisms[(source, target)]
        return morphism['degree']
    
    def new_scale_function(self, n):
        """
        Define new scale function T(n) = n + floor(n/2).
        
        This represents a different way of measuring "size" in the Frobenioid.
        
        Args:
            n: Natural number
            
        Returns:
            int: T(n) = n + floor(n/2)
        """
        return n + n // 2
    
    def compare_scales(self, max_n=10):
        """
        Compare original degree function with new scale function.
        
        Args:
            max_n: Maximum value to compare
            
        Returns:
            dict: Comparison data
        """
        comparison = {}
        
        for n in range(1, max_n + 1):
            original_degree = self.degree_function(n)
            new_scale = self.new_scale_function(n)
            
            comparison[n] = {
                'original_degree': original_degree,
                'new_scale': new_scale,
                'difference': new_scale - original_degree,
                'ratio': new_scale / original_degree if original_degree != 0 else float('inf')
            }
        
        return comparison
    
    def generate_objects_table(self, max_n=15):
        """
        Generate table of objects, morphisms, and degree differences.
        
        Args:
            max_n: Maximum object value
            
        Returns:
            list: List of object data
        """
        objects_data = []
        
        for n in range(1, max_n + 1):
            degree = self.degree_function(n)
            new_scale = self.new_scale_function(n)
            
            # Find morphisms from this object
            outgoing_morphisms = []
            for (source, target), morphism_data in self.morphisms.items():
                if source == n:
                    outgoing_morphisms.append({
                        'target': target,
                        'multiplier': morphism_data['multiplier'],
                        'degree': morphism_data['degree']
                    })
            
            objects_data.append({
                'object': n,
                'degree': degree,
                'new_scale': new_scale,
                'outgoing_morphisms': outgoing_morphisms
            })
        
        return objects_data
    
    def plot_degree_comparison(self, max_n=20):
        """
        Plot comparison between original degree and new scale function.
        
        Args:
            max_n: Maximum value to plot
        """
        n_values = list(range(1, max_n + 1))
        original_degrees = [self.degree_function(n) for n in n_values]
        new_scales = [self.new_scale_function(n) for n in n_values]
        
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 2, 1)
        plt.plot(n_values, original_degrees, 'b-o', label='Original degree', markersize=4)
        plt.plot(n_values, new_scales, 'r-s', label='New scale T(n)', markersize=4)
        plt.xlabel('n')
        plt.ylabel('Value')
        plt.title('Degree vs New Scale Function')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 2)
        differences = [new_scales[i] - original_degrees[i] for i in range(len(n_values))]
        plt.plot(n_values, differences, 'g-^', markersize=4)
        plt.xlabel('n')
        plt.ylabel('T(n) - deg(n)')
        plt.title('Difference: New Scale - Original Degree')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 3)
        ratios = [new_scales[i] / original_degrees[i] for i in range(len(n_values))]
        plt.plot(n_values, ratios, 'm-d', markersize=4)
        plt.xlabel('n')
        plt.ylabel('T(n) / deg(n)')
        plt.title('Ratio: New Scale / Original Degree')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 4)
        plt.scatter(original_degrees, new_scales, alpha=0.7)
        plt.xlabel('Original Degree')
        plt.ylabel('New Scale')
        plt.title('Scatter Plot: Original vs New Scale')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def plot_frobenioid_graph(self, max_n=10):
        """
        Plot the Frobenioid as a directed graph.
        
        Args:
            max_n: Maximum object value to include
        """
        G = nx.DiGraph()
        
        # Add nodes
        for n in range(1, max_n + 1):
            G.add_node(n, degree=self.degree_function(n))
        
        # Add edges (morphisms)
        for (source, target), morphism_data in self.morphisms.items():
            if source <= max_n and target <= max_n:
                G.add_edge(source, target, 
                          multiplier=morphism_data['multiplier'],
                          degree=morphism_data['degree'])
        
        plt.figure(figsize=(12, 8))
        
        # Use spring layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw nodes with size proportional to degree
        node_sizes = [self.degree_function(node) * 200 for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                              node_color='lightblue', alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True, 
                              arrowsize=20, edge_color='gray')
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        plt.title(f'Frobenioid Graph (Objects 1-{max_n})', fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


class FrobenioidExamples:
    """
    Examples demonstrating Frobenioid theory concepts.
    """
    
    def __init__(self):
        self.frobenioid = MonoidFrobenioid()
    
    def demonstrate_basic_frobenioid(self):
        """
        Demonstrate basic Frobenioid operations.
        """
        print("=== Frobenioid Theory: Monoid Example ===\n")
        
        print("Objects (first 10 natural numbers):")
        for i in range(1, 11):
            degree = self.frobenioid.degree_function(i)
            new_scale = self.frobenioid.new_scale_function(i)
            print(f"  Object {i}: degree = {degree}, T({i}) = {new_scale}")
        
        print(f"\nTotal objects: {len(self.frobenioid.objects)}")
        print(f"Total morphisms: {len(self.frobenioid.morphisms)}")
    
    def demonstrate_morphisms(self):
        """
        Demonstrate morphisms in the Frobenioid.
        """
        print("\n=== Morphisms ===\n")
        
        # Show some example morphisms
        morphism_examples = list(self.frobenioid.morphisms.items())[:10]
        
        print("Example morphisms (source -> target):")
        for (source, target), morphism_data in morphism_examples:
            multiplier = morphism_data['multiplier']
            degree = morphism_data['degree']
            print(f"  {source} -> {target}: multiply by {multiplier}, degree = {degree}")
    
    def demonstrate_degree_comparison(self):
        """
        Demonstrate degree comparison between original and new scale.
        """
        print("\n=== Degree Comparison ===\n")
        
        comparison = self.frobenioid.compare_scales(max_n=10)
        
        print("Comparison of original degree vs new scale T(n):")
        print("n | Original | New Scale | Difference | Ratio")
        print("-" * 50)
        
        for n in range(1, 11):
            data = comparison[n]
            print(f"{n:2d} | {data['original_degree']:8d} | {data['new_scale']:9d} | "
                  f"{data['difference']:10d} | {data['ratio']:6.2f}")
    
    def demonstrate_objects_table(self):
        """
        Demonstrate objects table with morphisms.
        """
        print("\n=== Objects Table ===\n")
        
        objects_data = self.frobenioid.generate_objects_table(max_n=8)
        
        for obj_data in objects_data:
            obj = obj_data['object']
            degree = obj_data['degree']
            new_scale = obj_data['new_scale']
            morphisms = obj_data['outgoing_morphisms']
            
            print(f"Object {obj}: degree = {degree}, T({obj}) = {new_scale}")
            
            if morphisms:
                print("  Morphisms:")
                for morphism in morphisms[:5]:  # Show first 5 morphisms
                    target = morphism['target']
                    multiplier = morphism['multiplier']
                    morphism_degree = morphism['degree']
                    print(f"    -> {target} (×{multiplier}, deg={morphism_degree})")
            
            print()
    
    def demonstrate_visualizations(self):
        """
        Demonstrate visualizations of the Frobenioid.
        """
        print("\n=== Visualizations ===\n")
        
        print("Generating degree comparison plot...")
        self.frobenioid.plot_degree_comparison(max_n=15)
        
        print("Generating Frobenioid graph...")
        self.frobenioid.plot_frobenioid_graph(max_n=8)


def demonstrate_frobenioid():
    """
    Demonstrate Frobenioid theory with monoid examples.
    """
    print("=== Frobenioid Theory: Monoid Implementation ===\n")
    
    examples = FrobenioidExamples()
    
    # Demonstrate basic Frobenioid
    examples.demonstrate_basic_frobenioid()
    
    # Demonstrate morphisms
    examples.demonstrate_morphisms()
    
    # Demonstrate degree comparison
    examples.demonstrate_degree_comparison()
    
    # Demonstrate objects table
    examples.demonstrate_objects_table()
    
    # Demonstrate visualizations
    examples.demonstrate_visualizations()
    
    return examples


if __name__ == "__main__":
    demonstrate_frobenioid()
