# accounts.py

class Account:
    """
    A simple account management system for a trading simulation platform.
    """

    def __init__(self, user_id: str, initial_deposit: float):
        """
        Initializes a new account with a unique user ID and an initial deposit.
        
        :param user_id: Unique identifier for the user.
        :param initial_deposit: Initial amount deposited into the account.
        """
        self.user_id = user_id
        self.initial_deposit = initial_deposit
        self.balance = initial_deposit
        self.holdings = {}  # Dictionary to hold stock shares (symbol: quantity)
        self.transaction_history = []  # List to record transaction history

    def deposit(self, amount: float) -> None:
        """
        Deposits funds into the account.
        
        :param amount: Amount to be deposited.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.transaction_history.append(f"Deposited ${amount:.2f}")

    def withdraw(self, amount: float) -> None:
        """
        Withdraws funds from the account, if sufficient balance exists.
        
        :param amount: Amount to be withdrawn.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds for withdrawal")
        self.balance -= amount
        self.transaction_history.append(f"Withdrew ${amount:.2f}")

    def buy_shares(self, symbol: str, quantity: int) -> None:
        """
        Buys shares of a stock.
        
        :param symbol: Stock symbol of the shares to buy.
        :param quantity: Number of shares to buy.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        share_price = get_share_price(symbol)
        total_cost = share_price * quantity
        
        if self.balance < total_cost:
            raise ValueError("Insufficient funds to buy shares")
        
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self.transaction_history.append(f"Bought {quantity} shares of {symbol} at ${share_price:.2f} each")

    def sell_shares(self, symbol: str, quantity: int) -> None:
        """
        Sells shares of a stock.
        
        :param symbol: Stock symbol of the shares to sell.
        :param quantity: Number of shares to sell.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("You do not have enough shares to sell")
        
        share_price = get_share_price(symbol)
        total_revenue = share_price * quantity
        
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]  # Remove symbol if no shares left
        
        self.transaction_history.append(f"Sold {quantity} shares of {symbol} at ${share_price:.2f} each")

    def calculate_portfolio_value(self) -> float:
        """
        Calculates the total value of the user's portfolio.
        
        :return: Total value of the portfolio including cash and holdings.
        """
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_loss(self) -> float:
        """
        Calculates the profit or loss from the initial deposit.
        
        :return: Profit or loss from the initial deposit.
        """
        return self.calculate_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        """
        Reports the current holdings of the user.
        
        :return: A dictionary of stocks and their respective quantities held.
        """
        return self.holdings.copy()

    def get_profit_loss(self) -> float:
        """
        Reports the profit or loss of the user.
        
        :return: Current profit or loss from initial deposit to current state.
        """
        return self.calculate_profit_loss()

    def get_transactions(self) -> list:
        """
        Lists all transactions made by the user.
        
        :return: List of transaction records.
        """
        return self.transaction_history.copy()


def get_share_price(symbol: str) -> float:
    """
    A mock function to get share price for testing.

    :param symbol: The stock symbol to retrieve the price for.
    :return: The current price of the stock.
    """
    prices = {
        "AAPL": 150.00,
        "TSLA": 700.00,
        "GOOGL": 2800.00
    }
    return prices.get(symbol, 0.0)  # Return 0 if the stock is not found