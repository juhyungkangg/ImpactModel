from model.ImpactModel import *
import matplotlib.pyplot as plt
from taq.MyDirectories import *


if __name__ == "__main__":
    for i in range(1, 11, 3):
        lookback = i
        percentile = 95

        ig = InputGenerator(lookback=lookback)
        ig.vol_filter(percentile=percentile)

        x1, x2, x3, x4, x5, x6, x7, x8 = ig.getInputs()
        impact_model = ImpactModel(x1, x2, x3, x4, x5, x6, x7, x8)


        sigma = impact_model.avg_daily_volatility
        x = impact_model.avg_daily_imbalance
        v = impact_model.avg_daily_value
        h = impact_model.h

        x_vals = x / ((6/6.5) * v)
        y_vals = h / sigma

        plt.scatter(x_vals, y_vals, alpha=0.3)
        plt.xlabel('X / ((6/6.5) * V)')
        plt.ylabel('h / sigma')
        plt.title(f'Data Scatter Plot [lookback={lookback}]')
        plt.savefig(getDataDir() + f'/plots/data_scatter_plot_lookback_{lookback}.png')
        plt.show()