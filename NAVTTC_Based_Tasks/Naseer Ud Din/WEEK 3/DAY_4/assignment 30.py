
# Assignment 30 — Week 3, Day 4
# Topic: NumPy Array Slicing

import numpy as np


# Exercise 1: Basic Array Slicing

arr = np.array([10, 20, 30, 40, 50, 60])

print("Exercise 1: Basic Slicing")
print(arr[1:4])


# Exercise 2: Slice from the Beginning

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 2: Slice from the Beginning")
print(arr[:4])


# Exercise 3: Slice Until the End

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 3: Slice Until the End")
print(arr[2:])


# Exercise 4: Use Negative Indexes

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 4: Negative Slicing")
print(arr[-4:-1])


# Exercise 5: Use a Step Value

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 5: Slicing with Step")
print(arr[::2])


# Exercise 6: Slice Every Second Element from Index 1

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 6: Step Slicing")
print(arr[1::2])


# Exercise 7: Slice a 2-D Array

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 7: First Row, First Two Elements")
print(arr[0, 0:2])


# Exercise 8: Slice Both Rows and Columns

arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("\nExercise 8: First Two Rows and First Two Columns")
print(arr[0:2, 0:2])


# Exercise 9: Get All Rows of a Specific Column

arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("\nExercise 9: All Rows of the Second Column")
print(arr[:, 1])


# Exercise 10: Get Specific Rows and All Columns

arr = np.array([[10, 20, 30],
                [40, 50, 60],
                [70, 80, 90]])

print("\nExercise 10: First Two Rows and All Columns")
print(arr[0:2, :])


# Exercise 11: Slice the Last Two Elements

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 11: Last Two Elements")
print(arr[-2:])


# Exercise 12: Reverse an Array Using Slicing

arr = np.array([10, 20, 30, 40, 50, 60])

print("\nExercise 12: Reverse the Array")
print(arr[::-1])
