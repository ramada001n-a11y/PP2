a = int(input())

for i in range(0,a+1,2):
    if i+1 != a and i != a:
        print(i, end=',')
    if i == a or i+1 == a:
        print(i)
