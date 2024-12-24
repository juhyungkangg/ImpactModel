from taq.MyDirectories import *
import numpy as np


class AvgDailyImbalance(object):
    def __init__(self,
                 value_imbalances,   # Imbalance matrix
                 lookback=10,  # Lookback period to get average
                ):
        # Set variables
        shape = value_imbalances.shape
        n_dates = shape[1]
        n_tickers = shape[0]

        if lookback == 0:
            self.avg_daily_imbalance = value_imbalances
        else:
            # Calculate average daily imbalance
            reduced_n_dates = n_dates-lookback
            size = (n_tickers, reduced_n_dates)
            avg_daily_imbal_mat = np.full(size, np.nan)


            for i in range(reduced_n_dates):
                avg_daily_imbal_mat[:,i] = np.mean(value_imbalances[:, i:i+lookback], axis=1)

            self.avg_daily_imbalance = avg_daily_imbal_mat


if __name__ == "__main__":
    value_imbalances = np.load(os.path.join(getDataDir(),'matrices/value_imbalances.npy'))
    avg_daily_imbal = AvgDailyImbalance(value_imbalances).avg_daily_imbalance
    print(avg_daily_imbal)