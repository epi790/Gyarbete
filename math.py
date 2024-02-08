from decimal import *

getcontext().prec = 382

x = Decimal(64**64)

prod = 1

for i in range(1,2301):
    prod *= (x - i) / x

i = 0

while True:
    result = 1 - (prod**(i * (3155760*10**100)))
    print(result)
    if result > 0.009:
        print(f" {i} * 10^100 years")
        print(1 - (prod**((i - 1) * 3155760*10**100)))
        print(1 - (prod**((i) * 3155760*10**100)))
        break
    i += 1

