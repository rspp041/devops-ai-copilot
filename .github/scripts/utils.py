import os
import requests

def gh_headers():
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN or GITHUB_TOKEN not set.")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

def gh_post(url: str, payload: dict, headers=None):
    r = requests.post(url, json=payload, headers=headers or gh_headers(), timeout=60)
    r.raise_for_status()
    return r
