class Money:
    MIN_AMOUNT = 0.01

    def __str__(self):
        return f'Money: {self.value}'

    def __repr__(self):
        return self.__str__()

    def __init__(self, value: float):
        self.value = round(value, 2)

    def __add__(self, other):
        return Money(self.value + other.value)

    def __sub__(self, other):
        return Money(self.value - other.value)

    def __eq__(self, other):
        return self.value - other.value < self.MIN_AMOUNT

    def __mul__(self, other):
        return Money(self.value * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        return self.value < other.value

    def __truediv__(self, other):
        try:
            return self.value / other.value
        except AttributeError:
            return Money(self.value / other)