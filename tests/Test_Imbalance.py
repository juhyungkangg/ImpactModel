import unittest
from taq.MyDirectories import *
from taq.TAQTradesReader import TAQTradesReader
from impactUtils.Imbalance import Imbalance

# Test ReturnBuckets class used to compute
# returns of some length of time, e.g. 2 minutes
# or 15 minutes
class Test_Imbalance(unittest.TestCase):

    def test_classify(self):
        imbalance = Imbalance()
        self.assertTrue(imbalance.classify(100) == 0)
        self.assertTrue(imbalance.classify(100) == 0)
        self.assertTrue(imbalance.classify(101) == 1)
        self.assertTrue(imbalance.classify(101) == 1)
        self.assertTrue(imbalance.classify(102) == 1)
        self.assertTrue(imbalance.classify(101) == -1)
        self.assertTrue(imbalance.classify(101) == -1)
        self.assertTrue(imbalance.classify(102) == 1)

    def test_computeImbalance(self):
        startTS = 18 * 60 * 60 * 1000 / 2  # 930AM
        endTS = 16 * 60 * 60 * 1000  # 4PM
        fileName = MyDirectories.BinRTTradesDir + '/20070919/IBM_trades.binRT'
        data = TAQTradesReader( fileName )
        imblance = Imbalance().computeImbalance(data, startTS, endTS)

        self.assertAlmostEqual(imblance,-41921805.438568115)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()