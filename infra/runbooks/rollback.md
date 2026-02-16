# Rollback Runbook (Allowlisted)

## When to rollback
- Error rate spike after deploy
- Customer impact confirmed
- No faster mitigation available (restart/scale)

## Preconditions
- Confirm last known good version
- Confirm dependency health
- Approval required (GitHub environment gate)

## Execution
- Trigger `/rollback`
- Verify service health
- Add timeline notes and follow-up actions
