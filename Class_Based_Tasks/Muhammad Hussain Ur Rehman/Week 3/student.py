students = [
    {
        "name": "Ali Khan",
        "roll_no": 1,
        "password": "python1",
        "grade": "A",
        "marks": 450,
        "class": "10th",
        "section": "A",
        "subjects": {
            "English": 85,
            "Math": 92,
            "Physics": 88,
            "Chemistry": 90,
            "Computer": 95
        }
    },
    {
        "name": "Ahmed Raza",
        "roll_no": 2,
        "password": "python2",
        "grade": "B+",
        "marks": 410,
        "class": "10th",
        "section": "A",
        "subjects": {
            "English": 78,
            "Math": 85,
            "Physics": 82,
            "Chemistry": 80,
            "Computer": 85
        }
    },
    {
        "name": "Hassan Ali",
        "roll_no": 3,
        "password": "python3",
        "grade": "A-",
        "marks": 430,
        "class": "10th",
        "section": "B",
        "subjects": {
            "English": 82,
            "Math": 90,
            "Physics": 85,
            "Chemistry": 86,
            "Computer": 87
        }
    },
    {
        "name": "Usman Tariq",
        "roll_no": 4,
        "password": "python4",
        "grade": "B",
        "marks": 385,
        "class": "10th",
        "section": "B",
        "subjects": {
            "English": 75,
            "Math": 78,
            "Physics": 77,
            "Chemistry": 80,
            "Computer": 75
        }
    }
]

passwords = []
for student in students:
    passwords.append(student['password'])

roll_num_array = []
for student in students:
    roll_num_array.append(student['roll_no'])

def login():
    print("========= Enter Password =========")
    for student in students:
        pass_user = input("Please enter password : ")
        if(pass_user not in passwords):
            print("⚠️ Password is worng! Try again...")
            continue
        else:
            print("✔️ login Successful ")
            break

def roll_no():
    print("========= Enter Rollno =========")
    for i in students:
        roll_number = int(input("Please enter Roll no : "))
        if(roll_number not in roll_num_array):
            print("⚠️ Roll no is worng! Try again...")
            continue
        else:
            for key,student in enumerate(students):
                if(student['roll_no'] == roll_number):
                    print("================== details =================== ")
                    print("Name:", student["name"])
                    print("Roll No:", student["roll_no"])
                    print("Grade:", student["grade"])
                    print("Class:", student["class"])
                    print("Section:", student["section"])
                    print("Subjects:", student["subjects"])
                    print("Marks:", student["marks"])
                    break
                else:
                    continue
            break

login()
roll_no()
            
        