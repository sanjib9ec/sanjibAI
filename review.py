import os
import openai  # or GitHub Copilot Enterprise SDK
from github import Github

repo_name = os.getenv("GITHUB_REPOSITORY")
pr_number = os.getenv("GITHUB_REF").split("/")[-2]
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(repo_name)
pr = repo.get_pull(int(pr_number))

# Collect changed code
diffs = "\n".join([f.filename for f in pr.get_files()])

# Load rules
rules = open(".rules/security.md").read()

# Call Copilot/OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a code review assistant."},
    {"role": "user", "content": f"Review this diff:\n{diffs}\nApply these rules:\n{rules}"}
  ]
)

# Post review back to PR
pr.create_issue_comment(response.choices[0].message["content"])
