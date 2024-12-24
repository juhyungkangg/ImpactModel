from model.ImpactModel import *
from model.InputGenerator import *


if __name__ == "__main__":
    lookback = 0
    percentile = 95

    ig = InputGenerator(lookback=lookback)
    ig.vol_filter(percentile=percentile)

    x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()

    n_half = int(x1.shape[1]/2)

    x1_t = x1[:, :n_half]
    x2_t = x2[:, :n_half]
    x3_t = x3[:, :n_half]
    x4_t = x4[:, :n_half]
    x5_t = x5[:, :n_half]
    x6_t = x6[:, :n_half]
    x7_t = x7[:, :n_half]
    x8_t = x8[:, :n_half]


    impact_model = ImpactModel(x1_t, x2_t, x3_t, x4_t, x5_t, x6_t, x7_t, x8_t)
    impact_model.fit((0.14, 0.6), threshold=0.0025, exclude_outliers=True)

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.plot_residuals(f" [First half]")
    impact_model.plot_actual_vs_predict(f" [First half]")

    print("First Half")
    impact_model.summary()
    print("\n")

    x1_t = x1[:, n_half:]
    x2_t = x2[:, n_half:]
    x3_t = x3[:, n_half:]
    x4_t = x4[:, n_half:]
    x5_t = x5[:, n_half:]
    x6_t = x6[:, n_half:]
    x7_t = x7[:, n_half:]
    x8_t = x8[:, n_half:]

    impact_model = ImpactModel(x1_t, x2_t, x3_t, x4_t, x5_t, x6_t, x7_t, x8_t)
    impact_model.fit((0.14, 0.6), threshold=0.0025, exclude_outliers=True)

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.plot_residuals(f" [Second half]")
    impact_model.plot_actual_vs_predict(f" [Second half]")

    print("Second Half")
    impact_model.summary()