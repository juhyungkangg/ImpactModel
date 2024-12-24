from taq.MyDirectories import *
import numpy as np


class AvgDailyVolatility(object):
    def __init__(self,
                 returns,   # Return matrix
                 lookback=10,  # Lookback period to get average
                 n_buckets=195  # The number of return buckets
                ):
        # Change nan to 0
        self.returns = np.nan_to_num(returns, nan=0)

        # Set variables
        ret_shape = returns.shape
        n_dates = int(ret_shape[1] / n_buckets)
        n_tickers = ret_shape[0]
        size = (n_tickers, n_dates)
        daily_vol_mat = np.full(size, np.nan)

        # Calculate daily volatility
        for i in range(n_dates):
            # Scale from 2-min vol to 1-day vol
            daily_vol_mat[:,i] = np.std(self.returns[:, i*n_buckets:(i+1)*n_buckets], axis=1) * np.sqrt(n_buckets)

        if lookback == 0:
            self.avg_daily_volatility = daily_vol_mat
        else:
            # Calculate average daily volatility
            reduced_n_dates = n_dates-lookback
            size = (n_tickers, reduced_n_dates)
            avg_daily_vol_mat = np.full(size, np.nan)

            for i in range(reduced_n_dates):
                avg_daily_vol_mat[:, i] = np.mean(daily_vol_mat[:, i:i+lookback], axis=1)

            self.avg_daily_volatility = avg_daily_vol_mat


if __name__ == "__main__":
    returns = np.load(os.path.join(getDataDir(),'matrices/returns.npy'))
    vol = AvgDailyVolatility(returns, 0).avg_daily_volatility
    print(np.mean(vol))