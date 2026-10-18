
# Assignment 29 — Week 3, Day 4
# Topic: NumPy Array Indexing

import numpy as np


# Exercise 1: Access the First Element

arr = np.array([10, 20, 30, 40, 50])

print("Exercise 1: First Element")
print(arr[0])


# Exercise 2: Access the Second Element

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 2: Second Element")
print(arr[1])


# Exercise 3: Access the Third Element

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 3: Third Element")
print(arr[2])


# Exercise 4: Access the Last Element

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 4: Last Element")
print(arr[-1])


# Exercise 5: Access the Second-Last Element

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 5: Second-Last Element")
print(arr[-2])


# Exercise 6: Access Elements of a 2-D Array

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 6: Element at Row 1, Column 2")
print(arr[0, 1])


# Exercise 7: Access Another Element of a 2-D Array

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 7: Element at Row 2, Column 3")
print(arr[1, 2])


# Exercise 8: Access Elements of a 3-D Array

arr = np.array([[[1, 2, 3], [4, 5, 6]],
                [[7, 8, 9], [10, 11, 12]]])

print("\nExercise 8: Access Element")
print(arr[0, 1, 2])


# Exercise 9: Array Slicing

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 9: Elements from Index 1 to 3")
print(arr[1:4])


# Exercise 10: Slice from the Beginning

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 10: First Three Elements")
print(arr[:3])


# Exercise 11: Slice Until the End

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 11: Elements from Index 2 to the End")
print(arr[2:])


# Exercise 12: Negative Slicing

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 12: Negative Slicing")
print(arr[-3:-1])


# Exercise 13: Slicing with a Step

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 13: Every Second Element")
print(arr[::2])


# Exercise 14: Slice a 2-D Array

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 14: First Two Elements of the First Row")
print(arr[0, 0:2])


# Exercise 15: Access a Complete Column

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 15: Second Column")
print(arr[:, 1])
