# Complete the exercise on the set data type in Python.
# Reference: https://www.programiz.com/python-programming/set

# Creating sets
numbers = {1, 2, 3, 4, 5}
fruits = {"apple", "banana", "mango"}
print("Numbers:", numbers)
print("Fruits:", fruits)

# Creating an empty set
empty_set = set()
print("Empty Set:", empty_set)

# Duplicate values are automatically removed
my_set = {1, 2, 2, 3, 3, 4}
print("Set without duplicates:", my_set)

# Adding an element
numbers.add(6)
print("After adding 6:", numbers)

# Adding multiple elements
numbers.update([7, 8, 9])
print("After adding multiple elements:", numbers)

# Removing an element
numbers.remove(3)
print("After removing 3:", numbers)

# Removing an element safely
numbers.discard(10)
print("After discard:", numbers)

# Removing an arbitrary element
removed_item = numbers.pop()
print("Removed item:", removed_item)
print("After pop:", numbers)

# Checking whether an element exists
print("Is 5 present?", 5 in numbers)
print("Is 10 present?", 10 in numbers)

# Set union
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}
print("Union:", set_a.union(set_b))

# Set intersection
print("Intersection:", set_a.intersection(set_b))

# Set difference
print("Difference A - B:", set_a.difference(set_b))
print("Difference B - A:", set_b.difference(set_a))

# Symmetric difference
print("Symmetric Difference:", set_a.symmetric_difference(set_b))

# Check subset and superset
set_c = {1, 2}
print("Is C a subset of A?", set_c.issubset(set_a))
print("Is A a superset of C?", set_a.issuperset(set_c))

# Check disjoint sets
set_d = {7, 8, 9}
print("Are A and D disjoint?", set_a.isdisjoint(set_d))

# Find the number of elements
print("Length of set A:", len(set_a))

# Loop through a set
print("Elements of set A:")
for item in set_a:
    print(item)

# Copy a set
set_copy = set_a.copy()
print("Copied Set:", set_copy)

# Clear all elements
set_copy.clear()
print("After clearing the copied set:", set_copy)
