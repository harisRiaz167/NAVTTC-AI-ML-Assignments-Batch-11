from collections import Counter

class Solution:
    def findTheDifference(self, s: str, t: str) -> str:
        count_s = Counter(s)
        result = ""

        for char in reversed(t):
            if count_s[char] > 0:
                count_s[char] -= 1
            else:
                result += char

        return result


s = "abcd"
t = "acded"

solution = Solution()
print(solution.findTheDifference(s, t))