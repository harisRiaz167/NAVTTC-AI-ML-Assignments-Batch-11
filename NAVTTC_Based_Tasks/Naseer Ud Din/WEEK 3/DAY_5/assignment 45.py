
import pandas as pd

# 1. Create sample student data
data = {
    "Name": ["Ali", "Ahmed", "Sara", "Ayesha", "Usman"],
    "Age": [20, 21, 19, 22, 20],
    "Marks": [85, 90, 78, 95, 82],
    "City": ["Lahore", "Karachi", "Lahore", "Islamabad", "Multan"]
}

df = pd.DataFrame(data)

# 2. Save the DataFrame as a CSV file
df.to_csv("students.csv", index=False)

print("CSV file created successfully.")

# 3. Read the CSV file
df = pd.read_csv("students.csv")

print("\nComplete CSV data:")
print(df)

# 4. Display the first five rows
print("\nFirst five rows:")
print(df.head())

# 5. Display the first two rows
print("\nFirst two rows:")
print(df.head(2))

# 6. Display the last two rows
print("\nLast two rows:")
print(df.tail(2))

# 7. Read only selected columns
print("\nNames and marks:")
print(pd.read_csv("students.csv", usecols=["Name", "Marks"]))

# 8. Display basic information
print("\nDataFrame information:")
df.info()

# 9. Display statistical summary
print("\nStatistical summary:")
print(df.describe())

# 10. Find students with marks greater than 80
print("\nStudents with marks greater than 80:")
print(df[df["Marks"] > 80])

# 11. Display the number of rows and columns
print("\nDataFrame shape:")
print(df.shape)

# 12. Display column names
print("\nColumn names:")
print(df.columns.tolist())
