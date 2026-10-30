# Responsible AI assessment skill bundle
Version 0.1.0 | 30 October 2026 | Implementation draft; baseline blocked.

## What this is
One packageable skill derived from the uploaded Responsible AI Agent and MVP PRD v2.0. `SKILL.md` is the entry point. It uses numbered, on-demand references, separate templates, JSON schemas and an executable Python validation/rule/export helper. The MVP takes precedence over the original agent's weighted scoring and approval language.

## Installation and use
Unzip and place the entire `responsible-ai-assessment/` folder in the skills location supported by your selected host. Keep `SKILL.md` at the folder root. If the host accepts skill ZIP uploads, use this ZIP only after checking that host's packaging requirements. This bundle has not been installed or tested in your Claude environment; no universal upload compatibility is claimed.
The helper requires Python 3.10+ and `jsonschema>=4.18,<5` (see requirements.txt). No network, credentials or connectors are used. Dependency installation is an environment-administrator task, not an automatic skill action.

**Before assessment:** complete and approve `assets/policy-pack/public-sector-rai.json`, or supply a completed draft and explicitly authorise design testing. The shipped empty scaffold deliberately fails operational validation. Confirm runtime and data-handling controls. See OPEN_QUESTIONS.md.

Example user request: “Assess this project's authorised AI evidence against the bundled public sector pack. Confirm material missing inputs first. Produce the control assessment, concern/action register and downloadable package. Do not modify source files.”

## Local commands
Run from the skill root:
- `python -m unittest discover -s tests -v`
- `python scripts/rai_tool.py validate-pack assets/policy-pack/public-sector-rai.json` (expected to fail while scaffold is blocked)
- `python scripts/rai_tool.py validate-assessment assessment.json --pack assets/policy-pack/public-sector-rai.json`
- `python scripts/rai_tool.py render assessment.json assessment-report.md`
- `python scripts/rai_tool.py export assessment.json assets/policy-pack/public-sector-rai.json assessment-package.zip`

The model performs evidence interpretation and optional comparison. Code enforces schema, references, rule mapping, key lifecycle invariants, rendering and export integrity. The rule engine supports exact evidence-status predicates only. It does not implement general policy logic, evidence extraction, semantic matching or independent identity verification. A specialist must approve any extension.

## Contents
- `SKILL.md`: inputs, stop rules, ten internal steps and complete numbered references index.
- `references/`: detailed processing rules loaded only when needed.
- `assets/`: intake/questions/report templates, canonical JSON template, schemas and blocked baseline scaffold.
- `scripts/rai_tool.py`: offline validation, IDs, hashing, fixed rules, rendering and ZIP export.
- `tests/`: explicitly synthetic technical tests, not real policy controls.
- `evals/`: specialist review cases and requirements traceability.
- `OPEN_QUESTIONS.md`: unresolved source dependencies, not silently decided.
- `PROVENANCE.md`: source authority and design changes.

The canonical JSON template is intentionally uncompleted and is not a valid assessment. Do not confuse packaging tests with approval, reasoning evaluation or tenant acceptance. Generated assessment outputs remain separate draft records. No raw evidence is copied into exports by default.
