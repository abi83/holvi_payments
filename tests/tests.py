from invoice_tester import invoice_categorisation_tester
from timer import timer


def test_xs():
    invoice_categorisation_tester(10, ranges='xs')


def test_s():
    invoice_categorisation_tester(10, ranges='s')


def test_m():
    invoice_categorisation_tester(10, ranges='m')


def test_l():
    invoice_categorisation_tester(5, ranges='l')


def test_xl():
    invoice_categorisation_tester(4, ranges='xl')


@timer
def main():
    invoice_categorisation_tester(5, ranges='xs')
    invoice_categorisation_tester(5, ranges='s')
    invoice_categorisation_tester(5, ranges='m')
    invoice_categorisation_tester(3, ranges='l')
    invoice_categorisation_tester(2, ranges='xl')


if __name__ == '__main__':
    main()
