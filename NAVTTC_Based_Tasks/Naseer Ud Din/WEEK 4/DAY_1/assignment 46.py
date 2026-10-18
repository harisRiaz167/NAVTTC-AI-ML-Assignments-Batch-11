
import pandas as pd

# Create sample student data
data = {
    "Name": ["Ali", "Ahmed", "Sara", "Ayesha", "Usman"],
    "Age": [20, 21, 19, 22, 20],
    "Marks": [85, 90, 78, 95, 82],
    "Attendance": [90, 85, 95, 98, 80]
}

df = pd.DataFrame(data)

# 1. Display the complete dataset
print("Complete Dataset:")
print(df)

# 2. Display the first five rows
print("\nFirst five rows:")
print(df.head())

# 3. Display the last three rows
print("\nLast three rows:")
print(df.tail(3))

# 4. Display information about the dataset
print("\nDataset Information:")
df.info()

# 5. Display statistical summary
print("\nStatistical Summary:")
print(df.describe())

# 6. Calculate average marks
print("\nAverage Marks:")
print(df["Marks"].mean())

# 7. Calculate maximum marks
print("\nMaximum Marks:")
print(df["Marks"].max())

# 8. Calculate minimum marks
print("\nMinimum Marks:")
print(df["Marks"].min())

# 9. Count the number of students
print("\nTotal Students:")
print(len(df))

# 10. Find students who scored more than 80
print("\nStudents with Marks Greater Than 80:")
print(df[df["Marks"] > 80])

# 11. Find students with attendance of at least 90
print("\nStudents with Attendance >= 90:")
print(df[df["Attendance"] >= 90])

# 12. Sort students by marks in descending order
print("\nStudents Sorted by Marks:")
print(df.sort_values(by="Marks", ascending=False))

# 13. Calculate average attendance
print("\nAverage Attendance:")
print(df["Attendance"].mean())
