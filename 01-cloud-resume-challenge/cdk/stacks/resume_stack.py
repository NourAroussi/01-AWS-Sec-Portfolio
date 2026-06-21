from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigatewayv2 as apigwv2,
    aws_apigatewayv2_integrations as integrations,
)
from constructs import Construct


class CloudResumeStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # S3 Bucket for static site
        bucket = s3.Bucket(
            self, "WebsiteBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # CloudFront Distribution
        distribution = cloudfront.Distribution(
            self, "Distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                compress=True,
            ),
            default_root_object="index.html",
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
        )

        # Deploy site files to S3 and invalidate CloudFront cache
        s3deploy.BucketDeployment(
            self, "DeploySite",
            sources=[s3deploy.Source.asset("../site")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # DynamoDB Table
        table = dynamodb.Table(
            self, "VisitorCounter",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Lambda Function
        counter_fn = _lambda.Function(
            self, "CounterFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="counter.handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={"TABLE_NAME": table.table_name},
        )
        table.grant_read_write_data(counter_fn)

        # HTTP API Gateway
        api = apigwv2.HttpApi(
            self, "CounterApi",
            cors_preflight=apigwv2.CorsPreflightOptions(
                allow_origins=["*"],
                allow_methods=[apigwv2.CorsHttpMethod.GET],
            ),
        )
        api.add_routes(
            path="/count",
            methods=[apigwv2.HttpMethod.GET],
            integration=integrations.HttpLambdaIntegration("CounterIntegration", counter_fn),
        )

        # Outputs
        CfnOutput(self, "WebsiteURL", value=f"https://{distribution.domain_name}")
        CfnOutput(self, "ApiURL", value=f"{api.url}count")
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
