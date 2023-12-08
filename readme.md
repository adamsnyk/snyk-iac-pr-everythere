# README for GitHub Repository Processing Script

## Overview

This script is designed to automate the process of adding a specific GitHub Actions workflow file (`snyk-iac-pr.yml`) to repositories within a specified GitHub organization. It targets repositories containing infrastructure-related files (like Terraform, Kubernetes, or CloudFormation) and adds a Snyk token as a GitHub Actions secret for each repository.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- A GitHub account and a personal access token with appropriate permissions.
- A Snyk account and a Snyk token.

### Installation

1. **Clone or Download the Repository**

   - Clone this repository to your local machine or download the source code.

2. **Install Required Python Packages**
   - Navigate to the root directory of the project where the `requirements.txt` file is located.
   - Create a virtual environment (recommended) to isolate the project dependencies:
     - For Windows: `python -m venv venv`
     - For Linux/macOS: `python3 -m venv venv`
   - Activate the virtual environment:
     - For Windows: `.env\Scriptsctivate`
     - For Linux/macOS: `source venv/bin/activate`
   - Install the dependencies: `pip install -r requirements.txt`

### Configuration

1. **Set Environment Variables**

   - Set the `GITHUB_TOKEN` and `SNYK_TOKEN` environment variables with your GitHub and Snyk tokens, respectively.

     - For Windows (CMD):
       - `set GITHUB_TOKEN=your_github_token`
       - `set SNYK_TOKEN=your_snyk_token`
     - For Windows (PowerShell):
       - `$env:GITHUB_TOKEN="your_github_token"`
       - `$env:SNYK_TOKEN="your_snyk_token"`
     - For Linux/macOS:
       - `export GITHUB_TOKEN=your_github_token`
       - `export SNYK_TOKEN=your_snyk_token`

   - Replace `your_github_token` and `your_snyk_token` with the actual tokens.

### Usage

1. **Running the Script**
   - With the environment variables set and dependencies installed, you can run the script using the following command:
     - `python iac-pr-everywhere.py GITHUB_ORG=your_org_name`
   - Replace `your_org_name` with the name of your GitHub organization.

## Important Notes

- Keep your tokens confidential to prevent unauthorized access.
- Ensure that your GitHub token has the necessary permissions for the script to function correctly.
- Test the script in a controlled environment before using it in production.
- Deactivate your virtual environment after use with the `deactivate` command.

---

This README provides instructions for setting up, configuring, and running the script. Modify and use it according to your project's needs!
