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

### Releasing

- Merging to `main` does **not** release.
- To release: bump `version` in `pyproject.toml` on `main`, then push an annotated tag `vX.Y.Z` — that publishes GHCR `:latest` / `:X.Y.Z` (bare semver) and attaches wheels to a GitHub Release.
