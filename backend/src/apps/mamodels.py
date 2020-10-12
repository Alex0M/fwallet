from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from apps.dbmodels import Operation, OperationType, Account, AccountType, User, Category

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()



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
    account_type = fields.Nested(AccountTypeSchema)
    users = fields.Nested(UserSchema)

class CategoryShema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
    
    parent_category = fields.Nested(lambda: CategoryShema(exclude=("parent_category",)))


class OperationTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OperationType

    name = ma.auto_field()


class OperationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Operation

    operation_type = fields.Nested(OperationTypeSchema)
    account = fields.Nested("AccountSchema", only=("id", "name", "account_type", "users"))
    category = fields.Nested(CategoryShema)



operation_schema = OperationSchema()
operations_schema = OperationSchema(many=True)

accounts_schema = AccountSchema(many=True)