from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
import csv

DB_NAME = "ecomm"
HOST= "localhost"
MYSQL_USER= "root"
MYSQL_PASSWORD= "ashish123"

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config['SECRET_KEY'] = 'abba jabba dabbba'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{HOST}/{DB_NAME}"

    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = '587'
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'dummygadgetworld@outlook.com'
    app.config['MAIL_DEFAULT_SENDER'] = 'dummygadgetworld@outlook.com'

    app.config['MAIL_PASSWORD'] = 'Dummy@123'


    mail.init_app(app)

    db.init_app(app)

    from .user_views import user_views
    from .seller_views import seller_views
    from .auth import auth

    app.register_blueprint(user_views, url_prefix='/')
    app.register_blueprint(seller_views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Seller, Product, Tag
    from .data import fetch_products
    
    with app.app_context():
        db.create_all()
        fetch_products()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_type = session.get('user_type')
        if user_type == 'user':
            return User.query.get(int(user_id))
        elif user_type == 'seller':
            return Seller.query.get(int(user_id))
        else:
            return None


    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


