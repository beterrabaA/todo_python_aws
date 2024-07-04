from boto3.dynamodb.conditions import Key
import json
from utils.help import DecimalEncoder, _get_table


def handler(event, context):
    path_parameters = event['pathParameters']
    user_id = path_parameters['user_id']
    table = _get_table()

    try:
        response = table.query(
            IndexName="user-index",
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,
            Limit=10
        )
        tasks = response.get('Items')
        return {'statusCode': 200, 'body': json.dumps({'tasks': tasks}, cls=DecimalEncoder)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'something went wrong! Error: {str(e)}'})}