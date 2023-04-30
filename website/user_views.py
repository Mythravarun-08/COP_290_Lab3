from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from functools import wraps
from sqlalchemy import text
from .models import Product, CartItems, OrderItems, User, Seller, OrderedItems, SearchHistory
# from .ml import recommendations
from . import db
import json

user_views = Blueprint('user_views', __name__)

# TODO : 
# 1. Enusre nav bar works at every page : done 
# 2. Add-product feature for the seller : done
# 3. Implement Change-Credential logic : done
# 4. Implement ML API
# 5. Create distinction between user and seller instance : done
# 6. Create separate user_views.py and seller_views.py for code cleanliness : done 
# 7. While adding to the cart create a vector of pairs(product, quantity)
# 8. Implement filter in the search  : done





@user_views.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        if isinstance(current_user, Seller):
            return redirect(url_for('seller_views.selleraccount'))
        else:
            return redirect(url_for('user_views.dashboard'))
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
        # render the html we made for this
        return render_template("index.html")


@user_views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant go to dashboard', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    view_product_id = request.args.get('view_product_id')
    if view_product_id is not None:
        return redirect(url_for('user_views.product_page', product_id=view_product_id))

    cart_product_id = request.args.get('cart_product_id')
    if cart_product_id is not None:
        cart_item = CartItems(user_id=current_user.id,
                              product_id=cart_product_id, quantity=1)
        current_user.cart_items.append(cart_item)
        db.session.commit()
        flash('Item added to the cart', category='success')

    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))

    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    else:
        products = Product.query.all()
        # recommened_products = recommended(current_user.id)
        # Pass the fetched products to the template
        return render_template("dashboard.html", user=current_user, products=products)


@user_views.route('/conformation/<int:product_id>', methods=['GET', 'POST'])
def conformation(product_id):
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant go to conformation page', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    product = Product.query.get_or_404(product_id)
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    elif action == 'confirm-buy':
        order_item = OrderItems(user_id=current_user.id,product_id=product.id, quantity=1)
        current_user.order_items.append(order_item)
        seller = Seller.query.get(product.seller_id)
        ordered_item = OrderedItems(seller_id= seller.id,product_id= product.id,quantity=1)
        seller.ordered_items.append(ordered_item)
        db.session.commit()
        return redirect(url_for('user_views.orders'))
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
    return render_template("conformation-page.html", user=current_user, product=product)


