from limitUOB import limitUOB
from order import order

class predictionExchange:
    def __init__(self):
        self.accounts = {}
        self.books = {}    
    
    def addInstrument(self, name):
        if not name in self.books:
            self.books[name] = limitUOB(name)
    
    def addAccount(self, accountName):
        if accountName in self.accounts:
            return None
        self.accounts[accountName] = {'assets': {'base':1000}, 'bp':{'base':1000}}
    
    def changeAsset(self, acctName, tgt, assetName, qty):
        if not acctName in self.accounts:
            print('account does not exist')
            return None
        acct = self.accounts[acctName]
        if not tgt in acct:
            print('specified target does not exist')
            return None
        target = self.accounts[acctName][tgt]
        if not assetName in target:
            target[assetName] = 0
        newQty = target[assetName] + qty
        if newQty < 0:
            print('caught attempt to change account asset to the negative')
            return None
        target[assetName] = newQty
                
    def postOrder(self, order):
        if not order.traderID in self.accounts:
            print('Trader does not exist')
            return None
        if not order.instrumentID in self.books:
            print('Instrument does not exist')
            return None
        optionSide = 'C' if order.optionSide == 0 else 'P'
        print(order.side)
        expenditureAsset = 'base' if order.side == 0 else order.instrumentID + '-' + optionSide
        expenditureQty = order.price * order.qty if order.side == 'B' else order.qty
        if not expenditureAsset in self.accounts[order.traderID]['bp']:
            print(expenditureAsset, 'does not exist in account')
            return None
        bp = self.accounts[order.traderID]['bp'][expenditureAsset]
        if bp - expenditureQty < 0:
            print('insufficiant', expenditureAsset, 'balance')
            return None
        self.books[order.instrumentID].addOrder(order)
        
    def matchOrders(self):
        chgs = []
        for book in self.books:
            chgs.extend(self.books[book].matchOrders())
        print(chgs)
        for i in chgs:
            print(i)
            for assetName in i[2]:
                assetChange = i[2][assetName]
                self.changeAsset(i[1], 'bp', assetName, assetChange)
                if i[0] == 'f':
                    self.changeAsset(i[1], 'assets', assetName, assetChange)

exchg = predictionExchange()
exchg.addAccount('A')
exchg.addAccount('B')
exchg.addInstrument('STMXPO1')

exchg.postOrder(order(orderID=1, traderID = 'A', instrumentID='STMXPO1', optionSide=0, price=0.6, qty = 1000))
exchg.postOrder(order(orderID=2, traderID = 'B', instrumentID='STMXPO1', optionSide=1, price=0.9, qty = 500))
exchg.matchOrders()
print(exchg.accounts)
exchg.postOrder(order(orderID=3, traderID = 'A', instrumentID='STMXPO1', optionSide=0, price=0.6, qty = -100))
exchg.postOrder(order(orderID=4, traderID = 'B', instrumentID='STMXPO1', optionSide=1, price=0.4, qty = -100))
for i in exchg.books:
    print(exchg.books[i].books)
exchg.matchOrders()
print(exchg.accounts)
