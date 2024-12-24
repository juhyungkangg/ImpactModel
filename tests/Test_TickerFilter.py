import unittest
from preprocess.TickerFilter import *


# Test TickerFilter class used to filter tickers

class Test_TickerFilter(unittest.TestCase):

    def testTickerFilter(self):
        dates = ['20070827']

        tickers = TickersFilter()
        tickers.feed(os.path.join(getDataDir(), 'ChildAddedListener1.js'))
        tickers.filter(dates)

        self.assertEqual([('SUNW', '20070827', 'quote'), ('SUNW', '20070827', 'trades'), ('CMCSA', '20070827', 'quote'), ('CMCSA', '20070827', 'trades')],
                         tickers.filter_data)


if __name__ == "__main__":
    unittest.main()