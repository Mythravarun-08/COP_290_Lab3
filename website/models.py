from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    address = db.Column(db.String(300))
    password = db.Column(db.String(150))
    cart_items = db.relationship('CartItems', backref='user')
    order_items = db.relationship('OrderItems', backref='user')

class Seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=False)
    aadhar = db.Column(db.BigInteger, nullable=False)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    photo = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    tags = db.relationship('Tag', secondary='product_tag', backref='products')
    cart_items = db.relationship('CartItems', backref='product')
    order_items = db.relationship('OrderItems', backref='product')

    def __init__(self, name, description, photo, price, stock):
        self.name = name
        self.description = description
        self.photo = photo
        self.price = price
        self.stock = stock

    product_tag = db.Table('product_tag',
        db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    )


class CartItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f"Cart(id={self.id}, product_id={self.product_id}, quantity={self.quantity})"

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity})"