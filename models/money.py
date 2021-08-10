from decimal import Decimal

MIN_AMOUNT = 0.01


class Money:
    """
    A class represented 'Money' - with two decimal places. Only necessary
    for this assigment magic methods implemented.
    """
    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return self.__str__()

    def __init__(self, value: (float, str)):
        self.value = Decimal(value).quantize(Decimal('0.01'))

    def __add__(self, other):
        return Money(self.value + other.value)

    def __sub__(self, other):
        return Money(self.value - other.value)

    def __eq__(self, other):
        return self.value - other.value < MIN_AMOUNT

    def __mul__(self, other):
        return Money(self.value * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __lt__(self, other):
        return self.value < other.value

    def __truediv__(self, other):
        try:
            # receive a proportion when dividing Money and Money
            return self.value / other.value
        except AttributeError:
            # receive a part of Money, dividing Money by int or float
            return Money(self.value / other)
