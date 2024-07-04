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

        hello_fn = lambda_.Function(
            self,
            'HelloWorldfn',
            code=lambda_.Code.from_asset('./lambdas'),
            description='function to return hello message',
            function_name='hello_world_function',
            handler="hello.handler",
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

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

        http_todo_api.add_routes(
            path='/',
            methods=[_apigw.HttpMethod.GET],
            integration=_integration.HttpLambdaIntegration('LambdaHelloInt', handler=hello_fn)
        )

        CfnOutput(
            self,
            'Todo Api Endpoints',
            description='endpoints from todo api',
            value=http_todo_api.api_endpoint)

