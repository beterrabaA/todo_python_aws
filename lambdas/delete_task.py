import json
from utils.help import _get_table


def handler(event, context):
    path_parameters = event['pathParameters']
    task_id = path_parameters['task_id']

    try:
        table = _get_table()
        table.delete_item(Key={'task_id': task_id})

        return {'statusCode': 200, 'body': json.dumps({'deleted_task_id': task_id})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'something went wrong! Error: {str(e)}'})}