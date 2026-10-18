
# Assignment 38 — Week 3, Day 4
# Topic: Searching NumPy Arrays

import numpy as np


# Exercise 1: Find the Index of a Value

arr = np.array([10, 20, 30, 40, 50])

result = np.where(arr == 30)

print("Exercise 1: Find Index of 30")
print(result)


# Exercise 2: Find All Even Numbers

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

result = np.where(arr % 2 == 0)

print("\nExercise 2: Find Even Number Indexes")
print(result)


# Exercise 3: Find All Odd Numbers

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

result = np.where(arr % 2 == 1)

print("\nExercise 3: Find Odd Number Indexes")
print(result)


# Exercise 4: Find Values Greater Than 30

arr = np.array([10, 20, 30, 40, 50, 60])

result = np.where(arr > 30)

print("\nExercise 4: Values Greater Than 30")
print(result)


# Exercise 5: Find the Insertion Index Using Searchsorted

arr = np.array([10, 20, 30, 40, 50])

result = np.searchsorted(arr, 35)

print("\nExercise 5: Searchsorted")
print("Insertion index:", result)


# Exercise 6: Search for Multiple Values

arr = np.array([10, 20, 30, 40, 50])

result = np.searchsorted(arr, [15, 25, 45])

print("\nExercise 6: Search Multiple Values")
print(result)


# Exercise 7: Use the Right Side of Searchsorted

arr = np.array([10, 20, 20, 30, 40])

result = np.searchsorted(arr, 20, side="right")

print("\nExercise 7: Searchsorted Right")
print(result)


# Exercise 8: Find Matching Values Using a Condition

arr = np.array([5, 10, 15, 20, 25, 30])

result = arr[arr >= 20]

print("\nExercise 8: Values Greater Than or Equal to 20")
print(result)
