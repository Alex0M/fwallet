from flask import Flask
from apps.dbmodels import db, Transaction, TransactionType, Account, AccountType, Currency
from apps.mamodels import ma, transaction_schema, transactions_schema, accounts_schema
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
    def get(self):
        account =  Account.query.all()
        return accounts_schema.dump(account)


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

api.add_resource(AccountListResource, '/api/v2/accounts')

api.add_resource(DBupResource, '/api/v2/dbup')


if __name__ == '__main__':
    app.run(debug=True)