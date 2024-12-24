import unittest

from model.AvgDailyImbalance import AvgDailyImbalance
import numpy as np

# Test Volatility class

class Test_AvgDailyImbalance(unittest.TestCase):

    def testAvgDailyImbalance(self):
        shape = (500, 1000)
        lookback = 10

        vals = np.random.randn(*shape)

        val = AvgDailyImbalance(vals, lookback).avg_daily_imbalance

        self.assertEqual(val.shape[1], shape[1]-lookback)
        self.assertAlmostEqual(0, np.mean(val),2)


if __name__ == "__main__":
    unittest.main()