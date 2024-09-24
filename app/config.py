# app/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'dividends.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
