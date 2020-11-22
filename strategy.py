import datetime
import pytz

from models.chart import Chart


YEAR_PROMPT = """
    Would you like to see how the strategy performs over specific years? 
    (otherwise analysis will be over all the price history available) (y/N)
    """


class Strategy:
    """Performs analysis on the EMA crossover trading strategy."""
    def __init__(self, app):
        self.app = app
        self.input_fast = None
        self.input_slow = None
        self.year_start = None
        self.year_end = None


    def input_ema_values(self):
        """function to get user input values for both fast and slow EMA.
        Will only accept an integer for EMA values. Forces user to input a higher
        integer for Slow EMA than Fast EMA.
        """
        while True:
            try:
                self.input_fast = int(input("Enter the fast/lower EMA: "))
            except ValueError:
                print("\nInvalid entry. Please enter a number")
            else:
                break

        while True:
            try:
                self.input_slow = int(input("Enter the slow/higher EMA: "))
                if self.input_slow < self.input_fast:
                    raise Exception
            except ValueError:
                print("\nInvalid entry. Please enter a number.")
            except Exception:
                print("\nInvalid entry. The Slow EMA needs to be larger than the Fast EMA. Please try again.")
            else:
                break

    def analysis(self):
        """Asks user to select certain years to examine or else will perform the trading strategy over all the years available.
        """
        self.year_log = input(YEAR_PROMPT)
        if self.year_log == "y":
            self.selected_years()
        else:
            self.app.chart.perform_strategy(self)

    def selected_years(self):
        """"""
        self.year_start = int(input("Enter the year you wish to Start from (2016 earliest): "))
        self.year_end = input("Enter the year you wish to End from (or press enter to end in the present): ")

        self.year_start = datetime.datetime(
            year=self.year_start, month=1, day=1, hour=0, minute=0, second=0
        ).astimezone(pytz.utc)

        if self.year_end:
            year_end = datetime.datetime(
                year=int(self.year_end), month=1, day=1, hour=0, minute=0, second=0
            ).astimezone(pytz.utc)

        self.app.chart.perform_strategy(self)
