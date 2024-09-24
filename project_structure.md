# In the server directory: 
# 1 run.py file:

# -*- coding: utf-8 -*-cls
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# 2 init_db.py file:

import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")


# One directory down is the app directory with the following files:

# 1 _init_.py file:

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dividends.db')
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app

# 2 add_stocks.py file: 

import pandas as pd
import sys
import os

# Adjust the system path to include the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Stock

app = create_app()

with app.app_context():
    # Create all tables (if not already created)
    db.create_all()

    # Get the absolute path of the CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dividend_data.csv')

    # Read stock positions from CSV file
    stock_positions = pd.read_csv(csv_file_path)

    for index, row in stock_positions.iterrows():
        stock = Stock(ticker=row['ticker'], quantity=row['quantity'])
        db.session.add(stock)

    db.session.commit()
    print("Stock positions added successfully!")

# 3 dividend_data.csv

# 4 dividends.db

# 5. models.py

 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Dividend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

# 6. routes.py 

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

# 7 scraper.py
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

# 8 verify_tables.py

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('server/app/dividends.db')
cursor = conn.cursor()

# Query to check if the 'stock' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='stock';")
stock_table = cursor.fetchone()

# Query to check if the 'dividend' table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dividend';")
dividend_table = cursor.fetchone()

# Print the results
if stock_table:
    print("The 'stock' table exists.")
else:
    print("The 'stock' table does not exist.")

if dividend_table:
    print("The 'dividend' table exists.")
else:
    print("The 'dividend' table does not exist.")

# Close the connection
conn.close()


