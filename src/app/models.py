from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    registered_on = db.Column(datetime.utcnow(), db.DateTime)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return self.id

    @staticmethod
    def password_hash(password):
        return generate_password_hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)