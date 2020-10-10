from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Operation(db.Model):
    __tablename__ = 'operation'
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    operationtype_id = db.Column(db.Integer, db.ForeignKey('operation_type.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date = db.Column(db.Date)
    amount = db.Column(db.Numeric(10, 3))
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)

    def __repr__(self):
        return '<Operation {}>'.format(self.id)