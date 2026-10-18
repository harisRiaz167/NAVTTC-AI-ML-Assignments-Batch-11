
# Assignment 40 — Week 3, Day 3
# Topic: NumPy Random Techniques

import numpy as np


# Exercise 1: Generate a Random Integer

number = np.random.randint(100)

print("Exercise 1: Random Integer")
print(number)


# Exercise 2: Generate a Random Integer Between 1 and 10

number = np.random.randint(1, 11)

print("\nExercise 2: Random Integer Between 1 and 10")
print(number)


# Exercise 3: Generate a Random Float

number = np.random.rand()

print("\nExercise 3: Random Float")
print(number)


# Exercise 4: Generate Multiple Random Floats

numbers = np.random.rand(5)

print("\nExercise 4: Five Random Floats")
print(numbers)


# Exercise 5: Generate a 1-D Array of Random Integers

numbers = np.random.randint(1, 50, size=5)

print("\nExercise 5: Random Integer Array")
print(numbers)


# Exercise 6: Generate a 2-D Array of Random Integers

numbers = np.random.randint(1, 100, size=(2, 3))

print("\nExercise 6: Two-Dimensional Random Array")
print(numbers)


# Exercise 7: Generate Random Numbers from 0 to 1

numbers = np.random.random(4)

print("\nExercise 7: Random Numbers from 0 to 1")
print(numbers)


# Exercise 8: Select a Random Item from an Array

arr = np.array([10, 20, 30, 40, 50])

number = np.random.choice(arr)

print("\nExercise 8: Random Choice")
print(number)


# Exercise 9: Select Multiple Random Items

arr = np.array([10, 20, 30, 40, 50])

numbers = np.random.choice(arr, size=3)

print("\nExercise 9: Three Random Choices")
print(numbers)


# Exercise 10: Generate a Random Boolean Array

numbers = np.random.choice([True, False], size=5)

print("\nExercise 10: Random Boolean Array")
print(numbers)


# Exercise 11: Shuffle an Array

arr = np.array([1, 2, 3, 4, 5])

np.random.shuffle(arr)

print("\nExercise 11: Shuffled Array")
print(arr)


# Exercise 12: Generate a Random Permutation

arr = np.array([1, 2, 3, 4, 5])

numbers = np.random.permutation(arr)

print("\nExercise 12: Random Permutation")
print(numbers)


# Exercise 13: Generate Random Numbers from a Normal Distribution

numbers = np.random.normal(size=5)

print("\nExercise 13: Normal Distribution")
print(numbers)


# Exercise 14: Generate Random Numbers from a Binomial Distribution

numbers = np.random.binomial(n=10, p=0.5, size=5)

print("\nExercise 14: Binomial Distribution")
print(numbers)


# Exercise 15: Generate Random Numbers with a Fixed Seed

np.random.seed(42)

numbers = np.random.randint(1, 100, size=5)

print("\nExercise 15: Random Numbers with Seed")
print(numbers)
