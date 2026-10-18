
import pandas as pd

# Create sample data containing errors
data = {
    "Name": ["Ali", "Ahmed", "Sara", "Ayesha", "Sara"],
    "Age": [20, 21, 19, 22, 19],
    "Date": [
        "2026-01-01",
        "2026-01-02",
        "2026-01-03",
        "2026-01-04",
        "2026-01-03"
    ],
    "Duration": [60, 60, 450, 45, 450],
    "Calories": [300, None, 250, None, 250]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# 1. Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 2. Fill missing Calories with the column average
average_calories = df["Calories"].mean()
df["Calories"] = df["Calories"].fillna(average_calories)

print("\nAfter Filling Missing Calories:")
print(df)

# 3. Convert Date column to datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\nAfter Converting Dates:")
print(df)

# 4. Correct wrong Duration values
# Assume 450 is an incorrect value and should be 45
df.loc[df["Duration"] == 450, "Duration"] = 45

print("\nAfter Correcting Duration:")
print(df)

# 5. Find duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated())

# 6. Remove duplicate rows
df = df.drop_duplicates()

print("\nAfter Removing Duplicates:")
print(df)

# 7. Check missing values again
print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# 8. Display final cleaned data
print("\nFinal Cleaned Data:")
print(df)

# 9. Reset row indexes
df = df.reset_index(drop=True)

print("\nData with Reset Index:")
print(df)
