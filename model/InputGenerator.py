from model.AvgDailyImbalance import *
from model.AvgDailyValue import *
from model.AvgDailyVolatility import *
class InputGenerator(object):
    def __init__(self, lookback):
        returns = np.load(os.path.join(getDataDir(), 'matrices/returns.npy'))
        total_daily_values = np.load(os.path.join(getDataDir(), 'matrices/total_daily_values.npy'))
        arrival_prices = np.load(os.path.join(getDataDir(), 'matrices/arrival_prices.npy'))
        value_imbalances = np.load(os.path.join(getDataDir(), 'matrices/value_imbalances.npy'))
        partial_vwaps = np.load(os.path.join(getDataDir(), 'matrices/partial_vwaps.npy'))
        full_vwaps = np.load(os.path.join(getDataDir(), 'matrices/full_vwaps.npy'))
        terminal_prices = np.load(os.path.join(getDataDir(), 'matrices/terminal_prices.npy'))
        total_daily_volume = np.load(os.path.join(getDataDir(), 'matrices/total_daily_volume.npy'))

        # Calculate average matrices
        self.avg_daily_volatility = AvgDailyVolatility(returns, lookback).avg_daily_volatility
        self.avg_daily_value = AvgDailyValue(total_daily_values, lookback).avg_daily_value
        self.avg_daily_imbalance = AvgDailyImbalance(value_imbalances, lookback).avg_daily_imbalance

        # Truncate matrices
        self.arrival_prices = arrival_prices[:, lookback:]
        self.partial_vwaps = partial_vwaps[:, lookback:]
        self.full_vwaps = full_vwaps[:, lookback:]
        self.terminal_prices = terminal_prices[:, lookback:]
        self.total_daily_volume = total_daily_volume[:, lookback:]

    def getInputs(self):
        return (self.avg_daily_volatility,
                self.avg_daily_value,
                self.avg_daily_imbalance,
                self.arrival_prices,
                self.partial_vwaps,
                self.full_vwaps,
                self.terminal_prices,
                self.total_daily_volume)

    def vol_filter(self, percentile=95):
        # Filter days with high volatility
        avg_vol = np.mean(self.avg_daily_volatility, axis=0)
        threshold = np.percentile(avg_vol, percentile)
        filtered_indexes = np.where(avg_vol < threshold)[0]

        self.avg_daily_volatility = self.avg_daily_volatility[:, filtered_indexes]
        self.avg_daily_value = self.avg_daily_value[:, filtered_indexes]
        self.avg_daily_imbalance = self.avg_daily_imbalance[:, filtered_indexes]

        self.arrival_prices = self.arrival_prices[:, filtered_indexes]
        self.partial_vwaps = self.partial_vwaps[:, filtered_indexes]
        self.full_vwaps = self.full_vwaps[:, filtered_indexes]
        self.terminal_prices = self.terminal_prices[:, filtered_indexes]
        self.total_daily_volume = self.total_daily_volume[:, filtered_indexes]