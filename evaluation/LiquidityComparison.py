from model.ImpactModel import *


if __name__ == "__main__":
    lookback = 0
    percentile = 95

    ig = InputGenerator(lookback=lookback)
    ig.vol_filter(percentile=percentile)

    x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()

    mean_volume = np.mean(x8, axis=1)

    indexed_arr = [(val, idx) for idx, val in enumerate(mean_volume)]
    sorted_mean_volume = sorted(indexed_arr, reverse=True)

    top_tickers_idx = [idx for val, idx in sorted_mean_volume[:200]]
    bottom_tickers_idx = [idx for val, idx in sorted_mean_volume[-200:]]

    x1_t = x1[top_tickers_idx, :]
    x2_t = x2[top_tickers_idx, :]
    x3_t = x3[top_tickers_idx, :]
    x4_t = x4[top_tickers_idx, :]
    x5_t = x5[top_tickers_idx, :]
    x6_t = x6[top_tickers_idx, :]
    x7_t = x7[top_tickers_idx, :]
    x8_t = x8[top_tickers_idx, :]

    impact_model = ImpactModel(x1_t, x2_t, x3_t, x4_t, x5_t, x6_t, x7_t, x8_t)
    impact_model.fit((0.14, 0.6), threshold=0.0025, exclude_outliers=True)

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.plot_residuals(" [Liquid]")
    impact_model.plot_actual_vs_predict(" [Liquid]")

    impact_model.summary()


    x1_b = x1[bottom_tickers_idx, :]
    x2_b = x2[bottom_tickers_idx, :]
    x3_b = x3[bottom_tickers_idx, :]
    x4_b = x4[bottom_tickers_idx, :]
    x5_b = x5[bottom_tickers_idx, :]
    x6_b = x6[bottom_tickers_idx, :]
    x7_b = x7[bottom_tickers_idx, :]
    x8_b = x8[bottom_tickers_idx, :]

    impact_model = ImpactModel(x1_b, x2_b, x3_b, x4_b, x5_b, x6_b, x7_b, x8_b)
    impact_model.fit((0.14, 0.6), threshold=0.0025, exclude_outliers=True)

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.r_squared()
    impact_model.white_test()
    impact_model.p_values()

    impact_model.plot_residuals(" [Illiquid]")
    impact_model.plot_actual_vs_predict(" [Illiquid]")

    impact_model.summary()