from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Seller
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login-page.html", user=current_user)

@auth.route('/seller-login', methods=['GET', 'POST'])
def seller_login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')

        seller = Seller.query.filter_by(email=email).first()
        if seller:
            if check_password_hash(seller.password, password):
                flash('Seller logged in successfully!', category='success')
                login_user(seller, remember=True)
                return redirect(url_for('views.selleraccount'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("seller-login-page.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        first_name = request.form.get('first name')
        last_name = request.form.get('last name')
        address = request.form.get('address')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm password')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <= 7:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,last_name=last_name, password=generate_password_hash(
                password1, method='sha256'),address=address)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.dashboard'))
    return render_template("signup-page.html", user=current_user)

@auth.route('/seller-sign-up', methods=['GET', 'POST'])
def seller_sign_up():
    if request.method == 'POST':
        print(request.form)
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
            login_user(new_seller, remember=True)
            flash('Seller account created!', category='success')
            return redirect(url_for('views.selleraccount'))
    return render_template("seller-sign-up.html", user=current_user)

