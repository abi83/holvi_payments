# from .money import Money

class Payment:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount
        self.categorisations = []

    def calc_mistake(self):
        return round(sum(category['net_amount'] for category in self.categorisations) - self.amount, 2)

    def categorise_payment(self, cat_proportions: dict, categories_limits: dict):
        money_left = self.amount
        for category, proportion in cat_proportions.items():
            net_amount = round(
                        min(
                            self.amount * proportion,
                            categories_limits[category],
                            money_left
                        ), 2)
            self.categorisations.append(
                {
                    'category': category,
                    'net_amount': net_amount
                })
            money_left -= net_amount
        return {
            category['category']: round(categories_limits[category['category']] - category['net_amount'], 2)
            for category in self.categorisations
        }

