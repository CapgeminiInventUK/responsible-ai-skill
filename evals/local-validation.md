# Local technical validation

Executed 30 October 2026 in the build environment. 18 synthetic technical tests passed. The shipped policy scaffold was separately confirmed to fail operational validation as intended. No model assessment evaluation, policy approval or target-Claude-environment acceptance was performed.

```text
test_ambiguous_rule (test_rai_tool.Tests.test_ambiguous_rule) ... ok
test_approval_missing (test_rai_tool.Tests.test_approval_missing) ... ok
test_blocked_pack (test_rai_tool.Tests.test_blocked_pack) ... ok
test_closure_blocked (test_rai_tool.Tests.test_closure_blocked) ... ok
test_cross_project (test_rai_tool.Tests.test_cross_project) ... ok
test_draft_authorisation (test_rai_tool.Tests.test_draft_authorisation) ... ok
test_duplicate_ids (test_rai_tool.Tests.test_duplicate_ids) ... ok
test_exclusion (test_rai_tool.Tests.test_exclusion) ... ok
test_export (test_rai_tool.Tests.test_export) ... ok
test_human_closure (test_rai_tool.Tests.test_human_closure) ... ok
test_missing_control (test_rai_tool.Tests.test_missing_control) ... ok
test_question (test_rai_tool.Tests.test_question) ... ok
test_references (test_rai_tool.Tests.test_references) ... ok
test_rule_tamper (test_rai_tool.Tests.test_rule_tamper) ... ok
test_score_rejected (test_rai_tool.Tests.test_score_rejected) ... ok
test_unknown_citation (test_rai_tool.Tests.test_unknown_citation) ... ok
test_unreviewed_citation (test_rai_tool.Tests.test_unreviewed_citation) ... ok
test_valid (test_rai_tool.Tests.test_valid) ... ok

----------------------------------------------------------------------
Ran 18 tests in 3.010s

OK
```
