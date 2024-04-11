from collections import deque

n,m = list(map(int, input().split())) # 격자 크기, 사람 수
board = [list(map(int, input().split())) for _ in range(n)]
store = [list(map(int, input().split())) for _ in range(m)]
person = {}

camp = []
for i in range(n):
    for j in range(n):
        if board[i][j] == 1:
            camp.append([i,j])
for i in range(m):
    store[i] = [store[i][0]-1, store[i][1]-1]
    board[store[i][0]][store[i][1]] = 2

d=[(-1,0),(0,-1),(0,1),(1,0)]
visited=[[0]*n for _ in range(n)]
step = [[0] * n for _ in range(n)]
def bfs(sy,sx): # bfs 시작 좌표를 매개변수로 받아옴
    # visited, step 값을 전부 초기화합니다.
    for i in range(n):
        for j in range(n):
            visited[i][j] = 0
            step[i][j] = 0
    q = deque()
    q.append((sy, sx))
    visited[sy][sx] = 1
    while q:
        y, x = q.popleft()
        for dy, dx in d:
            Y = y + dy
            X = x + dx
            if 0 <= Y < n and 0 <= X < n and not visited[Y][X] and board[Y][X] != -1:
                visited[Y][X] = 1
                step[Y][X] = step[y][x] + 1
                q.append((Y, X))

def enterBaseCamp(time):
    #global m,n,d,board,person
    cy,cx=store[time]
    bfs(cy, cx)
    dist = 1e9  # 최단거리값
    by, bx = -1, -1
    for i in range(n):
        for j in range(n):
            # 방문 가능한 베이스 캠프 중 거리가 가장 가까운 위치를 찾기
            if visited[i][j] and board[i][j] == 1 and dist > step[i][j]:
                dist = step[i][j]
                by,bx = i, j
    person[time]=[by,bx]
    board[by][bx]=-1

idx = 0
while True:
    # [1] 가고 싶은 편의점 방향으로 1칸 이동 (최단 거리로 상,좌,우,하 순)
    # [1-1] 4방향 최단거리 구하기
    dist = []
    for key in list(person.keys()):
        pi,pj = person[key]
        si,sj = store[key]
        bfs(si,sj)
        dist = 1e9
        ty, tx = -1, -1 
        for dx,dy in d:
            ni,nj = pi+dx, pj+dy
            if 0<=ni<n and 0<=nj<n and visited[ni][nj] and dist > step[ni][nj]:
                ty, tx =ni,nj
                dist = step[ni][nj]
        person[key] = [ty, tx]
        # 편의점 도착시 -1로 바꿈
        if person[key] == store[key]:
            board[si][sj] = -1
            del person[key]
    # [3-1] 가고 싶은 편의점과 가장 가까운 베이스캠프를 구해서 이동
    if idx < m:
        enterBaseCamp(idx) 
        # dist = 1e9
        # short_camp = 0
        # si,sj = store[idx][0], store[idx][1]
        # bfs(si,sj)
        # by, bx = -1, -1
        # for i in range(len(camp)):
        #     if camp[i] == -1:
        #         continue
        #     ci, cj = camp[i][0], camp[i][1]
        #     if visited[] abs(si - ci) + abs(sj-cj) < dist:
        #         dist = abs(si - ci) + abs(sj-cj)
        #         short_camp = i
        # person[idx] = camp[short_camp]
        # board[camp[short_camp][0]][camp[short_camp][1]] = -1
        # camp[short_camp] = -1
    idx+= 1
    if len(person) == 0:
        break
print(idx)