
# Assignment 39 — Week 3, Day 4
# Topic: Sorting NumPy Arrays

import numpy as np


# Exercise 1: Sort a Numeric Array

arr = np.array([3, 1, 5, 2, 4])

result = np.sort(arr)

print("Exercise 1: Sort Numeric Array")
print(result)


# Exercise 2: Sort a String Array

arr = np.array(["banana", "apple", "cherry", "mango"])

result = np.sort(arr)

print("\nExercise 2: Sort String Array")
print(result)


# Exercise 3: Sort a Boolean Array

arr = np.array([True, False, True, False])

result = np.sort(arr)

print("\nExercise 3: Sort Boolean Array")
print(result)


# Exercise 4: Sort a 2-D Array by Rows

arr = np.array([[3, 2, 1], [6, 5, 4]])

result = np.sort(arr)

print("\nExercise 4: Sort 2-D Array")
print(result)


# Exercise 5: Sort Each Column of a 2-D Array

arr = np.array([[3, 1, 2], [6, 4, 5]])

result = np.sort(arr, axis=0)

print("\nExercise 5: Sort by Columns")
print(result)


# Exercise 6: Sort Each Row of a 2-D Array

arr = np.array([[3, 1, 2], [6, 4, 5]])

result = np.sort(arr, axis=1)

print("\nExercise 6: Sort by Rows")
print(result)


# Exercise 7: Sort an Array in Descending Order

arr = np.array([3, 1, 5, 2, 4])

result = np.sort(arr)[::-1]

print("\nExercise 7: Descending Order")
print(result)


# Exercise 8: Check the Original Array After Sorting

arr = np.array([50, 10, 40, 20, 30])

result = np.sort(arr)

print("\nExercise 8: Original and Sorted Arrays")
print("Original array:", arr)
print("Sorted array:", result)
