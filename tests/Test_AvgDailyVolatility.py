import unittest

from model.AvgDailyVolatility import AvgDailyVolatility
import numpy as np

# Test Volatility class

class Test_AvgDailyVolatility(unittest.TestCase):

    def testAvgDailyVolatility(self):
        shape = (500, 195*1000)
        lookback = 10
        n_buckets = 195
        returns = np.random.randn(*shape)

        vol = AvgDailyVolatility(returns, lookback, n_buckets).avg_daily_volatility

        self.assertEqual(vol.shape[1], shape[1]/n_buckets-lookback)
        self.assertAlmostEqual(np.sqrt(195), np.mean(vol),0)


if __name__ == "__main__":
    unittest.main()