"""
NAVTTC AI & Machine Learning - Batch 11
Week 1 - Task 3: Mathematical & Algebraic Operations in Python
Author: Muhammad Ahmed Nadeem
"""

import math
import cmath

def task_square_root_real(number: float = 8.0) -> float:
    """Calculates square root of a real positive number using math.sqrt()"""
    result = math.sqrt(number)
    print(f"[Task 3] Number: {number} -> Square Root: {result}")
    return result

def task_square_root_complex(complex_val: complex = 1 + 2j) -> complex:
    """Calculates square root of a complex number using cmath.sqrt()"""
    result = cmath.sqrt(complex_val)
    print(f"[Task 4] Complex Number: {complex_val} -> Square Root: {result}")
    return result

def task_celsius_to_fahrenheit(celsius: float = 37.5) -> float:
    """Converts Celsius temperature to Fahrenheit"""
    fahrenheit = (celsius * 9.0 / 5.0) + 32.0
    print(f"[Task 5] Temperature: {celsius}°C -> {fahrenheit}°F")
    return fahrenheit

def task_triangle_area_heron(a: float = 5.0, b: float = 6.0, c: float = 7.0) -> float:
    """Calculates area of a triangle using Heron's formula"""
    s = (a + b + c) / 2.0
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    print(f"[Task 6] Triangle sides ({a}, {b}, {c}) -> Semi-perimeter: {s}, Area: {area}")
    return area

def task_solve_quadratic(a: float = 1.0, b: float = 5.0, c: float = 6.0):
    """Solves quadratic equation ax^2 + bx + c = 0 using quadratic formula"""
    discriminant = (b ** 2) - (4.0 * a * c)
    root1 = (-b + cmath.sqrt(discriminant)) / (2.0 * a)
    root2 = (-b - cmath.sqrt(discriminant)) / (2.0 * a)
    print(f"[Task 7] Equation: {a}x² + {b}x + {c} = 0 -> Roots: {root1}, {root2}")
    return root1, root2

def task_km_to_miles(km: float = 10.0) -> float:
    """Converts kilometers to miles using international conversion factor"""
    miles = km * 0.621371
    print(f"[Task 8] Distance: {km} km -> {miles} miles")
    return miles

if __name__ == "__main__":
    print("=" * 60)
    print("NAVTTC Batch 11 - Week 1 Assignment Script")
    print("Student: Muhammad Ahmed Nadeem")
    print("=" * 60)
    task_square_root_real(8)
    task_square_root_complex(1 + 2j)
    task_celsius_to_fahrenheit(37.5)
    task_triangle_area_heron(5, 6, 7)
    task_solve_quadratic(1, 5, 6)
    task_km_to_miles(10.0)
    print("=" * 60)
