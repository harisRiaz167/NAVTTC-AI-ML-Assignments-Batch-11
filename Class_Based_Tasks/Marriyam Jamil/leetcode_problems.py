# Task: Robot position Movement / When a Robot returns to its original position return True otherwise False.
sum=0
robot_mov1=input("Where Robot move")
dictt={'U':1,'D':-1,'R':1,'L':-1}
for x in robot_mov1:
    sum+=dictt[x]
if sum==0:
    print ("True")
else:
    print ("False")

#Task: Problem statement You are given two strings, s and t. String t is created by shuffling the characters of s and then adding one extra character. Find and return the extra character.
s='abcd'
t='acded'
lis=[]
for x in t:
    if x in s:
        if x not in lis:
           lis.append(x)
        else:
            print(x)
    else:
        print(x)
