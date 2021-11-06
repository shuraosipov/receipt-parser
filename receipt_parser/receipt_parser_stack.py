import os

from aws_cdk import (
    aws_lambda as lambda_,
    aws_s3 as _s3,
    aws_s3_notifications,
    aws_iam as iam,
    core as cdk
)

class ReceiptParserStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create IAM role for lambda function
        lambda_role = iam.Role(self, "My Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        # attach AWS managed default service role for Lambda function
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        
        # provide access to textract
        lambda_role.add_to_policy(iam.PolicyStatement(
            resources=["*"],
            actions=["textract:AnalyzeExpense"]
        ))

        # create s3 Bucket
        s3 = _s3.Bucket(self, "s3bucket")


        # import an existing Lambda Layer based on ARN
        # layer = lambda_.LayerVersion.from_layer_version_arn(self, "TextractParserLayer",
        #     layer_version_arn = "arn:aws:lambda:us-east-1:419091122511:layer:Amazon-Textract-Parsing-Library-Layer:1"
        # )

        # create lambda layer
        layer = lambda_.LayerVersion(self, "TextractParserLayer",
            code=lambda_.Code.from_asset("lambda-layer"),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_9],
            description="Lambda layer containting amazon-textract-response-parser and amazon-textract-prettyprinter python libraries"
        )

        # create Lambda function
        function = lambda_.Function(self, "MyLambda",
            code=lambda_.Code.from_asset("lambda"),
            handler="lambda_function.lambda_handler",
            runtime=lambda_.Runtime.PYTHON_3_9,
            layers=[layer],
            role=lambda_role,
            timeout=cdk.Duration.seconds(15)
        )

        # create s3 notification for lambda function
        notification = aws_s3_notifications.LambdaDestination(function)

        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3.add_event_notification(_s3.EventType.OBJECT_CREATED, notification, _s3.NotificationKeyFilter(prefix="landing"))

        # provide lambda function with read access to s3 bucket
        s3.grant_read_write(function)


