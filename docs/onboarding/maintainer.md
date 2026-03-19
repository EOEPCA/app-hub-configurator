# Maintainer onboarding

This guide is for repository maintainers responsible for quality and releases.

## 1. Core responsibilities

- Review pull requests for correctness and backward compatibility
- Ensure test and lint pipelines stay green
- Maintain docs and release notes quality
- Cut and publish tagged releases

## 2. Review checklist

1. Behavior change is covered by tests.
2. Docs are updated for user-facing changes.
3. No accidental breaking changes in profile slugs, CLI options, or schema.
4. CI workflows still pass (`package`, `docs`).

## 3. Release checklist

1. Bump version in `configurator/__about__.py`.
2. Confirm `task test` and `task check` pass.
3. Tag the release (`vX.Y.Z`) matching project version.
4. Push tag to trigger GitHub publish workflow.
5. Verify package is published and installable.
6. Validate Skaffold deployment profiles (`baseline`, `develop`, `main`) still point to expected hub image/tag and config file wiring.

## 4. Security and governance

- Follow `SECURITY.md` for vulnerability reporting.
- Follow `CODE_OF_CONDUCT.md` for community interactions.
- Keep templates in `.github/` current for issues and PRs.

## 5. Recommended first reads

- `docs/dev/release.md`
- `CONTRIBUTING.md`
- `.github/workflows/package.yaml`
