import copy
n,m,kk,c = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(n)]

for i in range(n):
    for j in range(n):
        if board[i][j] == -1:
            board[i][j] = -999999
dx = [0,0,-1,1]
dy = [-1,1,0,0]
vx = [1,1,-1,-1] # 대각선
vy = [1,-1,1,-1]
ans = 0

for _ in range(m):
    # 1. 나무의 성장
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                tmp = 0
                for k in range(4):
                    if 0<=i+dx[k]<n and 0<=j+dy[k]<n and board[i+dx[k]][j+dy[k]] > 0:
                        tmp += 1
                board[i][j] += tmp
            if -999999<board[i][j]<0:
                board[i][j] += 1
    # 2. 나무의 번식
    new_board = copy.deepcopy(board)
    for i in range(n):
        for j in range(n):
            if board[i][j] > 0:
                tmp = []
                for k in range(4):
                    if 0<=i+dx[k]<n and 0<=j+dy[k]<n and board[i+dx[k]][j+dy[k]] == 0:
                        tmp.append([i+dx[k],j+dy[k]])
                if len(tmp)>=1:
                    for k in tmp:
                        new_board[k[0]][k[1]] += board[i][j] // len(tmp)
    board = new_board
    # 3. 제초제
    die_tree = [0,0,0]
    for i in range(n):
        for j in range(n):
            if board[i][j] > -1:
                die = board[i][j]
                for k in range(4):
                    for l in range(kk):
                        if 0<=i+vx[k]*(l+1)<n and 0<=j+vy[k]*(l+1)<n and board[i+vx[k]*(l+1)][j+vy[k]*(l+1)] not in [-999999, 0]:
                            die += board[i+vx[k]*(l+1)][j+vy[k]*(l+1)]
                        else:
                            break
                if die > die_tree[0]:
                    die_tree = [die,i,j]
    ans += die_tree[0]
    board[die_tree[1]][die_tree[2]] = -c -1
    for k in range(4):
        for l in range(kk):
            if 0<=die_tree[1]+vx[k]*(l+1)<n and 0<=die_tree[2]+vy[k]*(l+1)<n and board[die_tree[1]+vx[k]*(l+1)][die_tree[2]+vy[k]*(l+1)] not in [-999999, 0]:
                board[die_tree[1]+vx[k]*(l+1)][die_tree[2]+vy[k]*(l+1)] = -c-1
            else:
                break
print(ans)