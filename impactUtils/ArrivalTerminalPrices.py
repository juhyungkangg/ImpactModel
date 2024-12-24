class ArrivalTerminalPrices(object):
    def __init__(
        self,
        data # TAQTradesReader object
    ):

        startTS = 19 * 60 * 60 * 1000 / 2
        endTS = 16 * 60 * 60 * 1000

        datalen = data.getN()

        for i in range(datalen):
            if data.getTimestamp(i) >= startTS:
                self.arrivalPrice = data.getPrice(i)
                break

        for i in range(datalen-1, -1, -1):
            if data.getTimestamp(i) <= endTS:
                self.terminalPrice = data.getPrice(i)
                break

    def getArrivalPrice(self):
        return self.arrivalPrice

    def getTerminalPrice(self):
        return self.terminalPrice
