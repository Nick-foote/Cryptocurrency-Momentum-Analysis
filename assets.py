import pandas as pd

# -- Cryptocurrencies --

crypto_filepath = 'files/crypto_currencies/'
trad_filepath = 'files/traditional/'



btc_filename = 'BTCUSD_BITSTAMP_240.csv'
eth_filename = 'ETHUSD_COINBASE_240.csv'
xrp_filename = 'XRPUSD_BITSTAMP_240.csv'
link_filename = 'LINKUSD_BINANCE_240.csv'

gold_filename = 'XAUUSD_OANDA_240.csv'


###########

# filename = {'symbol': 'btc', 'name': 'bitcoin', 'filename': 'BTCUSD_BITSTAMP_240.csv'}
files = {'btc': {'name': 'Bitcoin', 'filename': 'BTCUSD_BITSTAMP_240.csv'},
        'eth': {'name': 'Etherum', 'filename': 'ETHUSD_COINBASE_240.csv'},
        'xrp': {'name': 'XRP', 'filename': 'XRPUSD_BITSTAMP_240.csv'},
        'link': {'name': 'LinkChain', 'filename': 'LINKUSD_BINANCE_240.csv'}}

crypto_filenames = [btc_filename, eth_filename, xrp_filename, link_filename]

def read_in(file):
    try:
        file = pd.read_csv(
            crypto_filepath + files[file]['filename'],
            usecols=['time', 'close'],
            parse_dates=['time']
        )
        file.set_index('time', inplace=True)
    except FileNotFoundError:
        print(f"Unable to locate {files[file]['filename']}")



for file in files:
    read_in(file)
    print(file)




###########


try:
    # Bitcoin Chart
    btc = pd.read_csv(
        crypto_filepath + btc_filename,
        usecols=['time', 'close'],
        parse_dates=['time']
    )
    btc.set_index('time', inplace=True)


    # Ethereum Chart
    eth = pd.read_csv(
        crypto_filepath + eth_filename,
        usecols=['time', 'close'],
        parse_dates=['time']
    )
    eth.set_index('time', inplace=True)


    # XRP Chart
    xrp = pd.read_csv(
        crypto_filepath + xrp_filename,
        usecols=['time', 'close'],
        parse_dates=['time']
    )
    xrp.set_index('time', inplace=True)

    # LINK Chart
    link = pd.read_csv(
        crypto_filepath + link_filename,
        usecols=['time', 'close'],
        parse_dates=['time']
    )
    link.set_index('time', inplace=True)


# -- Traditional Markets --

    # Gold Chart
    gold = pd.read_csv(
        trad_filepath + gold_filename,
        usecols=['time', 'close'],
        parse_dates=['time']
    )
    gold.set_index('time', inplace=True)

except IOError as e:
    print(e)


# --- Exporting data ---

# to a CSV document
# btc.to_csv(f'{input_fast}_{input_slow}_EMA.csv')

