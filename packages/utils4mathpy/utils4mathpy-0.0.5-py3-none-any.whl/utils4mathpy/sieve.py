from math import sqrt, ceil

def sieve(n: int) -> list[int]:
    numbers = [i for i in range(2, n + 1)]
    for i in range(2, ceil(sqrt(n))):
        if numbers[i - 2] != 0:
            for j in range(i, ceil(n / i)):
                numbers[j * i - 2] = 0
    return [i for i in numbers if i != 0]
