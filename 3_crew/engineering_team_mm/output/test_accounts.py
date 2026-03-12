import unittest
from unittest.mock import patch
from accounts import Account, get_share_price


class TestGetSharePrice(unittest.TestCase):
    """Test cases for the get_share_price function."""
    
    def test_get_share_price_known_symbol(self):
        """Test getting price for known stock symbols."""
        self.assertEqual(get_share_price("AAPL"), 150.00)
        self.assertEqual(get_share_price("TSLA"), 700.00)
        self.assertEqual(get_share_price("GOOGL"), 2800.00)
    
    def test_get_share_price_unknown_symbol(self):
        """Test getting price for unknown stock symbol."""
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)


class TestAccountInitialization(unittest.TestCase):
    """Test cases for Account initialization."""
    
    def test_account_initialization(self):
        """Test that account initializes correctly."""
        account = Account("user123", 1000.0)
        self.assertEqual(account.user_id, "user123")
        self.assertEqual(account.initial_deposit, 1000.0)
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.transaction_history, [])
    
    def test_account_initialization_zero_deposit(self):
        """Test account initialization with zero deposit."""
        account = Account("user456", 0.0)
        self.assertEqual(account.balance, 0.0)
        self.assertEqual(account.initial_deposit, 0.0)


class TestAccountDeposit(unittest.TestCase):
    """Test cases for deposit functionality."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account("user123", 1000.0)
    
    def test_deposit_positive_amount(self):
        """Test depositing a positive amount."""
        self.account.deposit(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertIn("Deposited $500.00", self.account.transaction_history)
    
    def test_deposit_multiple_times(self):
        """Test multiple deposits."""
        self.account.deposit(200.0)
        self.account.deposit(300.0)
        self.assertEqual(self.account.balance, 1500.0)
        self.assertEqual(len(self.account.transaction_history), 2)
    
    def test_deposit_negative_amount(self):
        """Test that depositing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(-100.0)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")
    
    def test_deposit_zero_amount(self):
        """Test that depositing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.deposit(0.0)
        self.assertEqual(str(context.exception), "Deposit amount must be positive")


class TestAccountWithdrawal(unittest.TestCase):
    """Test cases for withdrawal functionality."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account("user123", 1000.0)
    
    def test_withdraw_valid_amount(self):
        """Test withdrawing a valid amount."""
        self.account.withdraw(300.0)
        self.assertEqual(self.account.balance, 700.0)
        self.assertIn("Withdrew $300.00", self.account.transaction_history)
    
    def test_withdraw_entire_balance(self):
        """Test withdrawing entire balance."""
        self.account.withdraw(1000.0)
        self.assertEqual(self.account.balance, 0.0)
    
    def test_withdraw_insufficient_funds(self):
        """Test that withdrawing more than balance raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(1500.0)
        self.assertEqual(str(context.exception), "Insufficient funds for withdrawal")
    
    def test_withdraw_negative_amount(self):
        """Test that withdrawing negative amount raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(-100.0)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")
    
    def test_withdraw_zero_amount(self):
        """Test that withdrawing zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.withdraw(0.0)
        self.assertEqual(str(context.exception), "Withdrawal amount must be positive")


class TestAccountBuyShares(unittest.TestCase):
    """Test cases for buying shares."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account("user123", 10000.0)
    
    def test_buy_shares_valid(self):
        """Test buying shares with sufficient funds."""
        self.account.buy_shares("AAPL", 10)
        self.assertEqual(self.account.balance, 10000.0 - (150.0 * 10))
        self.assertEqual(self.account.holdings["AAPL"], 10)
        self.assertIn("Bought 10 shares of AAPL at $150.00 each", self.account.transaction_history)
    
    def test_buy_shares_multiple_times_same_symbol(self):
        """Test buying same stock multiple times."""
        self.account.buy_shares("AAPL", 5)
        self.account.buy_shares("AAPL", 3)
        self.assertEqual(self.account.holdings["AAPL"], 8)
        self.assertEqual(self.account.balance, 10000.0 - (150.0 * 8))
    
    def test_buy_shares_different_symbols(self):
        """Test buying different stocks."""
        self.account.buy_shares("AAPL", 5)
        self.account.buy_shares("TSLA", 2)
        self.assertEqual(self.account.holdings["AAPL"], 5)
        self.assertEqual(self.account.holdings["TSLA"], 2)
        expected_balance = 10000.0 - (150.0 * 5) - (700.0 * 2)
        self.assertEqual(self.account.balance, expected_balance)
    
    def test_buy_shares_insufficient_funds(self):
        """Test buying shares with insufficient funds."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("GOOGL", 100)
        self.assertEqual(str(context.exception), "Insufficient funds to buy shares")
    
    def test_buy_shares_negative_quantity(self):
        """Test buying negative quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("AAPL", -5)
        self.assertEqual(str(context.exception), "Quantity must be positive")
    
    def test_buy_shares_zero_quantity(self):
        """Test buying zero quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.buy_shares("AAPL", 0)
        self.assertEqual(str(context.exception), "Quantity must be positive")


class TestAccountSellShares(unittest.TestCase):
    """Test cases for selling shares."""
    
    def setUp(self):
        """Set up test account with holdings before each test."""
        self.account = Account("user123", 10000.0)
        self.account.buy_shares("AAPL", 20)
        self.account.buy_shares("TSLA", 5)
    
    def test_sell_shares_valid(self):
        """Test selling shares that exist in holdings."""
        initial_balance = self.account.balance
        self.account.sell_shares("AAPL", 10)
        self.assertEqual(self.account.holdings["AAPL"], 10)
        self.assertEqual(self.account.balance, initial_balance + (150.0 * 10))
        self.assertIn("Sold 10 shares of AAPL at $150.00 each", self.account.transaction_history)
    
    def test_sell_all_shares_of_symbol(self):
        """Test selling all shares of a symbol removes it from holdings."""
        self.account.sell_shares("TSLA", 5)
        self.assertNotIn("TSLA", self.account.holdings)
        self.assertEqual(self.account.holdings["AAPL"], 20)
    
    def test_sell_shares_not_owned(self):
        """Test selling shares not owned raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("GOOGL", 1)
        self.assertEqual(str(context.exception), "You do not have enough shares to sell")
    
    def test_sell_more_shares_than_owned(self):
        """Test selling more shares than owned raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", 25)
        self.assertEqual(str(context.exception), "You do not have enough shares to sell")
    
    def test_sell_shares_negative_quantity(self):
        """Test selling negative quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", -5)
        self.assertEqual(str(context.exception), "Quantity must be positive")
    
    def test_sell_shares_zero_quantity(self):
        """Test selling zero quantity raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.account.sell_shares("AAPL", 0)
        self.assertEqual(str(context.exception), "Quantity must be positive")


class TestAccountPortfolioCalculations(unittest.TestCase):
    """Test cases for portfolio value and profit/loss calculations."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account("user123", 10000.0)
    
    def test_calculate_portfolio_value_cash_only(self):
        """Test portfolio value with only cash."""
        portfolio_value = self.account.calculate_portfolio_value()
        self.assertEqual(portfolio_value, 10000.0)
    
    def test_calculate_portfolio_value_with_holdings(self):
        """Test portfolio value with cash and holdings."""
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 2)
        portfolio_value = self.account.calculate_portfolio_value()
        expected_value = self.account.balance + (150.0 * 10) + (700.0 * 2)
        self.assertEqual(portfolio_value, expected_value)
    
    def test_calculate_profit_loss_no_change(self):
        """Test profit/loss when no transactions occurred."""
        profit_loss = self.account.calculate_profit_loss()
        self.assertEqual(profit_loss, 0.0)
    
    def test_calculate_profit_loss_with_profit(self):
        """Test profit/loss calculation with profit."""
        self.account.deposit(5000.0)
        profit_loss = self.account.calculate_profit_loss()
        self.assertEqual(profit_loss, 5000.0)
    
    def test_calculate_profit_loss_with_loss(self):
        """Test profit/loss calculation with loss."""
        self.account.withdraw(3000.0)
        profit_loss = self.account.calculate_profit_loss()
        self.assertEqual(profit_loss, -3000.0)
    
    def test_calculate_profit_loss_with_trading(self):
        """Test profit/loss after buying and selling."""
        initial_balance = self.account.balance
        self.account.buy_shares("AAPL", 10)
        self.account.sell_shares("AAPL", 10)
        portfolio_value = self.account.calculate_portfolio_value()
        self.assertEqual(portfolio_value, initial_balance)
        self.assertEqual(self.account.calculate_profit_loss(), 0.0)


