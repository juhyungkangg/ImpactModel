from model.ImpactModel import *
from model.InputGenerator import *


if __name__ == "__main__":
    lookback_li = [0,1,2,3,4,5,6,7,8,9,10,11,12]

    for lookback in lookback_li:
        percentile = 95

        ig = InputGenerator(lookback=lookback)
        ig.vol_filter(percentile=percentile)

        x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()
        impact_model = ImpactModel(x1, x2, x3, x4, x5, x6, x7, x8)

        impact_model.fit((0.2, 0.5), threshold=0.0025, exclude_outliers=False)

        impact_model.r_squared()
        impact_model.white_test()
        impact_model.p_values()

        # impact_model.plot_residuals(f" [lookback={lookback}]")
        # impact_model.plot_actual_vs_predict(f" [lookback={lookback}]")

        print(f"lookback {lookback}")
        impact_model.summary()
        print("\n")