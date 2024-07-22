class Stock:
    def __init__(self, ticker, weight, data):
        self.__ticker = ticker.upper()  # Ensure ticker symbol is uppercase
        self.__percentage_in_portfolio = weight
        self.__data = data
        self.__amount_invested = 0
        self.__amount_of_shares = 0


    #Updata the amount of shares
    def set_amount_of_shares(self, amount):
        self.__amount_of_shares += amount

    def set_amount_invested(self, amount):
        self.__amount_invested += amount

    def get_data(self):
        return self.__data

    def get_amount_invested(self):
        return self.__amount_invested
    def get_percentage_in_portfolio(self):
        return self.__percentage_in_portfolio
    def get_ticker(self):
        return self.__ticker
    def get_amount_of_shares(self):
        return self.__amount_of_shares