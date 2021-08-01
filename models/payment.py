import random

from .money import Money


class Payment:
    def __init__(self, id, amount):
        self.id = id
        self.amount = Money(amount)
        self.categorisations = []

    def calc_mistake(self):
        return sum((category['net_amount'] for category in self.categorisations), start=Money(0)) - self.amount

    def categorise_payment(self, cat_proportions: dict, categories_limits: dict, last, hungry=Money(0.01)):
        money_left = self.amount
        # if sum(net for net in )
        items = [*cat_proportions.items()]
        random.shuffle(items)
        # print(cat_proportions)
        for category, proportion in items:
            net_amount = min(
                            self.amount * proportion + hungry,
                            categories_limits[category],
                            money_left
            )
            self.categorisations.append(
                {
                    'category': category,
                    'net_amount': net_amount
                })
            money_left -= net_amount
        # assert money_left == Money(0) or last
        if money_left > Money(0):
            print('Re!', hungry)
            breakpoint()
            self.categorisations = []
            return self.categorise_payment(cat_proportions, categories_limits, last, hungry+Money(0.01))
            # breakpoint()
        return {
            category['category']: categories_limits[category['category']] - category['net_amount']
            for category in self.categorisations
        }

