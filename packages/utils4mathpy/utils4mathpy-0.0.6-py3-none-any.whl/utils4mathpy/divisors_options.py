class DivisorsOptions:
    """
    Class for divisors function options.

    Attributes:
    - limit (int): The maximum number of divisors to return.
    - reverse (bool): Whether to reverse the order of divisors.
    - include_self (bool): Whether to include the number itself as a divisor.
    - include_one (bool): Whether to include one as a divisor.
    """
    def __init__(self,
                 limit: int = 0,
                 reverse: bool = False,
                 include_self: bool = True,
                 include_one: bool = False):

        self._limit = limit
        self._reverse = reverse
        self._include_self = include_self
        self._include_one = include_one
    
    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, value: int):
        self._limit = value
    
    @property
    def reverse(self):
        return self._reverse
    
    @reverse.setter
    def reverse(self, value: bool):
        self._reverse = value

    @property
    def include_self(self):
        return self._include_self
    
    @include_self.setter
    def include_self(self, value: bool):
        self._include_self = value

    @property
    def include_one(self):
        return self._include_one
    
    @include_one.setter
    def include_one(self, value: bool):
        self._include_one = value
