from aws_cdk import (
    aws_lambda as lambda_,
    aws_apigatewayv2 as _apigw,
    aws_apigatewayv2_integrations as _integration,
    aws_dynamodb as _dynamo,
    CfnOutput,
    Stack
)
from constructs import Construct


class TodoPythonAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        task_table = _dynamo.Table(
            self,
            'Tasks',
            billing_mode=_dynamo.BillingMode.PAY_PER_REQUEST,
            partition_key=_dynamo.Attribute(name='task_id',type=_dynamo.AttributeType.STRING),
            table_name='todo_tasks',
            time_to_live_attribute='ttl'
            )
        
        task_table.add_global_secondary_index(
            index_name='user-index',
            partition_key=_dynamo.Attribute(name='user_id',type=_dynamo.AttributeType.STRING),
            sort_key=_dynamo.Attribute(name="created_time",type=_dynamo.AttributeType.NUMBER)
            )

        """----------lambda functions----------"""
        hello_fn = lambda_.Function(
            self,
            'helloWorldfn',
            code=lambda_.Code.from_asset('./lambdas'),
            description='function to return hello message',
            function_name='hello_world_function',
            handler="hello.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

        read_task_fn = lambda_.Function(
            self,
            'readTaskfn',
            code=lambda_.Code.from_asset('./lambdas'),
            description='function to get task by id',
            function_name='read_task_function',
            handler="task.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

        read_all_tasks_fn = lambda_.Function(
            self,
            'readAllTaskfn',
            code=lambda_.Code.from_asset('./lambdas'),
            description='function to retrieve all tasks by user ID',
            function_name='read_all_tasks_function',
            handler="list_tasks.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )
        """----------lambda functions----------"""

        """----------database permissions----------"""
        task_table.grant_read_data(read_task_fn)
        task_table.grant_read_data(read_all_tasks_fn)
        """----------database permissions----------"""

        http_todo_api = _apigw.HttpApi(
            self,
            'TodoHttpApi',
            cors_preflight=_apigw.CorsPreflightOptions(
                allow_methods=[
                    _apigw.CorsHttpMethod.GET,
                    _apigw.CorsHttpMethod.POST,
                    _apigw.CorsHttpMethod.PUT,
                    _apigw.CorsHttpMethod.DELETE
                    ],
                allow_origins=['*'],
            )
        )

        """----------gateway routes----------"""
        http_todo_api.add_routes(
            path='/',
            methods=[_apigw.HttpMethod.GET],
            integration=_integration.HttpLambdaIntegration('LambdaHelloInt', handler=hello_fn)
        )

        http_todo_api.add_routes(
            path='/task/{task_id}',
            methods=[_apigw.HttpMethod.GET],
            integration=_integration.HttpLambdaIntegration('ReadTaskInt', handler=read_task_fn)
        )
        """----------gateway routes----------"""

        CfnOutput(
            self,
            'Todo Api Endpoints',
            description='endpoints from todo api',
            value=http_todo_api.api_endpoint)

