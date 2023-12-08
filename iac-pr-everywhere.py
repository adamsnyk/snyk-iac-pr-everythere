import os
import sys
import base64
from github import Github
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Parsing command-line arguments for GitHub and Snyk tokens
if len(sys.argv) != 3 or not sys.argv[1].startswith("GITHUB_ORG=") or not sys.argv[2].startswith("SNYK_TOKEN="):
    raise ValueError("Usage: python iac-pr-everywhere.py GITHUB_ORG=your_org_name SNYK_TOKEN=your_snyk_token")

org_name = sys.argv[1].split("=")[1]
snyk_token = sys.argv[2].split("=")[1]

# Authentication - using an environment variable for the GitHub token
github_token = os.getenv('GITHUB_TOKEN')
if not github_token:
    raise Exception("GitHub token not found in environment variables")

g = Github(github_token)

# Function to encrypt a secret using the provided public key
def encrypt_secret(public_key, secret_value):
    public_key = serialization.load_pem_public_key(
        base64.b64decode(public_key.encode("utf-8")), 
        backend=default_backend()
    )
    encrypted = public_key.encrypt(
        secret_value.encode("utf-8"),
        padding.PKCS1v15()
    )
    return base64.b64encode(encrypted).decode("utf-8")

# Function to check for specific file types in a repo
def contains_infra_files(repo):
    query_formats = ['extension:tf', 'extension:yml', 'extension:yaml', 'extension:template', 'extension:json']
    for query in query_formats:
        result = g.search_code(query=f'{query} repo:{org_name}/{repo.name}')
        if result.totalCount > 0:
            return True
    return False

# Main processing
org = g.get_organization(org_name)
file_path = './snyk-iac-pr.yml'

with open(file_path, 'r') as file:
    file_content = file.read()
encoded_content = base64.b64encode(file_content.encode("utf-8"))

for repo in org.get_repos():
    print(f"Checking repo: {repo.name}")

    if contains_infra_files(repo):
        print(f"Processing repo: {repo.name}")
        default_branch = repo.default_branch

        # Encrypt SNYK_TOKEN and add it as a secret
        public_key_info = repo.get_public_key()
        encrypted_snyk_token = encrypt_secret(public_key_info.key, snyk_token)
        repo.create_secret("SNYK_TOKEN", encrypted_snyk_token)

        # Create a new branch from the default branch
        target_branch = 'add-snyk-iac-pr-file'
        source_branch_ref = repo.get_git_ref(f'heads/{default_branch}')
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
                         base=default_branch)

        print(f"Pull request created for repo: {repo.name}")
    else:
        print(f"Skipping repo: {repo.name} (No relevant infrastructure files found)")

print("Script completed.")
