from collections import defaultdict

nums = [1, 1, 1, 2, 3]
k = 2

groups = defaultdict(list)

for num in nums:
    groups[num].append(num)

o = list(groups.values())

result = [group[0] for group in o[:k]]

print(result)