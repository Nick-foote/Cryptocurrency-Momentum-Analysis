from connection_pool import get_connection
import database
from models.chart import Chart
from strategy import Strategy

# -- String Statements --

WELCOME = """Welcome to my Cryptocurrency trading strategy program using Exponential Moving Averages.

This strategy uses two EMAs over to calculate moving averages of the Close price over periods of time. 
When the smaller/faster EMA is above the longer/slower EMA, the strategy indicates to buy and go long on the asset.
And then when the faster EMA is below the slower EMA, this indicates to sell the position."""


ASSET_CHOICE = """
Options currently are:

    Bitcoin (btc)
    ETHEREUM (eth)
    XRP (xrp)
    LINK (link)

Enter a asset you want to examine: """


MENU_PROMPT = """
Please pick an option:

    1) Review chart for Price History
    2) Enter EMA values Analysis results for an EMA crossover strategy 
    3) Review best 20 highest performing EMA combinations

    Or press ENTER to quit
  
Your selection:    
"""

crypto_asset_symbols = ['btc', 'eth', 'xrp', 'link']


class App:
    def __init__(self):
        """Initial set up and selection of crypto asset to perform analysis on."""
        self.chart = None
        self.user_asset = None
        print(WELCOME)


    def start(self):
        while True:
            self.user_asset = input(ASSET_CHOICE).lower()
            if self.user_asset in crypto_asset_symbols:
                break
            else:
                print('Invalid Entry. Please enter a symbol.')
                continue

        with get_connection() as connection:
            database.create_ema_table(connection, self.user_asset)
        self.chart = Chart(self.user_asset)
        self.menu()

    def menu(self):
        """turns the menu mapped value into a function()"""
        while len(selection := input(MENU_PROMPT)) != 0:
            if selection == "1":
                self.get_price_chart()
            elif selection == "2":
                self.ema_analysis()
            elif selection == "3":
                self.get_top_20_results()
            else:
                print("Invalid input selected. Please try again.")

    def get_price_chart(self):
        """plots price chart over the whole time range with only the Close price.
        """

        self.chart.get_price_chart()

    def ema_analysis(self):
        strategy = Strategy(self)
        strategy.input_ema_values()
        strategy.analysis()

    def get_top_20_results(self):
        """Retrieves the highest performing EMA pairs for an asset.
        """
        with get_connection() as connection:
            results = database.get_top_20_results(connection, self.user_asset)
            print(f"-- Top performing EMA values (fast/slow) for {self.chart.name} --\n")
            for result in results:
                print(f"{result[0]}/{result[1]} with a return of {result[2]}%")



app = App()

if __name__ == '__main__':
    app.start()

print("-- Exiting App --")