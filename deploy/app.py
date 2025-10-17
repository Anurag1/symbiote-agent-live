#!/usr/bin/env python3
import aws_cdk as cdk
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_iam as iam

app = cdk.App()

class SymbioteStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_fn = _lambda.Function(
            self, "SymbioteAgentLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_handler.lambda_handler",
            code=_lambda.Code.from_asset(".."),
            environment={"BEDROCK_REGION": "us-east-1"}
        )

        lambda_fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:*", "bedrock-agent-runtime:*"],
            resources=["*"]
        ))

        api = apigw.RestApi(self, "SymbioteAPI")
        integration = apigw.LambdaIntegration(lambda_fn)
        api.root.add_method("POST", integration)

        cdk.CfnOutput(self, "Endpoint", value=api.url)

SymbioteStack(app, "SymbioteAgentStack")
app.synth()
