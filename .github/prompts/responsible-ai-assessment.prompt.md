---
name: responsible-ai-assessment
description: Run a bounded Responsible AI evidence assessment for one project against the bundled public sector policy pack.
argument-hint: "Project ID/name, AI purpose, lifecycle stage and the evidence files or paths to review"
agent: agent
---

Run the Responsible AI assessment defined in [SKILL.md](../../SKILL.md) for the request that follows this command.

Rules for this run:

1. Read [SKILL.md](../../SKILL.md) first, then load only the numbered reference from its References table that the current step needs. Reference paths are relative to the repository root (`references/`, `assets/`, `scripts/`).
2. Use the user's message after `/responsible-ai-assessment` as the project context and evidence boundary. Ask focused questions for any required input that is missing (see the stop-and-ask rule in SKILL.md) before processing evidence.
3. Use the schemas and checklists in the skill's references; there are no scripts to run. Do not invent results, hashes or validation you did not actually perform.
4. Write outputs only to the location the user approves. Do not modify source evidence, and do not claim approval, compliance certification, or saving to a repository.
