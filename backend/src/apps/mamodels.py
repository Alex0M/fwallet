from flask_marshmallow import Marshmallow
from apps.dbmodels import Operation

ma = Marshmallow()


class OperationSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "operationtype_id", "currency_id", "category_id", "account_id")
        model = Operation

operation_schema = OperationSchema()
operations_schema = OperationSchema(many=True)