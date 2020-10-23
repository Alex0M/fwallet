from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from apps.dbmodels import Transaction, TransactionType, Account, AccountType, User, Category

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()



class AccountTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = AccountType
    
    name = ma.auto_field()



class AccountSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Account
    
    id = ma.auto_field()
    name = ma.auto_field()
    balance = ma.auto_field()
#    account_type = fields.Nested(AccountTypeSchema)
#    users = fields.Nested(UserSchema)

class CategoryShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
    
    parent_category = fields.Nested(lambda: CategoryShema(exclude=("parent_category",)))


class TransactionTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = TransactionType

    name = ma.auto_field()


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction

    transaction_type = fields.Nested(TransactionTypeSchema)
    account = fields.Nested("AccountSchema", only=("id", "name", "account_type", "users"))
    category = fields.Nested(CategoryShema)



transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)