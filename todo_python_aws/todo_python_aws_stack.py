from aws_cdk import (
    CfnOutput,
    aws_lambda as lambda_,
    aws_apigatewayv2 as _apigw,
    aws_apigatewayv2_integrations as _integration,
    Stack
)
from constructs import Construct


class TodoPythonAwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        hello_fn = lambda_.Function(
            self,
            'HelloWorldfn',
            code=lambda_.Code.from_asset('./lambdas'),
            handler="hello.handler",
            function_name='hello_world_function',
            description='function to return hello message',
            runtime=lambda_.Runtime.PYTHON_3_12,
        )

        http_api = _apigw.HttpApi(
            self,
            'TodoHttpApi',
            cors_preflight=_apigw.CorsPreflightOptions(
                allow_methods=[_apigw.CorsHttpMethod.GET],
                allow_origins=['*'],
            )
        )