@user_views.route('/orders', methods=['GET', 'POST'])
def orders():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant order', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    view_product_id = request.args.get('view_product_id')
    if view_product_id is not None:
        return redirect(url_for('user_views.product_page', product_id=view_product_id))
    
    track_product_id = request.args.get('track')
    if track_product_id is not None:
        return redirect(url_for('user_views.order_tracking', product_id=track_product_id))

    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
    
    action = request.args.get('action')
    # Process the place order action
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'My Orders':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'Place Order':
        # TODO: Implement the checkout logic
        order_items = OrderItems.query.filter_by(user_id=current_user.id).all()
        if (order_items == None or len(order_items) == 0):
            flash('Order something first !!', category='error')
        else:
            return redirect(url_for('user_views.cart_conformation'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    order_items = OrderItems.query.filter_by(user_id=current_user.id).all()
    # create an empty list to store the Product objects
    products = []
    totalprice = 0
    numorders=0
    # loop through the CartItems objects and retrieve the corresponding Product objects
    for order_item in order_items:
        product = Product.query.get(order_item.product_id)
        if product:
            products.insert(0, product)
            totalprice += product.price
            numorders+=1
    return render_template("orders.html", user=current_user, products=products, totalprice=totalprice,numorders=numorders)


@user_views.route('/order-tracking/<int:product_id>', methods=['GET', 'POST'])
def order_tracking(product_id):
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller dont need to track order', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
    product = Product.query.get_or_404(product_id)
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    return render_template("order-tracking.html", user=current_user, product=product)


@user_views.route('/product-page/<int:product_id>', methods=['GET', 'POST'])
def product_page(product_id):
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller dont need to see this', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
    product = Product.query.get_or_404(product_id)
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'buy-now':
        return redirect(url_for('user_views.conformation', product_id=product_id))
    elif action == 'add-to-cart':
        cart_item = CartItems(user_id=current_user.id, product_id=product.id, quantity=1)
        current_user.cart_items.append(cart_item)
        db.session.commit()
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    # top_products = recommendations(current_user.id)
    return render_template("product-page.html", user=current_user, product=product)


@user_views.route('/myaccount', methods=['GET', 'POST'])
def myaccount():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller not allowed at user account', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    elif action == 'orders':
        return redirect(url_for('user_views.orders'))
    elif action == 'change-credentials':
        return redirect(url_for('auth.change_credentials'))
    elif action == 'upload-photo':
        k =0

    
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
        
    order_items = OrderItems.query.filter_by(user_id=current_user.id).all()
    # create an empty list to store the Product objects
    products = []

    # loop through the OrderItems objects and retrieve the corresponding Product objects
    for order_item in order_items:
        product = Product.query.get(order_item.product_id)
        if product:
            products.insert(0, product)

    

    # return render_template("cart.html", user=current_user, order_items=order_items,products=products,bound=bound)
    # render the html we made for this
    return render_template("profile-page.html", user=current_user)


@user_views.route('/cart-conformation', methods=['GET', 'POST'])
def cart_conformation():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant confirm orders', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))

    cart_items = CartItems.query.filter_by(user_id=current_user.id).all()
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'confirm-buy':
        # loop through the CartItems objects and retrieve the corresponding Product objects
        for cart_item in cart_items:
            order_item = OrderItems(user_id=current_user.id, product_id=cart_item.product_id, quantity=1)
            current_user.order_items.append(order_item)
            product = Product.query.get(cart_item.product_id)
            seller = Seller.query.get(product.seller_id)
            ordered_item = OrderedItems(seller_id= seller.id,product_id= product.id,quantity=1)
            seller.ordered_items.append(ordered_item)
            db.session.delete(cart_item)
        db.session.commit()
        flash('Order placed successfully', category='success')
        return redirect(url_for('user_views.myaccount'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))

    products = []
    totalprice = 0
    # loop through the CartItems objects and retrieve the corresponding Product objects
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            products.insert(0, product)
            totalprice += product.price

    return render_template("cart-confirmation.html", user=current_user, cart_items=cart_items, products=products,totalprice=totalprice)



@user_views.route('/cart', methods=['GET', 'POST'])
def cart():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant view a cart', category='error')
        return redirect(url_for('seller_views.selleraccount'))
    # Process the delete action
    if request.args.get('delete'):
        # extract the product ID from the "delete" parameter
        product_id = request.args.get('delete')
        cart_item = CartItems.query.filter_by(
            user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Product deleted from cart', category='success')
    # Process the place order action
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
    # Process the view order action
    view_product_id = request.args.get('view_product_id')
    if view_product_id is not None:
        return redirect(url_for('user_views.product_page', product_id=view_product_id))
    # Process other actions
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'My Orders':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'Place Order':
        # TODO: Implement the checkout logic
        cart_items = CartItems.query.filter_by(user_id=current_user.id).all()
        if (cart_items == None or len(cart_items) == 0):
            flash('Put something in the cart !!', category='error')
        else:
            return redirect(url_for('user_views.cart_conformation'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    cart_items = CartItems.query.filter_by(user_id=current_user.id).all()
    # create an empty list to store the Product objects
    products = []
    totalprice = 0
    # loop through the CartItems objects and retrieve the corresponding Product objects
    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        if product:
            products.insert(0, product)
            totalprice += product.price
    numb = len(products)
    return render_template("cart.html", user=current_user, cart_items=cart_items, products=products, totalprice=totalprice, numb = numb)


@user_views.route('/search/<string:product_name>', methods=['GET', 'POST'])
def search(product_name):
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    
    # Implementing view button
    view_product_id = request.args.get('view_product_id')
    if view_product_id is not None:
        return redirect(url_for('user_views.product_page', product_id=view_product_id))
    
    # Implementing Add to cart button
    cart_product_id = request.args.get('cart_product_id')
    if cart_product_id is not None:
        cart_item = CartItems(user_id=current_user.id,
                              product_id=cart_product_id, quantity=1)
        current_user.cart_items.append(cart_item)
        db.session.commit()
        flash('Item added to the cart', category='success')

    # If we get another search from the search page 
    new_search = request.args.get('product_name')
    if new_search is not None:
        if (len(new_search) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=new_search))
    
    #Handling nav-bar actions
    action = request.args.get('action')
    if action == 'dashboard':
        return redirect(url_for('user_views.dashboard'))
    elif action == 'myaccount':
        return redirect(url_for('user_views.myaccount'))
    elif action == 'cart':
        return redirect(url_for('user_views.cart'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    
    # Showing the results
    if product_name:
        # Perform search logic here, e.g. query the database for matching results
        # and render a page displaying the results
        results = Product.query.filter(
            Product.name.like("%"+product_name+"%")).all()
        
        min='min'
        max='max'
        # Implementing filters
        product_type = request.form.get('type')
        if product_type is not None and product_type != 'Open this select menu':
            filtered_results = []
            for result in results:
                if result.type == product_type:
                    filtered_results.append(result)
            results = filtered_results
        min_price = request.form.get('min')
        if min_price is not None and min_price != '':
            filtered_results = []
            for result in results:
                if result.price >= int(min_price):
                    filtered_results.append(result)
            results = filtered_results
            min=min_price
        max_price = request.form.get('max')
        if max_price is not None and max_price != '':
            filtered_results = []
            for result in results:
                if result.price <= int(max_price):
                    filtered_results.append(result)
            results = filtered_results
            max=max_price


        search_query = ""  # the search query
        end = len(results)
        if end > 10:
            end = 10
        for i in range(end):
            search_query+=str(results[i].id)+","
        if search_query !="":
            search_query = search_query[:-1]  # remove the last comma
            search_history_entry = SearchHistory(user_id=current_user.id, searches=search_query)
            db.session.add(search_history_entry)
            db.session.commit()

        search_history_entries = current_user.search_history
        for entry in search_history_entries:
            print("Query: ",entry.searches)
        return render_template('search-result-page.html', products=results, search_query=product_name, min=min,max=max)
    else:
        flash('Empty search !! ', category='error')
        return redirect(url_for('user_views.dashboard'))
    

    
    if request.method == 'POST' and product_name:
        if not min:
            flash('Please enter min price for the product.', category='error')
        elif not min.isdigit():
            flash('Please enter a valid min price for the product.', category='error')
            results = Product.query.filter(Product.name.like("%"+product_name+"%")).all()
            return render_template('search-result-page.html', products=results, search_query=product_name, bound=len(results))  
        elif not max:
            flash('Please enter max price for the product.', category='error')
        elif not max.isdigit():
            flash('Please enter a valid max price for the product.', category='error')
            results = Product.query.filter(Product.name.like("%"+product_name+"%")).all()
            return render_template('search-result-page.html', products=results, search_query=product_name, bound=len(results))  
        else:
            products = Product.query.filter(Product.name.like("%"+product_name+"%")).all()
            results = []
            for product in products:
                if product.price >= int(min) and product.price <= int(max):
                    results.append(product)
            return render_template('search-result-page.html', products=results, search_query=product_name, bound=len(results))  
        

    

      
