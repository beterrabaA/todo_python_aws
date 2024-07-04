import boto3
from decimal import Decimal
import json
import os


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def _get_table():
    table_name = os.environ.get("TABLE_NAME")
    return boto3.resource('dynamodb').Table(table_name)