
# Assignment 33 — Week 3, Day 3
# Topic: NumPy Array Shape

import numpy as np


# Exercise 1: Check the Shape of a 1-D Array

arr = np.array([10, 20, 30, 40, 50])

print("Exercise 1: Shape of 1-D Array")
print(arr.shape)


# Exercise 2: Check the Shape of a 2-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 2: Shape of 2-D Array")
print(arr.shape)


# Exercise 3: Check the Shape of a 3-D Array

arr = np.array([[[1, 2, 3], [4, 5, 6]],
                [[7, 8, 9], [10, 11, 12]]])

print("\nExercise 3: Shape of 3-D Array")
print(arr.shape)


# Exercise 4: Check Rows and Columns

arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("\nExercise 4: Rows and Columns")
print("Shape:", arr.shape)
print("Number of rows:", arr.shape[0])
print("Number of columns:", arr.shape[1])


# Exercise 5: Check the Number of Dimensions

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 5: Number of Dimensions")
print(arr.ndim)


# Exercise 6: Check the Total Number of Elements

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 6: Total Elements")
print(arr.size)
