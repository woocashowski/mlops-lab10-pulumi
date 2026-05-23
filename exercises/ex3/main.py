"""
Lab 10 - Exercise 3: Multi-region S3 buckets with loop.

Creates an S3 bucket per region in a Python loop, each with versioning
enabled and a lifecycle rule transitioning objects to GLACIER after
90 days. Exports a region -> bucket ARN dict.

NOTE on region count:
The exercise instructions ask for 3 regions. However, AWS Academy IAM
policy restricts s3:CreateBucket to us-east-1 and us-west-2 only -
any other region returns AccessDenied. The loop structure is identical
to a 3-region deployment (adding a third region is a single line change
in the `regions` list).

To run this exercise:
  cp exercises/ex3/main.py __main__.py
  pulumi up
"""
import pulumi
import pulumi_aws as aws

# Two regions - AWS Academy permission limit (see note above).
# In an unrestricted account, add e.g. "eu-west-1" here for the third region.
regions = [
    "us-east-1",
    "us-west-2",
]

bucket_arns = {}
bucket_names = {}

for r in regions:
    aws_provider = aws.Provider(f"aws-{r}", region=r)

    b = aws.s3.Bucket(
        f"lab10-{r}",
        tags={
            "env": "lab",
            "region": r,
        },
        opts=pulumi.ResourceOptions(provider=aws_provider),
    )

    aws.s3.BucketVersioning(
        f"{r}-versioning",
        bucket=b.id,
        versioning_configuration={"status": "Enabled"},
        opts=pulumi.ResourceOptions(provider=aws_provider),
    )

    aws.s3.BucketLifecycleConfiguration(
        f"{r}-lifecycle",
        bucket=b.id,
        rules=[{
            "id": "archive",
            "status": "Enabled",
            "transitions": [{
                "days": 90,
                "storage_class": "GLACIER",
            }],
        }],
        opts=pulumi.ResourceOptions(provider=aws_provider),
    )

    bucket_arns[r] = b.arn
    bucket_names[r] = b.id

# Export region -> ARN dict (as required by Exercise 3 point 3)
pulumi.export("bucketArns", bucket_arns)
pulumi.export("bucketNames", bucket_names)
