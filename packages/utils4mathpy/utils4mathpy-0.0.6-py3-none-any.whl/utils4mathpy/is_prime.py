from utils4mathpy import divisors, invalid_int_greater_than
from utils4mathpy.divisors_options import DivisorsOptions

def is_prime(n: int) -> bool:
    if not isinstance(n, int) or n <= 1:
        raise TypeError(invalid_int_greater_than(1))
    for i in divisors(n, DivisorsOptions(include_self = False)):
        if n % i == 0:
            return False
    return True
