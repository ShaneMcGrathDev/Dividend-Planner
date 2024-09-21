import requests
from bs4 import BeautifulSoup
from .models import Stock  # Import the Stock model

def get_stock_info(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the necessary information
    # Example: dividend yield
    dividend_yield = soup.find('td', {'data-test': 'DIVIDEND_AND_YIELD-value'}).text
    return dividend_yield



def calculate_dividends():
    stocks = Stock.query.all()
    total_dividends = 0
    for stock in stocks:
        dividend_yield = get_stock_info(stock.ticker)
        total_dividends += stock.quantity * float(dividend_yield.split()[0])
    return total_dividends