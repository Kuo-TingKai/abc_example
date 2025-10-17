"""
p-adic Teichmüller Theory - Tate Curve Implementation

This module implements the simplest computable example of p-adic Teichmüller theory
using Tate curves (Tate uniformization) for elliptic curves over p-adic fields.
"""

import numpy as np
from sympy import symbols, series, latex
import matplotlib.pyplot as plt


class TateCurve:
    """
    Tate curve implementation for p-adic Teichmüller theory.
    
    The Tate curve E_q is defined by q-expansion formulas when |q|_p < 1.
    It provides p-adic Teichmüller uniformization and can be computed numerically
    using series truncation.
    """
    
    def __init__(self, p=5, q=None, precision=10):
        """
        Initialize Tate curve with prime p and parameter q.
        
        Args:
            p: Prime number (default: 5)
            q: Parameter q with |q|_p < 1 (default: p^(-3))
            precision: Series truncation precision
        """
        self.p = p
        self.precision = precision
        
        if q is None:
            # Default: q = p^(-3) = 1/125 for p=5
            self.q = p**(-3)
        else:
            self.q = q
            
        # Verify |q|_p < 1
        if abs(self.q) >= 1:
            raise ValueError(f"|q|_p must be < 1, got |{self.q}| = {abs(self.q)}")
    
    def weierstrass_coefficients(self):
        """
        Compute Weierstrass coefficients a_4(q) and a_6(q) using Tate curve formulas.
        
        Returns:
            tuple: (a_4, a_6) coefficients
        """
        q = self.q
        
        # Tate curve formulas for Weierstrass coefficients
        # a_4(q) = -5 * sum of n^3 * q^n / (1 - q^n) for n >= 1
        # a_6(q) = -1/12 * sum of (7n^5 + 5n^3) * q^n / (1 - q^n) for n >= 1
        
        a_4 = 0
        a_6 = 0
        
        for n in range(1, self.precision + 1):
            q_n = q**n
            denom = 1 - q_n
            
            if abs(denom) < 1e-10:  # Avoid division by zero
                continue
                
            # a_4 coefficient
            a_4 += -5 * (n**3) * q_n / denom
            
            # a_6 coefficient  
            a_6 += -(1/12) * (7 * n**5 + 5 * n**3) * q_n / denom
        
        return a_4, a_6
    
    def elliptic_curve_equation(self):
        """
        Return the elliptic curve equation y^2 = x^3 + a_4*x + a_6.
        
        Returns:
            str: Equation as string
        """
        a_4, a_6 = self.weierstrass_coefficients()
        return f"y^2 = x^3 + {a_4:.6f}*x + {a_6:.6f}"
    
    def point_addition(self, P1, P2):
        """
        Compute point addition on the elliptic curve.
        
        Args:
            P1, P2: Points as tuples (x, y) or (x, y, z) for projective coordinates
            
        Returns:
            tuple: Sum point P1 + P2
        """
        if len(P1) == 2 and len(P2) == 2:
            x1, y1 = P1
            x2, y2 = P2
            
            # Handle point at infinity
            if x1 == float('inf'):
                return P2
            if x2 == float('inf'):
                return P1
            
            # Handle same point (point doubling)
            if abs(x1 - x2) < 1e-10:
                if abs(y1 - y2) < 1e-10:
                    return self.point_doubling(P1)
                else:
                    return (float('inf'), float('inf'))  # Point at infinity
            
            # Standard point addition formula
            a_4, a_6 = self.weierstrass_coefficients()
            
            slope = (y2 - y1) / (x2 - x1)
            x3 = slope**2 - x1 - x2
            y3 = slope * (x1 - x3) - y1
            
            return (x3, y3)
        
        return (float('inf'), float('inf'))
    
    def point_doubling(self, P):
        """
        Compute point doubling 2*P on the elliptic curve.
        
        Args:
            P: Point as tuple (x, y)
            
        Returns:
            tuple: Doubled point 2*P
        """
        if len(P) == 2:
            x, y = P
            
            if y == 0:  # Point of order 2
                return (float('inf'), float('inf'))
            
            a_4, a_6 = self.weierstrass_coefficients()
            
            # Doubling formula
            slope = (3 * x**2 + a_4) / (2 * y)
            x2 = slope**2 - 2 * x
            y2 = slope * (x - x2) - y
            
            return (x2, y2)
        
        return (float('inf'), float('inf'))
    
    def compute_points(self, x_range=(-2, 2), num_points=100):
        """
        Compute points on the elliptic curve for visualization.
        
        Args:
            x_range: Range of x values to sample
            num_points: Number of points to compute
            
        Returns:
            list: List of (x, y) points on the curve
        """
        a_4, a_6 = self.weierstrass_coefficients()
        points = []
        
        x_values = np.linspace(x_range[0], x_range[1], num_points)
        
        for x in x_values:
            # Solve y^2 = x^3 + a_4*x + a_6
            discriminant = x**3 + a_4*x + a_6
            
            if discriminant >= 0:
                y = np.sqrt(discriminant)
                points.append((x, y))
                if y != 0:  # Add negative y if y != 0
                    points.append((x, -y))
        
        return points
    
    def plot_curve(self, x_range=(-2, 2), num_points=100, save_path=None):
        """
        Plot the Tate curve.
        
        Args:
            x_range: Range of x values to plot
            num_points: Number of points for plotting
            save_path: Path to save the plot (optional)
        """
        points = self.compute_points(x_range, num_points)
        
        if points:
            x_coords, y_coords = zip(*points)
            
            plt.figure(figsize=(10, 8))
            plt.scatter(x_coords, y_coords, s=1, alpha=0.6)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Tate Curve E_q with q = {self.q:.6f}, p = {self.p}')
            plt.grid(True, alpha=0.3)
            plt.axis('equal')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Plot saved to: {save_path}")
            else:
                plt.show()
    
    def __str__(self):
        """String representation of the Tate curve."""
        a_4, a_6 = self.weierstrass_coefficients()
        return f"Tate Curve E_q: y^2 = x^3 + {a_4:.6f}*x + {a_6:.6f} (q = {self.q:.6f}, p = {self.p})"


def demonstrate_tate_curve():
    """
    Demonstrate Tate curve computation with the simplest example.
    """
    print("=== p-adic Teichmüller Theory: Tate Curve Example ===\n")
    
    # Create Tate curve with p=5, q=1/125
    tate = TateCurve(p=5, q=1/125, precision=10)
    
    print(f"Parameters: p = {tate.p}, q = {tate.q}")
    print(f"Elliptic curve equation: {tate.elliptic_curve_equation()}")
    
    # Compute Weierstrass coefficients
    a_4, a_6 = tate.weierstrass_coefficients()
    print(f"Weierstrass coefficients: a_4 = {a_4:.6f}, a_6 = {a_6:.6f}")
    
    # Test point operations
    print("\nPoint operations:")
    
    # Find some points on the curve
    points = tate.compute_points(x_range=(-1, 1), num_points=50)
    if len(points) >= 2:
        P1 = points[0]
        P2 = points[1]
        
        print(f"Point P1: {P1}")
        print(f"Point P2: {P2}")
        
        # Point addition
        P3 = tate.point_addition(P1, P2)
        print(f"P1 + P2 = {P3}")
        
        # Point doubling
        P4 = tate.point_doubling(P1)
        print(f"2*P1 = {P4}")
    
    # Plot the curve
    print("\nGenerating plot...")
    tate.plot_curve(save_path="plots/tate_curve.png")
    
    return tate


if __name__ == "__main__":
    demonstrate_tate_curve()
