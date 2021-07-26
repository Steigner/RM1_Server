# library -> app create by python flask server library
from flask import Flask
# library -> manage acces, changes, commits to databases
from flask_sqlalchemy import SQLAlchemy
# library -> manage logging to app
from flask_login import LoginManager

# script -> import Configuration class with set properties 
from config import Config

db = SQLAlchemy()

def create_app():
    # init app
    server_app = Flask(__name__)
    # put set properties to flask engine
    server_app.config.from_object(Config)
    # init database by set properties
    db.init_app(server_app)
    
    # init login manager
    login_manager = LoginManager()
    login_manager.init_app(server_app)
    # protect logging session = strong = protect before use multiple broswers,
    # or devices on the same loggin
    login_manager.session_protection = "strong"
    
    # script -> architecture dabase of users
    from .models import User

    # protect logging
    @login_manager.user_loader
    def load_user(session_token):
        return User.query.filter_by(session_token=session_token).first()

    # Note: This app has 2 blueprints
    # 1. blueprint - app:
    # This blueprient is used as level for basic control app as control,
    # acces to database by read QR code etc ...
    # script -> app routes
    from .routes import app
    server_app.register_blueprint(app)
    
    # 2. blueprint - auth:
    # This blueprient is used as level for acces to databases, admin acces,
    # documentation etc ...
    # script -> authorization routes
    from .routes_auth import auth
    server_app.register_blueprint(auth)
    
    return server_app