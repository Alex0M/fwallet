from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify
from flask.json import JSONEncoder
import mysql.connector
from datetime import date
import os
from numbers import Number

app = Flask(__name__)
api = Api(app)

class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            if isinstance(obj, Number):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


class TransactionListAPI(Resource):
    def get(self):
        db = mysql.connector.connect(host=os.environ['MYSQL_HOST'],port=os.environ['MYSQL_PORT'],database=os.environ['MYSQL_DATABASE'],user=os.environ['MYSQL_USER'],password=os.environ['MYSQL_PASSWORD'])
        cursor = db.cursor()

        query = ("select operation.id 'id', operation.date 'date', operation.amount 'amount', category.name 'description', p_category.name 'category', account.name 'account', users.username 'user' from operation, operation_type, category, category p_category, account, users "
              "where operation.operationtype_id=operation_type.id and operation.category_id=category.id and category.parent_id=p_category.id and operation.account_id=account.id and account.users_id=users.id and")
    

        query = query[:-4] + ';'

        cursor.execute(query)
        headers=[x[0] for x in cursor.description]
        json_data=[]
        
        for result in cursor.fetchall():
            json_data.append(dict(zip(headers,result)))

        cursor.close()
        db.close()

        return jsonify(json_data)

    def post(self):
        pass

class TransactionAPI(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass

    def delete(self, id):
        pass

class AccountListAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(TransactionListAPI, '/api/v2/transactions')
api.add_resource(TransactionAPI, '/api/v2/transactions/<int:id>')

api.add_resource(AccountListAPI, '/api/v2/accounts')


if __name__ == '__main__':
    app.run(debug=True)