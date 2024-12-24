from taq.MyDirectories import *
import numpy as np


class AvgDailyValue(object):
    def __init__(self,
                 total_daily_values,   # Return matrix
                 lookback=10,  # Lookback period to get average
                ):
        # Set variables
        shape = total_daily_values.shape
        n_dates = shape[1]
        n_tickers = shape[0]

        if lookback == 0:
            self.avg_daily_value = total_daily_values
        else:
            # Calculate average daily value
            reduced_n_dates = n_dates-lookback
            size = (n_tickers, reduced_n_dates)
            avg_daily_val_mat = np.full(size, np.nan)


            for i in range(reduced_n_dates):
                avg_daily_val_mat[:,i] = np.mean(total_daily_values[:, i:i+lookback], axis=1)

            self.avg_daily_value = avg_daily_val_mat


if __name__ == "__main__":
    returns = np.load(os.path.join(getDataDir(),'matrices/total_daily_values.npy'))
    avg_daily_val = AvgDailyValue(returns).avg_daily_value
    print(avg_daily_val)