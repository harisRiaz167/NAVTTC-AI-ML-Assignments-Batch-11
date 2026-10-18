
# Assignment 31 — Week 3, Day 4
# Topic: NumPy Data Types

import numpy as np


# Exercise 1: Check the Data Type of an Integer Array

arr = np.array([1, 2, 3, 4, 5])

print("Exercise 1: Integer Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 2: Check the Data Type of a Float Array

arr = np.array([1.5, 2.5, 3.5, 4.5])

print("\nExercise 2: Float Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 3: Create a String Array

arr = np.array(["apple", "banana", "orange"])

print("\nExercise 3: String Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 4: Create a Boolean Array

arr = np.array([True, False, True, False])

print("\nExercise 4: Boolean Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 5: Specify the Data Type Using dtype

arr = np.array([1, 2, 3, 4], dtype="i")

print("\nExercise 5: Integer Data Type")
print(arr)
print("Data type:", arr.dtype)


# Exercise 6: Create an Array with Float Data Type

arr = np.array([1, 2, 3, 4], dtype="f")

print("\nExercise 6: Float Data Type")
print(arr)
print("Data type:", arr.dtype)


# Exercise 7: Convert Integer Values into Floats

arr = np.array([1, 2, 3, 4])

new_arr = arr.astype(float)

print("\nExercise 7: Convert Integer to Float")
print("Original array:", arr)
print("Converted array:", new_arr)
print("New data type:", new_arr.dtype)


# Exercise 8: Convert Float Values into Integers

arr = np.array([1.1, 2.5, 3.9, 4.7])

new_arr = arr.astype(int)

print("\nExercise 8: Convert Float to Integer")
print("Original array:", arr)
print("Converted array:", new_arr)
print("New data type:", new_arr.dtype)


# Exercise 9: Convert Integers into Strings

arr = np.array([10, 20, 30, 40])

new_arr = arr.astype(str)

print("\nExercise 9: Convert Integer to String")
print("Original array:", arr)
print("Converted array:", new_arr)
print("New data type:", new_arr.dtype)


# Exercise 10: Create an Array with 64-bit Integers

arr = np.array([10, 20, 30, 40], dtype=np.int64)

print("\nExercise 10: 64-bit Integer Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 11: Create an Array with 32-bit Floats

arr = np.array([1.5, 2.5, 3.5], dtype=np.float32)

print("\nExercise 11: 32-bit Float Array")
print(arr)
print("Data type:", arr.dtype)


# Exercise 12: Check the Data Type of Each Array Element

arr = np.array([10, 20, 30])

print("\nExercise 12: Data Type of an Element")
print(type(arr[0]))
print("Array data type:", arr.dtype)
