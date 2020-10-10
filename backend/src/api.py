from flask import Flask
from apps.dbmodels import db, Operation
from apps.mamodels import ma, operation_schema, operations_schema
from flask_restful import Api, Resource
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://'+os.environ['MYSQL_USER']+':'+os.environ['MYSQL_PASSWORD']+'@'+os.environ['MYSQL_HOST']+':'+os.environ['MYSQL_PORT']+'/'+os.environ['MYSQL_DATABASE']+'?charset=utf8'
db.init_app(app)
ma.init_app(app)
api = Api(app)


class OperationListResource(Resource):
    def get(self):
        operation = Operation.query.all()
        return operations_schema.dump(operation)


class OperationResource(Resource):
    def get(self, operation_id):
        operation = Operation.query.get_or_404(operation_id)
        return operation_schema.dump(operation)


api.add_resource(OperationListResource, '/api/v2/operations')
api.add_resource(OperationResource, '/api/v2/operations/<int:operation_id>')


if __name__ == '__main__':
    app.run(debug=True)