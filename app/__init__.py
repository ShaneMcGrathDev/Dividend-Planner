from flask import Flask
from .config import Config
from .models import db
from .routes import bp as main_bp  # Import the blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(main_bp, url_prefix='/api')  # Make sure the url_prefix is set


    with app.app_context():
        db.create_all()  # Create database tables


    return app
