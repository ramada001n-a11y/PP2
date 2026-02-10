a = int(input())
b = list(map(int, input().split()))

c = b.sort(reverse=True)


for i in range(1, 11):
    print(i, end=' ')