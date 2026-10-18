
import pandas as pd

# 1. Create a Pandas Series
data = [10, 20, 30, 40, 50]
series = pd.Series(data)

print("Pandas Series:")
print(series)

# 2. Create a DataFrame
student_data = {
    "Name": ["Ali", "Ahmed", "Sara", "Ayesha"],
    "Age": [20, 21, 19, 22],
    "Marks": [85, 90, 78, 95]
}

df = pd.DataFrame(student_data)

print("\nComplete DataFrame:")
print(df)

# 3. Display the first two rows
print("\nFirst two rows:")
print(df.head(2))

# 4. Display the last two rows
print("\nLast two rows:")
print(df.tail(2))

# 5. Display column names
print("\nColumn names:")
print(df.columns)

# 6. Display DataFrame information
print("\nDataFrame information:")
df.info()

# 7. Display statistical information
print("\nStatistical summary:")
print(df.describe())

# 8. Select one column
print("\nStudent names:")
print(df["Name"])

# 9. Select a specific row
print("\nFirst student:")
print(df.iloc[0])

# 10. Calculate average marks
print("\nAverage marks:")
print(df["Marks"].mean())

# 11. Find students with marks greater than 80
print("\nStudents with marks greater than 80:")
print(df[df["Marks"] > 80])
