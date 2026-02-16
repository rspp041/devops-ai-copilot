import argparse
from pathlib import Path
from .utils import gh_post

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--issue-number", required=True)
    ap.add_argument("--body-file", required=True)
    args = ap.parse_args()

    owner, name = args.repo.split("/", 1)
    issue_number = args.issue_number
    body = Path(args.body_file).read_text(encoding="utf-8", errors="ignore")

    url = f"https://api.github.com/repos/{owner}/{name}/issues/{issue_number}/comments"
    gh_post(url, {"body": body})

if __name__ == "__main__":
    main()
