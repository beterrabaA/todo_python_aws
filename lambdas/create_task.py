import json
import time
import uuid
from utils.help import _get_table


def handler(event, context):
    body = json.loads(event['body'])

    user_id = body['user_id']
    content = body['content']

    str_uuid = str(uuid.uuid4())
    created_time = int(time.time())

    item = {
        'task_id': str_uuid,
        'user_id': user_id,
        'content': content,
        'is_done': False,
        'created_time': created_time,
        'ttl': int(created_time + 86400)  # expire 24 hours
    }
    try:
        table = _get_table()
        table.put_item(Item=item)

        return {'statusCode': 200, 'body': json.dumps(item)}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'message': f'something went wrong! Error: {str(e)}'})}