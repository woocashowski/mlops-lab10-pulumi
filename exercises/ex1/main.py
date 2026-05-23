"""
Lab 10 - Exercise 1: GitHub repository + branch protection.

Creates a public GitHub repository with branch protection on 'main'
requiring at least 1 approving review for pull requests.

To run this exercise:
  cp exercises/ex1/main.py __main__.py
  pulumi up
"""
import pulumi
import pulumi_github as github

config = pulumi.Config()
github_token = config.require_secret("github_token")
repo_visibility = config.get("repo_visibility") or "private"

provider = github.Provider("github-provider", token=github_token)

repo = github.Repository(
    "lab-repo",
    name="pulumi-managed-repo",
    description="Repository managed by Pulumi - MLOps Lab 10",
    visibility=repo_visibility,
    auto_init=True,
    opts=pulumi.ResourceOptions(provider=provider),
)

branch_protection = github.BranchProtection(
    "main-protection",
    repository_id=repo.node_id,
    pattern="main",
    enforce_admins=True,
    required_pull_request_reviews=[
        github.BranchProtectionRequiredPullRequestReviewArgs(
            required_approving_review_count=1,
            dismiss_stale_reviews=True,
        )
    ],
    opts=pulumi.ResourceOptions(provider=provider, depends_on=[repo]),
)

pulumi.export("repo_url", repo.html_url)
pulumi.export("repo_full_name", repo.full_name)
pulumi.export("branch_protection_id", branch_protection.id)
