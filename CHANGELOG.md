# Changelog
## Unreleased
HTML output: the assessment is now one self-contained `[project]-rai-assessment.html` built from `assets/output.template.html`, which renders the embedded JSON record and policy-pack snapshot (the template is now data-driven and has no sample content). It replaces `assessment.json`, `assessment-report.md`, the `policy-pack.json` snapshot and `assets/report.template.md`. The page has a button to download the embedded JSON.

Slash command: removed `.github/prompts/responsible-ai-assessment.prompt.md`, which only worked when this repo was the open workspace and duplicated the skill name. `SKILL.md` is now invoked directly via `/responsible-ai-assessment` (added `argument-hint` and `user-invocable`). `build-zip.ps1` now wraps files in a `responsible-ai-assessment/` folder so the folder name matches the skill name without manual renaming.

Unavailable information: questions are asked once. Only the acknowledgement, authorisation/handling, a valid policy pack and project identity/purpose still pause the run. Anything the user says they do not have is logged in a new required `assumptions_and_gaps` array (schema, template, reference 02 gap protocol, reference 09 checks) and shown as an Assumptions and gaps section in the report, with conservative defaults (absent evidence is Not evidenced, unknown applicability stays Applicable).
Added Step 0 to the assessment process: before any assessment work, the user must accept responsibility for the output (as guidance, not certification or approval) and type an email address in valid format as confirmation. The email is not stored or recorded; declining leaves the status `Not started - acknowledgement not given`. Updated SKILL.md, references 02, the intake template and the prompt file.

Removed the Python helper, its tests and the `jsonschema` dependency. Pack validation, rule lookup, report generation and output validation are now model-performed checklists (references 03, 06 and 09). Output is saved as separate files rather than a checksummed ZIP, and SHA-256 hashes are recorded as `Not computed` unless the host can verifiably compute them.

## 0.1.0 - 2026-10-30
Initial packageable implementation draft derived from supplied agent and MVP v2.0. Policy pack remains blocked pending approved content. Added progressive references, templates, schemas, offline helper, technical tests and release questions. No operational approval claimed.
