a = input()

number  = {
    "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4", "FIV": "5",
    "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9", "ZER": "0",
    "1": "ONE", "2": "TWO", "3": "THR", "4": "FOU", "5": "FIV",
    "6": "SIX", "7": "SEV", "8": "EIG", "9": "NIN", "0": "ZER"
}

b = ""
c = ""
h1 = ""
h2 = ""
op = ""
res = ""
for i in range(len(a)):
    if a[i] == "+" or a[i] == "-" or a[i] == "*" or a[i] == "/":
        b = a[0:i]
        c = a[i+1:]
        op = a[i]
        break

for i in range(0,len(b),3):
    h1 += number[b[i:i+3]]
for i in range(0,len(c),3):
    h2 += number[c[i:i+3]]

if op == "+":
    v =str(int(h1) + int(h2))
elif op == "-":
    v = str(int(h1) - int(h2))
elif op == "*":
    v = str(int(h1) * int(h2))
elif op == "/":
    v = str(int(h1) // int(h2))

for i in range(len(v)):
    res += number[v[i]]

print(res)