T = [71, 72, 68, 71, 76, 80]

OL = [1, 3, 1, 1, 0]

for i in range(len(OL)):
    if OL[i] == 1:
        print(T[i], "connection is True")
    elif OL[i] == 3:
        print(T[i], "Condition is 3")
    else:
        print(T[i], "Condition is False")
