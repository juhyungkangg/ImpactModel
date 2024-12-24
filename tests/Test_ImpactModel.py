import unittest
from model.ImpactModel import *


# Test ImpactModel

class Test_ImpactModel(unittest.TestCase):

    def testImpactModel(self):
        lookback = 0
        percentile = 95

        ig = InputGenerator(lookback=lookback)
        ig.vol_filter(percentile=percentile)

        x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()
        impact_model = ImpactModel(x1, x2, x3, x4, x5, x6, x7, x8)

        impact_model.fit((0.2, 0.5), threshold=0.0025, exclude_outliers=False)

        impact_model.r_squared()
        impact_model.white_test()
        impact_model.p_values()

        impact_model.plot_residuals()
        impact_model.plot_actual_vs_predict()

        impact_model.summary()

        self.assertAlmostEqual(impact_model.eta, 0.20454346545573976)
        self.assertAlmostEqual(impact_model.beta, 0.7264143720436982)
        self.assertAlmostEqual(impact_model.r_squared_val, 0.008168293726886211)
        self.assertAlmostEqual(impact_model.white_test_result, 0)


if __name__ == "__main__":
    unittest.main()