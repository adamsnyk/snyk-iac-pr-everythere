# Snyk IaC PR Everywhere

### Run Snyk IaC PR checks across all repos (containing IaC)

Running the script.

```
export GITHUB_TOKEN=your_token_here
python iac-pr-everywhere.py GITHUB_ORG=my_org_here SNYK_TOKEN=snyk_token_here
```

How the script works

1. Connect to the GH org specified
2. Go through each repo
3. If the repo contains IaC files
   - Add `SNYK_TOKEN` as a repo secret
   - Add `.github/workflows/snyk-iac-pr.yml` as a PR checker
   - Open a pull request to add these files

After the script runs, your developers can accept IaC PR checks!

(Maybe put it into a cron job to add new repos?) I'd have to edit this a bit to handle that ;)

(6d81e448-45c0-47a0-b7d8-bc708aea1933 chat Id for my own sanity to keep progressing)
