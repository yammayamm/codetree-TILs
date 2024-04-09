n = int(input())
nums = list(map(int, input().split()))
cnt = list(map(int, input().split()))

#순열
lst = []
def dfs(tmp):
    global lst
    if len(tmp) == n-1:
        lst.append(tmp[:])
        return
    for i in range(len(cnt)):
        if cnt[i] > 0:
            cnt[i] -= 1
            tmp.append(i)
            dfs(tmp)
            cnt[i] += 1
            tmp.pop()
dfs([])

anslis = []
for per in lst:
    ans = nums[0]
    for i in range(n-1):
        if per[i] == 0:
            ans += nums[i+1]
        elif per[i] == 1:
            ans -= nums[i+1]
        elif per[i] == 2:
            ans *= nums[i+1]
    anslis.append(ans)
print(min(anslis), max(anslis))