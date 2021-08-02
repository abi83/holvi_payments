from .money import Money


class InvoiceLine:
    def __init__(self,
                 description: str,
                 quantity: int,
                 category: str,
                 unit_price_net: str):
        self.description: str = description
        self.quantity: int = quantity
        self.category: str = category
        self.unit_price_net: Money = Money(float(unit_price_net))
