import unittest
from model.ImpactModel import *

class ParametricBootstrap(unittest.TestCase):

    def test_parametric_bootstrap(self):
        # Set model
        lookback = 0
        percentile = 95

        ig = InputGenerator(lookback=lookback)
        ig.vol_filter(percentile=percentile)

        x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()

        np.random.seed(47)
        ridx = np.random.choice(x1.shape[0], size=200, replace=False)

        impact_model = ImpactModel(x1[ridx, :], x2[ridx, :],
                                   x3[ridx, :], x4[ridx, :],
                                   x5[ridx, :], x6[ridx, :],
                                   x7[ridx, :], x8[ridx, :])


        impact_model.fit((0.2, 0.5), threshold=0.0025, exclude_outliers=False)

        eta = impact_model.eta
        beta = impact_model.beta

        n_sample = 10

        eta_arr = np.zeros(n_sample)
        beta_arr = np.zeros(n_sample)
        for i in range(n_sample):
            ridx = np.random.choice(x1.shape[0], size=200, replace=False)

            sigma = x1[ridx, :]
            v = x2[ridx, :]
            x = x3[ridx, :]

            # Generate h
            h_hat = eta * sigma * np.sign(x) * (np.abs(x/((6/6.5)*v))**beta)

            recover_model = ImpactModel(sigma, v, x,
                                        x4[ridx, :], x5[ridx, :],
                                        x6[ridx, :], x7[ridx, :], x8[ridx, :])
            recover_model.set_h(h_hat)
            recover_model.fit((0.2, 0.5), threshold=0.0025, exclude_outliers=False)

            eta_arr[i] = recover_model.eta
            beta_arr[i] = recover_model.beta

        print(eta)
        print(beta)
        print(np.mean(eta_arr))
        print(np.std(eta_arr))
        print(np.mean(beta_arr))
        print(np.std(beta_arr))

        # Compare recovered parameters with original parameters
        self.assertAlmostEqual(eta, np.mean(eta_arr))
        self.assertAlmostEqual(beta, np.mean(beta_arr))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()