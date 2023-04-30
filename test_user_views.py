from main import app
import pytest
# from website.models import User, db 
# from flask_login import login_user, login_required, logout_user, current_user
from website import db, create_app, user_views, auth, seller_views
from flask_login import current_user
from website.models import User, Seller, Product, CartItems, OrderItems
from flask import url_for
from flask_login import current_user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

# test user email = test@test.com password = password
# test seller email = sellertest@test.com password = password

def test_home():
    with app.app_context():
        with app.test_client() as c:
            response = c.get('/')
            assert response.status_code == 200

            response = c.get(url_for('user_views.home', action = 'Login'))
            assert response.status_code == 302
            assert response.location == url_for('auth.login')

            response = c.get(url_for('user_views.home', action = 'Sign up'))
            assert response.status_code == 302
            assert response.location == url_for('auth.sign_up')

            response = c.get(url_for('user_views.home', action = 'Seller Login'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_login')

            response = c.get(url_for('user_views.home', action = 'Become a Seller'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_sign_up')

            response = c.get(url_for('user_views.home', action = 'Log'))
            assert response.status_code == 200

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            print(current_user)

            response = c.get('/')
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

def test_dashboard():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/dashboard')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.post(url_for('user_views.dashboard', view_product_id =1))
            assert response.status_code == 302
            assert response.location == url_for('user_views.product_page', product_id = 1)

            # for cart_id
            response = c.post(url_for('user_views.dashboard', cart_product_id= 1))
            assert response.status_code == 200
            # assert response.location == url_for('user_views.product_page', product_id = 1)

            response = c.post(url_for('user_views.dashboard', product_name= ''))
            assert response.status_code == 200
            # assert response.location == url_for('user_views.product_page')

            response = c.post(url_for('user_views.dashboard', product_name= 'test'))
            assert response.status_code == 302
            # assert response.location == url_for('user_views.search', product_name = 'test')

            response = c.get(url_for('user_views.dashboard', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.dashboard', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.dashboard', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.dashboard', action = 'log'))
            assert response.status_code == 200

def test_conformation():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/conformation/1')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.conformation', product_id = 1, action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.conformation', product_id = 1, action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.conformation', product_id = 1, action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.conformation', product_id = 1, action = 'confirm-buy'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.orders')

            response = c.get(url_for('user_views.conformation', product_id = 1, product_name = 'test'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.search', product_name = 'test')
            
            response = c.get(url_for('user_views.conformation', product_id = 1))
            assert response.status_code == 200

            response = c.get(url_for('user_views.conformation', product_id = 1, action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_orders():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/orders')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.orders', view_product_id = 1))
            assert response.status_code == 302
            assert response.location == url_for('user_views.product_page', product_id = 1)

            response = c.get(url_for('user_views.orders', track = 1))
            assert response.status_code == 302
            assert response.location == url_for('user_views.order_tracking', product_id = 1)

            response = c.get(url_for('user_views.orders', product_name = 'test'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.search', product_name = 'test')

            response = c.get(url_for('user_views.orders', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.orders', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.orders', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.orders', action = 'My Orders'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.orders', action = 'Place Order'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart_conformation')

            response = c.get(url_for('user_views.orders'))
            assert response.status_code == 200

            response = c.get(url_for('user_views.orders', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_order_tracking():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/order-tracking/1')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.order_tracking', product_id = 1, product_name = 'test'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.search', product_name = 'test')

            response = c.get(url_for('user_views.order_tracking', product_id = 1, action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.order_tracking', product_id = 1, action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')
            
            response = c.get(url_for('user_views.order_tracking', product_id = 1, action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.order_tracking', product_id = 1))
            assert response.status_code == 200

            response = c.get(url_for('user_views.order_tracking', product_id = 1, action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_product_page():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/product-page/1')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.product_page', product_id = 1, product_name = 'test'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.search', product_name = 'test')

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'buy-now'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.conformation', product_id = 1)

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'add-to-cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.product_page', product_id = 1))
            assert response.status_code == 200

            response = c.get(url_for('user_views.product_page', product_id = 1, action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_myaccount():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/myaccount')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.myaccount', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.myaccount', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.myaccount', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.myaccount', action = 'orders'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.orders')

            response = c.get(url_for('user_views.myaccount', action = 'change-credentials'))
            assert response.status_code == 302
            assert response.location == url_for('auth.change_credentials')

            response = c.get(url_for('user_views.myaccount', action = 'upload-photo'))
            assert response.status_code == 200

            response = c.get(url_for('user_views.myaccount', product_name = 'test'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.search', product_name = 'test')

            response = c.get(url_for('user_views.myaccount'))
            assert response.status_code == 200

            response = c.get(url_for('user_views.myaccount', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_search_product_name():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/search/test')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.search', product_name = 'test', view_product_id = 1))
            assert response.status_code == 302
            assert response.location == url_for('user_views.product_page', product_id = 1)

            response = c.get(url_for('user_views.search', product_name = 'test', cart_product_id = 1))
            assert response.status_code == 200

            response = c.get(url_for('user_views.search', product_name = 'test', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.search', product_name = 'test', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.search', product_name = 'test', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.search', product_name = 'test'))
            assert response.status_code == 200

            response = c.post(url_for('user_views.search', product_name = 'test'))
            assert response.status_code == 200

            response = c.get(url_for('user_views.search', product_name = 'test', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_cart():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/cart')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.cart', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.cart', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.cart', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('user_views.cart', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_cart_coformation():
    with app.app_context():
        with app.test_client() as c:
            # check without logging in
            response = c.get('/cart-conformation')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # log in as user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('user_views.cart_conformation', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.cart_conformation', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.cart_conformation', action = 'cart'))
            assert response.status_code == 302

            response = c.get(url_for('user_views.cart_conformation', action = 'confirm-buy'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('user_views.cart_conformation'))
            assert response.status_code == 200

            response = c.get(url_for('user_views.cart_conformation', action = 'logout'))
            assert response.status_code == 302
