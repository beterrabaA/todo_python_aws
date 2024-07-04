import json
from utils.help import _get_table


def handler(event, context):
    path_parameters = event['pathParameters']
    task_id = path_parameters['task_id']

    body = json.loads(event['body'])

    content = body['content']
    is_done = body['is_done']
    try:
        table = _get_table()
        table.update_item(
            Key={'task_id': task_id},
            UpdateExpression='SET content = :content, is_done = :is_done',
            ExpressionAttributeValues={
                ':content': content,
                ':is_done': is_done
            },
            ReturnValues='ALL_NEW'

        )

        return {'statusCode': 200, 'body': json.dumps({'updated_task_id': task_id})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'something went wrong! Error: {str(e)}'})}