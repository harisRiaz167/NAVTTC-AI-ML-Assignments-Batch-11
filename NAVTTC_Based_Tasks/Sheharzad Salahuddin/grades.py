import numpy as np

GRADE_POINTS = {
    "A": 4,
    "B": 3,
    "C": 2,
    "F": 1,
}

class Student: 
    def __init__(self, name): 
        self.name = name 
        self.courses = [] 
        self.subjects = []
        
    def add_grade(self, course, grade, credits=3): 
        self.courses.append((course, grade.upper(), credits)) 
        
    def gpa(self): 
        points = np.array([GRADE_POINTS[g] for _, g, _ in self.courses]) 
        credits = np.array([c for _, _, c in self.courses]) 
        return round((points * credits).sum() / credits.sum(), 2)
    
    def add_subject(self, subject):
        self.subjects.append(subject)

student = Student("Sheharzad")

student.add_grade("Math", "A", 2)
student.add_grade("History", "B", 3)
student.add_grade("Physics", "A", 1)
student.add_grade("General Science", "A", 4)
student.add_grade("Computer Science", "F", 1)

student.add_subject("Math")
student.add_subject("History")
student.add_subject("Physics")
student.add_subject("General Science")
student.add_subject("Computer Science")

print("Student:", student.name)
print("Subjects:", student.subjects)
print("Courses:", len(student.courses))
print("GPA:", student.gpa())


# arr = np.array([2, 3, 1, 1])

# print("Original array:")
# print(arr)

# print("Reshaped array:")
# print(arr.reshape(2, 2))