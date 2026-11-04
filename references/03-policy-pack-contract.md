# Policy pack contract
Read `assets/public-sector-rai.json` and `assets/policy-pack.schema.json`. Validate the pack with the checklist below before any control assessment.
## Required metadata
Pack ID, version, status (Blocked, Draft, Approved), owner, jurisdiction, scope, effective date, review date, source records, approval records, controls and severity rules. Approval records distinguish policy and severity-rule approval. Approved packs require both, with named supplied approvers, dates and source decision locators. Review/effective dates are checked against runtime UTC date. A structurally valid pack can still be blocked or outside its validity window.
## Control contract
Each control has ID, title, domain, mandatory/high-impact flags, mandatory-requirement/guidance distinction, source ID and locator, applicability rule, expected evidence, criteria for every evidence status, and rule IDs. Source records contain title, version/date and a supplied locator. A URL is a locator, not permission to retrieve it. Provide approved source extracts or authorised readable source artefacts when interpretation requires them. Never manufacture quotations or claim the underlying standard has been inspected from a title alone.
## Executable rule subset
Rules have ID, control ID, exact evidence-status predicate, severity (Critical/High/Medium/Low/None), hard-gate result (Triggered/Not triggered/Not applicable) and explicit rationale. Exactly one rule must match each control/status combination. No precedence guessing. This deliberately small rule model supports only evidence-status predicates. If the approved rules depend on other facts, stop and request an explicitly reviewed extension of the rule model and schema; never flatten them into invented thresholds. A missing or ambiguous match returns Unassigned, never a guess.

## Pack validation checklist
The model performs this by reading the pack; it is not executable validation. Any failure means the pack is invalid and assessment stops.
1. The pack follows `assets/policy-pack.schema.json`.
2. Status is not Blocked. Owner, jurisdiction and scope are supplied (not blank, TBC, Not supplied or Unknown).
3. Effective and review dates are present, and today falls between them.
4. Source, control and rule IDs are unique, and at least one source and one control exist.
5. An Approved pack records an approval for both "Policy" and "Severity rules", each with an approver and decision locator.
6. Every control names an existing source, has expected-evidence criteria, and lists no duplicate rule IDs.
7. Every rule a control lists exists and belongs to that control. No rule is orphaned (unlisted by its control).
8. For every control, exactly one listed rule applies to each of the five evidence statuses: Supported, Partly supported, Not evidenced, Conflicting evidence, Not assessed.
9. A rule with hard gate Triggered has a severity other than None.
## Release and design-test modes
The shipped Blocked scaffold has no controls or rules. It is a packaging artefact, not a baseline. A completed Draft pack requires explicit design-test authorisation recorded in the run; outputs remain labelled unapproved. Approved assessment requires approved metadata, applicable scope and human confirmation. Never upgrade a draft by user request alone without recorded approval evidence.
Changes require specialist impact review, manual version release notes, approval and a comparability decision. Preserve the previous version. Do not retrospectively change results; create a new assessment.
