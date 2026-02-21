def f(a):
    for i in range((len(a))):
        if int(a[i])/2 != (int(a[i]))//2:
            return "Not valid"
        if i == len(a)-1: 
            return "Valid"

a = input()
print(f(a))