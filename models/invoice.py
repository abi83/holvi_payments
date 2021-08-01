from .incoice_line import InvoiceLine
from .payment import Payment
from .money import Money


class Invoice:
    def __init__(self, invoice_lines, payments):
        self.invoice_lines = [InvoiceLine(**line) for line in invoice_lines]
        self.payments = [Payment(**payment) for payment in payments]
        self._invoice_sum_cached = None
        self._categories_sum = None
        self._categories_proportions = None
        self.categories_limit = self.categories_sum

    @property
    def payments_sum(self) -> float:
        return sum((payment.amount for payment in self.payments), start=Money(0))

    @property
    def invoice_sum(self) -> float:
        if self._invoice_sum_cached is None:
            self._invoice_sum_cached = sum((
                    line.unit_price_net * line.quantity
                    for line in self.invoice_lines
                ), start=Money(0))
        return self._invoice_sum_cached

    @property
    def categories_sum(self) -> dict:
        if self._categories_sum is None:
            categories_sum = {}
            for element in self.invoice_lines:
                try:
                    categories_sum[element.category] = categories_sum[element.category] + element.unit_price_net * element.quantity
                except KeyError:
                    categories_sum[element.category] = (
                            element.unit_price_net * element.quantity)
            self._categories_sum = categories_sum
        return self._categories_sum

    @property
    def categories_proportions(self) -> dict:
        if self._categories_proportions is None:
            self._categories_proportions = {
                category: category_sum / self.invoice_sum
                for category, category_sum in self.categories_sum.items()
            }
        return self._categories_proportions

    def payments_categorisations(self):
        for payment in self.payments:
            self.categories_limit = payment.categorise_payment(self.categories_proportions, self.categories_limit)
