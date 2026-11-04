# Changelog
## Unreleased
Added Step 0 to the assessment process: before any assessment work, the user must accept responsibility for the output (as guidance, not certification or approval) and type an email address in valid format as confirmation. The email is not stored or recorded; declining leaves the status `Not started - acknowledgement not given`. Updated SKILL.md, references 02, the intake template and the prompt file.

Removed the Python helper, its tests and the `jsonschema` dependency. Pack validation, rule lookup, report generation and output validation are now model-performed checklists (references 03, 06 and 09). Output is saved as separate files rather than a checksummed ZIP, and SHA-256 hashes are recorded as `Not computed` unless the host can verifiably compute them.

## 0.1.0 - 2026-10-30
Initial packageable implementation draft derived from supplied agent and MVP v2.0. Policy pack remains blocked pending approved content. Added progressive references, templates, schemas, offline helper, technical tests and release questions. No operational approval claimed.
