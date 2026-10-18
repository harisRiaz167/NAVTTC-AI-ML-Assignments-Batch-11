# List Data Type in Python

# Creating a list
my_list = [10, 20, 30, 40, 50]
print("Original List:", my_list)

# Creating a list with different data types
mixed_list = [10, "Python", 3.5, True]
print("Mixed List:", mixed_list)

# Creating an empty list
empty_list = []
print("Empty List:", empty_list)

# Accessing list elements
print("First Element:", my_list[0])
print("Last Element:", my_list[-1])

# Slicing a list
print("First Three Elements:", my_list[0:3])
print("Elements from Index 2:", my_list[2:])
print("List in Reverse:", my_list[::-1])

# Finding the length of a list
print("Length:", len(my_list))

# Adding an element
my_list.append(60)
print("After Append:", my_list)

# Inserting an element
my_list.insert(1, 15)
print("After Insert:", my_list)

# Adding multiple elements
my_list.extend([70, 80])
print("After Extend:", my_list)

# Updating an element
my_list[0] = 5
print("After Updating:", my_list)

# Removing an element by value
my_list.remove(30)
print("After Remove:", my_list)

# Removing an element by index
removed_item = my_list.pop(1)
print("Removed Item:", removed_item)
print("After Pop:", my_list)

# Deleting an element using del
del my_list[-1]
print("After Del:", my_list)

# Counting occurrences
numbers = [10, 20, 10, 30, 10, 40]
print("Count of 10:", numbers.count(10))

# Finding the index of an element
print("Index of 30:", numbers.index(30))

# Checking if an element exists
print("Is 20 present?", 20 in numbers)
print("Is 100 present?", 100 in numbers)

# Sorting a list
numbers.sort()
print("Sorted List:", numbers)

# Sorting in descending order
numbers.sort(reverse=True)
print("Descending Order:", numbers)

# Reversing a list
numbers.reverse()
print("Reversed List:", numbers)

# Finding minimum, maximum, and sum
print("Minimum:", min(numbers))
print("Maximum:", max(numbers))
print("Sum:", sum(numbers))

# Looping through a list
print("List Elements:")
for item in numbers:
    print(item)

# List comprehension
squares = [x ** 2 for x in range(1, 6)]
print("Squares:", squares)

# Copying a list
copied_list = numbers.copy()
print("Copied List:", copied_list)

# Joining two lists
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined_list = list1 + list2
print("Combined List:", combined_list)

# Repeating a list
print("Repeated List:", list1 * 2)

# Clearing a list
copied_list.clear()
print("After Clear:", copied_list)
