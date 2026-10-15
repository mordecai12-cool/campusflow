# CampusFlow submission links and verified evidence

Prepared from the complete Fellows' Engineering Guide. The application is
published at Michael's explicit request. Genuine reviewed contributions and
individual learning evidence remain outstanding for assessment completion.

Repository main: https://github.com/mordecai12-cool/campusflow2/tree/main
Engineer A's existing PR: https://github.com/mordecai12-cool/campusflow2/pull/1
Engineer B's integration PR: https://github.com/mordecai12-cool/campusflow2/pull/2
Actual campus source integration: https://github.com/mordecai12-cool/campusflow2/pull/8
Follow-up refactor awaiting review: https://github.com/mordecai12-cool/campusflow2/pull/9

## Verification snapshots

| Snapshot | Unittest result | Extra contract checks | Scope |
| --- | --- | --- | --- |
| Baseline main: 3f068e38d4bf478033415c79b22e18ea11275093 | 15 passed | 2 passed, 5 failed | Historical baseline before PR #2 |
| PR #2 source: daf51ad581bb8fe3e76d3107a38c0f1bdc8288e3 | 66 passed | 7 passed | Merged as 7fa245cf13e8567557f3dbd9e5cdec8aa9b38b18; merged main also tested successfully |
| Actual campus source integration | 95 passed | 7 passed | Includes actual engineer folders, compatible original API and mixed-API persistence test |
| Proposed ID/lifecycle refactor: af1f19a2071d566c2e29eacb9d885101f9b506f5 | 97 passed | 7 passed | PR proposal; requires actual partner approval before merge |

The assistant actually ran these commands. Evidence: [main test output](main-test-output.txt),
[branch test output](test-output.txt), [main contract checks](main-contract-checks.txt),
[branch contract checks](integration-contract-checks.txt), [demo output](demo-output.txt).
Syntax checks also passed. See [source mapping](source-integration.md),
[copied-file hashes](campus-source-manifest.json) and
[combined-source test evidence](source-integration-test-output.txt).
The [source-integration PR discussion](https://github.com/mordecai12-cool/campusflow2/pull/8)
records the final published main SHA
and actual post-merge output; GitHub Actions also verifies published main.
Current refactor evidence is in [refactor-test-output.txt](refactor-test-output.txt).
The published main SHA remains 28ad65a106e8e90bbd666f426ab05aff8271e524
until a new approved merge. See [review-ready.md](review-ready.md) for the
remaining human steps and [contribution-provenance.md](contribution-provenance.md)
for the actual source history.

## Guide requirements and remaining actions

| Area | Marks | Verified preparation | Required completion |
| --- | --- | --- | --- |
| Functional implementation | 40 | Combined application implements F1-F7 and fixes reproduced baseline defects | Both fellows demonstrate the published app from main |
| Testing and reliability | 15 | 95 combined tests; snapshot outputs and independent probes recorded | Preserve actual final-main output and demonstrate independent verification |
| Professional Git workflow | 20 | Both PR links and original authors are verified | Genuine code/test PR per fellow; two substantive cross-review observations each; final approval before merge |
| AI-native engineering | 20 | Existing logs retained; assistant executions and authorship disclosed | Three actual interactions per fellow, independent results, and a verified correction/improvement/rejection each |
| Technical defence | 5 | README, contracts, demo and defence prompts available | Both fellows explain their work and demonstrate it together |

PR #1 is already merged without recorded review and changes only cache files.
Do not describe retrospective comments as approval before merge. Mordecai
needs a genuine application-and-test PR for his reviewed contribution.
PR #2 was merged at Michael's explicit request with no recorded partner
approval; this does not complete the guide's review requirement. Michael's AI-assisted work
must be distinguished from his personally written code and tests.

The five contracts are documented in design-decisions.md; neither fellow's
actual agreement is asserted. Personal prompts, independent experiments and
actual agreement details have been requested in chat and remain pending.

## Finish in this order

1. Both fellows supply actual contribution and learning evidence and discuss
   the five documented contracts. Record the real date and decisions.
2. Both fellows complete genuine application-and-test improvements from
   updated main on their own issue branches and author their own PRs.
3. Each reviews the other's actual diff and checks, leaves at least two
   substantive observations, requests fixes if needed and approves satisfactory
   final changes before merge. Historical publication cannot be backdated
   as reviewed work. No fellow approves their own PR.
4. Merge the approved contribution. Fetch final main into a clean checkout,
   record `git rev-parse HEAD`, run `python3 -m unittest discover -s . -t . -v`,
   syntax checks and `python3 run.py --demo`. Retain actual results.
5. Update this packet with the final main SHA, results and both qualifying
   reviewed PR links. Submit those links and demonstrate both contributions.

No historical commits, individual experiments, reviews or signatures are
fabricated by this packet. miikese/campusflow remains the reference repository.
