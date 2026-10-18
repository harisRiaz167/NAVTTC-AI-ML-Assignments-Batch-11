
# Assignment 27 — Week 2, Day 1
# Topic: User-Defined Exception Handling


# Exercise 1: Creating a User-Defined Exception

class MyError(Exception):
    pass


try:
    raise MyError("This is a user-defined exception.")

except MyError as error:
    print("Error:", error)


# Exercise 2: Age Validation Using Custom Exception

class InvalidAgeError(Exception):
    pass


try:
    age = int(input("Enter your age: "))

    if age < 18:
        raise InvalidAgeError("You must be 18 or older.")

    print("You are eligible.")

except InvalidAgeError as error:
    print("Error:", error)

except ValueError:
    print("Please enter a valid number.")


# Exercise 3: Checking for Negative Numbers

class NegativeNumberError(Exception):
    pass


try:
    number = int(input("Enter a positive number: "))

    if number < 0:
        raise NegativeNumberError("Negative numbers are not allowed.")

    print("You entered:", number)

except NegativeNumberError as error:
    print("Error:", error)

except ValueError:
    print("Please enter a valid integer.")


# Exercise 4: Checking Marks

class InvalidMarksError(Exception):
    pass


try:
    marks = int(input("Enter your marks (0-100): "))

    if marks < 0 or marks > 100:
        raise InvalidMarksError("Marks must be between 0 and 100.")

    print("Your marks are:", marks)

except InvalidMarksError as error:
    print("Error:", error)

except ValueError:
    print("Please enter valid marks.")


# Exercise 5: Bank Withdrawal Using Custom Exception

class InsufficientBalanceError(Exception):
    pass


try:
    balance = 5000

    amount = int(input("Enter withdrawal amount: "))

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if amount > balance:
        raise InsufficientBalanceError("Insufficient bank balance.")

    balance = balance - amount

    print("Withdrawal successful.")
    print("Remaining balance:", balance)

except InsufficientBalanceError as error:
    print("Error:", error)

except ValueError as error:
    print("Error:", error)
