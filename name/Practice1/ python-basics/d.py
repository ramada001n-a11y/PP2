a = input().split()
b = 0

for i in range(0, len(a)):
    if a[i].isdigit():
        b = a[i]
        if (b < a[i]):
            b = a[i]

print(b)