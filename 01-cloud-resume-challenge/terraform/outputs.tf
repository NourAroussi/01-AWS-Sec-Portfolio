output "website_url" {
  description = "CloudFront distribution URL"
  value       = "https://${aws_cloudfront_distribution.website.domain_name}"
}

output "api_url" {
  description = "API Gateway URL for visitor counter"
  value       = "${aws_apigatewayv2_api.counter.api_endpoint}/count"
}

output "s3_bucket" {
  description = "S3 bucket name for uploading site files"
  value       = aws_s3_bucket.website.id
}
