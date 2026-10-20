from collections import defaultdict

L = ["ate", "eat", "tea", "bat", "nat", "tan"]

groups = defaultdict(list)

for word in L:
    key = "".join(sorted(word))
    groups[key].append(word)

o = list(groups.values())

print(o)