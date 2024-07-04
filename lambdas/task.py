import json
from utils.help import DecimalEncoder, _get_table


def handler(event, context):
    path_parameters = event['pathParameters']
    task_id = path_parameters['task_id']

    try:
        table = _get_table()
        response = table.get_item(Key={'task_id': task_id})
        item = response.get('Item')
        if not item:
            return {'statusCode': 404, 'body': json.dumps({'message': f"task {task_id} not found"})}
        return {'statusCode': 200, 'body': json.dumps(item, cls=DecimalEncoder)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'something went wrong! Error: {str(e)}'})}