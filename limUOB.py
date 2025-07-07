from limOrder import order  

class limitUOB:
    def __init__(self, instrumentID):
        self.instrumentID = str(instrumentID)
        self.names = [self.instrumentID + '-C', self.instrumentID + '-P']
        self.books = {}, {}
        self.orders = {}
    
    def addOrder(self, order):
        if order.instrumentID == self.instrumentID:
            self.orders[order.orderID] = order
            sideBook = self.books[order.postSide]
            if not order.postPrice in sideBook:
                sideBook[order.postPrice] = []
            sideBook[order.postPrice].append(order.orderID)
    
    def getOrderExpenditure(self, orderID):
        if not orderID in self.orders:
            print('order', str(orderID), 'does not exist')
        order = self.orders[orderID]
        expenditureAsset = self.names[order.optionSide] if order.side == 1 else 'base'
        expenditureQty = order.qty
        return expenditureAsset, expenditureQty
    
    def removeOrder(self, orderID):
        if not orderID in self.orders:
            print('order', str(orderID), 'does not exist')
        expenditures = self.getOrderExpenditure(orderID)
        order = self.orders[orderID]
        self.books[order.postSide][order.postPrice].remove(orderID)
        if len(self.books[order.postSide][order.postPrice]) == 0:
            del self.books[order.postSide][order.postPrice]
        del order
        if expenditures[1] != 0:
            return ['c', {expenditures[0]:expenditures[1]}]
    
    def getMatch(self):
        bidPrice = 0
        matchPair = []
        for i in range(0, 2):
            book = self.books[i]
            prices = self.books[i].keys()
            bestPrice = None if len(prices) == 0 else (max(prices) if i == 0 else min(prices))
            if bestPrice == None:
                break
            bestOrder = min(book[bestPrice])
            if i == 0:
                bidPrice = bestPrice
                matchPair.append(bestOrder)
            else:
                if bestPrice <= bidPrice:
                    matchPair.append(bestOrder)  
                else:
                    break
        if len(matchPair) != 2:
            return None
        else:
            b, s = matchPair
            return matchPair, 0 if b > s else 1
    
    def fillOrder(self, orderID, price, qty):
        order = self.orders[orderID]
        trader, optionSide = order.traderID, order.optionSide
        fillPrice = 1 - price if optionSide == 1 else price
        cof = 1 if order.side == 0 else -1
        chgs = [['f', trader, {'base':-cof * fillPrice * qty, self.names[optionSide]:cof * qty}, ('fill', str(orderID), str(fillPrice), str(qty))]]
        order.qty -= qty
        if order.qty < 1:
            remChange = self.removeOrder(orderID)
            if not remChange is None: chgs.append(remChange)
        return chgs
        
    def matchOrders(self):
        chgs = []
        while True:
            match = self.getMatch()
            print('aggr', match)
            if match is None:
                break
            
            taker = self.orders[match[0][match[1]]]
            maker = self.orders[match[0][1 - match[1]]]
            fillPrice = maker.postPrice
            fillQty = min(maker.qty, taker.qty)
            if maker.traderID == taker.traderID:
                chgs.extend(self.removeOrder(maker.orderID))
                chgs.extend(self.removeOrder(taker.orderID))
            else:
                chgs.extend(self.fillOrder(maker.orderID, fillPrice, fillQty))
                chgs.extend(self.fillOrder(taker.orderID, fillPrice, fillQty))
        return chgs

# book = limitUOB('HAIRO')
# book.addOrder(order(orderID=1, traderID='a', instrumentID='HAIRO', optionSide=0, price=0.3, qty=-40))
# book.addOrder(order(orderID=2, traderID='b', instrumentID='HAIRO', optionSide=1, price=0.1, qty=-25))
# # book.addOrder(order(orderID=3, traderID='c', instrumentID='HAIRO', optionSide=1, price=0.5 , qty=50))
# print(book.books)
# print(book.matchOrders())
# for item in book.matchOrders():
    # print(item)
