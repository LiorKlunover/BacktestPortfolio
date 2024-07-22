from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd

class Portfolio:
    def __init__(self, initial_investment, monthly_investment, start_date, end_date):
        """
        Initializes the Portfolio with the given parameters.

        :param initial_investment: Initial amount of money invested
        :param monthly_investment: Amount of money invested monthly
        :param start_date: Start date of the investment
        :param end_date: End date of the investment
        """
        self.stocks = []
        self.initial_investment = initial_investment
        self.monthly_investment = monthly_investment
        self.total_amount_invested = 0
        self.start_date = start_date
        self.end_date = end_date
        self.current_total_value = 0
        self.acount_balacne = initial_investment


    def add_stock(self, stock):
        """
        Adds a Stock object to the portfolio.

        :param stock: Stock object to be added
        """
        self.stocks.append(stock)


    def set_acount_balacne(self, amount_to_decrease):
        """
        Updates the total value of the portfolio.
        :param amount_to_decrease: Amount to decrease from the total value
        """
        self.acount_balacne -= amount_to_decrease

    def calculate_initial_portfolio(self):
        """
        Calculates the total value of the portfolio.
        :return: Total value of the portfolio
        """
        self.total_amount_invested = self.initial_investment
        for stock in self.stocks:
            try:
                amount = self.initial_investment * stock.get_percentage_in_portfolio()
                self.buy_fractions_stock(stock, amount, self.start_date)
            except Exception as e:
                print(f"Error calculating portfolio for stock {stock.symbol}: {e}")

    def calculate_monthly_portfolio(self, start_date):
        """
        Calculates the total value of the portfolio on a monthly basis.

        :param start_date: The starting date of the calculation.
        """
        dates = self.get_valid_months_dates(self.stocks[0].get_data(), start_date, self.end_date, start_date.day)
        for date in dates:
            self.set_acount_balacne(-self.monthly_investment)
            self.total_amount_invested += self.monthly_investment
            for stock in self.stocks:
                try:
                    amount = self.monthly_investment * stock.get_percentage_in_portfolio()
                    self.buy_fractions_stock(stock, amount, date)
                except Exception as e:
                    print(f"Error calculating portfolio for stock {stock.symbol} on {date}: {e}")

    def get_current_total_value(self):
        for stock in self.stocks:
            last_close_price = stock.get_data().iloc[-1]['Close']
            self.current_total_value += stock.get_amount_of_shares() * last_close_price
        return self.current_total_value + self.acount_balacne

    def buy_full_stock(self, stock, amount, day_to_buy):
        """
        Buys a stock and adds it to the portfolio.

        :param stock: Stock object to buy
        :param amount: Amount to invest in the stock
        :param day_to_buy: Date to buy the stock (string format "YYYY-MM-DD")
        :return: Number of shares bought
        """
        try:
            data = stock.get_data()
            day_to_buy = pd.to_datetime(day_to_buy)
            closing_price = data.at[day_to_buy, 'Close']
            number_of_shares = int(amount / closing_price)
            stock.set_amount_invested(number_of_shares * closing_price)
            stock.set_amount_of_shares(number_of_shares)
            self.set_acount_balacne(number_of_shares * closing_price)
            print(f"Bought {number_of_shares} shares of {stock.get_ticker()} at {closing_price} on {day_to_buy}" )
            print("account balance: ", self.acount_balacne)
            return number_of_shares
        except KeyError:
            print(f"No data available for {stock.get_ticker()} the date: {day_to_buy}")
            return 0
        except Exception as e:
            print(f"Error buying stock {stock.symbol}: {e}")
            return 0
    def buy_fractions_stock(self, stock, amount, day_to_buy):
        """
        Buys a stock and adds it to the portfolio.

        :param stock: Stock object to buy
        :param amount: Amount to invest in the stock
        :param day_to_buy: Date to buy the stock (string format "YYYY-MM-DD")
        :return: Number of shares bought
        """
        try:
            data = stock.get_data()
            day_to_buy = pd.to_datetime(day_to_buy)
            closing_price = data.at[day_to_buy, 'Close']
            number_of_shares = amount / closing_price
            stock.set_amount_invested(amount)
            stock.set_amount_of_shares(number_of_shares)
            self.set_acount_balacne(amount)
            print(f"Bought {number_of_shares} shares of {stock.get_ticker()} at {closing_price} on {day_to_buy}" )
            print("account balance: ", self.acount_balacne)
            return number_of_shares
        except KeyError:
            print(f"No data available for {stock.get_ticker()} the date: {day_to_buy}")
            return 0
        except Exception as e:
            print(f"Error buying stock {stock.symbol}: {e}")
            return 0
    def get_valid_months_dates(self, data, start_date, end_date, date_in_month):
        """
        Get valid dates where data exists for each specified day of the month between start and end dates.

        :param data: DataFrame containing date and 'Close' columns.
        :param start_date: The starting date of the search.
        :param end_date: The ending date of the search.
        :param date_in_month: The specific day of the month to check for data availability.
        :return: List of valid dates.
        """
        valid_dates = []
        current_date = start_date

        while current_date <= end_date:
            try:
                # Set the target date to the specified day in the current month
                target_date = current_date.replace(day=date_in_month)
            except ValueError:
                # If the day is invalid for the month (e.g., February 30), set to the last day of the month
                next_month = current_date + relativedelta(months=1)
                target_date = next_month.replace(day=1) - timedelta(days=1)

            # Ensure target date is within the provided date range
            if target_date > end_date:
                break

            # If the target date is valid, add to the list
            if target_date in data.index:
                valid_dates.append(target_date)
            else:
                # If the exact target date is not available, search for the nearest valid date
                while target_date.month == current_date.month:
                    target_date += timedelta(days=1)
                    if target_date in data.index:
                        valid_dates.append(target_date)
                        break

            # Move to the next month
            current_date += relativedelta(months=1)
            current_date = current_date.replace(day=1)

        return valid_dates
