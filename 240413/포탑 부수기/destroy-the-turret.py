from collections import deque

N,M,K = list(map(int, input().split()))
arr = [list(map(int, input().split())) for _ in range(N)]

top = {}
for i in range(N):
    for j in range(M):
        if arr[i][j] > 0:
            top[(i,j)] = [arr[i][j], 0]
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

def laser(ax, ay, tx, ty):
    q = deque()
    q.append((ax, ay, []))  # x, y, route
    visited = [[False] * M for _ in range(N)]
    visited[ax][ay] = True
    while q:
        x, y, route = q.popleft()
        for d in range(4):
            nx = (x + dx[d]) % N
            ny = (y + dy[d]) % M
            if visited[nx][ny]: continue
            if arr[nx][ny] == 0: continue

            # 타겟에 도달한 경우
            if nx == tx and ny == ty:
                arr[nx][ny] -= point
                top[(tx, ty)][0] -= point
                for rx, ry in route:  # 경로 추적
                    arr[rx][ry] -= half_point
                    top[(rx,ry)][0] -= half_point
                    attack[rx][ry] = True
                return True

            # 경로 체크
            tmp_route = route[:]
            tmp_route.append((nx, ny))
            visited[nx][ny] = True
            q.append((nx, ny, tmp_route))

    # 타겟이 도달하지 못하는 경우
    return False

def potan(ax,ay,tx,ty):
    arr[tx][ty] -= arr[ax][ay]
    top[(tx,ty)][0] -= arr[ax][ay]

    ddx = [-1,-1,0,1,1,1,0,-1]
    ddy = [0,1,1,1,0,-1,-1,-1]
    for d in range(8):
        nx = (tx+ddx[d]) % N
        ny = (ty+ddy[d]) % M
        if nx==ax and ny==ay:
            continue
        elif arr[nx][ny]>0:
            arr[nx][ny] -= half_point
            top[(nx,ny)][0] -= half_point
            attack[nx][ny] = True

for k in range(K):
    if len(top) <= 1:
        break
    attack = [[False] * M for _ in range(N)]
    # 1. 공격자 선정
    sort_top = sorted(top.items(), key=lambda x:(x[1][0],-x[1][1],-(x[0][0]+x[0][1]), -x[0][1]))
    ax, ay = sort_top[0][0]
    arr[ax][ay] = sort_top[0][1][0] + N + M
    point = arr[ax][ay]
    top[(ax, ay)][0] = point    # 공격력 바꾸기
    half_point = point // 2
    attack[ax][ay] = True
    top[(ax,ay)][1] = k+1 # 최근 공격 + 1
    # 2. 공격자의 공격
    tx, ty = sort_top[-1][0]
    attack[tx][ty] = True
    # [2-1]. 레이저 공격
    if not laser(ax,ay,tx,ty):
        # [2-2]. 포탄 공격
        potan(ax,ay,tx,ty)
    # [3,4] 포탑 부서짐, 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0:
                arr[i][j] = 0
                if (i,j) in top:
                    del top[(i,j)]
            elif not attack[i][j]:
                arr[i][j] += 1
                top[(i,j)][0] += 1
mx = 0
for i in range(N):
    mx = max(mx, max(arr[i]))
print(mx)