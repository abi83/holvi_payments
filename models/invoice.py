from .incoice_line import InvoiceLine
from .payent import Payment


class Invoice:
    def __init__(self, invoice_lines, payments):
        self.invoice_lines = [InvoiceLine(**line) for line in invoice_lines]
        self.payments = [Payment(**payment) for payment in payments]
        self._invoice_sum_cached = None
        self._categories_proportions = None

    @property
    def invoice_sum(self):
        if self._invoice_sum_cached is None:
            self._invoice_sum_cached = round(sum([
                line.unit_price_net * line.quantity for line in self.invoice_lines
            ]), 2)
        return self._invoice_sum_cached

    @property
    def categories_proportions(self):
        if self._categories_proportions is None:
            categories_sum = {}
            for element in self.invoice_lines:
                try:
                    categories_sum[element.category] += element.unit_price_net * element.quantity
                except KeyError:
                    categories_sum[element.category] = element.unit_price_net * element.quantity
            self._categories_proportions = {key: value/self.invoice_sum for key, value in categories_sum.items()}
        return self._categories_proportions

    @staticmethod
    def fix_mistake(payment_obj, mistake):
        fixes_number = abs(int(mistake / 0.01))
        fixes_value = round(mistake / fixes_number, 2)
        max_categories = [{'index': 0, 'net_amount': payment_obj['categorisations'][0]['net_amount']}]
        for index, item in enumerate(payment_obj['categorisations']):
            if item['net_amount'] > max([el['net_amount'] for el in max_categories]):
                max_categories.append({'index': index, 'net_amount': item['net_amount']})
                max_categories.sort(key=lambda item: item['net_amount'])
                max_categories.pop(0)
        for index in [el['index'] for el in max_categories]:
            payment_obj['categorisations'][index]['net_amount'] = round(
                payment_obj['categorisations'][index]['net_amount'] - fixes_value, 2)
        return payment_obj

    @staticmethod
    def calculate_mistake(payment_obj, right_value):
        return round(sum([category['net_amount'] for category in payment_obj['categorisations']]) - right_value, 2)

    def payments_categorisations(self):
        categorisation = []
        for payment in self.payments:
            categorized_payment = {
                'id': payment.id,
                'categorisations': [
                    {
                        'category': key,
                        'net_amount': round(payment.amount * value, 2)
                    }
                    for key, value in self.categories_proportions.items()
                ],
            }
            mistake = self.calculate_mistake(categorized_payment, payment.amount)
            if abs(mistake) >= 0.01:
                mistake_after_fix = mistake
                while abs(mistake_after_fix) >= 0.01:
                    categorized_payment = self.fix_mistake(categorized_payment, mistake_after_fix)
                    mistake_after_fix = self.calculate_mistake(categorized_payment, payment.amount)
            self.validate_output(categorized_payment, payment.amount)
            categorisation.append(categorized_payment)
        return categorisation

    def validate_output(self, data, right_value):
        mistake = self.calculate_mistake(data, right_value)
        if abs(mistake) >= 0.01:
            raise ValueError(f'Rounding error, '
                             f'diff: {round(mistake, 2)}, '
                             f'lines: {len(self.invoice_lines)}, '
                             f'paymnts: {len(self.payments)} '
                             )
