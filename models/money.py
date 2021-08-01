class Money:
    MIN_AMOUNT = 0.01

    def __init__(self, value: float):
        self.value = round(value, 2)

    def __add__(self, other):
        return Money(self.value + other.value)

    def __sub__(self, other):
        return Money(self.value - other.value)

    def __eq__(self, other):
        return self.value - other.value < self.MIN_AMOUNT



