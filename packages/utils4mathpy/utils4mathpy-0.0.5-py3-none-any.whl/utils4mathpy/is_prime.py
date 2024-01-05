from utils4mathpy import divisors, DivisorsOptions, invalidIntGreaterThan

def is_prime(n: int) -> bool:
    if not isinstance(n, int) or n <= 1:
        raise TypeError(invalidIntGreaterThan(1))
    for i in divisors(n, DivisorsOptions(include_self = False)):
        if n % i == 0:
            return False
    return True
