## Task 1: 
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

## Task 2:
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

## Task 3:
For each day, determine how many days you must wait until a warmer temperature occurs. If there is no future day with a warmer temperature, put 0.
T = [71, 72, 68, 71, 76, 80]

def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    ans = [0] * n
    hottest = 0

    
    for i in range(n - 1, -1, -1):
        current_temp = temperatures[i]
        
        if current_temp >= hottest:
            hottest = current_temp
            continue
        
        days_ahead = 1
        while temperatures[i + days_ahead] <= current_temp:
            days_ahead += ans[i + days_ahead]

        ans[i] = days_ahead

    return ans

print(daily_temperatures(T))
