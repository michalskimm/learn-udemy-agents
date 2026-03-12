import gradio as gr
from accounts import Account

# Global account instance - single user for this demo
account = None

def create_account(user_id, initial_deposit):
    global account
    try:
        account = Account(user_id, float(initial_deposit))
        return f"Account created successfully for {user_id} with initial deposit ${initial_deposit:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def deposit_funds(amount):
    global account
    if account is None:
        return "Please create an account first"
    try:
        account.deposit(float(amount))
        return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def withdraw_funds(amount):
    global account
    if account is None:
        return "Please create an account first"
    try:
        account.withdraw(float(amount))
        return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def buy_shares(symbol, quantity):
    global account
    if account is None:
        return "Please create an account first"
    try:
        account.buy_shares(symbol, int(quantity))
        return f"Bought {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def sell_shares(symbol, quantity):
    global account
    if account is None:
        return "Please create an account first"
    try:
        account.sell_shares(symbol, int(quantity))
        return f"Sold {quantity} shares of {symbol}. New balance: ${account.balance:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def view_portfolio():
    global account
    if account is None:
        return "Please create an account first"
    
    holdings = account.get_holdings()
    portfolio_value = account.calculate_portfolio_value()
    profit_loss = account.get_profit_loss()
    
    output = f"Cash Balance: ${account.balance:.2f}\n\n"
    output += "Holdings:\n"
    if holdings:
        for symbol, quantity in holdings.items():
            output += f"  {symbol}: {quantity} shares\n"
    else:
        output += "  No shares held\n"
    
    output += f"\nTotal Portfolio Value: ${portfolio_value:.2f}\n"
    output += f"Profit/Loss: ${profit_loss:.2f}"
    
    return output

def view_transactions():
    global account
    if account is None:
        return "Please create an account first"
    
    transactions = account.get_transactions()
    if not transactions:
        return "No transactions yet"
    
    output = "Transaction History:\n"
    for i, transaction in enumerate(transactions, 1):
        output += f"{i}. {transaction}\n"
    
    return output

# Create Gradio interface
with gr.Blocks(title="Trading Account Demo") as demo:
    gr.Markdown("# Trading Account Management System")
    gr.Markdown("A simple demo for account management, deposits, withdrawals, and trading shares.")
    
    with gr.Tab("Account Setup"):
        with gr.Row():
            user_id_input = gr.Textbox(label="User ID", value="user123")
            initial_deposit_input = gr.Number(label="Initial Deposit", value=10000)
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_btn.click(create_account, inputs=[user_id_input, initial_deposit_input], outputs=create_output)
    
    with gr.Tab("Deposit/Withdraw"):
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Deposit Amount", value=1000)
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
                deposit_btn.click(deposit_funds, inputs=deposit_amount, outputs=deposit_output)
            
            with gr.Column():
                withdraw_amount = gr.Number(label="Withdraw Amount", value=500)
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
                withdraw_btn.click(withdraw_funds, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Trade Shares"):
        gr.Markdown("Available stocks: AAPL ($150), TSLA ($700), GOOGL ($2800)")
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Stock Symbol", value="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
                buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Stock Symbol", value="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=5)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
                sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        portfolio_btn = gr.Button("View Portfolio")
        portfolio_output = gr.Textbox(label="Portfolio Summary", lines=10)
        portfolio_btn.click(view_portfolio, outputs=portfolio_output)
    
    with gr.Tab("Transactions"):
        transactions_btn = gr.Button("View Transaction History")
        transactions_output = gr.Textbox(label="Transaction History", lines=15)
        transactions_btn.click(view_transactions, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()