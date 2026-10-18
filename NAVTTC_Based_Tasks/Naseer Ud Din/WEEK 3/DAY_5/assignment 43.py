
import pandas as pd

# 1. Create a Series from a list
data = [10, 20, 30, 40, 50]
s = pd.Series(data)

print("Series from a list:")
print(s)

# 2. Create a Series with custom indexes
s = pd.Series(data, index=["a", "b", "c", "d", "e"])

print("\nSeries with custom indexes:")
print(s)

# 3. Access an item using its index label
print("\nValue at index 'c':")
print(s["c"])

# 4. Create a Series from a dictionary
student_marks = {
    "Ali": 85,
    "Ahmed": 90,
    "Sara": 78
}

marks = pd.Series(student_marks)

print("\nSeries from a dictionary:")
print(marks)

# 5. Access a student's marks
print("\nAli's marks:")
print(marks["Ali"])

# 6. Create a Series using selected dictionary keys
selected_marks = pd.Series(student_marks, index=["Ali", "Sara"])

print("\nSelected students' marks:")
print(selected_marks)

# 7. Display the first two values
print("\nFirst two values:")
print(marks.head(2))

# 8. Display the number of values
print("\nNumber of values:")
print(marks.size)

# 9. Calculate total marks
print("\nTotal marks:")
print(marks.sum())

# 10. Calculate average marks
print("\nAverage marks:")
print(marks.mean())
