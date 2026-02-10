a = int(input())
b = list(map(int, input().split()))
c = b[0]
i = 0
while a > i:
    if b[i] > c:
        c = b[i]
    i += 1

print(c)