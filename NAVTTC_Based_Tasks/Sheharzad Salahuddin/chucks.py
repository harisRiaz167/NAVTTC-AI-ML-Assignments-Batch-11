L = [1, 3, 5, 6]
T = 3

found = False
for i in range(len(L)):
    for j in range(i + 1, len(L)):
        if L[i] + L[j] == T:
            print([i, j])
            found = True

if not found:
    print("No pair found")
