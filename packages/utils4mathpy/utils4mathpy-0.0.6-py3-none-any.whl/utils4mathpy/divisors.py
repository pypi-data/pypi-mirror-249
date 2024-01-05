from utils4mathpy import invalid_int_greater_than

from utils4mathpy.divisors_options import DivisorsOptions

def divisors(n: int, opts: DivisorsOptions = None) -> list[int]:
    if not isinstance(n, int) or n <= 1:
        raise TypeError(invalid_int_greater_than(1))
    opts = opts or DivisorsOptions()
    numbers = []
    if opts.include_one is True:
        numbers += [1]
    numbers += [i for i in range(2, n) if n % i == 0]
    if opts.include_self is True:
        numbers.append(n)
    if opts.reverse is True:
        numbers.sort(reverse = True)
    if opts.limit == 0:
        return numbers
    return numbers[:opts.limit]
