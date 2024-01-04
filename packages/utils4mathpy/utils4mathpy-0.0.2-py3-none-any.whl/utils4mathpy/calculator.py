import math

class GeneratorOptions:

    def __init__(self, limit: int = 0, reverse: bool = False):
        self.limit = limit
        self.reverse = reverse

def divisors(n: int, opts: GeneratorOptions) -> list[int]:
    
    '''
    Returns a list of divisors of a given number.

    Parameters
    ----------
    n : int
        The number to be factored.
    opts : GeneratorOptions
        The options for the generator.

    Returns
    -------
    list
        A list of divisors of a given number.

    Examples
    --------
    >>> divisors(20)
    [2, 4, 5, 10]
    >>> divisors(20, GeneratorOptions(limit = 1))
    [2]
    >>> divisors(20, GeneratorOptions(limit = 1, reverse = True))
    [10]
    '''

    # numbers = []

    # for i in [i for i in range(2, n)]:
    #     if (n % i == 0):
    #         numbers.append(i)

    numbers = [i for i in range(2, n) if n % i == 0]

    if (opts.reverse == True):
        numbers.sort(reverse = True)

    if (opts.limit == 0):
        return numbers
    
    return numbers[:opts.limit]

def is_prime(x: int):
    for i in divisors(x):
        if(x % i == 0): return False
    return True

def factorize(n: int):
    numbers = divisors(n, limit = 1)
    for i in numbers:
        None

def sieve(n: int):
    numbers = [i for i in range(2, n + 1)]
    for i in range(2, math.ceil(math.sqrt(n))):
        if numbers[i - 2] != 0:
            for j in range(i, math.ceil(n / i)):
                numbers[j * i - 2] = 0
    return [i for i in numbers if i != 0]
