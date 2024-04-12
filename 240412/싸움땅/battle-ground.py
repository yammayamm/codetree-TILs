n,m,k = list(map(int, input().split())) #격자크기, 플레이어 수, 라운드수
board = [list(map(int, input().split())) for _ in range(n)]
for i in range(n):
    for j in range(n):
        if board[i][j] == 0:
            board[i][j] = []
        else:
            board[i][j] = [board[i][j]]
player = [list(map(int, input().split())) for _ in range(m)] #x,y,d,s
gun = [0 for _ in range(m)]
point = [0 for _ in range(m)]
player_loc = {}
for i in range(len(player)):
    player[i][0] -= 1
    player[i][1] -= 1
    point[i] = 0
    player_loc[(player[i][0],player[i][1])] = i
dx = [-1,0,1,0] # 상,우,하,좌
dy = [0,1,0,-1]

def fight(p1,p2):
    p1_score = player[p1][3] + gun[p1]
    p2_score = player[p2][3] + gun[p2]
    if p1_score > p2_score:
        winner = p1
    elif p1_score < p2_score:
        winner = p2
    elif player[p1][3] > player[p2][3]:
        winner = p1
    else:
        winner = p2
    point[winner] += abs(p1_score - p2_score)
    # [2-2-2] 진 플레이어는 가지고 있는 총을 내려놓고, 방향대로 이동
    loser = p1 if winner==p2 else p2
    if gun[loser]>0:
        x,y = player[loser][:2]
        board[x][y].append(gun[loser])
        gun[loser] = 0
    # 이동
    x,y,d,s = player[loser]

    for _ in range(4):      # 만약 이동하려는 칸에 다른 플레이어가 있거나 격자 범위 밖인 경우에는 오른쪽으로 90도씩 회전하여 빈 칸이 보이는 순간 이동
        nx,ny = x+dx[d], y+dy[d]
        if nx<0 or nx>=n or ny<0 or ny>=n or (nx,ny) in player_loc:
            d = (d + 1) % 4
        else:
            break
    player[loser] = [nx,ny,d,s]
    player_loc[(x,y)] = winner
    player_loc[(nx,ny)] = loser
    # 해당 칸에 총이 있으면 총 획득하고 나머지 내려놓음
    if board[nx][ny]:
        mx = max(board[nx][ny])
        gun[loser] = mx
        board[nx][ny].remove(mx)

    # [2-2-3] 이긴 플레이어는 떨어져있는 총과 원래 있던 총 중 가장 공격력 높은 총 획득
    x, y, d, s = player[winner]
    if gun[winner] ==0 and board[x][y]:
        gun[winner] = board[x][y][0]
        board[x][y] = []
    elif board[x][y]:
        mx = max(board[x][y])
        if gun[winner] < mx:
            board[x][y].append(gun[winner])
            gun[winner] = mx
            board[x][y].remove(mx)
for _ in range(k):
    for i in range(len(player)):
        # [1-1] 첫번째 플레이어부터 방향으로 한 칸 이동
        x,y,d,s = player[i]
        nx, ny = x+dx[d], y+dy[d]
        if nx<0 or nx>=n or ny<0 or ny>=n:
            d = (d+2) % 4       #반대방향으로
            nx, ny = x+dx[d], y+dy[d]
        player[i] = [nx,ny,d,s]
        # [2-1] 플레이어 없으면 이동하고 총 확인
        if (nx,ny) not in player_loc:
            if board[nx][ny]: # 칸에 총이 있는 경우
                mx = max(board[nx][ny])
                if mx > gun[i]: #더 강한 총이면
                    if gun[i] > 0:
                        board[nx][ny].append(gun[i])
                    board[nx][ny].remove(mx)
                    gun[i] = mx
            del player_loc[(x,y)]
            player_loc[(nx,ny)] = i
        # [2-2-1] 이동한 방향에 플레이어가 있으면 싸움
        else:
            del player_loc[(x, y)]
            fight(player_loc[(nx,ny)], i)
print(*point)