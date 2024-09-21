from flask import Blueprint, request, jsonify
from .models import Stock, db
from .scraper import get_stock_info

bp = Blueprint('main', __name__)

@bp.route('/add_stock', methods=['POST'])
def add_stock():
    data = request.get_json()
    new_stock = Stock(ticker=data['ticker'], quantity=data['quantity'])
    db.session.add(new_stock)
    db.session.commit()
    return jsonify({'message': 'Stock added successfully!'})

@bp.route('/stocks', methods=['GET'])
def get_stocks():
    stocks = Stock.query.all()
    return jsonify([{'ticker': stock.ticker, 'quantity': stock.quantity} for stock in stocks])

@bp.route('/calculate_dividends', methods=['GET'])
def calculate_dividends():
    stocks = Stock.query.all()
    total_dividends = 0
    for stock in stocks:
        dividend_yield = get_stock_info(stock.ticker)
        total_dividends += stock.quantity * float(dividend_yield.split()[0])
    return jsonify({'total_dividends': total_dividends})








# This was the default set up modified with the test API route before updating

# from flask import Blueprint, jsonify

# bp = Blueprint('main', __name__)

# @bp.route('/api/test', methods=['GET'])
# def test():
#     return jsonify({"message": "Backend Connection Test Worked!"})