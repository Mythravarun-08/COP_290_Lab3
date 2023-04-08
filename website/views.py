from flask import Blueprint, render_template, request, flash, jsonify,redirect, url_for,request
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import text
from .models import Note,Product, CartItems, OrderItems
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    action = request.args.get('action')
    if action == 'Login':
        return redirect(url_for('auth.login'))
    elif action == 'Sign up':
        return redirect(url_for('auth.sign_up'))
    elif action == 'Seller Login':
        return redirect(url_for('auth.seller_login'))
    elif action == 'Become a Seller':
        return redirect(url_for('auth.seller_sign_up'))
    else:
        products = Product.query.all()
        return render_template("index.html", user=current_user,products = products) # render the html we made for this 
    
@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('views.home'))
    product_id=request.args.get('product_id')
    if product_id is not None:
        return redirect(url_for('views.product_page', product_id=product_id))
    action = request.args.get('action')
    # print(action, "ACTIONN")
    if action == 'cart':
        return redirect(url_for('views.cart'))
    elif action == 'myaccount':
        return redirect(url_for('views.myaccount'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    else:
        products = Product.query.all()
        # Pass the fetched products to the template
        return render_template("dashboard.html", user=current_user, products=products)

@views.route('/conformation/<int:product_id>', methods=['GET', 'POST'])
def conformation(product_id):
    product = Product.query.get_or_404(product_id)
    action = request.args.get('action')
    if action == 'confirm-buy':
        order_item = OrderItems(user_id=current_user.id, product_id=product.id, quantity=1)
        current_user.order_items.append(order_item)
        db.session.commit()
        return redirect(url_for('views.myaccount'))

    return render_template("conformation-page.html", user=current_user)    
    
@views.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('views.home'))
    action = request.args.get('action')
    print(action)
    if action == 'cart':
        return redirect(url_for('views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    elif action=='dashboard':
        return redirect(url_for('views.dashboard'))
    
    order_items = OrderItems.query.filter_by(user_id=current_user.id).all()
    # create an empty list to store the Product objects
    products = []

    # loop through the OrderItems objects and retrieve the corresponding Product objects
    for order_item in order_items:
        product = Product.query.get(order_item.product_id)
        if product:
            products.append(product)

    bound=min(len(order_items),4)
    # return render_template("cart.html", user=current_user, order_items=order_items,products=products,bound=bound)
    return render_template("profile-page.html", user=current_user,order_items=order_items,products=products,bound=bound) # render the html we made for this


@views.route('/product-page/<int:product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    product = Product.query.get_or_404(product_id)
    action = request.args.get('action')
    print(action)
    if action == 'buy-now':
        return redirect(url_for('views.conformation', product_id=product_id))
    elif action == 'myaccount':
        return redirect(url_for('views.myaccount'))
    elif action=='cart':
        return redirect(url_for('views.cart'))
    elif action == 'add-to-cart':
        cart_item = CartItems(user_id=current_user.id, product_id=product.id, quantity=1)
        current_user.cart_items.append(cart_item)
        db.session.commit()
        return redirect(url_for('views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    return render_template("product-page.html", user=current_user, product=product)

@views.route('/cart-conformation', methods=['GET', 'POST'])
def cart_conformation():

    cart_items=CartItems.query.filter_by(user_id=current_user.id).all()

    action = request.args.get('action')
    if action == 'confirm-buy':
        # loop through the CartItems objects and retrieve the corresponding Product objects
        for cart_item in cart_items:
            order_item = OrderItems(user_id=current_user.id, product_id=cart_item.product_id, quantity=1)
            current_user.order_items.append(order_item)
        db.session.commit()
        flash('Order placed successfully', category='success')
        return redirect(url_for('views.myaccount'))
    elif action == 'dashboard':
        return redirect(url_for('views.dashboard'))
    
    products = []
    totalprice=0
    # loop through the CartItems objects and retrieve the corresponding Product objects
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            products.append(product)
            totalprice+=product.price
            print(product.id)
    bound=min(len(cart_items),4)
    return render_template("cart-confirmation.html", user=current_user, cart_items=cart_items,products=products,bound=bound,totalprice=totalprice)
  
@views.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('views.home'))

    # Process the delete action
    if request.args.get('delete'):
        product_id = request.args.get('delete') # extract the product ID from the "delete" parameter
        cart_item = CartItems.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Product deleted from cart', category='success')
    action = request.args.get('action')
    # Process the place order action
    if action == 'My Orders':
        return redirect(url_for('views.myaccount'))
    elif action == 'dashboard':
        return redirect(url_for('views.dashboard'))
    elif action == 'Place Order':
        # TODO: Implement the checkout logic
        cart_items = CartItems.query.filter_by(user_id=current_user.id).all()
        if(cart_items==None or len(cart_items)==0):
            flash('Put something in the cart !!', category='error')
        else:
            return redirect(url_for('views.cart_conformation'))     
            
    elif action == 'Logout':
        return redirect(url_for('auth.logout'))
    cart_items = CartItems.query.filter_by(user_id=current_user.id).all()
    # create an empty list to store the Product objects
    products = []
    totalprice=0
    # loop through the CartItems objects and retrieve the corresponding Product objects
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            products.append(product)
            totalprice+= product.price
            print(product.id)
    bound=min(len(cart_items),4)
    return render_template("cart.html", user=current_user, cart_items=cart_items,products=products,bound=bound,totalprice=totalprice)









@views.route('/selleraccount', methods=['GET', 'POST'])
def selleraccount():
    if not current_user.is_authenticated:
        flash('You need to log in as a seller', category='error')
        return redirect(url_for('views.home'))
    return render_template("seller-profile-page.html", user=current_user) # render the html we made for this

@views.route('/search/<string:product_name>', methods=['GET', 'POST'])
def search(product_name):
        if product_name:
            # Perform search logic here, e.g. query the database for matching results
            # and render a page displaying the results
            results = Product.query.filter(Product.name.like("%"+product_name+"%")).all()
            return render_template('search_results.html', results=results, search_query=product_name)
        else:
            flash('Empty search !! ', category='error')
            return redirect(url_for('views.dashboard'))