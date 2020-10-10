from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from apps.dbmodels import Operation, OperationType, Account, AccountType, User

ma = Marshmallow()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

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



class OperationTypeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = OperationType

    name = ma.auto_field()


class OperationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Operation

    operation_type = fields.Nested(OperationTypeSchema)
    account = fields.Nested("AccountSchema", only=("name", "account_type", "users"))



operation_schema = OperationSchema()
operations_schema = OperationSchema(many=True)

accounts_schema = AccountSchema(many=True)