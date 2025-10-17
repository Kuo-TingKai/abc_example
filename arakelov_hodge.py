"""
Arakelov/Hodge Theory - Height Computation Implementation

This module implements the simplest computable example of Arakelov/Hodge theory
using height calculations for rational points and projective spaces.
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import gcd, Rational
from fractions import Fraction
import math


class HeightCalculator:
    """
    Height calculator for Arakelov/Hodge theory.
    
    Arakelov theory combines Archimedean and non-Archimedean geometry
    to produce global heights. For rational points, we compute naive heights.
    """
    
    def __init__(self):
        """Initialize height calculator."""
        pass
    
    def naive_height_rational(self, x):
        """
        Compute naive height of a rational number.
        
        For x = a/b in reduced form, h(x) = log max(|a|, |b|)
        
        Args:
            x: Rational number (can be Fraction, Rational, or float)
            
        Returns:
            float: Naive height
        """
        if isinstance(x, (int, float)):
            # Convert to rational
            x = Fraction(x).limit_denominator(1000000)
        
        if isinstance(x, Fraction):
            numerator = abs(x.numerator)
            denominator = abs(x.denominator)
        elif hasattr(x, 'p') and hasattr(x, 'q'):  # SymPy Rational
            numerator = abs(x.p)
            denominator = abs(x.q)
        else:
            raise ValueError(f"Cannot compute height for {type(x)}")
        
        return math.log(max(numerator, denominator))
    
    def projective_height(self, point):
        """
        Compute height of a projective point [a₀:a₁:...:aₙ].
        
        Height = log max(|aᵢ|) for all i
        
        Args:
            point: List or tuple of coordinates
            
        Returns:
            float: Projective height
        """
        if not point:
            return 0
        
        # Convert to integers if possible
        coords = []
        for coord in point:
            if isinstance(coord, (int, float)):
                coord = Fraction(coord).limit_denominator(1000000)
            coords.append(coord)
        
        # Find common denominator
        denominators = [abs(coord.denominator) if isinstance(coord, Fraction) else 1 
                       for coord in coords]
        lcm_denom = 1
        for d in denominators:
            lcm_denom = lcm_denom * d // math.gcd(lcm_denom, d)
        
        # Convert to integers
        int_coords = []
        for coord in coords:
            if isinstance(coord, Fraction):
                int_coords.append(abs(coord.numerator * (lcm_denom // coord.denominator)))
            else:
                int_coords.append(abs(int(coord * lcm_denom)))
        
        return math.log(max(int_coords))
    
    def global_height(self, point, places=None):
        """
        Compute global height using all places (Archimedean and non-Archimedean).
        
        For simplicity, we use the naive height which corresponds to
        the sum over all places of log max(|x|_v) where |·|_v is the v-adic absolute value.
        
        Args:
            point: Rational point
            places: List of places (for extension, not used in simple case)
            
        Returns:
            float: Global height
        """
        return self.naive_height_rational(point)
    
    def height_distribution(self, max_height=5, num_points=1000):
        """
        Generate distribution of heights for random rational points.
        
        Args:
            max_height: Maximum height to consider
            num_points: Number of points to generate
            
        Returns:
            tuple: (heights, counts) for histogram
        """
        heights = []
        
        for _ in range(num_points):
            # Generate random rational number
            numerator = np.random.randint(-100, 101)
            denominator = np.random.randint(1, 101)
            
            if numerator == 0:
                continue
            
            x = Fraction(numerator, denominator)
            height = self.naive_height_rational(x)
            
            if height <= max_height:
                heights.append(height)
        
        return heights
    
    def plot_height_distribution(self, heights, bins=50):
        """
        Plot height distribution histogram.
        
        Args:
            heights: List of heights
            bins: Number of histogram bins
        """
        plt.figure(figsize=(10, 6))
        plt.hist(heights, bins=bins, alpha=0.7, edgecolor='black')
        plt.xlabel('Height')
        plt.ylabel('Frequency')
        plt.title('Distribution of Heights of Rational Points')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def compare_heights(self, points):
        """
        Compare heights of multiple points.
        
        Args:
            points: List of rational points
            
        Returns:
            dict: Dictionary mapping points to their heights
        """
        height_dict = {}
        
        for point in points:
            if isinstance(point, (list, tuple)) and len(point) > 1:
                height = self.projective_height(point)
            else:
                height = self.naive_height_rational(point)
            
            height_dict[str(point)] = height
        
        return height_dict


class ArakelovExamples:
    """
    Examples demonstrating Arakelov/Hodge theory concepts.
    """
    
    def __init__(self):
        self.calculator = HeightCalculator()
    
    def demonstrate_basic_heights(self):
        """
        Demonstrate basic height calculations.
        """
        print("=== Arakelov/Hodge Theory: Basic Height Examples ===\n")
        
        # Example points
        points = [
            Fraction(3, 2),  # x = 3/2
            Fraction(1, 1),  # x = 1
            Fraction(0, 1),  # x = 0
            Fraction(-5, 3), # x = -5/3
            Fraction(7, 1),  # x = 7
        ]
        
        print("Rational point heights:")
        for point in points:
            height = self.calculator.naive_height_rational(point)
            print(f"  h({point}) = log(max({abs(point.numerator)}, {abs(point.denominator)})) = {height:.6f}")
        
        print("\nProjective point heights:")
        projective_points = [
            [1, 2, 3],      # [1:2:3]
            [3, 4, 5],      # [3:4:5]
            [1, 1, 1],      # [1:1:1]
            [2, 3, 6],      # [2:3:6]
        ]
        
        for point in projective_points:
            height = self.calculator.projective_height(point)
            print(f"  h({point}) = {height:.6f}")
    
    def demonstrate_height_properties(self):
        """
        Demonstrate properties of heights.
        """
        print("\n=== Height Properties ===\n")
        
        # Property 1: Height of 0
        height_0 = self.calculator.naive_height_rational(0)
        print(f"Height of 0: h(0) = {height_0:.6f}")
        
        # Property 2: Height of 1
        height_1 = self.calculator.naive_height_rational(1)
        print(f"Height of 1: h(1) = {height_1:.6f}")
        
        # Property 3: Height of reciprocals
        x = Fraction(3, 2)
        height_x = self.calculator.naive_height_rational(x)
        height_1_x = self.calculator.naive_height_rational(1/x)
        print(f"h({x}) = {height_x:.6f}")
        print(f"h(1/{x}) = h({1/x}) = {height_1_x:.6f}")
        print(f"Note: Heights of x and 1/x are generally different")
        
        # Property 4: Height growth
        print("\nHeight growth with numerator/denominator:")
        for n in range(1, 6):
            x = Fraction(n, 1)
            height = self.calculator.naive_height_rational(x)
            print(f"  h({n}) = {height:.6f}")
    
    def demonstrate_height_distribution(self):
        """
        Demonstrate height distribution for random rational points.
        """
        print("\n=== Height Distribution Analysis ===\n")
        
        # Generate height distribution
        heights = self.calculator.height_distribution(max_height=4, num_points=5000)
        
        print(f"Generated {len(heights)} points with heights ≤ 4")
        print(f"Mean height: {np.mean(heights):.4f}")
        print(f"Standard deviation: {np.std(heights):.4f}")
        print(f"Min height: {min(heights):.4f}")
        print(f"Max height: {max(heights):.4f}")
        
        # Plot distribution
        self.calculator.plot_height_distribution(heights)
    
    def demonstrate_elliptic_curve_heights(self):
        """
        Demonstrate heights on elliptic curves (toy example).
        """
        print("\n=== Heights on Elliptic Curves (Toy Example) ===\n")
        
        # Simple elliptic curve: y² = x³ + 1
        # Find some rational points
        rational_points = []
        
        for x_num in range(-10, 11):
            for x_den in range(1, 11):
                x = Fraction(x_num, x_den)
                y_squared = x**3 + 1
                
                # Check if y² is a perfect square
                if y_squared >= 0:
                    y_sqrt = int(np.sqrt(y_squared.numerator / y_squared.denominator))
                    if y_sqrt * y_sqrt == y_squared.numerator / y_squared.denominator:
                        y = Fraction(y_sqrt, 1)
                        rational_points.append((x, y))
        
        print(f"Found {len(rational_points)} rational points on y² = x³ + 1:")
        
        for i, (x, y) in enumerate(rational_points[:10]):  # Show first 10
            height_x = self.calculator.naive_height_rational(x)
            height_y = self.calculator.naive_height_rational(y)
            height_point = self.calculator.projective_height([x, y, 1])
            
            print(f"  Point {i+1}: ({x}, {y})")
            print(f"    h(x) = {height_x:.4f}, h(y) = {height_y:.4f}, h(point) = {height_point:.4f}")


def demonstrate_arakelov_hodge():
    """
    Demonstrate Arakelov/Hodge theory with height calculations.
    """
    print("=== Arakelov/Hodge Theory: Height Computations ===\n")
    
    examples = ArakelovExamples()
    
    # Demonstrate basic heights
    examples.demonstrate_basic_heights()
    
    # Demonstrate height properties
    examples.demonstrate_height_properties()
    
    # Demonstrate height distribution
    examples.demonstrate_height_distribution()
    
    # Demonstrate elliptic curve heights
    examples.demonstrate_elliptic_curve_heights()
    
    return examples


if __name__ == "__main__":
    demonstrate_arakelov_hodge()
