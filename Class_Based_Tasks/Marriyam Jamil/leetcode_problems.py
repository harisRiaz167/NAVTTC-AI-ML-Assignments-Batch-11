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
#Task: For each day, determine how many days you must wait until a warmer temperature occurs. If there is no future day with a warmer temperature, put 0.
T=[71,72,68,71,76,80]
output_list=[]
index=0
for x in range(0,len(T)):
    if x==len(T)-1: 
        output_list.append(0) 
    else: for y in range(x+1,len(T)):
        if T[y]>T[x]:
            s=T[y]-T[x] 
            index+=1 
            output_list.append(index) 
            index=0 
            break 
        else: 
            index+=1 
print(output_list) 
# Output: [1, 3, 1, 1, 1, 0]
