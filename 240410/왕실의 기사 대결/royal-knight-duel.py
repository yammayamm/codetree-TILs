L,N,Q = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(L)]
sold = [list(map(int, input().split())) for _ in range(N)] #r,c,h,w,k
order = [list(map(int, input().split())) for _ in range(Q)]

dx = [-1,0,1,0] # 위,오,아,왼 (0,1,2,3)
dy = [0,1,0,-1]

sold_map = [[0 for _ in range(L)] for _ in range(L)]

sold_dic = {}
idx = 1
for r,c,h,w,k in sold:
    for i in range(h):
        for j in range(w):
            sold_map[r+i-1][c+j-1] = idx
            if idx not in sold_dic:
                sold_dic[idx] = [[r+i-1,c+j-1]]
            else:
                sold_dic[idx].append([r+i-1,c+j-1])
    idx += 1

def check(i,d):
    global stack
    #visited = [False for _ in range(len(sold))]
    for j in sold_dic[i]:
        # if not visited[i-1]:
        #     stack.extend(sold_dic[i])
        #     visited[i-1] = True
        stack.append(j)
        nx, ny = j[0]+dx[d], j[1]+dy[d]
        if nx<0 or nx>=L or ny<0 or ny>=L or board[nx][ny]==2: # 벽이면 이동 못함
            return False
        elif sold_map[nx][ny] in [0,i]: # 자기자신이거나 빈칸이면
            continue
        else:
            if not check(sold_map[nx][ny], d):
                return False
    return True

def move(i,d,stack): # (0,-1)
    stack = sorted(stack, key=lambda x:(dx[d]* x[0],dy[d] * x[1]))
    move_loc = []
    while stack:
        x,y = stack.pop()
        nx,ny = x+dx[d], y+dy[d]
        num = sold_map[x][y]
        sold_dic[num].pop()
        sold_dic[num] = [[nx,ny],*sold_dic[num]]
        sold_map[nx][ny] = num
        sold_map[x][y] = 0
        if num!=i:
            move_loc.append([nx,ny])
    # 데미지 계산
    for j in move_loc:
        num = sold_map[j[0]][j[1]]
        if board[j[0]][j[1]] == 1: # 기사가 함정에 들어가면
            damage_cnt[num-1] += 1
    for k in range(len(sold)):
        if sold[num-1][-1] <= damage_cnt[num-1]: # 체력이 소진되면 사라짐
            damage_cnt[num-1] = 0
            for j in sold_dic[num]:
                sold_map[j[0]][j[1]] = 0
            sold_dic[num] = []
    return
damage_cnt = [0 for _ in range(len(sold))]
for i,d in order: # 3,3(왼쪽)
    stack = []
    if check(i,d):
        move(i,d,stack)
print(sum(damage_cnt))