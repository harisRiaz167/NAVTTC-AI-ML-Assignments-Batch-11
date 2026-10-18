
# Assignment 34 — Week 3, Day 3
# Topic: NumPy Array Reshaping

import numpy as np


# Exercise 1: Reshape a 1-D Array into a 2-D Array

arr = np.array([1, 2, 3, 4, 5, 6])

new_arr = arr.reshape(2, 3)

print("Exercise 1: Reshape into 2 Rows and 3 Columns")
print(new_arr)


# Exercise 2: Reshape into 3 Rows and 2 Columns

arr = np.array([1, 2, 3, 4, 5, 6])

new_arr = arr.reshape(3, 2)

print("\nExercise 2: Reshape into 3 Rows and 2 Columns")
print(new_arr)


# Exercise 3: Reshape into a 3-D Array

arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])

new_arr = arr.reshape(2, 2, 2)

print("\nExercise 3: Reshape into a 3-D Array")
print(new_arr)


# Exercise 4: Use -1 to Calculate a Dimension Automatically

arr = np.array([1, 2, 3, 4, 5, 6])

new_arr = arr.reshape(2, -1)

print("\nExercise 4: Reshape Using -1")
print(new_arr)


# Exercise 5: Check the Shape After Reshaping

arr = np.array([10, 20, 30, 40, 50, 60])

new_arr = arr.reshape(2, 3)

print("\nExercise 5: Check the New Shape")
print(new_arr)
print("Shape:", new_arr.shape)


# Exercise 6: Convert a 2-D Array into a 1-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

new_arr = arr.reshape(-1)

print("\nExercise 6: Convert into a 1-D Array")
print(new_arr)


# Exercise 7: Check Whether Reshaping Returns a View

arr = np.array([1, 2, 3, 4, 5, 6])

new_arr = arr.reshape(2, 3)

print("\nExercise 7: Check the Base Array")
print(new_arr)
print("Shares original array as base:", new_arr.base is arr)
