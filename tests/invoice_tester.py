import random

from faker import Faker

from models import Invoice, Money


def invoice_categorisation_tester(runs_number: int, ranges=None) -> None:
    """
    Runs Invoice.payments_categorisations method runs_number times with
    random values depends on ranges value: XtraSmall, Small, Medium, Large or
    XtraLarge. Asserts if each categorised payment in invoice nad NO mistake in
    categories summ
    Separately checks if Invoice.categories_limit is enough to cover remaining
    payments
    """
    settings = {
        'xs': (5, 5, 5, .03),
        's': (10, 10, 20, 1),
        'm': (20, 20, 40, 100),
        'l': (100, 100, 100, 10_000),
        'xl': (100, 300, 1000, 10_000_000)
    }
    (MAX_CATEGORIES_COUNT, MAX_PAYMENTS_COUNT,
     MAX_LINES_COUNT, MAX_PRICE) = settings[ranges]
    fully_payed_count = {
        True: 0,
        False: 0
    }
    for test_case_number in range(1, runs_number):
        fake = Faker()
        categories_number = fake.random_int(min=2, max=MAX_CATEGORIES_COUNT)
        categories = [fake.bs() for _ in range(categories_number)]
        invoice_lines = [
            {
                "description": fake.catch_phrase(),
                "quantity": fake.random_int(min=1, max=3),
                "category": categories[random.randint(0, len(categories)-1)],
                "unit_price_net": max(round(random.random()*MAX_PRICE, 2), 0.01)
             } for _ in range(random.randint(1, MAX_LINES_COUNT))
        ]
        invoice_lines_sum = round(
            sum(line['unit_price_net']*line['quantity']
                for line in invoice_lines), 2)
        payment_number = random.randint(1, MAX_PAYMENTS_COUNT)
        payments = []
        sum_left = invoice_lines_sum
        for index in range(payment_number):
            payment_sum = max(
                round(random.random()*invoice_lines_sum/2, 2), 0.01)
            if sum_left > payment_sum:
                sum_left = round(sum_left - payment_sum, 2)
            else:
                payment_sum = round(sum_left, 2)
                sum_left = 0
            assert payment_sum > 0 and sum_left >= 0
            payments.append({"id": index, "amount": payment_sum })
            if sum_left == 0:
                break
        invoice = Invoice(invoice_lines, payments)
        invoice.payments_categorisations()
        fully_payed_count[invoice.invoice_sum == invoice.payments_sum] += 1
        for payment in invoice.payments:
            assert payment.calc_mistake() == Money(0), f'Very big mistake in {payment}'
        assert (
            invoice.invoice_sum - invoice.payments_sum - sum((remaining for remaining in invoice.categories_limit.values()), start=Money(0)) == Money(0)),\
            'Incorrect remaining'
    print(f'{ranges} tested {runs_number} times. Fully paid?: {fully_payed_count}')
