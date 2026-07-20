## Summary

<!-- What does this PR change and why? -->

## Test plan

- [ ] Pip CI green
- [ ] Wheels CI green
- [ ] Docker CI green (if Docker/example paths changed)

### Branch name

- Use `<type>/<description>` (lowercase), e.g. `feat/docker-ghcr`, `fix/mqtt-timeout`, `ci/wheels`.
- Allowed types (same as commitlint): `feat` `fix` `docs` `style` `refactor` `perf` `test` `build` `ci` `chore` `revert`.

### Labels

- Add **`ready-to-merge`** when CI is green to enable auto-merge (squash + delete branch).
- Add **one** of `release:patch` | `release:minor` | `release:major` to influence the next release bump (default is patch).
- Release PRs are opened via the **Release PR** workflow and must carry a `release:*` label so merge tags a new `vX.Y.Z` and publishes GHCR `:latest` / `:X.Y.Z`.
