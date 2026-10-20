def missing_number(L):
    n = len(L)
    num = n * (n + 1) // 2
    num2 = sum(L)
    return num - num2


print(missing_number([0, 1, 3]))
# print(missing_number([0, 1, 2]))
# print(missing_number([1, 2, 3, 5]))
# print(missing_number([4, 4]))

print(missing_number([6]))