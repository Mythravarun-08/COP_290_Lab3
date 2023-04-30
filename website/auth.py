from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Seller
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            # The current user is a seller
            flash('User already looged in', category='error')
            return redirect(url_for('user_views.dashboard'))
        else : 
            flash('Seller already looged in', category='error')
            return redirect(url_for('seller_views.selleraccount'))
    action = request.args.get('action')
    if action == 'Sign up':
        return redirect(url_for('auth.sign_up'))
    elif action =='index':
        return redirect(url_for('user_views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                session['user_type'] = 'user'
                login_user(user, remember=True)
                return redirect(url_for('user_views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
            
    return render_template("login-page.html", user=current_user)

@auth.route('/seller-login', methods=['GET', 'POST'])
def seller_login():
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            # The current user is a seller
            flash('User already looged in', category='error')
            return redirect(url_for('user_views.dashboard'))
        else : 
            flash('Seller already looged in', category='error')
            return redirect(url_for('seller_views.selleraccount'))
    action = request.args.get('action')
    if action == 'Become a Seller':
        return redirect(url_for('auth.seller_sign_up'))
    elif action =='index':
        return redirect(url_for('user_views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        seller = Seller.query.filter_by(email=email).first()
        if seller:
            if check_password_hash(seller.password, password):
                flash('Seller logged in successfully!', category='success')
                session['user_type'] = 'seller'
                login_user(seller, remember=True)
                return redirect(url_for('seller_views.selleraccount'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("seller-login-page.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        if not isinstance(current_user, User):
            # The current user is a seller
            flash('User already looged in', category='error')
            return redirect(url_for('user_views.dashboard'))
        else : 
            flash('Seller already looged in', category='error')
            return redirect(url_for('seller_views.selleraccount'))
    action = request.args.get('action')
    if action == 'Login':
        return redirect(url_for('auth.login'))
    elif action =='index':
        return redirect(url_for('user_views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        address = request.form.get('address')
        number= request.form.get('phone number')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif not number.isdigit() or len(number) != 10:
            flash('Please enter a valid phone number.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <= 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,last_name=last_name, password=generate_password_hash(
                password1, method='sha256'),address=address,phone_number=number)
            db.session.add(new_user)
            db.session.commit()
            session['user_type'] = 'user'
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('user_views.dashboard'))
    return render_template("signup-page.html", user=current_user)

@auth.route('/change-credentials', methods=['GET', 'POST'])
@login_required # requires user to be logged in to access this page
def change_credentials():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, Seller):
        # The current user is a seller
        flash('Seller cant change user credentials', category='error')
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
    
    product_name = request.args.get('product_name')
    if product_name is not None:
        if (len(product_name) == 0):
            flash('Empty search !! ', category='error')
        else:
            return redirect(url_for('user_views.search', product_name=product_name))
        
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        address = request.form.get('address')
        number= request.form.get('phone number')
        password = request.form.get('current password')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm password')
        user = User.query.filter_by(email=email).first()
        if user and user.id != current_user.id: # check if email is already taken by another user
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif not number.isdigit() or len(number) != 10:
            flash('Please enter a valid phone number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <= 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            if check_password_hash(user.password, password):
                current_user.email = email
                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.address = address
                current_user.phone_number=number
                if password1:
                    current_user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Credentials updated successfully!', category='success')
                return redirect(url_for('user_views.myaccount'))
            else:
                flash('Incorrect password, try again.', category='error')
    return render_template("user-detalis-update.html")

@auth.route('/seller-sign-up', methods=['GET', 'POST'])
def seller_sign_up():
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            # The current user is a seller
            flash('User already looged in', category='error')
            return redirect(url_for('user_views.dashboard'))
        else : 
            flash('Seller already looged in', category='error')
            return redirect(url_for('seller_views.selleraccount'))
    action = request.args.get('action')
    if action == 'Seller Login':
        return redirect(url_for('auth.seller_login'))
    elif action =='index':
        return redirect(url_for('user_views.home'))
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        number= request.form.get('phone number')
        address = request.form.get('address')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm password')
        aadhar = request.form.get('aadhar')
        seller = Seller.query.filter_by(email=email).first()
        if seller:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif not aadhar.isdigit() or len(aadhar) != 12:
            flash('Please enter a valid Aadhar number.', category='error')
        elif not number.isdigit() or len(number) != 10:
            flash('Please enter a valid phone number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <= 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_seller = Seller(email=email, first_name=first_name,last_name=last_name, 
            password=generate_password_hash(password1, method='sha256'),address=address,aadhar=aadhar,phone_number=number)
            db.session.add(new_seller)
            db.session.commit()
            session['user_type'] = 'seller'
            login_user(new_seller, remember=True)
            flash('Seller account created!', category='success')
            return redirect(url_for('seller_views.selleraccount'))
    return render_template("seller-sign-up.html", user=current_user)

@auth.route('/seller-change-credentials', methods=['GET', 'POST'])

def seller_change_credentials():
    if not current_user.is_authenticated:
        flash('You need to log in first', category='error')
        return redirect(url_for('user_views.home'))
    elif isinstance(current_user, User):
        # The current user is a seller
        flash('User cant change seller credentials', category='error')
        return redirect(url_for('user_views.dashboard'))
    action = request.args.get('action')
    if action == 'seller-account':
        return redirect(url_for('seller_views.selleraccount'))
    elif action == 'seller-orders': 
        return redirect(url_for('seller_views.seller_orders'))
    elif action == 'logout':
        return redirect(url_for('auth.logout'))
    elif request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        address = request.form.get('address')
        number= request.form.get('phone number')
        password = request.form.get('current password')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm password')
        aadhar = request.form.get('aadhar')
        seller = Seller.query.filter_by(email=email).first()
        if seller and seller.id != current_user.id: # check if email is already taken by another user
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif not number.isdigit() or len(number) != 10:
            flash('Please enter a valid phone number.', category='error')
        elif not aadhar.isdigit() or len(aadhar) != 12:
            flash('Please enter a valid Aadhar number.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <= 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            if check_password_hash(seller.password, password):
                current_user.email = email
                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.address = address
                current_user.phone_number = number
                if password1:
                    current_user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Credentials updated successfully!', category='success')
                return redirect(url_for('seller_views.selleraccount'))
            else:
                flash('Incorrect password, try again.', category='error')
    return render_template("seller-details-update.html")
