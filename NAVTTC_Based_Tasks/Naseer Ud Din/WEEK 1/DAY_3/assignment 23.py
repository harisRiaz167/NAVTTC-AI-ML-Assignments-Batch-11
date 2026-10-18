# Topic: Python
# Complete the exercise on the string data type in Python.
# Reference: https://www.programiz.com/python-programming/string
# # 
# Creating strings
text1 = "Hello Python"
text2 = 'Welcome to Python Programming'

print("String 1:", text1)
print("String 2:", text2)

# Accessing characters using indexing
print("First character:", text1[0])
print("Last character:", text1[-1])

# Slicing a string
print("First five characters:", text1[0:5])
print("Characters from index 6:", text1[6:])
print("String in reverse:", text1[::-1])

# Finding the length of a string
print("Length:", len(text1))

# Joining strings
first_name = "Naseer"
last_name = "Ud Din"
full_name = first_name + " " + last_name
print("Full Name:", full_name)

# Repeating a string
print("Repeated String:", "Python " * 3)

# Checking whether a substring exists
print("Is Python present?", "Python" in text1)
print("Is Java present?", "Java" in text1)

# Changing letter case
message = "hello python programming"
print("Uppercase:", message.upper())
print("Lowercase:", message.lower())
print("Title Case:", message.title())
print("Capitalized:", message.capitalize())

# Removing whitespace
text3 = "   Hello Python   "
print("Original:", repr(text3))
print("After stripping:", repr(text3.strip()))
print("Left strip:", repr(text3.lstrip()))
print("Right strip:", repr(text3.rstrip()))

# Replacing text
sentence = "I like Java"
print("After replacement:", sentence.replace("Java", "Python"))

# Splitting a string
words = "Python is easy to learn"
print("Split words:", words.split())

# Joining a list of strings
languages = ["Python", "C++", "Java"]
print("Joined string:", ", ".join(languages))

# Counting occurrences
text4 = "banana"
print("Count of a:", text4.count("a"))

# Finding a substring
print("Index of 'Python':", text1.find("Python"))

# Checking string contents
print("Is alphabetic?", "Python".isalpha())
print("Is numeric?", "12345".isdigit())
print("Is alphanumeric?", "Python123".isalnum())
print("Is lowercase?", "hello".islower())
print("Is uppercase?", "HELLO".isupper())
print("Starts with Hello?", text1.startswith("Hello"))
print("Ends with Python?", text1.endswith("Python"))

# Formatting a string
name = "Naseer"
age = 21
print(f"My name is {name} and I am {age} years old.")

# Multiline string
paragraph = """Python is easy to learn.
Python is used in AI and Machine Learning."""
print("Multiline String:")
print(paragraph)

# Escape characters
print("Hello\nPython")
print("Hello\tPython")

# Strings are immutable
original = "Python"
new_string = "J" + original[1:]
print("Original String:", original)
print("New String:", new_string)
