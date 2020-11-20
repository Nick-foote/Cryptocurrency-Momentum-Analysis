import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import database
from data import Data
from connection_pool import get_connection


class Chart(Data):
    """Takes asset symbol input from user.
    Inherits self.name, self.dataframe.
    Charts Price history and EMA crossovers with MatPlotLib
    """
    def __init__(self, asset: str):
        super().__init__(asset)
        self.asset = asset
        self.read_in()


    def __repr__(self):
        return f"Asset {self.asset}"

    def get_price_chart(self):
        """Creates chart with from the Close Price column over the time available."""

        figure = plt.figure(figsize=(15, 10))
        ax_close = figure.add_subplot()
        ax_close.plot(self.dataframe['close'])

        plt.title(f"{self.name} Price History")
        plt.ylabel("Close Price - USD$")
        plt.show()

    def ema_strategy(self, input_fast: int, input_slow: int, year_start=None, year_end=None):
        """Connects to the dataframe and adding EMA values"""
        df = self.dataframe

        if year_end:        # check if a specific range of years to examine has been entered
            df = df.loc[year_start:year_end].copy(deep=False)
        elif year_start:
            df = df.loc[year_start:].copy(deep=False)

        df['Fast EMA'] = df['close'].ewm(span=input_fast).mean()
        df['Slow EMA'] = df['close'].ewm(span=input_slow).mean()

        # EMA crossovers shown on Price chart
        figure1 = plt.figure(figsize=(15, 10))
        ax_close = figure1.add_subplot()
        ax_close.plot(df['close'])

        df['Fast EMA'].plot()
        df['Slow EMA'].plot()

        plt.title("Price History")
        plt.ylabel("Close Price - USD$")
        plt.legend()
        plt.show()

        # The new column "position"  indicates going long on a stock.
        # If the fast EMA > slow EMA, denote as 1 (long one asset/stock), otherwise denote as 0 (do nothing)
        df['position'] = [1 if df.loc[ei, 'Fast EMA'] > df.loc[ei, 'Slow EMA'] else 0 for ei in df.index]

        df['close1'] = df['close'].shift(-1)
        df['profit'] = [
            df.loc[ei, 'close1'] - df.loc[ei, 'close'] if df.loc[ei, 'position'] == 1
            else 0 for ei in df.index]

        # Change in profit record, not currently needed.
        # df['profit'].plot()
        # plt.axhline(y=0, color='red')

        df['wealth'] = df['profit'].cumsum()
        initial_cost = df.loc[df.index[0], 'close']
        final_return = df.loc[df.index[-2], 'wealth']
        roi = final_return / initial_cost
        roi_percent = roi * 100

        df['buy_hold'] = df['close'] - initial_cost

        # Plots EMA crossovers Strategy against a Buy & Hold Approach
        fig, ax = plt.subplots(figsize=(16, 8))
        plt.title(f"Performance of {self.name} EMA Cross Over Strategy")
        plt.plot(df['wealth'], color='green', label='EMA Strategy')
        plt.plot(df['buy_hold'], color='b', label='Buy and Hold Strategy')
        plt.ylabel('USD$')
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.legend()
        plt.show()

        print(f"\nWith an initial investment of $100 in {self.name}, you would have return of ${(100 * roi + 100):,.0f} today")
        print(f'Overall return on investment is {roi_percent:,.2f}%')

        # Only include ROI to compare when strategy is applied to all years
        if year_start is None:
            try:
                with get_connection() as connection:
                    database.insert_ema_values(connection, self.asset, input_fast, input_slow, roi_percent)
            except:
                print("This EMA pair have already been added to the database")
