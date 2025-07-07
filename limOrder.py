class order:
    def __init__(self, orderID, traderID, instrumentID, optionSide, price, qty):
        self.orderID = int(orderID)
        self.traderID = str(traderID)
        self.instrumentID = str(instrumentID)
        self.optionSide = int(optionSide)
        self.price = price
        self.postPrice = 1 - self.price if optionSide == 1 else self.price
        self.side = 0 if qty > 0 else 1
        self.postSide = self.side if self.optionSide == 0 else 1 - self.side
        self.qty = abs(qty)
