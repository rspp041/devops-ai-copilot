# DevOps AI Copilot (AWS + GitHub Actions + OpenAI)

A portfolio repo demonstrating:
- **GenAI test creation** from PR diffs (`/generate-tests`)
- **AI incident triage** from evidence bundles (`/triage`)
- **Gated rollback** with GitHub Environment approvals + AWS OIDC role (`/rollback`)

> ✅ Tokens/keys are **never** stored in the repo. All secrets are read from environment variables or GitHub Secrets.

---

## Quick start (local)

### 1) Create a virtualenv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r tools/requirements-ci.txt
```

### 2) Set env vars (no secrets in repo)
```bash
cp .env.example .env
# then edit .env and export values (or use direnv)
```

### 3) Run AI test generation locally
```bash
python ai/generate_tests.py \
  --diff tools/sample_pr.diff \
  --repo-root . \
  --service apps/sample-service \
  --out-dir /tmp/ai-tests
```

### 4) Run incident triage locally
```bash
python ai/incident_triage.py \
  --evidence-dir tools/sample_evidence \
  --runbooks-dir infra/runbooks \
  --out /tmp/triage.md
cat /tmp/triage.md
```

---

## GitHub Actions ChatOps commands

Add a comment on a PR or issue:

- `/generate-tests`  
  Pulls PR diff → produces a test plan + generates pytest tests → commits back to branch → posts a report comment.

- `/triage`  
  Summarizes evidence → ranks likely causes → recommends **safe** next action (suggest-only).

- `/rollback`  
  Requires **GitHub Environment approval** (`production` environment) and uses AWS OIDC role.

---

## Guardrails
- Suggest-first, execute-only-after-approval (production)
- Allowlisted automation actions
- Least privilege via GitHub OIDC -> AWS IAM role
- Audit trail in GitHub Actions runs + issue comments

---

## Setup checklist (GitHub)

### Repository secrets
- `OPENAI_API_KEY` (required for OpenAI calls)

### Repository variables
- `OPENAI_MODEL` (optional; default `gpt-5.2`)
- `AWS_REGION`
- `AWS_GITHUB_ROLE_ARN` (Terraform output role ARN)
- `LLM_PROVIDER` = `openai`

### GitHub Environment
Create an environment named **production** and enable **required reviewers**.

---

## OpenAI SDK notes
This repo uses the official OpenAI Python SDK with the **Responses API** (recommended).
- Developer quickstart citeturn0search1
- Python SDK reference citeturn0search5
- Responses API reference citeturn0search3
- Migration guide to Responses citeturn0search0
