from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import csv

DB_NAME = "ecomm"
HOST= "localhost"
MYSQL_USER= "root"
MYSQL_PASSWORD= "Abcd_123"

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'abba jabba dabbba'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOST}/{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Seller, Product, Tag
    from .data import fetch_products

    
    
    with app.app_context():
        db.create_all()
        fetch_products()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id:
            user = User.query.get(int(user_id))
            if user is not None:
                return user
            seller = Seller.query.get(int(user_id))
            if seller is not None:
                return seller

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


