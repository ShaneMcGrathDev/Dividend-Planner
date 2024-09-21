# Here you are initializing your database

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dividends.db'
    db.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app