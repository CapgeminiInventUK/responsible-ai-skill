# Contributing

## Branching

- Start every change from the latest `main`.
- Use one branch per skill or logical change, named `type/short-description`.
- Use lowercase letters and hyphens only in the description: no spaces, capitals or underscores.
- Choose a type that matches the change:
  - `feat/` for a new skill or capability, such as `feat/product-intent-author`
  - `fix/` to correct existing behaviour, such as `fix/task-spec-validation`
  - `docs/` for documentation changes, such as `docs/v1-2-proposition`
  - `chore/` for tooling, configuration or maintenance, such as `chore/setup-validation`

For example:

```sh
git switch main
git pull --ff-only
git switch -c feat/short-description
```

## Pull requests

Push your branch and merge changes into `main` through a pull request. Do not commit directly to `main`. Branch protection is not yet enforced, so this is a convention; see [GOVERNANCE.md](https://github.com/CapgeminiInventUK/Invent-Agentic-Engineering-Suite/blob/main/GOVERNANCE.md#branch-protection).

Before opening a pull request, run the checks relevant to your change and include their results and a concise summary in the pull request description.
