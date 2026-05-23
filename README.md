# MLOps Lab 10 — Infrastructure as Code (Pulumi)

Solutions for AGH MLOps course, Lab 10. Track: **Pulumi + Python**.

## Repository structure
Each exercise lives in its own folder so they can be inspected independently.
The root `__main__.py` and `components.py` hold the final state (Exercise 4).
To run an earlier exercise, copy its files into the root:

```bash
cp exercises/ex2/main.py __main__.py
pulumi up
```

## Prerequisites

- AWS account + AWS CLI configured (`aws sts get-caller-identity` should succeed)
- Pulumi CLI installed
- `uv` for Python dependency management
- GitHub Personal Access Token (only needed for Exercise 1)

## Setup

```bash
uv sync
source .venv/bin/activate

export PULUMI_CONFIG_PASSPHRASE=""
pulumi login --local
pulumi stack init dev

# Only for Exercise 1:
pulumi config set --secret github_token <YOUR_GITHUB_PAT>
pulumi config set repo_visibility public
```

## Running an exercise

```bash
pulumi preview     # see planned changes
pulumi up          # apply
pulumi destroy     # tear down
```

## Notes on AWS Academy limitations

This lab was completed on an AWS Academy sandbox account. The Academy IAM
policy restricts `s3:CreateBucket` to **`us-east-1`** and **`us-west-2`** only;
attempts in any other region (tested: `eu-west-1`, `us-east-2`, `us-west-1`)
return `AccessDenied`.

Exercise 3 specifies "three regions", but only two are deployable under this
constraint. The loop structure in `exercises/ex3/main.py` is identical to a
3-region deployment — adding a third region is a single-line change in the
`regions` list. See the report for screenshots of the AccessDenied errors
and the working 2-region deployment.

Exercise 5 (Lambda) was skipped — it is marked optional for AWS Academy
users in the lab instructions.

## Verifying the deployments

All deployments were verified end-to-end:

- **Exercise 1**: `pulumi up` output + GitHub UI screenshots of repository and
  branch protection rule (Require PR + 1 approval).
- **Exercise 2**: `curl` against the website endpoint returned the deployed
  HTML; AWS Console screenshot confirms Static website hosting Enabled.
- **Exercise 3**: `aws s3api get-bucket-versioning` and
  `get-bucket-lifecycle-configuration` confirmed both buckets had versioning
  enabled and a GLACIER transition rule with 90-day trigger.
- **Exercise 4**: Same AWS CLI checks confirmed **different `lifecycle_days`
  per region** (60 days for us-east-1, 90 days for us-west-2), proving the
  `RegionalBucket` ComponentResource is properly parameterised.

All resources were destroyed (`pulumi destroy`) after verification to avoid
ongoing costs. The local state in `.pulumi/` reflects an empty stack at
submission time.
