from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column('password', db.String(255))
    email = db.Column(db.String(120), unique=True, nullable=False)
#   registered_on = db.Column(datetime.utcnow(), db.DateTime)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id

    def is_correct_password(self, plaintext):
        if check_password_hash(self._password, plaintext):
            return True

        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)