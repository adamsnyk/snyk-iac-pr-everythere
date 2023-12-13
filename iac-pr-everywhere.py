import os
import sys
import time
from github import Github

repo_names = []

# Parsing command-line argument for GitHub organization
if len(sys.argv) != 2 or not sys.argv[1].startswith("GITHUB_ORG="):
    raise ValueError("Usage: python iac-pr-everywhere.py GITHUB_ORG=your_org_name")

org_name = sys.argv[1].split("=")[1]

# Authentication - using environment variables for the GitHub and Snyk tokens
github_token = os.getenv('GITHUB_TOKEN')
snyk_token = os.getenv('SNYK_TOKEN')

if not github_token:
    raise Exception("GitHub token not found in environment variables")
if not snyk_token:
    raise Exception("Snyk token not found in environment variables")

g = Github(github_token)

# Main processing
org = g.get_organization(org_name)
file_path = './snyk-iac-pr.yml'

with open(file_path, 'r') as file:
    file_content = file.read()
content = file_content

# Collect repo objects from the names provided
repos = []
try:
    if repo_names == '*':
        repos = org.get_repos()
    else:
        for repo_name in repo_names:
            repo = org.get_repo(repo_name)
            repos.append(repo)
            time.sleep(1)
    print(f"Collected repos for: {repo_names}")
except:
    print(f"Failed to create repository objects for: {repo_names}")


for repo in repos:
    if repo_names!= '*' and repo.name not in repo_names:
        print(f"Skipping repo: {repo.name}")
        continue

    print(f"Processing repo: {repo.name}")
    default_branch = repo.default_branch

    # Create a GH action secret for Snyk token
    repo.create_secret("SNYK_TOKEN", snyk_token)
    print(f" - Created secret")
    time.sleep(1)

    # Create a new branch from the default branch
    target_branch = 'add-snyk-iac-pr-file'
    source_branch_ref = repo.get_git_ref(f'heads/{default_branch}')
    repo.create_git_ref(ref=f'refs/heads/{target_branch}', sha=source_branch_ref.object.sha)
    print(f" - Created branch")
    time.sleep(1)

    # Create the .github/workflows directory if it does not exist and add the new file
    workflows_path = ".github/workflows/snyk-iac-pr.yml"
    repo.create_file(path=workflows_path,
                        message="Add Snyk IAC PR GitHub Action",
                        content=content,
                        branch=target_branch)
    print(f" - Added file ")
    time.sleep(1)

    # Create a pull request
    repo.create_pull(title="Add Snyk IAC PR GitHub Action",
                        body="Automated PR to add Snyk IAC PR GitHub Action",
                        head=target_branch,
                        base=default_branch)
    print(f" - Created PR")
    print(f" - Sleeping for 10s")
    time.sleep(10)

print("Script completed.")