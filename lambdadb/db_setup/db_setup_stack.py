# from aws_cdk import (
#     # Duration,
#     Stack,
#     # aws_sqs as sqs,
# )
from constructs import Construct

from aws_cdk import core as cdk 
from aws_cdk import core
from aws_cdk import aws_lambda 
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod
import os



class DbSetupStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        cwd = os.getcwd()
        random_drink_lambda= aws_lambda.Function(self, 
                                                id = "RandomDrinkFunctionV2",
                                                code = aws_lambda.Code.from_asset(os.path.join(cwd, "db_setup/compute")),
                                                handler = "random_drink.lambda_handler",
                                                runtime = aws_lambda.Runtime.PYTHON_3_9)
        
        random_drink_integration = HttpLambdaIntegration(
            "random_drink_lambda", random_drink_lambda
        )

        http_api = HttpApi(self, "RandomDrinkHttpApi")
        http_api.add_routes(
            path= "/random_drink",
            methods=[HttpMethod.ANY],
            integration=random_drink_integration
        )

