# Responsible AI assessment skill bundle
Version 0.1.0 | 30 October 2026 | Implementation draft; baseline blocked.

## What this is
One packageable skill derived from the uploaded Responsible AI Agent and MVP PRD v2.0. `SKILL.md` is the entry point. It uses numbered, on-demand references, separate templates and JSON schemas. It needs no Python, scripts or installed packages. The MVP takes precedence over the original agent's weighted scoring and approval language.

## Installation and use
The skill is invoked directly as a slash command: `/responsible-ai-assessment` is the skill itself (there is no separate prompt file). VS Code only loads a skill when its folder name matches the `name` in `SKILL.md`, so the folder must be called `responsible-ai-assessment`.
1. Run `build-zip.ps1` to produce `responsible-ai-skill.zip`. The zip contains a single `responsible-ai-assessment/` folder.
2. Extract the zip **into** your skills folder, so the result is `<skills folder>/responsible-ai-assessment/SKILL.md`:
   - **GitHub Copilot (VS Code), personal:** `~/.copilot/skills/` (PowerShell: `Expand-Archive responsible-ai-skill.zip -DestinationPath $HOME\.copilot\skills`)
   - **GitHub Copilot (VS Code), project:** `.github/skills/`
   - **Claude Code:** `~/.claude/skills/`
3. Start a new chat and type `/responsible-ai-assessment` followed by your project details. If it does not appear in the `/` menu, run **Chat: Open Customizations**, open Skills and check the skill is listed; a name or folder mismatch makes it silently not load.

For other hosts, use the location that host documents for skills. No universal compatibility is claimed.
No network, credentials, connectors or code execution are used.

**Output:** one file, `[project]-rai-assessment.html`, saved to the location you approve. It is a self-contained web page (open it in any browser) that includes an Assumptions and gaps section listing information or resources you said you did not have.

**Before assessment:** complete and approve `assets/public-sector-rai.json`, or supply a completed draft and explicitly authorise design testing. The shipped empty scaffold deliberately fails operational validation. Confirm runtime and data-handling controls. See OPEN_QUESTIONS.md.

Example user request: “Assess this project's authorised AI evidence against the bundled public sector pack. Ask once for missing material inputs and log anything I don't have as a gap. Produce the HTML assessment report. Do not modify source files.”

## How checks work
The model performs evidence interpretation, optional comparison, pack validation, rule lookup, report generation and output validation, following the checklists in references 03, 06 and 09. There is no executable code, so these checks are model-performed and can miss errors; the skill must say so in its outputs. The rule model supports exact evidence-status predicates only. It does not implement general policy logic, evidence extraction, semantic matching or independent identity verification. A specialist must approve any extension.

## Contents
- `SKILL.md`: inputs, stop rules, ten internal steps and complete numbered references index.
- `references/`: detailed processing rules and checklists loaded only when needed.
- `assets/`: intake/questions templates, HTML output template, canonical JSON template, schemas and blocked baseline scaffold.
- `evals/`: specialist review cases and requirements traceability.
- `OPEN_QUESTIONS.md`: unresolved source dependencies, not silently decided.
- `PROVENANCE.md`: source authority and design changes.

The canonical JSON template is intentionally uncompleted and is not a valid assessment. Do not confuse packaging tests with approval, reasoning evaluation or tenant acceptance. Generated assessment outputs remain separate draft records. No raw evidence is copied into exports by default.
