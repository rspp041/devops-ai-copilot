variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-west-2"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository in owner/repo format"
}
