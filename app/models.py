from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @staticmethod
    def insert_user(username, password):
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = password

    def verify_password(self, password):
        return self.password_hash == password

# callback function for flask-login extentsion
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))