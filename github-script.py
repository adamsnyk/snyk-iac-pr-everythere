import os
from github import Github, InputGitTreeElement
import base64

# Import os module to access environment variables
import os

# Authentication - using an environment variable for the token
token = os.getenv('GITHUB_TOKEN')
if not token:
    raise Exception("GitHub token not found in environment variables")

g = Github(token)

# Organization name
org_name = 'YOUR_ORG_NAME'

# Path to your .yml file on your local system
file_path = './snyk-iac-pr.yml'

# Read the content of your .yml file
with open(file_path, 'r') as file:
    file_content = file.read()

# Encode the file content
encoded_content = base64.b64encode(file_content.encode("utf-8"))

# Get the organization
org = g.get_organization(org_name)

# Function to check for specific file types in a repo
def contains_infra_files(repo):
    query_formats = ['extension:tf', 'extension:yml', 'extension:yaml', 'extension:template', 'extension:json']
    for query in query_formats:
        result = g.search_code(query=f'{query} repo:{org_name}/{repo.name}')
        if result.totalCount > 0:
            return True
    return False

# List all repos in the org
for repo in org.get_repos():
    print(f"Checking repo: {repo.name}")

    # Check if repo contains Terraform, Kubernetes or CloudFormation files
    if contains_infra_files(repo):
        print(f"Processing repo: {repo.name}")

        # Create a new branch from the default branch
        source_branch = 'main'  # Adjust if your default branch is different
        target_branch = 'add-snyk-iac-pr-file'
        source_branch_ref = repo.get_git_ref(f'heads/{source_branch}')
        repo.create_git_ref(ref=f'refs/heads/{target_branch}', sha=source_branch_ref.object.sha)

        # Create the .github/workflows directory if it does not exist and add the new file
        workflows_path = ".github/workflows/snyk-iac-pr.yml"
        repo.create_file(path=workflows_path,
                         message="Add Snyk IAC PR GitHub Action",
                         content=encoded_content,
                         branch=target_branch)

        # Create a pull request
        repo.create_pull(title="Add Snyk IAC PR GitHub Action",
                         body="Automated PR to add Snyk IAC PR GitHub Action",
                         head=target_branch,
                         base=source_branch)

        print(f"Pull request created for repo: {repo.name}")
    else:
        print(f"Skipping repo: {repo.name} (No relevant infrastructure files found)")

print("Script completed.")
