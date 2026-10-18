
# Assignment 28 — Week 3, Day 3
# Topic: NumPy - Creating Arrays Using Python

import numpy as np


# Exercise 1: Create a 0-D Array

arr = np.array(10)

print("0-D Array:")
print(arr)
print("Number of dimensions:", arr.ndim)


# Exercise 2: Create a 1-D Array

arr = np.array([1, 2, 3, 4, 5])

print("\n1-D Array:")
print(arr)
print("Number of dimensions:", arr.ndim)


# Exercise 3: Create a 2-D Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\n2-D Array:")
print(arr)
print("Number of dimensions:", arr.ndim)


# Exercise 4: Create a 3-D Array

arr = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])

print("\n3-D Array:")
print(arr)
print("Number of dimensions:", arr.ndim)


# Exercise 5: Create an Array Using the ndmin Parameter

arr = np.array([1, 2, 3, 4], ndmin=5)

print("\nArray with Minimum 5 Dimensions:")
print(arr)
print("Number of dimensions:", arr.ndim)


# Exercise 6: Create an Array of Zeros

arr = np.zeros(5)

print("\nArray of Zeros:")
print(arr)


# Exercise 7: Create an Array of Ones

arr = np.ones(5)

print("\nArray of Ones:")
print(arr)


# Exercise 8: Create an Array Using arange()

arr = np.arange(1, 11)

print("\nArray Using arange():")
print(arr)


# Exercise 9: Create an Array with a Specific Data Type

arr = np.array([1, 2, 3, 4], dtype=float)

print("\nArray with Float Data Type:")
print(arr)


# Exercise 10: Check the Shape of an Array

arr = np.array([[1, 2, 3], [4, 5, 6]])

print("\nShape of Array:")
print(arr.shape)


# Exercise 11: Check the Data Type of an Array

arr = np.array([1, 2, 3, 4])

print("\nData Type of Array:")
print(arr.dtype)


# Exercise 12: Create an Empty Array with a Specific Shape

arr = np.empty((2, 3))

print("\nEmpty Array with Shape (2, 3):")
print(arr)
