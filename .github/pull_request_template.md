## Summary

<!-- What does this PR change and why? -->

## Test plan

- [ ] Pip CI green
- [ ] Wheels CI green
- [ ] Docker CI green (if Docker/example paths changed)

### Labels

- Add **one** of `release:patch` | `release:minor` | `release:major` on feature PRs into `dev` to influence the next release bump (default is patch).
- Release PRs (`dev` → `main`) are opened via the **Release PR** workflow and must carry a `release:*` label so merge tags a new `vX.Y.Z`.
