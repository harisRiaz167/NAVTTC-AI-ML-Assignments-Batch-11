import numpy as np

def checkSum(a, b):
    
    result = a * b
    
    number = result.flatten()
    
    total = number.sum()
    
    if total % 2 == 0: # you can change the number
        return "Even"
    
    else:
        print("Total: ", total)
        return "Could not get even"

a = np.array([[2, 4, 6],
                [8, 10, 12],
                [14, 16, 18]]) # I wanted to practice and test it

b = np.array([[1, 3, 5],
               [7, 9, 11],
               [13, 15, 17]])

print(np.random.randint(1, 30, (3, 3, 3)))

# even[0], even[2] = even[2], even[0].copy() # Practice, no need to understand

print(checkSum(a, b))