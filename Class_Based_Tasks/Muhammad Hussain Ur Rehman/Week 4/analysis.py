import pandas as pd
import numpy as np
students = pd.read_csv("students.csv", index_col= 'name')

print(f"Raw Data : {students}")

print('\n====================== ANALYSIS =================')

print(students.info)

students['top_marks_cities'] = np.where(students['scores'] > 400, students['city'],0)
print(students)

students['top_class'] = np.where(students['scores'] > 600, students['class'], 0)
print(students)

students['top_students_age'] = np.where(students['scores'] > 600, students['age'], 0)
print(students)