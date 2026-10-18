
import pandas as pd

# 1. Create a DataFrame from a dictionary
data = {
    "Name": ["Ali", "Ahmed", "Sara", "Ayesha"],
    "Age": [20, 21, 19, 22],
    "Marks": [85, 90, 78, 95],
    "City": ["Lahore", "Karachi", "Lahore", "Islamabad"]
}

df = pd.DataFrame(data)

print("Complete DataFrame:")
print(df)

# 2. Display the first three rows
print("\nFirst three rows:")
print(df.head(3))

# 3. Display the last two rows
print("\nLast two rows:")
print(df.tail(2))

# 4. Display one column
print("\nStudent names:")
print(df["Name"])

# 5. Display multiple columns
print("\nNames and marks:")
print(df[["Name", "Marks"]])

# 6. Access a row using its position
print("\nFirst row:")
print(df.iloc[0])

# 7. Access a specific value
print("\nMarks of the first student:")
print(df.loc[0, "Marks"])

# 8. Add a new column
df["Passed"] = df["Marks"] >= 50

print("\nDataFrame after adding Passed column:")
print(df)

# 9. Add a new student
df.loc[len(df)] = ["Usman", 20, 82, "Lahore", True]

print("\nDataFrame after adding a student:")
print(df)

# 10. Find students with marks greater than 80
print("\nStudents with marks greater than 80:")
print(df[df["Marks"] > 80])

# 11. Sort students by marks
print("\nStudents sorted by marks:")
print(df.sort_values(by="Marks", ascending=False))

# 12. Display DataFrame dimensions
print("\nShape (rows, columns):")
print(df.shape)

# 13. Display column names
print("\nColumn names:")
print(df.columns.tolist())

# 14. Display statistical summary
print("\nStatistical summary:")
print(df.describe())
