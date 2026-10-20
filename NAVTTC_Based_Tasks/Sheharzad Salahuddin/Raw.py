import pandas as pd


df = pd.DataFrame({
    "branches": ["DHA #4", "DHA #5", "DHA #6", "DHA #7"],
    "days": "Sat, Sun",
    "sales": [3000, 4000, 6000, 34000]
})

# find average sales for each branch
average_sales = df.groupby("branches")["sales"].mean()

# 

print(average_sales)
print(df)
