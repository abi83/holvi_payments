class InvoiceLine:
    def __init__(self, description, quantity, category, unit_price_net):
        self.description = description
        self.quantity = quantity
        self.category = category
        self.unit_price_net = unit_price_net


class Payment:
    def __init__(self, id, amount):
        id = id
        amount = amount
