
# Assignment 42: Pandas Getting Started

import pandas as pd

# 1. Display Pandas version
print("Pandas version:")
print(pd.__version__)

# 2. Create a Series
numbers = [10, 20, 30, 40, 50]
my_series = pd.Series(numbers)

print("\nPandas Series:")
print(my_series)

# 3. Create a DataFrame
data = {
    "Name": ["Ali", "Ahmed", "Sara"],
    "Age": [20, 21, 19],
    "City": ["Lahore", "Karachi", "Islamabad"]
}

df = pd.DataFrame(data)

print("\nPandas DataFrame:")
print(df)

# 4. Display the first five rows
print("\nFirst five rows:")
print(df.head())

# 5. Display the shape (rows, columns)
print("\nDataFrame shape:")
print(df.shape)

# 6. Display the data types
print("\nData types:")
print(df.dtypes)

# 7. Display basic information
print("\nDataFrame information:")
df.info()

# 8. Display the number of rows and columns
print("\nNumber of rows:", len(df))
print("Number of columns:", len(df.columns))
