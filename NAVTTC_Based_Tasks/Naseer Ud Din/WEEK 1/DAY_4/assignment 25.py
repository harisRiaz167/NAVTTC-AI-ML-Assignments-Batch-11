# Complete the exercise on the dictionary data type in Python.
# Reference: https://www.programiz.com/python-programming/dictionary
# # 

# Creating a dictionary
student = {
    "name": "Naseer Ud Din",
    "age": 21,
    "course": "BS Computer Science",
    "semester": 7,
    "marks": 85
}

# Display the dictionary
print("Student Dictionary:", student)

# Access dictionary values
print("Name:", student["name"])
print("Course:", student.get("course"))

# Add a new item
student["city"] = "Lahore"
print("After adding city:", student)

# Update an existing item
student["marks"] = 90
print("After updating marks:", student)

# Remove an item
student.pop("age")
print("After removing age:", student)

# Display all keys
print("Keys:", student.keys())

# Display all values
print("Values:", student.values())

# Display all key-value pairs
print("Items:", student.items())

# Check if a key exists
print("Is name present?", "name" in student)

# Find the length of the dictionary
print("Total items:", len(student))

# Loop through the dictionary
print("Student Information:")
for key, value in student.items():
    print(key, ":", value)

# Copy the dictionary
student_copy = student.copy()
print("Copied Dictionary:", student_copy)
