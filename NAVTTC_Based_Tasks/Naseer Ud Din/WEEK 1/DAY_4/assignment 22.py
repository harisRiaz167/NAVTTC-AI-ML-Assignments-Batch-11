# Assignment 22 — Week 1, Day 4
# Topic: Python
# Complete the exercise on the tuple data type in Python.

# Creating a tuple
my_tuple = (10, 20, 30, 40, 50)
print("Tuple:", my_tuple)

# Creating a tuple without parentheses
numbers = 1, 2, 3, 4, 5
print("Tuple without parentheses:", numbers)

# Creating a tuple with one element
single_tuple = (10,)
print("Single element tuple:", single_tuple)

# Creating an empty tuple
empty_tuple = ()
print("Empty tuple:", empty_tuple)

# Accessing tuple elements
print("First element:", my_tuple[0])
print("Last element:", my_tuple[-1])

# Slicing a tuple
print("First three elements:", my_tuple[0:3])
print("Elements from index 2:", my_tuple[2:])
print("Tuple in reverse:", my_tuple[::-1])

# Finding the length of a tuple
print("Length:", len(my_tuple))

# Checking if an element exists
print("Is 30 present?", 30 in my_tuple)
print("Is 100 present?", 100 in my_tuple)

# Counting occurrences
repeated_tuple = (10, 20, 10, 30, 10)
print("Count of 10:", repeated_tuple.count(10))

# Finding the index of an element
print("Index of 40:", my_tuple.index(40))

# Joining tuples
tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)
combined_tuple = tuple1 + tuple2
print("Combined tuple:", combined_tuple)

# Repeating a tuple
print("Repeated tuple:", tuple1 * 2)

# Looping through a tuple
print("Tuple elements:")
for item in my_tuple:
    print(item)

# Tuple packing
student = ("Naseer Ud Din", 21, "BS Computer Science")
print("Packed tuple:", student)

# Tuple unpacking
name, age, course = student
print("Name:", name)
print("Age:", age)
print("Course:", course)

# Converting a list into a tuple
my_list = [100, 200, 300]
converted_tuple = tuple(my_list)
print("List converted to tuple:", converted_tuple)

# Converting a tuple into a list
converted_list = list(my_tuple)
print("Tuple converted to list:", converted_list)

# Finding the minimum and maximum
print("Minimum value:", min(my_tuple))
print("Maximum value:", max(my_tuple))

# Calculating the sum
print("Sum:", sum(my_tuple))

# Checking tuple immutability
original_tuple = (1, 2, 3)
new_tuple = original_tuple + (4,)
print("Original tuple:", original_tuple)
print("New tuple:", new_tuple)
