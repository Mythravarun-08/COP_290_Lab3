from . import db
from flask_login import UserMixin

from sqlalchemy.sql import func

# class RoleMixin:
#     @property
#     def is_user(self):
#         return isinstance(self, User)

#     @property
#     def is_seller(self):
#         return isinstance(self, Seller)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    address = db.Column(db.String(300))
    phone_number = db.Column(db.BigInteger, nullable=False)
    password = db.Column(db.String(150))
    cart_items = db.relationship('CartItems', backref='user')
    order_items = db.relationship('OrderItems', backref='user')
    search_history = db.relationship('SearchHistory', backref='user')
    def get_id(self):
        return str(self.id)
    
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    searches = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=func.now())


class Seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.BigInteger, nullable=False)
    aadhar = db.Column(db.BigInteger, nullable=False)
    product_items = db.relationship('Product', backref='seller')
    ordered_items = db.relationship('OrderedItems', backref='seller')
    def get_id(self):
        return str(self.id)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(15), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    photo = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    tags = db.relationship('Tag', secondary='product_tag', backref='products')
    cart_items = db.relationship('CartItems', backref='product')
    order_items = db.relationship('OrderItems', backref='product')
    # product_items = db.relationship('ProductItems', backref='product')
    ordered_items = db.relationship('OrderedItems', backref='product')

    def __init__(self, name, description, photo, price, stock, seller_id, type):
        self.name = name
        self.description = description
        self.photo = photo
        self.price = price
        self.stock = stock
        self.seller_id= seller_id
        self.type= type

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
    
# class ProductItems(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Product(id={self.id}, product_id={self.product_id}, quantity={self.quantity})"

class OrderedItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Order(id={self.id}, product_id={self.product_id}, quantity={self.quantity})"