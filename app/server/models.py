# project/server/models.py


import datetime
from flask import current_app
from app.server import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean(), default=False)
    registered_on = db.Column(db.DateTime())


    def __init__(self,username = None, email=None, password=None, admin=False):
        self.username = username
        self.email = email
        self.admin = admin
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode('utf-8')
        self.registered_on = datetime.datetime.now()


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username

class Safe(db.Model):

    __tablename__ = 'safe'

    pass_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    entered_on = db.Column(db.DateTime())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('safe'))

    def __init__(self, name = None, password=None):
        self.username = username
        self.password = password
        self.registered_on = datetime.datetime.now()
