
# Assignment 36 — Week 3, Day 4
# Topic: Joining NumPy Arrays

import numpy as np


# Exercise 1: Join Two 1-D Arrays

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

new_arr = np.concatenate((arr1, arr2))

print("Exercise 1: Join Two Arrays")
print(new_arr)


# Exercise 2: Join Arrays Using Axis 0

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

new_arr = np.concatenate((arr1, arr2), axis=0)

print("\nExercise 2: Join Using Axis 0")
print(new_arr)


# Exercise 3: Join Arrays Using Axis 1

arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

new_arr = np.concatenate((arr1, arr2), axis=1)

print("\nExercise 3: Join Using Axis 1")
print(new_arr)


# Exercise 4: Join Arrays Using Stack

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

new_arr = np.stack((arr1, arr2))

print("\nExercise 4: Join Using Stack")
print(new_arr)


# Exercise 5: Join Arrays Using Horizontal Stack

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

new_arr = np.hstack((arr1, arr2))

print("\nExercise 5: Horizontal Stack")
print(new_arr)


# Exercise 6: Join Arrays Using Vertical Stack

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

new_arr = np.vstack((arr1, arr2))

print("\nExercise 6: Vertical Stack")
print(new_arr)


# Exercise 7: Join Arrays Using Depth Stack

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

new_arr = np.dstack((arr1, arr2))

print("\nExercise 7: Depth Stack")
print(new_arr)
