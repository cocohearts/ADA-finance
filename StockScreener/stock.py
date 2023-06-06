# Custom stock class for storing stock information
class Stock:
    def __init__(self, symbol='', name='', c_price=0, industry='', market_cap=0, metrics=None):
        self.symbol = symbol
        self.name = name
        self.c_price = c_price
        self.industry = industry
        self.market_cap = market_cap
        self.metrics = metrics
