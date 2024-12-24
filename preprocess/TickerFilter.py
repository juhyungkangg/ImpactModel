from taq.MyDirectories import *
import numpy as np

class TickersFilter:
    def __init__(self):
        self.tickers = []
        self.filter_data = []
        self.deleted_tickers = []
        self.filtered_tickers = []


    def feed(self, path):
        # Open the JavaScript file in read mode
        with open(path, 'r') as f:
            # Read the contents of the file and save them in a list
            self.tickers = [line.strip() for line in f.readlines()]

            # Remove if empty
            self.tickers = [x for x in self.tickers if x != '']

        return self.tickers

    def filter(self, dates):
        # Filter tickers that have data for all days
        for day in dates:
            # # Exclude XXX_XI
            quotes_tickers = [ticker for ticker in os.listdir(os.path.join(getQuotesDir(), day))]
            trades_tickers = [ticker for ticker in os.listdir(os.path.join(getTradesDir(), day))]


            for ticker in self.tickers:
                if ticker + '_quotes.binRQ' not in quotes_tickers:
                    self.filter_data.append((ticker, day, 'quote'))
                    print(f'Filtered {ticker}: No quotes data on {day}')
                if ticker + '_trades.binRT' not in trades_tickers:
                    self.filter_data.append((ticker, day, 'trades'))
                    print(f'Filtered {ticker}: No trades data on {day}')

            # # Include XXX_WI
            # quotes_tickers = [ticker.split('_')[0] for ticker in os.listdir(os.path.join(getQuotesDir(), day))]
            # trades_tickers = [ticker.split('_')[0] for ticker in os.listdir(os.path.join(getTradesDir(), day))]
            #
            #
            # for ticker in self.tickers:
            #     if ticker not in quotes_tickers:
            #         self.filter_data.append((ticker, day, 'quote'))
            #         print(f'Filtered {ticker}: No quotes data on {day}')
            #     if ticker not in trades_tickers:
            #         self.filter_data.append((ticker, day, 'trades'))
            #         print(f'Filtered {ticker}: No trades data on {day}')

        self.deleted_tickers = list(set([x[0] for x in self.filter_data]))
        self.filtered_tickers = [x for x in self.tickers if x not in self.deleted_tickers]

        # Save the filtered tickers
        np.save(os.path.join(getDataDir(),'filtered_tickers.npy'), self.filtered_tickers)

        return self.filtered_tickers

if __name__ == "__main__":
    import numpy as np
    tickers = TickersFilter()
    tickers.feed(os.path.join(getDataDir(), 'ChildAddedListener1.js'))
    tickers.filter(os.listdir(getQuotesDir()))
