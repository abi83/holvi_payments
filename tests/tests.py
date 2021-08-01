import random
from datetime import datetime
from faker import Faker
from models import Invoice


def timer(func):
    def timed(*args, **kw):
        ts = datetime.now()
        print('Started:', ts.strftime("%H:%M:%S  %f"))
        result = func(*args, **kw)
        te = datetime.now()
        print('Ended:', te.strftime("%H:%M:%S %f"))
        execution_time = te - ts
        print('Execution time:', execution_time.microseconds, 'microseconds')
        return result
    return timed


@timer
def my_tester(number):
    MAX_CATEGORIES_COUNT = 100
    MAX_PAYMENTS_COUNT = 300
    MAX_LINES_COUNT = MAX_CATEGORIES_COUNT * 7
    MAX_PRICE = 10_000_000

    for test_case_number in range(number):
        fake = Faker()

        categories_number = random.randint(1, MAX_CATEGORIES_COUNT)
        categories = [fake.bs() for _ in range(categories_number)]
        invoice_lines = [
            {
                "description": fake.catch_phrase(),
                "quantity": fake.random_int(min=1, max=100),
                "category": categories[
                    random.randint(0, len(categories) - 1)],
                "unit_price_net": fake.pyfloat(right_digits=2,
                                               positive=True,
                                               max_value=MAX_PRICE)
            } for _ in range(random.randint(1, MAX_LINES_COUNT))
        ]
        invoice_lines_sum = round(
            sum(line['unit_price_net'] * line['quantity'] for line in
                invoice_lines),
            2)
        payment_number = random.randint(1, MAX_PAYMENTS_COUNT)
        payments = []
        sum_left = invoice_lines_sum
        for index in range(payment_number):
            payment_sum = fake.pyfloat(
                right_digits=2,
                positive=True,
                min_value=int(invoice_lines_sum / (4.5 * payment_number)) + 1,
                max_value=int(invoice_lines_sum / 3))
            if sum_left > payment_sum:
                sum_left = round(sum_left - payment_sum, 2)
            else:
                payment_sum = round(sum_left, 2)
            assert payment_sum >= 0 and sum_left > 0
            payments.append(
                {
                    "id": index,
                    "amount": payment_sum
                }
            )
        x = Invoice(invoice_lines, payments)
        try:
            x.payments_categorisations()
            # print('Successs')
        except ValueError as e:
            print(e)


def test_runner():
    my_tester(500)


if __name__ == '__main__':
    test_runner()
