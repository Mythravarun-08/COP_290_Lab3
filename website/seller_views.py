from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import text
from .models import Product, User, Seller, OrderedItems, OrderItems
from . import db
import json

seller_views = Blueprint('seller_views', __name__)

@seller_views.route('/selleraccount', methods=['GET', 'POST'])
def selleraccount():
   if not current_user.is_authenticated:
      flash('You need to log in as a seller', category='error')
      return redirect(url_for('user_views.home'))
   elif isinstance(current_user, User):
      # The current user is a seller
      flash('User not allowed here', category='error')
      return redirect(url_for('user_views.dashboard'))
   
   action = request.args.get('action')
   if action == 'seller-account':
        return redirect(url_for('seller_views.selleraccount'))
   elif action == 'seller-orders':
      return redirect(url_for('seller_views.seller_orders'))
   elif action == 'seller-products':
      return redirect(url_for('seller_views.seller_products'))
   elif action == 'logout':
      return redirect(url_for('auth.logout'))
   elif action =='change-seller-credentials':
      return redirect(url_for('auth.seller_change_credentials')) 
   elif action =='add-product':
      return redirect(url_for('seller_views.add_product'))


   # render the html we made for this
   return render_template("seller-profile-page.html", seller=current_user)


@seller_views.route('/seller-orders', methods=['GET', 'POST'])
def seller_orders():
   if not current_user.is_authenticated:
      flash('You need to log in first', category='error')
      return redirect(url_for('user_views.home'))
   elif isinstance(current_user, User):
      # The current user is a seller
      flash("User cant view seller's orders", category='error')
      return redirect(url_for('user_views.dashboard'))
   productid = request.args.get('track')
   if productid is not None:
       return redirect(url_for('seller_views.order_tracking',product_id= productid))
   action = request.args.get('action')
   if action == 'seller-account':
        return redirect(url_for('seller_views.selleraccount'))
   elif action == 'seller-orders':
      return redirect(url_for('seller_views.seller_orders'))
   elif action == 'seller-products':
      return redirect(url_for('seller_views.seller_products'))
   elif action == 'logout':
      return redirect(url_for('auth.logout'))
   elif action =='add-product':
      return redirect(url_for('seller_views.add_product'))
   
   # TODO: Implement the checkout logic
   ordered_items = OrderedItems.query.filter_by(seller_id=current_user.id).all()
   # create an empty list to store the Product objects
   products = []
   totalprice = 0
   numorders = 0
   # loop through the CartItems objects and retrieve the corresponding Product objects
   for ordered_item in ordered_items:
      product = Product.query.get(ordered_item.product_id)
      if product:
         products.insert(0, product)
         totalprice += product.price
         numorders+=1
   return render_template("seller-orders.html", seller=current_user, ordered_items=ordered_items, products=products, totalprice=totalprice, numorders=numorders)

@seller_views.route('/seller-products', methods=['GET', 'POST'])
def seller_products():
   if not current_user.is_authenticated:
      flash('You need to log in first', category='error')
      return redirect(url_for('user_views.home'))
   elif isinstance(current_user, User):
      # The current user is a seller
      flash("User cant view seller's products", category='error')
      return redirect(url_for('user_views.dashboard'))
   
   action = request.args.get('action')
   if action == 'seller-account':
        return redirect(url_for('seller_views.selleraccount'))
   elif action == 'seller-orders':
      return redirect(url_for('seller_views.seller_orders'))
   elif action == 'logout':
      return redirect(url_for('auth.logout'))
   elif action =='add-product':
      return redirect(url_for('seller_views.add_product'))
   products = Product.query.filter_by(seller_id=current_user.id).all()
   numproducts = len(products)
   return render_template("seller-products-page.html", seller=current_user,  products=products, numproducts=numproducts)


@seller_views.route('/add-product', methods=['GET', 'POST'])
def add_product():
   if not current_user.is_authenticated:
      flash('You need to log in first', category='error')
      return redirect(url_for('user_views.home'))
   elif isinstance(current_user, User):
      # The current user is a seller
      flash("User can't add product", category='error')
      return redirect(url_for('user_views.dashboard'))

   action = request.args.get('action')
   if action == 'seller-account':
      return redirect(url_for('seller_views.selleraccount'))
   elif action == 'seller-orders':
      return redirect(url_for('seller_views.seller_orders'))
   elif action == 'logout':
      return redirect(url_for('auth.logout'))
   elif action == 'change-seller-credentials':
      return redirect(url_for('auth.seller_change_credentials'))
   elif action =='add-product':
      return redirect(url_for('seller_views.add_product'))

   if request.method == 'POST':
      name = request.form.get('name')
      description = request.form.get('description')
      photo = request.form.get('photo')
      product_type = request.form.get('type')
      price = request.form.get('price')
      quantitiy = request.form.get('quantity')
      tags = request.form.get('tags')
      

      # Perform checks on the input data
      if not name:
            flash('Please enter a name for the product.', category='error')
      elif not photo:
            flash('Please enter a URL for the product photo.', category='error')
      elif not product_type:
            flash('Please select a type for the product.', category='error')
      elif not product_type=="Laptop" and not product_type=="Television" and not product_type=="Mobile" and not product_type=="Gaming Console" and not product_type=="Tablet":
            flash('Please select a valid type for the product.', category='error')
      elif not price:
            flash('Please enter a price for the product.', category='error')
      elif not price.isdigit():
            flash('Please enter a valid price for the product.', category='error')
      elif not quantitiy:
            flash('Please enter a quantity for the product.', category='error')
      elif not quantitiy.isdigit():
            flash('Please enter a valid quantity for the product.', category='error')
      else:
            # Check if product with same name exists for this seller
            existing_product = Product.query.filter_by(name=name, seller_id=current_user.id).first()
            if existing_product:
               # If exists, update the stock of the product
               existing_product.stock += int(quantitiy)
               db.session.commit()
               flash('Product stock updated!', category='success')
            else:
               # If not exists, add the new product to the database
               new_product = Product(name=name, description=description, photo=photo,
                                        price=price,stock=quantitiy, seller_id=current_user.id, type=product_type)
               db.session.add(new_product)
               db.session.commit()
               flash('Product added!', category='success')

            return redirect(url_for('seller_views.selleraccount'))

   return render_template("add-product-page.html", seller=current_user)

@seller_views.route('/seller-order-tracking/<int:product_id>', methods=['GET', 'POST'])
def order_tracking(product_id):
   if not current_user.is_authenticated:
      flash('You need to log in first', category='error')
      return redirect(url_for('user_views.home'))
   elif isinstance(current_user, User):
      # The current user is a seller
      flash('User not allowed here', category='error')
      return redirect(url_for('user_views.dashboard'))
   product = Product.query.get_or_404(product_id)
   orderitem = OrderItems.query.filter_by(product_id=product_id).first()
   user = User.query.get(orderitem.user_id)
   action = request.args.get('action')
   if action == 'seller-account':
      return redirect(url_for('seller_views.selleraccount'))
   elif action == 'seller-orders':
      return redirect(url_for('seller_views.seller_orders'))
   elif action == 'logout':
      return redirect(url_for('auth.logout'))
   return render_template("seller-order-tracking.html", seller=current_user, product=product, user=user)

