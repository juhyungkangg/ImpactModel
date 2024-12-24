import unittest
from preprocess.TickerFilter import *
from preprocess.Preprocess import *
from taq.MyDirectories import *

# Test Preprocess class used to filter tickers

class Test_Preprocess(unittest.TestCase):

    def testPreprocess(self):
        import os

        # root_dir
        test_root_dir = getDataDir()

        # tickers
        test_tickers = ['AAPL']

        # dates
        test_dates = ['20070620']

        test_preprocess = Preprocess(test_root_dir, test_tickers, test_dates)
        test_preprocess.conduct()

        self.assertAlmostEqual(test_preprocess.returns[0][0], 2.98714530e-03)
        self.assertAlmostEqual(test_preprocess.total_daily_values[0][0], 3787624084.795143)
        self.assertAlmostEqual(test_preprocess.arrival_prices[0][0], 123.87999725)
        self.assertAlmostEqual(test_preprocess.value_imbalances[0][0], -111601212.42151642)
        self.assertAlmostEqual(test_preprocess.partial_vwaps[0][0], 122.86348485)
        self.assertAlmostEqual(test_preprocess.full_vwaps[0][0], 122.86348485)
        self.assertAlmostEqual(test_preprocess.terminal_prices[0][0], 121.62000275)
        self.assertAlmostEqual(test_preprocess.total_daily_volume[0][0], 30827907.0)

if __name__ == "__main__":
    unittest.main()