from copy import deepcopy
from collections import deque
K, M = list(map(int, input().split()))
board = [list(map(int, input().split())) for _ in range(5)]
nums = list(map(int, input().split()))

def get_score(board_copy):
    #bfs
    score = 0
    global path
    board_copy2 = deepcopy(board_copy)
    for i in range(5):
        for j in range(5):
            curr = board_copy2[i][j]
            if curr != 0:
                queue = deque([[i,j]])
                board_copy2[i][j] = 0
                temp = 1
                temp_path = [[i,j]]
                while queue:
                    ii,jj = queue.popleft()
                    for di,dj in ((0,-1),(0,1),(1,0),(-1,0)):
                        ni,nj = ii+di, jj+dj
                        if 0<=ni<5 and 0<=nj<5 and board_copy2[ni][nj] == curr:
                            temp += 1
                            queue.append([ni,nj])
                            board_copy2[ni][nj] = 0
                            temp_path.append([ni,nj])
                if temp>=3:
                    score += temp
                    path.extend(temp_path)
    return score
answer = 0
for _ in range(K):
    all_score = []
    for i in range(3):
        for j in range(3):
            three = board[i:i+3]
            three[0] = three[0][j:j+3]
            three[1] = three[1][j:j+3]
            three[2] = three[2][j:j+3]
            rotate_temp = deepcopy(three)
            for rotate in (90,180,270):
                rotate_temp = list(map(list, zip(*rotate_temp[::-1])))
                board_copy = deepcopy(board)
                board_copy[i][j:j+3] = rotate_temp[0]
                board_copy[i+1][j:j+3] = rotate_temp[1]
                board_copy[i+2][j:j+3] = rotate_temp[2]
                path = []
                score = get_score(board_copy)
                if score>0:
                    all_score.append([score, rotate, j,i,path])
    # 유물을 획득할 수 없었다면 모든 탐사는 그 즉시 종료
    if len(all_score) == 0:
        break

    bs, br, bj, bi, path = sorted(all_score, key=lambda x: (-x[0],x[1],x[2],x[3]))[0]
    answer += bs
    # 다시 돌리기
    three = board[bi:bi+3]
    three[0] = three[0][bj:bj+3]
    three[1] = three[1][bj:bj+3]
    three[2] = three[2][bj:bj+3]
    for rotate in (90,180,270):
        three = list(map(list, zip(*three[::-1])))
        board[bi][bj:bj+3] = three[0]
        board[bi+1][bj:bj+3] = three[1]
        board[bi+2][bj:bj+3] = three[2]
        if rotate == br:
            break
    while True:
        # path에 있는 유물 replace (열 작은 순, 행 큰 순)
        path.sort(key=lambda x:(x[1], -x[0]))
        for bpi,bpj in path:
            board[bpi][bpj] = nums[0]
            nums = nums[1:]
        # 유물 연쇄 획득
        path = []
        score = get_score(board)
        answer += score
        if score==0:
            break
print(answer)