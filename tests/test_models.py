from ../website/models import User


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(150))
#     last_name = db.Column(db.String(150))
#     email = db.Column(db.String(150), unique=True)
#     address = db.Column(db.String(300))
#     password = db.Column(db.String(150))
#     cart_items = db.relationship('CartItems', backref='user')
def test_new_user():
    user = User(first_name='susan', last_name='smith', email = 'test@gmail.com',address='123 main street', password='password')
    assert user.first_name == 'susan'
    assert user.last_name == 'smith'
    assert user.email == 'test@gmail.com'
    assert user.address == '123 main street'
    assert user.password == 'password'


                