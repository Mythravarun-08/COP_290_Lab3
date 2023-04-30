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


def test_selleraccount():
    with app.app_context():
        with app.test_client() as c:
            # without logging in
            response = c.get('/selleraccount')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # logging in as a seller
            response = c.post(url_for('auth.seller_login'), data={'email': 'sellertest@test.com', 'password': 'password'})
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.selleraccount',action = 'seller-account'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.selleraccount',action = 'seller-orders'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_orders')

            response = c.get(url_for('seller_views.selleraccount',action = 'seller-products'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_products')

            response = c.get(url_for('seller_views.selleraccount',action = 'change-seller-credentials'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_change_credentials')

            response = c.get(url_for('seller_views.selleraccount',action = 'add-product'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.add_product')

            response = c.get(url_for('seller_views.selleraccount',action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_seller_orders():
    with app.app_context():
        with app.test_client() as c:
            # without logging in
            response = c.get('/seller-orders')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # logging in as a seller
            response = c.post(url_for('auth.seller_login'), data={'email': 'sellertest@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('seller_views.seller_orders'))
            assert response.status_code == 200

            response = c.get(url_for('seller_views.seller_orders', track = 1))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.order_tracking', product_id = 1)

            response = c.get(url_for('seller_views.seller_orders', action = 'seller-account'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.seller_orders', action = 'seller-products'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_products')

            response = c.get(url_for('seller_views.seller_orders', action = 'seller-orders'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_orders')

            response = c.get(url_for('seller_views.seller_orders', action = 'add-product'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.add_product')

            response = c.get(url_for('seller_views.seller_orders', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_seller_products():
    with app.app_context():
        with app.test_client() as c:
            # without logging in
            response = c.get('/seller-products')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # logging in as a seller
            response = c.post(url_for('auth.seller_login'), data={'email': 'sellertest@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('seller_views.seller_products'))
            assert response.status_code == 200

            response = c.get(url_for('seller_views.seller_products', action = 'seller-account'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.seller_products', action = 'seller-orders'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_orders')

            response = c.get(url_for('seller_views.seller_products', action = 'add-product'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.add_product')

            response = c.get(url_for('seller_views.seller_products', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_order_tracking():
    with app.app_context():
        with app.test_client() as c:
            # without logging in
            response = c.get('/order-tracking/1')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # logging in as a seller
            response = c.post(url_for('auth.seller_login'), data={'email': 'sellertest@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('seller_views.order_tracking', product_id = 1))
            assert response.status_code == 200

            response = c.get(url_for('seller_views.order_tracking', product_id = 1, action = 'seller-account'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.order_tracking', product_id = 1, action = 'seller-orders'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_orders')

            response = c.get(url_for('seller_views.order_tracking', product_id = 1, action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

def test_add_product():
    with app.app_context():
        with app.test_client() as c:
            # without logging in
            response = c.get('/add-product')
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # logging in as a seller
            response = c.post(url_for('auth.seller_login'), data={'email': 'sellertest@test.com', 'password': 'password'})
            assert response.status_code == 302

            response = c.get(url_for('seller_views.add_product'))
            assert response.status_code == 200

            response = c.get(url_for('seller_views.add_product', action = 'seller-account'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.add_product', action = 'seller-orders'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.seller_orders')

            response = c.get(url_for('seller_views.add_product', action = 'change-seller-credentials'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_change_credentials')

            response = c.get(url_for('seller_views.add_product', action = 'add-product'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.add_product')

            response = c.post(url_for('seller_views.add_product'), data={'name': 'test', 'description': 'test', 'price': 1, 'quantity': 1, 'type': 'Laptop', 'photo': 'test','tags': 'test'})
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

            response = c.get(url_for('seller_views.add_product', action = 'logout'))
            assert response.status_code == 302
            


