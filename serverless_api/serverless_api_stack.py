from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_codedeploy as codedeploy,
    aws_s3 as s3,
    CfnOutput
)
from constructs import Construct


class ServerlessApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create Lambda function
        lambda_function = lambda_.Function(
            self, "ApiHandler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("lambda"),
            handler="index.handler",
            description="Lambda function for API Gateway proxy",
            timeout=Duration.seconds(30),
            memory_size=128,
            current_version_options=lambda_.VersionOptions(
                # removal_policy=lambda_.RemovalPolicy.RETAIN,
                description="Initial version",
            ),
        )

        # Create a specific version for the Lambda function
        version = lambda_function.current_version

        # Create an alias that points to the current version
        alias = lambda_.Alias(
            self, "ApiHandlerAlias",
            alias_name="live",
            version=version,
            description="Live alias for API Gateway"
        )

        # Create CodeDeploy application for Lambda deployment
        deployment_group = codedeploy.LambdaDeploymentGroup(
            self, "ApiDeploymentGroup",
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.ALL_AT_ONCE,
            alarms=[],  # You can add CloudWatch alarms here for deployment monitoring
        )

        # Create API Gateway REST API
        api = apigw.RestApi(
            self, "ServerlessApi",
            rest_api_name="Serverless API",
            description="Serverless API with Lambda proxy",
            deploy_options=apigw.StageOptions(
                stage_name="prod",
                description="Production stage",
                throttling_rate_limit=100,
                throttling_burst_limit=50,
            ),
            endpoint_types=[apigw.EndpointType.REGIONAL]
        )

        # Create a proxy resource with ANY method
        proxy_resource = api.root.add_proxy(
            default_integration=apigw.LambdaIntegration(
                alias,
                proxy=True,
                allow_test_invoke=True
            ),
            any_method=True,
        )

        # create S3 bucket to store artifacts
        artifact_bucket = s3.Bucket(self, "artifact_bucket")
        artifact_bucket.grant_read(deployment_group.role)

        # Output the API URL
        CfnOutput(
            self, "ApiUrl",
            description="URL of the API Gateway",
            value=api.url
        )

        # Output the S3 Bucket
        CfnOutput(
            self, "ArtifactBucket",
            description="Bucket Name",
            value=artifact_bucket.bucket_name
        )

        CfnOutput(
            self, "DeploymentGroupName",
            description="Deployment Group Name",
            value=deployment_group.deployment_group_name
        )

        CfnOutput(
            self, "ApplicationName",
            description="CodeDeploy Application Name",
            value=deployment_group.application.application_name
        )

        # Output the Lambda function name
        CfnOutput(
            self, "LambdaFunctionName",
            description="Lambda function name",
            value=lambda_function.function_name
        )

        # Output the Lambda function ARN
        CfnOutput(
            self, "LambdaFunctionArn",
            description="Lambda function ARN",
            value=lambda_function.function_arn
        )
