import pandas as pd

# -- Cryptocurrencies --

filepath = 'files/crypto_currencies/'

files = {
    'btc': {'name': 'Bitcoin', 'filename': 'BTCUSD_BITSTAMP_240.csv'},
    'eth': {'name': 'Ethereum', 'filename': 'ETHUSD_COINBASE_240.csv'},
    'xrp': {'name': 'XRP', 'filename': 'XRPUSD_BITSTAMP_240.csv'},
    'link': {'name': 'LinkChain', 'filename': 'LINKUSD_BINANCE_240.csv'}
}


class Data:
    def __init__(self, coin):
        self.coin = coin
        self.dataframe = None
        self.name = files[self.coin]['name']

    def read_in(self):
        try:
            self.dataframe = pd.read_csv(filepath + files[self.coin]['filename'],
                                         usecols=['time', 'close'],
                                         parse_dates=['time']
                                         )
            self.dataframe.set_index('time', inplace=True)
            print(f"{self.name!r} Dataframe setup completed")

        except FileNotFoundError:
            print(f"Unable to locate {files[self.coin]['filename']}")
