
def dailyTemperatures(arr):
    stack = []
    n = len(arr)
    ans = [0] * n

    stack.append(n - 1)
    ans[n - 1] = 0

    for i in range(n - 2, -1, -1):
        while stack:
            top = stack[-1]

            if arr[i] >= arr[top]:
                stack.pop()
            else:
                ans[i] = top - i
                break

        if not stack:
            ans[i] = 0

        stack.append(i)

    return ans


arr = [73, 74, 75, 71, 69, 72, 76, 73]
print(dailyTemperatures(arr))
