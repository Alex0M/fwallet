from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'    
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), nullable=False)
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


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(80, collation='utf8_general_ci'), nullable=False)
    
    parent_category = db.relationship("Category", remote_side=[id])
    budgets = db.relationship('Budget', backref='category', lazy=True)
    operations = db.relationship('Operation', backref='category', lazy=True)

    def __repr__(self):
        return '<Category {} child of {}>'.format(self.id, self.parent_category.id if self.parent_category else None)

    def as_dict(self):
        return {'name': self.name}


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)

    accounttype_id = db.Column(db.Integer, db.ForeignKey('account_type.id'), nullable=False)
    name = db.Column(db.String(80, collation='utf8_general_ci'), unique=True, nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Numeric(precision=10, scale=3, asdecimal=False))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    
    operations = db.relationship('Operation', backref='account', lazy=True)

    def __repr__(self):
        return '<Account {}>'.format(self.id)

    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class AccountType(db.Model):
    __tablename__ = 'account_type'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80, collation='utf8_general_ci'), unique=True, nullable=False)
    
    accounts = db.relationship('Account', backref='account_type', lazy=True)

    def __repr__(self):
        return '<AccountType: {}>'.format(self.name)


class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(5, collation='utf8_general_ci'), unique=True, nullable=False)
    base = db.Column(db.Boolean, nullable=False)
    rate = db.Column(db.Numeric(precision=10, scale=3, asdecimal=False), nullable=False)

    accounts = db.relationship('Account', backref='currency', lazy=True)

    def __repr__(self):
        return '<AccountType: {}>'.format(self.name)


class Budget(db.Model):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    limit = db.Column(db.Numeric(precision=10, scale=3, asdecimal=False))
    month_stamp = db.Column(db.String(7, collation='utf8_general_ci'), nullable=False)
    operationtype_id = db.Column(db.Integer, db.ForeignKey('operation_type.id'), nullable=False)

    def __repr__(self):
        return '<Budget {}>'.format(self.id)


class Operation(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    operationtype_id = db.Column(db.Integer, db.ForeignKey('operation_type.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date = db.Column(db.Date)
    amount = db.Column(db.Numeric(precision=10, scale=3, asdecimal=False))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)

    def __repr__(self):
        return '<Operation {}>'.format(self.id)

class OperationType(db.Model):
    __tablename__ = 'operation_type'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80, collation='utf8_general_ci'), unique=True, nullable=False)
    
    operations = db.relationship('Operation', backref='operation_type', lazy=True)

    def __repr__(self):
        return '<OperationType: {}>'.format(self.name)
