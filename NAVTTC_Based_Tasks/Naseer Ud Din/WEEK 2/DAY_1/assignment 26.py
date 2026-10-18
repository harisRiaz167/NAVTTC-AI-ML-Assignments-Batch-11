
# Assignment 26 — Week 2, Day 1
# Topic: Python Exception Handling


# Exercise 1: Basic Exception Handling

try:
    number = int(input("Enter a number: "))
    print("You entered:", number)

except ValueError:
    print("Invalid input! Please enter a number.")


# Exercise 2: Handling Division by Zero

try:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    result = num1 / num2
    print("Result:", result)

except ZeroDivisionError:
    print("Error! Cannot divide by zero.")

except ValueError:
    print("Error! Please enter valid numbers.")


# Exercise 3: Using the else Block

try:
    number = int(input("Enter a number: "))

except ValueError:
    print("Invalid input!")

else:
    print("Your number is:", number)
    print("No error occurred.")


# Exercise 4: Using the finally Block

try:
    number = int(input("Enter a number: "))
    print("Number:", number)

except ValueError:
    print("Please enter a valid number.")

finally:
    print("Program execution completed.")


# Exercise 5: Handling IndexError

numbers = [10, 20, 30]

try:
    print(numbers[5])

except IndexError:
    print("Error! List index does not exist.")


# Exercise 6: Using the raise Keyword

try:
    age = int(input("Enter your age: "))

    if age < 0:
        raise ValueError("Age cannot be negative.")

    print("Your age is:", age)

except ValueError as error:
    print("Error:", error)


# Exercise 7: Handling Multiple Exceptions

try:
    num1 = int(input("Enter first number: "))
    num2 = int(input("Enter second number: "))

    result = num1 / num2
    print("Result:", result)

except ValueError:
    print("Error! Enter numbers only.")

except ZeroDivisionError:
    print("Error! Cannot divide by zero.")

else:
    print("Calculation successful.")

finally:
    print("Program ended.")
