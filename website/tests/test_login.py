import pytest
from website import create_app
from flask_login import current_user
from website.models import User
from website.auth import auth


def test_sign_up_new_user(db):
    with auth:
        response = auth.post('/sign-up', data={
            'email': 'testuser@example.com',
            'first name': 'Test',
            'last name': 'User',
            'address': '123 Main St',
            'password': 'password123',
            'confirm password': 'password123',
            'phone number': '1234567890'
        })

        assert response.status_code == 302
        assert current_user.is_authenticated
        assert User.query.filter_by(email='testuser@example.com').first() is not None


def test_sign_up_existing_user(db, user):
    with auth:
        response = auth.post('/sign-up', data={
            'email': user.email,
            'first name': 'Test',
            'last name': 'User',
            'address': '123 Main St',
            'password': 'password123',
            'confirm password': 'password123'
        })

        assert response.status_code == 200
        assert b'Email already exists.' in response.data
        assert User.query.filter_by(email=user.email).first() == user


def test_sign_up_short_email(db):
    with auth:
        response = auth.post('/sign-up', data={
            'email': 'a',
            'first name': 'Test',
            'last name': 'User',
            'address': '123 Main St',
            'password': 'password123',
            'confirm password': 'password123'
        })

        assert response.status_code == 200
        print(response.data)
        assert User.query.filter_by(email='a').first() is None


def test_login_valid_user(app, db, user):
    response = auth.post('/login', data={
        'email': user.email,
        'password': 'password123'
    })

    assert response.status_code == 302
    assert current_user.is_authenticated


def test_login_invalid_email(app, db, user):
    response = auth.post('/login', data={
        'email': 'invalid@example.com',
        'password': 'password123'
    })

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
    assert not current_user.is_authenticated


def test_login_invalid_password(app, db, user):
    response = auth.post('/login', data={
        'email': user.email,
        'password': 'invalid'
    })

    assert response.status_code == 200
    assert b'Invalid email or password' in response.data
    assert not current_user.is_authenticated