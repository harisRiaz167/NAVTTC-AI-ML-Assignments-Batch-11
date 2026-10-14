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

