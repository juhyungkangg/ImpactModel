import unittest

from model.AvgDailyValue import AvgDailyValue
import numpy as np


class Test_AvgDailyValue(unittest.TestCase):

    def testAvgDailyValue(self):
        shape = (500, 1000)
        lookback = 10

        vals = np.random.randn(*shape)

        val = AvgDailyValue(vals, lookback).avg_daily_value

        self.assertEqual(val.shape[1], shape[1]-lookback)
        self.assertAlmostEqual(0, np.mean(val),2)


if __name__ == "__main__":
    unittest.main()