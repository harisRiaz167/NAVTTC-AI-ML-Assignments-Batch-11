# Task:
Robot position Movement / When a Robot returns to its original position return True otherwise False.

def robot(moves: str) -> bool:
    position = 0  
    
    directions = {'U': 1, 'D': -1, 'L': -1, 'R': 1}
    
    for move in moves:
        position += directions[move]
        
    return position == 0

print(robot("UDLR"))
print(robot("UD"))
print(robot("R"))

#Task:
Problem statement You are given two strings, s and t.
String t is created by shuffling the characters of s and then adding one extra character.
Find and return the extra character.

s = "abcd"
t = "acbde"

o = []
for x in t:
    if x not in s:
        o.append(x)
print(o)
