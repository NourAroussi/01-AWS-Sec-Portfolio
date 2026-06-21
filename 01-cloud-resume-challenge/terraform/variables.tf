variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "cloud-resume"
}

variable "domain_name" {
  description = "Custom domain name (optional - leave empty to use CloudFront URL)"
  type        = string
  default     = ""
}
