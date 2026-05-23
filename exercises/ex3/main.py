import pulumi
import pulumi_aws as aws

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

pulumi.export("bucketArns", bucket_arns)
pulumi.export("bucketNames", bucket_names)
