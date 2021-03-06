from .money import Money


class Payment:
    def __init__(self, id, amount):
        self.id = id
        self.amount: Money = Money(float(amount))
        self.categorisations: list = []

    def calc_mistake(self):
        return sum(
            (category['net_amount'] for category in self.categorisations),
            Money(0)
        ) - self.amount

    def categorise_payment(self,
                           cat_proportions: dict,
                           categories_limits: dict,
                           hungry=Money(0),
                           ) -> dict:
        """
        Trying to choose possible net_amount for each categori according to
        categories limit, money left inside payment and each category
        proportion. Trying to distribute payment amount as quick as possible
        by adding up to 0.01 money to each category. Next payment will recieve
        corrected limits and proportions to fix this approximation.
        :param hungry: params to rounds UP net_amount
        :param cat_proportions: current proportions of categories
        :param categories_limits: max limit for each category
        :return: new limits for categories
        """
        money_left = self.amount
        for category, proportion in cat_proportions.items():
            net_amount = min(
                categories_limits[category],
                money_left,
                self.amount * proportion + hungry,
            )
            self.categorisations.append(
                {
                    'category': category,
                    'net_amount': net_amount
                })
            money_left -= net_amount
        if money_left > Money(0):
            # one more attempt with increased hungry
            self.categorisations = []
            return self.categorise_payment(cat_proportions, categories_limits,
                                           hungry + Money(0.01))
        return {
            category['category']: (
                categories_limits[category['category']]
                - category['net_amount']
            )
            for category in self.categorisations
        }
