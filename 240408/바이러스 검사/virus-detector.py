import math
n = int(input())
cus = list(map(int, input().split()))
poss = list(map(int, input().split()))

cnt = 0
for c in cus:
    if c - poss[0] <= 0:
        cnt+=1
    else:
        cnt += 1 + math.ceil((c-poss[0]) / poss[1])
print(cnt)