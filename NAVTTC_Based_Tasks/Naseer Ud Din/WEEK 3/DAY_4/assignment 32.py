
# Assignment 32 — Week 3, Day 4
# Topic: NumPy Array Copying and Viewing

import numpy as np


# Exercise 1: Create a Copy of an Array

arr = np.array([10, 20, 30, 40, 50])

new_arr = arr.copy()

print("Exercise 1: Copy an Array")
print("Original array:", arr)
print("Copied array:", new_arr)


# Exercise 2: Change the Copy

arr = np.array([10, 20, 30, 40, 50])

new_arr = arr.copy()

new_arr[0] = 100

print("\nExercise 2: Change the Copy")
print("Original array:", arr)
print("Copied array:", new_arr)


# Exercise 3: Create a View of an Array

arr = np.array([10, 20, 30, 40, 50])

new_arr = arr.view()

print("\nExercise 3: Create a View")
print("Original array:", arr)
print("Viewed array:", new_arr)


# Exercise 4: Change the View

arr = np.array([10, 20, 30, 40, 50])

new_arr = arr.view()

new_arr[0] = 100

print("\nExercise 4: Change the View")
print("Original array:", arr)
print("Viewed array:", new_arr)


# Exercise 5: Change the Original Array After Creating a Copy

arr = np.array([1, 2, 3, 4])

new_arr = arr.copy()

arr[0] = 100

print("\nExercise 5: Change Original Array After Copying")
print("Original array:", arr)
print("Copied array:", new_arr)


# Exercise 6: Change the Original Array After Creating a View

arr = np.array([1, 2, 3, 4])

new_arr = arr.view()

arr[0] = 100

print("\nExercise 6: Change Original Array After Viewing")
print("Original array:", arr)
print("Viewed array:", new_arr)


# Exercise 7: Check Whether Two Arrays Share the Same Data

arr = np.array([10, 20, 30, 40])

copy_arr = arr.copy()
view_arr = arr.view()

print("\nExercise 7: Check Base Attribute")
print("Copy base:", copy_arr.base)
print("View base:", view_arr.base)


# Exercise 8: Check Whether an Array Is a Copy or a View

arr = np.array([5, 10, 15, 20])

copy_arr = arr.copy()
view_arr = arr.view()

print("\nExercise 8: Check Copy and View")
print("Original array:", arr)
print("Copy array:", copy_arr)
print("View array:", view_arr)

print("Is copy based on original array?", copy_arr.base is arr)
print("Is view based on original array?", view_arr.base is arr)
