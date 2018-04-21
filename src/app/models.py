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
    accounts = db.relationship('Account', backref='users', lazy=True)

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



class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80, collation='utf8_general_ci'), unique=True, nullable=False)
    description = db.Column(db.Text(collation='utf8_general_ci'))

#    category = db.relationship('Category', backref='entity', lazy=True)
#    account = db.relationship('Account', backref='entity', lazy=True)
    operations = db.relationship('Operation', backref='entity', lazy=True)

    def __repr__(self):
        return '<Entity {} - {}>'.format(self.name, self.description)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)

    parent_id = db.Column(db.Integer)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    
    entity = db.relationship('Entity', backref='category', lazy=True)
    budgets = db.relationship('Budget', backref='category', lazy=True)
    operations = db.relationship('Operation', backref='category', lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.id)


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)

    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Numeric)
    currency = db.Column(db.Numeric)

    entity = db.relationship('Entity', backref='account', lazy=True)
    operations = db.relationship('Operation', backref='account', lazy=True)

    def __repr__(self):
        return '<Account {}>'.format(self.id)


class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    limit = db.Column(db.Numeric)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Budget {}>'.format(self.id)


class Operation(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date = db.Column(db.Date)
    amount = db.Column(db.Numeric)
    currency = db.Column(db.Numeric)

    def __repr__(self):
        return '<Operation {}>'.format(self.id)
