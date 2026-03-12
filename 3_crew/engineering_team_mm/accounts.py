
class Account:
    """
    A class to manage user accounts for a trading simulation platform.
    """

    def __init__(self, username: str, initial_deposit: float):
        """
        Initializes the account with a username and an initial deposit.
        
        :param username: The username of the account holder
        :param initial_deposit: The initial amount to deposit into the account
        """
        self.username = username
        self.balance = initial_deposit  # Current account balance
        self.portfolio = {}  # Dictionary to hold shares and their quantities
        self.transactions = []  # List to hold transaction records
        self.initial_deposit = initial_deposit  # Store initial deposit for profit/loss calculations

    def deposit(self, amount: float):
        """
        Deposits an amount into the account.
        
        :param amount: The amount to deposit
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount: float):
        """
        Withdraws an amount from the account, if sufficient balance is present.
        
        :param amount: The amount to withdraw
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds for withdrawal.")
        self.balance -= amount
        self.transactions.append(f"Withdrew: {amount}")

    def buy_shares(self, symbol: str, quantity: int):
        """
        Buys a certain quantity of shares for a given symbol.
        
        :param symbol: The stock symbol to buy
        :param quantity: The quantity of shares to buy
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to buy shares.")
        
        self.balance -= total_cost
        self.portfolio[symbol] = self.portfolio.get(symbol, 0) + quantity
        self.transactions.append(f"Bought {quantity} shares of {symbol} at {share_price} each.")

    def sell_shares(self, symbol: str, quantity: int):
        """
        Sells a certain quantity of shares for a given symbol.
        
        :param symbol: The stock symbol to sell
        :param quantity: The quantity of shares to sell
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")
        
        share_price = get_share_price(symbol)
        proceeds = share_price * quantity
        
        self.portfolio[symbol] -= quantity
        if self.portfolio[symbol] == 0:
            del self.portfolio[symbol]
        self.balance += proceeds
        self.transactions.append(f"Sold {quantity} shares of {symbol} at {share_price} each.")

    def calculate_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.

        :return: Total value of the portfolio.
        """
        total_value = sum(get_share_price(symbol) * quantity for symbol, quantity in self.portfolio.items())
        return total_value + self.balance

    def calculate_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        :return: Profit or loss amount.
        """
        current_value = self.calculate_portfolio_value()
        return current_value - self.initial_deposit

    def get_holdings(self) -> dict:
        """
        Returns the current holdings of the user.
        
        :return: A dictionary of the user's shares and their quantities.
        """
        return self.portfolio

    def get_profit_loss(self) -> float:
        """
        Returns the profit or loss of the user.
        
        :return: Profit or loss amount.
        """
        return self.calculate_profit_loss()

    def list_transactions(self) -> list:
        """
        Returns a list of all transactions made by the user.
        
        :return: A list of transaction records.
        """
        return self.transactions


def get_share_price(symbol: str) -> float:
    """
    A mock function to return fixed prices for specific stock symbols.

    :param symbol: The stock symbol to retrieve the price for
    :return: The price of the share for the given symbol
    """
    prices = {
        "AAPL": 150.00,
        "TSLA": 700.00,
        "GOOGL": 2800.00
    }
    return prices.get(symbol, 0.0)
