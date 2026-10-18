# Topic: Python
# Complete the exercise on user-defined functions in Python.
# Reference: https://www.geeksforgeeks.org/functions-in-python/
# # 




# 1. Creating and calling a function
def greet():
    print("Hello! Welcome to Python.")

greet()


# 2. Function with parameters
def greet_user(name):
    print("Hello,", name)

greet_user("Naseer")


# 3. Function with multiple parameters
def add(a, b):
    print("Sum:", a + b)

add(10, 20)


# 4. Function with a return value
def multiply(a, b):
    return a * b

result = multiply(5, 4)
print("Multiplication:", result)


# 5. Function with a default argument
def introduce(name, age=21):
    print("My name is", name, "and my age is", age)

introduce("Naseer")
introduce("Ali", 22)


# 6. Function with keyword arguments
def student_info(name, course):
    print("Name:", name)
    print("Course:", course)

student_info(course="BS Computer Science", name="Naseer")


# 7. Function with *args
def add_numbers(*args):
    print("Numbers:", args)
    print("Total:", sum(args))

add_numbers(10, 20, 30, 40)


# 8. Function with **kwargs
def display_info(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)

display_info(name="Naseer", age=21, city="Lahore")


# 9. Function to check even or odd
def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

print("10 is:", check_even_odd(10))
print("7 is:", check_even_odd(7))


# 10. Function to find the largest of three numbers
def largest(a, b, c):
    return max(a, b, c)

print("Largest number:", largest(15, 25, 10))


# 11. Recursive function to calculate factorial
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print("Factorial of 5:", factorial(5))


# 12. Lambda function
square = lambda x: x * x
print("Square of 6:", square(6))


# 13. Function with a local variable
def show_message():
    message = "This is a local variable"
    print(message)

show_message()


# 14. Function with a global variable
message = "This is a global variable"

def display_message():
    print(message)

display_message()


# 15. Function to calculate the area of a rectangle
def rectangle_area(length, width):
    return length * width

print("Rectangle Area:", rectangle_area(10, 5))


# 16. Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

print("Temperature:", celsius_to_fahrenheit(25), "F")


# 17. Function to calculate the average
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

print("Average:", calculate_average([70, 80, 90]))


# 18. Function to reverse a string
def reverse_string(text):
    return text[::-1]

print("Reversed String:", reverse_string("Python"))


# 19. Function to count vowels
def count_vowels(text):
    count = 0
    for character in text.lower():
        if character in "aeiou":
            count += 1
    return count

print("Vowels:", count_vowels("Programming"))


# 20. Function to check a palindrome
def is_palindrome(text):
    text = text.lower().replace(" ", "")
    return text == text[::-1]

print("Is madam a palindrome?", is_palindrome("madam"))
print("Is python a palindrome?", is_palindrome("python"))
