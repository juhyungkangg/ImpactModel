from taq.TAQQuotesReader import TAQQuotesReader
from taq.TAQTradesReader import TAQTradesReader
from taq.MyDirectories import *
from impactUtils.ReturnBuckets import ReturnBuckets
from impactUtils.VWAP import VWAP
from impactUtils.Imbalance import Imbalance
from impactUtils.ArrivalTerminalPrices import ArrivalTerminalPrices
from preprocess.TickerFilter import TickersFilter
from tqdm import tqdm

import numpy as np
import multiprocessing

class Preprocess(object):
    def __init__(
        self,
        root_dir, # root directory
        tickers, # list of stock tickers (str)
        dates # list of dates (str)
    ):
        self.root_dir = root_dir
        self.tickers = tickers
        self.dates = dates

        self.n_tickers = len(tickers)
        self.n_dates = len(dates)
        size = (self.n_tickers, self.n_dates)

        self.n_buckets = 195
        returns_size = (self.n_tickers, self.n_dates * self.n_buckets)

        self.returns = np.full(returns_size, np.nan)
        self.total_daily_values = np.full(size, np.nan)
        self.arrival_prices = np.full(size, np.nan)
        self.value_imbalances = np.full(size, np.nan)
        self.partial_vwaps = np.full(size, np.nan)
        self.full_vwaps = np.full(size, np.nan)
        self.terminal_prices = np.full(size, np.nan)
        self.total_daily_volume = np.full(size, np.nan)

    def calc_returns(self):
        for i in range(self.n_tickers):
            stock = self.tickers[i]

            for j in range(self.n_dates):
                quote_path = os.path.join(self.root_dir, 'quotes/' + self.dates[j] + '/' + stock + '_quotes.binRQ')
                quotes_reader = TAQQuotesReader(quote_path)

                # Compute 2-minute mid-quote returns
                rets = ReturnBuckets(quotes_reader, None, None, self.n_buckets)
                twoMinReturns = rets._returns

                self.returns[i, j*self.n_buckets:(j+1)*self.n_buckets] = twoMinReturns

    def calc_total_daily_values(self):
        # Compute total daily value
        totalDailyValue = self.full_vwaps * self.total_daily_volume

        self.total_daily_values = totalDailyValue

    def calc_arrival_terminalprices(self):
        for i in range(self.n_tickers):
            stock = self.tickers[i]

            for j in range(self.n_dates):
                trade_path = os.path.join(self.root_dir, 'trades/' + self.dates[j] + '/' + stock + '_trades.binRT')
                trades_reader = TAQTradesReader(trade_path)

                # Compute arrival price & terminal price
                prices = ArrivalTerminalPrices(trades_reader)
                arrivalPrice = prices.getArrivalPrice()
                terminalPrice = prices.getTerminalPrice()

                self.arrival_prices[i, j] = arrivalPrice
                self.terminal_prices[i, j] = terminalPrice

    def calc_value_imbalances(self):
        for i in range(self.n_tickers):
            stock = self.tickers[i]

            for j in range(self.n_dates):
                trade_path = os.path.join(self.root_dir, 'trades/' + self.dates[j] + '/' + stock + '_trades.binRT')

                trades_reader = TAQTradesReader(trade_path)

                # Compute 9:30-3:30 value imbalance
                imbal = Imbalance()
                valueImbalance = imbal.computeImbalance(trades_reader, 19 * 60 * 60 * 1000 / 2, 16 * 60 * 60 * 10000 - 60000 * 30)

                self.value_imbalances[i, j] = valueImbalance

    def calc_vwaps(self):
        for i in range(self.n_tickers):
            stock = self.tickers[i]

            for j in range(self.n_dates):
                trade_path = os.path.join(self.root_dir, 'trades/' + self.dates[j] + '/' + stock + '_trades.binRT')

                trades_reader = TAQTradesReader(trade_path)

                # Compute 9:30-3:30 VWAP and 9:30-4:00 VWAP
                partialVWAP = VWAP(trades_reader, 19 * 60 * 60 * 1000 / 2, 16 * 60 * 60 * 10000 - 60000 * 30).getVWAP()
                fullVWAP = VWAP(trades_reader, 19 * 60 * 60 * 1000 / 2, 16 * 60 * 60 * 10000).getVWAP()

                self.partial_vwaps[i, j] = partialVWAP
                self.full_vwaps[i, j] = fullVWAP

    def calc_total_daily_volume(self):
        for i in range(self.n_tickers):
            stock = self.tickers[i]

            for j in range(self.n_dates):
                trade_path = os.path.join(self.root_dir, 'trades/' + self.dates[j] + '/' + stock + '_trades.binRT')

                trades_reader = TAQTradesReader(trade_path)

                # Compute total daily volume
                totalDailyVolume = trades_reader.getTotalVolume()

                self.total_daily_volume[i, j] = totalDailyVolume

    def conduct(self):
        print(f"Preprocessing started for {self.tickers[:3]} and other tickers.")
        self.calc_vwaps()
        print(f"VWAP Calculation Completed for {self.tickers[:3]} and other tickers.")
        self.calc_total_daily_volume()
        print(f"Volume Calculation Completed for {self.tickers[:3]} and other tickers.")
        self.calc_arrival_terminalprices()
        print(f"Arrival/Terminal Prices Calculation Completed for {self.tickers[:3]} and other tickers.")
        self.calc_returns()
        print(f"Returns Calculation Completed for {self.tickers[:3]} and other tickers.")
        self.calc_value_imbalances()    # partial vwap required
        print(f"Imbalance Calculation Completed for {self.tickers[:3]} and other tickers.")
        self.calc_total_daily_values()  # Full vwap and daily volume required
        print(f"Value Calculation Completed for {self.tickers[:3]} and other tickers.")


