import math

n = int(input())

r = math.sqrt(n)
a = math.ceil(r)

b2 = a**2 - n

while b2 < 0 or math.sqrt(b2) % 1 != 0:
    a += 1
    b2 = a**2 - n

b = int(math.sqrt(b2))
f1 = a - b
f2 = a + b

print(f1, f2)
