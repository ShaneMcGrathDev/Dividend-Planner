from flask import Blueprint, jsonify
from .models import Stock
import requests  # Optional, if you fetch yields from an API

bp = Blueprint('main', __name__)

@bp.route('/calculate_dividends', methods=['GET'])
def calculate_dividends():
    stocks = Stock.query.all()
    total_dividends = 0

    for stock in stocks:
        # Replace this with your logic to get the dividend yield for each stock
        dividend_yield = get_dividend_yield(stock.ticker)
        
        # Calculate dividends for the stock
        if dividend_yield:
            # Assume dividend_yield is a percentage (e.g., 0.05 for 5%)
            dividend_amount = stock.quantity * dividend_yield
            total_dividends += dividend_amount

    return jsonify({'total_dividends': total_dividends})

def get_dividend_yield(ticker):
    # Placeholder for your logic to fetch the dividend yield for a given ticker
    # You can use a web scraper or API request here
    # For demonstration purposes, we'll return a fixed value
    # In a real scenario, you'd implement actual fetching logic
    return 0.05  # Example: 5% yield