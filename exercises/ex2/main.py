"""
Lab 10 - Exercise 2: S3 static website.

Creates an S3 bucket configured as a public static website hosting
a single index.html page.

To run this exercise:
  cp exercises/ex2/main.py __main__.py
  pulumi up
"""
import pulumi
import pulumi_aws as aws

# 1. Bucket
bucket = aws.s3.Bucket(
    "lab-bucket",
    tags={"Name": "pulumi-lab-website"},
)

# 2. Website hosting configuration
website = aws.s3.BucketWebsiteConfiguration(
    "website",
    bucket=bucket.id,
    index_document=aws.s3.BucketWebsiteConfigurationIndexDocumentArgs(
        suffix="index.html"
    ),
)

# 3. Disable default public access block (so the bucket policy can grant public reads)
pab = aws.s3.BucketPublicAccessBlock(
    "public-access-block",
    bucket=bucket.id,
    block_public_acls=False,
    block_public_policy=False,
    ignore_public_acls=False,
    restrict_public_buckets=False,
)

# 4. Bucket policy: allow anonymous s3:GetObject on all objects
policy_document = pulumi.Output.format(
    '{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":"*","Action":"s3:GetObject","Resource":"{0}/*"}}]}}',
    bucket.arn,
)

bucket_policy = aws.s3.BucketPolicy(
    "bucket-policy",
    bucket=bucket.id,
    policy=policy_document,
    opts=pulumi.ResourceOptions(depends_on=[pab]),
)

# 5. Upload index.html
index_html = aws.s3.BucketObject(
    "index-html",
    bucket=bucket.id,
    key="index.html",
    content="""<!DOCTYPE html>
<html lang="pl">
<head>
  <meta charset="UTF-8">
  <title>Pulumi Lab - MLOps Lab 10</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 4em auto; padding: 2em; background: #f5f5f7; }
    h1 { color: #8a3ffc; }
    code { background: #eee; padding: 2px 6px; border-radius: 4px; }
  </style>
</head>
<body>
  <h1>Hello from Pulumi!</h1>
  <p>This static website is served from an S3 bucket provisioned with Pulumi.</p>
  <p>MLOps Lab 10 - Infrastructure as Code</p>
</body>
</html>""",
    content_type="text/html",
)

# Exports
pulumi.export("bucket_name", bucket.id)
pulumi.export("bucket_arn", bucket.arn)
pulumi.export("website_url", pulumi.Output.format("http://{0}", website.website_endpoint))
