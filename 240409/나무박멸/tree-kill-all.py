from copy import deepcopy

n, m, k, c = map(int, input().split()) # n : 격자크기, m : 년 수, k : 제초제 확산범위, c : 제초제 남아있는 년 수
pan = [ list(map(int, input().split())) for _ in range(n) ] # 나무 : 1~100, 빈칸 : 0, 벽 : -1
weedkiller = [ [0] * n for _ in range(n) ]
answer = 0 # 총 박멸한 나무의 그루 수
dx, dy = [0, 0, -1, 1], [-1, 1, 0, 0]


def tree_grow(): # 나무의 성장

    tmp = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if 1 <= pan[i][j]:

                for k in range(4):
                    mx = i + dx[k]
                    my = j + dy[k]

                    if 0 <= mx < n and 0 <= my < n:
                        if 1 <= pan[mx][my]:
                            tmp[i][j] += 1

    for i in range(n):
        for j in range(n):
            pan[i][j] += tmp[i][j]


def tree_spread(): # 나무의 확산

    tmp = deepcopy(pan)

    for i in range(n):
        for j in range(n):
            if 1 <= pan[i][j]:

                tree_amount = pan[i][j] # 번식할 숙주 나무의 양
                cnt = 0 # 번식이 가능한(벽, 다른 나무, 제초제 모두 없는 칸)의 개수
                for k in range(4):
                    mx = i + dx[k]
                    my = j + dy[k]

                    if 0 <= mx < n and 0 <= my < n:
                        if pan[mx][my] == 0 and weedkiller[mx][my] == 0:
                            cnt += 1


                if cnt != 0:
                    tree_spread_amount = tree_amount // cnt

                    for k in range(4):
                        mx = i + dx[k]
                        my = j + dy[k]

                        if 0 <= mx < n and 0 <= my < n:
                            if pan[mx][my] == 0 and weedkiller[mx][my] == 0:
                                tmp[mx][my] += tree_spread_amount

    return tmp

# 대각선 좌표
d_dx = [-1, -1, 1, 1]
d_dy = [-1, 1, -1, 1]
def tree_kill_xy(x, y): # 가장 많은 나무를 죽일 수 있는 위치를 찾는 함수
    global k_x, k_y, kill_amount

    value = pan[x][y] # 제초제로 죽일 수 있는 나무의 양

    for p in range(4):
        cur_x, cur_y = x, y
        for _ in range(k):

            mx = cur_x + d_dx[p]
            my = cur_y + d_dy[p]

            if not (0 <= mx < n and 0 <= my < n):
                break

            if pan[mx][my] <= 0:
                break

            if 1 <= pan[mx][my]:
                value += pan[mx][my]
                cur_x, cur_y = mx, my


    if kill_amount < value:
        k_x, k_y = x, y
        kill_amount = value


def tree_kill(x, y): # 나무를 죽이는 제초제를 뿌리는 함수.

    weedkiller[x][y] = c
    pan[x][y] = 0

    for p in range(4):
        cur_x, cur_y = x, y
        for _ in range(k):
            mx = cur_x + d_dx[p]
            my = cur_y + d_dy[p]

            if not (0 <= mx < n and 0 <= my < n):
                break

            if pan[mx][my] == -1: # 벽일때는 제초제를 안뿌려도 됨.
                break

            if pan[mx][my] == 0: # 빈칸일때는 제초제를 뿌리고 더이상 뿌리지 않음.
                weedkiller[mx][my] = c
                break

            if 1 <= pan[mx][my]:
                weedkiller[mx][my] = c
                pan[mx][my] = 0
                cur_x, cur_y = mx, my


def weedkiller_down():

    for i in range(n):
        for j in range(n):
            if weedkiller[i][j] > 0:
                weedkiller[i][j] -= 1

# m년 동안 총 박멸한 나무의 그루 수 구하기
for _ in range(m):

    # 1. 인접한 네 개의 칸 중 나무가 있는 칸의 수만큼 나무가 성장합니다. 성장은 모든 나무에게 동시에 일어납니다.
    tree_grow()

    # for i in pan:
    #     print(i)
    # print()

    # 2. 기존에 있었던 나무들은 인접한 4개의 칸 중 벽, 다른 나무, 제초제 모두 없는 칸에 번식을 진행합니다.
    pan = tree_spread()

    # for i in pan:
    #     print(i)
    # print()

    # 3. 각 칸 중 제초제를 뿌렸을 때 나무가 가장 많이 박멸되는 칸을 찾는다.
    k_x, k_y = 0, 0
    kill_amount = 0
    for i in range(n):
        for j in range(n):
            if pan[i][j] >= 1:
                tree_kill_xy(i, j)

    # print(k_x, k_y)
    # print(kill_amount)

    # 4. 제초제 시간을 줄여준다.
    weedkiller_down()

    # 5. 제초제를 살포한다.
    tree_kill(k_x, k_y)
    
    answer += kill_amount

print(answer)