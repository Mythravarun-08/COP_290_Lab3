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


def test_login():

    with app.app_context():

        with app.test_client() as c:
            response = c.get('/login')
            assert response.status_code == 200

            # for GET request
            response = c.get(url_for('auth.login', action = 'Sign up'))
            assert response.status_code == 302
            assert response.location == url_for('auth.sign_up')

            response = c.get(url_for('auth.login', action = 'index'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # for POST request
            # login with test user
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password' : 'password'} )
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            assert current_user.is_authenticated == True

            # login with incorect password
            response = c.post(url_for('auth.login'), data = {'email': 'test@test.com', 'password' : 'password1'} )
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            # login with incorrect email
            response = c.post(url_for('auth.login'), data = {'email': 'testis@test.com', 'password' : 'password'} )
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            # check flash message

            response = c.get(url_for('auth.login'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('user_views.dashboard', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

            response = c.post(url_for('auth.seller_login'), data = {'email': 'sellertest@test.com', 'password' : 'password'} )
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            assert current_user.is_authenticated == True

            response = c.get(url_for('auth.login'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            assert current_user.is_authenticated == True


def test_seller_login():
    with app.app_context():
        with app.test_client() as c:
            response = c.get('/seller-login')
            assert response.status_code == 200

            # for GET request
            response = c.get(url_for('auth.seller_login', action = 'Become a Seller'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_sign_up')

            response = c.get(url_for('auth.seller_login', action = 'index'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # for POST request
            # login with test user
            response = c.post(url_for('auth.seller_login'), data = {'email': 'sellertest@test.com', 'password' : 'password'} )
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')
            assert current_user.is_authenticated == True

            response = c.get(url_for('seller_views.selleraccount', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

            # login with incorect password
            response = c.post(url_for('auth.seller_login'), data = {'email': 'sellertest@test.com', 'password' : 'password1'} )
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')
            # assert current_user.is_authenticated == 

            # login with incorrect email
            response = c.post(url_for('auth.seller_login'), data = {'email': 'sellertest1@test.com', 'password' : 'password'} )
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')
            # assert current_user.is_authenticated == False

            response = c.get(url_for('auth.seller_login'))
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')

def test_logout():
    with app.test_client() as c:
        response = c.get('/logout')
        assert response.status_code == 302
        # assert response.location == url_for('user_views.home')
        assert current_user.is_authenticated == False

def test_sign_up():
    with app.app_context():
        with app.test_client() as c:
            response = c.get('/sign-up')
            assert response.status_code == 200

            # for GET request
            response = c.get(url_for('auth.sign_up', action = 'Login'))
            assert response.status_code == 302
            assert response.location == url_for('auth.login')

            response = c.get(url_for('auth.sign_up', action = 'index'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            # for POST request
            # sign up with test user
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'sellertest@test.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(email) < 4
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'tes',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(first_name) < 2
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test@sample.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 't',
                'last name' : 'test',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(email) < 4
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 't@',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(last_name) < 2  
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test@sample.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 't',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(phone_number) < 10
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test@sample.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '12345678',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            # sign up with len(password) < 7
            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test@sample.com',
                'password' : 'pass',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '123456',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test@sample.com',
                'password' : 'password1',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : '1234567890',
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('auth.login')
            assert current_user.is_authenticated == False

            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'test3@sample.com',
                'password' : 'passw',
                'confirm password' : 'passw',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : 1234567890,
                'address' : 'test',
            })
            assert response.status_code == 200
            # assert response.location == url_for('user_views.dashboard')
            # assert current_user.is_authenticated == True

            response = c.post(url_for('auth.sign_up'), data = {
                'email': 'tester3@sample.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : 1234567890,
                'address' : 'test',
            })
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            assert current_user.is_authenticated == True

            print(current_user.id)
            user_to_remove = User.query.get(current_user.id)
            db.session.delete(user_to_remove)
            db.session.commit()


            # login and check
            response = c.post(url_for('auth.login'), data = {
                'email': 'test@test.com',
                'password' : 'password',
            })
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')
            assert current_user.is_authenticated == True

            response = c.get(url_for('auth.sign_up'))
            assert response.status_code == 302
            # assert response.location == url_for('user_views.dashboard')

            # logout and check
            response = c.get(url_for('auth.logout'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')
            assert current_user.is_authenticated == False

            # login as seller 
            response = c.post(url_for('auth.seller_login'), data = { 'email' : 'sellertest@testcom', 'password' : 'password'})
            assert response.status_code == 200

            response = c.get(url_for('auth.sign_up'))
            assert response.status_code == 200
            # assert response.location == url_for('seller_views.selleraccount')
            

def test_change_credentials():
    with app.app_context():
        
        with app.test_client() as c:
            
            # check without logging in 
            response = c.get('/change-credentials')
            assert response.status_code == 302
            # assert response.location == '/'

            # login as user
            response = c.post(url_for('auth.login'), data = { 'email' : 'test@test.com', 'password' : 'password'})
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            # check actions
            response = c.get(url_for('auth.change_credentials', action = 'dashboard'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.dashboard')

            response = c.get(url_for('auth.change_credentials', action = 'myaccount'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')

            response = c.get(url_for('auth.change_credentials', action = 'cart'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.cart')

            response = c.get(url_for('auth.change_credentials', action = 'logout'))
            assert response.status_code == 302
            assert response.location == url_for('auth.logout')

            response = c.get(url_for('auth.change_credentials', data ={ 'product_name' : ''}))
            assert response.status_code == 200

            # response = c.get(url_for('auth.change_credentials', data ={ 'product_name' : 'test'}))
            # assert response.status_code == 302
            # assert response.location == url_for('user_views.search', product_name = 'test')

            # now check for post
            

            # check with other user
            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'tes',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : '1234567890',
                'current password' : 'password',
                'new password' : 'newpassword',
                'confirm password' : 'newpassword',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'testis@tes.com1',
                'first name' : 't',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : '1234567890',
                'current password' : 'password',
                'new password' : 'newpassword',
                'confirm password' : 'newpassword',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'testis@tes.com1',
                'first name' : 'test',
                'last name' : 't',
                'address' : 'test',
                'phone number' : '1234567890',
                'current password' : 'password',
                'new password' : 'newpassword',
                'confirm password' : 'newpassword',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'testis@test.com1',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : 1234567,
                'current password' : 'password',
                'new password' : 'newpassword',
                'confirm password' : 'newpassword',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'testis@test.com1',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : 1234567890,
                'current password' : 'password',
                'new password' : 'newpassword',
                'confirm password' : 'newpassword1',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'testis@test.com',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : 1234567890,
                'current password' : 'password1',
                'password' : 'newp',
                'confirm password' : 'newp',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'test@test.com',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : 1234567890,
                'current password' : 'passwor',
                'password' : 'newpassword',
                'confirm password' : 'newpassword',
            })
            assert response.status_code == 200

            response = c.post(url_for('auth.change_credentials'), data = {
                'email': 'test@test.com',
                'first name' : 'test',
                'last name' : 'test',
                'address' : 'test',
                'phone number' : 1234567890,
                'current password' : 'password',
                'password' : 'password',
                'confirm password' : 'password',
            })
            assert response.status_code == 302
            assert response.location == url_for('user_views.myaccount')


def test_seller_sign_up():
    with app.app_context():
        
        with app.test_client() as c:
            
            # check without logging in 
            response = c.get('/seller-sign-up')
            assert response.status_code == 200

            response = c.get(url_for('auth.seller_sign_up', action = 'Seller Login'))
            assert response.status_code == 302
            assert response.location == url_for('auth.seller_login')

            response = c.get(url_for('auth.seller_sign_up', action = 'index'))
            assert response.status_code == 302
            assert response.location == url_for('user_views.home')

            response = c.post(url_for('auth.seller_sign_up'), data = {
                'email': 'tester4@sample.com',
                'password' : 'password',
                'confirm password' : 'password',
                'first name' : 'test',
                'last name' : 'test',
                'phone number' : 1234567890,
                'address' : 'test',
                'aadhar' : '123456789012'
            })
            assert response.status_code == 302
            assert response.location == url_for('seller_views.selleraccount')
            assert current_user.is_authenticated == True

            print(current_user.id)
            user_to_remove = Seller.query.get(current_user.id)
            db.session.delete(user_to_remove)
            db.session.commit()







