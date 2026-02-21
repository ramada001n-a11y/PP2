def f():
    n = int(input())
    while n :
        if n / 2 == n // 2:
            n /=2
            continue
        elif n / 5 == n // 5:
            n /= 5
            continue
        elif n / 3 == n // 3:
            n /= 3
            continue
        elif n == 1:
            print("Yes")
            break
        else: 
            print("No")
            break

f()