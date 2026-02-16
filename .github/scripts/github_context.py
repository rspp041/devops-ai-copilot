import argparse
from pathlib import Path
import requests
from .utils import gh_headers

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["pr-diff"])
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--issue-number", required=True, help="PR number")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    owner, name = args.repo.split("/", 1)
    pr_number = args.issue_number

    if args.mode == "pr-diff":
        url = f"https://api.github.com/repos/{owner}/{name}/pulls/{pr_number}"
        headers = gh_headers()
        headers["Accept"] = "application/vnd.github.v3.diff"
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        Path(args.out).write_text(r.text, encoding="utf-8")

if __name__ == "__main__":
    main()
