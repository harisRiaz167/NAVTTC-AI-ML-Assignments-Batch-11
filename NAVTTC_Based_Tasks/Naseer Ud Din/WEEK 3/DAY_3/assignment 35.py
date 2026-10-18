
# Assignment 35 — Week 3, Day 3
# Topic: NumPy Array Iteration

import numpy as np


# Exercise 1: Iterate Through a 1-D Array

arr = np.array([10, 20, 30, 40, 50])

print("Exercise 1: Iterate Through a 1-D Array")

for x in arr:
    print(x)


# Exercise 2: Iterate Through a 2-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 2: Iterate Through a 2-D Array")

for x in arr:
    print(x)


# Exercise 3: Access Every Element of a 2-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 3: Access Every Element")

for x in arr:
    for y in x:
        print(y)


# Exercise 4: Iterate Through a 3-D Array

arr = np.array([[[1, 2], [3, 4]],
                [[5, 6], [7, 8]]])

print("\nExercise 4: Iterate Through a 3-D Array")

for x in arr:
    print(x)


# Exercise 5: Access Every Element of a 3-D Array

arr = np.array([[[1, 2], [3, 4]],
                [[5, 6], [7, 8]]])

print("\nExercise 5: Access Every Element of a 3-D Array")

for x in arr:
    for y in x:
        for z in y:
            print(z)


# Exercise 6: Use nditer() to Iterate Through a 2-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nExercise 6: Using nditer()")

for x in np.nditer(arr):
    print(x)


# Exercise 7: Iterate Through an Array with Indexes

arr = np.array([10, 20, 30, 40, 50])

print("\nExercise 7: Array Indexes")

for index, value in np.ndenumerate(arr):
    print("Index:", index, "Value:", value)


# Exercise 8: Iterate Through a 2-D Array with Indexes

arr = np.array([[10, 20, 30], [40, 50, 60]])

print("\nExercise 8: 2-D Array Indexes")

for index, value in np.ndenumerate(arr):
    print("Index:", index, "Value:", value)
