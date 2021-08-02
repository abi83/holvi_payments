from invoice_tester import invoice_categorisation_tester
from timer import timer


def test_xs():
    invoice_categorisation_tester(100, ranges='xs')


def test_s():
    invoice_categorisation_tester(75, ranges='s')


def test_m():
    invoice_categorisation_tester(50, ranges='m')


def test_l():
    invoice_categorisation_tester(25, ranges='l')


def test_xl():
    invoice_categorisation_tester(10, ranges='xl')


@timer
def main():
    invoice_categorisation_tester(100, ranges='xs')
    invoice_categorisation_tester(100, ranges='s')
    invoice_categorisation_tester(100, ranges='m')
    invoice_categorisation_tester(100, ranges='l')
    invoice_categorisation_tester(100, ranges='xl')


if __name__ == '__main__':
    main()
