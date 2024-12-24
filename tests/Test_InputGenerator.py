import unittest
from model.AvgDailyImbalance import *
from model.AvgDailyValue import *
from model.AvgDailyVolatility import *
from model.InputGenerator import *
import numpy as np


class Test_InputGenerator(unittest.TestCase):

    def testInputGenerator(self):
        # Check the matrices are the same
        lookback = 10

        ig = InputGenerator(lookback)

        returns = np.load(os.path.join(getDataDir(), 'matrices/returns.npy'))
        total_daily_values = np.load(os.path.join(getDataDir(), 'matrices/total_daily_values.npy'))
        arrival_prices = np.load(os.path.join(getDataDir(), 'matrices/arrival_prices.npy'))
        value_imbalances = np.load(os.path.join(getDataDir(), 'matrices/value_imbalances.npy'))
        partial_vwaps = np.load(os.path.join(getDataDir(), 'matrices/partial_vwaps.npy'))
        full_vwaps = np.load(os.path.join(getDataDir(), 'matrices/full_vwaps.npy'))
        terminal_prices = np.load(os.path.join(getDataDir(), 'matrices/terminal_prices.npy'))
        total_daily_volume = np.load(os.path.join(getDataDir(), 'matrices/total_daily_volume.npy'))

        avg_daily_volatility = AvgDailyVolatility(returns, lookback).avg_daily_volatility
        avg_daily_value = AvgDailyValue(total_daily_values, lookback).avg_daily_value
        avg_daily_imbalance = AvgDailyImbalance(value_imbalances, lookback).avg_daily_imbalance

        self.assertTrue(np.array_equal(ig.avg_daily_volatility, avg_daily_volatility))
        self.assertTrue(np.array_equal(ig.avg_daily_value, avg_daily_value))
        self.assertTrue(np.array_equal(ig.avg_daily_imbalance, avg_daily_imbalance))

        self.assertTrue(np.array_equal(ig.arrival_prices, arrival_prices[:, lookback:]))
        self.assertTrue(np.array_equal(ig.partial_vwaps, partial_vwaps[:, lookback:]))
        self.assertTrue(np.array_equal(ig.full_vwaps, full_vwaps[:, lookback:]))
        self.assertTrue(np.array_equal(ig.terminal_prices, terminal_prices[:, lookback:]))
        self.assertTrue(np.array_equal(ig.total_daily_volume, total_daily_volume[:, lookback:]))


        # Volatility filter test
        n_dates = avg_daily_value.shape[1]

        ig.vol_filter(95)
        filtered_n_dates = ig.avg_daily_value.shape[1]

        self.assertEqual(int(n_dates*0.95), filtered_n_dates)

if __name__ == "__main__":
    unittest.main()