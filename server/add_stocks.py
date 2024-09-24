# server/add_stocks.py
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Stock

app = create_app()

with app.app_context():
    csv_file_path = os.path.join(os.path.dirname(__file__), 'dividend_data.csv')
    stock_positions = pd.read_csv(csv_file_path)

    for index, row in stock_positions.iterrows():
        stock = Stock(ticker=row['ticker'], quantity=row['quantity'])
        db.session.add(stock)

    db.session.commit()
    print("Stock positions added successfully!")