def worker(chunk, *args):
    root_dir, dates = args
    tickers = chunk
    preprocess = Preprocess(root_dir, tickers, dates)
    preprocess.conduct()

    return [preprocess.returns, preprocess.total_daily_values, preprocess.arrival_prices,
            preprocess.value_imbalances, preprocess.partial_vwaps, preprocess.full_vwaps,
            preprocess.terminal_prices, preprocess.total_daily_volume]


if __name__ == "__main__":
    import os
    import time

    # Start the timer
    start_time = time.time()

    # root_dir
    root_dir = getDataDir()

    # tickers
    if os.path.exists(os.path.join(getDataDir(),'filtered_tickers.npy')):
        tickers = np.load(os.path.join(getDataDir(),'filtered_tickers.npy'))
    else:
        Tickers = TickersFilter()
        Tickers.feed(os.path.join(getDataDir(), 'ChildAddedListener1.js'))
        Tickers.filter(os.listdir(getQuotesDir()))
        tickers = Tickers.filtered_tickers

    # dates
    dates = os.listdir(getQuotesDir())

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    chunk_size = len(tickers)//num_processes
    chunks = [tickers[i:i+chunk_size] for i in range(0, len(tickers), chunk_size)]
    results = pool.starmap(worker, [(chunk, root_dir, dates) for chunk in chunks])

    print(results)

    temp = []
    for res in results:
        temp.append(np.concatenate(res, axis=1))
    temp2 = np.concatenate(temp, axis=0)

    n_dates = len(dates)
    returns = temp2[:, :-7*n_dates]
    total_daily_values = temp2[:, -7*n_dates:-6*n_dates]
    arrival_prices = temp2[:, -6*n_dates:-5*n_dates]
    value_imbalances = temp2[:, -5*n_dates:-4*n_dates]
    partial_vwaps = temp2[:, -4*n_dates:-3*n_dates]
    full_vwaps = temp2[:, -3*n_dates:-2*n_dates]
    terminal_prices = temp2[:, -2*n_dates:-n_dates]
    total_daily_volume = temp2[:, -n_dates:]

    pool.close()
    pool.join()

    np.save(os.path.join(getDataDir(),'matrices/returns.npy'), returns)
    np.save(os.path.join(getDataDir(),'matrices/total_daily_values.npy'), total_daily_values)
    np.save(os.path.join(getDataDir(),'matrices/arrival_prices.npy'), arrival_prices)
    np.save(os.path.join(getDataDir(),'matrices/value_imbalances.npy'), value_imbalances)
    np.save(os.path.join(getDataDir(),'matrices/partial_vwaps.npy'), partial_vwaps)
    np.save(os.path.join(getDataDir(),'matrices/full_vwaps.npy'), full_vwaps)
    np.save(os.path.join(getDataDir(),'matrices/terminal_prices.npy'), terminal_prices)
    np.save(os.path.join(getDataDir(), 'matrices/total_daily_volume.npy'), total_daily_volume)
    print("Saved matrices")

    # End the timer
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time_seconds = end_time - start_time
    elapsed_time_minutes = np.round(elapsed_time_seconds / 60,2)

    print("Elapsed time:", elapsed_time_minutes, "minutes ")
