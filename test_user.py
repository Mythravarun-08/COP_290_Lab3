from main import app
import pytest
# from website.models import User, db 
# from flask_login import login_user, login_required, logout_user, current_user
from website import db, create_app
from website.models import User, Seller

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


#-----------------Home-----------------
def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200


#-----------------Sign up-----------------
def test_signup_route():
    with app.test_client() as c:
        response = c.get('/sign-up')
        json_response = response.get_json()
        assert response.status_code == 200
        print(json_response)


def test_user_signup_success():
    with app.test_client() as c:
        print("hehe1")
        response = c.post('/sign-up', data={
            'email': 'sample@gmail.com',
            'first name': 'admin',
            'last name': 'admin',
            'address': 'sample address',
            'password': 'test@1234',
            'confirm password': 'test@1234'
        })
        print("hehe2")
        json_response = response.get_json()
        assert response.status_code == 200
        user = User.query.filter_by(email='sample@gmail.com').first()
        assert user is not None
        assert user.first_name == 'admin'
        assert user.last_name == 'admin'
        assert user.address == 'sample address'

def test_user_signup_password_doesnt_match():
    with app.test_client() as c:
        print("hehe1")
        response = c.post('/sign-up', data={
            'email': 'sample@gmail.com',
            'first name': 'admin',
            'last name': 'admin',
            'address': 'sample address',
            'password': 'test@1234',
            'confirm password': 'test@123'
        })
        print("hehe2")
        print(response.status_code)
        print(response.data)
        # json_response = response.get_json()
        assert response.status_code == 200
        print(response.data.decode('utf-8'))
        # user = User.query.filter_by(email='sample@gmail.com').first()
        # assert user is not None
        # assert user.first_name == 'admin'
        # assert user.last_name == 'admin'
        # assert user.address == 'sample address'
test_user_signup_password_doesnt_match()


# test_user_signup_success()

def test_seller_signup_success():
    with app.test_client() as c:
        print("hehe1")
        response = c.post('/seller-sign-up', data={
            'email': 'samplee@gmail.com',
            'first name': 'admin',
            'last name': 'admin',
            'address': 'sample address',
            'password': 'test@1234',
            'confirm password': 'test@1234',
            'aadhar': 123456789012,
            'phone number': 1234567890
        })
        print("hehe2")
        print(response.status_code)
        
        json_response = response.get_json()
        assert response.status_code == 200
        user = Seller.query.filter_by(email='samplee@gmail.com').first()
        assert user is not None
        assert user.first_name == 'admin'
        assert user.last_name == 'admin'
        assert user.address == 'sample address'
        assert user.aadhar == 123456789012
        print(user.aadhar)

# test_seller_signup_success()




# test_user_sign_up_email_exits()


def test_user_sign_up_short_password():
    with app.test_client() as c:
        print("hehe1")
        response = c.post('/sign-up', data={
            'email': 'sample@gmail.com',
            'first name': 'admin',
            'last name': 'admin',
            'address': 'sample address',
            'password': 'te',
            'confirm password': 'te'
        })
        print("hehe2")
        print(response.data)
        json_response = response.get_json()
        assert response.status_code == 200






    #assert that the response is 400

# test_user_sign_up_short_password()

#-----------------Login-----------------
def test_login_route():
    with app.test_client() as c:
        response = c.get('/login')
        assert response.status_code == 200


def test_become_seller():
    response = app.test_client().get('/seller-sign-up')
    assert response.status_code == 200

# test_become_seller()

def test_become_seller_login():
    response = app.test_client().get('/seller-login')
    assert response.status_code == 200

def test_dashboard():
    response = app.test_client().get('/dashboard')
    assert response.status_code == 302

def test_myaccount():
    response = app.test_client().get('/myaccount')
    assert response.status_code == 302

def test_seller_account():
    response = app.test_client().get('/selleraccount')
    assert response.status_code == 302

def test_cart():
    response = app.test_client().get('/cart')
    print(response.status_code)
    assert response.status_code == 302

def test_cart():
    response = app.test_client().post('/cart')
    print(response.status_code)
    assert response.status_code == 302
# test_cart()





# def test_product_page_route():
#     response = app.test_client().get('/product-page')
#     print(response.status_code)
#     assert response.status_code == 30

# test_product_page_route()



