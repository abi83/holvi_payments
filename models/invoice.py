from .incoice_line import InvoiceLine
from .payment import Payment
from .money import Money


class Invoice:
    def __init__(self, invoice_lines, payments):
        self.invoice_lines: list = [InvoiceLine(**line)
                                    for line in invoice_lines]
        self.payments: list = [Payment(**payment) for payment in payments]
        self._invoice_sum_cached: Money = Money(0)
        self._categories_sum: dict = {}
        self._categories_proportions: dict = {}
        self.categories_limit: dict = self.categories_sum

    @property
    def payments_sum(self) -> Money:
        return sum(
            (payment.amount for payment in self.payments),
            Money(0))

    @property
    def invoice_sum(self) -> Money:
        if self._invoice_sum_cached == Money(0):
            self._invoice_sum_cached = sum(
                (
                    line.unit_price_net * line.quantity
                    for line in self.invoice_lines
                ), Money(0))
        return self._invoice_sum_cached

    @property
    def categories_sum(self) -> dict:
        if not self._categories_sum:
            categories_sum = {}
            for element in self.invoice_lines:
                try:
                    categories_sum[element.category] += (
                        element.unit_price_net * element.quantity)
                except KeyError:
                    categories_sum[element.category] = (
                        element.unit_price_net * element.quantity)
            self._categories_sum = categories_sum
        return self._categories_sum

    @property
    def categories_proportions(self) -> dict:
        self._categories_proportions = {
            category: category_sum / sum(
                (x for x in self.categories_limit.values()), Money(0))
            for category, category_sum in self.categories_limit.items()
        }
        return self._categories_proportions

    def payments_categorisations(self) -> None:
        for payment in self.payments:
            self.categories_limit = payment.categorise_payment(
                self.categories_proportions,
                self.categories_limit)
