class Amount:
    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value


class InvoiceLine:
    def __init__(self, description, quantity, category, unit_price_net):
        self.description = description
        self.quantity = quantity
        self.category = category
        self.unit_price_net = unit_price_net


class Payment:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount


class Invoice:
    def __init__(self, invoice_lines, payments):
        self.invoice_lines = [InvoiceLine(**line) for line in invoice_lines]
        self.payments = [Payment(**payment) for payment in payments]
    def to_JSON(self):
        return self.categories_weight()
    @property
    def invoice_sum(self):
        # TODO: check if invoice lines summ is not equal to payments sum
        return sum([line.unit_price_net*line.quantity for line in self.invoice_lines])
    def categories_weight(self):
        x = {}
        for element in self.invoice_lines:
            try:
                x[element.category] += element.unit_price_net*element.quantity
            except KeyError:
                x[element.category] = element.unit_price_net*element.quantity
        return {key: value/self.invoice_sum for key, value in x.items()}
    def payments_categorisations(self):
        x = [
            {
                'id': payment.id,
                'categorisations': [
                    {
                        'category': key,
                        'net_amount': str(round(payment.amount*value, 2))
                    }
                    for key, value in self.categories_weight().items()
                ]
             }
            for payment in self.payments
        ]
        invoice_payment_sum, cat_payment_amount = 0, 0
        for payment in self.payments:
            for i in self.payments:
                if i.id == payment.id:
                    invoice_payment_sum = i.amount
            for index, value in enumerate(x):
                if value['id'] == payment.id:
                    payment_index = index
            cat_payment_amount = sum([float(item['net_amount']) for item in x[payment_index]['categorisations']])
            if invoice_payment_sum != cat_payment_amount:
                dif = round(invoice_payment_sum - cat_payment_amount, 2)
                if abs(dif) >= 0.01:
                    raise ValueError(f'Rounding error, diff: {dif}, lines: {len(self.invoice_lines)}, paymnts: {len(self.payments)}')
                else:
                    print(f'Very small dif {invoice_payment_sum - cat_payment_amount}')
        return x