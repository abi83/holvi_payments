from .money import Money


class Payment:
    def __init__(self, id, amount):
        self.id = id
        self.amount = Money(amount)
        self.categorisations = []

    def calc_mistake(self):
        return sum((category['net_amount'] for category in self.categorisations), start=Money(0)) - self.amount

    def categorise_payment(self, cat_proportions: dict, categories_limits: dict):
        money_left = self.amount
        for category, proportion in cat_proportions.items():
            net_amount = min(
                            self.amount * proportion,
                            categories_limits[category],
                            money_left
            )
            self.categorisations.append(
                {
                    'category': category,
                    'net_amount': net_amount
                })
            money_left -= net_amount

        return {
            category['category']: categories_limits[category['category']] - category['net_amount']
            for category in self.categorisations
        }

