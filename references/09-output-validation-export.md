# Output, validation and export
Canonical record: `assets/assessment.template.json`, structured per `assets/assessment.schema.json` (use the schema as the field and value reference) and checked with the manual checklist below. Report: a single HTML file built from `assets/output.template.html` that renders only that embedded record. Questions: `assets/open-questions.md` for paused intake and the canonical array for assessments. Never hand-maintain a second conflicting register.
## Package contents
One file, `[project]-rai-assessment.html`, saved to the output location the user approved, never inside the skill folder. `[project]` is the project name in lowercase with runs of non-alphanumeric characters replaced by a single hyphen (for example `farm-funding-assistant-rai-assessment.html`); use the project ID if the name is unavailable. It contains the full record (run metadata, manifest, results, concerns/actions, decisions, questions, assumptions and gaps, comparison and limitations) and the baseline pack snapshot. Do not create a ZIP or checksum manifest unless the host can do so verifiably. Raw evidence is not included by default. The user controls saving and sharing. The file is an assessment record, not a workspace update.

## Report generation
Copy `assets/output.template.html` unchanged except for the two placeholders: replace `{{ASSESSMENT_JSON}}` with the completed `assessment.json` content and `{{POLICY_PACK_JSON}}` with the pack content, each as compact valid JSON. Escape every `<` in the JSON as `\u003c`. Do not edit the markup, styles or script, and do not add or alter findings; the page derives all counts, tables and filters from the JSON. Open or re-read the saved file and confirm both blocks parse and no `{{` placeholder remains. The page includes the `assumptions_and_gaps` section, so every gap logged during the run must be in the record.

## Identifiers and hashes
Run ID format: `RUN-` followed by the UTC date and time (`YYYYMMDD-HHMMSS`) and four random characters. Without code execution, record SHA-256 as `Not computed` and never estimate or invent a hash. Compute one only if the host provides a tool that actually returns it. Record this as a limitation.
## Completion
Complete means processing finished, all controls have results, and no blocking questions, pending applicability or applicable Not assessed controls remain. It does not mean controls are supported, concerns are closed or approval is granted. Partial means some valid results exist but coverage/decisions remain incomplete. Failed means the assessment could not be performed or a valid package could not be produced. An intake blocked before a usable baseline should produce only the questions artefact, not a purported validated assessment.
## Checks
Validation is performed by the model re-reading the finished record. It is not executable validation and can miss errors; say so in the summary and the limitations. Work through every item, record any failure, fix it and re-check from the start:
1. Every field in the schema is present with an allowed value; no extra scores, ratings or trust labels.
2. IDs are unique within each list (evidence, controls, concerns, decisions, questions, gaps).
3. Every reference (evidence, control, concern, decision IDs) points to an existing record, and every citation points to evidence that was Reviewed or Partly reviewed.
4. Every pack control has exactly one control result, and the evidence manifest is not empty.
5. Required intake fields are confirmed (not blank, TBC, Not supplied or Unknown), including assessor independence, and project IDs match throughout.
6. Pack ID, version and status match the pack; the baseline label is "Design test - unapproved baseline" for a Draft pack (with recorded design-test authorisation) or "Approved baseline - draft assessment" for an Approved pack.
7. For each Applicable control, severity, rule ID and hard gate equal the pack rule for its evidence status (see reference 06). Supported, Partly supported and Conflicting evidence need citations. Any non-None severity or Triggered gate has a linked concern.
8. Pending review or Not applicable controls are Not assessed, severity None, rule ID null and hard gate Not applicable. Not applicable on a mandatory or high-impact control needs a linked human decision of kind Applicability exception.
9. Each concern copies its control's severity, rule ID and hard gate, and has evidence references or an explicit evidence gap.
10. A Closed concern has closure evidence (Reviewed or Partly reviewed), all of it listed in the linked human Closure decision, which names a decision maker and authority.
11. Resolved questions have an answer. Complete status means no open blocking questions and no Pending review or Not assessed Applicable controls.
12. Compared mode records the previous run ID.
13. The HTML file contains the complete record: both JSON blocks parse, no `{{` placeholder remains, and the record has the same content as the validated `assessment.json`.
14. Every user statement of unavailable information or resources during the run has an `assumptions_and_gaps` entry with unique ID, type, handling and affected controls, and none was re-asked.

Review source citations and evidence interpretations manually; this checklist cannot establish their truth. If the host cannot save files, say so and ask for an approved output alternative. Formats and limits are local implementation choices until tested in the selected environment.
Generated records remain drafts for human review. Summarise project/time/pack, coverage, severity counts, hard gates, material questions and processing limits. No trust label, compliance certificate, deployment recommendation or model sign-off.
