"""
Lab 10 - Exercise 4: ComponentResource refactor of Exercise 3.

Uses the RegionalBucket component to provision two regional buckets
with different lifecycle configurations and a custom name prefix.
"""
import pulumi
from components import RegionalBucket

# Region -> lifecycle_days. Different values per region (as required by Ex. 4 point 3).
region_config = {
    "us-east-1": 60,   # archive faster - example: dev/test data
    "us-west-2": 90,   # standard archive window - example: production logs
}

bucket_name_prefix = "lab10-mlops-"

buckets = {
    region: RegionalBucket(
        f"lab-{region}",
        region=region,
        lifecycle_days=days,
        bucket_name_prefix=bucket_name_prefix,
    )
    for region, days in region_config.items()
}

# Export region -> ARN, same shape as Exercise 3
pulumi.export(
    "bucketArns",
    {region: b.bucket.arn for region, b in buckets.items()},
)
pulumi.export(
    "bucketNames",
    {region: b.bucket.id for region, b in buckets.items()},
)
pulumi.export(
    "lifecycleDaysByRegion",
    region_config,
)
