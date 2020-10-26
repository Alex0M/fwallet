from flask import Flask, request
from apps.dbmodels import db, Transaction, TransactionType, Account, AccountType, Currency, User
from apps.mamodels import ma, transaction_schema, transactions_schema, account_schema, accounts_schema, users_schema, user_schema, accounttypes_schema, accounttype_schema
from flask_restful import Api, Resource
import os


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.environ['MYSQL_USER']+':'+os.environ['MYSQL_PASSWORD']+'@'+os.environ['MYSQL_HOST']+':'+os.environ['MYSQL_PORT']+'/'+os.environ['MYSQL_DATABASE']+'?charset=utf8'
db.init_app(app)
ma.init_app(app)
api = Api(app)


class TransactionListResource(Resource):
    def get(self):
        transaction = Transaction.query.all()
        return transactions_schema.dump(transaction)

    def post(self):
        pass



class TransactionResource(Resource):
    def get(self, transaction_id):
        transaction = Transaction.query.get_or_404(transaction_id)
        return transaction_schema.dump(transaction)


class AccountListResource(Resource):
    def get(self, user_id=None):
        if user_id is not None:
            account =  Account.query.filter_by(users_id=user_id).all()
        else:
            account =  Account.query.all()
        return accounts_schema.dump(account)

    def post(self):
        new_account = Account(
            name = request.json['name'],
            balance = request.json['balance'],
            currency_id = request.json['currency_id'],
            accounttype_id = request.json['accounttype_id'],
            users_id = request.json['users_id']
        )

        db.session.add(new_account)
        db.session.commit()
        return account_schema.dump(new_account)


class AccountResource(Resource):
    def get(self, account_id):
        account =  Account.query.get_or_404(account_id)
        return account_schema.dump(account)

    def patch (self, account_id):
        account =  Account.query.get_or_404(account_id)

        if 'name' in request.json:
            account.name = request.json['name']
        if 'balance' in request.json:
            account.balance = request.json['balance']
        if 'users_id' in request.json:
            account.users_id = request.json['users_id']
        if 'currency_id' in request.json:
            account.currency_id = request.json['currency_id']
        if 'accounttype_id' in request.json:
            account.accounttype_id = request.json['accounttype_id']

        db.session.commit()
        return account_schema.dump(account)

    def delete(self, account_id):
        account =  Account.query.get_or_404(account_id)
        db.session.delete(account)
        db.session.commit()
        return '', 204


class UserListResource(Resource):
    def get(self):
        user = User.query.all()
        return users_schema.dump(user)

    def post(self):
        new_user = User(
            username = request.json['username'],
            email = request.json['email'],
            password = request.json['password']
        )

        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        if 'username' in request.json:
            user.username = request.json['username']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.password = request.json['password']

        db.session.commit()
        return user_schema.dump(user)



class AccountTypeListResource(Resource):
    def get(self):
        account_type = AccountType.query.all()
        return accounttypes_schema.dump(account_type)


class AccountTypeResource(Resource):
    def get(self, account_type_id):
        account_type = AccountType.query.get_or_404(account_type_id)
        return accounttype_schema.dump(account_type)


class DBupResource(Resource):
    def get(self):
        db.create_all()

        type_to_insert = [AccountType(name="Наличные"), AccountType(name="Банковский счет"), AccountType(name="Депозит"), AccountType(name="Кредит"), AccountType(name="Инвестиции")]
        op_type_to_insert = [TransactionType(name="expense"), TransactionType(name="income"), TransactionType(name="transfer")]
        currency_to_insert = [Currency(name="uah", base=1, rate=1), Currency(name="usd", base=0, rate=25.25), Currency(name="eur", base=0, rate=28)]
        db.session.bulk_save_objects(type_to_insert)
        db.session.bulk_save_objects(op_type_to_insert)
        db.session.bulk_save_objects(currency_to_insert)
        db.session.commit()

        return ({"dbup": True})


api.add_resource(TransactionListResource, '/api/v2/transactions')
api.add_resource(TransactionResource, '/api/v2/transactions/<int:operation_id>')


api.add_resource(UserListResource, '/api/v2/users')
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')

api.add_resource(AccountListResource, '/api/v2/accounts', '/api/v2/users/<int:user_id>/accounts')
api.add_resource(AccountResource, '/api/v2/accounts/<int:account_id>')


api.add_resource(AccountTypeListResource, '/api/v2/accounttypes')
api.add_resource(AccountTypeResource, '/api/v2/accounttypes/<int:account_type_id>')

api.add_resource(DBupResource, '/api/v2/dbup')


if __name__ == '__main__':
    app.run(debug=True)