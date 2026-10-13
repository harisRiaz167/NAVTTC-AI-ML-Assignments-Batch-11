l = [1, 2, 2, 3, 2, 2, 1]
num = len(l) / 2
result = []

for i in range(len(l)):
    freq = 0
    for j in range(len(l)):
        if l[i] == l[j]:
            freq += 1
    if freq > num:
        result.append(l[i])

print(result[0]) 