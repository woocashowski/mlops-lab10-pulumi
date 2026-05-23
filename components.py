import pulumi
import pulumi_aws as aws


class RegionalBucket(pulumi.ComponentResource):

    def __init__(
        self,
        name: str,
        region: str,
        lifecycle_days: int = 90,
        bucket_name_prefix: str = "",
        opts: pulumi.ResourceOptions = None,
    ):
        super().__init__("lab:index:RegionalBucket", name, {}, opts)

        child_opts = pulumi.ResourceOptions(parent=self)

        provider = aws.Provider(
            f"{name}-provider",
            region=region,
            opts=child_opts,
        )

        resource_opts = pulumi.ResourceOptions(parent=self, provider=provider)

        bucket_args = {
            "tags": {
                "Region": region,
                "Lab": "mlops-lab10",
                "Component": "RegionalBucket",
            },
        }
        if bucket_name_prefix:
            bucket_args["bucket_prefix"] = bucket_name_prefix

        self.bucket = aws.s3.Bucket(
            f"{name}-bucket",
            **bucket_args,
            opts=resource_opts,
        )

        aws.s3.BucketVersioning(
            f"{name}-versioning",
            bucket=self.bucket.id,
            versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
                status="Enabled"
            ),
            opts=resource_opts,
        )

        aws.s3.BucketLifecycleConfiguration(
            f"{name}-lifecycle",
            bucket=self.bucket.id,
            rules=[
                aws.s3.BucketLifecycleConfigurationRuleArgs(
                    id="archive",
                    status="Enabled",
                    filter=aws.s3.BucketLifecycleConfigurationRuleFilterArgs(prefix=""),
                    transitions=[
                        aws.s3.BucketLifecycleConfigurationRuleTransitionArgs(
                            days=lifecycle_days,
                            storage_class="GLACIER",
                        )
                    ],
                )
            ],
            opts=resource_opts,
        )

        self.register_outputs(
            {
                "bucket_id": self.bucket.id,
                "bucket_arn": self.bucket.arn,
            }
        )
