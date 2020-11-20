import datetime
import pytz

from connection_pool import get_connection
import database
from models.chart import Chart

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


YEAR_PROMPT = """
    Would you like to see how the strategy performs over specific years? 
    (otherwise analysis will be over all the price history available) (y/N)
    """


# -- Functions --

def prompt_get_price_chart():
    """plots price chart over the whole time range with only the Close price
    """
    Chart(user_asset.lower()).get_price_chart()


def input_ema_values():
    """function to get user input values for both fast and slow EMA.
    Will only accept an integer for EMA values. Forces user to input a higher
    integer for Slow EMA than Fast EMA.
    """
    while True:
        try:
            input_fast = int(input("Enter the fast/lower EMA: "))
        except ValueError:
            print("\nInvalid entry. Please enter a number")
        else:
            break

    while True:
        try:
            input_slow = int(input("Enter the slow/higher EMA: "))
            if input_slow < input_fast:
                raise Exception
        except ValueError:
            print("\nInvalid entry. Please enter a number.")
        except Exception:
            print("\nInvalid entry. The Slow EMA needs to be larger than the Fast EMA. Please try again.")
        else:
            break

    return input_fast, input_slow


def prompt_ema_analysis():
    input_fast, input_slow = input_ema_values()

    year_log = input(YEAR_PROMPT)
    if year_log == "y":
        year_start = int(input("Enter the year you wish to Start from (2016 earliest): "))
        year_end = input("Enter the year you wish to End from (or press enter to end in the present): ")

        year_start = datetime.datetime(
            year=year_start, month=1, day=1, hour=0, minute=0, second=0
        ).astimezone(pytz.utc)

        if year_end:
            year_end = datetime.datetime(
                year=int(year_end), month=1, day=1, hour=0, minute=0, second=0
            ).astimezone(pytz.utc)

        # Analysis over user selected years, non year specific
        analysis = Chart(user_asset)
        analysis.ema_strategy(input_fast, input_slow, year_start, year_end)

    # Analysis over the available price history, non year specific
    else:
        analysis = Chart(user_asset)
        analysis.ema_strategy(input_fast, input_slow)


# Retrieves the highest performing EMA pairs for an asset
def prompt_get_top_20_results():
    with get_connection() as connection:
        results = database.get_top_20_results(connection, user_asset)
        print_results(results)


def print_results(results):
    print(f"-- Top performing EMA values (fast/slow) for crypto asset --\n")
    for result in results:
        print(f"{result[0]}/{result[1]} with a return of {result[2]}%")


# -- App Menu --

# Mapping the menu to actions
MENU_OPTIONS = {
    "1": prompt_get_price_chart,
    "2": prompt_ema_analysis,
    "3": prompt_get_top_20_results,
}


def menu():
    print(WELCOME)

    with get_connection() as connection:
        database.create_ema_table(connection, user_asset)

    while len(selection := input(MENU_PROMPT)) != 0:
        try:
            MENU_OPTIONS[selection]()        # turns the menu mapped value into a function()
        except KeyError:
            print("Invalid input selected. Please try again.")


user_asset = input(ASSET_CHOICE)

menu()

print("-- Exiting App --")