class TestAccountGetters(unittest.TestCase):
    """Test cases for getter methods."""
    
    def setUp(self):
        """Set up test account before each test."""
        self.account = Account("user123", 10000.0)
    
    def test_get_holdings_empty(self):
        """Test getting holdings when none exist."""
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {})
    
    def test_get_holdings_with_shares(self):
        """Test getting holdings when shares exist."""
        self.account.buy_shares("AAPL", 10)
        self.account.buy_shares("TSLA", 5)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {"AAPL": 10, "TSLA": 5})
    
    def test_get_holdings_returns_copy(self):
        """Test that get_holdings returns a copy, not reference."""
        self.account.buy_shares("AAPL", 10)
        holdings = self.account.get_holdings()
        holdings["AAPL"] = 999
        self.assertEqual(self.account.holdings["AAPL"], 10)
    
    def test_get_profit_loss(self):
        """Test get_profit_loss method."""
        self.account.deposit(2000.0)
        profit_loss = self.account.get_profit_loss()
        self.assertEqual(profit_loss, 2000.0)
    
    def test_get_transactions_empty(self):
        """Test getting transactions when none exist."""
        transactions = self.account.get_transactions()
        self.assertEqual(transactions, [])
    
    def test_get_transactions_with_history(self):
        """Test getting transactions when history exists."""
        self.account.deposit(500.0)
        self.account.withdraw(200.0)
        self.account.buy_shares("AAPL", 5)
        transactions = self.account.get_transactions()
        self.assertEqual(len(transactions), 3)
        self.assertIn("Deposited $500.00", transactions)
        self.assertIn("Withdrew $200.00", transactions)
    
    def test_get_transactions_returns_copy(self):
        """Test that get_transactions returns a copy, not reference."""
        self.account.deposit(500.0)
        transactions = self.account.get_transactions()
        transactions.append("Fake transaction")
        self.assertEqual(len(self.account.transaction_history), 1)


class TestAccountIntegration(unittest.TestCase):
    """Integration tests for complex account scenarios."""
    
    def test_complete_trading_scenario(self):
        """Test a complete trading scenario with multiple operations."""
        account = Account("trader001", 5000.0)
        
        account.deposit(5000.0)
        self.assertEqual(account.balance, 10000.0)
        
        account.buy_shares("AAPL", 10)
        account.buy_shares("TSLA", 5)
        
        expected_balance = 10000.0 - (150.0 * 10) - (700.0 * 5)
        self.assertEqual(account.balance, expected_balance)
        
        account.sell_shares("AAPL", 5)
        expected_balance += 150.0 * 5
        self.assertEqual(account.balance, expected_balance)
        
        portfolio_value = account.calculate_portfolio_value()
        expected_portfolio = expected_balance + (150.0 * 5) + (700.0 * 5)
        self.assertEqual(portfolio_value, expected_portfolio)
        
        self.assertEqual(len(account.get_transactions()), 4)
    
    def test_edge_case_buy_and_sell_all(self):