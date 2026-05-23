import pulumi
from components import RegionalBucket

region_config = {
    "us-east-1": 60,   
    "us-west-2": 90,  
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
