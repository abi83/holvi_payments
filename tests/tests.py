def test_case():
    assert 5 == 5


def test_case2():
    assert 6 == 6

import random
from faker import Faker
import uuid
from models.models import Invoice


def tester(number):
    MAX_CATEGORIES_COUNT = 5
    MAX_PAYMENTS_COUNT = 3

    for test_case_number in range(number):
        fake = Faker()

        categories_number = random.randint(1,MAX_CATEGORIES_COUNT)
        categories = [fake.bs() for _ in range(categories_number)]
        invoice_lines = [
            {
                "description": fake.catch_phrase(),
                "quantity": fake.random_int(min=1, max=100),
                "category": categories[random.randint(0, len(categories)-1)],
                "unit_price_net": fake.pyfloat(right_digits=2, positive=True, max_value=100)
             } for _ in range(random.randint(1, MAX_CATEGORIES_COUNT*3))
        ]
        invoice_sum = sum(line['unit_price_net']*line['quantity'] for line in invoice_lines)
        payment_number = random.randint(1, MAX_PAYMENTS_COUNT)
        payments = []
        for index in range(payment_number):
            payment_amount = fake.pyfloat(right_digits=2, positive=True,
                                          min_value=int(invoice_sum/(4*payment_number))+1,
                                          max_value=int(invoice_sum))
            # print('payment_amount', payment_amount)
            if invoice_sum > payment_amount:
                invoice_sum -= payment_amount
            else:
                payment_amount = round(invoice_sum, 2)
            payments.append(
                {
                    "id": index,
                    "amount": payment_amount
                }
            )
        x = Invoice(invoice_lines, payments)
        try:
            x.payments_categorisations()
            print('Successs')
        except ValueError as e:
            print(e)

def test_runner():
    tester(100)
