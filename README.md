# Responsible AI assessment skill bundle
Version 0.1.0 | 30 October 2026 | Implementation draft; baseline blocked.

## What this is
One packageable skill derived from the uploaded Responsible AI Agent and MVP PRD v2.0. `SKILL.md` is the entry point. It uses numbered, on-demand references, separate templates and JSON schemas. It needs no Python, scripts or installed packages. The MVP takes precedence over the original agent's weighted scoring and approval language.

## Installation and use
1. Unzip the download and rename the folder to `responsible-ai-assessment` (it must match the skill name).
2. Copy that folder into your skills folder:
   - **Claude Code:** `~/.claude/skills/`
   - **GitHub Copilot (VS Code):** `~/.copilot/skills/`
3. Restart the app, then type `/responsible-ai-assessment` in chat, followed by your project details.

Alternatively, open the unzipped folder as a workspace in VS Code; `/responsible-ai-assessment` works there via `.github/prompts/`. For other hosts, use the location that host documents for skills. No universal compatibility is claimed.
No network, credentials, connectors or code execution are used.

**Before assessment:** complete and approve `assets/policy-pack/public-sector-rai.json`, or supply a completed draft and explicitly authorise design testing. The shipped empty scaffold deliberately fails operational validation. Confirm runtime and data-handling controls. See OPEN_QUESTIONS.md.

Example user request: “Assess this project's authorised AI evidence against the bundled public sector pack. Confirm material missing inputs first. Produce the control assessment, concern/action register and output files. Do not modify source files.”

## How checks work
The model performs evidence interpretation, optional comparison, pack validation, rule lookup, report generation and output validation, following the checklists in references 03, 06 and 09. There is no executable code, so these checks are model-performed and can miss errors; the skill must say so in its outputs. The rule model supports exact evidence-status predicates only. It does not implement general policy logic, evidence extraction, semantic matching or independent identity verification. A specialist must approve any extension.

## Contents
- `SKILL.md`: inputs, stop rules, ten internal steps and complete numbered references index.
- `references/`: detailed processing rules and checklists loaded only when needed.
- `assets/`: intake/questions/report templates, canonical JSON template, schemas and blocked baseline scaffold.
- `evals/`: specialist review cases and requirements traceability.
- `OPEN_QUESTIONS.md`: unresolved source dependencies, not silently decided.
- `PROVENANCE.md`: source authority and design changes.

The canonical JSON template is intentionally uncompleted and is not a valid assessment. Do not confuse packaging tests with approval, reasoning evaluation or tenant acceptance. Generated assessment outputs remain separate draft records. No raw evidence is copied into exports by default.
