import json


def handler(event, context):
    message = {'message': 'Hello world from a lambda function!'}
    return {'statusCode': 200, 'body': json.dumps(message)}