# Lab 10 - Pulumi

MLOps AGH, Lab 10 - IaC, Pulumi + Python path.

## Structure

Each exercise is in a separate folder under `exercise/`. The files from the last exercise (ex4) remain in the root directory so that `pulumi up` will work immediately from the root directory.

To run the previous exercise:

cp exercises/ex2/main.py __main__.py
pulumi up

## Setup

uv sync
source .venv/bin/activate
export PULUMI_CONFIG_PASSPHRASE=""
pulumi login --local
pulumi stack init dev

For ex1, also:

pulumi config set --secret github_token <PAT>
pulumi config set repo_visibility public

## Note - AWS Academy

Sandbox Academy only allows `s3:CreateBucket` in `us-east-1` and `us-west-2`. Other regions (I tested eu-west-1, us-east-2, us-west-1) return AccessDenied. That's why ex3 and ex4 are in 2 regions instead of 3 - in the code, simply add the region to the `regions` list, and the loop will work.

Ex5 (Lambda) - omitted; according to the instructions, this is optional for AWS Academy.

## After each exercise,

`pulumi destroy`, nothing remains in the account.
