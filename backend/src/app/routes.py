from app import app
from flask import request, jsonify, make_response
import mysql.connector
import os
from numbers import Number


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/api/v2/transactions', methods=['GET'])
def get_all_transactions():
    db = mysql.connector.connect(host=os.environ['MYSQL_HOST'],port=os.environ['MYSQL_PORT'],database=os.environ['MYSQL_DATABASE'],user=os.environ['MYSQL_USER'],password=os.environ['MYSQL_PASSWORD'])
    cursor = db.cursor()
    
    query = ("select operation.id 'id', operation.date 'date', operation.amount 'amount', category.name 'description', p_category.name 'category', account.name 'account', users.username 'user' from operation, operation_type, category, category p_category, account, users "
              "where operation.operationtype_id=operation_type.id and operation.category_id=category.id and category.parent_id=p_category.id and operation.account_id=account.id and account.users_id=users.id;")
    
    cursor.execute(query)
    headers=[x[0] for x in cursor.description]
    json_data=[]
    
    for result in cursor.fetchall():
        json_data.append(dict(zip(headers,result)))

    cursor.close()
    db.close()
    
    return jsonify(json_data)

@app.route('/api/v2/accounts', methods=['GET'])
def get_all_acounts():

    query = ("select users.username 'username', account.id 'id', account.name 'name', account_type.name 'type', account_type.id 'type_id', account.balance 'balance', currency.name 'currency' from account, account_type, users, currency "
             "where account.accounttype_id=account_type.id and account.users_id=users.id and account.currency_id=currency.id and")

    if (request.args):
        query_parameters = request.args

        username = query_parameters.get('username')

        if username:
            query += ' users.username="' + username + '" and'
        if not (username):
            return page_not_found(404)
    else:
        query = query
    
    query = query[:-4] + ';'
    
    db = mysql.connector.connect(host=os.environ['MYSQL_HOST'],port=os.environ['MYSQL_PORT'],database=os.environ['MYSQL_DATABASE'],user=os.environ['MYSQL_USER'],password=os.environ['MYSQL_PASSWORD'])
    cursor = db.cursor()
    cursor.execute(query)
    headers=[x[0] for x in cursor.description]
    json_data=[]
        
    for result in cursor.fetchall():
        json_data.append(dict(zip(headers,result)))

    cursor.close()
    db.close()
    
    return jsonify(json_data)