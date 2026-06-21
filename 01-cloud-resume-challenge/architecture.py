from diagrams import Diagram, Edge
from diagrams.aws.network import Route53, CloudFront, APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb

with Diagram("Cloud Resume Challenge", filename="architecture", outformat="png", show=False, direction="TB"):
    dns = Route53("Route 53")
    cdn = CloudFront("CloudFront\n(HTTPS, CDN)")

    s3 = S3("S3 Bucket\n(Static Site)")
    api = APIGateway("API Gateway\n(REST)")
    fn = Lambda("Lambda\n(Python)")
    db = Dynamodb("DynamoDB\n(Visitor Counter)")

    dns >> cdn
    cdn >> s3
    cdn >> api >> fn >> db
