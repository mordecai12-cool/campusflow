# Actual campus source integration

Michael asked to combine the work in /home/student/campus with Mordecai's
project. The actual working-tree files, including the local ownership-folder
reorganization and one-pass report refactor, are now copied into this repo.
The original local workspace and Mordecai's repository history are preserved.
Publication PR: https://github.com/mordecai12-cool/campusflow2/pull/8.

| Local campus source | Combined application |
| --- | --- |
| engineer_a/tickets.py | Same ownership path; shared creation, validation, priority, IDs and queries |
| engineer_b/workflow.py | Same ownership path; shared assignment, transitions, reopening and queue |
| engineer_b/reports.py | Same ownership path; one-pass complete counts |
| Both engineer test folders | Same ownership paths; original local matching tests retained |
| main.py | Copied CLI directly uses the engineer modules |
| campusflow/storage.py and campusflow/demo.py | Copied persistence and demo use those same modules |

The original campusflow/tickets.py, workflow.py and reports.py import or adapt
the ownership modules. Mordecai's original API remains available: create_ticket
keeps its list-last argument and workflow functions accept a stored record.
There is one implementation of each business rule. Both interfaces work on
the same collection; no separate collections or duplicated runtime state exist.

Adaptations: the resolved-reassignment message retains the wording checked by
the existing CLI test; storage trailing whitespace is removed; the copied
Engineer B walkthrough links to this integration record. The source manifest
records original and destination hashes and whether each file was adapted.
No runtime ticket data, bytecode, secrets or another repository's Git directory
are copied. Existing personal learning entries and commit history remain intact.

Validation: 95 tests pass: 66 existing tests through the compatibility API,
28 copied ownership tests, and one new test exercising both APIs together
through lifecycle, reports, save and reload. Root-level unittest discovery and
CI include all three groups. The seven requirement probes, syntax checks and
the temporary-data demo also pass. See source-integration-test-output.txt.

PR #2 was first merged at Michael's explicit request after successful checks;
the direct source-folder integration follows on an issue-linked branch.
Assistant-authored code and tests remain disclosed as such. Actual partner
review, independently written contributions and personal learning evidence
are still outstanding under the guide. Publication is not peer approval.

The copied-file manifest describes the import snapshot; later changes are
tracked by Git. The proposed follow-up refactor adds two regression tests,
bringing its branch suite to 97, and changes the canonical helpers while
preserving both APIs. See refactor-test-output.txt and review-ready.md.
