# Changelog
## Unreleased
Removed the Python helper, its tests and the `jsonschema` dependency. Pack validation, rule lookup, report generation and output validation are now model-performed checklists (references 03, 06 and 09). Output is saved as separate files rather than a checksummed ZIP, and SHA-256 hashes are recorded as `Not computed` unless the host can verifiably compute them.

## 0.1.0 - 2026-10-30
Initial packageable implementation draft derived from supplied agent and MVP v2.0. Policy pack remains blocked pending approved content. Added progressive references, templates, schemas, offline helper, technical tests and release questions. No operational approval claimed.
