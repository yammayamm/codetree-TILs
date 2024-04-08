n = int(input())
work = [list(map(int, input().split())) for _ in range(n)]

visited = [False for _ in range(len(work))]
result = 0
def dfs(idx, money):
    global result
    if idx >= n:
        result = max(result, money)
        return
    for i in range(idx, len(work)):
        if not visited[i] and i+work[i][0] <= n:
            visited[i] = True
            dfs(i+work[i][0], money + work[i][1])
            visited[i] = False
dfs(0, 0)
print(result)