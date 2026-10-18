
# Assignment 37 — Week 3, Day 4
# Topic: Splitting NumPy Arrays

import numpy as np


# Exercise 1: Split an Array into Three Parts

arr = np.array([1, 2, 3, 4, 5, 6])

new_arr = np.array_split(arr, 3)

print("Exercise 1: Split into Three Parts")

print(new_arr[0])
print(new_arr[1])
print(new_arr[2])


# Exercise 2: Split an Array into Two Parts

arr = np.array([10, 20, 30, 40, 50, 60])

new_arr = np.array_split(arr, 2)

print("\nExercise 2: Split into Two Parts")

print(new_arr[0])
print(new_arr[1])


# Exercise 3: Split an Array into Four Parts

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

new_arr = np.array_split(arr, 4)

print("\nExercise 3: Split into Four Parts")

for part in new_arr:
    print(part)


# Exercise 4: Split a 2-D Array Horizontally

arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])

new_arr = np.array_split(arr, 2, axis=0)

print("\nExercise 4: Split Rows")

for part in new_arr:
    print(part)


# Exercise 5: Split a 2-D Array by Columns

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8]])

new_arr = np.array_split(arr, 2, axis=1)

print("\nExercise 5: Split Columns")

for part in new_arr:
    print(part)


# Exercise 6: Use Split Instead of Array Split

arr = np.array([10, 20, 30, 40, 50, 60])

new_arr = np.split(arr, 3)

print("\nExercise 6: Using np.split()")

for part in new_arr:
    print(part)
