
import pandas as pd

# Create sample student data
data = {
    "StudyHours": [1, 2, 3, 4, 5],
    "Attendance": [50, 60, 70, 80, 90],
    "Marks": [40, 50, 60, 70, 80],
    "SleepHours": [9, 8, 7, 6, 5]
}

df = pd.DataFrame(data)

print("Student Data:")
print(df)

# 1. Calculate correlation between all numerical columns
print("\nCorrelation Matrix:")
print(df.corr())

# 2. Find correlation between StudyHours and Marks
print("\nStudy Hours vs Marks:")
print(df["StudyHours"].corr(df["Marks"]))

# 3. Find correlation between Attendance and Marks
print("\nAttendance vs Marks:")
print(df["Attendance"].corr(df["Marks"]))

# 4. Find correlation between SleepHours and Marks
print("\nSleep Hours vs Marks:")
print(df["SleepHours"].corr(df["Marks"]))

# 5. Calculate Pearson correlation
print("\nPearson Correlation:")
print(df.corr(method="pearson"))

# 6. Calculate Spearman correlation
print("\nSpearman Correlation:")
print(df.corr(method="spearman"))

# 7. Calculate Kendall correlation
print("\nKendall Correlation:")
print(df.corr(method="kendall"))

# 8. Display the correlation between every feature and Marks
print("\nCorrelation with Marks:")
print(df.corr()["Marks"])
